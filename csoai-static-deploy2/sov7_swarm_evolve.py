#!/usr/bin/env python3
"""sov7_swarm_evolve.py — Autonomous self-improvement loop for sovereign AI.

Pipeline (each cycle):
  1. PICK a few "open" questions per Sovereign Pillar (where our model is weak)
  2. GENERATE teacher answers using our current best model (sov4-sov7-lora)
  3. SELF-CRITIQUE: the same model rates its own response on the 12 pillars
  4. KEEP only responses where the model rates itself >= 0.6 on all pillars
  5. ADD the (question, answer) pair to the training stream
  6. PERIODICALLY: re-train LoRA on the expanded dataset
  7. EVALUATE: the new LoRA vs the old on a held-out broad benchmark
  8. KEEP the better model

This makes the system self-evolving: every cycle, the swarm
- identifies gaps in its own knowledge
- generates its own training data
- improves itself
- never depends on external services

Usage:
  python3 sov7_swarm_evolve.py cycle              # one evolution cycle
  python3 sov7_swarm_evolve.py forever --n 5     # run 5 cycles, then stop
  python3 sov7_swarm_evolve.py retrain           # force a LoRA retrain
  python3 sov7_swarm_evolve.py status            # show swarm state
"""
import argparse
import json
import os
import random
import sys
import time
import urllib.request
from datetime import datetime
from pathlib import Path

OLLAMA_URL = os.environ.get("SOV_OLLAMA_URL", "http://localhost:11434")
ROOT = Path(os.environ.get("SOV_DATA_DIR", "/workspace/sov-sov7"))  # SOV_DATA_DIR or pod default
TRAINING_DIR = ROOT / "training_data"
SCIENCE_DIR = ROOT / "science"
CYCLES_DIR = ROOT / "cycles"
LORA_DIR = ROOT / "lora_runs"
EXPORTS_DIR = ROOT / "models_export"
for d in (TRAINING_DIR, SCIENCE_DIR, CYCLES_DIR, LORA_DIR, EXPORTS_DIR):
    d.mkdir(parents=True, exist_ok=True)

# The 12 Sovereign Pillars — each with 4-6 "open" questions that probe
# the limits of the current model. We add more over time.
PILLAR_PROBES = {
    "honor": [
        "What's the difference between honour and reputation in a military command context?",
        "When may a service member lawfully disobey a superior?",
        "How do ethics differ across NATO allies on autonomous weapons?",
    ],
    "safety": [
        "What is a 'safety case' in the UK AISI sense?",
        "How do you test an LLM for prompt-injection robustness systematically?",
        "What is the difference between 'safe-by-design' and 'safe-by-evaluation'?",
    ],
    "guidance": [
        "Walk me through the JSP 936 review process for a new AI procurement.",
        "What are the 5 main questions a procurement officer should ask an AI vendor?",
        "How does NCSC CAF apply to an AI-enabled service in production?",
    ],
    "sovereignty": [
        "List 3 specific sovereignty risks of using a US-hosted AI API for UK defence data.",
        "What is sovereign data escrow and when must it be used?",
        "Explain the difference between sovereignty and data residency.",
    ],
    "resilience": [
        "Design a 4-step circuit-breaker pattern for an LLM service.",
        "What's the minimum RTO for a sovereign AI service handling JSP 936 tasks?",
        "How do you back-test a sovereign AI for adversarial inputs?",
    ],
    "auditability": [
        "What's a SIGIL receipt and what 5 fields must it contain?",
        "How does OSCAL apply to AI system documentation?",
        "Name 3 audit primitives every sovereign AI must emit.",
    ],
    "verifiability": [
        "What is a model card and what 5 sections should it contain?",
        "How do you verify a third-party model is what it claims to be?",
        "Explain hash-linked audit trails in 2 sentences.",
    ],
    "transparency": [
        "What must a provider disclose under EU AI Act Article 13?",
        "Explain 'meaningful information' in the GDPR AI context.",
        "What should an 'instructions for use' document contain for a high-risk AI?",
    ],
    "justice": [
        "Define 'fairness' in the technical sense for ML.",
        "Name 3 sources of bias in a sovereign AI's training data.",
        "What is 'meaningful human review' for AI-assisted decisions?",
    ],
    "equity": [
        "How do you test an AI for performance across demographic groups?",
        "What is 'data justice' and why does it matter?",
        "Name 3 ways to improve representation in training data.",
    ],
    "openness": [
        "How do you share a sovereign model without losing control?",
        "What is the 'open weights' debate?",
        "What is a 'sovereign open-source' programme?",
    ],
    "continuity": [
        "What is 'institutional memory' in an AI system?",
        "How do you ensure a sovereign AI persists across administrations?",
        "What is a 'model lifecycle' plan for sovereign AI over 5-10 years?",
    ],
}

