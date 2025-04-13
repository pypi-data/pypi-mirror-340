# AWS Amplify Gen 2 Documentation MCP Server

Model Context Protocol (MCP) server for AWS Amplify Gen 2 Documentation

This MCP server provides tools to access AWS Amplify Gen 2 documentation and search for content.

## Features

- **Read Documentation**: Fetch and convert AWS Amplify Gen 2 documentation pages to markdown format
- **Search Documentation**: Search AWS documentation using the official search API

## Prerequisites

### Installation Requirements

1. Install `uv` from [Astral](https://docs.astral.sh/uv/getting-started/installation/) or the [GitHub README](https://github.com/astral-sh/uv#installation)
2. Install Python 3.13 or newer using `uv python install 3.13` (or a more recent version)

## Installation

To add this MCP server to your Amazon Q or Claude, add the following to your MCP config file. With Amazon Q, create (if does not yet exist) a file named `.amazonq/mcp.json` under the same directory that is running `q chat`. Then add the following config:

```json
{
  "mcpServers": {
    "unirt.amplify-doc-mcp-server": {
        "command": "uvx",
        "args": ["unirt.amplify-doc-mcp-server@latest"],
        "env": {
          "FASTMCP_LOG_LEVEL": "ERROR"
        },
        "disabled": false,
        "autoApprove": []
    }
  }
}
```

## Basic Usage

Example:

- "How can I create custom resources in Amplify Gen 2? Please provide a detailed explanation based on the documentation."
- "Please explain the permission configuration details in Amplify Gen2 based on the documentation."

## Tools

### read_amplify_documentation

Fetches an AWS Amplify Gen 2 documentation page and converts it to markdown format.

```python
read_amplify_documentation(url: str, max_length: int = 10000, start_index: int = 0) -> str
```

### search_amplify_documentation

Searches AWS Amplify Gen 2 documentation using the official AWS Amplify Gen 2 Documentation Search API (Algolia).

```python
search_amplify_documentation(search_phrase: str, platform: Optional[str], limit: int) -> list[dict]
```
