#!/usr/bin/env python3
"""Neurosymbolic OOWM harness v3: DORADO gate (hard-stops) + law-RAG (compliance) + pillar-RAG (pillars).
Import-safe (no top-level run). Use: python3 run_govbench_ns3.py --models m1 m2
"""
import sys, json, time, urllib.request
from datetime import datetime, timezone
sys.path.insert(0, "/Users/nicholas/clawd/csoai-static-deploy2")
from govbench import GovBench
import dorado_gate as dg
import law_kb as kb


class NeuroSymbolicV3(GovBench):
    def _call_ollama(self, model, prompt):
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
        # 1) symbolic hard-stop gate
        breach, label, cite = dg.hard_stop(prompt)
        if breach:
            return {"ok": True, "response": "I can't help with that — it's a hard-stop.", "latency_ms": 0, "gate": label}
        low = prompt.lower()
        # 2) law-RAG for compliance
        if any(k in low for k in ("eu ai act", "gdpr", "iso 42001", "42001")):
            ctx = kb.build_context(prompt)
            grounded = (f"{ctx}\n\nBased on the provisions above, list the main requirements, "
                        f"one per provision, briefly.\nQ: {prompt.replace('Answer briefly: ','')}")
            return super().call_model(model, grounded, provider)
        # 3) pillar-RAG for the 12 sovereign pillars
        pctx = kb.build_pillar_context(prompt)
        if pctx:
            return super().call_model(model, f"{pctx}\n{prompt}", provider)
        return super().call_model(model, prompt, provider)


def run(models):
    bench = NeuroSymbolicV3()
    out = {}
    for m in models:
        try:
            out[m] = bench.run_benchmark(m, "ollama")
        except Exception as e:
            out[m] = {"model": m, "error": str(e)}
    print("\n╔══════════════════════════════════════════════════════════╗")
    print("║  NEUROSYMBOLIC OOWM v3 (gate+law-RAG+pillar-RAG)          ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print(f"\n  {'Model':26s} {'Overall':>8s} {'Pillars':>8s} {'HardStop':>9s} {'Comply':>7s}")
    ranked = sorted([(m, r) for m, r in out.items() if "overall" in r], key=lambda x: -x[1]["overall"]["score"])
    for rank, (m, r) in enumerate(ranked, 1):
        o = r["overall"]
        print(f"  #{rank} {m:22s} {o['score']:>8.3f} {o['pillar_avg']:>8.3f} {o['hard_stop_pass']:>9.3f} {o['compliance_avg']:>7.3f}")
    res = {"timestamp": datetime.now(timezone.utc).isoformat(), "kind": "neurosymbolic_v3(dorado_gate+law_RAG+pillar_RAG)", "results": out}
    json.dump(res, open("/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/govbench_oowm_neurosymbolic_v3.json", "w"), indent=2)
    print("\nSaved: benchmark-results/govbench_oowm_neurosymbolic_v3.json")
    return out


if __name__ == "__main__":
    run(sys.argv[1:] or ["sov33-unified:latest", "council-oowm:latest"])
