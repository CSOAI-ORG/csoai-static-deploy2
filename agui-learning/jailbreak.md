# GSPC — JAILBREAK Axis: Top 10 Competitor/Peer Research

**Prepared for:** CSOAI (Council of AI) — AG UI Jailbreak chat window
**Axis:** `jailbreak` (jail-break / refusal-safety measurement — jail banks, prompt-injection testing)
**Date:** 2026-08-21
**Method:** `web_search` + `curl` (live HTTP + GitHub API verification). No accounts created, no submissions made.
**Honesty policy:** verified claims only. Each row below was confirmed live (HTTP 200 / repo metadata / rendered site title) unless explicitly flagged.

---

## 0. Verification summary (all candidates checked)

| # | Candidate | Exists & current? | Evidence (checked 2026-08-21) |
|---|---|---|---|
| 1 | NVIDIA **garak** | ✅ Yes — active | `github.com/NVIDIA/garak` HTTP 200, ★8,885, last push 2026-08-19 |
| 2 | Microsoft **PyRIT** | ✅ Yes — active | `github.com/microsoft/PyRIT` HTTP 200 (canonical; `Azure/PyRIT` redirects) |
| 3 | **Giskard** | ✅ Yes — active | `github.com/Giskard-AI/giskard` → `giskard-oss`, HTTP 200 |
| 4 | **promptfoo** (red-team) | ✅ Yes — active | `github.com/promptfoo/promptfoo` + `promptfoo.dev` HTTP 200. **Now part of OpenAI.** |
| 5 | **Lakera Guard** | ✅ Yes — active | `lakera.ai` HTTP 200 |
| 6 | **Robust Intelligence** | ✅ Yes — **now Cisco AI Defense** | `cisco.com` AI Defense page + `robustintelligence` redirect |
| 7 | **Adversa AI** | ✅ Yes — active | `adversa.ai` HTTP 200 |
| 8 | **HiddenLayer** | ✅ Yes — active | `hiddenlayer.com` + `docs.hiddenlayer.ai` HTTP 200 |
| 9 | UK AISI **Inspect** | ✅ Yes — active | `inspect.aisi.org.uk` HTTP 200 |
| 10 | **DecodingTrust** (RobustQA) | ✅ Yes — benchmark | `github.com/AI-secure/DecodingTrust` HTTP 200 |
| L1 | **StrongREJECT** | ✅ Yes | `github.com/alexandrasouly/strongreject` HTTP 200 (+ `dsbowen/strong_reject` reimpl) |
| L2 | **HarmBench** | ✅ Yes | `github.com/centerforaisafety/HarmBench` HTTP 200 |
| L3 | **JailbreakBench** | ✅ Yes — benchmark | `github.com/JailbreakBench/jailbreakbench` HTTP 200, ★655 |
| A | **asisecurity.ai** | ✅ Yes — **real, but in-estate** | `asisecurity.ai` HTTP 200; site links `csoai.org`, `os.meok.ai`, `proofof.ai` (see §4) |

---

## 1. The 10-competitor table

