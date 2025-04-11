# mcp-server-hai

A MCP server implementation for HAI (Hyper Application Inventor) services

## Installation

```bash
uv pip install mcp-server-hai
```

## Usage

Run the server:
```bash
uv run mcp-server-hai
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
uv pip install -e .[dev]
```

## Publishing

Build and publish to PYPI:
```bash
uv pip install build twine
uv run python -m build
uv run twine upload dist/*
