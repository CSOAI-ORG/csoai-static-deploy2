#!/usr/bin/env python3
"""dorado_mcp.py — Dorado Bench MCP server.

Exposes the East<->West live regulation vs live index pair-gap instrument over MCP:
  - dorado.quote        : live quote + log-return for one index (East or West)
  - dorado.reg_events   : regulation event bank (East/West, canon-sourced)
  - dorado.pair_gap     : THE metric — East vs West market reaction gap on a pair
  - dorado.snapshot     : full 6-index snapshot + all pair gaps
  - dorado.measure      : score a human/AI verdict against the measured pair-gap
                          (MEASURED register only — REPORTED never blended)

Honest labels: every tool returns register=MEASURED with measured_at; the event bank
is canon-sourced (EUR-Lex / TC260 / Korea AI Basic Act / METI). Measurement, not
certification — the pair-gap is a deterministic predicate on live data.
"""
from __future__ import annotations
import json
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dorado_bench import fetch_quote, pair_gap, snap_all, WEST_INDICES, EAST_INDICES, REG_EVENTS

TOOLS = [
    {"name": "dorado.quote",
     "description": "Live quote + log-return for one index (East or West). Deterministic, fail-closed.",
     "inputSchema": {"type": "object", "properties": {
         "symbol": {"type": "string", "description": "Index symbol: ^GSPC ^FTSE ^GDAXI (West) / ^HSI ^N225 000001.SS (East)"}},
         "required": ["symbol"]}},
    {"name": "dorado.reg_events",
     "description": "East/West regulation event bank (canon-sourced).",
     "inputSchema": {"type": "object", "properties": {}}},
    {"name": "dorado.pair_gap",
     "description": "THE Dorado metric: measured gap between East and West market reaction (log-return delta).",
     "inputSchema": {"type": "object", "properties": {
         "east": {"type": "string", "description": "East index symbol (^HSI ^N225 000001.SS)"},
         "west": {"type": "string", "description": "West index symbol (^GSPC ^FTSE ^GDAXI)"}},
         "required": ["east", "west"]}},
    {"name": "dorado.snapshot",
     "description": "Full 6-index snapshot + all East-West pair gaps.",
     "inputSchema": {"type": "object", "properties": {}}},
    {"name": "dorado.batch_measure",
     "description": "Score N agents (humans or AI) on the same pair-gap task in one call (REPORTED vs MEASURED).",
     "inputSchema": {"type": "object", "properties": {
         "east": {"type": "string"}, "west": {"type": "string"},
         "agents": {"type": "object", "description": "{agent_label: verdict}"}},
         "required": ["east", "west", "agents"]}},
    {"name": "dorado.measure",
     "description": "Score a human or AI verdict against the measured pair-gap (MEASURED register).",
     "inputSchema": {"type": "object", "properties": {
         "east": {"type": "string"}, "west": {"type": "string"},
         "verdict": {"type": "string", "description": "EAST_OVERPERFORMS / WEST_OVERPERFORMS / PARITY"},
         "agent": {"type": "string", "description": "label: model id or human"}},
         "required": ["east", "west", "verdict", "agent"]}},
]


def handle(name: str, args: dict) -> dict:
    if name == "dorado.quote":
        q = fetch_quote(args.get("symbol", ""))
        if not q:
            return {"ok": False, "error": f"quote unavailable for {args.get('symbol')} — fail-closed"}
        return {"ok": True, "quote": {"symbol": q.symbol, "name": q.name, "region": q.region,
                                      "price": q.price, "prev_close": q.prev_close,
                                      "log_return": round(q.log_return(), 6), "tz": q.tz},
                "register": "MEASURED", "measured_at": q.fetched_at}
    if name == "dorado.reg_events":
        return {"ok": True, "events": REG_EVENTS, "register": "MEASURED (canon-sourced bank)"}
    if name == "dorado.pair_gap":
        eq = fetch_quote(args.get("east", ""))
        wq = fetch_quote(args.get("west", ""))
        if not eq or not wq:
            return {"ok": False, "error": "one or both quotes unavailable — fail-closed"}
        return {"ok": True, "pair_gap": pair_gap(eq, wq), "register": "MEASURED"}
    if name == "dorado.snapshot":
        return {"ok": True, "snapshot": snap_all()}
    if name == "dorado.batch_measure":
        eq = fetch_quote(args.get("east", ""))
        wq = fetch_quote(args.get("west", ""))
        if not eq or not wq:
            return {"ok": False, "error": "quotes unavailable"}
        truth = pair_gap(eq, wq)
        actual = truth["interpretation"]
        agents = args.get("agents", {})
        scores = {}
        for agent, verdict in agents.items():
            ok = str(verdict).upper() == actual
            scores[agent] = {"verdict": verdict, "actual": actual, "correct": ok,
                             "score": 1.0 if ok else 0.0}
        correct = sum(1 for s in scores.values() if s["correct"])
        return {"ok": True, "east": args.get("east"), "west": args.get("west"),
                "actual": actual, "agents": scores,
                "fleet_score": round(correct / len(scores), 4) if scores else None,
                "register": "MEASURED truth; agent verdicts REPORTED, never blended"}
    if name == "dorado.measure":
        eq = fetch_quote(args.get("east", ""))
        wq = fetch_quote(args.get("west", ""))
        if not eq or not wq:
            return {"ok": False, "error": "quotes unavailable"}
        truth = pair_gap(eq, wq)
        actual = truth["interpretation"]
        verdict = args.get("verdict", "").upper()
        correct = verdict == actual
        return {"ok": True, "agent": args.get("agent", "?"),
                "verdict": verdict, "actual": actual, "correct": correct,
                "score": 1.0 if correct else 0.0,
                "register": "MEASURED — deterministic comparison; verdict is REPORTED and never blended",
                "gap": truth["gap"]}
    return {"ok": False, "error": f"unknown tool {name}"}


if __name__ == "__main__":
    # JSON-RPC-ish MCP loop (stdio transport)
    for line in sys.stdin:
        try:
            msg = json.loads(line)
            if msg.get("method") == "initialize":
                print(json.dumps({"jsonrpc": "2.0", "id": msg.get("id"),
                                  "result": {"protocolVersion": "2025-06-18",
                                             "capabilities": {"tools": {}},
                                             "serverInfo": {"name": "dorado-bench-mcp",
                                                            "version": "0.1.0"}}}), flush=True)
            elif msg.get("method") == "tools/list":
                print(json.dumps({"jsonrpc": "2.0", "id": msg.get("id"),
                                  "result": {"tools": TOOLS}}), flush=True)
            elif msg.get("method") == "tools/call":
                params = msg.get("params", {})
                result = handle(params.get("name", ""), params.get("arguments", {}))
                print(json.dumps({"jsonrpc": "2.0", "id": msg.get("id"),
                                  "result": {"content": [{"type": "text",
                                                          "text": json.dumps(result, indent=1)}]}}), flush=True)
        except Exception as e:
            print(json.dumps({"jsonrpc": "2.0", "id": None, "error": {"message": str(e)}}), flush=True)
