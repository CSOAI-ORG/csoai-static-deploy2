#!/usr/bin/env bash
# auto_e2e_overnight.sh — full EAT automation: synthesize → patch → benchmark → train → aggregate
# Runs all phases, records everything in benchmark-results/sov_space/.
#
# Phases:
#   0. Set up sov_space dir + manifest
#   1. Synthesize research from KB + flywheel pairs + greenfield dims (synthesize_research.py)
#   2. Build patched models from synthesis (merge_export.py)
#   3. Run GovBench on every patched model
#   4. Run EAT weak-dim on every patched model
#   5. Run flywheel daily with default clan pair
#   6. Run CompBench on the top 2 patched models
#   7. Aggregate greenfield + EAT + flywheel (aggregate_greenfield_eat.py)
#   8. Re-synthesize with new flywheel fuel + loop
#
# Usage:
#   ./auto_e2e_overnight.sh [--loops N] [--skip-compbench] [--models m1,m2,...]
set -uo pipefail

cd ~/clawd/csoai-static-deploy2 || exit 1

LOOPS=1
SKIP_COMPBENCH=0
MODELS="sov33-v7:latest,sov-sovereign-v4:latest,clan-sovereignty-cited:latest,clan-sovereignty-refusing:latest"
SOV_SPACE_DIR="benchmark-results/sov_space/$(date -u +%Y-%m-%d_%H%M%S)"

while [[ $# -gt 0 ]]; do
  case $1 in
    --loops) LOOPS="$2"; shift 2 ;;
    --skip-compbench) SKIP_COMPBENCH=1; shift ;;
    --models) MODELS="$2"; shift 2 ;;
    *) echo "Unknown arg: $1"; exit 1 ;;
  esac
done

mkdir -p "$SOV_SPACE_DIR"
LOG="$SOV_SPACE_DIR/auto_run.log"
ERR="$SOV_SPACE_DIR/auto_run.err"

echo "Auto E2E Overnight: $(date -u +%Y-%m-%dT%H:%M:%SZ)" | tee "$LOG"
echo "SOV space: $SOV_SPACE_DIR" | tee -a "$LOG"
echo "Models: $MODELS" | tee -a "$LOG"
echo "Loops: $LOOPS" | tee -a "$LOG"
echo "" | tee -a "$LOG"

# Track elapsed time
SECONDS=0

# Verify Ollama + hub up
echo "[$(date -u +%H:%M:%S)] Verifying Ollama..." | tee -a "$LOG"
if ! curl -sf http://localhost:11434/api/tags > /dev/null 2>&1; then
  echo "  Ollama not running. Aborting." | tee -a "$LOG" "$ERR"
  exit 1
fi
echo "  OK" | tee -a "$LOG"

# Verify hub running. Accept any HTTP response from a live port (2xx OR 5xx):
# a degraded service (e.g. mcp-gateway returning a 503 + JSON health body) is
# still a reachable process and the batch should not gate on its health check.
# Only a hard connect failure (curl exit 7 / no 3-digit HTTP code) means down.
echo "[$(date -u +%H:%M:%S)] Verifying hub..." | tee -a "$LOG"
for url in http://localhost:8080/health http://localhost:3000/health http://localhost:9094/health; do
  if ! curl -s "$url" -o /dev/null -w "%{http_code}" -m 3 2>/dev/null | grep -qE '^[0-9]{3}$'; then
    echo "  Hub not reachable ($url). Aborting." | tee -a "$LOG" "$ERR"
    exit 1
  fi
done
echo "  OK (sov-gateway, mcp-gateway, flywheel)" | tee -a "$LOG"

# Convert comma list to array
IFS=',' read -ra MODEL_ARR <<< "$MODELS"

