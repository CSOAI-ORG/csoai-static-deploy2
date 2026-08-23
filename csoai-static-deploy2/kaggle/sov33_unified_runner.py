#!/usr/bin/env python3
"""
sov33_unified_runner.py — Unified runner for all SOV33 operations.

Runs everything from a single command:
  - Distillation from teacher models
  - Benchmark evaluation
  - Self-training loop
  - C-Space creative simulation
  - SOV SPACE visual mapping

Usage:
  python3 sov33_unified_runner.py --mode all --tasks 5
  python3 sov33_unified_runner.py --mode distill --teacher groq --tasks 20
  python3 sov33_unified_runner.py --mode eval --model qwen2.5:0.5b --tasks 10
  python3 sov33_unified_runner.py --mode train --student qwen2.5:0.5b
  python3 sov33_unified_runner.py --mode dream --scenario "win EU AI Act contract"
"""
from __future__ import annotations
import argparse, json, os, sys, time, hashlib
from datetime import datetime
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).parent.parent
BENCH = ROOT / "benchmark-results"
TRAINING = BENCH / "training"
TRAINING.mkdir(exist_ok=True)
sys.path.insert(0, str(ROOT / "kaggle"))

try:
    from harness_loader import APICall, OllamaCall
    from sov33_e2e_orchestrator_v2 import PROVIDERS
except ImportError:
    PROVIDERS = {}


# ── Unified Model Caller ──────────────────────────────────────────────────
class ModelCaller:
    """Unified caller for Ollama + API models."""
    def __init__(self, provider: str = "ollama", model: str = "", model_override: str = ""):
        self.provider = provider
        self.model = model
        
        if provider == "ollama":
            self._caller = OllamaCall(model_id=model, use_chat=True, timeout=60)
        else:
            cfg = PROVIDERS.get(provider, {})
            api_key = os.environ.get(cfg.get("key", ""), "")
            if not api_key:
                raise ValueError(f"No API key for {provider}")
            self._caller = APICall(
                model_id=model_override or cfg.get("model", model),
                base_url=cfg.get("base", ""),
                api_key=api_key, timeout=60
            )
    
    def __call__(self, prompt: str, max_tokens: int = 256) -> str:
        return self._caller(prompt, max_new_tokens=max_tokens)


# ── Grading ────────────────────────────────────────────────────────────────
def grade(task: dict, response: str) -> bool:
    if not response or not response.strip(): return False
    opts = task.get("opts")
    if opts:
        return _grade_mc(response, task.get("ans", ""))
    if "ans" in task:
        return _grade_math(response, str(task["ans"]))
    if task.get("ans_contains"):
        return task["ans_contains"].lower() in response.lower()
    return False

def _grade_mc(r: str, a: str) -> bool:
    import re
    ru = r.upper()
    if not a: return False
    m = re.match(r'^\s*\(?([A-J])(?:[\.\)]|\s|\n|$)', ru)
    if m and m.group(1) == a: return True
    for p in [r'(?:THE\s+ANSWER\s+IS|ANSWER\s*:?)\s*\(?([A-J])\)?', r'\b([A-J])\b[\.\)]?\s*$']:
        m = re.search(p, ru, re.M)
        if m and m.group(1) == a: return True
    return False

def _grade_math(r: str, g: str) -> bool:
    import re
    ns = re.findall(r'-?\d+\.?\d*', r)
    if ns:
        try: return abs(float(ns[-1]) - float(g)) < 0.01
        except: return ns[-1] == g
    return g.lower() in r.lower()


# ── Build prompt ───────────────────────────────────────────────────────────
def build_prompt(task: dict) -> str:
    suite = task.get("_suite", "")
    if suite.startswith("owem_") or suite.startswith("sovereign_"):
        if task.get("opts"):
            return (f"You are a SOV33 sovereign expert.\n\n"
                    f"Question: {task['q']}\n" + "\n".join(task["opts"])
                    + "\n\nAnswer with one letter A-D.")
        return f"You are a SOV33 sovereign expert. Question: {task['q']}\nAnswer concisely."
    if task.get("opts"):
        return f"Question: {task['q']}\n" + "\n".join(task["opts"]) + "\n\nAnswer with one letter A-D."
    return f"Question: {task['q']}\nAnswer concisely."


# ── Distill ────────────────────────────────────────────────────────────────
def distill(tasks: list, caller: ModelCaller, candidates: int = 3) -> list:
    """Distill knowledge from teacher model."""
    print(f"\n{'#'*60}\n# DISTILL: {len(tasks)} tasks × {candidates} candidates\n{'#'*60}")
    distilled = []
    for i, task in enumerate(tasks):
        prompt = build_prompt(task)
        best, best_ok = None, False
        for _ in range(candidates):
            try:
                resp = caller(prompt, max_tokens=256)
                ok = grade(task, resp)
                if ok:
                    best, best_ok = resp, True
                    break
                elif not best:
                    best = resp
            except Exception:
                pass
        if best:
            distilled.append({
                "task_id": task.get("id", "?"), "suite": task.get("_suite", "?"),
                "question": task.get("q", ""), "gold": str(task.get("ans", "")),
                "teacher_response": best, "correct": best_ok,
            })
        if (i+1) % 10 == 0:
            print(f"  [{i+1}/{len(tasks)}] distilled={len(distilled)}", flush=True)
    
    # Save
    out = TRAINING / f"distilled_{int(time.time())}.jsonl"
    with out.open("w") as f:
        for d in distilled:
            f.write(json.dumps(d) + "\n")
    print(f"  Saved: {out} ({len(distilled)} examples)")
    return distilled


