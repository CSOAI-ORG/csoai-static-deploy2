#!/usr/bin/env python3
"""n_eff.py — how many INDEPENDENT votes does the quorum actually have?

═══════════════════════════════════════════════════════════════════════════════
WHY THIS EXISTS
═══════════════════════════════════════════════════════════════════════════════
The OWEM design calls for a 3-leg quorum, and the estate has repeatedly described that as
Byzantine-fault-tolerant. But all 17 sovereign variants are **system prompts over one shared
397MB blob**. Three copies of one model that agree because they are the same model is not a
quorum; it is one vote with extra latency and a longer log.

The correlated-error literature is blunt about this: Kim et al. (arXiv 2506.07962, ICML 2025,
350+ models) found models "agree 60% of the time when both models err", and same-architecture
pairs agree measurably more on wrong answers. "Nine Judges, Two Effective Votes"
(arXiv 2605.29800) reports a 9-judge panel collapsing to n_eff ≈ 2.0–2.4.

═══════════════════════════════════════════════════════════════════════════════
THE MEASURE
═══════════════════════════════════════════════════════════════════════════════
For each pair of legs, take the binary error vectors (1 = wrong, 0 = right) over the same
frozen items and compute the **phi coefficient** — Pearson correlation on two binary
variables, which for a 2×2 table is:

    phi = (n11*n00 - n10*n01) / sqrt((n11+n10)(n01+n00)(n11+n01)(n10+n00))

Then Kish's effective sample size for k voters with mean pairwise correlation phi_bar:

    n_eff = k / (1 + (k-1) * phi_bar)

At k=3: phi_bar 0.0 -> 3.0 · 0.2 -> 2.4 · 0.4 -> 1.9 · 1.0 -> 1.0

═══════════════════════════════════════════════════════════════════════════════
THE GATE
═══════════════════════════════════════════════════════════════════════════════
**Quorum value may not be claimed until measured n_eff materially exceeds 2** (target ≥2.4
for three legs, i.e. phi_bar ≤ ~0.2). If n_eff ≈ 2 with three legs, the third leg is dead
weight and the honest move is to say so rather than ship a council that votes with itself.

PREDICTION, WRITTEN BEFORE RUNNING: our legs share one blob, so I expect phi_bar well above
0.5 and n_eff close to 1. If that is what comes back, the BFT framing must be retired from
every document until architecturally distinct legs exist.

    python3 n_eff.py --legs sov33-dist-c1:latest sov33-dist-c2:latest sov33-dist-c3:latest
"""
from __future__ import annotations

import argparse, json, math, sys, time
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))


def phi(a: list[int], b: list[int]) -> float | None:
    """Phi coefficient on two binary error vectors. None when undefined."""
    n11 = sum(1 for x, y in zip(a, b) if x and y)
    n10 = sum(1 for x, y in zip(a, b) if x and not y)
    n01 = sum(1 for x, y in zip(a, b) if not x and y)
    n00 = sum(1 for x, y in zip(a, b) if not x and not y)
    den = math.sqrt((n11 + n10) * (n01 + n00) * (n11 + n01) * (n10 + n00))
    if den == 0:
        # A leg that is right on everything (or wrong on everything) has no variance, so
        # correlation is undefined. That is UNMEASURED — not zero, which would flatter n_eff.
        return None
    return (n11 * n00 - n10 * n01) / den


