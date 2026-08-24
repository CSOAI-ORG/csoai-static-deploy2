#!/bin/bash
# POD SELF-CHECK — the drum's gates ON the pod (sov-brain-2). Run nightly on the pod.
set -u
D="${1:-/workspace/frameworks-drum}"
cd "$D" || { echo "FAIL: drum dir missing on pod"; exit 1; }
FAIL=0
python3 -c "import json; c=json.load(open('catalog.json')); print('catalog:', len(c['items']), 'items')" || FAIL=1
python3 -c "import sys; sys.path.insert(0,'.'); import build_catalog as b; sys.exit(1 if b.lint_surfaces() else 0)" >/dev/null 2>&1 || { echo "FAIL: lint"; FAIL=1; }
if [ -f MANIFEST.sha256 ]; then shasum -a 256 -c MANIFEST.sha256 >/dev/null 2>&1 && echo "manifest TEA walk: PASS" || { echo "FAIL: manifest drift"; FAIL=1; }; fi
python3 ops/ingest_sovos.py --oowm-root /workspace/sov33-oowm >/dev/null 2>&1 && echo "OOWM ingest: refreshed" || echo "OOWM ingest: skip (no tree)"
[ "$FAIL" -eq 0 ] && echo "POD SELF-CHECK: ALL GREEN" || echo "POD SELF-CHECK: FAILURES"
exit $FAIL
