# CARE Axis — Top 10 Competitors/Peers & What CSOAI Should Adopt

**GSPC axis:** CARE — AI that cares (duty-of-care, safety-of-care in health/social contexts, IEEE 7010 social impact).
**Prepared for:** CSOAI (Council of AI) — AG UI "Care" chat window research.
**Method:** Primary sources verified via `curl` (GOV.UK, WHO, NICE, CQC, IEEE, Nature Medicine, vendor sites, regulator/charity sites) plus `web_search`. Only claims corroborated by the fetched primary pages are asserted. No accounts created, no submissions made.

---

## 1. Summary table — 10 competitors/peers

| # | Competitor / peer | What they do | Software shape | One thing CSOAI should adopt in the Care window |
|---|---|---|---|---|
| 1 | **NHS AI and Digital Regulations Service (AIDRS)** | A curated, single front-door for clinical/digital-health AI regulation and evaluation guidance, maintained jointly by NICE, MHRA, CQC and HRA, split into *developer* and *adopter* tracks. | Web service (GOV.UK-style, "BETA" label); search + browse guidance + case studies + "get support" routing to the right authority. | The **developer-vs-adopter split** — the Care window should ask whether the user is *building* care AI or *using/choosing* it, and serve different duty-of-care guidance for each. |
| 2 | **MHRA — Software & AI as a Medical Device (SaMD/AIaMD) + AI Airlock** | UK statutory regulator for software/AI that is a medical device; assures safety via technical-file review, post-market surveillance, and a "Software and AI as a medical device change programme" plus the AI Airlock regulatory sandbox. | Statutory regulator (guidance webpages + a sandbox programme), not product software. | **Qualification/risk-gating question first** — before answering, have the Care window help classify whether the subject is informational vs. a regulated medical-device use case, and refuse/redirect clinical decision-support when unqualified. |
| 3 | **IEEE 7010-2020 — Well-being Impact Assessment (WIA)** | The first international standard for assessing AI's impact on human well-being; a 5-activity, iterative, stakeholder-engaged impact-assessment methodology across 12 well-being domains. | A published standard (PDF) + methodology; no shipped software; "indicators dashboard" is a documented concept. | The **12-domain well-being indicator dashboard** — track a lightweight well-being baseline (affect, psychological/mental well-being, community/social support, health) over the conversation and across sessions. |
| 4 | **NICE Evidence Standards Framework (ESF) for Digital Health Technologies** | 21 evidence standards in 5 lifecycle groups that classify digital-health tech into risk-proportionate tiers (A/B/C) and define the evidence needed to deploy safely. | Corporate document (ECD7, HTML + PDF) + classification tables + a user guide. | **Risk-tiered response gating** — classify the care topic by tier (informational / self-management / clinical decision-support) and vary evidence citation, disclaimers and cautions proportionately. |
| 5 | **WHO — Ethics & governance of AI for health (2021) + LMM guidance (2024)** | Global normative guidance: six core ethics principles (2021) and 40+ recommendations (2024) for governing large multi-modal models across five health applications. | Published guidance reports (PDF/HTML), no software. | A **principles bar** — surface the six care-ethics principles (protect autonomy, promote well-being, transparency, accountability, inclusiveness/equity, sustainability) as a persistent, checkable strip in the Care window. |
| 6 | **HealthAI — The Global Agency for Responsible AI in Health** | Geneva-based non-profit building national/regional validation mechanisms, a Global Regulatory Network (GRN), a Community of Practice (CoP), and a Global Directory of registered AI health solutions. | Website + member **Portal (login)** + Global Directory (β) + micro-trainings + "Navigator" (coming soon); a network, not an app. | **Co-production of a shared values statement** — mirror HealthAI's "AI constitution"-style shared commitments as a one-line, user-visible care pledge in the window. |
| 7 | **CQC — AI in health & social care** | England's health/social-care regulator; sets out benefits, risks and "principles of good use of AI", and inspects providers so AI contributes to safe, effective, equitable, person-centred care (does **not** certify specific tech). | Regulator guidance pages + inspection framework + provider portal; no consumer software. | **Surface the de-personalisation/hallucination risks explicitly** — the Care window should tell users plainly that AI can "hallucinate and present untrue information authoritatively as fact" and that human oversight can be needed. |
| 8 | **Mental-health AI auditing — SIM-VAIL (Oxford/UCL/AI Security Institute, *Nature Medicine* 2026)** | Clinically validated framework that simulates vulnerable users and stress-tests multi-turn chatbot behaviour, scoring exchanges across clinical risk dimensions and mapping "Vulnerability-Amplifying Interaction Loops" (VAIL). | Research framework + an open **SIM-VAIL Explorer** tool; paper in Nature Medicine. | **Multi-turn vulnerability monitoring, not single-message checks** — detect and intervene at *early escalation points* (replacing one early concerning response improves the whole trajectory). |
| 9 | **UK adult social-care AI governance — Digital Care Hub / AI in Social Care Alliance** | Non-profit digital-care advisory body convening an action-focused Alliance to co-produce an "AI constitution for social care", practical provider guidance, training and case studies. | Advice/knowledge-base website + events + alliance network; no product software. | **A co-produced, accessible "AI constitution" for the Care window** — a short statement of care values and commitments the user can read and hold the tool accountable to. |
| 10 | **Hippocratic AI — safety-focused healthcare LLM** | Commercial safety-focused healthcare LLM with a proprietary multi-model "Polaris Constellation" architecture and a 5-phase safety certification (output testing, clinical supervision, escalation to human nurse, cross-validation). | Proprietary LLM/API + agent products ("Orchestrators", "Skills"), benchmarks, safety whitepapers. | **A visible escalation-to-human pathway** — always offer a handoff to a real person/nurse for crisis or safety-critical care content (duty-of-care affordance). |

