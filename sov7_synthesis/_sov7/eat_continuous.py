#!/usr/bin/env python3
"""
EAT Continuous Training Loop (Evolve, Absorb, Transform)
Runs indefinitely, testing models, identifying weaknesses, and generating
targeted improvement training data.
"""

import json, time, random, sys, re, os
import urllib.request, urllib.error
from pathlib import Path
from collections import defaultdict
from datetime import datetime

BASE_DIR = Path(__file__).parent
OLLAMA_URL = "http://localhost:11434/api/generate"
TAGS_URL = "http://localhost:11434/api/tags"
CORPUS = BASE_DIR / "reasoning_corpus_5k.jsonl"
HONEY_DIR = BASE_DIR.parent / "sov_space" / "honey_consolidated"
IMPROVEMENTS_FILE = BASE_DIR / "eat_improvements.jsonl"
PROGRESS_FILE = BASE_DIR / "eat_progress.json"
TIMEOUT = 30
NUM_PREDICT = 256

MODELS = [
    "sov33-evolved:latest",
    "sov33-strong:latest",
    "sov-sovereign-v3:latest",
    "qwen2.5:0.5b",
]

CATEGORIES = ["math", "code", "reasoning", "sovereign", "knowledge"]

CAT_PATTERNS = {
    "math": [r"\b(solve|equation|derivative|integral|calculate|simplify|factor)\b",
             r"\b(what is \d+[\+\-\*\/])", r"\b(percentage|percent|fraction|ratio)\b",
             r"\b(geometry|algebra|trigonometry|calculus)\b", r"\b(sum|product|difference|quotient)\b",
             r"\bmatrix|vector|polynomial|logarithm\b"],
    "code": [r"\b(python|javascript|java|c\+\+|rust|golang)\b", r"\b(def |class |import |function)\b",
             r"\b(algorithm|implement|program|code|script)\b", r"\b(api|database|sql|html|css)\b",
             r"\b(recursion|loop|array|hash|tree|graph)\b", r"```"],
    "reasoning": [r"\b(explain|analyze|evaluate|compare|contrast|discuss)\b",
                  r"\b(argument|premise|conclusion|logical|fallacy)\b",
                  r"\b(scenario|situation|dilemma|ethical|moral)\b",
                  r"\b(strategy|plan|approach|methodology)\b"],
    "sovereign": [r"\b(eu ai act|gdpr|regulation|compliance|audit)\b",
                  r"\b(sovereign|sovereignty|digital sovereignty)\b",
                  r"\b(privacy|data protection|rights|freedom)\b",
                  r"\b(governance|policy|legislation|jurisdiction)\b",
                  r"\b(bias|fairness|transparency|accountability)\b"],
    "knowledge": [r"\b(history|historical|century|ancient|medieval)\b",
                  r"\b(science|physics|chemistry|biology|astronomy)\b",
                  r"\b(geography|country|continent|capital|population)\b",
                  r"\b(literature|author|novel|poem|philosophy)\b",
                  r"\b(medicine|health|disease|treatment|vaccine)\b"],
}

WEAK_THRESHOLD = 0.7

# ---------------------------------------------------------------------------
# Classification
# ---------------------------------------------------------------------------

def classify(text):
    tl = text.lower()
    scores = {}
    for cat, patterns in CAT_PATTERNS.items():
        scores[cat] = sum(1 for p in patterns if re.search(p, tl))
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "reasoning"

# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_corpus(max_samples=200):
    samples = []
    if not CORPUS.exists():
        print(f"  WARN: Corpus not found at {CORPUS}")
        return samples
    with open(CORPUS) as f:
        for line in f:
            obj = json.loads(line)
            q = obj.get("q", "")
            a = obj.get("a", "")
            if not q or not a:
                continue
            cat = classify(q)
            kws = [w for w in re.findall(r'\b\w{4,}\b', a[:300].lower())][:8]
            samples.append({
                "q": q[:500],
                "a": a[:500],
                "category": cat,
                "expected_keywords": kws,
                "source": "corpus"
            })
            if len(samples) >= max_samples:
                break
    return samples


