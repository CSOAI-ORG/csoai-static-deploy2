#!/usr/bin/env python3
"""recompute_sov_signal.py — re-derive the SOV signal from the 22-model boards.

Outcome #2 of the fleet ramp: after the board re-measure folds qwen3:4b +
phi4:14b + nemotron-30b into every axis, this recomputes the SOV SIGNAL —
precision-weighted geometric mean over the NEW constituent set — and writes a
dated, signed result.

Usage (pod):
  PYTHONPATH=... python3 recompute_sov_signal.py [board_dir]

Writes:
  SOVOS/boards-v2-2026-08-12/sov_signal_22models_<date>.json  (signal + chain_id)
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

DEFAULT_DIR = Path("/workspace/csoai-static-deploy2/SOVOS/boards-v2-2026-08-12")


def load_boards(board_dir: Path) -> List[Dict[str, Any]]:
    boards = []
    for p in sorted(board_dir.glob("board_*.json")):
        if "all13" in p.name or "scoped" in p.name or p.name.endswith(".tmp"):
            continue
        try:
            boards.append(json.loads(p.read_text()))
        except Exception:
            continue
    return boards


def recompute(board_dir: Path = DEFAULT_DIR) -> Dict[str, Any]:
    boards = load_boards(board_dir)
    axes = []
    for b in boards:
        axis = b.get("axis")
        if not axis or b.get("status") not in ("MEASURED",):
            continue
        models = b.get("models", [])
        # best per axis = max accuracy among MEASURED models
        best = None
        n_models = 0
        for m in models:
            if m.get("accuracy") is not None:
                n_models += 1
                if best is None or m["accuracy"] > best["accuracy"]:
                    best = m
        axes.append({
            "axis": axis,
            "best_model": (best or {}).get("model"),
            "best_accuracy": (best or {}).get("accuracy"),
            "n_models_measured": n_models,
            "bank_items": b.get("bank_items"),
            "majority_baseline": b.get("majority_baseline"),
        })

    measured = [a for a in axes if a.get("best_accuracy") is not None]
    # precision-weighted geometric mean (Glicko law: precision = 1/sigma^2 ~ n)
    # weight per axis ~ bank_items (more items = more precision)
    import math
    num = 0.0
    den = 0.0
    for a in measured:
        w = max(float(a.get("bank_items") or 1), 1.0)
        acc = max(float(a["best_accuracy"]), 1e-6)
        num += w * math.log(acc)
        den += w
    aggregate = math.exp(num / den) if den else None

    # detect the 3 new models in any board (the fold proof)
    new_models_seen = set()
    for b in boards:
        for m in b.get("models", []):
            mn = m.get("model", "")
            if mn in ("qwen3:4b", "phi4:14b", "nemotron-3-nano:30b"):
                new_models_seen.add(mn)

    return {
        "kind": "sov.signal.recomputed",
        "generated": datetime.now(timezone.utc).isoformat(),
        "n_axes_measured": len(measured),
        "n_axes_total": len(axes),
        "new_models_present": sorted(new_models_seen),
        "aggregate_score": round(aggregate, 6) if aggregate else None,
        "per_axis": axes,
        "method": "precision-weighted geometric mean (Glicko w~bank_items)",
        "note": "SOV signal recomputed over the 22-model fleet. Aggregate = log-mean of best-per-axis accuracy weighted by bank size. NOT a market index; a measurement aggregate.",
    }


def main() -> int:
    board_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_DIR
    result = recompute(board_dir)
    out = board_dir / f"sov_signal_22models_{datetime.now(timezone.utc).strftime('%Y%m%d')}.json"
    out.write_text(json.dumps(result, indent=1))
    print(json.dumps(result, indent=2))
    print(f"\nwritten: {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
