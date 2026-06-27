# 🔍 CROWN JEWELS HUNT — 2026-06-27 (live findings)

**Method:** GitHub REST API direct queries (no Firecrawl needed). 3 parallel research delegations also in flight (will merge when they return).

**Status:** Personal scan done. Delegations running for: sovereign-agent verticals + traditional AI verticals + EU AI Act tooling deep-dive. Results will fold in below as they return.

---

## 🏆 Top 10 crown jewels found (live, GitHub-sourced, 2026-06-27)

| # | Repo | ★ | License | Pushed | Why-it-matters |
|---|---|---:|---|---|---|
| 1 | **`SHAdd0WTAka/Zen-Ai-Pentest`** | 406 | MIT | 2026-06-26 | AI-Powered Penetration Testing Framework — **red-team our own estate** with this; complements our `agent-prompt-injection-firewall-mcp` (the defender). Also a competitor reference. https://github.com/SHAdd0WTAka/Zen-Ai-Pentest |
| 2 | **`mukul975/Privacy-Data-Protection-Skills`** | 179 | Apache-2.0 | 2026-03-16 | 282+ structured privacy/data-protection skills for AI agents (GDPR, CCPA, EU AI Act) — **drop-in skill library** we can expose through our A2A substrate. https://github.com/mukul975/Privacy-Data-Protection-Skills |
| 3 | **`transilienceai/shasta`** | 142 | MIT | 2026-05-17 | AWS + Azure compliance automation platform for SOC2/ISO — **direct overlap** with our compliance fleet. Worth studying + cross-pollinating. https://github.com/transilienceai/shasta |
| 4 | **`SdSarthak/AegisAI`** | 89 | NOASSERTION | 2026-06-23 | Open-source AI-GRC platform, EU AI Act compliance — **fresh** (2 days old). Direct competitor. https://github.com/SdSarthak/AegisAI |
| 5 | **`gensecaihq/Wazuh-MCP-Server`** | 189 | MIT | 2026-06-26 | Wazuh SIEM via MCP — could be our **SOC integration wedge**. https://github.com/gensecaihq/Wazuh-MCP-Server |
| 6 | **`gensecaihq/pfsense-mcp-server`** | 72 | MIT | 2026-06-26 | pfSense firewall via MCP — **network-layer security agent integration**. https://github.com/gensecaihq/pfsense-mcp-server |
| 7 | **`Ansvar-Systems/EU_compliance_MCP`** | 24 | Apache-2.0 | 2026-06-22 | **EU-focused compliance MCP server** — direct competitor/collaborator for our compliance fleet. https://github.com/Ansvar-Systems/EU_compliance_MCP |
| 8 | **`opena2a-org/opena2a`** | 19 | Apache-2.0 | 2026-06-26 | **"One scan for AI risk. `opena2a review` checks an AI project"** — direct competitor to our `meok-governance-engine-mcp`. https://github.com/opena2a-org/opena2a |
| 9 | **`VibeTensor/attestix`** | 17 | Apache-2.0 | 2026-06-25 | **Attestation infra for AI Agents. DID-based agent identity, W3C VC** — exactly complements our `agent-identity-trust-mcp` A2A substrate. https://github.com/VibeTensor/attestix |
| 10 | **`airblackbox/airblackbox`** | 18 | Apache-2.0 | 2026-06-11 | Open-source EU AI Act compliance scanner, **51 checks across Articles 9-15**. Drop-in scanner. https://github.com/airblackbox/airblackbox |

## 💎 Top 5 diamonds (lesser-known gems, <100★, fresh)

| # | Repo | ★ | License | Pushed | Why-it-matters |
|---|---|---:|---|---|---|
| 1 | **`joergmichno/clawguard`** | 11 | MIT | 2026-06-22 | **Open-Source Prompt Injection Scanner. 225 detection patterns** — perfect companion to our `agent-prompt-injection-firewall-mcp`. Cross-reference our 225 vs theirs. https://github.com/joergmichno/clawguard |
| 2 | **`Responsible-AI-Labs/rail-score-sdk`** | 14 | MIT | 2026-06-12 | Official Python SDK for **RAIL Score** — LLM evaluation across 8 dimensions, guardrails. Could be a feature for our `ll144-bias-audit-mcp`. https://github.com/Responsible-AI-Labs/rail-score-sdk |
| 3 | **`archetech/materna-link-mcp`** | 0 | NOASSERTION | 2026-04-23 | **Healthcare identity verification MCP** — directly adjacent to our `healthcare-ai-governance-mcp` + `hl7-fhir-bridge-mcp`. Worth absorbing. https://github.com/archetech/materna-link-mcp |
| 4 | **`itbench-hub/ITBench-CISO-CAA-Agent`** | 21 | Apache-2.0 | 2025-05-08 | **CISO agent as part of ITBench** — direct competitor to our BFT council + sovereign orchestrator. https://github.com/itbench-hub/ITBench-CISO-CAA-Agent |
| 5 | **`causa-prima-ai/scribo`** | 13 | NOASSERTION | 2026-06-03 | **Scribo — AI-native EN 16931-compliant e-invoicing** — could plug into our `tax-bridge-mcp` for EU ViDA. https://github.com/causa-prima-ai/scribo |

