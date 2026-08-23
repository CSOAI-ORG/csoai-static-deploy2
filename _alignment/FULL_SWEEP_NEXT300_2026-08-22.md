# FULL SWEEP + NEXT 300 MOVES — 2026-08-22 (production-ready 100/100 A++++)

## 0. THE MANDATE
Offload bulk work off the Mac to RAG volumes (RunPod + Oracle) so the machine is free
for NN/training. Full top-down sweep: audit what's done/not-done across ALL planned work
(Downloads, sprint plans, action-items), test/audit/improve/research/improve, drive every
aspect to production-ready. Then set the next 300 moves.

## 1. MAC OFFLOAD STATUS (in progress)
Mac disk: 228Gi/99% (12Gi used, 176Mi free — CRITICAL).
- **sim-world-data/train (7.6G)** → streaming to 3090 pod `/workspace/sim-train` (RUNNING,
  177M/7.6G, slow at ~2MB/s over SSH — will complete; consider rsync after).
- OFFLOAD TARGETS: RunPod `sovos-merge-800` (800GB) + `sov-workspace-mtl4` (200GB) NV.
  Oracle `/evac-bulk` (49G, 5.8G free). Pod `/workspace` (3090: 68G free).
- CANDIDATES (big, safe to offload): sim-world-data/train 7.6G · clawd/csoai-static-deploy2
  9.1G (deploy archive) · clawd/.git (large) · sim-world-data/games-venv 1.2G ·
  experiments 1.2G · clawd/agentsociety 608M · oowm-v8-e2e 583M · meok-oneos 554M.
- KEEP LOCAL (ACTIVE): clawd/councilof-ai (2.6G, live repo) · sim-world-data/cards ·
  corpus · overnight · benchmark-results. These are the working set.
- ACTION: after train completes, offload the archival dirs (deploy archive, old venvs,
  viz/agentsociety) to the RunPod NV + Oracle. Keep active repos + cards + corpus local.

## 2. DONE ✓ (verified this session, across all lanes)
- **CBOLA sprint Day-1**: naming tap (CIBOLA) · domains/handles · schema v0.1 (validated)
  · example card · GOVERNANCE (neutrality+anti-capture) · dual license · banned-string
  purge (clean) · RFC draft 031-040 (.md+.txt) · schema-CI (PASS) · kid.js RFC9679 ·
  bundle. 14 moves DONE.
- **verify-loop fix**: PR #321 merged (797cd8ee76), live /verify → 308 → /gspc-verify (200),
  drift-guard PASS, deploy success.
- **Fleet connectivity**: 4 Ollama tunnels (A100 :11434, micro1 :11436, micro2 :11437,
  3090 :11439) · DSH settings rebuilt (4 providers/11 models).
- **Bench hardening**: pod-bench (load gate, auto-discovery, broker-models dropped) +
  pod-sweep (load gate, resolve-retry, incremental pull). 78/80 real records sweeps.
- **A2A signed-receipts v0.2**: RFC 8785 JCS, exact-key DID, revocation, 12/12 tests.
- **EAT**: 100-cycle machine, chain 3,511 chainOk, forest 10,107+, +133 cards this session.
- **Web fixes**: A2A receipts 12/12 · corpus 113/113 · IndexNow 366/366 · HF 30 datasets.

## 3. NOT DONE / OPEN (the actionable queue)
### 🔴 Owner-gated (money/accounts/clicks) — Nick
1. RealPDE Track 2 registration (Deadline PASSED Aug 20 — re-check status)
2. Rotate kimi-regen GitHub PAT (P0 security) → credential helper
3. arXiv S7VDXA → endorsement → Moon (7-day clock, ~4 days left)
4. Register cibola.dev + getcibola.com (~£15) + UKIPO (~£170)
5. AIUC-1 contributor · Erin reply · Appia/JDF · Growth Lab (27 Sep window)
6. OpenAI Apps identity verification (queue 30-120d — FILE NOW)
7. C2PA disclosures · DIF form · Firewall Charter one-read approval
8. Kaggle phone verification

### 🥇 Lane-executable (I can do) — the "spray"
9. Official MCP Registry: mcp-publisher for the flagship verification server (DONE for
   gspc/proofof/a2a — add more servers)
