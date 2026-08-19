# VALS AI TEARDOWN — CONFIRMED OPENINGS (K3 #82, research delivered 2026-08-19)
**Competitive research · never contacted, never echoed · every claim dated**

---

## The verified picture (all dated sources)
- **What they measure:** 30+ private expert benchmarks (finance, legal, tax, healthcare, coding, frontier-risk: RSI Index, ProofBench, CyberBench), three-way splits (public / licensed-private / secret), LLM-judge + SME rubrics, SEM error bars, bench retirement when saturated.
- **Business model — ISSUER-PAYS (CONFIRMED):** free public leaderboards + paid private evals **sold to the labs and enterprises it grades**. ~$1.3M 2025 revenue, ~12 staff, 8× growth. $400M valuation (a16z, Aug 13).
- **Crypto signing: NONE (CONFIRMED by absence).** Zero signature/hash/attestation machinery anywhere — every Vals score is a trust-me web number.
- **Conflicts (CONFIRMED, BSKiller Issue #10, 16 Aug, verdict TRUE):** "Vals AI grades AI for the labs that pay it. DISCLOSED: CUSTOMER RELATIONSHIP WITH PARTICIPANTS." Noah Intelligence independently named the same structural conflict (grading investors' portfolio companies while taking their money).

## The three openings (ours, by architecture)
1. **Signed, recomputable result cards** — the verification primitive Vals lacks. We have Ed25519 + 3KB cards + OTS anchoring.
2. **Conflict-free revenue** — demand-side only (buyers/regulators), published funding wall, **no money from either direction** (our EZ firewall). The exact inverse of BSKiller's finding.
3. **"Private until retired, public forever after"** — anchored publication timestamps. Vals' economics depend on permanent secrecy; it cannot follow.

## The 90-day execution plans (from full teardown — fire these)
**Opening 1 (signed cards):** ship signed cards for 1 flagship axis (finance or coding) + a public verifier + a "signed-verification wall" listing every Vals score without a signed card.
**Opening 2 (conflict-free):** publish the funding-wall charter; sign 2–3 buyer-side design partners (procurement/regulator-adjacent); issue the first no-issuer-money evaluation of a frontier model, signed.
**Opening 3 (auditable transparency):** publish validation set + correlation proof for one axis; publish a "retirement release" of one already-retired benchmark (**CorpFin — Vals retired it May 2026; we can re-measure it openly**); anchor the publication calendar.

**Cross-cutting (optional 4th):** the frontier-risk axes (safety, sovereignty, alignment, human-vs-AI) are where Vals' coverage is newest (RSI Index launched 13 Aug) and where regulators buy — a signer with a neutral-funding wall can own "the safety scorecard with receipts" before Vals' brand hardens there.

## Doctrine re-confirmed
- Never partner with Vals, never take their money, never echo their scores without re-measurement.
- Independence is the moat: issuer-pays = the attack surface. We are the measurer nobody owns.
- Our differentiators (signed · verify-free-forever · no-money-either-direction) are now **empirically validated** as the gap.

## SIGIL
`vals-teardown-2026-08-19-jeeves`
