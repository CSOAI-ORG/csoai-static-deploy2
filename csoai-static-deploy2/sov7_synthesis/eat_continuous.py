#!/usr/bin/env python3
"""
EAT Continuous Training Loop (Evolve, Absorb, Transform)
Tests models, identifies weaknesses, generates targeted improvement data.
Usage: python3 eat_continuous.py [--max-cycles=N]
"""

import json, time, random, sys, re
import urllib.request, urllib.error
from pathlib import Path
from collections import defaultdict

BASE_DIR = Path(__file__).parent
OLLAMA_URL = "http://localhost:11434/api/generate"
TAGS_URL = "http://localhost:11434/api/tags"
HONEY_DIR = BASE_DIR.parent / "sov_space" / "honey_consolidated"
CORPUS_FILE = BASE_DIR / "reasoning_corpus_5k.jsonl"
IMPROVEMENTS_FILE = BASE_DIR / "eat_improvements.jsonl"
PROGRESS_FILE = BASE_DIR / "eat_progress.json"
RESULTS_FILE = BASE_DIR / "eat_cycle_results.json"
TIMEOUT = 30
NUM_PREDICT = 256

MODELS = [
    "sov33-evolved:latest",
    "sov33-strong:latest",
    "sov-sovereign-v3:latest",
    "qwen2.5:0.5b",
]

CATEGORIES = ["math", "code", "reasoning", "sovereign", "knowledge"]
WEAK_THRESHOLD = 0.7

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

TRAINING_TEMPLATES = {
    "math": [
        {"q": "Solve: What is the derivative of x^3 + 2x^2 - 5x + 7?",
         "a": "Using the power rule: d/dx(x^3)=3x^2, d/dx(2x^2)=4x, d/dx(-5x)=-5, d/dx(7)=0. Answer: 3x^2 + 4x - 5."},
        {"q": "Calculate 15% of 240.",
         "a": "15% of 240 = 0.15 x 240 = 36."},
        {"q": "Simplify: (3x^2 * 4x^3) / (2x^4)",
         "a": "(12x^5) / (2x^4) = 6x."},
        {"q": "What is the integral of 2x + 3?",
         "a": "x^2 + 3x + C, where C is the constant of integration."},
        {"q": "Factor: x^2 - 9",
         "a": "Difference of squares: (x + 3)(x - 3)."},
    ],
    "code": [
        {"q": "Write a Python function to check if a string is a palindrome.",
         "a": "def is_palindrome(s):\n    s = s.lower().replace(' ', '')\n    return s == s[::-1]"},
        {"q": "Write a Python function for factorial using recursion.",
         "a": "def factorial(n):\n    if n <= 1:\n        return 1\n    return n * factorial(n - 1)"},
        {"q": "Write a Python function to flatten a nested list.",
         "a": "def flatten(lst):\n    result = []\n    for item in lst:\n        if isinstance(item, list):\n            result.extend(flatten(item))\n        else:\n            result.append(item)\n    return result"},
        {"q": "Write a Python function to find the most frequent element.",
         "a": "from collections import Counter\n\ndef most_frequent(lst):\n    return Counter(lst).most_common(1)[0][0]"},
        {"q": "Write a Python function to merge two sorted lists.",
         "a": "def merge_sorted(a, b):\n    result, i, j = [], 0, 0\n    while i < len(a) and j < len(b):\n        if a[i] <= b[j]:\n            result.append(a[i]); i += 1\n        else:\n            result.append(b[j]); j += 1\n    result.extend(a[i:])\n    result.extend(b[j:])\n    return result"},
    ],
    "reasoning": [
        {"q": "If all roses are flowers and some flowers fade quickly, can we conclude some roses fade quickly?",
         "a": "No. The premise says SOME flowers fade quickly, but we don't know if those include roses. This is a syllogistic fallacy."},
        {"q": "A farmer has 17 sheep. All but 9 die. How many are left?",
         "a": "9 sheep are left. 'All but 9' means 9 survive."},
        {"q": "If 5 machines take 5 minutes to make 5 widgets, how long for 100 machines to make 100 widgets?",
         "a": "5 minutes. Each machine makes 1 widget in 5 minutes. 100 machines each make 1 in 5 min = 100 widgets."},
        {"q": "You have two ropes, each burns in 1 hour non-uniformly. Measure 45 minutes.",
         "a": "Light rope 1 at both ends and rope 2 at one end. Rope 1 burns out in 30 min. Light rope 2's other end. It burns out in 15 more min = 45 min total."},
        {"q": "Three boxes labeled Apples, Oranges, Mixed — all labels wrong. Pick from Mixed, get apple. What's in each?",
         "a": "Mixed box = Apples (can't be mixed). Oranges box = Mixed (can't be oranges). Apples box = Oranges."},
    ],
    "sovereign": [
        {"q": "What is the maximum fine under GDPR for data breaches?",
         "a": "€20 million or 4% of annual global turnover, whichever is higher."},
        {"q": "Explain the EU AI Act risk classification system.",
         "a": "Four levels: unacceptable (banned), high risk (strict requirements), limited risk (transparency), minimal risk (no requirements)."},
        {"q": "What is ISO 42001?",
         "a": "International standard for AI management systems — framework for governance, risk management, and ethical AI."},
        {"q": "What are the key GDPR data protection principles?",
         "a": "Lawfulness, purpose limitation, data minimization, accuracy, storage limitation, integrity/confidentiality, accountability."},
        {"q": "What does 'human oversight' mean in the EU AI Act?",
         "a": "High-risk AI must allow human intervention: understand outputs, override decisions, halt operation when needed."},
    ],
    "knowledge": [
        {"q": "What is photosynthesis?",
         "a": "Process by which plants convert light energy, water, and CO2 into glucose and oxygen."},
        {"q": "What is the capital of France and when was the Eiffel Tower built?",
         "a": "Paris. Eiffel Tower built 1887-1889 for the World's Fair."},
        {"q": "Explain special relativity simply.",
         "a": "Speed of light is constant for all observers. Time slows down at high speeds (time dilation)."},
        {"q": "What are the three states of matter?",
         "a": "Solid (fixed shape/volume), liquid (fixed volume, takes container shape), gas (expands to fill container)."},
        {"q": "Who wrote Romeo and Juliet?",
         "a": "William Shakespeare, composed between 1591 and 1596."},
    ],
}