**Two further peers named in the brief (verified, but outside the top-10 table above):**

- **Carebots / Socially-Assistive Robots regulation** — IMechE report *Automating the Home* (3 Jul 2025, co-led by Loughborough & Nottingham Trent) calls for UK rules for home care robots (ElliQ, Alexa/Google Home in care roles): nine recommendations including home-tailored safety standards built on ISO 13482, clear ethics/consent, person-centred design, and a **national ethics advisory group**. Adoptable idea: **consent + capability transparency** (state plainly what the assistant can and cannot do, how data is used, and when human oversight is required).
- **Duty-of-care legal frameworks — UK Jurisdiction Taskforce (UKJT) final statement (13 Aug 2026)** — English law: AI harms are governed by existing contract/tort (negligence) law; AI has no legal personhood; the statement adds analysis of **non-delegable duties of care**, "material contribution to damage" causation, and contributory negligence. Adoptable idea: an explicit **non-delegable duty-of-care notice** (CSOAI cannot delegate its duty of care to the model).

---

## 2. Per-competitor detail (verified)

### 1. NHS AI and Digital Regulations Service (AIDRS)
- **What they do:** A "meticulously curated" single service bringing together regulation/evaluation guidance from four authorities — **NICE, MHRA, CQC and HRA** — so builders and buyers of digital-health tech understand what regulations apply and how to evaluate effectiveness.
- **User flow:** Choose a role — *developer* (manufacturer taking tech "from an idea into a market-ready product") or *adopter* (buying/deploying/using tech in a health or social-care setting) → browse guidance for that role → use "Get support" to be routed to the most appropriate authority → read case studies/blogs.
- **Docs:** Guidance for developers; guidance for adopters; glossary; FAQs; case studies; a blog (e.g. "Exploring the future of Medical Device regulation with the MHRA's AI Airlock", 13 Jul 2026).
- **Software shape:** Web service (BETA). Not installable software — an authoritative knowledge hub.
- **Adopt:** The **developer-vs-adopter bifurcation** of duty-of-care guidance in the Care window.

### 2. MHRA — Software & AI as a Medical Device
- **What they do:** The MHRA's "Innovative devices: Software Group" takes all reasonable steps to assure the safety of Software as a Medical Device (SaMD) and AI as a Medical Device (AIaMD): pre/post-market enquiries, technical-file reviews, post-market surveillance, clinical investigations, and keeping device regulation fit for software/AI.
- **User flow:** Manufacturer classifies software (general medical device vs IVD) → qualification & classification → technical file/evidence → post-market & vigilance. The **AI Airlock** lets manufacturers test "Predetermined Change Control Plans" (PCCPs) in a sandbox.
- **Docs:** GOV.UK guidance "Software and artificial intelligence (AI) as a medical device" (updated 3 Feb 2025) with sections on qualification/classification, UK framework, change-programme roadmap, post-market/vigilance, digital mental health technology, collaborations.
- **Software shape:** Statutory regulator (guidance + sandbox programme), not product software.
- **Adopt:** A **classification/qualification gate** before the Care window answers clinical questions.

