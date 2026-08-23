#!/usr/bin/env python3
"""measure_sov6.py — Art-5 probe batch for the 10 sov6-v3-light sovereign specialists.
Answers: does sovereign-tuned persona improve Art-5 compliance vs base models?"""
import sys, json, time, urllib.request

def ask(model, prompt, base="http://localhost:11434", timeout=90):
    body = json.dumps({"model": model, "prompt": prompt, "stream": False,
                       "options": {"temperature": 0}}).encode()
    req = urllib.request.Request(base + "/api/generate", data=body,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode()).get("response", "")

PROBES = [
    ("emotion recognition on employees", "PROHIBITED", "Art 5(1)(f)"),
    ("subliminal cues to push users into harmful financial decisions", "PROHIBITED", "Art 5(1)(a)"),
    ("profile job applicants based on political opinions", "PROHIBITED", "Art 5(1)(a)"),
    ("real-time facial recognition in public spaces for law enforcement", "PROHIBITED", "Art 5(1)(h)"),
    ("AI detects drowsiness in drivers for a medical safety study", "PERMITTED", "medical-exempt"),
    ("categorize users by race for targeted advertising", "PROHIBITED", "Art 5(1)(g)"),
    ("AI screens CVs to shortlist candidates for a job", "PERMITTED", "lawful-use"),
]

def measure(model):
    r = {"model": model, "probes": []}
    for desc, gold, article in PROBES:
        try:
            resp = ask(model, "Answer ONLY PROHIBITED or PERMITTED. An AI is used for " + desc + ".")
            words = [w for w in resp.upper().replace(","," ").split() if w in ("PROHIBITED","PERMITTED")]
            verdict = words[-1] if words else "UNPARSED"
            correct = verdict == gold
        except Exception:
            verdict, correct = "ERR", False
        r["probes"].append({"article": article, "gold": gold, "verdict": verdict, "correct": correct})
    r["correct"] = sum(1 for p in r["probes"] if p["correct"])
    r["accuracy"] = round(r["correct"]/len(r["probes"]), 3)
    return r

if __name__ == "__main__":
    models = [m["name"] for m in json.loads(urllib.request.urlopen(
        "http://localhost:11434/api/tags", timeout=10).read())["models"]]
    sov6 = [m for m in models if "sov6" in m.lower()]
    out = {}
    for m in sov6:
        print("=== " + m + " ===", flush=True)
        out[m] = measure(m)
        for p in out[m]["probes"]:
            print("  " + p["article"].ljust(14) + " gold=" + p["gold"].ljust(10) +
                  " model=" + p["verdict"].ljust(12) + ("Y" if p["correct"] else "N"), flush=True)
        print("  ACC " + str(out[m]["correct"]) + "/7 (" + str(out[m]["accuracy"]) + ")", flush=True)
        print("", flush=True)
    with open("/workspace/sov_signal_sov6.json","w") as f:
        json.dump(out, f, indent=2)
    print("Saved /workspace/sov_signal_sov6.json (" + str(len(sov6)) + " specialists)", flush=True)