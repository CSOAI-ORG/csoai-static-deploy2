#!/usr/bin/env python3
"""care_gate_eval.py — measure v1 (LLM-only) vs v2 (deterministic + advisory LLM)
against the adversarial battery. Reports BOTH failure directions.

Recall alone is meaningless here: a gate that refuses everything scores 1.00 recall and is
useless. Over-blocking (refusing legitimate audit/policy/legal questions) is reported with
equal weight, and the BENIGN_NEAR items exist specifically to catch it.

    python3 care_gate_eval.py            # deterministic tier only (fast, free, no model)
    python3 care_gate_eval.py --with-llm # include the advisory LLM tier
"""
from __future__ import annotations

import argparse, json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

from care_battery import BATTERY, stats
from care_gate_v2 import gate, tier2_soft_score, FLOOR


def evaluate(use_llm: bool) -> dict:
    tp = fp = tn = fn = 0
    by_diff = defaultdict(lambda: {"tp": 0, "fn": 0, "fp": 0, "tn": 0})
    misses, overblocks = [], []

    for text, should_breach, cat, diff in BATTERY:
        r = gate(text, use_llm=use_llm)
        breached = r["breach"]
        if should_breach and breached:
            tp += 1; by_diff[diff]["tp"] += 1
        elif should_breach and not breached:
            fn += 1; by_diff[diff]["fn"] += 1
            misses.append({"text": text, "category": cat, "difficulty": diff})
        elif not should_breach and breached:
            fp += 1; by_diff[diff]["fp"] += 1
            overblocks.append({"text": text, "tier": r["tier"], "reason": r["reason"]})
        else:
            tn += 1; by_diff[diff]["tn"] += 1

    n_harm, n_benign = tp + fn, tn + fp
    return {
        "recall": round(tp / n_harm, 3) if n_harm else 0.0,
        "precision": round(tp / (tp + fp), 3) if (tp + fp) else 0.0,
        "overblock_rate": round(fp / n_benign, 3) if n_benign else 0.0,
        "tp": tp, "fn": fn, "fp": fp, "tn": tn,
        "by_difficulty": {k: dict(v) for k, v in by_diff.items()},
        "missed_harms": misses, "overblocked": overblocks,
    }


def llm_only_baseline() -> dict:
    """v1 behaviour: LLM scorer alone decides. The thing measured as a rubber stamp."""
    tp = fp = tn = fn = 0
    for text, should_breach, _, _ in BATTERY:
        breached = tier2_soft_score(text) < FLOOR
        if should_breach and breached: tp += 1
        elif should_breach: fn += 1
        elif breached: fp += 1
        else: tn += 1
    n_harm, n_benign = tp + fn, tn + fp
    return {"recall": round(tp / n_harm, 3) if n_harm else 0.0,
            "overblock_rate": round(fp / n_benign, 3) if n_benign else 0.0,
            "tp": tp, "fn": fn, "fp": fp, "tn": tn}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--with-llm", action="store_true")
    ap.add_argument("--baseline", action="store_true", help="also run the v1 LLM-only baseline (slow)")
    a = ap.parse_args()

    s = stats()
    print(f"  battery: {s['total']} items ({s['harmful']} harmful / {s['benign']} benign)")
    print(f"  difficulty mix: {s['by_difficulty']}\n")

    v2 = evaluate(use_llm=a.with_llm)
    print(f"  === CARE GATE v2 {'(deterministic + LLM advisory)' if a.with_llm else '(deterministic tier only)'} ===")
    print(f"    harm RECALL      : {v2['recall']:.3f}   ({v2['tp']}/{v2['tp']+v2['fn']} caught)")
    print(f"    OVER-BLOCK rate  : {v2['overblock_rate']:.3f}  ({v2['fp']}/{v2['fp']+v2['tn']} benign wrongly refused)")
    print(f"    by difficulty    : ", {k: f"{v['tp']}/{v['tp']+v['fn']}" for k, v in v2["by_difficulty"].items() if v['tp']+v['fn']})
    if v2["missed_harms"]:
        print(f"    ⚠️  MISSED {len(v2['missed_harms'])} harm(s) — the honest cost of determinism:")
        for m in v2["missed_harms"][:6]:
            print(f"        [{m['difficulty']:11}] {m['text'][:62]}")
    if v2["overblocked"]:
        print(f"    ⚠️  OVER-BLOCKED {len(v2['overblocked'])} legitimate request(s):")
        for o in v2["overblocked"][:6]:
            print(f"        ({o['reason']}) {o['text'][:60]}")

    out = {"timestamp": datetime.now(timezone.utc).isoformat(), "battery": s, "v2": v2}

    if a.baseline:
        print("\n  === v1 BASELINE (LLM scorer alone — the rubber stamp) ===")
        b = llm_only_baseline()
        print(f"    harm RECALL      : {b['recall']:.3f}   ({b['tp']}/{b['tp']+b['fn']} caught)")
        print(f"    OVER-BLOCK rate  : {b['overblock_rate']:.3f}")
        out["v1_llm_only"] = b
        print(f"\n  Δ recall (v2 − v1): {v2['recall'] - b['recall']:+.3f}")

    p = Path("benchmark-results/care_gate_eval.json")
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(out, indent=2))
    print(f"\n  -> {p}")


if __name__ == "__main__":
    main()
