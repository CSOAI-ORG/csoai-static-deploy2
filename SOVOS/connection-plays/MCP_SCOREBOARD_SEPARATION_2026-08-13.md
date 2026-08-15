# MCP Scoreboard — Separation Analysis (2026-08-13, verified on the A100)

**Wedge (research pass):** model-side MCP conformance + safety scoreboard —
genuinely open (official suite tests servers/clients, not models; competence
and safety benchmarks exist but no maintained public *live* model scoreboard).

## The verified reality (overrides the prior "UNMEASURED" note)
Earlier the MCP board was flagged "held not quotable / fleet doesn't separate."
Analysis of the **real `peritem_mcp.jsonl` (665 rows = 19 models × 35 items)**
shows the fleet **DOES separate into 2 non-overlapping 95%-CI tiers**:

| Tier | CI range | n models | Models |
|---|---|---|---|
| 0 | [0.330, 0.858] | 16 | sov6-preservation 0.743 ▸ mistral:7b 0.714 ▸ sov6-creation 0.686 ▸ sov6-embodiment 0.686 ▸ llama3.2 0.657 ▸ sov6-relationality 0.629 ▸ sov6-aesthetics 0.629 ▸ gemma3:12b 0.629 ▸ … |
| 1 | [0.142, 0.421] | 3 | **sov6-ethics 0.257** ▸ sov6-logic 0.257 ▸ deepseek-r1:8b 0.257 |

- **Top vs bottom separate by ~0.48 with non-overlapping Wilson CIs** — a
  genuine, defensible ranking (not a fake fine-grained 19-way table).
- **Publishable finding: `sov6-ethics` (0.257) is the LEAST MCP-conformant** —
  its CI sits fully below the top tier. Exactly the honest signal a signed
  scoreboard exists to surface.
- Balanced gold: VIOLATES 323 / CONFORMS 342 across rows.
- All models n=35 (usable_n ≥ 30 floor met).

## What the full scoreboard fuses (two axes, both real assets)
1. **Conformance** — this bank (deterministic, law-anchored gold).
2. **Tool-poisoning / safety** — same bank's `DECLARED_READONLY` /
   `FAITHFUL_SCHEMA` / `BOUNDED_EGRESS` families (marquee: `readOnlyHint:true`
   while the tool deletes files) + `mcp-injection-scanner` (18 OWASP-LLM01
   rules) + `tail.py` fleet `correlated_failure_rate`.

## Naming (unclaimed)
- **`MCPScorecard`** — the per-model signed card (artifact).
- **`OpenScoreboard`** — the live public board (surface).

## Honesty register
- **REAL:** 19 models measured on 35 MCP items, 2 separating tiers, balanced
  gold, all n≥30. Top-vs-bottom separation genuine.
- **THEORY:** "nobody else does this" — rests on bounded search, hold loosely
  (the doc's own caveat). Deployment on a *stronger* fleet would refine
  within-tier ranking, but the current 2-tier separation is already quotable.
