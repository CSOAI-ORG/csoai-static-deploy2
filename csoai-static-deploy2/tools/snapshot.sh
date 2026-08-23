#!/usr/bin/env bash
# tools/snapshot.sh — timestamped full backup of csoai-static-deploy2/
# Owner-gated: runs only if csoai-static-deploy2/.git/ exists OR --force flag passed.
# Schedule via com.meok.deploy-snapshot.plist (LaunchAgent; owner loads it manually).
#
# Usage:
#   ./tools/snapshot.sh                  # creates .backups/YYYY-MM-DD_HHMMSS/
#   ./tools/snapshot.sh --force          # bypass owner gate (debug only)
#   ./tools/snapshot.sh --keep N         # retain N most-recent backups (default 7)
#
# Output:
#   .backups/YYYY-MM-DD_HHMMSS/    — full mirror of all deploy dir files
#   .backups/LATEST -> YYYY-MM-DD_HHMMSS  — symlink to most-recent backup
#   .backups/manifest-YYYY-MM-DD_HHMMSS.txt — file count + sha256 of each file
#
# Side-effects: creates .backups/ if missing. Does NOT modify anything inside deploy root.

set -euo pipefail

# Resolve deploy root (parent of tools/) regardless of invocation cwd
DEPLOY_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BACKUPS="${DEPLOY_ROOT}/.backups"
KEEP=3   # was 7 — 7 full mirrors is what filled the disk
FORCE=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --force) FORCE=1; shift ;;
    --keep)  KEEP="$2"; shift 2 ;;
    --keep=*) KEEP="${1#*=}"; shift ;;
    *) echo "snapshot.sh: unknown arg $1" >&2; exit 64 ;;
  esac
done

# Owner gate: refuse unless .git exists (which means git init was run by us) or --force.
if [[ ! -d "${DEPLOY_ROOT}/.git" && $FORCE -eq 0 ]]; then
  echo "snapshot.sh: refusing to run — no .git/ in ${DEPLOY_ROOT}" >&2
  echo "snapshot.sh: either run 'git init' + 'git commit' first, or pass --force for debug" >&2
  exit 77
fi

mkdir -p "${BACKUPS}"

TS="$(date -u +%Y-%m-%d_%H%M%S)"
DEST="${BACKUPS}/${TS}"
MANIFEST="${BACKUPS}/manifest-${TS}.txt"

mkdir -p "${DEST}"

# Mirror the full deploy directory into the timestamped backup.
# We deliberately exclude .backups/ itself (would recurse forever), .vercel/ (build cache),
# .git/ (the git dir is its own history), and tmp scratch files.
cd "${DEPLOY_ROOT}"
COUNT=0
SKIPPED=0
SKIPPED_BYTES=0
TOTAL_BYTES=0
{
  echo "# snapshot manifest — ${TS} UTC"
  echo "# deploy_root=${DEPLOY_ROOT}"
  echo "# host=$(hostname -s 2>/dev/null || hostname)"
  echo "# format: <sha256>  <bytes>  <path>"
  echo
  while IFS= read -r -d '' f; do
    rel="${f#./}"
    case "$rel" in
      .backups/*|.vercel/*|.git/*|./.backups/*|./.vercel/*|./.git/*) continue ;;
    esac
    SIZE=$(wc -c < "$f" | tr -d ' ')
    SHA=$(shasum -a 256 "$f" | awk '{print $1}')
    # Manifest EVERY file (hash + size) — the integrity record stays complete.
    printf '%s  %s  %s\n' "$SHA" "$SIZE" "$rel" >> "$MANIFEST"

    # 2026-07-28 — DO NOT COPY MODEL WEIGHTS.
    # This snapshot ran every 6h keeping KEEP=7 full mirrors, each carrying two 988MB
    # LoRA safetensors. That is ~14GB of the SAME weights duplicated on a timer, and it
    # filled the Mac's disk to 0 bytes free — which took down the shell entirely.
    # Weights are large, immutable, and already exist at asi_results/adapters/ (and belong
    # on HuggingFace, not in a local backup). A backup's job here is to preserve CODE and
    # CONFIG; a GB-scale binary copied verbatim 7 times is not a backup, it is a leak.
    # The manifest above still records each weight's sha256 + size, so the snapshot can
    # still PROVE what the weights were — it just doesn't hoard another copy of them.
    case "$rel" in
      *.safetensors|*.gguf|*.bin|*.pt|*.pth|*.ckpt|*.onnx|*.tar.gz|*.zip)
        if [ "$SIZE" -gt 52428800 ]; then          # >50MB only; small .bin/.zip still copied
          SKIPPED=$((SKIPPED + 1))
          SKIPPED_BYTES=$((SKIPPED_BYTES + SIZE))
          continue
        fi
        ;;
    esac

    mkdir -p "${DEST}/$(dirname "$rel")"
    cp -p "$f" "${DEST}/${rel}"
    COUNT=$((COUNT + 1))
    TOTAL_BYTES=$((TOTAL_BYTES + SIZE))
  done < <(find . -type f -print0 | sort -z)
} 

# Update / refresh the LATEST symlink atomically.
ln -sfn "${TS}" "${BACKUPS}/LATEST"

# Prune old backups beyond --keep (keep manifest + dir).
if [[ -d "${BACKUPS}" ]]; then
  # List timestamped backup dirs oldest-first; remove all but the most-recent $KEEP.
  # Portable: don't rely on bash mapfile (bash 4+) or GNU find -printf (Linux).
  # Use plain find -exec + sort + read into a bash 3.2 array.
  ALL=()
  while IFS= read -r d; do
    base=$(basename "$d")
    [[ "$base" == "LATEST" ]] && continue
    ALL+=("$base")
  done < <(find "${BACKUPS}" -maxdepth 1 -mindepth 1 -type d | sort)
  if (( ${#ALL[@]} > KEEP )); then
    REMOVE_COUNT=$((${#ALL[@]} - KEEP))
    for ((i=0; i<REMOVE_COUNT; i++)); do
      OLD="${BACKUPS}/${ALL[$i]}"
      rm -rf "$OLD"
      rm -f "${BACKUPS}/manifest-${ALL[$i]}.txt"
    done
  fi
  # Also prune orphan manifests.
  for m in "${BACKUPS}"/manifest-*.txt; do
    [[ -e "$m" ]] || continue
    base=$(basename "$m" .txt)
    base="${base#manifest-}"
    if [[ ! -d "${BACKUPS}/${base}" ]]; then
      rm -f "$m"
    fi
  done
fi

# Report skipped weights explicitly. Silent omission from a backup is how you discover, at
# restore time, that the thing you needed was never in it. Manifested-but-not-copied is a
# deliberate, stated choice — so say it out loud on every run.
printf 'snapshot ok: ts=%s files=%d bytes=%d manifest=%s\n' \
  "$TS" "$COUNT" "$TOTAL_BYTES" "$MANIFEST"
if (( SKIPPED > 0 )); then
  printf 'snapshot: SKIPPED %d large model/archive file(s), %d bytes NOT copied (>50MB).\n' \
    "$SKIPPED" "$SKIPPED_BYTES"
  printf 'snapshot: their sha256+size ARE in the manifest. Source of truth: asi_results/adapters/ + HuggingFace.\n'
fi

# Self-restoration is impossible if this script is itself inside the deployment directory tree
# and the deployment got blown away. The companion plist restores from the most recent backup
# before the snapshot step.

exit 0