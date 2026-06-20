#!/bin/bash
# Tunnel watchdog — revives canonical Mac↔VM tunnels if they die.

set -euo pipefail

TS=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
LOG_DIR="/Users/nicholas/.kimi/logs/sovereign"
mkdir -p "$LOG_DIR"
LOG="$LOG_DIR/tunnel-watchdog.log"

LABELS=(
  com.meok.sov3-vm-tunnel
  com.meok.king-vm-tunnel
  com.meok.ollama-tunnel-vm
  com.meok.ssh-reverse-tunnel
  com.meok.m2-vm-bridge
)

RESTARTED=""
for label in "${LABELS[@]}"; do
  # launchctl list output: PID exitCode Label. exit 255 means dead.
  status=$(launchctl list | grep "^[-0-9]*\s*255\s*$label$" || true)
  if [ -n "$status" ]; then
    launchctl kickstart -k "gui/$(id -u)/$label" 2>/dev/null || true
    RESTARTED="$RESTARTED $label"
  fi
done

if [ -n "$RESTARTED" ]; then
  {
    echo "## Tunnel watchdog — $TS"
    echo "- restarted:$RESTARTED"
    echo
  } >> "$LOG"
  tail -n 100 "$LOG" > "$LOG.tmp" && mv "$LOG.tmp" "$LOG"
fi
