#!/bin/bash
# runpod-fleet-guardian.sh — keeps the RunPod fleet alive (P4, 2026-08-18).
# Mirrors the oracle-fleet-guardian pattern: if a pod whose desiredStatus is
# RUNNING stops answering its SSH probe, try `runpodctl start` to recover it.
# Runs via LaunchAgent (StartInterval ~900). Log: ~/clawd/_evacuation/logs/runpod-guardian.log
set -uo pipefail

export PATH="/opt/homebrew/bin:/usr/local/bin:$HOME/.local/bin:$PATH"
LOG="$HOME/clawd/_evacuation/logs/runpod-guardian.log"
mkdir -p "$(dirname "$LOG")"
TS() { date -u +%Y-%m-%dT%H:%M:%SZ; }
SSH_KEY="$HOME/.runpod/ssh/runpodctl-ssh-key"

# Pod registry: id|name|host|port (verified 2026-08-21 via runpodctl ssh info)
PODS=(
  "qdigrzjp5na1ek|sov-brain-a100-fresh-20260811|AUTO_RESOLVE|AUTO_RESOLVE"
  "fpowppss5ngtkw|sov-repull|194.26.196.156|23243"
  "l7g747oivyq6ab|sovos-light-master-mine|AUTO_RESOLVE|AUTO_RESOLVE"
)

echo "$(TS) runpod-fleet-guardian tick" >> "$LOG"

for entry in "${PODS[@]}"; do
  IFS='|' read -r pod_id pod_name pod_host pod_port <<< "$entry"
  # Resolve live endpoints (endpoints drift across restarts — 2026-08-20 lesson)
  if [ "$pod_host" = "AUTO_RESOLVE" ]; then
    info=$(runpodctl ssh info "$pod_id" 2>/dev/null)
    pod_host=$(echo "$info" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('ip',''))" 2>/dev/null)
    pod_port=$(echo "$info" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('port',''))" 2>/dev/null)
    [ -n "$pod_host" ] && [ -n "$pod_port" ] || { echo "$(TS) $pod_name endpoint unresolved (pod not ready)"; continue; }
  fi
  # SSH probe (BatchMode, short timeout)
  if ssh -i "$SSH_KEY" -p "$pod_port" -o ConnectTimeout=6 -o BatchMode=yes \
       -o StrictHostKeyChecking=accept-new root@"$pod_host" 'echo OK' 2>/dev/null | grep -q OK; then
    echo "$(TS) $pod_name OK (reachable)" >> "$LOG"
  else
    echo "$(TS) $pod_name UNREACHABLE — attempting runpodctl pod start $pod_id" >> "$LOG"
    if runpodctl pod start "$pod_id" >> "$LOG" 2>&1; then
      echo "$(TS) $pod_name start issued" >> "$LOG"
    else
      echo "$(TS) $pod_name start FAILED" >> "$LOG"
    fi
  fi
done

# Keep log small
tail -500 "$LOG" > "$LOG.tmp" && mv "$LOG.tmp" "$LOG"
