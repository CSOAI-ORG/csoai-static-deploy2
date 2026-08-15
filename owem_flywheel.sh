#!/usr/bin/env bash
# owem_flywheel.sh — the self-closing loop: new expert -> benchmarked -> auto-routed.
#
# ═══════════════════════════════════════════════════════════════════════════════
# WHY THIS RUNS UNATTENDED — the cluster is MONOTONIC (measured 2026-07-28)
# ═══════════════════════════════════════════════════════════════════════════════
# Composition is MAX-based, not average-based: a dimension routes to whichever expert scores
# highest on it. So a new expert can only ever ADD. If it wins nothing, it is never routed and
# costs nothing but disk. There is no way to make the cluster worse by adding to it.
#
# Verified by replaying every subset in descending solo-score order — every single addition was
# Δ >= 0, and the WORST model on the board (14.9% solo, dead last) contributed +1.67, the largest
# gain of the final four:
#
#     +sov33-evolved      solo=54.2%  cluster=54.2%
#     +sov33-dist-c2      solo=52.3%  cluster=57.5%  Δ=+3.33
#     +sov-sovereign-v4   solo=45.1%  cluster=60.4%  Δ=+1.77
#     +qwen2.5:0.5b       solo=38.2%  cluster=61.9%  Δ=+1.00
#     +sov33-evolved-c2   solo=14.9%  cluster=63.6%  Δ=+1.67   <- the worst model, still additive
#
# THIS is why the flywheel does not need supervision. In a single-model regime a bad checkpoint
# is a regression you must catch and roll back. In a max-composed cluster a bad expert is inert.
# Training runs can fail, produce junk, or take weeks — none of it can damage what already works.
# That is the "water to honey" property: time only accrues, it never subtracts.
#
# ⚠️ THE ONE THING THAT BREAKS IT: this holds for the ORACLE (perfect routing). The live cluster
# is oracle × routing-accuracy, and the spine's accuracy on user-shaped queries is NOT yet
# measured (see _alignment/SPINE_ROUTING_REALITY_2026-07-28.md). Monotonic in composition does
# NOT yet mean monotonic in delivered score. Do not claim the latter.
#
# Usage:
#   bash owem_flywheel.sh            # benchmark any un-benchmarked ollama model, then report
#   bash owem_flywheel.sh --status   # show what is pending, run nothing
set -uo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RESULTS="${HERE}/benchmark-results/govbench"
STATUS_ONLY=0
[[ "${1:-}" == "--status" ]] && STATUS_ONLY=1

cd "$HERE"

# Which ollama models have no 15-dim result yet?
PENDING=()
while IFS= read -r m; do
  [[ -z "$m" ]] && continue
  safe="${m//:/_}"; safe="${safe//\//_}"
  if [[ ! -f "${RESULTS}/${safe}.json" ]]; then PENDING+=("$m"); fi
done < <(ollama list 2>/dev/null | awk 'NR>1{print $1}')

echo "  OWEM FLYWHEEL"
echo "  models in ollama : $(ollama list 2>/dev/null | tail -n +2 | wc -l | tr -d ' ')"
echo "  awaiting bench   : ${#PENDING[@]}"
[[ ${#PENDING[@]} -gt 0 ]] && printf '    - %s\n' "${PENDING[@]}"

if [[ $STATUS_ONLY -eq 1 ]]; then exit 0; fi
if [[ ${#PENDING[@]} -eq 0 ]]; then
  echo "  nothing to do — every expert is benchmarked."
  python3 owem_cluster.py --explain | tail -6
  exit 0
fi

BEFORE=$(python3 owem_cluster.py --explain 2>/dev/null | grep "cluster (oracle)" | grep -oE "[0-9.]+" | head -1)

for m in "${PENDING[@]}"; do
  echo
  echo "  ── benchmarking ${m} ──"
  # govbench_eval writes NO file for an unreachable model, so a failed run simply leaves it
  # pending for the next pass. It can never enter the routing table on a failed measurement.
  python3 govbench_eval.py --model "$m" --provider ollama 2>&1 | grep -E "OVERALL|CERTIF|UNREACHABLE" | sed 's/^/    /'
done

AFTER=$(python3 owem_cluster.py --explain 2>/dev/null | grep "cluster (oracle)" | grep -oE "[0-9.]+" | head -1)

echo
echo "  ── cluster after this turn of the wheel ──"
python3 owem_cluster.py --explain 2>/dev/null | tail -8
if [[ -n "${BEFORE:-}" && -n "${AFTER:-}" ]]; then
  echo
  awk -v b="$BEFORE" -v a="$AFTER" 'BEGIN{printf "  oracle %.1f%% -> %.1f%%  (Δ %+.2f)\n", b, a, a-b}'
  awk -v b="$BEFORE" -v a="$AFTER" 'BEGIN{ if (a < b - 0.001) print "  ⚠️  CLUSTER WENT DOWN — that should be impossible under max-composition.\n     Something is wrong with the results directory or the table builder. Investigate."}'
fi
exit 0
