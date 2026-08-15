#!/usr/bin/env python3
"""cad_analysis.py — Pre-registered analysis for CAD-augmented retrieval.

WRITTEN BEFORE RUNNING — 2026-07-29.
An analysis chosen after seeing the data is not an analysis.

WHAT THIS TESTS
    retrieval_bench measured: statute retrieval makes answers WORSE (Δ -5.26).
    CAD (Context-Aware Decoding) is designed to fix exactly this: force the model
    to weight retrieved context over its baked-in prior.

    We re-run retrieval_bench with CAD and compare:
      ARM A (WEIGHTS): question alone → model answers from weights
      ARM B (CAD):     question + statute → model answers with CAD contrastive decoding

    Same items, same model, only the decoding strategy differs.

PRE-REGISTERED PREDICTION (written 2026-07-29, before running):
    1. CAD will shift Δ from -5.26 toward positive on statute-answerable items.
    2. If Δ > 0 with CI excluding zero: CAD revives the retrieval layer.
    3. If CI still crosses zero: CAD does not fix the problem at 0.5B scale.
    4. The improvement will be largest on items where the bare model gets the
       wrong statute (e.g., confuses Article 27 with Article 22).
    5. AdaCAD (adaptive α) will outperform fixed α=0.5 because the optimal
       contrastive weight varies by question difficulty.

WHAT WOULD INVALIDATE THE CLAIM
    - If CAD Δ is negative and significant: CAD makes it worse (the contrastive
      signal confuses the small model).
    - If agreement is always ≥0.9: the model gives the same answer with or without
      context, meaning it's ignoring the statute entirely.
    - If citation_correct is always False with CAD: the model doesn't learn to cite
      even when forced to attend to context.

    python3 cad_analysis.py
"""
from __future__ import annotations

import json
import math
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

OUT = HERE / "benchmark-results" / "cad_analysis.json"

# The same dimensions retrieval_bench used — for comparability
DIMS = ["compliance", "governance", "cross_walk", "regional_law", "privacy", "redress"]


def ci(ds: list[float]) -> tuple[float, float, float]:
    n = len(ds)
    if n < 2:
        return 0.0, 0.0, 0.0
    mu = sum(ds) / n
    sd = math.sqrt(sum((d - mu) ** 2 for d in ds) / (n - 1))
    se = sd / math.sqrt(n)
    return mu, mu - 1.96 * se, mu + 1.96 * se


