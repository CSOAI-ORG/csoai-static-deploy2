# FAIRNESS Axis — Competitive & Peer Research (GSPC bias/fairness)

**Scope:** The `FAIRNESS` axis of the GSPC — the `ll144-bias-audit` surface and EU AI Act
Art. 10 bias requirements. This is competitive/peer research to learn what the market already
builds for bias detection, fairness measurement, and audit, and to extract adoptable ideas for
CSOAI's **AG UI Fairness chat window**.

**Method:** `web_search` + `curl` against primary sources (READMEs, docs, license files, vendor
sites). **Verified claims only** — where a claim could not be confirmed from a primary source it
is marked ⚠️ or stated as lower confidence. Research only; no accounts created, no submissions.

---

## 1. Ten-competitor summary table

| # | Competitor | What they do (one line) | Software shape | ONE thing CSOAI could adopt |
|---|------------|-------------------------|----------------|------------------------------|
| 1 | **IBM AI Fairness 360 (AIF360)** | Open-source toolkit: fairness metrics + explanations + bias-mitigation algorithms across the AI lifecycle | Python + R library (Apache-2.0), notebooks, ReadTheDocs, interactive web demo | Metric-with-plain-English-explanation + matched mitigation suggestions in the fairness window |
| 2 | **Google What-If Tool (WIT)** | No-code visual "probing" of a black-box model; counterfactual edits + fairness over data subsets | Web UI inside TensorBoard + Jupyter/Colab notebook widget (PAIR) | Counterfactual "what-if" panel: flip a protected attribute and show the decision delta |
| 3 | **Microsoft Fairlearn** | Fairness metrics + mitigation algorithms framed around harms (allocation vs quality-of-service) | Python package (MIT), Jupyter notebooks, Fairlearn dashboard / Azure ML integration | Group-fairness framing: label each check as *allocation harm* vs *quality-of-service harm* |
| 4 | **Holistic AI** | Commercial AI governance/GRC platform: bias auditing, risk assessment, EU AI Act compliance | SaaS platform + "programmable controls" for continuous governance | Bias-audit *evidence* + continuous (not one-shot) re-audit cadence in the UI |
| 5 | **Credo AI** | Enterprise responsible-AI governance: requirements, risk/fairness assessment, policy, registries | SaaS platform + Integrations Hub (toolchain connections) | Fairness check mapped to a policy/requirement + compliance status trail |
| 6 | **LatticeFlow** | Model validation & EU AI Act compliance evaluation (incl. LLM bias/fairness) | SaaS/enterprise platform + public "EU AI Act Checker" | Clause-level regulatory mapping: show which EU AI Act article each fairness check evidences |
| 7 | **Arthur AI** | Proactive ML model monitoring & observability: performance, drift, bias/fairness | Enterprise SaaS monitoring platform (APIs/SDK) | Continuous fairness monitoring vs a static snapshot — time-series drift on fairness scores |
| 8 | **Fiddler AI** | AI observability + explainable AI (SHAP-based): bias/fairness, drift, root-cause | Enterprise SaaS (pipeline integration) | Slice/subgroup explorer with explanation overlay on the fairness metric |
| 9 | **TruEra** | AI quality management: testing, diagnostics (fairness/drift/explainability), monitoring | Enterprise platform; test harnesses ("AIQ tests") + diagnostics | Fairness as a *test suite* with pass/fail gates, not just a report number |
| 10 | **Parity AI** | Responsible-AI bias auditing, notably recruitment-algorithm audits | Consulting-flavored audit service + analytics (smaller vendor) ⚠️ | Third-party/independent-auditor stance: "we measure, you decide" neutrality framing |
| — | **Audit frameworks (DORA / CSRD / EU AI Act Art. 10)** | Regulatory lenses that make bias a *material* disclosure item | Standards/text (not software) | Materiality + disclosure framing: tie fairness score to a regulatory obligation |

---

## 2. Per-competitor detail (1–5)

### 1. IBM AI Fairness 360 (AIF360) ✅ verified via README
- **(1) What it does:** An extensible open-source toolkit "to help detect and mitigate bias in
  machine learning models throughout the AI application lifecycle." Ships a comprehensive set of
  fairness metrics (group-fairness, sample-distortion, Generalized Entropy Index, Differential
  Fairness/Bias Amplification), explanations for those metrics, and ~15 bias-mitigation algorithms
  (Optimized Preprocessing, Disparate Impact Remover, Equalized Odds, Reweighing, Reject Option
  Classification, Prejudice Remover, Calibrated Equalized Odds, Learning Fair Representations,
  Adversarial Debiasing, Exponentiated/Gradient/Grid-Search Reductions, Fair Data Adaptation,
  Sensitive Set Invariance).
