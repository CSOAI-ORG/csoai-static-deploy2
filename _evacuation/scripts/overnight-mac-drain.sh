#!/bin/bash
# overnight-mac-drain.sh — autonomous overnight offload: drain the MacBook
# into the fleet (RunPod volumes / Oracle micros / Google storage when billing
# returns) and log everything. Runs from launch until 04:00 local, then parks.
# Resumable: every shard rsyncs with --partial; re-running skips what landed.
#
# Targets (verified 2026-08-17):
#   sov-brain-2  (RunPod 3090, /root has 144G free)  — big data
#   oracle-micro (Oracle E2, 15G free)               — small/medium data
#   gs://meok-archive-498012/intake/                 — Google (billing-gated)
#
# Log: ~/clawd/_evacuation/logs/overnight-mac-drain.log
set -uo pipefail

export PATH="/opt/homebrew/bin:/usr/local/bin:$HOME/.local/bin:/Users/nicholas/google-cloud-sdk/bin:$PATH"
LOG="$HOME/clawd/_evacuation/logs/overnight-mac-drain.log"
LOCK="$HOME/clawd/_evacuation/.overnight-mac-drain.lock"
mkdir -p "$(dirname "$LOG")"
TS() { date +%Y-%m-%d\ %H:%M:%S; }

# Single-instance guard (LaunchAgent StartInterval + internal loop both fire)
if ! mkdir "$LOCK" 2>/dev/null; then
  echo "$(TS) another instance running — exiting" >> "$LOG"
  exit 0
fi
trap 'rmdir "$LOCK" 2>/dev/null' EXIT

echo "===== overnight-mac-drain start $(TS) =====" >> "$LOG"

RSYNC="/opt/homebrew/bin/rsync"
SSH_OPTS="-o ServerAliveInterval=30 -o ServerAliveCountMax=12 -o ConnectTimeout=10 -o BatchMode=yes"

# Conflict guard: is a live rsync already writing this target? One rsync per
# target, period (duplicate rsyncs write the same temp file = corruption risk).
rsync_active() {  # $1 = marker string that uniquely identifies the target
  pgrep -f "rsync -a --partial" >/dev/null 2>&1 \
    && ps aux | grep -E "[r]sync -a --partial" | grep -q "$1"
}

# ── Stop at 04:00 local (next occurrence — robust regardless of start time) ──
NOW_EPOCH=$(date +%s)
TODAY_0400=$(date -j -f "%Y-%m-%d %H:%M" "$(date +%Y-%m-%d) 04:00" +%s 2>/dev/null || date -d "$(date +%Y-%m-%d) 04:00" +%s 2>/dev/null)
if [ "$NOW_EPOCH" -lt "$TODAY_0400" ]; then
  STOP_EPOCH=$TODAY_0400
else
  STOP_EPOCH=$((TODAY_0400 + 86400))
fi
echo "$(TS) overnight window: until $(date -r $STOP_EPOCH +%H:%M)" >> "$LOG"

while [ "$(date +%s)" -lt "$STOP_EPOCH" ]; do
  # ── Shard 1: opencode.db (5G dormant) → sov-brain-2 (oracle-micro OOMs: 956MB RAM) ──
  if [ -f "$HOME/.local/share/opencode/opencode.db" ] && ! rsync_active "mac-offload/opencode"; then
    echo "$(TS) shard1 rsync opencode.db → sov-brain-2:/root/" >> "$LOG"
    ssh $SSH_OPTS sov-brain-2 'mkdir -p /root/mac-offload/opencode' >> "$LOG" 2>&1
    $RSYNC -a --partial --timeout=60 -e "ssh $SSH_OPTS" "$HOME/.local/share/opencode/opencode.db" sov-brain-2:/root/mac-offload/opencode/ >> "$LOG" 2>&1
    echo "$(TS) shard1 done rc=$?" >> "$LOG"
  fi

  # ── Shard 2: downloads (small) → oracle-micro-2 (verified reachable, 32G free) ──
  if [ -d "$HOME/Downloads" ] && ! rsync_active "mac-offload/Downloads"; then
    echo "$(TS) shard2 rsync Downloads → oracle-micro-2" >> "$LOG"
    ssh $SSH_OPTS oracle-micro-2 'mkdir -p ~/mac-offload/Downloads' >> "$LOG" 2>&1
    $RSYNC -a --partial --timeout=60 -e "ssh $SSH_OPTS" "$HOME/Downloads/" oracle-micro-2:~/mac-offload/Downloads/ >> "$LOG" 2>&1
    echo "$(TS) shard2 done rc=$?" >> "$LOG"
  fi

  # ── Shard 3: Google storage (only works when billing re-enabled) ────────────
  gcloud storage ls "gs://meok-archive-498012/" >/dev/null 2>&1 \
    && gcloud storage cp -r "$HOME/Downloads/"* "gs://meok-archive-498012/intake/" >> "$LOG" 2>&1 \
    && echo "$(TS) shard3 gcs copy ok" >> "$LOG" \
    || echo "$(TS) shard3 gcs skipped (billing gate)" >> "$LOG"

  # ── Shard 3.5: Claude vm_bundles (8G regenerable VM sandbox) → sov-brain-2 ──
  VM_BUNDLE="$HOME/Library/Application Support/Claude/vm_bundles/claudevm.bundle"
  if [ -d "$VM_BUNDLE" ] && ! rsync_active "claude-vm-bundles"; then
    echo "$(TS) shard3.5 rsync claudevm.bundle → sov-brain-2:/root/" >> "$LOG"
    ssh $SSH_OPTS sov-brain-2 'mkdir -p /root/mac-offload/claude-vm-bundles' >> "$LOG" 2>&1
    $RSYNC -a --partial --timeout=60 -e "ssh $SSH_OPTS" \
      "$VM_BUNDLE/" sov-brain-2:/root/mac-offload/claude-vm-bundles/claudevm.bundle/ >> "$LOG" 2>&1
    echo "$(TS) shard3.5 done rc=$?" >> "$LOG"
  fi

  # ── Shard 4: claude-science orgs (45G = one 47.9GB sqlite + small dirs) ────
  # Single-file rsync is the proven-stable pattern (tree-scan kept 255-ing).
  SRC="$HOME/.claude-science/orgs/afd8d9ac-019f-4b20-9510-5402272d5585"
  if [ -d "$SRC" ] && [ -f "$SRC/operon-cli.db" ] && ! rsync_active "claude-science-orgs"; then
    echo "$(TS) shard4 rsync operon-cli.db → sov-brain-2:/root/" >> "$LOG"
    $RSYNC -a --partial --timeout=60 -e "ssh $SSH_OPTS" \
      "$SRC/operon-cli.db" sov-brain-2:/root/claude-science-orgs-afd8d9ac/operon-cli.db >> "$LOG" 2>&1
    echo "$(TS) shard4 big-file done rc=$?" >> "$LOG"
    # small dirs once, ignore-existing (never re-copy the big file)
    $RSYNC -a --ignore-existing --timeout=60 -e "ssh $SSH_OPTS" \
      "$SRC/" sov-brain-2:/root/claude-science-orgs-afd8d9ac/ >> "$LOG" 2>&1
    echo "$(TS) shard4 small-dirs done rc=$?" >> "$LOG"
  fi

  # ── Loop pacing: 30 min between passes (transfers are long-lived anyway) ────
  echo "$(TS) pass complete — sleep 1800" >> "$LOG"
  sleep 1800
done

echo "===== overnight-mac-drain parked $(TS) (04:00 reached) =====" >> "$LOG"
