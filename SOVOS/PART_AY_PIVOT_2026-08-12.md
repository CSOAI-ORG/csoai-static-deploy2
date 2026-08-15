# Part AY — Pivot-and-Attack Register

> "Every lab now marks its own output. We prove the whole pipeline."

## Why this is KILLED (not REAL or THEORY)

The Anthropic Code of Practice signing (alongside Google, Meta, Microsoft, Mistral, OpenAI) was the **legal minimum** required by Article 50(2) of the EU AI Act. Six labs converging on the same regulatory requirement is not one lab reading our work. The watermarking vocabulary is the regulation's, not theirs or ours.

## Dates (lock these everywhere)

| Date | Meaning |
|---|---|
| **2 August 2026** | EU AI Act Article 50(2) **in force** — marking obligation applies to new systems |
| **2 December 2026** | Grace period end — **pre-existing systems** must also mark |

(The note said "2 December" — half right. The other half is "since 2 August.")

## What they shipped vs. what we ship

| Anthropic & friends | MEOK (us) |
|---|---|
| Model-level sampling watermark | Deployer-side attestation + evidence trail |
| File metadata (C2PA) | Hash-chained audit at the gate |
| Per-vendor, heterogeneous | Cross-vendor, federated |
| "Proves processing, not authorship" (their words) | Proves the **whole pipeline** — who ran what, when, where |
| No published false-positive rates | Wilson CIs on every arena measurement |
| Verify, don't trust | Sigil-signed, versioned, replayable |

## What convergence means

1. **Marks are everywhere** — heterogeneity guaranteed
2. **Heterogeneous pipelines need a verifier** — published FP rates + a published false-negative rate
3. **The legal semantic stays** — Article 50 wording is regulation; the verification gap is the invention

## Three moves (this week)

1. **Today** — audit every public artifact, fix all dates (2 Aug + 2 Dec)
2. **This week** — file P6/P8/P20 provisionals. Convergence means prior art is piling up weekly.
3. **While the news cycle is hot** — publish the line. Their launch becomes our headline.

## Public positioning line (draft tonight)

> **"Every lab now marks its own output. We prove the whole pipeline."**

## The audit we built this session

- **Live arena wire:** `sovos-league/arena_wire.py` + `league_for_fleet()` — real ollama probes against 4 models (qwen2.5:0.5b-instruct + spec-governance + spec-safety + spec-care), 12 axes per model = 48 real matches.
- **Real finding:** specialists all produce `????????????????????` (ollama safetensors→GGUF bug). Base model works correctly. The ouroboros loop correctly REVERTED the specialists.
- **Pantheon League Season 2 (live):** Eunomia 1560.5 (defender, won 48) / spec-care 1481.6 / spec-safety 1480.4 / spec-governance 1479.2 / qwen2.5:0.5b 1499.7 — specialists all lose to the gate.
- **Ouroboros loop:** `SOVOS/agents/ouroboros.py` — bounded self-improvement end-to-end (probe → run → measure → adjust) with precision-floor + recall-up gates.

## Honest scope

- The "convergence is convergent engineering" reading is *technical*, not *legal*. Filing P6/P8/P20 is what gives the position teeth.
- We do NOT claim the verification gap is "patent-grade yet" — the pipeline is real, the Wilson CIs are real, but the published FP/FN rates haven't been peer-reviewed.
- The "heterogeneity is the surface" framing assumes all six frontier labs actually ship. If any pull back (OpenAI's earlier reluctance), the surface area shrinks.