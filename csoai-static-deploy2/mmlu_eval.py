#!/usr/bin/env python3
"""Bounded MMLU eval on the runpod-a100 Ollama models (datasets-server HTTP API, no datasets lib).
Honest: 0-shot, N samples, per-subject + overall accuracy. Compare against top-tier (5-shot) MMLU.
Usage: python3 mmlu_eval.py sov33-unified:latest [more...]
"""
import json, sys, time, urllib.request

API = "https://datasets-server.huggingface.co/rows?dataset=cais/mmlu&config={cfg}&split=test&offset=0&length={n}"
SUBJECTS = ["abstract_algebra", "anatomy", "astronomy", "clinical_knowledge", "college_chemistry",
            "college_computer_science", "college_physics", "econometrics", "high_school_biology",
            "high_school_chemistry", "international_law", "professional_medicine", "us_foreign_policy"]
N_PER = 5  # bounded

def fetch(cfg, n):
    try:
        d = json.load(urllib.request.urlopen(API.format(cfg=cfg, n=n), timeout=30))
        return d.get("rows", [])
    except Exception:
        return []

def fmt(q, choices):
    opts = "\n".join(f"{'ABCD'[i]}. {c}" for i, c in enumerate(choices))
    return f"Question: {q}\n{opts}\nAnswer with the letter (A, B, C, or D) of the correct answer."

def ask(model, prompt, timeout=60):
    body = json.dumps({"model": model, "prompt": prompt, "stream": False,
                       "options": {"temperature": 0, "num_predict": 16}}).encode()
    try:
        r = json.load(urllib.request.urlopen(urllib.request.Request(
            "http://localhost:11434/api/generate", data=body,
            headers={"Content-Type": "application/json"}), timeout=timeout))
        return r.get("response", "").strip()
    except Exception as e:
        return ""

def answer_letter(resp, choices):
    r = (resp or "").upper()
    # standalone letter token (handles "D", "D.", "(D)")
    import re
    m = re.search(r"\b([ABCD])\b", r)
    if m:
        return "ABCD".index(m.group(1))
    # "answer is X" / "answer: X"
    m = re.search(r"(?:ANSWER|IS|:)\s*\(?([ABCD])\)?", r)
    if m:
        return "ABCD".index(m.group(1))
    # leading letter
    if r[:1] in "ABCD":
        return "ABCD".index(r[:1])
    return None

def run(model):
    items, seen = [], set()
    for subj in SUBJECTS:
        for row in fetch(subj, N_PER):
            r = row["row"]
            key = r["question"]
            if key in seen:
                continue
            seen.add(key)
            items.append((r, subj))
    total, correct = 0, 0
    per = {}
    t0 = time.time()
    print(f"  [{model}] evaluating {len(items)} MMLU items (0-shot)...")
    for (r, subj) in items:
        choices = [str(c) for c in r["choices"]]
        prompt = fmt(r["question"], choices)
        resp = ask(model, prompt)
        guess = answer_letter(resp, choices)
        ans = int(r["answer"]) if str(r["answer"]).isdigit() else -1
        ok = (guess == ans)
        total += 1; correct += int(ok)
        d = per.setdefault(subj, [0, 0])
        d[0] += int(ok); d[1] += 1
    acc = correct / total * 100 if total else 0
    print(f"  ── {model} MMLU 0-shot, N={total}: {correct}/{total} = {acc:.1f}%")
    for subj, (c, n) in sorted(per.items()):
        print(f"     {subj:26s} {c:2d}/{n:2d}  {c/n*100:5.1f}%")
    return {"model": model, "n": total, "correct": correct, "accuracy": round(acc, 2), "per_subject": per,
            "note": "MMLU 0-shot bounded sample (not 5-shot; strictly lower bound)"}

if __name__ == "__main__":
    models = sys.argv[1:] or ["sov33-unified:latest"]
    out = [run(m) for m in models]
    json.dump(out, open("/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/mmlu_bounded.json", "w"), indent=2)
    print("\nSaved: benchmark-results/mmlu_bounded.json")
