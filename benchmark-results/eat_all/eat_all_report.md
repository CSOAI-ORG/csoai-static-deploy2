# EAT_ALL Run Report

**Run ID**: eat_all_1786717666
**Finished**: 2026-08-14T14:27:46.908776+00:00
**Phase summary**: {'ran': 17, 'failed': 2, 'skipped': 0}

## Phases

| Phase | Status | Duration | Notes |
|---|---|---|---|
| PHASE_0_HEALTH | ran | 34.0s | sov_local_status=unreachable: <urlopen error [Errno 61] Connection refused>; ollama_status=unreachable: Command '['ollama', 'list']' timed out after 5 seconds; kb_entries=9217 |
| PHASE_1_REBOARD | ran | 24.2s | exit_code=0 |
| PHASE_2_KB_GROW | ran | 111.6s | exit_code=0 |
| PHASE_3_PROBES | ran | 3.2s | chatml=1; bloodline=1 |
| PHASE_4_TRAINING | ran | 0.0s | training_scripts_available=['sov_groq_distill.py', 'sov_grpo_train.py', 'sov_minimal_train.py'] |
| PHASE_5_HONEY | ran | 150.1s | exit_code=0; events=4676 |
| PHASE_6_DOWNLOADS | failed | 51.1s | (no error message) |
| PHASE_7_PORTAL | ran | 33.6s | exit_code=0 |
| PHASE_9_ARTIFACTS | ran | 34.0s | deck_cards=55; kb_entries=9217; kb_ok=True |
| PHASE_9B_EXTERNAL_HARNESS | ran | 20.6s | clans_routed=0; swarm_id=owem-clans-1786717403 |
| PHASE_9C_OWEM_CLUSTER | ran | 19.2s | clusters_routed=0 |
| PHASE_9D_BENCHMARKS_HARNESS | ran | 12.7s | benchmarks_routed=0 |
| PHASE_9E_TRAINING_DATA_HARNESS | ran | 13.2s | data_sources_routed=0 |
| PHASE_9F_SOVEREIGN_TRAINING_PIPELINE | ran | 14.7s | stages_routed=0 |
| PHASE_9G_AUDIENCE_HARNESS | ran | 15.2s | audiences_routed=0 |
| PHASE_9H_SOV_HIVE_HARNESS | ran | 62.8s | kb_entries_added=7; exit_code=0 |
| PHASE_9I_SOV_CAPTURE | failed | 79.3s | Command '['python3', '/Users/nicholas/clawd/csoai-static-deploy2/sov_capture.py', '--status']' timed |
| PHASE_9J_IWM_BOOTSTRAP | ran | 19.8s | iwm_records=0; kb_entries_added=0; exit_code=0 |
| PHASE_10B_MODEL_ROUTING | ran | 22.8s | models_routed=0; specs_routed=1 |

## Artifacts

- `/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/eat_all/sov_kb.json`
- `/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/eat_all/honey_all_producers.jsonl`
- `/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/eat_all/honey_layer0.jsonl`
- `/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/eat_all/honey_downloads.jsonl`
- `/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/eat_all/gpu_inventory.json`
- `/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/eat_all/tier0_routers.json`
- `/Users/nicholas/clawd/csoai-static-deploy2/forest/jspace_deck.json`
- `/Users/nicholas/clawd/csoai-static-deploy2/forest/c_space_card.json`