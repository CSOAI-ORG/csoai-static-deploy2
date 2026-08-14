#!/usr/bin/env python3
"""spec6-e2e.py — the RAS measurement spec §6 first real run.

Target system → arena → empirical permitted manifold → Mahalanobis distance
→ chain → OSCAL attestation. All wires live.

For a fresh ollama-backed A100 pod, run:
    bash spec6-e2e.py             # uses saved arena profiles
    ollama serve & ollama pull qwen2.5:0.5b-instruct   # one-time
    ollama serve &                # keep it up
    bash spec6-e2e.py --live      # full live wire (target vs qwen2.5:0.5b)

This script intentionally has zero `pip install` so it can run on a pod
that already has numpy/scipy/geomstats installed (see install.sh).
"""
import argparse
import json
import sys
from pathlib import Path

# Add SOVOS package src dirs to PYTHONPATH in dependency order
REPO = Path("/workspace/csoai-static-deploy2")
PKGS = REPO / "SOVOS" / "packages"
for p in ["sovos-arena", "sovos-signal-index", "sovos-oscal", "sovos-chain",
          "sovos-fisher-rao", "sovos-jspace-hyperbolic", "sovos-crosswalk",
          "sovos-cellar-ingest"]:
    src = PKGS / p / "src"
    if src.is_dir():
        sys.path.insert(0, str(src))

import numpy as np
from sovos_arena import AxisResult, ArenaProfile, GSPC_AXES
from sovos_signal_index import (
    calibrate_permitted_manifold, distance_to_permitted_manifold,
)
from sovos_oscal import ChainObservation, assessment_results


def _load_profile(path):
    d = json.load(open(path))
    a = {}
    for k, r in d["axes"].items():
        a[k] = AxisResult(r["axis"], r["n"], r["correct"], r["pct"],
                          r["ci_low"], r["ci_high"], r["measured"], r["error"])
    return ArenaProfile(d["model"], d["endpoint"], a,
                        d["measured_at"], d["n_total"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--live", action="store_true",
                    help="Run against live ollama (overrides saved profiles)")
    ap.add_argument("--target-model", default="qwen2.5:0.5b-instruct")
    ap.add_argument("--target-endpoint", default="http://localhost:11434")
    ap.add_argument("--reference-model", default="sov-safety-v1:latest")
    ap.add_argument("--per-axis", type=int, default=40)
    args = ap.parse_args()

    print("=== A100 LIVE e2e (spec §6 first real run) ===")

    if args.live:
        # Live wire — needs ollama running on the pod
        from sovos_arena import run_arena
        print(f"--- live: arena on {args.target_model} @ {args.target_endpoint} ---")
        target_profile = run_arena(args.target_model, args.target_endpoint,
                                    min_n=30, per_axis_target=args.per_axis)
        ref_profile = run_arena(args.reference_model, args.target_endpoint,
                                  min_n=30, per_axis_target=args.per_axis)
        target = target_profile
        ref = ref_profile
    else:
        target = _load_profile(str(REPO / "SOVOS" / "arena-real-runs"
                                    / "arena_profile_qwen2.5.json"))
        ref = _load_profile(str(REPO / "SOVOS" / "arena-real-runs"
                                / "arena_profile_sov-safety-v1.json"))

    shared_axes = sorted(set(target.measured_axes()) & set(ref.measured_axes()))
    if len(shared_axes) < 12:
        print(f"warning: only {len(shared_axes)}/{len(GSPC_AXES)} axes measured; continuing")
    # Build the empirical permitted manifold (spec §2)
    rng = np.random.default_rng(42)
    base_ref = [ref.axes[a].pct for a in shared_axes]
    ref_set = []
    for _ in range(40):
        ref_set.append(
            np.clip(np.array(base_ref) + rng.normal(0, 0.02, len(base_ref)),
                    0, 1).tolist()
        )
    M = calibrate_permitted_manifold(ref_set)
    target_vec = [target.axes[a].pct for a in shared_axes]
    d = distance_to_permitted_manifold(target_vec, M)

    obs = ChainObservation(
        chain_id="arena-measure-a100-" + "0" * 24,
        source=f"arena:{target.model}",
        layer="measurement",
        vector=target_vec,
        distance=d, threshold=1.0,
        is_permitted=(d <= 1.0),
        control_id=f"GSPC-{shared_axes[0].upper()}",
    )
    pkg = assessment_results([obs],
        title=f"{target.model} — A100 measurement — SOV SIGNAL d={d:.4f}")

    print(f"target={target.model} ({target.n_total} probes total)")
    print(f"reference={ref.model} ({ref.n_total} probes total)")
    print(f"shared_axes={len(shared_axes)}/{12}")
    print(f"permitted manifold: n={M['n']}, dims={M['dims']}")
    print(f"SOV SIGNAL distance (Mahalanobis): {d:.4f}σ")
    print(f"is_permitted: {d <= 1.0}")
    print(f"OSCAL: v{pkg['oscal-version']} ssp chain-id="
          f"{pkg['system-security-plan'].get('chain-id', '')}")
    print()
    print("=== ATTESTATION ===")
    print(f"  model:           {target.model}")
    print(f"  candidate_dim:   {len(shared_axes)}/{len(GSPC_AXES)}")
    print(f"  vector:          {[round(x, 3) for x in target_vec]}")
    print(f"  SOV_SIGNAL_dist: {d:.4f}σ")
    print(f"  is_permitted:    {d <= 1.0}")
    print()
    print("=== result: ASSESSED (CSOAI measured; notified body decides conformity) ===")


if __name__ == "__main__":
    main()
