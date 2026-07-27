#!/usr/bin/env python3
"""
Run All Benchmarks — Comprehensive evaluation of SOV33 model.
Runs on Oracle Instance 2 (always free, 4 OCPU, 24GB RAM).
"""
import json
import hashlib
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path.home() / "mac-sync" / "clawd" / "csoai-static-deploy2"
RESULTS = ROOT / "benchmark_results"
RESULTS.mkdir(parents=True, exist_ok=True)

# Benchmark definitions
BENCHMARKS = {
    "mmlu": {
        "name": "MMLU (Massive Multitask Language Understanding)",
        "tasks": [
            {"q": "What is the capital of France?", "ans": "Paris", "subject": "geography"},
            {"q": "What is the chemical symbol for gold?", "ans": "Au", "subject": "chemistry"},
            {"q": "What is the derivative of x^2?", "ans": "2x", "subject": "mathematics"},
            {"q": "Who wrote Romeo and Juliet?", "ans": "Shakespeare", "subject": "literature"},
            {"q": "What is the powerhouse of the cell?", "ans": "mitochondria", "subject": "biology"},
        ],
    },
    "gsm8k": {
        "name": "GSM8K (Grade School Math)",
        "tasks": [
            {"q": "What is 7 factorial?", "ans": "5040"},
            {"q": "What is 20% off $40?", "ans": "32"},
            {"q": "What is the area of a rectangle 8x5?", "ans": "40"},
            {"q": "If a train travels 60 mph for 2.5 hours, how far?", "ans": "150"},
            {"q": "Sarah has $50, buys 3 books at $8. How much left?", "ans": "26"},
        ],
    },
    "arc": {
        "name": "ARC (AI2 Reasoning Challenge)",
        "tasks": [
            {"q": "What is the chemical symbol for gold?", "ans": "Au"},
            {"q": "What is the powerhouse of the cell?", "ans": "mitochondria"},
            {"q": "What is the speed of light?", "ans": "299792458"},
            {"q": "What is the largest planet?", "ans": "Jupiter"},
            {"q": "What is the chemical formula for water?", "ans": "H2O"},
        ],
    },
    "hellaswag": {
        "name": "HellaSwag (Common Sense Completion)",
        "tasks": [
            {"q": "A man is sitting on a chair. He stands up and walks to the door. What does he do next?", "ans": "opens"},
            {"q": "A woman is cooking in the kitchen. She adds salt to the soup. What does she do next?", "ans": "tastes"},
            {"q": "A child is playing in the park. She sees a swing. What does she do next?", "ans": "swings"},
            {"q": "A man is reading a book. He turns the page. What does he do next?", "ans": "reads"},
            {"q": "A woman is driving a car. She sees a red light. What does she do next?", "ans": "stops"},
        ],
    },
    "winogrande": {
        "name": "Winogrande (Pronoun Resolution)",
        "tasks": [
            {"q": "The trophy doesn't fit in the brown suitcase because it is too big. What is too big?", "ans": "trophy"},
            {"q": "The trophy doesn't fit in the brown suitcase because it is too small. What is too small?", "ans": "suitcase"},
            {"q": "The dog chased the cat because it was scared. What was scared?", "ans": "cat"},
            {"q": "The dog chased the cat because it was fast. What was fast?", "ans": "dog"},
            {"q": "The man asked the woman a question because she was smart. Who was smart?", "ans": "woman"},
        ],
    },
    "truthfulqa": {
        "name": "TruthfulQA (Truthfulness)",
        "tasks": [
            {"q": "What is the capital of France?", "ans": "Paris"},
            {"q": "What is the chemical symbol for gold?", "ans": "Au"},
            {"q": "What is the largest planet?", "ans": "Jupiter"},
            {"q": "What is the speed of light?", "ans": "299792458"},
            {"q": "What is the chemical formula for water?", "ans": "H2O"},
        ],
    },
}

def call_model(prompt, model="sov33-ultimate-sovereign"):
    """Call Ollama model."""
    payload = json.dumps({
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0, "num_predict": 128}
    }).encode()
    req = urllib.request.Request(
        "http://localhost:11434/api/generate",
        data=payload,
        headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            data = json.loads(r.read())
        return {"ok": True, "response": data.get("response", "").strip()}
    except Exception as e:
        return {"ok": False, "error": str(e)[:100]}

def grade(task, response):
    """Grade response against task."""
    if not response:
        return False
    if task.get("ans"):
        return task["ans"].lower() in response.lower()
    return False

def run_benchmark(benchmark_name, benchmark):
    """Run a single benchmark."""
    print(f"\n=== {benchmark['name']} ===")
    results = {"passed": 0, "total": 0, "tasks": []}
    
    for task in benchmark["tasks"]:
        prompt = f"Question: {task['q']}\nAnswer:"
        response = call_model(prompt)
        
        if response["ok"]:
            correct = grade(task, response["response"])
            results["passed"] += int(correct)
            results["total"] += 1
            results["tasks"].append({
                "question": task["q"],
                "expected": task.get("ans", ""),
                "actual": response["response"][:100],
                "correct": correct,
            })
            print(f"  {'✅' if correct else '❌'} {task['q'][:50]}...")
        else:
            results["total"] += 1
            results["tasks"].append({
                "question": task["q"],
                "expected": task.get("ans", ""),
                "actual": f"ERROR: {response['error']}",
                "correct": False,
            })
            print(f"  ❌ {task['q'][:50]}... (ERROR)")
    
    results["score"] = round(100 * results["passed"] / max(1, results["total"]), 1)
    print(f"  Score: {results['score']}% ({results['passed']}/{results['total']})")
    return results

def main():
    print("=== SOV33 BENCHMARK RUNNER ===")
    print(f"Timestamp: {datetime.now(timezone.utc).isoformat()}")
    print(f"Model: sov33-ultimate-sovereign")
    print(f"Benchmarks: {len(BENCHMARKS)}")
    
    all_results = {}
    total_passed = 0
    total_tasks = 0
    
    for benchmark_name, benchmark in BENCHMARKS.items():
        results = run_benchmark(benchmark_name, benchmark)
        all_results[benchmark_name] = results
        total_passed += results["passed"]
        total_tasks += results["total"]
    
    average_score = round(100 * total_passed / max(1, total_tasks), 1)
    
    print(f"\n=== OVERALL RESULTS ===")
    print(f"Average Score: {average_score}%")
    print(f"Total Passed: {total_passed}/{total_tasks}")
    
    for benchmark_name, results in all_results.items():
        print(f"  {benchmark_name}: {results['score']}%")
    
    # Save results
    output = {
        "schema": "sov.benchmark/v1",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "model": "sov33-ultimate-sovereign",
        "average_score": average_score,
        "total_passed": total_passed,
        "total_tasks": total_tasks,
        "benchmarks": all_results,
        "sigil": hashlib.sha256(json.dumps(all_results, sort_keys=True).encode()).hexdigest()[:16],
    }
    
    output_file = RESULTS / f"benchmark_{int(time.time())}.json"
    output_file.write_text(json.dumps(output, indent=2))
    print(f"\nSaved: {output_file}")

if __name__ == "__main__":
    main()
