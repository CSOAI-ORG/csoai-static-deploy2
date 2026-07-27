#!/usr/bin/env python3
"""
Extended EAT (Evolutionary Adversarial Testing) Cycle
Tests 5 Ollama models against 100 categorized reasoning samples from SupraLabs corpus.
Uses only stdlib (urllib, json, time, random, sys, re).
"""

import json
import time
import random
import sys
import re
import urllib.request
import urllib.error
from pathlib import Path
from collections import defaultdict

OLLAMA_URL = "http://localhost:11434/api/generate"
TAGS_URL = "http://localhost:11434/api/tags"
CORPUS_PATH = Path(__file__).parent / "reasoning_corpus_5k.jsonl"
RESULTS_PATH = Path(__file__).parent / "eat_extended_results.json"
TIMEOUT = 30
NUM_SAMPLES = 100

MODELS = [
    "sov33-unified:latest",
    "sov33-unified-c4:latest",
    "sov33-evolved:latest",
    "sov33-strong-v2:latest",
    "qwen2.5:0.5b",
]

# ── Category classification ──────────────────────────────────────────────────

CATEGORY_PATTERNS = {
    "math": [
        r"\b(solve|equation|derivative|integral|calculate|simplify|factor)\b",
        r"\b(what is \d+[\+\-\*\/])", r"\b\d+ [\+\-\*\/] \d+",
        r"\b(percentage|percent|fraction|ratio)\b",
        r"\b(geometry|algebra|trigonometry|calculus)\b",
        r"\b(sum|product|difference|quotient)\b",
        r"\bmatrix|vector|polynomial|logarithm\b",
    ],
    "code": [
        r"\b(python|javascript|java|c\+\+|rust|golang)\b",
        r"\b(function|def |class |import )\b",
        r"\b(algorithm|implement|program|code|script)\b",
        r"\b(api|database|sql|html|css|react)\b",
        r"\b(recursion|loop|array|hash|tree|graph)\b",
        r"\b(debug|compile|execute|runtime|syntax)\b",
        r"\b(git|docker|kubernetes|deploy|server)\b",
        r"```",
    ],
    "reasoning": [
        r"\b(explain|analyze|evaluate|compare|contrast|discuss)\b",
        r"\b(argument|premise|conclusion|logical|fallacy)\b",
        r"\b(scenario|situation|dilemma|ethical|moral)\b",
        r"\b(strategy|plan|approach|methodology)\b",
        r"\b(why|how|what if|suppose|assume)\b",
        r"\b(reason|cause|effect|consequence|impact)\b",
    ],
    "sovereign": [
        r"\b(eu ai act|gdpr|regulation|compliance|audit)\b",
        r"\b(sovereign|sovereignty|digital sovereignty)\b",
        r"\b(privacy|data protection|rights|freedom)\b",
        r"\b(governance|policy|legislation|jurisdiction)\b",
        r"\b(bias|fairness|transparency|accountability)\b",
        r"\b(risk.{0,5}(assessment|management|mitigation))\b",
    ],
    "knowledge": [
        r"\b(history|historical|century|ancient|medieval)\b",
        r"\b(science|physics|chemistry|biology|astronomy)\b",
        r"\b(geography|country|continent|capital|population)\b",
        r"\b(literature|author|novel|poem|philosophy)\b",
        r"\b(economy|market|inflation|gdp|trade)\b",
        r"\b(climate|environment|ecosystem|species)\b",
        r"\b(medicine|health|disease|treatment|vaccine)\b",
    ],
}


def classify_category(question: str) -> str:
    """Classify a question into a category based on pattern matching."""
    q_lower = question.lower()
    scores = {}
    for cat, patterns in CATEGORY_PATTERNS.items():
        score = sum(1 for p in patterns if re.search(p, q_lower))
        scores[cat] = score
    best = max(scores, key=scores.get)
    if scores[best] == 0:
        return "reasoning"  # default
    return best


def load_and_categorize_samples(n=100):
    """Load n samples from corpus, classify each, balance across categories."""
    with open(CORPUS_PATH, "r") as f:
        lines = f.readlines()

    random.seed(42)
    # Shuffle all lines
    random.shuffle(lines)

    # Classify all, then pick balanced samples
    categorized = defaultdict(list)
    for line in lines:
        obj = json.loads(line)
        q = obj.get("q", "")
        a = obj.get("a", "")
        if not q or not a:
            continue
        cat = classify_category(q)
        keywords = [w for w in re.findall(r'\b\w{4,}\b', a[:300].lower())][:8]
        categorized[cat].append({
            "q": q,
            "a": a[:500],
            "category": cat,
            "expected_keywords": keywords,
            "source_len": obj.get("tok_len", 0),
        })

    # Pick balanced: ~20 per category
    samples = []
    cats = list(categorized.keys())
    per_cat = n // len(cats) + 1
    for cat in cats:
        pool = categorized[cat][:per_cat]
        samples.extend(pool)

    random.shuffle(samples)
    return samples[:n]


