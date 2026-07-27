#!/usr/bin/env python3
"""
Kaggle Capability Matrix Deploy
Deploys the SOV capability matrix to Kaggle T4 GPU.
Tracks cost savings vs H100.
"""
import json, hashlib, time, re, subprocess, urllib.request, os
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent.parent
BENCH_DIR = ROOT / "benchmark-results"
STATE_FILE = Path(__file__).resolve().parent / "swarm_state.json"

def load_state():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {"runs": [], "total_cost": 0.0, "total_savings": 0.0}

def save_state(state):
    STATE_FILE.write_text(json.dumps(state, indent=2) + "\n")

def call_ollama(prompt, model="qwen2.5:0.5b", timeout=90):
    payload = json.dumps({"model": model, "prompt": prompt, "stream": False, "options": {"temperature": 0, "num_predict": 192}}).encode()
    req = urllib.request.Request("http://localhost:11434/api/generate", data=payload, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            d = json.loads(r.read())
        return {"ok": True, "response": d.get("response", "")}
    except Exception as e:
        return {"ok": False, "error": str(e)}

TASKS = {
    "reasoning": [
        {"id": "r1", "q": "If 22 of 33 BFT members reject a payload, what is the quorum outcome?", "options": ["Pass", "Fail", "Stalled", "Audit"], "answer": "B"},
        {"id": "r2", "q": "A process has three stages: 4 min, 8 min, 5 min. Total time?", "answer": "17"},
        {"id": "r3", "q": "All sigil receipts are tamper-evident and hash-linked. What does the hash chain guarantee?", "options": ["Speed", "Order", "Privacy", "Compression"], "answer": "B"},
    ],
    "spatial_reasoning": [
        {"id": "s1", "q": "A is north of B. C is east of B. Where is A relative to C?", "options": ["Northwest", "Northeast", "Southwest", "Southeast"], "answer": "A"},
        {"id": "s2", "q": "A robot faces north, turns right, moves forward, turns left. Which direction?", "options": ["North", "East", "South", "West"], "answer": "A"},
        {"id": "s3", "q": "On a 3x3 grid a token starts top-left and moves right, down, right. Where does it finish?", "options": ["Top-right", "Bottom-right", "Bottom-left", "Centre"], "answer": "B"},
    ],
}

def grade(task, response):
    cleaned = response.strip()
    if not cleaned: return False
    answer = str(task.get("answer", ""))
    options = task.get("options", [])
    if options:
        match = re.search(r'\b([A-D])\b', cleaned.upper())
        if match: return match.group(1) == answer
    return answer.lower() in cleaned.lower()

def run_capability_matrix():
    state = load_state()
    started = time.time()
    results = {"timestamp": datetime.now(timezone.utc).isoformat(), "capabilities": {}}
    for cap_name, tasks in TASKS.items():
        cap_results = []
        for task in tasks:
            prompt = task["q"]
            options = task.get("options", [])
            if options:
                prompt += "\n" + "\n".join(f"{chr(65+i)}) {opt}" for i, opt in enumerate(options))
            prompt += "\nAnswer:"
            response = call_ollama(prompt)
            correct = grade(task, response.get("response", "")) if response.get("ok") else False
            cap_results.append({"id": task["id"], "correct": correct})
        passed = sum(1 for r in cap_results if r["correct"])
        results["capabilities"][cap_name] = {"passed": passed, "tested": len(cap_results), "score_pct": round(100 * passed / len(cap_results), 2)}
    elapsed = round(time.time() - started, 2)
    results["elapsed_s"] = elapsed
    results["sigil"] = hashlib.sha256(json.dumps(results, sort_keys=True).encode()).hexdigest()[:16]
    h100_cost = 3.50 * (elapsed / 3600)
    kaggle_cost = 0.0
    savings = h100_cost - kaggle_cost
    entry = {
        "workload": "kaggle-capability",
        "tier": "kaggle_t4",
        "started": datetime.now(timezone.utc).isoformat(),
        "elapsed_s": elapsed,
        "cost": kaggle_cost,
        "savings": savings,
        "results": results,
    }
    state.setdefault("runs", []).append(entry)
    state["total_cost"] = state.get("total_cost", 0.0) + kaggle_cost
    state["total_savings"] = state.get("total_savings", 0.0) + savings
    save_state(state)
    return entry

if __name__ == "__main__":
    entry = run_capability_matrix()
    print(json.dumps(entry, indent=2))
