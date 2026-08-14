# EAT_ALL Run Report

**Run ID**: eat_all_1786716703
**Finished**: 2026-08-14T14:11:43.952110+00:00
**Phase summary**: {'ran': 17, 'failed': 2, 'skipped': 0}

## Phases

| Phase | Status | Duration | Notes |
|---|---|---|---|
| PHASE_0_HEALTH | ran | 78.8s | sov_local_status=unreachable: <urlopen error [Errno 61] Connection refused>; ollama_status=unreachable: Command '['ollama', 'list']' timed out after 5 seconds; kb_entries=9193 |
| PHASE_1_REBOARD | ran | 19.9s | exit_code=0 |
| PHASE_2_KB_GROW | ran | 9.6s | exit_code=0 |
| PHASE_3_PROBES | ran | 0.4s | chatml=1; bloodline=1 |
| PHASE_4_TRAINING | ran | 0.0s | training_scripts_available=['sov_groq_distill.py', 'sov_grpo_train.py', 'sov_minimal_train.py'] |
| PHASE_5_HONEY | ran | 22.6s | exit_code=0; events=4676 |
| PHASE_6_DOWNLOADS | failed | 11.4s | (no error message) |
| PHASE_7_PORTAL | ran | 25.6s | exit_code=0 |
| PHASE_9_ARTIFACTS | ran | 15.8s | deck_cards=55; kb_entries=9200; kb_ok=True |
| PHASE_9B_EXTERNAL_HARNESS | ran | 7.4s | clans_routed=0; swarm_id=owem-clans-1786716508 |
| PHASE_9C_OWEM_CLUSTER | ran | 7.3s | clusters_routed=0 |
| PHASE_9D_BENCHMARKS_HARNESS | ran | 18.1s | benchmarks_routed=0 |
| PHASE_9E_TRAINING_DATA_HARNESS | ran | 16.8s | data_sources_routed=0 |
| PHASE_9F_SOVEREIGN_TRAINING_PIPELINE | ran | 14.0s | stages_routed=0 |
| PHASE_9G_AUDIENCE_HARNESS | ran | 10.1s | audiences_routed=0 |
| PHASE_9H_SOV_HIVE_HARNESS | ran | 60.3s | kb_entries_added=8; exit_code=0 |
| PHASE_9I_SOV_CAPTURE | failed | 46.7s | Command '['python3', '/Users/nicholas/clawd/csoai-static-deploy2/sov_capture.py', '--status']' timed |
| PHASE_9J_IWM_BOOTSTRAP | ran | 15.3s | iwm_records=0; kb_entries_added=0; exit_code=0 |
| PHASE_10B_MODEL_ROUTING | ran | 5.4s | models_routed=0; specs_routed=1 |

## Artifacts

- `/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/eat_all/sov_kb.json`
- `/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/eat_all/honey_all_producers.jsonl`
- `/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/eat_all/honey_layer0.jsonl`
- `/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/eat_all/honey_downloads.jsonl`
- `/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/eat_all/gpu_inventory.json`
- `/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/eat_all/tier0_routers.json`
- `/Users/nicholas/clawd/csoai-static-deploy2/forest/jspace_deck.json`
- `/Users/nicholas/clawd/csoai-static-deploy2/forest/c_space_card.json`