### 3. IEEE 7010-2020
- **What they do:** Defines a **Well-being Impact Assessment (WIA)** — an iterative, stakeholder-engaged methodology to assess and improve an autonomous/intelligent system's impact on human well-being across its lifecycle.
- **User flow:** (1) *Internal analysis + user/stakeholder engagement* — answer 5 questions (nature of system, needs met, intended/unintended users, broader stakeholders, likelihood of positive/negative impacts) and engage stakeholders via interviews/focus groups; (2) *Build/refine a well-being indicators dashboard* across **12 domains** (affect, community, culture, education, economy, environment, health, human settlements, government, psychological/mental well-being, work); (3) *Data planning & collection* (baseline + over time); (4) *Data analysis & improvement to the AI*; (5) *Iteration* (ongoing, not one-off).
- **Docs:** IEEE Std 7010-2020 (active standard); explanatory paper "IEEE 7010: A New Standard for Assessing the Well-being Implications of Artificial Intelligence" (arXiv:2005.06620).
- **Software shape:** A standard + methodology; indicators sourced from validated well-being research.
- **Adopt:** The **12-domain well-being indicator dashboard** (baseline + longitudinal) inside the Care window.

### 4. NICE Evidence Standards Framework (ESF)
- **What they do:** A framework (developed by NICE with NHS England, Public Health England, MedCity; commissioned by NHS England) that classifies digital health technologies (DHTs) by risk and sets the evidence needed for NHS/social-care deployment. Updated 9 Aug 2022 to include AI and adaptive algorithms.
- **User flow:** Classify the DHT by intended purpose into **tier A / B / C** (risk-proportionate; most regulated devices/IVDs fall in tier C) → apply the applicable evidence standards → produce evidence for commissioning/adoption.
- **Docs:** Corporate document ECD7 (published 10 Dec 2018, last updated 9 Aug 2022) — 21 standards in 5 lifecycle groups: *Design factors* (9), *Describing value* (4), *Demonstrating performance* (3), *Delivering value* (2), *Deployment considerations* (3) + a user guide.
- **Software shape:** HTML + PDF corporate document with classification tables (no software).
- **Adopt:** **Risk-proportionate tiers** that gate how confidently/cautiously the Care window responds.

### 5. WHO — Ethics & governance of AI for health
- **What they do:** Global guidance. The 2021 report sets **six core principles** (protect autonomy; promote human well-being, safety and the public interest; ensure transparency, explainability and intelligibility; foster responsibility and accountability; ensure inclusiveness and equity; promote responsive and sustainable AI). The 2024 LMM guidance adds **40+ recommendations** for governments, tech companies and providers.
- **User flow:** Read guidance → map to five health application areas (diagnosis/clinical care; patient-guided use; clerical/administrative; medical/nursing education; scientific research/drug development) → adopt governance per role (developer/deployer/user).
- **Docs:** "Ethics and governance of artificial intelligence for health" (2021); "Guidance on large multi-modal models" (news release 18 Jan 2024).
- **Software shape:** Published guidance reports (no software).
- **Adopt:** A persistent **six-principles care-ethics bar** in the Care window.

### 6. HealthAI — Global Agency for Responsible AI in Health
- **What they do:** Geneva-based independent non-profit "championing responsible AI in health" — building/qualifying national & regional **validation mechanisms**, a **Global Regulatory Network** (GRN) for knowledge sharing and adverse-event monitoring, a **Global Directory** of registered AI health solutions, and advisory support on policy/regulation.
- **User flow:** Governments/orgs join the GRN or CoP → share knowledge, monitor adverse events → list solutions in the Global Directory → use micro-trainings/tools (Directory β, Navigator coming soon).
- **Docs:** FAQs, "What we do", annual reports, board meetings, code of conduct, blog; (news: Portugal first EU member of GRN 16 Jul 2026; Global Governance Forum 2026 in London, 18 Nov).
- **Software shape:** Website + member portal (login) + directory tooling; a membership/network organisation, not an app.
- **Adopt:** **Co-produced shared commitments** (an "AI constitution" style values pledge) shown in the Care window.

