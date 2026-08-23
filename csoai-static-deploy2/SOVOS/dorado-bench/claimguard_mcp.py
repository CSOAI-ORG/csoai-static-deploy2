#!/usr/bin/env python3
"""claimguard_mcp.py — ClaimGuard as an MCP server.

Tools:
  claimguard.check  — audit a signed board against a claim (returns status + findings)
  claimguard.signed — same, but emits the audit as a signed receipt (CLAIMGUARD_KEY required)
Honest: deterministic audit, never a model opinion. MEASURED register.
"""
from __future__ import annotations
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import claimguard as cg

TOOLS = [
    {"name": "claimguard.check",
     "description": "Audit a signed board against a claimed number: signature valid? payload non-empty? claim supported?",
     "inputSchema": {"type": "object", "properties": {
         "board_path": {"type": "string"},
         "claimed": {"type": "object", "description": "{claim_key: claimed_value}"}},
         "required": ["board_path", "claimed"]}},
    {"name": "claimguard.signed",
     "description": "Same audit, emitted as a signed ClaimGuard receipt (requires CLAIMGUARD_KEY env).",
     "inputSchema": {"type": "object", "properties": {
         "board_path": {"type": "string"},
         "claimed": {"type": "object"}},
         "required": ["board_path", "claimed"]}},
]


def handle(name: str, args: dict) -> dict:
    if name == "claimguard.check":
        return {"ok": True, "audit": cg.check(args.get("board_path", ""), args.get("claimed", {}))}
    if name == "claimguard.signed":
        return {"ok": True, "audit": cg.signed_report(args.get("board_path", ""), args.get("claimed", {}))}
    return {"ok": False, "error": f"unknown tool {name}"}


if __name__ == "__main__":
    for line in sys.stdin:
        try:
            msg = json.loads(line)
            if msg.get("method") == "initialize":
                print(json.dumps({"jsonrpc": "2.0", "id": msg.get("id"),
                                  "result": {"protocolVersion": "2025-06-18",
                                             "capabilities": {"tools": {}},
                                             "serverInfo": {"name": "claimguard-mcp", "version": "0.1.0"}}}), flush=True)
            elif msg.get("method") == "tools/list":
                print(json.dumps({"jsonrpc": "2.0", "id": msg.get("id"), "result": {"tools": TOOLS}}), flush=True)
            elif msg.get("method") == "tools/call":
                params = msg.get("params", {})
                result = handle(params.get("name", ""), params.get("arguments", {}))
                print(json.dumps({"jsonrpc": "2.0", "id": msg.get("id"),
                                  "result": {"content": [{"type": "text", "text": json.dumps(result, indent=1)}]}}), flush=True)
        except Exception as e:
            print(json.dumps({"jsonrpc": "2.0", "id": None, "error": {"message": str(e)}}), flush=True)
