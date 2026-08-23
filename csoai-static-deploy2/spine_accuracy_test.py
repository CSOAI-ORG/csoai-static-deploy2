#!/usr/bin/env python3
"""spine_accuracy_test.py — measure the SOV1 spine's routing accuracy.

WHY THIS IS THE NUMBER THAT MATTERS:
owem_cluster reports a per-dimension ORACLE of 63.6% — the score IF every query reaches the
expert that wins its dimension. That is an upper bound, not a score. The spine is keyword-based
and its accuracy has never been measured.

    real cluster score  ≈  oracle × routing accuracy

Without this number, "our cluster scores 63.6%" is exactly the class of claim this estate keeps
having to retract. With it, the cluster has a defensible score.

GROUND TRUTH: GovBench's own DIMENSIONS dict. Every test question is already filed under the
dimension it belongs to — that labelling was done when the benchmark was written, independently
of the router. So it is genuine held-out ground truth, not something the router was tuned on.
"""
from __future__ import annotations
import json, sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from govbench_eval import DIMENSIONS
from owem_cluster import classify_dimension, build_expert_table


def main() -> int:
    pairs = [(t["q"], dim) for dim, d in DIMENSIONS.items() for t in d["tests"]]
    correct = 0
    confusion = defaultdict(Counter)
    misses = []
    for q, true_dim in pairs:
        pred = classify_dimension(q)
        confusion[true_dim][pred] += 1
        if pred == true_dim:
            correct += 1
        else:
            misses.append({"q": q[:64], "true": true_dim, "pred": pred})

    acc = correct / len(pairs)
    print(f"  SPINE ROUTING ACCURACY — {len(pairs)} labelled questions, {len(DIMENSIONS)} dimensions\n")
    print(f"    correct : {correct}/{len(pairs)}")
    print(f"    accuracy: {acc:.3f}\n")

    print("  PER-DIMENSION RECALL (did questions from this dimension route here?)")
    for dim in sorted(confusion):
        tot = sum(confusion[dim].values())
        hit = confusion[dim][dim]
        flag = "" if hit == tot else f"   -> {dict(confusion[dim])}"
        print(f"    {dim:15s} {hit}/{tot}{flag}")

    table, models = build_expert_table()
    if table:
        oracle = sum(v["score"] for v in table.values()) / len(table)
        avg = {m: sum(d.values()) / 15 for m, d in models.items()}
        best = max(avg.values())
        est = oracle * acc + best * (1 - acc)   # misrouted queries land on SOME expert, not zero
        print(f"\n  ORACLE (perfect routing)      : {oracle:.1f}%")
        print(f"  best single model             : {best:.1f}%")
        print(f"  ESTIMATED cluster score       : {est:.1f}%   (oracle x acc + best x (1-acc))")
        print(f"  net vs best single model      : {est-best:+.1f} pts")
        if est <= best:
            print(f"\n  ⚠️  At this routing accuracy the cluster does NOT beat the best single model.")
            print(f"     The spine is the bottleneck — fix routing before claiming a cluster gain.")

    if misses:
        print(f"\n  MISROUTED ({len(misses)}) — the spine's actual failure modes:")
        for m in misses[:10]:
            print(f"    {m['true']:14s} -> {m['pred']:14s}  {m['q']}")

    out = {"timestamp": datetime.now(timezone.utc).isoformat(),
           "questions": len(pairs), "correct": correct, "accuracy": round(acc, 4),
           "misrouted": misses}
    p = Path("benchmark-results/govbench/spine_accuracy.json")
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(out, indent=2))
    print(f"\n  -> {p}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
