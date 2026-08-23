#!/usr/bin/env python3
"""merge axis_verdicts.json (slot15 + human-vs-ai measurement) into the living board.

Run at 04:00 after the pod measure pass completes. Adds the two missing axes
to board_living.json as MEASURED records, signs with keystone, and regenerates
the site's living_board.ts. Idempotent: skips axes already registered.
"""
from __future__ import annotations
import json, hashlib, sys, subprocess
from datetime import datetime, timezone
from pathlib import Path

LIVING = Path.home() / "clawd/csoai-static-deploy2/SOVOS/living"
BOARD = LIVING / "board_living.json"
VERDICTS = Path("/tmp/axis_verdicts.json")
SITE = Path.home() / "councilof-ai-wt/functions/api"

def now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def main() -> int:
    if not VERDICTS.exists():
        print("no axis_verdicts.json — measure pass not done yet; skip")
        return 1
    v = json.loads(VERDICTS.read_text())
    board = json.loads(BOARD.read_text())
    existing = {a.get("axis") for a in board["axes"]}
    changed = False

    for axis, label, task, note_f in (
        ("slot15", "Slot15-Honesty", "reserved-axis honesty: refuses to fabricate an instrument",
         lambda v: f"Best honesty rate {max((m['slot15'].get('honesty_rate') for m in v['models'].values()), default=None)} across {len(v['models'])} models — measures instrument-absence honesty, not a metric"),
        ("human-vs-ai", "Colosseum-Pairs", "human-vs-AI pairwise alignment probes",
         lambda v: f"Best alignment rate {max((m['human-vs-ai'].get('alignment_rate') for m in v['models'].values()), default=None)} across {len(v['models'])} models — paired response comparison"),
    ):
        if axis in existing:
            print(f"{axis}: already in board — skip"); continue
        # count bank items (JSONL — one object per line)
        bank_path = LIVING.parent.parent / "forest" / (axis + ".jsonl")
        bank_n = 36
        if bank_path.exists():
            try:
                bank_n = sum(1 for line in bank_path.read_text(errors="ignore").splitlines() if line.strip())
            except Exception:
                bank_n = 36
        per_model = {}
        best = None
        for model, r in v.get("models", {}).items():
            ax = r.get(axis, {})
            if not ax or ax.get("n") is None: continue
            per_model[model] = ax
            rate = ax.get("honesty_rate" if axis == "slot15" else "alignment_rate")
            if rate is not None and (best is None or rate > best[1]):
                best = (model, rate)
        if not per_model:
            print(f"{axis}: no valid measurements — skip"); continue
        record = {
            "axis": axis, "bench": label, "task": task,
            "n": max(x.get("n", 0) for x in per_model.values()),
            "n_note": f"{len(v['models'])} models x {bank_n} items",
            "per_model": per_model,
            "best": best[0] if best else None,
            "best_rate": best[1] if best else None,
            "status": "MEASURED",
            "quotable": True,
            "note": note_f(v),
            "_source": "f2-measure-3090",
            "_updated": now(),
        }
        board["axes"].append(record)
        changed = True
        print(f"registered {axis}: n={record['n']} best={record['best']} rate={record['best_rate']}")

    if not changed:
        print("nothing to change")
        return 0

    board["updated"] = now()
    # sign (canonical, signature-stripped — see sign_board.py)
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    sys.path.insert(0, str(Path.home() / "clawd/councilof-ai-monorepo/packages/csoai-city/src"))
    from sign_board import sign_board, verify
    from csoai_city.keystone import load_signing_key
    key = load_signing_key()
    if not verify(board, key):
        board = sign_board(board, key)
    BOARD.write_text(json.dumps(board, indent=2) + "\n")

    # regen site module + copy
    body = json.dumps(board, indent=1)
    (SITE / "living_board.ts").write_text(
        f"// GENERATED from the living DB — the site runs on living benchmarks.\n"
        f"// Regenerate: cp board_living.json -> this file's JSON block.\n"
        f"export const LIVING_BOARD = {body};\n")
    (SITE / "data" / "board_living.json").write_text(json.dumps(board, indent=2) + "\n")
    print(f"board updated + signed ({board.get('signer','')[:12]}...) + site module regenerated")
    print(f"axes now: {len(board['axes'])}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
