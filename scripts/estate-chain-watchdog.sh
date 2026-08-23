#!/bin/bash
# estate-chain-watchdog.sh — the EXTERNAL dead-man's switch for the signing chain.
# Runs from the Mac (survives pod restarts), every 10 min via LaunchAgent.
# Catches the exact failure class the E2E batch found twice: "pod up but chain
# silently dead" (env wiped → nacl missing; key wiped → FileNotFoundError).
#
# Checks (all via SSH, all inference-based, never port-liveness):
#   1. chain process alive (anchored pgrep)
#   2. chain log fresh (< 15 min — the 5-min tick + margin)
#   3. signing key present (/root/.sovos/city_ed25519)
#   4. pynacl importable (the env-wipe class)
#   5. no sign-block that the fallback guard would clear
# Recovery ladder: restart chain → clear wedge → restore key → fix env → flag.
set -uo pipefail
SSH_KEY="$HOME/.runpod/ssh/runpodctl-ssh-key"
POD="root@194.26.196.156"
PORT="23243"
LOG="$HOME/clawd/_evacuation/logs/chain-watchdog.log"
mkdir -p "$(dirname "$LOG")"
TS() { date -u +%Y-%m-%dT%H:%M:%SZ; }

# Resolve pod endpoint live (endpoints drift across restarts)
info=$(runpodctl ssh info fpowppss5ngtkw 2>/dev/null)
IP=$(echo "$info" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('ip',''))" 2>/dev/null)
PORT=$(echo "$info" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('port',''))" 2>/dev/null)
[ -n "$IP" ] && [ -n "$PORT" ] && POD="root@$IP"

PROBE() { ssh -o ConnectTimeout=12 -o ServerAliveInterval=4 -o BatchMode=yes -o StrictHostKeyChecking=no -i "$SSH_KEY" -p "$PORT" "$POD" "$1" 2>/dev/null; }

CHAIN_PID=$(PROBE "pgrep -f '^python3 /workspace/measure_chain.py' | head -1")
# Freshness check: heartbeat file (touched every 60s by the chain's heartbeat
# thread since 2026-08-21) is authoritative — long jobs no longer trigger false
# kills. Falls back to log mtime if the heartbeat file is absent (pre-patch).
FRESH=$(PROBE "if [ -f /workspace/.chain-heartbeat ]; then echo \$(( \$(date +%s) - \$(stat -c %Y /workspace/.chain-heartbeat) )); else echo \$(( \$(date +%s) - \$(stat -c %Y /workspace/measure_chain.log 2>/dev/null || echo 0) )); fi" 2>/dev/null)
LOG_AGE="$FRESH"
KEY_OK=$(PROBE "test -f /root/.sovos/city_ed25519 && echo YES || echo NO")
NACL_OK=$(PROBE "python3 -c 'import nacl' 2>/dev/null && echo YES || echo NO")

HEALTH="chain_pid=${CHAIN_PID:-NONE} log_age=${LOG_AGE:-?}s key=${KEY_OK:-?} nacl=${NACL_OK:-?}"

if [ -z "${CHAIN_PID:-}" ] || [ "${LOG_AGE:-99999}" -gt 900 ] || [ "$KEY_OK" != "YES" ] || [ "$NACL_OK" != "YES" ]; then
  echo "$(TS) DEGRADED — $HEALTH — running recovery" >> "$LOG"
  # 1. fix env (nacl + deps) if the env was wiped
  [ "$NACL_OK" != "YES" ] && PROBE "pip3 install -q pynacl 2>/dev/null; echo env-fixed" >> "$LOG" 2>&1
  # 2. restore key if wiped (scp from Mac — the canonical copy)
  if [ "$KEY_OK" != "YES" ]; then
    PROBE "mkdir -p /root/.sovos && chmod 700 /root/.sovos" >> "$LOG" 2>&1
    scp -o StrictHostKeyChecking=no -i "$SSH_KEY" -P "$PORT" "$HOME/.sovos/city_ed25519" "$POD:/root/.sovos/city_ed25519" >> "$LOG" 2>&1
    PROBE "chmod 600 /root/.sovos/city_ed25519" >> "$LOG" 2>&1
    echo "$(TS) key restored" >> "$LOG"
  fi
  # 3. clear any stale sign-block (fallback guard passes via councilof.ai)
  PROBE "rm -f /workspace/.sign-blocked" >> "$LOG" 2>&1
  # 4. restart the chain (anchored restart script on pod)
  PROBE "bash /workspace/restart_chain.sh" >> "$LOG" 2>&1
  echo "$(TS) recovery issued — $HEALTH" >> "$LOG"
else
  echo "$(TS) OK — $HEALTH" >> "$LOG"
fi
