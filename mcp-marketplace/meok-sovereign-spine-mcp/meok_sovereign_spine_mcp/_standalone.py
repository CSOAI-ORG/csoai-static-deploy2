"""meok-sovereign-spine-mcp — the SIGNING SPINE MCP wrapper.

Wraps spine_v2.py with MCP tools for the sovereign substrate.

8 tools:
  1. sign_card         - sign a card (any of 5 standard kinds)
  2. verify_card       - verify a card's CID + Ed25519 sig
  3. recompute_check   - external-recompute probe (is the CID in our ledger + does it verify?)
  4. register_kind     - register a new card kind (extensible)
  5. list_kinds        - list all registered kinds
  6. list_cards        - list cards in ledger (filter by kind)
  7. canonical_json    - canonicalise a JSON value (RFC 8785-style)
  8. content_hash      - compute the CID for a payload
"""
from __future__ import annotations
import sys
import os

# Ensure we can import spine_v2 (relative or absolute)
_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_SPINE_PATH = os.environ.get("SPINE_V2_PATH", os.path.join(_THIS_DIR, "spine_v2.py"))
if _THIS_DIR not in sys.path:
    sys.path.insert(0, _THIS_DIR)
if os.path.dirname(_SPINE_PATH) and os.path.dirname(_SPINE_PATH) not in sys.path:
    sys.path.insert(0, os.path.dirname(_SPINE_PATH))

try:
    import spine_v2
except ImportError:
    # Try with filename
    import importlib.util
    spec = importlib.util.spec_from_file_location("spine_v2", _SPINE_PATH)
    spine_v2 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(spine_v2)

# Re-export the 8 tools
PROTOCOL = "sovereign-spine-mcp/2.0"
VERSION = "2.0.0"

# Each tool is a thin wrapper that handles JSON serialisation for MCP transports.

def mcp_sign_card(kind: str, payload: dict, key_path: str = None) -> dict:
    """Sign a card. Returns {cid, kind, payload, sig, pub_key, ts, protocol, version}."""
    return spine_v2.sign_card(kind, payload, key_path)


def mcp_verify_card(card: dict) -> dict:
    """Verify a signed card. Returns {valid: bool, reason?, cid?, kind?}."""
    return spine_v2.verify_card(card)


def mcp_recompute_check(cid: str) -> dict:
    """External-recompute probe. Is the CID in our ledger? Does it verify?"""
    return spine_v2.recompute_check(cid)


def mcp_register_kind(name: str, schema: dict, description: str = "") -> dict:
    """Register a new card kind."""
    return spine_v2.register_kind(name, schema, description)


def mcp_list_kinds() -> dict:
    return spine_v2.list_kinds()


def mcp_list_cards(kind: str = None, limit: int = 100) -> dict:
    return spine_v2.list_cards(kind, limit)


def mcp_canonical_json(payload) -> dict:
    """Canonicalise a JSON value. Returns {canonical: str, bytes: int}."""
    canon = spine_v2.canonical_json(payload)
    return {"canonical": canon.decode("utf-8"), "bytes": len(canon)}


def mcp_content_hash(payload) -> dict:
    """Compute the CID for a payload. Returns {cid: 'sha256:...'}."""
    return {"cid": spine_v2.content_hash(payload)}


def main():
    """MCP discovery entrypoint."""
    return {
        "name": "meok-sovereign-spine-mcp",
        "version": VERSION,
        "protocol": PROTOCOL,
        "tools": [
            {"name": "spine_sign_card",       "fn": mcp_sign_card,      "schema": {"kind": "str", "payload": "dict"}},
            {"name": "spine_verify_card",     "fn": mcp_verify_card,    "schema": {"card": "dict"}},
            {"name": "spine_recompute_check", "fn": mcp_recompute_check,"schema": {"cid": "str"}},
            {"name": "spine_register_kind",   "fn": mcp_register_kind,  "schema": {"name": "str", "schema": "dict", "description": "str?"}},
            {"name": "spine_list_kinds",      "fn": mcp_list_kinds,     "schema": {}},
            {"name": "spine_list_cards",      "fn": mcp_list_cards,     "schema": {"kind": "str?", "limit": "int?"}},
            {"name": "spine_canonical_json",  "fn": mcp_canonical_json, "schema": {"payload": "any"}},
            {"name": "spine_content_hash",    "fn": mcp_content_hash,   "schema": {"payload": "any"}},
        ],
    }


if __name__ == "__main__":
    import json
    print(json.dumps(main(), indent=2, default=str))
