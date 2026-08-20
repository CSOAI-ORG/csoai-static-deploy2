#!/bin/bash
# Sovereign MCP test sweep — runs all 161 meok-sovereign-*-mcp test suites.
# Use the system python3 (3.14) with cryptography + numpy from break-system pip.
# PYTHONPATH MUST be cleared (Hermes venv pollution breaks numpy/crypto).
#
# Usage:
#   ./scripts/sovereign_test_sweep.sh                # full sweep, clean
#   ./scripts/sovereign_test_sweep.sh meok-sovereign-arena-mcp  # single MCP

set -e
cd "$(dirname "$0")/.."

PY="/usr/local/bin/python3"

if [ -n "$1" ]; then
    cd "mcp-marketplace/$1"
    PYTHONPATH= PYTHONDONTWRITEBYTECODE=1 "$PY" -m pytest tests/ -v --tb=short -p no:cacheprovider
else
    PYTHONPATH= /usr/local/bin/python3 /tmp/run_sweep2.py
fi
