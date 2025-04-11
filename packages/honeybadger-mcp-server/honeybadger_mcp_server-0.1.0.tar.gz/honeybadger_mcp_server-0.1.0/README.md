# honeybadger-mcp-server: A Honeybadger API MCP Server

## Overview

A Model Context Protocol server for interacting with the Honeybadger API. This server provides tools to query error details and fault information from your Honeybadger projects via Large Language Models.

Please note that honeybadger-mcp-server requires both a Honeybadger API key and Project ID to function. You can obtain these from your [Honeybadger account settings](https://app.honeybadger.io/users/edit).

### Tools

1. `list_faults`

   - List faults from Honeybadger with optional filtering
   - Inputs:
     - `q` (string, optional): A search string
     - `created_after` (number, optional): Unix timestamp (seconds since epoch)
     - `occurred_after` (number, optional): Unix timestamp (seconds since epoch)
     - `occurred_before` (number, optional): Unix timestamp (seconds since epoch)
     - `limit` (number, optional): Number of results to return (max and default are 25)
     - `order` (string, optional): Sort order ("recent" or "frequent", default: "recent")
   - Returns: List of faults matching the criteria

2. `get_fault_details`
   - Get detailed notice information for a specific fault
   - Inputs:
     - `fault_id` (string): The ID of the fault
     - `created_after` (number, optional): Unix timestamp (seconds since epoch)
     - `created_before` (number, optional): Unix timestamp (seconds since epoch)
     - `limit` (number, optional): Number of notices to return (max 25, default: 1)
   - Returns: Detailed fault notice information

## Installation

### Option 1: Install from PyPI (Recommended)

You can install using either `uv` (recommended) or `pip`:

```bash
# Using uv (recommended for better dependency management)
uv pip install honeybadger-mcp-server

# Or using pip
pip install honeybadger-mcp-server
```

After installation, you can run the server using either:

```bash
# Using uvx (recommended)
uvx honeybadger-mcp-server

# Or using python directly
python -m honeybadger_mcp_server
```

### Option 2: Local Development

For local development, clone this repository and install in development mode:

```bash
git clone https://github.com/yourusername/honeybadger-mcp
cd honeybadger-mcp

# Using uv (recommended)
uv pip install -e .

# Or using pip
pip install -e .
```

Then run using either:

```bash
# Using uv (recommended)
uv run --directory . -m honeybadger_mcp_server

# Or using python directly
python -m honeybadger_mcp_server
```

Note: While `uv` is recommended for better dependency management and isolation, the server will work with standard Python tools as well.

## Configuration

The server requires both a Honeybadger API key and Project ID to be set in the environment:

```bash
export HONEYBADGER_API_KEY="your-api-key-here"
export HONEYBADGER_PROJECT_ID="your-project-id-here"
```

### Usage with Claude Desktop

Add this to your `claude_desktop_config.json`:

#### If installed from PyPI:

```json
{
  "mcpServers": {
    "honeybadger": {
      "command": "uvx",
      "args": ["honeybadger-mcp-server"],
      "env": {
        "HONEYBADGER_API_KEY": "your-api-key-here",
        "HONEYBADGER_PROJECT_ID": "your-project-id-here"
      }
    }
  }
}
```

#### For local development:

```json
{
  "mcpServers": {
    "honeybadger": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "/path/to/honeybadger-mcp",
        "-m",
        "honeybadger_mcp_server"
      ],
      "env": {
        "HONEYBADGER_API_KEY": "your-api-key-here",
        "HONEYBADGER_PROJECT_ID": "your-project-id-here"
      }
    }
  }
}
```

### Usage with [Zed](https://github.com/zed-industries/zed)

Add to your Zed settings.json:

#### If installed from PyPI:

```json
"context_servers": {
  "honeybadger": {
    "command": {
      "path": "uvx",
      "args": ["honeybadger-mcp-server"],
      "env": {
        "HONEYBADGER_API_KEY": "your-api-key-here",
        "HONEYBADGER_PROJECT_ID": "your-project-id-here"
      }
    }
  }
}
```

#### For local development:

```json
"context_servers": {
  "honeybadger": {
    "command": {
      "path": "uv",
      "args": [
        "run",
        "--directory",
        "/path/to/honeybadger-mcp",
        "-m",
        "honeybadger_mcp_server"
      ],
      "env": {
        "HONEYBADGER_API_KEY": "your-api-key-here",
        "HONEYBADGER_PROJECT_ID": "your-project-id-here"
      }
    }
  }
}
```

## Debugging

You can use the MCP inspector to debug the server. For uvx installations:

```
npx @modelcontextprotocol/inspector uvx honeybadger-mcp-server
```

Or if you've installed the package in a specific directory or are developing on it:

```
cd path/to/servers/src/honeybadger
npx @modelcontextprotocol/inspector uv run honeybadger_mcp_server
```

Running `tail -n 20 -f ~/Library/Logs/Claude/mcp*.log` will show the logs from the server and may
help you debug any issues.

## Development

If you are doing local development, you can test your changes using the MCP inspector:

```bash
# From your project directory
npx @modelcontextprotocol/inspector -- uv run --directory . -m honeybadger_mcp_server
```

Running `tail -n 20 -f ~/Library/Logs/Claude/mcp*.log` will show the logs from the server and may
help you debug any issues.

## Docker Support

The MCP server can be run in a Docker container. This provides an isolated environment and makes deployment easier.

### Building the Docker Image

```bash
# Build the image
docker build -t honeybadger-mcp-server .
```

### Running with Docker

```bash
# Run the container with your Honeybadger credentials
docker run \
  -e HONEYBADGER_API_KEY=your_api_key_here \
  -e HONEYBADGER_PROJECT_ID=your_project_id_here \
  honeybadger-mcp-server

# Run with custom verbosity level
docker run \
  -e HONEYBADGER_API_KEY=your_api_key_here \
  -e HONEYBADGER_PROJECT_ID=your_project_id_here \
  honeybadger-mcp-server --verbose

# Run in detached mode
docker run -d \
  -e HONEYBADGER_API_KEY=your_api_key_here \
  -e HONEYBADGER_PROJECT_ID=your_project_id_here \
  honeybadger-mcp-server
```

### Environment Variables

The Docker container accepts the following environment variables:

- `HONEYBADGER_API_KEY` (required): Your Honeybadger API key
- `HONEYBADGER_PROJECT_ID` (required): Your Honeybadger Project ID

### Docker Best Practices

1. Never commit your API key or Project ID in the Dockerfile or docker-compose files
2. Use environment files or secure secrets management for sensitive credentials
3. Consider using Docker health checks in production
4. The container runs as a non-root user for security

## License

This MCP server is licensed under the MIT License. This means you are free to use, modify, and distribute the software, subject to the terms and conditions of the MIT License. For more details, please see the LICENSE file in the project repository.
