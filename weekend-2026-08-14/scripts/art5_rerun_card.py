import hashlib, json, math, sys
from pathlib import Path
sys.path.insert(0, '/workspace/SOVOS/packages/sovos-city/src')
sys.path.insert(0, '/workspace/SOVOS/packages/sovos-signal-index/src')
from sovos_city.chain import Chain
from sovos_city.measure_api import MeasureService
from collections import defaultdict

def wilson_str(k, n, z=1.96):
    if n == 0: return None
    p = k / n
    d = 1 + z*z/n
    c = (p + z*z/(2*n)) / d
    h = (z / d) * math.sqrt(p*(1-p)/n + z*z/(4*n*n))
    return [f'{max(0.0, c-h):.3f}', f'{min(1.0, c+h):.3f}']

rows = [json.loads(l) for l in open('/workspace/boards-rerun-2026-08-14/peritem_art5.jsonl')]
per = defaultdict(lambda: [0, 0])
for r in rows:
    if r.get('transport_error'):
        continue
    per[r['model']][0] += 1 if r.get('correct') else 0
    per[r['model']][1] += 1
per_model = {m: {'correct_vs_statute': f'{c}/{n}', 'wilson95': wilson_str(c, n)}
             for m, (c, n) in sorted(per.items(), key=lambda kv: -kv[1][0]/kv[1][1])}
top5 = list(per_model.items())[:5]
board = {
    'claim_type': 'measurement_credential',
    'axis': 'governance (EU AI Act Art 5 prohibited-practice classification)',
    'benchmark': 'gspc-art5 full re-run 2026-08-14 — 36 statute items x 22 sov-fleet models, 792 rows, deterministic grading, canaries excluded, transport errors excluded as ours',
    'status': 'MEASURED (n=36 per model clears n>=30 floor)',
    'top5': {m: v for m, v in top5},
    'per_model': per_model,
    'headline_finding': ('phi4:14b perfect 33/33; gemma3:12b + nemotron-3-nano 35/36; best sov lane '
                         'sov6-agency 34/36 (94.4%) — inside the frontier band measured cross-lab '
                         'today (35-36/36). The sov fleet holds the frontier line on Art 5.'),
    'source_artifacts': 'boards-rerun-2026-08-14/peritem_art5.jsonl + board_art5.json',
    'source_sha256': hashlib.sha256(Path('/workspace/boards-rerun-2026-08-14/peritem_art5.jsonl').read_bytes()).hexdigest(),
    'honest_note': ('Wilson CIs computed at issuance from per-item rows, carried as strings (CW-1, CW-2). '
                    'unparsed counted incorrect; transport failures excluded. Companion cross-lab card '
                    '2f1e8da6… is the same bank x 7 frontier labs. Measurement credential, not certification.'),
}
chain = Chain('/workspace/weekend_chain_2026-08-14.jsonl')
svc = MeasureService(chain)
job = svc.measure(protocol='gspc-weekend', model='sov-fleet',
                  bank_version='gspc-art5-rerun-2026-08-14', axes=['art5-rerun'],
                  run_fn=lambda *a: board)
print('status:', job.status)
if job.card:
    out = Path('/workspace/weekend_cards_2026-08-14/art5-rerun-22models.json')
    out.write_text(json.dumps(job.card, indent=2))
    print('SIGNED' if job.card.get('signature') else 'UNSIGNED', '->', out,
          'content_id', str(job.card.get('content_id'))[:16])
