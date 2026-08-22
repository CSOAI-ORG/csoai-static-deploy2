# GSPC SAFETY Axis — Top 10 Competitor/Peer Research

**Prepared for:** Council of AI (CSOAI) — neutral AI-governance measurement body
**Axis:** SAFETY (jailbreak / refusal / security-safety — asisecurity.ai, rainbow testing, jail banks, sandboxes)
**Date:** 2026-08-21 · **Researcher lane:** JEEVES (delegated subagent)

**Honesty ledger (read first):** Every claim below was checked against a live source (curl of the vendor site / GitHub README / PyPI / docs) or a web-search source snapshot on the research date. Claims I could **not** independently verify are marked `⚠ unverified` or `⚠ vendor claim`. No accounts were created and no submissions were made. Two search queries ("rainbow testing" and "asisecurity.ai") timed out once; both were re-verified by direct curl of the underlying pages, so they are marked verified below where noted.

---

## 1. The 10-competitor table

| # | Name | What it does | User flow | Docs / onboarding | Software shape | ONE idea for CSOAI's AG Safety window |
|---|------|--------------|-----------|-------------------|----------------|----------------------------------------|
| 1 | **garak** (NVIDIA) | Open-source **LLM vulnerability scanner** — probes hallucination, data leakage, prompt injection, misinformation, toxicity, jailbreaks. "nmap / Metasploit for LLMs." | `pip install garak` → `garak --model_type ... --probes ...` → pass/fail report per probe category. | `docs.garak.ai`; README on GitHub `NVIDIA/garak`; PyPI `garak` (v0.16.0 verified). | Python CLI + library. Apache-2.0. Static + dynamic + **adaptive** probes; plugin architecture (attack/defense). | **Adopt its probe taxonomy + `trigger/detector` structure** — label *why* a response failed (which probe category), like nmap output, instead of a flat pass/fail. |
| 2 | **PyRIT** (Microsoft) | Open-source **AI red-teaming framework** ("Python Risk Identification Tool for generative AI") — orchestrates attacks, scores, and stores results. | `pip install pyrit` → compose orchestrator (attack strategy → converter → target → scorer) → notebook or CLI campaign → scored DB. | `microsoft.github.io/PyRIT`; GitHub `microsoft/PyRIT`; CITATION.cff. Docs 1.0.1+. | Python framework. MIT license. Notebook + Azure AI Foundry integration. Memory/DB of all conversations. | **Adopt its orchestrator + persistent memory model** — every probe in the Safety window is *scored and persisted* to a ledger (feeds our living DB → `sim_emit_card`), not just shown. |
| 3 | **AILuminate** (MLCommons) | **Standardized LLM safety benchmark + public leaderboard** — grades models on a set of hazard categories with a 5-point scale; now multimodal + jailbreak + agentic workstreams. | Submit model → benchmark run against (mostly non-public) hazard prompt sets → receive per-hazard safety grade → leaderboard. | `mlcommons.org/ailuminate/` (verified: 59,624 test prompts, 477 test images, 109 models, 12 hazard categories). Demo dataset is public; live set is held back to prevent contamination. | Benchmark harness + public leaderboard; Creative-Commons demo prompt dataset on GitHub. | **Adopt its 5-point grade scale + hazard taxonomy** so the Safety window shows a standardized safety *grade badge* per hazard, plus its "hold the live set private to prevent contamination" discipline. |
| 4 | **promptfoo** | Open-source **LLM eval + red-teaming** framework — declarative YAML config, jailbreak/prompt-injection strategies, guardrails, CI/CD. | Write `promptfooconfig.yaml` (targets + strategies + assertions) → `npx promptfoo redteam run` → pass/fail + mitigation report. | `promptfoo.dev/docs/red-team/`; GitHub `promptfoo/promptfoo`. Vendor labels itself "part of OpenAI" (`⚠ vendor claim`). | Node/CLI. MIT core. Plugins, strategies, frameworks, MCP proxy, code scanning. | **Adopt its declarative "redteam config" + named attack strategies** — let the Safety window load a JSON attack plan and run named strategies (jailbreak, prompt-injection, RAG leakage) with assertions, CI-style. |
| 5 | **Lakera** | Commercial **AI security platform**: Lakera **Guard** (real-time prompt-injection/jailbreak detection) + **Red** (red teaming) + workforce/agent security. | Sign up → get API key → wrap LLM calls (`lakera_guard` endpoint) → get real-time risk verdict per prompt → optional Red engagements. | `lakera.ai` + docs (verified). Slack "Momentum" community. | SaaS API + SDK + self-hosted option. Known for the public "Gandalf" prompt-injection game. `⚠ vendor claims`: "sub-50 ms" latency, "1M+ hackers", "100+ languages". | **Adopt the inline refusal-score UI** — show a live per-prompt verdict with *category confidence* (prompt-injection vs jailbreak vs safe) and a reason, like Lakera Guard's classify output. |
| 6 | **Protect AI** → **Prisma AIRS (Palo Alto Networks)** | AI security platform: **Guardian** (model scanning) + **Recon** (red teaming) + open-source `llm-guard`. **Verified change:** `protectai.com` now redirects to Palo Alto's "Prisma AIRS" platform; `protectai/llm-guard` README states the project is **ARCHIVED**. | Scan models/registry for malicious/backdoored weights (Guardian) → run automated red-team (Recon) → runtime AI firewall. | `protectai.com` (now Prisma AIRS); GitHub `protectai`; archived `protectai/llm-guard` docs + HF playground. | SaaS + SDK + AWS toolkit + archived OSS. | **Adopt a "scan before you probe" preflight** — run a model/registry integrity scan (backdoored-weight / malicious-dependency signal) and show it *before* the jail-bank probe results. |
| 7 | **Adversa AI** | Commercial **continuous AI red-teaming platform** for LLM + agentic AI; publishes the **AIRQ** AI Risk Quadrant (rates enterprise agents). | Book demo / onboard target → autonomous engine probes full AI stack → vulnerability report + remediation playbooks. | `adversa.ai` (verified). Claims `⚠ vendor claim`: "300+ attack techniques", "40+ threat groups", "100% OWASP LLM Top 10 coverage", "<4 hrs to break a frontier model". | SaaS platform + services. | **Adopt attack-technique → framework mapping** — tag every jail-bank prompt with its OWASP LLM Top 10 / MITRE ATLAS technique so results are traceable to a governance framework (essential for a *measurement* body). |
| 8 | **HiddenLayer** | Commercial **AISec Platform**: AI discovery (shadow AI), AI attack simulation, AI supply-chain security, AI runtime security, model scanner. | Deploy agent/scanner → discover AI assets → run attack simulation → model scan (malicious/backdoored) → runtime detection. | `hiddenlayer.com` (verified); also on Microsoft + OECD catalogues; Model Scanner on MS Marketplace. | SaaS platform (Webflow-based site). | **Adopt the "attack simulation" framing** — a continuous, automated adversarial-run view (not one-off), plus a provenance/supply-chain check before trusting a model's safety score. |
| 9 | **Giskard** | Open-source **eval + red-teaming + test generation for agentic systems**; automatic **LLM vulnerability scanner** (`giskard-scan`). | `pip install "giskard[scan]"` → wrap model → run scan → categorized vulnerability report (hallucination, prompt injection, etc.). | `docs.giskard.ai`; GitHub `Giskard-AI/giskard-oss` (verified: v3 rewrite, async-first, v2 deprecated). | Python library + Giskard Hub (collab). Apache-2.0. | **Adopt the one-click "scan → severity report" UX** — a single action that returns categorized vulnerabilities with severity levels, the way Giskard's scan report is structured. |
| 10 | **NeMo Guardrails** (NVIDIA) | Open-source **programmable guardrails** toolkit — sits between app and LLM and enforces **rails** (input/output/dialog/retrieval/execution) via the **Colang** DSL. | `pip install nemoguardrails` → define `config.yml` + Colang flows → wrap the app (SDK or server) → rejected input gets a safe-alternative response. | `docs.nvidia.com/nemo/guardrails` (verified architecture doc: layers = integration / config / runtime / external). | Python SDK + server. Apache-2.0. | **Adopt the "which rail caught it" view** — visualize input-rail vs output-rail vs retrieval-rail so the user sees *where* the guard triggered, not just that it blocked. |

