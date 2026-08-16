#!/bin/bash
# master_batch.sh — autonomous batch runner for MASTER_33_MOVES (T1 + T2 + T3 server-side moves)
# Run on: RunPod 3090 (sov-repull) or any pod with the csoai-static-deploy2 clone.
# Usage: bash master_batch.sh [--bench|--harvest|--cards|--all]
set -uo pipefail
cd /workspace/csoai-static-deploy2 || exit 1
PY=/workspace/sov-governance-venv/bin/python
OUT=/workspace/batch_outputs
mkdir -p "$OUT"
echo "=== MASTER BATCH $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="

run_bench() {
  echo "--- T2.11: 7-model full gov bench (already ran; re-run if missing) ---"
  [ -f /workspace/bench_results_7models_24.json ] || $PY /workspace/full_bench_7.py
  echo "  bench done: $(ls -la /workspace/bench_results_7models_24.json 2>/dev/null | awk '{print $5}')B"
}

run_harvest() {
  echo "--- T3.17: honey harvest (OGL/UK gov/public data banks present on pod) ---"
  # Aggregate any honey producers already on disk (flight-safe; no network unless cable)
  if [ -f forest/honey_all_producers.jsonl ]; then
    n=$(wc -l < forest/honey_all_producers.jsonl)
    echo "  honey_all_producers.jsonl rows: $n"
    echo "{\"ts\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"rows\":$n}" >> "$OUT/honey_count.jsonl"
  else
    echo "  no honey file (lane owns harvest)"
  fi
}

run_cards() {
  echo "--- T3.20: 3KB cards for registered models (sov_3kb_converter) ---"
  for M in /workspace/oowm_merge_v1 /workspace/refusal-lora-repull/merged; do
    $PY /workspace/sovos-mergekit/sov_3kb_converter.py --input "$M" --clan council --axis GOV \
      --out "$OUT/3kb_cards" 2>&1 | tail -1
  done
}

run_all() { run_bench; run_harvest; run_cards; }

case "${1:---all}" in
  --bench) run_bench ;;
  --harvest) run_harvest ;;
  --cards) run_cards ;;
  --all|*) run_all ;;
esac
echo "=== BATCH COMPLETE $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="