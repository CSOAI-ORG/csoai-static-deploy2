# EAT_ALL Run Report

**Run ID**: eat_all_1786200694
**Finished**: 2026-08-08T14:51:34.186699+00:00
**Phase summary**: {'ran': 19, 'failed': 0, 'skipped': 0}

## Phases

| Phase | Status | Duration | Notes |
|---|---|---|---|
| PHASE_0_HEALTH | ran | 3.1s | sov_local_status=unreachable: timed out; ollama_models=3; kb_entries=4928 |
| PHASE_1_REBOARD | ran | 0.1s | exit_code=0 |
| PHASE_2_KB_GROW | ran | 0.2s | exit_code=0 |
| PHASE_3_PROBES | ran | 0.0s | chatml=1; bloodline=1 |
| PHASE_4_TRAINING | ran | 0.0s | training_scripts_available=['sov_groq_distill.py', 'sov_grpo_train.py', 'sov_minimal_train.py'] |
| PHASE_5_HONEY | ran | 0.2s | exit_code=0; events=187 |
| PHASE_6_DOWNLOADS | ran | 6.0s | exit_code=1; files_mined=158 |
| PHASE_7_PORTAL | ran | 0.2s | exit_code=0 |
| PHASE_9_ARTIFACTS | ran | 0.0s |  |
| PHASE_9B_EXTERNAL_HARNESS | ran | 0.1s | clans_routed=0; swarm_id=owem-clans-1786200691 |
| PHASE_9C_OWEM_CLUSTER | ran | 0.1s | clusters_routed=0 |
| PHASE_9D_BENCHMARKS_HARNESS | ran | 0.1s | benchmarks_routed=0 |
| PHASE_9E_TRAINING_DATA_HARNESS | ran | 0.1s | data_sources_routed=0 |
| PHASE_9F_SOVEREIGN_TRAINING_PIPELINE | ran | 0.2s | stages_routed=0 |
| PHASE_9G_AUDIENCE_HARNESS | ran | 0.2s | audiences_routed=0 |
| PHASE_9H_SOV_HIVE_HARNESS | ran | 0.4s | kb_entries_added=7; exit_code=0 |
| PHASE_9I_SOV_CAPTURE | ran | 0.9s | events_processed=256; skills_extracted=1; refine_output=KB Refinery — processing today's capture events...
  terminal: 500 events (refine window 500)
  browser: 0 events
  files: 0 events
  chat: 0 events
  KB: 4935 → 5435 entries (+500 new)
  Saved to: /Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/sov_kb.json
; extract_output=GNN Spine — extracting patterns from capture events...
  Extracted 1 unique skills
  Skills file: /Users/nicholas/.sov/iwm/skills_20260808.jsonl
  KB updated: 5436 entries total
 |
| PHASE_9J_IWM_BOOTSTRAP | ran | 0.2s | iwm_records=0; kb_entries_added=0; exit_code=0 |
| PHASE_10B_MODEL_ROUTING | ran | 0.1s | models_routed=0; specs_routed=1 |

## Artifacts

- `/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/eat_all/sov_kb.json`
- `/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/eat_all/honey_all_producers.jsonl`
- `/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/eat_all/honey_layer0.jsonl`
- `/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/eat_all/honey_downloads.jsonl`
- `/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/eat_all/gpu_inventory.json`
- `/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/eat_all/tier0_routers.json`