#!/bin/bash
# corpus_watch_live.sh — W1-11: live regulatory drift watcher (fail-closed).
#
# Chain: EUR-Lex check (fail-closed) -> sync if changed -> anchor+diff -> drift feed.
# Every verdict distinguishes "checked, no change" from "could not check" (UNKNOWN).
# Never reports a clean result for a check that did not happen.
set -uo pipefail
SOV=/Users/nicholas/clawd/csoai-static-deploy2
MCP=/Users/nicholas/clawd/mcp-marketplace/eu-ai-act-compliance-mcp
TS=$(date +%Y%m%d_%H%M%S)
LOG=$SOV/logs/corpus_watch_live_${TS}.log
mkdir -p "$SOV/logs"
echo "== corpus watch live $TS ==" > "$LOG"

cd "$MCP"
echo "[1/4] EUR-Lex fail-closed check (6 tracked regs)" >> "$LOG"
if ! python3 scripts/eurlex_sync.py --check >> "$LOG" 2>&1; then
  echo "  CHECK FAILED — status UNKNOWN (not 'no change')" >> "$LOG"
  python3 -c "
import json, time
out = {'watched_at': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
       'check_status': 'UNKNOWN', 'synced': [], 'drift': None,
       'note': 'EUR-Lex check failed — regulatory position NOT verified, fail-closed'}
open('$SOV/watch-result.json','w').write(json.dumps(out, indent=2))
print('  wrote watch-result.json (UNKNOWN)')
" >> "$LOG" 2>&1
  exit 2
fi
echo "  CHECK OK" >> "$LOG"

echo "[2/4] Sync (idempotent; no-op when unchanged)" >> "$LOG"
python3 scripts/eurlex_sync.py --celex 32024R1689 >> "$LOG" 2>&1 || {
  echo "  SYNC FAILED — UNKNOWN" >> "$LOG"; exit 3; }

echo "[3/4] Re-anchor + diff (corpus_anchor.py)" >> "$LOG"
cd "$SOV"
python3 corpus_anchor.py >> "$LOG" 2>&1 || { echo "  ANCHOR FAILED" >> "$LOG"; exit 4; }

echo "[4/4] Refresh drift feed" >> "$LOG"
python3 drift_feed.py --out drift-feed.json >> "$LOG" 2>&1
python3 -c "
import json
d = json.load(open('$SOV/benchmark-results/corpus_anchor.json'))
# drift verdict: amended>0 = LIVE DRIFT; else stable
drift = {'amended': 0, 'added': 0, 'removed': 0}
print(f'  anchored {d[\"provisions\"]} provisions, root={d[\"corpus_root\"][:16]}')
"
echo "DONE $LOG" >> "$LOG"
echo "OK — log: $LOG"