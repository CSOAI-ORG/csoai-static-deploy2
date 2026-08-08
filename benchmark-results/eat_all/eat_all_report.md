# EAT_ALL Run Report

**Run ID**: eat_all_1786198188
**Finished**: 2026-08-08T14:09:48.639734+00:00
**Phase summary**: {'ran': 18, 'failed': 1, 'skipped': 0}

## Phases

| Phase | Status | Duration | Notes |
|---|---|---|---|
| PHASE_0_HEALTH | ran | 22.4s | sov_local_status=unreachable: <urlopen error [Errno 61] Connection refused>; ollama_models=3; kb_entries=328070 |
| PHASE_1_REBOARD | ran | 5.1s | exit_code=0 |
| PHASE_2_KB_GROW | ran | 32.8s | exit_code=0 |
| PHASE_3_PROBES | ran | 0.1s | chatml=1; bloodline=1 |
| PHASE_4_TRAINING | ran | 0.0s | training_scripts_available=['sov_groq_distill.py', 'sov_grpo_train.py', 'sov_minimal_train.py'] |
| PHASE_5_HONEY | ran | 1.5s | exit_code=0; events=133 |
| PHASE_6_DOWNLOADS | ran | 3.7s | exit_code=0; files_mined=158 |
| PHASE_7_PORTAL | ran | 0.8s | exit_code=0 |
| PHASE_9_ARTIFACTS | ran | 2.6s |  |
| PHASE_9B_EXTERNAL_HARNESS | ran | 15.3s | clans_routed=0; swarm_id=owem-clans-1786197989 |
| PHASE_9C_OWEM_CLUSTER | ran | 10.3s | clusters_routed=0 |
| PHASE_9D_BENCHMARKS_HARNESS | ran | 14.3s | benchmarks_routed=0 |
| PHASE_9E_TRAINING_DATA_HARNESS | ran | 20.5s | data_sources_routed=0 |
| PHASE_9F_SOVEREIGN_TRAINING_PIPELINE | ran | 9.3s | stages_routed=0 |
| PHASE_9G_AUDIENCE_HARNESS | ran | 29.1s | audiences_routed=0 |
| PHASE_9H_SOV_HIVE_HARNESS | ran | 24.4s | kb_entries_added=7; exit_code=0 |
| PHASE_9I_SOV_CAPTURE | failed | 60.2s | Command '['python3', '/Users/nicholas/clawd/csoai-static-deploy2/sov_capture.py', '--refine']' timed |
| PHASE_9J_IWM_BOOTSTRAP | ran | 17.2s | iwm_records=0; kb_entries_added=0; exit_code=0 |
| PHASE_10B_MODEL_ROUTING | ran | 12.6s | models_routed=0; specs_routed=1 |

## Artifacts

- `/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/eat_all/sov_kb.json`
- `/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/eat_all/honey_all_producers.jsonl`
- `/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/eat_all/honey_layer0.jsonl`
- `/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/eat_all/honey_downloads.jsonl`
- `/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/eat_all/gpu_inventory.json`
- `/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/eat_all/tier0_routers.json`