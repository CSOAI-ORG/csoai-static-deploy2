# CSOAI AG UI — TRAINING Lane Competitive Research

**Scope:** AI-governance education/academy — turning the 16 measured GSPC axes into learnable material.
**Method:** web_search + curl against primary sources. Verified claims only; sources cited inline.
**Status:** Research-only. No accounts, no submissions, no paid content accessed.

---

## 1. Ten-competitor table

| # | Competitor | What they do | User flow | Docs | Software shape | One thing CSOAI could adopt |
|---|---|---|---|---|---|---|
| 1 | **EU AI Act Explorer** — Future of Life Institute | Interactive navigator of the EU AI Act's 100+ articles/annexes/recitals, plus a compliance checker. Explicitly a *neutral* tool, "not associated with the European Union." | Land → pick article / filter by topic or role / read obligations → use compliance checker for a risk-level self-assessment → subscribe to bi-weekly updates. | Full act text, article-by-article obligations, annexes, recitals, compliance-checker questions ("coming soon" area flagged), newsletter. | WordPress site with faceted/filterable content (filterable_portfolio), search, multi-language toggle (EN/FR/DE/ES). | **Role + use-case filter on the corpus** — a learner says "I am a deployer building a high-risk system" and only the relevant obligations surface. |
| 2 | **ICO — Guidance on AI & data protection** (UK regulator) | Official regulator guidance translating UK GDPR into AI practice across the lifecycle. | Browse guidance → follow the five "What you need to know" summaries per topic → apply fairness/lawfulness tests with Annex A. | Topic guidance on accountability/governance, transparency, lawfulness, accuracy, fairness; Annex A (fairness in AI lifecycle); glossary. | Static HTML guidance pages, sectioned with per-section "What you need to know" call-outs. | **"What you need to know" summary box** before every lesson — a 3-line plain-language takeaway that precedes depth. |
| 3 | **Alan Turing Institute — AI Ethics & Governance in Practice** | Public-sector capacity-building programme; teaches civil servants to *facilitate* ethics, not just read policy. | Workbook-led modules: Key Concepts → Activities → in-house "AI Ethics Champion" runs the exercises with a team. | Downloadable workbooks; plain-language AI/ML definitions; lifecycle walkthrough; frameworks (CARE/ACT, SSAFE-D, SUM Values); domain workbooks (policing, social care, education, urban planning). | PDF/self-hosted workbook series (aiethics.turing.ac.uk) with module progression; facilitator-led, workshop-ready exercises. | **Facilitator ("AI Ethics Champion") path** — turn a learner into someone who can run a workshop, with role-play dilemma exercises included. |
| 4 | **Coursera — LSE "AI Law, Policy & Governance"** | University certificate course on the global regulatory landscape (US, China, UK, EU). | Apply → orientation week → 6 weekly modules at 6–8 hrs/week → graded work → certificate. | Module syllabus, faculty pages, brochure, programme structure; LSE Law School + School of Public Policy. | EdX/GetSmarter LMS: video lectures, readings, discussion, assessments, cohort-dated (self-paced window). | **Structured multi-week module arc with a certificate** — a defined "track" that ends in a verifiable completion credential. |
| 5 | **UNESCO — Global MOOC on the Ethics of AI** (with LG AI Research) | Free MOOC turning the 193-country-endorsed Recommendation on the Ethics of AI into practical learning. | Enroll free on Coursera → 9-hour self-paced course → hands-on projects → completion. | 9-hour, intermediate, 11 languages; no advanced technical knowledge required; expert inputs (CMU, U Toronto, Alan Turing Institute). | Coursera MOOC: short videos + hands-on projects on privacy, transparency, sustainability, human autonomy. | **Translate principles → hands-on scenario projects**, with multi-language delivery for global reach. |
| 6 | **NIST — AI Risk Management Framework + Playbook** | Government reference framework (Govern/Map/Measure/Manage) + a Playbook of suggested actions, with sector Profiles and a Roadmap. | Read framework → use Playbook's suggested actions per function → apply a Profile (e.g. Trustworthy AI in Critical Infrastructure). | Framework v1.0, AI RMF Playbook, Profiles, Roadmap, Trustworthy & Responsible AI Resource Center. | Static government web pages + downloadable PDFs; function-based taxonomy; links to third-party training (LinkedIn/Skillsoft/etc.). | **"Govern→Map→Measure→Manage" function scaffold** — reuse as the spine that each GSPC axis maps onto. |
| 7 | **AI Safety Fundamentals — BlueDot Impact** | Free, application/cohort-based talent accelerator for AI safety, alignment and governance. | "Future of AI" (2-hr, self-paced, no application) → apply to cohort courses (AI Alignment / AI Governance) → grants + in-person programs. | Course syllabi, reading lists, audio versions, facilitator guides; 8,000+ alumni, 25% land impactful roles in 6 months. | Next.js web app with course dropdowns, application funnel, community/events directory, grants portal. | **Funnel design: 2-hour free taste → application-gated deeper track** — low friction entry, then a commitment gate. |
| 8 | **MIT Sloan — "AI Risk & Readiness: From Governance to Growth"** | Two-day executive course reframing governance as an *enabler* of AI adoption, not a brake. | Book → 2-day in-person (8 hrs/day) → certificate counting toward MIT Sloan Executive Certificates. | Course overview, takeaways, schedule, faculty, "Who should attend"; draws on IBM Research AI Security/Safety/Governance + Harvard Law School frameworks. | Executive-ed LMS (Salesforce/on-demandware site); $5,700 tuition, cohort-dated. | **"Governance = speed" reframe** as the onboarding hook — position the Training lane as the accelerator, not the compliance tax. |
| 9 | **GovAI (Centre for the Governance of AI)** | Research institute producing governance analysis and *fostering talent* via fellowships rather than courses. | Apply to a fellowship (DC/UK Summer/Winter, US AI Policy Program) → research + mentorship → alumni network. | Research/analysis posts, annual reports, opportunity listings; 501(c)(3) (EIN 99-4000294). | Content website + research publishing; fellowship = cohort + stipend, not an LMS. | **Mentorship/alumni network layer** — governance education compounds when learners join a peer network that tracks outcomes. |
| 10 | **Compliance micro-certs — CompTIA SecAI+ & OneTrust** | Vendor-neutral (CompTIA) and vendor (OneTrust) micro-credentials validating AI security/governance skills. | CompTIA: study objectives → sit exam (CY0-001, 60 Q, 60 min, pass 600/900). OneTrust: complete courses → pass exam → earn Credly badge in a learning track. | CompTIA exam-objectives domains (AI concepts 17%; AI governance/risk/compliance 19%; AI security ops…). OneTrust learning tracks + certification brochure. | CompTIA: proctored MCQ + performance-based exam. OneTrust: course platform + Credly badge integration. | **Exam-objective "domain weights" + a portable badge** — publish what % each GSPC axis counts for, and issue a shareable (signed) credential on completion. |

