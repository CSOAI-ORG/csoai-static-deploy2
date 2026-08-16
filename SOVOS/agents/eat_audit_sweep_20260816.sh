#!/usr/bin/env bash
# EAT audit sweep 2026-08-16 — run entirely on pod, zero Mac compute.
# Usage: bash SOVOS/agents/eat_audit_sweep_20260816.sh
set -uo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"
OUT="SOVOS/cross-lab-runs/2026-08-16"
mkdir -p "$OUT"
echo "=== EAT AUDIT SWEEP $(date -u +%FT%TZ) ==="

# 1. Repo hygiene: pull to latest
git fetch origin --quiet 2>/dev/null && git merge --ff-only origin/$(git branch --show-current) 2>/dev/null && echo "git: synced to origin/$(git branch --show-current)" || echo "git: sync skipped/failed (continuing on local head)"

# 2. Full pytest sweep (collection + pass/fail counts)
echo "--- pytest collection + run ---"
python3 -m pytest SOVOS/packages -x -q --co 2>/dev/null | tail -1 || echo "collection: FAILED"
python3 -m pytest SOVOS/packages -q 2>&1 | tail -6 | tee "$OUT/pytest_tail.txt"

# 3. Claim-linter (G4 gate)
echo "--- claim linter ---"
python3 ci/run_claim_linter.py 2>&1 | tail -5

# 4. Inspect bridge (audit-machine seam)
echo "--- sovos-inspect-bridge tests ---"
python3 -m pytest SOVOS/packages/sovos-inspect-bridge -q 2>&1 | tail -2

# 5. Fleet manifest / capability registry (the canons)
echo "--- registry/fleet canons ---"
python3 -m pytest SOVOS/packages/sovos-fleet-manifest SOVOS/packages/sovos-capability-registry -q 2>&1 | tail -2

# 6. City protocols + scenario bank + gold bank (measurement front)
echo "--- sovos-city audit front ---"
python3 -m pytest SOVOS/packages/sovos-city -q 2>&1 | tail -2

# 7. Daily index refresh if board data exists (no Mac involvement)
if [ -d SOVOS/boards-v2-2026-08-12 ]; then
  echo "--- daily index refresh ---"
  python3 SOVOS/agents/daily_index.py SOVOS/boards-v2-2026-08-12 2>&1 | tail -3 || echo "index refresh skipped"
else
  echo "boards dir not found — skipping index refresh"
fi

echo "=== EAT AUDIT SWEEP COMPLETE $(date -u +%FT%TZ) ==="
tail -20 "$OUT/pytest_tail.txt" 2>/dev/null || true