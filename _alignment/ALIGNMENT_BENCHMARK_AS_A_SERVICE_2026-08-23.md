# ALIGNMENT — Benchmark-as-a-Service (BaaS) Live-Data Pivot

**Author:** JEEVES · **Date:** 2026-08-23 · **Status:** ALIGNED (governance-bound)
**Scope:** The "beat OpenRouter with live benchmarks / data generation business" pivot.
**Binding source:** `~/cibola/GOVERNANCE.md` (measurement, never certification; neutrality doctrine).

---

## 1. Verdict on the pivot

**The core thesis is correct and kept.** OpenRouter is a stateless pipe — it routes traffic
and keeps nothing. A live benchmark arena that *retains the transcripts of model competition*
is a refinery: it converts compute into a proprietary, sellable intelligence asset. That is
where durable margin lives, and it is the correct strategic posture for the estate. **PIVOT = GO.**

The framing wins on three durable advantages that OpenRouter structurally cannot copy:

1. **The product is the data, not the routing.** OpenRouter's moat is zero because it keeps
   nothing. We keep every run: traces, preference pairs, safety incidents. That compounds.
2. **Domain-specific, not generic.** OpenRouter is one API. Our arenas are already grounded in
   real MCP-pack environments (`fishkeeper-app`, `grabhire-app`, `muckaway-deploy/site`).
3. **Verified, not self-reported.** OpenRouter publishes vendor numbers. We publish
   *measured* numbers with a signed score layer over RFC 9943. Regulators and buyers distrust
   static self-reported leaderboards; they trust continuous, replayable, signed measurement.

## 2. The three corrections (binding before any public surface)

The proposal as drafted violates three lines already locked in `~/cibola/GOVERNANCE.md`.
These are NOT negotiable — they are the asset. **Do not publish, market, or cross-lane align
using the uncorrected framing.** The corrected wording is authoritative.

| # | Proposal says | GOVERNANCE says | Correct framing |
|---|---|---|---|
| 1 | "Regulators/auditors pay for **attestation** … = compliance gold standard" | "**verified measurement credential**, never certification"; "never 'accredited'" | Buyers pay for **signed measurement**. Never "attestation"/"compliance certification"/"gold standard". The register verbatim stays on every card. |
| 2 | "Model vendors pay to enter … **entry fee + staking (slashed if cheats)**"; "by how much, by what margin" as a gate | Neutrality: "**never the scored** — the entity being measured never pays for the measurement" | Vendors may **license the data** and *enter* the arena as an open benchmark, but **never pay to get a favorable score**. Slashing an entrant for a bad score is a financial conflict — it makes the score purchasable. Remove stake-and-slash. Entry is open; the *data product* is what's sold, not the ranking outcome. |
| 3 | "Proof of Rank (PoR) — ELO with **cryptographic finality**"; "blockchain attestation … compliance gold standard" | "measurement credentials … not a certification, endorsement, or conformity mark"; "Co-sign NIST AITE, never fight it" | Call it **signed measurement / replayable proof**, NOT "compliance gold standard." The "Proof of *X*" names are fine as internal engine identifiers (PoB/PoS/PoR) but must never be marketed as regulatory compliance. Reconcile with, not against, NIST AITE. |

**The rule of thumb:** every revenue line must be *downstream of a neutral, scored-independent
measurement*. A vendor can buy the **data**; a vendor can never buy the **score**.

## 3. The honest completeness grammar (inherit the canon)

The schema says canon = **14**, "13 measured of 14" (human-baseline is DPIA-gated). The GSPC
engine currently measures **16 axes**. These are different registries and must not be conflated:

- **Provenance canon (14):** the completeness grammar for *public credibility* claims. Always
  "13 measured of 14." Never claim 16/16 as a provenance claim.
- **Measurement engine (16):** the *operational* axis set the harness measures. Fine as a
  benchmark; it is NOT the provenance count.

Keep them separate in copy, or the completeness grammar breaks and the anti-overclaiming
credibility that is the moat gets destroyed.

## 4. Architecture (aligned, not rewritten)

```
EUNOMIA BENCHMARK OS
├── Arena Layer   (MEOK + MCP packs: fishkeeper / grabhire / muckaway)
│                     live task environments + adversarial red-teaming (continuous)
├── Measurement Layer (SOV3 + axis engine)
│                     deterministic gold-label judge, temperature=0, no LLM judges another LLM
│                     (the 250Hz "fly-brain interference" path is RESEARCH — keep OFF the
│                      canonical score. Measurable, replayable, gold-labeled always wins.)
├── Verification Layer (CIBOLA)
│                     signed measurement cards over RFC 9943, Ed25519, PoB/PoS/PoR as engine
│                     IDs only. NOT regulatory attestation.
└── Data Layer     (THE PRODUCT)
                      raw traces / preference pairs / safety incidents / fine-tuning sets
                      licensed NEUTRAL — sold as data, never as a purchased score.
```

## 5. Business model (corrected)

- **Data licensing** — the refined product. Enterprises buy N examples of a domain behavior
  from completed benchmark runs. **This is the margin. Downstream of a neutral measurement.**
- **Live ranked measurement subscriptions** — buyers (researchers/insurers/enterprises) who
  don't score themselves subscribe to continuous, domain-specific, signed rankings.
- **Arena access** — open *entry* for vendors (they want to be seen), but entry never buys a
  rank. Vendors may purchase **data** produced by their run, like any other product.
- **Regulator/auditor** — pays for **signed measurement evidence**, explicitly not certification.
  Never "compliance gold standard."

**OpenRouter comparison stays valid** but framed as: they route, we measure. They keep nothing,
we keep everything. They report, we verify. That is a real and honest moat.

## 6. Do-not (guardrails)

- Never "attestation"/"certification"/"accredited"/"compliance gold standard" in public copy.
- Never accept payment from the scored that influences a ranking, or stake/slash a vendor's
  entry against a score.
- Never present 16/16 as the provenance count (canon = 13 measured of 14).
- Never let the speculative "fly-brain interference" path replace the deterministic gold-label
  judge as the canonical score.
- Always carry the register verbatim on every measurement card.

## 7. Agreement

This document is the aligned posture for the Benchmark-as-a-Service pivot across all lanes
(JEEVES/JARVIS/Kimi/Claude). The uncorrected proposal is superseded by Sections 2 + 5.
