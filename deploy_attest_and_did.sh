#!/usr/bin/env bash
# deploy_attest_and_did.sh — ONE-SHOT deploy: did:web identity root + external verifier.
#
# Unblocks BOTH open claims at once:
#   • hosts .well-known/did.json at csoai.org  (did:web signer resolves for third parties)
#   • routes the Ed25519 verifier at csoai.org/verify  ("verify without trusting us", live)
#
# ── RUN THIS ────────────────────────────────────────────────────────────────
#   1. AFTER you rotate CLOUDFLARE_API_TOKEN (and `export CLOUDFLARE_API_TOKEN=...`).
#   2. ON THE PRODUCTION SIGNING KEYSTONE (the A100) — so the PUBLISHED key equals the
#      key that actually signs. If you run it on a machine with a different local key,
#      you will publish the wrong identity. (See _alignment/SIGNER_IDENTITY_2026-08-14.md —
#      the estate has >1 signing key; reconcile to ONE before this goes public.)
#
#       export CLOUDFLARE_API_TOKEN=<new-token>
#       ./deploy_attest_and_did.sh
# ─────────────────────────────────────────────────────────────────────────────
set -euo pipefail
cd "$(dirname "$0")"

: "${CLOUDFLARE_API_TOKEN:?rotate + export CLOUDFLARE_API_TOKEN first}"

echo "== 1. regenerate did.json from THIS machine's signing keystone =="
python3 make_did.py

echo "== 2. sync did.json into the Pages deploy dir (_site/.well-known/) =="
mkdir -p _site/.well-known
cp .well-known/did.json _site/.well-known/did.json
grep -o '"x":[^,]*' _site/.well-known/did.json | head -1

echo "== 3. deploy the Pages site (publishes did.json + the honest home) =="
npx wrangler pages deploy _site --project-name csoai-site

echo "== 4. deploy the external verifier worker (routes csoai.org/verify) =="
( cd workers/attest-verify && npx wrangler deploy )

echo "== 5. VERIFY LIVE =="
echo "-- did:web resolves? --"
curl -fsS "https://csoai.org/.well-known/did.json" | head -c 240; echo
echo "-- verifier verifies a real card? --"
python3 - <<'PY'
import json
d = json.load(open("benchmark-results/signed_mcp_card_demo.json"))
c = d["attestation"]["signed_card"]
json.dump({"body": c["body"], "signature": c["signature"],
           "pubkey": c["signer"], "content_id": c["content_id"]}, open("/tmp/verify_payload.json", "w"))
PY
curl -fsS -X POST "https://csoai.org/verify" -H "Content-Type: application/json" \
     --data @/tmp/verify_payload.json
echo
echo "== DONE — if the verifier returned valid:true and did.json served, both claims are now LIVE. =="
