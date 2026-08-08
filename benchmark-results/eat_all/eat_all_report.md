# EAT_ALL Run Report

**Run ID**: eat_all_1786198782
**Finished**: 2026-08-08T14:19:42.690672+00:00
**Phase summary**: {'ran': 13, 'failed': 6, 'skipped': 0}

## Phases

| Phase | Status | Duration | Notes |
|---|---|---|---|
| PHASE_0_HEALTH | ran | 25.9s | sov_local_status=unreachable: <urlopen error [Errno 61] Connection refused>; ollama_models=3; kb_entries=328078 |
| PHASE_1_REBOARD | ran | 5.5s | exit_code=0 |
| PHASE_2_KB_GROW | ran | 44.0s | exit_code=0 |
| PHASE_3_PROBES | ran | 0.2s | chatml=1; bloodline=1 |
| PHASE_4_TRAINING | ran | 0.0s | training_scripts_available=['sov_groq_distill.py', 'sov_grpo_train.py', 'sov_minimal_train.py'] |
| PHASE_5_HONEY | ran | 6.2s | exit_code=0; events=133 |
| PHASE_6_DOWNLOADS | ran | 6.6s | exit_code=1; files_mined=158 |
| PHASE_7_PORTAL | ran | 3.9s | exit_code=0 |
| PHASE_9_ARTIFACTS | ran | 10.1s |  |
| PHASE_9B_EXTERNAL_HARNESS | ran | 58.9s | clans_routed=0; swarm_id=owem-clans-1786198364 |
| PHASE_9C_OWEM_CLUSTER | ran | 17.5s | clusters_routed=0 |
| PHASE_9D_BENCHMARKS_HARNESS | ran | 38.4s | benchmarks_routed=0 |
| PHASE_9E_TRAINING_DATA_HARNESS | failed | 42.0s | [Errno 28] No space left on device |
| PHASE_9F_SOVEREIGN_TRAINING_PIPELINE | failed | 6.0s | Expecting value: line 5996183 column 21 (char 205012992) |
| PHASE_9G_AUDIENCE_HARNESS | failed | 6.0s | Expecting value: line 5996183 column 21 (char 205012992) |
| PHASE_9H_SOV_HIVE_HARNESS | failed | 3.2s | Expecting value: line 5996183 column 21 (char 205012992) |
| PHASE_9I_SOV_CAPTURE | failed | 300.3s | Command '['python3', '/Users/nicholas/clawd/csoai-static-deploy2/sov_capture.py', '--refine']' timed |
| PHASE_9J_IWM_BOOTSTRAP | ran | 2.3s | iwm_records=0; kb_entries_added=0; exit_code=1 |
| PHASE_10B_MODEL_ROUTING | failed | 1.5s | Expecting value: line 5996183 column 21 (char 205012992) |

## Artifacts

- `/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/eat_all/sov_kb.json`
- `/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/eat_all/honey_all_producers.jsonl`
- `/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/eat_all/honey_layer0.jsonl`
- `/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/eat_all/honey_downloads.jsonl`
- `/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/eat_all/gpu_inventory.json`
- `/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/eat_all/tier0_routers.json`