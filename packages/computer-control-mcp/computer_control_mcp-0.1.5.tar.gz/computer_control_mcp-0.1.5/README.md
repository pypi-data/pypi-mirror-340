# Computer Control MCP

A Python package that provides computer control capabilities using PyAutoGUI through a Model Context Protocol (MCP) server.

## Quick Usage (MCP Setup Using `uvx`)

```json
{
  "mcpServers": {
    "computer-control-mcp": {
      "command": "uvx",
      "args": ["computer-control-mcp"]
    }
  }
}
```

## Features

- Control mouse movements and clicks
- Type text at the current cursor position
- Take screenshots of the entire screen or specific windows with optional saving to downloads directory
- List and activate windows
- Press keyboard keys
- Drag and drop operations

### Running as a Module

You can run the package as a module:

```bash
python -m computer_control_mcp
```

## Development

### Setting up the Development Environment

```bash
# Clone the repository
git clone https://github.com/yourusername/computer-control-mcp.git
cd computer-control-mcp

# Install in development mode
pip install -e .
```

Or with uv:

```bash
# Clone the repository
git clone https://github.com/yourusername/computer-control-mcp.git
cd computer-control-mcp

# Install in development mode
uv pip install -e .
```

### Running Tests

```bash
python -m pytest
```

## API Reference

See the [API Reference](docs/api.md) for detailed information about the available functions and classes.

## License

MIT
