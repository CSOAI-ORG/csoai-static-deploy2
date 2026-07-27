#!/usr/bin/env python3
"""
Extended EAT (Evolutionary Adversarial Testing) Cycle
Tests 5 Ollama models against 100 categorized reasoning samples.
Incrementally saves after each model. Uses only stdlib.
"""

import json, time, random, sys, re, os
import urllib.request, urllib.error
from pathlib import Path
from collections import defaultdict

OLLAMA_URL = "http://localhost:11434/api/generate"
TAGS_URL   = "http://localhost:11434/api/tags"
CORPUS     = Path(__file__).parent / "reasoning_corpus_5k.jsonl"
RESULTS    = Path(__file__).parent / "eat_extended_results.json"
TIMEOUT    = 25
N_SAMPLES  = 100
NUM_PREDICT = 256

MODELS = [
    "sov33-unified:latest",
    "sov33-unified-c4:latest",
    "sov33-evolved:latest",
    "sov33-strong-v2:latest",
    "qwen2.5:0.5b",
]

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

def classify(q):
    ql = q.lower()
    scores = {c: sum(1 for p in ps if re.search(p, ql)) for c, ps in CAT_PATTERNS.items()}
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "reasoning"

def load_samples(n=N_SAMPLES):
    with open(CORPUS) as f:
        lines = f.readlines()
    random.seed(42)
    random.shuffle(lines)
    out = []
    for line in lines:
        obj = json.loads(line)
        q, a = obj.get("q",""), obj.get("a","")
        if not q or not a: continue
        cat = classify(q)
        kws = [w for w in re.findall(r'\b\w{4,}\b', a[:300].lower())][:8]
        out.append({"q": q, "a": a[:500], "category": cat, "expected_keywords": kws,
                     "source_len": obj.get("tok_len",0)})
        if len(out) >= n: break
    return out

def query(model, prompt):
    payload = json.dumps({"model": model, "prompt": prompt, "stream": False,
                          "options": {"temperature": 0.2, "num_predict": NUM_PREDICT}}).encode()
    req = urllib.request.Request(OLLAMA_URL, data=payload,
                                 headers={"Content-Type": "application/json"}, method="POST")
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            body = json.loads(resp.read().decode())
            return body.get("response",""), time.time()-t0
    except:
        return None, time.time()-t0

def score(text, keywords):
    if not text: return 0.0
    tl = text.lower()
    kw = sum(1 for k in keywords if k.lower() in tl) / max(len(keywords),1)
    ln = min(len(text)/500, 1.0) * 0.3
    return round(min(kw*0.7 + ln, 1.0), 3)

def load_progress():
    if RESULTS.exists():
        with open(RESULTS) as f:
            return json.load(f)
    return {"models_done": {}, "samples": None}

def save_progress(data):
    with open(RESULTS, "w") as f:
        json.dump(data, f, indent=2)

def breakdown(results):
    cats = defaultdict(list)
    for r in results: cats[r["category"]].append(r)
    bd = {}
    for c, items in sorted(cats.items()):
        sc = [r["score"] for r in items]
        tm = [r["time_sec"] for r in items]
        bd[c] = {"count": len(items), "avg_score": round(sum(sc)/len(sc),3),
                 "avg_time": round(sum(tm)/len(tm),2), "max_score": max(sc),
                 "min_score": min(sc), "timeouts": sum(1 for r in items if r["timeout"])}
    return bd

