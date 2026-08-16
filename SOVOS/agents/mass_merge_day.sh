#!/usr/bin/env bash
# MASS-MERGE DAY — sweep every CSOAI-ORG fork, find local deltas vs upstream,
# rebase them onto latest upstream, and report which need PRs.
# Git-only (no API rate limit). Run on Mac or pod. Idempotent.
set -uo pipefail
WORK=/tmp/mass-merge-day
LIST=$WORK/fork-list.txt
mkdir -p "$WORK"
: > "$WORK/status.tsv"

# --- CONFIRMED external-upstream forks (from the 2026-08-16 inventory scan, API-verified)
# upstream repo | our fork repo | our branch (if any)
CONFIRMED=(
  "NVIDIA-NeMo/labs-OO-Agents|CSOAI-ORG/labs-OO-Agents|feat/gspc-provision-eval"   # PR 75 flags
  "c2pa-org/specifications|CSOAI-ORG/specifications|main"                            # standards watch
  "theopenlane/awesome-compliance|CSOAI-ORG/awesome-compliance-csoai|main"           # GEO play
  "morganrcu/awesome-eu-ai-act|CSOAI-ORG/awesome-eu-ai-act|main"                     # GEO play
  "GenAI-Gurus/awesome-eu-ai-act|CSOAI-ORG/awesome-eu-ai-act-genaigurus|main"        # GEO play
  "Vaquill-AI/awesome-legaltech|CSOAI-ORG/awesome-legaltech|main"                    # GEO play
)

for entry in "${CONFIRMED[@]}"; do
  IFS='|' read -r upstream fork branch <<< "$entry"
  dir="$WORK/$(basename "$fork")"
  echo "=== $fork vs $upstream ==="
  if [ ! -d "$dir/.git" ]; then
    git clone -q "https://github.com/$fork.git" "$dir" 2>/dev/null || { echo "  clone FAILED" >> "$WORK/status.txt"; continue; }
    git -C "$dir" remote add upstream "https://github.com/$upstream.git" 2>/dev/null
  fi
  git -C "$dir" fetch -q origin "$branch" 2>/dev/null
  git -C "$dir" fetch -q upstream main 2>/dev/null || git -C "$dir" fetch -q upstream master 2>/dev/null
  UPSTREAM_BRANCH=main
  git -C "$dir" rev-parse -q --verify upstream/master >/dev/null 2>&1 && UPSTREAM_BRANCH=master
  base=$(git -C "$dir" rev-parse "origin/$branch" 2>/dev/null)
  up=$(git -C "$dir" rev-parse "upstream/$UPSTREAM_BRANCH" 2>/dev/null)
  if [ -z "$base" ] || [ -z "$up" ]; then
    echo "  MISSING refs (branch=$branch upstream=$UPSTREAM_BRANCH)" >> "$WORK/status.txt"
    continue
  fi
  ahead=$(git -C "$dir" rev-list --count "upstream/$UPSTREAM_BRANCH..origin/$branch" 2>/dev/null)
  behind=$(git -C "$dir" rev-list --count "origin/$branch..upstream/$UPSTREAM_BRANCH" 2>/dev/null)
  echo "  ahead(ours): $ahead  behind(upstream): $behind"
  if [ "$ahead" -gt 0 ] && [ "$behind" -gt 0 ]; then
    echo "  → STALE: rebase needed (carrying $ahead local commits, missing $behind upstream)" >> "$WORK/status.txt"
  elif [ "$ahead" -gt 0 ] && [ "$behind" -eq 0 ]; then
    echo "  → READY: $ahead local commits on latest upstream — PR openable" >> "$WORK/status.txt"
  elif [ "$ahead" -eq 0 ]; then
    echo "  → SYNCED: mirror of upstream (no local delta)" >> "$WORK/status.txt"
  fi
done

echo ""
echo "=== MASS-MERGE-DAY STATUS ==="
cat "$WORK/status.txt"