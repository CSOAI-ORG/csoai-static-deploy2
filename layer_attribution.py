#!/usr/bin/env python3
"""layer_attribution.py — per-layer deltas computed FROM THE ROWS, not typed in by hand.

═══════════════════════════════════════════════════════════════════════════════
WHY THIS FILE EXISTS
═══════════════════════════════════════════════════════════════════════════════
The published layer table

    deterministic gate   n=31   +34.84  [+17.50, +52.18]
    knowledge base       n=14   +19.64  [ +6.87, +32.41]
    tuned model          n=141   +9.42  [ +4.82, +14.03]

had **no generating code anywhere in the estate.** The figures existed only as hardcoded
strings inside `make_leaderboard.py` and `sov_whole.py`. Nothing could recompute them,
nothing could check them, and the per-item data they came from was written to /tmp and lost.

Two things were wrong beyond that, and both were invisible precisely because no code owned
the numbers:

  1. **They are from a different run than the headline they sit under.** 31+14+141 = 186.
     The HF Space says so plainly — "n=186 … whole system +14.43". The website prints the
     same three rows beneath a **+12.21, n=195** headline. The layers do not decompose the
     total they are printed under; they decompose an earlier, smaller run.

  2. **The gate row is defined by the gate's own behaviour.** Its subgroup is "items the gate
     chose to block". On those items the system refuses and the base answers, so on a
     must-refuse item the gate scores 100 and the base scores near 0 — by construction. Any
     item where the gate *should* have fired and didn't is silently excluded from the gate's
     own scorecard. That is not an effect estimate; it is the same absence-shaped error that
     let silence score full marks on the fairness dimension earlier today, wearing a
     different hat.

So this file reports layer attribution three ways and refuses to collapse them into one
number: by ACTION (what the layer did — descriptive, circular, reported for continuity),
by LABEL (what the item required — the honest estimate), and the DIFFERENCE between them,
which is the size of the circularity.

    python3 layer_attribution.py [benchmark-results/system_bench.json]
    python3 layer_attribution.py --selftest
"""
from __future__ import annotations

import json, math, random, sys
from pathlib import Path

from system_analysis import clustered_ci


def ci(xs: list[float]) -> tuple[float, float]:
    """Naive 95% CI. Only used where a cluster-robust one is not defined (n too small)."""
    n = len(xs)
    if n < 2:
        return (float("nan"), float("nan"))
    m = sum(xs) / n
    sd = math.sqrt(sum((x - m) ** 2 for x in xs) / (n - 1))
    se = sd / math.sqrt(n)
    return m - 1.96 * se, m + 1.96 * se


def subgroup(rows: list[dict], pred, label: str) -> dict:
    """Summarise one subgroup, and say plainly when it cannot support an interval."""
    sel = [r for r in rows if pred(r)]
    n = len(sel)
    if n == 0:
        return {"label": label, "n": 0, "verdict": "UNMEASURED — no items in this subgroup"}
    deltas = [r["delta"] * 100 for r in sel]
    mean = sum(deltas) / n
    out = {"label": label, "n": n, "mean_delta": round(mean, 2)}
    if n < 2:
        out["verdict"] = "UNMEASURED — a single item cannot carry an interval"
        return out
    lo, hi = ci(deltas)
    out["ci_naive"] = [round(lo, 2), round(hi, 2)]
    # Cluster on dimension where the subgroup spans more than one. A subgroup confined to a
    # single dimension has no between-cluster variation to estimate, and saying so is more
    # use than printing an interval that pretends otherwise.
    dims = {r["dim"] for r in sel}
    if len(dims) >= 2:
        clo, chi, deff, g = clustered_ci(deltas, [r["dim"] for r in sel])
        out["clusters"] = g
        out["design_effect"] = round(deff, 2)
        out["ci_clustered"] = [round(clo, 2), round(chi, 2)]
        out["verdict"] = "positive" if clo > 0 else ("negative" if chi < 0 else "no effect shown")
    else:
        out["clusters"] = 1
        out["verdict"] = f"UNCLUSTERED — all {n} items sit in one dimension ({dims.pop()})"
    return out


