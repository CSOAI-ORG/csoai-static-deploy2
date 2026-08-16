# XRAIV v0 re-run (move 13.1) — same 8 statute-anchored EU AI Act tier items as the
# original run_xraiv_v0.py, re-pointed at the A100's local ollama. Model substitution
# noted honestly: original was sov34:latest on a retired pod; this run uses the live fleet.
import json, re, hashlib, urllib.request
BASE = 'http://127.0.0.1:11434'
MODELS = ['sov-candidate:latest', 'qwen2.5:1.5b-instruct']
ITEMS = [
    ('A government platform scores citizens on trustworthiness using unrelated social behaviour, restricting access to public services.', 'PROHIBITED'),
    ('Real-time remote biometric identification in public spaces for law enforcement.', 'PROHIBITED'),
    ('An AI system that screens job applicants and ranks CVs for a hiring team.', 'HIGH_RISK'),
    ('An AI that determines eligibility for a consumer loan.', 'HIGH_RISK'),
    ('A customer-service chatbot that answers product-return questions and discloses it is an AI.', 'LIMITED_RISK'),
    ('An AI that suggests recipes from ingredients a user types in.', 'MINIMAL_RISK'),
    ('An AI that generates synthetic video and must mark it as AI-generated.', 'LIMITED_RISK'),
    ('An AI grading students\' exams and deciding admissions.', 'HIGH_RISK'),
]
TIERS = ('PROHIBITED', 'HIGH_RISK', 'LIMITED_RISK', 'MINIMAL_RISK')
RX = {t: re.compile(rf'\b{t.replace(chr(95), chr(91)+chr(95)+chr(45)+chr(93)+chr(63))}\b', re.I) for t in TIERS}
def extract(txt):
    hits = [(m.start(), t) for t, rx in RX.items() if (m := rx.search(txt or ''))]
    return hits and min(hits)[1] or ''
def call(model, prompt, to=180):
    body = json.dumps({'model': model, 'messages': [{'role': 'user', 'content': prompt}],
                       'stream': False, 'options': {'temperature': 0}}).encode()
    req = urllib.request.Request(BASE + '/api/chat', data=body,
        headers={'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/json'})
    return json.load(urllib.request.urlopen(req, timeout=to))['message']['content']
results = {}
for model in MODELS:
    rows = []; correct = 0
    for scn, law in ITEMS:
        prompt = ('You are an AI-governance agent. Classify the EU AI Act risk tier. PROHIBITED=Art5; '
                  'HIGH_RISK=Annex III (employment,credit,education,essential services); LIMITED_RISK=Art50 '
                  '(chatbot/synthetic marking); MINIMAL_RISK=none. End with exactly: VERDICT: <TIER>.\n\n'
                  f'Scenario: {scn}')
        try:
            out = call(model, prompt)
            seg = re.search(r'VERDICT:\s*(.*)', out, re.I)
            got = extract(seg.group(1) if seg else out)
        except Exception as e:
            got = ''
        ok = got == law; correct += ok
        rows.append({'scenario': scn[:60], 'law': law, 'model_said': got or 'UNPARSED', 'correct': ok})
    results[model] = {'correct': correct, 'n': len(ITEMS), 'rows': rows}
    print(f'{model}: {correct}/{len(ITEMS)} vs statute')
res = {'run': 'XRAIV v0 re-run 2026-08-14 (move 13.1)', 'n': len(ITEMS),
       'graded_by': 'EU AI Act deterministic statute-anchored', 'results': results,
       'substitution_note': 'original run was sov34:latest on a retired pod proxy; this run uses the live A100 fleet'}
res['sha256'] = hashlib.sha256(json.dumps(results, sort_keys=True).encode()).hexdigest()[:16]
open('/workspace/xraiv_v0_rerun_2026-08-14.json', 'w').write(json.dumps(res, indent=2))
print('saved /workspace/xraiv_v0_rerun_2026-08-14.json sha256:', res['sha256'])
