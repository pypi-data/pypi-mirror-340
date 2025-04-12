# Keboola MCP Server

A Model Context Protocol (MCP) server that reveals skills exposed by the Skill Registry.

## Requirements

- Keboola Skill Registry API Token (Skill Group)

## Installation

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

2. Add the following configuration (adjust paths according to your setup):

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
        "SKILL_REGISTRY_TOKEN": "XXX",
        "PYTHONPATH": "/path/to/keboola-skill-registry-mcp-server/src"
      }
    }
  }
}
```

Replace:
- `/path/to/keboola-mcp-server` with your actual path to the cloned repository
- `SKILL_REGISTRY_TOKEN` skill registry api token (skill group token)


## Available Tools

The server will include all tools that are exposed for the particular Skill registry token.


## License

MIT License - see LICENSE file for details.