| # | Competitor | (1) What it does | (2) User flow | (3) Docs | (4) Software shape | (5) ONE thing CSOAI should adopt |
|---|---|---|---|---|---|---|
| 1 | **garak** (NVIDIA) — "the LLM vulnerability scanner" | Open-source LLM vulnerability scanner. Enumerates attacks as **plugins called "probes"** (jailbreaks incl. encoding/DAN-style, prompt injection, etc.) with paired **detectors** that flag failures/refusals. ★8,885. | CLI: `pip install garak` → point at target (HuggingFace, local, REST, or commercial API via litellm) → `garak --probes ...` → emits structured hitlog JSON + HTML/PDF report. | `docs.garak.ai` + extensive GitHub wiki | Python package (PyPI) + CLI; probe/detector/generator/buff plugin architecture; standalone or library. | **Probe + detector plugin model**: expose every jailbreak as a named "probe" with a pass/fail detector, run an entire bank in one click, return a structured hitlog. |
| 2 | **PyRIT** (Microsoft) — "Python Risk Identification Tool" | Open-source generative-AI red-teaming framework. Orchestrates **multi-turn attack campaigns**, with converters (obfuscation), prompt targets, and **scoring engines** to classify responses (jailbreak, prompt injection, etc.). | `pip install pyrit` → author an orchestration script/notebook → define target + prompts + scorers → run async → results to memory/DB + report dashboard. | `learn.microsoft.com` security docs + GitHub README + bundled notebooks | Python library + CLI; notebook-driven orchestration; Azure/cloud + local target connectors; MIT. | **Multi-turn campaign orchestrator + scorer engine**: let the chat run a jailbreak as attacker/model/defender turns with per-turn auto-scored refusal. |
| 3 | **Giskard** | Open-source evaluation & testing library for LLM **agents**; ships an LLM vulnerability scanner for dynamic multi-turn red-teaming ("rainbow"-style attack sweeps: jailbreak, prompt injection, etc.). | `pip install giskard` → wrap model/agent → `giskard.scan(model)` runs a batch of attacks → returns issues with severity; optional hosted Hub for collaboration. | `docs.giskard.ai` (OSS + Hub) | Python library (Apache-2.0) + optional SaaS Hub; `scan()` engine. | **`scan()` "rainbow" sweep**: run many jailbreak vectors concurrently against the target and return a **ranked severity issue list** straight into the chat. |
| 4 | **promptfoo** | Declarative LLM eval + red-teaming/pentesting. **Red-team mode** auto-generates adversarial probes (jailbreaks, prompt injection, harmful content) from declarative YAML strategies/plugins. **Now part of OpenAI.** | `npx promptfoo init` → write `promptfooconfig.yaml` (targets + `redteam` strategies/plugins) → `promptfoo redteam run` → HTML report + CLI; CI/CD native. | `promptfoo.dev/docs/red-team` (open, extensive) | Node/TypeScript CLI + npm package; YAML declarative config; open-source core + optional cloud. | **Declarative red-team config + named strategy sets**: a "red team run" button in the AG UI that runs a chosen strategy set (jailbreaks) and returns a pass/fail report. |
| 5 | **Lakera Guard** | AI security platform; **Guard** is a real-time **prompt-injection / jailbreak / moderation detection API** classifying prompt & response risk per category. Also **Lakera Red** (red-teaming) and the Gandalf jailbreak challenge. | POST prompt/response to Guard API (REST / Python / JS SDK) → per-category risk scores + verdict → enforce block/flag in app; interactive playground. | `platform.lakera.ai` docs (full API reference) | SaaS API + SDKs + framework integrations (LangChain etc.); hosted closed model. | **Real-time inline verdict band**: show a live per-message jailbreak/injection risk score *as the operator types/tests*, not only after a run. |
| 6 | **Robust Intelligence** (now **Cisco AI Defense**) | End-to-end AI risk/security platform: **automated red-teaming** (AI stress testing) + an **AI Firewall** (runtime guardrail proxy). Acquired by Cisco and folded into **Cisco AI Defense**. | Enterprise SaaS — connect model endpoint → run AI stress tests / continuous validation → dashboard of risks; deploy AI Firewall as runtime proxy. | `cisco.com` AI Defense docs (formerly `docs.robustintelligence.com`) | Proprietary SaaS + on-prem; SDK/API; firewall proxy component. | **Test-now + deploy-guardrail duality**: offer both "run jail-bank now" and "turn result into a runtime guardrail" from the same window. |
| 7 | **Adversa AI** | **Continuous** AI red-teaming platform for agentic AI: automated adversarial testing (jailbreak/refusal, prompt injection, adversarial examples). KupperKollege "Innovation Leader" in Generative AI Defense Compass. | Enterprise platform — define model/use-case → automated red-team **campaigns** → threat modeling + risk reports → remediation guidance. | `adversa.ai` (blog/resources) + OECD catalogue listing | Proprietary SaaS (agentic red-team engine); some open research. | **"Continuous campaign" framing**: recurring, scheduled jail-bank sweeps with drift tracking, not one-off tests. |
| 8 | **HiddenLayer** | AI security platform (**AISec**) with **Automated Red Teaming (ART)** for AI; focuses on adversarial ML, model theft, and ML-specific threats; holds patents in AI security. | Enterprise — deploy sensor / connect models → ART runs adversarial + jailbreak scenarios → findings in platform dashboard → integrate. | `docs.hiddenlayer.ai` | Proprietary SaaS + on-prem appliance/agents; API. | **Normalized threat taxonomy + severity**: adopt a standard adversarial/jailbreak/abuse category + severity label in the chat output. |
| 9 | **UK AISI — Inspect** | Open-source LLM evaluation framework by the UK AI Safety Institute; **safeguards evals bundle jailbreak scorers** (a StrongREJECT scorer ships in `inspect_evals`). Government-grade model-safety evaluation. | `pip install inspect-ai` → define eval (tasks + dataset + scorers) → `inspect eval` → `inspect view` local log viewer; evals are Python packages. | `inspect.aisi.org.uk` (extensive) + `inspect_evals` registry | Python framework + CLI + local log viewer; Apache-2.0; scorers as pluggable components. | **Scorer layer**: adopt StrongREJECT-style rubric scorers (refusal vs. harmful-compliance) as the grading engine behind jailbreak results. |
| 10 | **DecodingTrust** (RobustQA) | Academic benchmark from the RobustQA team (AI-secure): comprehensive **trustworthiness assessment of GPT models across 8 dimensions** incl. jailbreaking, prompt injection, adversarial robustness. | Research code — clone repo → run adversarial/jailbreak attack scripts + evaluation datasets → compute per-dimension trustworthiness scores. | GitHub README + paper (arXiv 2306.11698) + `decodingtrust.github.io` | Python research codebase + datasets; academic. | **Dimension-based scoring**: map the GSPC jailbreak axis to sub-dimensions (jailbreak / prompt-injection / adversarial robustness) and report a per-dimension score. |

