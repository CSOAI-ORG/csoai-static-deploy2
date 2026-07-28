#!/usr/bin/env python3
"""mitosis.py — the division rule. The piece that makes the hive actually fractal.

═══════════════════════════════════════════════════════════════════════════════
WHAT WAS MISSING
═══════════════════════════════════════════════════════════════════════════════
The hive already has its anatomy: `family_cells` (4-split left/right × small/big),
`spawn_clans` (12 specialist layers), `master_hives` (5 groups), `sandwich_brain`
(IWM/OWM × Frozen/Fluid), `stigmergy` (traces the cluster reads back).

What it did not have is a rule for **when a cell divides**. Without one the structure is a
fixed three-level tree that we drew, not a fractal — the depth comes from the diagram rather
than from the domain. A fractal needs a recursion rule that fires on its own.

═══════════════════════════════════════════════════════════════════════════════
THE RULE: MITOSIS IS GATED ON EVIDENCE, NOT ON ARCHITECTURE
═══════════════════════════════════════════════════════════════════════════════
A cell divides when its workload contains a **distinction it can be shown to be failing to
make** — not when the diagram says four boxes. Formally, cell C serving dimensions D may
divide into daughters (A, B) iff there is a partition of D where:

    1. RESOLUTION   the split is decidable at the item counts we actually hold:
                    observed gap > minimum detectable effect at that n
    2. SEPARATION   the Wilson intervals of the two sides do not overlap
    3. LOAD         both daughters retain enough items to be measured at all

Every one of those is the same discipline applied everywhere else in this stack. Biological
mitosis is not a good analogy for architecture-driven splitting; a cell divides in response
to a signal, and a cell that divides without one is a tumour. A hive that spawns a daughter
per dimension because the diagram has boxes for them is generating structure, not capability
— and it will report that structure as though it were capability, which is the defect this
whole session has been about.

**PREDICTED OUTCOME, WRITTEN BEFORE RUNNING:** almost nothing will be allowed to divide.
0 of 15 dimensions currently resolve to a single model, all-tied in 13 of 15, and the
minimum detectable effect at n=5 is ≈63 points against observed margins of 1-15. If that is
what comes back, the correct output is **a shallow hive and a list of how many items each
cell needs before depth can be earned** — not a deeper one.

    python3 mitosis.py
    python3 mitosis.py --need     # items required before each blocked split is decidable
"""
from __future__ import annotations

import argparse, json, math, sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
OUT = HERE / "benchmark-results" / "mitosis.json"

MIN_DAUGHTER_ITEMS = 5      # below this a daughter cannot be measured, so it may not be born


def mde(n: int, p: float = 0.5) -> float:
    """Minimum detectable effect (percentage points) for a two-proportion comparison at
    n items per side, alpha=0.05, power=0.8. Below this, a gap is not evidence of anything.

    This is the number that makes the whole board honest: at n=5 it is ~63 points, and every
    per-dimension margin we have observed is 1-15."""
    if n < 2:
        return 100.0
    return min(100.0, (1.96 + 0.84) * math.sqrt(2 * p * (1 - p) / n) * 100)


def wilson(k: float, n: int, z: float = 1.96) -> tuple[float, float]:
    if n == 0:
        return 0.0, 1.0
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    m = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return max(0.0, (c - m) / d), min(1.0, (c + m) / d)


def cell_dimensions() -> dict[str, list[str]]:
    """The cells the hive currently has, and which dimensions each one owns."""
    from master_hives import HIVES
    return {name: list(h["dimensions"]) for name, h in HIVES.items()
            if h.get("dimensions")}


def board_scores() -> dict[str, float]:
    """Per-dimension score the hive can actually reach: the best model on that dimension.

    Reads the CORRECTED board — `rescore_absence_dims.json` overrides fairness and
    robustness, and `sov33-evolved-c2` is excluded as unreproducible. A division rule fed
    the retracted numbers would be deciding structure from a grader that paid for silence.

    2026-07-28 — the first version of this called `hive_table(name)[d]["score"]`, which is
    not what that function returns, and wrapped it in a bare `except Exception: scores = {}`.
    Every cell came back with zero dimensions and the tool printed a confident
    "0 of 5 cells may divide" — a conclusion produced entirely by a swallowed TypeError.
    No bare except here: if the board cannot be read, this raises and nothing is reported.
    """
    from rank_intervals import load
    models = load()
    rs = HERE / "benchmark-results" / "rescore_absence_dims.json"
    if rs.exists():
        r = json.loads(rs.read_text())
        for m in r["unreproducible_excluded"]:
            models.pop(m, None)
        for m, dd in r["scores"].items():
            if m in models:
                for d in r["dimensions_rescored"]:
                    if dd.get(d) is not None:
                        models[m][d] = dd[d]
    dims = next(iter(models.values()))
    return {d: max(mm[d] for mm in models.values()) for d in dims}


def best_partition(dims: list[str], scores: dict, n_items: dict) -> dict | None:
    """Search partitions of a cell's dimensions for the most separated 2-way split.

    Exhaustive for small dimension counts, which is all a cell ever has. Returns the
    candidate with the widest gap, along with everything needed to judge whether it is real.
    """
    if len(dims) < 2:
        return None
    best = None
    for mask in range(1, 2 ** (len(dims) - 1)):
        a = [d for i, d in enumerate(dims) if mask >> i & 1]
        b = [d for d in dims if d not in a]
        if not a or not b:
            continue
        na = sum(n_items.get(d, 0) for d in a)
        nb = sum(n_items.get(d, 0) for d in b)
        if na == 0 or nb == 0:
            continue
        # item-weighted mean score on each side
        sa = sum(scores[d] * n_items.get(d, 0) for d in a) / na
        sb = sum(scores[d] * n_items.get(d, 0) for d in b) / nb
        gap = abs(sa - sb)
        if best is None or gap > best["gap"]:
            lo_a, hi_a = wilson(sa / 100 * na, na)
            lo_b, hi_b = wilson(sb / 100 * nb, nb)
            best = {"a": a, "b": b, "n_a": na, "n_b": nb,
                    "score_a": round(sa, 1), "score_b": round(sb, 1), "gap": round(gap, 1),
                    "ci_a": [round(lo_a * 100, 1), round(hi_a * 100, 1)],
                    "ci_b": [round(lo_b * 100, 1), round(hi_b * 100, 1)]}
    return best


