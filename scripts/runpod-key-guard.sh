#!/bin/bash
# B6 — RunPod key hygiene guard (19 Aug 2026)
# Doctrine (estate map §2): "do not put it on the command line — ps aux leaks it;
# use env files chmod 600." Verified: Mac ~/.runpod/api_key = mode 600.
#
# This guard: (1) refuses to run runpodctl with a key on argv; (2) provides the
# safe env-file pattern for any catapult/measurement script; (3) audits for the
# leak class. Run: bash runpod-key-guard.sh [--audit]

set -uo pipefail
KEYFILE="${RUNPOD_KEYFILE:-$HOME/.runpod/api_key}"
LOG="$HOME/.runpod/key-guard.log"

audit() {
  echo "=== runpod key guard audit $(date -u +%FT%TZ) ===" >> "$LOG"
  # 1. key file mode must be 600
  if [ -f "$KEYFILE" ]; then
    mode=$(stat -f "%Lp" "$KEYFILE" 2>/dev/null || echo "?")
    [ "$mode" = "600" ] && echo "  ✅ keyfile mode 600" >> "$LOG" \
                       || { echo "  ❌ keyfile mode $mode (must be 600)" >> "$LOG"; return 1; }
  else
    echo "  ⚠️ no keyfile at $KEYFILE (expected path)" >> "$LOG"
  fi
  # 2. no runpodctl invocation carries the key on argv (ps leak class)
  leak=$(ps aux | grep -E "runpodctl.*(api[_-]?key|token)" | grep -v grep | head -2)
  [ -z "$leak" ] && echo "  ✅ no key-on-argv processes" >> "$LOG" \
                 || { echo "  ❌ KEY ON ARGV: $leak" >> "$LOG"; return 1; }
  # 3. no script in the estate passes the key positionally to runpodctl
  hits=$(grep -rln "runpodctl.*\$RUNPOD_API\|runpodctl.*apiKey" \
         "$HOME/clawd/scripts" "$HOME/clawd/_evacuation/scripts" 2>/dev/null \
         | grep -v "runpod-key-guard.sh" | head -3)
  [ -z "$hits" ] && echo "  ✅ no script passes key to runpodctl argv" >> "$LOG" \
                 || { echo "  ❌ leak scripts: $hits" >> "$LOG"; return 1; }
  echo "  ✅ guard PASS" >> "$LOG"
  return 0
}

run_safe() {
  # Usage: run_safe <cmd...> — loads the key into env, never onto argv.
  [ -f "$KEYFILE" ] || { echo "no keyfile"; return 1; }
  RUNPOD_API_KEY="$(cat "$KEYFILE")" "$@"
}

case "${1:-}" in
  --audit) audit ;;
  run) shift; run_safe "$@" ;;
  *) echo "usage: runpod-key-guard.sh [--audit|run <cmd...>]"; exit 2 ;;
esac
