#!/bin/bash
# FRAMEWORKS DRUM — standing check (move 14): lint + check + tests + selftests.
# Intended for cron/launchd; exit non-zero on any failure.
# --verify-only: read-only pass (no catalog rebuild) for frequent scheduled runs.
set -u
DRUM="$HOME/master-harness/knowledge/frameworks-drum"
FAIL=0

echo "== frameworks-drum check $(date -u +%FT%TZ) =="

cd "$DRUM" || { echo "drum dir missing"; exit 1; }

if [ "${1:-}" = "--verify-only" ]; then
  python3 -c "import sys,json; sys.path.insert(0,'.'); import build_catalog as b; c=json.load(open('catalog.json')); sys.exit(1 if b.check_catalog(c) else 0)" >/dev/null 2>&1 || { echo "FAIL: check (read-only)"; FAIL=1; }
  python3 -c "import sys; sys.path.insert(0,'.'); import build_catalog as b; sys.exit(1 if b.lint_surfaces() else 0)" >/dev/null 2>&1 || { echo "FAIL: lint (read-only)"; FAIL=1; }
else
  python3 build_catalog.py --check --lint >/dev/null 2>&1 || { echo "FAIL: build/check/lint"; FAIL=1; }
fi
python3 tests/test_drum.py >/dev/null 2>&1 || { echo "FAIL: tests"; FAIL=1; }
python3 tests/e2e_properties.py >/dev/null 2>&1 || { echo "FAIL: property tests"; FAIL=1; }
python3 tests/e2e_drum.py >/dev/null 2>&1 || { echo "FAIL: e2e"; FAIL=1; }
python3 mcp/frameworks_drum_server.py --selftest >/dev/null 2>&1 || { echo "FAIL: mcp selftest"; FAIL=1; }
python3 router/conformal_router.py --selftest >/dev/null 2>&1 || { echo "FAIL: conformal router"; FAIL=1; }
python3 archive/knowledge_archive.py --selftest >/dev/null 2>&1 || { echo "FAIL: knowledge archive"; FAIL=1; }
python3 archive/dualwalk.py >/dev/null 2>&1 || { echo "FAIL: TEA backward walk"; FAIL=1; }
python3 ops/align_audit.py >/dev/null 2>&1 || { echo "FAIL: top-down alignment audit"; FAIL=1; }

if [ "$FAIL" -eq 0 ]; then
  echo "ALL GREEN"
else
  echo "FAILURES PRESENT"
fi
exit $FAIL
