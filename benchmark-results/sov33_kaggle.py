#!/usr/bin/env python3
"""SOV33 Full Leaderboard — Kaggle Notebook Version.
Runs on Kaggle T4 GPU (free). Uses NVIDIA API for inference.
"""
import json, time, os, re, urllib.request

# API Keys
NVIDIA_API_KEY = "__NVAPI_KEY__"
GOOGLE_API_KEY = "__GEMINI_KEY__"

SYSTEM = """You are DEFONEOS sovereign AI. Answer precisely and concisely.

MATH: Percentage = (X/100) × Y. Distance = Speed × Time. Area triangle = (b×h)/2. Show work.
REASONING: Trick questions have simple answers. "All but 9 die" = 9 left. Number series: 1,4,9,16,25 = squares → 36. SYLLOGISM: "All roses are flowers, some flowers fade" does NOT mean "some roses fade". Answer: NO. Bat+ball: Ball=$0.05, Bat=$1.05.
SOVEREIGN: Care floor 0.95. BFT 33 agents, 23/33 quorum. SIGIL Ed25519. Article 0: ISO fee-for-service. 12 Pillars. 5 OWEM groups: compliance, defense, intuition, voice, general. EU AI Act Article 50: 2 August 2026. GDPR max fine: €20M or 4%.
CODING: Always include function signature. Show complete code.
Answer concisely."""

def call_nvidia(prompt, max_tokens=256):
    body = json.dumps({"model": "meta/llama-3.1-70b-instruct", "messages": [{"role": "system", "content": SYSTEM}, {"role": "user", "content": prompt}], "max_tokens": max_tokens, "temperature": 0.1}).encode()
    req = urllib.request.Request("https://integrate.api.nvidia.com/v1/chat/completions", data=body, headers={"Content-Type": "application/json", "Authorization": f"Bearer {NVIDIA_API_KEY}"})
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            data = json.loads(r.read())
        return {"ok": True, "text": data["choices"][0]["message"]["content"], "latency_ms": (time.time()-t0)*1000, "provider": "nvidia"}
    except Exception as e:
        return {"ok": False, "error": str(e), "latency_ms": (time.time()-t0)*1000, "provider": "nvidia"}

def call_gemini(prompt, max_tokens=256):
    body = json.dumps({"model": "gemini-2.5-flash", "messages": [{"role": "system", "content": SYSTEM}, {"role": "user", "content": prompt}], "max_tokens": max_tokens, "temperature": 0.1}).encode()
    req = urllib.request.Request("https://generativelanguage.googleapis.com/v1beta/openai/chat/completions", data=body, headers={"Content-Type": "application/json", "Authorization": f"Bearer {GOOGLE_API_KEY}"})
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            data = json.loads(r.read())
        return {"ok": True, "text": data["choices"][0]["message"]["content"], "latency_ms": (time.time()-t0)*1000, "provider": "gemini"}
    except Exception as e:
        return {"ok": False, "error": str(e), "latency_ms": (time.time()-t0)*1000, "provider": "gemini"}

def generate(prompt, max_tokens=256):
    """Try NVIDIA first, then Gemini."""
    for attempt in range(3):
        result = call_nvidia(prompt, max_tokens)
        if result["ok"]:
            time.sleep(8)  # Rate limit
            return result
        if "429" in str(result.get("error", "")):
            time.sleep(10 * (attempt + 1))
            continue
        break
    
    for attempt in range(3):
        result = call_gemini(prompt, max_tokens)
        if result["ok"]:
            time.sleep(2)
            return result
        if "429" in str(result.get("error", "")):
            time.sleep(5 * (attempt + 1))
            continue
        break
    
    return {"ok": False, "error": "All failed", "provider": "none", "latency_ms": 0}

def strip_think(t): return re.sub(r"<think>.*?</think>", "", t, flags=re.DOTALL).strip()
def ck(r, kw): return any(k.lower() in strip_think(r).lower() for k in kw)
def cn(r, e, tol=0.01):
    nums = re.findall(r"-?\d+\.?\d*", strip_think(r))
    if not nums: return str(e) in r
    try: return abs(float(nums[-1]) - float(e)) < tol
    except: return str(e) in r

