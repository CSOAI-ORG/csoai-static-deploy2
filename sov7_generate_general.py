#!/usr/bin/env python3
"""sov7_generate_general.py — Generate teacher data for general capabilities
and agentic tasks. Used to build sov4-sov7-master-pro, the broad top-tier.

Categories:
  MATH       - GSM8K, math word problems, algebra
  CODE       - HumanEval, Python functions, debugging
  REASONING  - BBH, ARC, logical deduction
  KNOWLEDGE  - MMLU, GPQA, factual QA
  AGENTIC    - tool use, planning, multi-step, API calls
  CHAT       - instruction following, roleplay, conversation
"""
import argparse, json, os, sys, time, urllib.request
from pathlib import Path

# General capability prompts
GENERAL_PROMPTS = {
    "math": [
        ("What is 7 * 8?", "7 × 8 = 56"),
        ("If a train travels 60 mph for 2.5 hours, how far does it go?", "60 × 2.5 = 150 miles"),
        ("Solve: 2x + 5 = 17", "2x = 12, so x = 6"),
        ("What is 15% of 240?", "15% × 240 = 0.15 × 240 = 36"),
        ("The sum of three consecutive integers is 72. What are they?", "Let n, n+1, n+2 = 72, so 3n+3=72, 3n=69, n=23. The integers are 23, 24, 25."),
        ("A rectangle has length 12 and width 5. What is its area?", "12 × 5 = 60 square units"),
        ("If 3x - 7 = 2x + 5, find x.", "3x - 2x = 5 + 7, x = 12"),
        ("Convert 0.75 to a fraction.", "0.75 = 75/100 = 3/4"),
        ("What is 144 divided by 12?", "144 / 12 = 12"),
        ("The perimeter of a square is 32 cm. What is its side length?", "32 / 4 = 8 cm"),
        ("If f(x) = 2x² - 3x + 1, find f(2).", "f(2) = 2(4) - 3(2) + 1 = 8 - 6 + 1 = 3"),
        ("How many seconds in 3 hours?", "3 × 60 × 60 = 10,800 seconds"),
    ],
    "code": [
        ("Write a Python function to compute factorial of n.", "def factorial(n):\n    return 1 if n <= 1 else n * factorial(n-1)"),
        ("Write a Python function to check if a string is a palindrome.", "def is_palindrome(s):\n    return s == s[::-1]"),
        ("Write a Python function to find the maximum in a list.", "def find_max(lst):\n    if not lst: return None\n    return max(lst)"),
        ("Write a Python function to compute fibonacci numbers.", "def fib(n):\n    a, b = 0, 1\n    for _ in range(n):\n        a, b = b, a + b\n    return a"),
        ("Write a Python function to merge two sorted lists.", "def merge_sorted(a, b):\n    result, i, j = [], 0, 0\n    while i < len(a) and j < len(b):\n        if a[i] <= b[j]: result.append(a[i]); i += 1\n        else: result.append(b[j]); j += 1\n    return result + a[i:] + b[j:]"),
        ("Write SQL to find the second-highest salary from an Employees table.", "SELECT MAX(salary) FROM Employees WHERE salary < (SELECT MAX(salary) FROM Employees);"),
        ("Write a Python function to flatten a nested list.", "def flatten(lst):\n    result = []\n    for item in lst:\n        if isinstance(item, list): result.extend(flatten(item))\n        else: result.append(item)\n    return result"),
        ("Explain what this code does: lambda x: x**2 if x > 0 else -x**2", "It squares x positively if x>0, else squares and negates. Equivalent to: positive-definite squared result for all reals (returns -x² for x<0)."),
        ("Write a Python function to count word frequency in a text.", "def word_freq(text):\n    from collections import Counter\n    return Counter(text.lower().split())"),
        ("Write regex to validate an email address.", r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"),
        ("Write a Python decorator that retries a function 3 times on exception.", "def retry(times=3):\n    def deco(f):\n        def wrapper(*a, **kw):\n            for i in range(times):\n                try: return f(*a, **kw)\n                except Exception: pass\n            return f(*a, **kw)\n        return wrapper\n    return deco"),
    ],
    "reasoning": [
        ("If all roses are flowers, and some flowers fade quickly, can we conclude some roses fade quickly? Explain.", "No. 'Some flowers fade quickly' doesn't mean all flowers or any specific flowers. We can't conclude anything about roses from this premise alone. This is the fallacy of the undistributed middle."),
        ("A bat and ball cost $1.10 total. The bat costs $1 more than the ball. How much does the ball cost?", "5 cents. If the ball were 10 cents, the bat would be $1.10, totaling $1.20. With 5 cents for the ball, the bat is $1.05, totaling $1.10."),
        ("If you rearrange the letters 'CIFAIPC', you get the name of a(n):", "Ocean: PACIFIC"),
        ("Which is heavier: a pound of feathers or a pound of lead?", "Same weight: one pound. The question tricks you into thinking feathers are lighter, but weight is weight."),
        ("A farmer has 17 sheep. All but 9 die. How many are left?", "9. 'All but 9' means 9 survived, the rest died."),
        ("If 5 machines make 5 widgets in 5 minutes, how long for 100 machines to make 100 widgets?", "5 minutes. Each machine makes 1 widget in 5 minutes, so 100 machines make 100 widgets in 5 minutes (parallel)."),
        ("What's the next number in the sequence: 2, 4, 8, 16, ?", "32. Each number doubles."),
        ("A is the father of B. B is the father of C. What is A to C?", "Grandfather (or grandmother if A is female)."),
        ("If it's false that 'no cats are dogs', what can we conclude?", "Some cats are dogs OR all cats are dogs. At least one cat is a dog (in the world of this statement)."),
        ("Three friends: Alice (truth), Bob (lies), Carol (random). One says 'I am Alice'. Who is it?", "It can't be Alice (truth-teller would say 'I am Alice' truthfully, so it could be Alice actually). Wait - if it's Alice, she'd say 'I am Alice' truthfully. So it could be Alice or Bob (lying). Need more context — but if forced to choose, it's likely Bob (lying)."),
    ],
    "knowledge": [
        ("What is the capital of Australia?", "Canberra (not Sydney)"),
        ("Who wrote 'Pride and Prejudice'?", "Jane Austen"),
        ("What is the speed of light in m/s?", "Approximately 299,792,458 m/s (≈ 3×10⁸ m/s)"),
        ("What is the largest planet in our solar system?", "Jupiter"),
        ("Who proposed the theory of general relativity?", "Albert Einstein (1915)"),
        ("What is the chemical symbol for gold?", "Au (from Latin 'aurum')"),
        ("What year did World War II end?", "1945"),
        ("What is the boiling point of water at sea level in Celsius?", "100°C"),
        ("Who painted the Mona Lisa?", "Leonardo da Vinci"),
        ("What is the largest ocean?", "Pacific Ocean"),
        ("What is the smallest country in the world?", "Vatican City (0.49 km²)"),
        ("What does CPU stand for?", "Central Processing Unit"),
        ("What is photosynthesis?", "The process by which plants convert sunlight, water, and CO₂ into glucose and oxygen."),
        ("What is the Pythagorean theorem?", "In a right triangle, a² + b² = c², where c is the hypotenuse."),
    ],
    "chat": [
        ("Explain quantum entanglement to a 10-year-old.", "Imagine two magic dice that are connected. If you roll one and get a 6, the other one — even if it's far away on the moon — instantly shows the opposite. Spooky action at a distance!"),
        ("Write a haiku about programming.", "Code flows like streams /\n Bugs emerge, then fade away /\n Ship it, watch it gleam"),
        ("What is the meaning of life, the universe, and everything?", "42 (according to Douglas Adams' Hitchhiker's Guide). More seriously, this is a question each person answers for themselves."),
        ("Give me a productivity tip.", "Time-box your tasks: set a 25-min timer (Pomodoro), focus on one thing, take a 5-min break. Repeat. The constraint creates focus."),
        ("Explain GDPR in one sentence.", "A European regulation giving individuals control over their personal data and requiring organisations to handle that data transparently, lawfully, and securely."),
        ("What is the best programming language for beginners?", "Python — readable syntax, large community, broad applications from web to data science to AI."),
        ("Compare SQL and NoSQL databases.", "SQL databases are relational, use structured schemas, and excel at complex joins and ACID transactions. NoSQL databases are non-relational, schema-flexible, and scale horizontally for unstructured data."),
        ("What's the difference between machine learning and deep learning?", "Machine learning is a broad field where algorithms learn from data. Deep learning is a subset using multi-layer neural networks, especially good at perception tasks (vision, speech, language)."),
        ("Explain the concept of 'technical debt'.", "The accumulated cost of choosing easy solutions now over better ones later, similar to financial debt — it compounds and slows future development until 'paid down'."),
    ],
    "agentic": [
        ("Plan a 3-day trip to Tokyo for a first-time visitor.", "Day 1: Arrive, Shibuya & Shinjuku (Tokyo Metropolitan Building for night view).\nDay 2: Asakusa (Senso-ji), Akihabara, Ueno Park.\nDay 3: Tsukiji outer market, Imperial Palace, Ginza, depart.\n\nBook: hotel near Shinjuku or Asakusa for transit. Get a Suica/Pasmo card. JR Pass if going further."),
        ("Break down the task: 'migrate a PostgreSQL database to MySQL'.", "1. Schema analysis: list tables, indexes, constraints, sequences.\n2. Type mapping: PG types → MySQL equivalents (json→json, uuid→char(36), serial→auto_increment).\n3. Export: pg_dump with --no-owner --compatible=ansi.\n4. Transform: convert SQL syntax (e.g. ::cast, NOW() → CURRENT_TIMESTAMP).\n5. Import: mysql < transformed.sql.\n6. Validate: row counts, sample queries, data integrity checks.\n7. Update app: connection string, ORM config.\n8. Cutover plan: read-replica, swap, monitor."),
        ("You have a budget of $5000 to launch a podcast. Plan the spend.", "Equipment: $800 (mic, headphones, interface, pop filter).\nHosting: $200/yr (e.g. Transistor).\nDomain + hosting setup: $50.\nCover art: $300 (designer on Fiverr).\nEditing software: $0 (Audacity free) or $200 (Adobe Audition).\nMusic licensing: $300 (Epidemic Sound 1 yr).\nMarketing: $2500 (Meta ads, guest swaps, social).\nReserve: $850 (unexpected)."),
        ("Debug: a website returns 500 error only on /checkout. List hypotheses in order.", "1. Payment gateway API down or returning error.\n2. Database write failing (lock, full disk, FK violation).\n3. Session/cookie corruption specific to checkout flow.\n4. New deploy introduced regression (check recent commits).\n5. Third-party service (tax, shipping) failing.\n6. Rate limit hit on /checkout.\n\nCheck: server logs around the time, recent deploys, payment provider status page, DB error log."),
        ("Outline a 6-month plan to learn machine learning from scratch.", "Month 1-2: Python, NumPy, pandas, matplotlib. Mini projects.\nMonth 3: Statistics, probability, linear algebra essentials. Andrew Ng's course (or 3Blue1Brown).\nMonth 4: Classical ML (scikit-learn). Regression, classification, trees, ensembles. Kaggle Titanic + House Prices.\nMonth 5: Deep learning basics. PyTorch. CNNs, RNNs. MNIST + CIFAR-10.\nMonth 6: Specialization (NLP, vision, or RL). One portfolio project end-to-end."),
        ("If a user reports the app is slow, what do you check first?", "1. Reproduce: get their exact steps and timing.\n2. Browser DevTools: Network tab — check waterfall for slow requests.\n3. Server logs: latency, error rate for the affected endpoint.\n4. APM (if available): traces, slow queries, external calls.\n5. Recent deploy: did something change?\n6. Capacity: CPU, memory, DB connections, queue depth.\n7. External: third-party API status, DNS, CDN."),
    ],
}


def call_ollama(host, model, prompt, max_tokens=400, timeout=120):
    payload = json.dumps({"model": model, "prompt": prompt, "stream": False,
                          "options": {"temperature": 0, "num_predict": max_tokens}}).encode()
    req = urllib.request.Request(f"{host}/api/generate", data=payload,
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            d = json.loads(r.read())
        return {"ok": True, "response": d.get("response", "").strip()}
    except Exception as e:
        return {"ok": False, "error": str(e)[:200]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default="http://localhost:11435")
    ap.add_argument("--teacher", default="sov4-sov7-master")
    ap.add_argument("--out", default="/tmp/teacher_general.jsonl")
    ap.add_argument("--max-tokens", type=int, default=300)
    args = ap.parse_args()

    print(f"=== TEACHER: {args.teacher} via {args.host} ===")
    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)

    n = 0
    started = time.time()
    for category, qa_list in GENERAL_PROMPTS.items():
        print(f"\n--- {category.upper()} ({len(qa_list)} prompts) ---")
        for i, (q, expected) in enumerate(qa_list, 1):
            prompt = (f"You are an expert {category} tutor. Answer accurately and concisely. "
                      f"2-4 sentences max. No preamble.\n\nQ: {q}\nA:")
            r = call_ollama(args.host, args.teacher, prompt, max_tokens=args.max_tokens)
            if not r.get("ok"):
                print(f"  [{i:2d}] ERR {r.get('error','')[:80]}")
                continue
            a = r["response"].strip()
            if not a:
                print(f"  [{i:2d}] empty response")
                continue
            rec = {
                "category": category, "q": q, "a": a, "expected": expected,
                "teacher": args.teacher, "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            }
            with open(args.out, "a") as f:
                f.write(json.dumps(rec) + "\n")
            n += 1
            print(f"  [{i:2d}] {q[:55]:55s} -> {a[:70]}")
    elapsed = time.time() - started
    print(f"\nDONE: {n} examples in {elapsed:.0f}s -> {args.out}")


if __name__ == "__main__":
    main()
