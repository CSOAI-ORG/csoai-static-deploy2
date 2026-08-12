# EAT_ALL Run Report

**Run ID**: eat_all_1786541020
**Finished**: 2026-08-12T13:23:40.535565+00:00
**Phase summary**: {'ran': 17, 'failed': 2, 'skipped': 0}

## Phases

| Phase | Status | Duration | Notes |
|---|---|---|---|
| PHASE_0_HEALTH | ran | 1.9s | sov_local_status=unreachable: <urlopen error [Errno 61] Connection refused>; ollama_models=2; kb_entries=5648 |
| PHASE_1_REBOARD | ran | 2.8s | exit_code=0 |
| PHASE_2_KB_GROW | ran | 1.2s | exit_code=0 |
| PHASE_3_PROBES | ran | 0.0s | chatml=1; bloodline=1 |
| PHASE_4_TRAINING | ran | 0.0s | training_scripts_available=['sov_groq_distill.py', 'sov_grpo_train.py', 'sov_minimal_train.py'] |
| PHASE_5_HONEY | ran | 6.7s | exit_code=0; events=3213 |
| PHASE_6_DOWNLOADS | failed | 8.8s | (no error message) |
| PHASE_7_PORTAL | ran | 6.4s | exit_code=0 |
| PHASE_9_ARTIFACTS | ran | 2.6s | deck_cards=55; kb_entries=5648; kb_ok=True |
| PHASE_9B_EXTERNAL_HARNESS | ran | 2.0s | clans_routed=0; swarm_id=owem-clans-1786540836 |
| PHASE_9C_OWEM_CLUSTER | ran | 1.9s | clusters_routed=0 |
| PHASE_9D_BENCHMARKS_HARNESS | ran | 2.2s | benchmarks_routed=0 |
| PHASE_9E_TRAINING_DATA_HARNESS | ran | 2.5s | data_sources_routed=0 |
| PHASE_9F_SOVEREIGN_TRAINING_PIPELINE | ran | 5.0s | stages_routed=0 |
| PHASE_9G_AUDIENCE_HARNESS | ran | 3.6s | audiences_routed=0 |
| PHASE_9H_SOV_HIVE_HARNESS | ran | 45.5s | kb_entries_added=7; exit_code=0 |
| PHASE_9I_SOV_CAPTURE | failed | 102.2s | Command '['python3', '/Users/nicholas/clawd/csoai-static-deploy2/sov_capture.py', '--status']' timed |
| PHASE_9J_IWM_BOOTSTRAP | ran | 13.7s | iwm_records=0; kb_entries_added=0; exit_code=0 |
| PHASE_10B_MODEL_ROUTING | ran | 4.4s | models_routed=0; specs_routed=1 |

## Artifacts

- `/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/eat_all/sov_kb.json`
- `/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/eat_all/honey_all_producers.jsonl`
- `/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/eat_all/honey_layer0.jsonl`
- `/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/eat_all/honey_downloads.jsonl`
- `/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/eat_all/gpu_inventory.json`
- `/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/eat_all/tier0_routers.json`
- `/Users/nicholas/clawd/csoai-static-deploy2/forest/jspace_deck.json`
- `/Users/nicholas/clawd/csoai-static-deploy2/forest/c_space_card.json`