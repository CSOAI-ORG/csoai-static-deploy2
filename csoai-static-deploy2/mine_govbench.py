#!/usr/bin/env python3
"""Mine backbones on the runpod-a100 to find the most feasible neurosymbolic OOWM stack.
Neurosymbolic = backbone + DORADO gate + law-RAG. Ranks candidates by GOVBENCH overall.
Usage: python3 mine_govbench.py --models sov33-ultimate-sovereign:latest qwen3:8b deepseek-r1:8b
"""
import sys, json
from datetime import datetime, timezone
sys.path.insert(0, "/Users/nicholas/clawd/csoai-static-deploy2")
import argparse
from run_govbench_ns2 import NeuroSymbolicV2

ap = argparse.ArgumentParser()
ap.add_argument("--models", nargs="*", default=["sov33-ultimate-sovereign:latest", "qwen3:8b"])
args = ap.parse_args()

bench = NeuroSymbolicV2()
all_results = {}
for model in args.models:
    try:
        all_results[model] = bench.run_benchmark(model, "ollama")
    except Exception as e:
        all_results[model] = {"model": model, "error": str(e)}

print("\n╔══════════════════════════════════════════════════════════╗")
print("║  NEUROSYMBOLIC OOWM — STACK MINING LEADERBOARD           ║")
print("╚══════════════════════════════════════════════════════════╝")
print(f"\n  {'Model':28s} {'Overall':>8s} {'Pillars':>8s} {'HardStop':>9s} {'Comply':>7s}")
ranked = sorted([(m, r) for m, r in all_results.items() if "overall" in r], key=lambda x: -x[1]["overall"]["score"])
for rank, (model, r) in enumerate(ranked, 1):
    o = r["overall"]
    print(f"  #{rank} {model:24s} {o['score']:>8.3f} {o['pillar_avg']:>8.3f} {o['hard_stop_pass']:>9.3f} {o['compliance_avg']:>7.3f}")

out = {"timestamp": datetime.now(timezone.utc).isoformat(), "kind": "ga (gate+RAG)", "results": all_results}
json.dump(out, open("/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/govbench_oowm_mine.json", "w"), indent=2)
print("\nSaved: benchmark-results/govbench_oowm_mine.json")
