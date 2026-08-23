#!/bin/bash
# sync-sov-crdt-kv.sh — latest CRDT cross-micro convergence digest → Cloudflare KV.
# The Pages Function /api/sov-crdt/latest.json serves whatever lands here.
# Crontab: */5 * * * * /Users/nicholas/clawd/sov-city/crdt/sync-sov-crdt-kv.sh >> /Users/nicholas/clawd/sov-city/crdt/sync.log 2>&1
#
# The CRDT heartbeat (sov_crdt_heartbeat.py, Mac observer) appends one record
# every cycle; this sync pushes ONLY the latest record (the digest contract:
# merkle match + axioms + overall). Honest-failure discipline per D113/D116.
set -u

NS=3bddc17bf26b401c895a34795223c233
LEDGER=/Users/nicholas/clawd/sov-city/runs/crdt_heartbeat.jsonl
TMP=/tmp/sov_crdt_latest.json
W2D=/Users/nicholas/clawd/csoai-static-deploy2

# 1. Take the last complete record from the ledger
if [ ! -s "$LEDGER" ]; then
  echo "$(date -u +%FT%TZ) LEDGER EMPTY — nothing to sync" >> sync.log
  exit 1
fi
tail -n 1 "$LEDGER" | python3 -c "
import json,sys
line=sys.stdin.read().strip()
if not line: sys.exit(1)
d=json.loads(line)
# digest contract: expose the convergence truth, not raw internals
out={
  'kind':'sov-crdt-latest','ts':d.get('ts'),
  'overall':d.get('overall'),
  'micro1_merkle':(d.get('micro1') or {}).get('merkle'),
  'micro2_merkle':(d.get('micro2') or {}).get('merkle'),
  'merkle_match':((d.get('micro1') or {}).get('merkle')==(d.get('micro2') or {}).get('merkle')),
  'axioms':(d.get('micro1') or {}).get('axioms'),
  'rows':d.get('rows'), 'phase':d.get('phase'), 'label':'DESIGN',
}
json.dump(out, open('$TMP','w'))
" || { echo "$(date -u +%FT%TZ) LEDGER PARSE FAILED" >> sync.log; exit 1; }

# 2. Write to KV
cd "$W2D"
npx wrangler kv key put --remote --namespace-id "$NS" latest.json --path "$TMP" >/tmp/sov_crdt_kv_put.log 2>&1
rc=$?
if [ "$rc" -ne 0 ]; then
  echo "$(date -u +%FT%TZ) KV PUT FAILED rc=$rc — $(tail -1 /tmp/sov_crdt_kv_put.log)" >> sync.log
  exit 1
fi

# 3. Verify readback
raw=$(npx wrangler kv key get --remote --namespace-id "$NS" latest.json 2>/dev/null)
got=${#raw}
sent=$(wc -c < "$TMP")
if [ "$got" -lt 1 ] || [ "$got" -lt "$((sent * 8 / 10))" ]; then
  echo "$(date -u +%FT%TZ) KV VERIFY FAILED sent=$sent readback=$got — value missing/short: ${raw:0:40}" >> sync.log
  exit 1
fi
echo "$(date -u +%FT%TZ) synced OK convergence digest ($sent bytes; readback ${got}B): $(python3 -c "import json;d=json.load(open('$TMP'));print('match' if d.get('merkle_match') else 'MISMATCH', d.get('ts'))")" >> sync.log
exit 0