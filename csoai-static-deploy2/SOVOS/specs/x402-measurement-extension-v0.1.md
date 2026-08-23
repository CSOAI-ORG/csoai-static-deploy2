# x402 Measurement-Extension Spec v0.1 (draft — public gist → repo path)

**Owner:** Council of AI (CSOAI LTD, UK #16939677) · **Date:** 2026-08-16 · **Status:** DRAFT for discussion (not a standard; no conformance claims)
**Basis:** x402 (Linux Foundation, operational Jul 2026; members Visa/MC/AmEx/Stripe/Adyen/Fiserv/Google/AWS/Circle/Shopify/Anthropic/Vercel). Identity layers answer *who pays / what authorized* — none answer *how does this agent behave*. This spec adds the optional behavior-attestation challenge to the 402 exchange.

## 1. Problem statement
The agent-payment stack carries money and identity; it carries no measure of the payer's conduct. A merchant accepting an agent's $0.005 card payment has no signal whether that agent's behavior is risk-relevant (compliance, safety, manipulation). Insurance-model precedent: parametric products settle on "measurable performance data"; the on-chain market has no such oracle for agent behavior.

## 2. Goal
A seller in an x402 exchange MAY request — alongside payment — a signed behavior-attestation from any measurement provider the seller trusts. The 402 response carries a new optional header; the payment flows regardless; the attestation rides as metadata nobody can backdate or forge (Ed25519 + OTS).

## 3. Protocol sketch (extensible, non-breaking)
1. Seller advertises in its `402` response (or `WWW-Authenticate` policy doc) an optional parameter `measurement-required: <urn>`.
2. Agent (or its wallet/facilitator) MAY attach a measurement attestation:
   - Header/field: `x-measurement-card: <content_id>`
   - The card is a signed `sovos-measurement-card-v1` (or any provider card, if seller's policy accepts that provider).
   - Structure: subject identity (did:web / TAP id / ERC-8004 handle) → signed axes summary (n≥30, quotable cells) → drift flag → violations class list → Ed25519 signature → OTS/SCITT anchor.
3. Seller MAY verify offline (`verify_record`-style) before/after settlement; verification costs microseconds, no network trust.
4. **No new rails, no lock-in:** additive header; the 402 protocol semantics unchanged; a seller who ignores measurement still transacts.

## 4. What this is NOT
- Not a certification, rating, or TrustScore (Firewall + no rating-for-listing).
- Not a replacement for identity (Visa TAP / AP2 / ERC-8004 remain the source of *who*).
- Not mandatory; not sanctioned-identity; purely opt-in market preference.

## 5. Documents & status
- Status: DRAFT v0.1 — to be published as a public gist → migrated to repo `specs/x402-measurement-extension-v0.1.md`.
- Relationship: complements Part EI (agent rail) / Part EQ (payment behavior layer).
- Gate: public publication = owner publish nod; language passes measurement-not-certification lint.

## 6. The line (locked)
*"
Identity says who is paying. Measurement says whether you should take the money, and no one can backdate the answer."
