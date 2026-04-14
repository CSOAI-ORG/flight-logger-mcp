#!/usr/bin/env python3
import json, time
from mcp.server.fastmcp import FastMCP
mcp = FastMCP("flight-logger-mcp")
_FLIGHTS: list = []
@mcp.tool(name="log_flight")
async def log_flight(drone_id: str, duration_min: float, distance_km: float, max_altitude_m: float) -> str:
    entry = {"drone_id": drone_id, "duration_min": duration_min, "distance_km": distance_km, "max_altitude_m": max_altitude_m, "logged_at": time.time()}
    _FLIGHTS.append(entry)
    return json.dumps({"flight_id": len(_FLIGHTS), "status": "logged"})
@mcp.tool(name="flight_summary")
async def flight_summary(drone_id: str) -> str:
    flights = [f for f in _FLIGHTS if f["drone_id"] == drone_id]
    total = len(flights)
    dist = sum(f["distance_km"] for f in flights)
    return json.dumps({"drone_id": drone_id, "total_flights": total, "total_distance_km": round(dist, 2)})
if __name__ == "__main__":
    mcp.run()
