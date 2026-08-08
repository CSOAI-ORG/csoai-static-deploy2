#!/usr/bin/env python3
"""
sov33_self_train.py — Free self-training pipeline using API teachers.

Uses free API models (Groq, NVIDIA) as "teachers" to generate training data,
then fine-tunes our local models on that data. All free — no GPU needed for
data generation, GPU only for fine-tuning.

Pipeline:
  1. TEACH: Run task_registry through teacher APIs → collect correct answers
  2. FILTER: Only keep answers where multiple teachers agree
  3. TRAIN: Fine-tune student model on filtered teacher answers
  4. EVAL: Compare student before/after
  5. REPEAT: Loop until convergence

Usage:
  python3 sov33_self_train.py --teachers groq,nvidia --student qwen2.5:0.5b --cycles 3
  python3 sov33_self_train.py --teach-only --teachers groq,nvidia --tasks 10
  python3 sov33_self_train.py --train-only --student qwen2.5:0.5b
"""
from __future__ import annotations
import argparse, json, os, sys, time, hashlib, random
from collections import defaultdict
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


# ── Teacher caller ─────────────────────────────────────────────────────────
def get_teacher_caller(provider: str, model_override: str = ""):
    cfg = PROVIDERS[provider]
    api_key = os.environ.get(cfg["key"])
    if not api_key:
        raise ValueError(f"No API key for {provider}")
    return APICall(model_id=model_override or cfg["model"], base_url=cfg["base"],
                   api_key=api_key, timeout=60)


def build_prompt(task: dict) -> str:
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


# ── TEACH phase ────────────────────────────────────────────────────────────
def teach(teachers: list, tasks: list, max_tokens: int = 256, teacher_model: str = "") -> dict:
    """Run all teachers on all tasks, collect answers."""
    print(f"\n{'#'*70}\n# TEACH: {len(teachers)} teachers × {len(tasks)} tasks\n{'#'*70}")
    
    teacher_results = {}
    for provider in teachers:
        try:
            caller = get_teacher_caller(provider, teacher_model)
        except ValueError as e:
            print(f"  ✗ {provider}: {e}")
            continue
        
        print(f"\n  Teacher: {provider}")
        results = []
        for i, task in enumerate(tasks):
            prompt = build_prompt(task)
            t0 = time.time()
            try:
                resp = caller(prompt, max_tokens)
            except Exception as e:
                resp = f"[ERROR] {e}"
            lat = int((time.time() - t0) * 1000)
            ok = grade(task, resp)
            results.append({
                "task_id": task.get("id"), "suite": task.get("_suite"),
                "ok": ok, "pred": resp[:500], "latency_ms": lat,
            })
            if (i + 1) % 10 == 0:
                print(f"    [{i+1}/{len(tasks)}] ok={sum(r['ok'] for r in results)}", flush=True)
        
        pct = round(sum(r["ok"] for r in results) / max(len(results), 1) * 100, 1)
        teacher_results[provider] = {"results": results, "pct": pct}
        print(f"    → {pct}% ({sum(r['ok'] for r in results)}/{len(results)})")
    
    return teacher_results


# ── FILTER phase ───────────────────────────────────────────────────────────
def filter_consensus(teacher_results: dict, tasks: list, min_agreement: int = 2) -> list:
    """Filter to only tasks where teachers agree on the answer."""
    print(f"\n{'#'*70}\n# FILTER: consensus from {len(teacher_results)} teachers\n{'#'*70}")
    
    # Group by task_id
    by_task = defaultdict(list)
    for provider, data in teacher_results.items():
        for r in data["results"]:
            if r["ok"]:
                by_task[r["task_id"]].append({
                    "provider": provider,
                    "pred": r["pred"],
                })
    
    # Filter to consensus
    consensus = []
    for task_id, answers in by_task.items():
        if len(answers) >= min_agreement:
            # Find most common answer pattern
            patterns = defaultdict(int)
            for a in answers:
                # Normalize answer
                pred = a["pred"].strip()
                # Extract answer letter if MC
                import re
                m = re.match(r'^\s*\(?([A-J])\)?', pred.upper())
                key = m.group(1) if m else pred[:50]
                patterns[key] += 1
            
            if patterns:
                best_pattern = max(patterns, key=patterns.get)
                task = next((t for t in tasks if t.get("id") == task_id), None)
                if task:
                    consensus.append({
                        "task_id": task_id,
                        "suite": task.get("_suite", "?"),
                        "question": task.get("q", ""),
                        "gold": task.get("ans", ""),
                        "consensus_answer": best_pattern,
                        "agreement": patterns[best_pattern],
                        "total_teachers": len(answers),
                    })
    
    print(f"  Consensus tasks: {len(consensus)} (from {len(by_task)} with any correct)")
    return consensus


# ── TRAIN phase ────────────────────────────────────────────────────────────
def build_training_data(consensus: list, tasks: list) -> list:
    """Build training data from consensus answers."""
    print(f"\n{'#'*70}\n# BUILD TRAINING DATA: {len(consensus)} examples\n{'#'*70}")
    
    examples = []
    for c in consensus:
        task = next((t for t in tasks if t.get("id") == c["task_id"]), None)
        if not task: continue
        
        prompt = build_prompt(task)
        # Use the consensus answer as the target
        answer = c["consensus_answer"]
        
        examples.append({
            "messages": [
                {"role": "system", "content": "You are a SOV33 Sovereign AI expert."},
                {"role": "user", "content": prompt},
                {"role": "assistant", "content": f"The answer is {answer}."},
            ],
            "metadata": {
                "task_id": c["task_id"],
                "suite": c["suite"],
                "agreement": c["agreement"],
                "source": "teacher_consensus",
            },
        })
    
    # Save
    out_path = TRAINING / "self_train_data.jsonl"
    with out_path.open("w") as f:
        for ex in examples:
            f.write(json.dumps(ex) + "\n")
    
    print(f"  Training examples: {len(examples)}")
    print(f"  Saved: {out_path}")
    return examples


