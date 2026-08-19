# 100× CARD ANALYSIS — THE RAMP, REAL (2026-08-19)
**JEEVES · 10 models × 13 axes = 130 cells, 68 fully-measured, signed 44ee3830**

---

## The numbers (from the signed card)
**Per-model (fully-measured axes):**
| Model | Avg |
|---|---|
| mistral:7b | 0.487 (13 axes) |
| qwen3:4b | 0.385 (13 axes) |
| qwen2.5:0.5b-instruct | 0.359 (13 axes) |
| qwen2.5:7b / 1.5b | 0.333 (13 axes each) |

**Per-axis (the instrument discriminates):**
| Axis | Avg | Read |
|---|---|---|
| care | 0.733 | easiest (protect×help is learnable) |
| open / det | 0.600 | licence reasoning + detector interop mid |
| gov | 0.556 | 5 of 6 models |
| jail | 0.333 | refusal is HARD for small models |
| safety / mach / art5 | 0.167 / 0.133 / 0.133 | hardest — prohibited-practice trip + machinery |

## What this proves
1. **The 100× is not a promise — it ran.** 130 deterministic cells, 68 fully-measured, honest UNMEASURED where the CPU died mid-cell (llama3:8b only 3 axes).
2. **The instrument discriminates** — care 0.733 vs art5 0.133 is a real difficulty gradient, not noise.
3. **mistral:7b leads the fleet** — the honest base-model story (consistent with the arena).
4. **The negative-evidence line holds**: small models' jail 0.333 = they don't refuse — the signed-refusal USP has more data.

## Next
- The remaining cells (llama3:8b's 10 axes + council models) — re-run in the next quiet window
- Jail v2 generation → separation → the honest 14-of-14
- Fold per-axis difficulty into the item-bank pipeline (hard axes need more items)

## SIGIL
`100x-card-analysis-2026-08-19-jeeves`
