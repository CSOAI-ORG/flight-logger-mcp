# Flight Logger

> By [MEOK AI Labs](https://meok.ai) — Drone and aircraft flight logging. Log flights, track compliance, view history, and manage maintenance. By MEOK AI Labs.

Flight Logger MCP — MEOK AI Labs. Drone/aircraft flight logging, compliance tracking, maintenance scheduling.

## Installation

```bash
pip install flight-logger-mcp
```

## Usage

```bash
# Run standalone
python server.py

# Or via MCP
mcp install flight-logger-mcp
```

## Tools

### `log_flight`
Log a completed drone/aircraft flight with full telemetry data.

**Parameters:**
- `drone_id` (str)
- `duration_min` (float)
- `distance_km` (float)
- `max_altitude_m` (float)
- `location` (str)
- `notes` (str)
- `battery_start_pct` (float)
- `battery_end_pct` (float)

### `flight_summary`
Get flight history and statistics for a drone or all drones.

**Parameters:**
- `drone_id` (str)
- `last_n` (int)

### `compliance_report`
Generate a compliance report for a drone — regulatory adherence, altitude violations, maintenance status.

**Parameters:**
- `drone_id` (str)

### `list_drones`
List all registered drones and their flight statistics.


## Authentication

Free tier: 15 calls/day. Upgrade at [meok.ai/pricing](https://meok.ai/pricing) for unlimited access.

## Links

- **Website**: [meok.ai](https://meok.ai)
- **GitHub**: [CSOAI-ORG/flight-logger-mcp](https://github.com/CSOAI-ORG/flight-logger-mcp)
- **PyPI**: [pypi.org/project/flight-logger-mcp](https://pypi.org/project/flight-logger-mcp/)

## License

MIT — MEOK AI Labs