def classify(text):
    tl = text.lower()
    scores = {}
    for cat, patterns in CAT_PATTERNS.items():
        scores[cat] = sum(1 for p in patterns if re.search(p, tl))
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "reasoning"


def generate_corpus():
    """Generate reasoning corpus from honey data."""
    samples = []
    if not HONEY_DIR.exists():
        print(f"  WARN: Honey dir not found: {HONEY_DIR}")
        return samples

    for jf in sorted(HONEY_DIR.glob("honey_*.jsonl")):
        with open(jf) as f:
            for line in f:
                try:
                    obj = json.loads(line)
                except Exception:
                    continue
                convs = obj.get("conversations", [])
                user_msg = ""
                asst_msg = ""
                for c in convs:
                    if c.get("from") == "user":
                        user_msg = c.get("value", "")
                    elif c.get("from") == "assistant":
                        asst_msg = c.get("value", "")
                if not user_msg or not asst_msg or len(asst_msg) < 20:
                    continue
                cat = classify(user_msg)
                kws = [w for w in re.findall(r'\b\w{4,}\b', asst_msg[:300].lower())][:8]
                samples.append({
                    "q": user_msg[:500],
                    "a": asst_msg[:500],
                    "category": cat,
                    "expected_keywords": kws,
                    "source": f"honey:{jf.stem}",
                })

    # Inject synthetic samples for underrepresented categories
    for cat, templates in TRAINING_TEMPLATES.items():
        for t in templates:
            kws = [w for w in re.findall(r'\b\w{4,}\b', t["a"][:300].lower())][:8]
            samples.append({
                "q": t["q"],
                "a": t["a"],
                "category": cat,
                "expected_keywords": kws,
                "source": "synthetic",
            })

    random.seed(42)
    random.shuffle(samples)
    return samples


def get_available_models():
    try:
        with urllib.request.urlopen(TAGS_URL, timeout=5) as resp:
            data = json.loads(resp.read().decode())
            return [m["name"] for m in data.get("models", [])]
    except Exception as e:
        print(f"  ERROR: {e}")
        return []


def query_model(model, prompt):
    payload = json.dumps({
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.2, "num_predict": NUM_PREDICT},
    }).encode()
    req = urllib.request.Request(
        OLLAMA_URL, data=payload,
        headers={"Content-Type": "application/json"}, method="POST",
    )
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            body = json.loads(resp.read().decode())
            return body.get("response", ""), time.time() - t0
    except Exception:
        return None, time.time() - t0


def score_response(text, keywords):
    if not text:
        return 0.0
    tl = text.lower()
    kw = sum(1 for k in keywords if k.lower() in tl) / max(len(keywords), 1)
    ln = min(len(text) / 500, 1.0) * 0.3
    return round(min(kw * 0.7 + ln, 1.0), 3)


# ── EAT Phases ───────────────────────────────────────────────────────────

