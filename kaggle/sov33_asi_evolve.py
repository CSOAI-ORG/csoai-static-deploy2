#!/usr/bin/env python3
"""
sov33_asi_evolve.py — ASI Evolve autonomous loop.

Runs continuously using free APIs:
  1. EVAL — evaluate all models
  2. DISTILL — extract knowledge from best models
  3. TRAIN — build training data
  4. IMPROVE — compare and improve
  5. REPEAT

Handles rate limits by rotating providers.
All free — runs on Oracle CPU.

Usage:
  python3 sov33_asi_evolve.py --hours 8
  python3 sov33_asi_evolve.py --cycles 10
"""
from __future__ import annotations
import argparse, json, os, sys, time, hashlib, random
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


# ── Provider rotation (handle rate limits) ─────────────────────────────────
PROVIDER_ORDER = ["groq", "nvidia", "openrouter"]
current_provider_idx = 0

def get_caller():
    """Get caller with automatic provider rotation."""
    global current_provider_idx
    for _ in range(len(PROVIDER_ORDER)):
        prov = PROVIDER_ORDER[current_provider_idx]
        cfg = PROVIDERS.get(prov, {})
        api_key = os.environ.get(cfg.get("key", ""), "")
        if api_key:
            try:
                caller = APICall(
                    model_id=cfg["model"],
                    base_url=cfg["base"],
                    api_key=api_key,
                    timeout=60,
                )
                # Quick test
                resp = caller("Say OK", max_new_tokens=5)
                if resp and len(resp.strip()) > 0:
                    return caller, prov
            except Exception:
                pass
        current_provider_idx = (current_provider_idx + 1) % len(PROVIDER_ORDER)
    raise RuntimeError("No working API providers")


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


# ── ASI Evolve cycle ──────────────────────────────────────────────────────
def asi_cycle(cycle: int, tasks: list, max_tokens: int = 128) -> dict:
    """One cycle of ASI Evolve: eval → distill → improve."""
    print(f"\n{'='*60}")
    print(f"  ASI EVOLVE CYCLE {cycle}")
    print(f"  {datetime.now().strftime('%H:%M:%S')}")
    print(f"{'='*60}\n")

    # Get working provider
    try:
        caller, provider = get_caller()
        print(f"  Provider: {provider}")
    except RuntimeError as e:
        print(f"  ERROR: {e}")
        return {"cycle": cycle, "error": str(e)}

    # 1. EVAL
    print(f"\n  [EVAL] {len(tasks)} tasks...")
    eval_results = []
    for i, task in enumerate(tasks):
        prompt = build_prompt(task)
        t0 = time.time()
        try:
            resp = caller(prompt, max_new_tokens=max_tokens)
            ok = grade(task, resp)
        except Exception:
            resp, ok = "", False
            global current_provider_idx
            current_provider_idx = (current_provider_idx + 1) % len(PROVIDER_ORDER)
        latency = int((time.time() - t0) * 1000)
        eval_results.append({
            "task_id": task.get("id"), "suite": task.get("_suite"),
            "ok": ok, "pred": resp[:300], "latency_ms": latency,
        })
        if (i+1) % 20 == 0:
            ok_count = sum(r["ok"] for r in eval_results)
            print(f"    [{i+1}/{len(tasks)}] ok={ok_count}", flush=True)

    n = len(eval_results)
    ok = sum(r["ok"] for r in eval_results)
    pct = round(ok*100/n, 1) if n else 0
    print(f"  Result: {pct}% ({ok}/{n})")

    # 2. DISTILL (extract from successful responses)
    print(f"\n  [DISTILL] Extracting from successful responses...")
    distilled = []
    for r in eval_results:
        if r["ok"] and r["pred"]:
            task = next((t for t in tasks if t.get("id") == r["task_id"]), None)
            if task:
                distilled.append({
                    "task_id": r["task_id"],
                    "suite": r["suite"],
                    "question": task.get("q", ""),
                    "gold": str(task.get("ans", "")),
                    "teacher_response": r["pred"],
                    "teacher_model": provider,
                })
    print(f"  Distilled: {len(distilled)}")

    # 3. Save
    cycle_result = {
        "cycle": cycle,
        "ts": datetime.now().isoformat(),
        "provider": provider,
        "eval_pct": pct,
        "eval_correct": ok,
        "eval_total": n,
        "distilled_count": len(distilled),
        "results": eval_results,
        "distilled": distilled,
    }

    out = BENCH / f"asi_cycle_{cycle}.json"
    out.write_text(json.dumps(cycle_result, indent=2, default=str))

    distilled_path = TRAINING / f"asi_distilled_{cycle}.jsonl"
    with distilled_path.open("w") as f:
        for d in distilled:
            f.write(json.dumps(d) + "\n")

    print(f"  Saved: {out}")
    print(f"  Distilled: {distilled_path}")

    return cycle_result


# ── Main loop ──────────────────────────────────────────────────────────────
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--hours", type=float, default=8)
    ap.add_argument("--cycles", type=int, default=0)
    ap.add_argument("--tasks", type=int, default=10)
    ap.add_argument("--sleep-between", type=int, default=60)
    args = ap.parse_args()

    end_time = datetime.now() + timedelta(hours=args.hours)

    # Load tasks
    reg = json.loads((BENCH / "task_registry.json").read_text())
    all_tasks = []
    for sname, sdata in reg["suites"].items():
        for t in sdata["tasks"][:args.tasks]:
            t2 = dict(t); t2["_suite"] = sname
            all_tasks.append(t2)
    print(f"Tasks: {len(all_tasks)} | Hours: {args.hours}")

    cycle = 0
    all_cycles = []
    all_distilled = []

    while True:
        cycle += 1
        if args.cycles and cycle > args.cycles:
            break
        if datetime.now() >= end_time:
            break

        result = asi_cycle(cycle, all_tasks)
        all_cycles.append(result)
        all_distilled.extend(result.get("distilled", []))

        # Sleep between cycles (let rate limits reset)
        remaining = (end_time - datetime.now()).total_seconds()
        if remaining > 0 and cycle < (args.cycles or 999):
            sleep_time = min(args.sleep_between, remaining)
            print(f"\n  Sleeping {sleep_time:.0f}s (rate limits)...")
            time.sleep(sleep_time)

    # Summary
    print(f"\n{'='*60}")
    print(f"  ASI EVOLVE COMPLETE — {len(all_cycles)} cycles")
    print(f"{'='*60}")
    print(f"  Total distilled: {len(all_distilled)}")
    if all_cycles:
        pcts = [c.get("eval_pct", 0) for c in all_cycles]
        print(f"  Best eval: {max(pcts):.1f}%")
        print(f"  Last eval: {pcts[-1]:.1f}%")
        print(f"  Eval history: {pcts}")

    summary = {
        "hours": args.hours,
        "cycles": len(all_cycles),
        "total_distilled": len(all_distilled),
        "eval_history": [c.get("eval_pct", 0) for c in all_cycles],
        "best_pct": max((c.get("eval_pct", 0) for c in all_cycles), default=0),
        "final_pct": all_cycles[-1].get("eval_pct", 0) if all_cycles else 0,
    }
    out = BENCH / f"asi_evolve_summary.json"
    out.write_text(json.dumps(summary, indent=2))
    print(f"\n  Summary: {out}")


if __name__ == "__main__":
    main()