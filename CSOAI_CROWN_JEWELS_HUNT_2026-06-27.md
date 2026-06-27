# 🔍💎 Crown-Jewels Hunt — OSS to absorb + new competitors in our lane (2026-06-27)

Deep-research sweep across the board: open-source code, latest 2026 news, CCO/buyer developments — hunting for diamonds we can absorb **and** mapping who just landed in our Article-12 / legacy-compliance lane. Honest read: the hunt found **both gold to absorb and real new competitors** — and the competitors *sharpen* where our moat actually is.

---

## 💎 TIER 1 — ABSORB THESE (highest value, low risk, strengthens the moat)

### 1. `oscal-compass/compliance-trestle` — the OSCAL platform we should stand on, not rebuild
- **What:** IBM-origin (now a CNCF-adjacent community, `oscal-compass`), opinionated **compliance-as-code** tooling over NIST OSCAL. Runs as a **CI/CD pipeline on compliance artifacts in git** — create/validate/govern OSCAL SSPs, component-defs, assessment results, with transparency across stakeholders. Apache-2.0.
- **Why it's a jewel:** This is *exactly* the layer our `oscal-generator-mcp` is hand-rolling — but mature, tested, multi-format (XML/JSON/YAML), with a real community. **We should wrap trestle as the engine behind oscal-generator-mcp** instead of maintaining our own canonicaliser/validator. Our differentiator stays the **Ed25519 signing + SIGIL chain + the 55-component Layer-0 package**; trestle does the heavy OSCAL plumbing underneath.
- **Move:** add `compliance-trestle` as a dependency in oscal-generator; keep our sign/verify/RFC-0024 tools on top. Validate our `layer0_protocol.oscal.json` *through trestle* → instant external-tool credibility ("our package validates under the standard community toolchain").
- 🔗 https://github.com/oscal-compass/compliance-trestle

### 2. `usnistgov/oscal-cli` + `usnistgov/OSCAL` — the official NIST validator
- **What:** NIST's own CLI + schemas for OSCAL operations (validate, convert XML↔JSON↔YAML).
- **Why:** Free, authoritative validation oracle. Run our signed package through `oscal-cli validate` in CI → "NIST-tool-validated" is a real trust claim for the FedRAMP RFC-0024 wedge (machine-readable mandate, 30 Sep 2026).
- **Move:** add `oscal-cli validate` to the oscal-generator CI workflow.
- 🔗 https://github.com/usnistgov/oscal-cli · https://github.com/usnistgov/OSCAL

### 3. `Azure-Samples/Legacy-Modernization-Agents` — the COBOL-understanding front-end to our bridges
- **What:** Microsoft's open AI-agent framework that **reverse-engineers COBOL** (BusinessLogicExtractorAgent → human-readable docs) before converting to Java Quarkus / C# .NET. Multi-provider (Azure OpenAI / Copilot / OpenAI).
- **Why it's a jewel AND not a threat:** It does **modernization (migration)**; CSOAI does **governance (compliance attestation)**. They're complementary — their "understand the COBOL first" agent is the perfect *input* to our `cobol-bridge-mcp` (parse → **then govern + sign**). A bank modernizing COBOL with this still needs our signed EU-AI-Act/DORA attestation on the result. **Position: "we govern what Azure modernizes."**
- **Move:** reference it in the cobol-bridge demo as the upstream; explore calling its extractor to enrich our `parse_cobol_program` output.
- 🔗 https://github.com/Azure-Samples/Legacy-Modernization-Agents

### 4. The "awesome" jewel-maps — mine these for the next 20 absorb candidates
- `morganrcu/awesome-eu-ai-act` — tools that **generate the evidence the law requires** (our exact niche). 🔗 https://github.com/morganrcu/awesome-eu-ai-act
- `GenAI-Gurus/awesome-eu-ai-act` — OSS + templates + guides. 🔗 https://github.com/GenAI-Gurus/awesome-eu-ai-act
- `theopenlane/awesome-compliance` — broad compliance libraries/tooling. 🔗 https://github.com/theopenlane/awesome-compliance
- `Vaquill-AI/awesome-legaltech` — **MCP servers, models, datasets for the legal ecosystem** (legaltech distribution surface — where are *our* reg-MCPs listed? answer: nowhere yet). 🔗 https://github.com/Vaquill-AI/awesome-legaltech
- **Move:** submit CSOAI's reg-MCP fleet + bridges as PRs to these awesome-lists = free, durable GEO/distribution (the GRC giants aren't on them either).

---

## ⚔️ TIER 2 — NEW COMPETITORS IN OUR ARTICLE-12 LANE (the honest threat read)

