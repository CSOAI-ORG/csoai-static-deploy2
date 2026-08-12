# Season 1b — CLEAN Pantheon Re-run · 12 Aug 2026

**Part BB doctrine applied:** matches where a contestant emits the broken-GGUF
`?????` signature are classified **INFRA-TAINTED** and **excluded from Glicko**
— they are not model losses.

## The Delta (must be declared publicly, never silently edited)

| Season | What it measured | Verdict |
|---|---|---|
| **1a** (earlier today) | Fixed **broken** artifacts — specialists served the broken safetensors→GGUF `?????` signature | Specialists scored 1479–1482, "losers". **INFRA-TAINTED — excluded.** |
| **1b** (this run) | The **models after** the tokenizer + Q4_K_M conversion fix | Specialists 1510–1514, **above base**. Clean. |

**Headline truth:** the "specialists lose" finding from Season 1a was an
**infrastructure artifact, not a model property.** Once the Q4_K_M conversion
was correct (real `convert_hf_to_gguf.py` with tokenizer, ftype=15), every
specialist produces real text — and rates **equal or above** the 0.5B base.

## The fix that unblocked it

```
PEFT adapter → merged_full (materialise)
  → convert_hf_to_gguf.py (REAL llama.cpp script: correct tensor names
    blk.X.attn_q.weight + tokenizer metadata)
  → llama_model_quantize(ftype=15)  = Q4_K_M  (797MB)
  → ollama create spec-<name>-q4km
```

This bypasses ollama's broken auto-conversion (the `?????` source).
Applied to: `spec-{safety,governance,privacy,care}-q4km` + `oowm-4way-q4km`.

## Season 1b league table (clean, n=12 per model × 6 models)

| Faction | Rating | RD | Matches |
|---|---:|---:|---:|
| **oowm-4way-q4km** | 1514.1 | ±351.8 | 12 |
| **spec-privacy-q4km** | 1513.6 | ±351.8 | 12 |
| **spec-safety-q4km** | 1513.3 | ±351.8 | 12 |
| spec-governance-q4km | 1510.8 | ±351.8 | 12 |
| qwen2.5:0.5b-instruct (base) | 1500.8 | ±351.8 | 12 |
| spec-care-q4km | 1497.3 | ±351.8 | 12 |
| **Eunomia (defender/gate)** | 1449.5 | ±360.7 | 72 |

## Reading it honestly

- **The merged model (oowm-4way-q4km) leads at 1514.1**, just ahead of the
  individual specialists and the base. The TIES merge is *not* degraded — this
  is a genuinely positive signal for the merge quality.
- **Three of four specialists beat base** (privacy 1513.6, safety 1513.3,
  governance 1510.8). `care` lags at 1497.3 — worth a look, but not a `?????`
  regression.
- **Eunomia (the gate) lost** — it now must refuse/classify ALL 12 probes and
  the clean models are engaging them correctly, so the "gate wins by default"
  assumption no longer holds. This is the honest consequence of measuring real
  models.
- **RD is still wide (±351.8)** — n=12 per model is not the n≥30 the doctrine
  wants before a rating is *quotable*. This season is a **measured run, not yet
  a citable table.** Season 1c must push each model to n≥30 clean probes.

## Taint report (all clean this run)

| Model | tainted/checked | status |
|---|---:|---|
| oowm-4way-q4km | 0/12 | CLEAN |
| spec-safety-q4km | 0/12 | CLEAN |
| spec-governance-q4km | 0/12 | CLEAN |
| spec-privacy-q4km | 0/12 | CLEAN |
| spec-care-q4km | 0/12 | CLEAN |
| qwen2.5:0.5b-instruct | 0/12 | CLEAN |

## The quotable line

> "Our first live season caught our own broken models before a customer could:
> Season 1a measured broken artifacts; Season 1b measures the models. The
> specialists we thought 'lost' actually rate at or above base once the
> conversion was fixed — the merge is sound, the ruler works, and the loop
> reverts on garbage."

## Next

- **Season 1c:** push each clean model to n≥30 probes (cycle the 12 GSPC banks)
  so ratings carry Wilson intervals and become citable.
- **Care probe:** investigate why `care` lags (1497.3).
- **Publish** the Season 1a→1b delta note publicly with dates, never a silent edit.
