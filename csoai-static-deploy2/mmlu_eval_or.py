#!/usr/bin/env python3
"""Bounded MMLU on a FRONTIER model via OpenRouter (the 'large core' the router should route to).
Same 65-item 0-shot set as mmlu_eval.py for a fair top-tier comparison.
Usage: python3 mmlu_eval_or.py qwen/qwen3.7-max
"""
import os, json, sys, time, urllib.request

API = "https://datasets-server.huggingface.co/rows?dataset=cais/mmlu&config={cfg}&split=test&offset=0&length={n}"
SUBJECTS = ["abstract_algebra", "anatomy", "astronomy", "clinical_knowledge", "college_chemistry",
            "college_computer_science", "college_physics", "econometrics", "high_school_biology",
            "high_school_chemistry", "international_law", "professional_medicine", "us_foreign_policy"]
N_PER = 5
KEY = os.popen("grep -E '^DEEPSEEK_API_KEY=' " + os.path.expanduser("~/.dsh/.env") + " | cut -d= -f2-").read().strip()

def fetch(cfg, n):
    try:
        d = json.load(urllib.request.urlopen(API.format(cfg=cfg, n=n), timeout=30))
        return d.get("rows", [])
    except Exception:
        return []

def ask(model, prompt, timeout=60):
    body = json.dumps({"model": model, "messages": [{"role": "user", "content": prompt}], "max_tokens": 16}).encode()
    try:
        req = urllib.request.Request("https://api.deepseek.com/v1/chat/completions", data=body,
            headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read())["choices"][0]["message"]["content"].strip()
    except Exception:
        return ""

def answer_letter(resp):
    import re
    r = (resp or "").upper()
    m = re.search(r"\b([ABCD])\b", r)
    if m: return "ABCD".index(m.group(1))
    m = re.search(r"(?:ANSWER|IS|:)\s*\(?([ABCD])\)?", r)
    if m: return "ABCD".index(m.group(1))
    return None

def run(model):
    items, seen = [], set()
    for subj in SUBJECTS:
        for row in fetch(subj, N_PER):
            r = row["row"]
            if r["question"] in seen: continue
            seen.add(r["question"]); items.append((r, subj))
    tot, ok = 0, 0
    for (r, subj) in items:
        choices = [str(c) for c in r["choices"]]
        prompt = f"Question: {r['question']}\n" + "\n".join(f"{'ABCD'[i]}. {c}" for i, c in enumerate(choices)) + "\nAnswer with the letter (A, B, C, or D) of the correct answer."
        g = answer_letter(ask(model, prompt))
        ans = int(r["answer"]) if str(r["answer"]).isdigit() else -1
        tot += 1; ok += int(g == ans)
    print(f"  [{model}] MMLU 0-shot N={tot}: {ok}/{tot} = {ok/tot*100:.1f}%")
    return {"model": model, "n": tot, "correct": ok, "accuracy": round(ok/tot*100, 2)}

if __name__ == "__main__":
    models = sys.argv[1:] or ["deepseek-chat"]
    out = [run(m) for m in models]
    json.dump(out, open("/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/mmlu_frontier.json", "w"), indent=2)
    print("Saved: benchmark-results/mmlu_frontier.json")
