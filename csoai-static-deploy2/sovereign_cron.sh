#!/bin/bash
# sovereign_cron.sh — Cron wrapper for sovereign_api.py health checks
# Runs every 15 minutes via launchd/cron
# Checks: Ollama health, care-floor compliance, SIGIL chain integrity
set -euo pipefail
BASE="/Users/nicholas/clawd/csoai-static-deploy2"
LOG="$BASE/sovereign_cron.log"
cd "$BASE"

echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] sovereign_cron start" >> "$LOG"

# 1. Check Ollama is running
if curl -sf http://localhost:11434/api/tags > /dev/null 2>&1; then
  echo "  ✓ Ollama running" >> "$LOG"
else
  echo "  ✗ Ollama down — restarting" >> "$LOG"
  ollama serve > /dev/null 2>&1 &
  sleep 3
fi

# 2. Run sovereign_api.py list (verify registry loads)
if python3 "$BASE/sovereign_api.py" list > /dev/null 2>&1; then
  echo "  ✓ Registry loaded" >> "$LOG"
else
  echo "  ✗ Registry load failed" >> "$LOG"
fi

# 3. Care-floor check on a sample prompt
RESULT=$(python3 "$BASE/sovereign_api.py" call "health check" --owem general --care 0.95 2>&1)
if echo "$RESULT" | grep -q "Care:"; then
  CARE=$(echo "$RESULT" | grep "Care:" | awk '{print $2}')
  echo "  ✓ Care score: $CARE" >> "$LOG"
else
  echo "  ✗ Care check failed" >> "$LOG"
fi

# 4. SIGIL chain integrity (check last sigil hash)
LATEST_SIGIL=$(ls -t "$BASE"/tick-*-sigil.json 2>/dev/null | head -1)
if [ -n "$LATEST_SIGIL" ]; then
  SIGIL_HASH=$(python3 -c "import json; d=json.load(open('$LATEST_SIGIL')); print(d.get('signature','')[:16] or d.get('root_hash','')[:16])" 2>/dev/null)
  echo "  ✓ Latest sigil: $(basename "$LATEST_SIGIL") hash=$SIGIL_HASH" >> "$LOG"
else
  echo "  ○ No sigils found" >> "$LOG"
fi

# 5. EAT cycle status (if running)
if [ -f "$BASE/asi_evolution.log" ]; then
  LAST_EAT=$(tail -1 "$BASE/asi_evolution.log" 2>/dev/null | head -c 120)
  echo "  ○ EAT: $LAST_EAT" >> "$LOG"
fi

echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] sovereign_cron end" >> "$LOG"
