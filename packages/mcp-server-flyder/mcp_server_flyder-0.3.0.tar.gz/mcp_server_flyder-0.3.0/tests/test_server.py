import os
import pytest
from unittest.mock import AsyncMock, patch, MagicMock

from mcp_server_flyder.server import (
    api_request, 
    list_workflows, 
    run_workflow_by_id, 
    FLYDER_API_BASE
)

TEST_API_BASE = "https://example.com/api"

@pytest.fixture
def mock_env_variables():
    """Set up mock environment variables for testing."""
    with patch.dict(os.environ, {
        "FLYDER_EMAIL": "test@example.com",
        "FLYDER_API_KEY": "test-api-key"
    }):
        yield

@pytest.fixture
def mock_httpx_client():
    """Mock the httpx.AsyncClient."""
    with patch("httpx.AsyncClient") as mock_client:
        client_instance = AsyncMock()
        mock_client.return_value.__aenter__.return_value = client_instance
        yield client_instance


class TestApiRequest:
    @pytest.mark.asyncio
    async def test_api_request_get_success(self, mock_env_variables, mock_httpx_client):
        """Test successful GET request."""
        # Setup
        mock_response = MagicMock()
        mock_response.raise_for_status = MagicMock()
        mock_response.json.return_value = {"success": True, "data": "test-data"}
        mock_httpx_client.get = AsyncMock(return_value=mock_response)
        
        # Execute
        result = await api_request(f"{TEST_API_BASE}/test")
        
        # Assert
        mock_httpx_client.get.assert_called_once()
        assert result == {"success": True, "data": "test-data"}
    
    @pytest.mark.asyncio
    async def test_api_request_post_success(self, mock_env_variables, mock_httpx_client):
        """Test successful POST request."""
        # Setup
        mock_response = MagicMock()
        mock_response.raise_for_status = MagicMock()
        mock_response.json.return_value = {"success": True, "data": "test-data"}
        mock_httpx_client.post = AsyncMock(return_value=mock_response)
        
        # Execute
        result = await api_request(
            f"{TEST_API_BASE}/test", 
            method="POST", 
            data={"key": "value"}
        )
        
        # Assert
        mock_httpx_client.post.assert_called_once()
        assert result == {"success": True, "data": "test-data"}
    
    @pytest.mark.asyncio
    async def test_api_request_invalid_method(self, mock_env_variables, mock_httpx_client):
        """Test invalid HTTP method."""
        # Execute
        result = await api_request(f"{TEST_API_BASE}/test", method="DELETE")
        
        # Assert
        assert result is None
    
    @pytest.mark.asyncio
    async def test_api_request_exception_handling(self, mock_env_variables, mock_httpx_client):
        """Test exception handling in API request."""
        # Setup - AsyncMock with side_effect for proper awaiting
        mock_httpx_client.get = AsyncMock(side_effect=Exception("Test exception"))
        
        # Execute
        result = await api_request(f"{TEST_API_BASE}/test")
        
        # Assert
        assert result is None


class TestListWorkflows:
    @pytest.mark.asyncio
    async def test_list_workflows_success(self):
        """Test successful workflow listing."""
        # Setup
        mock_workflows = [
            {"id": 1, "name": "Test Workflow 1"},
            {"id": 2, "name": "Test Workflow 2"}
        ]
        
        with patch("mcp_server_flyder.server.api_request", new_callable=AsyncMock) as mock_request:
            mock_request.return_value = mock_workflows
            
            # Execute
            result = await list_workflows()
            
            # Assert
            mock_request.assert_called_once_with(f"{FLYDER_API_BASE}/workflow/list")
            assert result == mock_workflows
    
    @pytest.mark.asyncio
    async def test_list_workflows_empty(self):
        """Test empty workflow list."""
        # Setup
        with patch("mcp_server_flyder.server.api_request", new_callable=AsyncMock) as mock_request:
            mock_request.return_value = []
            
            # Execute
            result = await list_workflows()
            
            # Assert
            assert result == []
    
    @pytest.mark.asyncio
    async def test_list_workflows_invalid_format(self):
        """Test invalid response format."""
        # Setup
        with patch("mcp_server_flyder.server.api_request", new_callable=AsyncMock) as mock_request:
            mock_request.return_value = {"not_a_list": True}
            
            # Execute
            result = await list_workflows()
            
            # Assert
            assert result == []
    
    @pytest.mark.asyncio
    async def test_list_workflows_api_failure(self):
        """Test API request failure."""
        # Setup
        with patch("mcp_server_flyder.server.api_request", new_callable=AsyncMock) as mock_request:
            mock_request.return_value = None
            
            # Execute
            result = await list_workflows()
            
            # Assert
            assert result == []

