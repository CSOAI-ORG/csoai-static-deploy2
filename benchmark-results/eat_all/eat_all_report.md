# EAT_ALL Run Report

**Run ID**: eat_all_1786196151
**Finished**: 2026-08-08T13:35:51.924034+00:00
**Phase summary**: {'ran': 18, 'failed': 1, 'skipped': 0}

## Phases

| Phase | Status | Duration | Notes |
|---|---|---|---|
| PHASE_0_HEALTH | ran | 4.5s | sov_local_status=unreachable: <urlopen error [Errno 61] Connection refused>; ollama_models=3; kb_entries=2619 |
| PHASE_1_REBOARD | ran | 7.4s | exit_code=0 |
| PHASE_2_KB_GROW | ran | 6.6s | exit_code=0 |
| PHASE_3_PROBES | ran | 0.2s | chatml=1; bloodline=1 |
| PHASE_4_TRAINING | ran | 0.0s | training_scripts_available=['sov_groq_distill.py', 'sov_grpo_train.py', 'sov_minimal_train.py'] |
| PHASE_5_HONEY | ran | 1.9s | exit_code=0; events=67 |
| PHASE_6_DOWNLOADS | ran | 7.7s | exit_code=1; files_mined=157 |
| PHASE_7_PORTAL | ran | 3.4s | exit_code=0 |
| PHASE_9_ARTIFACTS | ran | 0.0s |  |
| PHASE_9B_EXTERNAL_HARNESS | ran | 0.1s | clans_routed=0; swarm_id=owem-clans-1786196137 |
| PHASE_9C_OWEM_CLUSTER | ran | 0.1s | clusters_routed=0 |
| PHASE_9D_BENCHMARKS_HARNESS | ran | 0.1s | benchmarks_routed=0 |
| PHASE_9E_TRAINING_DATA_HARNESS | ran | 0.2s | data_sources_routed=0 |
| PHASE_9F_SOVEREIGN_TRAINING_PIPELINE | ran | 0.1s | stages_routed=0 |
| PHASE_9G_AUDIENCE_HARNESS | ran | 0.1s | audiences_routed=0 |
| PHASE_9H_SOV_HIVE_HARNESS | ran | 0.4s | kb_entries_added=7; exit_code=0 |
| PHASE_9I_SOV_CAPTURE | failed | 13.4s | Command '['python3', '/Users/nicholas/clawd/csoai-static-deploy2/sov_capture.py', '--status']' timed |
| PHASE_9J_IWM_BOOTSTRAP | ran | 0.4s | iwm_records=0; kb_entries_added=0; exit_code=0 |
| PHASE_10B_MODEL_ROUTING | ran | 0.1s | models_routed=0; specs_routed=1 |

## Artifacts

- `/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/eat_all/sov_kb.json`
- `/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/eat_all/honey_all_producers.jsonl`
- `/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/eat_all/honey_layer0.jsonl`
- `/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/eat_all/honey_downloads.jsonl`
- `/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/eat_all/gpu_inventory.json`
- `/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/eat_all/tier0_routers.json`