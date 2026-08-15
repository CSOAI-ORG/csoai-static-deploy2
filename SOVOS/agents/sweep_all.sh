#!/usr/bin/env bash
# sweep_all.sh — run every SOVOS package's tests on a single pod,
# with the right PYTHONPATH that fixes sovos-chain's transitive
# dependency on sovos-fisher-rao.
set -e

REPO="${REPO:-/workspace/csoai-static-deploy2}"
cd "$REPO"

# Build a PYTHONPATH that includes ALL package src dirs (so chain
# can find fisher-rao, arena can find chain, etc.)
PYTHONPATHS=""
for pkg in arena signal-index map-elites birth bus-redis article-zero sheaf-gate x402-gate sigma-calibration stigmergy cpo-calculator capability-registry fleet-manifest glass harvest merge-arena persona fleet dream robot-ras league chain fisher-rao jspace-hyperbolic; do
  if [ -d "SOVOS/packages/sovos-$pkg/src" ]; then
    PYTHONPATHS="$PYTHONPATHS:SOVOS/packages/sovos-$pkg/src"
  fi
done
# City needs article-zero + chain + fisher-rao on path
PYTHONPATHS="$PYTHONPATHS:SOVOS/packages/sovos-city/src"

export PYTHONPATH="$PYTHONPATHS"

total_pass=0
total_fail=0
total_skip=0
for pkg in arena signal-index map-elites birth bus-redis article-zero sheaf-gate x402-gate sigma-calibration stigmergy cpo-calculator alchemist alphabet council crosswalk invariants jspace-hyperbolic jspace-pipeline jspace-move oscal quantum-bridge quantum-router certification-loop hive cellar-ingest qtask-converter a2a-swarm capability-registry fleet-manifest glass harvest merge-arena persona fleet dream robot-ras league chain fisher-rao city; do
  if [ -d "SOVOS/packages/sovos-$pkg/tests" ]; then
    out=$(/usr/bin/python3 -m pytest SOVOS/packages/sovos-$pkg/tests --tb=no -q 2>&1 | tail -1)
    echo "$pkg: $out"
    # tally
    p=$(echo "$out" | grep -oE "[0-9]+ passed" | head -1 | grep -oE "[0-9]+" || echo 0)
    f=$(echo "$out" | grep -oE "[0-9]+ failed" | head -1 | grep -oE "[0-9]+" || echo 0)
    s=$(echo "$out" | grep -oE "[0-9]+ skipped" | head -1 | grep -oE "[0-9]+" || echo 0)
    total_pass=$((total_pass + p))
    total_fail=$((total_fail + f))
    total_skip=$((total_skip + s))
  fi
done
echo ""
echo "=== TOTAL: $total_pass passed, $total_fail failed, $total_skip skipped ==="