---

## 🔬 Tactical action items (M4 lane, no owner keys)

### A. Run `Janix-ai/mcp-validator` against our 369 MCPs [STARTED — 2026-06-27]
- **Repo:** https://github.com/Janix-ai/mcp-validator (75★)
- **Status:** Cloned to `/tmp/mcp-validator`. **Smoke test passed**: reference stdio server (their bundled example) scored **36/36 = 100% compliant** against protocol `2025-03-26`.
- **What:** Validate our 369 MCPs against the latest spec.
- **Blocker:** The validator hangs when running against our MCPs — likely a subprocess/TTY issue with `python server.py` (the tool spawns the server and expects an MCP handshake; our MCPs are mostly stdio without proper TTY init). **Needs follow-up**: probably wrap each server in a small launcher that pipes proper MCP initialize + version negotiation.
- **Honest finding:** **0 of our MCPs are currently Janix-validator-confirmed**. Spec v2 is dropping in weeks — getting ahead of this is high-value.

### B. Absorb `mukul975/Privacy-Data-Protection-Skills` into our A2A substrate
- **Why:** 282+ structured skills for GDPR/CCPA/EU AI Act agents — they did the curation work, we expose it through our `agent-*` MCPs.
- **How:** Clone, port the skill definitions into our `agent-policy-enforcement-mcp` registry format, document provenance.
- **Estimated effort:** 2–3 hours.

### C. Cross-reference `clawguard`'s 225 prompt-injection patterns with our `agent-prompt-injection-firewall-mcp`
- **Why:** Their pattern library might have categories we missed (jailbreak variants, multi-modal injection, etc.).
- **How:** Diff our pattern set vs theirs, identify gaps, add new patterns + tests.
- **Estimated effort:** 1–2 hours.

### D. Investigate `opena2a` + `Ansvar-Systems/EU_compliance_MCP` as competitive intel
- **Why:** Both launched in the last week; they may be filling gaps we have. Read their code, update our positioning docs.
- **Estimated effort:** 1–2 hours.

### E. Red-team our estate with `Zen-Ai-Pentest` (406★)
- **Why:** Catch vulnerabilities before adversaries do. Especially relevant given the 2 HIGH Python SDK CVEs we just bumped around.
- **How:** Clone, configure for our stack, run as a weekly CI job.
- **Estimated effort:** 2–3 hours initial setup.

### F. Adopt `VibeTensor/attestix` for agent attestation
- **Why:** DID-based agent identity + W3C VC — exactly the gap our `agent-identity-trust-mcp` should plug into.
- **How:** Read their spec, integrate their DID/VC primitives into our existing agent identity MCP.
- **Estimated effort:** 2–3 hours.

### G. Partner-or-poach `Ansvar-Systems/EU_compliance_MCP`
- **Why:** 24★ Apache-2.0 EU compliance MCP, just launched. Either collaborate (their content + our distribution) or build a counter-positioning MCP. **Nick's call (GTM)**.
- **Estimated effort:** 1 hour to read + decide.

---

## 📋 What I'm NOT doing yet (deferred until delegations return)

The 3 parallel delegations will add:
1. CCO/AIOps tools + EU AI Act tooling ecosystem (deleg_cdf0534c)
2. Sovereign-AI / self-hosted LLM / agent-identity / Ed25519 / x402 (deleg_318dbc11)
3. Healthcare + Finance + Robotics + Insurance verticals (deleg_455eb605)

When they return, I'll fold their findings into this doc + update the action list.

---

*M4 lane · GitHub REST API direct queries · 2026-06-27 06:25*