#!/usr/bin/env python3
"""Frontier Move 2 — measure COMPOSITE vs BEST-SINGLE across 2 decorrelated legs.

The 07-24 verdict: fine-tuning won't climb boards; only a stronger base OR a decorrelated
composite will. Cross-family fusion is measured to decorrelate (rho = -0.725, SEATS); same-family
does not (rho = +0.764). Best-of-N across decorrelated legs is already 0.975 GSM8K served — but we
have NOT yet measured composite-vs-best-single on the HARD boards because that needs >=2 legs served
live. This harness does exactly that, once two decorrelated endpoints are up.

UNTESTED until two live endpoints exist. Legs must be CROSS-FAMILY to seat (e.g. a transformer
instruct model + an SSM/Mamba or a genuinely different architecture) — NOT two same-family models.

Run:
  python composite_vs_best_single.py \
     --leg "qwen,http://localhost:8000/v1,Qwen2.5-7B-Instruct" \
     --leg "mamba,http://localhost:8001/v1,<decorrelated SSM leg>" \
     --board gsm8k --n 100
Endpoints are OpenAI-compatible (vLLM/Ollama/llama.cpp). Prints per-leg acc, composite acc,
the lift over best-single, and the measured answer-correlation rho between the legs.
"""
import argparse, json, re, urllib.request
from collections import Counter

def call(url, model, prompt, temperature=0.7, max_tokens=1024):
    body = {"model": model, "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature, "max_tokens": max_tokens}
    req = urllib.request.Request(url.rstrip("/") + "/chat/completions",
          data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req, timeout=180))["choices"][0]["message"]["content"]

def extract_final(text):
    # GSM8K-style: last integer, or '#### N'
    m = re.findall(r"####\s*(-?\d[\d,]*)", text)
    if m: return m[-1].replace(",", "")
    nums = re.findall(r"-?\d[\d,]*", text)
    return nums[-1].replace(",", "") if nums else None

def load_board(board, n):
    # minimal loader: expects datasets available; falls back to a tiny embedded sample.
    try:
        from datasets import load_dataset
        if board == "gsm8k":
            ds = load_dataset("gsm8k", "main", split=f"test[:{n}]")
            return [(r["question"], extract_final(r["answer"])) for r in ds]
        if board == "arc":
            ds = load_dataset("allenai/ai2_arc", "ARC-Challenge", split=f"test[:{n}]")
            return [(r["question"] + "\nChoices: " + str(r["choices"]), r["answerKey"]) for r in ds]
    except Exception as e:
        print(f"[warn] dataset load failed ({e}); using 2 embedded samples")
    return [("Natalia sold 48 clips in April and half as many in May. Total?", "72"),
            ("A robe takes 2 bolts blue and half that white. Total bolts?", "3")]

def best_of_n_answer(url, model, prompt, k=5):
    """One leg's self-consistency vote (majority over k samples)."""
    votes = [extract_final(call(url, model, prompt)) for _ in range(k)]
    votes = [v for v in votes if v is not None]
    return Counter(votes).most_common(1)[0][0] if votes else None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--leg", action="append", required=True,
                    help='repeat: "name,url,model" — MUST be cross-family to seat')
    ap.add_argument("--board", default="gsm8k")
    ap.add_argument("--n", type=int, default=100)
    ap.add_argument("--k", type=int, default=5, help="best-of-N samples per leg")
    args = ap.parse_args()
    legs = [dict(zip(("name","url","model"), s.split(",", 2))) for s in args.leg]
    assert len(legs) >= 2, "need >=2 decorrelated legs — that's the whole point"

    board = load_board(args.board, args.n)
    prompt_t = "Solve step by step. End with '#### <answer>'.\n\n{q}"

    per_leg_correct = {l["name"]: 0 for l in legs}
    composite_correct = 0
    agree_vec = {l["name"]: [] for l in legs}  # 1/0 correctness per item, for rho

    for q, gold in board:
        p = prompt_t.format(q=q)
        leg_ans = {}
        for l in legs:
            a = best_of_n_answer(l["url"], l["model"], p, k=args.k)
            leg_ans[l["name"]] = a
            ok = int(a == gold)
            per_leg_correct[l["name"]] += ok
            agree_vec[l["name"]].append(ok)
        # composite = jury vote across legs' best-of-N answers (ties -> first leg)
        tally = Counter(v for v in leg_ans.values() if v is not None)
        comp = tally.most_common(1)[0][0] if tally else None
        composite_correct += int(comp == gold)

    N = len(board)
    print("\n=== RESULT (n=%d, %s) ===" % (N, args.board))
    best_single = 0.0
    for l in legs:
        acc = per_leg_correct[l["name"]] / N
        best_single = max(best_single, acc)
        print(f"  leg {l['name']:>10}: {acc:.3f}")
    comp_acc = composite_correct / N
    print(f"  {'COMPOSITE':>10}: {comp_acc:.3f}")
    print(f"  lift over best-single: {comp_acc - best_single:+.3f}  (best-single={best_single:.3f})")

    # answer-correlation rho between first two legs (decorrelation check: want NEGATIVE / low)
    try:
        import numpy as np
        a = np.array(agree_vec[legs[0]["name"]]); b = np.array(agree_vec[legs[1]["name"]])
        if a.std() and b.std():
            print(f"  measured correctness-rho({legs[0]['name']},{legs[1]['name']}) = {np.corrcoef(a,b)[0,1]:+.3f}"
                  "  (negative/low = decorrelated = seats)")
    except Exception:
        pass

if __name__ == "__main__":
    main()
