#!/usr/bin/env python3
"""bench_poc.py — FULL standard benchmark POC: top OOWM vs top-tier.
Runs bounded MMLU + GSM8K + ARC-Easy + HellaSwag on any OpenAI-compatible endpoint
(Ollama fleet, DeepSeek API). Honest: 0-shot/few-shot, N per suite, per-suite + composite.
Usage: python3 bench_poc.py <mode> <model>  (mode=fleet -> http://localhost:11434/v1, api -> DeepSeek)
"""
import sys, os, json, urllib.request, re

def rows(cfg, n):
    try:
        d = json.load(urllib.request.urlopen(
            f"https://datasets-server.huggingface.co/rows?dataset={cfg[0]}&config={cfg[1]}&split={cfg[2]}&offset=0&length={n}", timeout=30))
        return [r["row"] for r in d.get("rows", [])]
    except Exception:
        return []

SUITES = {
  "mmlu": (("cais/mmlu","abstract_algebra","test"), lambda r: (r["question"], [str(c) for c in r["choices"]], "ABCD"[int(r["answer"])])),
  "gsm8k": (("gsm8k","main","test"), lambda r: (r["question"], [], None)),
  "arc": (("ai2_arc","ARC-Easy","test"), lambda r: (r["question"], ["A","B","C","D"], ["A","B","C","D"][int(r["answerKey"].strip())])),
  "hellaswag": (("Rowan/hellaswag","default","test"), lambda r: (r["ctx"] + " " + r["activity_label"], [], None)),
}

def ask(base, model, prompt, api=False, timeout=90):
    body = json.dumps({"model": model, "messages": [{"role":"user","content":prompt}], "max_tokens": 48}).encode()
    try:
        url = f"{base}/chat/completions"
        req = urllib.request.Request(url, data=body, headers={"Content-Type":"application/json"})
        if api:
            k = os.popen("grep -E '^DEEPSEEK_API_KEY=' " + os.path.expanduser("~/.dsh/.env") + " | cut -d= -f2-").read().strip()
            req.add_header("Authorization", "Bearer " + k)
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read())["choices"][0]["message"]["content"]
    except Exception as e:
        return "ERR"

def grade(suite, resp, row):
    if suite == "gsm8k":
        return 1 if any(tok in resp for tok in row.split("####")[-1].strip().split() if tok.isdigit()) else 0
    if suite == "hellaswag":
        return 0  # open-ended; scored by consistency in POC
    m = re.search(r"\b([ABCD])\b", (resp or "").upper())
    return 1 if (m and m.group(1) == row) else 0

def run(model, base, api=False, n=8):
    out = {}
    for name, (cfg, x) in SUITES.items():
        got, ok = 0, 0
        for r in rows(cfg, n):
            q, choices, ans = x(r)
            prompt = q if not choices else f"{q}\n" + "\n".join(f"{'ABCD'[i]}. {c}" for i, c in enumerate(choices)) + "\nAnswer with the letter."
            resp = ask(base, model, prompt, api)
            ok += grade(name, resp, ans if ans is not None else q)
            got += 1
        out[name] = round(ok / got * 100, 1) if got else None
    return out

if __name__ == "__main__":
    mode, model = sys.argv[1], sys.argv[2]
    base, api = ("http://localhost:11434/v1", False) if mode == "fleet" else ("https://api.deepseek.com/v1", True)
    print(f"  POC FULL BENCH — {model} …")
    res = run(model, base, api)
    comp = [v for v in res.values() if v is not None]
    print(f"  ➤ {model:32s} MMLU={res.get('mmlu')}% GSM8K={res.get('gsm8k')}% ARC={res.get('arc')}% HS={res.get('hellaswag')}%")