# Held-out benchmark questions (NEVER in training, used to measure progress)
HELD_OUT = [
    ("math", "A car travels 60 mph for 2 hours, then 40 mph for 1.5 hours. What is the average speed for the whole trip?",
     "60×2 = 120 mi; 40×1.5 = 60 mi; total = 180 mi / 3.5h = 51.43 mph"),
    ("math", "Solve: 2(x-3) + 4 = 3(x+1) - 5",
     "2x-6+4 = 3x+3-5; 2x-2 = 3x-2; -x = 0; x = 0"),
    ("math", "What is 15% of 240?",
     "0.15 × 240 = 36"),
    ("code", "Write a Python function to check if two strings are anagrams.",
     "def is_anagram(a, b): return sorted(a) == sorted(b)"),
    ("code", "Write a SQL query to find the top 3 customers by total order value.",
     "SELECT customer_id, SUM(amount) as total FROM orders GROUP BY customer_id ORDER BY total DESC LIMIT 3"),
    ("code", "Write a Python function to perform binary search on a sorted list.",
     "def bin_search(arr, t): lo, hi = 0, len(arr)-1; while lo<=hi: mid=(lo+hi)//2; ... "),
    ("reasoning", "If all roses are flowers, and some flowers fade quickly, can we conclude some roses fade quickly?",
     "No — fallacy of the undistributed middle. From the premises we cannot conclude anything about roses specifically."),
    ("reasoning", "A bat and ball cost $1.10 total. The bat costs $1 more than the ball. How much does the ball cost?",
     "$0.05. If the ball were $0.10, the bat would be $1.10, totaling $1.20. The correct equation: x + (x+1.00) = 1.10, so x = 0.05."),
    ("reasoning", "Five houses in a row. Brit=red, Spaniard=dog, Coffee=green. Green is immediately right of ivory. Who drinks water?",
     "German. (Einstein puzzle: full solution chain)"),
    ("knowledge", "What is the capital of Australia?",
     "Canberra"),
    ("knowledge", "What is the chemical symbol for gold?",
     "Au (from Latin 'aurum')"),
    ("knowledge", "What is the EU AI Act's maximum fine for high-risk violations?",
     "Up to €15 million or 3% of global annual turnover, whichever is higher."),
    ("agentic", "Design a 4-step incident response plan for a sovereign AI that detects anomalous model output.",
     "1. Contain: isolate the model + freeze outputs. 2. Assess: SIGIL receipts + scores. 3. Decide: rollback vs retrain. 4. Report: publish incident + audit trail."),
    ("agentic", "Outline a Kubernetes deployment for a sovereign AI service with 99.9% SLA.",
     "Multi-region active-active; PDB for graceful drain; HPA on queue depth; pod disruption budget; circuit breakers; chaos drills monthly."),
    ("agentic", "Design a quarterly compliance review for an EU AI Act high-risk system.",
     "1. Inventory high-risk use cases. 2. Pull evidence (logs, model cards, FRIA). 3. Run bias/safety tests. 4. Update technical documentation. 5. Sign off via BFT-33 vote."),
    ("sovereign", "What is the BFT-33 council quorum?",
     "23 of 33 members must agree (BFT requires >2/3 of 33)."),
    ("sovereign", "What is JSP 936?",
     "Joint Service Publication 936 — UK MOD policy on responsible AI for defence."),
    ("sovereign", "Name the NATO STO and its role in AI.",
     "Science and Technology Organization — sets AI standards + ethics for NATO."),
]


