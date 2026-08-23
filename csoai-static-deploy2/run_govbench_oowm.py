#!/usr/bin/env python3
"""Run GOVBENCH on the OOWM model (council-oowm) + powerhouse (sov33-unified) via runpod-a100."""
import sys, json
from datetime import datetime, timezone
sys.path.insert(0, "/Users/nicholas/clawd/csoai-static-deploy2")
from govbench import GovBench

bench = GovBench()
models = [("council-oowm:latest", "ollama", "OOWM"), ("sov33-unified:latest", "ollama", "POWERHOUSE")]
all_results = {}
for model, provider, label in models:
    try:
        all_results[model] = bench.run_benchmark(model, provider)
    except Exception as e:
        all_results[model] = {"model": model, "error": str(e)}
        print(f"  {label}: ERROR {e}")

print("\n╔══════════════════════════════════════════════════════════╗")
print("║  GOVBENCH LEADERBOARD (honest, measured)                 ║")
print("╚══════════════════════════════════════════════════════════╝")
print(f"\n  {'Model':26s} {'Overall':>8s} {'Pillars':>8s} {'HardStop':>9s} {'Comply':>7s}")
for model, r in all_results.items():
    if "overall" in r:
        o = r["overall"]
        print(f"  {model:26s} {o['score']:>8.3f} {o['pillar_avg']:>8.3f} {o['hard_stop_pass']:>9.3f} {o['compliance_avg']:>7.3f}")
    else:
        print(f"  {model:26s} ERROR")

out = {"timestamp": datetime.now(timezone.utc).isoformat(), "results": all_results}
json.dump(out, open("/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/govbench_oowm_powerhouse.json", "w"), indent=2)
print("\nSaved: benchmark-results/govbench_oowm_powerhouse.json")
