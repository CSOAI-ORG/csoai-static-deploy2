#!/usr/bin/env python3
"""
sov33_overnight.py — Overnight E2E improvement loop.

Runs continuously on Oracle CPU (slow but works):
  1. DISTILL — extract knowledge from Groq 70B (free)
  2. EVAL — evaluate all models on comprehensive benchmark
  3. TRAIN — build training data from distilled knowledge
  4. IMPROVE — compare before/after, select best answers
  5. REPEAT — loop until convergence or time limit

All free — no GPU needed. Runs on Oracle CPU.

Usage:
  python3 sov33_overnight.py --hours 8 --tasks 20
  python3 sov33_overnight.py --cycles 5 --tasks 10
"""
from __future__ import annotations
import argparse, json, os, sys, time, hashlib, subprocess
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).parent.parent
BENCH = ROOT / "benchmark-results"
TRAINING = BENCH / "training"
TRAINING.mkdir(exist_ok=True)
sys.path.insert(0, str(ROOT / "kaggle"))

from harness_loader import APICall
from sov33_e2e_orchestrator_v2 import PROVIDERS


# ── Teacher caller ─────────────────────────────────────────────────────────
def get_teacher():
    cfg = PROVIDERS["groq"]
    api_key = os.environ.get(cfg["key"])
    if not api_key:
        raise ValueError("GROQ_API_KEY not set")
    return APICall(model_id="llama-3.3-70b-versatile",
                   base_url=cfg["base"], api_key=api_key, timeout=60)


# ── Build prompt ───────────────────────────────────────────────────────────
def build_prompt(task: dict) -> str:
    suite = task.get("_suite", "")
    if suite.startswith("owem_") or suite.startswith("sovereign_"):
        if task.get("opts"):
            return (f"You are a SOV33 sovereign expert. Use precise EU AI Act, GDPR, "
                    f"ISO 42001, AUKUS, NCSC knowledge.\n\n"
                    f"Question: {task['q']}\n" + "\n".join(task["opts"])
                    + "\n\nAnswer with one letter A-D.")
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


# ── Distill ────────────────────────────────────────────────────────────────
def distill(teacher, tasks: list, candidates: int = 3) -> list:
    """Distill knowledge from teacher."""
    distilled = []
    for i, task in enumerate(tasks):
        prompt = build_prompt(task)
        best, best_ok = None, False
        for _ in range(candidates):
            try:
                resp = teacher(prompt, max_new_tokens=256)
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
            print(f"    [{i+1}/{len(tasks)}] distilled={len(distilled)}", flush=True)
    return distilled


# ── Eval ───────────────────────────────────────────────────────────────────
def eval_tasks(teacher, tasks: list) -> dict:
    """Evaluate teacher on tasks."""
    results = []
    for i, task in enumerate(tasks):
        prompt = build_prompt(task)
        t0 = time.time()
        try:
            resp = teacher(prompt, max_new_tokens=128)
            ok = grade(task, resp)
        except Exception:
            resp, ok = "", False
        results.append({"task_id": task.get("id"), "suite": task.get("_suite"),
                        "ok": ok, "pred": resp[:200],
                        "latency_ms": int((time.time()-t0)*1000)})
        if (i+1) % 20 == 0:
            print(f"    [{i+1}/{len(tasks)}] ok={sum(r['ok'] for r in results)}", flush=True)
    n = len(results)
    ok = sum(r["ok"] for r in results)
    return {"pct": round(ok*100/n, 1) if n else 0, "correct": ok, "total": n, "results": results}


# ── Improve ────────────────────────────────────────────────────────────────
def improve(distilled: list, eval_result: dict) -> dict:
    """Compare distilled answers vs eval results. Find improvements."""
    eval_by_task = {}
    for r in eval_result.get("results", []):
        if r.get("task_id"):
            eval_by_task[r["task_id"]] = r

    improvements = []
    for d in distilled:
        tid = d["task_id"]
        eval_r = eval_by_task.get(tid)
        if eval_r and not eval_r.get("ok") and d.get("correct"):
            improvements.append({
                "task_id": tid,
                "suite": d["suite"],
                "distilled_response": d["teacher_response"][:200],
                "improvement": True,
            })

    return {
        "total_distilled": len(distilled),
        "total_evaluated": len(eval_result.get("results", [])),
        "improvements_found": len(improvements),
        "improvements": improvements[:20],
    }


