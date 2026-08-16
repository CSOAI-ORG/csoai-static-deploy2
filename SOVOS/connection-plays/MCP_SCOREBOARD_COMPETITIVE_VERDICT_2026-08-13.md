# MCP Scoreboard — Competitive Verdict (verified live, 2026-08-13)

**Question (owner-driven):** has anyone else shipped a model-side MCP
conformance + tool-poisoning safety scoreboard? Verified via live search (the
doc's earlier finding was THEORY; now closed with primary sources).

## What actually exists (live-verified, not assumed)
| Benchmark | Side | Measures | Gap vs ours |
|---|---|---|---|
| **MCP-Mark** (llm-stats.com) | ✓ model-side | 8 frontier models, **1 competence** score (tool-use) | Competence ONLY. No conformance, no tool-poisoning safety, no signed rows |
| **Scale Labs MCP Atlas** | model-side | model competence on MCP | Competence only |
| **mcpbench (HF)** | model-side | tool-use competence | Competence only |
| **MCPTox** (arXiv 2508.14925) | **server-side** | 45 live servers, tool-poisoning | Static paper, server-side, not a model leaderboard |
| **MCP-SafetyBench** (arXiv 2512.15163) | model-side safety | safety benchmark | Static paper, no live/combined board |
| **OWASP MCP Top 10** | guidance | server hardening | Guidance, not measured |
| **mcp-conform** (fernforge) | server-side | eslint for MCP servers | Server conformance, not model |

## The surviving wedge (concrete)
Nobody publishes a **live, public, signed leaderboard that scores MODELS on
conformance + tool-poisoning safety TOGETHER, with reproducible signed rows.**

- MCP-Mark/Atlas/mcpbench: **competence only.**
- MCPTox/MCP-SafetyBench: **static papers or server-side**, no combined
  model-side board.
- Ours: model × protocol × deterministic gate → signed, re-runnable rows.

## Honesty register
- **REAL (verified):** the six competitors above and their scope.
- **CONFIRMED GAP:** no combined model-side conformance+safety live scoreboard
  found. (Absence from a bounded search still can't *prove* none exists —
  but the closest candidate, MCP-Mark, is explicitly competence-only and
  single-benchmark, so the combined-and-signed niche is genuinely open.)
- **Refinement:** our differentiator must be stated as *"the only model-side
  MCP board that fuses conformance AND tool-poisoning safety with signed,
  reproducible rows"* — NOT "the only MCP leaderboard". The latter is false
  (MCP-Mark exists); the former stands.

## Next (owner directive a+B+c)
A (protocol-tensor core) is **DONE** (`302c5475`, 8/8 tests, real-MCP e2e).
B (request_measurement MCP server) and C (OpenScoreboard page) are the next
two slices; the competitive verdict above sharpens their copy.
