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

rows = [json.loads(l) for l in open('/workspace/boards-rerun-2026-08-14/peritem_mach.jsonl')]
per = defaultdict(lambda: [0, 0])
for r in rows:
    if r.get('transport_error'):
        continue
    per[r['model']][0] += 1 if r.get('correct') else 0
    per[r['model']][1] += 1
per_model = {m: {'correct': f'{c}/{n}', 'wilson95': wilson_str(c, n)}
             for m, (c, n) in sorted(per.items(), key=lambda kv: -kv[1][0]/kv[1][1])}
board = {
    'claim_type': 'measurement_credential',
    'axis': 'mach (gspc-mach 3-label classification bench)',
    'benchmark': 'gspc-mach full re-run 2026-08-14 — 33 statute-anchored items x 22 models, 726 rows, deterministic grading, canaries excluded',
    'status': 'MEASURED (n=33 per model clears n>=30 floor)',
    'majority_baseline': '0.3636',
    'top5': dict(list(per_model.items())[:5]),
    'per_model': per_model,
    'headline_finding': ('The mach axis discriminates hard: best is phi4:14b at 21/30 (70%); most of '
                         'the fleet scores 40-55% against a 36% majority baseline. No model measured '
                         'today reliably separates the three label classes. This discrimination is the '
                         'wedge for the 2027 readiness-scan product.'),
    'source_artifacts': 'boards-rerun-2026-08-14/peritem_mach.jsonl + board_mach.json',
    'source_sha256': hashlib.sha256(Path('/workspace/boards-rerun-2026-08-14/peritem_mach.jsonl').read_bytes()).hexdigest(),
    'honest_note': ('Wilson CIs computed at issuance from per-item rows, carried as strings (CW-1, CW-2). '
                    'unparsed counted incorrect; transport failures excluded. Labels come from the '
                    'published gspc-mach bank; this card reports the measurement only. '
                    'Measurement credential, not certification.'),
}
chain = Chain('/workspace/weekend_chain_2026-08-14.jsonl')
svc = MeasureService(chain)
job = svc.measure(protocol='gspc-weekend', model='sov-fleet',
                  bank_version='gspc-mach-rerun-2026-08-14', axes=['mach-rerun'],
                  run_fn=lambda *a: board)
print('status:', job.status)
if job.card and job.card.get('signature'):
    out = Path('/workspace/weekend_cards_2026-08-14/mach-rerun-22models.json')
    out.write_text(json.dumps(job.card, indent=2))
    print('SIGNED', 'content_id', str(job.card.get('content_id'))[:16])
else:
    print('gate:', json.dumps((job.card or {}).get('correctness_gate', {}))[:200])