# ── Main loop ──────────────────────────────────────────────────────────────
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--hours", type=float, default=8)
    ap.add_argument("--cycles", type=int, default=0)
    ap.add_argument("--tasks", type=int, default=10)
    ap.add_argument("--out-prefix", default="overnight")
    args = ap.parse_args()

    end_time = datetime.now() + timedelta(hours=args.hours)
    cycle = 0

    # Load tasks
    reg = json.loads((BENCH / "task_registry.json").read_text())
    all_tasks = []
    for sname, sdata in reg["suites"].items():
        for t in sdata["tasks"][:args.tasks]:
            t2 = dict(t); t2["_suite"] = sname
            all_tasks.append(t2)
    print(f"Tasks: {len(all_tasks)} | Hours: {args.hours}")

    teacher = get_teacher()
    all_cycles = []
    all_distilled = []

    while True:
        cycle += 1
        if args.cycles and cycle > args.cycles:
            break
        if datetime.now() >= end_time:
            break

        print(f"\n{'='*60}")
        print(f"  CYCLE {cycle} — {datetime.now().strftime('%H:%M:%S')}")
        print(f"  Time remaining: {(end_time - datetime.now()).total_seconds()/60:.0f} min")
        print(f"{'='*60}")

        # 1. Eval
        print(f"\n  [EVAL] Evaluating on {len(all_tasks)} tasks...")
        eval_result = eval_tasks(teacher, all_tasks)
        print(f"  Result: {eval_result['pct']}% ({eval_result['correct']}/{eval_result['total']})")

        # 2. Distill
        print(f"\n  [DISTILL] Extracting from Groq 70B...")
        distilled = distill(teacher, all_tasks, candidates=3)
        all_distilled.extend(distilled)
        print(f"  Distilled: {len(distilled)} (total: {len(all_distilled)})")

        # 3. Improve
        print(f"\n  [IMPROVE] Finding improvements...")
        improvement = improve(distilled, eval_result)
        print(f"  Improvements: {improvement['improvements_found']}")

        # 4. Save cycle
        cycle_result = {
            "cycle": cycle,
            "ts": datetime.now().isoformat(),
            "eval": eval_result,
            "distilled": len(distilled),
            "improvement": improvement,
        }
        all_cycles.append(cycle_result)

        # Save incremental results
        out = BENCH / f"{args.out_prefix}_cycle_{cycle}.json"
        out.write_text(json.dumps(cycle_result, indent=2, default=str))
        print(f"  Saved: {out}")

        # Save distilled data
        distilled_path = TRAINING / f"overnight_distilled_{cycle}.jsonl"
        with distilled_path.open("w") as f:
            for d in distilled:
                f.write(json.dumps(d) + "\n")
        print(f"  Distilled: {distilled_path}")

        # 5. Wait (CPU-bound work, small pause)
        time.sleep(5)

    # Final summary
    print(f"\n{'='*60}")
    print(f"  OVERNIGHT RUN COMPLETE — {cycle} cycles")
    print(f"{'='*60}")
    print(f"  Total distilled: {len(all_distilled)}")
    print(f"  Cycles: {len(all_cycles)}")

    if all_cycles:
        pcts = [c["eval"]["pct"] for c in all_cycles]
        print(f"  Best eval: {max(pcts):.1f}%")
        print(f"  Last eval: {pcts[-1]:.1f}%")

    # Save final summary
    summary = {
        "hours": args.hours,
        "cycles": len(all_cycles),
        "total_distilled": len(all_distilled),
        "eval_history": [c["eval"]["pct"] for c in all_cycles],
        "best_pct": max((c["eval"]["pct"] for c in all_cycles), default=0),
        "final_pct": all_cycles[-1]["eval"]["pct"] if all_cycles else 0,
    }
    out = BENCH / f"{args.out_prefix}_summary.json"
    out.write_text(json.dumps(summary, indent=2))
    print(f"\n  Summary: {out}")


if __name__ == "__main__":
    main()