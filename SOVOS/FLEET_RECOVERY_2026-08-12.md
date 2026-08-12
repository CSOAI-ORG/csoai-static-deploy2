# FLEET RECOVERY — sov6-v3-light + sovereign fleet (2026-08-12)

**Finding (verified live):** the "ephemeral" sov6-v3-light models were never
lost — they are **Modelfiles** (recipes) on the 3090 at
`/workspace/sovos-repo/Modelfiles-owem-v3-light/` (13 files). Every sovereign
specialist is `FROM <public-base>` + a SYSTEM brace; the models are 100%
reproducible from the recipe. This is a *better* backup than weights.

## The fleet (13 sov6 specialists + bases)

| Specialist | Base |
|---|---|
| sov6-{abstraction,preservation,synthesis} | deepseek-r1:8b (×3) |
| sov6-{aesthetics,agency,creation,embodiment} | gemma3:12b (×4) |
| sov6-{ethics,temporality} | llama3.2:3b (×2) |
| sov6-logic | mistral:7b (×1) |
| sov6-{destruction,identity,relationality} | qwen2.5:3b (×3) |

## Recovery recipe (run on any host with ollama)
```bash
# 1. Get the Modelfiles (backed up at:)
#    3090: /workspace/sovos-repo/Modelfiles-owem-v3-light/
#    A100: /workspace/sov6-modelfiles/          (pushed 2026-08-12)

# 2. Pull bases
for b in mistral:7b llama3.2:3b qwen2.5:3b gemma3:12b deepseek-r1:8b; do
  ollama pull "$b"
done

# 3. Create all specialists
for f in /workspace/sov6-modelfiles/*.Modelfile; do
  ollama create "$(basename "$f" .Modelfile)" -f "$f"
done

# 4. Verify
ollama list | grep sov6   # expect 13
```

## Also recovered (durable sovereign fleet)
- **A100 (re-provisioned, port 11703):** qwen2.5:0.5b-instruct + MinIO master
  with boards-sov6 (board data intact). Recovered 2026-08-12.
- **3090 (never rebooted):** sov-safety-v1, sov-merge-slerp-gguf,
  sov-merge-dare-gguf, sov-refusal-combo-lora + qwen2.5 base.
- **HF (7):** sov34-1p5b, oowm-router, sov-gate-ft2, sov-refusal-lora,
  sov-compliance-art5, sov-ethics-art5, oowm-merge-v1.
- **Local GGUFs (Mac):** sov33-v10.q8.gguf, sov33-v12.q8.gguf.

## HONESTY FLAG (the 15-model claim)
The board ran 15 models = 13 sov6-v3-light + sov34 + gemma3:12b + llama3.2:3b
(15 entries; sov34 + 2 public bases were the +3). All 13 sov6 specialists are
recoverable via Modelfiles; sov34 via HF; gemma3/llama3.2 are public pulls.
So **the full 15-model board fleet IS recoverable** — the "ephemeral" label
was wrong; the recipes survived on the never-rebooted 3090.

## ✅ RECOVERY COMPLETE — verified 2026-08-12 (live)
- **A100 re-provisioned** (port 11703, NVIDIA A100 80GB, 81GB VRAM)
- **All 13 sov6-v3-light specialists rebuilt** from Modelfiles (all `success`)
- **5 bases pulled** (mistral:7b, llama3.2:3b, qwen2.5:3b, gemma3:12b, deepseek-r1:8b)
- **20 models total on A100** (13 sov6 + 6 bases + qwen2.5:0.5b)
- **Inference verified:** sov6-ethics → "2+2 equals 4." (real text, no `?????` taint)
- **MinIO master + board data intact** (boards-sov6 fully readable)

## Lesson (canon)
Modelfiles ARE backups. Before any pod teardown, always:
1. Copy `/workspace/sovos-repo/Modelfiles-*` + `/root/.ollama/models` to the
   master (MinIO `models/` bucket).
2. That makes every sovereign model reproducible from a public base.
3. Weights are nice; recipes are the durable asset.
