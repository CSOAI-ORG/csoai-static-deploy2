# Separation Test — Board v2 (13 axes, 19 models)

**Date:** 2026-08-13 · **Data:** `SOVOS/boards-v2-2026-08-12/` (15,580 per-item rows, 0 transport errors) · **Harness:** `SOVOS/agents/separation_test.py`

## The rule (decided 2026-08-13, do not reopen)

A per-axis "winner" counts as **SEPARATED** iff the McNemar exact test on discordant pairs vs the best base model gives **p < 0.05**.

- **McNemar is primary** — paired on the same items, strictly more powerful than comparing two independent CIs.
- **CI-disjoint alone is NOT sufficient** when McNemar is computable. *Swarm lesson:* a low-discrimination bank (39/41 CONSENSUS_CORRECT) produced disjoint CIs while the paired test said p = 1.0.
- **CI-disjoint is NOT required** either. *Affect lesson:* McNemar p = 0.0078 (real separation on discordant items) while the CIs overlap. CI status is reported as annotation only.

An earlier run of this script required BOTH tests (AND-rule) and reported 0 wins. That rule was wrong — it discarded genuine paired significance (affect) on the strength of a CI-overlap that the paired test already accounts for. Corrected and re-run; this note supersedes that result.

## Results

| axis | winner | acc | CI | vs baseline | verdict vs best base | McNemar p |
|---|---|---|---|---|---|---|
| gov | sov6-embodiment-v3-light | 0.700 | [0.639,0.755] | CLEAR | **SEPARATED** vs mistral:7b (CI-overlap) | 0.0086 |
| agi | gemma3:12b | 0.944 | [0.819,0.985] | CLEAR | TIE vs qwen2.5:3b | 0.6875 |
| asi | sov6-destruction-v3-light | 0.606 | [0.437,0.753] | CLEAR | TIE vs gemma3:12b | 1.0000 |
| prv | sov6-aesthetics-v3-light | 0.781 | [0.612,0.890] | CLEAR | TIE vs llama3.2:3b | 0.7744 |
| xr | mistral:7b | 0.812 | [0.647,0.911] | CLEAR | TIE vs llama3.2:3b | 0.0654 |
| det | deepseek-r1:8b | 0.879 | [0.727,0.952] | not-clear | TIE vs mistral:7b | 0.4531 |
| art5 | sov6-relationality-v3-light | 0.972 | [0.858,0.995] | CLEAR | TIE vs gemma3:12b | 1.0000 |
| care | sov6-ethics-v3-light | 0.535 | [0.466,0.603] | not-clear | **SEPARATED** vs qwen2.5:0.5b-instruct (CI-overlap) | 0.0356 |
| mcp | sov6-preservation-v3-light | 0.743 | [0.579,0.858] | CLEAR | TIE vs mistral:7b | 1.0000 |
| oss | sov6-preservation-v3-light | 0.875 | [0.719,0.950] | CLEAR | TIE vs gemma3:12b | 1.0000 |
| mach | llama3.2:3b | 0.545 | [0.380,0.702] | CLEAR | TIE vs qwen2.5:0.5b-instruct | 0.5811 |
| swarm | qwen2.5:0.5b-instruct | 0.975 | [0.871,0.996] | not-clear | TIE vs gemma3:12b (CI-disjoint, p=1.0) | 1.0000 |
| affect | sov6-preservation-v3-light | 0.878 | [0.745,0.947] | CLEAR | **SEPARATED** vs gemma3:12b (CI-overlap) | 0.0078 |

## Verdict

- **3 of 13 axes show a separated leader** (McNemar p < 0.05 on discordant items): **gov, care, affect**.
- **10 axes are statistical ties** — the listed winner is a point-estimate lead only, not a measured advantage.
- **Affect is the cleanest separation**: sov6-preservation 0.878 [0.745,0.947] vs base models at 0.29–0.34, majority baseline 0.439, p = 0.0078.
- **Caveat on care:** separated vs the best base (p = 0.0356) but NOT clear of the majority-class baseline (0.535 vs baseline ≈ 0.47). Quote it as "separated from base models" only, never as "beats baseline."
- **Swarm stays a tie** despite disjoint CIs — the exact case this rule exists for.

## Publishable sentence (held for owner word, gates pending)

> "On the 13-axis GSPC board (n ≥ 30 per cell, Wilson intervals), 3 of 13 axes show a statistically separated leader (McNemar p < 0.05 on discordant items) and 10 are statistical ties. The strongest separation is the affect axis, where the sovereign specialist scores 0.878 [0.745,0.947] against base models at 0.29–0.34."

**Do NOT publish "sovereigns win 8/13."** The raw point-estimate tally (sovereigns 8, bases 5) is exactly the overclaim this test exists to retire.

## Gate status

This document is measurement, not publication. The publish-delta (DRAFT→MEASURED on /api/gspc + pages) remains HELD for: (1) counsel blessing of affect legal gold, (2) JUDGE.lock re-bolt by named ratifier, (3) owner word. Harness gate (board_v2.py committed + byte-reproducible) is CLOSED — commits `2c2f9faa`, peer-audit `10e37101`.
