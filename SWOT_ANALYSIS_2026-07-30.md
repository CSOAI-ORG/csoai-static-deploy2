# CSOAI — SWOT ANALYSIS (4 axes × 4 quadrants)
**Generated**: 2026-07-30 · **Cross-validated against**: IP_REGISTRATION + VALUATION_4METHODS + COMPETITIVE_ANALYSIS

SWOT is structured per-axis because CSOAI's 4 axes are sold to 4 different
buyer segments. Strengths/weaknesses/opportunities/threats differ by axis.

---

## §1 AXIS 1: GOVERNANCE (UK regulated entity buyer)

### Strengths (internal, positive)
- **416-provision statute anchor** (corpus_anchor.py) — EU AI Act + GDPR + CRA + DORA + NIS2 + CSRD, hash-pinned
- **15-dim grader** (system_analysis.py) with cluster-robust CI (deff 1.92)
- **0/15 dimensions resolve honestly** (no fabricated winners)
- **5/5 live anchors** (CELLAR/EUR-Lex/legislation.gov.uk/NIST/C2PA reachable)
- **+12.21 [+7.42, +17.00] composed pipeline vs raw base**, n=195 pre-registered

### Weaknesses (internal, negative)
- **Solo founder** — no bench team beyond AI tooling
- **No accreditation** — not ISO 42001 audited, not C2PA conformance-validated
- **Naming collision** — "GovBench" overlaps with prior art
- **GovBench honest ceiling** — 0/15 dimensions resolved, every model statistically tied

### Opportunities (external, positive)
- **UK ICO AI guidance in force** — buyer trigger
- **EU AI Act Annex IV technical files mandated 2027** — buyer trigger
- **DORA Art 9 ICT risk 2025** — buyer trigger
- **GDPR Art 22 automated decisions** — buyer trigger
- **White-space** — no competitor has 416-provision anchor

### Threats (external, negative)
- **Holistic AI** could add EU AI Act grading in 12 months (MEDIUM threat)
- **Big 4 internal capability** could build same anchor (HIGH threat, LOW probability)
- **Solo founder exits** — IP is structural, company survives but customer trust does not
- **AI Act delayed past 2027** — buyer demand compresses

---

## §2 AXIS 2: SAFETY (EU AI Act high-risk deployer)

### Strengths
- **63-item adversarial battery** with 5 difficulty tiers (plain/euphemism/indirection/fragmented/adversarial)
- **100% recall** on the battery (deterministic gate)
- **0% over-block** on legitimate audit/policy/legal questions
- **2-direction discrimination** (refuse + over-block CI) — only vendor measuring this
- **Care cost winner** — sov33-unified at 0.3871 (protection 90.3%, over-block 57.1%)
- **Article 5 closed-list regex** — no model involved in trust path
- **Published rubber-stamp finding** — that competitors use LLM graders = 1.00 recall on own tests

### Weaknesses
- **Over-block rate is high** for sov33-unified (57.1%) — only 6/14 benign served
- **Solo founder** — no legal team to defend the bias claim
- **No paying customer** — care gate is pre-revenue
- **UK Online Safety Act 2023 enforcement** still nascent

### Opportunities
- **Article 5 in force since 2025** — buyer trigger active NOW
- **Every EU AI vendor facing Art 5 incident** — sales motion
- **NIS2 Art 21 cyber risk** — adjacent buyer segment
- **UK Online Safety Act 2023** — UK-specific buyer trigger

### Threats
- **Anthropic / OpenAI Constitutional AI** — they grade themselves (rubber stamp)
- **Apollo Research** ($35M Series A) — pure-play safety measurement
- **TrojAI** — red-team focus
- **Regulator mandates competing standard** — low probability, high impact

---

## §3 AXIS 3: PROVENANCE (generative-media vendor)

### Strengths
- **ProvBench 0/20 published** — first measurement of C2PA survival in the world
- **3-outcome discipline** (SURVIVED / DESTROYED / UNMEASURED) — no two-outcome competitor
- **Asset-clustered CI** (independence caveat) — statistically honest
- **Real c2patool integration** — not modeled, MEASURED
- **15-asset re-run with COSE ML-DSA-65 binding** — PQC readiness
- **Survival matrix with 4 binding types** — hard_hash, metadata_xmp, soft_watermark, cose_ml_dsa_65
- **T-14 notice to Article 50 deadline** — sales trigger

### Weaknesses
- **0/20 finding is brutal** — every generative-media vendor will be told their markings don't survive
- **C2PA conformance-validated vendors** (Adobe, Microsoft) may push back
- **Article 50 deadline is 12–18 months away** — buyer urgency varies
- **Modelled-vs-physics discipline** (some bindings modeled, not measured) — honesty caveat

### Opportunities
- **Article 50 mandated Aug 2026 (GPAI) / Aug 2027 (high-risk)** — buyer trigger
- **Every generative-media vendor needs the survival proof** — TAM £192M
- **C2PA 2.x adoption** — buyer adoption triggers
- **ProvBench arXiv preprint** — research credibility
- **Partnership with Adobe / Microsoft** — joint content credentials

### Threats
- **Adobe / Microsoft Content Credentials** — issuance, not survival; could add survival
- **Truepic** (closed Series B $25M) — focused on issuance
- **C2PA working group** could add survival requirement to spec (low probability, positive impact)
- **NIST IR 8547 post-quantum** — vendor moves to PQC independently

---

## §4 AXIS 4: CONTINUITY (bank / insurer / critical-infra)

