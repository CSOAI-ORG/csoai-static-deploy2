#!/usr/bin/env python3
"""retrieval_bench.py — does answering from statute beat answering from weights?

One correct answer is an anecdote. `statute_retrieval` fixed the Article 27 question that
`sov_whole` got wrong, which proves the mechanism runs — not that it helps. This measures it.

PAIRED, same items, same model, only the context differs:
    WEIGHTS    the question alone
    RETRIEVED  the question preceded by the top-k statute text

Restricted to the statute-answerable dimensions. Asking whether retrieval helps on `fairness`
would measure nothing: there is no article that settles whether men are better leaders, and
padding the denominator with items the treatment cannot affect biases the estimate toward
zero while looking like a broader test.

PREDICTION, WRITTEN BEFORE RUNNING: retrieval helps on items naming a specific article and
does little on open "what is X" items, because the corpus can only settle a question that has
a statutory answer. If the overall CI crosses zero I will say the retrieval layer is not
demonstrated, and the Article 27 fix stays an anecdote.

    python3 retrieval_bench.py
"""
from __future__ import annotations

import json, math, sys, time
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

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
    from statute_retrieval import search, NoStatuteFound, relevant, expand_crossrefs

    model, _ = select_expert("compliance")
    items = [(d, t) for d in DIMS if d in DIMENSIONS for t in DIMENSIONS[d]["tests"]]
    print(f"  RETRIEVAL vs WEIGHTS — {len(items)} items across {len(DIMS)} dimensions")
    print(f"  model: {model} (same on both arms; only the context differs)\n")

    w, r, names = [], [], []
    no_statute = 0
    t0 = time.time()
    for dim, t in items:
        q = t["q"]
        try:
            hits = search(q, 4)
            # Retrieving SOMETHING is not retrieving the RIGHT thing. Without this gate the
            # layer measured Δ -9.16 [-17.64, -0.69]: BM25 always returns its top-k, and the
            # grounding instruction then turned every miss into a confident wrong answer.
            ok, _why = relevant(q, hits)
            if not ok:
                no_statute += 1
                hits = None
            else:
                # 2026-07-29 — follow the edges. Art 27 retrieves correctly but delegates to
                # Annex III, which was absent from the corpus entirely until today and is
                # still not retrieved by term-frequency for the credit-scoring phrasing.
                hits = expand_crossrefs(hits)
        except NoStatuteFound:
            no_statute += 1
            hits = None
        try:
            s_w = grade_response(t, call_model(model, q))
            if hits:
                ctx = "\n\n".join(f"[{h['id']}]\n{h['text'][:1500]}" for h in hits)
                p = ("Answer using ONLY the regulation text below. If it does not settle the "
                     f"question, say so.\n\n{ctx}\n\nQuestion: {q}\nAnswer:")
                s_r = grade_response(t, call_model(model, p))
            else:
                # No statute retrieved: the retrieval arm gets the SAME answer as weights
                # rather than being scored as a failure. Retrieval cannot be blamed for an
                # item it never had a chance to affect.
                s_r = s_w
        except Exception as e:
            print(f"    ⏭️  {dim:18s} dropped from BOTH arms ({str(e)[:40]})")
            continue
        w.append(s_w * 100); r.append(s_r * 100); names.append((dim, q))
        d = (s_r - s_w) * 100
        flag = "📖" if hits else "  "
        print(f"    {flag} {dim:18s} weights={s_w*100:5.1f} retrieved={s_r*100:5.1f} "
              f"{d:+6.1f}  {q[:38]}", flush=True)

    n = len(w)
    if n < 5:
        print(f"  only {n} items"); return 2
    ds = [a - b for a, b in zip(r, w)]
    mu, lo, hi = ci(ds)
    wins = sum(1 for d in ds if d > 0); losses = sum(1 for d in ds if d < 0)
    real = not (lo < 0 < hi)

    print(f"\n  n={n} · {no_statute} items had no statute retrieved · {time.time()-t0:.0f}s\n")
    print(f"    WEIGHTS    {sum(w)/n:5.1f}%")
    print(f"    RETRIEVED  {sum(r)/n:5.1f}%")
    print(f"    Δ {mu:+6.2f}  95% CI [{lo:+6.2f}, {hi:+6.2f}]  "
          f"{'✅ real' if real else '❌ CI crosses zero'}")
    print(f"    wins {wins} · losses {losses} · ties {n-wins-losses}\n")

    # 2026-07-28 — the first version branched on `real` alone and printed "Retrieval beats
    # answering from weights" for a Δ of **-9.16**. Significance is not direction. A verdict
    # that reads only the CI's distance from zero and never its sign will announce a win for
    # any large enough loss, which is this session's defect wearing a statistics costume.
    if not real:
        print(f"  ⚠️  THE RETRIEVAL LAYER IS NOT DEMONSTRATED ON THIS BOARD.")
        print(f"     The Article 27 fix remains a single corrected case, not a system result.")
    elif mu < 0:
        print(f"  ❌ RETRIEVAL MAKES IT SIGNIFICANTLY WORSE — Δ {mu:+.2f}, CI excludes zero.")
        print(f"     Naive top-k stuffing into a 0.5B context is a REGRESSION, not an upgrade.")
        print(f"     Do not ship this layer on. The Art 27 case it fixed was real and")
        print(f"     unrepresentative; {losses} items got worse against {wins} better.")
    else:
        print(f"  ✅ Retrieval beats answering from weights on statute-answerable items.")

    out = {"timestamp": datetime.now(timezone.utc).isoformat(), "n": n, "model": model,
           "dimensions": DIMS, "no_statute_retrieved": no_statute,
           "weights_pct": round(sum(w)/n, 1), "retrieved_pct": round(sum(r)/n, 1),
           "delta": round(mu, 2), "ci": [round(lo, 2), round(hi, 2)], "significant": real,
           "wins": wins, "losses": losses, "ties": n-wins-losses}
    p = HERE / "benchmark-results" / "retrieval_bench.json"
    p.write_text(json.dumps(out, indent=2))
    print(f"  -> {p}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
