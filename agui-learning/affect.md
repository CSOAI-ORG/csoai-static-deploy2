# GSPC AFFECT Axis — Top-10 Competitor/Peer Research

**Scope:** emotional impact / mental-health-adjacent AI measurement (IEEE 7010 well-being, affective-computing assessment).
**Method:** web_search + curl against primary sources (standards pages, PDFs, GitHub, law-firm/think-tank explainers). Verified claims only; sources inline.
**Date of research:** 2026-08-21.

---

## 1. IEEE 7010-2020 — Well-Being Impact Assessment

- **What they do:** A voluntary "Recommended Practice for Assessing the Impact of Autonomous and Intelligent Systems on Human Well-Being." It gives product teams a *process* to assess how an A/IS affects human well-being, using defined well-being indicators, across the system lifecycle. It is a methodology, not a pass/fail certification.
- **User flow:** Assessor identifies affected stakeholders → selects relevant well-being indicators → maps the system's known/likely impacts to those indicators → iterates the assessment before, during, and after deployment. Human-driven; no automated scoring engine.
- **Docs:** [IEEE SA store — IEEE 7010-2020](https://standards.ieee.org/ieee/7010/7718/); full title on [normadoc](https://www.normadoc.com/english/ieee-7010-2020-5052480.html).
- **Software shape:** No software. A normative PDF standard; implementers typically build their own checklists/spreadsheets.
- **One thing CSOAI could adopt:** a **well-being-indicator readout** — the Affect chat window should surface a small, structured "well-being impact" panel (autonomy, control, belonging, relatedness, etc.) mapping the conversation to IEEE 7010-style indicators, instead of a single raw "emotion score."

## 2. Affective-Computing Evaluation Benchmarks — MME-Emotion (FunAudioLLM)

- **What they do:** MME-Emotion is the largest emotional-intelligence benchmark for multimodal LLMs: **6,500 curated video clips**, **8 emotional tasks**, scored on **three metrics** (recognition score, reasoning score, chain-of-thought score). Evaluation is done by a multi-agent system and the strategy was **validated by 5 human experts**; 20 open + closed MLLMs are benchmarked.
- **User flow:** Run a model on the video-QA set → extract key reasoning steps → a GPT-4o judge scores responses → compute the three metrics → submit to a public leaderboard.
- **Docs:** [GitHub repo](https://github.com/FunAudioLLM/MME-Emotion), [arXiv 2508.09210](https://www.arxiv.org/pdf/2508.09210), [project page + leaderboard](https://mme-emotion.github.io/), [HF dataset](https://huggingface.co/datasets/Karl28/MME-Emotion).
- **Software shape:** Open-source Python eval pipeline (extract-step → eval-CoT → metrics) + HF dataset + leaderboard.
- **One thing CSOAI could adopt:** split **recognition from reasoning** — the Affect window should report *"what emotion is present"* separately from *"why it might be present / what triggered it"*, never collapsing both into one sentiment label.
- *Adjacent peers verified:* [EmoNet-Face (DFKI, expert-annotated synthetic emotion recognition)](https://www.dfki.de/web/forschung/projekte-publikationen/publikation/16238), [LibEER (EEG emotion recognition benchmark)](https://www.semanticscholar.org/paper/LibEER%3A-A-Comprehensive-Benchmark-and-Algorithm-for-Liu-Yang/08c7a0169e699ffb137bbc99eed838666c6e2a85), [ParaLBench (computational paralinguistics)](https://ieeexplore.ieee.org/document/10767298).

## 3. Mental-Health AI Audit Frameworks — JMIR Psychotherapy Conversational Agent Framework

- **What they do:** "Evaluating the Quality of Psychotherapy Conversational Agents: Framework Development and Cross-Sectional Study" (JMIR Formative Research, 2025) develops and applies a multidimensional rubric to grade the *quality and safety* of mental-health chatbots — explicitly going beyond engagement to cover clinical safety, empathy, boundary handling, and escalation.
- **User flow:** Evaluators score a given mental-health conversational agent against the framework's dimensions, cross-sectionally, producing a structured quality profile rather than a single score.
- **Docs:** [JMIR Formative Research 2025;1:e65605](https://formative.jmir.org/2025/1/e65605). *Adjacent:* [Beyond Engagement — safe development of agentic AI in mental health (ACM)](https://dl.acm.org/doi/10.1007/978-3-032-06004-4_8); UK clinical context via [Wysa/Limbic/Woebot + NICE guidance](https://www.iatrox.com/blog/ai-mental-health-wysa-limbic-woebot-nice-guidance-uk).
- **Software shape:** Published evaluation framework (rubric + cross-sectional study), not packaged software.
- **One thing CSOAI could adopt:** a **crisis-escalation path** baked into the Affect window — detect distress markers and surface a human/helpline route, mirroring the safety/escalation dimension these audits actually score.

## 4. AIES / FAccT Research — Luke Stark & Jesse Hoey, "The Ethics of Emotion in AI Systems"

- **What they do:** Foundational peer-review critique of emotion-recognition AI. It confronts the scientific validity problem (drawing on Barrett et al. 2019's challenges to inferring emotion from facial movement) and catalogs the ethical harms of treating inferred affect as ground truth. The reference point for AIES/FAccT work on affect.
- **User flow:** Research artifact — scholars/designers read it to (a) question the construct validity of emotion-AI and (b) avoid over-claiming measurement.
- **Docs:** [ACM DL — DOI 10.1145/3442188.3445939 (FAccT '21)](https://dlnext.acm.org/doi/epdf/10.1145/3442188.3445939); [free PDF (UWaterloo)](https://cs.uwaterloo.ca/~jhoey/papers/AoIR2019-emotion_ethics_AI_final.pdf).
- **Software shape:** Paper (theory + critique); no software.
- **One thing CSOAI could adopt:** a permanent **validity disclaimer** in the Affect window — e.g., *"emotion labels are inferred, not observed"* — so CSOAI never over-claims what it is measuring.

## 5. EU AI Act — Article 5(1)(f) Workplace/Education Emotion-Recognition Ban

- **What they do:** The regulation itself. Article 5(1)(f) **prohibits** placing on the market, putting into service, or use of AI systems to **infer the emotions of a natural person in the workplace and education institutions** on the basis of biometric data, with narrow exceptions for **medical and safety** purposes. Emotion-recognition systems outside that scope are **high-risk** under Annex III. Article 3(39) defines "emotion recognition system" (identifying/inferring emotions *or intentions* from biometric data).
- **User flow:** Compliance — a deployer determines whether their system "infers emotions" of individuals in workplace/education from biometric data; if yes it is prohibited (unless medical/safety), otherwise high-risk obligations attach.
- **Docs:** [FPF "Red Lines" series — prohibition of emotion recognition](https://fpf.org/blog/red-lines-under-eu-ai-act-unpacking-the-prohibition-of-emotion-recognition-in-the-workplace-and-education-institutions/); [Wolters Kluwer analysis](https://global-workplace-law-and-policy.kluwerlawonline.com/2025/04/14/the-prohibition-of-ai-emotion-recognition-technologies-in-the-workplace-under-the-ai-act/); [Freshfields](https://www.freshfields.com/en/our-thinking/blogs/technology-quotient/eu-ai-act-unpacked-25-european-commission-releases-critical-ai-act-implementati-102kfql).
- **Software shape:** Law (no software).
- **One thing CSOAI could adopt:** a **scope-by-context gate** — explicitly scope the Affect window OUT of "inferring emotions of natural persons in workplace/education from biometric data," and frame it as voluntary self-reflection rather than biometric inference, keeping CSOAI clean of the prohibition.

## 6. Partnership on AI — "The Ethics of AI and Emotional Intelligence" (2020)

- **What they do:** PAI's report surveying the deployment of emotion-recognition across sectors (retail mood-based ads, classroom "engagement" scoring, automated video-interview mood evaluation, employee facial-expression monitoring) and framing the ethical questions — including the inference-validity limits (Barrett et al.) and the gap between what systems *claim* and what they *can* measure.
- **User flow:** Policy/design guidance — teams read the report to frame governance and to know which deployment patterns are ethically fraught.
- **Docs:** [PAI report page + PDF](https://partnershiponai.org/paper/the-ethics-of-ai-and-emotional-intelligence/) (published 2020-07-30; PAI Staff).
- **Software shape:** Report (PDF); no software.
- **One thing CSOAI could adopt:** a **"known misuses" framing** — the Affect window should carry a brief notice of the misuses CSOAI is *not* engaging in (workplace monitoring, hiring inference), aligning with PAI's misuse taxonomy and reinforcing neutrality.

## 7. NIST — ARIA program + AI 600-1 GenAI Profile (emotional attachment/entanglement)

- **What they do:** Two layers. **ARIA** (Assessing Risks and Impacts of AI) is a human-centric measurement program: scenario-based user↔AI interactions across three layers (model testing → red-teaming → field testing), with an annotation schema whose **"Interaction Style"** category captures whether output is *"perceived … as conveying an attitude or tone and creat[ing] a sense of relationship or dependency."* The **NIST AI 600-1 GenAI Profile** documents GAI-specific risks of **anthropomorphization, algorithmic aversion, over-reliance, and "emotional entanglement"** (including "Users' emotional entanglement with GAI functions" and "track and document instances of anthropomorphization").
- **User flow:** ARIA: scripted scenarios → human testers interact → annotators score whether risks materialized. GenAI Profile: organizations map emotional-entanglement/anthropomorphization risks to RMF functions.
- **Docs:** [ARIA Program Companion Document (PDF)](https://ai-challenges.nist.gov/aria/docs/ARIA_Program_Companion_Document_Dec20.pdf); [NIST AI 700-2](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.700-2.pdf); [Stanford Law "Emotional Entanglement in Generative AI" (on NIST AI 600-1)](https://law.stanford.edu/2024/05/13/emotional-entanglement-in-generative-ai/). *(Honesty note: the "emotional attachment" rubric lives in NIST AI 600-1 GenAI Profile; ARIA supplies the human-interaction measurement layer, not a standalone "attachment rubric.")*
- **Software shape:** Program/measurement methodology + a standards profile (PDFs); ARIA has a testbed/annotation tooling for its evaluations.
- **One thing CSOAI could adopt:** an **"interaction-style / dependency" signal** — detect and transparently flag when the chat is drifting toward a *relationship/dependency* dynamic (over-reliance, parasocial attachment), and surface it to the user rather than optimizing for it.

## 8. Trismik — Psychometric AI Evaluation (Cambridge spin-out)

- **What they do:** Applies **psychometric methods originally developed for measuring human intelligence** (e.g., Item Response Theory) plus **adaptive testing that adjusts difficulty in real time** to evaluating AI models — moving beyond narrow accuracy scores to richer evidence of a model's strengths/limitations. Raised **£2.2M** (2025).
- **User flow:** A model is administered an adaptive battery of items; item difficulty recalibrates from responses; the output is a calibrated ability estimate with uncertainty, not a single accuracy number.
- **Docs:** [Cambridge Enterprise case study](https://www.enterprise.cam.ac.uk/case-studies/trismik-applying-psychometric-methods-for-safer-ai/); [tech.eu funding note](https://tech.eu/2025/09/25/cambridge-spin-out-trismik-raises-ps22m-to-redefine-ai-evaluation/); [Scorebook library on GitHub](https://colab.research.google.com/github/trismik/scorebook/blob/main/tutorials/quickstarts/getting_started.ipynb); [adaptive-testing blog](https://www.trismik.com/blog/adaptive-testing-does-it-really-work/).
- **Software shape:** Proprietary platform + open-source `scorebook` Python library (GitHub/Colab).
- **One thing CSOAI could adopt:** **adaptive, calibrated measurement** — the Affect window should vary item difficulty by prior responses and report an estimate *with uncertainty* (confidence interval), never a naked label.

## 9. EU Commission — Guidelines on Prohibited AI Practices (Feb 2025)

- **What they do:** The Commission's interpretive guidelines operationalizing Article 5 (the "prohibited emotion-recognition provisions"). They clarify that the ban targets **"AI systems to infer emotions"** (not all "emotion-recognition systems"), that the inference must be **based on biometric data**, that **"inference of intentions"** sits inside the Article 3(39) definition but the prohibition's core is *inference of emotions*, and that **medical/safety** uses are excepted.
- **User flow:** Compliance practitioners read the guidelines to classify a system: is it "inferring emotions," on what basis, in what context, under which exception.
- **Docs:** [FPF Red Lines summary](https://fpf.org/blog/red-lines-under-eu-ai-act-unpacking-the-prohibition-of-emotion-recognition-in-the-workplace-and-education-institutions/); [CMS explainer (Part II)](https://cms.law/en/cze/legal-updates/eu-commission-issues-guidelines-on-prohibited-ai-practices-part-ii); [Lewis Silkin](https://www.lewissilkin.com/insights/2025/02/17/understanding-the-eu-ai-acts-prohibited-practices-key-workplace-and-advertising-102k011).
- **Software shape:** Guidance document (PDF); no software.
- **One thing CSOAI could adopt:** **definitional rigor in CSOAI's own claims** — mirror the guidelines by distinguishing *inferring emotion* from *inferring intention* and by requiring a biometric-data basis before any "emotion" claim, so the Affect window's wording stays provable and conservative.

## 10. IEEE P7014.1 — Emulated Empathy Ethics (draft standard)

- **What they do:** Draft "Recommended Practice for Ethical Considerations of Emulated Empathy in Partner-based General-Purpose AI Systems." It defines ethical considerations and good practices for systems that **emulate empathy** (companion/partner AI), including the central question of when emulated empathy becomes **deception**.
- **User flow:** Designers of companion/empathic systems use the recommended practices to bound when/how the system signals empathy and how to disclose that the empathy is simulated.
- **Docs:** [IEEE SA draft page](https://xplorestaging.ieee.org/document/11270034); [Bangor U — "Emulated Empathy: Can Risks be Countered by a Soft-law Standard?"](https://research.bangor.ac.uk/files/80472515/Emulated_Empathy_Can_Risks_be_Countered_by_a_Soft-law_Standard_.pdf).
- **Software shape:** Standard document (draft); no software.
- **One thing CSOAI could adopt:** a **deception guardrail** — the Affect window should *always* disclose when its empathy is simulated and never imply genuine feeling (disclosure-of-emulation), the exact concern P7014.1 is written to address.

---

## 10-Competitor Summary Table

| # | Competitor / Peer | Category | What it is | Software shape | Adopt in Affect window |
|---|---|---|---|---|---|
| 1 | [IEEE 7010-2020](https://standards.ieee.org/ieee/7010/7718/) | Well-being impact assessment | Recommended practice to assess A/IS impact on human well-being via indicators | Standard PDF (no code) | Well-being-indicator readout panel |
| 2 | [MME-Emotion](https://github.com/FunAudioLLM/MME-Emotion) (+ EmoNet-Face, LibEER) | Affective-computing eval | 6,500 clips, 8 tasks, recognition/reasoning/CoT metrics, multi-agent scoring | Open-source Python + HF + leaderboard | Split recognition vs. reasoning |
| 3 | [JMIR Psychotherapy Agent Framework](https://formative.jmir.org/2025/1/e65605) (+ "Beyond Engagement") | Mental-health AI audit | Multidimensional quality/safety rubric for mental-health chatbots | Published rubric | Crisis/escalation path + safety scoring |
| 4 | [Stark & Hoey, FAccT '21](https://dlnext.acm.org/doi/epdf/10.1145/3442188.3445939) | AIES/FAccT research | Critique of emotion-AI validity + harms | Paper | "Inferred, not observed" validity caveat |
| 5 | [EU AI Act Art. 5(1)(f)](https://fpf.org/blog/red-lines-under-eu-ai-act-unpacking-the-prohibition-of-emotion-recognition-in-the-workplace-and-education-institutions/) | Emotion-AI regulator | Prohibits workplace/education emotion inference (medical/safety excepted) | Law | Scope-by-context gate |
| 6 | [PAI "Ethics of AI & Emotional Intelligence"](https://partnershiponai.org/paper/the-ethics-of-ai-and-emotional-intelligence/) | PAI affective tools | Sector survey of emotion-AI deployment + ethics framing | Report PDF | "Known misuses" framing |
| 7 | [NIST ARIA](https://ai-challenges.nist.gov/aria/docs/ARIA_Program_Companion_Document_Dec20.pdf) + [AI 600-1 GenAI Profile](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf) | Emotional-attachment rubric | Human-interaction risk measurement; emotional-entanglement/anthropomorphization risks | Methodology + profile PDF | Interaction-style / dependency signal |
| 8 | [Trismik](https://www.enterprise.cam.ac.uk/case-studies/trismik-applying-psychometric-methods-for-safer-ai/) | Psychometric AI eval | IRT + adaptive testing for calibrated model measurement | Platform + `scorebook` OSS | Adaptive, calibrated (uncertainty) measurement |
| 9 | [EU Commission Prohibited-Practices Guidelines](https://cms.law/en/cze/legal-updates/eu-commission-issues-guidelines-on-prohibited-ai-practices-part-ii) | Prohibited-provisions guidance | Clarifies "infer emotions," biometric basis, intention vs. emotion, exceptions | Guidance PDF | Definitional rigor in CSOAI claims |
| 10 | [IEEE P7014.1](https://xplorestaging.ieee.org/document/11270034) | Emulated-empathy ethics | Recommended practice for ethical emulated empathy / deception risk | Draft standard | Emulation-disclosure guardrail |

---

## What CSOAI Should Adopt — 5 Concrete Improvements for the Affect Chat Window

1. **Well-being-indicator readout instead of a raw emotion score (IEEE 7010).**
   Replace any single "emotion/sentiment" number with a structured panel of well-being dimensions — autonomy, control, relatedness, competence, safety — each with a plain-language line and a confidence range. This positions CSOAI as measuring *well-being impact* (the defensible, standard-aligned construct) rather than "reading" emotion (the contested construct).

2. **Split recognition from reasoning, with a "why" trace (MME-Emotion).**
   Show two distinct outputs: *what* affective state is suggested (recognition) and *why* — the observable cues/triggers in the conversation that led there (reasoning). Make the "why" the primary artifact; it is falsifiable and reviewable, whereas a bare label is not.

3. **Permanent validity + emulation disclosure (Stark/Hoey + IEEE P7014.1).**
   Always render two fixed disclaimers in the window: (a) *"affect labels are inferred from text cues, not observed"* (construct-validity honesty) and (b) *"any empathy expressed here is simulated"* (deception guardrail). Never let the UI imply the model has genuine feeling or clinically-validated insight.

4. **Crisis/escalation + safety path, not engagement (mental-health AI audits).**
   Add a distress-detection layer that, on recognized crisis markers, (a) pauses measurement framing, (b) surfaces validated helpline/care options, and (c) offers a human/clinical handoff note. Score the interaction on safety/boundary-handling axes — never on "did the user stay engaged."

5. **Scope-by-context gate + definitional rigor (EU AI Act Art. 5(1)(f) + Commission Guidelines).**
   Put a visible, machine-readable scope statement in the window: CSOAI does **not** infer the emotions of natural persons in workplace/education settings from biometric data; it offers **voluntary self-reflection** on user-authored text. Adopt the Guidelines' precision in CSOAI's own copy — say "inferred affective signal," never "detected emotion," and never claim an "intention" reading. This keeps the Affect axis on the safe side of the prohibition while still being a real measurement instrument.

---

### Honesty ledger (claims NOT made)
- IEEE 7010, P7014.1, and the EU AI Act/Guidelines ship no software — described as standards/law only.
- NIST's emotional-attachment language is attributed to **AI 600-1 (GenAI Profile)**, not to ARIA as a standalone "attachment rubric"; ARIA is credited for the human-interaction measurement layer and the "Interaction Style → relationship/dependency" annotation.
- MME-Emotion's 6,500/8/3/5/20 figures and Trismik's £2.2M raise are quoted from primary sources linked above; not independently re-measured.
- No accounts created, no submissions made (research-only, per instruction).
