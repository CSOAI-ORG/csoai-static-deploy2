#!/usr/bin/env python3
"""build_govbench_leaderboard.py — assemble the GovBench leaderboard from result files.

THE RULE THIS ENFORCES: a failed run is not a score.

The results directory contains entries scoring 0.0 on EVERY dimension for
google/gemma-2-2b-it, mistralai/mistral-7b-instruct-v0.3 and meta/llama-3.1-8b-instruct,
all with provider=nvidia and no credential configured. Those are API failures. Publishing
them as a leaderboard row would state that Google's and Mistral's models score zero on
governance — false, and defamatory toward models we never actually ran.

A model is EXCLUDED when it scores exactly 0.0 on every dimension, because no real model
does that (even a model that answers nothing scores >0 on refusal dimensions, since
"no answer" reads as a refusal). If a third-party model is absent here, we could not run
it — it is never reported as zero.

    python3 build_govbench_leaderboard.py [--out leaderboard.md]
"""
from __future__ import annotations

import argparse, glob, json
from datetime import datetime, timezone
from pathlib import Path

RESULTS = Path("benchmark-results/govbench")


def load() -> tuple[list[dict], list[dict]]:
    kept, excluded = [], []
    seen: set[tuple] = set()
    for f in sorted(glob.glob(str(RESULTS / "*.json"))):
        try:
            doc = json.load(open(f))
        except Exception:
            continue
        for r in (doc if isinstance(doc, list) else [doc]):
            if not isinstance(r, dict) or "overall_score" not in r:
                continue
            dims = r.get("dimensions") or {}
            key = (r.get("model"), len(dims))
            if key in seen:
                continue
            seen.add(key)
            row = {"model": r.get("model", "?"), "score": r["overall_score"],
                   "cert": r.get("certification", ""), "dims": len(dims),
                   "provider": r.get("provider", "?"), "dimensions": dims,
                   "source": Path(f).name}
            # THE EXCLUSION RULE — all-zero across every dimension = failed run, not a score.
            if dims and all(float(v) == 0.0 for v in dims.values()):
                row["reason"] = f"all dimensions 0.0 (provider={row['provider']}) — API failure, not a measurement"
                excluded.append(row)
            else:
                kept.append(row)
    kept.sort(key=lambda x: -x["score"])
    return kept, excluded


def render(kept: list[dict], excluded: list[dict]) -> str:
    L = ["# GovBench leaderboard",
         "",
         f"_Generated {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}. "
         f"{len(kept)} measured runs. Scores across different dimension counts are NOT comparable._",
         ""]
    for n in sorted({r["dims"] for r in kept}, reverse=True):
        rows = [r for r in kept if r["dims"] == n]
        L += [f"## {n}-dimension harness", "",
              "| # | model | score | certification | provider |",
              "|---|---|---|---|---|"]
        for i, r in enumerate(rows, 1):
            L.append(f"| {i} | `{r['model']}` | **{r['score']:.1f}%** | {r['cert'] or '—'} | {r['provider']} |")
        L.append("")

    # Per-dimension detail for the largest harness — where the real story is.
    big = [r for r in kept if r["dims"] == max((r["dims"] for r in kept), default=0)]
    if big:
        dim_names = list(big[0]["dimensions"].keys())
        L += ["## Per-dimension (15-dim harness)", "",
              "| dimension | " + " | ".join(f"`{r['model'].split(':')[0]}`" for r in big) + " |",
              "|---|" + "---|" * len(big)]
        for d in dim_names:
            L.append(f"| {d} | " + " | ".join(f"{r['dimensions'].get(d,0):.1f}" for r in big) + " |")
        L.append("")

    L += ["## Excluded — failed runs, NOT scores", ""]
    if excluded:
        L += ["These scored 0.0 on **every** dimension, which no real model does. They are API",
              "failures with no credential configured. Reporting them as scores would be false and",
              "would defame models we never ran.", "",
              "| model | provider | why excluded |", "|---|---|---|"]
        for r in excluded:
            L.append(f"| `{r['model']}` | {r['provider']} | {r['reason']} |")
    else:
        L.append("_None._")
    L += ["", "**If a third-party model is absent from this leaderboard, we could not run it.",
          "It is never reported as zero.**", ""]
    return "\n".join(L)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="benchmark-results/govbench/LEADERBOARD.md")
    a = ap.parse_args()
    kept, excluded = load()
    Path(a.out).write_text(render(kept, excluded))
    print(f"  measured runs : {len(kept)}")
    print(f"  excluded      : {len(excluded)} (all-zero API failures)")
    for r in kept[:12]:
        print(f"    {r['score']:5.1f}%  {r['cert']:12s} dims={r['dims']:2d}  {r['model']}")
    print(f"  -> {a.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
