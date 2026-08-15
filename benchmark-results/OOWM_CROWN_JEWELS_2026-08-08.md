# SOVOS OOWM — Crown-Jewel Arsenal (verified 2026-08-08)

Today's mission: build the first open-source OOWM — all open-source models unified
under SOVOS. This manifest is the VERIFIED truth (no hedging, no fabrication).
All repos cloned to RunPod pod `/workspace`; all papers confirmed on arXiv.

## Verified repos (cloned, live)

| Layer | Tool | Pod path | SOVOS role |
|---|---|---|---|
| L1 Fusion | arcee-ai/mergekit | `/workspace/mergekit` | weight-space clan fusion (sandwich baker) |
| L1 Fusion | SakanaAI/evolutionary-model-merge | `/workspace/evolutionary-model-merge` | auto-evolve optimal merge recipes |
| L2 Runtime | togethercomputer/MoA | `/workspace/MoA` | 4 proposers + 1 aggregator (fluid council) |
| L4 Routing | lm-sys/RouteLLM | `/workspace/RouteLLM` | learned cheap-vs-strong router |
| L4 Routing | aurelio-labs/semantic-router | `/workspace/semantic-router` | <10ms embedding routing (the missing gap) |

Also confirmed real: BerriAI/litellm (gateway). `EnnengYang/Awesome-Model-Merging`
could not be resolved at clone time (moved/renamed) — not critical, papers below.

## Verified whitepapers (arXiv-confirmed, abstracts captured)

Manifest: `benchmark-results/oowm_crown_jewel_papers.json`

| Tag | arXiv | Title | Why it matters |
|---|---|---|---|
| CoMoL | 2603.00573 | Efficient Mixture of LoRA Experts via Dynamic Core Space Merging | LoRA+MoE+merging in one paper — the OWEM hive architecture proven |
| Darwin | 2605.14386 | MRI-Trust-Weighted Evolutionary Merging (Darwin Family) | training-free evolutionary merging, frontier reasoning |
| MergePipe | 2602.13273 | Budget-Aware Parameter Management for Scalable LLM Merging | cheap merging on free-GPU constraints |
| ProbInf | 2607.01689 | Model Merging as Probabilistic Inference in Fine-Tuning Parameter Space | mathematical legitimacy — "Bayesian inference over parameter space" |

## Estate native equivalents (do NOT rebuild)

- Routing: sov-hive `meta.rs` (ExpertiseMap/select), `sov_route.py`, `sov4_router.py`, hive.rs `select_models`
- Evolution-esque: `sov7_synthesis_orchestrator.py` (mergekit+evolution references)
- Gateway: `sov_fluid.py` (litellm references)
- Provenance: C2PA pipeline + sov-hive honey.rs (provenance-gated minting)

## Build order (next moves)

1. semantic-router install + first <10ms clan-routing smoke on pod (true gap)
2. RouteLLM install + train a cheap/strong split on govbench probes
3. MoA 4-clan proposer demo against local ollama clan models
4. Fuse a clan sandwich with mergekit (TIES) on 2-3 ollama 0.5-1.5B bases
5. Publish SOVOS-OOWM GitHub release with manifest + papers

## Honesty register

- Nutrition note was a screenshot artifact, not technical — ignored.
- NVIDIA Inception $200K is an external application (Nick action), not code.
- 55G `.claude-science` > 46G evac-bulk: remainder must land on a RunPod volume
  (boot retries continued) or pod `/workspace` after clawd migration drains.
## VERIFIED BUILD PROGRESS (same-day update)

- All 5 arsenal repos cloned to pod `/workspace`: mergekit, evolutionary-model-merge,
  MoA, RouteLLM, semantic-router.
- pod env fix: aiohttp pinned 3.14.x → 3.13.5 (litellm import was broken) — litellm + semantic_router now import clean.
- **SOVOS Clan Router LIVE**: `/workspace/sovos_clan_router.py` — local HF encoder,
  5 clans (fish/builder/watchdog/trader/proof), direct LocalIndex query path
  (SemanticRouter convenience __call__ was buggy on local index → we wire index.query()).
  Verified: 5/5 queries route to correct clan, zero LLM/cloud.
