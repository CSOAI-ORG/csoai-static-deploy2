#!/usr/bin/env bash
# EAT audit sweep 2026-08-16 v2 — run entirely on pod, zero Mac compute.
# v2 lessons (pod audit 2026-08-16):
#   * --import-mode=importlib  (kills duplicate bare-module collection errors)
#   * --ignore vendor dirs     (third-party suites, not our code)
#   * maxdepth 3 src find      (nested packages like sovos-mcp-servers/*/src)
# Usage: bash SOVOS/agents/eat_audit_sweep_20260816.sh
set -uo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"
OUT="SOVOS/cross-lab-runs/2026-08-16"
mkdir -p "$OUT"
echo "=== EAT AUDIT SWEEP v2 $(date -u +%FT%TZ) ==="

# 0. Wire every package src dir (depth 3 covers nested mcp-servers) 
PY="$(find SOVOS/packages -maxdepth 3 -type d -name src -print | paste -sd: -)"
echo "src dirs wired: $(echo "$PY" | tr ':' '\n' | grep -c src)"

# 1. Repo hygiene
git fetch origin --quiet 2>/dev/null && git merge --ff-only origin/$(git branch --show-current) 2>/dev/null && echo "git: synced" || echo "git: sync skipped"

# 2. Full pytest sweep
echo "--- pytest full sweep (importlib mode, vendor ignored) ---"
PYTHONPATH="$PY" python3 -m pytest SOVOS/packages -q --no-header --continue-on-collection-errors \
  --import-mode=importlib --ignore=SOVOS/packages/sovos-mind/vendor \
  2>&1 | tail -12 | tee "$OUT/pytest_tail.txt"

# 3. Claim-linter (G4 gate)
echo "--- claim linter ---"
python3 ci/run_claim_linter.py 2>&1 | tail -5

# 4. Inspect bridge (audit-machine seam)
echo "--- sovos-inspect-bridge ---"
PYTHONPATH="$PY" python3 -m pytest SOVOS/packages/sovos-inspect-bridge -q --import-mode=importlib 2>&1 | tail -2

# 5. Registry/fleet canons
echo "--- registry/fleet canons ---"
PYTHONPATH="$PY" python3 -m pytest SOVOS/packages/sovos-fleet-manifest SOVOS/packages/sovos-capability-registry -q --import-mode=importlib 2>&1 | tail -2

# 6. City measurement front
echo "--- sovos-city audit front ---"
PYTHONPATH="$PY" python3 -m pytest SOVOS/packages/sovos-city -q --import-mode=importlib 2>&1 | tail -2

# 7. Daily index refresh if board data exists
if [ -d SOVOS/boards-v2-2026-08-12 ]; then
  echo "--- daily index refresh ---"
  PYTHONPATH="$PY" python3 SOVOS/agents/daily_index.py SOVOS/boards-v2-2026-08-12 2>&1 | tail -3 || echo "index refresh skipped"
else
  echo "boards dir not found — skipping index refresh"
fi

echo "=== EAT AUDIT SWEEP v2 COMPLETE $(date -u +%FT%TZ) ==="