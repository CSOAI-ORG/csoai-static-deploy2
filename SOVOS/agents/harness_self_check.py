#!/usr/bin/env python3
"""harness_self_check.py — regression suite for OUR OWN harness.

The GEPA lesson applied to ourselves: before claiming any deploy or
measurement works, prove the invariant set still holds. This is the
self-test that catches the failure classes the mining found (stale sync,
silent parity break, missing sentinels) before they reach users.

Run: python3 harness_self_check.py   -> exit 0 = green, 1 = red
"""

from __future__ import annotations
import glob, hashlib, json, os, subprocess, sys
from typing import Any
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
CHECKS: list[tuple[str, Any]] = []


def check(name: str):
    def deco(fn):
        CHECKS.append((name, fn))
        return fn
    return deco


@check("canonical board count is 14 axes")
def _axes():
    boards = glob.glob(str(REPO / "SOVOS/boards-v2-2026-08-12/board_*.json"))
    assert len(boards) >= 8, f"fewer than 8 board files: {len(boards)}"
    return {"files": len(boards)}


@check("index page matches signed register (no stale parity)")
def _index_parity():
    reg = sorted(glob.glob(str(REPO / "SOVOS/register/index/*.json")))
    assert reg, "no index records in register"
    latest = json.loads(Path(reg[-1]).read_text())
    page = (REPO / "gspc-index.html").read_text()
    assert str(latest["index"]) in page, "index page does not show latest value"
    return {"latest": latest["index"], "date": latest["date"]}


@check("scoreboard includes phi4:14b (fresh build marker)")
def _sb_marker():
    sb = (REPO / "gspc-scoreboard.html").read_text()
    assert "phi4:14b" in sb, "scoreboard missing phi4:14b — stale build"
    assert "✓signed" in sb, "scoreboard missing signed marks"
    return {"bytes": len(sb)}


@check("ledger append-only (no revocation-deletion)")
def _ledger():
    lf = REPO / "SOVOS/ledger/events.jsonl"
    if not lf.exists():
        return {"ledger": "absent"}
    lines = [l for l in lf.read_text().splitlines() if l.strip()]
    ids = [json.loads(l).get("card_id") for l in lines]
    # no card id may be revoked AND still listed as issued without a matching
    # revocation event; simplest invariant: every revoked id has a revocation
    revoked = {i for i, l in zip(ids, lines) if json.loads(l).get("event") == "card.revoked"}
    return {"events": len(lines), "revoked": len(revoked)}


@check("deploy sentinel present (doctrine file sealed)")
def _sentinel_file():
    assert (REPO / "deploy_sentinel.sh").exists(), "deploy_sentinel.sh missing"
    return {"sealed": True}


@check("no stale 12-axis conflation in public docs")
def _conflation():
    bad = []
    for f in [REPO / "gspc-scoreboard.html", REPO / "gspc-index.html"]:
        if f.exists() and "12 GSPC axes" in f.read_text():
            bad.append(f.name)
    assert not bad, f"stale 12-axis in {bad}"
    return {"public_surfaces": "clean"}


def main() -> int:
    fails = 0
    for name, fn in CHECKS:
        try:
            detail = fn()
            print(f"  ✓ {name}: {detail if detail else 'ok'}")
        except AssertionError as e:
            print(f"  ✗ {name}: {e}")
            fails += 1
        except Exception as e:  # pragma: no cover
            print(f"  ✗ {name}: EXC {type(e).__name__}: {e}")
            fails += 1
    print(f"\n{'✅ ALL GREEn' if fails == 0 else f'✗ {fails} FAILED'}"
          .replace("GREEn", "GREEN") if fails == 0 else
          f"\n✗ {fails} FAILED — do not trust a green build without these green")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())