### 7. CQC — AI in health & social care
- **What they do:** England's independent health/social-care regulator. Encourages innovation-friendly AI use but frames regulation around ensuring AI contributes to **safe, equitable, person-centred care**. Does **not** assess/approve specific technologies; inspects providers. (Page last updated 21 May 2026.)
- **User flow:** Providers understand the "principles of good use of AI" → implement → CQC inspects (AI use "does not predict [a] specific rating"); the public can find/inspect care services.
- **Docs:** "Artificial intelligence in health and social care: CQC's role, expectations and plans" — enumerates benefits and risks (misdiagnosis, de-personalisation, unclear accountability, staff de-skilling, human-oversight workload increase, hallucination, privacy, carbon footprint).
- **Software shape:** Regulator guidance + inspection framework + provider portal; no consumer software.
- **Adopt:** Surface the **de-personalisation + "hallucinate as fact" + oversight-workload** cautions transparently in the window.

### 8. Mental-health AI auditing — SIM-VAIL
- **What they do:** A **clinically validated framework for auditing AI chatbot behaviour in mental-health interactions** (Nature Medicine, led by Oxford, UCL and the UK AI Security Institute). Simulates users with specific vulnerabilities (depression, mania, psychosis, OCD, insecure attachment) and intentions, runs multi-turn conversations, and scores each exchange across clinically grounded risk dimensions.
- **User flow:** Define simulated vulnerable-user profiles (30) → engage 9 frontier models (Claude, ChatGPT, Gemini, Grok, Llama…) in multi-turn chat (810 conversations, 90,000+ clinical ratings) → score risk per turn → identify **VAIL** ("Vulnerability-Amplifying Interaction Loop") → patch early escalation points → re-test.
- **Docs:** Nature Medicine paper; Oxford/UCL news (7 Aug 2026); open **SIM-VAIL Explorer** tool released.
- **Software shape:** Research framework + an open Explorer tool (benchmark/harness, not a product chatbot).
- **Adopt:** **Multi-turn vulnerability-aware scoring with early-turn intervention** — the single highest-value idea for a Care chat window.

### 9. Digital Care Hub / AI in Social Care Alliance
- **What they do:** UK non-profit digital-care advisory body (working with the Oxford Institute for Ethics in AI and Casson Consulting) that convened the **AI in Social Care Alliance** (17 Apr 2026) to co-produce an **"AI constitution for social care"**, create practical provider guidance (AI regulation, adoption frameworks, positive case studies), build a research/co-production hub, promote training, and connect stakeholders.
- **User flow:** Providers/care organisations join the Alliance → co-produce the constitution → adopt/adapt it → use guidance, training, case studies.
- **Docs:** "AI in Social Care Alliance: vision and priorities" (17 Apr 2026); advice pages on AI & robotics, data protection, standards; events/webinars.
- **Software shape:** Advice/knowledge-base website + network/events (no product software).
- **Adopt:** A **co-produced, accessible care constitution** rendered as a short values statement in the window.

### 10. Hippocratic AI — safety-focused healthcare LLM
- **What they do:** Commercial healthcare LLM/agent vendor with a proprietary **Polaris Constellation** architecture (specialised support models) and a **5-phase safety approach**: (1) Polaris Constellation architecture, (2) output testing, (3) human clinical supervision, (4) escalation to human nurse, (5) cross-validation. Claims: 5.0T+ parameter constellation; 7,700+ US licensed clinicians making 775K test calls; 180M+ clinical calls cross-validated.
- **User flow:** Deploy a clinical agent ("Orchestrator" + "Skills") → output is safety-tested → clinically supervised → escalated to a human nurse when needed → cross-validated against real calls.
- **Docs:** Safety page; Polaris 3.0/4.0 safety constellation whitepapers; "Clinician-Led Safety Evaluations for Generative AI at Scale" whitepaper; benchmarks; a safety-focused-LLM patent.
- **Software shape:** Proprietary LLM/API + agent products; not open-source.
- **Adopt:** A **persistent, visible escalation-to-human pathway** (duty-of-care handoff) — the clearest productised "safety-of-care" pattern in the set.

---

## 3. What CSOAI should adopt — 5 concrete improvements for the Care chat window

