#!/usr/bin/env python3
"""
sov33_benchmark_general.py — SOV33 General Capability Benchmark Suite

Benchmarks (all open datasets, HF Hub):
  - MMLU-Pro         (TIGER-Lab/MMLU-Pro,             mc 10-way, reasoning)
  - GSM8K            (openai/gsm8k,                   grade-school math)
  - AIME 2024        (Maxwell-Jia/AIME_2024,          olympiad math)
  - HellaSwag        (Rowan/hellaswag,                commonsense)
  - ARC-Challenge    (allenai/ai2_arc, ARC-Challenge, science reasoning)
  - HumanEval        (openai_humaneval,               code generation)
  - TruthfulQA-mc1   (truthfulqa/truthful_qa, mc1,    factuality)

Portable to:  local (transformers), Kaggle T4 (HF accelerate), HF Spaces.

Usage:
  python3 sov33_benchmark_general.py --model Qwen/Qwen2.5-3B-Instruct --suite quick
  python3 sov33_benchmark_general.py --model Qwen/Qwen2.5-3B-Instruct --suite full --n 200
  python3 sov33_benchmark_general.py --model Qwen/Qwen2.5-3B-Instruct --bench mmlu_pro,gsm8k --n 50
"""
from __future__ import annotations
import argparse, hashlib, json, os, random, re, sys, time
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Callable

# ── Result container ────────────────────────────────────────────────────────
@dataclass
class BenchResult:
    bench: str
    model: str
    n: int
    correct: int
    pct: float
    duration_s: float
    samples: list = field(default_factory=list)  # [{q, gold, pred, ok}]
    extra: dict = field(default_factory=dict)
    sigil: str = ""

    def finalize(self):
        self.sigil = hashlib.sha256(
            json.dumps({"b": self.bench, "m": self.model, "n": self.n,
                        "c": self.correct, "p": self.pct,
                        "s": [s.get("ok") for s in self.samples]},
                       sort_keys=True).encode()).hexdigest()

# ── HF datasets loaders (lazy) ──────────────────────────────────────────────
def _load(name, *a, **kw):
    from datasets import load_dataset
    return load_dataset(name, *a, **kw)

def get_mmlu_pro(n=200, seed=20260713):
    ds = _load("TIGER-Lab/MMLU-Pro", split="test", trust_remote_code=True)
    rows = list(ds); random.Random(seed).shuffle(rows); return rows[:n]

def get_gsm8k(n=200, seed=20260713):
    ds = _load("openai/gsm8k", "main", split="test", trust_remote_code=True)
    rows = list(ds); random.Random(seed).shuffle(rows); return rows[:n]

def get_aime(n=30):
    ds = _load("Maxwell-Jia/AIME_2024", split="train", trust_remote_code=True)
    return list(ds)

def get_hellaswag(n=200, seed=20260713):
    ds = _load("Rowan/hellaswag", split="validation", trust_remote_code=True)
    rows = list(ds); random.Random(seed).shuffle(rows); return rows[:n]

def get_arc_challenge(n=200, seed=20260713):
    ds = _load("allenai/ai2_arc", "ARC-Challenge", split="test", trust_remote_code=True)
    rows = list(ds); random.Random(seed).shuffle(rows); return rows[:n]

def get_humaneval(n=164):
    ds = _load("openai_humaneval", split="test", trust_remote_code=True)
    return list(ds)

def get_truthfulqa_mc1(n=200, seed=20260713):
    ds = _load("truthfulqa/truthful_qa", "multiple_choice", split="validation", trust_remote_code=True)
    rows = list(ds); random.Random(seed).shuffle(rows); return rows[:n]

# ── Graders ─────────────────────────────────────────────────────────────────
LETTERS = "ABCDEFGHIJ"
MC_RE = re.compile(r'(?:THE ANSWER IS|ANSWER\s*[:\s])\s*\(?([A-J])\)?', re.I)
LETTER_RE = re.compile(r'^\s*\(?([A-J])\)?\s*$')

