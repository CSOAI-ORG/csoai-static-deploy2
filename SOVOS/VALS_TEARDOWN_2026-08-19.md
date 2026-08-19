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

## Doctrine re-confirmed
- Never partner with Vals, never take their money, never echo their scores without re-measurement.
- Independence is the moat: issuer-pays = the attack surface. We are the measurer nobody owns.
- Our differentiators (signed · verify-free-forever · no-money-either-direction) are now **empirically validated** as the gap.

## SIGIL
`vals-teardown-2026-08-19-jeeves`