def kish(k: int, phi_bar: float) -> float:
    return k / (1 + (k - 1) * phi_bar)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--legs", nargs="+", required=True)
    ap.add_argument("--limit", type=int, default=0, help="cap items for a quick read")
    a = ap.parse_args()

    from govbench_eval import DIMENSIONS, grade_response, UngradedItem
    from system_bench import ask, Unreachable, preflight

    dead = preflight(a.legs)
    legs = [m for m in a.legs if m not in dead]
    if dead:
        print(f"  ⚠️  dead at preflight, excluded: {sorted(dead)}")
    if len(legs) < 2:
        print(f"  need ≥2 live legs, have {len(legs)}"); return 2

    items = [t for dd in DIMENSIONS.values() for t in dd["tests"]]
    if a.limit:
        items = items[: a.limit]

    print(f"  n_eff — {len(legs)} legs × {len(items)} items\n")
    print(f"  PREDICTION (pre-registered): these legs share one 397MB blob, so phi_bar should")
    print(f"  be well above 0.5 and n_eff close to 1.\n")

    # Error vectors, aligned on items scored by EVERY leg. An item any leg could not answer
    # is dropped from all of them — a ragged matrix would silently change which items each
    # correlation is computed over.
    raw: dict[str, dict[int, int]] = {m: {} for m in legs}
    t0 = time.time()
    for m in legs:
        for i, t in enumerate(items):
            try:
                raw[m][i] = 0 if grade_response(t, ask(m, t["q"])) >= 0.5 else 1
            except (Unreachable, UngradedItem, Exception):
                pass
        print(f"    {m:30s} {len(raw[m])}/{len(items)} scored · {time.time()-t0:.0f}s", flush=True)

    common = sorted(set.intersection(*(set(raw[m]) for m in legs)))
    if len(common) < 20:
        print(f"\n  only {len(common)} items scored by every leg — too few to correlate"); return 2
    vec = {m: [raw[m][i] for i in common] for m in legs}

    print(f"\n  {len(common)} items scored by every leg")
    print(f"  error rates: " + " · ".join(f"{m.split(':')[0]}={sum(vec[m])/len(common):.2f}" for m in legs))

    pairs, undefined = [], []
    print(f"\n  PAIRWISE ERROR CORRELATION (phi)")
    for i in range(len(legs)):
        for j in range(i + 1, len(legs)):
            p = phi(vec[legs[i]], vec[legs[j]])
            label = f"{legs[i].split(':')[0]} ↔ {legs[j].split(':')[0]}"
            if p is None:
                undefined.append(label)
                print(f"    {label:44s} UNDEFINED (a leg has no error variance)")
            else:
                pairs.append(p)
                print(f"    {label:44s} phi = {p:+.3f}")

    if not pairs:
        print(f"\n  no defined pairs — n_eff UNMEASURED"); return 2
    phi_bar = sum(pairs) / len(pairs)
    k = len(legs)
    ne = kish(k, phi_bar)

    print(f"\n  mean pairwise phi : {phi_bar:+.3f}   ({len(pairs)} defined pairs"
          f"{', ' + str(len(undefined)) + ' undefined' if undefined else ''})")
    print(f"  nominal votes     : {k}")
    print(f"  EFFECTIVE VOTES   : {ne:.2f}")

    passed = ne > 2.0
    print()
    if passed:
        print(f"  ✅ n_eff {ne:.2f} > 2 — the quorum carries more than one leg's worth of signal.")
    else:
        print(f"  ❌ GATE FAILED — n_eff {ne:.2f} does NOT exceed 2.")
        print(f"     {k} nominal legs are worth {ne:.2f} independent votes. The extra legs are")
        print(f"     latency, not redundancy, and Byzantine-fault-tolerance MAY NOT be claimed.")
        print(f"     Decorrelation needs a different ARCHITECTURE (an SSM leg), not different")
        print(f"     prompts over the same weights.")

    out = {"timestamp": datetime.now(timezone.utc).isoformat(), "legs": legs,
           "n_items": len(common), "pairwise_phi": [round(p, 4) for p in pairs],
           "undefined_pairs": undefined, "phi_bar": round(phi_bar, 4),
           "nominal_votes": k, "n_eff": round(ne, 3), "gate_passed": passed,
           "gate": "n_eff > 2.0 required before claiming quorum value",
           "prediction_before_running": "shared blob -> phi_bar > 0.5, n_eff near 1"}
    p = HERE / "benchmark-results" / "n_eff.json"
    p.write_text(json.dumps(out, indent=2))
    print(f"\n  -> {p}")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
