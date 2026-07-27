#!/usr/bin/env python3
"""sov7_catalog.py — Comprehensive catalog + benchmark of all sovereign models.

Tests each model on:
  - 4 math questions (correctness)
  - 4 code questions (correctness)
  - 4 reasoning questions (logic)
  - 4 knowledge questions (EU AI Act, GDPR, etc)
  - 4 agentic questions (planning)
  - 1 BFT-33 / 1 JSP-936 (signature sovereignty tests)
  - 1 each per pillar (sovereign specialty)

Outputs a comparison table showing which model wins per category.
"""
import json
import os
import subprocess
import time
import urllib.request
from pathlib import Path

OLLAMA_URL = os.environ.get("SOV_OLLAMA_URL", "http://localhost:11434")
OUT = Path("/workspace/sov-sov7/catalog")
OUT.mkdir(parents=True, exist_ok=True)

BENCH = {
    "math": [
        ("What is 7 times 8?", "56"),
        ("If a train travels 60 mph for 2.5 hours, how far does it go?", "150"),
        ("What is 15% of 240?", "36"),
        ("Solve: 2x + 5 = 17", "6"),
    ],
    "code": [
        ("Write a Python function to check if a string is a palindrome.", "s == s[::-1]"),
        ("Write a Python function to compute the factorial of n.", "factorial"),
        ("Write a SQL query to find the top 3 customers by total order value.", "ORDER BY"),
        ("Write a Python function to compute the Fibonacci sequence.", "fib"),
    ],
    "reasoning": [
        ("If all roses are flowers, and some flowers fade, can we conclude some roses fade? (yes/no)", "no"),
        ("A bat and ball cost $1.10. The bat is $1 more than the ball. What does the ball cost?", "5"),
        ("How many times do the hour and minute hands of a clock overlap in 12 hours?", "11"),
        ("If 5 machines make 5 widgets in 5 minutes, how long for 100 machines to make 100 widgets?", "5"),
    ],
    "knowledge": [
        ("What is the EU AI Act Article 50 deadline?", "2 august 2026"),
        ("What is GDPR Article 83 max fine?", "20 million"),
        ("What is the BFT-33 council quorum?", "23"),
        ("What is JSP 936?", "Joint Service Publication"),
    ],
    "agentic": [
        ("List 3 steps for incident response for anomalous AI output.", "contain"),
        ("Outline a Kubernetes deployment for 99.9% SLA.", "autoscaling"),
        ("Plan a quarterly compliance review for EU AI Act high-risk.", "bias"),
        ("Design a circuit-breaker pattern for an LLM service.", "failure"),
    ],
}

PILLAR_TESTS = {
    "honor": "What's the difference between honour and reputation in a military command context?",
    "safety": "What is a 'safety case' in the UK AISI sense?",
    "guidance": "Walk through the JSP 936 review process for a new AI procurement.",
    "sovereignty": "List 3 specific sovereignty risks of using a US-hosted AI API for UK defence data.",
    "resilience": "Design a 4-step circuit-breaker pattern for an LLM service.",
    "auditability": "What is a SIGIL receipt and what 5 fields must it contain?",
    "verifiability": "What is a model card and what 5 sections should it contain?",
    "transparency": "What must a provider disclose under EU AI Act Article 13?",
    "justice": "Define 'fairness' in the technical sense for ML.",
    "equity": "How do you test an AI for performance across demographic groups?",
    "openness": "How do you share a sovereign model without losing control?",
    "continuity": "What is 'institutional memory' in an AI system?",
}


