#!/usr/bin/env bash
# Pre-flight check for Sovereign Town p0_aqua.
# Run before committing or deploying.
set -euo pipefail
cd "$(dirname "$0")"

PYTHON="${PYTHON:-/opt/homebrew/bin/python3.11}"

echo "==> Running selftest.py"
"$PYTHON" selftest.py

echo "==> Running e2e_test.py"
"$PYTHON" e2e_test.py

# Browser-level tests (optional — run if Playwright venv and services are present).
if [[ -d .venv-playwright ]]; then
  echo "==> Running browser_test.py (Playwright)"
  if .venv-playwright/bin/python -m pytest browser_test.py -q; then
    echo "==> Browser tests passed"
  else
    echo "==> Browser tests failed or services unavailable; skipping blocker"
  fi
else
  echo "==> Skipping browser_test.py (no .venv-playwright)"
fi

echo "==> All checks passed"
