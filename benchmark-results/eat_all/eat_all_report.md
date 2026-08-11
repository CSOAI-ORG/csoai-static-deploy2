# EAT_ALL Run Report

**Run ID**: eat_all_1786455391
**Finished**: 2026-08-11T13:36:31.395714+00:00
**Phase summary**: {'ran': 18, 'failed': 1, 'skipped': 0}

## Phases

| Phase | Status | Duration | Notes |
|---|---|---|---|
| PHASE_0_HEALTH | ran | 4.2s | sov_local_status=unreachable: HTTP Error 404: Not Found; ollama_models=2; kb_entries=4412 |
| PHASE_1_REBOARD | ran | 1.0s | exit_code=0 |
| PHASE_2_KB_GROW | ran | 1.4s | exit_code=0 |
| PHASE_3_PROBES | ran | 0.0s | chatml=1; bloodline=1 |
| PHASE_4_TRAINING | ran | 0.0s | training_scripts_available=['sov_groq_distill.py', 'sov_grpo_train.py', 'sov_minimal_train.py'] |
| PHASE_5_HONEY | ran | 2.0s | exit_code=0; events=2733 |
| PHASE_6_DOWNLOADS | failed | 6.5s | (no error message) |
| PHASE_7_PORTAL | ran | 2.0s | exit_code=0 |
| PHASE_9_ARTIFACTS | ran | 2.1s | deck_cards=54; kb_entries=4412; kb_ok=True |
| PHASE_9B_EXTERNAL_HARNESS | ran | 1.8s | clans_routed=0; swarm_id=owem-clans-1786455358 |
| PHASE_9C_OWEM_CLUSTER | ran | 0.6s | clusters_routed=0 |
| PHASE_9D_BENCHMARKS_HARNESS | ran | 0.4s | benchmarks_routed=0 |
| PHASE_9E_TRAINING_DATA_HARNESS | ran | 2.3s | data_sources_routed=0 |
| PHASE_9F_SOVEREIGN_TRAINING_PIPELINE | ran | 1.1s | stages_routed=0 |
| PHASE_9G_AUDIENCE_HARNESS | ran | 1.0s | audiences_routed=0 |
| PHASE_9H_SOV_HIVE_HARNESS | ran | 4.7s | kb_entries_added=7; exit_code=0 |
| PHASE_9I_SOV_CAPTURE | ran | 19.5s | events_processed=0; skills_extracted=0; refine_output=KB Refinery — processing today's capture events...
  terminal: 0 events
  browser: 0 events
  files: 0 events
  chat: 0 events
  No events to refine.
; extract_output=GNN Spine — extracting patterns from capture events...
  No terminal events today.
 |
| PHASE_9J_IWM_BOOTSTRAP | ran | 2.2s | iwm_records=0; kb_entries_added=0; exit_code=0 |
| PHASE_10B_MODEL_ROUTING | ran | 1.1s | models_routed=0; specs_routed=1 |

## Artifacts

- `/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/eat_all/sov_kb.json`
- `/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/eat_all/honey_all_producers.jsonl`
- `/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/eat_all/honey_layer0.jsonl`
- `/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/eat_all/honey_downloads.jsonl`
- `/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/eat_all/gpu_inventory.json`
- `/Users/nicholas/clawd/csoai-static-deploy2/benchmark-results/eat_all/tier0_routers.json`
- `/Users/nicholas/clawd/csoai-static-deploy2/forest/jspace_deck.json`
- `/Users/nicholas/clawd/csoai-static-deploy2/forest/c_space_card.json`s/nicholas/clawd/csoai-static-deploy2/forest/c_space_card.json`