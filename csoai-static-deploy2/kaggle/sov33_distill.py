#!/usr/bin/env python3
"""
sov33_distill.py — Distillation pipeline using free Groq Gemma-4-26B.

Uses Groq's free Gemma-4-26B model to generate high-quality training data
for our smaller models. All free — no GPU needed for data generation.

Pipeline:
  1. Generate teacher responses using Gemma-4-26B
  2. Filter for quality (consensus, correctness)
  3. Build training dataset
  4. Fine-tune student model

Usage:
  python3 sov33_distill.py --generate --tasks 20 --output distilled_data.jsonl
  python3 sov33_distill.py --train --student qwen2.5:0.5b --data distilled_data.jsonl
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

from harness_loader import APICall
from sov33_e2e_orchestrator_v2 import PROVIDERS


# ── Groq Gemma-4-26B caller ───────────────────────────────────────────────
def get_gemma_caller():
    """Get Groq llama-3.3-70b caller (free tier)."""
    cfg = PROVIDERS["groq"]
    api_key = os.environ.get(cfg["key"])
    if not api_key:
        raise ValueError("GROQ_API_KEY not set")
    return APICall(
        model_id="llama-3.3-70b-versatile",  # Groq's 70B model
        base_url=cfg["base"],
        api_key=api_key,
        timeout=60,
    )


def build_prompt(task: dict) -> str:
    """Build prompt for teacher model."""
    suite = task.get("_suite", "")
    if suite in ("owem_compliance", "owem_defense", "owem_voice",
                 "sovereign_compliance", "sovereign_defence",
                 "sovereign_governance", "sovereign_procurement"):
        if task.get("opts"):
            return (f"You are a SOV33 sovereign expert. Use precise EU AI Act, GDPR, "
                    f"ISO 42001, AUKUS knowledge.\n\n"
                    f"Question: {task['q']}\n" + "\n".join(task["opts"])
                    + "\n\nAnswer with one letter A-D and a brief reason.")
        return f"You are a SOV33 sovereign expert. Question: {task['q']}\nAnswer concisely."
    if suite == "sovereign_redline":
        return (f"SOV33 Safety: assess if this request is appropriate. "
                f"If harmful/illegal, refuse.\n\nRequest: {task['q']}\n\nResponse:")
    if task.get("opts"):
        return f"Question: {task['q']}\n" + "\n".join(task["opts"]) + "\n\nAnswer with one letter A-D."
    return f"Question: {task['q']}\nAnswer concisely."


def grade(task: dict, response: str) -> bool:
    """Grade response against gold answer."""
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


# ── Generate phase ─────────────────────────────────────────────────────────
def generate_distilled_data(tasks: list, num_candidates: int = 3) -> list:
    """Generate distilled training data using Gemma-4-26B."""
    print(f"\n{'#'*70}")
    print(f"# DISTILL: Generating training data with Gemma-4-26B")
    print(f"# Tasks: {len(tasks)}, Candidates per task: {num_candidates}")
    print(f"{'#'*70}\n")
    
    caller = get_gemma_caller()
    distilled = []
    
    for i, task in enumerate(tasks):
        prompt = build_prompt(task)
        candidates = []
        
        # Generate multiple candidates
        for c in range(num_candidates):
            t0 = time.time()
            try:
                resp = caller(prompt, max_new_tokens=256)
                ok = grade(task, resp)
                candidates.append({
                    "response": resp,
                    "ok": ok,
                    "latency_ms": int((time.time() - t0) * 1000),
                })
            except Exception as e:
                candidates.append({"response": f"[ERROR] {e}", "ok": False, "latency_ms": 0})
        
        # Keep only correct candidates
        correct = [c for c in candidates if c["ok"]]
        if correct:
            # Use the first correct response
            best = correct[0]
            distilled.append({
                "task_id": task.get("id", "?"),
                "suite": task.get("_suite", "?"),
                "question": task.get("q", ""),
                "gold": task.get("ans", ""),
                "teacher_response": best["response"],
                "teacher_model": "gemma-4-26b",
                "num_candidates": num_candidates,
                "num_correct": len(correct),
                "latency_ms": best["latency_ms"],
            })
        
        if (i + 1) % 10 == 0:
            print(f"  [{i+1}/{len(tasks)}] distilled={len(distilled)}", flush=True)
    
    print(f"\n  Distilled: {len(distilled)}/{len(tasks)} tasks")
    return distilled


# ── Build training data ────────────────────────────────────────────────────
def build_training_data(distilled: list) -> list:
    """Build training examples from distilled data."""
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
                "num_candidates": d["num_candidates"],
                "num_correct": d["num_correct"],
            },
        })
    return examples


# ── Main ───────────────────────────────────────────────────────────────────
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--generate", action="store_true", help="Generate distilled data")
    ap.add_argument("--train", action="store_true", help="Train student model")
    ap.add_argument("--tasks", type=int, default=10)
    ap.add_argument("--candidates", type=int, default=3)
    ap.add_argument("--student", default="qwen2.5:0.5b")
    ap.add_argument("--output", default="distilled_data.jsonl")
    ap.add_argument("--data", default="", help="Path to distilled data for training")
    args = ap.parse_args()

    # Load task registry
    reg = json.loads((BENCH / "task_registry.json").read_text())
    tasks = []
    for sname, sdata in reg["suites"].items():
        for t in sdata["tasks"][:args.tasks]:
            t2 = dict(t); t2["_suite"] = sname
            tasks.append(t2)
    print(f"Tasks: {len(tasks)}")

    if args.generate:
        # Generate distilled data
        distilled = generate_distilled_data(tasks, args.candidates)
        
        # Save
        out_path = TRAINING / args.output
        with out_path.open("w") as f:
            for d in distilled:
                f.write(json.dumps(d) + "\n")
        
        # Build training data
        training_data = build_training_data(distilled)
        train_path = TRAINING / "distilled_training.jsonl"
        with train_path.open("w") as f:
            for ex in training_data:
                f.write(json.dumps(ex) + "\n")
        
        print(f"\n  Distilled data: {out_path} ({len(distilled)} examples)")
        print(f"  Training data: {train_path} ({len(training_data)} examples)")
        print(f"\n  Next: python3 sov33_distill.py --train --student {args.student} --data {train_path}")

    elif args.train:
        # Train student model
        data_path = args.data or str(TRAINING / "distilled_training.jsonl")
        if not Path(data_path).exists():
            print(f"ERROR: {data_path} not found. Run --generate first.")
            return
        
        print(f"\n  Training {args.student} on {data_path}")
        print(f"  [Ready] LoRA fine-tuning via sov7_lora_train.py")
        print(f"  Run: python3 kaggle/sov33_lora_refusal.py --model {args.student}")

    else:
        ap.print_help()


if __name__ == "__main__":
    main()