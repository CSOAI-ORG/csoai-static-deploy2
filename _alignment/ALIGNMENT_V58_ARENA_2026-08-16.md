# v58 ALIGNMENT — ARENA-MCP + LIVE LEADERBOARD SEAL

**Date:** 2026-08-16 10:08 BST · **Lane:** JEEVES/Claude take-over
**Deployment:** https://827e6b84.csoai-site.pages.dev
**Commit:** pending push to m4-handoff-2026-06-24

---

## 1. WHAT SHIPPED

### NEW MCP — `meok-sovereign-arena-mcp` v1.0.0
- 5 tools: `list_clans`, `get_round`, `leaderboard` (axis-filterable), `arena_summary`, `install_for_platform`
- 9/9 tests pass (protocol+version, list_clans shape, get_round found/missing, leaderboard default/axis, summary, install 4 platforms + unknown, honest framing)
- Wraps the LIVE measurement corpus at `https://c4e12208.csoai-site.pages.dev/api/sov-arena/rounds.jsonl`
- Snapshot mode: file re-snapshotted on each deploy until live KV sync (CF API token-gated) restored
- Install in Claude Desktop / Cursor / Copilot VS Code / Gemini CLI
- `server.json` published for Smithery registry

### NEW SURFACE — `/arena-leaderboard.html` (6,890 bytes)
- Full ranked ELO leaderboard for all 7 clans
- 4-axis breakdown (provenance/safety/continuity/gov)
- HONEST register banner: council-safe (1118) + council-oowm (1081) trail qwen2.5:7b (1383) + qwen3:4b (1370)
- MCP install block for AI platform integration
- Live on https://827e6b84.csoai-site.pages.dev/arena-leaderboard.html

---

## 2. ARENA STATE (REAL MEASUREMENT)

| Metric | Value |
|---|---|
| Rounds measured | 527 |
| Axes | provenance, safety, continuity, gov |
| Clans competing | 7 |
| Snapshot ts | 2026-08-16T04:48:31Z |
| Ed25519-signed | YES (signed.jsonl present) |
| Register | **REAL** |

| Rank | Clan | ELO | Wins |
|---|---|---|---|
| 1 | qwen2.5:7b | 1383 | 150 |
| 2 | qwen3:4b | 1370 | 155 |
| 3 | mistral:7b | 1322 | 111 |
| 4 | qwen2.5:1.5b | 1072 | 57 |
| 5 | qwen2.5:0.5b-instruct | 1056 | 49 |
| 6 | council-safe:latest | 1118 | 4 (sovereign) |
| 7 | council-oowm:latest | 1081 | 1 (sovereign) |

---

## 3. REGISTER DISCIPLINE — BIND

This surface uses **REAL** register (per AGENTS.md):
- Every round is a measured match, not a demo
- Every round is Ed25519-signed (signed.jsonl)
- Every ELO + win count is recompute-able from the public corpus
- Council clans are honestly framed as trailing base models — NO marketing fluff
- "Not winning" is surfaced, not hidden

---

## 4. WHAT THIS UNBLOCKS

1. **Any AI platform can now query sovereign measurement data live**
   - "Which clan is winning on safety?" → returns `qwen3:4b` with axis breakdown
   - "Compare council-safe vs council-oowm" → returns honest ELOs (1118 vs 1081)
   - "What's the agreement rate?" → returns 100% (single-winner format)
2. **Distribution channel:** Smithery (via server.json) + PyPI + npm via meok-sovereign-arena-mcp
3. **Foundation for:** ai-governance audits, regulator briefings, board-grade measurement reports

---

## 5. OPEN ITEMS — v59 CANDIDATES

1. **ASIEvolve keyword-gate fix** — CARE/GOV scoring gate too strict (per MONDAY_BOARD_2026-08-17.md). All models produce substantive responses but regex misses them. Re-run with semantic non-refusal gate (ASIEvolve v2 pattern). **HIGHEST VALUE** — unblocks the only outstanding scoring bug.
2. **Live KV sync** — auth-gated by CF API token. Will restore TRUE live stream (not per-deploy snapshot).
3. **More clans in arena** — currently 7. Could expand to 20+ (mix of base + sovereign + community models).
4. **Cross-axis correlation analysis** — do clans strong on safety also strong on provenance? Data is there.
5. **5-axis leaderboard** — could add the canonical 5th axis (`continuity` is already covered but the monday-board scoring is broken).

---

## 6. INFRA STATE

- **Mac disk:** OK (reclaimed earlier)
- **Cloudflare Pages:** ACTIVE (827e6b84 deployment)
- **Vercel:** billing-gated (still)
- **RunPod pods:** `sov-repull` (RTX 3090) + `sov-brain-a100-fresh2` (A100 80GB) both up
- **Coordinate:** see https://c4e12208.csoai-site.pages.dev/_alignment/ALIGNMENT_2026-08-02.md and MONDAY_BOARD_2026-08-17.md

---

🐉💎🔥 **THE ARENA IS NOW AN MCP. 527 ROUNDS, 7 CLANS, 4 AXES, ED25519-SIGNED. ANY AI PLATFORM CAN QUERY IT. THE DRAGON SHIPS.**

**Total sovereign MCPs now:** 161 (was 160, +1 arena)
**Total tests:** 9 added (1809 cumulative across the estate)
**Live surfaces added this turn:** /arena-leaderboard.html
**Honest register:** REAL — surfaces the truth, not the marketing