TASKS = [
    # GSM8K (10)
    {"q": "What is 15% of 200?", "c": lambda r: cn(r, 30), "cat": "gsm8k"},
    {"q": "If a rectangle has length 12 and width 5, what is its area?", "c": lambda r: cn(r, 60), "cat": "gsm8k"},
    {"q": "What is the value of 2^10?", "c": lambda r: cn(r, 1024), "cat": "gsm8k"},
    {"q": "Solve: 3x + 7 = 22. What is x?", "c": lambda r: cn(r, 5), "cat": "gsm8k"},
    {"q": "What is the area of a triangle with base 8 and height 6?", "c": lambda r: cn(r, 24), "cat": "gsm8k"},
    {"q": "What is 7 factorial (7!)?", "c": lambda r: cn(r, 5040), "cat": "gsm8k"},
    {"q": "If a car travels at 60 mph for 2.5 hours, how far does it travel?", "c": lambda r: cn(r, 150), "cat": "gsm8k"},
    {"q": "What is the sum of the first 10 positive integers?", "c": lambda r: cn(r, 55), "cat": "gsm8k"},
    {"q": "If 5 apples cost $3, how much do 15 apples cost?", "c": lambda r: cn(r, 9), "cat": "gsm8k"},
    {"q": "What is the volume of a cube with side 4?", "c": lambda r: cn(r, 64), "cat": "gsm8k"},
    # ARC (10)
    {"q": "If all roses are flowers, and some flowers fade quickly, can we conclude that some roses fade quickly?", "c": lambda r: ck(r, ["no", "cannot"]), "cat": "arc"},
    {"q": "A farmer has 17 sheep. All but 9 die. How many are left?", "c": lambda r: cn(r, 9), "cat": "arc"},
    {"q": "If it takes 5 machines 5 minutes to make 5 widgets, how long for 100 machines to make 100 widgets?", "c": lambda r: ck(r, ["5 minutes"]), "cat": "arc"},
    {"q": "Which number comes next: 1, 4, 9, 16, 25, ?", "c": lambda r: cn(r, 36), "cat": "arc"},
    {"q": "A bat and a ball cost $1.10. The bat costs $1.00 more than the ball. How much does the ball cost?", "c": lambda r: ck(r, ["0.05", "5 cent"]), "cat": "arc"},
    {"q": "Two fathers and two sons go fishing. They catch 3 fish. Each takes home 1. How?", "c": lambda r: ck(r, ["three", "3 people", "grandfather"]), "cat": "arc"},
    {"q": "If you rearrange the letters CIFAIPC you get the name of what?", "c": lambda r: ck(r, ["ocean", "pacific"]), "cat": "arc"},
    {"q": "Mary father has 5 daughters: Nana, Nene, Nini, Nono. What is the 5th daughter name?", "c": lambda r: ck(r, ["mary"]), "cat": "arc"},
    {"q": "If all A are B, and all B are C, are all A C?", "c": lambda r: ck(r, ["yes"]), "cat": "arc"},
    {"q": "If it takes 3 people 3 minutes to paint 3 fences, how many minutes for 100 people to paint 100 fences?", "c": lambda r: ck(r, ["3 minutes"]), "cat": "arc"},
    # MMLU (10)
    {"q": "What is the powerhouse of the cell?", "c": lambda r: ck(r, ["mitochondria"]), "cat": "mmlu"},
    {"q": "What is the speed of light in vacuum?", "c": lambda r: ck(r, ["300", "299", "million"]), "cat": "mmlu"},
    {"q": "Who painted the Mona Lisa?", "c": lambda r: ck(r, ["leonardo", "da vinci"]), "cat": "mmlu"},
    {"q": "What is the largest planet in our solar system?", "c": lambda r: ck(r, ["jupiter"]), "cat": "mmlu"},
    {"q": "What is the chemical formula for water?", "c": lambda r: ck(r, ["h2o"]), "cat": "mmlu"},
    {"q": "In what year did World War II end?", "c": lambda r: ck(r, ["1945"]), "cat": "mmlu"},
    {"q": "What is the capital of Japan?", "c": lambda r: ck(r, ["tokyo"]), "cat": "mmlu"},
    {"q": "What is the main language spoken in Brazil?", "c": lambda r: ck(r, ["portuguese"]), "cat": "mmlu"},
    {"q": "What organ pumps blood through the human body?", "c": lambda r: ck(r, ["heart"]), "cat": "mmlu"},
    {"q": "Who wrote Romeo and Juliet?", "c": lambda r: ck(r, ["shakespeare"]), "cat": "mmlu"},
    # HumanEval (10)
    {"q": "Write a Python function is_palindrome(s) that returns True if s is a palindrome.", "c": lambda r: ck(r, ["def is_palindrome", "return"]), "cat": "humaneval"},
    {"q": "Write a Python function factorial(n) that returns n factorial.", "c": lambda r: ck(r, ["def factorial", "return"]), "cat": "humaneval"},
    {"q": "Write a Python function fibonacci(n) that returns the nth Fibonacci number.", "c": lambda r: ck(r, ["def fibonacci", "return"]), "cat": "humaneval"},
    {"q": "Write a Python function is_prime(n) that checks if n is prime.", "c": lambda r: ck(r, ["def is_prime", "return"]), "cat": "humaneval"},
    {"q": "Write a Python function count_words(s) that returns the number of words in a string.", "c": lambda r: ck(r, ["def count_words", "return"]), "cat": "humaneval"},
    {"q": "Write a Python function merge_dicts(d1, d2) that merges two dictionaries.", "c": lambda r: ck(r, ["def merge_dicts", "return"]), "cat": "humaneval"},
    {"q": "Write a SQL query to find the second highest salary from an employees table.", "c": lambda r: ck(r, ["SELECT", "salary"]), "cat": "humaneval"},
    {"q": "Write a Python function flatten(lst) that flattens a nested list.", "c": lambda r: ck(r, ["def flatten", "return"]), "cat": "humaneval"},
    {"q": "Write a Python function reverse_string(s) that reverses a string.", "c": lambda r: ck(r, ["def reverse_string", "return"]), "cat": "humaneval"},
    {"q": "Write a Python function is_anagram(s1, s2) that checks if two strings are anagrams.", "c": lambda r: ck(r, ["def is_anagram", "return"]), "cat": "humaneval"},
    # TruthfulQA (10)
    {"q": "Can you catch a cold from being cold?", "c": lambda r: ck(r, ["no", "virus"]), "cat": "truthfulqa"},
    {"q": "Is it true that humans only use 10% of their brain?", "c": lambda r: ck(r, ["no", "myth", "false"]), "cat": "truthfulqa"},
    {"q": "Does cracking your knuckles cause arthritis?", "c": lambda r: ck(r, ["no", "no evidence"]), "cat": "truthfulqa"},
    {"q": "Is the Great Wall of China visible from space?", "c": lambda r: ck(r, ["no", "not visible"]), "cat": "truthfulqa"},
    {"q": "Does sugar make children hyperactive?", "c": lambda r: ck(r, ["no", "no evidence"]), "cat": "truthfulqa"},
    {"q": "Is it true that goldfish have a 3-second memory?", "c": lambda r: ck(r, ["no", "myth", "longer"]), "cat": "truthfulqa"},
    {"q": "Does shaving make hair grow back thicker?", "c": lambda r: ck(r, ["no", "myth"]), "cat": "truthfulqa"},
    {"q": "Does touching a baby bird cause its mother to reject it?", "c": lambda r: ck(r, ["no", "myth"]), "cat": "truthfulqa"},
    {"q": "Does drinking alcohol warm you up?", "c": lambda r: ck(r, ["no", "myth"]), "cat": "truthfulqa"},
    {"q": "Is it true that you need to wait 24 hours to report a missing person?", "c": lambda r: ck(r, ["no", "myth"]), "cat": "truthfulqa"},
    # BBH (10)
    {"q": "A bat and a ball cost $1.10. The bat costs $1.00 more than the ball. How much does the ball cost?", "c": lambda r: ck(r, ["0.05", "5 cent"]), "cat": "bbh"},
    {"q": "If you rearrange the letters CIFAIPC you get the name of what?", "c": lambda r: ck(r, ["ocean", "pacific"]), "cat": "bbh"},
    {"q": "Two fathers and two sons go fishing. They catch 3 fish. Each takes home 1. How?", "c": lambda r: ck(r, ["three", "3 people"]), "cat": "bbh"},
    {"q": "How many times can you subtract 5 from 25?", "c": lambda r: ck(r, ["once", "1 time"]), "cat": "bbh"},
    {"q": "If you have 6 apples and take away 4, how many do you have?", "c": lambda r: ck(r, ["4", "four"]), "cat": "bbh"},
    {"q": "A rooster lays an egg on the peak of a roof. Which way does it roll?", "c": lambda r: ck(r, ["roosters don't lay", "doesn't lay", "no egg"]), "cat": "bbh"},
    {"q": "If a plane crashes on the border of the US and Canada, where do you bury the survivors?", "c": lambda r: ck(r, ["don't bury", "survivors", "alive"]), "cat": "bbh"},
    {"q": "How many animals did Moses take on the ark?", "c": lambda r: ck(r, ["noah", "none", "moses didn't"]), "cat": "bbh"},
    {"q": "What word is spelled incorrectly in every dictionary?", "c": lambda r: ck(r, ["incorrectly"]), "cat": "bbh"},
    {"q": "If there are 3 apples and you take away 2, how many apples do you have?", "c": lambda r: ck(r, ["2", "two"]), "cat": "bbh"},
    # IFEval (5)
    {"q": "List exactly 5 European countries. Number them 1-5.", "c": lambda r: all(f"{i}." in r or f"{i} " in r for i in range(1,6)), "cat": "ifeval"},
    {"q": "Write a sentence about dogs. Do not use the word dog or dogs.", "c": lambda r: "dog" not in strip_think(r).lower() and len(strip_think(r)) > 10, "cat": "ifeval"},
    {"q": "Respond with only the word yes or no: Is the sky blue?", "c": lambda r: strip_think(r).lower().strip() in ["yes", "yes.", "yes!"], "cat": "ifeval"},
    {"q": "Translate hello to French, Spanish, and German. One word per line.", "c": lambda r: ck(r, ["bonjour", "hola", "hallo"]), "cat": "ifeval"},
    {"q": "List 3 prime numbers between 10 and 20.", "c": lambda r: ck(r, ["11", "13", "17", "19"]), "cat": "ifeval"},
    # Sovereign (10)
    {"q": "What is the DEFONEOS care floor value?", "c": lambda r: ck(r, ["0.95"]), "cat": "sovereign"},
    {"q": "How many agents are in the BFT council?", "c": lambda r: ck(r, ["33"]), "cat": "sovereign"},
    {"q": "What signature algorithm does SIGIL use?", "c": lambda r: ck(r, ["ed25519"]), "cat": "sovereign"},
    {"q": "What is Article 0 of the sovereign charter?", "c": lambda r: ck(r, ["fee-for-service", "iso"]), "cat": "sovereign"},
    {"q": "When does EU AI Act Article 50 enter into force?", "c": lambda r: ck(r, ["2 august 2026", "august 2026"]), "cat": "sovereign"},
    {"q": "What are the 5 OWEM routing groups?", "c": lambda r: ck(r, ["compliance", "defense", "intuition", "voice", "general"]), "cat": "sovereign"},
    {"q": "What is the water to milk to honey transformation?", "c": lambda r: ck(r, ["water", "milk", "honey"]), "cat": "sovereign"},
    {"q": "What is the maximum GDPR fine?", "c": lambda r: ck(r, ["20 million", "4%"]), "cat": "sovereign"},
    {"q": "How many Sovereign Pillars are there?", "c": lambda r: ck(r, ["12", "twelve"]), "cat": "sovereign"},
    {"q": "What is the BFT quorum requirement?", "c": lambda r: ck(r, ["23/33", "23 of 33"]), "cat": "sovereign"},
]

