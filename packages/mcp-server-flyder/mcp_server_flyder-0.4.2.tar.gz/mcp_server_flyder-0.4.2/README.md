# mcp-server-flyder
MCP Server for Flyder

# mcp-server-flyder: MCP Server for Flyder

## Overview

A Model Context Protocol server for Flyder workflow integration.

Please note that mcp-server-flyder is currently in early development. The functionality and available tools are subject to change as we continue to develop and improve the server.

### Tools

1. `list_workflows`
   - Get a list of workflows that belong to the user. This returns a dictionary that has workflow names and their IDs.
   - Input:
     - none
   - Returns: A list containing workflow names and their IDs. The IDs can later be used to run a specific workflow.

2. `run_workflow_by_id`
   - Run a specific workflow using its ID.
   - Input:
     - `workflow_id` (int): The ID of the workflow to run.
     - `input` (str, optional): The input text to be passed to the workflow. If not provided, the default input from the workflow will be used.
   - Returns: An object containing the result of the workflow run.

## Installation

### Using uvx (recommended)

Using [`uv`](https://docs.astral.sh/uv/) no specific installation is needed. We will use [`uvx`](https://docs.astral.sh/uv/guides/tools/) to directly run *mcp-server-flyder*.

## Configuration

### Usage with Claude Desktop

Add this to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "flyder": {
      "command": "uvx",
      "args": [ 
        "mcp_server_flyder"
      ],
      "env": {
        "FLYDER_EMAIL": "<email used to sign up on Flyder>",
        "FLYDER_API_KEY": "<your Flyder API key>"
      }
    }
  }
}
```

## Debugging

You can use the MCP inspector to debug the server. 

```
cd path/to/repo
npx @modelcontextprotocol/inspector uv run mcp-server-flyder
```

Running `tail -n 20 -f ~/Library/Logs/Claude/mcp*.log` will show the logs from the server and may
help you debug any issues.

## Development

If you are doing local development, there are two ways to test your changes:

1. Run the MCP inspector to test your changes. See [Debugging](#debugging) for run instructions.

2. Test using the Claude desktop app. Add the following to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "flyder": {
      "command": "uv",
      "args": [ 
        "--directory",
        "/<path to repo>",
        "run",
        "mcp-server-flyder"
      ],
      "env": {
        "FLYDER_EMAIL": "<email used to sign up on Flyder>",
        "FLYDER_API_KEY": "<your Flyder API key>"
      }
    }
  }
}
```


## License

This MCP server is licensed under the GNU General Public License. This means you are free to use, modify, and distribute the software, subject to the terms and conditions of the GNU License. For more details, please see the LICENSE file in the project repository.