---

## 2. Supplementary findings (dead / adjacent / technique)

**Robust Intelligence — absorbed, effectively dead (flag, do not copy).**
- Founded 2019 for adversarial/ML security; known for "Algorithmic AI Red Teaming" + "AI Firewall" runtime protection. **Acquired by Cisco** (2024, widely reported).
- `robustintelligence.com` returned an **empty body on curl** on 2026-08-21 → `⚠ unverified live status`. Treat as absorbed into Cisco security; no active standalone product to learn from. Do not list as a live peer.

**Guardrails AI (validation framework) — adjacent, less red-team.**
- Open-source "adding guardrails to LLMs" — RAIL spec (Reliable AI markup language) + validators + structured output guarantees (`guardrails-ai` on PyPI, GitHub `guardrails-ai/guardrails`). A sibling package `openai-guardrails` exists. Focus is **output schema/validation**, not jailbreak probing — useful as a *validator* idea, weaker as a *safety-measurement* peer.

**Rainbow Teaming — a *technique* to adopt, not a company (verified).**
- NeurIPS 2024 paper: *"Rainbow Teaming: Open-Ended Generation of Diverse Adversarial Prompts"* (Samvelyan et al., incl. Foerster & Raileanu — Meta context). Casts adversarial-prompt generation as a **quality-diversity** open-ended search that yields a *diverse* set of effective prompts (the "rainbow") without human-crafted red-team datasets. Verified from the abstract: **>90% attack success rate** across Llama 2/3, high transferability, and fine-tuning on the synthetic prompts *improves* model safety without hurting helpfulness. This is the conceptual basis for much of Meta's Purple Llama / CyberSecEval red-teaming work. **Directly relevant to the "rainbow tests" ask.**

