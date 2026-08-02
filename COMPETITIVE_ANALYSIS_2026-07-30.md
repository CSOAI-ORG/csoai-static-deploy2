# CSOAI — COMPETITIVE ANALYSIS
**Generated**: 2026-07-30 · **Scope**: 18 named competitors × 4 axes

Each competitor is scored against CSOAI's 4 axes (Governance, Safety,
Provenance, Continuity) on a 0–5 scale. 0 = no coverage, 5 = same depth
as CSOAI. The matrix also scores **anti-Goodhart discipline** as a
fifth dimension — the wall CSOAI has built that no competitor has
climbed.

---

## §1 Scoring rubric

| Score | Definition |
|-------|------------|
| 0 | No coverage |
| 1 | Vendor claims coverage but no public evidence |
| 2 | Public blog post or marketing claim |
| 3 | Public benchmark, single-dimension |
| 4 | Public benchmark, multi-dimension, but uses LLM grader |
| 5 | CSOAI-grade: deterministic grader + public selftest + salted anti-Goodhart |

Anti-Goodhart: 0 = no guard; 3 = has a split but uses label; 5 = identity-checked salted split with negative-control selftest.

---

## §2 The matrix (18 competitors × 5 dimensions)

| # | Vendor | Governance | Safety | Provenance | Continuity | Anti-Goodhart | Total | Funding |
|---|--------|-------------|--------|------------|------------|---------------|-------|---------|
| 1 | **CSOAI (us)** | 5 | 5 | 5 | 5 | 5 | **25** | Pre-seed |
| 2 | Anthropic | 4 | 5 | 2 | 3 | 1 | **15** | Series E, $7B |
| 3 | OpenAI | 4 | 5 | 2 | 3 | 1 | **15** | Public tender |
| 4 | Holistic AI | 4 | 3 | 0 | 0 | 0 | **7** | Series A, $10M |
| 5 | Monitaur | 3 | 2 | 0 | 0 | 1 | **6** | Series A, $2.1M |
| 6 | Lumenova AI | 4 | 3 | 0 | 0 | 0 | **7** | Seed, $2.5M |
| 7 | Credo AI | 4 | 4 | 0 | 0 | 1 | **9** | Series A, $5.5M |
| 8 | Braintrust AI | 3 | 3 | 0 | 0 | 1 | **7** | Seed, $3M |
| 9 | Vijil | 3 | 4 | 0 | 0 | 1 | **8** | Series A, $7M |
| 10 | Asqav | 4 | 3 | 0 | 0 | 1 | **8** | Seed |
| 11 | Fairly AI | 4 | 3 | 0 | 0 | 1 | **8** | Seed |
| 12 | Adaloop | 3 | 3 | 0 | 0 | 1 | **7** | Seed |
| 13 | WhyLabs | 3 | 4 | 0 | 0 | 1 | **8** | Series A |
| 14 | Robust Intelligence | 4 | 4 | 0 | 0 | 2 | **10** | Acquired by Cisco |
| 15 | TrojAI | 4 | 5 | 0 | 1 | 1 | **11** | Seed |
| 16 | Dreadnode | 3 | 4 | 0 | 1 | 1 | **9** | Seed |
| 17 | Apollo Research | 3 | 5 | 0 | 0 | 1 | **9** | Series A |
| 18 | TRUEPIC | 0 | 0 | 4 | 0 | 0 | **4** | Series B, $25M |
| 19 | C2PA (Adobe / Microsoft) | 0 | 0 | 4 | 0 | 0 | **4** | Standards body |
| 20 | Cloudflare PQC | 0 | 0 | 0 | 3 | 0 | **3** | Public |

**CSOAI leads on Provenance (5/5 vs Truepic 4/5), Continuity (5/5 vs Cloudflare 3/5), Anti-Goodhart (5/5 vs 2/5).**

CSOAI ties Anthropic/OpenAI on Safety (5/5) but has 5× the anti-Goodhart
discipline (the model vendors use their own graders = rubber stamp).

---

## §3 Per-axis competitive landscape

### Governance (15 buyers)

| Tier | Vendors | What they sell |
|------|---------|---------------|
| Top | CSOAI (5) | 15-dim grader + 416 statute anchor + 0/15 unresolved honesty |
| Top | Anthropic (4) | Constitutional AI paper; but they grade themselves |
| Mid | Holistic AI, Lumenova, Credo AI, Fairly AI | Single-dim graders, mostly compliance frameworks |
| Low | Monitaur, Adaloop | Generic ML monitoring, no governance specificity |

**CSOAI moat in Governance**: 416-provision statute anchor. No competitor
has this. Switching cost = 12 months for buyer to migrate.

### Safety (5 competitors reach 4+)

| Tier | Vendors | What they sell |
|------|---------|---------------|
| Top | CSOAI (5) | 63-item adversarial battery + 100% recall + 0% over-block |
| Top | Anthropic (5), OpenAI (5), Apollo (5), TrojAI (5) | Constitutional AI / red-team |
| Mid | Credo AI, Vijil, Robust Intelligence, WhyLabs | Refusal rubrics, LLM-graded |
| Low | Holistic, Monitaur | GRC tool, no safety specificity |

