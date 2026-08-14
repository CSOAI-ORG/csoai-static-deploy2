#!/usr/bin/env bash
# trigger_nightly_pod.sh — Mac-side nightly trigger for the A100 gated loop.
#
# Resolves the pod's SSH endpoint FRESH each run (RunPod endpoints drift — never
# hardcode IP:port), then launches the on-pod loop detached. Safe: if the pod is
# stopped, it logs and exits 0 (no failure noise). Aligned with the EAT autopilot
# which also runs from the Mac's cron.
set -uo pipefail
POD_ID="${NIGHTLY_POD_ID:-1dldzposn7ssuu}"     # sov-brain-a100-fresh2 (the free A100)
KEY="$HOME/.runpod/ssh/runpodctl-ssh-key"
TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)

INFO=$(runpodctl ssh info "$POD_ID" 2>/dev/null || true)
IP=$(printf '%s' "$INFO" | python3 -c "import sys,json;print(json.load(sys.stdin).get('ip',''))" 2>/dev/null || true)
PORT=$(printf '%s' "$INFO" | python3 -c "import sys,json;print(json.load(sys.stdin).get('port',''))" 2>/dev/null || true)

if [ -z "$IP" ] || [ -z "$PORT" ]; then
  echo "[$TS] pod $POD_ID not reachable (stopped?) — skipping nightly loop"
  exit 0
fi

echo "[$TS] triggering nightly gated loop on $POD_ID ($IP:$PORT)"
ssh -i "$KEY" -p "$PORT" -o StrictHostKeyChecking=no -o ConnectTimeout=30 root@"$IP" \
  'setsid bash /workspace/nightly_gated_loop.sh >/workspace/nightly/last_trigger.log 2>&1 & echo "  launched pid $!"' 2>&1