for LOOP in $(seq 1 $LOOPS); do
  echo "" | tee -a "$LOG"
  echo "============================================================" | tee -a "$LOG"
  echo "  LOOP $LOOP of $LOOPS  ($(date -u +%H:%M:%S))" | tee -a "$LOG"
  echo "============================================================" | tee -a "$LOG"

  # ── PHASE 1: Synthesize research ──
  echo "" | tee -a "$LOG"
  echo "[$(date -u +%H:%M:%S)] PHASE 1: Synthesize research pairs" | tee -a "$LOG"
  python3 synthesize_research.py 2>&1 | tee -a "$LOG" | tail -5
  SYNTH=$(ls -t training_data/synth_*.jsonl 2>/dev/null | head -1)
  echo "  Synth file: $SYNTH" | tee -a "$LOG"

  # ── PHASE 2: Build patched models ──
  echo "" | tee -a "$LOG"
  echo "[$(date -u +%H:%M:%S)] PHASE 2: Patch models" | tee -a "$LOG"
  PATCHED_MODELS=""
  for m in "${MODEL_ARR[@]}"; do
    patched="${m%:latest}-patched:latest"
    echo "  Patching $m → $patched" | tee -a "$LOG"
    python3 merge_export.py "$m" 2>&1 | tail -3 | tee -a "$LOG"
    # Only add the patched name to the eval list if it was ACTUALLY created.
    # merge_export.py falls back to prompt-injection when ollama create fails;
    # in that case the -patched model does not exist and naming it makes
    # govbench/EAT report UNREACHABLE instead of measuring. Check the real
    # ollama registry before trusting the name.
    if ollama list 2>/dev/null | awk '{print $1}' | grep -qx "${patched%:latest}"; then
      PATCHED_MODELS="$PATCHED_MODELS,$patched"
      echo "    ✓ created: $patched" | tee -a "$LOG"
    else
      echo "    ✗ not created — $patched skipped (may fall back to prompt injection)" | tee -a "$LOG"
    fi
  done
  PATCHED_MODELS="${PATCHED_MODELS#,}"
  # Bare-name list (":latest" stripped) for eval tools — ollama normalises
  # "name:latest"->"name", so passing ":latest" makes evals return HTTP 400.
  PATCHED_CALLNAMES=$(echo "$PATCHED_MODELS" | tr ',' '\n' | sed 's/:latest$//' | paste -sd, -)

  # ── PHASE 3: GovBench on patched models ──
  echo "" | tee -a "$LOG"
  echo "[$(date -u +%H:%M:%S)] PHASE 3: GovBench on patched models" | tee -a "$LOG"
  IFS=',' read -ra PATCHED_ARR <<< "$PATCHED_MODELS"
  for m in "${PATCHED_ARR[@]}"; do
    # Ollama normalises "name:latest" -> "name", so passing the trailing ":latest"
    # makes govbench/eat hit HTTP 400 invalid-model-name -> UNREACHABLE -> EAT 0.0
    # while the bare name responds fine. Strip it for every eval call (2026-08-08 fix).
    callname="${m%:latest}"
    echo "  GovBench $callname..." | tee -a "$LOG"
    safe=$(echo "$callname" | tr ':' '_')
    out="benchmark-results/govbench/${safe}.json"
    if [[ -f "$out" ]]; then
      score=$(jq -r '.overall_score // "?"' "$out" 2>/dev/null)
      echo "    already scored: $score" | tee -a "$LOG"
    else
      python3 govbench_eval.py --model "$callname" --provider ollama 2>&1 | tee -a "$LOG" | tail -3
    fi
  done

  # ── PHASE 4: EAT weak-dim on patched models ──
  echo "" | tee -a "$LOG"
  echo "[$(date -u +%H:%M:%S)] PHASE 4: EAT weak-dim on patched models" | tee -a "$LOG"
  for m in "${PATCHED_ARR[@]}"; do
    callname="${m%:latest}"
    echo "  EAT $callname..." | tee -a "$LOG"
    python3 eat_run_local.py "$callname" 2>&1 | tee -a "$LOG" | tail -5
  done

  # ── PHASE 5: Flywheel daily ──
  echo "" | tee -a "$LOG"
  echo "[$(date -u +%H:%M:%S)] PHASE 5: Flywheel daily" | tee -a "$LOG"
  python3 flywheel.py --models clan-sovereignty-cited,clan-sovereignty-refusing --items 20 2>&1 | tee -a "$LOG" | tail -10

  # ── PHASE 6: CompBench on top 2 patched ──
  if [[ $SKIP_COMPBENCH -eq 0 ]]; then
    echo "" | tee -a "$LOG"
    echo "[$(date -u +%H:%M:%S)] PHASE 6: CompBench on top 2 patched" | tee -a "$LOG"
    TOP2=$(echo "$PATCHED_MODELS" | cut -d',' -f1-2)
    IFS=',' read -ra TOP_ARR <<< "$TOP2"
    for m in "${TOP_ARR[@]}"; do
      callname="${m%:latest}"
      echo "  CompBench $callname..." | tee -a "$LOG"
      python3 compbench_local.py "$callname" 2>&1 | tee -a "$LOG" | tail -5
    done
  fi

  # ── PHASE 7: Aggregate ──
  echo "" | tee -a "$LOG"
  echo "[$(date -u +%H:%M:%S)] PHASE 7: Aggregate greenfield + EAT + flywheel" | tee -a "$LOG"
  python3 aggregate_greenfield_eat.py 2>&1 | tee -a "$LOG" | tail -25

  # ── PHASE 8: EAT stack combined report ──
  echo "" | tee -a "$LOG"
  echo "[$(date -u +%H:%M:%S)] PHASE 8: EAT stack combined report" | tee -a "$LOG"
  python3 eat_stack.py $PATCHED_CALLNAMES 2>&1 | tee -a "$LOG" | tail -15