def query_ollama(model, prompt, timeout=TIMEOUT):
    """Send generate request to Ollama. Returns (response_text, elapsed_sec)."""
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
    except (urllib.error.URLError, TimeoutError, OSError, json.JSONDecodeError):
        elapsed = time.time() - t0
        return None, elapsed


def score_response(text, expected_keywords):
    """Quality score: keyword overlap (0.7) + length adequacy (0.3)."""
    if not text:
        return 0.0
    text_lower = text.lower()
    hits = sum(1 for kw in expected_keywords if kw.lower() in text_lower)
    keyword_score = hits / max(len(expected_keywords), 1)
    # Length score: reward responses between 100-600 chars
    rlen = len(text)
    if rlen < 20:
        length_score = 0.0
    elif rlen < 100:
        length_score = 0.3
    elif rlen < 600:
        length_score = 0.6 + (rlen - 100) / 500 * 0.4
    else:
        length_score = 1.0
    return round(keyword_score * 0.7 + length_score * 0.3, 3)


def run_model_benchmark(model, samples):
    """Run all samples for one model. Returns list of result dicts."""
    results = []
    total = len(samples)
    for i, sample in enumerate(samples):
        prompt = sample["q"]
        cat = sample["category"]
        print(f"    [{i+1:3d}/{total}] {cat:<11} {prompt[:60]}...", end="", flush=True)
        text, elapsed = query_ollama(model, prompt)
        if text is None:
            score = 0.0
            print(f" TIMEOUT ({elapsed:.1f}s)")
        else:
            score = score_response(text, sample["expected_keywords"])
            print(f" {elapsed:5.1f}s  {score:.3f}  ({len(text)}ch)")
        results.append({
            "question": prompt[:150],
            "category": cat,
            "time_sec": round(elapsed, 2),
            "score": score,
            "response_length": len(text) if text else 0,
            "response_preview": (text or "")[:200],
            "timeout": text is None,
        })
    return results


def compute_category_breakdown(model_results):
    """Compute per-category aggregates for a model's results."""
    cats = defaultdict(list)
    for r in model_results:
        cats[r["category"]].append(r)

    breakdown = {}
    for cat, items in sorted(cats.items()):
        scores = [r["score"] for r in items]
        times = [r["time_sec"] for r in items]
        timeouts = sum(1 for r in items if r["timeout"])
        breakdown[cat] = {
            "count": len(items),
            "avg_score": round(sum(scores) / len(scores), 3) if scores else 0,
            "avg_time": round(sum(times) / len(times), 2) if times else 0,
            "max_score": max(scores) if scores else 0,
            "min_score": min(scores) if scores else 0,
            "timeouts": timeouts,
        }
    return breakdown


def find_category_winners(all_results):
    """Determine which model wins each category."""
    categories = set()
    for model_res in all_results.values():
        categories.update(model_res["breakdown"].keys())

    winners = {}
    for cat in sorted(categories):
        best_model = None
        best_score = -1
        for model, data in all_results.items():
            bd = data["breakdown"].get(cat, {})
            s = bd.get("avg_score", 0)
            if s > best_score:
                best_score = s
                best_model = model
        winners[cat] = {"model": best_model, "score": best_score}
    return winners


def print_summary(all_results, total_elapsed):
    """Print formatted summary tables."""
    print(f"\n\n{'=' * 90}")
    print("  EXTENDED EAT CYCLE — RESULTS SUMMARY")
    print(f"{'=' * 90}")
    print(f"  Total time: {total_elapsed:.0f}s ({total_elapsed/60:.1f}min)")
    print(f"  Models tested: {len(all_results)}")

    # Per-model, per-category table
    print(f"\n  {'─' * 86}")
    print(f"  {'Model':<28} {'Category':<11} {'N':>3} {'AvgScr':>7} {'AvgTime':>8} {'TO':>3} {'MaxScr':>7}")
    print(f"  {'─' * 86}")

    model_overalls = {}
    for model, data in all_results.items():
        model_scores = []
        model_times = []
        for cat in sorted(data["breakdown"].keys()):
            bd = data["breakdown"][cat]
            print(f"  {model:<28} {cat:<11} {bd['count']:>3} {bd['avg_score']:>6.3f} "
                  f"{bd['avg_time']:>7.1f}s {bd['timeouts']:>3} {bd['max_score']:>6.3f}")
            model_scores.extend([bd["avg_score"]] * bd["count"])
            model_times.extend([bd["avg_time"]] * bd["count"])
        overall = sum(model_scores) / len(model_scores) if model_scores else 0
        avg_time = sum(model_times) / len(model_times) if model_times else 0
        model_overalls[model] = {"overall_score": round(overall, 4), "avg_time": round(avg_time, 2)}
        print(f"  {'→ ' + model:<28} {'OVERALL':<11} {len(model_scores):>3} {overall:>6.4f} {avg_time:>7.1f}s")
        print()

    # Category winners
    winners = find_category_winners(all_results)
    print(f"\n  {'=' * 86}")
    print("  CATEGORY WINNERS")
    print(f"  {'=' * 86}")
    for cat, info in winners.items():
        print(f"  {cat:<12} → {info['model']:<32} (score: {info['score']:.3f})")

    # Overall leaderboard
    print(f"\n  {'=' * 86}")
    print("  OVERALL LEADERBOARD")
    print(f"  {'=' * 86}\n")
    ranked = sorted(model_overalls.items(), key=lambda x: x[1]["overall_score"], reverse=True)
    print(f"  {'Rank':<5} {'Model':<32} {'Score':>8} {'AvgTime':>9}")
    print(f"  {'─'*5} {'─'*32} {'─'*8} {'─'*9}")
    for rank, (m, info) in enumerate(ranked, 1):
        marker = " ★" if rank == 1 else ""
        print(f"  {rank:<5} {m:<32} {info['overall_score']:>7.4f} {info['avg_time']:>8.1f}s{marker}")