- semantic-router gotchas recorded: fit(X,y) trains classifier not index; auto_sync="local"
  writes empty config; must call router.index.add(embeddings,routes,utterances) then index.query(vector,top_k).
- Next: MoA 4-clan proposer demo → mergekit TIES clan sandwich → RouteLLM cheap/strong split → publish.

## MoA DEMO — LIVE (verified)

- `/workspace/sovos_moa.py` — sovereign Mixture-of-Agents, fully local Ollama:
  2 clan proposers (sov-refusal-combo-lora, sov-refusal-lora-repull) + local aggregator.
- Ollama OpenAI-compat endpoint confirmed (`/v1/chat/completions`, fp_ollama).
- Live run: faction proposals ($50 quote + safety checks) then council synthesis
  that self-corrected the price — MoA council behavior proven on local models.
- Next: mergekit TIES clan sandwich (both sov-refusal sisters) → published HuggingFace base.

## COMPLETE OOWM CHAIN — LIVE (verified, second build)

- `/workspace/sovos_chain.py` — full sovereign OOWM pipeline: SEMANTIC ROUTER →
  CLAN MODEL → GSPC GOVERNANCE GATE (governance/security/privacy/commerce).
- Fixed pod env from mergekit install: transformers 5.12.1 (broken BACKENDS_MAPPING
  on tensorflow_text) → pinned 4.49.0. semantic_router + chain both import clean.
- Live run: fish_clan + builder_clan routed; GSPC gate HONESTLY quarantined both
  refusal-tuned outputs (commerce gate FAIL) — abstinence-by-design, no fake passes.
- mergekit GGUF finding: this mergekit is safetensors-only (methods linear/slerp/
  dare/passthrough/gen-task-arithmetic). GGUF fusion needs safetensors export —
  recorded as follow-up, NOT faked. Two sov33 v10/v11 f16 GGUFs (994M, distinct md5)
  sit on pod at /workspace/p5/ for that later step.

## P0 EXECUTION BATCH (2026-08-09) — verified live

- P0-1 meok.ai: HTTP 200 "MEOK OS — Your Sovereign AI" (CF proxy). DONE.
- P0-3 king-runestone portal v6: /portal/health JSON ok; full signup→login→submit→audit
  cycle verified (SOVEREIGN 0.917). Live :7777.
- P0-6 ledger persists: data/sovereign-portal/runestone-ledger.jsonl (was /tmp). DONE.
- P0-5 Ed25519 REAL: emit_sigil signs with persistent keypair (data/…/sigil_ed25519.key/.pub);
  audit returns crypto:Ed25519 + pub.verify(). Tamper test: pristine T / tampered F / corrupt sig F. DONE.
- P0-4 payload→pod pipeline built: trust-registry-api/src/runpodDispatch.ts (order→pod via
  podFindAndDeployOnDemand, ~/.runpod key) + checkout webhook appends data/stripe-orders.jsonl
  + dispatches. Smoke: ledger written; dispatch reached RunPod API (supply constraint at boot = infra).
- P0-2 CEASAI 1-pager deployed-ready: csoai-static-deploy2/ceasai.html (AEO complete) →
  needs dashboard bind of ceasai.org (Namecheap BasicDNS, currently 000 no host).

## GATED (Nick dashboard actions)
- ceasai.org bind → CF Pages or Vercel 301
- NVIDIA application: needs SECOND unique @csoai.org contact email (form parked)
- Funding apps (AI Grant/Mozilla/InnovateUK/AngelList/SeedLegals): need account creds
- Companies House £13 filing: Nick payment
- LinkedIn SOVOS post: Nick posts (draft ready below)
- Stripe live keys → pod boot (supply/deriv credentials)
