#!/usr/bin/env python3
"""funnel_tools.py — dispatch state machine + pipeline forecast. (Moves 117-119)

Layered on outreach/funnel_tracker.jsonl. Stages: draft-ready → sent → replied →
meeting → proposal → closed. NOTHING moves to 'sent' except by Nick (dispatch is
owner-gated); this tool records the transition he reports, it never sends.

    python3 funnel_tools.py --list              # tracker + pipeline value
    python3 funnel_tools.py --advance P1 sent   # Nick reports P1 dispatched
    python3 funnel_tools.py --forecast          # pipeline forecast by stage
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

TRACKER = Path(__file__).resolve().parent / "outreach" / "funnel_tracker.jsonl"
STAGES = ("draft-ready", "sent", "replied", "meeting", "proposal", "closed")


def load() -> list[dict]:
    if not TRACKER.exists():
        return []
    return [json.loads(l) for l in TRACKER.open() if l.strip()]


def save(rows: list[dict]) -> None:
    TRACKER.parent.mkdir(parents=True, exist_ok=True)
    with TRACKER.open("w") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")


def list_rows() -> int:
    rows = load()
    tot = sum(r.get("value_usd", 0) for r in rows)
    print(f"prospects: {len(rows)} · pipeline value: ${tot:,}")
    for r in rows:
        print(f"  {r['id']} {r['type']:10s} {r['value_usd']:>10,} {r['sector']:12s} [{r['stage']}]")
    return 0


def advance(pid: str, stage: str) -> int:
    if stage not in STAGES:
        print(f"stage must be one of {STAGES}")
        return 1
    rows = load()
    for r in rows:
        if r["id"] == pid:
            if r["stage"] == "closed":
                print(f"{pid} already closed — no further transitions")
                return 0
            r["stage"] = stage
            r["updated_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            save(rows)
            # Move 121: entering 'sent' must also leave an append-only, hash-chained
            # dispatch record — the tracker says WHERE it is, the log proves WHEN.
            if stage == "sent":
                from dispatch_log import log_dispatch
                log_dispatch(pid, "email", f"outreach {r['sector']} pack",
                             target=r.get("draft", ""))
            print(f"{pid}: {r['type']}/{r['sector']} → [{stage}] (recorded; dispatch still owner-gated)")
            return 0
    print(f"no prospect {pid}")
    return 1


def forecast() -> int:
    rows = load()
    by_stage: dict[str, int] = {}
    for r in rows:
        by_stage[r["stage"]] = by_stage.get(r["stage"], 0) + r.get("value_usd", 0)
    print("pipeline forecast by stage:")
    for s in STAGES:
        v = by_stage.get(s, 0)
        print(f"  {s:12s} ${v:>12,}")
    print(f"  {'TOTAL':12s} ${sum(by_stage.values()):>12,}")
    # honest conversion guard: only sent+ stages are real pipeline; draft-ready is pipeline possible
    real = sum(v for k, v in by_stage.items() if k in ("sent", "replied", "meeting", "proposal"))
    print(f"  (real-pipeline (post-dispatch) value: ${real:,})")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--advance", nargs=2, metavar=("ID", "STAGE"))
    ap.add_argument("--forecast", action="store_true")
    args = ap.parse_args()
    if args.list:
        return list_rows()
    if args.advance:
        return advance(args.advance[0], args.advance[1])
    if args.forecast:
        return forecast()
    list_rows()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())