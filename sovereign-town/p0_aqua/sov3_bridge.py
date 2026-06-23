#!/usr/bin/env python3
"""
SOV3 cross-terminal bridge.

The Mac dashboard can reach the VM SOV3 mesh through the managed SSH tunnel at
``SOV_TOWN_SOV3_MESH_URL`` (default http://127.0.0.1:3101/mcp).  This module
provides a signed Ed25519 handshake and a thin proxy to the ``bridge_think``
MCP tool.
"""
from __future__ import annotations

import base64
import os
import time
from typing import Any

import httpx

import config
import sign_lib

SOV3_MESH_URL = config.SOV3_MESH_URL
SOV3_KEY = os.environ.get("SOV_TOWN_SOV3_KEY")

_KEY_CACHE: tuple[Any, str] | None = None


def _load_key() -> tuple[Any, str]:
    global _KEY_CACHE
    if _KEY_CACHE is None:
        priv, pubkey = sign_lib.load_or_create_key()
        _KEY_CACHE = (priv, pubkey)
    return _KEY_CACHE


def _b64_nonce(n: int = 16) -> str:
    return base64.b64encode(os.urandom(n)).decode()


def handshake() -> dict[str, str]:
    """Return a signed attestation the VM can verify against ``town_pub.key``."""
    priv, pubkey = _load_key()
    nonce = _b64_nonce()
    timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    message = f"sov3-handshake|{nonce}|{timestamp}"
    sig = sign_lib.sign(priv, message)
    return {
        "pubkey": pubkey,
        "nonce": nonce,
        "timestamp": timestamp,
        "sig": sig,
        "message": message,
    }


def verify_handshake(payload: dict[str, str]) -> bool:
    """Verify a handshake payload signed by ``handshake()``."""
    pubkey = payload.get("pubkey")
    message = payload.get("message")
    sig = payload.get("sig")
    if not pubkey or not message or not sig:
        return False
    return sign_lib.verify(pubkey, message, sig)


async def bridge_think(
    character: str,
    message: str,
    profile: str = "balanced",
) -> dict[str, Any]:
    """
    Call the VM SOV3 ``bridge_think`` tool.

    Returns the raw JSON-RPC result on success, or a structured error dict if
    SOV3 is unreachable or the tool is not registered.
    """
    body = {
        "jsonrpc": "2.0",
        "id": f"sov-town-{int(time.time()*1000)}",
        "method": "tools/call",
        "params": {
            "name": "bridge_think",
            "arguments": {
                "character": character,
                "message": message,
                "profile": profile,
            },
        },
    }
    headers = {"Content-Type": "application/json"}
    if SOV3_KEY:
        headers["Authorization"] = f"Bearer {SOV3_KEY}"
    try:
        async with httpx.AsyncClient(timeout=httpx.Timeout(60.0, connect=5.0)) as client:
            r = await client.post(SOV3_MESH_URL, json=body, headers=headers)
        try:
            data = r.json()
        except Exception:
            data = {"raw": r.text[:500]}
        if r.status_code >= 400:
            return {
                "error": "SOV3 bridge_think returned an error",
                "status_code": r.status_code,
                "detail": data,
            }
        return data
    except httpx.ConnectError as e:
        return {
            "error": "SOV3 mesh unreachable",
            "detail": str(e),
            "hint": f"Is the tunnel to {SOV3_MESH_URL} alive?",
        }
    except httpx.TimeoutException as e:
        return {
            "error": "SOV3 bridge_think timed out",
            "detail": str(e),
        }
