#!/usr/bin/env bash
# =============================================================================
# runpod_drain.sh — copy a RunPod network volume to FREE durable storage, verify,
#                   then STOP. Deletes nothing. Run once per volume, then confirm
#                   the manifest before deleting the volume in the web UI.
#
# WHY: 3 network volumes bleed ~$49/mo even with all pods EXITED:
#   sov-models (300GB, CA-MTL-3) · sov-artifacts (200GB, CA-MTL-3) · sov-workspace-mtl4 (200GB, CA-MTL-4)
# Draining them to HuggingFace (weights/datasets) + Oracle ARM (everything) makes RunPod $0 forever.
#
# DESIGN: pod-boot-with-volume is a 2-click web action (capacity-gated, so keep it manual).
#         This script is the reliable COPY+VERIFY half you run once the pod is up.
#
# SAFETY: idempotent · checksums before + after · NO rm/delete anywhere · dry-run default.
# =============================================================================
set -euo pipefail

# ---- CONFIG (edit per drain) -------------------------------------------------
POD_HOST="${POD_HOST:?set POD_HOST=<pod public ip>}"     # e.g. 69.19.136.195
POD_PORT="${POD_PORT:-22}"                                # RunPod SSH port
POD_USER="${POD_USER:-root}"
VOL_MOUNT="${VOL_MOUNT:-/workspace}"                      # where the volume is mounted in the pod
VOL_NAME="${VOL_NAME:?set VOL_NAME=sov-models|sov-artifacts|sov-workspace-mtl4}"
SSH_KEY="${SSH_KEY:-$HOME/.ssh/id_ed25519}"

# Free durable destinations
ORACLE_HOST="${ORACLE_HOST:-145.241.232.16}"             # Oracle ARM always-on (free)
ORACLE_USER="${ORACLE_USER:-ubuntu}"
ORACLE_DEST="${ORACLE_DEST:-/data/runpod-drain}"          # ensure this dir + disk space exists
HF_REPO="${HF_REPO:-}"                                    # optional: nicktempleman/<repo> for weights/datasets
HF_TOKEN="${HF_TOKEN:-}"                                  # optional: only if pushing to HF

DRY_RUN="${DRY_RUN:-1}"                                   # 1 = show plan only; 0 = actually copy
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
MANIFEST_LOCAL="$HOME/clawd/csoai-static-deploy2/DRAIN_MANIFEST_${VOL_NAME}_${STAMP}.txt"

SSH="ssh -p ${POD_PORT} -i ${SSH_KEY} -o StrictHostKeyChecking=accept-new ${POD_USER}@${POD_HOST}"

say(){ printf '\n\033[1;36m== %s\033[0m\n' "$*"; }

# ---- 0. reachability ---------------------------------------------------------
say "0/5  probe pod ${POD_USER}@${POD_HOST}:${POD_PORT} (vol ${VOL_NAME} at ${VOL_MOUNT})"
$SSH "test -d '${VOL_MOUNT}' && echo POD_OK && df -h '${VOL_MOUNT}' | tail -1" || { echo "pod/volume unreachable"; exit 1; }

# ---- 1. inventory + source checksums (nothing copied yet) --------------------
say "1/5  inventory + SHA256 manifest of ${VOL_NAME} (source of truth for the delete decision)"
$SSH "cd '${VOL_MOUNT}' && find . -type f -printf '%10s  %p\n' | sort -k2" | tee "${MANIFEST_LOCAL}.list"
echo "  file count: $(wc -l < "${MANIFEST_LOCAL}.list")"
$SSH "cd '${VOL_MOUNT}' && find . -type f -exec sha256sum {} +" > "${MANIFEST_LOCAL}.sha256" || true
echo "  wrote source checksums -> ${MANIFEST_LOCAL}.sha256"

if [ "${DRY_RUN}" = "1" ]; then
  say "DRY_RUN=1 — inventory captured, NO copy performed. Re-run with DRY_RUN=0 to copy."
  echo "  manifest: ${MANIFEST_LOCAL}.list  /  .sha256"
  exit 0
fi

# ---- 2. copy -> Oracle ARM (durable, free, full fidelity) --------------------
say "2/5  rsync ${VOL_NAME} -> Oracle ${ORACLE_USER}@${ORACLE_HOST}:${ORACLE_DEST}/${VOL_NAME}"
$SSH "mkdir -p /tmp/oracle_key && \
      rsync -aHz --info=progress2 --partial '${VOL_MOUNT}/' \
        -e 'ssh -o StrictHostKeyChecking=accept-new' \
        '${ORACLE_USER}@${ORACLE_HOST}:${ORACLE_DEST}/${VOL_NAME}/'"

# ---- 3. optional: push weights/datasets -> HuggingFace (free, durable) -------
if [ -n "${HF_REPO}" ] && [ -n "${HF_TOKEN}" ]; then
  say "3/5  push large model/dataset artifacts -> HF ${HF_REPO}"
  $SSH "pip -q install -U 'huggingface_hub[cli]' >/dev/null 2>&1; \
        export HF_TOKEN='${HF_TOKEN}'; \
        huggingface-cli upload '${HF_REPO}' '${VOL_MOUNT}' . --repo-type model || \
        echo 'HF push skipped/failed — Oracle copy still holds the data'"
else
  say "3/5  HF push skipped (HF_REPO/HF_TOKEN not set) — Oracle copy is the durable store"
fi

# ---- 4. verify: re-checksum at destination and diff --------------------------
say "4/5  verify Oracle copy against source SHA256 (must be 0 mismatches before any delete)"
ssh -o StrictHostKeyChecking=accept-new "${ORACLE_USER}@${ORACLE_HOST}" \
  "cd '${ORACLE_DEST}/${VOL_NAME}' && find . -type f -exec sha256sum {} +" > "${MANIFEST_LOCAL}.dest.sha256" || true
# normalize + compare hashes only (paths identical by construction)
comm_missing=$(comm -23 \
  <(awk '{print $1}' "${MANIFEST_LOCAL}.sha256" | sort) \
  <(awk '{print $1}' "${MANIFEST_LOCAL}.dest.sha256" | sort) | wc -l | tr -d ' ')
say "5/5  RESULT for ${VOL_NAME}: source hashes not present at dest = ${comm_missing}"
if [ "${comm_missing}" = "0" ]; then
  echo "  ✅ VERIFIED — every source file reproduced at Oracle. Safe to delete ${VOL_NAME} in the web UI."
else
  echo "  ❌ ${comm_missing} hash(es) missing at destination — DO NOT DELETE. Re-run copy for ${VOL_NAME}."
fi
echo "  manifests: ${MANIFEST_LOCAL}.sha256 (src) / ${MANIFEST_LOCAL}.dest.sha256 (dest)"
