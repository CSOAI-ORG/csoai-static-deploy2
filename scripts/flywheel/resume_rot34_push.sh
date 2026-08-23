#!/bin/bash
# Resume rot4 Kaggle push loop (rot3 fully done). Survives quota 429 + CLI hangs.
set -uo pipefail
R4="$HOME/clawd/scripts/flywheel/multicluster-kernels-rot4"
LOG="$HOME/clawd/scripts/flywheel/rot34-push.log"
PUSHED_R4="nicktempleman/owem-affect-rot4 nicktempleman/owem-art5-safeguard-rot4 nicktempleman/owem-care-rot4"

echo "$(date -u +%H:%M) rot4 resume start" >> "$LOG"

push_kernel() {
  local dir="$1" id="$2"
  for attempt in 1 2 3 4 5 6 7 8; do
    # python timeout wrapper (no gtimeout dependency)
    out=$(python3 -c "
import subprocess
p = subprocess.Popen(['kaggle','kernels','push','-p','$dir'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
try:
    o,_ = p.communicate(timeout=300)
except subprocess.TimeoutExpired:
    p.kill(); o = 'TIMEOUT_OR_HANG'
print(o)
" 2>&1)
    if echo "$out" | grep -q "successfully pushed"; then
      echo "$(date -u +%H:%M) OK  $id" >> "$LOG"
      return 0
    fi
    local wait=$((attempt * 600))
    echo "$(date -u +%H:%M) RETRY $id attempt $attempt wait ${wait}s: $(echo "$out" | tail -1 | cut -c1-80)" >> "$LOG"
    sleep "$wait"
  done
  echo "$(date -u +%H:%M) FAIL $id" >> "$LOG"
  return 1
}

for d in "$R4"/kaggle-*; do
  id=$(grep '"id"' "$d/kernel-metadata.json" | head -1 | sed 's/.*: *"\([^"]*\)".*/\1/')
  case " $PUSHED_R4 " in
    *" $id "*) echo "$(date -u +%H:%M) SKIP $id (already pushed)" >> "$LOG"; continue;;
  esac
  push_kernel "$d" "$id"
  sleep 20
done

echo "$(date -u +%H:%M) rot4 resume done" >> "$LOG"
