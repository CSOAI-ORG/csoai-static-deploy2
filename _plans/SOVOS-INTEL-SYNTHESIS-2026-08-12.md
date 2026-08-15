# SOVOS DEEP INTEL SYNTHESIS — 2026-08-12
*Three parallel research sweeps (regulation / market / technical) + external audit. Every claim sourced in the agent reports; UNVERIFIED items flagged. Companion files: sovos-external-audit-2026-08-12.md · SOVOS-MONOREPO-PLAN-2026-08-12.md*

## 0. CANON CORRECTIONS (register-level, immediate)

| # | Old canon | Corrected | Source |
|---|---|---|---|
| C1 | "Non-signatories xAI/Amazon" (AY/BE) | **Amazon SIGNED the GPAI CoP — all three chapters. Meta refused (18 Jul 2025). xAI signed Safety & Security only. Chinese providers (DeepSeek, Alibaba, Baidu, Zhipu) unsigned.** Any material using "xAI/Amazon refused" must be fixed | aiwiki.ai/wiki/gpai_code_of_practice |
| C2 | Art 50 "in force" | **Art 50 enforcement CONFIRMED live since 2 Aug 2026** (Commission press IP/26/1714 per trackers); fines up to €15M/3%. Transparency CoP final 10 Jun 2026; **~190 first-list signatories** (31 Jul); EU icon set ("AI+GENERATED"/"AI+MODIFIED"); text <200 tokens exempt from marking; detection-interop deadline 2 Feb 2027 | EC/tracker sources in agent report |
| C3 | Ollama platform changes | None found — UNVERIFIED either way (quiet) | market sweep |

## 1. THE FIVE CATAPULTS (ranked by window urgency × fit)

### 🥇 C1 — The Art 50 evidence window (~90 days, hard)
Enforcement live 2 Aug · marking retrofit deadline **2 Dec 2026** · new Art 5 NCII/CSAM prohibition same date with legal test = *"reasonable and adequate technical safeguards"* (an empirical measurement question) · non-signatories must prove "adequate alternative means" individually to 27 national authorities · Anthropic marked everything globally but **shipped no verification tooling**. The article-50 page (G1) is already live — now productize the verification pack behind it. **Window closes 2 Dec 2026.**

### 🥈 C2 — Companion/emotion-AI: the statutory demand curve nobody can serve
- **Colorado HB 26-1263 Chatbot Safety Act**: annual AG report with **"metrics necessary to determine efficacy and reliability of safeguards"** — first US law explicitly demanding efficacy *metrics* (effective 1 Jan 2027)
- **CA SB 243**: annual reporting + **regular third-party audits** + private right of action ($1,000/violation)
- **NY GBL Art 47** live (3-hour recurring disclosure); WA HB 2225; PA HB 2006 moving; **child-safety carved out of federal preemption push** = durable demand
- **China** (effective 15 Jul 2026): anti-dependency safeguards + provincial CAC filings; major platforms already pulled companion features
- **Armilla EXCLUDES mental-health/companion AI from cover** — the risk is *uninsurable because nobody measures it*
- Character.AI settled five teen-harm suits (Jan 2026); PA suing over fake-psychiatrist claims (May 2026)
**The Emotional Safety Card is no longer a concept — it's the missing artifact for statutes already signed.**

### 🥉 C3 — Sell to underwriters (both sides)
Mosaic×Munich Re **aiSure** (parametric, up to €15M, underwritten on documented performance specs + benchmarking methodology) · **AIUC-1** (5,000+ adversarial sims pre-binding, Drata distribution) · **NAIC 12-state AI Systems Evaluation Tool pilot** (ends Sep 2026 — examiners literally conducting structured AI evidence reviews) · EIOPA: documented monitoring = faster cover · Lloyd's (Chaucer/Armilla $25M, Testudo) conditioning capacity on third-party assessment. **CVaR cards speak insurer natively (BV.4 confirmed by market structure). AIUC's auditor-profits-from-underwriting conflict is the attack surface for an independent card issuer.**

### C4 — Technical first-movers (≤2 weeks each)
1. **EVT/GPD on per-item eval rows: VERIFIED GREENFIELD** — no in-window paper fits GPD/POT to eval-score tails. scipy genpareto + mean-excess threshold = 2-week build. First-ish mover. *(Catapult from BV/BT doctrine.)*
2. **RQGM epoch-frozen judge** (arXiv 2606.26294) — the rigorous version of our fixed-judge doctrine, quantified (1.91× reviewer over-acceptance fixed). Adopt: epoch boundaries + ground-truth-anchored judge upgrades + held-out selection + old-score retirement.
3. **Sigsum witness cosigning** — alive, maintained (sigsum-go v0.14.1), Ed25519+threshold witnesses = production-grade quorum witnessing for signed cards. Crib **Sello's COSE_Sign1 receipt schema** (arXiv 2606.04193) for card format. *(Unblocks the Sigsum diamond from BE — run on net-capable host.)*
4. **Benchmark-integrity gate**: 15% of Terminal-Bench 2.0 hackable (Terminal Wrench); Meerkat found answer-key injection via AGENTS.md. **Hash-pin environment files + injection scan before any result signs.**
5. **OMD-CVaR reporting format** (arXiv 2605.09946): CVaR(0.125) + severity strata — copy the format for our tail blocks.

