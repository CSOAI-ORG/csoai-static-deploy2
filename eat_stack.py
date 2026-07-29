#!/usr/bin/env python3
"""eat_stack.py — THE 'eat all' ENTRYPOINT. Runs the whole EAT stack offline, $0.

Suites:
  1. GOVBENCH   (govbench_eval.py)     — 15 behavioural dims: refusal, jailbreak, bias, knowledge + SIGIL
  2. COMPBENCH  (compbench_local.py)   — 110 capability tasks across 8 categories (Open-LLM-v2 style)
  3. EAT weak-dim (eat_run_local.py)   — baseline vs RAG-context lift on the 5 weak governance dims

All local Ollama. No cloud key. Writes a combined, hash-signed leaderboard.

  python3 eat_stack.py                       # default model set
  python3 eat_stack.py sov33-v7:latest ...   # explicit models
"""
import hashlib, json, subprocess, sys, time
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).parent
OUT = HERE / "benchmark-results" / "eat_stack"; OUT.mkdir(parents=True, exist_ok=True)
DEFAULT_MODELS = ["sov33-v7:latest", "sov-sovereign-v4:latest"]

def sh(cmd, timeout=3600):
    t0 = time.time()
    p = subprocess.run(cmd, cwd=HERE, capture_output=True, text=True, timeout=timeout)
    return {"cmd": " ".join(cmd), "rc": p.returncode, "secs": round(time.time()-t0, 1),
            "stdout": p.stdout[-4000:], "stderr": p.stderr[-1500:]}

def latest_json(pattern):
    hits = sorted(OUT.parent.glob(pattern), key=lambda p: p.stat().st_mtime, reverse=True)
    if not hits: return None
    try: return json.loads(hits[0].read_text())
    except Exception: return None

def sigil(obj):
    """Deterministic content hash over the result set (the estate's SIGIL convention)."""
    return hashlib.sha256(json.dumps(obj, sort_keys=True, default=str).encode()).hexdigest()

def main():
    models = [a for a in sys.argv[1:] if not a.startswith("--")] or DEFAULT_MODELS
    print("=" * 70); print(f"  EAT STACK — {len(models)} model(s), offline, $0"); print("=" * 70)
    runs, per_model = [], {}

    for m in models:
        print(f"\n### {m}")
        print("  [1/3] CompBench (110 capability tasks) ...")
        runs.append(sh([sys.executable, "compbench_local.py", m]))
        print("  [2/3] EAT weak-dimension (baseline vs RAG) ...")
        runs.append(sh([sys.executable, "eat_run_local.py", m]))
        print("  [3/3] GovBench (15 behavioural dims + SIGIL) ...")
        runs.append(sh([sys.executable, "govbench_eval.py", "--model", m, "--provider", "ollama"]))

        safe = m.replace(":", "_").replace("/", "_")
        comp = latest_json(f"compbench/compbench_{safe}_neutral.json")
        eat  = latest_json(f"eat_govbench/eat_local_{safe}.json")
        per_model[m] = {
            "compbench_composite": (comp or {}).get("composite"),
            "compbench_categories": (comp or {}).get("categories"),
            "eat_baseline": (eat or {}).get("avg_baseline"),
            "eat_context": (eat or {}).get("avg_context"),
            "eat_rag_lift": (round((eat["avg_context"] - eat["avg_baseline"]), 1)
                             if eat and eat.get("avg_context") is not None else None),
        }

    report = {"timestamp": datetime.now(timezone.utc).isoformat(),
              "backend": "ollama-local", "cost_usd": 0.0,
              "models": per_model, "runs": runs}
    report["sigil"] = sigil(report["models"])
    fp = OUT / "eat_stack_report.json"; fp.write_text(json.dumps(report, indent=2))

    print("\n" + "=" * 70); print("  EAT STACK — COMBINED LEADERBOARD"); print("=" * 70)
    print(f"  {'model':26s} {'CompBench':>10s} {'EAT base':>9s} {'EAT ctx':>8s} {'RAG lift':>9s}")
    for m, r in sorted(per_model.items(), key=lambda kv: -(kv[1]["compbench_composite"] or 0)):
        f = lambda v, s="%5.1f": (s % v) if isinstance(v, (int, float)) else "   n/a"
        print(f"  {m:26s} {f(r['compbench_composite']):>10s} {f(r['eat_baseline']):>9s} "
              f"{f(r['eat_context']):>8s} {f(r['eat_rag_lift'],'%+5.1f'):>9s}")
    print("=" * 70)
    print(f"  SIGIL: {report['sigil'][:32]}...")
    print(f"  -> {fp}")

if __name__ == "__main__":
    main()