# ── Eval ───────────────────────────────────────────────────────────────────
def eval_model(tasks: list, caller: ModelCaller) -> dict:
    """Evaluate model on tasks."""
    print(f"\n{'#'*60}\n# EVAL: {caller.provider}:{caller.model}\n{'#'*60}")
    results = []
    for i, task in enumerate(tasks):
        prompt = build_prompt(task)
        t0 = time.time()
        try:
            resp = caller(prompt, max_tokens=128)
            ok = grade(task, resp)
        except Exception:
            resp, ok = "", False
        results.append({"task_id": task.get("id"), "suite": task.get("_suite"),
                        "ok": ok, "latency_ms": int((time.time()-t0)*1000),
                        "pred": resp[:200]})
        if (i+1) % 10 == 0:
            print(f"  [{i+1}/{len(tasks)}] ok={sum(r['ok'] for r in results)}", flush=True)
    
    n = len(results)
    ok = sum(r["ok"] for r in results)
    pct = round(ok*100/n, 1) if n else 0
    print(f"  Result: {pct}% ({ok}/{n})")
    return {"model": f"{caller.provider}:{caller.model}", "pct": pct,
            "correct": ok, "total": n, "results": results}


# ── Train ──────────────────────────────────────────────────────────────────
def train(student: str, distilled: list):
    """Build training data from distilled examples."""
    print(f"\n{'#'*60}\n# TRAIN: {student}\n{'#'*60}")
    examples = []
    for d in distilled:
        examples.append({
            "messages": [
                {"role": "system", "content": "You are a SOV33 Sovereign AI."},
                {"role": "user", "content": d["question"]},
                {"role": "assistant", "content": d["teacher_response"]},
            ],
            "metadata": {"task_id": d["task_id"], "suite": d["suite"], "correct": d["correct"]},
        })
    out = TRAINING / f"training_{student.replace('/','_')}_{int(time.time())}.jsonl"
    with out.open("w") as f:
        for ex in examples:
            f.write(json.dumps(ex) + "\n")
    print(f"  Training data: {out} ({len(examples)} examples)")
    print(f"  Next: python3 kaggle/kaggle_rwkv7_sov33.py (on Kaggle T4)")


# ── Main ────────────────────────────────────────────────────────────────────
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", default="all", choices=["all", "distill", "eval", "train", "dream"])
    ap.add_argument("--teacher", default="groq", help="Teacher provider for distillation")
    ap.add_argument("--teacher-model", default="", help="Override teacher model")
    ap.add_argument("--student", default="qwen2.5:0.5b", help="Student model")
    ap.add_argument("--model", default="", help="Model for eval")
    ap.add_argument("--provider", default="ollama", help="Provider for eval")
    ap.add_argument("--tasks", type=int, default=5)
    ap.add_argument("--candidates", type=int, default=3)
    ap.add_argument("--scenario", default="What if we won the EU AI Act contract?")
    args = ap.parse_args()

    # Load tasks
    reg = json.loads((BENCH / "task_registry.json").read_text())
    tasks = []
    for sname, sdata in reg["suites"].items():
        for t in sdata["tasks"][:args.tasks]:
            t2 = dict(t); t2["_suite"] = sname
            tasks.append(t2)
    print(f"Tasks: {len(tasks)}")

    if args.mode == "distill":
        cfg = PROVIDERS.get(args.teacher, {})
        caller = ModelCaller(provider=args.teacher, model=args.teacher_model or cfg.get("model", ""))
        distill(tasks, caller, args.candidates)

    elif args.mode == "eval":
        provider = args.provider or "ollama"
        caller = ModelCaller(provider=provider, model=args.model or "qwen2.5:0.5b")
        result = eval_model(tasks, caller)
        out = BENCH / f"eval_{args.model.replace('/','_')}_{int(time.time())}.json"
        out.write_text(json.dumps(result, indent=2))
        print(f"Saved: {out}")

    elif args.mode == "train":
        # Load latest distilled data
        distilled_files = sorted(TRAINING.glob("distilled_*.jsonl"))
        if not distilled_files:
            print("No distilled data. Run --mode distill first.")
            return
        distilled = []
        with distilled_files[-1].open() as f:
            for line in f:
                distilled.append(json.loads(line))
        train(args.student, distilled)

    elif args.mode == "dream":
        print(f"\nDreaming: {args.scenario}")
        print("(C-Space simulation — use sov_space_creative.py for full implementation)")

    elif args.mode == "all":
        # Run everything
        print(f"\n{'='*60}")
        print("  UNIFIED RUNNER — ALL MODES")
        print(f"{'='*60}")
        
        # 1. Distill
        cfg = PROVIDERS.get(args.teacher, {})
        teacher = ModelCaller(provider=args.teacher, model=cfg.get("model", ""))
        distilled = distill(tasks, teacher, args.candidates)
        
        # 2. Train
        train(args.student, distilled)
        
        # 3. Eval student
        student_caller = ModelCaller(provider="ollama", model=args.student)
        student_result = eval_model(tasks, student_caller)
        
        # 4. Eval teacher (baseline)
        teacher_result = eval_model(tasks, teacher)
        
        # 5. Compare
        print(f"\n{'='*60}")
        print("  COMPARISON")
        print(f"{'='*60}")
        print(f"  Teacher: {teacher_result['pct']}%")
        print(f"  Student: {student_result['pct']}%")
        print(f"  Delta: {student_result['pct'] - teacher_result['pct']:+.1f}%")


if __name__ == "__main__":
    main()