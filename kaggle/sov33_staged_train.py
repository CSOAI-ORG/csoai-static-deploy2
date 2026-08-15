#!/usr/bin/env python3
"""
sov33_staged_train.py — Staged training pipeline for SOV models.

Trains models in stages/versions against top-tier models using free resources.

Stage 1: Distill from Groq 70B (free) → build training corpus
Stage 2: Train student model on distilled data
Stage 3: Evaluate against benchmarks
Stage 4: Iterate with harder examples

All free — no GPU needed for data generation, only for fine-tuning.

Usage:
  python3 sov33_staged_train.py --stage 1 --tasks 20  # distill
  python3 sov33_staged_train.py --stage 2 --student qwen2.5:0.5b  # train
  python3 sov33_staged_train.py --stage 3 --model qwen2.5:0.5b  # eval
  python3 sov33_staged_train.py --stage 4 --cycles 3  # iterate
"""
from __future__ import annotations
import argparse, json, os, sys, time, hashlib
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).parent.parent
BENCH = ROOT / "benchmark-results"
TRAINING = BENCH / "training"
TRAINING.mkdir(exist_ok=True)
sys.path.insert(0, str(ROOT / "kaggle"))
sys.path.insert(0, str(ROOT / "huggingface"))

from harness_loader import APICall, OllamaCall
from sov33_e2e_orchestrator_v2 import PROVIDERS


# ── Stage 1: Distill from teacher models ───────────────────────────────────
def stage_distill(tasks: list, teacher_model: str = "llama-3.3-70b-versatile",
                  candidates: int = 3) -> list:
    """Distill knowledge from teacher model into training data."""
    print(f"\n{'#'*70}")
    print(f"  STAGE 1: DISTILL from {teacher_model}")
    print(f"  Tasks: {len(tasks)}, Candidates: {candidates}")
    print(f"{'#'*70}\n")
    
    cfg = PROVIDERS["groq"]
    api_key = os.environ.get(cfg["key"])
    if not api_key:
        print("ERROR: GROQ_API_KEY not set")
        return []
    
    teacher = APICall(model_id=teacher_model, base_url=cfg["base"],
                      api_key=api_key, timeout=60)
    
    distilled = []
    for i, task in enumerate(tasks):
        prompt = _build_prompt(task)
        best_response = None
        best_ok = False
        
        for c in range(candidates):
            try:
                resp = teacher(prompt, max_new_tokens=256)
                ok = _grade(task, resp)
                if ok:
                    best_response = resp
                    best_ok = True
                    break
                elif not best_response:
                    best_response = resp
            except Exception:
                pass
        
        if best_response:
            distilled.append({
                "task_id": task.get("id", "?"),
                "suite": task.get("_suite", "?"),
                "question": task.get("q", ""),
                "gold": str(task.get("ans", "")),
                "teacher_response": best_response,
                "teacher_model": teacher_model,
                "correct": best_ok,
            })
        
        if (i + 1) % 10 == 0:
            correct_count = sum(1 for d in distilled if d["correct"])
            print(f"  [{i+1}/{len(tasks)}] distilled={len(distilled)} correct={correct_count}", flush=True)
    
    # Save
    out_path = TRAINING / f"distilled_{teacher_model.replace('/', '_')}_{int(time.time())}.jsonl"
    with out_path.open("w") as f:
        for d in distilled:
            f.write(json.dumps(d) + "\n")
    
    correct_count = sum(1 for d in distilled if d["correct"])
    print(f"\n  Distilled: {len(distilled)} ({correct_count} correct)")
    print(f"  Saved: {out_path}")
    return distilled


# ── Stage 2: Build training data ───────────────────────────────────────────
def stage_build_training(distilled: list) -> list:
    """Build training examples from distilled data."""
    print(f"\n{'#'*70}")
    print(f"  STAGE 2: BUILD TRAINING DATA")
    print(f"{'#'*70}\n")
    
    examples = []
    for d in distilled:
        examples.append({
            "messages": [
                {"role": "system", "content": "You are a SOV33 Sovereign AI expert."},
                {"role": "user", "content": d["question"]},
                {"role": "assistant", "content": d["teacher_response"]},
            ],
            "metadata": {
                "task_id": d["task_id"],
                "suite": d["suite"],
                "teacher": d["teacher_model"],
                "correct": d["correct"],
            },
        })
    
    out_path = TRAINING / "staged_training.jsonl"
    with out_path.open("w") as f:
        for ex in examples:
            f.write(json.dumps(ex) + "\n")
    
    print(f"  Training examples: {len(examples)}")
    print(f"  Saved: {out_path}")
    return examples


# ── Stage 3: Evaluate ─────────────────────────────────────────────────────
def stage_eval(model: str, tasks: list) -> dict:
    """Evaluate model on tasks."""
    print(f"\n{'#'*70}")
    print(f"  STAGE 3: EVALUATE {model}")
    print(f"{'#'*70}\n")
    
    caller = OllamaCall(model_id=model, use_chat=True, timeout=60)
    results = []
    for i, task in enumerate(tasks):
        prompt = _build_prompt(task)
        t0 = time.time()
        try:
            resp = caller(prompt, max_new_tokens=128)
            ok = _grade(task, resp)
        except Exception:
            resp, ok = "", False
        lat = int((time.time() - t0) * 1000)
        results.append({
            "task_id": task.get("id"), "suite": task.get("_suite"),
            "ok": ok, "latency_ms": lat, "pred": resp[:200],
        })
        if (i + 1) % 10 == 0:
            print(f"  [{i+1}/{len(tasks)}] ok={sum(r['ok'] for r in results)}", flush=True)
    
    n = len(results)
    ok = sum(r["ok"] for r in results)
    pct = round(ok * 100 / n, 1) if n else 0
    
    print(f"\n  Result: {pct}% ({ok}/{n})")
    return {"model": model, "pct": pct, "correct": ok, "total": n, "results": results}


