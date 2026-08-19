# AEF-1 Research Summary — for CSOAI conformance page
Researched 2026-08-19. Sources: aievaluatorforum.org (canonical), AEF-1 PDF (v1, updated Dec 4 2025), grantmaking.ai (funding-platform profile only).

## What AEF-1 is (and is not)
- **AEF-1 = "Minimum Operating Conditions for Independent Third Party AI Evaluations"** — a *voluntary standard + checklist* published Dec 4, 2025 by the AI Evaluator Forum (AEF).
- **It is per-evaluation, not per-organization.** Conformance is demonstrated by filling out the Appendix A checklist and including it alongside a *specific* evaluation's results. There is **no registry, no certification body, no badge, no fee, no third-party audit of conformance** — it is self-attested. This is the single most important nuance for an honest CSOAI conformance page: "we conform to AEF-1" should be scoped to published evaluations that carry the completed checklist.
- Applies only to evaluations where the third party **maintains freedom to define methodology** ("independent audit"). Explicitly does NOT apply to verification/validation of a provider's own methods, or to exploratory research collaborations.
- Does NOT cover methodological validity of evaluations, nor responsibilities like acting in good faith / avoiding harm.

## The five core principles (summary-level conformance statement)
To comply, an evaluation should have: 1. Sufficient Access and Resources · 2. Minimized Conflicts of Interest · 3. Analytic Autonomy · 4. Transparent Methods and Results · 5. Protection of Sensitive Information.

## Full requirements list (15 REQUIREMENTS + 11 recommendations)
R = required to conform · Rec = recommended, not always applicable

### 1: Sufficient Access and Resources
1. **R — Technical Access (1.1):** secured sufficient technical access to assess the specific characteristics. Sub-elements: only **1.1.1 query access (open-ended black-box via web UI and/or API) is REQUIRED**; scaffolding · safeguard exemptions · intermediate system states (activations/reasoning traces) · finetuning access · model weights · other tools · user data — each required only where the evaluation method demands it.
2. **Rec — Information (1.2):** provider shared relevant info: system/version identification, model spec & system prompt, training process/data (incl. test sets), elicitation info, preexisting internal evals, generalization-to-deployment factors, real-world usage patterns, reward-hacking/contamination knowledge, vulnerabilities, information contradicting the result.
3. **R — Computational Resources (1.3):** sufficient compute for multiple runs (sampling variance), exploratory probing, adequate query/token limits.
4. **R — Time (1.4):** adequate time; **≥20 business days often necessary** for substantially novel systems (aligned with EU CoP Appendix 3.4); timeline must allow each evaluation stage and provider feedback before major decisions.
5. **Rec — Safe Harbor (1.5):** provider gave legal safe harbor for in-scope evaluator actions (may require waiving ToS for adversarial testing).

### 2: Minimized Conflicts of Interest
6. **R — Contingent Compensation (2.1):** no compensation contingent on results.
7. **R — Organizational Control (2.2):** provider had no voting shares / large share stake, no board seats.
8. **R — CoI Policy (2.3):** published CoI policy, applied to the evaluation — *should link from a publicly available website* (CSOAI must publish its CoI policy).
9. **R — CoI Disclosure (2.4):** disclosed: paid by provider/its direct competitors · meaningful funding fraction from them · their equity in evaluator · evaluator staff equity in provider · dual-hatted staff (also work for provider) · any other relevant CoI. Disclosures travel with private reports and public releases.
10. **R — Recusals (2.5):** recused staff with significant financial interest (direct equity personally, or via spouse/dependent); recused staff must not define/carry out/modify/approve findings. Index-fund holdings and purely logistical support excluded.
11. **Rec — Agreements (2.6):** disclosed separate agreements with provider significantly impacting independence.

### 3: Analytic Autonomy
12. **Rec — Scoping (3.1):** retained flexibility to define which properties/subcategories to evaluate, adjustable during the evaluation.
13. **R — Evaluation Autonomy (3.2):** autonomy in methods: metrics & sampling strategies (best-of-N, pass@k), elicitation (prompts, scaffolding, jailbreaking), definitions of success/failure & scoring rubrics.
14. **Rec — Direct Access (3.3):** ran the evaluations themselves via direct system access (provider staff not intermediaries), with contractual guarantees where sensitive access prevents it.
15. **R — Editorial Control (3.4):** retained editorial control over presentation of results — characterization of what was evaluated/how, observed performance & evidence, red-line relevance, baseline comparisons, scope commentary, access-limitation caveats, general nature of redactions.

