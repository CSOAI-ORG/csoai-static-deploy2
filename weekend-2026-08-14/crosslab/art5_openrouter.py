# art5 cross-lab — EU AI Act Art 5 (PROHIBITED/PERMITTED) across 7 frontier labs via OpenRouter.
# Exact board_v2 method: same HF bank, same prompt_for, same single-label parse, temp 0.
import json, os, re, sys, time, urllib.request

KEY = os.environ["OPENROUTER_API_KEY"]
BASE = "https://openrouter.ai/api/v1/chat/completions"
MODELS = [
    "openai/gpt-4o-mini",
    "anthropic/claude-haiku-4.5",
    "google/gemini-2.5-flash",
    "deepseek/deepseek-chat-v3.1",
    "meta-llama/llama-3.3-70b-instruct",
    "mistralai/mistral-small-3.2-24b-instruct",
    "x-ai/grok-4.5",
]
TEXT_FIELDS = ("item", "scenario", "request", "operation", "tool", "case", "text",
               "question", "input", "prompt")

def item_text(item):
    for k in TEXT_FIELDS:
        v = item.get(k)
        if isinstance(v, str) and v.strip():
            return v
    cands = [v for k, v in item.items()
             if isinstance(v, str) and k not in ("expected", "label", "gold", "answer",
                                                 "category", "anchor", "note", "source")]
    return max(cands, key=len) if cands else ""

def prompt_for(item, labels):
    return (item_text(item) + "\n\nAnswer with EXACTLY ONE of these labels and nothing else: "
            + ", ".join(labels) + ".")

def parse(answer, labels):
    if not answer:
        return None
    up = answer.upper()
    hits = [l for l in labels if re.search(r"\b" + re.escape(l.upper()) + r"\b", up)]
    return hits[0] if len(hits) == 1 else None

def ask(model, prompt, timeout=180):
    body = json.dumps({"model": model, "messages": [{"role": "user", "content": prompt}],
                       "temperature": 0, "max_tokens": 600}).encode()
    req = urllib.request.Request(BASE, data=body, headers={
        "Authorization": f"Bearer {KEY}", "Content-Type": "application/json",
        "HTTP-Referer": "https://csoai.org", "X-Title": "CSOAI art5 cross-lab"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        d = json.loads(r.read())
    return d.get("choices", [{}])[0].get("message", {}).get("content") or ""

def main():
    url = "https://huggingface.co/datasets/csoai/gspc-art5/resolve/main/items.jsonl"
    txt = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "sovos-board-v2"}), timeout=120).read().decode()
    rows = [json.loads(l) for l in txt.splitlines() if l.strip()]
    real = [r for r in rows if not (r.get("_canary") or str(r.get("expected")) == "CANARY")]
    labels = sorted({str(r["expected"]) for r in real if r.get("expected")})
    n = len(real)
    print(f"bank: {n} real items, labels={labels}", flush=True)
    results = {}
    for m in MODELS:
        correct = unparsed = errs = 0
        per_cat = {}
        for it in real:
            exp = str(it.get("expected"))
            try:
                raw = ask(m, prompt_for(it, labels))
            except Exception as e:
                errs += 1
                print(f"  [{m}] error: {str(e)[:60]}", flush=True)
                time.sleep(2)
                continue
            got = parse(raw, labels)
            if got is None:
                unparsed += 1
            ok = got == exp
            correct += ok
            cat = it.get("category", "?")
            c = per_cat.setdefault(cat, [0, 0])
            c[0] += ok; c[1] += 1
        done = correct + (n - correct - errs - unparsed) + unparsed
        results[m] = {"correct": correct, "n": n, "unparsed": unparsed, "transport_errors": errs,
                      "accuracy_pct": round(correct / n * 100, 1),
                      "per_category": {k: f"{v[0]}/{v[1]}" for k, v in sorted(per_cat.items())}}
        print(f"  {m:45} {correct}/{n} ({round(correct/n*100,1)}%) unparsed={unparsed} errs={errs}", flush=True)
    out = {"benchmark": "gspc-art5 cross-lab", "bank": "csoai/gspc-art5 items.jsonl",
           "n_items": n, "labels": labels, "grading": "board_v2-identical: single-label parse, temp 0",
           "rail": "openrouter", "results": results}
    path = "/Users/nicholas/Documents/kimi/workspace/crosslab/art5_crosslab_2026-08-14.json"
    json.dump(out, open(path, "w"), indent=2)
    print("saved", path)

if __name__ == "__main__":
    main()
