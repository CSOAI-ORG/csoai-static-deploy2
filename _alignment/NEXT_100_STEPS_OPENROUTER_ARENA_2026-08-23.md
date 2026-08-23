# NEXT 100 STEPS — OpenRouter + Arena + Improve Ours (2026-08-23)
Owner: JEEVES lane. Estate: RunPod volume = home, Mac = thin client, Oracle = redundancy mirror.
Compass: honest measurement (UNMEASURED ≠ 0), RAG ≥ best-parent (no weight-merge lies), assess/never certify.

---
## PHASE 0 — FINISH THE MOVE (steps 1-10) [in flight / 2 done]
1. ✅ Harness+mirror rsyncs resumable (sovos-sync-resume.sh, append-verify, retries x6)
2. ✅ Reverse tunnel live (pod -> Mac :8766/:11434/:8877 via com.sovos.remote-services)
3. ⏳ Finalize job (bash-20): provision after SSH cooldown = git birth + push + cron + train + proof EAT
4. Verify sovos-harness git repo pushed to github.com/CSOAI-ORG/sovos-harness (main)
5. Verify pod cron `0 3 * * * /workspace/sovos-eat.sh` + first proof EAT cycle log
6. Mirror sovos-harness repo to Oracle micro (git clone --mirror; free-tier ARM, off-site redundancy)
7. Add Oracle clone to backup procedure (sovos-backup.sh: rsync secrets+repo -> oracle micro if reachable)
8. Daily backup plist verified one run (com.sovos.backup log entries)
9. Free Mac disk fully: after mirror verified, trash non-essential local copies (keep thin working tree)
10. Wire state doc: SOVOS_ESTATE_STATE-2026-08-23.md on volume (canonical, both copies)

## PHASE 1 — LEARN OPENROUTER (steps 11-27)
11. Read OpenRouter routing doc: provider fallback chains, weights, auto-router (openrouter.ai/blog/insights/model-routing/)
12. Read BYOK doc (openrouter.ai/docs/guides/overview/auth/byok) — we have 8 provider keys; BYOK = instant catalog access
13. Audit eunomia-gateway.cjs vs OpenRouter surface: /v1/models, /v1/chat/completions w/ fallback, /ledger vs usage API
14. Implement provider abstraction in gateway: {provider, model, key, health, weight} — mirror OR's routing chain
15. Implement fallback: primary->secondary->tertiary per model alias (same OR semantics, our lease of truth)
16. Add /api/v1/usage + price table (our margins, honest ledger) — the "OpenRouter school" business surface
17. Add /api/v1/auth/key (BYOK-style client keys for our rentable models) — MEOK AI = OpenRouter of everything
18. Wire RunPod serverless endpoints as "providers" with health probes (scale-to-zero aware ccx)
19. Catalog sweep: capture top-30 OR models (usage rank, price, context) into honey/sov_kb (data-gen business)
20. Reconcile our 12-model DSH catalog vs OR catalog (elder estate note: DSH is a tenant, OR is a peer)
21. Cost model: OR credits vs direct RunPod; when to route DIRECT (RunPod) vs VIA (OpenRouter) — margin table
22. OpenRouter top-up / BYOK registration (NICK GATE: account + $) — otherwise step 12-13 are read-only
23. Learn OR moderation/data postures (what OR anonymizes) — mirrors our honest-data stance
24. Prototype OR client in gateway: call OR via BYOK for frontier fallback when RunPod workers 500
25. Stress: 1k routed calls across 8 providers, log latency/price/502 rates -> routing table v1
26. Ship gateway v2 :8877 (restart-unbind-safety: systemd-style keepalive for the pod? gateway stays on Mac? -> pod next)
27. Move gateway to pod (node exists there; tunnel flips) — Mac only hosts DSH + portal

## PHASE 2 — LEARN LM ARENA (steps 28-40)
28. Read LMArena methodology: random-pair battles, hidden Elo + bootstrap CIs (benchlm.ai blog)
29. Read style/setup details: length-control, style-control battles, category leaderboards (botnation.ai)
30. Compare judge styles: LLM-judge (strong judge) vs crowd votes vs rule judges — pick ours (DORADO mixed)
31. Map our meok_arena.py to Arena semantics: random pairing, hidden reference, winner + preference pair
32. Add Elo engine (Bradley-Terry, bootstrap CI 95%) to /ledger — honest Elo, NO fabrication
33. Add category leaderboards: safe/code/legal/domain axes (aligns with 21-axis engine)
34. Battle protocol v2: style-matched pairs (minimize judge bias), 4 rounds, judge = 2-model ensemble
35. Battle protocol v3: human-verifiable subset (10% of battles shown verbatim in /ledger)
36. Write ARENA_METHODOLOGY.md (public-grade doc — our measurement body voice)
37. Cross-check our Elo vs known anchors (run same tasks on 3 known models) — calibration test
38. Add arena API /v1/battles (data-gen product: battle records are the sellable dataset)
39. Enrich battle records: task, probe family, verdicts, latency, chosen head — the "LM Arena data"
40. Optional: study submissions — how orgs submit models to LMArena (api-based) for OUR entry later (NICK GATE: identity/eligibility)

