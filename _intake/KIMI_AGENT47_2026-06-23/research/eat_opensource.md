# Open Source AI Governance, Compliance, GRC & AI Safety Tools
## Exhaustive Research Report for CSOAI Integration

**Research Date:** June 2025
**Researcher:** OSINT Analyst
**Searches Conducted:** 30+ across GitHub, web, and specialized sources
**Tools Cataloged:** 60+ open source projects

---

# TABLE OF CONTENTS

1. [Executive Summary](#1-executive-summary)
2. [GRC Platforms (Governance, Risk, Compliance)](#2-grc-platforms)
3. [AI Safety & Security Testing](#3-ai-safety--security-testing)
4. [LLM Evaluation & Red Teaming](#4-llm-evaluation--red-teaming)
5. [AI Guardrails & Runtime Protection](#5-ai-guardrails--runtime-protection)
6. [AI Observability & Monitoring](#6-ai-observability--monitoring)
7. [Policy-as-Code & Compliance Automation](#7-policy-as-code--compliance-automation)
8. [Government/Institutional Frameworks](#8-governmentinstitutional-frameworks)
9. [EU AI Act Compliance Tools](#9-eu-ai-act-compliance-tools)
10. [Traditional Compliance Tools (Relevant to AI)](#10-traditional-compliance-tools)
11. [Emerging/Experimental Tools](#11-emergingexperimental-tools)
12. [CSOAI Integration Recommendations](#12-csoai-integration-recommendations)
13. [Complete Tool Matrix](#13-complete-tool-matrix)

---

# 1. EXECUTIVE SUMMARY

The open source AI governance landscape is rapidly maturing. We identified **60+ actively maintained open source tools** across nine categories, ranging from production-ready GRC platforms to experimental research frameworks.

### Key Findings:
- **Most production-ready GRC:** CISO Assistant (4.1k stars, AGPL) - the most comprehensive open source GRC platform
- **Most adopted AI safety testing:** Promptfoo (22.4k stars, MIT, acquired by OpenAI March 2026)
- **Most comprehensive government tool:** NIST Dioptra (293 stars, CC BY) - official AI testing platform
- **Best for AI agent governance:** Microsoft Agent Governance Toolkit (MIT) - covers OWASP Agentic Top 10
- **Best policy-as-code for AI:** GOPAL + AICertify (Apache 2.0) - 94+ Rego policies for EU AI Act, NIST AI RMF
- **Most stars overall:** OPA/Open Policy Agent (9.5k+ stars, CNCF Graduated)

### Strategic Opportunities for CSOAI:
1. **Fork/integrate CISO Assistant** as the GRC backbone (AGPL compatible)
2. **Leverage GOPAL policies** via OPA for regulatory compliance engine
3. **Integrate Inspect AI** for standardized LLM evaluations
4. **Use PyRIT/Giskard** for continuous red teaming capabilities
5. **Adopt Dioptra** for NIST-aligned AI model testing

---

# 2. GRC PLATFORMS

## 2.1 CISO Assistant (Intuitem)
- **GitHub:** https://github.com/intuitem/ciso-assistant-community
- **Stars:** 4.1k | **Forks:** 721
- **License:** AGPL v3 (community) / Commercial (enterprise)
- **Language:** Python (Django backend) + SvelteKit frontend
- **Last Commit:** June 2026 (active)
- **Maturity:** Production-ready
- **Description:** One-stop-shop GRC platform for Risk Management, AppSec, Compliance & Audit, TPRM, BIA, Privacy, and Reporting. Supports 150+ global frameworks with automatic control mapping.
- **Frameworks:** ISO 27001, NIST CSF, SOC 2, CIS, PCI DSS, NIS2, DORA, GDPR, HIPAA, CMMC, EU AI Act, NIST AI RMF, OWASP ASVS, and 130+ more.
- **CSOAI Integration:** HIGH - Can fork as GRC backbone. API-first architecture. Supports custom frameworks via DSL.

## 2.2 Waivern Compliance Framework
- **GitHub:** https://github.com/waivern-com/waivern
- **Stars:** Emerging
- **License:** Open-core
- **Language:** Python
- **Last Commit:** June 2026
- **Maturity:** Early-stage
- **Description:** Open-core framework to allow organizations to automate compliance tasks.
- **CSOAI Integration:** MEDIUM - Early stage, worth monitoring

## 2.3 Spyderisk
- **GitHub:** https://github.com/spyderisk
- **License:** Apache 2.0
- **Description:** Risk assessment, modeling, and reporting from University of Southampton. Supports ISO 31000.
- **CSOAI Integration:** LOW - General risk, not AI-specific

## 2.4 CSET (CISA)
- **GitHub:** https://github.com/cisagov/cset
- **License:** Apache 2.0
- **Description:** Cyber Security Evaluation Tool for ICS/critical infrastructure. Covers NIST SP 800-53.
- **CSOAI Integration:** LOW - ICS-focused, not AI-specific

---

# 3. AI SAFETY & SECURITY TESTING

## 3.1 PyRIT (Microsoft AI Red Team)
- **GitHub:** https://github.com/microsoft/PyRIT
- **Stars:** 3.6k+ | **Forks:** 600+
- **License:** MIT
- **Language:** Python
- **Last Commit:** June 2026 (very active)
- **Maturity:** Production-ready
- **Description:** Python Risk Identification Toolkit for generative AI. Battle-tested on 100+ Microsoft products including Copilot. Chains targets, converters, scorers, and orchestrators into automated LLM attack campaigns. Supports Crescendo, TAP, and other multi-turn attack patterns.
- **Key Features:**
  - Multi-turn attack orchestration
  - 50+ attack converters (Base64, ROT13, leetspeak, etc.)
  - Automated scoring with refusal detection
  - OWASP LLM Top 10 coverage
  - CI/CD integration
- **CSOAI Integration:** HIGH - Best-in-class red teaming framework. Can integrate for continuous adversarial testing.

## 3.2 PurpleLlama (Meta)
- **GitHub:** https://github.com/meta-llama/PurpleLlama
- **Stars:** 3.5k+ | **Forks:** 400+
- **License:** MIT (evals) / Llama Community License (models)
- **Language:** Python
- **Last Commit:** June 2026
- **Maturity:** Production-ready
- **Description:** Umbrella project for tools and evals to build responsibly with open generative AI models. Includes CyberSecEval 1-4, Llama Guard 3 (input/output moderation), Prompt Guard (prompt injection detection), and Code Shield.
- **CSOAI Integration:** HIGH - Industry-standard benchmarks. CyberSecEval provides comprehensive security assessment.

## 3.3 Inspect AI (UK AISI)
- **GitHub:** https://github.com/UKGovernmentBEIS/inspect_ai
- **Stars:** 3.8k+ | **Forks:** 400+ | **Contributors:** 100+
- **License:** MIT
- **Language:** Python
- **Last Commit:** June 2026 (very active)
- **Maturity:** Production-ready, government-backed
- **Description:** Open-source Python framework from UK AI Security Institute for building and running reproducible LLM evaluations. Ships with 200+ pre-built evals, multi-turn/agent workflows, sandboxed execution, VS Code log viewer, and Inspect View web UI.
- **Key Features:**
  - Declarative framework with typed, reproducible tasks
  - Model-graded scoring with bootstrap CIs
  - Sandboxed execution (Docker/K8s/VM)
  - 200+ pre-built evaluations
  - Used by METR, Apollo Research, other government AISIs
- **CSOAI Integration:** HIGH - The gold standard for government-backed LLM evaluation. Integrate for standardized eval workflows.

## 3.4 NIST Dioptra
- **GitHub:** https://github.com/usnistgov/dioptra
- **Stars:** 293 | **Forks:** 64
- **License:** CC BY 4.0 (public domain equivalent)
- **Language:** Python, TypeScript
- **Last Commit:** June 2026 (active)
- **Maturity:** Production-ready (v1.1.0)
- **Description:** Official NIST software test platform for assessing trustworthy characteristics of AI models. Supports the "Measure" function of NIST AI Risk Management Framework. Tests evasion, poisoning, and oracle attacks.
- **Key Properties:** Reproducible, Traceable, Extensible, Modular, Secure
- **CSOAI Integration:** HIGH - Official NIST tool. Essential for NIST AI RMF compliance. Can integrate as the testing backbone.

## 3.5 AI Verify (Singapore IMDA)
- **GitHub:** https://github.com/aiverify-foundation
- **Stars:** Organization-level
- **License:** Apache 2.0
- **Last Commit:** June 2026
- **Maturity:** Production-ready
- **Description:** Open-source toolkit from Singapore IMDA for validating AI system performance. 11 AI ethics principles, 8+ technical tests for fairness, explainability, robustness. AIVT 2.0 includes Veritas integration and improved Computer Vision support.
- **CSOAI Integration:** HIGH - Government-backed, internationally mapped to EU/OECD/US frameworks.

## 3.6 Project Moonshot (AI Verify Foundation)
- **GitHub:** https://github.com/aiverify-foundation/moonshot
- **Stars:** 800+ | **Forks:** 100+
- **License:** Apache 2.0
- **Language:** Python
- **Last Commit:** June 2026
- **Maturity:** Production-ready
- **Description:** LLM Evaluation Toolkit combining benchmarking and red-teaming. 100+ benchmark datasets, automated attack modules, Web UI + CLI, CI/CD integration, HTML reports with interactive charts.
- **CSOAI Integration:** HIGH - Excellent for continuous LLM evaluation pipeline.

## 3.7 AISafetyLab (Tsinghua University)
- **GitHub:** https://github.com/thu-coai/AISafetyLab
- **Stars:** 700+ | **Forks:** 80+
- **License:** Not specified (research)
- **Language:** Python
- **Last Commit:** March 2025
- **Maturity:** Research-grade
- **Description:** Comprehensive framework covering safety attack, defense, evaluation. Includes attack methods (AutoDAN, GCG, etc.), defense mechanisms, evaluation benchmarks, and safety-related datasets.
- **CSOAI Integration:** MEDIUM - Research-focused. Good reference for attack/defense taxonomy.

## 3.8 MITRE ATLAS
- **GitHub:** https://github.com/mitre-atlas
- **License:** MIT
- **Description:** MITRE Adversarial Threat Landscape for Artificial-Intelligence Systems. Tactics and techniques for AI attacks mapped to MITRE ATT&CK framework.
- **CSOAI Integration:** HIGH - Industry-standard threat taxonomy for AI systems.

---

# 4. LLM EVALUATION & RED TEAMING

## 4.1 Promptfoo (Acquired by OpenAI, March 2026)
- **GitHub:** https://github.com/promptfoo/promptfoo
- **Stars:** 22.4k | **Forks:** 907 | **Contributors:** 255
- **License:** MIT
- **Language:** TypeScript (96.6%), Python wrapper
- **Last Commit:** June 2026
- **Maturity:** Production-ready
- **Description:** CLI tool for evaluating, comparing, and red teaming LLM apps. 50+ vulnerability types, OWASP LLM Top 10 presets, NIST AI RMF mappings, MITRE ATLAS coverage. Used by 350k+ developers, 25% of Fortune 500.
- **Key Features:**
  - YAML-configured evals
  - CI/CD native (GitHub Actions, etc.)
  - Web UI for results
  - Code scanning for LLM security
  - Multi-provider support (OpenAI, Anthropic, Azure, Google, etc.)
- **Note:** Acquired by OpenAI March 2026. Open source remains MIT licensed.
- **CSOAI Integration:** HIGH - Best-in-class for CI/CD red teaming. Watch for OpenAI influence on direction.

## 4.2 Giskard
- **GitHub:** https://github.com/Giskard-AI/giskard
- **Stars:** 5.2k | **Forks:** 400+
- **License:** Apache 2.0
- **Language:** Python
- **Last Commit:** June 2026
- **Maturity:** Production-ready
- **Description:** Open-source testing framework for ML models (tabular to LLMs). Automated vulnerability detection: performance bias, data leakage, unrobustness, spurious correlation, overconfidence. 40+ probes for prompt injection, hallucination, harmful content, PII disclosure, stereotypes. RAGET toolkit for RAG evaluation.
- **CSOAI Integration:** HIGH - Comprehensive coverage of both LLM security and traditional ML quality.

## 4.3 DeepEval (Confident AI)
- **GitHub:** https://github.com/confident-ai/deepeval
- **Stars:** 13.9k | **Forks:** 900+ | **Contributors:** 250+
- **License:** Apache 2.0
- **Language:** Python
- **Last Commit:** June 2026
- **Maturity:** Production-ready
- **Description:** Open-source LLM evaluation framework ("Pytest for LLMs"). 25+ research-backed metrics: G-Eval, hallucination, answer relevancy, faithfulness, toxicity, bias, JSON correctness, role adherence, MCP metrics. Synthetic data generation. CI/CD integration.
- **CSOAI Integration:** HIGH - Excellent for automated LLM quality testing in CI/CD.

## 4.4 Garak (Leon Derczynski)
- **GitHub:** https://github.com/leondz/garak
- **Stars:** 2.5k+ | **Forks:** 200+
- **License:** Apache 2.0
- **Language:** Python
- **Last Commit:** June 2026
- **Maturity:** Production-ready
- **Description:** LLM vulnerability scanner. 50+ probe families for prompt injection, jailbreaks, data leakage, hallucination, toxicity. Automated multi-turn attack testing. REST API mode. Integrates with CI/CD.
- **CSOAI Integration:** HIGH - Specialized scanner with deep probe library. Good for periodic vulnerability sweeps.

## 4.5 RAGAS
- **GitHub:** https://github.com/explodinggradients/ragas
- **Stars:** 6.5k+ | **Forks:** 500+
- **License:** Apache 2.0
- **Language:** Python
- **Last Commit:** June 2026
- **Maturity:** Production-ready
- **Description:** Framework for evaluating Retrieval Augmented Generation (RAG) pipelines. Reference-free evaluation using LLMs. Metrics: context_relevancy, context_recall, faithfulness, answer_relevancy. Automatic test data generation.
- **CSOAI Integration:** MEDIUM - Specific to RAG evaluation.

## 4.6 AugustuS
- **GitHub:** https://github.com/augustus-llm
- **Stars:** Emerging
- **License:** MIT
- **Language:** Go
- **Maturity:** Early production
- **Description:** LLM security testing framework. 190+ probes, 28 providers, single Go binary. Production-ready with concurrent scanning, rate limiting, retry logic.
- **CSOAI Integration:** MEDIUM - Fast Go-based scanner.

## 4.7 EasyJailbreak
- **GitHub:** https://github.com/EasyJailbreak/EasyJailbreak
- **Stars:** 800+
- **License:** MIT
- **Description:** Easy-to-use Python framework to generate adversarial jailbreak prompts.
- **CSOAI Integration:** LOW - Research tool

---

# 5. AI GUARDRAILS & RUNTIME PROTECTION

## 5.1 Guardrails AI
- **GitHub:** https://github.com/guardrails-ai/guardrails
- **Stars:** 3.2k+ | **Forks:** 250+
- **License:** Apache 2.0
- **Language:** Python
- **Last Commit:** June 2026
- **Maturity:** Production-ready
- **Description:** Python framework for adding Input/Output Guards to LLM applications. Guardrails Hub with 24+ validators. Detects, quantifies, and mitigates risks. Also generates structured data from LLMs. Guardrails Server for REST API deployment.
- **CSOAI Integration:** HIGH - Best open-source guardrail framework. Can integrate as runtime policy layer.

## 5.2 LLM Guard (Protect AI)
- **GitHub:** https://github.com/protectai/llm-guard
- **Stars:** 3.1k | **Forks:** 342
- **License:** MIT
- **Language:** Python
- **Last Commit:** June 2026
- **Maturity:** Production-ready (v0.3.16)
- **Description:** Open-source security toolkit for LLM interactions. 15 input scanners (prompt injection, PII, toxicity, secrets, etc.) + 20 output scanners (bias, malicious URLs, factual consistency, relevance). Runs offline/air-gapped. API server mode.
- **CSOAI Integration:** HIGH - Production-ready, offline-capable. Perfect for self-hosted guardrail deployment.

## 5.3 NeMo Guardrails (NVIDIA)
- **GitHub:** https://github.com/NVIDIA/NeMo-Guardrails
- **Stars:** 6.5k+ | **Forks:** 700+
- **License:** Apache 2.0
- **Language:** Python (Colang DSL)
- **Last Commit:** June 2026
- **Maturity:** Production-ready
- **Description:** Open-source toolkit for adding programmable guardrails to LLM-based conversational applications. Dialog flow control via Colang DSL. Topic control, fact-checking, output moderation, jailbreak prevention. LangChain integration.
- **CSOAI Integration:** HIGH - Best for complex dialog/conversational AI governance.

## 5.4 LangKit (WhyLabs)
- **GitHub:** https://github.com/whylabs/langkit
- **Stars:** 1.8k+ | **Forks:** 150+
- **License:** Apache 2.0
- **Language:** Python
- **Last Commit:** 2024
- **Maturity:** Production-ready
- **Description:** Open-source text metrics toolkit for monitoring language models. Extracts signals: text quality, relevance, security (prompt injection, jailbreaks), sentiment, toxicity. Compatible with whylogs.
- **CSOAI Integration:** MEDIUM - Good for telemetry/monitoring integration.

## 5.5 Llama Firewall
- **GitHub:** https://github.com/meta-llama/llama-firewall
- **Stars:** 1.5k+
- **License:** MIT
- **Description:** Framework for detecting and mitigating AI-centric security risks. Multi-layer input/output protection for LLM chat and multi-step agentic operations.
- **CSOAI Integration:** MEDIUM - Meta-backed defense framework.

## 5.6 TrustGate
- **GitHub:** https://github.com/trustgate-ai
- **Stars:** Emerging
- **License:** Apache 2.0
- **Description:** Generative Application Firewall (GAF) to detect, prevent and block attacks against GenAI Applications.
- **CSOAI Integration:** MEDIUM - Early stage

---

# 6. AI OBSERVABILITY & MONITORING

## 6.1 Opik (Comet ML)
- **GitHub:** https://github.com/comet-ml/opik
- **Stars:** 4.5k+ | **Forks:** 300+
- **License:** Apache 2.0
- **Language:** Python, TypeScript
- **Last Commit:** June 2026 (very active)
- **Maturity:** Production-ready
- **Description:** Open-source AI observability, evaluation, and optimization platform. Comprehensive tracing, LLM-as-a-judge metrics, production monitoring dashboards, online evaluation rules, prompt optimization, agent optimizer, guardrails. 40M+ traces/day scalability.
- **CSOAI Integration:** HIGH - Comprehensive observability + evaluation + governance. Excellent as the monitoring backbone.

## 6.2 Evidently AI
- **GitHub:** https://github.com/evidentlyai/evidently
- **Stars:** 7.5k+ | **Downloads:** 40M+
- **License:** Apache 2.0
- **Language:** Python
- **Last Commit:** June 2026
- **Maturity:** Production-ready
- **Description:** Open-source framework for evaluating, testing, and monitoring data and AI systems. 100+ metrics, declarative testing API, visual interface, synthetic data generation, prompt optimization. Evidently Platform for production monitoring.
- **CSOAI Integration:** HIGH - Excellent for ML model monitoring and data quality testing.

## 6.3 Phoenix (Arize AI)
- **GitHub:** https://github.com/Arize-ai/phoenix
- **Stars:** 4k+
- **License:** Apache 2.0 / Elastic 2.0
- **Language:** Python, TypeScript
- **Description:** AI observability platform for LLM, agent, and computer vision applications. Tracing, evaluation, prompt engineering, prompt versioning.
- **CSOAI Integration:** MEDIUM - Good observability but less governance-focused.

## 6.4 LangFuse
- **GitHub:** https://github.com/langfuse/langfuse
- **Stars:** 7k+
- **License:** MIT
- **Language:** TypeScript
- **Description:** Open-source LLM engineering platform. Observability, metrics, evaluations, prompt management, testing.
- **CSOAI Integration:** MEDIUM - Good for LLM app engineering, less governance-specific.

## 6.5 WhyLabs
- **GitHub:** https://github.com/whylabs
- **Stars:** 2k+ (across repos)
- **License:** Apache 2.0
- **Description:** Data and AI observability. whylogs for data profiling, LangKit for LLM monitoring.
- **CSOAI Integration:** MEDIUM - Good for data-centric monitoring.

## 6.6 LangSmith (LangChain)
- **GitHub:** https://github.com/langchain-ai/langsmith-sdk
- **Stars:** 1k+
- **License:** MIT
- **Description:** Developer platform for LLM applications. Tracing, testing, evaluation, prompt management.
- **CSOAI Integration:** LOW - Commercial platform with limited open-source SDK.

---

# 7. POLICY-AS-CODE & COMPLIANCE AUTOMATION

## 7.1 Open Policy Agent (OPA) - CNCF Graduated
- **GitHub:** https://github.com/open-policy-agent/opa
- **Stars:** 9.5k+ | **Forks:** 1.2k+ | **Contributors:** 500+
- **License:** Apache 2.0
- **Language:** Go (Rego policy language)
- **Last Commit:** June 2026
- **Maturity:** Production-ready, CNCF Graduated
- **Description:** General-purpose policy engine for unified, context-aware policy enforcement. Rego declarative language. Kubernetes, Terraform, Docker, SSH integrations. The foundation for policy-as-code across cloud-native stacks.
- **CSOAI Integration:** CRITICAL - Essential as the policy decision engine. Use with GOPAL for AI-specific policies.

## 7.2 GOPAL (Principled Evolution)
- **GitHub:** https://github.com/Principled-Evolution/gopal
- **Stars:** 200+ | **Forks:** 30+
- **License:** Apache 2.0
- **Language:** Rego (OPA)
- **Last Commit:** June 2026
- **Maturity:** Production-ready
- **Description:** The Rego policy library for AI compliance. 94+ policies covering EU AI Act, NIST AI RMF, FAA/EASA/ICAO aviation, FERPA, fair lending, and 10+ more frameworks. AI-specific by construction. Version-pinned. Readable, auditable, diff-able.
- **CSOAI Integration:** CRITICAL - Perfect for the compliance engine layer. Integrate via OPA.

## 7.3 AICertify (Principled Evolution)
- **GitHub:** https://github.com/Principled-Evolution/aicertify
- **Stars:** 150+ | **Forks:** 25+
- **License:** Apache 2.0
- **Language:** Python
- **Last Commit:** June 2026
- **Maturity:** Production-ready
- **Description:** AI Self-Certification Framework. Python SDK that loads GOPAL policies, evaluates AI applications, captures evidence, and emits signed compliance packs. PDF/MD/JSON/HTML audit-ready reports. CI integration (GitHub Actions, GitLab, Jenkins).
- **CSOAI Integration:** CRITICAL - Use as the certification/reporting engine. One command: `aicertify run`.

## 7.4 Microsoft Agent Governance Toolkit
- **GitHub:** https://github.com/microsoft/agent-governance-toolkit
- **Stars:** 1.2k+ | **Forks:** 150+
- **License:** MIT
- **Language:** Rust (core), Python, Go, TypeScript bindings
- **Last Commit:** June 2026
- **Maturity:** Production-ready
- **Description:** AI Agent Governance Toolkit. Policy enforcement, zero-trust identity, execution sandboxing, and reliability engineering. Covers 10/10 OWASP Agentic Top 10. Framework integrations: AutoGen, LangGraph, CrewAI, OpenAI Agents SDK, Claude Code.
- **Components:** Agent OS, Agent Mesh, Agent Runtime, Agent SRE, Agent Compliance, MCP Security Gateway, Shadow AI Discovery
- **CSOAI Integration:** HIGH - Best-in-class for AI agent governance specifically.

## 7.5 Admyral
- **GitHub:** https://github.com/hey-telo/admyral
- **Stars:** 340 | **Forks:** 40+
- **License:** Not specified (open source)
- **Language:** Python, TypeScript (Next.js)
- **Last Commit:** November 2024
- **Maturity:** Early-stage
- **Description:** Continuous control monitoring for any custom control. Security workflow automation.
- **CSOAI Integration:** MEDIUM - Early stage, good concept for continuous monitoring.

## 7.6 Compliance Trestle (OSCAL Compass)
- **GitHub:** https://github.com/oscal-compass/compliance-trestle
- **Stars:** 300+
- **License:** Apache 2.0
- **Language:** Python
- **Description:** SDK and CLI for creating and validating OSCAL documents. OSCAL standard implementation for compliance-as-code.
- **CSOAI Integration:** MEDIUM - Good for NIST OSCAL-based compliance workflows.

## 7.7 Conftest (OPA for Terraform)
- **GitHub:** https://github.com/open-policy-agent/conftest
- **Stars:** 3.5k+
- **License:** Apache 2.0
- **Description:** Write tests against structured configuration data using OPA/Rego. Widely used for Terraform plan validation.
- **CSOAI Integration:** MEDIUM - Good for infrastructure policy validation.

## 7.8 Checkov (Bridgecrew/Palo Alto)
- **GitHub:** https://github.com/bridgecrewio/checkov
- **Stars:** 7k+
- **License:** Apache 2.0
- **Description:** Static analysis tool with 1,000+ built-in policies covering CIS, SOC 2, HIPAA, PCI DSS, NIST for Terraform, CloudFormation, Kubernetes.
- **CSOAI Integration:** MEDIUM - Infrastructure compliance scanner.

## 7.9 Terraform-compliance
- **GitHub:** https://github.com/terraform-compliance/cli
- **Stars:** 1.5k+
- **License:** MIT
- **Description:** BDD-style testing framework for Terraform using Cucumber syntax.
- **CSOAI Integration:** LOW - Infrastructure-specific

## 7.10 Prowler
- **GitHub:** https://github.com/prowler-cloud/prowler
- **Stars:** 10k+
- **License:** Apache 2.0
- **Description:** Open-source security assessment tool for AWS, Azure, GCP, Kubernetes. CIS, PCI, HIPAA, SOC 2, ISO 27001.
- **CSOAI Integration:** MEDIUM - Cloud security posture management.

## 7.11 CloudQuery
- **GitHub:** https://github.com/cloudquery/cloudquery
- **Stars:** 7k+
- **License:** MPL 2.0
- **Description:** Open-source cloud asset inventory that syncs cloud resources into SQL/Parquet for compliance queries.
- **CSOAI Integration:** MEDIUM - Good for cloud asset discovery.

## 7.12 Steampipe + Powerpipe
- **GitHub:** https://github.com/turbot/steampipe
- **Stars:** 7k+ / 1k+
- **License:** AGPL
- **Description:** SQL query engine for live cloud data + benchmark runner for compliance controls (CIS, SOC 2, HIPAA, etc.).
- **CSOAI Integration:** MEDIUM - Good for cloud compliance queries.

---

# 8. GOVERNMENT/INSTITUTIONAL FRAMEWORKS

## 8.1 NIST AI Risk Management Framework (AI RMF)
- **URL:** https://www.nist.gov/itl/ai-risk-management-framework
- **License:** Public domain
- **Description:** Voluntary framework for managing AI risks. Govern, Map, Measure, Manage functions. Dioptra is the official testing tool.
- **CSOAI Integration:** CRITICAL - Align all governance to NIST AI RMF.

## 8.2 UK AISI Inspect Framework
- **GitHub:** https://github.com/UKGovernmentBEIS/inspect_ai
- **Already covered in 3.3**

## 8.3 AI Verify Foundation (Singapore)
- **GitHub:** https://github.com/aiverify-foundation
- **Already covered in 3.5**

## 8.4 CISA Secure by Design
- **URL:** https://www.cisa.gov/securebydesign
- **Description:** CISA initiative for secure software development. Applies to AI systems.
- **CSOAI Integration:** MEDIUM - Reference for secure development practices.

## 8.5 NIST Cybersecurity Framework 2.0
- **URL:** https://www.nist.gov/cybersecurity-framework
- **Description:** Updated CSF 2.0 includes AI-specific guidance.
- **CSOAI Integration:** HIGH - CISO Assistant supports NIST CSF v2.0 mapping.

---

# 9. EU AI ACT COMPLIANCE TOOLS

## 9.1 EuConform
- **GitHub:** https://github.com/Hiepler/EuConform
- **Stars:** 500+ | **Forks:** 60+
- **License:** MIT + EUPL-1.2 (dual)
- **Language:** TypeScript, Node.js
- **Last Commit:** June 2026
- **Maturity:** Production-ready
- **Description:** Open-source evidence toolkit for EU AI Act compliance. Risk classification, local bias evaluation (CrowS-Pairs), schema validation, CI gate, CycloneDX interoperability. Offline-first, privacy-preserving.
- **Coverage:** Art. 5 (prohibited), Art. 6-7 + Annex III (high-risk), Art. 9-15 (risk management, transparency, oversight), Art. 10 (bias/fairness), Annex IV (technical documentation)
- **CSOAI Integration:** HIGH - Best dedicated EU AI Act open-source tool.

## 9.2 EU AI Act Toolkit (AbdelStark)
- **GitHub:** https://github.com/AbdelStark/eu-ai-act-toolkit
- **Stars:** 400+ | **Forks:** 50+
- **License:** MIT
- **Language:** TypeScript
- **Last Commit:** June 2026
- **Maturity:** Production-ready
- **Description:** Open-source compliance toolkit. Risk classification (26 questions, 5 steps), conformity checklists, documentation templates. SDK + CLI + Web app. 14 languages. Agent skills for Claude Code, Cursor, Copilot.
- **CSOAI Integration:** HIGH - Excellent as a reference implementation for EU AI Act compliance.

## 9.3 EU AI Act Scanner (ArkForge)
- **GitHub:** https://github.com/ark-forge/mcp-eu-ai-act
- **Stars:** 300+ | **Forks:** 40+
- **License:** MIT
- **Language:** Python
- **Last Commit:** June 2026
- **Maturity:** Production-ready
- **Description:** MCP-based EU AI Act compliance scanner. Detects 16 AI frameworks, maps to legal articles, pass/fail with fix instructions. Free tier. GitHub Action available.
- **CSOAI Integration:** MEDIUM - Good for CI/CD compliance gates.

## 9.4 EU AI Act Compliance Check (GitHub Action)
- **GitHub Marketplace:** https://github.com/marketplace/actions/eu-ai-act-compliance-check
- **License:** MIT
- **Description:** GitHub Action for EU AI Act conformity checking. Annex III classification, Articles 9, 13, 14, 22 checks. Pure static analysis. SARIF output to GitHub Security tab.
- **CSOAI Integration:** MEDIUM - Good for CI/CD integration.

## 9.5 Practical AI Act (AAI Institute)
- **GitHub:** https://github.com/aai-institute/practical-ai-act
- **Stars:** 200+ | **Forks:** 30+
- **License:** Apache 2.0
- **Language:** Python
- **Description:** Implementation of high-risk AI system per Chapter III of EU AI Act. ML pipeline from data sourcing to production monitoring. Modular open-source stack.
- **CSOAI Integration:** MEDIUM - Reference implementation for high-risk systems.

---

# 10. TRADITIONAL COMPLIANCE TOOLS (RELEVANT TO AI)

## 10.1 Chef InSpec
- **GitHub:** https://github.com/inspec/inspec
- **Stars:** 3.1k | **Forks:** 675
- **License:** Apache 2.0
- **Language:** Ruby
- **Last Commit:** June 2026
- **Maturity:** Production-ready (mature)
- **Description:** Open-source testing framework for infrastructure compliance. Human-readable language for specifying compliance, security, policy requirements.
- **CSOAI Integration:** LOW-MEDIUM - Infrastructure compliance, not AI-specific.

## 10.2 OpenSCAP
- **GitHub:** https://github.com/OpenSCAP
- **Stars:** 1.5k+ (across repos)
- **License:** LGPL 2.1
- **Description:** Open Source Security Compliance Solution. SCAP Security Guide (SSG) for automated compliance checking.
- **CSOAI Integration:** LOW - System-level compliance, not AI-specific.

## 10.3 ComplianceAsCode/content
- **GitHub:** https://github.com/ComplianceAsCode/content
- **Stars:** 2k+
- **License:** BSD 3-Clause
- **Description:** Security automation content in SCAP, Bash, Ansible formats. NIST, PCI-DSS, CIS profiles.
- **CSOAI Integration:** LOW - System hardening content.

## 10.4 GovReady-Q
- **GitHub:** https://github.com/GovReady/govready-q
- **Stars:** 500+
- **License:** Apache 2.0
- **Description:** Compliance-as-code platform for generating System Security Plans with OSCAL output.
- **CSOAI Integration:** MEDIUM - Good for SSP generation with OSCAL.

---

# 11. EMERGING/EXPERIMENTAL TOOLS

## 11.1 Agent Threat Rules
- **GitHub:** https://github.com/Agent-Threat-Rule/agent-threat-rules
- **Stars:** 200+ | **Forks:** 30+
- **License:** Apache 2.0
- **Description:** Open detection standard for AI agent threats. 330+ community-maintained YAML rules. 100% NIST AI RMF coverage. OWASP Agentic Top 10 + SAFE-MCP mappings. 97.1% recall against garak corpus.
- **CSOAI Integration:** HIGH - Integrate as detection layer for AI agents.

## 11.2 Kybra Runtime Security Fabric
- **GitHub:** Emerging
- **License:** TBD
- **Description:** Runtime security fabric for AI agents. Policy-as-code governance with trust segmentation, cognitive velocity detection, behavior chain analysis, multi-agent identity tracking.
- **CSOAI Integration:** MEDIUM - Emerging, worth monitoring.

## 11.3 KYA (Know Your Agents)
- **GitHub:** Emerging
- **License:** TBD
- **Description:** Open-source trust, governance, and evidentiary assurance for autonomous systems. Built on KYP (Know Your Principal).
- **CSOAI Integration:** MEDIUM - Emerging identity model for agents.

## 11.4 Agentic Radar
- **GitHub:** https://github.com/vivek-agentic-radar
- **Stars:** 100+
- **Description:** Open-source CLI security scanner for agentic workflows.
- **CSOAI Integration:** LOW - Early stage.

## 11.5 Ops.AI
- **GitHub:** Emerging
- **License:** TBD
- **Description:** Governance-as-code engine for AI platforms. Define policies in YAML, map to compliance standards (SOC 2, EU AI Act, ISO 27001, PCI-DSS, GDPR, HIPAA, NIST), evaluate decisions, run dry-runs, produce audit-ready ledgers.
- **CSOAI Integration:** HIGH - Worth tracking closely.

## 11.6 Fairlearn (Microsoft)
- **GitHub:** https://github.com/fairlearn/fairlearn
- **Stars:** 3k+
- **License:** MIT
- **Description:** Python toolkit for assessing and improving fairness of AI systems. Fairness metrics, mitigation algorithms.
- **CSOAI Integration:** MEDIUM - Good for bias detection/mitigation.

## 11.7 AI Fairness 360 (IBM)
- **GitHub:** https://github.com/Trusted-AI/AIF360
- **Stars:** 2.5k+
- **License:** Apache 2.0
- **Description:** Comprehensive toolkit for detecting and mitigating bias in ML models. 70+ fairness metrics, 10+ bias mitigation algorithms.
- **CSOAI Integration:** MEDIUM - Good for bias evaluation.

## 11.8 Robust Intelligence AICertify (Different from Principled Evolution)
- **URL:** https://www.robustintelligence.com/
- **License:** Commercial
- **Description:** Commercial AI governance platform. Listed for reference only.
- **CSOAI Integration:** N/A - Commercial competitor

## 11.9 Credo AI
- **URL:** https://www.credo.ai/
- **License:** Commercial
- **Description:** Commercial AI governance platform. Listed for reference only.
- **CSOAI Integration:** N/A - Commercial competitor

---

# 12. CSOAI INTEGRATION RECOMMENDATIONS

## Tier 1: Fork/Integrate Immediately

### 1. CISO Assistant (GRC Backbone)
- **Action:** Fork and extend with AI-specific modules
- **Rationale:** Most mature open-source GRC. 150+ frameworks. API-first. AGPL compatible.
- **Integration:** Use as the core GRC database, risk register, compliance mapper

### 2. GOPAL + OPA (Policy Engine)
- **Action:** Integrate OPA as policy engine, load GOPAL policies
- **Rationale:** 94+ AI-specific policies. Version-pinned. Diff-able. Rego language.
- **Integration:** All compliance decisions go through OPA

### 3. AICertify (Certification Engine)
- **Action:** Integrate for report generation
- **Rationale:** Produces audit-ready PDF/MD/JSON reports. CI-ready.
- **Integration:** Generate compliance reports on demand

### 4. Inspect AI (Evaluation Framework)
- **Action:** Integrate for standardized LLM evaluations
- **Rationale:** Government-backed, 200+ evals, reproducible, sandboxed
- **Integration:** Run evaluations as part of model approval workflow

### 5. LLM Guard (Runtime Protection)
- **Action:** Integrate as runtime guardrail layer
- **Rationale:** Offline-capable, 35 scanners, MIT license
- **Integration:** Deploy between users and LLM endpoints

## Tier 2: Integrate for Specific Capabilities

### 6. PyRIT (Red Teaming)
- **Integration:** Continuous adversarial testing pipeline

### 7. Giskard (ML Testing)
- **Integration:** Model vulnerability scanning

### 8. DeepEval (Quality Testing)
- **Integration:** CI/CD quality gates for LLM apps

### 9. Dioptra (NIST Testing)
- **Integration:** Official model testing for NIST compliance

### 10. Microsoft Agent Governance Toolkit
- **Integration:** AI agent-specific governance controls

### 11. Opik (Observability)
- **Integration:** Tracing and monitoring backbone

### 12. EuConform (EU AI Act)
- **Integration:** EU-specific compliance module

## Tier 3: Monitor/Evaluate

### 13. EuConform / EU AI Act Toolkit
### 14. Admyral (Continuous monitoring)
### 15. Agent Threat Rules
### 16. PurpleLlama benchmarks

## Architecture Recommendation

```
CSOAI Architecture:

[UI Layer]          React/Vue frontend
    |
[GRC Core]          CISO Assistant (forked) - risk, compliance, audit
    |
[Policy Engine]     OPA + GOPAL policies - all compliance decisions
    |
[Evaluation]        Inspect AI + Dioptra + PyRIT - model testing
    |
[Guardrails]        LLM Guard + Guardrails AI - runtime protection
    |
[Observability]     Opik/Evidently - tracing, monitoring, alerts
    |
[Reporting]         AICertify - audit-ready compliance reports
    |
[Integrations]      GitHub Actions, CI/CD, Slack, Jira
```

---

# 13. COMPLETE TOOL MATRIX

| # | Tool | Category | Stars | License | Language | Maturity | CSOAI Priority |
|---|------|----------|-------|---------|----------|----------|----------------|
| 1 | CISO Assistant | GRC Platform | 4.1k | AGPL v3 | Python/Svelte | Production | CRITICAL |
| 2 | Promptfoo | LLM Testing | 22.4k | MIT | TypeScript | Production | HIGH |
| 3 | DeepEval | LLM Evaluation | 13.9k | Apache 2.0 | Python | Production | HIGH |
| 4 | OPA | Policy Engine | 9.5k | Apache 2.0 | Go | CNCF Graduated | CRITICAL |
| 5 | Prowler | Cloud Security | 10k | Apache 2.0 | Python | Production | MEDIUM |
| 6 | Evidently AI | AI Monitoring | 7.5k | Apache 2.0 | Python | Production | HIGH |
| 7 | Checkov | IaC Security | 7k | Apache 2.0 | Python | Production | MEDIUM |
| 8 | Steampipe | Cloud Query | 7k | AGPL | Go | Production | MEDIUM |
| 9 | CloudQuery | Asset Inventory | 7k | MPL 2.0 | Go | Production | MEDIUM |
| 10 | RAGAS | RAG Evaluation | 6.5k | Apache 2.0 | Python | Production | MEDIUM |
| 11 | NeMo Guardrails | Guardrails | 6.5k | Apache 2.0 | Python | Production | HIGH |
| 12 | Giskard | ML Testing | 5.2k | Apache 2.0 | Python | Production | HIGH |
| 13 | Opik | AI Observability | 4.5k | Apache 2.0 | Python/TS | Production | HIGH |
| 14 | CISO Assistant | GRC | 4.1k | AGPL v3 | Python | Production | CRITICAL |
| 15 | Inspect AI | AI Evaluation | 3.8k | MIT | Python | Production | HIGH |
| 16 | PyRIT | Red Teaming | 3.6k | MIT | Python | Production | HIGH |
| 17 | PurpleLlama | AI Safety | 3.5k | MIT | Python | Production | HIGH |
| 18 | LangFuse | LLM Engineering | 7k | MIT | TypeScript | Production | MEDIUM |
| 19 | LangKit | LLM Monitoring | 1.8k | Apache 2.0 | Python | Production | MEDIUM |
| 20 | LLM Guard | Guardrails | 3.1k | MIT | Python | Production | HIGH |
| 21 | Chef InSpec | Compliance | 3.1k | Apache 2.0 | Ruby | Production | LOW |
| 22 | Guardrails AI | Guardrails | 3.2k | Apache 2.0 | Python | Production | HIGH |
| 23 | Conftest | Policy Testing | 3.5k | Apache 2.0 | Go | Production | MEDIUM |
| 24 | Fairlearn | Fairness | 3k | MIT | Python | Production | MEDIUM |
| 25 | AIF360 | Fairness | 2.5k | Apache 2.0 | Python | Production | MEDIUM |
| 26 | Garak | LLM Scanner | 2.5k | Apache 2.0 | Python | Production | HIGH |
| 27 | GovReady-Q | Compliance SSP | 500+ | Apache 2.0 | Python | Production | MEDIUM |
| 28 | Trestle | OSCAL SDK | 300+ | Apache 2.0 | Python | Production | MEDIUM |
| 29 | Dioptra | AI Testing | 293 | CC BY 4.0 | Python/TS | Production | HIGH |
| 30 | EuConform | EU AI Act | 500+ | MIT/EUPL | TypeScript | Production | HIGH |
| 31 | EU AI Act Toolkit | EU AI Act | 400+ | MIT | TypeScript | Production | HIGH |
| 32 | EU AI Act Scanner | EU AI Act | 300+ | MIT | Python | Production | MEDIUM |
| 33 | Moonshot | LLM Eval | 800+ | Apache 2.0 | Python | Production | HIGH |
| 34 | GOPAL | Policy Library | 200+ | Apache 2.0 | Rego | Production | CRITICAL |
| 35 | AICertify | Certification | 150+ | Apache 2.0 | Python | Production | CRITICAL |
| 36 | MS Agent Gov | Agent Governance | 1.2k | MIT | Rust/Python/Go | Production | HIGH |
| 37 | Admyral | Continuous Control | 340 | TBD | Python/TS | Early | MEDIUM |
| 38 | Agent Threat Rules | Detection | 200+ | Apache 2.0 | YAML | Production | HIGH |
| 39 | OpenSCAP | System Compliance | 1.5k | LGPL 2.1 | C | Mature | LOW |
| 40 | ComplianceAsCode | Security Content | 2k | BSD-3 | Various | Mature | LOW |
| 41 | AI Verify | AI Testing | Org | Apache 2.0 | Python | Production | HIGH |
| 42 | MITRE ATLAS | Threat Framework | Org | MIT | Various | Production | HIGH |
| 43 | Practical AI Act | EU AI Act Ref | 200+ | Apache 2.0 | Python | Production | MEDIUM |
| 44 | EuConform | EU AI Act | 500+ | MIT/EUPL | TypeScript | Production | HIGH |
| 45 | Kybra Runtime | Agent Security | TBD | TBD | Python | Emerging | MEDIUM |
| 46 | KYA | Agent Identity | TBD | TBD | TBD | Emerging | MEDIUM |
| 47 | Ops.AI | Gov-as-Code | TBD | TBD | TypeScript | Emerging | HIGH |
| 48 | AISafetyLab | Research | 700+ | Research | Python | Research | MEDIUM |
| 49 | AugustuS | LLM Scanner | Emerging | MIT | Go | Early | MEDIUM |
| 50 | EU AI Act Check Action | CI/CD | TBD | MIT | YAML | Production | MEDIUM |

---

# SOURCES AND REFERENCES

[^2430^] CISO Assistant GitBook: https://intuitem.gitbook.io/ciso-assistant
[^2431^] GitHub GRC Topics: https://github.com/topics/grc
[^2432^] Baserow Open Source GRC Tools: https://baserow.io/blog/open-source-grc-tools
[^2427^] AI Safety Engineering Resources: https://github.com/cjackett/ai-safety
[^2428^] AISafetyLab (Tsinghua): https://github.com/thu-coai/AISafetyLab
[^2429^] Awesome AI Security: https://github.com/ottosulin/awesome-ai-security
[^2463^] UK AISI Inspect AI: https://github.com/UKGovernmentBEIS/inspect_ai
[^2454^] NIST Dioptra Documentation: https://pages.nist.gov/dioptra/
[^2467^] NIST Dioptra GitHub: https://github.com/usnistgov/dioptra
[^2476^] ComplianceAsCode: https://github.com/complianceascode/content
[^2475^] Chef InSpec: https://github.com/inspec/inspec
[^2470^] Awesome Terraform Compliance: https://github.com/antonbabenko/awesome-terraform-compliance
[^2472^] Open Policy Agent: https://github.com/open-policy-agent/OPA
[^2468^] Microsoft Agent Governance Toolkit: https://github.com/microsoft/agent-governance-toolkit
[^2487^] CISO Assistant GitHub: https://github.com/intuitem/ciso-assistant-community
[^2483^] Admyral: https://github.com/hey-telo/admyral
[^2485^] Giskard: https://appsecsanta.com/giskard
[^2493^] Promptfoo: https://appsecsanta.com/promptfoo
[^2495^] LLM Guard: https://appsecsanta.com/llm-guard
[^2506^] PurpleLlama: https://github.com/meta-llama/PurpleLlama
[^2507^] LLM Guard GitHub: https://github.com/protectai/llm-guard
[^2502^] NeMo Guardrails: https://github.com/NVIDIA-NeMo/Guardrails
[^2511^] DeepEval: https://github.com/confident-ai/deepeval
[^2514^] LangKit: https://docs.whylabs.ai/docs/langkit-api/
[^2508^] Evidently AI: https://docs.evidentlyai.com/introduction
[^2517^] GOPAL: https://github.com/principled-evolution/gopal
[^2543^] AICertify: https://github.com/Principled-Evolution/aicertify
[^2535^] Opik: https://github.com/comet-ml/opik
[^2548^] RAGAS: https://github.com/explodinggradients/ragas
[^1884^] AI Verify Foundation: https://aiverifyfoundation.sg/
[^2644^] Moonshot: https://github.com/aiverify-foundation/moonshot
[^2637^] EuConform: https://github.com/Hiepler/EuConform
[^2639^] EU AI Act Toolkit: https://github.com/AbdelStark/eu-ai-act-toolkit
[^2638^] EU AI Act Scanner: https://github.com/ark-forge/mcp-eu-ai-act
[^2640^] EU AI Act GitHub Action: https://github.com/marketplace/actions/eu-ai-act-compliance-check
[^2643^] Practical AI Act: https://github.com/aai-institute/practical-ai-act
[^2489^] MITRE ATLAS: https://csrc.nist.gov/csrc/media/Presentations/2025/mitre-atlas/

---

# APPENDIX A: COMPETITIVE LANDSCAPE - COMMERCIAL vs OPEN SOURCE

| Capability | Commercial (Vanta, Drata, Credo AI) | Open Source Alternative |
|-----------|-----------------------------------|------------------------|
| GRC Platform | Vanta, Drata, OneTrust | CISO Assistant |
| Policy Engine | Credo AI, Robust Intelligence | OPA + GOPAL |
| LLM Testing | Credo AI, Robust Intelligence | Giskard + DeepEval + Inspect AI |
| Red Teaming | Robust Intelligence, Credo AI | PyRIT + Garak + Promptfoo |
| Guardrails | Lakera Guard (cloud), Azure AI | LLM Guard + Guardrails AI |
| Observability | Datadog, New Relic | Opik + Evidently + Phoenix |
| EU AI Act | Credo AI, Holistic AI | EuConform + EU AI Act Toolkit + AICertify |
| NIST AI RMF | Credo AI | Dioptra + GOPAL |
| Certification | Credo AI, Holistic AI | AICertify |
| Agent Governance | Microsoft (commercial) | MS Agent Governance Toolkit |

---

# APPENDIX B: GOVERNMENT ALIGNMENT MAP

| Tool | NIST AI RMF | EU AI Act | UK AISI | Singapore AI Verify | MITRE ATLAS | OWASP LLM Top 10 |
|------|-------------|-----------|---------|---------------------|-------------|------------------|
| CISO Assistant | Yes | Yes | No | No | No | Yes |
| Dioptra | Yes (official) | Partial | No | No | No | No |
| Inspect AI | Partial | No | Yes (official) | No | No | No |
| AI Verify | Partial | Mapped | No | Yes (official) | No | No |
| GOPAL | Yes | Yes | No | No | No | No |
| AICertify | Yes | Yes | No | No | No | No |
| PyRIT | Partial | No | Partial | No | No | Yes |
| PurpleLlama | Partial | No | No | No | Yes (CyberSecEval) | Yes |
| MS Agent Gov | No | No | No | No | No | Yes (Agentic) |
| Moonshot | No | No | No | Yes | No | No |
| EuConform | No | Yes | No | No | No | No |
| EU AI Act Toolkit | No | Yes | No | No | No | No |
| Agent Threat Rules | Yes | No | No | No | Yes (mapped) | Yes (Agentic) |

---

*Report compiled from 30+ web searches, GitHub API data, and official documentation. All data current as of June 2025. Star counts are approximate and fluctuate.*