def grade_mc1(response: str, gold_letter: str) -> bool:
    r = (response or "").upper().strip()
    m = MC_RE.search(r) or LETTER_RE.match(r)
    if m and m.group(1).upper() == gold_letter.upper():
        return True
    return gold_letter.upper() in r.split()[-3:] if r else False

def grade_math(response: str, gold) -> bool:
    r = response or ""
    if isinstance(gold, (int, float)):
        gold_str = str(gold)
        nums = re.findall(r'-?\d+\.?\d*', r)
        if nums:
            try:
                return abs(float(nums[-1]) - float(gold)) < 1e-2
            except Exception:
                pass
        return gold_str in r
    return str(gold) in r

def extract_code(text: str) -> str:
    m = re.search(r"```(?:python)?\s*\n(.*?)```", text, re.S)
    return m.group(1) if m else text

def grade_code(response: str, prompt: str, test: str, entry_point: str) -> bool:
    """HumanEval: exec generated body with canonical test."""
    code = extract_code(response or "")
    # Wrap into full module
    full = f"{prompt}\n{code}\n{test}\ncheck({entry_point})"
    try:
        exec(full, {})
        return True
    except Exception:
        return False

# ── Prompt builders ─────────────────────────────────────────────────────────
def prompt_mmlu_pro(q, options):
    choices = "\n".join(f"{LETTERS[i]}. {o}" for i, o in enumerate(options))
    return (f"The following are multiple choice questions about {q.get('category','')}.\n\n"
            f"Question: {q['question']}\n{choices}\n"
            f"Answer with a single letter A-{LETTERS[len(options)-1]}. The answer is ")

def prompt_gsm8k(q):
    return f"Question: {q['question']}\nAnswer with the final number after '####'. Let's solve step by step.\n"

def prompt_aime(q):
    return f"Question: {q['Problem']}\nAnswer with the integer 0-999. Let's solve step by step.\n"

def prompt_hellaswag(q):
    ctx = q["ctx"]
    endings = q["endings"]
    choices = "\n".join(f"{LETTERS[i]}. {e}" for i, e in enumerate(endings))
    return (f"Choose the most plausible continuation.\nContext: {ctx}\n{choices}\n"
            f"Answer with a single letter. The answer is ")

def prompt_arc(q):
    labels = q["choices"]["label"]
    texts = q["choices"]["text"]
    choices = "\n".join(f"{l}. {t}" for l, t in zip(labels, texts))
    return (f"Question: {q['question']}\n{choices}\n"
            f"Answer with a single letter. The answer is ")

def prompt_humaneval(q):
    return (f"Complete the following Python function. Return only the function body.\n\n"
            f"```python\n{q['prompt']}\n```\n")

def prompt_truthfulqa(q):
    choices = "\n".join(f"{i+1}. {c}" for i, c in enumerate(q["mc1_targets"]["choices"]))
    return (f"Question: {q['question']}\n{choices}\n"
            f"Answer with a single number. The answer is ")

# ── Benchmark runners ───────────────────────────────────────────────────────
def run_mmlu_pro(model_call, n=200):
    rows = get_mmlu_pro(n)
    correct = 0; samples = []; t0 = time.time()
    for i, row in enumerate(rows):
        gold = LETTERS[int(row["answer_index"])]
        resp = model_call(prompt_mmlu_pro(row, row["options"]), max_new_tokens=8)
        ok = grade_mc1(resp, gold)
        correct += int(ok)
        samples.append({"i": i, "gold": gold, "pred": resp[:80], "ok": ok})
        if (i+1) % 25 == 0: print(f"  MMLU-Pro {i+1}/{len(rows)}")
    return BenchResult("mmlu_pro", model_call.model_id, len(rows), correct,
                       100*correct/len(rows), time.time()-t0, samples).tap(lambda r: r.finalize())

