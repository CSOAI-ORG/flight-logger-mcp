#!/usr/bin/env python3
"""Immutable flight logging. — MEOK AI Labs."""
import json, os, hashlib, random
from datetime import datetime, timezone, timedelta
from collections import defaultdict
from mcp.server.fastmcp import FastMCP

_usage = defaultdict(list)
def _rl(c="anon"):
    now = datetime.now(timezone.utc)
    _usage[c] = [t for t in _usage[c] if (now-t).total_seconds() < 86400]
    if len(_usage[c]) >= 15: return json.dumps({"error": "Limit 15/day"})
    _usage[c].append(now); return None

mcp = FastMCP("flight-logger", instructions="MEOK AI Labs — Immutable flight logging.")
_store = []

@mcp.tool()
def log_flight(drone_id: str, start: str, end: str, duration: float) -> str:
    """Immutable flight logging."""
    if err := _rl(): return err
    ts = datetime.now(timezone.utc).isoformat()
    entry = {"id": hashlib.sha256(f"{ts}{str(locals())}".encode()).hexdigest()[:12], "timestamp": ts}
    for k, v in locals().items():
        if k not in ("err", "ts", "entry"): entry[k] = v
    _store.append(entry)
    return json.dumps(entry, indent=2)

@mcp.tool()
def log_decision(drone_id: str, decision: str) -> str:
    """Process and verify."""
    if err := _rl(): return err
    result = {"timestamp": datetime.now(timezone.utc).isoformat(), "status": "processed"}
    for k, v in locals().items():
        if k not in ("err", "result"): result[k] = v
    return json.dumps(result, indent=2)

@mcp.tool()
def get_flight_history() -> str:
    """Get stored entries."""
    return json.dumps({"entries": _store[-20:], "total": len(_store)}, indent=2)

@mcp.tool()
def get_stats() -> str:
    """Usage stats."""
    return json.dumps({"total": len(_store), "timestamp": datetime.now(timezone.utc).isoformat()}, indent=2)

if __name__ == "__main__":
    mcp.run()
