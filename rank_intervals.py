#!/usr/bin/env python3
"""rank_intervals.py — report TIED SETS, not winners. The honest replacement for a leaderboard row.

═══════════════════════════════════════════════════════════════════════════════
WHY
═══════════════════════════════════════════════════════════════════════════════
We measured that 14 of 15 dimensions had a "winner" decided by less than one test item, and four
were exactly tied. Research then supplied the statistics, and the numbers are worse than the
margin analysis suggested:

  • **Minimum detectable effect at n=5, 80% power, α=0.05: δ ≈ 63 percentage points.**
    Our observed margins are ~1–15 points. We are two orders of magnitude below resolution.
  • **A 95% Wilson interval on 4/5 correct spans 37.5% – 96.4%** — ±29 points.
  • **15 dimensions × C(11,2) = 825 pairwise comparisons.** Uncorrected at α=0.05 you expect
    **~41 spurious "winners" from pure noise even if every model were identical.**
  • The four exact ties are not an anomaly — with a 6-valued score space (0/20/40/60/80/100 at
    n=5) and 11 models, ties are guaranteed by pigeonhole.

Miller (Anthropic, arXiv:2411.00640) puts the floor at **~1,000 items per comparison**; MMLU set
≥100 per subject; AILuminate uses 1,000 per hazard. We had 5.

═══════════════════════════════════════════════════════════════════════════════
WHAT THIS DOES INSTEAD
═══════════════════════════════════════════════════════════════════════════════
Reports each dimension as the SET OF MODELS STATISTICALLY TIED FOR FIRST, using Wilson score
intervals — the same move Chatbot Arena makes (models sharing a rank when their intervals
overlap). A dimension with 9 models in its tied set is telling the truth: we cannot distinguish
them, and printing one name would be a fabrication with a decimal point on it.

**Wilson, not normal-approximation**, because at n=5 the normal interval is badly wrong and can
run below 0 or above 1. Wilson stays inside [0,1] and is the standard recommendation for small n.

**HONEST LIMITS OF THIS FILE:**
- Wilson assumes independent Bernoulli trials. Our items are weighted and grouped by dimension,
  so a clustered SE (Miller Appendix A, implemented in `inspect_ai` as `stderr(cluster=)`) would
  be more correct. This is a floor on the uncertainty, not a ceiling.
- It does NOT do paired testing. Models see identical items, so a paired test (McNemar /
  Wilcoxon) would recover real power — roughly 33% variance reduction at ρ=0.5. No mainstream
  harness does this; `evalstats` and `hibayes` (UK AISI, built for <20 points per eval) do.
- No multiplicity correction here. With 825 comparisons, Benjamini–Hochberg is required before
  any pairwise claim is made.

    python3 rank_intervals.py
    python3 rank_intervals.py --json
"""
from __future__ import annotations

import argparse, glob, json, math, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
Z95 = 1.959963985


def wilson(k: float, n: int, z: float = Z95) -> tuple[float, float]:
    """Wilson score interval. Correct at small n where the normal approximation is not."""
    if n <= 0:
        return (0.0, 1.0)
    p = max(0.0, min(1.0, k / n))
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    m = z * math.sqrt(max(0.0, p * (1 - p) / n + z * z / (4 * n * n)))
    return (max(0.0, (c - m) / d), min(1.0, (c + m) / d))



def items_to_resolve(p1: float, p2: float) -> int | None:
    """Items per model needed for the top TWO Wilson intervals to separate.

    ═══════════════════════════════════════════════════════════════════════════
    WHY THIS IS NOT THE MARGIN TEST
    ═══════════════════════════════════════════════════════════════════════════
    `margin_report` asks a weaker question — is the winner decided by more than one item's
    worth of score? Three dimensions pass that. `rank_intervals` asks whether the top two
    confidence intervals actually separate, and **zero** pass it.

    Both are honest; they are not the same bar, and the stricter one is what gates a public
    ranking. Reporting "3 of 15 have a credible winner" without also saying "0 of 15 resolve"
    would be choosing the friendlier statistic after seeing both.

    This prices the gap: given the observed top-two scores, how many items would each model
    need before the intervals stop overlapping? Uses the normal approximation to the Wilson
    half-width, which is close enough to plan with and always stated as approximate.

    Returns None when the scores are equal — no n fixes an exact tie in the observed data.

    ═══════════════════════════════════════════════════════════════════════════
    ⚠️ MEASURED 2026-07-29 — ESTIMATES FROM SMALL n ARE SYSTEMATICALLY OPTIMISTIC
    ═══════════════════════════════════════════════════════════════════════════
    This priced `robustness` at ~24 items/model from a 100.0-vs-85.7 gap observed at n=5.
    Robustness was expanded to 24 and re-measured on all 10 models. Result:

        top-two gap   14.3 -> 8.4 points
        tied for first          10 of 10 — STILL UNRESOLVED
        re-priced               ~230 items/model

    **The estimate was ~10x optimistic**, and the reason is structural rather than bad luck:
    at n=5 a single item is worth 20 points, so observed gaps are inflated by the coarseness
    of the score space. Expanding the item set does not merely add precision — it reveals the
    gap was smaller than it looked, and a smaller gap needs quadratically more items.

    So: a price computed from n<20 is a LOWER BOUND, not a target. Treat it as "at least
    this many", re-price after every expansion, and trust the estimate derived from the
    largest n available. The priced list published on 2026-07-29 carries this caveat for
    every dimension still at n=5.
    """
    gap = abs(p1 - p2)
    if gap <= 0:
        return None
    # separation requires roughly: gap > z*(se1 + se2), se_i = sqrt(p_i(1-p_i)/n)
    z = 1.96
    import math
    spread = math.sqrt(p1 * (1 - p1)) + math.sqrt(p2 * (1 - p2))
    if spread == 0:
        return None
    n = (z * spread / gap) ** 2
    return int(math.ceil(n))

