# Mosaic × Munich Re aiSure — Outreach Brief (2026-08-21)
Target: **Dennis Bertram** — SVP, Managing Director Europe, Head of Europe Cyber, **Head of AI
Underwriting**, Mosaic Insurance (Cologne). Contact via the aiSure/Mosaic product page.

## The one-line ask
A 30-minute pilot conversation: can a **signed provision-conformance receipt** be the objective
threshold test inside aiSure's parametric-like settlement?

## Why aiSure (their own language, not ours)
- "Covers AI performance failures using a **parametric-like structure for fast, objective claims**"
  (Munich Re, aiSure page).
- "Claims are settled quickly, **based on measurable performance data**, without lengthy investigations."
- Cover responds when a model "fails to meet **clearly defined performance thresholds**."
→ The mechanism already depends on measurable thresholds. What's missing is an *independently
verifiable instrument* that produces that measurement. The peer literature names it: "missing
AI-specific trigger metric" (arXiv 2605.18784).

## The instrument (30-second demo, already live)
`art50_demo.py` — EU AI Act **Article 50** (live 2 Aug 2026; high-risk deferred to Dec 2027 by the
Digital Omnibus; penalties to €15M / 3% turnover):
- **T0 BINDING** — disclosure + machine-readable marking present → **CONFORMING** (receipt R1,
  content_id 21c20fd0…, Ed25519 sig, kid did:web:csoai.org#card-attestation-1)
- **T1 MID-POLICY** — marking disappears → **NON-CONFORMING** (R2, f0c8f9f9…) — the trigger event
- **T2 AFTER FIX** — restored → **CONFORMING** (R3, d5876917…)
- Chain R1→R2→R3 = the policy's conformance ledger. Any party verifies offline (recompute
  content_id + check signature vs trust root). No trust in CSOAI required.

## Four insertion points
1. **Condition precedent at binding** (the sprinkler certificate of AI cover)
2. **In-force monitoring** — CONFORMING→NON-CONFORMING on frozen text = non-discretionary trigger
3. **Claims settlement** — "breached, and when" deterministically (aiSure's own promise, delivered)
4. **Aggregation/ILS** — fleet-level conformance index = candidate parametric trigger (the literature's gap)

## Honesty guardrails (stated up front)
Measurement, not certification · not loss prediction (we concede Testudo's eval↔loss null result) ·
basis risk stays in the wording · UNMEASURED stays UNMEASURED.

## Precedent
Eticas × Armilla already prices independent audit at up to 20% premium reduction — the buying
behaviour is proven; we supply a cryptographically stronger version of the same input.

## Next
- Verify Omnibus dates against Official Journal publication before any external deck.
- Owner: approve the send (Nick GO for external communications).

## DATE VERIFICATION (2026-08-21, web-verified)
- Art 50 transparency obligations: **apply from 2 Aug 2026** — CONFIRMED (Jones Walker, iubenda).
- High-risk (Annex III) obligations deferred to **2 Dec 2027** by the Digital Omnibus (adopted) —
  CONFIRMED. Annex I products to Aug 2028.
- Penalties: to €15M or 3% worldwide turnover. Legacy provider-side content-marking grace to 2 Dec 2026.
- Sources: joneswalker.com (AI Law blog) · iubenda.com (AI Omnibus adopted) · lexology (Next Stop Omnibus).
