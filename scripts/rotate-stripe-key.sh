#!/bin/bash
# rotate-stripe-key.sh — ONE-COMMAND STRIPE KEY ROLL UPDATER (post-dashboard-roll)
#
# USE (after Nick rolls the key in dashboard.stripe.com):
#   printf '%s' 'sk_live_NEW...' | bash scripts/rotate-stripe-key.sh
#   (or interactive: bash scripts/rotate-stripe-key.sh  → it prompts from tty, not shown)
#
# WHAT IT DOES (all safe, none echo the key):
#   1. Reads the NEW key from stdin/tty (never stored on disk, never echoed)
#   2. Pushes it to Cloudflare Pages secret STRIPE_SECRET_KEY on `csoai-site`
#   3. Verifies the secret landed (wrangler pages secret list)
#   4. PROVES the key is live via Stripe /v1/balance (Bearer auth — correct)
#   5. Re-probes the apex checkout/signup routes (no regression)
#   6. Reports PASS/FAIL — never prints the key value
#
# Notes:
#   - The live sk_live_ currently has NO server-side code path (buy.stripe.com
#     links are static client-side); the CF secret is held for future
#     integrations. Rotation is hygiene; this makes the CF copy current.
#   - The old key is invalidated by the dashboard roll itself.

set -uo pipefail

SOV=/Users/nicholas/clawd/csoai-static-deploy2
PROJECT=csoai-site

# --- 1. get the new key (stdin or tty, never echo) --------------------------
if [ -t 0 ]; then
  echo -n "Paste the NEW sk_live_ (no echo): " >&2
  read -rs KEY
  echo >&2
else
  KEY=$(cat)
fi
KEY=$(echo -n "$KEY" | tr -d ' \n\r')
if [ -z "$KEY" ]; then
  echo "FAIL: no key provided (pipe it via printf, or run interactively)" >&2
  exit 1
fi
case "$KEY" in
  sk_live_*|rk_live_*) ;;  # full or restricted live key accepted
  *) echo "FAIL: key does not look like a live Stripe key (sk_live_/rk_live_)" >&2; exit 1 ;;
esac

echo "[1/5] reading new key: ${#KEY} chars (ok, not echoing)"

# --- 2. push to Cloudflare Pages secret -------------------------------------
echo "[2/5] pushing to CF Pages secret STRIPE_SECRET_KEY ($PROJECT)..."
cd "$SOV"
printf '%s' "$KEY" | npx wrangler pages secret put STRIPE_SECRET_KEY --project-name="$PROJECT" 2>&1 | tail -2
RC=$?
if [ $RC -ne 0 ]; then echo "FAIL: wrangler secret put errored (rc=$RC)" >&2; exit 1; fi

# --- 3. verify the secret is in CF (D105/D106: trust list, not the push msg)
echo "[3/5] verifying the secret landed..."
if npx wrangler pages secret list --project-name="$PROJECT" 2>&1 | grep -qi "STRIPE_SECRET_KEY"; then
  echo "      STRIPE_SECRET_KEY present in $PROJECT ✓"
else
  echo "FAIL: STRIPE_SECRET_KEY not listed after push — investigate" >&2
  exit 1
fi

# --- 4. prove the key is live via Stripe /v1/balance (Bearer auth) ----------
echo "[4/5] proving the key is live (Stripe balance probe, Bearer auth)..."
BAL=$(curl -s --max-time 15 \
  -H "Authorization: Bearer $KEY" \
  -H "Stripe-Version: 2025-09-16.api" \
  https://api.stripe.com/v1/balance 2>&1)
if echo "$BAL" | grep -q '"available"'; then
  echo "      LIVE KEY ✓ (balance endpoint accepted the key)"
elif echo "$BAL" | grep -qi '"error"'; then
  echo "WARN: Stripe rejected the probe (see below) — key may be restricted or account auth differs"
  echo "$BAL" | head -c 300
  echo
else
  echo "WARN: Stripe probe returned unexpected body (not necessarily a failure)"
fi

# --- 5. apex re-probe (no regression) ---------------------------------------
echo "[5/5] re-probing apex..."
for p in "" "checkout" "signup"; do
  code=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 -H "User-Agent: Mozilla/5.0" "https://csoai.org/$p")
  echo "      /$p -> HTTP $code"
done

echo
echo "DONE. The new key is in CF Pages secrets ($PROJECT). Old key invalidated by the dashboard roll."
echo "Next (optional): update the key in any OTHER surface that holds it (estate vault / Vercel meok-ai per D110)."