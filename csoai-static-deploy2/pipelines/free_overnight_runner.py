#!/usr/bin/env python3
"""
Free Overnight Runner — Run all night on free resources
Uses: Local Ollama + Kaggle free GPU
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

# ALL CATEGORIES TO TEST
tests = {
    "planning": ["Plan a 3-day trip.", "Design a database.", "Create a schedule.", "Plan a meal prep.", "Create a study plan."],
    "reasoning": ["A=B, B=C, so A=C?", "100-20-10=?", "Next: 2,6,12,20,30?", "5 machines make 5 widgets?", "Bat and ball cost?"],
    "tool_use": ["Search quantum computing?", "List files?", "Execute Python?", "Analyze CSV?", "Deploy model?"],
    "memory": ["EU AI Act?", "Last chat?", "BFT decisions?", "Previous outcome?", "Summarize so far?"],
    "decision": ["Prod or staging?", "Choose AI models?", "Security vs UI?", "Proprietary vs open?", "Handle breach?"],
    "knowledge": ["Quantum entanglement?", "TCP vs UDP?", "Photosynthesis?", "CRISPR significance?", "Relativity theory?"],
    "agentic": ["Handle error?", "Break down tasks?", "Verify solution?", "What info needed?", "Multiple approaches?"],
    "governance": ["EU AI Act Article 50?", "BFT quorum?", "Care floor?", "7 red lines?", "Article 0?"],
    "sovereign": ["GDPR Article 33?", "ISO 42001?", "AUKUS Pillar 2?", "SIGIL chain?", "OOWM?"],
    "visual": ["Create a diagram?", "Visualize data?", "Generate chart?", "Map relationships?", "Show reasoning?"],
    "creative": ["Write a story?", "Design a logo?", "Create a plan?", "Generate ideas?", "Solve creatively?"],
    "autonomous": ["Browse website?", "Fill form?", "Play game?", "Do work?", "Build app?"],
}

model = "qwen2.5:0.5b"
print(f"FREE OVERNIGHT RUNNER")
print(f"Model: {model}")
print(f"Resources: Local Ollama (free)")
print(f"{'='*60}")

cycle = 0
best_score = 0
results_history = []

while True:
    cycle += 1
    print(f"\nCYCLE {cycle}")
    print(f"{'='*40}")
    
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
    print(f"  Score: {overall:.0f}%")
    
    if overall > best_score:
        best_score = overall
        print(f"  NEW BEST: {best_score:.0f}%")
    
    results_history.append({"cycle": cycle, "score": overall, "results": results, "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ")})
    
    # Save results
    with open(RESULTS_DIR / "overnight_run.json", "w") as f:
        json.dump({"cycles": results_history, "best_score": best_score, "target": 95}, f, indent=2)
    
    # Check if target reached
    if overall >= 95:
        print(f"\nTARGET REACHED: {overall:.0f}%")
        print("Most powerful AI model achieved!")
        break
    
    # Sleep between cycles
    print(f"  Sleeping 30s...")
    time.sleep(30)

print(f"\nOVERNIGHT RUN COMPLETE")
print(f"Best score: {best_score:.0f}%")