def load_honey():
    samples = []
    if not HONEY_DIR.exists():
        print(f"  WARN: Honey dir not found at {HONEY_DIR}")
        return samples
    for jf in sorted(HONEY_DIR.glob("honey_*.jsonl")):
        with open(jf) as f:
            for line in f:
                try:
                    obj = json.loads(line)
                except:
                    continue
                convs = obj.get("conversations", [])
                user_msg = ""
                asst_msg = ""
                for c in convs:
                    if c.get("from") == "user":
                        user_msg = c.get("value", "")
                    elif c.get("from") == "assistant":
                        asst_msg = c.get("value", "")
                if not user_msg or not asst_msg:
                    continue
                cat = classify(user_msg)
                family = obj.get("family", jf.stem.replace("honey_", ""))
                kws = [w for w in re.findall(r'\b\w{4,}\b', asst_msg[:300].lower())][:8]
                samples.append({
                    "q": user_msg[:500],
                    "a": asst_msg[:500],
                    "category": cat,
                    "expected_keywords": kws,
                    "source": f"honey:{family}"
                })
    return samples

# ---------------------------------------------------------------------------
# Ollama API
# ---------------------------------------------------------------------------

def query_model(model, prompt):
    payload = json.dumps({
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.2, "num_predict": NUM_PREDICT}
    }).encode()
    req = urllib.request.Request(
        OLLAMA_URL, data=payload,
        headers={"Content-Type": "application/json"}, method="POST"
    )
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            body = json.loads(resp.read().decode())
            return body.get("response", ""), time.time() - t0
    except Exception:
        return None, time.time() - t0


def get_available_models():
    try:
        with urllib.request.urlopen(TAGS_URL, timeout=5) as resp:
            data = json.loads(resp.read().decode())
            return [m["name"] for m in data.get("models", [])]
    except Exception as e:
        print(f"  ERROR connecting to Ollama: {e}")
        return []

# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------

def score_response(text, keywords):
    if not text:
        return 0.0
    tl = text.lower()
    kw_hits = sum(1 for k in keywords if k.lower() in tl) / max(len(keywords), 1)
    length_score = min(len(text) / 500, 1.0) * 0.3
    return round(min(kw_hits * 0.7 + length_score, 1.0), 3)

# ---------------------------------------------------------------------------
# EAT Phases
# ---------------------------------------------------------------------------

def evolve(samples, models, cycle_num):
    """EVOLVE: Test all models on a batch of samples."""
    batch_size = 10
    start = (cycle_num * batch_size) % max(len(samples), 1)
    batch = samples[start:start + batch_size]
    if len(batch) < batch_size:
        batch = samples[:batch_size]

    results = []
    for model in models:
        for s in batch:
            text, elapsed = query_model(model, s["q"])
            timeout = text is None
            sc = score_response(text, s["expected_keywords"]) if not timeout else 0.0
            results.append({
                "model": model,
                "category": s["category"],
                "score": sc,
                "time_sec": round(elapsed, 2),
                "timeout": timeout,
                "source": s["source"],
                "question": s["q"][:100],
            })
    return results


def absorb(results):
    """ABSORB: Identify weak categories and trends."""
    cat_scores = defaultdict(list)
    for r in results:
        cat_scores[r["category"]].append(r["score"])

    weaknesses = {}
    for cat in CATEGORIES:
        scores = cat_scores.get(cat, [])
        if not scores:
            continue
        avg = sum(scores) / len(scores)
        weaknesses[cat] = {
            "avg_score": round(avg, 3),
            "count": len(scores),
            "weak": avg < WEAK_THRESHOLD,
            "min_score": round(min(scores), 3),
            "max_score": round(max(scores), 3),
        }
    return weaknesses


