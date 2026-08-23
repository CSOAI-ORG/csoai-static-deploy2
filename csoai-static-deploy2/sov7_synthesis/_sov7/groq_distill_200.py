#!/usr/bin/env python3
"""
Groq Distillation — 200 diverse prompts across 5 categories (40 each).
Calls Groq free API via curl. Saves JSONL with thought_trace when available.
"""

import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path
from datetime import datetime, timezone

OUTPUT_PATH = Path(__file__).parent / "groq_distilled_200.jsonl"
GROQ_ENDPOINT = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama-3.3-70b-versatile"
FALLBACK = "llama-3.1-8b-instant"
RATE_LIMIT_DELAY = 2.0
MAX_RETRIES = 3


def get_api_key():
    key = os.environ.get("GROQ_API_KEY")
    if key:
        return key
    keyfile = Path.home() / ".groq" / "api_key"
    if keyfile.exists():
        return keyfile.read_text().strip()
    return ""


def is_error(text: str) -> bool:
    return text.startswith("[") or text.startswith("{\"message\"")


def call_groq(api_key: str, prompt: str, model: str) -> tuple:
    payload = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 1024,
    })
    try:
        r = subprocess.run(
            ["curl", "-s", "--max-time", "60", GROQ_ENDPOINT,
             "-H", f"Authorization: Bearer {api_key}",
             "-H", "Content-Type: application/json",
             "-d", payload],
            capture_output=True, text=True, timeout=65
        )
        if r.returncode != 0:
            return f"[CURL_ERROR] {r.stderr[:200]}", "", True
        data = json.loads(r.stdout)
        if "error" in data:
            return json.dumps(data["error"]), "", True
        choice = data["choices"][0]["message"]
        content = choice.get("content", "")
        reasoning = choice.get("reasoning_content", "")
        return content, reasoning, False
    except json.JSONDecodeError:
        return f"[JSON_ERROR] {r.stdout[:200]}", "", True
    except Exception as e:
        return f"[ERROR] {e}", "", True


def extract_wait(text: str) -> float:
    m = re.search(r"try again in (\d+)m([\d.]+)s", text)
    if m:
        return int(m.group(1)) * 60 + float(m.group(2))
    m = re.search(r"try again in ([\d.]+)s", text)
    if m:
        return float(m.group(1))
    return 30.0


