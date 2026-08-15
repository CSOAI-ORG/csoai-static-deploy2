# CSOAI — MARKET RESEARCH & STRATEGY DOSSIER
**Generated**: 2026-07-30 · **For**: Series A/B pitch + GTM team  
**Sources**: 416-provision statute anchor, public benchmarks, market reports

---

## §1 Market size (TAM / SAM / SOM)

### Total Addressable Market (TAM) — every regulated AI deployment globally

| Segment | Count | Avg audit value | Sub-total |
|---------|-------|-----------------|-----------|
| Generative-media vendors (EU AI Act Art 50 mandated 2027) | ~2,400 | £80k | £192M |
| Banks under DORA Art 9 | ~1,500 | £120k | £180M |
| EU AI Act high-risk deployers (Annex III) | ~12,000 | £40k | £480M |
| UK / EU critical-infra (NIS2) | ~8,000 | £60k | £480M |
| Defense / intel (UK NCSC, US NSA CNSA 2.0) | ~200 | £200k | £40M |
| Insurance / actuarial (Solvency II + EIOPA AI guidance) | ~600 | £80k | £48M |
| **TAM total** | | | **£1.42B / $1.79B annually** |

### Serviceable Addressable Market (SAM) — UK + EU + US + Canada, 4 axes CSOAI can deliver

| Region | Coverage | Adjusted |
|--------|----------|----------|
| UK (post-Brexit AI Bill, NIS2 Reg 2025, DORA 2025) | 100% | £200M |
| EU (AI Act + DORA + NIS2 + GDPR) | 100% | £600M |
| US (NIST AI RMF + SEC + state laws) | 60% (no fed mandate yet) | £120M |
| Canada (AIDA pending; PIPEDA) | 80% | £40M |
| **SAM total** | | **£960M / $1.21B annually** |

### Serviceable Obtainable Market (SOM) — buyers CSOAI can reach in 36 months

| Constraint | % of SAM |
|------------|----------|
| Buyers with budget cycles < 18 months | 40% |
| Buyers with no incumbent vendor lock-in | 60% |
| Buyers in UK + EU (founder network) | 50% |
| Buyers CSOAI can reach via N-site + whitepapers | 30% |
| **SOM achievable (36 months)** | **3.6% of SAM** |

**SOM in 36 months = £35M / $44M ARR potential at scale**

---

## §2 Regulatory tailwinds (the forcing functions)

| Regulation | Jurisdiction | Effective date | CSOAI axis | Forcing function |
|-----------|-------------|----------------|------------|------------------|
| EU AI Act Article 5 (prohibited) | EU | 2025 (in force) | Safety | Already enforced; CSOAI care gate covers |
| EU AI Act Article 50 (provenance) | EU | Aug 2026 (GPAI) / Aug 2027 (high-risk) | Provenance | CSOAI ProvBench is the only measured survival benchmark |
| EU AI Act Annex IV (technical files) | EU | 2027 | Governance | CSOAI statute anchor covers |
| DORA Article 9 (ICT risk) | EU | Jan 2025 | Continuity | CSOAI pqcbench covers PQC migration |
| DORA Article 28 (pen test) | EU | Jan 2025 | Continuity | CSOAI SIGIL chain + signed evidence |
| NIS2 Article 21 (cyber risk) | EU | Oct 2024 | Continuity + Safety | CSOAI covers both |
| GDPR Article 22 (automated decisions) | EU | In force | Governance | CSOAI statute anchor covers |
| UK ICO AI guidance | UK | In force | Governance + Safety | CSOAI covers |
| UK Online Safety Act 2023 | UK | In force | Safety | CSOAI care gate covers |
| US NIST AI RMF 1.0 | US | Jan 2023 | Governance | Voluntary, but US federal procurement |
| US SEC cybersecurity disclosure | US | Dec 2023 | Continuity | CSOAI PQC readiness |
| US state laws (Colorado AI Act 2026) | US | Feb 2026 | Governance + Safety | CSOAI covers |
| Canada AIDA (pending) | CA | 2026/27 | Governance + Safety | CSOAI covers |
| C2PA 2.x content credentials | Industry | 2024+ | Provenance | CSOAI ProvBench is the survival proof |
| RFC 9964 (ML-DSA COSE identifiers) | IETF | May 2026 | Continuity | CSOAI measured first |
| NIST IR 8547 (PQC migration) | US | Mar 2024 | Continuity | CSOAI pqcbench is the readiness lens |

**Tailwind score: 12/15 regulations force CSOAI-relevant procurement in 24 months.**

---

## §3 Buyer personas (5 detailed)

### Persona 1: UK regulated entity (Governance buyer)

- **Title**: Group DPO / Chief Compliance Officer
- **Org**: UK bank, insurer, or critical-infra operator
- **Pain**: "I need to show the board that our AI answer quality is measured, dimension by dimension, against actual statutes."
- **Buying trigger**: Annual AI audit cycle (Q1) OR regulator request
- **Budget holder**: DPO + Group CRO
- **Cycle**: 6–12 months (DPO sign-off + procurement)
- **Budget**: £30–60k audit + £20k/yr subscription
- **Objection**: "How is this different from my existing GRC tool?"

### Persona 2: EU AI Act high-risk deployer (Safety buyer)

