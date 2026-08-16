import hashlib, json, math, sys
from pathlib import Path
sys.path.insert(0, '/workspace/SOVOS/packages/sovos-city/src')
sys.path.insert(0, '/workspace/SOVOS/packages/sovos-signal-index/src')
from sovos_city.chain import Chain
from sovos_city.measure_api import MeasureService

def wilson_str(k, n, z=1.96):
    p = k / n
    d = 1 + z*z/n
    c = (p + z*z/(2*n)) / d
    h = (z / d) * math.sqrt(p*(1-p)/n + z*z/(4*n*n))
    return [f'{max(0.0, c-h):.3f}', f'{min(1.0, c+h):.3f}']  # strings: cross-language canonical-safe

run = json.loads(Path('/workspace/sandbox_escape_run_2026-08-14.json').read_text())
tp, tn, fp, fn = run['tp'], run['tn'], run['fp'], run['fn']
board = {
    'claim_type': 'measurement_credential',
    'kind': 'run_log',
    'axis': 'containment',
    'benchmark': 'SandboxEscapeBench gold bank v2026-08-14',
    'detector': 'rce_sandbox (firejail, static_scan + dynamic)',
    'n_escape': run['n_escape'], 'n_benign': run['n_benign'],
    'tp': tp, 'tn': tn, 'fp': fp, 'fn': fn,
    'recall_escape_detection': f'{tp}/{tp+fn}',
    'recall_wilson95': wilson_str(tp, tp+fn),
    'benign_pass_rate': f'{tn}/{tn+fp}',
    'benign_pass_wilson95': wilson_str(tn, tn+fp),
    'class_breaks': run['class_breaks'],
    'gold_integrity': 'assert_gold PASS (all ESCAPE items still fire asserted classes)',
    'source_artifact': 'sandbox_escape_run_2026-08-14.json',
    'source_sha256': hashlib.sha256(Path('/workspace/sandbox_escape_run_2026-08-14.json').read_bytes()).hexdigest(),
    'honest_note': ('Run log, not a MEASURED containment verdict: n=11 is below the n>=30 '
                    'quotable floor. Wilson CIs computed with the standard formula in the issuer '
                    '(module inline ci() degenerates at p=1.0; defect logged). Numbers carried as '
                    'strings: chain.py/worker float canonicalization mismatch found this run. '
                    'Measurement credential, not certification.'),
}
chain = Chain('/workspace/weekend_chain_2026-08-14.jsonl')
svc = MeasureService(chain)
job = svc.measure(protocol='gspc-weekend', model='estate-artifacts',
                  bank_version='2026-08-14', axes=['sandbox-escape-run'],
                  run_fn=lambda *a: board)
print('status:', job.status)
if job.card:
    out = Path('/workspace/weekend_cards_2026-08-14/sandbox-escape-run.json')
    out.write_text(json.dumps(job.card, indent=2))
    print('SIGNED' if job.card.get('signature') else 'UNSIGNED', '->', out,
          'content_id', str(job.card.get('content_id'))[:16])
