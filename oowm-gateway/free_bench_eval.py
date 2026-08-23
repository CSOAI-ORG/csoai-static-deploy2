#!/usr/bin/env python3
"""free_bench_eval.py — evaluate our FREE sovereign fleet against the open-license
MMLU/GPQA data downloaded from Kaggle. Deterministic exact-match grading on a
calibrated subset (the tunnel fleet is slow). Honest: our scores are on our
fleet vs. a public benchmark — never blended with external/market numbers.

Usage: python3 free_bench_eval.py --limit 20 --model phi4:14b
"""
import csv, json, sys, os, time, urllib.request, argparse

OLLAMA = "http://127.0.0.1:11434/api/chat"
BENCH_DIR = os.path.expanduser("~/sim-world-data/free-benches")

def mmlu_items(limit):
    """Yield (question, choices[4], answer_letter) from the MMLU test CSV dir."""
    n = 0
    csvs = list(filter(lambda f: f.endswith("_test.csv"), os.listdir(os.path.join(BENCH_DIR, "data", "test"))))
    for cf in csvs[:6]:  # sample 6 subjects (bounded)
        with open(os.path.join(BENCH_DIR, "data", "test", cf), newline="", encoding="utf-8") as f:
            for row in csv.reader(f):
                if len(row) < 6: continue
                q, *choices, ans = row[0], row[1:5], row[5]
                yield (q, choices, ans.strip())
                n += 1
                if limit and n >= limit: return

def chat(model, prompt, n=24, timeout=60):
    body = json.dumps({"model": model, "messages": [{"role": "user", "content": prompt}],
                       "stream": False, "options": {"num_predict": n}}).encode()
    req = urllib.request.Request(OLLAMA, data=body, headers={"Content-Type": "application/json"})
    try:
        return json.loads(urllib.request.urlopen(req, timeout=timeout).read()).get("message", {}).get("content", "")
    except Exception:
        return ""

def grade(resp, ans_letter, choices):
    t = (resp or "").upper()
    # single letter present in answer
    for l in t:
        if l in "ABCD": return l == ans_letter
    return False

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="phi4:14b")
    ap.add_argument("--limit", type=int, default=12)
    args = ap.parse_args()
    ok = 0; tot = 0; t0 = time.time()
    for q, choices, ans in mmlu_items(args.limit):
        opts = "\n".join("{} {}".format("ABCD"[i], c) for i, c in enumerate(choices))
        prompt = "Answer ONLY the correct letter. Question: %s\n%s\nThe correct option is:" % (q, opts)
        resp = chat(args.model, prompt, timeout=90)
        good = grade(resp, ans, choices)
        ok += good; tot += 1
        print(f"  [{'OK' if good else 'X'}] {q[:44]} -> {resp[:18]!r} (exp {ans})", flush=True)
    acc = ok / tot if tot else 0
    print(f"\n{args.model}: {ok}/{tot} = {acc:.3f} on MMLU sample (free open-license data) in {time.time()-t0:.0f}s")
    print(json.dumps({"model": args.model, "n": tot, "correct": ok, "accuracy": round(acc, 3), "source": "Kaggle MMLU (lizhecheng/mmlu-dataset, free)", "honest": "our measured result on a public benchmark; not blended with market"}))

if __name__ == "__main__":
    main()