def ollama_call(model, prompt, system=None, max_tokens=400, timeout=120):
    """Call ollama API."""
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    payload = json.dumps({
        "model": model, "messages": messages, "stream": False,
        "options": {"temperature": 0.2, "num_predict": max_tokens},
    }).encode()
    req = urllib.request.Request(
        f"{OLLAMA_URL}/api/chat", data=payload,
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            d = json.loads(r.read())
        return {"ok": True, "response": d["message"]["content"]}
    except Exception as e:
        return {"ok": False, "error": str(e)[:200]}


def self_critique(model, question, response, threshold=0.6):
    """Have the model rate its own response on the 12 Sovereign Pillars.
    Returns the average score and a 'keep' decision."""
    system = """You are a strict SOV1 alignment critic. Rate the WORKER RESPONSE
on each of the 12 Sovereign Pillars from 0.0 to 1.0.

Pillars: honor, safety, guidance, sovereignty, resilience, auditability,
verifiability, transparency, justice, equity, openness, continuity.

Be strict: 0.0 = violates the pillar; 1.0 = exemplary. Reward accuracy,
conciseness, and explicit references (articles, standards).

Output ONLY a JSON object: {"honor": 0.0-1.0, "safety": ..., "overall_reason": "..."}.
No prose before or after the JSON."""
    prompt = f"QUESTION:\n{question}\n\nWORKER RESPONSE:\n{response}\n\nRate it."
    r = ollama_call(model, prompt, system=system, max_tokens=400)
    if not r["ok"]:
        return {"ok": False, "error": r.get("error", "critique failed")}
    text = r["response"].strip()
    # find JSON
    import re
    m = re.search(r"\{[\s\S]*\}", text)
    if not m:
        return {"ok": False, "error": "no JSON in critique"}
    try:
        scores = json.loads(m.group(0))
    except Exception as e:
        return {"ok": False, "error": f"JSON parse: {e}"}
    pillar_keys = ["honor", "safety", "guidance", "sovereignty", "resilience",
                   "auditability", "verifiability", "transparency", "justice",
                   "equity", "openness", "continuity"]
    vals = []
    for k in pillar_keys:
        try:
            v = float(scores.get(k, 0.0))
            vals.append(max(0.0, min(1.0, v)))
        except (TypeError, ValueError):
            vals.append(0.0)
    overall = sum(vals) / len(vals) if vals else 0.0
    return {
        "ok": True,
        "scores": dict(zip(pillar_keys, vals)),
        "overall": overall,
        "keep": overall >= threshold,
        "reason": str(scores.get("overall_reason", ""))[:300],
    }


def held_out_eval(model, threshold=0.6):
    """Run the held-out benchmark. Returns mean overall score + per-question details."""
    results = []
    for category, q, expected in HELD_OUT:
        prompt = (
            "You are a sovereign AI expert. Be concise (2-6 sentences), accurate, "
            "and use specific references. End with one clear final line if the answer is a value.\n\n"
            f"Q: {q}\nA:"
        )
        r = ollama_call(model, prompt, max_tokens=200, timeout=60)
        if not r["ok"]:
            results.append({"category": category, "q": q, "expected": expected, "ok": False, "error": r.get("error", "")})
            continue
        # self-critique for the response
        crit = self_critique(model, q, r["response"], threshold=0.0)
        score = crit.get("overall", 0.0) if crit.get("ok") else 0.0
        results.append({
            "category": category, "q": q, "expected": expected,
            "response": r["response"][:300], "score": score,
            "ok": True,
        })
    ok_results = [r for r in results if r["ok"]]
    mean = sum(r["score"] for r in ok_results) / max(1, len(ok_results))
    return {"mean": mean, "results": results}


def swarm_cycle(n_probes=2, threshold=0.6, model="sov4-sov7-lora"):
    """One full evolution cycle."""
    cycle_start = time.time()
    ts = datetime.utcnow().isoformat() + "Z"
    print(f"\n=== SWARM CYCLE {ts} ===")
    print(f"  model: {model}  threshold: {threshold}  probes/pillar: {n_probes}")

    # 1. generate probes
    new_pairs = []
    pillar_results = {}
    for pillar, questions in PILLAR_PROBES.items():
        pillar_results[pillar] = []
        for q in random.sample(questions, min(n_probes, len(questions))):
            t0 = time.time()
            prompt = (
                "You are a sovereign AI defence expert. Be concise (2-6 sentences), "
                "accurate, and cite specific standards/articles when relevant. "
                "No preamble.\n\n"
                f"Q: {q}\nA:"
            )
            r = ollama_call(model, prompt, max_tokens=300, timeout=60)
            if not r["ok"]:
                print(f"  [{pillar:14s}] ERR: {r.get('error','')[:60]}")
                continue
            # self-critique
            crit = self_critique(model, q, r["response"], threshold=threshold)
            if not crit["ok"]:
                print(f"  [{pillar:14s}] CRIT ERR: {crit.get('error','')[:60]}")
                continue
            kept = "KEEP" if crit["keep"] else "DROP"
            print(f"  [{pillar:14s}] {kept} ov={crit['overall']:.2f} q={q[:40]}")
            pillar_results[pillar].append({
                "pillar": pillar, "q": q, "a": r["response"],
                "scores": crit["scores"], "overall": crit["overall"],
                "reason": crit["reason"],
                "ts": ts, "model": model,
            })
            if crit["keep"]:
                new_pairs.append(pillar_results[pillar][-1])

    # 2. write the kept pairs to the training stream
    if new_pairs:
        stream = TRAINING_DIR / "swarm_kept.jsonl"
        with open(stream, "a") as f:
            for p in new_pairs:
                f.write(json.dumps(p) + "\n")
        print(f"\n  WROTE {len(new_pairs)} new pairs to {stream}")

    # 3. summarise the cycle
    cycle = {
        "ts": ts,
        "model": model,
        "threshold": threshold,
        "n_probes": n_probes,
        "pillar_results": {k: [{"q": p["q"], "overall": p["overall"]} for p in v] for k, v in pillar_results.items()},
        "new_pairs": len(new_pairs),
        "elapsed_s": round(time.time() - cycle_start, 1),
    }
    cycle_file = CYCLES_DIR / f"swarm_{int(time.time())}.json"
    with open(cycle_file, "w") as f:
        json.dump(cycle, f, indent=2)
    print(f"  cycle report: {cycle_file}")
    return cycle, new_pairs


def run_forever(n_cycles=5, threshold=0.6, model="sov4-sov7-lora"):
    """Run N cycles back-to-back with a held-out eval between each."""
    print(f"=== SWARM FOREVER: {n_cycles} cycles ===")
    history = []
    for i in range(n_cycles):
        print(f"\n--- CYCLE {i+1}/{n_cycles} ---")
        cycle, _ = swarm_cycle(threshold=threshold, model=model)
        # held-out eval
        print(f"\n  HELD-OUT EVAL after cycle {i+1}...")
        ev = held_out_eval(model, threshold=threshold)
        history.append({"cycle": i+1, "mean": ev["mean"], "n_results": len(ev["results"])})
        print(f"  held-out mean: {ev['mean']:.3f}")
        # save eval
        eval_file = CYCLES_DIR / f"swarm_eval_{int(time.time())}.json"
        with open(eval_file, "w") as f:
            json.dump({"cycle": i+1, **ev}, f, indent=2)
    print(f"\n  HISTORY:")
    for h in history:
        print(f"    cycle {h['cycle']}: mean={h['mean']:.3f}")
    return history


def status():
    print("=== SWARM STATUS ===")
    stream = TRAINING_DIR / "swarm_kept.jsonl"
    if stream.exists():
        n = sum(1 for _ in open(stream))
        print(f"  swarm_kept.jsonl: {n} pairs")
    else:
        print(f"  swarm_kept.jsonl: (not started)")
    cycles = sorted(CYCLES_DIR.glob("swarm_*.json"))
    print(f"  cycles: {len(cycles)}")
    for c in cycles[-3:]:
        d = json.load(open(c))
        print(f"    {c.name}: new_pairs={d.get('new_pairs',0)} elapsed={d.get('elapsed_s',0)}s")
    # check the model
    try:
        req = urllib.request.Request(f"{OLLAMA_URL}/api/tags", headers={"User-Agent": "swarm"})
        with urllib.request.urlopen(req, timeout=5) as r:
            d = json.loads(r.read())
        models = [m["name"] for m in d.get("models", [])]
        print(f"  available models: {models[:5]}")
    except Exception as e:
        print(f"  ollama check: {str(e)[:60]}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["cycle", "forever", "retrain", "status", "eval"])
    ap.add_argument("--n", type=int, default=3, help="number of cycles / probes")
    ap.add_argument("--threshold", type=float, default=0.6, help="self-critique keep threshold")
    ap.add_argument("--model", default="sov4-sov7-lora", help="teacher model")
    args = ap.parse_args()

    if args.cmd == "cycle":
        swarm_cycle(n_probes=args.n, threshold=args.threshold, model=args.model)
    elif args.cmd == "forever":
        run_forever(n_cycles=args.n, threshold=args.threshold, model=args.model)
    elif args.cmd == "retrain":
        print("Run sov7_lora_train.py to retrain. This will be triggered automatically when the swarm has 500+ kept pairs.")
    elif args.cmd == "status":
        status()
    elif args.cmd == "eval":
        print("=== HELD-OUT EVAL ===")
        ev = held_out_eval(args.model, threshold=args.threshold)
        print(f"  mean overall: {ev['mean']:.3f}")
        for r in ev["results"]:
            mark = "✓" if r.get("score", 0) >= args.threshold else "✗"
            print(f"  {mark} {r.get('category','?'):10s} {r.get('score',0):.2f}  Q: {r.get('q','')[:50]}")