def call_ollama(model, prompt, max_tokens=300, timeout=60):
    payload = json.dumps({"model": model, "prompt": prompt, "stream": False,
                          "options": {"temperature": 0, "num_predict": max_tokens}}).encode()
    req = urllib.request.Request(f"{OLLAMA_URL}/api/generate", data=payload,
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            d = json.loads(r.read())
        return d.get("response", "").strip()
    except Exception as e:
        return f"ERR: {str(e)[:100]}"


def score(category, response, expected):
    """Simple contains-based scoring."""
    if response.startswith("ERR:"):
        return 0.0
    r = response.lower()
    e = expected.lower()
    return 1.0 if e in r else 0.0


def get_models():
    """Get all available models."""
    payload = json.dumps({}).encode()
    req = urllib.request.Request(f"{OLLAMA_URL}/api/tags",
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=5) as r:
            d = json.loads(r.read())
        return [m["name"].split(":")[0] for m in d.get("models", [])]
    except Exception:
        return []


def main():
    models = get_models()
    print(f"=== CATALOG BENCHMARK ===")
    print(f"  ollama: {OLLAMA_URL}")
    print(f"  models: {len(models)}")
    for m in models:
        print(f"    - {m}")

    # results[model][category] = [scores]
    results = {m: {c: [] for c in list(BENCH.keys()) + ["pillar_specific"]} for m in models}

    for model in models:
        print(f"\n--- testing {model} ---")
        for cat, qs in BENCH.items():
            for q, expected in qs:
                t0 = time.time()
                resp = call_ollama(model, q)
                s = score(cat, resp, expected)
                elapsed = time.time() - t0
                results[model][cat].append(s)
                marker = "✓" if s == 1.0 else "✗"
                print(f"  {cat:10s} {marker} ov={s:.0f} ({elapsed:.0f}s) Q: {q[:40]}")
        # pillar-specific
        for pillar, q in PILLAR_TESTS.items():
            resp = call_ollama(model, q, max_tokens=200)
            # soft score: 1.0 if response is non-empty and non-ERR
            if resp.startswith("ERR:") or len(resp) < 5:
                s = 0.0
            else:
                s = 0.5  # baseline
            results[model]["pillar_specific"].append(s)

    # save
    out_file = OUT / f"catalog_{int(time.time())}.json"
    with open(out_file, "w") as f:
        json.dump({"models": models, "results": results, "bench": BENCH,
                   "pillar_tests": PILLAR_TESTS}, f, indent=2)

    # print summary
    print(f"\n{'='*80}")
    print(f"  FINAL LEADERBOARD (mean score per category, 0-1)")
    print(f"{'='*80}")
    print(f"  {'MODEL':28s}  {'math':5s} {'code':5s} {'reas':5s} {'know':5s} {'agnt':5s} {'pilla':5s}  {'AVG':5s}")
    print(f"  {'-'*28}  {'-'*5} {'-'*5} {'-'*5} {'-'*5} {'-'*5} {'-'*5}  {'-'*5}")
    leaderboard = []
    for model in models:
        cats = results[model]
        means = {c: (sum(s)/len(s)) if s else 0 for c, s in cats.items()}
        avg = sum(means.values()) / len(means)
        leaderboard.append((model, avg, means))
    leaderboard.sort(key=lambda x: -x[1])
    for model, avg, means in leaderboard:
        print(f"  {model:28s}  {means['math']:.2f}  {means['code']:.2f}  {means['reasoning']:.2f}  {means['knowledge']:.2f}  {means['agentic']:.2f}  {means['pillar_specific']:.2f}  {avg:.2f}")

    # save leaderboard
    lb_file = OUT / f"leaderboard_{int(time.time())}.md"
    with open(lb_file, "w") as f:
        f.write("# SOV7 Catalog Leaderboard\n\n")
        f.write(f"  ollama: {OLLAMA_URL}\n")
        f.write(f"  models tested: {len(models)}\n")
        f.write(f"  benchmark: math/code/reasoning/knowledge/agentic (4 each) + 12 pillar probes\n\n")
        f.write("| Model | Math | Code | Reas | Know | Agnt | Pillar | AVG |\n")
        f.write("|---|---|---|---|---|---|---|---|\n")
        for model, avg, means in leaderboard:
            f.write(f"| {model} | {means['math']:.2f} | {means['code']:.2f} | {means['reasoning']:.2f} | {means['knowledge']:.2f} | {means['agentic']:.2f} | {means['pillar_specific']:.2f} | **{avg:.2f}** |\n")
    print(f"\n  saved: {out_file}")
    print(f"  saved: {lb_file}")


if __name__ == "__main__":
    main()
