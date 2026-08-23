#!/usr/bin/env python3
"""compbench_local.py — CompBench: the capability half of the EAT stack, run OFFLINE.

Reuses the 110-task bank + graders already in benchmark-results/comprehensive_e2e.py
(math, reasoning, coding, governance, agentic, general, truthful, instruction) but fixes
TWO things that made the original unusable as a benchmark:

  1. It called NVIDIA/Gemini — both keys are dead. -> routed to LOCAL Ollama ($0, offline).
  2. Its SYSTEM prompt LEAKED THE ANSWERS ("15% of 200 = 30", "next is 36", "Ball=$0.05").
     Grading a model on answers you handed it measures nothing. -> neutral system prompt.

Usage:
  python3 compbench_local.py sov33-v7:latest [more models...]
  python3 compbench_local.py --leak-test sov33-v7:latest   # A/B: neutral vs answer-leaking prompt
"""
import json, re, sys, time, urllib.request
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "benchmark-results"))

# Import the task bank + graders WITHOUT executing the module's API-key/network code:
# comprehensive_e2e defines TASKS/ck/cn/strip_think at import time and only calls out under __main__.
import comprehensive_e2e as CE
TASKS = CE.TASKS

NEUTRAL_SYSTEM = "You are a helpful assistant. Answer precisely and concisely."
OLLAMA = "http://localhost:11434/api/chat"
RESULTS_DIR = Path("benchmark-results/compbench"); RESULTS_DIR.mkdir(parents=True, exist_ok=True)

def call(model, prompt, system=NEUTRAL_SYSTEM, timeout=120):
    body = json.dumps({
        "model": model, "stream": False,
        "options": {"temperature": 0, "num_predict": 256},
        "messages": [{"role": "system", "content": system},
                     {"role": "user", "content": prompt}],
    }).encode()
    req = urllib.request.Request(OLLAMA, data=body, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read())["message"]["content"]
    except Exception:
        return ""

def run(model, system=NEUTRAL_SYSTEM, label="neutral"):
    print("=" * 66); print(f"  COMPBENCH (offline) — {model}  [{label} prompt]"); print("=" * 66)
    cats, t0 = {}, time.time()
    for t in TASKS:
        cat = t["cat"]
        resp = call(model, t["q"], system)
        try:
            ok = bool(t["c"](resp))
        except Exception:
            ok = False
        d = cats.setdefault(cat, {"correct": 0, "total": 0})
        d["correct"] += int(ok); d["total"] += 1

    out_cats, tot_c, tot_n = {}, 0, 0
    for cat, d in sorted(cats.items()):
        pct = d["correct"] / d["total"] * 100
        out_cats[cat] = {"correct": d["correct"], "total": d["total"], "pct": round(pct, 1)}
        tot_c += d["correct"]; tot_n += d["total"]
        print(f"  {cat:14s} {d['correct']:3d}/{d['total']:<3d}  {pct:5.1f}%")
    composite = tot_c / tot_n * 100
    print("-" * 66)
    print(f"  {'COMPOSITE':14s} {tot_c:3d}/{tot_n:<3d}  {composite:5.1f}%   ({time.time()-t0:.0f}s)")

    out = {"timestamp": datetime.now(timezone.utc).isoformat(), "model": model,
           "backend": "ollama-local", "prompt_mode": label,
           "categories": out_cats, "composite": round(composite, 1),
           "correct": tot_c, "total": tot_n}
    fp = RESULTS_DIR / f"compbench_{model.replace(':','_').replace('/','_')}_{label}.json"
    fp.write_text(json.dumps(out, indent=2)); print(f"  -> {fp}")
    return out

if __name__ == "__main__":
    args = sys.argv[1:]
    leak_test = "--leak-test" in args
    models = [a for a in args if not a.startswith("--")] or ["sov33-v7:latest"]
    results = []
    for m in models:
        results.append(run(m))
        if leak_test:
            # A/B the contaminated prompt to QUANTIFY the leak (honesty check, not a score to publish)
            leaked = run(m, system=CE.SYSTEM, label="answer-leaking")
            delta = leaked["composite"] - results[-1]["composite"]
            print(f"\n  ⚠ LEAK DELTA for {m}: {delta:+.1f} pts from the answer-carrying system prompt")
    if len(results) > 1:
        print("\n=== COMPBENCH LEADERBOARD (neutral prompt) ===")
        for r in sorted(results, key=lambda x: -x["composite"]):
            print(f"  {r['model']:26s} {r['composite']:5.1f}%")
