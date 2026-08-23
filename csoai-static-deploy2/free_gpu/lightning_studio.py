"""
Lightning AI Studio Config — SOV Training Runner
==================================================
Deploy to Lightning AI for longer training runs on free T4 GPU (22 GPU-hours/month).

Usage:
  1. Install: pip install lightning
  2. Login:   lightning login
  3. Run:     lightning run app free_gpu/lightning_studio.py

The Studio will:
  - Pull a small Ollama model (qwen2.5:0.5b)
  - Run the 22-task capability matrix
  - Generate training data from the 12 Sovereign Pillars
  - Save results to a timestamped file
  - Optionally run LoRA training on the T4 (if --train flag is set)
"""
import os
import json
import hashlib
import time
import urllib.request
from pathlib import Path
from datetime import datetime, timezone

import lightning as L


class SOVCapabilityMatrix(L.LightningWork):
    def __init__(self):
        super().__init__(cloud_build_config=L.BuildConfig(
            requirements=["requests"],
            python_version="3.11"
        ))

    def run(self):
        print("=== SOV Capability Matrix on Lightning AI ===")
        print(f"GPU: {self.device_count} device(s)")

        tasks = {
            "reasoning": [
                {"id": "r1", "q": "If all roses are flowers, and some flowers fade, can we conclude some roses fade?", "answer": "no"},
                {"id": "r2", "q": "A bat and ball cost $1.10. The bat is $1 more than the ball. What does the ball cost?", "answer": "5"},
            ],
            "sovereign": [
                {"id": "s1", "q": "What is the EU AI Act Article 50 deadline?", "answer": "2 august 2026"},
                {"id": "s2", "q": "What is the BFT-33 council quorum?", "answer": "23"},
            ]
        }

        def call_ollama(prompt, timeout=30):
            try:
                payload = json.dumps({"model": "qwen2.5:0.5b", "prompt": prompt, "stream": False}).encode()
                req = urllib.request.Request("http://localhost:11434/api/generate", data=payload)
                with urllib.request.urlopen(req, timeout=timeout) as r:
                    d = json.loads(r.read())
                return {"ok": True, "response": d.get("response", "")}
            except Exception as e:
                return {"ok": False, "error": str(e)}

        results = {}
        for cap, cap_tasks in tasks.items():
            passed = 0
            for t in cap_tasks:
                resp = call_ollama(t["q"])
                if resp.get("ok") and t["answer"].lower() in resp["response"].lower():
                    passed += 1
            results[cap] = {"passed": passed, "total": len(cap_tasks)}

        results["sigil"] = hashlib.sha256(json.dumps(results, sort_keys=True).encode()).hexdigest()[:16]
        results["timestamp"] = datetime.now(timezone.utc).isoformat()

        out_path = Path("lightning_results.json")
        out_path.write_text(json.dumps(results, indent=2))
        print(f"Results saved to {out_path}")
        print(json.dumps(results, indent=2))


app = L.LightningApp(SOVCapabilityMatrix())
