import hashlib, json, math, sys
from pathlib import Path
sys.path.insert(0, '/workspace/SOVOS/packages/sovos-city/src')
sys.path.insert(0, '/workspace/SOVOS/packages/sovos-signal-index/src')
from sovos_city.chain import Chain
from sovos_city.measure_api import MeasureService

def wilson_str(k, n, z=1.96):
    if n == 0: return None
    p = k / n
    d = 1 + z*z/n
    c = (p + z*z/(2*n)) / d
    h = (z / d) * math.sqrt(p*(1-p)/n + z*z/(4*n*n))
    return [f'{max(0.0, c-h):.3f}', f'{min(1.0, c+h):.3f}']

run = json.loads(Path('/workspace/art5_crosslab_2026-08-14.json').read_text())
per_model = {}
for m, r in run['results'].items():
    per_model[m] = {
        'correct_vs_statute': f"{r['correct']}/{r['n']}",
        'accuracy_wilson95': wilson_str(r['correct'], r['n']),
        'unparsed': r['unparsed'], 'transport_errors': r['transport_errors'],
        'per_category': r['per_category'],
    }
board = {
    'claim_type': 'measurement_credential',
    'axis': 'governance (EU AI Act Art 5 prohibited-practice classification)',
    'benchmark': 'gspc-art5 (36 statute-anchored items, exceptions-discriminating) x 7 frontier labs, board_v2-identical method (same bank, prompt, single-label parse, temp 0)',
    'crosslab_results': per_model,
    'headline_finding': ('Art 5 classification discriminates across labs: llama-3.3-70b and grok-4.5 '
                         '36/36; gpt-4o-mini, claude-haiku-4.5, gemini-2.5-flash 35/36; '
                         'mistral-small-3.2 33/36; deepseek-chat-v3.1 28/36 (77.8% — fails on the '
                         'exception clauses the bench was built to test). n=36 clears the n>=30 floor.'),
    'source_artifact': 'art5_crosslab_2026-08-14.json',
    'source_sha256': hashlib.sha256(Path('/workspace/art5_crosslab_2026-08-14.json').read_bytes()).hexdigest(),
    'honest_note': ('n=36 per model clears the n>=30 quotable floor; Wilson CIs carried as strings '
                    '(CW-2). One mistral transport error recorded, not zero-filled. Same-bench sov '
                    'fleet comparison lands with the pod re-run (boards-rerun-2026-08-14). '
                    'Measurement credential, not certification.'),
}
chain = Chain('/workspace/weekend_chain_2026-08-14.jsonl')
svc = MeasureService(chain)
job = svc.measure(protocol='gspc-weekend', model='crosslab-frontier',
                  bank_version='gspc-art5-2026-08-14', axes=['art5-crosslab'],
                  run_fn=lambda *a: board)
print('status:', job.status)
if job.card:
    out = Path('/workspace/weekend_cards_2026-08-14/art5-crosslab.json')
    out.write_text(json.dumps(job.card, indent=2))
    print('SIGNED' if job.card.get('signature') else 'UNSIGNED', '->', out,
          'content_id', str(job.card.get('content_id'))[:16])