---

## 2. The eval-leaderboard angle (measurement instruments, not platforms)

These three are what the platforms *use as their yardstick* — directly relevant because CSOAI's GSPC is itself a measurement instrument. **Adopt their metrics as the AG UI's scoring substrate.**

| Benchmark | What it is | Why it matters to CSOAI |
|---|---|---|
| **StrongREJECT** (`github.com/alexandrasouly/strongreject`) | Jailbreak evaluation rubric + dataset with an **auto-grader** that classifies each response as *refusal* vs. *compliant-and-harmful*; high agreement with human raters. Also ships as an Inspect scorer (`strong_reject/scorer.py`). | Gives the AG UI a **defensible auto-scorer** for "did the model refuse or comply?" — the core of jailbreak/refusal measurement. |
| **HarmBench** (`github.com/centerforaisafety/HarmBench`) | Standardized evaluation framework for automated red teaming + robust refusal; 400+ behaviors, 18 attack methods, 30+ LLMs; leaderboard. | Supplies a ready **jail-bank taxonomy** (attack methods + behavior categories) CSOAI can curate into the chat's jail banks. |
| **JailbreakBench** (`github.com/JailbreakBench/jailbreakbench`, ★655) | Open robustness benchmark for jailbreaking (NeurIPS 2024); standardizes attacks & defenses with an **Attack Success Rate (ASR)** leaderboard + pipeline for new attacks/defenses. | The **ASR leaderboard pattern** is the format CSOAI should publish: per-model ASR across attacks, signed. |

---

## 3. What CSOAI should adopt — 5 concrete improvements for the AG UI Jailbreak chat window

