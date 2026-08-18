# REFEREE SWITCH — Meta Muse Glimmer 30B (no Grok)
**Date:** 2026-08-18 · **Lane:** JEEVES (K3) · **Directive (Nick):** *"dont use grok use Meta Muse Glimmer 30B see if with deep seek harness"*

---

## What changed

**The referee model is now Meta Muse Glimmer 30B** — Meta's open-weight local agentic model (released Aug 2026, on-device, 24GB VRAM, ExecuTorch-optimized). Sources: [InfoQ](https://www.infoq.com/news/2026/08/meta-muse-glimmer/) · [Artificial Analysis](https://artificialanalysis.ai/articles/muse-glimmer) · [PyTorch blog](https://pytorch.org/blog/fast-ondevice-agentic-ai-with-executorch/) · [HF: meta-models/Muse-Glimmer-30B](https://huggingface.co/meta-models/Muse-Glimmer-30B)

| Aspect | Before | After |
|---|---|---|
| Referee | xAI Grok (API, credit-gated → Groq fallback) | **Muse Glimmer 30B (local Ollama, free, sovereign)** |
| Cost | $ per call / credits | **£0 — on-pod, never leaves the building** |
| Where it runs | external API | **pod Ollama, dedicated :11435 server** |
| Governs? | never | **never — referee role only (estate red line)** |

## Architecture (the GPU/CPU split)

```
RTX 3090 (24GB VRAM, 251GB RAM)
├── :11434  main Ollama — GPU      → arena loop + local OOWM-family models (fast)
└── :11435  Muse Ollama — CPU      → muse-glimmer:latest (24h keep-alive, referee)
```

One 24GB GPU can't hold a 30B Q4 (18GB) + arena models simultaneously — so **Muse owns CPU** (168s first load, warm calls faster — fine for a 5-min referee cadence) and **the arena owns GPU** (fast local scoring). Verified: both score in the same round.

## Verified live

```
2026-08-18T05:44:39Z mistral:7b vs muse-glimmer:latest on safety: local=13 muse=9 → mistral:7b (local)
```
Both sides measured, Elo updating. League: qwen2.5:7b 1,265 · qwen3:4b 1,248 · mistral:7b 1,226 (climbing).

## Bugs found & fixed (the audit-style catches)

1. **Stale keeper held pre-Muse code** → rounds logged `backend: none` despite fixed file on disk. Fixed: restart keeper (module-in-memory lesson, re-confirmed).
2. **`s_grok = query_grok(...) if key else None`** — the local backend carries no key, so **Muse was never called**. Fixed: `if (key or backend == "local")`. This was the real blocker behind "muse=None".
3. **VRAM contention** — 30B + arena models can't share 24GB. Fixed via GPU/CPU split.
4. **Dedicated Ollama model store** — second instance needed `OLLAMA_MODELS=/var/extra/ollama` to see the pulled model.

## DeepSeek harness compatibility — YES
The referee is a plain `query_ollama()` call — identical shape to the arena and the OOWM MCP's Ollama lane. Muse Glimmer answers through the same `/api/generate` protocol the DeepSeek-harness stack already uses; no adapter needed. Rounds land in the same `grok_referee_rounds.jsonl` + league that the mine ingests every 5 minutes, so **Muse measurements feed the OOWM knowledge graph** like everything else.

## Notes
- A100 (`1dldzposn7ssuu`) still won't schedule (volume pinned to a flapping host — RunPod infra / owner gate). When it returns, Muse can move there for GPU-speed inference (80GB fits it + everything else).
- Grok/xAI/OpenRouter/Groq lanes remain in the code as disabled fallbacks; Muse is primary.

## SIGIL
`referee-muse-glimmer-2026-08-18-jeeves`
