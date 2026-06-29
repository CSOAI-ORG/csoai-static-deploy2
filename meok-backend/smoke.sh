#!/usr/bin/env bash
# MEOK backend live smoke test — exercises every endpoint via real HTTP.
set -e
BASE=${BASE:-http://127.0.0.1:8765}
PY=python3

echo "=== /api/healthz ==="
curl -sS "$BASE/api/healthz"; echo

echo "=== /api/backend/status ==="
curl -sS "$BASE/api/backend/status"; echo

echo "=== /api/temples (head) ==="
curl -sS -o /tmp/m_temples.json "$BASE/api/temples"
$PY -c "import json; d=json.load(open('/tmp/m_temples.json')); print('count:', d['count']); print('first:', d['temples'][0]['code'], d['temples'][0]['name'])"

echo "=== /api/temple/uk ==="
curl -sS "$BASE/api/temple/uk"; echo

echo "=== /api/mcp/list ==="
curl -sS -o /tmp/m_mcps.json "$BASE/api/mcp/list"
$PY -c "import json; d=json.load(open('/tmp/m_mcps.json')); print('count:', d['count']); print('first:', d['mcps'][0])"

echo "=== /api/sov3/tools ==="
curl -sS -o /tmp/m_tools.json "$BASE/api/sov3/tools"
$PY -c "import json; d=json.load(open('/tmp/m_tools.json')); print('count:', d['count']); print('first 5:', d['tools'][:5])"

echo "=== /api/council/marcus ==="
curl -sS "$BASE/api/council/marcus"; echo

echo "=== /api/sigl/chain (head) ==="
curl -sS -o /tmp/m_chain.json "$BASE/api/sigl/chain"
$PY -c "import json; d=json.load(open('/tmp/m_chain.json')); print('length:', d['length']); print('entries:', len(d['entries'])); print('head:', d['head'])"

echo "=== /api/geo ==="
curl -sS "$BASE/api/geo"; echo

echo "=== /api/cascade/route_query (chat) ==="
curl -sS -X POST "$BASE/api/cascade/route_query" -H "Content-Type: application/json" -d '{"query":"hi","task_type":"chat"}'; echo

echo "=== /api/cascade/route_query (audit) ==="
curl -sS -X POST "$BASE/api/cascade/route_query" -H "Content-Type: application/json" -d '{"query":"x","task_type":"audit","config":{"force_tier":4}}'; echo

echo "=== /api/sigil/verify (head hash) ==="
HASH=$($PY -c "import json; print(json.load(open('/tmp/m_chain.json'))['entries'][0]['hash'])")
curl -sS -X POST "$BASE/api/sigil/verify" -H "Content-Type: application/json" -d "{\"hash\":\"$HASH\"}"; echo

echo "=== /api/sigil/verify (bad) ==="
curl -sS -X POST "$BASE/api/sigil/verify" -H "Content-Type: application/json" -d '{"hash":"deadbeef0000"}'; echo

echo "=== /api/news ==="
curl -sS -o /tmp/m_news.json "$BASE/api/news"
$PY -c "import json; d=json.load(open('/tmp/m_news.json')); print('count:', d['count']); [print(' -', n['headline'][:80]) for n in d['items']]"

echo "=== /api/ichar/create ==="
curl -sS -o /tmp/m_ichar.json -X POST "$BASE/api/ichar/create" -H "Content-Type: application/json" -d '{"user_id":"u1","name":"Tester","queen_model":"marcus","arcana_lens":0,"voice":"warm","cognition":"balanced","initial_message":"hi"}'
cat /tmp/m_ichar.json; echo
ICHAR_ID=$($PY -c "import json; print(json.load(open('/tmp/m_ichar.json'))['ichar_id'])")
echo "ICHAR_ID=$ICHAR_ID"

echo "=== /api/ichar/{id} ==="
curl -sS "$BASE/api/ichar/$ICHAR_ID"; echo

echo "=== /api/ichar/{id}/evolve ==="
curl -sS -X POST "$BASE/api/ichar/$ICHAR_ID/evolve" -H "Content-Type: application/json" -d '{"message":"ping"}'; echo

echo "=== /api/ichar/{id}/absorb ==="
curl -sS -X POST "$BASE/api/ichar/$ICHAR_ID/absorb" -H "Content-Type: application/json" -d '{"hive_gcp_vm":"meok-vm-7"}'; echo

echo "=== /api/ichar/user/u1 ==="
curl -sS "$BASE/api/ichar/user/u1" | $PY -c "import json,sys; d=json.load(sys.stdin); print('count:', d['count']); [print(' -', i['ichar_id'], i['name'], 'interactions:', i['interactions']) for i in d['ichars']]"

echo "=== /api/auth/signup ==="
curl -sS -X POST "$BASE/api/auth/signup" -H "Content-Type: application/json" -d '{"email":"smoke@meok.ai","password":"goodpass1","name":"Smoke"}'; echo

echo "=== /api/auth/login ==="
curl -sS -X POST "$BASE/api/auth/login" -H "Content-Type: application/json" -d '{"email":"smoke@meok.ai","password":"goodpass1"}'; echo

echo "=== /api/auth/login (bad pw) ==="
curl -sS -o /tmp/m_badlogin.json -w "HTTP=%{http_code}\n" -X POST "$BASE/api/auth/login" -H "Content-Type: application/json" -d '{"email":"smoke@meok.ai","password":"badpass"}'
cat /tmp/m_badlogin.json; echo

echo "=== /api/sov3/invoke ==="
curl -sS -X POST "$BASE/api/sov3/invoke" -H "Content-Type: application/json" -d '{"tool":"sov_route_query","args":{"q":"hi"}}'; echo

echo "=== /api/sov3/invoke (unknown) ==="
curl -sS -o /tmp/m_badtool.json -w "HTTP=%{http_code}\n" -X POST "$BASE/api/sov3/invoke" -H "Content-Type: application/json" -d '{"tool":"no_such_tool","args":{}}'
cat /tmp/m_badtool.json; echo

echo "=== /api/temple-os/bundle ==="
curl -sS -o /tmp/m_bundle.json "$BASE/api/temple-os/bundle"
$PY -c "import json; d=json.load(open('/tmp/m_bundle.json')); print('keys:', list(d.keys())); print('healthy:', d['status']['healthy']); print('mcp_count:', d['mcp_count']); print('sov3_tool_count:', d['sov3_tool_count']); print('temples:', len(d['temples'])); print('queens:', len(d['queens'])); print('arcana:', len(d['arcana'])); print('sigil_length:', d['sigil_length']); print('news_count:', d['news']['count'])"

echo "=== CORS preflight ==="
curl -sS -o /dev/null -w "HTTP=%{http_code}\n" -X OPTIONS "$BASE/api/backend/status" -H "Origin: https://meok.ai" -H "Access-Control-Request-Method: GET"

echo "=== ALL SMOKE TESTS PASSED ==="