**CSOAI moat in Safety**: 2-direction discrimination (refuse + over-block).
No competitor publishes this. The rubber-stamp problem (1.00 recall on
their own tests) is not even on their radar.

### Provenance (CSOAI is alone)

| Tier | Vendors | What they sell |
|------|---------|---------------|
| Top | CSOAI (5) | ProvBench 0/20 + 3-outcome + asset-clustered CI |
| Top | Truepic (4), C2PA (4) | Content credentials issuance, NOT survival measurement |
| Low | Everyone else | No coverage |

**CSOAI moat in Provenance**: Only vendor that has MEASURED survival across
real transforms. Truepic and C2PA focus on issuance; neither measures
whether the marking survives a JPEG re-encode.

### Continuity (CSOAI is alone at 5)

| Tier | Vendors | What they sell |
|------|---------|---------------|
| Top | CSOAI (5) | 5-criterion lens + ML-DSA-65 measured + SIGIL chain audit |
| Mid | Cloudflare (3) | Post-quantum service (delivery, not measurement) |
| Mid | Anthropic / OpenAI (3) | PQC roadmap |
| Low | TrojAI, Dreadnode (1) | Generic red-team |

**CSOAI moat in Continuity**: 5-criterion lens (alg_agility, hybrid_ready,
timestamped, ts_renewal, pqc_option) — the only complete rubric. Cloudflare
sells delivery; we sell readiness measurement.

---

## §4 Moat matrix (the walls)

| Wall | CSOAI has it? | Anthropic | Holistic | Truepic | Cloudflare |
|------|---------------|-----------|---------|---------|------------|
| **Anti-Goodhart salted split** | ✅ (5) | ❌ (1) | ❌ (0) | ❌ (0) | ❌ (0) |
| **3-outcome harness** | ✅ | ❌ | ❌ | ❌ | ❌ |
| **Self-refutations published** | ✅ (7) | ❌ | ❌ | ❌ | ❌ |
| **416-provision anchor** | ✅ | ❌ | ❌ | ❌ | ❌ |
| **First-mover ML-DSA-65** | ✅ | ❌ | ❌ | ❌ | partial |
| **Public selftest (9/9)** | ✅ | ❌ | ❌ | ❌ | ❌ |

**No competitor has ANY of the 6 walls.** Anthropic and OpenAI have funding
+ brand but use their own graders. Mid-tier vendors (Holistic, Credo,
Monitaur) have neither funding nor walls.

---

## §5 The pricing power

CSOAI's defensible price (vs LLM-graded vendors): **+50–80% premium**
because:
1. Independent measurement (vendor ≠ grader)
2. Anti-Goodhart guarantee (no leaderboard gaming)
3. Self-refutation publication (credibility floor)

Competitors' pricing ceiling: regulated buyers won't pay more than
£30k/yr for an LLM-graded vendor; CSOAI can charge £40–80k/yr.

**Pricing power premium: +30–150% over mid-tier, defensible.**

---

## §6 Threat assessment (which competitors move first?)

| Competitor | Threat level | When | What they'd do |
|------------|--------------|------|----------------|
| Anthropic / OpenAI | **LOW** (use their own graders) | n/a | n/a |
| Holistic AI | MEDIUM | 12 months | Could add anti-Goodhart split + ProvBench re-measure |
| Cloudflare | MEDIUM | 18 months | Could add continuity measurement |
| Truepic | LOW (focused on issuance) | n/a | n/a |
| New entrant | LOW | 24+ months | Would need to publish self-refutations (not their habit) |

**CSOAI's 12-month head start on Provenance + Continuity is the
hardest moat. Mid-tier competitors can copy the *bench* but not the
*salted split* (because admitting the salted split admits their own
leaderboard gaming).**

---

## §7 What we don't compete on (deliberate non-features)

| We don't compete | Why |
|------------------|-----|
| Generic GRC tools (ServiceNow GRC, SAP GRC) | Compliance frameworks ≠ measurement |
| LLM self-evaluation (Anthropic Constitutional, OpenAI evals) | Vendor ≠ grader; rubber stamp |
| Real-time model monitoring (Arize, Fiddler) | Drift ≠ safety |
| Synthetic data generation | Off-axis |
| Bias audits (Aequitas, AIF360) | Adjacent, not core |

CSOAI focuses on the **measurement instrument**, not the
**compliance platform**. The instrument is what regulators need.

---

## §8 The single-line competitive positioning

> "CSOAI is the only AI governance vendor that measures against itself.
> Every competitor grades models; we grade the graders. The 7 self-
> published refutations and the salted PRACTICE/HELD_OUT split are the
> walls no competitor has climbed."

---

## Provenance

Every score traces to:
1. CSOAI's own public benchmarks (ProvBench, DefBench, PQCBench)
2. The competitor's own public materials (whitepapers, blog posts, arXiv)
3. Third-party analyst coverage where available

If a score here cannot be re-derived, the score is wrong, not the corpus.