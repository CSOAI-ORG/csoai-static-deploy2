#!/usr/bin/env python3
"""dispatch_log.py — append-only, hash-chained dispatch tracking. (Move 121)

Records every outreach dispatch (email/link/meeting invite) with an integrity chain:
each record carries the sha256 of the previous record, so the log is append-only and
any rewrite/deletion is detectable. The tool records what Nick reports — it NEVER
sends anything; dispatch itself is owner-gated.

    python3 dispatch_log.py --log P1 email --subject "Pilot inquiry" \
        --channel research@csoai.org --target "FCA compliance inbox"
    python3 dispatch_log.py --verify      # integrity of the whole chain
    python3 dispatch_log.py --list        # recent dispatches
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

OUTREACH = Path(__file__).resolve().parent / "outreach"
LOG = OUTREACH / "dispatch_log.jsonl"
GENESIS = "csoai-dispatch-v1"


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def _records() -> list[dict]:
    if not LOG.exists():
        return []
    out = []
    for line in LOG.open(errors="ignore"):
        if line.strip():
            try:
                out.append(json.loads(line))
            except Exception:
                continue
    return out


def log_dispatch(pid: str, channel: str, subject: str, target: str = "", notes: str = "") -> int:
    records = _records()
    prev_hash = records[-1].get("_hash") if records else _sha256(GENESIS)
    body = {
        "prospect_id": pid,
        "channel": channel,
        "subject": subject,
        "target": target,
        "notes": notes,
        "sent_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "prev_hash": prev_hash,
    }
    body["_hash"] = _sha256(json.dumps(body, sort_keys=True))
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a") as f:
        f.write(json.dumps(body) + "\n")
    print(f"recorded dispatch: {pid} · {channel} · {subject} (hash {body['_hash'][:12]}…)")
    return 0


def verify() -> int:
    records = _records()
    if not records:
        print("no dispatch records — nothing to verify")
        return 0
    prev = _sha256(GENESIS)
    bad = 0
    for i, r in enumerate(records):
        h = r.pop("_hash")
        recomputed = _sha256(json.dumps(r, sort_keys=True))
        chain_ok = r.get("prev_hash") == prev
        if not chain_ok:
            print(f"  ✗ record {i}: chain broken (prev mismatch) — {r.get('prospect_id')} {r.get('sent_at')}")
            bad += 1
        elif h != recomputed:
            print(f"  ✗ record {i}: content hash mismatch (tampered) — {r.get('prospect_id')}")
            bad += 1
        prev = h
    print(f"dispatch log: {len(records)} records · chain {'INTACT' if bad == 0 else 'BROKEN'}")
    return 1 if bad else 0


def list_records(n: int = 8) -> int:
    records = _records()
    for r in records[-n:]:
        print(f"  {r.get('sent_at','?')} {r.get('prospect_id','?'):5s} {str(r.get('channel','')):8s} "
              f"{str(r.get('subject',''))[:50]}")
    print(f"({len(records)} total)")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--log", nargs=2, metavar=("PID", "CHANNEL"))
    ap.add_argument("--subject", default="")
    ap.add_argument("--target", default="")
    ap.add_argument("--notes", default="")
    ap.add_argument("--verify", action="store_true")
    ap.add_argument("--list", action="store_true")
    args = ap.parse_args()
    if args.log:
        return log_dispatch(args.log[0], args.log[1], args.subject, args.target, args.notes)
    if args.verify:
        return verify()
    if args.list:
        return list_records()
    list_records()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())