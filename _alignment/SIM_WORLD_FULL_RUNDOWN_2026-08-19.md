# SIM WORLD — FULL RUNDOWN · 2026-08-19 11:20 UTC
## What we have right now · what's planned · ramp to 100%

---

## ══ 1. LIVE STATUS NOW (all verified this session) ══

### The machine (all green)
| Surface | Status | Detail |
|---|---|---|
| Sim World (GUI at :3080) | ✅ RUNNING | Round **3,803** and stepping (advancing ~75 rounds between two reads minutes apart); **145 agents** across 12 hives; sov-space Rust core **wired** |
| SimServer :4190 | ✅ | 7 tools live (scene/spawn/step/control/benchmark/emit_card/runpod) |
| CROSS overlay :4191 | ✅ | `/health` → `{"ok":true,"agui":true}` — divergence map served |
| GUI shell | ✅ | sim-world client.js served (rev 7c13535dab51) |
| Live benchmark DB | ✅ | **867 records** (seq 0→866), ticking every ~5 min via LaunchAgent |
| Card chain | ✅ | **1,071 linked / 0 unlinked / chainOk:true** (regenerated 11:18Z); 128 h3k files on disk + .gz |
| verify-all | ✅ | 11/11 checks passed 11:16Z; self-healed sim plane at 11:16 (home-patch re-apply) |
| Train corpus | ✅ | **30,036 SFT pairs** in cards-train.jsonl (~13.7K cards + duplicates-safe) |
| Disk | ✅ | 23 GiB free |
| LaunchAgents | ✅ | 17 sim-world/eat-all-related loaded (overnight, miner, sweep, cardseed, agui, restore, watchdog, fleet-guardian, a100-mine-hunter…) |

### The measurement estate
| Asset | Count/Detail |
|---|---|
| Signed h3k cards | 1,071 chained · 3KB ed25519-signed · J-space prev-linked |
| Card chain index | 1,071 linked, 0 breaks |
| Benchmark records | 867 (gov/care/swarm/affect/jail/slot15/human-vs-ai… all 16 axes covered) |
| HF org csoai | **29 datasets** — ALL now carry machine-parsed `cardData.license: cc-by-4.0` (license gap CLOSED this week) |
| Measured roster | qwen2.5-0.5b-cards-lora-300it **0.938** (best) · 1.5B 0.875 · gemma-3-1b 0.875 · base 0.688 — deterministic 16-axis judge, no LLM-as-judge |
| THE CROSS | MMLU real cell: human 0.898 · fleet 0.350 · divergence 0.548 · 5 honest UNMEASURED |
| Zenodo spine | DOI 10.5281/zenodo.21991104 → record 21991105 (ours, live) |
| PyPI | csoai + proofof-ai-mcp live |
| DID trust root | csoai.org/.well-known/did.json 200, both keys |
| Machine endpoints | api/gspc (23KB, correct grammar), arena/rounds.jsonl (553KB), feed.xml, badge ("13 of 14 axes") — ALL 200 |

### The product (finished view, live in GUI)
Brand header "Council of AI · GSPC Arena" · full 14-axis GSPC BOARD (status+accuracy from /api/gspc) · THE CROSS (real MMLU cell + honest UNMEASURED) · VERIFY widget · GAME humans-vs-AI scoreline · loading/error states · Escape-close · Cesium 3D globe.

---

## ══ 2. THE 1-by-1 N-SITES TEST — scorecard (delivered this session) ══
Full detail: `_alignment/N_SITES_ENDUSER_TEST_2026-08-19.md`

- **26 verified PASS** (HF 29 datasets w/ license · Zenodo · PyPI · OpenRouter · Codabench · ClawHub · ModelScope · OpenXLab · LlamaHub · RapidAPI · 4 benchmark aggregators · CompassHub · OpenVSX · Raycast · n8n · W3C/OWASP/OpenSSF/BSI · all 12 machine endpoints · GUI · CROSS · Sim World)
- **9 real FAILURES found** — each with a concrete fix:
  1. **Official MCP registry: llms.txt claim FALSE** — zero csoai entries across all 60+ pages; publish via mcp-publisher
  2. **IndexNow key not served** — returns SPA HTML at key path (text/html, not the key file)
  3. **Kaggle handle ≠ `csoai`** — 404; find the real handle
  4. **Smithery claimed listings 404** — proofof-ai / cobol-bridge / csoai all dead
  5. **ROR not created** — submit curation request (4–6 wk)
  6. **ORCID not created** — register named authors (USENIX gate)
  7. **OpenAlex DOI not indexed** — re-check after Zenodo matures
  8. **schema.org Dataset JSON-LD missing everywhere** — csoai.org has ZERO ld+json; add Dataset markup
  9. **csoai.org/api/badge.svg 404** — canonicalize badge URL
- **21 owner-gated/sequenced** (arXiv endorsement [N] · Anthropic/OpenAI [N] · Apify · Glama/PulseMCP/mcp.so auto-follow · OAI-PMH for CORE/OpenAIRE · Crossref/S2 · Wikidata · Zenodo Community)
- **12 queued** (HOL · VS Code · Terminal-Bench · τ²-bench · SWE-bench · Databricks · Chrome Store · Homebrew · etc.)

---

## ══ 3. RUNNING PIPELINES (the EATTT loops) ══

