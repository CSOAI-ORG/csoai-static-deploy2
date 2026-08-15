#!/usr/bin/env python3
"""bounded_sft_input.py — the free-lane SFT recipe input. (Moves 56-60)

SFT, not RLVR (arXiv 2501.12948: refusal/governance rewards are not verifiable —
keep SFT as the base, treat RLVR as bounded). This module selects a BALANCED,
bounded training set from the leak-guarded flywheel fuel and the honey KB:

  - only PRACTICE-derived pairs (held-out is law; the P1 writer already stripped them)
  - balanced: prefer ~50/50 refuse/answer behaviour so the model learns refusal,
    not a degenerate all-refuse or all-answer policy
  - bounded: --limit N (default 4,000) — free-lane T4-friendly size
  - deterministic: sorted by (model, item_id) so the recipe is reproducible

Emits training_data/sft_recipe_<date>.jsonl + prints the recipe card. This is the
INPUT contract for the Kaggle-T4 / free-lane training kernel; the kernel itself runs
on free infra and is NOT invoked here (zero spend).
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
FUEL_DIR = HERE / "training_data"
OUT_FILE = HERE / "training_data" / f"sft_recipe_{datetime.now(timezone.utc).strftime('%Y-%m-%d')}.jsonl"


def load_pairs() -> list[dict]:
    out = []
    for fp in sorted(FUEL_DIR.glob("flywheel_pairs_*.jsonl")):
        with fp.open() as f:
            for line in f:
                if not line.strip():
                    continue
                try:
                    d = json.loads(line)
                except Exception:
                    continue
                if d.get("source") != "flywheel":
                    continue
                out.append(d)
    return out


def select(pairs: list[dict], limit: int, refuse_frac: float = 0.5) -> tuple[list[dict], dict]:
    refuse = [p for p in pairs if p.get("behaviour") == "refuse"]
    answer = [p for p in pairs if p.get("behaviour") == "answer"]
    if not refuse or not answer:
        return [], {"candidate_pairs": len(pairs), "error": "need both refuse and answer pairs"}
    # deterministic order (reproducible recipe)
    refuse.sort(key=lambda p: (p.get("model", ""), p.get("prompt", "")))
    answer.sort(key=lambda p: (p.get("model", ""), p.get("prompt", "")))
    n_refuse = min(int(limit * refuse_frac), len(refuse))
    n_answer = min(limit - n_refuse, len(answer))
    # balance guard: if one behaviour is critically scarce (<25% of corpus), cap the
    # other side so the recipe never degenerates into an all-one-behaviour dump.
    avail_frac = min(len(refuse), len(answer)) / max(1, len(refuse) + len(answer))
    if avail_frac < 0.25:
        scarce = min(len(refuse), len(answer))
        n_refuse = min(n_refuse, scarce)
        n_answer = min(n_answer, scarce)
    sel = (refuse[:n_refuse] + answer[:n_answer])
    # enforce the limit deterministically
    sel.sort(key=lambda p: (p.get("model", ""), p.get("prompt", "")))
    sel = sel[:limit]
    card = {
        "candidate_pairs": len(pairs), "refuse_available": len(refuse),
        "answer_available": len(answer), "selected": len(sel),
        "selected_refuse": sum(1 for p in sel if p.get("behaviour") == "refuse"),
        "selected_answer": sum(1 for p in sel if p.get("behaviour") == "answer"),
        "limit": limit, "method": "deterministic balanced (SFT base, no RLVR)",
        "guard": "practice-derived only (held-out stripped at the writer)",
    }
    return sel, card


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=4000)
    ap.add_argument("--refuse-frac", type=float, default=0.5)
    args = ap.parse_args()
    pairs = load_pairs()
    sel, card = select(pairs, args.limit, args.refuse_frac)
    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with OUT_FILE.open("w") as f:
        for p in sel:
            f.write(json.dumps(p) + "\n")
    print(json.dumps(card, indent=2))
    print(f"wrote {OUT_FILE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())