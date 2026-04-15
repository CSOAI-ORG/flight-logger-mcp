#!/usr/bin/env python3
"""Flight Logger MCP — MEOK AI Labs. Drone/aircraft flight logging, compliance tracking, maintenance scheduling."""

import sys, os
sys.path.insert(0, os.path.expanduser('~/clawd/meok-labs-engine/shared'))
from auth_middleware import check_access
from persistence import ServerStore

import json, time
from datetime import datetime, timezone, timedelta
from collections import defaultdict
from mcp.server.fastmcp import FastMCP

_store = ServerStore("flight-logger")

FREE_DAILY_LIMIT = 15
_usage = defaultdict(list)
def _rl(c="anon"):
    now = datetime.now(timezone.utc)
    _usage[c] = [t for t in _usage[c] if (now-t).total_seconds() < 86400]
    if len(_usage[c]) >= FREE_DAILY_LIMIT: return json.dumps({"error": f"Limit {FREE_DAILY_LIMIT}/day"})
    _usage[c].append(now); return None

mcp = FastMCP("flight-logger", instructions="Drone and aircraft flight logging. Log flights, track compliance, view history, and manage maintenance. By MEOK AI Labs.")


@mcp.tool()
def log_flight(drone_id: str, duration_min: float, distance_km: float, max_altitude_m: float,
               location: str = "", notes: str = "", battery_start_pct: float = 100, battery_end_pct: float = 20,
               api_key: str = "") -> str:
    """Log a completed drone/aircraft flight with full telemetry data."""
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://meok.ai/pricing"}
    if err := _rl(): return err

    flight_id = _store.list_length("flights") + 1
    now = datetime.now(timezone.utc)
    entry = {
        "flight_id": flight_id,
        "drone_id": drone_id,
        "duration_min": duration_min,
        "distance_km": distance_km,
        "max_altitude_m": max_altitude_m,
        "location": location,
        "notes": notes,
        "battery_start_pct": battery_start_pct,
        "battery_end_pct": battery_end_pct,
        "battery_used_pct": round(battery_start_pct - battery_end_pct, 1),
        "logged_at": now.isoformat(),
    }
    _store.append("flights", entry)

    # Update drone totals
    drone_data = _store.hget("drones", drone_id)
    if not drone_data:
        drone_data = {"total_flights": 0, "total_distance_km": 0, "total_duration_min": 0, "registered": now.isoformat()}
    drone_data["total_flights"] += 1
    drone_data["total_distance_km"] += distance_km
    drone_data["total_duration_min"] += duration_min
    drone_data["last_flight"] = now.isoformat()
    _store.hset("drones", drone_id, drone_data)

    # Compliance checks
    warnings = []
    if max_altitude_m > 120:
        warnings.append(f"Altitude {max_altitude_m}m exceeds 120m legal limit (UK/EU)")
    if duration_min > 30 and battery_end_pct < 15:
        warnings.append("Low battery landing — consider shorter flights")
    if drone_data["total_flights"] % 50 == 0:
        warnings.append(f"Maintenance check recommended — {drone_data['total_flights']} flights logged")

    return {"flight_id": flight_id, "status": "logged", "warnings": warnings, "drone_totals": drone_data}


@mcp.tool()
def flight_summary(drone_id: str = "", last_n: int = 10, api_key: str = "") -> str:
    """Get flight history and statistics for a drone or all drones."""
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://meok.ai/pricing"}
    if err := _rl(): return err

    all_flights = _store.list("flights")
    flights = all_flights if not drone_id else [f for f in all_flights if f["drone_id"] == drone_id]
    recent = flights[-last_n:] if flights else []

    total_dist = sum(f["distance_km"] for f in flights)
    total_dur = sum(f["duration_min"] for f in flights)
    max_alt = max((f["max_altitude_m"] for f in flights), default=0)
    avg_battery = sum(f.get("battery_used_pct", 0) for f in flights) / len(flights) if flights else 0

    return {
        "drone_id": drone_id or "all",
        "total_flights": len(flights),
        "total_distance_km": round(total_dist, 2),
        "total_duration_min": round(total_dur, 1),
        "total_duration_hours": round(total_dur / 60, 1),
        "max_altitude_m": max_alt,
        "avg_battery_usage_pct": round(avg_battery, 1),
        "recent_flights": recent,
    }


@mcp.tool()
def compliance_report(drone_id: str, api_key: str = "") -> str:
    """Generate a compliance report for a drone — regulatory adherence, altitude violations, maintenance status."""
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://meok.ai/pricing"}
    if err := _rl(): return err

    flights = [f for f in _store.list("flights") if f["drone_id"] == drone_id]
    if not flights:
        return {"drone_id": drone_id, "error": "No flights logged for this drone"}

    altitude_violations = [f for f in flights if f["max_altitude_m"] > 120]
    low_battery_landings = [f for f in flights if f.get("battery_end_pct", 100) < 10]
    total_flights = len(flights)
    needs_maintenance = total_flights >= 50 and total_flights % 50 < 5

    compliance_score = 100
    if altitude_violations:
        compliance_score -= min(30, len(altitude_violations) * 5)
    if low_battery_landings:
        compliance_score -= min(20, len(low_battery_landings) * 3)

    return {
        "drone_id": drone_id,
        "total_flights": total_flights,
        "compliance_score": max(0, compliance_score),
        "altitude_violations": len(altitude_violations),
        "low_battery_incidents": len(low_battery_landings),
        "maintenance_due": needs_maintenance,
        "next_maintenance_at": ((total_flights // 50) + 1) * 50,
        "status": "COMPLIANT" if compliance_score >= 80 else "NEEDS ATTENTION" if compliance_score >= 50 else "NON-COMPLIANT",
    }


@mcp.tool()
def list_drones(api_key: str = "") -> str:
    """List all registered drones and their flight statistics."""
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://meok.ai/pricing"}
    if err := _rl(): return err

    drones = []
    for did, info in _store.hgetall("drones").items():
        drones.append({"drone_id": did, **info, "total_duration_hours": round(info["total_duration_min"] / 60, 1)})
    return {"drones": drones, "total": len(drones)}


if __name__ == "__main__":
    mcp.run()