def judge(split: dict | None) -> tuple[bool, str]:
    """Apply the three gates. Any failure blocks division — a cell stays whole by default."""
    if split is None:
        return False, "cell owns fewer than 2 dimensions — nothing to partition"
    if split["n_a"] < MIN_DAUGHTER_ITEMS or split["n_b"] < MIN_DAUGHTER_ITEMS:
        return False, (f"LOAD: daughter would hold {min(split['n_a'], split['n_b'])} items "
                       f"(<{MIN_DAUGHTER_ITEMS}) — unmeasurable, so it may not be born")
    need = mde(min(split["n_a"], split["n_b"]))
    if split["gap"] < need:
        return False, (f"RESOLUTION: gap {split['gap']:.1f} < minimum detectable effect "
                       f"{need:.1f} at n={min(split['n_a'], split['n_b'])} — the gap is noise")
    if split["ci_a"][1] >= split["ci_b"][0] and split["ci_b"][1] >= split["ci_a"][0]:
        return False, (f"SEPARATION: Wilson intervals overlap "
                       f"({split['ci_a']} vs {split['ci_b']}) — one population, not two")
    return True, f"gap {split['gap']:.1f} clears MDE {need:.1f} and intervals are disjoint"


def items_needed(split: dict) -> int:
    """How many items per side would make this split decidable, at the observed gap.
    Converts 'blocked' into a number someone can go and earn."""
    if not split or split["gap"] <= 0:
        return 0
    p = 0.5
    n = ((1.96 + 0.84) ** 2 * 2 * p * (1 - p)) / ((split["gap"] / 100) ** 2)
    return int(math.ceil(n))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--need", action="store_true", help="show items required per blocked split")
    a = ap.parse_args()

    from govbench_eval import DIMENSIONS

    cells = cell_dimensions()
    n_items = {d: len(dd["tests"]) for d, dd in DIMENSIONS.items()}
    scores = board_scores()          # raises rather than silently emptying — see board_scores

    # A score and an item count from different item sets must never be combined. Adding 6
    # items to `ethics` silently changed every interval this tool computes, because n came
    # from DIMENSIONS (live) and the score came from the board (2026-07-27). Nothing caught
    # it. Dimensions whose item set moved after the board run are dropped, loudly.
    fp = HERE / "benchmark-results" / "board_fingerprints.json"
    stale = {}
    if fp.exists():
        stale = json.loads(fp.read_text()).get("stale_vs_board", {})
    if stale:
        print(f"  ⚠️  {len(stale)} dimension(s) changed after the board run — EXCLUDED:")
        for d, why in stale.items():
            print(f"        {d}: {why}")
        print(f"      Re-benchmark them before they can inform a division.\n")
    for d in stale:
        scores.pop(d, None)

    print(f"  MITOSIS — division rule over {len(cells)} master cells\n")
    print(f"  A cell divides only when the split is RESOLVED, SEPARATED and LOAD-BEARING.")
    print(f"  Default is to stay whole. Structure without evidence is not capability.\n")

    report, allowed = [], 0
    for name, dims in sorted(cells.items()):
        known = [d for d in dims if d in scores and d in n_items]
        if len(known) < len(dims):
            # Say what was dropped. A cell silently shrinking to nothing is how the first
            # version of this file produced its confident, meaningless answer.
            print(f"      note: {name} owns {sorted(set(dims) - set(known))} with no board "
                  f"score — excluded from its partition search")
        dims = known
        split = best_partition(dims, scores, n_items)
        ok, why = judge(split)
        allowed += ok
        icon = "🔬 DIVIDE" if ok else "⬤  WHOLE "
        print(f"  {icon}  {name}   ({len(dims)} dimensions, "
              f"{sum(n_items.get(d,0) for d in dims)} items)")
        print(f"            {why}")
        if split and a.need and not ok:
            need = items_needed(split)
            print(f"            best candidate: {split['a']} ({split['score_a']}%) vs "
                  f"{split['b']} ({split['score_b']}%)")
            print(f"            needs ~{need} items PER SIDE to decide "
                  f"(has {min(split['n_a'], split['n_b'])})")
        print()
        report.append({"cell": name, "dimensions": dims, "divides": ok, "reason": why,
                       "split": split, "items_needed_per_side": items_needed(split) if split else 0})

    print(f"  ═══ {allowed} of {len(cells)} cells may divide ═══\n")
    if allowed == 0:
        print(f"  The hive stays ONE LEVEL DEEP. Not a failure — the measurement does not yet")
        print(f"  support a second level, and a fractal drawn deeper than its evidence is a")
        print(f"  diagram, not an architecture. Depth is earned by items, and `--need` prints")
        print(f"  exactly how many each blocked split is waiting on.")

    OUT.write_text(json.dumps({
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "rule": "divide iff RESOLUTION and SEPARATION and LOAD",
        "cells_examined": len(cells), "cells_may_divide": allowed,
        "min_daughter_items": MIN_DAUGHTER_ITEMS, "report": report}, indent=2))
    print(f"  -> {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
