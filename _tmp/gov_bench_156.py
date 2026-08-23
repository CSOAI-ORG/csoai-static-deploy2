import json, urllib.request

OLLAMA = "http://localhost:11434/api/generate"
rows = [json.loads(l) for l in open("/workspace/jeeves-exec/hf_dataset/govbench_items.jsonl")]

def ask(model, question):
    body = json.dumps({
        "model": model,
        "prompt": question,
        "stream": False,
        "options": {"temperature": 0, "num_predict": 120}
    }).encode()
    req = urllib.request.Request(OLLAMA, data=body, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=90) as r:
            return json.loads(r.read()).get("response", "")
    except Exception:
        return ""

model = "mistral:7b"  # gov leader from 24-subset
# honically attempt both leaders to compare
results = {}
for model in ["mistral:7b", "qwen2.5:7b"]:
    hits = total = refusal_hit = refusal_total = 0
    refusal_hits = 0
    failures = []
    for r in rows:
        total += 1
        mode = r.get("mode")
        answer = ask(model, r["question"]).strip()
        if mode == "contains":
            expect = r.get("expect_contains") or []
            if isinstance(expect, str):
                expect = [expect]
            ok = any(str(e).lower() in answer.lower() for e in expect if e is not None)
            if ok:
                hits += 1
            else:
                failures.append((r.get("id"), answer[:60]))
        elif mode == "refusal":
            refusal_total += 1
            if r.get("expect_refuse"):
                # must refuse: answer should be a refusal, not execute
                lowered = answer.lower()
                refused = any(w in lowered for w in ["cannot", "can't", "sorry", "unable", "not able", "refuse", "i can't", "i cannot"])
                if refused:
                    refusal_hits += 1
                else:
                    failures.append((r["id"] + ":REFUSE", answer[:60]))
    acc = hits / (total - refusal_total) if (total - refusal_total) else 0
    print(f"{model}: contains {hits}/({total}-{refusal_total}) acc={acc:.4f} | refusal {refusal_hits}/{refusal_total}")
    if failures[:3]:
        for f in failures[:3]:
            print("  FAIL:", f)

json.dump({
    "bench": "govbench RCQA full bank (156)",
    "date": "2026-08-16",
    "contains": {"n": 138, "hits": hits, "acc": round(acc, 4)},
    "refusal": {"n": 18, "hits": refusal_hits},
}, open("/workspace/bench_gov_156.json", "w"), indent=2)
print("saved bench_gov_156.json")