def run_gsm8k(model_call, n=200):
    rows = get_gsm8k(n)
    correct = 0; samples = []; t0 = time.time()
    for i, row in enumerate(rows):
        gold = row["answer"].split("####")[-1].strip()
        resp = model_call(prompt_gsm8k(row), max_new_tokens=256)
        ok = grade_math(resp, gold)
        correct += int(ok)
        samples.append({"i": i, "gold": gold, "pred": resp[:120], "ok": ok})
        if (i+1) % 25 == 0: print(f"  GSM8K {i+1}/{len(rows)}")
    return BenchResult("gsm8k", model_call.model_id, len(rows), correct,
                       100*correct/len(rows), time.time()-t0, samples).tap(lambda r: r.finalize())

def run_aime(model_call, n=30):
    rows = get_aime(n)
    correct = 0; samples = []; t0 = time.time()
    for i, row in enumerate(rows):
        resp = model_call(prompt_aime(row), max_new_tokens=512)
        ok = grade_math(resp, str(row["Answer"]))
        correct += int(ok)
        samples.append({"i": i, "gold": str(row["Answer"]), "pred": resp[:120], "ok": ok})
    return BenchResult("aime_2024", model_call.model_id, len(rows), correct,
                       100*correct/len(rows), time.time()-t0, samples).tap(lambda r: r.finalize())

def run_hellaswag(model_call, n=200):
    rows = get_hellaswag(n)
    correct = 0; samples = []; t0 = time.time()
    for i, row in enumerate(rows):
        gold = str(row["label"])
        resp = model_call(prompt_hellaswag(row), max_new_tokens=4)
        ok = grade_mc1(resp, gold)
        correct += int(ok)
        samples.append({"i": i, "gold": gold, "pred": resp[:40], "ok": ok})
        if (i+1) % 50 == 0: print(f"  HellaSwag {i+1}/{len(rows)}")
    return BenchResult("hellaswag", model_call.model_id, len(rows), correct,
                       100*correct/len(rows), time.time()-t0, samples).tap(lambda r: r.finalize())

def run_arc(model_call, n=200):
    rows = get_arc_challenge(n)
    correct = 0; samples = []; t0 = time.time()
    for i, row in enumerate(rows):
        gold = row["answerKey"]
        resp = model_call(prompt_arc(row), max_new_tokens=4)
        ok = grade_mc1(resp, gold)
        correct += int(ok)
        samples.append({"i": i, "gold": gold, "pred": resp[:40], "ok": ok})
        if (i+1) % 50 == 0: print(f"  ARC-C {i+1}/{len(rows)}")
    return BenchResult("arc_challenge", model_call.model_id, len(rows), correct,
                       100*correct/len(rows), time.time()-t0, samples).tap(lambda r: r.finalize())

def run_humaneval(model_call, n=164):
    rows = get_humaneval(n)
    correct = 0; samples = []; t0 = time.time()
    for i, row in enumerate(rows):
        resp = model_call(prompt_humaneval(row), max_new_tokens=512)
        ok = grade_code(resp, row["prompt"], row["test"], row["entry_point"])
        correct += int(ok)
        samples.append({"i": i, "gold": row["entry_point"], "pred": resp[:120], "ok": ok})
        if (i+1) % 25 == 0: print(f"  HumanEval {i+1}/{len(rows)}")
    return BenchResult("humaneval", model_call.model_id, len(rows), correct,
                       100*correct/len(rows), time.time()-t0, samples).tap(lambda r: r.finalize())

def run_truthfulqa(model_call, n=200):
    rows = get_truthfulqa_mc1(n)
    correct = 0; samples = []; t0 = time.time()
    for i, row in enumerate(rows):
        gold_idx = row["mc1_targets"]["labels"].index(1) + 1
        resp = model_call(prompt_truthfulqa(row), max_new_tokens=4)
        ok = grade_mc1(resp.replace("1","A").replace("2","B").replace("3","C")
                       .replace("4","D").replace("5","E").replace("6","F"),
                       LETTERS[gold_idx-1])
        correct += int(ok)
        samples.append({"i": i, "gold": gold_idx, "pred": resp[:40], "ok": ok})
        if (i+1) % 50 == 0: print(f"  TruthfulQA {i+1}/{len(rows)}")
    return BenchResult("truthfulqa_mc1", model_call.model_id, len(rows), correct,
                       100*correct/len(rows), time.time()-t0, samples).tap(lambda r: r.finalize())

