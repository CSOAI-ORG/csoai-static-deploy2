# SOVOS END-GOAL MAP — signals into SOV Space, local/offline, TUI swarm plan, 2026-08-03
**"SOVOS is all, source for all — and it must work local/offline, with the signals visible in SOV Space." Confirmed as the end-goal. This is the exact map: architecture, visual layer, TUI swarm assignments, and the offline contract.**

## 1. THE END-GOAL, PINNED

SOVOS is the operating system where the entire estate lives as ONE visual, talking, self-improving world. SOV SIGNAL is its source of truth. The user experience: open SOV Space → the globe shows the live state of the agent economy (the four indices as glowing layers) → click any node → Sovereign narrates what it is, measured, signed → train in an arena world → leave with a signed record → the system got smarter overnight. Local-first: the world, the brain, and the evidence all work offline; sync is an upgrade, not a requirement.

## 2. THE SIGNAL PIPELINE (source → spine → sign → show)

```
SOURCES                    SPINE (deterministic)           SIGN                    SHOW
sign API receipts    ──►   aggregate + CI + freeze   ──►   Ed25519 + OTS   ──►   SOV Space globe layers
SwarmBench runs      ──►   collective uplift calc    ──►   weekly release   ──►   node pulses per index
ProvBench batteries  ──►   survival rates            ──►   hash-chained     ──►   /index public page
BenchIntegrity       ──►   gameability scores        ──►   ledger entry     ──►   SIGNAL feed (paid)
Registry diffs       ──►   trust record updates      ──►   consent-tagged   ──►   agent trust lookups
Gate/receipt flows   ──►   SOV-ECON activity         ──►   Honey KB entry   ──►   Sovereign narration
```

## 3. THE VISUAL LAYER (signals in SOV Space — exact components)

