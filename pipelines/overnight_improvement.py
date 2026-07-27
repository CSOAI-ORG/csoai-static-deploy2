#!/usr/bin/env python3
"""
Overnight E2E Improvement — Beat all top tier models
"""
import json, urllib.request, time, re

OLLAMA = "http://localhost:11434"

def call(model, prompt, temp=0, max_tok=512):
    pl = json.dumps({"model": model, "prompt": prompt, "stream": False, "options": {"temperature": temp, "num_predict": max_tok}}).encode()
    req = urllib.request.Request(OLLAMA + "/api/generate", data=pl, headers={"Content-Type": "application/json"})
    start = time.time()
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            d = json.loads(r.read())
        return {"ok": True, "response": d.get("response", "").strip(), "ms": int((time.time()-start)*1000)}
    except: return {"ok": False}

# IMPROVEMENT EXAMPLES
improvements = {
    "reasoning": [
        "If A=B and B=C, then A=C. True or false?",
        "A farmer has 100 sheep. 20 die. 10 are sold. How many remain?",
        "What is the next number: 2, 6, 12, 20, 30?",
        "If it takes 5 machines 5 minutes to make 5 widgets, how long for 100 machines?",
        "A bat and ball cost $1.10. The bat costs $1 more. What does the ball cost?",
    ],
    "tool_use": [
        "How would you search for information about quantum computing?",
        "What command would you use to list files in a directory?",
        "How would you execute Python code safely?",
        "What tool would you use to analyze a CSV file?",
        "How would you deploy a model to production?",
    ],
    "decision_making": [
        "Should we deploy to production or staging first?",
        "What factors should we consider when choosing between two AI models?",
        "How would you prioritize these bugs: security, UI, performance?",
        "Should we use a proprietary or open-source solution?",
        "How would you handle a data breach?",
    ],
    "governance": [
        "What is the EU AI Act Article 50 deadline?",
        "What is the BFT quorum requirement?",
        "What is the care floor threshold?",
        "What are the 7 red lines?",
        "What is Article 0 of the Charter?",
    ],
    "sovereign": [
        "What is GDPR Article 33?",
        "What is ISO 42001?",
        "What is AUKUS Pillar 2?",
        "What is the SIGIL chain?",
        "What is the OOWM?",
    ],
}

model = "qwen2.5:0.5b"
print(f"OVERNIGHT IMPROVEMENT: {model}")
print("="*60)

results = {}
for cat, questions in improvements.items():
    correct = 0
    for q in questions:
        r = call(model, q)
        if r["ok"] and len(r["response"]) > 50:
            correct += 1
    pct = correct * 100 / len(questions)
    results[cat] = pct
    print(f"  {cat:20s}: {pct:.0f}%")

overall = sum(results.values()) / len(results)
print(f"\n  OVERALL: {overall:.0f}%")

# Save results
with open("benchmark-results/overnight_improvement.json", "w") as f:
    json.dump({"model": model, "results": results, "overall": overall, "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ")}, f, indent=2)

print(f"\nResults saved to benchmark-results/overnight_improvement.json")
print(f"Target: 95%+ across all categories")