def main():
    print("=" * 90)
    print("  EXTENDED EAT CYCLE — 5 Models × 100 Samples")
    print("=" * 90)

    # ── 1. Verify Ollama connectivity ────────────────────────────────────────
    print("\n[1/5] Checking Ollama API...")
    try:
        with urllib.request.urlopen(TAGS_URL, timeout=5) as resp:
            available = [m["name"] for m in json.loads(resp.read().decode()).get("models", [])]
    except Exception as e:
        print(f"ERROR: Cannot reach Ollama at {TAGS_URL}: {e}")
        sys.exit(1)

    print(f"  Available models: {len(available)}")
    models = [m for m in MODELS if m in available]
    missing = [m for m in MODELS if m not in available]
    if missing:
        print(f"  WARNING: Missing models: {missing}")
    if not models:
        print("  ERROR: No target models available. Exiting.")
        sys.exit(1)
    print(f"  Testing {len(models)} models: {models}")

    # ── 2. Load and categorize corpus ────────────────────────────────────────
    print(f"\n[2/5] Loading {NUM_SAMPLES} samples from reasoning corpus...")
    samples = load_and_categorize_samples(NUM_SAMPLES)
    cat_counts = defaultdict(int)
    for s in samples:
        cat_counts[s["category"]] += 1
    print(f"  Loaded {len(samples)} samples:")
    for cat, cnt in sorted(cat_counts.items()):
        print(f"    {cat:<12} {cnt:>3} samples")

    # ── 3. Run benchmarks ────────────────────────────────────────────────────
    print(f"\n[3/5] Running benchmarks ({len(models)} models × {len(samples)} samples)...")
    all_results = {}
    total_queries = len(models) * len(samples)
    query_count = 0
    total_start = time.time()

    for model in models:
        print(f"\n  {'━' * 80}")
        print(f"  MODEL: {model}")
        print(f"  {'━' * 80}")
        model_start = time.time()
        model_results = run_model_benchmark(model, samples)
        model_elapsed = time.time() - model_start
        query_count += len(samples)

        breakdown = compute_category_breakdown(model_results)
        overall_score = sum(r["score"] for r in model_results) / len(model_results)
        timeouts = sum(1 for r in model_results if r["timeout"])

        all_results[model] = {
            "results": model_results,
            "breakdown": breakdown,
            "overall_score": round(overall_score, 4),
            "total_time": round(model_elapsed, 1),
            "timeouts": timeouts,
            "avg_time_per_query": round(model_elapsed / len(model_results), 2),
        }

        elapsed_so_far = time.time() - total_start
        eta = elapsed_so_far / query_count * (total_queries - query_count)
        print(f"\n  → {model}: score={overall_score:.4f} time={model_elapsed:.0f}s "
              f"timeouts={timeouts}  (ETA: {eta:.0f}s remaining)")

    total_elapsed = time.time() - total_start

    # ── 4. Print summary ─────────────────────────────────────────────────────
    print_summary(all_results, total_elapsed)

    # ── 5. Save results ──────────────────────────────────────────────────────
    print(f"\n[5/5] Saving results...")
    winners = find_category_winners(all_results)
    output = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "total_time_sec": round(total_elapsed, 1),
        "num_samples": len(samples),
        "models_tested": list(all_results.keys()),
        "category_distribution": dict(cat_counts),
        "category_winners": winners,
        "leaderboard": [
            {
                "model": m,
                "overall_score": d["overall_score"],
                "avg_time": d["avg_time_per_query"],
                "timeouts": d["timeouts"],
            }
            for m, d in sorted(all_results.items(),
                               key=lambda x: x[1]["overall_score"], reverse=True)
        ],
        "per_model_breakdown": {
            m: {
                "overall_score": d["overall_score"],
                "total_time": d["total_time"],
                "timeouts": d["timeouts"],
                "avg_time_per_query": d["avg_time_per_query"],
                "category_breakdown": d["breakdown"],
            }
            for m, d in all_results.items()
        },
    }

    with open(RESULTS_PATH, "w") as f:
        json.dump(output, f, indent=2)
    print(f"  Results saved to: {RESULTS_PATH}")
    print(f"\n{'=' * 90}")
    print("  EAT CYCLE COMPLETE")
    print(f"{'=' * 90}")


if __name__ == "__main__":
    main()
