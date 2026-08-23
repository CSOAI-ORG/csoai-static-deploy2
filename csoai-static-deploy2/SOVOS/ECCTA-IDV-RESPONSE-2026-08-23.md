# ECCTA Identity Verification (IDV) — response from an independent measurement body
To: Companies House / ECCTA IDV consultation · From: CSOAI Ltd (UK 16939677) · Date: 2026-08-23 (draft, owner to send)
Measurement, not certification. Verification free forever. Nobody ranked pays.

## 1. What ECCTA IDV needs
The Economic Crime and Corporate Transparency Act makes **identity verification** a core part of
company formation and the PSC (persons with significant control) regime: a director or PSC proves who
they are to Companies House. The point is trust — a stranger (another company, a regulator, a
counterparty) should be able to rely on the identity behind a company, not just take a self-declaration.

## 2. How a neutral measurement body supports it
CSOAI is an independent measurement body for AI behaviour. Our exact mechanic — **deterministic,
signed, honest, stranger-verifiable** — is the shape of evidence ECCTA IDV is reaching for:

- **Signed + offline-verifiable.** An Ed25519-signed measurement card (SCITT / RFC 9943-aligned COSE
  receipt). Anyone recomputes the content_id + checks the signature — no account, no fee, no trust.
- **Deterministic, not a jury.** We never grade with a model; scores come from deterministic exact-label
  predicates against gold instruments — reproducible by anyone.
- **The honest register (disagreement-is-a-row).** If our own number is shown wrong, we publish a
  correction — append-only, never a hidden edit. That published-honesty record is what makes a stranger
  trust the signature over time.
- **Independence is the asset.** We never take money from the parties we measure, never re-score for
  payment. Neutrality is what makes the attestation credible to a relying third party.

## 3. The fit
AI systems increasingly make the judgement calls behind identity, AML and PSC checks. The consumer /
counterparty interest is: is the check **verifiable** (not just asserted), is the model **measured**
(not vendor-claimed), is the source **independent** (not issuer-paid)? A signed, deterministic,
honest measurement of the checking system is exactly that. It is not a cert — it is a verifiable fact
with a published honesty record, which is the strongest trust form ECCTA IDV can build on.

## 4. Recommendation
- Where an AI system supports ECCTA IDV identity/AML checks, require **independent measure-and-sign**
  evidence (deterministic, stranger-verifiable), alongside the regulator's own oversight.
- Adopt the **honest-register convention** (a wrong measurement becomes a published correction).
- Encourage **verifiable, not self-reported**, behaviour evidence from the checking system.

_Signed: CSOAI Ltd · measurement, not certification · independence is the asset · never issuer-paid._
