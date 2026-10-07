#!/usr/bin/env bash
# Council content/release gates — required by ~/.config/git/hooks/pre-push.
# Real checks, not stubs: naming lock + codename scan on changed files.
set -uo pipefail

REMOTE="${1:-origin}"
BRANCH="${2:-main}"
FAIL=0

# Files changed vs remote (fall back to last commit if remote ref missing)
CHANGED="$(git diff --name-only "origin/${BRANCH}...HEAD" 2>/dev/null || git diff --name-only HEAD~1...HEAD)"

# Gate 1: naming lock — public copy must never say Nic/Nick; always Nicholas Templeman
# Gate 2: codename lock — internal codenames must never appear in public page/markdown copy
# Gate 3: forbidden claims — no AUKUS partnership / DAIC certified / DEFONEOS-SEAL without signed letter
while IFS= read -r f; do
  [ -z "$f" ] && continue
  case "$f" in
    *.html|*.md|*.xml|*.json|*.txt) ;;
    *) continue ;;
  esac
  case "$f" in
    SOVOS/*|_alignment/*|scripts/*|benchmark-results/*) continue ;;  # internal paths exempt
  esac
  [ -f "$f" ] || continue
  if grep -lE '\b(Nic|Nick)\b' "$f" >/dev/null 2>&1; then
    echo "GATE FAIL: 'Nic/Nick' (use 'Nicholas Templeman') in $f"; FAIL=1
  fi
  if grep -lE 'SOVOS|sov6|OWEM|SOV-[0-9]' "$f" >/dev/null 2>&1; then
    echo "GATE FAIL: internal codename leaked into public copy: $f"; FAIL=1
  fi
  if grep -lE 'AUKUS partnership|DAIC certified|DEFONEOS-SEAL' "$f" >/dev/null 2>&1; then
    echo "GATE FAIL: unsigned claim (AUKUS/DAIC/DEFONEOS-SEAL) in $f"; FAIL=1
  fi
done <<< "$CHANGED"

if [ "$FAIL" -ne 0 ]; then
  echo "pre-push-gates: FAILED — fix naming/codename/claims before push."
  exit 1
fi
echo "pre-push-gates: PASS (naming lock + codename scan + claims scan clean on $(echo "$CHANGED" | grep -c . ) changed files)"
exit 0
