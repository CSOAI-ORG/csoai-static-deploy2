#!/usr/bin/env python3
"""gspc_agreement.py — inter-model AGREEMENT on statutory questions (GSPC empty cell #2).

WHY THIS CELL IS OPEN
---------------------
A crown-jewel hunt (4 Aug 2026) surveyed the field and found: LegalBench
(arXiv:2308.11462) and Vals Legal Research Bench measure per-model ACCURACY. The
model-spec stress-test (arXiv:2510.07686) measures general consistency, not regulatory.
Nobody publishes the AGREEMENT RATE between models on the same statutory question.

That gap matters commercially, not just academically. Two models can score identically and
still disagree on most items — same accuracy, different errors. A buyer choosing a model for
regulated use, an auditor reconciling two vendors' outputs, or an underwriter pricing model
risk all need to know whether models CONVERGE on the law or merely score alike on it.

WHAT IS COMPUTED
----------------
Over items where BOTH models emitted a parseable label:

  raw agreement   fraction of items where the two chose the same label
  Cohen's kappa   agreement corrected for chance, because on a 2-label axis two models
                  guessing independently already agree ~50% of the time. Raw agreement
                  alone would make coin-flips look like consensus.
  co-error rate   fraction where BOTH were wrong AND chose the SAME wrong label — the
                  dangerous case, because a second opinion that fails identically provides
                  no safety margin at all

DISCIPLINE, inherited from everything that broke on 2026-08-04
--------------------------------------------------------------
* an item where EITHER model was unparseable is excluded from that pair's denominator and
  counted, never treated as disagreement
* n and a 95% Wilson interval accompany every rate; at n=11-24 most pairs will not resolve
* kappa is undefined when one model emits a single label throughout — reported as null with
  the reason, not as 0.0

Usage:  python3 gspc_agreement.py [--run evidence/.../gspc-agreement-run.jsonl]
"""
from __future__ import annotations

import argparse
import itertools
import json
import math
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT = HERE / "evidence/harness/freeze/latest/gspc-agreement-run.jsonl"


def wilson(k: int, n: int, z: float = 1.96):
    if n == 0:
        return None, None, None
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    hw = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return round(p, 4), round(max(0.0, c - hw), 4), round(min(1.0, c + hw), 4)


def kappa(a: list, b: list):
    """Cohen's kappa. None when either rater is constant — kappa is undefined there, and
    reporting 0.0 would read as 'no better than chance' when the truth is 'not computable'."""
    n = len(a)
    if n == 0:
        return None, "no overlapping measured items"
    if len(set(a)) < 2 or len(set(b)) < 2:
        return None, "one model emitted a single label throughout — kappa undefined"
    po = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = Counter(a), Counter(b)
    pe = sum((ca[l] / n) * (cb[l] / n) for l in set(a) | set(b))
    if pe == 1:
        return None, "expected agreement is 1.0 — kappa undefined"
    return round((po - pe) / (1 - pe), 4), None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", default=str(DEFAULT))
    ap.add_argument("--out", default=str(HERE / "evidence/harness/freeze/latest/gspc-agreement.json"))
    args = ap.parse_args()

    rows = [json.loads(l) for l in Path(args.run).read_text().splitlines() if l.strip()]
    by_axis: dict[str, dict[str, dict]] = {}
    for r in rows:
        if "answers" in r:
            by_axis.setdefault(r["axis"], {})[r["model"]] = r

    out = {"generated": "2026-08-04", "source_run": Path(args.run).name,
           "metric": "inter-model agreement on statutory questions (GSPC empty cell #2)",
           "license": "CC-BY-4.0", "publisher": "CSOAI Ltd (UK 16939677)",
           "axes": {}}

    print("INTER-MODEL AGREEMENT ON STATUTORY QUESTIONS\n")
    for axis, models in by_axis.items():
        names = sorted(models)
        pairs = []
        for m1, m2 in itertools.combinations(names, 2):
            a1, a2 = models[m1]["answers"], models[m2]["answers"]
            exp = models[m1]["expected"]
            idx = [i for i in range(len(a1)) if a1[i] is not None and a2[i] is not None]
            excluded = len(a1) - len(idx)
            x, y = [a1[i] for i in idx], [a2[i] for i in idx]
            agree = sum(p == q for p, q in zip(x, y))
            co_err = sum(1 for i in idx
                         if a1[i] == a2[i] and a1[i] != exp[i])
            p, lo, hi = wilson(agree, len(idx))
            k, kreason = kappa(x, y)
            pairs.append({"model_a": m1, "model_b": m2, "n_compared": len(idx),
                          "excluded_unparseable": excluded,
                          "raw_agreement": p, "ci95": [lo, hi],
                          "cohens_kappa": k, "kappa_note": kreason,
                          "co_error_rate": round(co_err / len(idx), 4) if idx else None})
        out["axes"][axis] = pairs
        if pairs:
            ras = [q["raw_agreement"] for q in pairs if q["raw_agreement"] is not None]
            ks = [q["cohens_kappa"] for q in pairs if q["cohens_kappa"] is not None]
            ces = [q["co_error_rate"] for q in pairs if q["co_error_rate"] is not None]
            print(f"  {axis:12s} pairs={len(pairs):3d}  "
                  f"raw agreement {min(ras):.2f}-{max(ras):.2f} (mean {sum(ras)/len(ras):.2f})  "
                  f"kappa {'n/a' if not ks else f'{sum(ks)/len(ks):+.2f}'}  "
                  f"co-error {sum(ces)/len(ces):.2f}")

    Path(args.out).write_text(json.dumps(out, indent=2))
    print(f"\n  -> {args.out}")


if __name__ == "__main__":
    main()
