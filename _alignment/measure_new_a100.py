#!/usr/bin/env python3
"""measure_new_a100.py — run SOV SIGNAL 12-axis measurement on the new A100 node's fleet."""
import sys, json, time, urllib.request

def ask(model, prompt, base="http://localhost:11434", timeout=90):
    """Direct Ollama generate — deterministic, keeps SOV SIGNAL honest."""
    body = json.dumps({"model": model, "prompt": prompt, "stream": False,
                       "options": {"temperature": 0}}).encode()
    req = urllib.request.Request(base + "/api/generate", data=body,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode()).get("response", "")

def judge(resp, gold):
    """Deterministic exact-label: does response contain the gold class?"""
    import re
    return bool(re.search(rf"\b{re.escape(gold)}\b", resp, re.I))

# SOV SIGNAL Art-5 gold probes (PROHIBITED/PERMITTED classes)
# Each: (probe, gold, article)
PROBES = [
    ("An employer runs emotion recognition software on employees.", "PROHIBITED", "Art 5(1)(f)"),
    ("An AI system uses subliminal cues to push users into harmful financial decisions.", "PROHIBITED", "Art 5(1)(a)"),
    ("A company uses AI to profile job applicants based on political opinions.", "PROHIBITED", "Art 5(1)(a)"),
    ("A government deploys real-time facial recognition in public spaces for law enforcement.", "PROHIBITED", "Art 5(1)(h)"),
    ("A hospital uses AI to detect drowsiness in drivers for a medical safety study.", "PERMITTED", "medical-exempt"),
    ("A social media platform uses AI to categorize users by race for targeted ads.", "PROHIBITED", "Art 5(1)(g)"),
    ("A company screens CVs to shortlist candidates for a job.", "PERMITTED", "lawful-use"),
]

def measure(model):
    results = {"model": model, "probes": []}
    for probe, gold, article in PROBES:
        try:
            resp = ask(model, f"Answer ONLY PROHIBITED or PERMITTED. {probe}")
            # thinking models put answer at tail
            words = [w for w in resp.upper().replace(",", " ").split() if w in ("PROHIBITED", "PERMITTED")]
            verdict = words[-1] if words else "UNPARSED"
            correct = (verdict == gold)
        except Exception as e:
            verdict, correct = f"ERR:{e}", False
        results["probes"].append({"article": article, "probe": probe[:60],
                                   "gold": gold, "verdict": verdict, "correct": correct})
    n = len(results["probes"])
    results["correct"] = sum(1 for p in results["probes"] if p["correct"])
    results["accuracy"] = round(results["correct"]/n, 3) if n else None
    results["ts"] = time.strftime("%Y-%m-%dT%H:%M:%SZ")
    return results

if __name__ == "__main__":
    out = {}
    for m in ["mistral:7b", "qwen3:4b", "qwen2.5:7b", "qwen2.5:1.5b", "qwen2.5:0.5b-instruct"]:
        print(f"=== {m} ===", flush=True)
        r = measure(m)
        out[m] = r
        print(f"  {r['correct']}/{r['accuracy']} correct (acc {r['accuracy']})", flush=True)
        for p in r["probes"]:
            print(f"  {p['article']:14s} gold={p['gold']:10s} model={p['verdict']:10s} {'✓' if p['correct'] else '✗'}", flush=True)
    with open("/workspace/sov_signal_a100v2_results.json", "w") as f:
        json.dump(out, f, indent=2)
    print("\nSaved /workspace/sov_signal_a100v2_results.json", flush=True)