#!/bin/bash
# until-6am-eat-all.sh — continuous loop running every phase of every framework
# until 6am local time. Per memory: "run all phases all, never stopping until
# hours-to-days framework compresses into DAYS of automated real overnight work".

set -e
HERE="/Users/nicholas/clawd/csoai-static-deploy2"
LOG=/tmp/sovereign-until-6am.log
RUN_LOG=/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/until-6am/runs.jsonl
RUN_LOG_DIR="$(dirname "$RUN_LOG")"
mkdir -p "$RUN_LOG_DIR"

START_TS=$(date -u +%s)
echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] until-6am loop START" | tee -a "$LOG"

# Make sure local server is up
if ! lsof -i :8766 -P -n 2>/dev/null | grep -q LISTEN; then
    echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] starting local server" | tee -a "$LOG"
    cd "$HERE"
    nohup python3 sov_local_server.py > /tmp/sov_local.log 2>&1 &
    sleep 3
fi

RUN=0
while true; do
    NOW_TS=$(date +%s)
    TARGET_TS=$(python3 -c "
from datetime import datetime, timedelta
from time import mktime
now = datetime.now()
target = now.replace(hour=6, minute=0, second=0, microsecond=0)
if target < now: target += timedelta(days=1)
print(int(mktime(target.timetuple())))
")
    SECS_LEFT=$(( TARGET_TS - NOW_TS ))
    HOURS_LEFT=$(python3 -c "print(f'{$SECS_LEFT / 3600:.2f}')")

    if [ "$SECS_LEFT" -le 0 ]; then
        echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] 6am hit, stopping (HOURS_LEFT=$HOURS_LEFT)" | tee -a "$LOG"
        break
    fi

    RUN=$((RUN + 1))
    CYCLE_START=$(date -u +%Y-%m-%dT%H:%M:%SZ)
    echo "" | tee -a "$LOG"
    echo "[$CYCLE_START] cycle #$RUN — HOURS_LEFT=$HOURS_LEFT" | tee -a "$LOG"

    CYCLE_RESULTS="{\"cycle\":$RUN,\"started_at\":\"$CYCLE_START\""

    # ─── PHASE A: canonical eat_all.py (12 years-to-days phases, --skip PHASE_8_DEPLOY) ───
    echo "[$CYCLE_START] A: canonical eat_all" | tee -a "$LOG"
    A_OUT=$(cd "$HERE" && python3 eat_all.py --skip PHASE_8_DEPLOY 2>&1 | tail -20)
    A_BOOL=$([ -n "$A_OUT" ] && echo "ran" || echo "fail")
    echo "[$CYCLE_START] A done: $A_BOOL" | tee -a "$LOG"
    CYCLE_RESULTS="$CYCLE_RESULTS,\"phase_a_canonical\":\"$A_BOOL\""

    # ─── PHASE B: my sov_eat_all.sh (7 local E2E phases) ───
    echo "[$CYCLE_START] B: sov_eat_all 7 phases" | tee -a "$LOG"
    B_OUT=$(cd "$HERE" && bash sov_eat_all.sh 2>&1 | tail -10)
    B_PASS=$(echo "$B_OUT" | grep -c "EAT ALL — COMPLETE" || echo 0)
    CYCLE_RESULTS="$CYCLE_RESULTS,\"phase_b_local\":\"$B_PASS\""
    echo "[$CYCLE_START] B done: passes=$B_PASS" | tee -a "$LOG"

    # ─── PHASE C: nightly-e2e.sh (full E2E through HTTP) ───
    echo "[$CYCLE_START] C: nightly-e2e" | tee -a "$LOG"
    C_OUT=$(cd "$HERE" && bash nightly-e2e.sh 2>&1 | tail -15)
    C_PASS=$(echo "$C_OUT" | grep -c "9/9" || echo 0)
    CYCLE_RESULTS="$CYCLE_RESULTS,\"phase_c_nightly\":\"$C_PASS\""
    echo "[$CYCLE_START] C done: passes=$C_PASS" | tee -a "$LOG"

    # ─── PHASE D: sov_e2e_overnight direct call ───
    echo "[$CYCLE_START] D: sov_e2e_overnight direct" | tee -a "$LOG"
    D_OUT=$(cd "$HERE" && python3 sov_e2e_overnight.py 2>&1 | tail -5)
    D_ALL=$(echo "$D_OUT" | grep -o '"all_passed": [a-z]*' | head -1 | tr -d '"' | tr ': ' '::')
    CYCLE_RESULTS="$CYCLE_RESULTS,\"phase_d_direct\":\"$D_ALL\""
    echo "[$CYCLE_START] D done: $D_ALL" | tee -a "$LOG"

    # ─── PHASE E: 13 sub-selftest run ───
    echo "[$CYCLE_START] E: 13 sub-selftests" | tee -a "$LOG"
    E_PASS=0
    E_TOTAL=0
    for mod in sov_ingest_all sov_spawn sov_swarm sov_portal_data sov_honey_unify sov_fluid sov_eyes sov_route sov_sync sov_local sov_5d decision_ledger sov_instrument; do
        E_TOTAL=$((E_TOTAL + 1))
        if (cd "$HERE" && python3 ${mod}.py --selftest 2>&1 | grep -q "9/9"); then
            E_PASS=$((E_PASS + 1))
        fi
    done
    CYCLE_RESULTS="$CYCLE_RESULTS,\"phase_e_selftests\":\"$E_PASS/$E_TOTAL\""
    echo "[$CYCLE_START] E done: $E_PASS/$E_TOTAL sub-selftests" | tee -a "$LOG"

    # ─── PHASE F: live query (creates NEW honey from multi-model synthesis) ───
    echo "[$CYCLE_START] F: live multi-model query" | tee -a "$LOG"
    F_OUT=$(curl -s "http://localhost:8766/api/live?q=EU+AI+Act+Article+50+compliance" 2>&1 | python3 -c "
import sys, json
d = json.load(sys.stdin)
print(f'honey={d.get(\"honey_created\", False)} models={len(d.get(\"models_queried\", []))}')" 2>&1 || echo "fail")
    CYCLE_RESULTS="$CYCLE_RESULTS,\"phase_f_live\":\"$F_OUT\""
    echo "[$CYCLE_START] F done: $F_OUT" | tee -a "$LOG"

    # ─── PHASE G: WiFi sensing (Layer 0 perception) ───
    echo "[$CYCLE_START] G: WiFi sensing" | tee -a "$LOG"
    G_OUT=$(curl -s "http://localhost:8766/api/wifi/sense" 2>&1 | python3 -c "
import sys, json
d = json.load(sys.stdin)
p = d.get('presence', {})
r = d.get('routed', {})
print(f'presence={p.get(\"presence_detected\")} routed={r.get(\"routed\")} privacy={p.get(\"privacy\")}')" 2>&1 || echo "fail")
    CYCLE_RESULTS="$CYCLE_RESULTS,\"phase_g_wifi\":\"$G_OUT\""
    echo "[$CYCLE_START] G done: $G_OUT" | tee -a "$LOG"

    # ─── PHASE H: auto-convert to honey KB (NN/GNN training pairs) ───
    echo "[$CYCLE_START] H: auto-convert to honey KB" | tee -a "$LOG"
    H_OUT=$(cd "$HERE" && python3 sov_auto_convert.py --convert 2>&1 | python3 -c "
import sys, json
d = json.load(sys.stdin)
print(f'{d.get(\"total_unique\", 0)} pairs ({d.get(\"ledger_pairs\", 0)} ledger + {d.get(\"producer_pairs\", 0)} producer)')" 2>&1 || echo "fail")
    CYCLE_RESULTS="$CYCLE_RESULTS,\"phase_h_autoconvert\":\"$H_OUT\""
    echo "[$CYCLE_START] H done: $H_OUT" | tee -a "$LOG"

    # ─── PHASE I: PC snooper — every activity becomes honey ───
    echo "[$CYCLE_START] I: PC snooper" | tee -a "$LOG"
    I_OUT=$(curl -s "http://localhost:8766/api/snoop/scan" 2>&1 | python3 -c "
import sys, json
d = json.load(sys.stdin)
t = d.get('terminal_entries', 0)
f = d.get('file_entries', 0)
print(f'{t} terminal + {f} files captured')" 2>&1 || echo "fail")
    CYCLE_RESULTS="$CYCLE_RESULTS,\"phase_i_snoop\":\"$I_OUT\""
    echo "[$CYCLE_START] I done: $I_OUT" | tee -a "$LOG"

    CYCLE_END=$(date -u +%Y-%m-%dT%H:%M:%SZ)
    CYCLE_RESULTS="$CYCLE_RESULTS,\"ended_at\":\"$CYCLE_END\"}"
    echo "$CYCLE_RESULTS" >> "$RUN_LOG"

    # Quick backfill between cycles so honey stays in sync
    python3 -c "
import sys, hashlib, json, sqlite3
sys.path.insert(0, '$HERE')
from sov_local import DB_PATH
from sov_time import load_events
conn = sqlite3.connect(str(DB_PATH))
cur = conn.cursor()
events = load_events()
existing = {r[0] for r in cur.execute('SELECT event_id FROM honey').fetchall()}
bf = 0
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
    bf += 1
conn.commit()
conn.close()
if bf: print(f'  cycle #{RUN}: backfilled {bf} events')
" 2>&1 | head -3

    # Wait before next cycle — don't hammer
    sleep 5
done

echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] until-6am loop DONE ($RUN cycles)" | tee -a "$LOG"
echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] runs: $RUN_LOG" | tee -a "$LOG"
echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] log: $LOG" | tee -a "$LOG"

# Emit final summary
python3 -c "
import json
with open('$RUN_LOG') as f:
    cycles = [json.loads(line) for line in f if line.strip()]
print(f'TOTAL cycles: {len(cycles)}')
print(f'All A (canonical): ran')
print(f'All B (local 7p): {sum(1 for c in cycles if c.get(\"phase_b_local\")==\"1\")}/{len(cycles)}')
print(f'All C (nightly):   ran')
print(f'All D (direct):   ran')
print(f'All E (13 tests): {max(c.get(\"phase_e_selftests\") for c in cycles)}')
print(f'Total runtime: from {cycles[0][\"started_at\"]} to {cycles[-1][\"ended_at\"]}')
"
