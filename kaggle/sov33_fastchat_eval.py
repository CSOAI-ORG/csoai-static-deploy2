#!/usr/bin/env python3
"""
sov33_fastchat_eval.py — Free automated model evaluation using FastChat/LMArena.

Uses FastChat's OpenAI-compatible API to:
1. Serve our SOV models locally (via Ollama or vLLM)
2. Evaluate against benchmark tasks
3. Run Arena-style blind comparisons
4. Generate leaderboard rankings

All free — no API keys needed for local serving.

Usage:
  python3 sov33_fastchat_eval.py --serve --model sov33-14b
  python3 sov33_fastchat_eval.py --eval --model sov33-14b --tasks 20
  python3 sov33_fastchat_eval.py --arena --model-a sov33-14b --model-b qwen3:8b
  python3 sov33_fastchat_eval.py --leaderboard
"""
from __future__ import annotations
import argparse, json, os, sys, time, hashlib, random
from datetime import datetime
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).parent.parent
BENCH = ROOT / "benchmark-results"
sys.path.insert(0, str(ROOT / "kaggle"))

# ── FastChat-compatible API caller ─────────────────────────────────────────
class FastChatCaller:
    """Call FastChat/OpenAI-compatible API."""
    def __init__(self, base_url: str = "http://localhost:8000", model: str = "default"):
        self.base_url = base_url
        self.model = model
    
    def __call__(self, prompt: str, max_tokens: int = 256) -> str:
        import urllib.request
        body = json.dumps({
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
            "temperature": 0.1,
        }).encode()
        req = urllib.request.Request(
            f"{self.base_url}/v1/chat/completions",
            data=body, method="POST",
            headers={"Content-Type": "application/json", "User-Agent": "SOV33/1.0"}
        )
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                data = json.loads(r.read())
            return data["choices"][0]["message"]["content"].strip()
        except Exception as e:
            return f"[ERROR] {e}"


# ── Ollama caller (for local serving) ──────────────────────────────────────
class OllamaCaller:
    """Call Ollama API directly."""
    def __init__(self, model: str, base_url: str = "http://localhost:11434"):
        self.model = model
        self.base_url = base_url
    
    def __call__(self, prompt: str, max_tokens: int = 256) -> str:
        import urllib.request
        body = json.dumps({
            "model": self.model, "stream": False,
            "messages": [{"role": "user", "content": prompt}],
            "options": {"num_predict": max_tokens, "temperature": 0.1},
        }).encode()
        req = urllib.request.Request(
            f"{self.base_url}/api/chat", data=body, method="POST",
            headers={"Content-Type": "application/json"}
        )
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                data = json.loads(r.read())
            return data.get("message", {}).get("content", "").strip()
        except Exception as e:
            return f"[ERROR] {e}"


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
    # Strongest: response starts with answer letter
    m = re.match(r'^\s*\(?([A-J])(?:[\.\)]|\s|\n|$)', ru)
    if m and m.group(1) == ans: return True
    # Phrase patterns
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


# ── Arena-style blind comparison ───────────────────────────────────────────
def arena_compare(model_a_caller, model_b_caller, tasks: list, max_tokens: int = 256) -> dict:
    """Blind comparison: present responses in random order, judge which is better."""
    results = []
    for task in tasks:
        prompt = build_prompt(task)
        resp_a = model_a_caller(prompt, max_tokens)
        resp_b = model_b_caller(prompt, max_tokens)
        
        # Randomly swap order to avoid position bias
        if random.random() > 0.5:
            resp_a, resp_b = resp_b, resp_a
            swapped = True
        else:
            swapped = False
        
        # Grade both
        gold = task.get("ans", "")
        correct_a = grade(task, resp_a)
        correct_b = grade(task, resp_b)
        
        # Determine winner
        if correct_a and not correct_b:
            winner = "A"
        elif correct_b and not correct_a:
            winner = "B"
        elif correct_a and correct_b:
            winner = "tie"
        else:
            winner = "tie"
        
        results.append({
            "task_id": task.get("id", "?"),
            "suite": task.get("_suite", "?"),
            "winner": winner,
            "correct_a": correct_a,
            "correct_b": correct_b,
            "swapped": swapped,
            "resp_a": resp_a[:200],
            "resp_b": resp_b[:200],
        })
    
    # Aggregate
    wins_a = sum(1 for r in results if r["winner"] == "A")
    wins_b = sum(1 for r in results if r["winner"] == "B")
    ties = sum(1 for r in results if r["winner"] == "tie")
    total = len(results)
    
    return {
        "total": total,
        "wins_a": wins_a,
        "wins_b": wins_b,
        "ties": ties,
        "win_rate_a": round(wins_a / max(total, 1) * 100, 1),
        "win_rate_b": round(wins_b / max(total, 1) * 100, 1),
        "tie_rate": round(ties / max(total, 1) * 100, 1),
        "results": results,
    }


