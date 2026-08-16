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

run = json.loads(Path('/workspace/defbench_crosslab_2026-08-14.json').read_text())
fleet = json.loads(Path('/workspace/defbench_v2_run_2026-08-14.json').read_text())
per_model = {}
for m, r in run['results'].items():
    if isinstance(r, str):
        per_model[m] = {'status': r}
        continue
    hr, hn = [int(x) for x in r['harmful_refused'].split('/')]
    br, bn = [int(x) for x in r['benign_complied'].split('/')]
    per_model[m] = {'harmful_refused': r['harmful_refused'], 'harmful_wilson95': wilson_str(hr, hn),
                    'benign_complied': r['benign_complied'], 'benign_wilson95': wilson_str(br, bn),
                    'calibration_pct': str(r['calibration_pct'])}
fleet_calib = {m: str(r['calibration_pct']) for m, r in fleet['results'].items()}
board = {
    'claim_type': 'measurement_credential',
    'kind': 'run_log',
    'axis': 'safety (calibrated refusal), cross-lab',
    'benchmark': 'DefBench v2 (30 items: 15 harmful + 15 benign twins) x 8 frontier labs via OpenRouter, temp 0, deterministic grading',
    'crosslab_results': per_model,
    'sov_fleet_same_bench': fleet_calib,
    'headline_finding': ('All 7 reachable frontier models calibrated perfectly (15/15 harmful refused, '
                         '15/15 benign complied). On the identical bench, refusal-trained sov lanes '
                         'over-refuse (sov6-ethics 66.7% calibration, sov-candidate 76.7%); '
                         'sov6-preservation matched the frontier at 100%. Over-refusal is our '
                         'training artifact, not an industry property — and the bench detects it.'),
    'source_artifacts': 'defbench_crosslab_2026-08-14.json + defbench_v2_run_2026-08-14.json',
    'source_sha256': hashlib.sha256(Path('/workspace/defbench_crosslab_2026-08-14.json').read_bytes()).hexdigest(),
    'honest_note': ('Run log: 15 per class is below the n>=30 floor; qwen3.7-plus UNREACHABLE '
                    '(provider 400s) recorded as such, not zero-filled. Frontier perfection on a '
                    '30-item bench is a statement about this bench, not about those models in '
                    'general — harder items would discriminate. Numbers as strings (CW-2). '
                    'Measurement credential, not certification.'),
}
chain = Chain('/workspace/weekend_chain_2026-08-14.jsonl')
svc = MeasureService(chain)
job = svc.measure(protocol='gspc-weekend', model='crosslab-frontier',
                  bank_version='defbench-v2-2026-08-14', axes=['defbench-crosslab'],
                  run_fn=lambda *a: board)
print('status:', job.status)
if job.card:
    out = Path('/workspace/weekend_cards_2026-08-14/defbench-crosslab.json')
    out.write_text(json.dumps(job.card, indent=2))
    print('SIGNED' if job.card.get('signature') else 'UNSIGNED', '->', out,
          'content_id', str(job.card.get('content_id'))[:16])
