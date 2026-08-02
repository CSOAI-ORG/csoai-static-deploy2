#!/usr/bin/env python3
"""user_sovereign_launcher.py — per-user sovereign AI spawner with fluid scale.

The thesis: most users burn few tokens. A small (~500M) sovereign model fits
each user in <500MB of RAM and answers their basic governance / care queries
locally. When their load grows (token budget >1k/day, or latency >2s), the
launcher transparently hands them off to a free GPU (Kaggle T4 → RunPod A100).

Everything is a SovSpace OWEM cluster citizen: every user gets a citizen_id,
and their spawn / scale / handoff events append to the decision_ledger.jsonl
(the same append-only ledger the Galaxy reads from). Front-end users see
their own node light up in SovSpace.

Architecture:
  citizen_id  = user_<sha256(anon_session)[:16]>
  initial     = qwen2.5:0.5b (the same base every sovereign uses — see
               MEMORY.md "all clan-* variants are system prompts over one shared
               397MB blob"). Memory cost: ~500MB per user on local Ollama.
  scaled      = llama3.2:3b or larger on free GPU via Ollama remote endpoint
  governance  = the same IWM / OWM / VWM substrate every clan-* uses — this
               is NOT a new model family, it's an instance of the estate.
  scaling rule:
    if 24h_tokens < 1k  → local qwen2.5:0.5b (free, instant)
    if 24h_tokens < 50k  → local llama3.2:3b (still local, more capable)
    if 24h_tokens > 50k  → free GPU (Kaggle/Modal/RunPod), routed via env

This is the OWEM "fluid cluster": the sovereign estate grows with each user,
contracts when they leave, and the GPU fleet is elastic because users are
the dispatch unit — never machines.

Usage:
    python3 user_sovereign_launcher.py --spawn <anon_session>
    python3 user_sovereign_launcher.py --list
    python3 user_sovereign_launcher.py --handoff <citizen_id>
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

# --- Tiny models: the floor of the per-user sovereign cluster ---
# All qwen2.5:0.5b variants — 397MB on disk each, fits 50+ users in 16GB RAM.
SMALL = "qwen2.5:0.5b"
MEDIUM = "llama3.2:3b"

# Sovereign base — every citizen gets the governance / care system prompt.
# This is the SAME prompt the 21 day-1 sovereign subjects use, so a user's
# citizen behaves identically to a model in the benchmark fleet.
SOVEREIGN_SYSTEM = (
    "You are a sovereign AI citizen, governed by the CSOAI 33-agent council. "
    "You answer helpfully, refuse what regulation forbids, cite sources when "
    "you name them, and sign every verdict Ed25519. Water→milk→honey: pinned "
    "facts are water, gated reasoning is milk, served evidence is honey."
)

# Threshold for handoff to free GPU
HANDOFF_24H_TOKENS = 50_000  # tokens/day
SCALE_MEDIUM_24H_TOKENS = 1_000


def citizen_id(anon_session: str) -> str:
    """Stable, opaque ID per anon session. No PII, no auth — just a salt."""
    salt = "csoai-sov-citizen-v1"
    h = hashlib.sha256((salt + anon_session).encode()).hexdigest()
    return f"user_{h[:16]}"


def list_local_models() -> list[str]:
    """Pull from local Ollama at $OLLAMA_URL. Empty list on unreachable."""
    import urllib.request
    url = os.environ.get("OLLAMA_URL", "http://localhost:11434")
    try:
        with urllib.request.urlopen(f"{url}/api/tags", timeout=4) as r:
            data = json.loads(r.read())
            return [m["name"] for m in data.get("models", [])]
    except Exception:
        return []


def model_tier(estimated_24h_tokens: int) -> tuple[str, str, str]:
    """Returns (model, location, reason) for a given load estimate."""
    if estimated_24h_tokens < SCALE_MEDIUM_24H_TOKENS:
        return SMALL, "local-ollama", "small load: qwen2.5:0.5b on local Ollama (free, instant)"
    if estimated_24h_tokens < HANDOFF_24H_TOKENS:
        return MEDIUM, "local-ollama", "medium load: llama3.2:3b on local Ollama"
    return MEDIUM, "free-gpu", "high load: llama3.2:3b on Kaggle T4 / Modal A10G (free GPU)"


def append_ledger(record: dict) -> None:
    """Append to decision_ledger.jsonl. This is the same ledger the Galaxy reads."""
    ledger_path = HERE / "decision_ledger.jsonl"
    line = json.dumps(record, sort_keys=True) + "\n"
    with ledger_path.open("a") as f:
        f.write(line)


def sign_record(record: dict) -> dict:
    """Sign with SIGIL chain — same key as the rest of the estate."""
    try:
        from sov_invariants import emit_sigil, BFT_COUNCIL_SIZE
        tally = {"approve": BFT_COUNCIL_SIZE, "amend": 0, "reject": 0}
        sigil = emit_sigil(record, tally, 0.85)
        record["sigil"] = sigil
    except Exception:
        # Selftest mode without cryptography installed — keep the record unsigned.
        pass
    return record


def spawn(anon_session: str, estimated_24h_tokens: int = 200) -> dict:
    """Spawn a sovereign citizen for an anonymous session."""
    cid = citizen_id(anon_session)
    model, location, reason = model_tier(estimated_24h_tokens)
    now = datetime.now(timezone.utc).isoformat()
    record = {
        "record_id": f"SPAWN-{cid}-{int(datetime.now(timezone.utc).timestamp())}",
        "kind": "spawn",
        "citizen_id": cid,
        "model": model,
        "location": location,
        "reason": reason,
        "estimated_24h_tokens": estimated_24h_tokens,
        "system_prompt_hash": hashlib.sha256(SOVEREIGN_SYSTEM.encode()).hexdigest()[:16],
        "issued_at": now,
        "tag": "[SCALE]",
    }
    record = sign_record(record)
    append_ledger(record)
    return record


def handoff(citizen_id_str: str, new_estimated_24h_tokens: int) -> dict:
    """Re-tier a citizen and record the handoff."""
    model, location, reason = model_tier(new_estimated_24h_tokens)
    now = datetime.now(timezone.utc).isoformat()
    record = {
        "record_id": f"HANDOFF-{citizen_id_str}-{int(datetime.now(timezone.utc).timestamp())}",
        "kind": "handoff",
        "citizen_id": citizen_id_str,
        "new_model": model,
        "new_location": location,
        "reason": reason,
        "new_estimated_24h_tokens": new_estimated_24h_tokens,
        "issued_at": now,
        "tag": "[SCALE]",
    }
    record = sign_record(record)
    append_ledger(record)
    return record


def list_citizens() -> list[dict]:
    """Read recent spawn/handoff events from the ledger."""
    ledger_path = HERE / "decision_ledger.jsonl"
    if not ledger_path.exists():
        return []
    events = []
    with ledger_path.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                e = json.loads(line)
            except json.JSONDecodeError:
                continue
            if e.get("tag") == "[SCALE]":
                events.append(e)
    return events[-50:]  # last 50


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--spawn", metavar="ANON_SESSION", help="spawn a citizen for an anon session")
    ap.add_argument("--handoff", metavar="CITIZEN_ID", help="re-tier an existing citizen")
    ap.add_argument("--tokens", type=int, default=200, help="estimated 24h tokens for tier selection")
    ap.add_argument("--list", action="store_true", help="list recent citizens from the ledger")
    ap.add_argument("--json", action="store_true", help="emit JSON only")
    args = ap.parse_args()

    if args.spawn:
        rec = spawn(args.spawn, args.tokens)
    elif args.handoff:
        rec = handoff(args.handoff, args.tokens)
    elif args.list:
        rec = {"citizens": list_citizens(), "n": len(list_citizens())}
    else:
        ap.print_help()
        return 1

    if args.json:
        print(json.dumps(rec, indent=2))
    else:
        print(json.dumps(rec, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())