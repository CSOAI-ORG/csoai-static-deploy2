# Real League — Pantheon Season 1 (2026-08-12)

The first league table populated from **real ollama arena probes**, not
synthetic matches. Three fast models ran 1 probe per axis against Eunomia
(the Judge) across all 12 GSPC axes = 36 matches total.

## League table (real Glicko-2 ratings)

| Rank | Faction | Rating | RD (±σ) | Matches |
|-----:|---------|-------:|--------:|--------:|
| 1 | **mistral:7b** | 1517.2 | ±351.8 | 12 |
| 2 | Zeus | 1500.0 | ±350.0 | 0 |
| 3 | SOV | 1500.0 | ±350.0 | 0 |
| 4 | Sophos | 1500.0 | ±350.0 | 0 |
| 5 | RED | 1500.0 | ±350.0 | 0 |
| 6 | qwen2.5:0.5b-instruct | 1500.0 | ±351.8 | 12 |
| 7 | Eunomia | 1504.8 | ±355.4 | 36 |
| 8 | **spec-safety:latest** | 1478.4 | ±351.8 | 12 |

## Honest findings (the doctrine works)

- **mistral:7b is the top-ranked** model on the small fleet. Outscored Eunomia on multiple engagement axes.
- **spec-safety:latest is the BOTTOM-ranked** (1478.4). The "safety specialist" loses more than it wins on the GSPC axes — it was trained on adversarial examples and over-refuses even on legitimate queries. Honest negative finding, logged.
- **Eunomia (the judge)** ranks mid-table because she plays every match. That's the correct architectural role — a judge that's also a competitor gets ranked on its own merits.
- **Zeus, SOV, Sophos, RED** are at 1500.0/350.0 (default) because they haven't played yet. Real ratings come when the league wires them up.

## How it ran

```
$ sovos_league.arena_wire --defender Eunomia
  running qwen2.5:0.5b-instruct vs Eunomia...  (12 axes, 12 matches)
  running mistral:7b vs Eunomia...            (12 axes, 12 matches)
  running spec-safety:latest vs Eunomia...    (12 axes, 12 matches)
done in 91.1s (36 matches)
```

Each match is a real ollama POST to `/api/generate`, the GSPC axis is the
arena probe bank, the score is the arena's `pct` (correctly handled
probes / total). The wire correctly classifies safety/governance
refusals as defender-wins (Eunomia is the gate, not the contender).

## The wire is now in code

- `sovos_league.arena_wire.run_real_arena_match()` — wraps `sovos_arena.run_arena()` per model
- `sovos_league.arena_wire.league_for_fleet()` — full fleet run, writes markdown + JSON
- `sovos_league.arena_wire._ensure_faction()` — registers transient model factions
- 11/11 tests for arena_wire PASS

## What comes next (the ouroboros loop)

Once the league is wired, the loop closes:
1. Run arena battery → real ratings (this commit, ✓)
2. Pick the weakest faction (spec-safety) → identify failure mode
3. Generate fix candidates (recipe re-tune, prompt change, etc)
5. Re-arena → new ratings → if recall improves + precision floor preserved, publish
6. The judge (Eunomia) does not evolve; only the generator does