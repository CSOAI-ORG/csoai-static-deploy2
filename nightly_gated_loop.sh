#!/usr/bin/env bash
# nightly_gated_loop.sh — CSOAI honest measure → gated-evolve loop. Runs on the A100.
#
# SAFE for unsupervised nightly use BY DESIGN:
#   1) MEASURE the whole fleet on the GSPC axes — read-only inference, only ever
#      produces honest numbers (Wilson-CI, control-anchored, UNMEASURED-honest).
#   2) EVOLVE (gated): train ONE candidate from fuel, then RE-MEASURE it. It does
#      NOT auto-promote — it prints the ADOPT/KEEP verdict and leaves the swap to a
#      human. Gates: honey_barrier (won't train on a contaminated ruler) +
#      ouroboros verdict (a candidate that can't beat base is flagged KEEP).
#   Worst case of a bad training run: a rejected candidate + an honest "KEEP base".
#      Nothing in the live fleet changes without a human reading the verdict.
#
# Results land on the 2.3 PB /workspace network volume (survives pod restart).
# A second-machine copy (Mac pull / HF) is the durability completion — see README.
set -uo pipefail
cd /workspace
export OLLAMA_HOST=127.0.0.1:11434
TS=$(date -u +%Y%m%dT%H%M%SZ)
D=/workspace/nightly/$TS; mkdir -p "$D"
exec > >(tee -a "$D/loop.log") 2>&1
echo "=== CSOAI nightly gated loop $TS ==="

# ensure ollama is serving
curl -sf 127.0.0.1:11434/api/tags >/dev/null 2>&1 || {
  setsid bash -c "env OLLAMA_HOST=0.0.0.0 OLLAMA_MODELS=/workspace/ollama ollama serve >/workspace/ollama.log 2>&1" </dev/null &
  sleep 6
}

# ── 1) MEASURE the fleet (always on; cannot harm anything) ──────────────────
CONTROL="${CONTROL:-qwen2.5:0.5b-instruct}"
MODELS=$(ollama list | tail -n+2 | awk '{print $1}' | grep -v "^$CONTROL$" | grep -v "^$" | tr '\n' ' ')
echo "--- MEASURE: $(echo $MODELS | wc -w) models × GSPC axes (control=$CONTROL) ---"
if python3 -u gspc_flywheel.py --models $MODELS --control "$CONTROL" > "$D/fleet_measure.log" 2>&1; then
  echo "  measure: OK"; tail -3 "$D/fleet_measure.log"
else
  echo "  measure: FAILED (see $D/fleet_measure.log)"
fi

# ── 2) GATED EVOLVE (trains a candidate + re-measures; NEVER auto-promotes) ──
# Default ON — safe because it can't change the live fleet. Set NIGHTLY_EVOLVE=0
# to run measure-only. Requires close_train_hop.py + the trainer stack on the pod.
if [ "${NIGHTLY_EVOLVE:-1}" = "1" ] && [ -f close_train_hop.py ]; then
  echo "--- EVOLVE (gated): honey_barrier + ouroboros verdict, no auto-promote ---"
  if python3 -u close_train_hop.py \
        --base "${EVOLVE_BASE:-qwen2.5:1.5b}" \
        --hf-base "${EVOLVE_HF_BASE:-Qwen/Qwen2.5-1.5B-Instruct}" \
        --steps "${EVOLVE_STEPS:-100}" > "$D/evolve.log" 2>&1; then
    echo "  evolve: candidate trained + re-measured (read the verdict — promotion is yours)"
    tail -4 "$D/evolve.log"
  else
    echo "  evolve: skipped/failed (gate tripped or trainer deps missing) — see $D/evolve.log"
  fi
else
  echo "--- EVOLVE: disabled (NIGHTLY_EVOLVE=0 or close_train_hop.py absent) ---"
fi

echo "=== done $TS → $D (persistent volume) ==="
echo "$TS done" >> /workspace/nightly/history.log