The big change since the June audit: **open-source Article-12 / tamper-evident-logging tools are now shipping** — including **local-first / on-prem** ones (the sovereign angle we claimed as differentiated). This contests the "signed Art.12 audit on agents" wedge. **But every one of them governs MODERN agent frameworks (LangChain/CrewAI/AutoGen) — none bridge COBOL/SAP/SCADA/HL7.** The legacy moat *holds* and is now the *cleanest* differentiator.

| OSS competitor | What it ships | Overlaps us on | Does NOT have (our edge) |
|---|---|---|---|
| **AIR Blackbox** (`airblackbox/gateway`) | EU AI Act scanner, **39–51 checks Art.9-15**, **HMAC-SHA256 tamper-evident chains**, PII + prompt-injection block, **local-first** | Art.12 hash-chain + local-first (our SIGIL + sovereign claim) | Legacy bridges · BFT council · article-level reg *content* · Ed25519/OSCAL |
| **Sentinel Kernel** (`sebastianweiss83/sentinel-kernel`) | "Trace/Policy/Evidence under EU jurisdiction", **Apache-2.0, on-premise**, automatic tamper-resistant Art.12 logging | On-prem EU-jurisdiction Art.12 evidence | Legacy · signed OSCAL package breadth · the 22-bridge category |
| **Vaara** | Python runtime oversight, intercepts tool calls, **hash-chained audit logs** for Art.12 + Art.14 | Hash-chained audit (our SIGIL) | Legacy · OSCAL · bridges · BFT |
| **Systima Comply** | **AST-based** scanner, 37+ frameworks, call-chain tracing, Art.5-50 obligation checks, CLI + GH Action + TS API | Breadth of article coverage + CI distribution | Legacy bridges · signed artifacts · sovereign runtime |
| **ark-forge/mcp-eu-ai-act** | MCP scanner, now with **"ArkForge Trust Layer" → tamper-proof proof_id + public verification URL** | MCP-native + verifiable proof (our exact pattern) | Breadth (single EU-AI-Act MCP) · legacy · BFT |
| **Microsoft Agent Governance Toolkit** | 7-pkg MIT, OWASP Agentic Top-10, **EU AI Act + NIST + HIPAA + SOC2 mappings**, <0.1ms p99, 8+ agent frameworks | Layer-A plumbing + framework mappings | Legacy · signed OSCAL · article-level *depth* · BFT council |

### What this means (corrected, honest)
1. **The "signed Art.12 audit on modern agents" wedge is now OSS-contested.** AIR Blackbox + Sentinel Kernel + Vaara are *credible, local-first, hash-chained* — the same shape as our A2A `agent-audit-logger` + SIGIL. We should **stop pitching "we sign agent audit logs" as the differentiator** — it's becoming table-stakes, same as MS commoditized the plumbing.
2. **The legacy bridges are now the ONLY uncontested ground — even cleaner than before.** Five of six new competitors explicitly govern LangChain/CrewAI/AutoGen. **Zero touch COBOL/SAP/SCADA/HL7/ISO-20022.** This *confirms and sharpens* the `CSOAI_COMPETITIVE_MATRIX` Layer-A/Layer-B read: lead with legacy, exclusively.
3. **"Verifiable proof_id + public URL" (ark-forge) is a pattern we should match or beat.** Our offline-verifiable Ed25519 is *stronger* (no callback to a vendor), but we lack their *public verification UX*. **Build a public "verify this CSOAI attestation" page** (drop a sig → verifies offline-in-browser, like the OS already does on-device). That turns our cryptography into a sales-visible proof.
4. **The local-first / sovereign claim is no longer unique on its own** — Sentinel Kernel is Apache-2.0 on-prem EU-jurisdiction. Our sovereign differentiation has to be **legacy + on-device + BFT council + the 369-MCP breadth as a packaged whole**, not "on-prem" alone.

---

## 🏦 TIER 3 — THE BUYER (CCO) IS NOW SPENDING (the demand is real + dated)

