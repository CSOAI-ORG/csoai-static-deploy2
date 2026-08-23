#!/usr/bin/env python3
"""system_analysis.py — paired significance analysis of a system-vs-base run.

Written BEFORE the n=195 result was known, so the test cannot be chosen to fit the outcome.
That matters: today a +9.4 headline at n=18 turned out to have a 95% CI of [-3.1, +22.0] with
13 of 18 items tied and one item supplying half the effect. The analysis is what caught it, and
an analysis chosen after seeing the data is not an analysis.

WHAT IT COMPUTES
  • **Paired** mean difference — the same items go to both arms, so pairing is free power
    (roughly 33% variance reduction at ρ=0.5) and unpaired tests here would be simply wrong.
  • 95% CI on the paired difference. **Crossing zero means no claim may be made.**
  • **Leave-one-out**: the largest single |Δ| is removed and the mean recomputed. If the headline
    moves materially, it rests on one item and is not a system result.
  • **Sign test** on wins vs losses, ignoring ties — distribution-free, and ties are the
    majority here so they must not be counted as evidence either way.
  • **Per-layer attribution** from the trace: how many items the gate blocked, how many the KB
    served. A win the gate did not participate in may not be credited to the gate.

    python3 system_analysis.py /tmp/sysbench_full.log
"""
from __future__ import annotations

import json, math, random, re, sys
from pathlib import Path


def parse_json(p: Path) -> tuple[list[float], list[str], list[str], int, int]:
    """Read the durable per-item rows written by system_bench.py.

    Preferred over parse(). The log path was the only carrier of per-item data until
    2026-07-29, it lived in /tmp, and it was lost — taking with it the ability to recompute
    the estate's single claimable result. Rows now travel inside the result file itself.
    """
    d = json.loads(p.read_text())
    rows = d.get("items")
    if not rows:
        raise KeyError(f"{p} has no 'items' — written by a build before rows were persisted")
    # Rows store grades in 0–1; the log path printed them already scaled to points, and every
    # published figure is in points. Scale here so the two input paths agree — they did not
    # when this function was first written, and the analysis cheerfully reported "+0.07 points".
    return ([r["delta"] * 100 for r in rows],
            ["🛑" if r["blocked"] else ("📚" if r["kb_hit"] else " ") for r in rows],
            [r["dim"] for r in rows],
            d.get("gate_blocked", 0), d.get("kb_served", 0))


def clustered_ci(deltas: list[float], clusters: list[str]) -> tuple[float, float, float, int]:
    """95% CI with a cluster-robust SE, clustering on dimension.

    Items inside a dimension share a rubric, a grader and a prompt family, so sd/sqrt(n)
    treats correlated draws as independent and reports an interval narrower than the
    evidence supports. This is the same error ProvBench caught in its own pooled interval —
    12 assets counted nine times gave [0.0%, 3.4%] where the honest figure was [0.0%, 24.2%].

    Returns (lo, hi, design_effect, n_clusters). A design effect near 1 means the clustering
    cost nothing; a large one means the naive interval was fiction.
    """
    n = len(deltas)
    mean = sum(deltas) / n
    groups: dict[str, list[float]] = {}
    for d, c in zip(deltas, clusters):
        groups.setdefault(c, []).append(d)
    g = len(groups)
    if g < 2:
        raise ValueError("cluster-robust SE needs ≥2 clusters")
    # CRVE for a mean: var = Σ_g (Σ_{i∈g} (dᵢ − mean))² / n², with the G/(G−1) small-G correction.
    ss = sum(sum(x - mean for x in xs) ** 2 for xs in groups.values())
    var = (g / (g - 1)) * ss / (n ** 2)
    se_c = math.sqrt(var)
    sd = math.sqrt(sum((x - mean) ** 2 for x in deltas) / (n - 1))
    se_naive = sd / math.sqrt(n)
    deff = (se_c / se_naive) ** 2 if se_naive else float("nan")
    return mean - 1.96 * se_c, mean + 1.96 * se_c, deff, g


def parse(log: Path) -> tuple[list[float], list[str], int, int]:
    deltas, marks = [], []
    gated = kb = 0
    for line in log.read_text().splitlines():
        m = re.search(r"^\s*(🛑|📚|)\s*(\w+)\s+sys=\s*([\d.]+)\s+base=\s*([\d.]+)", line)
        if not m:
            g = re.search(r"gate blocked (\d+) · KB served (\d+)", line)
            if g:
                gated, kb = int(g.group(1)), int(g.group(2))
            continue
        deltas.append(float(m.group(3)) - float(m.group(4)))
        marks.append(m.group(1) or " ")
    return deltas, marks, gated, kb


