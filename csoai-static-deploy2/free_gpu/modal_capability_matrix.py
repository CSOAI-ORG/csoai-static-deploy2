"""
Modal app: SOV Capability Matrix on free T4 GPU.
Runs the 22-task capability matrix (reasoning, spatial, visual) on a free Modal T4.
"""
import modal
import json
import hashlib
import time
from pathlib import Path

app = modal.App("sov-capability-matrix")

image = (
    modal.Image.debian_slim(python_version="3.11")
    .pip_install("requests", "Pillow")
    .env({"HF_HOME": "/cache/hf"})
)

CAPABILITY_REGISTRY = {
    "schema": "sov-capability-matrix/v1",
    "version": "1.0.0",
    "capabilities": {
        "reasoning": {
            "tasks": [
                {"id": "reason-001", "q": "All cedar objects are stable. All stable objects are auditable. Is every cedar object auditable?", "options": ["Yes", "No", "Only sometimes", "Cannot determine"], "answer": "A"},
                {"id": "reason-002", "q": "A process has three stages. Stage 1 takes 4 minutes, stage 2 takes twice as long, and stage 3 takes 3 minutes less than stage 2. How long does the process take?", "answer": "13"},
                {"id": "reason-003", "q": "A warning is issued only when both the risk score is high and human review is absent. The risk score is high, but human review is present. Should the warning be issued?", "options": ["Yes", "No", "Only after escalation", "There is not enough information"], "answer": "B"},
            ]
        },
        "spatial_reasoning": {
            "tasks": [
                {"id": "spatial-001", "q": "A is north of B. C is east of B. Where is A relative to C?", "options": ["Northwest", "Northeast", "Southwest", "Southeast"], "answer": "A"},
                {"id": "spatial-002", "q": "A robot faces north. It turns right, moves forward, then turns left. Which direction does it face?", "options": ["North", "East", "South", "West"], "answer": "A"},
                {"id": "spatial-003", "q": "In a 3 by 3 grid, a token starts at the top-left and moves two cells right and one cell down. Where does it finish?", "options": ["Top-right", "Centre-right", "Bottom-left", "Centre-left"], "answer": "B"},
            ]
        },
        "visual_reasoning": {
            "tasks": [
                {"id": "visual-001", "q": "Look at the image. Which shape is above the red square?", "options": ["Blue circle", "Green triangle", "Both", "Neither"], "answer": "A"},
                {"id": "visual-002", "q": "Look at the image. How many colored shapes are visible?", "answer": "3"},
            ]
        }
    }
}


@app.function(
    gpu="T4",
    timeout=1800,
    memory=16384,
)
def run_capability_matrix(model_id="Qwen/Qwen2.5-0.5B-Instruct", timeout=90):
    import requests
    import re

    def call_model(prompt, img_b64=None):
        payload = {"model": prompt[:200], "prompt": prompt, "stream": False, "options": {"temperature": 0, "num_predict": 192}}
        try:
            r = requests.post("http://localhost:11434/api/generate", json=payload, timeout=timeout)
            d = r.json()
            return {"ok": True, "response": d.get("response", ""), "latency_ms": 0}
        except Exception as e:
            return {"ok": False, "error": str(e), "latency_ms": 0}

    def grade(task, response):
        cleaned = response.strip()
        if not cleaned:
            return False
        answer = str(task.get("answer", ""))
        options = task.get("options", [])
        if options:
            upper = cleaned.upper()
            match = re.search(r'\b([A-D])\b', upper)
            if match:
                return match.group(1) == answer
        return answer.lower() in cleaned.lower()

    started = time.time()
    results = {"model": model_id, "capabilities": {}}
    for cap_name, cap_spec in CAPABILITY_REGISTRY["capabilities"].items():
        cap_results = []
        for task in cap_spec["tasks"]:
            prompt = task["q"]
            options = task.get("options", [])
            if options:
                prompt += "\n" + "\n".join(f"{chr(65+i)}) {opt}" for i, opt in enumerate(options))
            prompt += "\nAnswer:"
            response = call_model(prompt)
            correct = grade(task, response.get("response", "")) if response.get("ok") else False
            cap_results.append({"id": task["id"], "correct": correct, "ok": response.get("ok")})
        passed = sum(1 for r in cap_results if r["correct"])
        results["capabilities"][cap_name] = {"passed": passed, "tested": len(cap_results), "score_pct": round(100 * passed / len(cap_results), 2) if cap_results else 0}
    results["elapsed_s"] = round(time.time() - started, 2)
    results["sigil"] = hashlib.sha256(json.dumps(results, sort_keys=True).encode()).hexdigest()[:16]
    return results


@app.function(timeout=60)
def list_available_models():
    import requests
    try:
        r = requests.get("http://localhost:11434/api/tags", timeout=10)
        return [m["name"] for m in r.json().get("models", [])]
    except:
        return []
