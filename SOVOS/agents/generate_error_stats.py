#!/usr/bin/env python3
"""generate_error_stats.py — aggregate the card-event ledger into published error statistics.

Implements the ERROR_STATISTICS_FORMAT policy: quarterly, machine-readable,
signed. The self-published error rate IS the credibility moat.

Usage:
    python3 generate_error_stats.py --ledger SOVOS/ledger/events.jsonl \
        --output SOVOS/register/error-stats/2026-Q3.json
"""

from __future__ import annotations
import argparse, hashlib, json, sys
from collections import Counter
from pathlib import Path


def load_events(path: Path) -> list[dict]:
    events = []
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        events.append(json.loads(line))
    return events


def aggregate(events: list[dict], period_prefix: str = "") -> dict:
    """Count card lifecycle events into the published metrics."""
    counts = Counter()
    for ev in events:
        # optional period filter: only events whose ts starts with prefix
        if period_prefix and not ev.get("ts", "").startswith(period_prefix):
            continue
        counts[ev.get("event")] += 1

    issued = counts.get("card.issued", 0)
    revoked = counts.get("card.revoked", 0)
    corrected = counts.get("card.corrected", 0)
    drifted = counts.get("card.watch", 0)  # watch raised = drift flag
    verified = counts.get("card.verified", 0)
    disputes_filed = counts.get("card.dispute_filed", 0)
    disputes_upheld = counts.get("card.dispute_upheld", 0)
    disputes_rejected = counts.get("card.dispute_rejected", 0)

    def rate(n, denom):
        return round(n / denom, 4) if denom else 0.0

    return {
        "period": period_prefix or "all",
        "cards_issued": issued,
        "revoked": revoked,
        "revocation_rate": rate(revoked, issued),
        "corrected": corrected,
        "correction_rate": rate(corrected, issued),
        "drift_flags": drifted,
        "drift_rate": rate(drifted, issued),
        "disputes": {
            "filed": disputes_filed,
            "upheld": disputes_upheld,
            "rejected": disputes_rejected,
            "open": disputes_filed - disputes_upheld - disputes_rejected,
        },
        "verifications": {
            "attempted": verified,
            "passed": counts.get("card.verified_passed", 0),
            "failed": counts.get("card.verified_failed", 0),
        },
    }


def sign(stats: dict, seed: str = "0" * 64) -> dict:
    canonical = json.dumps(stats, sort_keys=True, separators=(",", ":")).encode()
    digest = hashlib.sha256(canonical).hexdigest()
    signature = hashlib.sha256(
        bytes.fromhex(seed[:32]) + bytes.fromhex(digest[:32])
    ).hexdigest()[:64]
    return {**stats, "digest": digest, "signature": signature}


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--ledger", required=True, help="path to events.jsonl")
    p.add_argument("--output", default="-", help="output path or - for stdout")
    p.add_argument("--period", default="", help="e.g. 2026-Q3")
    p.add_argument("--pubkey-seed", default="0" * 64,
                   help="signing seed (estate key in production)")
    args = p.parse_args()

    events = load_events(Path(args.ledger)) if Path(args.ledger).exists() else []
    stats = sign(aggregate(events, args.period), args.pubkey_seed)

    out = json.dumps(stats, indent=2)
    if args.output and args.output != "-":
        Path(args.output).write_text(out + "\n")
        print(f"✅ error stats written: {args.output} ({len(out)} bytes)")
    else:
        print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())