class TestRunWorkflowById:
    @pytest.mark.asyncio
    async def test_run_workflow_success(self):
        """Test successful workflow run."""
        # Setup
        workflow_id = 123
        workflow_details = {
            "id": workflow_id,
            "name": "Test Workflow",
            "input_text": "default input"
        }
        workflow_result = {
            "success": True,
            "output": "Test output"
        }
        
        with patch("mcp_server_flyder.server.api_request", new_callable=AsyncMock) as mock_request:
            # Use side_effect for sequential return values
            mock_request.side_effect = [
                workflow_details,  # First call to get details
                workflow_result    # Second call to run workflow
            ]
            
            # Execute
            result = await run_workflow_by_id(workflow_id, "custom input")
            
            # Assert
            assert mock_request.call_count == 2
            assert mock_request.call_args_list[0].args[0] == f"{FLYDER_API_BASE}/workflow/details/{workflow_id}"
            assert mock_request.call_args_list[1].args[0] == f"{FLYDER_API_BASE}/workflow/run/{workflow_id}"
            assert mock_request.call_args_list[1].kwargs["method"] == "POST"
            assert mock_request.call_args_list[1].kwargs["data"] == {"input": "custom input"}
            assert result == workflow_result
    
    @pytest.mark.asyncio
    async def test_run_workflow_default_input(self):
        """Test workflow run with default input."""
        # Setup
        workflow_id = 123
        workflow_details = {
            "id": workflow_id,
            "name": "Test Workflow",
            "input_text": "default input"
        }
        workflow_result = {
            "success": True,
            "output": "Test output"
        }
        
        with patch("mcp_server_flyder.server.api_request", new_callable=AsyncMock) as mock_request:
            # Use side_effect for sequential return values
            mock_request.side_effect = [
                workflow_details,  # First call to get details
                workflow_result    # Second call to run workflow
            ]
            
            # Execute (no input provided)
            result = await run_workflow_by_id(workflow_id)
            
            # Assert
            assert mock_request.call_count == 2
            assert mock_request.call_args_list[1].kwargs["data"] == {"input": "default input"}
            assert result == workflow_result
    
    @pytest.mark.asyncio
    async def test_run_workflow_details_failure(self):
        """Test failure to fetch workflow details."""
        # Setup
        workflow_id = 123
        
        with patch("mcp_server_flyder.server.api_request", new_callable=AsyncMock) as mock_request:
            mock_request.return_value = None
            
            # Execute
            result = await run_workflow_by_id(workflow_id)
            
            # Assert
            mock_request.assert_called_once_with(f"{FLYDER_API_BASE}/workflow/details/{workflow_id}")
            assert result == {}
    
    @pytest.mark.asyncio
    async def test_run_workflow_execution_failure(self):
        """Test failure to execute workflow."""
        # Setup
        workflow_id = 123
        workflow_details = {
            "id": workflow_id,
            "name": "Test Workflow",
            "input_text": "default input"
        }
        
        with patch("mcp_server_flyder.server.api_request", new_callable=AsyncMock) as mock_request:
            # Use side_effect for sequential return values
            mock_request.side_effect = [
                workflow_details,  # First call to get details
                None               # Second call fails
            ]
            
            # Execute
            result = await run_workflow_by_id(workflow_id)
            
            # Assert
            assert mock_request.call_count == 2
            assert result == {}