10. AG-UI reader → live endpoint over the EU corpus (prototype built)
11. CIBOLA: did:web doc (020) + genesis card (053) + git repo scaffold + push
12. Registry spray: a2aregistry.org, mcp.so, MCP Directory, Influzer, Glama (glama.json),
    HOL (npx skill-publish), OpenRouter headers
13. Zenodo: CSOAI Community; corpus DOI; confirm concept DOI 21991104 everywhere
14. Inspect-receipts kernel/identity anchor spike (Rekor v2 + RFC 3161 TSA)
15. Stage-3 wedge: IL SB 315 page · Evals evacuation offer · Anthropic post ·
    cert concept note · Docker MCP Catalog PR · VS Code extension publish
16. GPU gymbridge (GSPC as NeMo Gym env) · x-csoai-receipts extension field
17. B5 A100/OOWM master-stack run · B6 RunPod-key-in-cmdline leak fix

### 🔧 Machine/environment
18. Mac cleanup: offload archives after train completes; deploy2 git gc; prune venvs
19. A100 tunnel :11438 (endpoint resolving)
20. council-oowm/council-safe broken weights on 3090
21. sim_runpod stale pod view (says 0, runpodctl sees 3)
22. MCP registry llms.txt freshness (truthful)

## 4. NEXT 300 MOVES (blocks 1-300)
### BLOCK A: MAC OFFLOAD + CLEAN (1-30)
1-15  complete the train offload; verify checksum on pod; rm local train after verify
16-25 rsync deploy archive + old venvs + viz/agentsociety to RunPod NV + Oracle
26-30 deploy2 git gc · prune ~/.cache · disk to <50% · confirm Mac free for NN

### BLOCK B: CIBOLA PUBLISH (31-70)
31-40 did:web doc at cibola.dev (after domains) + 3-resolver verify
41-50 genesis measurement card signed (053) + transparent statement
51-60 RFC draft → IETF datatracker + OSF preprint + arXiv S7VDXA via CIBOLA
61-70 git repo scaffold (move 004) + GitHub org + push; bundle publish

### BLOCK C: REGISTRY SPRAY (71-120)
71-85 MCP Registry: publish all flagship servers (verify, measure, crosswalk)
86-100 a2aregistry.org + mcp.so + MCP Directory + Influzer + Glama + HOL
101-110 OpenRouter headers + X-title fix
111-120 Zenodo Community + corpus DOI + confirm 21991104 everywhere

### BLOCK D: PROOF-LAYER (121-170)
121-135 kernel/identity + anchor spike (Rekor v2 + RFC 3161 TSA)
136-150 inspect-receipts hook scaffold (Inspect 0.3.258 scorer compat)
151-160 x-csoai-receipts extension field on our MCP entries
161-170 GPU gymbridge (GSPC as NeMo Gym env, signed reward)

### BLOCK E: ECONOMIC WEDGE (171-230)
171-185 IL SB 315 public mapping page (Jan 1 2027)
186-195 Evals evacuation offer + Anthropic response post (measurement-not-prediction)
196-205 evaluation-environment cert concept note (signed sandbox attestation)
206-215 Docker MCP Catalog PR + VS Code extension publish (6-mo tenure clock)
216-230 insurer minimum product: signed per-agent evidence + queryable feed

### BLOCK F: E2E + POLISH 100/100 (231-300)
231-245 full E2E suite: sites/APIs/fleet/tunnels/chain/HF/receipts/corpus (scripted)
246-260 every surface: Dataset JSON-LD, og:image, favicon, llms.txt truthful, IndexNow
261-275 drift-guard + claims-e2e GHA stability (transient runner fails)
276-290 jail v2 honest 14-of-14 · swarm ungate Wilson · muse-glimmer chat-path
291-300 final: board refresh · sign-off · run EAT to cycle sync · publish scoreboard

## 5. IMMEDIATE NEXT (this session)
- Verify train offload completes on pod, rm local (Mac cleanup move 1-15)
- CIBOLA git repo scaffold + push (B61) — high-value, unblocked
- Registry spray start: a2aregistry + Zenodo (C) — unblocked
- EAT keeps running; chain/pairs climb