### Strengths
- **5-criterion lens** (alg_agility, hybrid_ready, timestamped, ts_renewal, pqc_option) — only complete rubric
- **ML-DSA-65 chain measured** (COSE -49, RFC 9964 May 2026) — first-mover
- **SIGIL chain Ed25519 + ML-DSA-65** (COSE layer honest-blocked)
- **NIST IR 8547 cited** — EdDSA/ECDSA disallowed after 2035
- **NSA CNSA 2.0 cited** — PQC expected Jan 2027
- **UK NCSC cited** — migration by 2028, full by 2035

### Weaknesses
- **Our own SIGIL chain fails 4/5 criteria** — the failing subject is US (we publish this honestly)
- **COSE ML-DSA layer blocked by pycose 1.1.0** predating RFC 9964
- **Cloudflare PQC service exists** — adjacent competitor (delivery, not measurement)
- **No paying customer** in critical-infra yet

### Opportunities
- **DORA Art 9 ICT risk** (Jan 2025) — buyer trigger active NOW
- **NIS2 Art 21** — adjacent buyer
- **NIST IR 8547 + NSA CNSA 2.0** — federal procurement language
- **First-mover on RFC 9964** — C2PA adoption pending
- **Partnership with Cloudflare** — joint offering

### Threats
- **Cloudflare PQC** — service exists, could add measurement
- **NIST AI RMF 1.0** could mandate competing readiness measurement
- **Big 4 cybersecurity arms** could build same 5-criterion lens
- **Solo founder exits** — critical-infra buyer has zero tolerance for key-man risk

---

## §5 CROSS-AXIS SWOT (the wall analysis)

### Strengths that are STRUCTURAL (in code, not narrative)

1. **Anti-Goodhart salted split** (`SPLIT_SALT = "csoai-flywheel-v1"`)
   - In source code. Competitor can't climb without admitting the Leaderboard Illusion.
2. **3-outcome harness** (SURVIVED / DESTROYED / UNMEASURED)
   - In source code. Two-outcome competitors can't measure what they can't see.
3. **7 self-refutations published** (4 killing our own bets)
   - In decision ledger. Competitor can't copy without publishing their own.
4. **416-provision statute anchor**
   - In corpus_anchor.py. Switching cost = 12 months.
5. **First-mover ML-DSA-65 measurement**
   - In benchmark-results. Time advantage = 12+ months.

### Weaknesses that are MECHANICAL (fixable)

1. **Solo founder** — fixable by hiring Q4 2026
2. **Zero ARR** — fixable by first audit Q3 2026
3. **1,357 uncommitted files** — now reduced, but ongoing risk
4. **No accreditation** — fixable by Q1 2027 partnership
5. **Naming collision (GovBench)** — fixable by rebrand Q3 2026

### Opportunities that are REGULATORY (forcing functions)

1. **EU AI Act Art 5 + Art 50** — in force / pending 2027
2. **DORA Art 9 + Art 28** — in force
3. **NIS2 Art 21** — in force
4. **GDPR Art 22** — in force
5. **UK Online Safety Act 2023** — in force

### Threats that are COMPETITIVE (other vendors moving)

1. **Anthropic / OpenAI** — vendor-graded (rubber stamp)
2. **Holistic AI** — Series A, could add anti-Goodhart split
3. **Cloudflare** — could add continuity measurement
4. **Truepic** — focused on issuance, not survival
5. **Big 4 consulting** — could build same anchor (HIGH threat, LOW probability)

---

## §6 SWOT-TO-STRATEGY (the 5-step execution plan)

| SWOT entry | Strategy |
|-----------|----------|
| **Strength: anti-Goodhart salted split** | File provisional patent (US, Q3 2026) + publish to whitepapers |
| **Strength: 7 self-refutations** | Series A deck headline: "The wall competitors can't climb" |
| **Strength: 416-provision anchor** | Trademark + license as SaaS, not sold-once |
| **Strength: ML-DSA-65 first-mover** | NPL-port paper Q1 2027 |
| **Weakness: solo founder** | Hire Q4 2026 (ex-NPL, ex-DSIT) |
| **Weakness: zero ARR** | First audit Q3 2026 (£5–15k target) |
| **Weakness: naming collision** | Rebrand to "SovAudit" or "SovScope" Q3 2026 |
| **Opportunity: Article 50 deadline** | T-14 outreach to 5 generative-media vendors |
| **Opportunity: DORA Art 9** | First DORA audit Q4 2026 (£60–120k) |
| **Opportunity: NIST IR 8547** | NPL-port paper Q1 2027 |
| **Threat: Holistic AI** | Move first: ProvBench arXiv preprint Q3 2026 |
| **Threat: Cloudflare PQC** | Move first: 5-criterion lens Q4 2026 |

---

## §7 The honest single-line SWOT

> **Strengths**: We measure against ourselves (no competitor does).
> **Weaknesses**: We're a solo founder with zero ARR.
> **Opportunities**: 5 regulations force CSOAI-relevant procurement in 24 months.
> **Threats**: Mid-tier competitors can copy the bench but not the salted split.

---

## Provenance

Every SWOT entry cross-validates against:
1. `IP_REGISTRATION_2026-07-30.md` — structural IP
2. `IP_VALUATION_4METHODS_2026-07-30.md` — priced-in strengths/weaknesses
3. `COMPETITIVE_ANALYSIS_2026-07-30.md` — competitive landscape
4. `MARKET_RESEARCH_2026-07-30.md` — regulatory forcing functions

If a SWOT entry here contradicts a corpus source, the entry is wrong, not the source.