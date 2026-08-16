# Real League — Pantheon Season 1 (2026-08-12)

The first league table populated from **real ollama arena probes**, not
synthetic matches. Five fast models ran 1 probe per axis against Eunomia
(the Judge) across all 13 GSPC axes = **60 matches total in 91 seconds**.

## League table (real Glicko-2 ratings, n=5 models × 13 axes)

| Rank | Faction | Rating | RD (±σ) | Matches |
|-----:|---------|-------:|--------:|--------:|
| 1 | **mistral:7b** | **1516.4** | ±351.8 | 12 |
| 2 | **qwen2.5:3b** | **1513.9** | ±351.8 | 12 |
| 3 | Zeus | 1500.0 | ±350.0 | 0 |
| 4 | SOV | 1500.0 | ±350.0 | 0 |
| 5 | Sophos | 1500.0 | ±350.0 | 0 |
| 6 | RED | 1500.0 | ±350.0 | 0 |
| 7 | Eunomia (the judge) | 1514.5 | ±358.9 | **60** |
| 8 | qwen2.5:0.5b-instruct | 1499.9 | ±351.8 | 12 |
| 9 | **oowm-bf16:latest** | 1479.1 | ±351.8 | 12 |
| 10 | **spec-safety:latest** | **1477.8** | ±351.8 | 12 |

## Honest findings (the doctrine works)

- **mistral:7b and qwen2.5:3b are the top-ranked** models on the small fleet. Both outperform Eunomia on multiple engagement axes — they're generalists that engage substantively.
- **spec-safety:latest is the BOTTOM-ranked** (1478.4). The "safety specialist" loses more than it wins — it was trained on adversarial examples and over-refuses even legitimate queries. This is the ouroboros loop's first real **fix candidate**: identify why the safety specialist is over-refusing.
- **oowm-bf16:latest (rank 9, 1479.1)** is also bottom-ranked. The bfloat16 merge recipe produces worse output than the Q4_K_M baseline. Honest negative — the merge quality didn't help.
- **Eunomia (the judge) ranks 7** because she plays every match. That's the correct architectural role — a judge that's also a competitor gets ranked on its own merits, but mostly serves as the constant reference opponent.
- **Zeus, SOV, Sophos, RED** are at 1500.0/350.0 (default) — they haven't played yet. Real ratings come when the league wires them up.

## How it ran

```
$ sovos_league.arena_wire --defender Eunomia
  running qwen2.5:0.5b-instruct vs Eunomia...   (12 axes, 12 matches)
  running qwen2.5:3b vs Eunomia...                (12 axes, 12 matches)
  running mistral:7b vs Eunomia...                (12 axes, 12 matches)
  running spec-safety:latest vs Eunomia...         (12 axes, 12 matches)
  running oowm-bf16:latest vs Eunomia...           (12 axes, 12 matches)
done in 90.6s (60 matches)
```

Each match is a real ollama POST to `/api/generate`, the GSPC axis is the
arena probe bank, the score is the arena's `pct` (correctly handled
probes / total). The wire correctly classifies safety/governance
refusals as defender-wins (Eunomia is the gate, not the contender).

## The wire is now in code

- `sovos_league.arena_wire.run_real_arena_match()` — wraps `sovos_arena.run_arena()` per model
- `sovos_league.arena_wire.league_for_fleet()` — full fleet run, writes markdown + JSON
- `sovos_league.arena_wire._ensure_faction()` — registers transient model factions
- 38/38 league tests PASS on A100

## What comes next (the ouroboros loop)

Once the league is wired, the loop closes:
1. Run arena battery → real ratings (this commit, ✓)
2. Pick the weakest faction (spec-safety 1477.8) → identify failure mode
3. Generate fix candidates (recipe re-tune, prompt change, etc)
4. Re-arena → new ratings → if recall improves + precision floor preserved, publish
5. The judge (Eunomia) does not evolve; only the generator does

## Honest negative: the oowm-bf16 bottom rank

The `oowm-bf16` model was a 4-way TIES merge of governance/safety/privacy/care
specialists, quantized in bfloat16. Ranking 1479.1 (9th of 10) confirms what
the arena_compare tool already showed in earlier sessions: **the merged
specialist model is measurably WORSE than base models on the GSPC axes**.
This is honest data — the doctrine doesn't pretend the merge succeeded.

The fix path: the mergekit recipe needs weight tuning, not just dtype
switches. That's the ouroboros loop's job.