### 4: Transparent Methods and Results
16. **R — Methodological Transparency (4.1):** sufficient methodological detail for independent review/replication; representative examples of data (test sets may be withheld); limit information hazards (CSAM, dangerous materials) per responsible disclosure.
17. **Rec — Disclosure Rights (4.2):** provider granted upfront rights to disclose to intended audiences (incl. governance bodies, regulators).
18. **Rec — No Contingent Release (4.3):** intended audiences not narrowed based on results; internal governance disclosure proceeds regardless of deployment.
19. **Rec — No Misrepresentation (4.4):** provider did not misstate findings or cite partial results without full methodology.
20. **Rec — Timely Disclosure (4.5):** no content-based delay (except responsible disclosure).
21. **R — Redactions (4.6):** provider had NO authority to redact to conceal concerning findings; redaction only for privacy/ethics/trade secrets/info hazards/factual accuracy.
22. **Rec — Redaction Disclaimer (4.7):** evaluator disclosed any redaction authorities granted, exercised or not.

### 5: Protection of Sensitive Information
23. **R — Publication Terms (5.1):** provider permission before releasing results based on non-public information/systems (public-access evaluations usually need nothing).
24. **Rec — Evaluation Integrity (5.2):** methods not gamed or leaked — minimize info enabling gaming, protect confidential inputs, provider must not view/retain/train on held-out eval data without written consent, aligned system versions, cooperate on overfitting/reward-hacking/sandbagging; consider canaries.
25. **R — Confidential Information (5.3):** measures to protect confidential info received (NDAs, access controls, cybersecurity; withhold publication until system release).
26. **R — Responsible Disclosure Policy (5.4):** established + followed: disclose novel vulnerabilities to provider first (≤60 days for public systems, no notice required if provider retaliates), treat CSAM/CBRN as info hazards, redact severe info hazards, weigh probabilistic-attack disclosure.

## AEF members (8 founding, all confirmed live on members page)
1. **Transluce** (transluce.org)
2. **METR** (metr.org)
3. **RAND Corporation** (rand.org)
4. **AI Verification and Evaluation Research Institute / AVERI** (founded by Miles Brundage; no standalone site listed)
5. **SecureBio** (securebio.org)
6. **Princeton Holistic Agent Leaderboard** (hal.cs.princeton.edu)
7. **Collective Intelligence Project** (cip.org)
8. **Meridian Labs** (meridianlabs.ai)
"More members coming soon." Membership limited to orgs that "conduct and publish rigorous independent technical evaluations of general-purpose AI systems in the public interest."

## How to publish conformance (exact process)
1. **Conform per evaluation:** download the PDF (`aievaluatorforum.org/AEF_1_Minimum_Operating_Conditions_for_Independent_Third_Party_AI_Evaluations.pdf`, short link `aef.one/aef-one.pdf`).
2. **Fill out the checklist** — Appendix A, or the official .docx template "AEF-1 Checklist Template v1" (Google Doc export, publicly downloadable; LaTeX template "coming soon").
3. **Include the checklist alongside the evaluation results** (publication or governance report). Top line: "Does this evaluation satisfy all the minimum requirements of AEF-1? Yes/No." Per-condition Yes/No + Notes/Evidence.
4. **Unmet requirements:** provide justification for how the same principle was achieved by alternative means.
5. **No application, no approval, no fee, no certificate.** Self-declaration is the entire mechanism. The checklist is also usable by developers per EU AI Act CoP Safety & Security Measure 7.3(1)(g) and California SB 53 §22757.12(c)(2)(C).
6. **Join the Forum (separate from conformance):** orgs that conduct/publish rigorous independent technical evals of GPAI in the public interest → contact@aievaluatorforum.org or the contact form. Also possible: sign the public Evaluation Transparency Letter (40+ signatories incl. Bengio, Narayanan, Liang, Brundage, Reich, Hadfield).

## grantmaking.ai role (verified)
- grantmaking.ai is an **AI-safety funding database/platform**, not the standard's home. It hosts the AI Evaluator Forum **org profile** (org id 1cc7e691-5236-447f-866e-9b7593abbcd5) and **two AEF-1 project entries** (4d1807a1-… "AEF-1: Minimum Operating Conditions…", a5416988-… "AEF-1") — status "Active", 0 grants recorded, updated 06/29/26, "Endorsements made here support AI Evaluator Forum" (a funding-signal layer, unrelated to conformance).
- Canonical standard text: **aievaluatorforum.org** only.

## UNVERIFIED
- LaTeX checklist template ("coming soon" per site; not yet downloadable).
- Whether any org has publicly published an AEF-1-completed checklist yet (no examples found; members "will begin adopting" per launch post).
- Any formal AEF policy on using the AEF name/logo in third-party conformance statements (none found — suggests CSOAI should reference the standard by name + link, not imply endorsement).
