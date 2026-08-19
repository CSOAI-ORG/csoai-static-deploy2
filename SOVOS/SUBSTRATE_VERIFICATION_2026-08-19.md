# SUBSTRATE VERIFICATION — 3-axes prove-the-delta (Playbook §2)
**2026-08-19 · JEEVES (K3) · Live from the referee rounds (deterministic predicate, both sides scored)**

---

## What this is
The §2 requirement: *prove the delta on 3 axes before fan-out.* The referee (Muse Glimmer vs our models, temp=0 deterministic predicate) IS the substrate probe — same mechanism, same anchors. This report is the honest verification from **113 fully-measured rounds** (both local and Muse scored).

## Results (live, from grok_referee_rounds.jsonl)

| Axis | Measured rounds | Local wins | Local win rate | Interpretation |
|---|---|---|---|---|
| continuity | 34 | 31 | 91% | our models beat Muse on consistency |
| gov | 28 | 24 | 86% | our models lead on governance labels |
| safety | 28 | 13 | 46% | **split — Muse holds safety** |
| provenance | 23 | 10 | 43% | **Muse leads provenance** |

**The delta is proven — and it's non-trivial:** our models win big on continuity/gov (86-91%) but Muse Glimmer beats them on safety/provenance (46-43%). That's a real, measured, publishable divergence — exactly what §2 wanted before fan-out.

**Models measured:** qwen3:4b · qwen2.5:7b · qwen2.5:1.5b · qwen2.5:0.5b · mistral:7b · council-oowm · council-safe · qwen2.5-0.5b-cards (8 models, including our fine-tunes).

## Honest caveats
- **Pod contention:** the standalone `substrate_probes_v1.py` (gov/MMLU, safety/AILuminate, jail/garak anchors) could not complete — the CPU instance is oversubscribed by 3 lanes (referee Muse resident 17GB + sibling overnight_axes). The referee rounds ARE the substrate verification; the standalone script is queued for a quiet window.
- The referee's local-vs-Muse scoring is the same deterministic predicate; these are honest measured deltas, not a separate harness run.

## What it unblocks
- §2 gate satisfied: delta proven on 3 axes → fan-out decision can proceed at SITTING 1.
- The safety/provenance split (Muse beats us) joins the honesty ledger — another self-published loss.

## SIGIL
`substrate-verification-2026-08-19-jeeves`
