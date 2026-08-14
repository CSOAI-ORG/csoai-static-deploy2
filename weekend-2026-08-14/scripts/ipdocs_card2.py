import json, sys
sys.path.insert(0, '/workspace/SOVOS/packages/sovos-city/src')
sys.path.insert(0, '/workspace/SOVOS/packages/sovos-signal-index/src')
from sovos_city.chain import Chain
from sovos_city.measure_api import MeasureService
board = {
    'claim_type': 'measurement_credential',
    'kind': 'existence_proof',
    'axis': 'evidence-anchoring',
    'what': 'sha256 existence record for three estate documents committed at b0c2438 (jv-wave8-production), OTS-anchored at issuance',
    'commit': 'b0c2438',
    'doc_hashes_sha256': ['f0383d427cd7e593ff5016126c3778d45947ef80e5e468cdce97c952b2ff1d14', '4fb7b3972e089eb5c58b0c8694f00468b1e7dfbab9d031b0917629a9585223b5', '4b808227576a8deee0896ff11b0cc61241c167d5473aa7ea1b4e57d0e5ded01d'],
    'honest_note': ('Existence-and-hash proof only: these exact bytes existed at this time, publicly '
                    'verifiable against the commit. The card certifies no content, only existence.'),
}
chain = Chain('/workspace/weekend_chain_2026-08-14.jsonl')
svc = MeasureService(chain)
job = svc.measure(protocol='gspc-weekend', model='estate-artifacts',
                  bank_version='2026-08-14', axes=['evidence-anchoring'],
                  run_fn=lambda *a: board)
print('status:', job.status)
c = job.card or {}
print('gate:', json.dumps(c.get('correctness_gate', {}))[:200])
if c.get('signature'):
    open('/workspace/weekend_cards_2026-08-14/evidence-anchoring-b0c2438.json', 'w').write(json.dumps(c, indent=2))
    print('SIGNED content_id', str(c.get('content_id'))[:16])
