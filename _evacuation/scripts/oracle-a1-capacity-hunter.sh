#!/bin/bash
# oracle-a1-capacity-hunter.sh — retries A1.Flex launch every 15 min via
# com.meok.oracle-a1-hunter LaunchAgent. Tries 3 shapes across 3 availability
# domains. Logs "hit" on success (and stops retrying via marker) / "miss" + reason.
# Log: ~/clawd/_evacuation/logs/a1-hunter.log
# A1.Flex = 4 OCPU / 24 GB / 200 GB boot = £0 forever (Always Free).
# Note: OCI CLI must be on PATH (pip install oci-cli) and ~/.oci/config present.
set -uo pipefail

export SUPPRESS_LABEL_WARNING=True
export PATH="/opt/homebrew/bin:/usr/local/bin:$HOME/.local/bin:$PATH"

LOG="$HOME/clawd/_evacuation/logs/a1-hunter.log"
STDERR="$HOME/clawd/_evacuation/logs/a1-hunter-stderr.log"
MARKER="$HOME/clawd/_evacuation/A1_LAUNCHED.ok"
TS=$(date -u +%Y-%m-%d\ %H:%M:%S)

mkdir -p "$(dirname "$LOG")"

# Stop hunting once an A1 is up (idempotent marker)
if [ -f "$MARKER" ]; then
  echo "$TS A1_ALREADY_LAUNCHED (marker present, hunter exiting)" >> "$LOG"
  exit 0
fi

# Compartment (tenancy) from ~/.oci/config
if [ ! -f "$HOME/.oci/config" ]; then
  echo "$TS FATAL ~/.oci/config missing — cannot hunt A1" >> "$LOG"
  exit 41
fi
TENANCY=$(grep -E '^\s*tenancy\s*=' "$HOME/.oci/config" | head -1 | sed -E 's/^\s*tenancy\s*=\s*//' | tr -d '[:space:]')
if [ -z "$TENANCY" ]; then
  echo "$TS FATAL tenancy OCID not found in ~/.oci/config" >> "$LOG"
  exit 42
fi

# Prerequisite gates: without subnet + image OCID, fail honestly.
IMAGE_ID=""
[ -f "$HOME/clawd/_evacuation/oracle_image_id" ] && IMAGE_ID=$(tr -d '[:space:]' < "$HOME/clawd/_evacuation/oracle_image_id")
SUBNET_ID=""
[ -f "$HOME/clawd/_evacuation/oracle_subnet_id" ] && SUBNET_ID=$(tr -d '[:space:]' < "$HOME/clawd/_evacuation/oracle_subnet_id")
if [ -z "$IMAGE_ID" ] || [ -z "$SUBNET_ID" ]; then
  echo "$TS BLOCKED image_id/subnet_id reference files missing — set oracle_image_id + oracle_subnet_id in ~/clawd/_evacuation/ (owner: provision once via OCI console, then this hunter auto-runs)" >> "$LOG"
  exit 43
fi

# Hunt: 3 shapes x 3 ADs. First success wins and writes the marker.
hit=0

# Inject the fleet SSH key so a launched A1 is immediately reachable
# (a hit without ssh_authorized_keys would waste the £0 Always-Free slot).
SSH_KEY="$(cat "$HOME/.ssh/id_ed25519.pub" 2>/dev/null | tr -d '\n')"
if [ -z "$SSH_KEY" ]; then
  echo "$TS FATAL ~/.ssh/id_ed25519.pub missing — cannot launch SSH-accessible A1" >> "$LOG"
  exit 44
fi

for shape in "4:24" "2:12" "1:6"; do
  ocpus="${shape%%:*}"
  mem="${shape##*:}"
  for ad in 1 2 3; do
    adname="JiTr:UK-LONDON-1-AD-${ad}"
    resp=$(oci compute instance launch \
      --compartment-id "$TENANCY" \
      --availability-domain "$adname" \
      --shape VM.Standard.A1.Flex \
      --shape-config "{\"ocpus\":${ocpus},\"memoryInGBs\":${mem}}" \
      --image-id "$IMAGE_ID" \
      --subnet-id "$SUBNET_ID" \
      --assign-public-ip true \
      --display-name "sovereign-a1-$(date -u +%Y%m%d-%H%M%S)" \
      --metadata "{\"ssh_authorized_keys\": \"${SSH_KEY}\"}" \
      2>&1)
    rc=$?
    if [ $rc -eq 0 ]; then
      echo "$TS HIT $adname {\"ocpus\":${ocpus},\"memoryInGBs\":${mem}} — A1.Flex launched" >> "$LOG"
      touch "$MARKER"
      hit=1
      break 2
    else
      # Extract the OCI error message only (last line, trimmed)
      msg=$(echo "$resp" | grep -oE '"message":\s*"[^"]*"' | tail -1 | sed -E 's/"message":\s*"//; s/"$//')
      echo "$TS miss $adname {\"ocpus\":${ocpus},\"memoryInGBs\":${mem}} :: ${msg:-"$resp"}" >> "$LOG"
    fi
  done
done

if [ $hit -eq 0 ]; then
  echo "$TS all shapes exhausted — no A1 capacity this cycle (retry in 15 min)" >> "$LOG"
fi

# Keep log manageable
tail -2000 "$LOG" > "$LOG.tmp" && mv "$LOG.tmp" "$LOG"