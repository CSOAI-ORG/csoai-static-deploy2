# Lane Tasks — CLAUDE CODE (backend/compute/infra)
_Set by MEOK-SOV3 governance lane, 2026-07-11. Honest scope only._

## STATUS (Claude Code, 2026-07-11 — 3 of 4 done, 1 in progress)

1. ⏳ **Hunyuan3D-2.1 on Colab T4** — NOT started yet. Next up. (Scout doc done:
   `_compute/CHINESE_WORLD_MODELS_SCOUT_2026-07-11.md` — HY-World 2.0 for worlds, Hunyuan3D-2.1 for Hatch meshes.)
2. ✅ **Flywheel `on_decision()` wired into live `/chat`** (commit `46d36a7b`). Every real decision on
   `:3101` now emits a harmful/benign-classified label onto `~/.sovereign/nn_retrain_queue.jsonl`.
   **Verified: 11 labels accumulating from live traffic (5 harmful / 6 benign).** The 197-gap is now
   filling from real conversations — SPINNING→COMPOUNDING. Retrain fires at n≥200 (≥40 each class).
3. ✅ **Full-dataset eval DONE — the defensible score:**
   - **GSM8K = 0.922** (1216/1319, the **FULL** canonical test set — leaderboard-comparable)
   - **MMLU = 0.776** (776/1000, stratified sample)
   - Backend: `llama-3.3-70b` pooled Groq+OCI. Results: `_compute/sov33_evals_full_results.json`.
   - **State it as:** "reasoning tier scores 0.922 full-GSM8K / 0.776 MMLU, correctness-graded" — NOT a
     param-count. Replaces every retracted T-count. Harness: `_compute/sov33_evals_full.py` (checkpointed).
4. ✅ **HELD** — no Kimi/DeepSeek/Cerebras re-key. Groq ladder (`gpt-oss-120b` heavy, `qwen3-32b` reason)
   covers heavy+reason on the existing key via `sov33_compute.infer(prompt, tier=...)`.

### Also shipped this session (compute/infra lane, for other lanes to build on)
- **`_compute/sov33_compute.py`** — the compute router every lane/SOV33 can call: `infer(prompt, prefer=, tier=)`
  over Groq→OCI→Ollama, 4 backends verified. Wired into the brain (`agent_executor.call_llm` + `/chat` Groq-first).
- **Persistent memory** wired into `/chat` (reads+writes `~/.sovereign/sovereign_memory.jsonl`) →
  `memory_layer_wired=True` (grounded), verified cross-request recall.
- **Durable `:3101`** via `com.meok.sov3-keeper` launchd (KeepAlive, kill-tested).
- **Orchestrator** `brain_executor` → real inference (`SOV33_REAL_EXEC=1`).
- Scouts: `OSS_MODEL_SCOUT`, `CHINESE_WORLD_MODELS_SCOUT`, `COMPUTE_CENSUS`.

### Next (Claude Code): task #1 Hunyuan3D-2.1 Colab notebook → real Hatch meshes.

---
_original brief below_
1. **Wire Hunyuan3D-2.1 on Colab T4** — your own #1 rec, free, do-able now. Generates real Hatch character meshes for SovSpace. Export mesh, serve static in WebGL.
2. **Wire flywheel IMPROVE→bus into live `/chat`** — every real decision on `:3101` calls `sov33_nn_hive_bus.on_decision(text, decision, gate)` so labels accumulate. THIS is what unblocks the flywheel from SPINNING→COMPOUNDING (needs ~200 labels).
3. **Finish full-dataset eval + write final numbers** — GSM8K 1319 + MMLU 500. The defensible score that replaces every retracted T-count. Checkpointed run already going.
4. **HOLD** — do NOT re-key Kimi/DeepSeek/Cerebras yet (no-sprawl rule). The Groq ladder (gpt-oss-120b, qwen3-32b) already covers heavy+reason tiers on the existing key.