**asisecurity.ai — our own reference surface (verified, not a competitor).**
- `asisecurity.ai` is a CSOAI/MEOK surface: *"Pre-deployment security evidence for frontier AI"* — red-team results, threat-model builder, hardening evidence, all packaged as **signed Ed25519 evidence packs** ("trust spine"). Exposes MCP tools (`asisecurity-mcp.redteam`, `ai-incident-reporting-mcp.report`) and a free sign/verify API (`os.meok.ai/api/sign` + `/verify`, roundtrip-verified 2026-08-02). Its `agent.json` explicitly states the discipline: *"Reports measured results and signed attestations only — never certifications or accreditations."* This is the phrasing + signing pattern the Safety window should already inherit; treat it as the target UX to converge on, not an external competitor.

---

## 3. What CSOAI should adopt — 5 concrete Safety-chat-window improvements

**Map of the four asks → the five moves below:**

| Ask | Covered by |
|-----|-----------|
| Jail-bank queries | Move 1 |
| asisecurity checks | Move 2 |
| Rainbow tests | Move 3 |
| Sandbox runs | Move 4 |
| (fifth: standardize + visualize) | Move 5 |

### Move 1 — Embed a queryable **jail bank** with a standard attack taxonomy
- Load a canonical prompt bank organized by **garak-style probe categories × AILuminate hazard categories × OWASP LLM Top 10 / MITRE ATLAS technique** (borrow garak's probe list, AILuminate's hazard set, Adversa's technique-mapping idea).
- Safety window gains a **"Run jail-bank probe"** action: pick category → batch-fire N canonical prompts at the target → return per-category **pass/fail + which trigger fired + mapped framework ID**.
- Persist every run into the living DB so it feeds `sim_emit_card` (PyRIT's "score everything + keep a memory DB" model).

### Move 2 — Sign every Safety result as an **asisecurity evidence pack**
- After each probe/scan, package the result as a **signed Ed25519 evidence pack** via the `os.meok.ai/api/sign` backbone (the asisecurity.ai "trust spine" pattern) — not a raw chat transcript.
- Show a **"measured result · signed attestation · never a certification"** badge on every output (copy the exact `agent.json` wording; it's already our own, verified, honest discipline).
- Expose the same actions as MCP (`asisecurity-mcp.redteam`) so the window and any A2A client hit one path.

### Move 3 — Add **rainbow-teaming** open-ended probe generation
- Don't rely only on fixed jail-bank lists: add a **quality-diversity generator** (the NeurIPS-2024 Rainbow Teaming method) that auto-produces a *diverse, effective* batch of adversarial prompts against the target, scored by attack-success rate.
- Surface as **"Generate N diverse probes"** with the diversity/ASR stats reported — this is the single highest-leverage technique to copy, and it *improves* (rather than contaminates) safety measurement when used to also fine-tune.
- `⚠ note`: implement as research-grade, deterministic/seedable, and signed (consistent with our measurement-not-certification posture).

### Move 4 — Add a one-click **sandboxed probe runner**
- A **"Run sandbox scan"** action that executes a Giskard-`giskard-scan`-style + garak/PyRIT/promptfoo-style probe suite in an **isolated subprocess/container**, returns a **categorized vulnerability + severity report** (hallucination / prompt-injection / leakage / toxicity), and never touches the main process.
- Precede it with a **Protect-AI/Guardian-style preflight** (model/registry integrity, backdoored-weight signal) so results carry a "scanned first" provenance line (HiddenLayer's supply-chain angle).

### Move 5 — Standardize scoring + visualize *where* the guard fired
- Adopt **AILuminate's 5-point safety grade scale** (Poor → Excellent) per hazard as the window's score badge, so results are comparable and leaderboard-able.
- Adopt **NeMo Guardrails' rail view**: show *which rail* caught the issue (input / output / retrieval / execution) with a safe-alternative response, and keep **Lakera-style category confidence** (injection vs jailbreak vs safe) as the inline verdict.
- Result: the Safety window reads as *measurement instrument + guardrail observability*, not a black-box "blocked/not blocked" toggle.

---

## 4. Sources (verified on 2026-08-21)

- garak: `https://github.com/NVIDIA/garak` · `https://pypi.org/pypi/garak` (v0.16.0) — LLM vulnerability scanner, Apache-2.0.
- PyRIT: `https://microsoft.github.io/PyRIT/` · `https://github.com/microsoft/PyRIT` — Python Risk Identification Tool for generative AI.
- AILuminate: `https://mlcommons.org/ailuminate/` · `https://mlcommons.org/2024/12/mlcommons-ailuminate-v1-0-release/` · `https://mlcommons.org/2025/01/ailuminate-demo-benchmark-prompt-dataset/` — 12 hazard categories, 59,624 prompts, 109 models, public demo dataset vs held-back live set.
- promptfoo: `https://www.promptfoo.dev/docs/red-team/` · `https://github.com/promptfoo/promptfoo`.
- Lakera: `https://www.lakera.ai/` — Guard (real-time) + Red; sub-50 ms / 1M+ hackers are `⚠ vendor claims`.
- Protect AI → Prisma AIRS: `https://protectai.com/` (redirects to Palo Alto Prisma AIRS) · `https://github.com/protectai/llm-guard` (ARCHIVED).
- Adversa AI: `https://adversa.ai/ai-red-teaming-agentic-ai/` — 300+ techniques / 40+ threat groups / OWASP coverage are `⚠ vendor claims`.
- HiddenLayer: `https://www.hiddenlayer.com/` — AISec Platform (discovery / attack simulation / supply chain / runtime / model scanner).
- Giskard: `https://github.com/Giskard-AI/giskard-oss` — v3 "Evals, Red Teaming and Test Generation for Agentic Systems"; `giskard-scan` beta.
- NeMo Guardrails: `https://docs.nvidia.com/nemo/guardrails/about-nemo-guardrails-library/how-it-works.md` — Colang DSL, layered rails.
- Rainbow Teaming: `https://mlanthology.org/neurips/2024/samvelyan2024neurips-rainbow/` — NeurIPS 2024, quality-diversity adversarial prompt generation, >90% ASR.
- Robust Intelligence: `https://www.robustintelligence.com/` (empty body on curl → `⚠ unverified live status`); Cisco acquisition (2024, widely reported).
- Guardrails AI: `https://github.com/guardrails-ai/guardrails` · `https://pypi.org/project/guardrails-ai`.
- asisecurity.ai (own surface): `https://asisecurity.ai/` · `https://asisecurity.ai/agent.json` · `https://asisecurity.ai/.well-known/mcp.json`.
