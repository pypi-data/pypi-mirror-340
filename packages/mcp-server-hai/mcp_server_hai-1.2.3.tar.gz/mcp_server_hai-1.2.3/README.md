# mcp-server-hai

A MCP server implementation for Tencent HAI (Hyper Application Inventor) services

## Installation

### Cline
if you are using cline, no installation is needed, the installation is automatically executed by uvx.

### Local install
```bash
uv init example-project # init your project
uv add mcp-server-hai # download and install the package on PYPI
uv run mcp-server-hai # run the package
```


## Usage

### Using in Cline
open your cline setting file: `cline_mcp_setting.json`

add mcp-server-hai configuration to mcpServers as follows:
```json
{
    "mcpServers": {
      "mcp-server-hai": {
        "command": "uvx",
        "args": [
          "mcp-server-hai@latest" // make sure you have installed the latest version, to use a specific version, use mcp-server-hai@version instead
        ],
        "env": {
          "TENCENTCLOUD_SECRET_ID": "YOUR_SECRET_ID_HERE",
          "TENCENTCLOUD_SECRET_KEY": "YOUR_SECRET_KEY_HERE"
        },
        "transportType": "stdio"
      }
    }
  }
```


Then you can find the mcp server named mcp-server-hai in cline, enjoy ;)

### Directly run the server

```bash
uvx mcp-server-hai
```

Environment variables required:
- TENCENTCLOUD_SECRET_ID: Your Tencent Cloud secret ID
- TENCENTCLOUD_SECRET_KEY: Your Tencent Cloud secret key

## Features

- Create, start, stop and remove HAI instances
- Query instance information and network status
- Get available regions and instance types

## Development

Install development dependencies:
```bash
uv sync
```

## Publishing
Build and publish to PYPI:
```bash
uv add build twine
uv run python -m build
uv run twine upload dist/*