PROMPTS = {
    "math": [
        "Solve for x: 3x^2 - 12x + 9 = 0. Show your work step by step.",
        "Find the derivative of f(x) = x^3 * ln(x) using the product rule.",
        "What is the probability of getting exactly 3 heads in 5 fair coin flips?",
        "Given mean 50 and std dev 10, what percentage falls between 40 and 60 in a normal distribution?",
        "A circle has center (3,4) and passes through the origin. Find its equation and radius.",
        "Solve the system: 2x + 3y = 12 and 4x - y = 5.",
        "Evaluate the integral of x * e^(x^2) dx using u-substitution.",
        "A bag has 5 red, 3 blue, 2 green marbles. Probability of drawing 2 red without replacement?",
        "Find eigenvalues of [[4,1],[2,3]]. Show the characteristic polynomial.",
        "Prove sqrt(2) is irrational using proof by contradiction.",
        "Solve the differential equation dy/dx = 2xy with initial condition y(0) = 1.",
        "Find the Taylor series expansion of e^x centered at a=0 up to the 4th degree term.",
        "Compute the determinant of [[1,2,3],[0,4,5],[1,0,6]] using cofactor expansion.",
        "What is the sum of the infinite geometric series 1 + 1/2 + 1/4 + 1/8 + ...?",
        "Find the area enclosed between y = x^2 and y = 2x.",
        "Prove by induction that 1 + 2 + 3 + ... + n = n(n+1)/2.",
        "Convert the point (3, 3) from Cartesian to polar coordinates.",
        "Find the volume of the solid of revolution when y = sqrt(x) from x=0 to x=4 is rotated about the x-axis.",
        "Solve the recurrence relation a_n = 3a_{n-1} - 2a_{n-2} with a_0=1, a_1=3.",
        "What is the probability that a randomly chosen 3-digit number is divisible by 7?",
        "Find the inverse of the matrix [[2,1],[5,3]].",
        "Evaluate the limit of (sin x)/x as x approaches 0. Show L'Hopital's rule.",
        "Find the critical points of f(x,y) = x^2 + y^2 - 2x - 4y + 8.",
        "A fair die is rolled 3 times. What is the probability of getting at least one 6?",
        "Find the general solution to y'' + 4y = 0.",
        "Compute the dot product and cross product of vectors u=(1,2,3) and v=(4,5,6).",
        "Find the shortest distance from the point (1,2) to the line 3x + 4y = 12.",
        "How many ways can 8 people be arranged in a circle?",
        "Find the Maclaurin series for ln(1+x) and state its radius of convergence.",
        "Solve the inequality |2x - 5| < 3.",
        "What is the remainder when 2^100 is divided by 7?",
        "Find the arc length of y = x^(3/2) from x=0 to x=4.",
        "Prove that the set of rational numbers is countable.",
        "Find the flux of F(x,y,z) = (x,y,z) through the unit sphere.",
        "Determine whether the series sum(n=1 to inf) 1/n^2 converges or diverges.",
        "Find the QR decomposition of the matrix [[1,1],[1,0],[0,1]].",
        "What is the expected value and variance of a Poisson distribution with lambda=3?",
        "Solve the partial differential equation u_t = u_xx with given boundary conditions.",
        "Find the eigenvalues and eigenvectors of [[0,-1],[1,0]].",
        "Compute the double integral of (x+y) over the region 0<=x<=1, 0<=y<=x.",
    ],
    "code": [
        "Write a Python function to find the longest common subsequence using dynamic programming.",
        "Write a SQL query to find the top 5 customers by total order amount from 'customers' and 'orders'.",
        "Implement binary search in Python on a sorted array returning the index.",
        "Explain stack vs queue. Implement both in Python.",
        "Write a Python function to detect a cycle in a linked list using Floyd's algorithm.",
        "Debug this code and explain:\ndef merge_sort(arr):\n    if len(arr) <= 1: return arr\n    mid = len(arr) / 2\n    return merge(merge_sort(arr[:mid]), merge_sort(arr[mid:]))",
        "Write a Python memoization decorator that handles keyword arguments.",
        "Write a SQL window function query to rank employees by salary within each department.",
        "Implement a trie in Python with insert, search, and startsWith.",
        "Write Python code for topological sort on a DAG using DFS.",
        "Implement a LRU cache in Python with O(1) get and put operations.",
        "Write a Python generator that yields prime numbers using the Sieve of Eratosthenes.",
        "Write a SQL query to find employees who earn more than their department average.",
        "Implement a min-heap in Python with insert, extract_min, and heapify operations.",
        "Write a Python async function that fetches multiple URLs concurrently using aiohttp.",
        "Implement Dijkstra's shortest path algorithm in Python.",
        "Write a Python context manager for database connections with automatic rollback on error.",
        "Write a SQL query using CTEs to find the organizational hierarchy from an employees table.",
        "Implement a red-black tree insertion in Python.",
        "Write Python code to serialize and deserialize a binary tree.",
        "Implement quicksort in Python with median-of-three pivot selection.",
        "Write a Python metaclass that automatically registers all subclasses.",
        "Write a SQL query to find gaps in a sequence of IDs.",
        "Implement a thread-safe producer-consumer queue in Python.",
        "Write Python code to solve the N-queens problem using backtracking.",
        "Design a REST API for a blog application. Define endpoints, methods, and request/response schemas.",
        "Write a Python function to flatten a deeply nested JSON structure.",
        "Implement a B-tree with insert and search operations in Python.",
        "Write a SQL query to pivot rows into columns dynamically.",
        "Write Python code implementing the observer design pattern.",
        "Implement a graph using adjacency lists with BFS and DFS traversals in Python.",
        "Write a Python function to detect if a string has balanced parentheses.",
        "Design a rate limiter class in Python using the token bucket algorithm.",
        "Write a SQL query to calculate running totals and moving averages.",
        "Implement merge sort for a linked list in Python.",
        "Write Python code for a simple expression parser and evaluator.",
        "Implement a bloom filter in Python with configurable false positive rate.",
        "Write a Python decorator that retries a function on specific exceptions.",
        "Design a key-value store with TTL support in Python.",
        "Write a SQL query using window functions to find year-over-year growth.",
    ],
    "reasoning": [
        "All roses are flowers. Some flowers fade quickly. Can we conclude some roses fade quickly?",
        "If it rains, the ground gets wet. The ground is wet. Can we conclude it rained?",
        "A bat and ball cost $1.10. The bat costs $1.00 more than the ball. How much does the ball cost?",
        "Complete: Book is to Reading as Fork is to ___? Explain the pattern.",
        "Three switches control three bulbs in the next room. Enter once. How to determine which switch controls which?",
        "All bloops are razzies. All razzies are lazzies. Are all bloops definitely lazzies?",
        "A farmer has 17 sheep. All but 9 die. How many are left?",
        "Explain the Monty Hall problem. Why does switching give 2/3 probability?",
        "If A > B and B > C, is A necessarily > C? What reasoning type is this?",
        "Two trains 300km apart head toward each other at 60 and 90 km/h. When and where do they meet?",
        "You have 12 identical-looking balls. One is different weight. Find it in 3 weighings with a balance scale.",
        "If some doctors are lawyers and all lawyers are educated, can we conclude some doctors are educated?",
        "A snail climbs 3 meters up a 10-meter well each day and slips back 2 each night. When does it escape?",
        "Five pirates must divide 100 gold coins. What is the optimal strategy using backward induction?",
        "You have two ropes that each take exactly 1 hour to burn unevenly. How do you measure 45 minutes?",
        "If no heroes are cowards and some soldiers are heroes, what can we conclude about soldiers and cowards?",
        "Explain the prisoner's dilemma. What is the Nash equilibrium?",
        "A clock shows 3:15. What is the angle between the hour and minute hands?",
        "If you shuffle a deck of cards, what is more likely: a specific arrangement or all red cards on top?",
        "Three missionaries and three cannibals must cross a river. The boat holds two. Constraints?",
        "If all Zips are Zaps and no Zaps are Zops, can any Zips be Zops? Draw a Venn diagram.",
        "You have 8 coins, one lighter. Find it in 2 weighings. Explain your strategy.",
        "A town has one barber. He shaves all men who don't shave themselves. Who shaves the barber?",
        "If it takes 5 machines 5 minutes to make 5 widgets, how long for 100 machines to make 100 widgets?",
        "Complete the pattern: 2, 6, 12, 20, 30, ___",
        "You flip a coin 100 times and get heads every time. What is the probability of heads on flip 101?",
        "If A implies B, and B implies C, does not-C imply not-A?",
        "Two doors: one leads to safety, one to death. Two guards: one always lies, one always tells truth. One question allowed.",
        "A train leaves at 2pm going 60mph. Another leaves at 3pm going 80mph in same direction. When does the second catch the first?",
        "If some cats are dogs and some dogs are fish, can we conclude some cats are fish?",
        "You have a 3-gallon jug and a 5-gallon jug. Measure exactly 4 gallons.",
        "Explain the base rate fallacy with a medical testing example.",
        "If 5 cats catch 5 mice in 5 minutes, how many cats catch 100 mice in 100 minutes?",
        "What is the expected number of coin flips to get two heads in a row?",
        "A drawer has 10 black and 10 white socks. How many must you pull to guarantee a matching pair?",
        "If all A are B, and some B are C, what can we definitively conclude about A and C?",
        "You have 25 horses and a 5-lane track. Find the 3 fastest in minimum races.",
        "Explain the birthday paradox. Why is the probability >50% with just 23 people?",
        "If a hen and a half lays an egg and a half in a day and a half, how many eggs does one hen lay in one day?",
        "A pendulum swings. At what point is kinetic energy maximum and potential energy zero?",
    ],
    "sovereign": [
        "Explain the EU AI Act's four risk levels with examples of each.",
        "What are GDPR Articles 15-22 data subject rights? Explain each briefly.",
        "What does ISO 42001 require for AI governance? Explain main clauses.",
        "What is AUKUS and its implications for AI in defense?",
        "Explain NATO's principles on responsible AI use in military contexts.",
        "List the eight Annex III high-risk AI areas under the EU AI Act.",
        "How does GDPR Article 6 define lawful bases for processing?",
        "How do ISO 42001 and the EU AI Act complement each other?",
        "Explain meaningful human control in autonomous weapons under IHL.",
        "What are the EU AI Act Article 50 transparency obligations?",
        "What is the NCSC Cyber Assessment Framework (CAF)? Explain its 14 principles.",
        "Explain JSP 936: UK MoD policy on the use of AI in defence systems.",
        "What does the EU AI Act Article 5 prohibit? List all prohibited practices.",
        "Explain GDPR Article 25: data protection by design and by default.",
        "What are the key requirements for conformity assessment under the EU AI Act?",
        "How does ISO 42001 Annex B map to specific AI risk management controls?",
        "Explain the EU AI Act's requirements for foundation models (Article 53).",
        "What is the UK's pro-innovation approach to AI regulation? Compare to the EU AI Act.",
        "Explain GDPR Article 35: when is a Data Protection Impact Assessment required?",
        "What are the EU AI Act penalties? How are fines calculated per Article 99?",
        "Explain BFT (Byzantine Fault Tolerant) consensus in the context of distributed AI systems.",
        "What does the EU AI Act require for real-time biometric identification in public spaces?",
        "Explain the NIST AI Risk Management Framework and how it maps to ISO 42001.",
        "What are GDPR breach notification requirements under Articles 33 and 34?",
        "Explain the EU AI Act's requirements for human oversight of high-risk AI (Article 14).",
        "What is the relationship between the EU AI Act and the Product Liability Directive?",
        "Explain the concept of regulatory sandboxes under the EU AI Act (Article 57).",
        "What does the EU AI Act require for testing high-risk AI systems in real-world conditions?",
        "Explain GDPR's right to explanation under Articles 13-14 and automated decision-making under Article 22.",
        "What are the EU AI Act requirements for post-market monitoring of high-risk AI?",
        "Explain the OECD AI Principles and their influence on the EU AI Act.",
        "What does the EU AI Act require regarding training data quality and governance (Article 10)?",
        "Explain the concept of a 'provider' vs 'deployer' under the EU AI Act definitions.",
        "What are the EU AI Act's requirements for registration in the EU database (Article 49)?",
        "Explain the interplay between the EU AI Act and the Digital Services Act.",
        "What does the EU AI Act require for transparency to deployers of high-risk AI (Article 13)?",
        "Explain GDPR's territorial scope under Article 3. When does it apply outside the EU?",
        "What are the EU AI Act's requirements for AI literacy and training (Article 4)?",
        "Explain the EU AI Act's approach to general-purpose AI models and the AI Office.",
        "What does the GDPR's Article 17 right to erasure entail? What are its exceptions?",
    ],
    "knowledge": [
        "Explain photosynthesis including light-dependent and light-independent reactions.",
        "What were the main causes and consequences of the French Revolution?",
        "Explain plate tectonics and how it explains earthquakes and volcanoes.",
        "Compare Plato and Aristotle on reality and knowledge.",
        "What is quantum entanglement? Explain in accessible terms.",
        "Describe DNA structure and how it encodes proteins.",
        "What were the main achievements of the Islamic Golden Age?",
        "Explain entropy in thermodynamics and the second law.",
        "What is the significance of Shakespeare's Hamlet? Discuss themes.",
        "Explain the trolley problem. What do utilitarian and deontological views say?",
        "What is CRISPR-Cas9? Explain its mechanism and applications.",
        "Explain the causes of World War I. What role did alliances play?",
        "What is dark matter and dark energy? Why do physicists believe they exist?",
        "Explain the philosophical concept of existentialism. What did Sartre and Camus contribute?",
        "How does the human immune system work? Explain innate and adaptive immunity.",
        "What was the Renaissance? Describe its causes, key figures, and lasting impact.",
        "Explain the theory of general relativity. How does spacetime curvature work?",
        "What is the prisoner's dilemma in game theory? How does iterated version differ?",
        "Describe the structure of an atom. Explain the quantum mechanical model.",
        "What were the main philosophical contributions of Confucius and Laozi?",
        "Explain the greenhouse effect and its role in climate change.",
        "What is the significance of the Rosetta Stone? How did it enable decipherment?",
        "Explain how neural networks learn. What is backpropagation?",
        "What were the main causes of the fall of the Roman Empire?",
        "Explain the Doppler effect with examples in sound and light.",
        "What is Machiavelli's political philosophy in The Prince?",
        "Describe the process of evolution by natural selection. What is genetic drift?",
        "What was the Scientific Revolution? Who were its key figures?",
        "Explain the double-slit experiment. What does it reveal about quantum mechanics?",
        "What is utilitarianism? Compare Bentham's and Mill's versions.",
        "Explain how vaccines work. What is herd immunity?",
        "What were the main events and consequences of the Cold War?",
        "Explain the theory of relativity's mass-energy equivalence (E=mc^2).",
        "What is phenomenology? Explain Husserl's and Heidegger's approaches.",
        "Describe the water cycle and its importance for Earth's climate.",
        "What were the main intellectual movements of the Enlightenment?",
        "Explain how semiconductors work. What is a p-n junction?",
        "What is the social contract theory? Compare Hobbes, Locke, and Rousseau.",
        "Explain the human nervous system. How do neurons transmit signals?",
        "What is the significance of the discovery of penicillin?",
    ],
}


