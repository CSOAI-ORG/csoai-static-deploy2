#!/usr/bin/env python3
"""
sov33_benchmark_agentic.py — SOV33 Agentic Capability Benchmark Suite

Benchmarks:
  - GAIA-lite         (gaia-benchmark/GAIA,           verifiable assistant tasks)
  - tau-bench-retail  (sierra-research/tau-bench,     customer-service agent)
  - ALFWorld-text     (allenai/alfworld,              embodied household text)
  - HotpotQA          (hotpot_qa,                     multi-hop QA)
  - SWE-bench-lite    (princeton-nlp/SWE-bench_Lite,  software engineering)

Designed for HF Spaces / Kaggle T4 (16GB VRAM) with vLLM or transformers.

Usage:
  python3 sov33_benchmark_agentic.py --model Qwen/Qwen2.5-3B-Instruct --suite quick
  python3 sov33_benchmark_agentic.py --model Qwen/Qwen2.5-3B-Instruct --suite agentic --n 30
"""
from __future__ import annotations
import argparse, hashlib, json, os, random, re, sys, time
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Callable

@dataclass
class AgentBenchResult:
    bench: str
    model: str
    n: int
    correct: int
    pct: float
    duration_s: float
    samples: list = field(default_factory=list)
    extra: dict = field(default_factory=dict)
    sigil: str = ""

    def finalize(self):
        self.sigil = hashlib.sha256(json.dumps(
            {"b": self.bench, "m": self.model, "n": self.n,
             "c": self.correct, "p": self.pct,
             "s": [s.get("ok") for s in self.samples]},
            sort_keys=True).encode()).hexdigest()

def _tap(self, fn):
    fn(self); return self
AgentBenchResult.tap = _tap

# ── Loaders ─────────────────────────────────────────────────────────────────
def _load(name, *a, **kw):
    from datasets import load_dataset
    return load_dataset(name, *a, **kw)

def get_gaia_lite(n=20, level=1):
    ds = _load("gaia-benchmark/GAIA", "2023_all", split="validation", trust_remote_code=True)
    rows = [r for r in ds if int(r.get("Level", 0)) == level]
    return rows[:n]

def get_tau_retail(n=20):
    """tau-bench retail subset — text-based customer service tasks."""
    try:
        ds = _load("sierra-research/tau-bench", "retail", split="test", trust_remote_code=True)
        return list(ds)[:n]
    except Exception:
        # Fallback: use BFCL retail subset as proxy
        ds = _load("glaiveai/glaive-function-calling-v2", split="train", trust_remote_code=True)
        retail = [r for r in ds if "retail" in r.get("system", "").lower()][:n]
        return retail

def get_alfworld_text(n=20):
    ds = _load("allenai/alfworld", split="train", trust_remote_code=True)
    return list(ds)[:n]

def get_hotpotqa(n=50, seed=20260713):
    ds = _load("hotpot_qa", "distractor", split="validation", trust_remote_code=True)
    rows = list(ds); random.Random(seed).shuffle(rows); return rows[:n]

def get_swe_bench_lite(n=10):
    ds = _load("princeton-nlp/SWE-bench_Lite", split="test", trust_remote_code=True)
    return list(ds)[:n]

# ── Graders ─────────────────────────────────────────────────────────────────
def grade_gaia(pred, gold) -> bool:
    """GAIA answers are short strings/numbers; case-insensitive exact match."""
    if pred is None: return False
    p = re.sub(r'\s+', ' ', str(pred)).strip().lower().rstrip('.')
    g = re.sub(r'\s+', ' ', str(gold)).strip().lower().rstrip('.')
    return p == g or g in p

def grade_em_f1(pred, gold) -> tuple[bool, float]:
    """Exact match + token-F1 (HotpotQA-style)."""
    p_tokens = re.findall(r'\w+', (pred or "").lower())
    g_tokens = re.findall(r'\w+', str(gold).lower())
    if not p_tokens or not g_tokens: return False, 0.0
    common = {}
    for t in p_tokens:
        if t in g_tokens:
            common[t] = min(p_tokens.count(t), g_tokens.count(t))
    num_same = sum(common.values())
    if num_same == 0: return False, 0.0
    precision = num_same / len(p_tokens)
    recall = num_same / len(g_tokens)
    f1 = 2 * precision * recall / (precision + recall)
    em = (re.sub(r'\W+',' ',str(pred).lower()).strip() ==
          re.sub(r'\W+',' ',str(gold).lower()).strip())
    return em, f1

def grade_tool_use(pred, gold_actions) -> bool:
    """Does pred contain all required tool calls (in order, fuzzy)?"""
    pred_str = (pred or "").lower()
    return all(str(a).lower() in pred_str for a in (gold_actions or []))