def main():
    print("="*90)
    print("  EXTENDED EAT CYCLE — 5 Models × 100 Samples (incremental)")
    print("="*90)

    # Check Ollama
    print("\n[1/4] Checking Ollama...")
    try:
        with urllib.request.urlopen(TAGS_URL, timeout=5) as resp:
            avail = [m["name"] for m in json.loads(resp.read().decode()).get("models",[])]
    except Exception as e:
        print(f"ERROR: {e}"); sys.exit(1)

    models = [m for m in MODELS if m in avail]
    missing = [m for m in MODELS if m not in avail]
    if missing: print(f"  Missing: {missing}")
    print(f"  Testing {len(models)} models")

    # Load corpus
    print(f"\n[2/4] Loading {N_SAMPLES} samples...")
    prog = load_progress()
    if prog["samples"]:
        samples = prog["samples"]
        print(f"  Loaded from cache ({len(samples)} samples)")
    else:
        samples = load_samples()
        prog["samples"] = samples
        save_progress(prog)
    cc = defaultdict(int)
    for s in samples: cc[s["category"]] += 1
    for c, n in sorted(cc.items()): print(f"    {c:<12} {n:>3}")

    # Run
    print(f"\n[3/4] Running benchmarks...")
    total_start = time.time()
    done = set(prog["models_done"].keys())

    for model in models:
        if model in done:
            print(f"\n  SKIP {model} (already done, score={prog['models_done'][model]['overall_score']:.4f})")
            continue
        print(f"\n  {'━'*80}")
        print(f"  MODEL: {model}")
        print(f"  {'━'*80}")
        m_start = time.time()
        results = []
        for i, s in enumerate(samples):
            cat = s["category"]
            print(f"    [{i+1:3d}/{len(samples)}] {cat:<11} {s['q'][:58]}...", end="", flush=True)
            text, elapsed = query(model, s["q"])
            to = text is None
            sc = score(text, s["expected_keywords"]) if not to else 0.0
            print(f" {elapsed:5.1f}s {sc:.3f}" + (" TIMEOUT" if to else ""))
            results.append({"question": s["q"][:150], "category": cat, "time_sec": round(elapsed,2),
                            "score": sc, "response_length": len(text) if text else 0,
                            "response_preview": (text or "")[:200], "timeout": to})
        m_elapsed = time.time() - m_start
        bd = breakdown(results)
        overall = sum(r["score"] for r in results)/len(results)
        timeouts = sum(1 for r in results if r["timeout"])
        prog["models_done"][model] = {"results": results, "breakdown": bd,
                                       "overall_score": round(overall,4),
                                       "total_time": round(m_elapsed,1), "timeouts": timeouts,
                                       "avg_time": round(m_elapsed/len(results),2)}
        save_progress(prog)
        print(f"\n  → {model}: score={overall:.4f} time={m_elapsed:.0f}s timeouts={timeouts} [SAVED]")

    total_elapsed = time.time() - total_start

    # Summary
    print(f"\n\n{'='*90}")
    print("  EXTENDED EAT CYCLE — RESULTS SUMMARY")
    print(f"{'='*90}")
    print(f"  Time: {total_elapsed:.0f}s ({total_elapsed/60:.1f}min)  Models: {len(prog['models_done'])}")

    print(f"\n  {'─'*86}")
    print(f"  {'Model':<28} {'Category':<11} {'N':>3} {'AvgScr':>7} {'AvgTime':>8} {'TO':>3} {'MaxScr':>7}")
    print(f"  {'─'*86}")

    leaderboard = []
    for model, data in sorted(prog["models_done"].items()):
        scores_all = []
        for cat in sorted(data["breakdown"].keys()):
            bd = data["breakdown"][cat]
            print(f"  {model:<28} {cat:<11} {bd['count']:>3} {bd['avg_score']:>6.3f} "
                  f"{bd['avg_time']:>7.1f}s {bd['timeouts']:>3} {bd['max_score']:>6.3f}")
            scores_all.extend([bd["avg_score"]]*bd["count"])
        ov = sum(scores_all)/len(scores_all) if scores_all else 0
        print(f"  {'→ '+model:<28} {'OVERALL':<11} {len(scores_all):>3} {ov:>6.4f}")
        print()
        leaderboard.append((model, round(ov,4), data["avg_time"], data["timeouts"]))

    # Category winners
    cats_all = set()
    for d in prog["models_done"].values(): cats_all.update(d["breakdown"].keys())
    print(f"\n  {'='*86}")
    print("  CATEGORY WINNERS")
    print(f"  {'='*86}")
    for cat in sorted(cats_all):
        best_m, best_s = None, -1
        for m, d in prog["models_done"].items():
            s = d["breakdown"].get(cat,{}).get("avg_score",0)
            if s > best_s: best_s, best_m = s, m
        print(f"  {cat:<12} → {best_m:<32} ({best_s:.3f})")

    # Leaderboard
    leaderboard.sort(key=lambda x: x[1], reverse=True)
    print(f"\n  {'='*86}")
    print("  OVERALL LEADERBOARD")
    print(f"  {'='*86}\n")
    print(f"  {'Rank':<5} {'Model':<32} {'Score':>8} {'AvgTime':>9} {'TO':>3}")
    print(f"  {'─'*5} {'─'*32} {'─'*8} {'─'*9} {'─'*3}")
    for rank, (m, s, t, to) in enumerate(leaderboard, 1):
        star = " ★" if rank == 1 else ""
        print(f"  {rank:<5} {m:<32} {s:>7.4f} {t:>8.1f}s {to:>3}{star}")

    # Final save
    prog["summary"] = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "total_time_sec": round(total_elapsed,1),
        "leaderboard": [{"model":m,"score":s,"avg_time":t,"timeouts":to} for m,s,t,to in leaderboard],
    }
    save_progress(prog)
    print(f"\n  Results: {RESULTS}")
    print(f"\n{'='*90}")
    print("  EAT CYCLE COMPLETE")
    print(f"{'='*90}")

if __name__ == "__main__":
    main()
