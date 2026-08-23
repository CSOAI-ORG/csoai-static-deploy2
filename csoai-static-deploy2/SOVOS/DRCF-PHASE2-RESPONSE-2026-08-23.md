# DRCF Phase 2 response — regulators' consumer-interest AI call
To: drcf@ofcom.org.uk · From: CSOAI Ltd (UK 16939677) · Date: 2026-08-23 (draft, owner to send)
Submitted as an independent measurement body for AI behaviour. Measurement, not certification.

## 1. Who we are (one line)
CSOAI is an **independent, non-profit, measurement body** for AI behaviour: we run open-weight models
through a deterministic governance-axes battery, sign every result (Ed25519, RFC 9943 / SCITT-aligned
COSE receipt), and publish an honest register — **UNMEASURED cells are reported, never hidden.**

## 2. The consumer-interest problem we address
Regulators are right that consumers cannot currently verify what an AI system *does*. They are told
vendor claims ("safe", "responsible", "aligned") with no neutral, checkable evidence. The gap is not
more claims — it is a **stranger-verifiable measurement layer** between the claim and the consumer.

## 3. What we propose (the honest-register mechanic)
- **Deterministic, not a jury.** We never grade a model with another model. Scores come from
  deterministic exact-label predicates against gold instruments — reproducible by anyone.
- **Signed + offline-verifiable.** Every result is a signed, `not_a_certification` card. A consumer or
  regulator recomputes the content_id and checks the Ed25519 signature with no account, no fee, no trust.
- **Disagreement is a row (the honest register).** If our own number is shown wrong, we publish a
  correction — append-only, never a hidden edit. A body that publishes when its own measurement was
  wrong is the only kind a relying party can depend on.
- **Independence is the asset.** We never take money from the parties we measure, never re-score for
  payment, never rank a payer. That neutrality is what makes a stranger *trust* the signature.
- **Transparency as a consumer right.** Where the EU AI Act GPAI code-of-practice obliges providers to
  produce model documentation + transparency evidence, the neutral measurement body is the checkable
  form that evidence should take — not a vendor's own self-report.

## 4. Why this fits the consumer-interest intent
The consumer-interest lens is: does the consumer get **true, usable, checkable** information? A signed,
deterministic, honest measurement card is exactly that. It is not a stamp or a cert — it is a
**verifiable fact with a published honesty record**, which is the strongest consumer-protection form
that AI transparency can take today.

## 5. Recommendation
- Treat **independent, signed, deterministic measurement** as the trust layer for consumer-facing AI
  transparency, alongside (not instead of) the regulator's own oversight.
- Adopt the **honest-register convention** (a wrong number becomes a published correction) as a
  transparency best practice.
- Encourage providers to publish **verifiable, not self-reported**, model-behaviour evidence.

_Signed: CSOAI Ltd · Measurement, not certification · verification free forever · nobody ranked pays._