The deep-research on the buyer side strengthens the wedge with hard 2026 numbers:
- **Market:** AI governance & compliance spend → **$2.54B in 2026 → $8.23B by 2034**; legal/compliance GRC-tool investment **+50% by 2026**; consulting demand for AI-risk-governance **+40% in 2026**. *(Note: this is the broader gov-compliance spend; the narrower "AI governance platforms" Gartner figure is $492M→$1B+ — both cited, don't conflate.)*
- **The teeth:** EU AI Act high-risk obligations **fully enforceable Aug 2, 2026**; fines up to **€15M or 3% of global turnover**.
- **The named buyer:** banks' **AML, credit-scoring, fraud** systems are high-risk *by definition* (Annex III Part 5b/5c). **ECB 2025-26 supervisory priorities explicitly list AI governance + model-risk** — engagement letters already reference it. Healthcare AI validation **adds 20-40% compliance cost.**
- **The accountable human:** the **CCO / a designated senior exec must own AI oversight**, and the **board risk committee must formally include AI compliance** in its mandate (per the FluxForce CCO guide + Fortune/Yale framework).
- **Why it matters for the pitch:** the buyer (bank/insurer CCO) now has (a) a budget line that's growing 50%, (b) a hard date, (c) a personal-accountability mandate, and (d) legacy systems (COBOL/SAP) the funded competitors don't touch. **That is the single sharpest sales motion in the whole estate.**

🔗 Sources: [SQ Magazine AI compliance cost stats](https://sqmagazine.co.uk/ai-compliance-cost-statistics/) · [FluxForce CCO guide](https://www.fluxforce.ai/for/cco-ai-act-compliance) · [Modulos financial-services](https://www.modulos.ai/industries/financial-services/) · [Vantedge board playbook](https://www.vantedgesearch.com/resources/blog/board-playbook-eu-ai-act-deadlines-you-cant-miss/) · [Wilson Sonsini 2026 preview](https://www.wsgr.com/en/insights/2026-year-in-preview-ai-regulatory-developments-for-companies-to-watch-out-for.html)

---

## 🎯 THE DIAMONDS — concrete absorb/build moves (ranked, M4-lane)

1. **Wrap `compliance-trestle` under oscal-generator-mcp** — stop hand-rolling OSCAL plumbing; keep Ed25519/SIGIL on top. *(Biggest leverage: credibility + less code to maintain.)*
2. **Add `oscal-cli validate` + trestle-validate to CI** — "NIST-tool + community-tool validated" trust claim for the RFC-0024 wedge.
3. **Build the public "verify a CSOAI attestation" page** — match ark-forge's verifiable-proof UX, but offline/in-browser (we already do on-device verify in the OS — lift that into a standalone page).
4. **Submit the reg-MCP fleet + 22 bridges to the awesome-lists** (eu-ai-act ×2, awesome-compliance, awesome-legaltech) — free durable distribution the GRC giants haven't taken.
5. **Re-point the narrative once more (doc-level, not just claim):** drop "signed agent audit logs" from the headline (now OSS-contested by AIR Blackbox/Sentinel/Vaara) → lead **exclusively** with "govern + sign the legacy economy for Aug-2026, with the article-level reg content + BFT no one else has." Update the investor memo + outreach.
6. **Competitive-watch file:** add AIR Blackbox / Sentinel Kernel / Vaara / Systima / ark-forge to a living `CSOAI_OSS_COMPETITORS.md` so we track their roadmaps (they're moving fast in our lane).

---

## Honest bottom line
The hunt paid off **both ways**: real diamonds to absorb (**compliance-trestle, oscal-cli, the Azure COBOL-understanding agent, four awesome-list distribution surfaces**) *and* a sobering, useful finding — **the Article-12 signed-audit space we thought was ours is now OSS-contested** (local-first, hash-chained, EU-jurisdiction tools shipping). The silver lining is sharp: every new entrant governs *modern* agents, so the **legacy bridges are now the cleanest, most defensible moat in the whole estate** — and the buyer (bank/insurer CCO) has a growing budget, a hard date, and personal accountability. **Lead with legacy. Stand on trestle. Validate with NIST's own tools. Ship a public verify page. Get on the awesome-lists.**

*Sources (code): [Azure Legacy-Modernization-Agents](https://github.com/Azure-Samples/Legacy-Modernization-Agents) · [compliance-trestle](https://github.com/oscal-compass/compliance-trestle) · [oscal-cli](https://github.com/usnistgov/oscal-cli) · [usnistgov/OSCAL](https://github.com/usnistgov/OSCAL) · [airblackbox/gateway](https://github.com/airblackbox/gateway) · [sentinel-kernel](https://github.com/sebastianweiss83/sentinel-kernel) · [ark-forge/mcp-eu-ai-act](https://github.com/ark-forge/mcp-eu-ai-act) · [microsoft/agent-governance-toolkit](https://github.com/microsoft/agent-governance-toolkit) · [awesome-eu-ai-act (morganrcu)](https://github.com/morganrcu/awesome-eu-ai-act) · [awesome-eu-ai-act (GenAI-Gurus)](https://github.com/GenAI-Gurus/awesome-eu-ai-act) · [awesome-compliance](https://github.com/theopenlane/awesome-compliance) · [awesome-legaltech](https://github.com/Vaquill-AI/awesome-legaltech)*
