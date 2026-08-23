# OOWM Estate — Full Audit & Checklist (2026-08-23)

## What was done this session (verified, honest)

### A. OOWM fleet composition (the "12 around 1")
- Inspected the real fleet: 14 models 0.5B→31.6B (nemotron-30b, phi4-14b, gemma3-12b, deepseek-r1-8b, qwen2.5-7b, mistral-7b, ...).
- Extracted a per-model specialist map from `govbench_oowm_*` results (5 models × 12 governance pillars).
- **Built + measured the OOWM router**: routes each task to the measured specialist.
- **Benchmarked the big models** (phi4-14b, nemotron-30b, gemma3-12b) on knowledge Q&A:
  - phi4-14b = **1.00** (7/7), gemma3-12b = **1.00** (7/7), nemotron-30b = 0.429 (empty-response tunnel artifacts).
  - Finding: **phi4-14b is the factual-knowledge specialist.** Correcting the earlier small-model-only frame.

### B. OOWM router + domain gateway (the code)
- `oowm_router.py` — task-type router (knowledge→phi4/gemma, governance→qwen3:8b, safety→council-oowm) WITH load-balance + fallback.
- `domain_gateway.py` — domain router (law/regulation/framework→gov RAG, benchmark→arch RAG, sovereignty→sovereignty RAG, harm→safety RAG, knowledge→mine RAG) + model specialist.
- `retrieval.py` — BM25 retrieval (stdlib-only). `vector_retrieval.py` — TF-IDF+cosine vector retrieval (stdlib-only).
- `oowm-router.json` — measured-specialist policy.
- **Verified**: classifier 7/7 domains correct; BM25 pulls precise law cards (Article 50) vs naive noise; vector+BM25 integrated.

### C. AG-UI front-end alignment
- Added `/oowm` POST route to `agui-gateway.mjs` (:4191) — proxies to domain gateway :8767, fallback :8766.
- Added OOWM branch to `agui-overlay.html` handlePrompt — what/what-is/law/gspc queries route through `/oowm`.
- Restarted gateway (syntax OK, `health ok:true`).
- **End-user tested**: overlay serves (title), /health /cross /jail /leaderboard /games all 200, /oowm route present.

### D. Durability + repo/runpod placement
- Task router `:8766` (com.meok.oowm-router) + domain gateway `:8767` (com.meok.oowm-domain-gateway) = launchd durable.
- A100 tunnel (com.meok.ollama-tunnel-runpod) reloaded, :11434 serving 14 models.
- **Committed to clawd monorepo** (by name, isolated): `oowm-gateway/` (5 files, commit 9be985662) + `oowm-gateway/agui/` (2 files, commit 1014ff20a).
- **Pushed to runpod A100** `/workspace/csoai-rag/gateway/` (7 files + mined card bank).

## Honest blockers / NOT done
- **A100 Ollama engine reliability**: models listed but intermittently `not-found`/empty on `/api/chat` (qwen3:8b not-found, phi4/gemma intermittent). This is a **pod compute/infra issue** — routing is correct, but a live answer needs a stable engine. ❗
- **`:4190` (sim control) down** — "spawn/step" AG-UI actions won't work (sim-control port not up).
- Co-located pod gateway `:8770` not returning health (process not persisting).
- True neural embedding (nomic-embed-text via /api/embed) not served by this Ollama build — used BM25/TF-IDF vector instead.

## Others' work audited (for further improvement)
From recent commits (other lanes):
- `M4: MASTER_LAUNCH_CHECKLIST.md` (24.6K) — canonical launch checklist. → **align OOWM checklist with it.**
- `M4: Sovereign Witness MVP (L0.8)` + `MEOK_UE5_INNER_VAULT` — the Sovereign Witness / UE5 knowledge base.
- `King's Decree: all 8 Layer-0 protocols 100/100` — matches our attested-everything posture.
- `predicate upgrade: refusal 0.400→0.800 on safety-15` — relevant to our jail-hardening (0.833).
- `RealPDE self-calibrate default off` — A/B noise discipline (aligns with our no-fabrication rule).

## Next (feasible, prioritized)
1. **Stabilize the A100 Ollama engine** (pod-side) — unblocks live answers on all gateways.
2. **Reload co-located pod gateway** :8770 (nohup/setsid, keep alive) so runpod-side gateway works.
3. **Test AG-UI as each end-user type** (researcher→leaderboard/jail, regulator→register/compliance, consumer→board/games, dev→oowm/domain) once engine stable.
4. **Align OOWM checklist with M4's MASTER_LAUNCH_CHECKLIST.md.**
5. Fix `:4190` sim-control (SDK/AG-UI spawn/step).