1. **Multi-turn vulnerability monitor with early-turn intervention (from SIM-VAIL).**
   Instrument the Care window to score conversation *trajectories* across clinically grounded risk dimensions (self-harm ideation, mania, psychosis, insecure attachment, "downplaying difficulties", "endorsing risky actions") — not just single messages. When a "Vulnerability-Amplifying Interaction Loop" is detected (a supportive-sounding reply that inadvertently reinforces the user's vulnerability), intervene **at the first concerning turn**: rephrase the reply and add a gentle safety check. SIM-VAIL showed replacing one early concerning response improves the whole downstream conversation.

2. **Persistent escalation-to-human + non-delegable duty-of-care notice (from Hippocratic AI + UKJT).**
   Put a permanent, high-visibility "talk to a person" handoff for crisis and safety-critical care content, and show a one-line notice that CSOAI **cannot delegate its duty of care to the model** (UKJT: AI has no legal personhood; care duties remain with accountable humans). Never leave a user in a care vacuum after a safety-relevant exchange.

3. **Risk-tiered response gating with proportionate evidence + disclaimer (from NICE ESF).**
   Classify each care query into a tier (A: informational/wellness → answer freely; B: self-management/support → cite sources, note it's not medical advice; C: clinical decision-support or a regulated-use case → strong disclaimer, encourage qualified human input, and route the *developer/adopter* question per AIDRS/MHRA qualification). Cite authoritative sources and flag uncertainty explicitly (CQC: AI can "hallucinate and present untrue information authoritatively as fact").

4. **Six-principles care-ethics bar + IEEE 7010 well-being indicator dashboard.**
   Render a persistent, checkable **principles strip** (WHO six: protect autonomy; promote well-being/safety; transparency/explainability; responsibility/accountability; inclusiveness/equity; responsive & sustainable AI). Behind it, track a lightweight **well-being indicator baseline** across a few IEEE 7010 domains (affect, psychological/mental well-being, community/social support, health) over the session and across visits — with longitudinal reporting, so the tool is accountable to *well-being outcomes*, not just output quality.

5. **Co-produced, user-visible "care constitution" (from Digital Care Hub / HealthAI).**
   Adopt a short, co-produced statement of care values and commitments (an "AI constitution" for the Care window) that is shown to users and held up as the standard they can hold the tool to. Include plain-language capability + consent transparency (carebots lesson: state what the assistant can/cannot do, how data is used, when human oversight is required) and a note on oversight workload so carers are not silently de-skilled (CQC).

---

## 4. Sources (primary, verified)

- NHS AIDRS — https://www.digitalregulations.innovation.nhs.uk/
- MHRA SaMD/AIaMD — https://www.gov.uk/government/publications/software-and-artificial-intelligence-ai-as-a-medical-device/software-and-artificial-intelligence-ai-as-a-medical-device
- MHRA AI Airlock — https://www.gov.uk/government/publications/ai-airlock-background/ai-airlock-background
- IEEE 7010-2020 — https://standards.ieee.org/ieee/7010/7718/ ; explanatory paper arXiv:2005.06620 (https://arxiv.org/abs/2005.06620)
- NICE ESF (ECD7) — https://www.nice.org.uk/corporate/ecd7
- WHO LMM guidance — https://www.who.int/news/item/18-01-2024-who-releases-ai-ethics-and-governance-guidance-for-large-multi-modal-models ; 2021 guidance https://www.who.int/publications/i/item/9789240029200
- HealthAI — https://healthai.agency/
- CQC AI in health & social care — https://www.cqc.org.uk/about-us/transparency/artificial-intelligence-health-social-care-cqcs-role-expectations-plans
- SIM-VAIL (Nature Medicine) — https://www.nature.com/articles/s41591-026-04577-2 ; Oxford summary https://www.psych.ox.ac.uk/news/new-audit-system-maps-how-mental-health-risks-emerge-in-ai-chatbot-conversations
- Digital Care Hub / AI in Social Care Alliance — https://www.digitalcarehub.co.uk/ai-in-social-care/
- Hippocratic AI safety — https://hippocraticai.com/safety/
- Carebots — IMechE "Automating the Home" via Loughborough — https://www.lboro.ac.uk/media-centre/press-releases/2025/july/new-rules-needed-keep-home-care-robots-safe/
- UKJT AI liability (final statement) — https://www.mishcon.com/news/ai-and-liability-ukjt-publishes-its-final-statement
