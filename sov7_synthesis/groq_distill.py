#!/usr/bin/env python3
"""
Groq Distillation Script — 50 diverse prompts across 5 categories.
Calls Groq's free API (llama-3.3-70b-versatile) and saves responses as JSONL.
"""

import json
import os
import subprocess
import sys
import time
from pathlib import Path
from datetime import datetime, timezone

OUTPUT_PATH = Path(__file__).parent / "groq_distilled_500.jsonl"
GROQ_ENDPOINT = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama-3.3-70b-versatile"
RATE_LIMIT_DELAY = 2.0  # seconds between requests


def get_api_key():
    key = os.environ.get("GROQ_API_KEY")
    if key:
        return key
    keyfile = Path.home() / ".groq" / "api_key"
    if keyfile.exists():
        return keyfile.read_text().strip()
    return ""


def call_groq(api_key: str, prompt: str) -> str:
    payload = json.dumps({
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 2048,
    })

    try:
        result = subprocess.run(
            [
                "curl", "-s", "--max-time", "60",
                GROQ_ENDPOINT,
                "-H", f"Authorization: Bearer {api_key}",
                "-H", "Content-Type: application/json",
                "-d", payload,
            ],
            capture_output=True, text=True, timeout=65
        )
        if result.returncode != 0:
            return f"[CURL_ERROR] {result.stderr[:200]}"
        data = json.loads(result.stdout)
        if "error" in data:
            return f"[API_ERROR] {data['error']}"
        return data["choices"][0]["message"]["content"]
    except json.JSONDecodeError as e:
        return f"[JSON_ERROR] {result.stdout[:200]}"
    except Exception as e:
        return f"[ERROR] {e}"


PROMPTS = {
    "math": [
        "Solve for x: 3x^2 - 12x + 9 = 0. Show your work step by step.",
        "Find the derivative of f(x) = x^3 * ln(x) using the product rule.",
        "What is the probability of getting exactly 3 heads in 5 fair coin flips? Explain the combinatorial reasoning.",
        "Given a dataset with mean 50 and standard deviation 10, what percentage of values fall between 40 and 60 assuming a normal distribution?",
        "A circle has center (3, 4) and passes through the origin. What is its equation and radius?",
        "Solve the system of equations: 2x + 3y = 12 and 4x - y = 5 using substitution or elimination.",
        "Evaluate the integral of x * e^(x^2) dx. Show the u-substitution clearly.",
        "A bag contains 5 red, 3 blue, and 2 green marbles. What is the probability of drawing 2 red marbles without replacement?",
        "Find the eigenvalues of the matrix [[4, 1], [2, 3]]. Show the characteristic polynomial.",
        "Prove that the square root of 2 is irrational using proof by contradiction."
    ],
    "code": [
        "Write a Python function to find the longest common subsequence of two strings using dynamic programming.",
        "Write a SQL query to find the top 5 customers by total order amount from tables 'customers' and 'orders'.",
        "Implement a binary search algorithm in Python that works on a sorted array and returns the index of the target.",
        "Explain the difference between a stack and a queue. Implement both in Python using lists.",
        "Write a Python function to detect a cycle in a linked list using Floyd's tortoise and hare algorithm.",
        "Debug this Python code and explain the bug:\n\ndef merge_sort(arr):\n    if len(arr) <= 1:\n        return arr\n    mid = len(arr) / 2\n    left = merge_sort(arr[:mid])\n    right = merge_sort(arr[mid:])\n    return merge(left, right)",
        "Write a Python decorator that caches function results (memoization) and handles keyword arguments.",
        "Write a SQL query using a window function to rank employees by salary within each department.",
        "Implement a trie (prefix tree) in Python with insert, search, and startsWith methods.",
        "Write Python code to perform a topological sort on a directed acyclic graph using DFS."
    ],
    "reasoning": [
        "All roses are flowers. Some flowers fade quickly. Can we conclude that some roses fade quickly? Explain the logical fallacy if any.",
        "If it rains, the ground gets wet. The ground is wet. Can we conclude it rained? Identify the logical form and validity.",
        "A bat and a ball cost $1.10 in total. The bat costs $1.00 more than the ball. How much does the ball cost? Explain the common intuitive error.",
        "Complete the analogy: Book is to Reading as Fork is to ___? Explain the reasoning pattern.",
        "Three switches control three bulbs in the next room. You can only enter the room once. How do you determine which switch controls which bulb?",
        "If all bloops are razzies and all razzies are lazzies, are all bloops definitely lazzies? Explain using set theory.",
        "A farmer has 17 sheep. All but 9 die. How many sheep are left? Explain the common misreading.",
        "Explain the Monty Hall problem. Why does switching doors give a 2/3 probability of winning?",
        "If A is taller than B, and B is taller than C, is A necessarily taller than C? What type of reasoning is this?",
        "Two trains leave stations 300 km apart heading toward each other at 60 km/h and 90 km/h. When and where do they meet?"
    ],
    "sovereign": [
        "Explain the EU AI Act's risk classification system. What are the four risk levels and examples of each?",
        "What are the key data subject rights under GDPR Articles 15-22? Explain each right briefly.",
        "What does ISO 42001 require for AI governance? Explain the main clauses and their purpose.",
        "What is the AUKUS agreement and what are its implications for AI and autonomous systems in defense?",
        "Explain NATO's principles on responsible use of AI in military contexts. What are the key ethical boundaries?",
        "Under the EU AI Act, what are the requirements for high-risk AI systems in Annex III? List the eight areas.",
        "How does GDPR Article 6 define lawful bases for processing personal data? Explain each basis.",
        "What is the relationship between ISO 42001 and the EU AI Act? How do they complement each other?",
        "Explain the concept of 'meaningful human control' in autonomous weapons systems under international humanitarian law.",
        "What are the EU AI Act's transparency obligations for AI systems that interact with humans (Article 50)?"
    ],
    "knowledge": [
        "Explain the process of photosynthesis including the light-dependent and light-independent reactions.",
        "What were the main causes and consequences of the French Revolution? Cover political, economic, and social factors.",
        "Explain the theory of plate tectonics and how it explains earthquakes, volcanoes, and mountain formation.",
        "Compare and contrast the philosophical views of Plato and Aristotle on the nature of reality and knowledge.",
        "What is quantum entanglement? Explain it in accessible terms and describe its implications for information theory.",
        "Describe the structure and function of DNA. How does it replicate and how does it encode proteins?",
        "What were the main achievements of the Islamic Golden Age in science, mathematics, and medicine?",
        "Explain the concept of entropy in thermodynamics. How does it relate to the second law?",
        "What is the significance of Shakespeare's Hamlet in English literature? Discuss themes and literary devices.",
        "Explain the trolley problem in ethics. What do utilitarian and deontological perspectives say about it?"
    ],
}


