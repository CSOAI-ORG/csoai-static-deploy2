#!/bin/bash
# gcp-evac-watcher.sh — pings meok-backend (35.242.143.249:22) every 5 min.
# If the VM becomes reachable again (owner re-enables billing), fires the
# full GCP→Oracle evacuation immediately via gcp-evac-watcher-inner.sh.
# Runs via com.meok.gcp-evac-watcher LaunchAgent (StartInterval=300, KeepAlive=false).
# Log: ~/clawd/_evacuation/logs/watcher.log
# Marker: ~/clawd/_evacuation/EVAC_COMPLETE.ok (written only on success)
#
# This is a guard for the 189GB data moat + OLM brain + SOV3 BFT on
# meok-backend. The VM is billing-gated since ~21 Jul 2026.
set -uo pipefail

TS=$(date +%Y-%m-%d\ %H:%M:%S)
LOG="$HOME/clawd/_evacuation/logs/watcher.log"
EVAC_SCRIPT="$HOME/clawd/_evacuation/scripts/evacuate-gcp-vm.sh"
MARKER="$HOME/clawd/_evacuation/EVAC_COMPLETE.ok"

# If evac already completed, stop pinging forever
if [ -f "$MARKER" ]; then
  echo "$TS EVAC_ALREADY_COMPLETE (marker present, watcher exiting)" >> "$LOG"
  exit 0
fi

# Quick SSH connectivity probe (BatchMode, short timeout, no command)
if ssh -o BatchMode=yes -o ConnectTimeout=8 -o StrictHostKeyChecking=accept-new \
       -i "$HOME/.ssh/google_compute_engine" \
       nicholas@35.242.143.249 'echo ALIVE' 2>/dev/null | grep -q ALIVE; then
  echo "$TS VM REACHABLE — firing evacuation" >> "$LOG"
  if [ -x "$EVAC_SCRIPT" ]; then
    "$EVAC_SCRIPT" 2>&1 | tee -a "$LOG"
    RC=${PIPESTATUS[0]}
    echo "$TS evacuate-gcp-vm.sh exit=$RC" >> "$LOG"
  else
    echo "$TS EVAC_SCRIPT_MISSING: $EVAC_SCRIPT does not exist or is not executable" >> "$LOG"
  fi
else
  echo "$TS VM still unreachable (billing gate stands)" >> "$LOG"
fi

# Keep log manageable: retain last 2000 lines
tail -2000 "$LOG" > "$LOG.tmp" && mv "$LOG.tmp" "$LOG"