### C5 — Platform-positioning plays
- **NIST AI 800-2/800-3** (evaluation statistics) — align CI reporting = US federal procurement-ready
- **FedRAMP OSCAL mandate 30 Sep 2026** (<7 weeks) — OSCAL-format evidence packs = product extension
- **HF DOIs standard** (10.57967/hf/*) — DOI'd banks at zero marginal cost (B4 confirmed feasible)
- **MTEB transparency norms** (contamination flags, bracket reporting) — our honesty conventions are now platform-fashionable
- **UK Centre for AI Measurement at NPL** (Jan 2026) + DSIT consortium deliverables due ~Sep 2026 — **standard-setting seat to pursue now**; DSIT fund winners UNVERIFIED (check Innovate UK directly)

## 2. THREATS (ranked)

| # | Threat | Mitigation |
|---|---|---|
| T1 | **Annex III delay → Dec 2027** freezes high-risk eval budgets | Re-anchor: Art 50 (live), SB 243/CO audits, insurance, NCII ban (2 Dec 2026) |
| T2 | **AIUC-1 audit+insurance bundle** capturing the certification layer (Lloyd's/Munich Re/Drata rails) | Ship the independent alternative; attack the conflict-of-interest; move within the Art 50 window |
| T3 | **Suite absorption of "measurement" language**: Cisco/Galileo, ServiceNow, Gartner MQ (Jun 2026) platforms, Enzai "compliance scoring" | Publish methodology openly; name the distinction sharply (deterministic banks + intervals + UNMEASURED vs workflow tracking); the EMPATH paper (judge inflation 2→10 instability) is the scientific ammunition |
| T4 | **Modulos** owns certification credibility (first ISO 42001 product conformity, CertX-audited) | Certifies platforms, not models — different layer; stay measurement-pure |
| T5 | **EMPATH benchmark** = academic prior art in emotional-safety measurement | It validates us: documents LLM-judge inflation/instability → deterministic banks are the defensible instrument. Cite it, don't fight it |

## 3. TECHNICAL ADOPT LIST (condensed from the sweep)
- **ADOPT**: MedPRESS multi-turn pressure protocol · SycoBench-600 correction-selectivity · Anthropic functional-emotions (mechanistic sycophancy hook) · OMD-CVaR format · Terminal-Bench 2.0 protocol (5 trials) · benchmark-integrity gate · Sigsum + Sello receipts · RQGM epoch-frozen judge · mergekit baseline · GGUF-v3 via HF (kills broken-tokenizer class) · C2PA 2.3 + official Trust List pinning
- **ADAPT**: MemSyco-Bench (memory-induced sycophancy — new axis candidate) · DESG state-transition scoring · DarkBench+ taxonomy · lucid κ-warning (deterministic behavior-anchored rubrics; consider Gwet AC1) · PACT per-game rating vs Glicko-2 (held-out log-loss validation) · VoxelBench quorum-display precedent · microprediction/winning (validate rating choice, don't assume) · Butlin/Long/Bengio indicator framing for claim-policing
- **SECURITY: CVE-2026-5760 (CVSS 9.8)** — SGLang RCE via malicious GGUF chat_template Jinja2 SSTI. **Treat every GGUF as untrusted code; sandbox templates (ImmutableSandboxedEnvironment) in the conversion/eval pipeline NOW.** Plus: rotate + minimally scope HF tokens (July 2026 HF autonomous breach).
- **WATCH**: CAWG identity 1.3 · STELA watermark · DGM-H (breaks fixed-meta assumption — threat model) · LMArena→Arena ($1.7B) critique literature
- **IGNORE**: STOP (stale) · philosopedia sentience scores (untraceable)

## 4. AUDIT SUMMARY (full detail: sovos-external-audit-2026-08-12.md)
✅ domains codename-clean (except proofof.ai — owner gate) · ✅ zero exposed sensitive files · ✅ zero killed claims on sites · 🚨 **safetyof.ai DOWN (402 billing)** · ⚠️ **GitHub 568 public repos: contradictory fleet counts (300+/81/38), attestation overclaim, sovereign-phrasing + pricing on READMEs; secrets scan OWED** · ⚠️ HF `sov-*` public naming drift · ❌ Kaggle presence still unverified (all handles 404)

## 5. THE ONE-PARAGRAPH TRUTH
The market moved toward us this quarter: regulation made measurement statutory (CO efficacy metrics, CA audits, China filings, Art 50 enforcement), insurers made it billable (aiSure/AIUC/NAIC), academia made our discipline fashionable (EMPATH judge-inflation, MTEB transparency norms), and the technical greenfield we claimed (EVT-on-eval-rows, quorum-gated ratings, fixed-judge loops) is confirmed empty or converging on our design. The window is the Art 50 grace period: **92 days from today.** The exposure cleanup (GitHub READMEs, safetyof.ai, secrets scan) must complete first — you can't sell honest measurement from an estate that overclaims on its own distribution channel.
