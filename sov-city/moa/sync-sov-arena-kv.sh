#!/bin/bash
# sync-sov-arena-kv.sh — live arena rounds from 3090 pod → Cloudflare KV.
# The Pages Function /api/sov-arena/rounds.jsonl serves whatever lands here.
# Crontab: */5 * * * * /Users/nicholas/clawd/sov-city/moa/sync-sov-arena-kv.sh >> /Users/nicholas/clawd/sov-city/moa/sync.log 2>&1
#
# Flow: SSH to 3090 → pull reborn_rounds.jsonl → wrangler kv key put → verify.
# Honest: if the pod is unreachable, logs the failure and exits — does not
# overwrite KV with stale data.
set -u

NS=00634697bf5744edba3625905a922e96
KEY=rounds.jsonl
POD_HOST=194.26.196.156
POD_PORT=12853
POD_KEY=~/.runpod/ssh/runpodctl-ssh-key
POD_SRC=/workspace/arena-24x7/reborn_rounds.jsonl
TMP=/tmp/sov_arena_sync.jsonl
W2D=/Users/nicholas/clawd/csoai-static-deploy2
LOG="$W2D/sync.log"

# 1. Pull the latest rounds from the 3090
echo "--- $(date -u +%FT%TZ) ---"
if ! ssh -o StrictHostKeyChecking=no -o ConnectTimeout=12 -o BatchMode=yes \
    -i "$POD_KEY" -p "$POD_PORT" root@$POD_HOST \
    "cat $POD_SRC 2>/dev/null" > "$TMP" 2>/dev/null; then
    echo "POD UNREACHABLE — cannot pull $POD_SRC" >> "$LOG"
    exit 1
fi
size=$(wc -c < "$TMP" 2>/dev/null || echo 0)
if [ "$size" -lt 10 ]; then
    echo "POD EMPTY — $POD_SRC is $size bytes (arena may be recovering)" >> "$LOG"
    exit 1
fi
echo "pulled $size bytes from $POD_HOST:$POD_PORT" >> "$LOG"

# 2. Write to Cloudflare KV
cd "$W2D"
npx wrangler kv key put --remote --namespace-id "$NS" "$KEY" --path "$TMP" >/tmp/sov_arena_kv_put.log 2>&1
rc=$?
if [ "$rc" -ne 0 ]; then
    echo "KV PUT FAILED rc=$rc — $(tail -1 /tmp/sov_arena_kv_put.log)" >> "$LOG"
    exit 1
fi

# 3. Verify readback
raw=$(npx wrangler kv key get --remote --namespace-id "$NS" "$KEY" 2>/dev/null)
got=${#raw}
sent=$(wc -c < "$TMP")
if [ "$got" -lt 1 ] || [ "$got" -lt "$((sent * 8 / 10))" ]; then
    echo "KV VERIFY FAILED sent=$sent readback=$got — value missing/short" >> "$LOG"
    exit 1
fi
echo "synced OK — $sent bytes to KV, readback $got bytes, $(wc -l < "$TMP" | tr -d ' ') rounds" >> "$LOG"
exit 0