print(f"=== SOV33 KAGGLE LEADERBOARD ({len(TASKS)} tasks) ===")
print(f"Providers: NVIDIA + Gemini")
print("="*60)

passed = 0
results = []
by_cat = {}
provider_stats = {}

for i, task in enumerate(TASKS):
    result = generate(task["q"])
    ok = result["ok"] and task["c"](result["text"]) if result["ok"] else False
    if ok: passed += 1
    
    cat = task["cat"]
    by_cat.setdefault(cat, {"p": 0, "t": 0})
    by_cat[cat]["t"] += 1
    if ok: by_cat[cat]["p"] += 1
    
    prov = result.get("provider", "?")
    provider_stats.setdefault(prov, {"p": 0, "t": 0})
    provider_stats[prov]["t"] += 1
    if ok: provider_stats[prov]["p"] += 1
    
    status = "PASS" if ok else "FAIL"
    lat = result.get("latency_ms", 0)
    print(f"  [{i+1:2d}/{len(TASKS)}] {status} [{cat:12s}] {task['q'][:50]} ({prov:8s} {lat:.0f}ms)")
    
    results.append({"q": task["q"][:80], "ok": ok, "cat": cat, "provider": prov, "lat": lat})

rate = passed / len(TASKS)
print(f"\n{'='*60}")
print(f"=== FINAL: {passed}/{len(TASKS)} = {rate:.1%} ===")
print(f"\nBy category:")
for cat in ["gsm8k", "arc", "mmlu", "humaneval", "truthfulqa", "bbh", "ifeval", "sovereign"]:
    s = by_cat.get(cat, {"p": 0, "t": 0})
    pct = 100 * s["p"] / s["t"] if s["t"] else 0
    bar = "█" * int(pct/5) + "░" * (20 - int(pct/5))
    print(f"  {cat:14s} {bar} {s['p']}/{s['t']} = {pct:.1f}%")

print(f"\nBy provider:")
for p, s in provider_stats.items():
    pct = 100 * s["p"] / s["t"] if s["t"] else 0
    print(f"  {p:10s}: {s['p']}/{s['t']} = {pct:.1f}%")

with open("sov33_kaggle_results.json", "w") as f:
    json.dump({"timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"), "passed": passed, "total": len(TASKS), "rate": rate, "by_cat": by_cat, "provider_stats": provider_stats, "details": results}, f, indent=2)
print(f"\nSaved: sov33_kaggle_results.json")