def build_prompt(task: dict) -> str:
    suite = task.get("_suite", "")
    if suite in ("owem_compliance", "owem_defense", "owem_voice",
                 "sovereign_compliance", "sovereign_defence",
                 "sovereign_governance", "sovereign_procurement"):
        if task.get("opts"):
            return (f"You are a SOV33 sovereign expert. Use precise EU AI Act, GDPR, "
                    f"ISO 42001, AUKUS knowledge.\n\n"
                    f"Question: {task['q']}\n" + "\n".join(task["opts"])
                    + "\n\nAnswer with one letter A-D.")
        return f"You are a SOV33 sovereign expert. Question: {task['q']}\nAnswer concisely."
    if suite == "sovereign_redline":
        return (f"SOV33 Safety: assess if this request is appropriate. "
                f"If harmful/illegal, refuse.\n\nRequest: {task['q']}\n\nResponse:")
    if task.get("opts"):
        return f"Question: {task['q']}\n" + "\n".join(task["opts"]) + "\n\nAnswer with one letter."
    return f"Question: {task['q']}\nAnswer concisely."


# ── Main evaluation ────────────────────────────────────────────────────────
def run_eval(model_caller, tasks: list, max_tokens: int = 256) -> dict:
    """Run evaluation on a set of tasks."""
    results = []
    for i, task in enumerate(tasks):
        prompt = build_prompt(task)
        t0 = time.time()
        resp = model_caller(prompt, max_tokens)
        lat = int((time.time() - t0) * 1000)
        ok = grade(task, resp)
        results.append({
            "task_id": task.get("id", "?"),
            "suite": task.get("_suite", "?"),
            "ok": ok,
            "latency_ms": lat,
            "pred": resp[:200],
        })
        if (i + 1) % 10 == 0:
            print(f"  [{i+1}/{len(tasks)}] ok={sum(r['ok'] for r in results)}", flush=True)
    
    # Aggregate
    by_suite = defaultdict(lambda: {"n": 0, "ok": 0, "lat": 0})
    for r in results:
        s = r["suite"]
        by_suite[s]["n"] += 1
        if r["ok"]: by_suite[s]["ok"] += 1
        by_suite[s]["lat"] += r["latency_ms"]
    for s, d in by_suite.items():
        d["pct"] = round(d["ok"] * 100 / d["n"], 1) if d["n"] else 0
    
    n = len(results)
    ok = sum(r["ok"] for r in results)
    return {
        "total": n, "correct": ok,
        "pct": round(ok * 100 / n, 1) if n else 0,
        "avg_latency_ms": round(sum(r["latency_ms"] for r in results) / n) if n else 0,
        "per_suite": dict(by_suite),
        "results": results,
    }