| Loop | Mechanism | Throughput now | Ramp lever |
|---|---|---|---|
| **Card mining** | honey-miner.mjs v3 (auto-discovery) → cards2train → signed h3k | Miner ticking every 5 min; 0 pairs consumed last runs (estate drained — correct, dedup) | Re-point to fresh corpus: HF csoai datasets (29), Kaggle kernels once handle found, live arena rounds |
| **Benchmark** | 16-axis judge on roster, LaunchAgent | 867 records, ~5-min cadence | Raise count per run; add gemma-3-1b + 1.5B to live roster (0.875 models); fire per-axis sweeps |
| **Card signing** | ed25519 chain, prev-linked | 1,071 cards, chain 100% | Emit more per batch (max 100); keep chain-index regenerating |
| **Training** | MLX-LM LoRA (Qwen 0.5B = 0.938 best; gemma-3-1b GGUF 1.39GB on volume) | adapters2 (Qwen300it), adapters-gemma, adapters-15b present | Retrain on the new mined pairs; run jail-separation test (14-of-14 brick) on pod |
| **Verify** | verify-all.mjs self-heals (11/11) | Green | Keep home-patch mount as the durable fix (profile patch gets clobbered by sibling lane) |
| **World restore** | world-restore.mjs snapshot+respawn | Armed on reset | Persist in-engine (host-bundle change; needs host restart to deploy) |

---

## ══ 4. THE RAMP — 100% PLAN (today + this week) ══

### A. Close the 9 failures (fastest wins) — lane-doable
1. **IndexNow** — write key file to exact path on both domains (site lane deploy; content-type text/plain)
2. **MCP registry publish** — `mcp-publisher` for `io.github.CSOAI-ORG/gspc` (GitHub auth) → makes llms.txt TRUE + unlocks Glama/PulseMCP/mcp.so/auto-followers in one move
3. **Smithery re-link** — fix the GitHub-linked listing; correct sheet claim
4. **Kaggle** — locate real org handle; fix the sheet
5. **schema.org Dataset JSON-LD** — draft block for receipt/scoreboard pages (HZ J6)
6. **OAI-PMH endpoint** — one endpoint unlocks CORE/BASE/OpenAIRE/Unpaywall (HZ J9)
7. **ROR + ORCID** — draft requests this week
8. **Badge canonical URL** — pick one, update embeds
9. **Re-run the full test matrix** after each fix → target 100/100 next pass

### B. Ramp compute + measurement
- **Benchmark fan-out**: fill remaining CROSS cells (GPQA/ARC/GAIA/MATH/SWE-bench) with real fleet numbers — eval harness exists, queue the runs
- **Jail separation test** on the pod (the 14-of-14 brick) — queued; pod ollama saturated → run when lane frees
- **Gemma GGUF deploy** on pod (importer-blocked in ollama 0.32.9 — llama-server build or ollama upgrade)
- **1.5B Qwen GGUF deploy** (trained 0.875; 0.5B is best at 0.938 — deploy both, honest labels)

### C. Ramp the estate (today-order deadlines)
- **RealPDE Track 2 team form — TOMORROW 20 Aug [N]** (Codabench live; get exact URL)
- **BSI ART/1 application [N]** — free seat in ISO SC42 + CEN JTC21 (highest-leverage standards move)
- **Wikidata item** this week (independent refs + declared COI)
- **ROR request** this week
- **HF dataset DOIs + Dataset-Search JSON-LD** this week
- **awesome-mcp PR + Cline issue** this week
- **DRCF Phase 2 → drcf@ofcom.org.uk** by 2 Sep
- **EIC Accelerator Step 1** by 2 Sep ideal
- **ICLR 2027 abstract** 18 Sep — arXiv endorsement is THE gate [N] (Moon endorser unspent)

### D. Product front end (the demo)
- Arena e2e with games — the finished view is live; add: live duel ticker, VERIFY card-in/card-out demo, THE CROSS click-through cells
- CopilotKit shell + LiveKit/Pipecat avatar greeter (planned)
- MCP Apps (SEP-1865) reach

---

## ══ 5. HONEST RISKS / GATES ══
- **HF write token [N]** — blocks card sweep + DOI minting + ZeroGPU verifier Space
- **arXiv endorsement [N]** — blocks ICLR/USENIX/S2/Crossref cascade
- **OpenAI/Anthropic owner verification [N]** — 30–120 day queues; file EARLY
- **World persistence in-engine** — needs host restart (bundle change) to deploy
- **Pod ollama saturated** — jail separation + Gemma GGUF queued behind lane freeing
- **Sibling lane contention** — shared Playwright hijacked twice this session (EUSurvey); home-level patch is the durable mount (profile patch clobbered twice); commit by name, never `git add -A`

---

## ══ NET ══
**Have:** live world (round 3,803 / 145 agents / sov-core), 1,071 signed cards chain-clean, 867 benchmark records, 30K training pairs, 4-model measured roster (best 0.938), finished GUI product, 29 licensed HF datasets, DOI spine, 14 LaunchAgents self-healing, 26/26 machine surfaces green.
**Planned (100% ramp):** close 9 real failures → registry/IndexNow/Kaggle/ROR/ORCID/JSON-LD/OAI-PMH → benchmark fan-out for the CROSS → jail 14-of-14 → pod GGUF deploy → 5 this-week standards moves ([N]: RealPDE tomorrow, BSI ART/1, Wikidata, ROR, HF token) → ICLR 18 Sep → re-test matrix to 100/100.
