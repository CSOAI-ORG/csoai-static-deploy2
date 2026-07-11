#!/usr/bin/env python3
"""
SOV33 FULL EVALS — real HF datasets, correctness-graded, on the Groq-wired brain.
Checkpointed (survives rate-limits/restarts) + backoff. Router = Groq→OCI→Ollama.

  - GSM8K  : FULL test set (1319) — the canonical reasoning benchmark
  - MMLU   : stratified sample (N_MMLU per run; full 14042 is impractical at API latency)
  - IFEval : NOT here — full IFEval needs Google's official instruction_following_eval checker;
             the curated programmatic subset lives in sov33_evals.py (honest note).

Honest: GSM8K here IS the full standard test set → a directly-comparable published number.
MMLU is a large stratified sample, labelled as such.
"""
import re, sys, os, json, time
sys.path.insert(0, os.path.expanduser("~/clawd/_compute"))
from sov33_compute import infer
from datasets import load_dataset

CKPT = os.path.expanduser("~/clawd/_compute/sov33_evals_full_ckpt.json")
N_MMLU = int(os.environ.get("N_MMLU", "500"))

def _load_ckpt():
    if os.path.exists(CKPT):
        return json.load(open(CKPT))
    return {"gsm8k": {"done": {}, }, "mmlu": {"done": {}}}

def _save(ck):
    json.dump(ck, open(CKPT, "w"))

def _ask(prompt, max_tokens=400, tries=4):
    for i in range(tries):
        try:
            return infer(prompt, max_tokens=max_tokens)
        except Exception:
            time.sleep(2 ** i)  # backoff on rate-limit
    return ""

def _final_int(text):
    t = text.replace(",", "")
    m = re.search(r"####\s*(-?\d+)", t)
    if m: return int(m.group(1))
    tail = re.split(r"(?i)answer\s*(?:is|:)?", t)[-1]
    nums = re.findall(r"-?\d+", tail)
    if nums: return int(nums[-1])
    nums = re.findall(r"-?\d+", t)
    return int(nums[-1]) if nums else None

def _mc_letter(text):
    m = re.search(r"\b([ABCD])\b", text.strip()[:80].upper())
    return m.group(1) if m else None

def run_gsm8k(ck):
    ds = load_dataset("gsm8k", "main", split="test")
    done = ck["gsm8k"]["done"]
    for i, ex in enumerate(ds):
        if str(i) in done: continue
        gold = int(ex["answer"].split("####")[-1].replace(",", "").strip())
        a = _ask(f"Solve step by step, then end with '#### <final integer>'.\n{ex['question']}")
        done[str(i)] = int(_final_int(a) == gold)
        if i % 25 == 0:
            _save(ck); print(f"  gsm8k {i+1}/{len(ds)}  acc_so_far={sum(done.values())/len(done):.3f}", flush=True)
    _save(ck)
    return sum(done.values()), len(done)

def run_mmlu(ck):
    ds = load_dataset("cais/mmlu", "all", split="test")
    # stratified: even stride to cover subjects, capped at N_MMLU
    idxs = list(range(0, len(ds), max(1, len(ds)//N_MMLU)))[:N_MMLU]
    done = ck["mmlu"]["done"]
    letters = "ABCD"
    for n, i in enumerate(idxs):
        if str(i) in done: continue
        ex = ds[i]
        gold = letters[ex["answer"]]
        opts = "\n".join(f"{letters[j]}) {c}" for j, c in enumerate(ex["choices"]))
        a = _ask(f"Answer with ONLY the letter.\n{ex['question']}\n{opts}", max_tokens=8)
        done[str(i)] = int(_mc_letter(a) == gold)
        if n % 25 == 0:
            _save(ck); print(f"  mmlu {n+1}/{len(idxs)}  acc_so_far={sum(done.values())/len(done):.3f}", flush=True)
    _save(ck)
    return sum(done.values()), len(done)

if __name__ == "__main__":
    ck = _load_ckpt()
    print("=== GSM8K (full test) ===", flush=True)
    g_c, g_n = run_gsm8k(ck)
    print(f"GSM8K: {g_c}/{g_n} = {g_c/g_n:.4f}", flush=True)
    print(f"=== MMLU (stratified {N_MMLU}) ===", flush=True)
    m_c, m_n = run_mmlu(ck)
    print(f"MMLU: {m_c}/{m_n} = {m_c/m_n:.4f}", flush=True)
    res = {"gsm8k": {"n": g_n, "correct": g_c, "acc": round(g_c/g_n, 4), "set": "FULL test 1319"},
           "mmlu": {"n": m_n, "correct": m_c, "acc": round(m_c/m_n, 4), "set": f"stratified {N_MMLU}"},
           "backend": "groq llama-3.3-70b (via sov33_compute, OCI fallback)"}
    json.dump(res, open(os.path.expanduser("~/clawd/_compute/sov33_evals_full_results.json"), "w"), indent=2)
    print(json.dumps(res, indent=2))
