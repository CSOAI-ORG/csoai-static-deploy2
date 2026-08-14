#!/usr/bin/env python3
"""Agent-economy index — day-N signed observation of the live model market.

Pulls the public OpenRouter model catalog (no auth), computes supply and
price statistics, hashes the raw snapshot, and issues a signed gspc-card
on the SOVOS chain. This is day-1 of a daily series: the longitudinal
time-series is the moat (Part DK.3), so the raw snapshot is kept alongside
the card.

Doctrine: every number is a string (CW-2); the card is a measurement
credential, not a certification; the raw catalog hash lets anyone replay
the observation.
"""
import hashlib, json, statistics, sys, urllib.request
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, '/workspace/SOVOS/packages/sovos-city/src')
sys.path.insert(0, '/workspace/SOVOS/packages/sovos-signal-index/src')
from sovos_city.chain import Chain
from sovos_city.measure_api import MeasureService

CATALOG_URL = 'https://openrouter.ai/api/v1/models'
DATE = datetime.now(timezone.utc).strftime('%Y-%m-%d')
SNAPDIR = Path('/workspace/agent-economy-index')
SNAPDIR.mkdir(exist_ok=True)

req = urllib.request.Request(CATALOG_URL, headers={'User-Agent': 'csoai-index/0.1'})
raw = urllib.request.urlopen(req, timeout=60).read()
catalog = json.loads(raw)
sha = hashlib.sha256(raw).hexdigest()
snap_path = SNAPDIR / f'openrouter-catalog-{DATE}.json'
snap_path.write_bytes(raw)

models = catalog.get('data', [])
per_lab = {}
prompt_prices, completion_prices = [], []
free_models = 0
for m in models:
    lab = m.get('id', '?').split('/')[0]
    per_lab[lab] = per_lab.get(lab, 0) + 1
    pricing = m.get('pricing') or {}
    try:
        pp = float(pricing.get('prompt', '-1'))
        cp = float(pricing.get('completion', '-1'))
    except (TypeError, ValueError):
        continue
    if pp < 0 or cp < 0:
        continue  # dynamic/unpriced — excluded, noted
    if pp == 0 and cp == 0:
        free_models += 1
        continue  # free tier counted separately, not in price stats
    prompt_prices.append(pp * 1e6)       # $/Mtok
    completion_prices.append(cp * 1e6)   # $/Mtok

def stats(xs):
    if not xs:
        return None
    return {'n': str(len(xs)), 'min': f'{min(xs):.3f}', 'median': f'{statistics.median(xs):.3f}',
            'max': f'{max(xs):.3f}'}

top_labs = dict(sorted(per_lab.items(), key=lambda kv: -kv[1])[:12])

board = {
    'claim_type': 'measurement_credential',
    'index': 'agent-economy-index',
    'series_day': DATE,
    'observation': ('Daily signed snapshot of the public agent-economy supply side: '
                    'every model currently served on OpenRouter, its lab, and its listed price.'),
    'n_models_listed': str(len(models)),
    'n_labs': str(len(per_lab)),
    'models_per_lab_top12': {k: str(v) for k, v in top_labs.items()},
    'n_free_models': str(free_models),
    'input_price_usd_per_mtok': stats(prompt_prices),
    'output_price_usd_per_mtok': stats(completion_prices),
    'source': CATALOG_URL,
    'source_sha256': sha,
    'raw_snapshot': str(snap_path),
    'honest_note': ('Day-1 of a daily series — one observation is a point, not a trend; the value '
                    'is the accumulating longitudinal record, replayable from source_sha256. '
                    'Listed prices are a supply-side catalog view, not realized transaction prices. '
                    'Free-tier models counted separately; dynamic-priced models excluded. '
                    'Measurement credential, not certification. All numbers strings (CW-2).'),
}

chain = Chain('/workspace/weekend_chain_2026-08-14.jsonl')
svc = MeasureService(chain)
job = svc.measure(protocol='agent-economy-index', model='openrouter-catalog',
                  bank_version=f'catalog-{DATE}', axes=['agent-economy'],
                  run_fn=lambda *a: board)
print('status:', job.status)
if job.card:
    out = Path('/workspace/weekend_cards_2026-08-14') / f'agent-economy-index-{DATE}.json'
    out.write_text(json.dumps(job.card, indent=2))
    print('SIGNED' if job.card.get('signature') else 'UNSIGNED', '->', out,
          'content_id', str(job.card.get('content_id'))[:16])
    print('gate:', job.card.get('correctness_gate', {}).get('state'))
    print('time_anchor:', job.card.get('time_anchor', {}).get('state', 'n/a')
          if isinstance(job.card.get('time_anchor'), dict) else 'n/a')
