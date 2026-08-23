#!/usr/bin/env python3
"""rescore_robustness.py — re-measure the one dimension priced within reach.

`rank_intervals.items_to_resolve()` priced robustness at ~24 items per model to separate the
top two Wilson intervals — the cheapest of all 15 by 3.5x. It now holds 24. This re-scores
every board model on the new set and asks the only question that matters:

    does ANY dimension finally resolve?

PREDICTION, WRITTEN BEFORE RUNNING: ~24 is the *threshold* estimate from the observed 100.0 vs
85.7 gap, and that gap was measured at n=5 where a single item is worth 20 points. The true
gap will almost certainly shrink once there are 24 harder, more varied items — the expansion
deliberately added attack families the original five never probed. So I expect the gap to
narrow and the dimension to STILL NOT resolve. If it resolves, that is a genuine first and I
will say so; if it does not, the priced number simply moves up and that is the honest result.
"""
from __future__ import annotations
import json, sys, time
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))


def main() -> int:
    from govbench_eval import DIMENSIONS, grade_response, UngradedItem, all_fingerprints
    from system_bench import ask, Unreachable, preflight
    from rank_intervals import load as load_board, wilson, items_to_resolve

    models = sorted(load_board())
    dead = preflight(models)
    live = [m for m in models if m not in dead]
    tests = DIMENSIONS["robustness"]["tests"]
    print(f"  ROBUSTNESS re-board — {len(live)} models × {len(tests)} items\n")

    out, t0 = {}, time.time()
    for m in live:
        scores, unreachable = [], 0
        for t in tests:
            try:
                scores.append(grade_response(t, ask(m, t["q"])))
            except (Unreachable, UngradedItem, Exception):
                unreachable += 1        # UNMEASURED, never zero
        out[m] = {"pct": round(sum(scores) / len(scores) * 100, 1) if scores else None,
                  "n": len(scores), "unreachable": unreachable}
        print(f"    {m:30s} {out[m]['pct']:5}%  n={out[m]['n']:2d}  "
              f"{unreachable} unmeasured · {time.time()-t0:.0f}s", flush=True)

    scored = {m: v for m, v in out.items() if v["pct"] is not None}
    ranked = sorted(scored.items(), key=lambda kv: -kv[1]["pct"])
    n = len(tests)
    print(f"\n  WILSON INTERVALS at n={n}\n")
    rows = []
    for m, v in ranked:
        lo, hi = wilson(v["pct"] / 100 * n, n)
        rows.append((m, v["pct"], round(lo * 100, 1), round(hi * 100, 1)))
        print(f"    {m:30s} {v['pct']:5.1f}%  CI [{lo*100:5.1f}, {hi*100:5.1f}]")

    leader_lo = rows[0][2]
    tied = [r for r in rows if r[3] >= leader_lo]
    resolved = len(tied) == 1
    gap = rows[0][1] - rows[1][1] if len(rows) > 1 else 0.0
    need = items_to_resolve(rows[0][1] / 100, rows[1][1] / 100) if len(rows) > 1 else None

    print(f"\n  tied for first : {len(tied)} of {len(rows)}")
    print(f"  top-two gap    : {gap:.1f} points   (was 14.3 at n=5)")
    print(f"  re-priced      : {'TIED — no n fixes this' if need is None else f'~{need} items/model'}")
    print()
    if resolved:
        print(f"  ✅ RESOLVED — {rows[0][0]} is the first dimension winner the estate can publish.")
    else:
        print(f"  ❌ STILL UNRESOLVED at n={n}. {len(tied)} models remain statistically tied.")
        print(f"     The expansion was not wasted: the price is now measured on 24 real items")
        print(f"     rather than extrapolated from 5, and that estimate is the one to trust.")

    p = HERE / "benchmark-results" / "rescore_robustness.json"
    p.write_text(json.dumps({
        "timestamp": datetime.now(timezone.utc).isoformat(), "n_items": n,
        "fingerprint": all_fingerprints().get("robustness"),
        "scores": out, "intervals": rows, "n_tied": len(tied), "resolved": resolved,
        "top_two_gap": round(gap, 1), "repriced_items_needed": need,
        "prediction_before_running": "gap narrows on harder items; expect STILL UNRESOLVED",
    }, indent=2))
    print(f"  -> {p}")
    return 0
if __name__ == '__main__': raise SystemExit(main())
