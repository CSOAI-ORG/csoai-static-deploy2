# Model Estate Catalogue — Council of AI (2026-08-16, RunPod 3090 lane)

> Mining the models we OWN. Registered from real weights, never from a name.
> "A model NAME is not a model — join on weights." Honest register: measured, not certified.

## Registered ollama models (all loadable, on 3090 pod /workspace/ollama)
| Model | Size | Base | Provenance | Full-board gov (n=24, acc/macroF1) | Verdict |
|---|---|---|---|---|---|
| mistral:7b | 4.4GB | — | base (HF) | **0.542 / 0.536** | 🏆 best classifier |
| qwen2.5:7b | 4.7GB | — | base (HF) | 0.542 / 0.360 | 2nd |
| qwen2.5:1.5b | 986MB | — | base (HF) | 0.458 / 0.293 | base bias |
| qwen2.5:0.5b-instruct | 397MB | — | base (HF) | 0.292 / 0.170 | — |
| council-safe | 994MB | Qwen2.5-1.5B | refusal-lora-repull/merged | **0.250 / 0.135** | ⚠️ CORRECTED — early 5/8 was an easy subset; full-board BELOW base, not a generalised win |
| qwen3:4b | 2.5GB | — | base | 0.000 / 0.000 | parse-fail (thinking model, wrong template for label parse) |
| council-oowm | ~943MB | Qwen2.5-1.5B | oowm_merge_v1 | 0.000 / 0.000 | ⚠️ not instruction-following; unmeasured-useful only |

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