def transform(weaknesses):
    """TRANSFORM: Generate targeted training prompts for weak categories."""
    improvements = []
    for cat, info in weaknesses.items():
        if not info["weak"]:
            continue
        prompts = generate_training_prompts(cat, info["avg_score"])
        improvements.extend(prompts)
    return improvements


def generate_training_prompts(category, current_score):
    """Generate targeted training data for a weak category."""
    templates = {
        "math": [
            {"q": "Solve: What is the derivative of x^3 + 2x^2 - 5x + 7?",
             "a": "Using the power rule: d/dx(x^3) = 3x^2, d/dx(2x^2) = 4x, d/dx(-5x) = -5, d/dx(7) = 0. The derivative is 3x^2 + 4x - 5."},
            {"q": "Calculate 15% of 240.",
             "a": "15% of 240 = 0.15 × 240 = 36."},
            {"q": "Simplify: (3x^2 * 4x^3) / (2x^4)",
             "a": "(3x^2 * 4x^3) / (2x^4) = (12x^5) / (2x^4) = 6x."},
            {"q": "What is the integral of 2x + 3?",
             "a": "The integral of 2x + 3 is x^2 + 3x + C, where C is the constant of integration."},
            {"q": "Factor: x^2 - 9",
             "a": "x^2 - 9 is a difference of squares. It factors as (x + 3)(x - 3)."},
        ],
        "code": [
            {"q": "Write a Python function to check if a string is a palindrome.",
             "a": "def is_palindrome(s):\n    s = s.lower().replace(' ', '')\n    return s == s[::-1]"},
            {"q": "Write a Python function to find the factorial of n using recursion.",
             "a": "def factorial(n):\n    if n <= 1:\n        return 1\n    return n * factorial(n - 1)"},
            {"q": "Write a Python function to flatten a nested list.",
             "a": "def flatten(lst):\n    result = []\n    for item in lst:\n        if isinstance(item, list):\n            result.extend(flatten(item))\n        else:\n            result.append(item)\n    return result"},
            {"q": "Write a Python function to find the most frequent element in a list.",
             "a": "from collections import Counter\n\ndef most_frequent(lst):\n    return Counter(lst).most_common(1)[0][0]"},
            {"q": "Write a Python function to merge two sorted lists.",
             "a": "def merge_sorted(a, b):\n    result = []\n    i = j = 0\n    while i < len(a) and j < len(b):\n        if a[i] <= b[j]:\n            result.append(a[i]); i += 1\n        else:\n            result.append(b[j]); j += 1\n    result.extend(a[i:])\n    result.extend(b[j:])\n    return result"},
        ],
        "reasoning": [
            {"q": "If all roses are flowers and some flowers fade quickly, can we conclude that some roses fade quickly?",
             "a": "No, we cannot conclusively determine that. The premise says SOME flowers fade quickly, but we don't know if those specific flowers include roses. This is a classic syllogistic fallacy."},
            {"q": "A farmer has 17 sheep. All but 9 die. How many are left?",
             "a": "9 sheep are left. 'All but 9' means 9 survive."},
            {"q": "If it takes 5 machines 5 minutes to make 5 widgets, how long would it take 100 machines to make 100 widgets?",
             "a": "5 minutes. Each machine makes 1 widget in 5 minutes. 100 machines would each make 1 widget in 5 minutes, producing 100 widgets total."},
            {"q": "You have two ropes. Each takes exactly 1 hour to burn, but burns at non-uniform rates. How do you measure 45 minutes?",
             "a": "Light rope 1 at both ends and rope 2 at one end simultaneously. Rope 1 burns out in 30 minutes. At that moment, light the other end of rope 2. It will take 15 more minutes to burn out, totaling 45 minutes."},
            {"q": "Three boxes are labeled 'Apples', 'Oranges', and 'Mixed'. All labels are wrong. You pick one fruit from the box labeled 'Mixed'. It's an apple. What are the contents of each box?",
             "a": "The box labeled 'Mixed' contains Apples (since all labels are wrong, it can't be mixed). The box labeled 'Oranges' must be Mixed (can't be oranges). The box labeled 'Apples' must be Oranges."},
        ],
        "sovereign": [
            {"q": "What is the maximum fine under GDPR for data breaches?",
             "a": "The maximum fine under GDPR is €20 million or 4% of annual global turnover, whichever is higher, for the most serious violations."},
            {"q": "Explain the EU AI Act risk classification system.",
             "a": "The EU AI Act classifies AI systems into four risk levels: unacceptable risk (banned), high risk (strict requirements), limited risk (transparency obligations), and minimal risk (no specific requirements). High-risk AI must meet requirements for data governance, transparency, human oversight, and accuracy."},
            {"q": "What is ISO 42001?",
             "a": "ISO 42001 is an international standard for AI management systems. It provides a framework for organizations to establish, implement, maintain, and continually improve their AI management systems, addressing governance, risk management, and ethical considerations."},
            {"q": "What are the key principles of data protection under GDPR?",
             "a": "GDPR's key principles include: lawfulness, fairness and transparency; purpose limitation; data minimization; accuracy; storage limitation; integrity and confidentiality; and accountability."},
            {"q": "What does 'human oversight' mean in the context of the EU AI Act?",
             "a": "Human oversight under the EU AI Act means that high-risk AI systems must be designed to allow effective human intervention. This includes the ability to understand system outputs, override decisions, and halt system operation when needed."},
        ],
        "knowledge": [
            {"q": "What is photosynthesis?",
             "a": "Photosynthesis is the process by which green plants and some other organisms convert light energy into chemical energy. Plants use sunlight, water, and carbon dioxide to produce glucose and oxygen."},
            {"q": "What is the capital of France and when was the Eiffel Tower built?",
             "a": "The capital of France is Paris. The Eiffel Tower was built in 1887-1889 for the 1889 World's Fair."},
            {"q": "Explain the theory of relativity in simple terms.",
             "a": "Einstein's theory of relativity has two parts: Special Relativity says the speed of light is constant for all observers, and time slows down at high speeds. General Relativity says gravity is the curvature of spacetime caused by mass."},
            {"q": "What are the three states of matter?",
             "a": "The three common states of matter are solid (fixed shape and volume), liquid (fixed volume, takes shape of container), and gas (no fixed shape or volume, expands to fill container)."},
            {"q": "Who wrote Romeo and Juliet?",
             "a": "Romeo and Juliet was written by William Shakespeare, believed to have been composed between 1591 and 1596."},
        ],
    }
    items = templates.get(category, [])
    return [{"category": category, "prompt": item, "reason": f"weak_score_{current_score:.2f}",
             "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S")} for item in items]

