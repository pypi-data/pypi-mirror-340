# Keboola MCP Server

A Model Context Protocol (MCP) server that reveals skills exposed by the Keboola Skill Registry. This allows Claude to access and use tools from Keboola's Skill Registry directly within your conversations.

## Requirements

- Keboola Skill Registry API Token (Skill Group)

## Installation

## PyPI Installation (Recommended)

You can install the package directly from PyPI:

```bash
pip install keboola.skill_registry_mcp
```

### Manual Installation

First, clone the repository and create a virtual environment:

```bash
git clone https://github.com/keboola/keboola-mcp-server.git
cd keboola-mcp-server
python3 -m venv .venv
source .venv/bin/activate
```

Install the package in development mode:

```bash
pip3 install -e .
```

For development dependencies:

```bash
pip3 install -e ".[dev]"
```

## Claude Desktop Setup

To use this server with Claude Desktop, follow these steps:

1. Create or edit the Claude Desktop configuration file:
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

2. Add one of the following configurations (based on your installation method):

### Using PyPI Installation (Recommended)

```json
{
  "mcpServers": {
    "skill_registry": {
      "command": "keboola-sr-mcp",
      "args": [
        "--transport",
        "stdio",
        "--log-level",
        "DEBUG",
        "--api-url",
        "https://ksr.canary-orion.keboola.dev/api"
      ],
      "env": {
        "SKILL_REGISTRY_TOKEN": "SKILL_GROUP_TOKEN_FROM_REGISTRY_SERVICE"
      }
    }
  }
}
```

### Using Manual Installation

```json
{
  "mcpServers": {
   "skill_registry": {
      "command": "/path/to/keboola-skill-registry-mcp-server/.venv/bin/python",
      "args": [
        "-m",
        "keboola.skill_registry_mcp",
        "--transport",
        "stdio",
        "--log-level",
        "DEBUG",
        "--api-url",
        "https://ksr.canary-orion.keboola.dev/api"
      ],
      "env": {
        "SKILL_REGISTRY_TOKEN": "SKILL_GROUP_TOKEN_FROM_REGISTRY_SERVICE",
        "PYTHONPATH": "/path/to/keboola-skill-registry-mcp-server/src"
      }
    }
  }
}
```

Replace:

- `/path/to/keboola-mcp-server` with your actual path to the cloned repository
- `SKILL_REGISTRY_TOKEN` with your skill registry API token (skill group token)


## Available Tools

The server will include all tools that are exposed for the particular Skill Registry token. These tools will be automatically available to Claude when the MCP server is properly configured.

## Development

To contribute to this project:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: pytest
5. Submit a pull request

## License

MIT License - see LICENSE file for details.