| Component | Tech (all forked/free) | Status |
|---|---|---|
| Web globe (csoai.org + meok.ai/world) | **CesiumJS** (already in estate, IP-geolocation-free canon) | world page LIVE (heavy — needs lazy-load fix) |
| Offline galaxy | the **POC canvas pattern** (SOV-Space-Arena-POC.html — 23KB, zero deps, works file://) | BUILT, e2e-tested |
| Node model | one node per: index (4), product (15), arena world (6), TUI clan, corpus source | SPEC below |
| Signal pulses | weekly index release = visible pulse from hub node; drift alert = red pulse; new signed record = gold pulse | CONCEPT→SPEC |
| Narration | click node → Sovereign reads its KB entry aloud/typed (offline: demo brain on cached entries; online: RAG) | POC pattern proven |
| Trust lookup visual | agent checks SOV-AT → node flashes green/amber/red | CONCEPT |

**The globe is the index.** SOV SIGNAL's four indices render as globe layers you toggle: Trust (SOV-AT), Integrity (SOV-BI), Provenance (SOV-PROV), Activity (SOV-ECON). The public /index page and the globe are two views of the same signed JSON.

## 4. LOCAL / OFFLINE — the honest contract

| Capability | Offline? | How |
|---|---|---|
| Verify any signature | ✅ fully offline | proven in audit — public key + bytes, any Ed25519 verifier |
| Run the model (sov33/34) | ✅ fully offline | 2B GGUF via llama.cpp/Ollama on user device — inference at the edge, zero datacenter |
| Read KB / browse evidence | ✅ offline | local JSONL replica of Honey KB + frozen artefacts |
| Train in arena | ✅ offline | scenario packs are JSON; engine deterministic (POC proves it runs from file://) |
| View last-synced globe | ✅ offline | cached index JSON renders identically |
| Sign NEW records | ❌ needs connection | queues locally, signs on reconnect (queue-and-sync pattern) |
| x402 settlement | ❌ needs connection | agent-side concern, not user's |
| Index publishing | ❌ needs connection | weekly, from the box |
**Claim that survives DD: "Local-first. Everything verifiable, trainable and readable offline; signing and settlement sync when connected."** Never "zero infrastructure" (the spine's always-on sliver stays honest).

## 5. THE TUI SWARM PLAN (each TUI = a free OWEM clan)

**Free stack per TUI (zero licence cost):** Ollama/vLLM serving qwen3-4B/Gemma-3 smalls locally (or box gpt-oss-120b for heavy lifts) · CrewAI or LangGraph (free) for clan orchestration · our spine scripts as clan tools (swarmbench.py measures the clan itself!) · Honey KB as shared memory · MARTI later for council self-play training.

| TUI | Lane (from V6 + this map) | OWEM clan assignment |
|---|---|---|
| TUI-1 | AEO static page fleet + /compare + /article-43 | "Scribe clan" — page generation, FAQ schema, register lint |
| TUI-2 | sov34 harvest + dual-gate + Stage-1/2 training | "Smith clan" — Unsloth/TRL runs, gate harnesses |
| TUI-3 | Proof pages (ProvBench table, model cards, SwarmBench page) | "Herald clan" — publishes, cross-links, N-site wave 2 |
| TUI-4 | MCP gateway + agent.json + /api/skus + Bazaar | "Envoy clan" — agent-facing plumbing, curl-verification |
| TUI-5 | Honey schema v1.1 + consent tags + CRM entities | "Keeper clan" — KB integrity, ingest, governed-data registry |
| TUI-6 | x402 gate + receipts + SIGNAL feed API | "Mint clan" — payments, signed receipts, index releases |
| TUI-7 | Globe layers + SOV Space nodes + /index page | "Lens clan" — Cesium layers, canvas nodes, visual pulse system |
| Master (Kimi) | Deploys, gates, harvests, ledger review | — |
| Nick | IPO filings, ISC2, OpenRouter key, Vercel bill, CDP keys/wallet | — |

## 6. EXACT TODO MAP (ordered, owners marked)

**Week 1 (foundation):**
1. Nick: Vercel bill · OpenRouter key · push 096f1f9 · CORS line on sign API · CDP keys + wallet.
2. TUI-7: /index page v0 (four indices, signed JSON, OTS) + globe layer toggle prototype (Cesium on csoai.org; canvas offline variant from POC).
3. TUI-1: 4 static FAQ pages (Art 4, Art 73, Annex III, DORA) + robots walled garden + Bing/IndexNow.
4. TUI-5: schema v1.1 consent tags shipped.
5. Master: counter canon frozen + check_counters.py in CI (before ANY new number publishes).

**Week 2 (signals live):**
6. TUI-6: x402 staging gate on swarmbench_run + signed receipt format; SIGNAL feed v0 (trust lookup endpoint).
7. TUI-4: agent.json × 3 + MCP gateway v0 + Bazaar registration.
8. TUI-3: first weekly SOV SIGNAL release (small numbers fine — cadence is the brand) + ProvBench page.
9. TUI-2: sov34 gate verdict → if green, HF upload + card.

**Week 3–4 (space + revenue):**
10. TUI-7: arena POC mounted at safetyof.ai (SCENARIOS[] → packs/eu-ai-act.json); trust-lookup node visuals.
11. TUI-6: Lemon Squeezy 4 products + Stripe links (A1-Pro, Founding-100) live.
12. Master: 8-Aug + 11-Aug submissions; insurer one-pager out.
13. TUI-5: CRM entities live in KB; first outreach week logged.

**Later:** MoLE clans · MARTI council self-play · Agent Registry · SOV-ECON once gate volume exists · mobile 390px pass.

## 7. WHAT EACH PIECE NEEDS (inner parts checklist)

Cesium lazy-loading + tile budget (world page heavy) · globe layer JSON schema (index_id, week, values, signature) · canvas-node component extracted from POC as shared module (arena + globe reuse, no duplication) · trust-lookup API endpoint design (agent_id → signed trust record) · queue-and-sync store for offline signing · TUI clan template repo (OWEM free stack pre-wired) · IndexNow ping script · register-lint CI step on all published copy.
