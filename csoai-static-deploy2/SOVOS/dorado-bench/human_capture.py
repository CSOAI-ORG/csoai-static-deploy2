#!/usr/bin/env python3
"""human_capture.py — Council Ledger: human-baseline capture pipeline.

Replaces the hardcoded human example with a REAL capture flow: a human records their
verdict on the pair-gap task (or provision-conformance task), timestamped + provenance-
tagged, stored append-only, REPORTED register. Never blended with MEASURED.

Flow: record_human_verdict(agent, task, verdict, note) -> append to ledger file
      list_human_verdicts() -> all captured (provenance: human, recorded_at)
"""
from __future__ import annotations
import json, os, time, hashlib

DEFAULT_STORE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "human-verdicts.jsonl")


def record_human_verdict(agent: str, task: str, verdict: str, note: str = "",
                         store: str = DEFAULT_STORE) -> dict:
    """Append a human verdict. REPORTED register — provenance captured, never blended."""
    rec = {
        "schema": "csoai.ledger.human/0.1",
        "agent": agent,
        "kind": "human",
        "task": task,
        "verdict": verdict,
        "note": note,
        "recorded_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "provenance": "human-reported (REPORTED register — never blended with MEASURED)",
    }
    rec["record_sha256"] = hashlib.sha256(json.dumps(rec, sort_keys=True).encode()).hexdigest()[:16]
    with open(store, "a") as f:
        f.write(json.dumps(rec) + "\n")
    return rec


def list_human_verdicts(store: str = DEFAULT_STORE) -> list:
    if not os.path.exists(store):
        return []
    return [json.loads(l) for l in open(store) if l.strip()]


if __name__ == "__main__":
    r = record_human_verdict("human-nick", "pair-gap HSI|GSPC", "EAST_OVERPERFORMS",
                             note="live tape read 2026-08-20")
    print("recorded:", r["record_sha256"], r["recorded_at"])
    print("stored:", len(list_human_verdicts()), "verdicts")