def main():
    api_key = get_api_key()
    if not api_key:
        print("WARNING: No GROQ_API_KEY found. Requests may fail.")
        print("Set via: export GROQ_API_KEY=gsk_... or save to ~/.groq/api_key")
    else:
        print(f"API key loaded ({api_key[:10]}...)")

    all_prompts = []
    for category, prompts in PROMPTS.items():
        for p in prompts:
            all_prompts.append((category, p))

    print(f"Total prompts: {len(all_prompts)}")
    print(f"Model: {MODEL}")
    print(f"Output: {OUTPUT_PATH}")
    print("=" * 60)

    results = []
    errors = 0
    start_time = time.time()

    for i, (category, prompt) in enumerate(all_prompts, 1):
        print(f"[{i:2d}/{len(all_prompts)}] {category:10s} | {prompt[:60]}...")
        response = call_groq(api_key, prompt)

        if response.startswith("[HTTP") or response.startswith("[ERROR"):
            print(f"           ERROR: {response[:100]}")
            errors += 1
        else:
            print(f"           OK ({len(response)} chars)")

        record = {
            "q": prompt,
            "a": response,
            "source": "groq-70b",
            "category": category,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        results.append(record)

        if i < len(all_prompts):
            time.sleep(RATE_LIMIT_DELAY)

    with open(OUTPUT_PATH, "w") as f:
        for r in results:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    elapsed = time.time() - start_time
    category_counts = {}
    category_errors = {}
    for r in results:
        cat = r["category"]
        category_counts[cat] = category_counts.get(cat, 0) + 1
        if r["a"].startswith("[HTTP") or r["a"].startswith("[ERROR"):
            category_errors[cat] = category_errors.get(cat, 0) + 1

    print("=" * 60)
    print(f"COMPLETED in {elapsed:.1f}s")
    print(f"Total: {len(results)} | Errors: {errors} | Success: {len(results) - errors}")
    print(f"Output: {OUTPUT_PATH}")
    print(f"File size: {OUTPUT_PATH.stat().st_size / 1024:.1f} KB")
    print()
    print("Category breakdown:")
    for cat in ["math", "code", "reasoning", "sovereign", "knowledge"]:
        total = category_counts.get(cat, 0)
        errs = category_errors.get(cat, 0)
        print(f"  {cat:12s}: {total - errs}/{total} succeeded")


if __name__ == "__main__":
    main()
