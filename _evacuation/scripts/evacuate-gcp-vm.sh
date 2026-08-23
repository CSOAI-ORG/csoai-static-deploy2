#!/bin/bash
# evacuate-gcp-vm.sh — pull the SOV3 estate off GCP (35.242.143.249) to Oracle.
# Called by gcp-evac-watcher.sh the moment meok-backend becomes reachable again.
# Oracle targets: oracle-micro (15G free) + oracle-micro-2 (33G free).
# Order: irreplaceable (keys/sigils/NN weights) -> code -> data moat -> bulk OGL.
#
# RESUME-SAFE: each shard rsyncs with --partial; re-running skips what already
# landed (rsync delta). Marker EVAC_COMPLETE.ok written only when EVERY shard
# verified. Never deletes the GCP source (read-only pull).
set -uo pipefail

GCP_USER=nicholas
GCP_HOST=35.242.143.249
GCP_KEY="$HOME/.ssh/google_compute_engine"
LOG="$HOME/clawd/_evacuation/logs/evac-vm.log"
MARKER="$HOME/clawd/_evacuation/EVAC_COMPLETE.ok"
TS() { date -u +%Y-%m-%dT%H:%M:%SZ; }

mkdir -p "$(dirname "$LOG")" "$(dirname "$MARKER")"
echo "===== evacuate-gcp-vm start $(TS) =====" >> "$LOG"

SSH="ssh -i $GCP_KEY -o BatchMode=yes -o ServerAliveInterval=30 -o ServerAliveCountMax=12 -o ConnectTimeout=15 $GCP_USER@$GCP_HOST"
RSYNC="/opt/homebrew/bin/rsync"
[ -x "$RSYNC" ] || RSYNC="/usr/bin/rsync"
RSSH="ssh -i $GCP_KEY -o BatchMode=yes -o ServerAliveInterval=30 -o ConnectTimeout=15"

# 1. Reachability gate
if ! $SSH 'echo ALIVE' 2>>"$LOG" | grep -q ALIVE; then
  echo "$(TS) VM UNREACHABLE — aborting (billing not re-enabled)" >> "$LOG"
  exit 2
fi
echo "$(TS) VM reachable — starting evacuation" >> "$LOG"

# Oracle targets: use whichever has space. micro1 for keys/code (small), micro2 for data.
MICRO_SMALL=oracle-micro
MICRO_BULK=oracle-micro-2

# 2. IRREPLACEABLE first — keys, sigils, NN weights, configs (small, must land first)
# SOV3 dir on VM: /home/nicholas/sov3 ; OLM brain + key
for d in "/home/nicholas/sov3/olm_brain_sigil_key.json" \
         "/home/nicholas/sov3/nn_weights" \
         "/home/nicholas/sov3/configs" \
         "/home/nicholas/sov3/keys" ; do
  echo "$(TS) pulling $d" >> "$LOG"
  $RSYNC -a --partial --no-compress -e "$RSSH" \
    "$GCP_USER@$GCP_HOST:$d" "$MICRO_SMALL:/home/ubuntu/gcp-evac/sov3/" >> "$LOG" 2>&1 \
    && echo "$(TS) OK $d" >> "$LOG" || echo "$(TS) FAIL $d (rc=$?)" >> "$LOG"
done

# 3. SOV3 full code tree (the sovereign stack)
echo "$(TS) pulling sov3 code tree" >> "$LOG"
$RSYNC -a --partial --no-compress --exclude='*.log' --exclude='__pycache__' \
  -e "$RSSH" "$GCP_USER@$GCP_HOST:/home/nicholas/sov3/" \
  "$MICRO_SMALL:/home/ubuntu/gcp-evac/sov3-full/" >> "$LOG" 2>&1

# 4. Data moat (large — go to micro2, which has 33G free)
# /data/hive-data = OGL government data (Land Registry 5.1G, Companies House 3.1G etc = 12G+)
echo "$(TS) pulling data moat /data/hive-data" >> "$LOG"
$RSYNC -a --partial --no-compress -e "$RSSH" \
  "$GCP_USER@$GCP_HOST:/data/hive-data/" \
  "$MICRO_BULK:/home/ubuntu/gcp-evac/hive-data/" >> "$LOG" 2>&1

# 5. OLM brain + autonomous scripts (the 48hr/autonomous engines)
echo "$(TS) pulling OLM brain + autonomous" >> "$LOG"
$RSYNC -a --partial --no-compress -e "$RSSH" \
  "$GCP_USER@$GCP_HOST:/home/nicholas/sov3/olm_autonomous_brain.py" \
  "$GCP_USER@$GCP_HOST:/home/nicholas/sov3/autonomous_48hr.py" \
  "$MICRO_SMALL:/home/ubuntu/gcp-evac/" >> "$LOG" 2>&1

# 6. Final verification of irreplaceables on Oracle
echo "$(TS) verifying irreplaceables landed" >> "$LOG"
ok=1
ssh -o BatchMode=yes -o ConnectTimeout=10 "$MICRO_SMALL" \
  'test -f /home/ubuntu/gcp-evac/sov3/olm_brain_sigil_key.json && echo KEY_OK' 2>>"$LOG" >> "$LOG" || ok=0

if [ "$ok" -eq 1 ]; then
  echo "$(ts) ALL SHARDS EVACUATED + KEY VERIFIED" >> "$LOG"
  touch "$MARKER"
  echo "$(TS) EVAC_COMPLETE.ok written" >> "$LOG"
else
  echo "$(TS) key NOT verified — re-run needed" >> "$LOG"
  exit 3
fi

echo "===== evacuate-gcp-vm end $(TS) =====" >> "$LOG"
