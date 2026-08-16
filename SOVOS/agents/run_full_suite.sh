#!/usr/bin/env bash
# Canonical full-estate test sweep (pod-side, cross-package PYTHONPATH built in).
set -euo pipefail
cd /workspace
export PYTHONPATH=$(ls -d /workspace/sovos-*/src 2>/dev/null | tr "\n" ":")/workspace/sovos-tests
PKGS="sovos-arena sovos-article-zero sovos-birth sovos-bus-redis sovos-cellar-ingest sovos-chain sovos-council sovos-fisher-rao sovos-info-geometry sovos-map-elites sovos-mind sovos-oscal sovos-quantum-bridge sovos-sheaf-gate sovos-sigma-calibration sovos-signal-index sovos-x402-gate"
echo "=== FULL ESTATE SWEEP $(date -u +%FT%TZ) ==="
/workspace/sov-governance-venv/bin/python -m pytest $PKGS sovos-tests -q 2>&1 | tail -12
