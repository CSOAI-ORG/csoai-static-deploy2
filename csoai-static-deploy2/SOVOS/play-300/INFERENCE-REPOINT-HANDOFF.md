# INFERENCE RE-POINT HANDOFF (2026-08-22)

**GCP retired → inference is RunPod + Oracle.** This changed the tunnel topology; the toolchain
still defaults to a stale port.

## Root cause
- `localhost:11434` = SSH bridge → **A100 sibling** `l7g747oivyq6ab` (DO NOT TOUCH, sibling lane).
- Working backends: **`11439` = 3090 `fpowppss5ngtkw` WORKHORSE** · `11436`/`11437` = Oracle micros.
- Verified: `qwen2.5:7b` on 11439 returns clean chat (`done:stop`); EAT now produces real numbers.

## Systemic issue
~97 Python files hardcode `http://localhost:11434` (grep `11434` in `csoai-static-deploy2/*.py`).
These now hit the sibling or a dead port. Several already honor env overrides:
- `OLLAMA_URL` (sov_orchestrator, asi_evolution, unified_free_pipeline, distributed_evolution)
- `SOV_OLLAMA_URL` (sov_master, sov7_catalog, sov7_swarm_evolve)
- `RUNPOD_OLLAMA_URL` (sov6_stack)
- `OLLAMA_CHAT` (eat_run_local — added this session)

## Fix recipe (LANE, one PR)
Standardize every hardcode to: `os.environ.get("OLLAMA_URL", "http://localhost:11434")`, then run
the fleet with `OLLAMA_URL=http://localhost:11439`. A safe sed (review before merge):
```
rg -l 'localhost:11434' --glob '*.py' | xargs sed -i '' \
  's#http://localhost:11434#os.environ.get("OLLAMA_URL", "http://localhost:11434")#g'
```
Do NOT touch: sibling-lane files, `sov6_stack.py` (already env-aware), `free_gpu/tab2_m2_lan.py`
(M2 LAN, different host).

## Corrupted-model flags (rebuild tickets)
- `council-oowm:latest` on 11439 emits garbage `????` → rebuild from a clean base.
- `muse-glimmer:latest` — unverified, flag for a probe before any public claim.

## What I already fixed
- `eat_run_local.py`: `OLLAMA_CHAT` env + honest `UNMEASURABLE` + leaderboard `None`-safe.
- `citation_verify.py`: SB 315 / Decree 142 / KI-MIG / RFC 9942/9943 added as KNOWN instruments.

## Honest gate (unchanged)
POD signing key still unset → estate receipts honest-UNSIGNED. Inject `COUNCIL_SIGN_KEY` to flip
to stranger-verifiable.
