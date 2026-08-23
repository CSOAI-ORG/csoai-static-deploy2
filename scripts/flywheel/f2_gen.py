#!/usr/bin/env python3
"""F2 data flywheel generator — runs on the 3090 pod via SSH."""
import json, hashlib, time, urllib.request, random, os, sys
OLLAMA = 'http://localhost:11434/api/generate'
OUT = '/workspace/f2/sovereign_synth.jsonl'
os.makedirs(os.path.dirname(OUT), exist_ok=True)
batch = int(sys.argv[1]) if len(sys.argv) > 1 else 100
SPECS = [
    ('compliance', 'You are a precise regulatory compliance advisor. Cite exact articles and deadlines. Never guess.'),
    ('governance', 'You are an AI governance analyst. Map obligations across frameworks. Be deterministic.'),
    ('safety', 'You are an AI safety evaluator. Identify harms precisely. No hand-waving.'),
    ('provenance', 'You are a provenance auditor. Verify authenticity chains. Note what is UNMEASURED.'),
]
PROMPTS = [
    'What are the EU AI Act Article 50 obligations for synthetic content?',
    'Map the obligations for a high-risk AI system under Annex III.',
    'What must a deployer disclose under Article 13 transparency?',
    'How does C2PA provenance interact with Article 50 marking?',
    'What are the GDPR Article 22 implications for automated decisions?',
]
count = 0
for spec, sysp in SPECS:
    for i in range(max(1, batch // len(SPECS))):
        prompt = random.choice(PROMPTS)
        body = json.dumps({'model':'qwen3:4b','prompt':f'{sysp}\nQ: {prompt}\nA:','stream':False,'options':{'temperature':0.3}}).encode()
        try:
            req = urllib.request.Request(OLLAMA, data=body, headers={'Content-Type':'application/json'})
            resp = json.loads(urllib.request.urlopen(req, timeout=180).read())
            answer = resp.get('response','').strip()
            row = {'prompt':prompt,'response':answer,'spec':spec,'source':'f2-3090-qwen3-4b','ts':time.strftime('%Y-%m-%dT%H:%M:%SZ'),'sigil':hashlib.sha256((prompt+answer).encode()).hexdigest()[:16]}
            with open(OUT,'a') as f:
                f.write(json.dumps(row)+'\n')
            count += 1
            print(f'  [{spec}] {count} rows', flush=True)
        except Exception as e:
            print(f'ERR {spec} {i}: {e}', flush=True)
print(f'DONE: {count} rows appended to {OUT}')