# ---------------------------------------------------------------------------
# Progress tracking
# ---------------------------------------------------------------------------

def load_progress():
    if PROGRESS_FILE.exists():
        with open(PROGRESS_FILE) as f:
            return json.load(f)
    return {
        "cycles_completed": 0,
        "total_samples_tested": 0,
        "category_history": {c: [] for c in CATEGORIES},
        "model_scores": {m: [] for m in MODELS},
        "weakness_log": [],
        "start_time": time.strftime("%Y-%m-%dT%H:%M:%S"),
    }


def save_progress(prog):
    with open(PROGRESS_FILE, "w") as f:
        json.dump(prog, f, indent=2)


def save_improvements(improvements):
    with open(IMPROVEMENTS_FILE, "a") as f:
        for imp in improvements:
            f.write(json.dumps(imp) + "\n")

# ---------------------------------------------------------------------------
# Display
# ---------------------------------------------------------------------------

def print_header():
    print("=" * 80)
    print("  EAT CONTINUOUS TRAINING LOOP")
    print("  Evolve → Absorb → Transform")
    print("=" * 80)


def print_cycle_header(cycle, models):
    print(f"\n{'─' * 80}")
    print(f"  CYCLE {cycle}  |  {len(models)} models  |  {time.strftime('%H:%M:%S')}")
    print(f"{'─' * 80}")


