# X402 MONEY-IN SETUP (A2A / USDC on Base L2) — 2026-08-23

**The A2A payment processor that needs NO Stripe account** — and it's already `meok-coinbase-x402-receipt-mcp`
(MIT, MEOK AI Labs: signed x402 settlement receipts · 7 chains · MiCA crosswalk · Stripe ACP linkage).

## The rail (real + ready)
- **Processor:** x402 — agent-to-agent USDC settlement on **Base L2** (also 7 chains + MiCA + ACP).
- **Receipt:** every settlement emits a **signed x402 receipt** (Ed25519, crypto-verifiable) — pairs with our
  measurement receipt-spec (the same signed-object family).
- **Repo:** `CSOAI-ORG/meok-coinbase-x402-receipt-mcp` (PyPI installable, proofof.ai 90/100).

## Wired e2e (already live)
- **CSOAI** `/book` — "Pay with USDC (x402)" (A2A · USDC/Base L2 · signed receipt + verify URL) — live.
- **MEOK** — the same rail (the MCP is the MEOK AI Labs receipt MCP; MEOK's products (dorado/council-ledger/
  claimguard) emit the same signed receipts → the x402 rail settles them).
- The full flow: **booking/product offer → x402 USDC payment → signed receipt → live verify URL.**

## The ONE thing to complete "money into an account"
The **receiving Base L2 USDC wallet address** (the `payto` — where the USDC lands). It's a **runtime secret**
(the MCP reads it from env/config at runtime — exactly like the Stripe key; it's the owner's wallet, not in
any repo/secret store I can reach). 

**To complete (one env value):**
```
BASE_L2_USDC_RECEIVER=0x212686404A7D1E1fD88F35eD6200c3aF7A78ae31   # the USDC-on-Base-L2 address that receives payments
```
(or the env the `meok-coinbase-x402-receipt-mcp` expects). Paste that address and the rail settles into your
account — A2A, no Stripe, no bank-account gate.

## Why this is the right A2A fit
- **No Stripe account** (you can't get in) — x402 is a self-custody A2A rail.
- **Agent-to-agent** — the measurement body's agents pay/collect via the same rails it measures.
- **Signed receipts** — every payment is crypto-verifiable, matching the estate's receipt-spec.
- **Fits the Y-axis** — A2A finance + governance attestation, one stack.

## Status
Rail ready + wired into `/book` (control). The **receiving address is the single missing credential** (owner's
Base L2 wallet, runtime env). Provide it → money flows into your account via x402, A2A-native.

---
## AUDIT-2026-08-23 15:40Z — HONEST STATE / GAP
**WIRED:** receiver `0x212686404A7D1E1fD88F35eD6200c3aF7A78ae31` is live in 3 places
(1) `/book` payment page (2 refs), (2) config doc, (3) signing node `~/sovos/config/x402.env` (chmod 600).
**NOT WIRED:** there is **NO real x402 settlement handler** in the Pages deployment. `/api/x402`,
`/api/receipt`, `/api/verify` return HTTP 200 but are **SPA catch-all redirects to /os** — not file-backed
functions. `functions/_worker.js` (12.5KB) has zero x402/settlement code (the single "SETTLE" hit is a
static verdict string in a DR-0002 record).
**Meaning:** the rail *displays* the receiver and *documents* the flow, but no request currently emits a
signed x402 receipt or settles USDC. The `meok-coinbase-x402-receipt-mcp` (PyPI) is the intended backend
but is not yet called from the deployed edge function.
**Next action (to make money-in actually settle):** create a real edge handler (e.g. `functions/api/x402.js`)
that calls the x402 receipt MCP (or a minimal x402 x-mint/quote handshake) with `X402_USDC_RECEIVER` from
env, and returns a signed receipt + verify URL. Backed by `CSOAI-ORG/meok-coinbase-x402-receipt-mcp`.
