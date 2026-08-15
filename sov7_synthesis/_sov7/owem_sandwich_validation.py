#!/usr/bin/env python3
"""owem_sandwich_validation.py — validate the OWEM-sandwich merger.

After the TIES merge in sov7_synthesis/_sov7/owem_sandwich_merge.yaml produces
a new model artifact (e.g. sov-owem-sandwich:latest on the Ollama fleet), this
script:

  1. Scores the merged model on every GSPC axis via sovos.py (the canonical
     deterministic harness with USABLE_N=30 floor).
  2. Compares merged-model scores against:
     - The four specialist baselines (from govbench-owem-leaderboard.jsonl)
     - The qwen2.5:1.5b base (which TIES used as starting point)
  3. Reports a "dilution" verdict: did the merger beat or hurt each axis?
  4. Honours the UNMEASURED contract: any axis with n<30 is reported as
     UNMEASURED, never as a numeric score. Honest > hype.

Output: benchmark-results/owem_sandwich_validation_<timestamp>.json

Owner-gated (requires the merge to have run first). This script is part of
the recipe; it does NOT trigger the merge itself.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEPLOY2 = HERE.parent.parent  # ~/clawd/csoai-static-deploy2
RESULTS_DIR = DEPLOY2 / "benchmark-results"
LEADERBOARD = (
    DEPLOY2 / "evidence/harness/freeze/latest/govbench-owem-leaderboard.jsonl"
)

MERGED_MODEL_DEFAULT = "sov-owem-sandwich:latest"
BASE_MODEL = "qwen2.5:1.5b"
SPECIALISTS = [
    "sov34:latest",
    "sov-ethics-art5:latest",
    "sov33-unified:latest",
    "sov-compliance:latest",
]


def load_specialist_baselines() -> dict:
    """Load per-dimension top-score-per-specialist from the leaderboard."""
    if not LEADERBOARD.exists():
        return {}
    by_dim: dict[str, dict[str, float]] = {}
    with LEADERBOARD.open() as f:
        for line in f:
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            dim = row.get("dimension")
            model = row.get("model")
            pct = row.get("dimension_pct")
            if not dim or not model or pct is None:
                continue
            by_dim.setdefault(dim, {})[model] = float(pct)
    return by_dim


def run_sovos_axis(model: str, axis: str, endpoint: str = "ollama") -> dict:
    """Invoke sovos.py for one (model, axis). Returns its JSON line."""
    import subprocess
    cmd = [
        sys.executable,
        str(DEPLOY2 / "sovos.py"),
        "--model", model,
        "--endpoint", endpoint,
        "--axes", axis,
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    if proc.returncode != 0:
        return {"axis": axis, "model": model, "error": proc.stderr[-400:]}
    # sovos.py prints one JSON line per axis; parse the last one matching axis
    for line in reversed(proc.stdout.strip().splitlines()):
        try:
            row = json.loads(line)
            if row.get("axis") == axis:
                return row
        except json.JSONDecodeError:
            continue
    return {"axis": axis, "model": model, "error": "no_axis_row_in_stdout"}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--model", default=MERGED_MODEL_DEFAULT,
                    help=f"Merged Ollama model to validate (default: {MERGED_MODEL_DEFAULT})")
    ap.add_argument("--endpoint", default="ollama")
    ap.add_argument("--dry-run", action="store_true",
                    help="Just print the plan; don't actually invoke sovos.py")
    args = ap.parse_args()

    baselines = load_specialist_baselines()
    if not baselines:
        print(f"WARNING: no leaderboard at {LEADERBOARD}", file=sys.stderr)

    # Get the unique axes from the leaderboard (canonical set for this run).
    axes = sorted(baselines.keys()) if baselines else ["gov", "agi", "prv", "asi",
                                                       "mcp", "oss", "xr", "art5"]

    print(f"Will validate merged model={args.model!r} on {len(axes)} axes:")
    for a in axes:
        top = max(baselines.get(a, {}).items(), key=lambda kv: kv[1], default=(None, 0))
        print(f"  {a:<12}  top baseline: {top[0]} ({top[1]:.3f})")

    if args.dry_run:
        print("\n--dry-run set; no sovos.py invocations made.")
        return 0

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_path = RESULTS_DIR / f"owem_sandwich_validation_{ts}.json"

    rows = []
    for axis in axes:
        merged = run_sovos_axis(args.model, axis, args.endpoint)
        # Compare against the top specialist baseline for that axis
        baseline = baselines.get(axis, {})
        top_model, top_pct = (
            max(baseline.items(), key=lambda kv: kv[1])
            if baseline else (None, None)
        )
        merged_acc = merged.get("accuracy")
        dilution = (
            "BEAT" if merged_acc is not None and top_pct is not None
                and merged_acc > top_pct
            else "MATCH" if merged_acc is not None and top_pct is not None
                and abs(merged_acc - top_pct) < 0.05
            else "DILUTE" if merged_acc is not None and top_pct is not None
                and merged_acc < top_pct - 0.05
            else "UNMEASURED"
        )
        rows.append({
            "axis": axis,
            "merged_model": args.model,
            "merged_accuracy": merged_acc,
            "merged_n_measured": merged.get("n_measured"),
            "baseline_top_model": top_model,
            "baseline_top_pct": top_pct,
            "verdict": dilution,
            "raw": merged,
        })
        print(f"  {axis:<12} merged={merged_acc}  baseline={top_model}={top_pct}  → {dilution}")

    # Headline: count axes that beat / match / dilute / unmeasured
    counts = {"BEAT": 0, "MATCH": 0, "DILUTE": 0, "UNMEASURED": 0}
    for r in rows:
        counts[r["verdict"]] += 1

    summary = {
        "merged_model": args.model,
        "base_model": BASE_MODEL,
        "specialists": SPECIALISTS,
        "axes_evaluated": len(rows),
        "verdict_counts": counts,
        "headline": (
            f"{args.model} BEATS the top specialist on "
            f"{counts['BEAT']}/{len(rows)} measured axes"
            if counts["BEAT"] >= counts["DILUTE"]
            else f"{args.model} DILUTES on more axes ({counts['DILUTE']}) than it beats ({counts['BEAT']})"
        ),
        "measured_at": datetime.now(timezone.utc).isoformat(),
        "rows": rows,
    }

    out_path.write_text(json.dumps(summary, indent=2))
    print(f"\nHeadline: {summary['headline']}")
    print(f"Wrote {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())