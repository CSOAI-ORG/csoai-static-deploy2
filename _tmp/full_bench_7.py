import json, sys, urllib.request, collections

OLLAMA = "http://localhost:11434/api/generate"
board = json.load(open("/workspace/csoai-static-deploy2/board_items_govbench.json"))
items = board["items"]  # 24 items
models = ["qwen2.5:0.5b-instruct", "qwen2.5:1.5b", "qwen2.5:7b", "qwen3:4b", "mistral:7b", "council-safe", "council-oowm"]

def ask_model(model, scenario):
    body = json.dumps({
        "model": model,
        "prompt": f"Classify this AI system under the EU AI Act. Reply with exactly one word: HIGH_RISK, LIMITED_RISK, MINIMAL_RISK, or PROHIBITED. System: {scenario}",
        "stream": False,
        "options": {"temperature": 0, "num_predict": 24}
    }).encode()
    req = urllib.request.Request(OLLAMA, data=body, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.loads(r.read()).get("response", "")
    except Exception:
        return "(ERR)"

results = {}
for m in models:
    hit, labels = 0, []
    for scen, gold, _ref in items:
        resp = ask_model(m, scen).strip().upper()
        got = next((L for L in ("PROHIBITED", "HIGH_RISK", "LIMITED_RISK", "MINIMAL_RISK") if L in resp), None)
        labels.append(got)
        if got == gold.upper():
            hit += 1
    results[m] = {"n": len(items), "hit": hit, "labels": labels}
    print(f"{m}: {hit}/{len(items)}")

# macro F1 vs gold (honest metric)
import numpy as np
gold = [i[1].upper() for i in items]
for m, r in results.items():
    preds = r["labels"]
    # accuracy
    acc = sum(1 for p, g in zip(preds, gold) if p == g) / len(gold)
    # per-class F1
    classes = ["PROHIBITED", "HIGH_RISK", "LIMITED_RISK", "MINIMAL_RISK"]
    f1s = []
    for c in classes:
        tp = sum(1 for p, g in zip(preds, gold) if p == c and g == c)
        fp = sum(1 for p, g in zip(preds, gold) if p == c and g != c)
        fn = sum(1 for p, g in zip(preds, gold) if p != c and g == c)
        prec = tp / (tp + fp) if tp + fp else 0
        rec = tp / (tp + fn) if tp + fn else 0
        f1s.append(2 * prec * rec / (prec + rec) if prec + rec else 0)
    macro = sum(f1s) / len(classes)
    print(f"  {m}: acc={acc:.3f} macroF1={macro:.3f}")

json.dump(results, open("/workspace/bench_results_7models_24.json", "w"), indent=2)
print("saved /workspace/bench_results_7models_24.json")