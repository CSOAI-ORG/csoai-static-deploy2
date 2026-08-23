#!/usr/bin/env python3
"""
Benchmark all Ollama models (sov*/qwen*) against reasoning, math, code, and sovereign corpora.
Uses only stdlib (urllib, json, time, random, sys).
"""

import json
import time
import random
import sys
import urllib.request
import urllib.error
from pathlib import Path

OLLAMA_URL = "http://localhost:11434/api/generate"
TAGS_URL = "http://localhost:11434/api/tags"
CORPUS_PATH = Path(__file__).parent / "reasoning_corpus_5k.jsonl"
RESULTS_PATH = Path(__file__).parent / "benchmark_results.json"
TIMEOUT = 30

# ── Test sets ────────────────────────────────────────────────────────────────

MATH_SAMPLES = [
    {"q": "What is 847 + 263?", "expected_keywords": ["1110"]},
    {"q": "Solve for x: 3x + 7 = 22", "expected_keywords": ["5"]},
    {"q": "What is 15% of 240?", "expected_keywords": ["36"]},
    {"q": "Simplify: (2^3 * 2^4) / 2^5", "expected_keywords": ["4", "2^2"]},
    {"q": "What is the derivative of x^3 + 2x?", "expected_keywords": ["3x^2", "3x²", "3 x^2", "3x**2"]},
]

CODE_SAMPLES = [
    {"q": "Write a Python function `fibonacci(n)` that returns the nth Fibonacci number.", "expected_keywords": ["def fibonacci", "return"]},
    {"q": "Write a Python function `is_palindrome(s)` that checks if a string is a palindrome.", "expected_keywords": ["def is_palindrome", "return"]},
    {"q": "Write a Python function `flatten(lst)` that flattens a nested list.", "expected_keywords": ["def flatten", "return"]},
    {"q": "Write a Python function `binary_search(arr, target)` that returns the index of target or -1.", "expected_keywords": ["def binary_search", "return"]},
    {"q": "Write a Python function `merge_sort(arr)` that sorts a list using merge sort.", "expected_keywords": ["def merge_sort", "return"]},
]

SOVEREIGN_SAMPLES = [
    {"q": "What are the risk categories defined by the EU AI Act?", "expected_keywords": ["prohibited", "high-risk", "limited", "minimal"]},
    {"q": "Under the EU AI Act, what are the obligations for high-risk AI systems?", "expected_keywords": ["risk management", "data governance", "transparency", "logging", "human oversight"]},
    {"q": "What is the EU AI Act's stance on biometric identification in public spaces?", "expected_keywords": ["prohibited", "real-time", "remote", "biometric"]},
    {"q": "What penalties can be imposed under the EU AI Act for non-compliance?", "expected_keywords": ["fine", "million", "turnover", "percent", "35"]},
    {"q": "How does the EU AI Act define an AI system?", "expected_keywords": ["machine", "learn", "autonomous", "adapt", "infer", "output"]},
]


def load_reasoning_samples(n=10):
    """Load n random samples from the reasoning corpus."""
    samples = []
    with open(CORPUS_PATH, "r") as f:
        lines = f.readlines()
    random.seed(42)
    chosen = random.sample(lines, min(n, len(lines)))
    for line in chosen:
        obj = json.loads(line)
        q = obj.get("q", "")
        a = obj.get("a", "")
        # Use first 80 chars of answer as expected keyword source
        keywords = [w for w in a[:200].split() if len(w) > 4][:5]
        samples.append({"q": q, "expected_keywords": keywords})
    return samples