- **(2) User flow:** Data scientist loads a dataset → computes metrics → consults guidance material
  ("which metrics/algorithms are appropriate for my use case") → applies a mitigation algorithm →
  re-measures. An interactive web experience (`aif360.res.ibm.com/data`) gives a gentle no-code intro.
- **(3) Docs:** ReadTheDocs API + tutorials/notebooks in `examples/`; guidance page
  (`aif360.res.ibm.com/resources#guidance`).
- **(4) Software shape:** Python **and R** packages, Apache-2.0, CI-tested, Slack community.
- **(5) Adopt:** The pairing of **metric → plain-language explanation → matched mitigation**. In the
  Fairness window, every GSPC fairness reading should explain *what the number means* and *what a
  model owner can do about it*, not just report a score.

### 2. Google What-If Tool (WIT) ✅ verified via README
- **(1) What it does:** A no-code visual interface "for expanding understanding of a black-box
  classification or regression ML model" — inference over many examples, immediate visualization,
  and **counterfactual editing** (edit a datapoint, re-run, see the change). Includes tooling for
  "investigating model performance and fairness over subsets of a dataset."
- **(2) User flow:** Load a model + dataset → point-and-click on individual datapoints → edit feature
  values (e.g., flip a protected attribute) → observe prediction change → slice by fairness subsets.
  Zero code required.
- **(3) Docs:** `pair-code.github.io/what-if-tool` with tutorials (bias/features-overview) and demos
  (e.g., UCI Census salary predictor).
- **(4) Software shape:** Web widget embedded in **TensorBoard** or as a **Jupyter/Colab notebook
  extension**; part of Google's People + AI Research (PAIR). ⚠️ Primarily research/educational —
  not an actively marketed commercial product line.
- **(5) Adopt:** A **counterfactual probe panel** in the Fairness chat window: "show the datapoint
  whose decision flips when a protected attribute changes, and the size of that flip."

### 3. Microsoft Fairlearn ✅ verified via README.rst + fairlearn.org
- **(1) What it does:** A Python package to "assess their system's fairness and mitigate any observed
  unfairness." Frames unfairness as **harms** — *allocation harms* (opportunities/resources
  withheld, e.g., hiring, lending) and *quality-of-service harms* (system works worse for some
  people). Uses **group fairness** (which groups are at risk).
- **(2) User flow:** Specify sensitive/group features → compute metrics (e.g., **demographic parity,
  equalized odds**) → run mitigation algorithms → view results in a Fairlearn dashboard → export.
- **(3) Docs:** `fairlearn.org` (user guide, API, examples); Jupyter notebooks in-repo.
- **(4) Software shape:** Python package (MIT, Microsoft + Fairlearn contributors); **Azure Machine
  Learning fairness dashboard** integration for enterprise.
- **(5) Adopt:** The **harms taxonomy** — label each Fairness-window check as *allocation* vs
  *quality-of-service*, because the right metric and threshold depend on which harm applies.

### 4. Holistic AI ✅ vendor site + gov.uk listing
- **(1) What it does:** A commercial AI **governance, risk & compliance platform** covering bias
  auditing, robustness, explainability, and EU AI Act alignment. Listed on the UK government's AI
  assurance techniques catalogue (`gov.uk/ai-assurance-techniques`).
- **(2) User flow:** Register a model/AI use case → run bias & risk audits → get risk scores + gaps →
  remediate and re-audit. Emphasizes **continuous** governance via "programmable controls."
- **(3) Docs:** Vendor blog + platform docs; guidance materials; OECD Trustworthy AI Toolkit inclusion.
- **(4) Software shape:** SaaS GRC platform (not open source); 2025 IDC AI-governance-platform mention.
- **(5) Adopt:** **Continuous re-audit cadence** — the Fairness window should show *when* a model was
  last measured and schedule re-measurement (drift/retrain triggers), not treat fairness as one-and-done.

### 5. Credo AI ✅ vendor site + press
- **(1) What it does:** Enterprise responsible-AI governance platform: requirements management, risk
  and **fairness assessment**, policy enforcement, and model registries/evidence.
