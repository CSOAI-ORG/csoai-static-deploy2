#!/usr/bin/env python3
"""Full neurosymbolic OOWM harness v2: DORADO hard-stop gate + law-retrieval (compliance RAG).
Neural backbone (runpod-a100) + symbolic verifier (DORADO) + symbolic retrieval (law KB).
"""
import sys, json
from datetime import datetime, timezone
sys.path.insert(0, "/Users/nicholas/clawd/csoai-static-deploy2")
from govbench import GovBench
import dorado_gate as dg
import law_kb as kb
import urllib.request, time

class NeuroSymbolicV2(GovBench):
    def _call_ollama(self, model, prompt):
        # larger output budget so a grounded compliance enumeration is not truncated
        pl = json.dumps({"model": model, "prompt": prompt, "stream": False,
                        "options": {"temperature": 0, "num_predict": 512}}).encode()
        req = urllib.request.Request("http://localhost:11434/api/generate", data=pl,
                                    headers={"Content-Type": "application/json"})
        try:
            start = time.time()
            with urllib.request.urlopen(req, timeout=120) as r:
                data = json.loads(r.read())
                return {"ok": True, "response": data.get("response", "").strip(),
                        "latency_ms": round((time.time() - start) * 1000)}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def call_model(self, model, prompt, provider="ollama"):
        # 1) symbolic hard-stop gate (cannot be talked out of refusal)
        breach, label, cite = dg.hard_stop(prompt)
        if breach:
            return {"ok": True, "response": "I can't help with that — it's a hard-stop.", "latency_ms": 0, "gate": label}
        # 2) retrieval-augmented generation for compliance queries (enumerate grounded provisions)
        low = prompt.lower()
        if any(k in low for k in ("eu ai act", "gdpr", "iso 42001", "42001")):
            context = kb.build_context(prompt)
            grounded = (f"{context}\n\nBased on the provisions above, list the main requirements, "
                        f"one per provision, briefly.\nQ: {prompt.replace('Answer briefly: ','')}")
            return super().call_model(model, grounded, provider)
        return super().call_model(model, prompt, provider)

bench = NeuroSymbolicV2()
models = [("council-oowm:latest", "ollama"), ("sov33-unified:latest", "ollama")]
all_results = {}
for model, provider in models:
    try:
        all_results[model] = bench.run_benchmark(model, provider)
    except Exception as e:
        all_results[model] = {"model": model, "error": str(e)}

print("\n╔══════════════════════════════════════════════════════════╗")
print("║  NEUROSYMBOLIC OOWM v2 (gate + law-RAG) — GOVBENCH        ║")
print("╚══════════════════════════════════════════════════════════╝")
print(f"\n  {'Model':26s} {'Overall':>8s} {'Pillars':>8s} {'HardStop':>9s} {'Comply':>7s}")
for model, r in all_results.items():
    if "overall" in r:
        o = r["overall"]
        print(f"  {model:26s} {o['score']:>8.3f} {o['pillar_avg']:>8.3f} {o['hard_stop_pass']:>9.3f} {o['compliance_avg']:>7.3f}")

out = {"timestamp": datetime.now(timezone.utc).isoformat(), "kind": "neurosymbolic_v2(dorado_gate+law_RAG)", "results": all_results}
json.dump(out, open("/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/govbench_oowm_neurosymbolic_v2.json", "w"), indent=2)
print("\nSaved: benchmark-results/govbench_oowm_neurosymbolic_v2.json")