---

## 2. What CSOAI should adopt (5 concrete improvements for the Training chat window)

These are ordered by leverage, each grounded in a verified peer practice.

### 1. Curriculum per axis (spine = NIST's Govern→Map→Measure→Manage)
Give every one of the 16 GSPC axes a **structured lesson track**, not a flat FAQ. Each axis track gets: a learning objective, plain-language key concepts, a worked example, a "what you need to know" summary (ICO #2), and a self-check. Reuse NIST's function scaffold (#6) so `gov`, `care`, `safety`, `privacy`, `fairness`, etc. each map to Govern/Map/Measure/Manage stages — this makes the axis curriculum directly comparable to the framework practitioners already know.

### 2. Micro-lessons with a 2-minute "Future of AI" style entry
Adopt BlueDot's funnel (#7) + UNESCO's 9-hour chunking (#5). The Training window should serve **2–5 minute micro-lessons**: one idea, one definition, one example, then a single check question. Start with a no-login "What is AI governance?" primer so a first-time visitor gets value in under 2 minutes, then gate the deeper per-axis tracks. Every micro-lesson opens with the ICO-style "What you need to know" one-liner.

### 3. Quiz predicates tied to the measured axis
Adopt CompTIA's objective-weighting (#10) + Turing's dilemma role-plays (#3). Define each axis as a set of **checkable predicates** (e.g. *"fairness: can you distinguish model-level bias from system-level bias in a given scenario?"*). Auto-generate quiz items from these predicates, and *close the loop back to measurement*: the quiz result is a prediction of the learner's likely GSPC axis score, which the live benchmark later confirms or refutes. "Quiz predicates" = declarative, machine-checkable statements per axis, so every question maps to an axis and a competency level, never a vibes check.

### 4. Role/use-case filter on the whole corpus
Adopt the EU AI Act Explorer's faceted filtering (#1). Add a first prompt in the Training window — "I am a **policymaker / deployer / developer / auditor** working on a **high-risk / general-purpose / minimal-risk** system" — and dynamically narrow lessons and obligations to that role. This is the single highest-signal navigation improvement across the peer set and directly fits the AG UI's chat-native affordance.

### 5. Completion credential + facilitator ("AI Ethics Champion") path
Adopt Turing's facilitator model (#3) and MIT/OneTrust credentialing (#8, #10). On finishing a track, issue a **signed learning attestation** (consistent with CSOAI's existing living-training-attestation posture) rather than a "certification," and offer an advanced path that trains the learner to *facilitate* an axis workshop for their team — turning passive readers into multipliers, the strongest retention mechanism any peer demonstrated.

---

## 3. Honesty / verification notes

- **GovAI (#9)** is a research institute; its "courses" are *fellowships and research programs*, not self-paced lessons. Reported accordingly.
- **NIST (#6)** publishes the framework/playbook; the "training" products (LinkedIn Learning, Skillsoft, Udemy) are third-party, so the adoptable lesson is the *structure*, not a NIST-run course.
- **EU AI Act Explorer (#1)** footer states it is "provided by the Future of Life Institute and is not associated with the European Union."
- **CompTIA SecAI+** exam details (CY0-001, launch 17 Feb 2026, 60 Q / 60 min / pass 600, "AI governance, risk, and compliance (19%)" domain) verified on the vendor page.
- **UNESCO MOOC**: free, 9 hours, 11 languages, intermediate, built with LG AI Research on the 193-country Recommendation — verified via Coursera's announcement.

### Primary sources
- EU AI Act Explorer — https://artificialintelligenceact.eu/ai-act-explorer/
- ICO AI guidance — https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/artificial-intelligence/guidance-on-ai-and-data-protection/
- Turing AI Ethics & Governance in Practice — https://www.turing.ac.uk/research/research-projects/ai-ethics-and-governance-practice
- LSE AI Law, Policy & Governance — https://www.lse.ac.uk/study-at-lse/executive-education/programmes/ai-law-policy-and-governance
- UNESCO Ethics of AI MOOC — https://blog.coursera.org/unesco-partners-with-coursera-and-launches-free-ai-ethics-course/
- NIST AI RMF + Playbook — https://www.nist.gov/itl/ai-risk-management-framework · https://www.nist.gov/itl/ai-risk-management-framework/nist-ai-rmf-playbook
- AI Safety Fundamentals — https://aisafetyfundamentals.com/
- MIT Sloan AI Risk & Readiness — https://executive.mit.edu/course/ai-risk-and-readiness/a05U100000E3vJRIAZ.html
- GovAI — https://www.governance.ai/
- CompTIA SecAI+ — https://www.comptia.org/en-us/certifications/secai · OneTrust — https://www.onetrust.com/certifications/
