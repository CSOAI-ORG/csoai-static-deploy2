# CSOAI Insurance Lane — Top 10 Competitor / Peer Research

**Scope:** AI liability insurance, the underwriting-data-licence product, and risk assessment for AI deployments — viewed through the AG UI **Insurance chat window**.

**Doctrine anchors (bind this whole document):**
- **Neutrality is the asset.** CSOAI measures; it does not certify and does not sell placement.
- **Nobody-ranked-pays:** no pay-to-rank, no pay-to-play, no vendor can buy its way up the board. Rankings, if any, are measurement output, never a purchased position.
- **UNMEASURED shown honestly.** Axes that have not been measured stay UNMEASURED, never silently filled.
- **Crown jewels:** the signed-card format, GSPC axes, and instrument estate are not to be licensed to any party that could monetize them against the estate.

**Honesty rule applied throughout:** only claims verified against a live source in this research session are asserted as fact; everything else is labelled as an inference or left out. No accounts created, no submissions made (research only).

---

## 1. The 10-competitor table

| # | Competitor / peer | What they do | One thing CSOAI could adopt in the Insurance chat window |
|---|---|---|---|
| 1 | **Munich Re (Insure AI / aiSure™)** | Reinsurer that has underwritten AI *performance* risk since 2018; sells tailored risk-transfer for AI errors (lost revenue, business interruption, legal damages) and publishes applied AI-risk research (conformal-prediction failure bounds, IP-infringement mitigation, aggregated multi-model risk). | The chat should **quantify residual failure risk**, not just name it — surface a measured failure-probability bound per model/axis so a deployer sees a number, not a warning. |
| 2 | **AXA XL (CyberRiskConnect Gen-AI endorsement)** | Adds named Gen-AI coverage by endorsement to cyber policy: data poisoning, usage-rights/IP infringement, and EU AI Act regulatory-violation liability. | The chat should **map each deployment risk to a named coverage trigger** (poisoning / IP / regulatory) so users see "silent" gaps made affirmative. |
| 3 | **Lloyd's market (LMA AI blueprint + coverholders)** | The marketplace where AI liability actually trades: Armilla is a Lloyd's coverholder; Chaucer co-developed an AI liability product with Armilla; LMA published a market-wide AI governance blueprint; syndicates (e.g. OAK Global) build AI risk platforms. | The chat should be able to **state the backing/fronting structure** (coverholder vs. carrier vs. reinsurer) so a user understands who actually assumes the risk. |
| 4 | **CFC Underwriting** | Specialty MGA that embeds **affirmative AI cover** across its cyber/tech/media portfolio (explicitly says when AI-driven loss is covered, rather than leaving "silent" ambiguity). | The chat should lead with an **affirmative-vs-silent coverage diagnostic**: does the user's existing policy name AI events, or leave them to interpretation? |
| 5 | **Coalition (Active Insurance)** | Tech-first cyber insurer: "Active" policy that *prevents* loss in real time; explicitly defines AI-driven events in policy wording; Deepfake Response endorsement (forensic + legal takedown + crisis comms); free risk assessment + AI Best-Practices Checklist. | The chat should **close the loop to prevention**, not just indemnity — after assessing risk, hand the deployer an actionable checklist (like Coalition's free assessment → checklist flow). |
| 6 | **At-Bay (InsurSec / Stance)** | Cyber MGA that ships a bundled security platform ("Stance") with every policy — attack-surface monitoring, fraud defense, MDR — built on incident data from 40,000+ insureds. | The chat should **bundle continuous telemetry with the quote** — show that the licensed underwriting data is *ongoing measurement*, not a one-time snapshot. |
| 7 | **RiskGenius** | AI/NLP engine that reads and automates insurance policies (extraction, comparison, clause analysis); used by Guy Carpenter for silent-cyber analysis and by QBE for policy automation. | The chat should offer a **policy-language diff**: paste policy wording and get a neutral, clause-level breakdown of what AI risk is affirmatively covered vs. silent vs. excluded. |
| 8 | **EU AI Act — Art 6 + Annex III (insurance scoring)** | Classifies "risk assessment and pricing in relation to natural persons in the case of life and health insurance" as **high-risk** (Annex III point 5(b)); imposes governance/data/transparency duties on providers and deployers. | The chat should include a **regulatory-classification check**: is this deployment high-risk under Annex III, and which CSOAI measurements map to which duty? |
| 9 | **PRA / BoE (model-risk + AI expectations)** | UK prudential regulator: SS1/23 + PS6/23 model-risk-management principles (banks), April-2024 strategic AI letter to government, Dear-CEO AI expectations, Feb-2026 AI roundtables. | The chat should surface a **model-risk-management view** — governance, validation, explainability, monitoring — so the assessment doubles as PRA-style MRM evidence. |
| 10 | **AI risk-scoring SaaS (Gradient AI, Linqura, WTW Radar 5)** | Vendors selling insurers ML risk-scoring for underwriting (workers'-comp, P&C) and pricing platforms with Gen-AI; Gradient explicitly builds scoring "designed for emerging AI regulations." | The chat should be a **licence storefront for CSOAI underwriting data** — the measured axes become a scorable, licensable signal insurers can plug into their models. |

---

## 2. Per-competitor detail (5 fields each)

### 1. Munich Re — Insure AI / aiSure™
- **What they do:** Reinsurance + primary risk-transfer for AI *performance* risk. Dedicated "Insure AI" team underwriting AI performance since 2018. Flagship `aiSure™` covers multiple models and loss scenarios created by AI errors — lost revenue, business interruption, and legal damages.
- **User flow:** Enterprise/MGA → Munich Re Specialty → research-backed underwriting (conformal-prediction failure bounds, IP-infringement mitigation, aggregated-model correlation) → tailored AI risk-transfer policy.
- **Docs:** Published applied research + executive interviews ("Balancing the promise and peril of AI in insurance," Michael von Gablenz, Head of Insure AI).
- **Software shape:** Not a SaaS — a research-plus-underwriting shop whose IP is quantitative risk methods (conformal prediction, prompt-engineering IP reduction) translated into pricing/accumulation controls.
- **Adopt:** A measured, numeric failure bound in the chat (per model/axis), echoing their conformal-prediction approach — CSOAI's GSPC axes already carry `accuracy`, `separation`, `n`, so the number is computable.

### 2. AXA XL — CyberRiskConnect Gen-AI endorsement
- **What they do:** Adds Gen-AI coverage by **endorsement** to the CyberRiskConnect cyber policy, addressing three named risks: **data poisoning**, **usage-rights (IP/copyright) infringement**, and **regulatory violations (EU AI Act liability)**.
- **User flow:** Client via broker → CyberRiskConnect policy → Gen-AI endorsement selected → coverage extends to the three named AI risks. Available US/Canada, UK/Lloyd's, Europe, Asia.
- **Docs:** Press release and product pages describing the endorsement triggers.
- **Software shape:** Traditional (re)insurer product line (P&C + specialty division of AXA); coverage-by-endorsement, not standalone software.
- **Adopt:** The **named-trigger taxonomy** (poisoning / IP / regulatory) — the chat can use exactly these three buckets plus GSPC axes to show what is and isn't affirmative.

### 3. Lloyd's market — LMA AI blueprint + coverholders
- **What they do:** The venue where AI liability actually trades. Armilla AI is a **Lloyd's coverholder**; Chaucer Group co-developed an AI liability product with Armilla; the **Lloyd's Market Association (LMA)** issued an AI-governance blueprint; Lloyd's Lab has incubated AI-insurance alumni.
- **User flow:** Insured → licensed surplus-lines broker → coverholder (e.g. Armilla) underwrites under Lloyd's capacity → carrier/reinsurer backing (Chaucer, Axis, Convex, Greenlight Re, Swiss Re).
- **Docs:** LMA AI governance blueprint; Lloyd's Lab programme pages; coverholder product pages.
- **Software shape:** Marketplace + delegated-authority (coverholder/MGA) structure; software appears at the MGA layer (risk platforms, assessment portals).
- **Adopt:** **Capacity transparency** — the chat should be able to articulate the risk chain (who measures, who underwrites, who backs) without pretending CSOAI assumes risk.

### 4. CFC Underwriting
- **What they do:** Specialty MGA embedding **affirmative AI cover** across its portfolio — cyber, technology, and media (extended worldwide). Affirmative = the policy states when AI-driven loss is covered, closing the "silent AI" gap.
- **User flow:** Broker → CFC portal → select cyber/tech/media product with affirmative AI enhancement → quote/bind.
- **Docs:** Product pages and trade coverage describing the affirmative AI enhancements.
- **Software shape:** MGA platform with embedded product enhancements; low-friction quote-and-bind via brokers.
- **Adopt:** **"Affirmative vs. silent" as a first-class concept** in the chat — a one-click diagnostic of whether AI events are named or left to interpretation.

### 5. Coalition — Active Insurance
- **What they do:** Tech-first cyber insurer. "Active" insurance prevents loss in real time. On AI, Coalition **explicitly defines how existing coverage responds to AI-driven threats** (expanded definitions in the Active Cyber Policy), and ships a **Deepfake Response endorsement** (forensic analysis, legal takedown, crisis communications). Strategic global cyber partnership with Allianz Commercial (2026).
- **User flow:** Business or broker → **free cyber risk assessment** → Active policy (AI events named in wording) → optional endorsements → continuous active monitoring → downloadable AI Best-Practices Checklist for SMBs.
- **Docs:** AI coverage page with FAQ (silent vs. affirmative, deepfake endorsement, agent-caused failure), AI Best-Practices Checklist PDF, blog.
- **Software shape:** Full-stack insurtech — real-time attack-surface monitoring ("Coalition Control"), API/data-driven underwriting, broker appointment portal. Next.js/headless-CMS site with gated forms and chatbot.
- **Adopt:** **Prevention-close loop + free assessment as funnel entry** — chat starts with a neutral risk assessment and ends with an actionable checklist, mirroring Coalition's assessment→checklist path (but never a paid ranking).

### 6. At-Bay — InsurSec / Stance
- **What they do:** Cyber MGA that is also a security vendor ("InsurSec"). Every policy bundles **Stance**, an AI-powered unified security platform (attack-surface monitoring, fraud defense, phishing training, MDR) built on incident data from **40,000+ insureds**.
- **User flow:** Quote cyber policy → Stance platform included (up to ~$72k stated value) → continuous monitoring + fraud defense + vCISO/cyber-advisor consulting → claims.
- **Docs:** Stance product pages, cyber risk calculators (ransomware/breach cost), case studies, cyber-advisor AI-risk articles.
- **Software shape:** Bundled security SaaS (MXDR, email security) attached to insurance; WordPress/Schema.org marketing layer; risk calculators as lead-gen.
- **Adopt:** **"Measurement as a living stream" framing** — position CSOAI's licensed underwriting data as *continuous* measurement (re-runnable, re-signed), not a static report.

### 7. RiskGenius
- **What they do:** AI/NLP **policy-analysis engine** — extracts, compares, and automates insurance policy language. Deployed with Guy Carpenter for **silent-cyber analysis** and with QBE for **policy automation**.
- **User flow:** Insurer/reinsurer uploads policy corpus → NLP extraction/clause comparison → silent-coverage gap analysis / automation rules.
- **Docs:** "Engine for Policy Automation" profile (The Digital Insurer), vendor reviews.
- **Software shape:** B2B SaaS NLP pipeline for insurers; clause-level extraction and diffing.
- **Adopt:** A **policy-language diff** in the chat — paste wording, get a neutral clause breakdown (covered / silent / excluded) without CSOAI taking a paid position.

### 8. EU AI Act — Art 6 + Annex III (insurance scoring)
- **What they do (regulatory):** Annex III point 5(b) classifies as **high-risk** AI systems "intended to be used for **risk assessment and pricing in relation to natural persons in the case of life and health insurance**" (alongside credit-scoring in 5(b)). Article 6 routes Annex III systems through the high-risk obligations (risk management, data governance, technical documentation, transparency, human oversight, robustness). GPAI (general-purpose AI) obligations sit separately (Articles 52+).
- **User flow:** Deployer/provider → classify (is it Annex III 5(b)?) → if high-risk, meet conformity obligations → market surveillance.
- **Docs:** The Act itself; Commission draft guidelines on high-risk classification (May 2026); law-firm and specialist analyses (e.g. Glacis "Is Insurance Underwriting AI High-Risk Under EU AI Act?").
- **Software shape:** Not software — a legal classification regime that *governs* AI-underwriting software.
- **Adopt:** A **regulatory-classification check** in the chat that flags Annex III 5(b) high-risk status and maps CSOAI's measured axes to the corresponding duties.

### 9. PRA / Bank of England — model-risk & AI expectations
- **What they do (regulatory):** UK prudential supervisor. **SS1/23** and **PS6/23** set model-risk-management principles (banks; principles the PRA expects firms to apply to material models). April 2024: PRA + BoE **strategic AI letter** to government (tech-agnostic, principles-based). Ongoing **Dear-CEO AI expectations** and **AI roundtables** (Feb 2026 summary published).
- **User flow:** Regulated firm → align AI/model governance with SS1/23 principles (identification, governance, development/validation, deployment, monitoring) → respond to supervisory expectations.
- **Docs:** PRA SS1/23, PS6/23, April-2024 AI letter, Feb-2026 AI roundtable summary.
- **Software shape:** Not software — supervisory expectations that shape how insurers build/validate AI.
- **Adopt:** A **model-risk-management lens** in the chat — the assessment output structured to double as MRM evidence (governance, validation, monitoring), which is exactly what an insurer needs to *buy* CSOAI data.

### 10. AI risk-scoring SaaS for insurers (Gradient AI, Linqura, WTW Radar 5)
- **What they do:** Vendors selling insurers ML/AI **risk-scoring and pricing** for underwriting — Gradient AI (workers'-comp risk scoring, "designed for emerging AI regulations"), Linqura (P&C underwriting risk-scoring, now partnered with Sapiens), WTW Radar 5 (pricing/underwriting platform with Gen-AI).
- **User flow:** Insurer licences the SaaS → feeds portfolio data → ML risk scores / pricing → embeds into underwriting workflow.
- **Docs:** Vendor product pages, press releases (Businesswire, Barchart, MarketScreener).
- **Software shape:** Enterprise SaaS/ML platforms with risk-score APIs and underwriting integrations.
- **Adopt:** Position the chat as a **data-licence storefront** — CSOAI's signed GSPC measurements are the *input signal* these scoring engines need, licensed under clear terms rather than sold as a ranking.

---

## 3. What CSOAI should adopt — 5 concrete improvements for the Insurance chat window

Aligned with the **underwriting-data-licence product** and the **nobody-ranked-pays** doctrine.

### A. "Silent vs. affirmative" diagnostic (from Coalition + CFC)
The chat's opening move should not be a sales pitch — it should be a **coverage-gap diagnostic**. Ask the deployer to paste or summarise their existing policy, then return a neutral, clause-level breakdown: which AI risks are *named/affirmative*, which are *silent*, which are *excluded*. This borrows Coalition's affirmative-vs-silent framing and RiskGenius's policy-diff capability.
- **Doctrine-safe:** the diagnostic is neutral and free; CSOAI never ranks vendors and never charges for a placement.

### B. Named-trigger risk map → measured signal (from AXA XL + Munich Re)
After the diagnostic, map the deployment onto a **named-trigger taxonomy** (data poisoning, IP/usage-rights, regulatory liability, performance failure, bias/fairness) — AXA XL's three endorsement buckets extended with GSPC axes. For each trigger, surface the **measured** CSOAI signal (`accuracy`, `separation`, `n`, `UNMEASURED` where absent), echoing Munich Re's quantified failure-bound approach.
- **Product tie:** this is the exact moment the **underwriting-data licence** becomes the product — "licence the signed measurement card for axes X, Y, Z."
- **Doctrine-safe:** numbers come only from CSOAI's instrument; unmeasured axes are shown as UNMEASURED, never inferred.

### C. Regulatory-classification check (from EU AI Act Annex III 5(b) + PRA SS1/23)
Add a **compliance classifier**: (1) is this deployment high-risk under Annex III point 5(b) ("risk assessment and pricing … life and health insurance") or adjacent 5(b) credit-scoring? (2) does it fall under PRA-style model-risk expectations (SS1/23/PS6/23 principles)? For each "yes," show which CSOAI measurement axes evidence which duty (data governance, robustness, human oversight, monitoring).
- **Product tie:** turns CSOAI measurement into **regulatory-grade evidence** an insurer can cite — the strongest reason to licence.

### D. Free assessment → actionable checklist, no paywall (from Coalition + At-Bay)
Wrap A–C in a **free, structured risk assessment** that ends with a downloadable **deployment checklist** (governance, monitoring, red-team, fallback), Coalition's AI Best-Practices Checklist pattern. Then offer continuous re-measurement as At-Bay positions its platform — measurement as a *living stream*, re-runnable and re-signed.
- **Doctrine-safe:** the assessment is free and neutral; the licence is for *data/evidence*, not for a favourable position on any board.

### E. Capacity & honesty disclosure (from Lloyd's coverholder structure + Armilla exclusions)
Every chat response that touches insurance must state, plainly: **(1) CSOAI measures and licenses data — it does not underwrite, front, or assume risk** (mirror Armilla/Lloyd's coverholder disclosure and Coalition's "not a contract/guarantee" disclaimer); **(2) what is UNMEASURED**; **(3) that no coverage binds without a licensed carrier**; and **(4) the nobody-ranked-pays commitment** — no vendor can pay to be ranked or to suppress another's measurement.
- **Doctrine-safe:** this is the firewall made visible in-product; it is what makes the data licence *trustworthy* rather than another pay-to-play leaderboard.

---

## 4. Verification & sources

All factual claims above were checked against live sources retrieved during this session (no accounts, no submissions). Key sources:

- **Munich Re** — "Balancing the promise and peril of AI in insurance" (Michael von Gablenz, Head of Insure AI), aiSure™, conformal-prediction/IP/aggregation research: https://www.munichre.com/specialty/en/insights/artificial-intelligence/balancing-the-promise-and-peril-of-ai-in-insurance.item-23300f839cadad497538c08cdc0a6778.html
- **AXA XL** — Gen-AI endorsement press release (data poisoning, usage rights, EU AI Act): https://axaxl.com/press-releases/axa-xl-unveils-new-cyber-insurance-extending-coverage-to-help-businesses-manage-emerging-gen-ai-risks
- **Lloyd's / LMA / Armilla** — LMA AI governance blueprint (Insurance Business Mag); Armilla AI Lloyd's coverholder: https://www.armilla.ai/ai-insurance ; Chaucer–Armilla product: https://www.commercialriskonline.com/chaucer-and-armilla-launch-ai-liability-product/
- **CFC** — affirmative AI cover across cyber/tech/media: https://www.businessinsurance.com/cfc-unveils-updates-to-embed-affirmative-ai-cover/
- **Coalition** — Active Insurance AI coverage, Deepfake Response endorsement, AI Best-Practices Checklist, Allianz partnership: https://www.coalitioninc.com/en-ca/ai-coverage
- **At-Bay** — Stance platform (40,000+ insureds), Fraud Defense, MXDR: https://www.at-bay.com/stance/
- **RiskGenius** — policy-automation engine; Guy Carpenter silent-cyber and QBE partnerships: https://www.the-digital-insurer.com/dia/riskgenius-engine-for-policy-automation/
- **EU AI Act** — Annex III point 5(b) high-risk insurance/credit classification: https://www.glacis.io/guide-insurance-ai-high-risk ; https://www.mccannfitzgerald.com/knowledge/technology-and-innovation/essential-services-spotlight-eu-ai-act-draft-guidelines-on-high-risk-ai-classification
- **PRA / BoE** — SS1/23 & PS6/23 model risk; April-2024 AI letter; Feb-2026 AI roundtables: https://www.bankofengland.co.uk/prudential-regulation/publication/2023/may/model-risk-management-principles-for-banks ; https://www.bankofengland.co.uk/minutes/2026/february/summary-of-ai-roundtables-feb-2026
- **AI risk-scoring SaaS** — Gradient AI (workers'-comp, "designed for emerging AI regulations"): https://www.businesswire.com/news/home/20250416276843/en/ ; Linqura/Sapiens P&C risk-scoring: https://www.barchart.com/story/news/35313366/ ; WTW Radar 5 Gen-AI: https://www.marketscreener.com/news/wtw-launch-of-radar-5-with-gen-ai-capability-marks-a-major-milestone-in-insurance-pricing-and-underw-ce7d5ad9d18ff322

**Caveat:** product availability, pricing, and policy wording change frequently; treat the table as a competitive snapshot, not a binding market survey. Coverage descriptions are competitors' marketing/FAQ text and do not amend their policies.
