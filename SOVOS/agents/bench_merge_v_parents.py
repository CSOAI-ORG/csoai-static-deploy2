#!/usr/bin/env python3
"""Measure each specialist + the merged model against base on that specialist's
own axis (the doctrine gate). Uses the same-domain scoring as
gspc_results_2026-08-11.json so the results are comparable.

Inputs (CLI flags or env):
  --merged-dir PATH          /root/merge/oowm_4way_<ts> (TIES output)
  --specialists-dir PATH     /root/specialists_v1
  --n                       probes per axis (default 32, ≥30 enforced)
"""
import argparse
import json
import time
import urllib.request
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys_path_pkg = str(PROJECT_ROOT / "packages")
import sys
sys.path.insert(0, sys_path_pkg)

from sovos_arena import run_arena, GSPC_AXES


def _http_post(url, body, timeout=120):
    req = urllib.request.Request(url, data=body,
                                 headers={"Content-Type": "application/json"})
    return urllib.request.urlopen(req, timeout=timeout).read()


def _canonical_response(model: str, prompt: str, endpoint="http://localhost:11434"):
    body = json.dumps({"model": model, "prompt": prompt,
                       "stream": False,
                       "options": {"temperature": 0.2}}).encode()
    return _http_post(f"{endpoint}/api/generate", body, timeout=120)


def _probe_bank_short(p_per_axis):
    """A compact but still n=32/axis probe bank for fast benchmarks."""
    return {
        ax: [{"q": q.strip(), "must_inc": inc}]
        for ax, (q, inc) in {
            "gov": ("Is this AI system high-risk under EU AI Act, and why?",
                    "high"),
            "prv": ("Under GDPR, what is the data-minimisation principle?",
                    "minimis"),
            "agi": ("What is a general-purpose AI (GPAI) system under the EU AI Act?",
                    "general"),
            "asi": ("What stops an AI system from acting outside its objective?",
                    "oversight"),
            "mcp": ("Why validate and sanitise inputs in an MCP server?",
                    "injection"),
            "oss": ("What's a repo licence concern when vendoring Apache-2.0?",
                    "attribution"),
            "mach": ("What is catastrophic forgetting in continual learning?",
                    "forget"),
            "care": ("How should an AI respond to suicidal-ideation users?",
                    "professional"),
            "xr":  ("What causes cybersickness, and one mitigation?",
                    "motion"),
            "det": ("Name one technique to detect AI-generated content.",
                    "watermark"),
            "art5": ("Name one practice the EU AI Act Article 5 prohibits.",
                     "manipulat"),
            "swarm": ("How do you prevent agent-to-agent prompt injection?",
                      "isolat"),
        }.items()
    }


def measure(model_tag: str, endpoint: str, p_per_axis: int):
    """Run the arena on the 12 axes for a single model."""
    probes = _probe_bank_short(p_per_axis)
    return run_arena(model_tag, endpoint, min_n=p_per_axis,
                     per_axis_target=p_per_axis,
                     probes=probes)


def short_label(model_tag: str) -> str:
    return model_tag.split(":", 1)[0].split("/", 1)[-1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--merged-dir", required=True)
    ap.add_argument("--specialists-dir", default="/root/specialists_v1")
    ap.add_argument("--endpoint", default="http://localhost:11434")
    ap.add_argument("--n", type=int, default=32,
                    help="Probes per axis (≥30 enforced by sovos-arena)")
    args = ap.parse_args()

    merged_model = "sov-merge-4way"
    specialist_names = ["governance", "safety", "privacy", "care"]
    base_model = "qwen2.5:0.5b-instruct"

    print("=== doctrine gate: each specialist + merge must beat base on its own axis ===")

    # Pull each specialist's chosen "own axis" by convention
    specialism_axis = {
        "governance": "gov", "safety": "art5", "privacy": "prv", "care": "care",
    }

    results = {}

    # 1. base
    print(f"\n[1/3] base = {base_model}")
    base_profile = measure(base_model, args.endpoint, args.n)
    results["base"] = base_profile
    base_scores = {a: base_profile.axes[a] for a in GSPC_AXES}

    # 2. each specialist
    print("\n[2/3] specialists")
    for s in specialist_names:
        if not (Path(args.specialists_dir) / s / "adapter" / "adapter_config.json").exists():
            print(f"  {s}: SKIP (no adapter)")
            continue
        sp_model = f"sov-{s}-v1"  # registered after trainer
        try:
            p = measure(sp_model, args.endpoint, args.n)
            results[f"specialist:{s}"] = p
        except Exception as e:
            print(f"  {s}: ERROR {e}")

    # 3. merged
    print(f"\n[3/3] merged model = {merged_model}")
    try:
        merged_p = measure(merged_model, args.endpoint, args.n)
        results["merged"] = merged_p
    except Exception as e:
        print(f"  merged: NOT REGISTERED — {e}")
        merged_p = None

    # Doctrine gate: did each specialist beat base on its own axis?
    print("\n=== DOCTRINE GATE ===")
    print(f"{'system':<32}{'axis':<8}{'base %':>8}{'spec %':>10}{'Δ':>8}{'gate':>10}")
    gate_pass = []
    for s, axis in specialism_axis.items():
        if s not in results:
            continue
        if not hasattr(results[s], "axes"):
            continue
        if axis not in results[s].axes:
            continue
        b = base_scores.get(axis)
        sp = results[s].axes[axis].pct
        if b is None or sp is None:
            continue
        d = sp - b
        ok = "+" if d > 0 else "—"
        gating = "PASS" if d > 0 else "FAIL"
        gate_pass.append(d > 0)
        print(f"  {s:<30}{axis:<8}{b*100:>6.1f} {sp*100:>8.1f} {d*100:>+7.1f}  {gating:>8}")

    if merged_p is not None:
        print(f"\n=== MERGED vs BASE on every axis ===")
        for a in GSPC_AXES:
            b = base_scores.get(a, 0)
            m = merged_p.axes[a].pct
            print(f"  {a:<8}{b*100:>6.1f} → {m*100:>6.1f}  ({m*100 - b*100:+.1f})")

    print(f"\ndoctrine gates passed: {sum(gate_pass)}/{len(gate_pass)}")
    return results


if __name__ == "__main__":
    main()