def binom_p(k: int, n: int) -> float:
    """Two-sided exact sign test. No scipy dependency — this must run anywhere."""
    if n == 0:
        return 1.0
    c = lambda a, b: math.comb(a, b)
    tail = sum(c(n, i) for i in range(0, min(k, n - k) + 1)) / (2 ** n)
    return min(1.0, 2 * tail)


def main() -> int:
    default = Path(__file__).parent / "benchmark-results" / "system_bench.json"
    src = Path(sys.argv[1]) if len(sys.argv) > 1 else default
    if not src.exists():
        print(f"  no input at {src}"); return 2
    clusters: list[str] | None = None
    if src.suffix == ".json":
        try:
            deltas, marks, clusters, gated, kb = parse_json(src)
        except KeyError as e:
            print(f"  ❌ CANNOT RECOMPUTE — {e}")
            print("     The summary in that file states a result whose per-item evidence no")
            print("     longer exists. It is not wrong; it is unverifiable. Re-run")
            print("     system_bench.py to regenerate rows, then analyse those.")
            return 2
    else:
        deltas, marks, gated, kb = parse(src)
    n = len(deltas)
    if n < 2:
        print(f"  only {n} items parsed — run not finished?"); return 2

    mean = sum(deltas) / n
    sd = math.sqrt(sum((d - mean) ** 2 for d in deltas) / (n - 1))
    se = sd / math.sqrt(n)
    lo, hi = mean - 1.96 * se, mean + 1.96 * se

    wins = [d for d in deltas if d > 0]
    losses = [d for d in deltas if d < 0]
    ties = [d for d in deltas if d == 0]
    p_sign = binom_p(len(losses), len(wins) + len(losses))

    biggest = max(deltas, key=abs)
    rest = list(deltas); rest.remove(biggest)
    mean_loo = sum(rest) / len(rest)

    print(f"  SYSTEM vs BASE — paired analysis, n={n}\n")
    print(f"    mean Δ        {mean:+6.2f} points")
    print(f"    sd            {sd:6.2f}     se {se:5.2f}")
    print(f"    95% CI        [{lo:+.2f}, {hi:+.2f}]")
    sig = not (lo < 0 < hi)
    print(f"    significant?  {'✅ YES — CI excludes zero' if sig else '❌ NO — CI crosses zero'}\n")

    # The naive interval above assumes 195 independent draws. They are not: items cluster by
    # dimension. Report the cluster-robust interval alongside, and let the DESIGN EFFECT say
    # how much the naive one was overstating.
    cluster_info: dict | None = None
    if clusters:
        clo, chi, deff, g = clustered_ci(deltas, clusters)
        csig = not (clo < 0 < chi)
        cluster_info = {"clusters": g, "design_effect": round(deff, 2),
                        "n_effective": round(n / deff, 1),
                        "ci_clustered": [round(clo, 2), round(chi, 2)],
                        "significant_clustered": csig}
        print(f"    clustered on {g} dimensions (items in a dimension share a rubric and grader)")
        print(f"    design effect {deff:5.2f}   → effective n ≈ {n / deff:.0f} of {n}")
        print(f"    95% CI        [{clo:+.2f}, {chi:+.2f}]")
        print(f"    survives?     {'✅ YES' if csig else '❌ NO — the naive interval was the only thing holding the claim'}\n")
        sig = sig and csig
    else:
        print("    ⚠️  clustering UNMEASURED — input carries no dimension labels, so the\n"
              "       interval above assumes independence it has not demonstrated.\n")
    print(f"    wins {len(wins)} · losses {len(losses)} · ties {len(ties)}")
    print(f"    sign test p   {p_sign:.4f}  {'(significant)' if p_sign < 0.05 else '(not significant)'}")
    print(f"    ties are {len(ties)/n*100:.0f}% of items — they are not evidence either way\n")
    print(f"    largest single Δ  {biggest:+.0f}")
    print(f"    mean without it   {mean_loo:+.2f}  (from {mean:+.2f})")
    fragile = abs(mean_loo - mean) > abs(mean) * 0.3
    print(f"    {'⚠️  headline moves >30% — it rests on one item' if fragile else '✅ robust to leaving out the biggest item'}\n")
    print(f"    LAYER ATTRIBUTION")
    print(f"      gate blocked  {gated:3d} / {n}")
    print(f"      KB served     {kb:3d} / {n}")
    if gated == 0:
        print(f"      ⚠️  the gate never fired — no part of this result may be credited to it")
    if kb == 0:
        print(f"      ⚠️  the KB never fired — no part of this result may be credited to it")

    # Three outcomes, never two. A run whose clustering was never measured has not earned
    # "CLAIMABLE" — it has earned "not yet refuted", and the difference must survive into the
    # artefact, because the artefact is what gets quoted on the website a week later.
    if not sig:
        verdict = "NOT CLAIMABLE — CI crosses zero"
    elif fragile:
        verdict = "NOT CLAIMABLE — rests on one item"
    elif cluster_info is None:
        verdict = "UNVERIFIED — clustering unmeasured; interval assumes independence"
    else:
        verdict = "CLAIMABLE"
    print(f"\n    VERDICT: {verdict}")
    out = {"n": n, "mean": round(mean, 2), "ci": [round(lo, 2), round(hi, 2)],
           "significant": sig, "wins": len(wins), "losses": len(losses), "ties": len(ties),
           "sign_test_p": round(p_sign, 4), "mean_leave_one_out": round(mean_loo, 2),
           "fragile": fragile, "gate_blocked": gated, "kb_served": kb, "verdict": verdict,
           "clustering": cluster_info or "UNMEASURED"}
    p = Path(__file__).resolve().parent / "benchmark-results" / "system_analysis.json"
    p.write_text(json.dumps(out, indent=2))
    print(f"    -> {p}")
    return 0


