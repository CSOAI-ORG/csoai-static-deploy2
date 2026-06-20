#!/bin/bash
# VM corpus merge + sign pipeline (Kimi-managed).
# Gathers shards, merges, signs, and optionally trains per-hive models.
# Run manually or schedule on VM cron.

set -euo pipefail

TS=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
P0="/home/nicholas/sovereign-town/p0_aqua"
SHARD_DIR="/data/hive-data/sovereign-town/shards"
MERGED="/data/hive-data/sovereign-town/corpus_merged_${TS}.jsonl"
LOG="/home/nicholas/sovereign-town/runners/vm/merge-sign.log"
mkdir -p "$SHARD_DIR" "$(dirname "$LOG")"

echo "[$TS] Starting merge+sign" >> "$LOG"

# 1. Collect any new shards
SHARDS=$(find "$SHARD_DIR" -maxdepth 1 -name 'corpus_shard_*.json' -type f 2>/dev/null | sort)
if [ -z "$SHARDS" ]; then
  echo "[$TS] No shards found in $SHARD_DIR" >> "$LOG"
  exit 0
fi

# 2. Merge (simple JSON newline concat)
: > "$MERGED"
for s in $SHARDS; do
  /usr/bin/python3 - "$s" >> "$MERGED" <<'PY'
import json, sys
with open(sys.argv[1]) as f:
    data = json.load(f)
for row in data.get('rows', []):
    print(json.dumps(row))
PY
done

COUNT=$(wc -l < "$MERGED" | tr -d ' ')
echo "[$TS] Merged $COUNT rows -> $MERGED" >> "$LOG"

# 3. Sign merged corpus
SIGNATURE=$(cd "$P0" && /usr/bin/python3 - "$MERGED" <<'PY' 2>/dev/null
import json, sys, sign_lib
with open('.town_priv.key') as f: priv = f.read().strip()
rows = [json.loads(l) for l in open(sys.argv[1])]
body = json.dumps(rows, sort_keys=True)
sig = sign_lib.sign(priv, body)
print(sig)
PY
)

METADATA="/data/hive-data/sovereign-town/corpus_meta_${TS}.json"
/usr/bin/python3 - "$MERGED" "$SIGNATURE" "$COUNT" "$TS" > "$METADATA" <<'PY'
import json, sys, hashlib
merged_path, sig, count, ts = sys.argv[1:]
with open(merged_path, 'rb') as f:
    sha = hashlib.sha256(f.read()).hexdigest()
json.dump({
    "merged": merged_path,
    "sha256": sha,
    "signature": sig,
    "rows": int(count),
    "timestamp": ts
}, sys.stdout, indent=2)
PY

echo "[$TS] Signed metadata -> $METADATA" >> "$LOG"

# 4. Optional: train per-hive models if GPU available (commented until GPU credits)
# (cd "$P0" && /usr/bin/python3 train_all_hives.py --corpus "$MERGED") >> "$LOG" 2>&1 || true

# 5. Move processed shards to archive
mkdir -p "$SHARD_DIR/archive"
mv $SHARDS "$SHARD_DIR/archive/"
echo "[$TS] Done" >> "$LOG"
