#!/usr/bin/env bash
# trigger_3090_sims.sh — keep the small pod (3090) AUTOMATICALLY eating sims.
#
# Cron'd hourly on the Mac. Resolves the pod's SSH endpoint fresh each run
# (RunPod endpoints drift), checks whether the sim_burst loop is alive, and
# relaunches it if it stopped (8h burst ended, pod restarted, crash). This is
# the "it has to be automatic" keeper — the 3090 churns city+jail sim data
# toward the flywheel/3KB continuously, healing itself, no manual relaunch.
set -uo pipefail
POD_ID="${SIM_POD_ID:-fpowppss5ngtkw}"          # sov-repull (3090)
KEY="$HOME/.runpod/ssh/runpodctl-ssh-key"
TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)

INFO=$(runpodctl ssh info "$POD_ID" 2>/dev/null || true)
IP=$(printf '%s' "$INFO" | python3 -c "import sys,json;print(json.load(sys.stdin).get('ip',''))" 2>/dev/null || true)
PORT=$(printf '%s' "$INFO" | python3 -c "import sys,json;print(json.load(sys.stdin).get('port',''))" 2>/dev/null || true)
if [ -z "$IP" ] || [ -z "$PORT" ]; then
  echo "[$TS] 3090 $POD_ID unreachable (stopped?) — skip"
  exit 0
fi

# [s]im_burst.sh regex-bracket trick avoids pgrep self-matching its own cmdline.
ssh -i "$KEY" -p "$PORT" -o StrictHostKeyChecking=no -o ConnectTimeout=30 root@"$IP" '
  export PATH=/usr/local/bin:/usr/bin:$PATH
  if pgrep -f "[s]im_burst.sh" >/dev/null 2>&1; then
    echo "  sim_burst alive ($(wc -l < /workspace/sims/history.log 2>/dev/null || echo 0) rounds done)"
  else
    cd /workspace
    curl -sf 127.0.0.1:11434/api/tags >/dev/null 2>&1 || {
      setsid bash -c "env OLLAMA_HOST=0.0.0.0 OLLAMA_MODELS=/workspace/ollama ollama serve >/workspace/ollama.log 2>&1" </dev/null & sleep 6
    }
    setsid env BURST_HOURS=8 bash /workspace/sim_burst.sh >/workspace/sim_burst.log 2>&1 </dev/null & disown
    echo "  relaunched sim_burst (was stopped)"
  fi
' 2>&1
echo "[$TS] 3090 sim keeper ran"