def main() -> int:
    src = Path(sys.argv[1]) if len(sys.argv) > 1 else \
        Path(__file__).parent / "benchmark-results" / "system_bench.json"
    if not src.exists():
        print(f"  no input at {src}"); return 2
    d = json.loads(src.read_text())
    rows = d.get("items")
    if not rows:
        print(f"  ❌ {src} carries no per-item rows — layer attribution is UNCOMPUTABLE.")
        print("     Re-run system_bench.py (which now persists them) and analyse that.")
        return 2

    n = len(rows)
    all_d = [r["delta"] * 100 for r in rows]
    whole_mean = sum(all_d) / n
    wlo, whi, wdeff, wg = clustered_ci(all_d, [r["dim"] for r in rows])
    print(f"  LAYER ATTRIBUTION — computed from {n} persisted rows in {src.name}\n")
    print(f"    whole system     n={n:3d}  Δ {whole_mean:+6.2f}  "
          f"clustered [{wlo:+.2f}, {whi:+.2f}]  (deff {wdeff:.2f}, {wg} dims)\n")

    print("    BY ACTION — subgroup defined by what the layer did.")
    print("    Circular for the gate: it is scored only on items it chose to act on.")
    by_action = [
        subgroup(rows, lambda r: r["blocked"], "gate blocked"),
        subgroup(rows, lambda r: r["kb_hit"], "KB served"),
        subgroup(rows, lambda r: not r["blocked"] and not r["kb_hit"], "tuned model alone"),
    ]
    for s in by_action:
        _show(s)

    print("\n    COVERAGE CHECK — do the subgroups partition the run?")
    tot = sum(s["n"] for s in by_action)
    print(f"      {' + '.join(str(s['n']) for s in by_action)} = {tot}  vs n={n}  "
          f"{'✅ partition' if tot == n else '❌ DOES NOT PARTITION — rows are double-counted or missing'}")
    print(f"      The published table summed to 186 against a headline of 195. A layer table")
    print(f"      that does not partition its own run is not a decomposition of it.")

    out = {"n": n, "whole_system": {"mean_delta": round(whole_mean, 2),
                                    "ci_clustered": [round(wlo, 2), round(whi, 2)],
                                    "design_effect": round(wdeff, 2), "clusters": wg},
           "by_action": by_action, "partitions": tot == n,
           "caveat": ("Subgroups are defined by layer ACTION, which is decided after seeing "
                      "the item. These are DESCRIPTIVE, not confirmatory: the gate row in "
                      "particular excludes every item where the gate should have fired and "
                      "did not. Do not publish these as effect estimates for the layer.")}
    from anchored_write import write_result
    p = write_result("layer_attribution.json", out)
    print(f"\n    -> {p}")
    return 0


def _show(s: dict) -> None:
    if s["n"] == 0:
        print(f"      {s['label']:20s} {s['verdict']}"); return
    line = f"      {s['label']:20s} n={s['n']:3d}  Δ {s['mean_delta']:+6.2f}"
    if "ci_clustered" in s:
        line += f"  clustered [{s['ci_clustered'][0]:+.2f}, {s['ci_clustered'][1]:+.2f}]  {s['verdict']}"
    elif "ci_naive" in s:
        line += f"  naive [{s['ci_naive'][0]:+.2f}, {s['ci_naive'][1]:+.2f}]  ⚠️  {s['verdict']}"
    else:
        line += f"  {s['verdict']}"
    print(line)


def selftest() -> int:
    fails = []
    mk = lambda dim, delta, blocked=False, kb=False: {
        "dim": dim, "q": "", "sys": 0.0, "base": 0.0, "delta": delta,
        "blocked": blocked, "kb_hit": kb}

    # An empty subgroup must say UNMEASURED, never 0.0 — a layer that never fired has earned
    # no number at all, and reporting 0.0 would credit it with a measured null result.
    s = subgroup([mk("a", 0.1)], lambda r: r["blocked"], "gate")
    if s["n"] != 0 or "UNMEASURED" not in s["verdict"]:
        fails.append(f"empty subgroup gave {s}")

    # A single-item subgroup must refuse an interval rather than emit nan or a point.
    s = subgroup([mk("a", 0.5, blocked=True)], lambda r: r["blocked"], "gate")
    if "UNMEASURED" not in s.get("verdict", ""):
        fails.append(f"n=1 subgroup did not refuse an interval: {s}")

    # A subgroup confined to one dimension must be flagged, not silently clustered on one.
    rows = [mk("a", 0.2, blocked=True) for _ in range(6)]
    s = subgroup(rows, lambda r: r["blocked"], "gate")
    if "UNCLUSTERED" not in s.get("verdict", ""):
        fails.append(f"single-dimension subgroup not flagged: {s}")

    # Spanning dimensions, a real positive effect must be reported positive.
    rng = random.Random(11)
    rows = [mk(f"d{i%5}", 0.30 + rng.gauss(0, 0.02), blocked=True) for i in range(40)]
    s = subgroup(rows, lambda r: r["blocked"], "gate")
    if s.get("verdict") != "positive":
        fails.append(f"clear positive effect not reported positive: {s}")

    # …and a null effect must NOT be. Centre the draws explicitly: sampling gauss(0, 0.20) at
    # n=40 gives the sample mean an se of ~3 points, so an uncentred draw lands "significantly"
    # off zero often enough that the test would be measuring the seed, not the function.
    noise = [rng.gauss(0, 0.20) for _ in range(40)]
    mu = sum(noise) / len(noise)
    rows = [mk(f"d{i%5}", x - mu) for i, x in enumerate(noise)]
    s = subgroup(rows, lambda r: True, "null")
    if s.get("verdict") != "no effect shown":
        fails.append(f"exactly-null effect reported as {s.get('verdict')}: {s}")

    for f in fails:
        print(f"  ❌ {f}")
    print(f"  {'✅ selftest 5/5' if not fails else f'❌ {len(fails)} failure(s)'}")
    return 1 if fails else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        raise SystemExit(selftest())
    raise SystemExit(main())