def evolve(samples, models, cycle_num):
    """EVOLVE: test models on a batch of samples."""
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
            })
    return results


def absorb(results):
    """ABSORB: identify weak categories."""
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
    """TRANSFORM: generate training data for weak categories."""
    improvements = []
    for cat, info in weaknesses.items():
        if not info["weak"]:
            continue
        templates = TRAINING_TEMPLATES.get(cat, [])
        for t in templates:
            improvements.append({
                "category": cat,
                "prompt": t,
                "reason": f"weak_{cat}_score_{info['avg_score']:.2f}",
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
            })
    return improvements


# ── Persistence ──────────────────────────────────────────────────────────

def load_progress():
    if PROGRESS_FILE.exists():
        with open(PROGRESS_FILE) as f:
            return json.load(f)
    return {
        "cycles_completed": 0,
        "total_tests": 0,
        "category_history": {c: [] for c in CATEGORIES},
        "model_scores": {m: [] for m in MODELS},
        "weakness_log": [],
        "start_time": time.strftime("%Y-%m-%dT%H:%M:%S"),
    }


def save_progress(prog):
    with open(PROGRESS_FILE, "w") as f:
        json.dump(prog, f, indent=2)


def save_cycle_result(cycle, evolve_results, weaknesses, improvements):
    entry = {
        "cycle": cycle,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "evolve": {
            "total_tests": len(evolve_results),
            "by_model": {},
            "by_category": {},
        },
        "absorb": weaknesses,
        "transform_count": len(improvements),
    }
    model_groups = defaultdict(list)
    cat_groups = defaultdict(list)
    for r in evolve_results:
        model_groups[r["model"]].append(r["score"])
        cat_groups[r["category"]].append(r["score"])
    for m, scores in model_groups.items():
        entry["evolve"]["by_model"][m] = {
            "avg": round(sum(scores)/len(scores), 3),
            "n": len(scores),
        }
    for c, scores in cat_groups.items():
        entry["evolve"]["by_category"][c] = {
            "avg": round(sum(scores)/len(scores), 3),
            "n": len(scores),
        }

    all_results = []
    if RESULTS_FILE.exists():
        with open(RESULTS_FILE) as f:
            all_results = json.load(f)
    all_results.append(entry)
    with open(RESULTS_FILE, "w") as f:
        json.dump(all_results, f, indent=2)


def save_improvements(improvements):
    with open(IMPROVEMENTS_FILE, "a") as f:
        for imp in improvements:
            f.write(json.dumps(imp) + "\n")


# ── Display ──────────────────────────────────────────────────────────────

def print_banner():
    print("=" * 78)
    print("  EAT CONTINUOUS TRAINING LOOP")
    print("  Evolve -> Absorb -> Transform")
    print("=" * 78)


def print_cycle(cycle, models, results, weaknesses, improvements):
    print(f"\n{'─' * 78}")
    print(f"  CYCLE {cycle}  |  {len(models)} models  |  {time.strftime('%H:%M:%S')}")
    print(f"{'─' * 78}")

    # EVOLVE
    cat_groups = defaultdict(list)
    model_groups = defaultdict(list)
    for r in results:
        cat_groups[r["category"]].append(r["score"])
        model_groups[r["model"]].append(r["score"])

    print(f"\n  EVOLVE ({len(results)} tests):")
    print(f"  {'Category':<12} {'N':>3} {'Avg':>7} {'Min':>7} {'Max':>7}")
    print(f"  {'─' * 42}")
    for cat in CATEGORIES:
        if cat in cat_groups:
            s = cat_groups[cat]
            print(f"  {cat:<12} {len(s):>3} {sum(s)/len(s):>7.3f} {min(s):>7.3f} {max(s):>7.3f}")

    print(f"\n  {'Model':<28} {'Avg':>7} {'N':>3}")
    print(f"  {'─' * 42}")
    for model in sorted(model_groups.keys()):
        s = model_groups[model]
        print(f"  {model:<28} {sum(s)/len(s):>7.3f} {len(s):>3}")

    # ABSORB
    print(f"\n  ABSORB:")
    for cat in CATEGORIES:
        if cat in weaknesses:
            w = weaknesses[cat]
            flag = "!! WEAK" if w["weak"] else "OK"
            print(f"  {cat:<12} {w['avg_score']:>7.3f}  {flag}")

    # TRANSFORM
    if improvements:
        cats = defaultdict(int)
        for imp in improvements:
            cats[imp["category"]] += 1
        print(f"\n  TRANSFORM: {len(improvements)} training samples -> "
              + ", ".join(f"{c}:{n}" for c, n in sorted(cats.items())))
    else:
        print(f"\n  TRANSFORM: All categories above threshold")