done

# Final summary
ELAPSED=$SECONDS
echo "" | tee -a "$LOG"
echo "============================================================" | tee -a "$LOG"
echo "  AUTO E2E OVERNIGHT COMPLETE" | tee -a "$LOG"
echo "  Elapsed: $((ELAPSED/3600))h $((ELAPSED%3600/60))m $((ELAPSED%60))s" | tee -a "$LOG"
echo "  Results: $SOV_SPACE_DIR" | tee -a "$LOG"
echo "  Log: $LOG" | tee -a "$LOG"
echo "============================================================" | tee -a "$LOG"

# Mirror to sov_space root
cp "$LOG" "$SOV_SPACE_DIR/auto_run.log"

# Generate final report
python3 -c "
import json, glob, os
from pathlib import Path
from datetime import datetime, timezone

results = {
    'timestamp': datetime.now(timezone.utc).isoformat(),
    'sov_space_dir': '$SOV_SPACE_DIR',
    'elapsed_secs': $ELAPSED,
    'models': '$MODELS'.split(','),
    'patched_models': '$PATCHED_MODELS'.split(','),
    'loops': $LOOPS,
}

# Aggregate all GovBench scores (bare-name files written by govbench_eval;
# ":latest" was stripped in PHASE 3 so the eval writes *patched.json)
gb_results = []
for f in glob.glob('benchmark-results/govbench/*patched.json'):
    try:
        d = json.loads(Path(f).read_text())
        gb_results.append({
            'model': d.get('model', Path(f).stem),
            'overall_score': d.get('overall_score'),
            'dimensions': d.get('dimensions', {}),
        })
    except Exception as e:
        pass

# Aggregate all EAT scores
eat_results = []
for f in glob.glob('benchmark-results/eat_govbench/eat_local_*patched*.json'):
    try:
        d = json.loads(Path(f).read_text())
        eat_results.append({
            'model': d.get('model', Path(f).stem),
            'avg_baseline': d.get('avg_baseline'),
            'avg_context': d.get('avg_context'),
        })
    except Exception as e:
        pass

results['govbench'] = gb_results
results['eat_weak'] = eat_results

report_path = '$SOV_SPACE_DIR/auto_e2e_report.json'
Path(report_path).write_text(json.dumps(results, indent=2))
print(f'Report: {report_path}')
print()
print('=== OVERNIGHT AUTO E2E SUMMARY ===')
print(f'Models patched: {len(gb_results)}')
print(f'EAT scores: {len(eat_results)}')
print()
for r in gb_results:
    print(f'  {r[\"model\"]}: GovBench {r[\"overall_score\"]:.1f}%' if isinstance(r['overall_score'], (int, float)) else f'  {r[\"model\"]}: ?')
for r in eat_results:
    lift = (r['avg_context'] - r['avg_baseline']) if isinstance(r['avg_context'], (int, float)) else 0
    print(f'  {r[\"model\"]}: EAT base {r[\"avg_baseline\"]:.1f}% → ctx {r[\"avg_context\"]:.1f}% (+{lift:.1f}pp)' if isinstance(r['avg_baseline'], (int, float)) else f'  {r[\"model\"]}: ?')
" 2>&1 | tee -a "$LOG"

# Mirror to sov_space root
ls -la "$SOV_SPACE_DIR/" | tee -a "$LOG"