- **(2) User flow:** Define AI use-case + requirements → run assessments (fairness/risk) → track
  compliance status against policies → generate evidence for audits → connect tooling via Integrations Hub.
- **(3) Docs:** `credo.ai` resources/blog + an **Integrations Hub** describing ecosystem connectors.
- **(4) Software shape:** Enterprise SaaS; governance/registries + integrations (toolchain-agnostic).
- **(5) Adopt:** **Requirement ↔ evidence mapping** — each Fairness-window reading should link back to
  a named governance requirement/policy and carry a pass/warn/fail status, producing an audit trail.

### 6. LatticeFlow ✅ vendor site + Reuters/tech press
- **(1) What it does:** AI model evaluation & validation, including bias/fairness and safety;
  published an **EU AI Act Checker** that benchmarked leading models against the Act and reported
  compliance gaps (widely covered Oct 2024, incl. Reuters).
- **(2) User flow:** Onboard a model → run evaluation suite (fairness, robustness, safety) → get a
  clause-by-clause EU AI Act compliance report → remediate.
- **(3) Docs:** Vendor docs + public EU AI Act Checker results/leaderboard.
- **(4) Software shape:** Enterprise SaaS/platform; ETH Zürich spin-off lineage.
- **(5) Adopt:** **Clause-level regulatory mapping** — for each fairness check, explicitly state
  *which EU AI Act provision it evidences* (e.g., Art. 10 data governance bias) so the score is
  audit-ready, not abstract.

### 7. Arthur AI ✅ vendor site + directory listings
- **(1) What it does:** Proactive **ML model monitoring & observability** platform: performance,
  data/model **drift**, bias/fairness, and explainability across production deployments.
- **(2) User flow:** Connect models via SDK/API → dashboards surface performance + drift + fairness
  alerts → drill into root cause.
- **(3) Docs:** Vendor documentation portal (product docs).
- **(4) Software shape:** Enterprise SaaS observability platform (SDK/API integration).
- **(5) Adopt:** **Time-series fairness monitoring** — show the fairness score over time with a
  drift alarm, so the Fairness window catches *degradation*, not just a single baseline reading.

### 8. Fiddler AI ✅ vendor site + Mozilla Ventures
- **(1) What it does:** AI **observability + explainable AI** (SHAP-based explanations) with model
  performance management: bias/fairness metrics, drift, and root-cause analysis. Mozilla Ventures
  is a disclosed investor.
- **(2) User flow:** Integrate pipelines → monitor models → view **slices/subgroups** with
  explainability overlays → trace drift/bias to root cause.
- **(3) Docs:** Vendor docs + blog (e.g., "Human-Centric Design for Fairness and Explainable AI").
- **(4) Software shape:** Enterprise SaaS; pipeline/MLOps integrations.
- **(5) Adopt:** A **subgroup/slice explorer** — break the fairness score down per protected group
  (and intersections) with an explanation overlay on *why* the disparity exists.

### 9. TruEra ✅ docs.truera.com + datasheet
- **(1) What it does:** AI **quality management** — model testing, diagnostics (fairness, drift,
  explainability), and monitoring; markets "TruEra Diagnostics" and test harnesses ("AIQ tests").
- **(2) User flow:** Run a **test suite** on a model → receive test summaries (pass/fail) → drill into
  diagnostics (which slices/features drive unfairness) → monitor in production.
- **(3) Docs:** `docs.truera.com` (Model Test Summaries, test-harness results).
- **(4) Software shape:** Enterprise platform; diagnostics datasheets; test-harness concept. ⚠️
  Corporate/status specifics (any merger) not independently confirmed here.
- **(5) Adopt:** **Fairness-as-a-test-suite** — express the GSPC fairness axis as explicit
  pass/fail gates with named tests (disparate impact, equalized odds, subgroup parity), each
  individually reported.

### 10. Parity AI ✅ Computer Weekly + directory listings
- **(1) What it does:** A responsible-AI auditing company, notably auditing **recruitment
  algorithms for bias** (Computer Weekly coverage); positions as an independent bias-audit service.
- **(2) User flow:** Engagement-based: org submits an algorithm → Parity audits for bias → delivers
  findings/remediation recommendations. ⚠️ Smaller vendor; product surface less public.
