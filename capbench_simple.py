#!/usr/bin/env python3
"""capbench_simple.py — how well does our model do, on standard benchmarks, WITHOUT lm-eval.

    python3 capbench_simple.py --model qwen3:30b-a3b --endpoint http://localhost:11435

lm-eval is a Python/torch version triangle that will not resolve on this pod. This does the same job
the estate's own way: fetch standard-benchmark rows from HF's datasets-server (JSON, no `datasets`
lib), query OUR endpoint, grade DETERMINISTICALLY. Same discipline as sovos.py — three outcomes
(correct / wrong / UNMEASURED for an unparsed answer), no interval below usable_n>=30, honest n.

Benchmarks (a representative capability set):
  gsm8k        grade-school math — extract the final number, exact match
  arc_challenge science MC — extract the letter A-D
  mmlu         knowledge MC — extract the letter A-D
"""
import argparse, json, os, re, sys, math, urllib.request, urllib.parse

DS = "https://datasets-server.huggingface.co/rows"
USABLE_N = 30

BENCH = {
    "gsm8k":         {"dataset": "openai/gsm8k",       "config": "main",           "split": "test"},
    "arc_challenge": {"dataset": "allenai/ai2_arc",    "config": "ARC-Challenge",  "split": "test"},
    "mmlu":          {"dataset": "cais/mmlu",          "config": "all",            "split": "test"},
}


def rows(dataset, config, split, n):
    url = f"{DS}?{urllib.parse.urlencode({'dataset':dataset,'config':config,'split':split,'offset':0,'length':n})}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    return [r["row"] for r in json.loads(urllib.request.urlopen(req, timeout=60).read())["rows"]]


def ask(base, model, prompt):
    payload = {"model": model, "messages": [{"role": "user", "content": prompt}],
               "stream": False, "options": {"temperature": 0, "num_predict": 512}}
    req = urllib.request.Request(f"{base}/api/chat", data=json.dumps(payload).encode(),
                                 headers={"Content-Type": "application/json"})
    try:
        r = json.loads(urllib.request.urlopen(req, timeout=180).read())
        return (r.get("message") or {}).get("content")
    except Exception:
        return None


def wilson(c, n):
    if not n: return None
    z = 1.959963985; p = c/n; d = 1 + z*z/n
    m = (p + z*z/(2*n))/d; h = z*math.sqrt(p*(1-p)/n + z*z/(4*n*n))/d
    return [round(max(0., m-h), 4), round(min(1., m+h), 4)]


def grade_gsm8k(resp, row):
    gold = row["answer"].split("####")[-1].strip().replace(",", "")
    nums = re.findall(r"-?\d[\d,]*\.?\d*", (resp or "").replace(",", ""))
    return nums[-1].rstrip(".") == gold if nums else None


LETTERS = ["A", "B", "C", "D", "E"]
def grade_mc(resp, gold_letter):
    m = re.search(r"\b([A-E])\b", (resp or "").upper())
    return (m.group(1) == gold_letter) if m else None


def run_bench(name, base, model, limit):
    spec = BENCH[name]
    try:
        data = rows(spec["dataset"], spec["config"], spec["split"], limit)
    except Exception as e:
        return {"error": str(e)[:60]}
    correct = graded = 0
    for row in data:
        if name == "gsm8k":
            prompt = f"Solve. End with the final number.\n\n{row['question']}"
            v = grade_gsm8k(ask(base, model, prompt), row)
        elif name == "arc_challenge":
            ch = row["choices"]; opts = "\n".join(f"{l}. {t}" for l, t in zip(ch["label"], ch["text"]))
            prompt = f"Answer with the letter only.\n\n{row['question']}\n{opts}"
            v = grade_mc(ask(base, model, prompt), row["answerKey"])
        else:  # mmlu
            opts = "\n".join(f"{LETTERS[i]}. {c}" for i, c in enumerate(row["choices"]))
            prompt = f"Answer with the letter only.\n\n{row['question']}\n{opts}"
            v = grade_mc(ask(base, model, prompt), LETTERS[row["answer"]])
        if v is None: continue                    # unparsed = UNMEASURED, never wrong
        graded += 1; correct += 1 if v else 0
    return {"n_total": len(data), "usable_n": graded, "correct": correct,
            "accuracy": round(correct/graded, 4) if graded else None,
            "interval": wilson(correct, graded) if graded >= USABLE_N else None,
            "interval_withheld": None if graded >= USABLE_N else f"usable_n {graded} < {USABLE_N}"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--endpoint", default="http://localhost:11435")
    ap.add_argument("--limit", type=int, default=100)
    ap.add_argument("--benches", default="gsm8k,arc_challenge,mmlu")
    a = ap.parse_args()
    out = {"capbench": "simple", "model": a.model, "endpoint": a.endpoint, "results": {}}
    print(f"capbench_simple · {a.model} · limit {a.limit}")
    for b in [x.strip() for x in a.benches.split(",") if x.strip()]:
        r = run_bench(b, a.endpoint, a.model, a.limit)
        out["results"][b] = r
        iv = r.get("interval") or r.get("interval_withheld") or r.get("error")
        print(f"  {b:<14} acc={r.get('accuracy')} usable_n={r.get('usable_n')} {iv}")
    d = os.path.expanduser("~/clawd/_alignment/CAPBENCH")
    os.makedirs(d, exist_ok=True)
    p = f"{d}/{a.model.replace('/','_').replace(':','_')}.json"
    json.dump(out, open(p, "w"), indent=2)
    print(f"  → {p}")


if __name__ == "__main__":
    main()