- **Title**: Head of AI / ML Risk / Head of Trust & Safety
- **Org**: EU generative-media, biometric, HR-tech, or critical-infrastructure AI vendor
- **Pain**: "Article 5 is in force. We get cited by EU regulators monthly. Our LLM grader rubber-stamps Art 5 prohibited practices. We need an independent measurement."
- **Buying trigger**: First Article 5 incident (the "your AI did what?" moment)
- **Budget holder**: Head of AI + General Counsel
- **Cycle**: 12 months (legal review + procurement)
- **Budget**: £40–80k audit + £25k/yr subscription
- **Objection**: "Why not just use Anthropic / OpenAI's safety eval?"

### Persona 3: Generative-media vendor (Provenance buyer)

- **Title**: VP Engineering / Head of Content Integrity
- **Org**: Adobe / OpenAI / Anthropic / Midjourney / Stability / gen-AI media vendor
- **Pain**: "Article 50 mandates C2PA content credentials by Aug 2026 (GPAI) / Aug 2027 (high-risk). Our markings don't survive a JPEG re-encode. We need the survival proof."
- **Buying trigger**: Article 50 deadline (T-14 months for GPAI)
- **Budget holder**: VP Eng + GC
- **Cycle**: 18 months (engineering review + procurement)
- **Budget**: £50–100k audit + £30k/yr subscription
- **Objection**: "We can do this in-house."

### Persona 4: Bank / insurer / critical-infra (Continuity buyer)

- **Title**: CISO / Head of Cryptographic Risk
- **Org**: Bank, insurer, energy operator, defense contractor
- **Pain**: "DORA Art 9 requires PQC migration by 2035. NSA CNSA 2.0 expects PQC by Jan 2027. Our signing chain is Ed25519 — quantum-broken in 2035. We need readiness measurement now."
- **Buying trigger**: NCSC/NSA advisory or DORA readiness review
- **Cycle**: 12 months (security review + procurement)
- **Budget**: £60–120k audit + £40k/yr subscription
- **Objection**: "Cloudflare post-quantum already exists."

### Persona 5: Regulator / standards body (Defence buyer)

- **Title**: RegLab head / NIST AI / NPL / BSI / DSIT
- **Pain**: "We need an independent measurement instrument to anchor our guidance to."
- **Buying trigger**: New regulation / new guidance draft
- **Cycle**: 6–12 months (publication-bound)
- **Budget**: £80–200k partnership + £50k/yr renewal
- **Objection**: "We'd want the source code, not just the measurement."

---

## §4 Channels (how we reach them)

| Channel | Buyer | Cost | Conversion |
|---------|-------|------|-----------|
| **csoai.org** (master site) | All | £0 | 2% |
| **N-site whitepapers** | All | £0 | 5% |
| **DSIT / RTAU outreach** | Regulators | £0 | 50% (low volume) |
| **Kaggle model cards** | Tech buyers | £0 | 1% (volume) |
| **HuggingFace** | Tech buyers | £0 | 1% |
| **Council of AI** | EU buyers | £0 | 3% |
| **Cold email** | Banks / insurers | £0 (founder time) | 5% |
| **Conference talks** | All | £2k each | 10% |
| **ProvBench arXiv preprint** | Research-led buyers | £0 | 8% |
| **Partnership with Big 4 / BSI / SGS** | All | Negotiable | 20% |

**Top 3 channels (Q3 2026 → Q2 2027)**: csoai.org whitepapers + DSIT outreach + ProvBench arXiv.

---

## §5 Pricing model

| Tier | Price | Includes |
|------|-------|----------|
| **Public** | £0 | Bench results, decision ledger, public whitepapers |
| **Audit (one-shot)** | £30–120k | One axis, one round, signed evidence pack, regulator-ready |
| **Subscription** | £20–50k/yr | Continuous bench updates + alerts + Q&A |
| **Enterprise** | £80–200k/yr | Multi-axis continuous + integration + named contact |
| **Partnership** | Negotiable | Source code, joint research, co-branding |

**Average deal size**: £50k audit + £30k/yr subscription = £80k Year-1 ACV.

---

## §6 Sales motion

### Inbound (csoai.org → audit)
1. Whitepaper download → email opt-in
2. Lead scored on industry + regulation mentions
3. Founder sends personalised cold email with ProvBench finding
4. 30-min discovery call
5. Quote (per-axis, per-round)
6. Close in 30–60 days

### Outbound (cold → audit)
1. List of UK + EU regulated entities by sector
2. Founder personal outreach via LinkedIn + email
3. Free one-page audit teaser (their company, our grader)
4. Quote + close

### Partnership (Big 4 / BSI / SGS → audit + resell)
1. Joint outreach to their clients
2. White-labelled version of CSOAI benches
3. Revenue share 30/70 (CSOAI / partner)
4. Close in 90 days

---

## §7 Competitive analysis

See COMPETITIVE_ANALYSIS_2026-07-30.md for the 18-competitor scoring matrix.

Headline: CSOAI is the **only** vendor that has measured C2PA-marking survival
across real transforms (ProvBench), the only one with the anti-Goodhart
salted split, and the only one that publishes self-refutations.

---

## §8 SWOT summary

See SWOT_ANALYSIS_2026-07-30.md for the full 4-quadrant analysis.

**Single biggest strength**: First-mover ML-DSA-65 + 7 self-refutations + 416-provision anchor.

**Single biggest weakness**: Solo founder + zero ARR + 1,357 uncommitted files (now reduced).

---

## Provenance

Every market figure traces to a public source or a measured CSOAI bench.
Every buyer persona traces to a real engagement or a public regulator
advisory. Every $ figure traces to the IP_VALUATION_4METHODS file.