def selftest() -> int:
    """Validate clustered_ci against cases whose answers are known a priori.

    Written because the whole point of this function is to catch an interval that is too
    narrow, and a buggy version of it would fail in exactly the reassuring direction.
    """
    fails = []

    # 1. No within-cluster correlation → design effect ≈ 1, clustering costs nothing.
    # Two ways this test was wrong before it was right, both worth keeping as warnings:
    #   • clustering by i%12 with 12 even fixes parity inside a cluster — that silently builds
    #     the PERFECTLY-correlated case and reports the function broken when it is correct;
    #   • exactly-balanced clusters (5 up, 5 down) sum to zero deviation and give deff 0.00.
    # Genuine independence needs noise, not symmetry. Seeded, so this stays deterministic.
    rng = random.Random(7)
    d = [rng.gauss(3.0, 5.0) for _ in range(120)]
    c = [f"dim{i // 10}" for i in range(120)]
    _, _, deff, g = clustered_ci(d, c)
    if g != 12: fails.append(f"cluster count {g} != 12")
    if not 0.5 < deff < 1.6: fails.append(f"uncorrelated deff {deff:.2f} not ≈1")

    # 2. Perfect within-cluster correlation → effective n collapses to the cluster count,
    #    so deff should approach items-per-cluster (10 here).
    d = [float(i % 12) for i in range(120)]
    c = [f"dim{i % 12}" for i in range(120)]          # every item in a cluster identical
    _, _, deff, _ = clustered_ci(d, c)
    if deff < 5: fails.append(f"perfectly-correlated deff {deff:.2f} should approach 10")

    # 3. The interval must never come out NARROWER than the naive one when clusters are
    #    positively correlated — that direction of error is the dangerous one.
    lo_c, hi_c, _, _ = clustered_ci(d, c)
    mean = sum(d) / len(d)
    sd = math.sqrt(sum((x - mean) ** 2 for x in d) / (len(d) - 1))
    naive = 1.96 * sd / math.sqrt(len(d))
    if (hi_c - lo_c) / 2 < naive: fails.append("clustered interval narrower than naive")

    # 4. Fewer than two clusters is unmeasurable, not zero-variance.
    try:
        clustered_ci([1.0, 2.0], ["a", "a"]); fails.append("single cluster did not raise")
    except ValueError:
        pass

    for f in fails: print(f"  ❌ {f}")
    print(f"  {'✅ selftest 4/4' if not fails else f'❌ {len(fails)} failure(s)'}")
    return 1 if fails else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        raise SystemExit(selftest())
    raise SystemExit(main())