def load() -> dict:
    """Every downstream consumer of the board comes through here, so this is where a
    withdrawn model must be dropped — once, rather than in each caller. The raw result
    file is deliberately left on disk: it is the evidence for the withdrawal, and deleting
    it would remove the record of why the model is gone."""
    from withdrawn import is_withdrawn
    models = {}
    for f in glob.glob(str(HERE / "benchmark-results" / "govbench" / "*.json")):
        try:
            d = json.loads(Path(f).read_text())
        except Exception:
            continue
        for r in (d if isinstance(d, list) else [d]):
            if not isinstance(r, dict):
                continue
            dd = r.get("dimensions")
            if is_withdrawn(r.get("model", "")):
                continue
            if isinstance(dd, dict) and len(dd) == 15 and all(isinstance(v, (int, float)) for v in dd.values()):
                models[r["model"]] = dd
    return models


def report(as_json: bool = False) -> int:
    from govbench_eval import DIMENSIONS
    models = load()
    if len(models) < 2:
        print("  need >=2 measured models"); return 2
    dims = sorted(next(iter(models.values())))

    rows, n_pairs = [], 0
    for d in dims:
        n = len(DIMENSIONS[d]["tests"]) if d in DIMENSIONS else 5
        scored = []
        for m, dd in models.items():
            p = dd[d] / 100.0
            lo, hi = wilson(p * n, n)
            scored.append({"model": m, "score": dd[d], "lo": round(lo * 100, 1), "hi": round(hi * 100, 1)})
        scored.sort(key=lambda x: -x["score"])
        # Tied for first: anyone whose upper bound reaches the leader's lower bound.
        leader_lo = scored[0]["lo"]
        tied = [s for s in scored if s["hi"] >= leader_lo]
        n_pairs += len(models) * (len(models) - 1) // 2
        rows.append({"dimension": d, "n_items": n, "leader": scored[0]["model"],
                     "leader_score": scored[0]["score"],
                     "leader_ci": [scored[0]["lo"], scored[0]["hi"]],
                     "ci_width": round(scored[0]["hi"] - scored[0]["lo"], 1),
                     "tied_for_first": [s["model"] for s in tied],
                     "n_tied": len(tied), "resolved": len(tied) == 1})

    resolved = [r for r in rows if r["resolved"]]
    if as_json:
        print(json.dumps({"models": len(models), "dimensions": len(rows),
                          "resolved": len(resolved), "pairwise_comparisons": n_pairs,
                          "expected_false_winners_at_alpha_.05": round(n_pairs * 0.05, 1),
                          "rows": rows}, indent=2))
        return 0

    print(f"  RANK INTERVALS — {len(models)} models × {len(rows)} dimensions")
    print(f"  Wilson 95% intervals. A dimension is RESOLVED only if one model stands alone.\n")
    for r in sorted(rows, key=lambda x: x["n_tied"]):
        mark = "✅" if r["resolved"] else "⚠️ "
        print(f"    {mark} {r['dimension']:24s} n={r['n_items']:2d}  "
              f"{r['leader_score']:5.1f}%  CI [{r['leader_ci'][0]:5.1f}, {r['leader_ci'][1]:5.1f}]  "
              f"±{r['ci_width']/2:4.1f}  tied: {r['n_tied']}/{len(models)}")
    print(f"\n  {len(resolved)}/{len(rows)} dimensions RESOLVED to a single model.")
    print(f"  {n_pairs} pairwise comparisons across the board.")
    print(f"  At α=0.05 uncorrected, ~{n_pairs*0.05:.0f} spurious 'winners' are expected from")
    print(f"  pure noise even if every model were identical. Benjamini–Hochberg is required")
    print(f"  before any pairwise claim.")
    print(f"\n  Minimum detectable effect at n=5, 80% power: ~63 points. Our margins: 1–15.")
    print(f"  Miller (arXiv:2411.00640) floor: ~1,000 items per comparison. MMLU: ≥100/subject.")
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--json", action="store_true")
    raise SystemExit(report(ap.parse_args().json))
