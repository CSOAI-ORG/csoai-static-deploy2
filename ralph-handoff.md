# RALPH HANDOFF — free-OWEM routing objective
Start here. The estate is on RunPod pod sov-repull (SSH key ~/.runpod/ssh/runpodctl-ssh-key, port 23243, root@194.26.196.156). Work from the pod, not the Mac.

## WHAT IS DONE (verified, do not redo)
- EAT loop autonomous: axis_supervisor (mine+measure+sign+chain+board+backup+offline-sync threads),
  measure_chain, arena_loop_keeper, grok_referee, ops_daemons — all PPID=1 durable, runs overnight.
- Boards ~733, KB 5,726 signed, offline-index (KB/genome/board -> RAG volume) synced.
- Free sov-router (free_sov_router.py) built: routes GSPC probes to our best sov model per axis, COST £0.
- Free cross-eval (free_crosseval.py): sovereign (qwen3:4b-8k) acc=0.75 BEATS OpenRouter free frontier (0.0) — NO credits.
- Free sov models on pod: sov33-unified (2G), council-oowm, council-oowm-clean, qwen3:4b-8k, qwen3:32b, muse-glimmer.
- Dedicated bench ollama on :11435 (separate from main :11434) — parallel-safe.
- OpenRouter: 422 models, 22 free. API works but needs credits for paid (402). NOT required — our sov is the moat.

## NEXT (do these, in order)
1. FINISH the free sov-router: measure all 23 GSPC axes (not just the 6), persist free_sov_router.json
   (per-axis best sov model + scores). Measure on the dedicated bench server :11435 (parallel-safe).
2. Wire the route table into /api/model-router (Cloudflare function) + add to /api/tools discovery.
3. Wire routing into measure_chain (measure each axis with its champion sov model).
4. Kaggle free-GPU: copy the Mac kaggle token (~/.kaggle/kaggle.json) to the pod, mine free datasets into the KB.
5. Improve OURS: QLoRA fine-tune a sov variant on GSPC gap-axis failures, ouroboros-keep-only-if-improved.
6. Publish the honest sov-vs-frontier leaderboard at /api/gspc.

## SUBSTRATE
- OLLAMA_URL=http://localhost:11435 (dedicated bench), main=:11434. Signing key /root/.sovos/city_ed25519.
- PYTHON on pod has nacl, cryptography, requests. The sov-KB at /workspace/sovos-repo/benchmark-results/sov_kb.json.

## DOCTRINE
Measurement not certification. Honest negatives. Ouroboros (keep only if GSPC improves). Free-first (no OpenRouter credits). Online/offline (index has a durable offline copy).
