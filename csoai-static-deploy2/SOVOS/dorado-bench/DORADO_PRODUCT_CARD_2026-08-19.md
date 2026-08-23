# DORADO BENCH — Product Card (2026-08-19)
**Category:** Live governance-market pair measurement · **MCP:** yes · **Registers:** MEASURED/REPORTED/UNMEASURED

## One-liner
"East↔West live regulation vs live index markets — the pair-gap nobody else measures,
deterministic, signed-ready."

## What it measures (nobody else does this)
The **distance between how East and West markets price the same regulatory moment** —
measured live, not modeled. Every governance bench scores regulation against itself;
Dorado scores regulation against the market, East vs West, in real time.

## Ingredients (all ours)
- Live quotes: 6 indices (3 East: HSI/Nikkei/SSE · 3 West: S&P/FTSE/DAX) — Yahoo v8, no auth
- Regulation bank: EU AI Act / UK AI Principles / China TC260 + GenAI Measures / Korea AI
  Basic Act / Japan AI Guidelines (canon-sourced)
- Fleet: 16-axis measured models · Arena Elo · human baselines
- Honest registers: the pair-gap is MEASURED; human/AI verdicts are REPORTED, scored, never blended

## MCP tools (5)
dorado.quote · dorado.reg_events · dorado.pair_gap · dorado.snapshot · dorado.measure

## First live read (2026-08-20 01:21 UTC)
HSI +0.22% vs S&P −0.52% → EAST_OVERPERFORMS gap +0.74%. Human 2/3, AI tape-read 9/9.

## Why it wins
- **Nobody measures "between the pair"** — the regulation↔market gap East-vs-West is unoccupied
- Deterministic + reproducible (measurement, not certification — our neutrality is the moat)
- Live, signed-ready (h3k cards), MCP-native (every agent can call it)
- Both poles covered from day 1 (EU/UK/China/Korea/Japan)

## Go-to-market hooks
1. Regulators: "your rule moved the market — here's the measured distance, East vs West"
2. Market desks: live pair-gap feed as an MCP tool
3. Bench buyers: first live regulation-vs-market benchmark with honest registers

## Build status
- [x] Core instrument (dorado_bench.py) — live, tested
- [x] MCP server (dorado_mcp.py) — 5 tools, end-to-end tested
- [x] Scoring harness (dorado_score.py) — humans vs AI, MEASURED vs REPORTED
- [ ] Fleet AI verdicts (needs pod ollama reinstall — fleet lane)
- [ ] Signed h3k cards per snapshot (chain into estate)
- [ ] Public board page + badge (deploy lane)
