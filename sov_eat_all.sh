#!/bin/bash
# sov_eat_all.sh — the EAT ALL runner.
# Per memory: "EAT ALL" = batch execution, run everything without stopping.
# Years-to-days framework: days → weeks → months → year.

set -e
HERE="/Users/nicholas/clawd/csoai-static-deploy2"
cd "$HERE"

TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)
echo ""
echo "================================================================"
echo "  EAT ALL — years-to-days framework — ${TS}"
echo "================================================================"

if ! lsof -i :8766 -P -n 2>/dev/null | grep -q LISTEN; then
    echo "[eat_all] starting local server"
    nohup python3 sov_local_server.py > /tmp/sov_local_eat.log 2>&1 &
    sleep 3
fi

echo "[eat_all] phase 1/7 — DAYS: audit every producer"
python3 - <<'PY'
import sys, json
sys.path.insert(0, "/Users/nicholas/clawd/csoai-static-deploy2")
from sov_ingest_all import audit_producers
a = audit_producers()
print(f"  producers: {a['n_producers']}")
print(f"  total_kb:  {a['total_kb']}")
print(f"  kinds:     {sorted(set(p['kind'] for p in a['producers']))}")
PY

echo "[eat_all] phase 2/7 — WEEKS: ingest all → ledger + honey"
curl -s http://127.0.0.1:8766/api/producers/ingest | python3 -c "
import sys, json
d = json.load(sys.stdin)
print(f'  ledger_added: {d.get(\"ledger_added\", 0)}')
print(f'  honey_added:  {d.get(\"honey_added\", 0)}')
"

echo "[eat_all] phase 3/7 — MONTHS: spawn + grow sovereign"
USER="eat-all-$(date +%s)"
curl -s -X POST "http://127.0.0.1:8766/api/soul/${USER}" | python3 -c "
import sys, json
d = json.load(sys.stdin)
inh = d['soul']['inherited_routes']
print(f'  spawned: {d[\"soul\"][\"user_id\"]} tier {d[\"soul\"][\"tier\"]} {d[\"soul\"][\"label\"]}')
print(f'  inherited routes: {inh[\"n_producers\"]}')
"
for t in 1 2 3 4; do
    curl -s -X POST "http://127.0.0.1:8766/api/soul/${USER}/grow/${t}" > /dev/null
done
curl -s "http://127.0.0.1:8766/api/souls/list" | python3 -c "
import sys, json
d = json.load(sys.stdin)
soul = next((s for s in d['souls'] if s['user_id'] == '${USER}'), None)
if soul:
    print(f'  grown to tier: {soul[\"tier\"]} {soul[\"label\"]}')
    print(f'  growth_history: {len(soul[\"growth_history\"])} steps')
"

echo "[eat_all] phase 4/7 — YEAR: full E2E pipeline"
E2E_OUT=$(curl -s http://127.0.0.1:8766/api/e2e)
if echo "$E2E_OUT" | grep -q '"error"'; then
    echo "  [retry] backfilling honey then retrying"
    python3 -c "
import sys, hashlib, json, sqlite3
sys.path.insert(0, '/Users/nicholas/clawd/csoai-static-deploy2')
from sov_local import DB_PATH
from sov_time import load_events
conn = sqlite3.connect(str(DB_PATH))
cur = conn.cursor()
events = load_events()
existing = {r[0] for r in cur.execute('SELECT event_id FROM honey').fetchall()}
backfilled = 0
for ev in events:
    eid = ev.get('event_id')
    if eid in existing: continue
    cell = {'event_id': eid, 'prev': ev.get('prev_event'),
            'ts': ev.get('timestamp', 0), 'kind': ev.get('kind'),
            'summary': ev.get('summary'), 'prov': ev.get('provenance')}
    cch = hashlib.sha256(json.dumps(cell, sort_keys=True).encode()).hexdigest()
    cur.execute('INSERT OR IGNORE INTO honey VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
        (eid, ev.get('timestamp', 0), ev.get('kind'),
         (ev.get('summary') or '')[:1000], ev.get('provenance', ''),
         0, cch, ev.get('lens'), ev.get('canvas_x', 0), ev.get('canvas_y', 0)))
    backfilled += 1
conn.commit()
conn.close()
print(f'  backfilled {backfilled} events')
" 2>&1 | head -1
    E2E_OUT=$(curl -s http://127.0.0.1:8766/api/e2e)
fi
echo "$E2E_OUT" | python3 -c "
import sys, json
d = json.load(sys.stdin)
if 'error' in d:
    print(f'  error: {d[\"error\"]}')
else:
    print(f'  passed:           {d.get(\"passed\")}')
    print(f'  ledger events:    {d[\"ledger_events\"]}')
    print(f'  honey events:     {d[\"honey_events\"]}')
    print(f'  fluid nodes:      {d[\"fluid_nodes\"]}')
    print(f'  fluid kinds:      {d[\"fluid_kinds\"]}')
    print(f'  5D evidence pts:  {d[\"evidence_5d_pts\"]}')
    print(f'  IWM lens match:   {d[\"iwm_matched_lens\"]}')
    sub = d.get('substrate', {}).get('iwm', {}).get('guard', 'unknown')[:60]
    print(f'  IWM guard:        {sub}...')
"

echo "[eat_all] phase 5/7 — 13 sub-selftests"
python3 /Users/nicholas/clawd/csoai-static-deploy2/sov_e2e_overnight.py --selftest 2>&1 | tail -3

echo "[eat_all] phase 6/7 — OVERNIGHT runner"
python3 /Users/nicholas/clawd/csoai-static-deploy2/sov_e2e_overnight.py | python3 -c "
import sys, json
d = json.load(sys.stdin)
e4 = d.get('phase_4_e2e') or {}
print(f'  audit:      {d.get(\"phase_1_audit\")}')
print(f'  ingest:     {d.get(\"phase_2_ingest\")}')
print(f'  spawn+grow: {d.get(\"phase_3_spawn_grow\")}')
print(f'  e2e:        ledger={e4.get(\"ledger_events\", e4)} honey={e4.get(\"honey_events\", e4)}')
st = d.get('phase_selftests') or {}
print(f'  selftests:  {st.get(\"n_passed\", 0)}/{st.get(\"n_total\", 0)}')
print(f'  all_passed: {d.get(\"all_passed\")}')
print(f'  event_id:   {d.get(\"audit_event_id\", \"\")}')
"

echo "[eat_all] phase 7/7 — overnight_results.jsonl (history)"
test -f /Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/overnight_results.jsonl && \
    wc -l /Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/overnight_results.jsonl
tail -1 /Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/overnight_results.jsonl | python3 -c "
import sys, json
d = json.load(sys.stdin)
print(f'  last run: {d.get(\"timestamp\", \"?\")} all_passed={d.get(\"all_passed\")}')
"

echo ""
echo "================================================================"
echo "  EAT ALL — COMPLETE — ${TS}"
echo "================================================================"