# ── Bench registry ──────────────────────────────────────────────────────────
BENCHES: dict[str, Callable] = {
    "mmlu_pro":     run_mmlu_pro,
    "gsm8k":        run_gsm8k,
    "aime_2024":    run_aime,
    "hellaswag":    run_hellaswag,
    "arc_challenge": run_arc,
    "humaneval":    run_humaneval,
    "truthfulqa_mc1": run_truthfulqa,
}

SUITES: dict[str, list[str]] = {
    "quick":  ["mmlu_pro:50", "gsm8k:50", "hellaswag:50", "arc_challenge:50"],
    "code":   ["humaneval:164"],
    "math":   ["gsm8k:200", "aime_2024:30"],
    "knowledge": ["mmlu_pro:200", "hellaswag:200", "arc_challenge:200", "truthfulqa_mc1:200"],
    "full":   ["mmlu_pro:200", "gsm8k:200", "aime_2024:30", "hellaswag:200",
               "arc_challenge:200", "humaneval:164", "truthfulqa_mc1:200"],
}

# ── Monkey-patch tap (chainable finalize) ───────────────────────────────────
def _tap(self, fn):
    fn(self); return self
BenchResult.tap = _tap

# ── CLI ─────────────────────────────────────────────────────────────────────
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="Qwen/Qwen2.5-3B-Instruct")
    ap.add_argument("--suite", default="quick", choices=list(SUITES)+["custom"])
    ap.add_argument("--bench", default="", help="csv of bench:n pairs")
    ap.add_argument("--n", type=int, default=200)
    ap.add_argument("--out", default="benchmark-results")
    ap.add_argument("--max-new-tokens", type=int, default=None,
                    help="override per-bench default")
    ap.add_argument("--device", default="auto")
    args = ap.parse_args()

    # Lazy model loader (HF transformers)
    from harness_loader import ModelCall
    mc = ModelCall(args.model, device=args.device,
                   default_max_new_tokens=args.max_new_tokens)

    if args.suite == "custom":
        items = [b.strip() for b in args.bench.split(",") if b.strip()]
    else:
        items = SUITES[args.suite]
    plan = []
    for item in items:
        if ":" in item:
            b, n = item.split(":"); plan.append((b, int(n)))
        else:
            plan.append((item, args.n))

    Path(args.out).mkdir(exist_ok=True)
    suite_id = f"{args.suite}_{int(time.time())}"
    suite_results = {"suite": args.suite, "model": args.model, "started": datetime.now().isoformat(),
                     "results": []}
    for b, n in plan:
        if b not in BENCHES:
            print(f"⚠ unknown bench: {b}"); continue
        print(f"\n{'='*60}\n  {b} n={n}\n{'='*60}")
        try:
            r = BENCHES[b](mc, n=n)
            print(f"  → {r.pct:.1f}% ({r.correct}/{r.n})  sigil={r.sigil[:16]}")
            suite_results["results"].append(asdict(r))
        except Exception as e:
            print(f"  ✗ {b} failed: {e}")
            suite_results["results"].append({"bench": b, "error": str(e)})

    # Composite
    pcts = [r["pct"] for r in suite_results["results"] if "pct" in r]
    suite_results["composite_pct"] = round(sum(pcts)/len(pcts), 2) if pcts else 0.0
    suite_results["ended"] = datetime.now().isoformat()
    suite_results["sigil"] = hashlib.sha256(
        json.dumps(suite_results["results"], sort_keys=True).encode()).hexdigest()
    out_path = Path(args.out) / f"general_{args.model.split('/')[-1]}_{suite_id}.json"
    out_path.write_text(json.dumps(suite_results, indent=2))
    print(f"\n{'='*60}\nCOMPOSITE: {suite_results['composite_pct']:.2f}%\n"
          f"SIGIL: {suite_results['sigil']}\nWritten: {out_path}")

if __name__ == "__main__":
    main()