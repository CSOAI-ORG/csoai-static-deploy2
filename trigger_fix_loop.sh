#!/usr/bin/env bash
# trigger_fix_loop.sh — the AUTO fix cycle. The flywheel LEARNS on every pass,
# unattended. Every N hours: run measured-failures → real QLoRA → re-measure →
# promote-only-if-better on the 3090. SELF-GATING — a run that doesn't improve
# reverts (proven: overfit run REVERTED, tuned run PROMOTED +1.1pts). So it can
# run forever and only ever keep genuine, measured gains. Drift-resistant.
set -uo pipefail
POD_ID="${FIX_POD_ID:-fpowppss5ngtkw}"          # sov-repull (3090)
KEY="$HOME/.runpod/ssh/runpodctl-ssh-key"
TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)

INFO=$(runpodctl ssh info "$POD_ID" 2>/dev/null || true)
IP=$(printf '%s' "$INFO" | python3 -c "import sys,json;print(json.load(sys.stdin).get('ip',''))" 2>/dev/null || true)
PORT=$(printf '%s' "$INFO" | python3 -c "import sys,json;print(json.load(sys.stdin).get('port',''))" 2>/dev/null || true)
if [ -z "$IP" ] || [ -z "$PORT" ]; then echo "[$TS] fix pod unreachable — skip"; exit 0; fi

# don't stack runs — skip if a fix_loop is already grinding
if ssh -i "$KEY" -p "$PORT" -o StrictHostKeyChecking=no -o ConnectTimeout=20 root@"$IP" 'pgrep -f "[f]ix_loop.py" >/dev/null 2>&1'; then
  echo "[$TS] fix_loop already running — skip"; exit 0
fi
ssh -i "$KEY" -p "$PORT" -o StrictHostKeyChecking=no -o ConnectTimeout=25 root@"$IP" \
  "rm -f /workspace/fix_loop.log; nohup bash /workspace/fix_run.sh >/workspace/fix_loop.log 2>&1 & echo FIXCYCLE_\$!" 2>&1
echo "[$TS] fix cycle launched on $POD_ID"