def query_ollama(model, prompt, timeout=TIMEOUT):
    """Send a generate request to Ollama. Returns (response_text, elapsed_sec) or (None, elapsed_sec)."""
    payload = json.dumps({
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.2, "num_predict": 512},
    }).encode()

    req = urllib.request.Request(
        OLLAMA_URL,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = json.loads(resp.read().decode())
            text = body.get("response", "")
            elapsed = time.time() - t0
            return text, elapsed
    except (urllib.error.URLError, TimeoutError, OSError, json.JSONDecodeError) as e:
        elapsed = time.time() - t0
        return None, elapsed


def score_response(text, expected_keywords):
    """Simple quality score: fraction of expected keywords found + length bonus."""
    if not text:
        return 0.0
    text_lower = text.lower()
    hits = sum(1 for kw in expected_keywords if kw.lower() in text_lower)
    keyword_score = hits / max(len(expected_keywords), 1)
    length_bonus = min(len(text) / 500, 1.0) * 0.2  # up to 0.2 for length
    return round(min(keyword_score + length_bonus, 1.0), 3)


def run_benchmark(model, samples, category_name, progress_prefix=""):
    """Run benchmark for one category. Returns list of result dicts."""
    results = []
    for i, sample in enumerate(samples):
        prompt = sample["q"]
        print(f"  {progress_prefix}[{i+1}/{len(samples)}] {prompt[:72]}...", end="", flush=True)
        text, elapsed = query_ollama(model, prompt)
        if text is None:
            score = 0.0
            print(f" TIMEOUT ({elapsed:.1f}s)")
        else:
            score = score_response(text, sample["expected_keywords"])
            print(f" {elapsed:.1f}s  score={score:.3f}  len={len(text)}")
        results.append({
            "question": prompt[:120],
            "time_sec": round(elapsed, 2),
            "score": score,
            "response_length": len(text) if text else 0,
            "response_preview": (text or "")[:200],
        })
    return results


def main():
    print("=" * 78)
    print("  OLLAMA MODEL BENCHMARK — sov/qwen models")
    print("=" * 78)

    # ── 1. List models ───────────────────────────────────────────────────────
    try:
        with urllib.request.urlopen(TAGS_URL, timeout=5) as resp:
            all_models = [m["name"] for m in json.loads(resp.read().decode()).get("models", [])]
    except Exception as e:
        print(f"ERROR: Cannot reach Ollama at {TAGS_URL}: {e}")
        sys.exit(1)

    models = [m for m in all_models if "sov" in m.lower() or "qwen" in m.lower()]
    print(f"\nFound {len(all_models)} total models, {len(models)} matching sov/qwen:\n")
    for m in models:
        print(f"  • {m}")

    if not models:
        print("No matching models found. Exiting.")
        sys.exit(1)

    # ── 2. Prepare test sets ─────────────────────────────────────────────────
    print("\nLoading reasoning corpus samples...")
    reasoning_samples = load_reasoning_samples(10)
    print(f"  {len(reasoning_samples)} reasoning samples loaded")

    all_categories = [
        ("reasoning", reasoning_samples, "[REASONING]"),
        ("math", MATH_SAMPLES, "[MATH]"),
        ("code", CODE_SAMPLES, "[CODE]"),
        ("sovereign", SOVEREIGN_SAMPLES, "[SOVEREIGN]"),
    ]

    # ── 3. Run benchmarks ────────────────────────────────────────────────────
    all_results = {}
    total_start = time.time()

    for model in models:
        print(f"\n{'─' * 78}")
        print(f"  MODEL: {model}")
        print(f"{'─' * 78}")
        model_results = {}
        for cat_name, samples, prefix in all_categories:
            print(f"\n  Category: {cat_name.upper()} ({len(samples)} samples)")
            cat_results = run_benchmark(model, samples, cat_name, prefix)
            model_results[cat_name] = cat_results
        all_results[model] = model_results

    total_elapsed = time.time() - total_start

    # ── 4. Summary table ─────────────────────────────────────────────────────
    print(f"\n\n{'=' * 78}")
    print("  BENCHMARK RESULTS SUMMARY")
    print(f"{'=' * 78}")
    print(f"  Total time: {total_elapsed:.0f}s\n")

    # Header
    hdr = f"{'Model':<35} {'Cat':<11} {'AvgTime':>7} {'AvgScore':>8} {'AvgLen':>7}"
    print(hdr)
    print("─" * len(hdr))

    for model in models:
        for cat_name, _, _ in all_categories:
            cat_data = all_results[model].get(cat_name, [])
            if not cat_data:
                continue
            avg_time = sum(r["time_sec"] for r in cat_data) / len(cat_data)
            avg_score = sum(r["score"] for r in cat_data) / len(cat_data)
            avg_len = sum(r["response_length"] for r in cat_data) / len(cat_data)
            mname = model[:34]
            print(f"  {mname:<33} {cat_name:<11} {avg_time:>6.1f}s {avg_score:>7.3f} {avg_len:>6.0f}")
        print()

    # Overall leaderboard
    print(f"\n{'=' * 78}")
    print("  OVERALL LEADERBOARD (weighted avg score)")
    print(f"{'=' * 78}\n")

    leaderboard = []
    weights = {"reasoning": 0.4, "math": 0.2, "code": 0.2, "sovereign": 0.2}
    for model in models:
        weighted = 0.0
        total_w = 0.0
        for cat, w in weights.items():
            cat_data = all_results[model].get(cat, [])
            if cat_data:
                avg = sum(r["score"] for r in cat_data) / len(cat_data)
                weighted += avg * w
                total_w += w
        final = weighted / total_w if total_w > 0 else 0
        leaderboard.append((model, round(final, 4)))

    leaderboard.sort(key=lambda x: x[1], reverse=True)
    print(f"  {'Rank':<5} {'Model':<38} {'Score':>6}")
    print(f"  {'─'*5} {'─'*38} {'─'*6}")
    for rank, (m, s) in enumerate(leaderboard, 1):
        print(f"  {rank:<5} {m:<38} {s:>6.4f}")

    # ── 5. Save results ──────────────────────────────────────────────────────
    output = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "total_time_sec": round(total_elapsed, 1),
        "models_tested": models,
        "leaderboard": [{"model": m, "score": s} for m, s in leaderboard],
        "detailed_results": all_results,
    }
    with open(RESULTS_PATH, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\n  Results saved to: {RESULTS_PATH}")
    print("=" * 78)


if __name__ == "__main__":
    main()
