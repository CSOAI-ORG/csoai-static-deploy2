# EAT_ALL Run Report

**Run ID**: eat_all_1786541544
**Finished**: 2026-08-12T13:32:24.526637+00:00
**Phase summary**: {'ran': 17, 'failed': 2, 'skipped': 0}

## Phases

| Phase | Status | Duration | Notes |
|---|---|---|---|
| PHASE_0_HEALTH | ran | 31.0s | sov_local_status=unreachable: <urlopen error [Errno 61] Connection refused>; ollama_status=unreachable: Command '['ollama', 'list']' timed out after 5 seconds; kb_entries=5656 |
| PHASE_1_REBOARD | ran | 25.9s | exit_code=0 |
| PHASE_2_KB_GROW | ran | 10.6s | exit_code=0 |
| PHASE_3_PROBES | ran | 2.5s | chatml=1; bloodline=1 |
| PHASE_4_TRAINING | ran | 0.0s | training_scripts_available=['sov_groq_distill.py', 'sov_grpo_train.py', 'sov_minimal_train.py'] |
| PHASE_5_HONEY | ran | 58.9s | exit_code=0; events=3213 |
| PHASE_6_DOWNLOADS | failed | 35.2s | (no error message) |
| PHASE_7_PORTAL | ran | 11.2s | exit_code=0 |
| PHASE_9_ARTIFACTS | ran | 8.0s | deck_cards=55; kb_entries=5656; kb_ok=True |
| PHASE_9B_EXTERNAL_HARNESS | ran | 4.1s | clans_routed=0; swarm_id=owem-clans-1786541348 |
| PHASE_9C_OWEM_CLUSTER | ran | 5.8s | clusters_routed=0 |
| PHASE_9D_BENCHMARKS_HARNESS | ran | 11.4s | benchmarks_routed=0 |
| PHASE_9E_TRAINING_DATA_HARNESS | ran | 4.8s | data_sources_routed=0 |
| PHASE_9F_SOVEREIGN_TRAINING_PIPELINE | ran | 7.5s | stages_routed=0 |
| PHASE_9G_AUDIENCE_HARNESS | ran | 3.7s | audiences_routed=0 |
| PHASE_9H_SOV_HIVE_HARNESS | ran | 54.4s | kb_entries_added=7; exit_code=0 |
| PHASE_9I_SOV_CAPTURE | failed | 75.4s | Command '['python3', '/Users/nicholas/clawd/csoai-static-deploy2/sov_capture.py', '--status']' timed |
| PHASE_9J_IWM_BOOTSTRAP | ran | 19.3s | iwm_records=0; kb_entries_added=0; exit_code=0 |
| PHASE_10B_MODEL_ROUTING | ran | 12.4s | models_routed=0; specs_routed=1 |

## Artifacts

- `/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/eat_all/sov_kb.json`
- `/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/eat_all/honey_all_producers.jsonl`
- `/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/eat_all/honey_layer0.jsonl`
- `/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/eat_all/honey_downloads.jsonl`
- `/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/eat_all/gpu_inventory.json`
- `/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/eat_all/tier0_routers.json`
- `/Users/nicholas/clawd/csoai-static-deploy2/forest/jspace_deck.json`
- `/Users/nicholas/clawd/csoai-static-deploy2/forest/c_space_card.json`