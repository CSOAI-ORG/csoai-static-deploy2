
## 🚀 Run on Colab

Open directly in Colab T4 GPU free tier:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/gist/421dae75934ad2a836ea554c3ed55067)

# SOVEREIGN MERGE KIT — rung-4 "own weights from your configs"
## Fine-tune distinct experts → merge/upcycle → benchmark. Runnable on rented GPU.

> HONEST PREREQUISITE (verified on disk): your 4 brain-configs (sov3_4_brains_1_oowm.py) are
> currently PROMPT/ENSEMBLE configs over ONE base (qwen3:30b-a3b). They are NOT yet 4 weight-sets.
> You cannot merge identical weights. So the pipeline is:
>   STEP 1  fine-tune the base into N DISTINCT experts (one per brain-config, on that config's data)
>   STEP 2  merge/upcycle those experts into one new model (SLERP/TIES  OR  MoE upcycling)
>   STEP 3  benchmark the merged model vs the experts vs the base — PROVE it wins or kill it
> This produces genuinely new weights that are "yours from your configs" — the real rung 4.

## WHAT YOU NEED (all open-source, all pip-installable)
- transformers, peft, trl, bitsandbytes, accelerate, datasets  (fine-tune)
- mergekit  (the merge/upcycle engine — github.com/arcee-ai/mergekit, Apache-2 friendly)
- one base model pulled locally (start SMALL — see GPU spec: Qwen3.6-4B/8b for the pipeline proof,
  scale to Qwen3.6-35B-A3B only once the pipeline works)

## THE FILES IN THIS KIT
- 01_prep_expert_data.py   — split your estate data into per-expert training sets
- 02_finetune_expert.py    — LoRA fine-tune ONE expert (run N times, once per brain-config)
- 03_merge_experts.yaml    — mergekit config: SLERP/TIES merge of the experts
- 03b_moe_upcycle.yaml     — mergekit-moe config: assemble experts as an MoE (the "12 mindsets→1")
- 04_benchmark.py          — score merged vs experts vs base on your task battery
- GPU_RENTAL_SPEC.md       — exactly what to rent, where, and cost

## THE HONEST SEQUENCE
1. Prove the pipeline on a SMALL base (Qwen3.6-4B) — cheap, hours, ~£5-15 of GPU.
2. Only scale to Qwen3.6-35B-A3B once merge+benchmark works end-to-end on the small one.
3. Benchmark is non-negotiable: a merge that loses to its parts is dead weight. Quantify.
