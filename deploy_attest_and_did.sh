#!/usr/bin/env bash
# deploy_attest_and_did.sh — ONE-SHOT deploy: did:web identity root + external verifier.
#
# Unblocks BOTH open claims at once:
#   • hosts .well-known/did.json at csoai.org  (did:web signer resolves for third parties)
#   • routes the Ed25519 verifier at csoai.org/verify  ("verify without trusting us", live)
#
# ── RUN THIS ────────────────────────────────────────────────────────────────
#   Preview first (no changes, no token needed):
#       ./deploy_attest_and_did.sh --dry-run
#
#   Then the real deploy — AFTER rotating CLOUDFLARE_API_TOKEN, ON THE PRODUCTION
#   SIGNING KEYSTONE (the A100) so the PUBLISHED key equals the key that signs:
#       export CLOUDFLARE_API_TOKEN=<paste real token, no angle brackets>
#       ./deploy_attest_and_did.sh
#
#   (See _alignment/SIGNER_IDENTITY_2026-08-14.md — the estate has >1 signing key;
#    reconcile to ONE before this goes public. The script prints the published key.)
# ─────────────────────────────────────────────────────────────────────────────
set -euo pipefail
cd "$(dirname "$0")"

DRY=0
[ "${1:-}" = "--dry-run" ] && DRY=1

run() {  # execute normally; in --dry-run just print what WOULD run
  if [ "$DRY" = 1 ]; then echo "  [dry-run] would run: $*"; else "$@"; fi
}

if [ "$DRY" = 1 ]; then
  echo "== DRY RUN — no files written, no deploy, no token needed =="
  echo "== 1. did:web key that WOULD be published (from this machine's keystone) =="
  python3 - <<'PY'
import sys; sys.path.insert(0, "SOVOS/packages/sovos-city/src")
try:
    from make_did import keystone_pubkey_hex
    pub = keystone_pubkey_hex("~/.sovos/city_ed25519")
    print(f"     pubkey = {pub}")
    print("     did    = did:web:csoai.org")
    print("     ⚠️  is this the PRODUCTION signing key? if not, run on the A100 instead.")
except Exception as e:
    print(f"     (could not read keystone here: {str(e)[:80]})")
PY
else
  : "${CLOUDFLARE_API_TOKEN:?rotate + export CLOUDFLARE_API_TOKEN first (no angle brackets)}"
  echo "== 1. regenerate did.json from THIS machine's signing keystone =="
  run python3 make_did.py
fi

echo "== 2. sync did.json into the Pages deploy dir (_site/.well-known/) =="
run mkdir -p _site/.well-known
run cp .well-known/did.json _site/.well-known/did.json
[ "$DRY" = 0 ] && grep -o '"x":[^,]*' _site/.well-known/did.json | head -1 || true

echo "== 3. deploy the Pages site (publishes did.json + the honest home) =="
run npx wrangler pages deploy _site --project-name csoai-site

echo "== 4. deploy the external verifier worker (routes csoai.org/verify) =="
if [ "$DRY" = 1 ]; then
  echo "  [dry-run] would run: (cd workers/attest-verify && npx wrangler deploy)"
  echo "  route: $(grep -o 'pattern = "[^"]*"' workers/attest-verify/wrangler.toml)"
else
  ( cd workers/attest-verify && npx wrangler deploy )
fi

echo "== 5. VERIFY LIVE =="
if [ "$DRY" = 1 ]; then
  echo "  [dry-run] would: curl https://csoai.org/.well-known/did.json"
  echo "  [dry-run] would: POST a real card to https://csoai.org/verify and expect valid:true"
  echo "== DRY RUN complete — re-run without --dry-run (and with the token) to deploy for real. =="
  exit 0
fi
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