1. **Run the jail banks from chat.** Add a "Run jail bank" action in the chat window that executes curated banks — garak probes, HarmBench behaviors, JailbreakBench attacks — against a selected target, then renders the structured hitlog/report inline (garak's probe/detector + hitlog model is the reference). No separate CLI.

2. **asisecurity checks (signed evidence).** Wire every jailbreak run into the estate's Ed25519 sign/verify backbone (`os.meok.ai/api/sign` + `/api/verify`, referenced live by asisecurity.ai) so each run yields a **signed, verifiable evidence pack** — a *living attestation*, never a certification. The AG UI chat should emit a verify link + signature alongside every result.

3. **Rainbow tests (multi-vector sweep).** Adopt Giskard's `scan()`-style concurrent attack sweep plus PyRIT's multi-turn orchestration: run **N jailbreak vectors simultaneously** against the target and return a **ranked severity issue list** (worst-first), not a single pass/fail. This is the "rainbow" the operator wants to see at a glance.

4. **The sandbox (hard isolation).** Run all jail banks and probes in an **isolated sandbox** so a probe can never hit a production endpoint or exfiltrate data. Isolation is a first-class safety property of the chat window — the operator must be able to run the most hostile prompt-injection banks with confidence that the only target is the sandboxed model.

5. **StrongREJECT-style rubric auto-scoring + signed ASR leaderboard.** Use StrongREJECT/Inspect scorers to auto-grade each response as *refusal* vs. *harmful-compliance*, compute **Attack Success Rate (ASR)** per model/attack (JailbreakBench pattern), and publish signed leaderboard entries — turning one-off jailbreak chats into a continuously accumulating, verifiable measurement record.

---

## 4. asisecurity.ai — real, but not an external competitor

`asisecurity.ai` **is real and live** (HTTP 200; site header "Pre-deployment security evidence for frontier AI"; self-dated "verified live 2 August 2026"). It describes **frontier red-teaming (adversarial, jailbreak, exfiltration), a threat-model builder, and signed hardening-evidence packs**, with an Ed25519 sign/verify API.

**Honesty flag:** its "trust spine" links directly to the CSOAI estate — `csoai.org/gspc-arena`, `os.meok.ai/api/sign`, `proofof.ai`, `safetyof.pages.dev`, `agisafe.pages.dev`. That is, it is an **in-estate peer surface** (the GSPC/attestation family), *not* an independent external competitor. It should be treated as a **reference for how CSOAI itself packages jailbreak evidence** (item 2 above), not benchmarked as a third party.

---

## Sources (primary)

- garak — https://github.com/NVIDIA/garak · https://docs.garak.ai
- PyRIT — https://github.com/microsoft/PyRIT
- Giskard — https://github.com/Giskard-AI/giskard-oss · https://docs.giskard.ai
- promptfoo — https://github.com/promptfoo/promptfoo · https://www.promptfoo.dev/docs/red-team/ (now part of OpenAI)
- Lakera — https://www.lakera.ai/
- Cisco AI Defense (Robust Intelligence) — https://www.cisco.com/site/us/en/products/security/ai-defense/robust-intelligence-is-part-of-cisco/index.html
- Adversa — https://adversa.ai/ai-red-teaming-agentic-ai/
- HiddenLayer — https://docs.hiddenlayer.ai/ · https://www.hiddenlayer.com/
- UK AISI Inspect — https://inspect.aisi.org.uk/ · https://github.com/UKGovernmentBEIS/inspect_ai
- DecodingTrust — https://github.com/AI-secure/DecodingTrust (arXiv 2306.11698)
- StrongREJECT — https://github.com/alexandrasouly/strongreject
- HarmBench — https://github.com/centerforaisafety/HarmBench
- JailbreakBench — https://github.com/JailbreakBench/jailbreakbench (NeurIPS 2024)
- asisecurity.ai — https://asisecurity.ai/ (in-estate surface)