- **(3) Docs:** Limited public docs; coverage via Computer Weekly and vendor directories.
- **(4) Software shape:** Audit service + analytics (consulting-flavored rather than a self-serve SDK).
- **(5) Adopt:** The **independent-auditor stance** — the Fairness window should present CSOAI as a
  neutral measurer ("we measure, you decide"), reinforcing the measurement-neutrality brand, not a
  vendor pushing a single mitigation.

---

## 3. Audit-framework angle (DORA / CSRD / EU AI Act Art. 10)

- **EU AI Act Art. 10 (data & data governance):** high-risk AI training/validation/testing data must
  be relevant, representative, free of errors, complete, and must examine possible **biases**. This is
  the direct statutory hook for the `ll144-bias-audit` surface.
- **DORA (Digital Operational Resilience Act):** financial-entity operational resilience; increasingly
  read **in convergence with the EU AI Act** so AI/ML risks (incl. bias in financial models) become
  resilience/risk items with mandatory testing and incident reporting.
- **CSRD (Corporate Sustainability Reporting Directive):** ESG/sustainability reporting where the
  **social ("S") dimension** and due-diligence obligations make workforce/algorithmic fairness a
  material *disclosure* item.
- **Adoptable idea:** treat a fairness score as a **materiality/disclosure artifact** — the Fairness
  window should be able to state "this finding is material under Art. 10 / DORA / CSRD" and produce a
  citable evidence line, turning measurement into compliance fuel.

---

## 4. What CSOAI should adopt — 5 concrete improvements for the Fairness chat window

1. **Metric + plain-English explanation + matched mitigation (from AIF360).** Every fairness reading
   should render as: metric name (demographic parity / equalized odds / disparate impact / generalized
   entropy) → one-sentence plain-English meaning → a ranked list of *matched* mitigation options
   (reweighing, disparate-impact remover, equalized-odds postprocessing) with accuracy-vs-fairness
   trade-off notes. CSOAI *recommends* mitigations but never auto-applies — preserving neutrality.

2. **Counterfactual "what-if" probe (from What-If Tool).** Add an interactive panel that surfaces the
   datapoint(s) whose decision flips when a protected attribute changes, showing the max sensitivity
   delta. This converts a raw bias score into a human-legible "here is where it is unfair" probe with
   zero code required.

3. **Subgroup/slice explorer with explanation overlay (from Fiddler + Arthur).** Break the fairness
   score down per protected group and **intersections** (not just binary), with a drift time-series and
   a SHAP-style explanation of *why* a disparity exists. Moves the window from snapshot → monitoring.

4. **Fairness-as-a-test-suite with pass/fail gates (from TruEra + Fairlearn).** Render the GSPC
   fairness axis as explicit named tests (disparate impact, equalized odds, subgroup parity) with
   thresholds and pass/warn/fail status, each labeled *allocation* vs *quality-of-service* harm, and
   show a continuous re-audit cadence (from Holistic AI).

5. **Clause-level regulatory evidence trail (from LatticeFlow + Credo AI).** For each fairness check,
   emit an audit-grade evidence line mapping the measured artifact to a specific provision (EU AI Act
   Art. 10 bias / Art. 9 risk management) and add a DORA/CSRD materiality note. This makes the
   Fairness window a compliance-evidence generator — directly serving CSOAI's signed-h3k-card training
   fuel and neutral measurement mission.

---

## 5. Primary sources (verified)

- AIF360 README: https://github.com/Trusted-AI/AIF360 (metrics, algorithms, Apache-2.0, Python+R)
- What-If Tool: https://pair-code.github.io/what-if-tool/ + https://github.com/PAIR-code/what-if-tool
- Fairlearn: https://fairlearn.org/ + https://github.com/fairlearn/fairlearn (README.rst, MIT)
- Holistic AI: https://www.holisticai.com/ + https://www.gov.uk/ai-assurance-techniques/holistic-ai-governance-risk-and-compliance-platform
- Credo AI: https://www.credo.ai/ + https://www.credo.ai/integrations
- LatticeFlow: https://latticeflow.ai/ + Reuters EU AI Act Checker coverage (2024-10-16)
- Arthur AI: https://www.arthur.ai/
- Fiddler AI: https://www.fiddler.ai/ (Mozilla Ventures investment: blog.mozilla.org)
- TruEra: https://docs.truera.com/
- Parity AI: https://www.computerweekly.com/news/252527778 (recruitment-algorithm bias audit)

*⚠️ marks claims not fully confirmed from a primary source at time of writing; verify before reuse.*
