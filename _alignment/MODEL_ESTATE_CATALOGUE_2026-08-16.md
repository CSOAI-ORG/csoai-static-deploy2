# Model Estate Catalogue — Council of AI (2026-08-16, RunPod 3090 lane)

> Mining the models we OWN. Registered from real weights, never from a name.
> "A model NAME is not a model — join on weights." Honest register: measured, not certified.

## Registered ollama models (all loadable, on 3090 pod /workspace/ollama)
| Model | Size | Base | Provenance | Mini-bench gov (n=8) | Verdict |
|---|---|---|---|---|---|
| council-safe | 994MB | Qwen2.5-1.5B | refusal-lora-repull/merged (full ckpt: config+tokenizer+weights) | **5/8**, breaks label-collapse, correct PROHIBITED on Art 5(1)(c) | ✅ GENUINE improvement over base |
| council-oowm | ~943MB | Qwen2.5-1.5B | oowm_merge_v1 (full ckpt) | 0/8 (no parseable label — not instruction-following) | ⚠️ registered but UNMEASURED-useful; do not claim |
| qwen2.5:1.5b | 986MB | — | base (HF) | 4/8 but label-collapsed (always HIGH_RISK) | base bias noted |
| qwen2.5:7b | 4.7GB | — | base | (larger; bench-worthy) | — |
| qwen3:4b | 2.5GB | — | base | — | thinking-mode model |
| mistral:7b | 4.4GB | — | base | — | — |
| qwen2.5:0.5b-instruct | 397MB | — | base | — | arena workhorse |

## Registered this session (real weights → ollama)
- `council-safe` — Modelfile.council-safe (Qwen2.5 chat template + stop tokens + sovereign SYSTEM). `ollama create council-safe -f Modelfile.council-safe` → SUCCESS, id 4562353ae0c2
- `council-oowm` — Modelfile.council-oowm. `ollama create council-oowm` → SUCCESS (holds OOWM clan worldview merge; not verified for classification task yet)

## LoRA adapters (weights, unattached — need base to merge)
- `fix_runs/BEST/adapter_model.safetensors` (8.4MB) — Qwen2.5-1.5B LoRA, lora_alpha 16
- `fix_runs/20260814T*/adapter/adapter_model.safetensors` (8.4MB ×8) — training iterations
- `asi_results/adapters/lora_c1_final`, `lora_c2_final` (4.2MB each) — ASI round adapters
- `p5/sov33-v12/adapter/adapter_model.safetensors` (71MB) — sov33 v12 adapter

## Full merges (complete checkpoints)
- `refusal-lora-repull/merged/model.safetensors` (943MB) — refusal-safety applied ✓ (→ council-safe)
- `oowm_merge_v1/model.safetensors` (943MB) — OOWM worldview merge ✓ (→ council-oowm)
- `fix_runs/20260814T043155Z/adapter/model.safetensors` (1.1GB) — biggest full merge (no tokenizer in dir, candidate for tokenizer graft)

## Defunct / NOT mineable (honest)
- 8 sovereign Modelfiles in `sovos-repo/` (`Modelfile.sov-*`, `sov33-evolved-*`) — all `FROM` Mac-local blob paths (`/Users/nicholas/.ollama/blobs/...`) that do NOT resolve on this pod. These are Mac-origin build recipes, NOT weights. Do not count them as models.
- `sov_3kb_converter.py` / `sov_auto_convert.py` are sigil/training-pair compressors, not ollama importers.

## Method
- Registry = `ollama create <name> -f Modelfile.<name>` from the FULL checkpoint dir (config+tokenizer+safetensors)
- Modelfile MUST have FROM → real dir, TEMPLATE (chat template matching base), PARAMETER stop tokens, sovereign SYSTEM
- Mini-bench: board_items_govbench.json slice, temperature 0, substring label match

## Next scaling
1. Graft tokenizer onto the 1.1GB merge → register a 3rd named model
2. Run full-24-item gov bench on council-safe vs base (formal delta)
3. Wire council-safe into the arena pick-list as a contestant
4. If HF token restored: push refusal merge to HF models namespace as public checkpoint