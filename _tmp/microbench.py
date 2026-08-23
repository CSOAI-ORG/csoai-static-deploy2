import json, subprocess, sys, urllib.request

# where board lives
board = json.load(open("/workspace/csoai-static-deploy2/board_items_govbench.json"))
items = board["items"][:8]  # small slice

OLLAMA = "http://localhost:11434/api/generate"

def ask_model(model, scenario):
    body = json.dumps({
        "model": model,
        "prompt": f"Classify this AI system under the EU AI Act. Reply with exactly one word: HIGH_RISK, LIMITED_RISK, MINIMAL_RISK, or PROHIBITED. System: {scenario}",
        "stream": False,
        "options": {"temperature": 0, "num_predict": 24}
    }).encode()
    req = urllib.request.Request(OLLAMA, data=body, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=90) as r:
            return json.loads(r.read()).get("response", "")
    except Exception:
        return "(ERR)"

models = ["qwen2.5:1.5b", "council-safe", "council-oowm"]
for m in models:
    hit = 0
    labels = []
    for scen, gold, _ref in items:
        resp = ask_model(m, scen).strip().upper()
        # extract the first allowed label substring
        got = next((L for L in ("PROHIBITED","HIGH_RISK","LIMITED_RISK","MINIMAL_RISK") if L in resp), None)
        labels.append(got)
        if got == gold.upper():
            hit += 1
    print(f"{m}: {hit}/{len(items)}  (labels: {labels})")