def main():
    api_key = get_api_key()
    if not api_key:
        print("ERROR: No GROQ_API_KEY found. Set env var or create ~/.groq/api_key")
        sys.exit(1)
    print(f"API key loaded ({api_key[:10]}...)")

    all_prompts = [(cat, p) for cat, ps in PROMPTS.items() for p in ps]
    assert len(all_prompts) == 200, f"Expected 200 prompts, got {len(all_prompts)}"

    print(f"Total prompts: {len(all_prompts)}")
    print(f"Model: {MODEL} (fallback: {FALLBACK})")
    print(f"Rate limit: {RATE_LIMIT_DELAY}s between requests")
    print(f"Output: {OUTPUT_PATH}")
    print("=" * 70)

    results = []
    errors = 0
    retries_total = 0
    fallback_count = 0
    start_time = time.time()

    for i, (category, prompt) in enumerate(all_prompts, 1):
        tag = f"[{i:3d}/200] {category:10s}"

        response = None
        reasoning_trace = ""
        used_model = MODEL
        last_err = ""

        for attempt in range(MAX_RETRIES):
            content, reasoning, is_err = call_groq(api_key, prompt, MODEL)
            if not is_err:
                response = content
                reasoning_trace = reasoning
                used_model = MODEL
                break

            last_err = content
            if "rate_limit" in content.lower():
                retries_total += 1
                wait = extract_wait(content)
                if wait > 60:
                    print(f"{tag} | 70b limited ({wait:.0f}s), falling back to 8b...")
                    c2, r2, is_err2 = call_groq(api_key, prompt, FALLBACK)
                    if not is_err2:
                        response = c2
                        reasoning_trace = r2
                        used_model = FALLBACK
                        fallback_count += 1
                        break
                else:
                    print(f"{tag} | Rate limited, waiting {wait:.0f}s...")
                    time.sleep(wait)
                    retries_total += 1
            else:
                print(f"{tag} | ERROR: {content[:80]}")
                break

        if response is None:
            response = last_err
            errors += 1
            print(f"{tag} | FAILED")
        else:
            status = "OK"
            if i % 10 == 0 or i == 1:
                elapsed_so_far = time.time() - start_time
                rate = i / elapsed_so_far if elapsed_so_far > 0 else 0
                remaining = (200 - i) / rate if rate > 0 else 0
                print(f"{tag} | {status} ({len(response)}c, {used_model.split('/')[-1]}) "
                      f"[{i}/200 done, {elapsed_so_far:.0f}s elapsed, ~{remaining:.0f}s left]")

        record = {
            "q": prompt,
            "a": response,
            "source": "groq",
            "model": used_model,
            "category": category,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        if reasoning_trace:
            record["thought_trace"] = reasoning_trace
        results.append(record)

        # Save incrementally every 20 prompts
        if i % 20 == 0:
            with open(OUTPUT_PATH, "w") as f:
                for r in results:
                    f.write(json.dumps(r, ensure_ascii=False) + "\n")

        if i < len(all_prompts):
            time.sleep(RATE_LIMIT_DELAY)

    # Final write
    with open(OUTPUT_PATH, "w") as f:
        for r in results:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    elapsed = time.time() - start_time
    cat_counts = {}
    cat_ok = {}
    for r in results:
        c = r["category"]
        cat_counts[c] = cat_counts.get(c, 0) + 1
        if not is_error(r["a"]):
            cat_ok[c] = cat_ok.get(c, 0) + 1

    print("=" * 70)
    print(f"COMPLETED in {elapsed:.1f}s ({elapsed/60:.1f} min)")
    ok = sum(1 for r in results if not is_error(r["a"]))
    print(f"Total: {len(results)} | Success: {ok} | Errors: {errors}")
    print(f"Retries: {retries_total} | Fallbacks to 8b: {fallback_count}")
    print(f"Output: {OUTPUT_PATH} ({OUTPUT_PATH.stat().st_size / 1024:.1f} KB)")
    thought_count = sum(1 for r in results if r.get("thought_trace"))
    print(f"Thought traces captured: {thought_count}")
    print()
    print("Category breakdown:")
    for cat in ["math", "code", "reasoning", "sovereign", "knowledge"]:
        t = cat_counts.get(cat, 0)
        s = cat_ok.get(cat, 0)
        print(f"  {cat:12s}: {s}/{t} succeeded")


if __name__ == "__main__":
    main()