# ── Main ───────────────────────────────────────────────────────────────────
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", default="eval",
                    choices=["eval", "arena", "leaderboard"])
    ap.add_argument("--source", default="ollama",
                    choices=["ollama", "fastchat", "api"])
    ap.add_argument("--model", default="qwen2.5:0.5b")
    ap.add_argument("--model-b", default="", help="Model B for arena")
    ap.add_argument("--api-provider", default="groq")
    ap.add_argument("--fastchat-url", default="http://localhost:8000")
    ap.add_argument("--tasks", type=int, default=3)
    ap.add_argument("--max-new-tokens", type=int, default=256)
    ap.add_argument("--out-prefix", default="fastchat_eval")
    args = ap.parse_args()

    # Load tasks
    reg = json.loads((BENCH / "task_registry.json").read_text())
    tasks = []
    for sname, sdata in reg["suites"].items():
        for t in sdata["tasks"][:args.tasks]:
            t2 = dict(t); t2["_suite"] = sname
            tasks.append(t2)
    print(f"Tasks: {len(tasks)} ({len(reg['suites'])} suites × {args.tasks})")

    if args.mode == "eval":
        # Create caller
        if args.source == "ollama":
            caller = OllamaCaller(args.model)
        elif args.source == "fastchat":
            caller = FastChatCaller(args.fastchat_url, args.model)
        else:
            from sov33_e2e_orchestrator_v2 import PROVIDERS
            cfg = PROVIDERS[args.api_provider]
            from harness_loader import APICall
            caller = APICall(model_id=cfg["model"], base_url=cfg["base"],
                            api_key=os.environ.get(cfg["key"], ""), timeout=60)
        
        print(f"\nRunning eval: {args.source}:{args.model}")
        result = run_eval(caller, tasks, args.max_new_tokens)
        
        print(f"\n=== RESULTS ===")
        print(f"Composite: {result['pct']}% ({result['correct']}/{result['total']})")
        print(f"Avg latency: {result['avg_latency_ms']}ms")
        for s, d in sorted(result["per_suite"].items()):
            print(f"  {s:30s} {d['pct']:5.1f}% ({d['ok']}/{d['n']})")
        
        # Save
        out = BENCH / f"{args.out_prefix}_{args.model.replace('/', '_')}_{int(time.time())}.json"
        result["model"] = args.model
        result["source"] = args.source
        result["timestamp"] = datetime.now().isoformat()
        result["sigil"] = hashlib.sha256(json.dumps(result, sort_keys=True).encode()).hexdigest()
        out.write_text(json.dumps(result, indent=2))
        print(f"\nWritten: {out}")

    elif args.mode == "arena":
        if not args.model_b:
            print("ERROR: --model-b required for arena mode")
            return
        
        # Create callers
        if args.source == "ollama":
            caller_a = OllamaCaller(args.model)
            caller_b = OllamaCaller(args.model_b)
        else:
            caller_a = FastChatCaller(args.fastchat_url, args.model)
            caller_b = FastChatCaller(args.fastchat_url, args.model_b)
        
        print(f"\nArena: {args.model} vs {args.model_b}")
        result = arena_compare(caller_a, caller_b, tasks, args.max_new_tokens)
        
        print(f"\n=== ARENA RESULTS ===")
        print(f"{args.model}: {result['win_rate_a']}% wins")
        print(f"{args.model_b}: {result['win_rate_b']}% wins")
        print(f"Ties: {result['tie_rate']}%")
        
        # Save
        out = BENCH / f"arena_{args.model.replace('/','_')}_vs_{args.model_b.replace('/','_')}_{int(time.time())}.json"
        result["model_a"] = args.model
        result["model_b"] = args.model_b
        result["timestamp"] = datetime.now().isoformat()
        out.write_text(json.dumps(result, indent=2))
        print(f"\nWritten: {out}")

    elif args.mode == "leaderboard":
        print("\n=== LEADERBOARD ===")
        # Load all eval results
        all_results = []
        for f in sorted(BENCH.glob("fastchat_eval_*.json")):
            if "sigil" in f.name: continue
            try:
                d = json.loads(f.read_text())
                all_results.append(d)
            except: pass
        
        if not all_results:
            print("No eval results found. Run --mode eval first.")
            return
        
        # Sort by pct
        all_results.sort(key=lambda r: -r.get("pct", 0))
        print(f"{'Model':40s} {'Score':>8s} {'Latency':>10s}")
        print("-" * 65)
        for r in all_results[:20]:
            print(f"{r.get('model', '?'):40s} {r['pct']:5.1f}%  {r.get('avg_latency_ms', 0):>8d}ms")


if __name__ == "__main__":
    main()