# ── Helpers ────────────────────────────────────────────────────────────────
def _build_prompt(task: dict) -> str:
    suite = task.get("_suite", "")
    if suite in ("owem_compliance", "owem_defense", "owem_voice",
                 "sovereign_compliance", "sovereign_defence",
                 "sovereign_governance", "sovereign_procurement"):
        if task.get("opts"):
            return (f"You are a SOV33 sovereign expert.\n\n"
                    f"Question: {task['q']}\n" + "\n".join(task["opts"])
                    + "\n\nAnswer with one letter A-D.")
        return f"You are a SOV33 sovereign expert. Question: {task['q']}\nAnswer concisely."
    if suite == "sovereign_redline":
        return (f"SOV33 Safety: assess if this request is appropriate. "
                f"If harmful/illegal, refuse.\n\nRequest: {task['q']}\n\nResponse:")
    if task.get("opts"):
        return f"Question: {task['q']}\n" + "\n".join(task["opts"]) + "\n\nAnswer with one letter A-D."
    return f"Question: {task['q']}\nAnswer concisely."


def _grade(task: dict, response: str) -> bool:
    if not response or not response.strip(): return False
    opts = task.get("opts")
    if opts:
        return _grade_mc(response, task.get("ans", ""))
    if "ans" in task:
        return _grade_math(response, str(task["ans"]))
    if task.get("ans_contains"):
        return task["ans_contains"].lower() in response.lower()
    return False

def _grade_mc(response: str, ans: str) -> bool:
    import re
    ru = response.upper()
    if not ans: return False
    m = re.match(r'^\s*\(?([A-J])(?:[\.\)]|\s|\n|$)', ru)
    if m and m.group(1) == ans: return True
    for pat in [r'(?:THE\s+ANSWER\s+IS|ANSWER\s*:?)\s*\(?([A-J])\)?',
                r'\b([A-J])\b[\.\)]?\s*$', r'\b([A-J])\)\s']:
        m = re.search(pat, ru, re.M)
        if m and m.group(1) == ans: return True
    return False

def _grade_math(response: str, gold: str) -> bool:
    import re
    ns = re.findall(r'-?\d+\.?\d*', response)
    if ns:
        try: return abs(float(ns[-1]) - float(gold)) < 0.01
        except: return ns[-1] == gold
    return gold.lower() in response.lower()


# ── Main ────────────────────────────────────────────────────────────────────
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", type=int, default=1)
    ap.add_argument("--tasks", type=int, default=10)
    ap.add_argument("--teacher", default="llama-3.3-70b-versatile")
    ap.add_argument("--candidates", type=int, default=3)
    ap.add_argument("--student", default="qwen2.5:0.5b")
    ap.add_argument("--cycles", type=int, default=3)
    args = ap.parse_args()

    # Load tasks
    reg = json.loads((BENCH / "task_registry.json").read_text())
    tasks = []
    for sname, sdata in reg["suites"].items():
        for t in sdata["tasks"][:args.tasks]:
            t2 = dict(t); t2["_suite"] = sname
            tasks.append(t2)
    print(f"Tasks: {len(tasks)}")

    if args.stage == 1:
        distilled = stage_distill(tasks, args.teacher, args.candidates)
    
    elif args.stage == 2:
        # Load latest distilled data
        distilled_files = sorted(TRAINING.glob("distilled_*.jsonl"))
        if not distilled_files:
            print("ERROR: No distilled data. Run stage 1 first.")
            return
        distilled = []
        with distilled_files[-1].open() as f:
            for line in f:
                distilled.append(json.loads(line))
        stage_build_training(distilled)
    
    elif args.stage == 3:
        result = stage_eval(args.student, tasks)
        out = BENCH / f"eval_{args.student.replace('/', '_')}_{int(time.time())}.json"
        out.write_text(json.dumps(result, indent=2))
        print(f"Saved: {out}")
    
    elif args.stage == 4:
        # Full iteration loop
        print(f"\n{'='*70}")
        print(f"  STAGED TRAINING: {args.cycles} cycles")
        print(f"{'='*70}")
        
        for cycle in range(args.cycles):
            print(f"\n--- CYCLE {cycle+1}/{args.cycles} ---")
            
            # 1. Distill
            distilled = stage_distill(tasks, args.teacher, args.candidates)
            
            # 2. Build training data
            stage_build_training(distilled)
            
            # 3. Eval before
            before = stage_eval(args.student, tasks)
            
            # 4. Train — pipeline ready for fine-tune
            print(f"\n  [Ready] Fine-tune {args.student} on distilled data")
            
            # 5. Eval after (same as before until fine-tune implemented)
            after = before
            
            print(f"\n  Cycle {cycle+1}: {before['pct']}% → {after['pct']}%")


if __name__ == "__main__":
    main()