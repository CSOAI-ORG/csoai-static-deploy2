#!/bin/bash
# oracle-fleet-guardian.sh — keeps the Always-Free Oracle fleet alive.
# Oracle force-stops idle micros (reclaim); this guardian detects STOPPED
# instances and starts them again. Runs via LaunchAgent every 15 min.
# Log: ~/clawd/_evacuation/logs/fleet-guardian.log
set -uo pipefail

export SUPPRESS_LABEL_WARNING=True
export PATH="$HOME/.local/bin:/opt/homebrew/bin:/usr/local/bin:$PATH"
LOG="$HOME/clawd/_evacuation/logs/fleet-guardian.log"
mkdir -p "$(dirname "$LOG")"
TENANCY=$(grep "^tenancy" "$HOME/.oci/config" | head -1 | cut -d= -f2)
TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)

INSTANCES=$(oci compute instance list --compartment-id "$TENANCY" --all \
  --query 'data[*].{name:"display-name",state:"lifecycle-state",id:id}' \
  --output json 2>/dev/null) || { echo "$TS ERROR oci list failed" >> "$LOG"; exit 1; }

echo "$INSTANCES" | python3 -c "
import json, sys, subprocess
ts = '$TS'
for inst in json.load(sys.stdin):
    name, state, ocid = inst['name'], inst['state'], inst['id']
    if state == 'STOPPED':
        r = subprocess.run(['oci', 'compute', 'instance', 'action',
                            '--action', 'START', '--instance-id', ocid],
                           capture_output=True, text=True)
        ok = r.returncode == 0
        print(f'{ts} START {name} -> {\"issued\" if ok else \"FAILED: \" + r.stderr.strip()[:120]}')
    elif state in ('RUNNING', 'STOPPING', 'STARTING'):
        pass  # healthy or in transition
    else:
        print(f'{ts} NOTE {name} state={state}')
" >> "$LOG" 2>&1

# Keep the log small (last 500 lines)
tail -500 "$LOG" > "$LOG.tmp" && mv "$LOG.tmp" "$LOG"