def print_evolve_results(results):
    cat_counts = defaultdict(int)
    cat_scores = defaultdict(list)
    model_scores = defaultdict(list)
    for r in results:
        cat_counts[r["category"]] += 1
        cat_scores[r["category"]].append(r["score"])
        model_scores[r["model"]].append(r["score"])

    print(f"\n  EVOLVE Results ({len(results)} tests):")
    print(f"  {'Category':<12} {'N':>3} {'Avg':>6} {'Min':>6} {'Max':>6}")
    print(f"  {'─' * 40}")
    for cat in CATEGORIES:
        if cat in cat_scores:
            s = cat_scores[cat]
            print(f"  {cat:<12} {len(s):>3} {sum(s)/len(s):>6.3f} {min(s):>6.3f} {max(s):>6.3f}")

    print(f"\n  {'Model':<28} {'Avg':>6} {'N':>3}")
    print(f"  {'─' * 40}")
    for model in sorted(model_scores.keys()):
        s = model_scores[model]
        print(f"  {model:<28} {sum(s)/len(s):>6.3f} {len(s):>3}")


def print_absorb_results(weaknesses):
    print(f"\n  ABSORB Analysis:")
    print(f"  {'Category':<12} {'Score':>6} {'Weak?':>6} {'Status'}")
    print(f"  {'─' * 40}")
    for cat in CATEGORIES:
        if cat in weaknesses:
            w = weaknesses[cat]
            status = "!! NEEDS WORK" if w["weak"] else "OK"
            print(f"  {cat:<12} {w['avg_score']:>6.3f} {'YES' if w['weak'] else 'no':>6} {status}")


def print_transform_results(improvements):
    if improvements:
        cats = defaultdict(int)
        for imp in improvements:
            cats[imp["category"]] += 1
        print(f"\n  TRANSFORM Generated {len(improvements)} training samples:")
        for cat, n in sorted(cats.items()):
            print(f"    {cat}: {n}")
    else:
        print(f"\n  TRANSFORM: No weak categories — all performing well!")

# ---------------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------------

def run_cycle(samples, models, cycle_num, prog):
    """Run one complete EAT cycle."""
    print_cycle_header(cycle_num, models)

    # EVOLVE
    print("\n  [EVOLVE] Testing models on samples...")
    evolve_results = evolve(samples, models, cycle_num)
    print_evolve_results(evolve_results)
    prog["total_samples_tested"] += len(evolve_results)

    # ABSORB
    weaknesses = absorb(evolve_results)
    print_absorb_results(weaknesses)

    # Update history
    for cat, info in weaknesses.items():
        prog["category_history"][cat].append({
            "cycle": cycle_num,
            "avg_score": info["avg_score"],
            "count": info["count"],
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        })

    for r in evolve_results:
        prog["model_scores"][r["model"]].append(r["score"])

    weak_cats = [c for c, i in weaknesses.items() if i["weak"]]
    if weak_cats:
        prog["weakness_log"].append({
            "cycle": cycle_num,
            "weak_categories": weak_cats,
            "scores": {c: weaknesses[c]["avg_score"] for c in weak_cats},
        })

    # TRANSFORM
    improvements = transform(weaknesses)
    print_transform_results(improvements)
    if improvements:
        save_improvements(improvements)

    prog["cycles_completed"] = cycle_num
    save_progress(prog)

    return len(improvements)


