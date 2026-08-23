#!/usr/bin/env python3
"""F2 data flywheel generator v2 — expanded prompt bank (101 prompts).

v1 was stuck on 5 hardcoded prompts (2,647 rows, 5 unique). v2 loads the
estate's prompt bank (item banks + canon regulatory questions), samples a
rotating subset per batch, and produces genuinely new synth pairs.

Usage: python3 f2_gen_v2.py [target_rows] [--seed N]
"""
import json, hashlib, time, urllib.request, random, os, sys
OLLAMA = 'http://localhost:11434/api/generate'
OUT = '/workspace/f2/sovereign_synth.jsonl'
BANK = '/workspace/f2/prompt_bank.json'
os.makedirs(os.path.dirname(OUT), exist_ok=True)

TARGET = int(sys.argv[1]) if len(sys.argv) > 1 else 300
if '--seed' in sys.argv:
    random.seed(int(sys.argv[sys.argv.index('--seed') + 1]))

SPECS = [
    ('compliance', 'You are a precise regulatory compliance advisor. Cite exact articles and deadlines. Never guess.'),
    ('governance', 'You are an AI governance analyst. Map obligations across frameworks. Be deterministic.'),
    ('safety', 'You are an AI safety evaluator. Identify harms precisely. No hand-waving.'),
    ('provenance', 'You are a provenance auditor. Verify authenticity chains. Note what is UNMEASURED.'),
    ('index', 'You are an AI-economy index analyst. Produce signed, recomputable measurements.'),
    ('protocol', 'You are an agent-protocol conformance auditor. Test against the spec, not memory.'),
]

def load_bank():
    if os.path.exists(BANK):
        try:
            return json.load(open(BANK))
        except Exception:
            pass
    # fallback: the v1 prompts
    return [
        'What are the EU AI Act Article 50 obligations for synthetic content?',
        'Map the obligations for a high-risk AI system under Annex III.',
        'What must a deployer disclose under Article 13 transparency?',
        'How does C2PA provenance interact with Article 50 marking?',
        'What are the GDPR Article 22 implications for automated decisions?',
    ]

def ask(prompt: str) -> str:
    body = json.dumps({"model": "qwen3:4b", "prompt": prompt, "stream": False,
                       "options": {"temperature": 0.4}}).encode()
    try:
        req = urllib.request.Request(OLLAMA, data=body, headers={"Content-Type": "application/json"})
        return json.loads(urllib.request.urlopen(req, timeout=180).read()).get("response", "")
    except Exception:
        return ""

def main() -> int:
    bank = load_bank()
    # rotate: shuffle a working copy, cycle through
    pool = list(bank)
    random.shuffle(pool)
    count = 0
    with open(OUT, "a") as fh:
        i = 0
        while count < TARGET:
            prompt = pool[i % len(pool)]
            spec, sysp = SPECS[i % len(SPECS)]
            i += 1
            resp = ask(f"{sysp}\n\nQuestion: {prompt}")
            if not resp:
                continue
            rec = {"prompt": prompt, "response": resp, "family": spec,
                   "spec": sysp, "sigil": hashlib.sha256((spec + prompt).encode()).hexdigest()[:16],
                   "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ")}
            fh.write(json.dumps(rec) + "\n")
            fh.flush()
            count += 1
            if count % 20 == 0:
                print(f"[f2v2] {count}/{TARGET} rows", flush=True)
    print(f"[f2v2] DONE {count} rows from {len(bank)}-prompt bank", flush=True)
    return 0

if __name__ == "__main__":
    sys.exit(main())