def print_summary(prog):
    print(f"\n{'=' * 78}")
    print(f"  SUMMARY")
    print(f"{'=' * 78}")
    print(f"  Cycles: {prog['cycles_completed']}  |  Tests: {prog['total_tests']}  |  Since: {prog['start_time']}")

    print(f"\n  Category Trends (last 5 cycles):")
    for cat in CATEGORIES:
        hist = prog["category_history"].get(cat, [])
        if hist:
            recent = hist[-5:]
            scores = [h["avg_score"] for h in recent]
            trend = "up" if len(scores) > 1 and scores[-1] > scores[0] else \
                    "dn" if len(scores) > 1 and scores[-1] < scores[0] else "--"
            print(f"    {cat:<12} {scores[-1]:>7.3f} {trend}  ({len(hist)} cycles)")

    print(f"\n  Model Averages:")
    for model in MODELS:
        scores = prog["model_scores"].get(model, [])
        if scores:
            recent = scores[-50:]
            print(f"    {model:<28} {sum(recent)/len(recent):.3f}  (n={len(scores)})")

    n_imp = 0
    if IMPROVEMENTS_FILE.exists():
        with open(IMPROVEMENTS_FILE) as f:
            n_imp = sum(1 for _ in f)
    print(f"\n  Improvements generated: {n_imp}")


# ── Main ─────────────────────────────────────────────────────────────────

def main():
    max_cycles = None
    for arg in sys.argv[1:]:
        if arg.startswith("--max-cycles="):
            max_cycles = int(arg.split("=", 1)[1])

    print_banner()

    # Check Ollama
    print("\n[INIT] Checking Ollama...")
    avail = get_available_models()
    if not avail:
        print("  FATAL: Ollama not reachable at localhost:11434")
        sys.exit(1)
    print(f"  Available: {avail}")

    models = [m for m in MODELS if m in avail]
    if not models:
        models = [m for m in MODELS if any(m.split(":")[0] in a for a in avail)]
    if not models:
        models = avail[:4]
    print(f"  Active: {models}")

    # Generate corpus
    print("\n[INIT] Generating corpus from honey data...")
    samples = generate_corpus()
    print(f"  Total samples: {len(samples)}")

    dist = defaultdict(int)
    for s in samples:
        dist[s["category"]] += 1
    for cat in CATEGORIES:
        print(f"    {cat:<12} {dist.get(cat, 0):>4}")

    # Load progress
    prog = load_progress()
    if prog["cycles_completed"] > 0:
        print(f"\n[RESUME] {prog['cycles_completed']} cycles, {prog['total_tests']} tests done")

    # Run
    print(f"\n{'=' * 78}")
    print(f"  STARTING EAT LOOP  (Ctrl+C to stop)")
    if max_cycles:
        print(f"  Max cycles: {max_cycles}")
    print(f"{'=' * 78}")

    cycle = prog["cycles_completed"]
    try:
        while True:
            if max_cycles and cycle >= max_cycles:
                print(f"\n  Reached max cycles ({max_cycles}), stopping.")
                break

            cycle += 1
            results = evolve(samples, models, cycle)
            weaknesses = absorb(results)
            improvements = transform(weaknesses)

            # Update progress
            prog["total_tests"] += len(results)
            for cat, info in weaknesses.items():
                prog["category_history"][cat].append({
                    "cycle": cycle,
                    "avg_score": info["avg_score"],
                    "count": info["count"],
                    "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
                })
            for r in results:
                prog["model_scores"][r["model"]].append(r["score"])
            weak_cats = [c for c, i in weaknesses.items() if i["weak"]]
            if weak_cats:
                prog["weakness_log"].append({
                    "cycle": cycle,
                    "weak": weak_cats,
                    "scores": {c: weaknesses[c]["avg_score"] for c in weak_cats},
                })

            prog["cycles_completed"] = cycle
            save_progress(prog)
            save_cycle_result(cycle, results, weaknesses, improvements)
            if improvements:
                save_improvements(improvements)

            print_cycle(cycle, models, results, weaknesses, improvements)

            if cycle % 5 == 0:
                print_summary(prog)

            time.sleep(1)

    except KeyboardInterrupt:
        print(f"\n\n{'=' * 78}")
        print(f"  STOPPED at cycle {cycle}")
        print(f"{'=' * 78}")
        print_summary(prog)
        save_progress(prog)
        print(f"\n  Saved: {PROGRESS_FILE}")
        print(f"  Saved: {RESULTS_FILE}")
        print(f"  Saved: {IMPROVEMENTS_FILE}")
        print(f"{'=' * 78}")


if __name__ == "__main__":
    main()
