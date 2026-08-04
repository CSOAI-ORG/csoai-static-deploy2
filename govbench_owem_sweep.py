#!/usr/bin/env python3
"""govbench_owem_sweep.py — run the full 193-item GovBench across the OWEM fleet on the GPU.

WHY
---
csoai/govbench on Hugging Face holds seven result documents in six different schemas, which
is why its dataset viewer is broken — and none of them is a current, consistent leaderboard.
Its most dataset-shaped file, nvidia_leaderboard.json, contains ONE record.

This produces the thing that repo should serve alongside the items: a real leaderboard,
measured today, one row per (model, dimension), ONE schema — using the fixed grader (the
three refusal-matching bugs found 2026-08-04) and running every generation on the RunPod
OWEM pod so the Mac only does arithmetic.

HONESTY PROPERTIES, inherited from govbench_eval and enforced here:
  • UnreachableModel   a provider failure is the ABSENCE of a measurement. The model is
                       DROPPED from the board, never scored 0. This is exactly how
                       gemma/mistral/llama once appeared to "score zero on governance".
  • UngradedItem       an item matching no criterion raises rather than averaging in.
  • per-dimension rows so a strong overall score cannot hide a collapsed dimension — the
    defect found today when sov-refusal-balanced scored 0.839 overall and 1/5 on the single
    prohibition that mattered.

Usage:
  GOVBENCH_OLLAMA_URL=https://<pod>-11434.proxy.runpod.net python3 govbench_owem_sweep.py \
      --models sov34:latest sov33-unified:latest ...
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import govbench_eval as g  # noqa: E402

OUT = HERE / "evidence" / "harness" / "freeze" / "latest"


def sweep(models: list[str]) -> tuple[list[dict], dict]:
    rows: list[dict] = []
    dropped: dict[str, str] = {}
    stamp = datetime.now(timezone.utc).isoformat()

    for model in models:
        per_dim: dict[str, tuple[float, float]] = {}
        try:
            for dim_key, dim in g.DIMENSIONS.items():
                score = weight = 0.0
                for test in dim["tests"]:
                    w = test.get("weight", 1)
                    resp = g.call_model(model, test["q"], "ollama")
                    score += g.grade_response(test, resp) * w   # raises on unreachable
                    weight += w
                    time.sleep(0.05)
                per_dim[dim_key] = (score, weight)
        except g.UnreachableModel as e:
            # Absence of a measurement. Drop the model entirely rather than bank a partial
            # denominator that would look like a low score.
            dropped[model] = f"unreachable: {str(e)[:120]}"
            print(f"  {model:34s} DROPPED — {dropped[model]}", flush=True)
            continue
        except g.UngradedItem as e:
            dropped[model] = f"ungraded item: {str(e)[:120]}"
            print(f"  {model:34s} DROPPED — malformed item: {e}", flush=True)
            continue

        tot_s = sum(s for s, _ in per_dim.values())
        tot_w = sum(w for _, w in per_dim.values())
        overall = round(100 * tot_s / tot_w, 2) if tot_w else None
        for dim_key, (s, w) in per_dim.items():
            rows.append({
                "measured_at": stamp,
                "benchmark": "GovBench",
                "items_total": sum(len(d["tests"]) for d in g.DIMENSIONS.values()),
                "substrate": g.OLLAMA_URL,
                "grader": "govbench_eval.grade_response (hedge-aware _refuses, 2026-08-04)",
                "model": model,
                "dimension": dim_key,
                "dimension_name": g.DIMENSIONS[dim_key].get("name", dim_key),
                "dimension_items": len(g.DIMENSIONS[dim_key]["tests"]),
                "dimension_pct": round(100 * s / w, 2) if w else None,
                "overall_pct": overall,
            })
        print(f"  {model:34s} overall {overall}%", flush=True)
    return rows, dropped


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", nargs="+", required=True)
    ap.add_argument("--out", default=str(OUT / "govbench-owem-leaderboard.jsonl"))
    args = ap.parse_args()

    print(f"GovBench OWEM sweep — {len(args.models)} models x "
          f"{sum(len(d['tests']) for d in g.DIMENSIONS.values())} items on {g.OLLAMA_URL}\n")
    rows, dropped = sweep(args.models)

    schemas = {tuple(sorted(r)) for r in rows}
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(json.dumps(r) for r in rows))

    meta = {
        "measured_at": datetime.now(timezone.utc).isoformat(),
        "rows": len(rows),
        "models_scored": len({r["model"] for r in rows}),
        "models_dropped_unmeasured": dropped,
        "distinct_schemas": len(schemas),
        "note": ("Dropped models are UNMEASURED, not zero. They are absent from the board by "
                 "construction — the leaderboard cannot represent a model it failed to reach."),
    }
    Path(str(out).replace(".jsonl", ".meta.json")).write_text(json.dumps(meta, indent=2))
    print(f"\n  rows {len(rows)} · models scored {meta['models_scored']} · "
          f"dropped {len(dropped)} · schemas {len(schemas)} (must be 1)")
    print(f"  -> {out}")


if __name__ == "__main__":
    main()
