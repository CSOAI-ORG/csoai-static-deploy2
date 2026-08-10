#!/usr/bin/env bash
# update_kv_seed.sh — push the OOWM seed to Cloudflare KV (EAT_OWEM / owem_seed)
# Rebuilds the t[:200] payload (fits 25MiB KV ceiling per D113), pushes, verifies.
# Usage: ./update_kv_seed.sh [path/to/oowm_seed_1000.json]
set -euo pipefail

SEED="${1:-/Users/nicholas/clawd/oowm-v7-e2e/oowm_seed_1000.json}"
NS="22f96280dfdf414ab39506336f925280"   # EAT_OWEM
KET="owem_seed"
PAYLOAD_TL="${PAYLOAD_TL:-200}"          # text truncation (bytes) to fit 25MiB
TMP="/tmp/owem_seed_kv.json"

python3 - "$SEED" "$PAYLOAD_TL" "$TMP" <<'PY'
import json, pathlib, sys
seed = json.loads(pathlib.Path(sys.argv[1]).read_text())
tl = int(sys.argv[2])
s = [{"s": d["s"], "d": d["d"], "t": d["t"][:tl]} for d in seed]
b = json.dumps(s, ensure_ascii=False).encode()
if len(b) >= 26214400:  # 25 MiB ceiling (D113)
    raise SystemExit(f"PAYLOAD {len(b)/1e6:.1f}MB EXCEEDS 25MiB — lower PAYLOAD_TL")
pathlib.Path(sys.argv[3]).write_bytes(b)
print(f"payload {len(s)} docs, t[:{tl}], {len(b)/1e6:.1f}MB")
PY

cd /Users/nicholas/clawd/csoai-static-deploy2
echo "--- writing to KV (--remote) ---"
npx wrangler kv key put "$KET" --namespace-id="$NS" --path="$TMP" --remote

echo "--- read-back verify ---"
npx wrangler kv key get "$KET" --namespace-id="$NS" --remote 2>/dev/null \
  | python3 -c "import sys,json; d=json.loads(sys.stdin.read()); print(f'KV VERIFIED: {len(d)} docs, last src={d[-1][\"s\"]}')"
