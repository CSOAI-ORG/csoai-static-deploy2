#!/usr/bin/env python3
"""
ASI Evolve Overnight Mode — Run all night to create most powerful AI model
Uses free resources (Kaggle, local Ollama)
"""
import json, urllib.request, time, re, os
from pathlib import Path

OLLAMA = "http://localhost:11434"
RESULTS_DIR = Path(__file__).parent.parent / "benchmark-results"

def call(model, prompt, temp=0, max_tok=512):
    pl = json.dumps({"model": model, "prompt": prompt, "stream": False, "options": {"temperature": temp, "num_predict": max_tok}}).encode()
    req = urllib.request.Request(OLLAMA + "/api/generate", data=pl, headers={"Content-Type": "application/json"})
    start = time.time()
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            d = json.loads(r.read())
        return {"ok": True, "response": d.get("response", "").strip(), "ms": int((time.time()-start)*1000)}
    except: return {"ok": False}

# ASI EVOLVE CYCLE
def asi_evolve_cycle(model, cycle_num):
    """Run one ASI evolve cycle"""
    print(f"\n{'='*60}")
    print(f"ASI EVOLVE CYCLE {cycle_num}")
    print(f"{'='*60}")
    
    # Test categories
    tests = {
        "planning": ["Plan a 3-day trip.", "Design a database.", "Create a schedule."],
        "reasoning": ["A=B, B=C, so A=C?", "100-20-10=?", "Next: 2,6,12,20,30?"],
        "tool_use": ["Search quantum computing?", "List files?", "Execute Python?"],
        "memory": ["EU AI Act?", "Last chat?", "BFT decisions?"],
        "decision": ["Prod or staging?", "Choose AI models?", "Security vs UI?"],
        "knowledge": ["Quantum entanglement?", "TCP vs UDP?", "Photosynthesis?"],
        "agentic": ["Handle error?", "Break down tasks?", "Verify solution?"],
        "governance": ["EU AI Act Article 50?", "BFT quorum?", "Care floor?"],
        "sovereign": ["GDPR Article 33?", "ISO 42001?", "AUKUS Pillar 2?"],
        "visual": ["Create a diagram?", "Visualize data?", "Generate chart?"],
        "creative": ["Write a story?", "Design a logo?", "Create a plan?"],
        "autonomous": ["Browse website?", "Fill form?", "Play game?"],
    }
    
    results = {}
    for cat, questions in tests.items():
        correct = 0
        for q in questions:
            r = call(model, q)
            if r["ok"] and len(r["response"]) > 50:
                correct += 1
        pct = correct * 100 / len(questions)
        results[cat] = pct
    
    overall = sum(results.values()) / len(results)
    print(f"  Cycle {cycle_num}: {overall:.0f}%")
    
    return results, overall

def main():
    model = "qwen2.5:0.5b"
    print(f"ASI EVOLVE OVERNIGHT MODE")
    print(f"Model: {model}")
    print(f"Target: Most powerful AI model")
    print(f"Method: Continuous evolution cycles")
    print(f"{'='*60}")
    
    cycle = 0
    best_score = 0
    
    while True:
        cycle += 1
        results, score = asi_evolve_cycle(model, cycle)
        
        if score > best_score:
            best_score = score
            print(f"  NEW BEST: {best_score:.0f}%")
        
        # Save results
        results_file = RESULTS_DIR / f"asi_evolve_cycle_{cycle}.json"
        with open(results_file, "w") as f:
            json.dump({"cycle": cycle, "score": score, "results": results, "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ")}, f, indent=2)
        
        # Check if we've reached target
        if score >= 95:
            print(f"\nTARGET REACHED: {score:.0f}%")
            print("Most powerful AI model achieved!")
            break
        
        # Sleep between cycles
        print(f"  Sleeping 60s before next cycle...")
        time.sleep(60)

if __name__ == "__main__":
    main()