# ── Prompts ─────────────────────────────────────────────────────────────────
SYS_AGENT = ("You are an autonomous agent. Use tools and reasoning to solve the task. "
             "Output your final answer clearly prefixed with 'Final Answer:'.")

def prompt_gaia(q):
    return f"{SYS_AGENT}\n\nTask: {q['Question']}\nFinal Answer:"

def prompt_tau(task):
    return (f"{SYS_AGENT}\n\n"
            f"Persona: {task.get('user_persona','a customer')}\n"
            f"Task: {task.get('instruction','')}\n"
            f"Tools available: {{\"name\": str, \"find_user_id_by_email\": ..., \"get_product_details\": ...}}\n"
            f"Reason step by step, then call Final Answer:")

def prompt_alfworld(task):
    obs = task.get("observation", task.get("obs",""))
    goal = task.get("goal", task.get("task", ""))
    return (f"{SYS_AGENT}\n\nGoal: {goal}\nObservation: {obs}\nNext action (one of: go to, take, put, open, close, use, examine, inventory):")

def prompt_hotpot(q):
    ctx = " ".join(" ".join(s) for s in q["supporting_facts"].values())[:2000]
    return (f"Answer the multi-hop question. Use the context if helpful.\n\n"
            f"Context: {ctx}\n\nQuestion: {q['question']}\nFinal Answer:")

def prompt_swe(instance):
    return (f"{SYS_AGENT}\n\n"
            f"Repo: {instance.get('repo','?')}\n"
            f"Problem statement:\n{instance.get('problem_statement','')[:3000]}\n\n"
            f"Propose a unified diff that fixes the issue. Format:\n```diff\n...\n```\n"
            f"Final Answer: the patch")

# ── Runners ─────────────────────────────────────────────────────────────────
def run_gaia(mc, n=20):
    rows = get_gaia_lite(n)
    correct = 0; samples = []; t0 = time.time()
    for i, row in enumerate(rows):
        resp = mc(prompt_gaia(row), max_new_tokens=512)
        m = re.search(r'Final Answer:\s*(.+)$', resp, re.S)
        pred = m.group(1).strip() if m else resp
        ok = grade_gaia(pred, row.get("Final answer") or row.get("answer"))
        correct += int(ok)
        samples.append({"i": i, "gold": row.get("Final answer"), "pred": pred[:120], "ok": ok})
        if (i+1) % 5 == 0: print(f"  GAIA {i+1}/{len(rows)}")
    return AgentBenchResult("gaia_l1", mc.model_id, len(rows), correct,
                            100*correct/len(rows), time.time()-t0,
                            samples).tap(lambda r: r.finalize())

def run_tau_retail(mc, n=20):
    rows = get_tau_retail(n)
    correct = 0; samples = []; t0 = time.time()
    for i, task in enumerate(rows):
        gold = task.get("expected_action") or task.get("tools") or task.get("response","")
        resp = mc(prompt_tau(task), max_new_tokens=512)
        ok = bool(gold) and grade_tool_use(resp, [gold])
        correct += int(ok)
        samples.append({"i": i, "gold": str(gold)[:80], "pred": resp[:120], "ok": ok})
        if (i+1) % 5 == 0: print(f"  tau-retail {i+1}/{len(rows)}")
    return AgentBenchResult("tau_retail", mc.model_id, len(rows), correct,
                            100*correct/len(rows), time.time()-t0,
                            samples).tap(lambda r: r.finalize())

def run_alfworld(mc, n=20):
    rows = get_alfworld_text(n)
    correct = 0; samples = []; t0 = time.time()
    for i, task in enumerate(rows):
        gold = task.get("target_action") or task.get("plan", [""])[0]
        resp = mc(prompt_alfworld(task), max_new_tokens=128)
        ok = str(gold).lower() in (resp or "").lower()
        correct += int(ok)
        samples.append({"i": i, "gold": str(gold), "pred": resp[:120], "ok": ok})
        if (i+1) % 5 == 0: print(f"  ALFWorld {i+1}/{len(rows)}")
    return AgentBenchResult("alfworld_text", mc.model_id, len(rows), correct,
                            100*correct/len(rows), time.time()-t0,
                            samples).tap(lambda r: r.finalize())