def main() -> int:
    from govbench_eval import DIMENSIONS, grade_response
    from owem_cluster import ask as call_model, select_expert
    from statute_retrieval import search, NoStatuteFound, relevant
    from cad_decoder import ask_with_cad
    from ada_cad import ask_with_adacad

    model, _ = select_expert("compliance")
    items = [(d, t) for d in DIMS if d in DIMENSIONS for t in DIMENSIONS[d]["tests"]]
    print(f"  CAD ANALYSIS — pre-registered, written before running")
    print(f"  {len(items)} items across {len(DIMS)} dimensions")
    print(f"  model: {model}\n")

    # Three arms: weights, fixed CAD, adaptive CAD
    w_scores, cad_scores, adacad_scores = [], [], []
    cad_verdicts = []
    agreements_fixed, agreements_adapt = [], []
    no_statute = 0
    t0 = time.time()

    for dim, t in items:
        q = t["q"]
        try:
            hits = search(q, 4)
            ok, _why = relevant(q, hits)
            if not ok:
                no_statute += 1
                hits = None
        except NoStatuteFound:
            no_statute += 1
            hits = None

        try:
            # ARM A: weights only
            s_w = grade_response(t, call_model(model, q)) * 100

            if hits:
                ctx = "\n\n".join(f"[{h['id']}]\n{h['text'][:1500]}" for h in hits)
                arts = [h.get("id", "") for h in hits]

                # ARM B: fixed CAD (α=0.5)
                cad_resp = ask_with_cad(
                    question=q, statute_context=ctx,
                    retrieved_articles=arts, model=model,
                    dimension=dim, alpha=0.5,
                )
                s_cad = grade_response(t, cad_resp.answer) * 100
                agreements_fixed.append(cad_resp.agreement)

                # ARM C: adaptive CAD
                adacad_resp = ask_with_adacad(
                    question=q, statute_context=ctx,
                    retrieved_articles=arts, model=model,
                    dimension=dim,
                )
                s_adacad = grade_response(t, adacad_resp.answer) * 100
                agreements_adapt.append(adacad_resp.agreement)
                cad_verdicts.append(adacad_resp.cad_verdict)
            else:
                s_cad = s_w
                s_adacad = s_w

        except Exception as e:
            print(f"    ⏭️  {dim:18s} dropped ({str(e)[:40]})")
            continue

        w_scores.append(s_w)
        cad_scores.append(s_cad)
        adacad_scores.append(s_adacad)
        d_cad = s_cad - s_w
        d_adapt = s_adacad - s_w
        flag = "📖" if hits else "  "
        print(f"    {flag} {dim:18s} w={s_w:5.1f} cad={s_cad:5.1f} "
              f"adapt={s_adacad:5.1f}  {d_cad:+5.1f}/{d_adapt:+5.1f}  {q[:35]}", flush=True)

    n = len(w_scores)
    if n < 5:
        print(f"  only {n} items"); return 2

    elapsed = time.time() - t0

    # Analysis: weights vs fixed CAD
    ds_fixed = [c - w for c, w in zip(cad_scores, w_scores)]
    mu_f, lo_f, hi_f = ci(ds_fixed)
    wins_f = sum(1 for d in ds_fixed if d > 0)
    losses_f = sum(1 for d in ds_fixed if d < 0)
    sig_f = not (lo_f < 0 < hi_f)

    # Analysis: weights vs adaptive CAD
    ds_adapt = [a - w for a, w in zip(adacad_scores, w_scores)]
    mu_a, lo_a, hi_a = ci(ds_adapt)
    wins_a = sum(1 for d in ds_adapt if d > 0)
    losses_a = sum(1 for d in ds_adapt if d < 0)
    sig_a = not (lo_a < 0 < hi_a)

    # Agreement stats
    avg_agree_fixed = sum(agreements_fixed) / len(agreements_fixed) if agreements_fixed else 0
    avg_agree_adapt = sum(agreements_adapt) / len(agreements_adapt) if agreements_adapt else 0

    print(f"\n  n={n} · {no_statute} items had no statute · {elapsed:.0f}s\n")
    print(f"  WEIGHTS          {sum(w_scores)/n:5.1f}%")
    print(f"  FIXED CAD (α=0.5) {sum(cad_scores)/n:5.1f}%")
    print(f"  ADAPTIVE CAD      {sum(adacad_scores)/n:5.1f}%")
    print()
    print(f"  FIXED CAD vs WEIGHTS:")
    print(f"    Δ {mu_f:+6.2f}  95% CI [{lo_f:+6.2f}, {hi_f:+6.2f}]  "
          f"{'✅ SIGNIFICANT' if sig_f else '❌ CI crosses zero'}")
    print(f"    wins {wins_f} · losses {losses_f} · ties {n - wins_f - losses_f}")
    print(f"    avg agreement: {avg_agree_fixed:.2f}")
    print()
    print(f"  ADAPTIVE CAD vs WEIGHTS:")
    print(f"    Δ {mu_a:+6.2f}  95% CI [{lo_a:+6.2f}, {hi_a:+6.2f}]  "
          f"{'✅ SIGNIFICANT' if sig_a else '❌ CI crosses zero'}")
    print(f"    wins {wins_a} · losses {losses_a} · ties {n - wins_a - losses_a}")
    print(f"    avg agreement: {avg_agree_adapt:.2f}")
    print()
    
    # Verdict
    if sig_f and mu_f > 0:
        print(f"  ✅ FIXED CAD REVIVES THE RETRIEVAL LAYER.")
    elif sig_a and mu_a > 0:
        print(f"  ✅ ADAPTIVE CAD REVIVES THE RETRIEVAL LAYER.")
    elif not sig_f and not sig_a:
        print(f"  ⚠️  NEITHER CAD VARIANT SHOWS SIGNIFICANT IMPROVEMENT.")
        print(f"     The retrieval layer remains not demonstrated.")
    else:
        print(f"  ❌ CAD MAKES IT WORSE — do not ship.")

    if agreements_fixed and avg_agree_fixed > 0.9:
        print(f"\n  ⚠️  HIGH AGREEMENT ({avg_agree_fixed:.2f}) — model may be ignoring context entirely.")
    if agreements_adapt and avg_agree_adapt < 0.3:
        print(f"\n  ⚠️  LOW AGREEMENT ({avg_agree_adapt:.2f}) — model heavily contradicts its weights.")

    # Save
    out = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "pre_registered": True,
        "prediction": "CAD will shift Δ from -5.26 toward positive on statute-answerable items",
        "n": n, "model": model, "dimensions": DIMS,
        "no_statute_retrieved": no_statute,
        "weights_pct": round(sum(w_scores)/n, 1),
        "fixed_cad_pct": round(sum(cad_scores)/n, 1),
        "adaptive_cad_pct": round(sum(adacad_scores)/n, 1),
        "fixed_cad": {
            "delta": round(mu_f, 2), "ci": [round(lo_f, 2), round(hi_f, 2)],
            "significant": sig_f, "wins": wins_f, "losses": losses_f,
            "avg_agreement": round(avg_agree_fixed, 3),
        },
        "adaptive_cad": {
            "delta": round(mu_a, 2), "ci": [round(lo_a, 2), round(hi_a, 2)],
            "significant": sig_a, "wins": wins_a, "losses": losses_a,
            "avg_agreement": round(avg_agree_adapt, 3),
        },
        "verdict_distribution": {v: cad_verdicts.count(v) for v in set(cad_verdicts)},
    }
    OUT.write_text(json.dumps(out, indent=2))
    print(f"\n  -> {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
