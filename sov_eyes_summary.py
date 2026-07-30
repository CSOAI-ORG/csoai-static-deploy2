#!/usr/bin/env python3
"""sov_eyes_summary.py — write sov-sync-summary.json from the ledger.

sov-sync-proof.html + sov-three-eyes.html fetch this file to know the ledger
hash and event count. Cheaper than calling the Python server.

    python3 sov_eyes_summary.py         # writes sov-sync-summary.json
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from sov_time import load_events, LEDGER
from sov_sync import ledger_summary

OUTPUT = HERE / "sov-sync-summary.json"


def main() -> int:
    s = ledger_summary()
    OUTPUT.write_text(json.dumps(s, indent=2))
    print(f"wrote {OUTPUT}: events={s['events']} hash={s['hash']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
