#!/usr/bin/env python3
"""daily_index.py — the GSPC Daily Index (closing-cross pattern).

The Nasdaq Closing Cross applied to measurement: fixed-time batch
aggregation of the day's verified measurements → ONE official signed value
that downstream parties cite. The index is the settlement price of the agent
economy, not a dashboard.

Usage:
    python3 daily_index.py --boards SOVOS/boards-v2-2026-08-12 \
        --date 2026-08-15 \
        --output SOVOS/register/index/2026-08-15.json
"""

from __future__ import annotations
import argparse, hashlib, json, sys
from datetime import datetime, timezone
from pathlib import Path

# Pre-committed index constitution (public, fixed weights)
AXES = ["gov", "prv", "care", "safety", "art5", "mcp", "jail", "affect",
        "agn", "agi", "xr", "oss", "det", "log"]


def wilson(acc: float, n: int, z: float = 1.96) -> tuple[float, float]:
    """Wilson 95% CI on a proportion."""
    if n <= 0:
        return 0.0, 0.0
    p = acc
    denom = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    margin = z * ((p * (1 - p) / n + z * z / (4 * n * n)) ** 0.5) / denom
    return max(0.0, centre - margin), min(1.0, centre + margin)


def axis_cell(boards_dir: Path, axis: str) -> dict:
    bf = boards_dir / f"board_{axis}.json"
    if not bf.exists():
        return {"axis": axis, "measured": False, "usable_n": 0, "accuracy": 0.0,
                "ci": [0.0, 0.0]}
    data = json.loads(bf.read_text())
    models = data.get("models", [])
    if models:
        # Board shape: per-model entries {model, n, correct, unparsed, accuracy, ci95, quotable}
        quotable = [m for m in models if m.get("quotable")]
        if quotable:
            acc = sum(m["accuracy"] for m in quotable) / len(quotable)
            n = sum(m.get("n", 0) for m in quotable)
            los = [m["ci95"][0] for m in quotable]
            his = [m["ci95"][1] for m in quotable]
            return {"axis": axis, "measured": True, "usable_n": n,
                    "accuracy": round(acc, 4),
                    "ci": [round(sum(los) / len(los), 4), round(sum(his) / len(his), 4)]}
    return {"axis": axis, "measured": False, "usable_n": 0, "accuracy": 0.0,
            "ci": [0.0, 0.0]}


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--boards", required=True, help="boards-v2 dir")
    p.add_argument("--date", default=datetime.now(timezone.utc).date().isoformat())
    p.add_argument("--output", default="-")
    p.add_argument("--seed", default="0" * 64)
    args = p.parse_args()

    boards = Path(args.boards)
    cells = [axis_cell(boards, a) for a in AXES]
    measured = [c for c in cells if c.get("measured")]
    n = len(measured)
    if n:
        value = round(100.0 * sum(c["accuracy"] for c in measured) / n, 2)
        lo = sum(c["ci"][0] for c in measured) / n
        hi = sum(c["ci"][1] for c in measured) / n
    else:
        value, lo, hi = None, None, None

    record = {
        "schema": "gspc-index-closing-cross-v1",
        "date": args.date,
        "index": value,
        "ci95": [round(lo, 4), round(hi, 4)] if lo is not None else None,
        "axes_measured": n,
        "axes_total": len(AXES),
        "constitution": ("equal-weighted mean of axis accuracies, 14 axes, "
                         "fixed weights, change via methodology policy"),
        "cells": cells,
        "created": datetime.now(timezone.utc).isoformat(),
    }
    canon = json.dumps(record, sort_keys=True, separators=(",", ":")).encode()
    digest = hashlib.sha256(canon).hexdigest()
    sig = hashlib.sha256(
        bytes.fromhex(args.seed[:32]) + bytes.fromhex(digest[:32])
    ).hexdigest()[:64]
    record["digest"] = digest
    record["signature"] = sig

    out = json.dumps(record, indent=1)
    if args.output and args.output != "-":
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        Path(args.output).write_text(out + "\n")
        print(f"✅ index {args.date}: value={value} ({n}/{len(AXES)} axes measured), signed")
    else:
        print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())