## PHASE 3 — LEARN THE FRONTIER (steps 41-52)
41. Baseline frontier via our keys: 8 providers x 3 flagship tasks (GOVBENCH-style refusal + legal + code)
42. Mine top-OR models' behavior on our 6-task MEOK set (which refuse properly? which comply wrongly?)
43. Build "teacher table": rank providers by arena verdicts (our honest leaderboard of the frontier)
44. Record frontier refusal styles (soft/hard/tone) — distillable style grammar for our 0.5B
45. Record frontier COMPLY styles (legal answers with citations) — distillable for OOWM answers
46. Extract repeatable "verdict chains" (task->gate->answer shape) — training templates for data-gen
47. Learn category winners' tricks (math: check-and-verify; coding: tests-first) via sampled outputs
48. Ablation: same task, 8 providers -> which judge verdicts agree? (inter-judge reliability study)
49. Store everything into sovereign-distill-corpus.jsonl (raw) + honey (event stream)
50. Publish FRONTIER_TEACHER_TABLE.md on volume (evidence, not claim)
51. Note GSPC-adjacent gaps: what axes frontier models fail (their UNMEASURED spots) — differentiation
52. Feed findings into domain-packs (RAS/MEOK front) — the "sell verdicts" line

## PHASE 4 — IMPROVE OURS (steps 53-78)
53. Upgrade distill_corpus.py: MODELS = 8 provider keys (deepseek-chat, claude-3-5-haiku, gpt-4o-mini, gemini-2.0-flash, llama-3.3-70b-ver, mistral-small, together, perplexity)
54. Run live distillation: 8 providers x 6 tasks x 2 temps -> judge-verified completions (corpus 12 -> ~60-80)
55. Multi-task expansion: 12 task scenarios (add code-compliance, data-protection, medical, finance)
56. Build sovereign-sft-v3 dataset on pod (harness git tracks it; volume stores it)
57. Train SFT v3 on POD (150 steps -> 300 steps; CPU-safe) — sov-minimal-output-v3
58. Eval v3 with eval_student.py (6-task arena verdicts) — target 4/6 -> 6/6 (with gate: 6/6)
59. Compare v2 vs v3 vs base vs gate (honest table) — publish SFT_LEDGER.md
60. Add law-RAG at eval time: dorado_gate + law_kb retrieval -> measure delta (RAG >= best parent test)
61. Trial output-fusion (neural + RAG answer fusion) — the only honest fusion per our law
62. Re-test MMLU OOWM (41.5% baseline; target: stay honest, report delta)
63. GOVBENCH re-run (0.931; regression gate: must not drop)
64. COMPBENCH re-run (84.5%; regression gate)
65. DEFBENCH re-run (refusal 1.000 / over-block 0.000; regression gate)
66. Arena entry: sovereign (gated) enters our own Elo ladder vs 8 frontier teachers (honest placement)
67. Corpus mining from arena winners: 100+ preference pairs (chosen/rejected) — the data-gen product
68. Retrain cycle 2 (v4) on 100+ pairs + distillation; steps scaled to corpus
69. Teacher-improvement funnel: replace worst teacher with winner (adaptive teacher selection)
70. Try GRPO-lite (from sov_grpo_train.py) on pod for refusal shaping (care floor enforcement)
71. If v4 >= v3: promote; commit weights NOT to git (volume only) + hash manifest (honest reproducibility)
72. Register model card: sovereign-sov33 card (family, base, method, measured scores) — SOVOS canonical
73. Write MEASUREMENT_PACK.md per axis (documented axes, sample counts, dates) — certification-grade docs
74. Self-audit: honesty check (no measured->claimed inflation; every number has provenance line)
75. Publish on domain pack front (RAS product): sovereign measured results page (csoai.site)

## PHASE 5 — EAT + MELD (steps 79-100) [in flight]
79. EAT remote proof cycle verified (log has PHASE_8 deploy ok remotely)
80. EAT pod cron healthy 3+ days (honey grows from pod)
81. EAT extended: add arena events as honey producer (battle records -> honey)
82. EAT extended: add KB clauses from frontier teacher table
83. EAT extended: add "MIN' phase from /workspace/offload-dsh/clawd (remote corpus mining)
84. Weekly EAT report published (measured baseline vs weekly delta; honest)
85. Weekly sweep: restore test (clone harness fresh on Oracle -> runs -> clean) — backup VERIFIED, not assumed
86. Monthly check: RunPod balance burn vs EAT/Arena value (cost discipline: gateway margin report)
87. Plan: migrate sov33-unified (0.889->0.931 champion) judge+gate stack to run as ONE pod service (sovos-light A100)
88. Consolidate: DSH settings point at REMOTE services (pod gateway, pod ollama via tunnel) — Mac thin
89. DSH GUI: add remote model sources (gateway via tunnel) so DSH sees estate models
90. Knowledge: transfer all findings to shared-knowledge intel (cross-terminal law)
91. Business: MEOK arena data product = signed battle batches (council-sign) via council-measure
92. Business: RAS front + AGUI wired to gateway /ledger (verdicts sellable)
93. Publish methodology to board posture (measurement contributions to standards bodies)
94. IP: OIN scope check for any arena/routing patent-adjacent work (mandatory rule)
95. Security: rotate S3 keys into pod secrets (600) — keep S3 workflow on pod end
96. Security: gateway API key usage (only needed provider keys passed per request)
97. Resilience: pod outage drill (Mac still serves EAT; tunnel idempotent reconnect)
98. Resilience: volume snapshot cadence (RunPod volume backups or rsync to second volume)
99. Metric dashboard: Elo trend, corpus size, KB size, EAT completions — single METRICS.json
100. Lock: SOVOS_ESTATE_STATE.md canonical + sigil (measured, not claimed)

---
## NOW EXECUTING (this turn): steps 53-55 (multi-provider distillation) + 3-5 verification