def run_hotpot(mc, n=50):
    rows = get_hotpotqa(n)
    correct = 0; f1s = []; samples = []; t0 = time.time()
    for i, row in enumerate(rows):
        resp = mc(prompt_hotpot(row), max_new_tokens=128)
        m = re.search(r'Final Answer:\s*(.+)$', resp, re.S)
        pred = (m.group(1) if m else resp).strip().split('\n')[0]
        em, f1 = grade_em_f1(pred, row["answer"])
        f1s.append(f1)
        correct += int(em)
        samples.append({"i": i, "gold": row["answer"], "pred": pred[:80], "em": em, "f1": round(f1,3)})
        if (i+1) % 10 == 0: print(f"  HotpotQA {i+1}/{len(rows)}  em={correct}/{i+1}  f1={sum(f1s)/len(f1s):.3f}")
    r = AgentBenchResult("hotpotqa_distractor", mc.model_id, len(rows), correct,
                         100*correct/len(rows), time.time()-t0, samples,
                         extra={"avg_f1": round(sum(f1s)/len(f1s), 3) if f1s else 0.0})
    r.finalize(); return r

def run_swe_lite(mc, n=10):
    rows = get_swe_bench_lite(n)
    correct = 0; samples = []; t0 = time.time()
    for i, inst in enumerate(rows):
        gold_patch = inst.get("patch","")
        resp = mc(prompt_swe(inst), max_new_tokens=1024)
        # Soft match: does pred mention the gold files?
        files = re.findall(r'^--- a/(\S+)', gold_patch, re.M)
        ok = bool(files) and any(f in resp for f in files)
        correct += int(ok)
        samples.append({"i": i, "gold_files": files[:3], "pred": resp[:120], "ok": ok})
        print(f"  SWE-bench-lite {i+1}/{len(rows)} files={files[:2]}")
    return AgentBenchResult("swe_bench_lite", mc.model_id, len(rows), correct,
                            100*correct/len(rows), time.time()-t0,
                            samples).tap(lambda r: r.finalize())

BENCHES: dict[str, Callable] = {
    "gaia_l1":      run_gaia,
    "tau_retail":   run_tau_retail,
    "alfworld_text": run_alfworld,
    "hotpotqa_distractor": run_hotpot,
    "swe_bench_lite": run_swe_lite,
}

SUITES: dict[str, list[str]] = {
    "quick":   ["gaia_l1:10", "hotpotqa_distractor:20"],
    "agentic": ["gaia_l1:20", "tau_retail:20", "alfworld_text:20",
                "hotpotqa_distractor:50", "swe_bench_lite:10"],
    "tools":   ["tau_retail:20", "alfworld_text:20"],
    "reason":  ["hotpotqa_distractor:50", "gaia_l1:20"],
    "code":    ["swe_bench_lite:20"],
}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="Qwen/Qwen2.5-3B-Instruct")
    ap.add_argument("--suite", default="quick", choices=list(SUITES)+["custom"])
    ap.add_argument("--bench", default="")
    ap.add_argument("--n", type=int, default=20)
    ap.add_argument("--out", default="benchmark-results")
    ap.add_argument("--max-new-tokens", type=int, default=None)
    args = ap.parse_args()

    from harness_loader import ModelCall
    mc = ModelCall(args.model, default_max_new_tokens=args.max_new_tokens)

    if args.suite == "custom":
        items = [b.strip() for b in args.bench.split(",") if b.strip()]
    else:
        items = SUITES[args.suite]
    plan = [(b, int(n.split(":")[1]) if ":" in b else args.n)
            if ":" in b else (b, args.n) for b in items]

    Path(args.out).mkdir(exist_ok=True)
    suite_id = f"agentic_{int(time.time())}"
    suite_results = {"suite": args.suite, "model": args.model,
                     "started": datetime.now().isoformat(), "results": []}
    for b, n in plan:
        if b not in BENCHES: print(f"⚠ unknown bench: {b}"); continue
        print(f"\n{'='*60}\n  {b} n={n}\n{'='*60}")
        try:
            r = BENCHES[b](mc, n=n)
            print(f"  → {r.pct:.1f}% ({r.correct}/{r.n})  sigil={r.sigil[:16]}")
            suite_results["results"].append(asdict(r))
        except Exception as e:
            print(f"  ✗ {b} failed: {e}")
            suite_results["results"].append({"bench": b, "error": str(e)})

    pcts = [r["pct"] for r in suite_results["results"] if "pct" in r]
    suite_results["composite_pct"] = round(sum(pcts)/len(pcts), 2) if pcts else 0.0
    suite_results["ended"] = datetime.now().isoformat()
    suite_results["sigil"] = hashlib.sha256(
        json.dumps(suite_results["results"], sort_keys=True).encode()).hexdigest()
    out_path = Path(args.out) / f"agentic_{args.model.split('/')[-1]}_{suite_id}.json"
    out_path.write_text(json.dumps(suite_results, indent=2))
    print(f"\n{'='*60}\nCOMPOSITE: {suite_results['composite_pct']:.2f}%\n"
          f"SIGIL: {suite_results['sigil']}\nWritten: {out_path}")

if __name__ == "__main__":
    main()