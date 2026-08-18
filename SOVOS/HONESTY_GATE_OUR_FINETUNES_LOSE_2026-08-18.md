# OUR OWN FINE-TUNES ARE LOSING OUR OWN ARENA
**Published 2026-08-18 · Council of AI · honest measurement, embarrassing to us, verifiable by anyone**

> *"A measurer publishing a result that embarrasses it is what pulls outsiders in."* — Master Playbook §10, the honesty gate.

---

## The verdict, plainly

Our two sovereign fine-tunes — **council-oowm** and **council-safe** — are **losing to base models in our own 16-axis arena**, on our own GPU, with our own Elo ladder. We trained them. We measure them. They lose. We publish it.

## The numbers (live from the arena league, 2026-08-18)

| Model | Elo | Games | Note |
|---|---|---|---|
| qwen3:4b (base) | **1,326.7** | 672 | base model, no sovereign adapter |
| qwen2.5:1.5b (base) | 1,311.5 | 711 | smallest base, still ahead |
| mistral:7b (base) | 1,252.4 | 639 | base |
| **council-safe** (our fine-tune) | 1,124.6 | 533 | −202 vs leader |
| qwen2.5:0.5b (base) | 1,113.0 | 730 | tiny base |
| **council-oowm** (our fine-tune) | **1,015.8** | 496 | **dead last, −311 vs leader** |

**Headline: our two sovereign fine-tunes occupy the bottom half. One is last.** The base models we started from beat the adapters we built on them.

## Why this is the most credible thing we can publish

1. **It contradicts our own product narrative.** No one buys measurement from a body that hides its own losing results.
2. **It is fully reproducible.** 3,700+ signed arena rounds on the pod, `reborn_league.json` + `reborn_rounds.jsonl`, Ed25519-signable. Any stranger can rerun.
3. **It matches the known literature pattern.** Small-base fine-tunes on 4-axis governance batteries typically do not beat their base (our own earlier finding: *base Qwen2.5-0.5B beats every sovereign fine-tune on 8/9 measured governance axes*).
4. **It is the honest ceiling, stated before anyone else does:** *"This governs provenance, not correctness. An attested answer is attested, never verified."* Our fine-tunes prove the point: they are signed, and they still lose.

## What it means (and doesn't)

- **Does mean:** adapter-souping weak bases does not beat the base. The measurement rail works — it caught us.
- **Does NOT mean:** the instruments are broken. The instrument that shows us losing is the same one we sell. That is the point.
- **Next honest step (per canon):** base model + statute retrieval (the only path that beat the fine-tunes in our own evals), not weight-merging weak specialists.

## The signature

Every number above is from the live pod state at 2026-08-18, recorded in the arena league with the 16-axis battery. Recompute path: `reborn_league.json` on the 3090 pod, ~3,700 rounds, Elo K=32.

**SIGIL: `honesty-gate-our-finetunes-lose-2026-08-18-jeeves`**
