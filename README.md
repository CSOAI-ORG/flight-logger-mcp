<div align="center">

# Flight Logger MCP

**MCP server for flight logger mcp operations**

[![PyPI](https://img.shields.io/pypi/v/meok-flight-logger-mcp)](https://pypi.org/project/meok-flight-logger-mcp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![MEOK AI Labs](https://img.shields.io/badge/MEOK_AI_Labs-MCP_Server-purple)](https://meok.ai)

</div>

## Overview

Flight Logger MCP provides AI-powered tools via the Model Context Protocol (MCP).

## Tools

| Tool | Description |
|------|-------------|
| `log_flight` | Log a completed drone/aircraft flight with full telemetry data. |
| `flight_summary` | Get flight history and statistics for a drone or all drones. |
| `compliance_report` | Generate a compliance report for a drone — regulatory adherence, altitude violat |
| `list_drones` | List all registered drones and their flight statistics. |

## Installation

```bash
pip install meok-flight-logger-mcp
```

## Usage with Claude Desktop

Add to your Claude Desktop MCP config (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "flight-logger": {
      "command": "python",
      "args": ["-m", "meok_flight_logger_mcp.server"]
    }
  }
}
```

## Usage with FastMCP

```python
from mcp.server.fastmcp import FastMCP

# This server exposes 4 tool(s) via MCP
# See server.py for full implementation
```

## License

MIT © [MEOK AI Labs](https://meok.ai)