def print_summary(prog):
    """Print running summary."""
    print(f"\n{'=' * 80}")
    print(f"  RUNNING SUMMARY")
    print(f"{'=' * 80}")
    print(f"  Cycles completed: {prog['cycles_completed']}")
    print(f"  Total tests: {prog['total_samples_tested']}")
    print(f"  Start: {prog['start_time']}")

    print(f"\n  Category Trends (last 5):")
    for cat in CATEGORIES:
        history = prog["category_history"].get(cat, [])
        if history:
            recent = history[-5:]
            scores = [h["avg_score"] for h in recent]
            trend = "↑" if len(scores) > 1 and scores[-1] > scores[0] else "↓" if len(scores) > 1 and scores[-1] < scores[0] else "→"
            print(f"    {cat:<12} {scores[-1]:>6.3f} {trend}  ({len(history)} cycles)")

    print(f"\n  Model Performance (overall):")
    for model in MODELS:
        scores = prog["model_scores"].get(model, [])
        if scores:
            recent = scores[-50:]
            print(f"    {model:<28} avg={sum(recent)/len(recent):.3f}  n={len(scores)}")

    n_imp = 0
    if IMPROVEMENTS_FILE.exists():
        with open(IMPROVEMENTS_FILE) as f:
            n_imp = sum(1 for _ in f)
    print(f"\n  Improvement samples generated: {n_imp}")


def main():
    max_cycles = None
    for arg in sys.argv[1:]:
        if arg.startswith("--max-cycles="):
            max_cycles = int(arg.split("=")[1])

    print_header()

    # Check Ollama
    print("\n[INIT] Checking Ollama connection...")
    avail = get_available_models()
    if not avail:
        print("  FATAL: Cannot connect to Ollama at localhost:11434")
        sys.exit(1)
    print(f"  Available models: {len(avail)}")

    models = [m for m in MODELS if any(m.split(":")[0] in a for a in avail)]
    if not models:
        # Try exact matches
        models = [m for m in MODELS if m in avail]
    if not models:
        print(f"  WARN: None of the target models found. Trying all available.")
        models = avail[:4]
    print(f"  Active models: {models}")

    # Load data
    print("\n[INIT] Loading data...")
    corpus_samples = load_corpus(200)
    print(f"  Corpus samples: {len(corpus_samples)}")

    honey_samples = load_honey()
    print(f"  Honey samples: {len(honey_samples)}")

    all_samples = corpus_samples + honey_samples
    random.seed(42)
    random.shuffle(all_samples)
    print(f"  Total samples: {len(all_samples)}")

    cat_dist = defaultdict(int)
    for s in all_samples:
        cat_dist[s["category"]] += 1
    print(f"  Distribution:")
    for cat in CATEGORIES:
        print(f"    {cat:<12} {cat_dist.get(cat, 0):>4}")

    # Load progress
    prog = load_progress()
    if prog["cycles_completed"] > 0:
        print(f"\n[RESUME] Found previous progress: {prog['cycles_completed']} cycles, "
              f"{prog['total_samples_tested']} tests")

    # Run forever
    print(f"\n{'=' * 80}")
    print(f"  STARTING CONTINUOUS EAT LOOP  (Ctrl+C to stop)")
    print(f"{'=' * 80}")

    cycle = prog["cycles_completed"]
    try:
        while True:
            cycle += 1
            n_imp = run_cycle(all_samples, models, cycle, prog)

            # Print summary every 5 cycles
            if cycle % 5 == 0:
                print_summary(prog)

            # Brief pause between cycles
            time.sleep(2)

    except KeyboardInterrupt:
        print(f"\n\n{'=' * 80}")
        print(f"  EAT LOOP STOPPED (cycle {cycle})")
        print(f"{'=' * 80}")
        print_summary(prog)
        save_progress(prog)
        print(f"\n  Progress saved to: {PROGRESS_FILE}")
        print(f"  Improvements saved to: {IMPROVEMENTS_FILE}")
        print(f"{'=' * 80}")


if __name__ == "__main__":
    main()