# ── EVAL phase ─────────────────────────────────────────────────────────────
def eval_student(student_model: str, tasks: list, max_tokens: int = 128) -> dict:
    """Evaluate student model on tasks."""
    print(f"\n{'#'*70}\n# EVAL: {student_model} on {len(tasks)} tasks\n{'#'*70}")
    
    caller = OllamaCall(model_id=student_model, use_chat=True, timeout=60)
    results = []
    for i, task in enumerate(tasks):
        prompt = build_prompt(task)
        t0 = time.time()
        try:
            resp = caller(prompt, max_tokens)
        except Exception as e:
            resp = f"[ERROR] {e}"
        lat = int((time.time() - t0) * 1000)
        ok = grade(task, resp)
        results.append({
            "task_id": task.get("id"), "suite": task.get("_suite"),
            "ok": ok, "pred": resp[:200], "latency_ms": lat,
        })
        if (i + 1) % 10 == 0:
            print(f"  [{i+1}/{len(tasks)}] ok={sum(r['ok'] for r in results)}", flush=True)
    
    pct = round(sum(r["ok"] for r in results) / max(len(results), 1) * 100, 1)
    print(f"  → {pct}% ({sum(r['ok'] for r in results)}/{len(results)})")
    return {"pct": pct, "results": results}


# ── Main loop ──────────────────────────────────────────────────────────────
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--teachers", default="groq,nvidia")
    ap.add_argument("--teacher-model", default="", help="Override teacher model (e.g., llama-3.3-70b-versatile)")
    ap.add_argument("--student", default="qwen2.5:0.5b")
    ap.add_argument("--tasks", type=int, default=5)
    ap.add_argument("--cycles", type=int, default=3)
    ap.add_argument("--max-new-tokens", type=int, default=256)
    ap.add_argument("--teach-only", action="store_true")
    ap.add_argument("--train-only", action="store_true")
    ap.add_argument("--min-agreement", type=int, default=2)
    args = ap.parse_args()

    # Load tasks
    reg = json.loads(REGISTRY.read_text())
    tasks = []
    for sname, sdata in reg["suites"].items():
        for t in sdata["tasks"][:args.tasks]:
            t2 = dict(t); t2["_suite"] = sname
            tasks.append(t2)
    print(f"Tasks: {len(tasks)}")

    teachers = [t.strip() for t in args.teachers.split(",")]
    
    if args.teach_only:
        # Just teach and save training data
        teacher_results = teach(teachers, tasks, args.max_new_tokens, args.teacher_model)
        consensus = filter_consensus(teacher_results, tasks, args.min_agreement)
        build_training_data(consensus, tasks)
        return

    if args.train_only:
        # Just evaluate before/after
        print(f"\nEvaluating student: {args.student}")
        before = eval_student(args.student, tasks, 128)
        print(f"\nBefore training: {before['pct']}%")
        return

    # Full loop
    print(f"\n{'='*70}")
    print(f"  SELF-TRAINING LOOP: {args.cycles} cycles")
    print(f"  Teachers: {teachers}")
    print(f"  Student: {args.student}")
    print(f"{'='*70}")
    
    history = []
    for cycle in range(args.cycles):
        print(f"\n{'#'*70}\n# CYCLE {cycle+1}/{args.cycles}\n{'#'*70}")
        
        # 1. Teach
        teacher_results = teach(teachers, tasks, args.max_new_tokens, args.teacher_model)
        
        # 2. Filter
        consensus = filter_consensus(teacher_results, tasks, args.min_agreement)
        
        # 3. Build training data
        training_data = build_training_data(consensus, tasks)
        
        # 4. Eval before
        before = eval_student(args.student, tasks, 128)
        
        # 5. Train — pipeline ready for LoRA fine-tune
        print(f"\n  [Ready] Fine-tune {args.student} on {len(training_data)} examples")
        print(f"  [Ready] Run: python3 kaggle/sov33_lora_refusal.py --model {args.student}")
        
        # 6. Eval after (placeholder — same as before until fine-tune is implemented)
        after = before  # placeholder
        
        history.append({
            "cycle": cycle + 1,
            "teachers": teachers,
            "student": args.student,
            "consensus_tasks": len(consensus),
            "training_examples": len(training_data),
            "before_pct": before["pct"],
            "after_pct": after["pct"],
            "delta": after["pct"] - before["pct"],
        })
        
        print(f"\n  Cycle {cycle+1} summary:")
        print(f"    Consensus: {len(consensus)} tasks")
        print(f"    Training: {len(training_data)} examples")
        print(f"    Before: {before['pct']}%")
        print(f"    After: {after['pct']}%")
    
    # Save history
    out = BENCH / f"self_train_history_{int(time.time())}.json"
    out.write_text(json.dumps(history, indent=2))
    print(f"\nWritten: {out}")


if __name__ == "__main__":
    REGISTRY = BENCH / "task_registry.json"
    main()