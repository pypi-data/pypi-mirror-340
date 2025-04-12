from typing import Any
import httpx
import os
import logging
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("flyder")

# Constants
FLYDER_API_BASE = "https://flyder.ai/api"
USER_AGENT = "flyder-app/1.0"


async def api_request(url: str, method: str = "GET", data: dict[str, Any] | None = None) -> dict[str, Any] | None:
    """Make a request to the Flyder API with proper error handling."""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json",
        "User-Email": os.getenv("FLYDER_EMAIL", ""),
        "Authorization": f"Bearer {os.getenv('FLYDER_API_KEY', '')}"
    }
    async with httpx.AsyncClient() as client:
        try:
            if method.upper() == "GET":
                response = await client.get(url, headers=headers, timeout=30.0)
            elif method.upper() == "POST":
                response = await client.post(url, headers=headers, json=data, timeout=30.0)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logging.error(f"Error making request to {url}: {e}")
            return None


@mcp.tool(
    name="List-Workflows-Tool",
    description="Tool that returns the list of workflows belonging to the user.",
)
async def list_workflows() -> list[dict[str, Any]]:
    """
    Get a list of workflows that belong to the user. This returns a dictionary that has workflow names and their IDs.
    The IDs can later be used to run a specific workflow.

    Returns:
        list[dict[str, Any]]: A list of dictionaries containing workflow names and their IDs.
    """
    url = f"{FLYDER_API_BASE}/workflow/list"
    data = await api_request(url)

    if not data or not isinstance(data, list):
        logging.error("Unable to fetch workflows or invalid response format.")
        return []

    # Ensure each item in the list is a dictionary with an "id" key
    workflows = [workflow for workflow in data if isinstance(workflow, dict) and "id" in workflow]

    if not workflows:
        logging.info("No saved workflows were found.")
        return []

    return workflows


@mcp.tool(
    name="Run-Workflow-By-Id-Tool",
    description="Tool that runs a specific workflow with the associated ID.",
)
async def run_workflow_by_id(workflow_id: int, input: str = None) -> dict[str, Any]:
    """
    Run a specific workflow using its ID.

    Args:
        workflow_id (int): The ID of the workflow to run.
        input (str, optional): The input text to be passed to the workflow. If not provided, the default input from the workflow will be used.

    Returns:
        dict[str, Any]: A dictionary containing the result of the workflow run.
    """
    details_url = f"{FLYDER_API_BASE}/workflow/details/{workflow_id}"
    data = await api_request(details_url)
    if not data or not isinstance(data, dict):
        logging.error("Unable to fetch workflow details or invalid response format.")
        return {}
    
    url = f"{FLYDER_API_BASE}/workflow/run/{workflow_id}"
    
    if not input:
        input = data.get("input_text", "")
    
    payload = {"input": input}
    payload["uuid"] = os.urandom(16).hex()
    data = await api_request(url, method="POST", data=payload)

    if not data or not isinstance(data, dict):
        logging.error("Unable to run workflow or invalid response format.")
        return {}

    return data

if __name__ == "__main__":
    mcp.run(transport='stdio')