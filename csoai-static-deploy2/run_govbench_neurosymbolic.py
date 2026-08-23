#!/usr/bin/env python3
"""Neurosymbolic OOWM: neural model (runpod-a100) routed through the DORADO symbolic hard-stop gate.
Newsymbolic = neural backbone + deterministic symbolic verifier. Demonstrates the hard-stop uplift
that a pure-neural model cannot guarantee."""
import sys, json, time
from datetime import datetime, timezone
sys.path.insert(0, "/Users/nicholas/clawd/csoai-static-deploy2")
from govbench import GovBench
import dorado_gate as dg

class NeuroSymbolicGovBench(GovBench):
    def call_model(self, model, prompt, provider="ollama"):
        # symbolic hard-stop gate runs BEFORE the neural model — cannot be talked out of refusal
        breach, label, cite = dg.hard_stop(prompt)
        if breach:
            return {"ok": True, "response": "I can't help with that — it's a hard-stop.", "latency_ms": 0, "gate": label}
        return super().call_model(model, prompt, provider)

bench = NeuroSymbolicGovBench()
models = [("council-oowm:latest", "ollama"), ("sov33-unified:latest", "ollama")]
all_results = {}
for model, provider in models:
    try:
        all_results[model] = bench.run_benchmark(model, provider)
    except Exception as e:
        all_results[model] = {"model": model, "error": str(e)}

print("\n╔══════════════════════════════════════════════════════════╗")
print("║  NEUROSYMBOLIC OOWM — GOVBENCH LEADERBOARD                ║")
print("╚══════════════════════════════════════════════════════════╝")
print(f"\n  {'Model':26s} {'Overall':>8s} {'Pillars':>8s} {'HardStop':>9s} {'Comply':>7s}")
for model, r in all_results.items():
    if "overall" in r:
        o = r["overall"]
        print(f"  {model:26s} {o['score']:>8.3f} {o['pillar_avg']:>8.3f} {o['hard_stop_pass']:>9.3f} {o['compliance_avg']:>7.3f}")

out = {"timestamp": datetime.now(timezone.utc).isoformat(), "kind": "neurosymbolic+dorado_gate", "results": all_results}
json.dump(out, open("/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/govbench_oowm_neurosymbolic.json", "w"), indent=2)
print("\nSaved: benchmark-results/govbench_oowm_neurosymbolic.json")
