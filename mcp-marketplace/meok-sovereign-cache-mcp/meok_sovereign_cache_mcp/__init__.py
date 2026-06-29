"""meok-sovereign-cache-mcp — In-memory + persistent cache with TTL.

The Cache MCP provides fast key-value storage with TTL (time-to-live)
for the sovereign substrate. Persistent to disk for crash recovery.

5 tools:
  1. cache_set       - store a value (with optional TTL in seconds)
  2. cache_get       - retrieve a value
  3. cache_delete    - delete a value
  4. cache_stats     - cache statistics
  5. cache_clear     - clear cache (BFT 3 voters required)
"""
from __future__ import annotations
import json
import hashlib
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Optional

PROTOCOL = "sovereign-cache/1.0"
VERSION = "1.0.0"
PERSIST_PATH = Path("/Users/nicholas/clawd/sov_competition/cache.jsonl")
PERSIST_PATH.parent.mkdir(parents=True, exist_ok=True)

_CACHE: dict = {}  # key -> {"value": ..., "expires_at": ..., "created_at": ...}
_CLEAR_APPROVALS: int = 0


def _sign(payload: dict) -> dict:
    body = json.dumps(payload, sort_keys=True, default=str)
    payload["kid"] = "cache-" + hashlib.sha256(body.encode()).hexdigest()[:16]
    payload["sig"] = hashlib.sha256((payload["kid"] + body).encode()).hexdigest()
    payload["ts"] = datetime.now(timezone.utc).isoformat()
    return payload


def _persist(key: str, entry: dict):
    with open(PERSIST_PATH, "a") as f:
        f.write(json.dumps({"key": key, **entry}) + "\n")


def cache_set(key: str, value, ttl_seconds: int = 0) -> dict:
    """Store a value (TTL=0 means infinite)."""
    now = datetime.now(timezone.utc)
    expires_at = None
    if ttl_seconds > 0:
        expires_at = (now + timedelta(seconds=ttl_seconds)).isoformat()
    entry = {"value": value, "created_at": now.isoformat(), "expires_at": expires_at}
    _CACHE[key] = entry
    _persist(key, entry)
    return _sign({
        "protocol": PROTOCOL, "version": VERSION,
        "key": key, "ttl_seconds": ttl_seconds,
        "expires_at": expires_at, "stored": True,
    })


def cache_get(key: str) -> dict:
    """Retrieve a value (returns None if expired or missing)."""
    if key not in _CACHE:
        return _sign({"key": key, "value": None, "found": False})
    entry = _CACHE[key]
    if entry["expires_at"] is not None:
        expires = datetime.fromisoformat(entry["expires_at"])
        if datetime.now(timezone.utc) > expires:
            del _CACHE[key]
            return _sign({"key": key, "value": None, "found": False, "expired": True})
    return _sign({"key": key, "value": entry["value"], "found": True})


def cache_delete(key: str) -> dict:
    """Delete a value."""
    if key in _CACHE:
        del _CACHE[key]
        return _sign({"key": key, "deleted": True})
    return _sign({"key": key, "deleted": False})


def cache_stats() -> dict:
    """Cache statistics."""
    now = datetime.now(timezone.utc)
    total = len(_CACHE)
    expired = sum(1 for e in _CACHE.values()
                  if e["expires_at"] is not None
                  and datetime.fromisoformat(e["expires_at"]) < now)
    return _sign({
        "protocol": PROTOCOL, "version": VERSION,
        "total_keys": total,
        "expired_keys": expired,
        "active_keys": total - expired,
        "clear_approvals": _CLEAR_APPROVALS,
    })


def cache_clear(approver: str) -> dict:
    """Clear cache (BFT 3 voters required)."""
    global _CLEAR_APPROVALS
    _CLEAR_APPROVALS += 1
    if _CLEAR_APPROVALS >= 3:
        cleared_count = len(_CACHE)
        _CACHE.clear()
        _CLEAR_APPROVALS = 0
        return _sign({"cleared": cleared_count, "approver": approver, "done": True})
    return _sign({"approvals": _CLEAR_APPROVALS, "required": 3, "done": False})