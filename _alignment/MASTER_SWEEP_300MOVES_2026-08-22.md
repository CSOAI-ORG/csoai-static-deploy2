# MASTER SWEEP — Audit + Next 300 Moves (2026-08-22) · Directed by Nicholas

Scope: full alignment, offload Mac → RunPod/Oracle, audit everything (done/not-done), drive every
aspect to production-ready 100/100 + EAT. Everything below is from this session's work/measurements
unless marked [planned].

## 0. MAC DISK — CRITICAL (the driver)
**Mac disk = 176Mi free (99% used).** Biggest: `~/clawd` 26G · `~/sim-world-data` 10G · `~/.ollama` 5.5G ·
`~/projects/coai-dashboard` 2.2G · `~/Desktop` 1.2G.
**Offload targets found:** oracle-micro-2 (141.147.73.85) **31G free** · oracle-micro (145.241.232.16) 9.5G ·
RunPod pods (sov-brain-2, sovos-light-a100). rclone NOT on PATH (config has only `[gdrive]`).

## 1. ESTATE AUDIT — DONE ✅ (verified this session)
- **DSH harness**: root cause fixed (disk 2.8→~5Gi freed, latency 0.09→0.005s). 13 providers wired
  (12 catalog vendors + estate). `runpod-a100` (11 models) + `owem-estate` (73 models) wired + verified.
  SSH `sovos-light-a100` alias fixed (40637→15094). Config valid, DSH healthy.
- **Neurosymbolic OOWM** (`dorado_gate.py` + `law_kb.py` + `run_govbench_ns3.py`): GOVBENCH **0.931**,
  DEFBENCH **refusal 1.000/over-block 0.000**, COMPBENCH **84.5%** (governance 46.7%). Best stack =
  `sov33-unified` + gate + law-RAG + pillar-RAG (mine-confirmed).
- **Router** (learning): SOVOS goal = 1 large core + 3 specialist students + care-gate + sign + memory.
  RAG EXCEEDS best parent (84.2% vs 78.9%); route to best (RouteLLM). Frontier funded core = **DeepSeek**
  (MMLU 78.5%); OpenRouter 402 (no credits), Anthropic 401 (bad key).
- **Docs learned**: `_alignment/MASTER_PLAN_FUSION_OWEM.md`, `MODEL_FUSION_PLAYBOOK`, `EAT725_OWEM_FUSION_PLAYBOOK`,
  `train_ttt.py` (LTTTA Track-2), `~/Desktop/SOVOS GOAL.txt` (filesystem-err, use `~/Downloads/SOVOS_GOAL_DOC_FRESH_MINED_INTEL.md`).

## 2. ESTATE AUDIT — NOT DONE / GATED ⚠️
- **GSPC** UNMEASURED (signed issuance metered/paid on keystone). **flywheel** UNMEASURED (`fuel.pairs=0`).
- **MuCoCo** (code-consistency) not set up/harness. **SOV3 :3101** down (was GCP-narrative; confirm real host).
- **OpenRouter credits 0** (402) → qwen3.7-max unreachable. **Anthropic key dead** (401).
- **sov-light OOWM** = `council-oowm`/`council-oowm-hardened` on the runpod-a100; no separate model found.

## 3. THE SWEEP — PHASES (production-ready roadmap)
### Phase A — Offload Mac → RunPod/Oracle (frees the Mac for NN/training) [IN PROGRESS]
- A1. rsync `~/.ollama` → oracle-micro-2 (running: bg job bash-43). Then verify + free local (5.5G).
- A2. Pause sim-world lane → rsync `~/sim-world-data` (10G) → oracle-micro-2; verify; free local.
- A3. rsync `~/projects/coai-dashboard` build artifacts + regenerable caches → Oracle; free local.
- A4. Move `~/clawd` non-live docs/artifacts → Oracle/RunPod volume; keep only live needs.
- A5. Verify MD5/EOT on Oracle; delete local ONLY after verified (offload ≠ delete until confirmed).
- A6. Stand up rclone (RunPod object storage) or an rsync cron from Mac→Oracle micros as the durable
      offload rail. Point watch-crons at the offloaded paths (not Mac).

### Phase B — Router to BEST (production gate) [PLANNED]
- B1. Wire the DSH/sov-core router: general → **DeepSeek (frontier, funded, 78.5%)** as the large core;
      governance/safety → sovereign OOWM + `dorado_gate` + `law_kb` RAG (0.931/1.0).
- B2. Add the 3 specialist students + care-gate + signature + memory under the large core (the SOVOS goal).
- B3. Make the specific frontier reachable: top up OpenRouter / fix Anthropic key, or use DeepSeek only.

### Phase C — Production-readiness (100/100 A++++) [PLANNED]
- C1. Fix GSPC (enable keystone signed-issuance) + flywheel fuel lanes → complete "top on all".
- C2. Set up MuCoCo harness → run on the sovereign + frontier for the code-consistency axis.
- C3. Publish the OOWM + demo + benchmark cards to the front-end/pods (csoai.org / RunPod / Oracle), SIGIL-signed.
- C4. Add care-gate + signing + memory end-to-end (governed ship — audit trail on every decision).
- C5. EAT loop: daily eat → RAG/honey → IWM → retrain/distill → re-bench (practice/held-out) → improve.

## 4. VERIFIED NUMPBERS (honest, this session)
GOVBENCH 0.931 (was 0.448) · DEFBENCH refusal 1.000/0.129 bare · COMPBENCH 84.5% · MMLU local OOWM 41.5%
vs DeepSeek frontier 78.5% (0-shot N=65) · RAG exceeds best parent 84.2% vs 78.9% · DSH 20× faster.
