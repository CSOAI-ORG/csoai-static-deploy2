# District Build-Map — the safe-sandbox model-vs-others benchmark arena
**2026-08-13. Internal planning doc. Names here are INTERNAL — see naming gate at end before anything ships publicly.**

## The one product

Not 14 things. One: **a contained sandbox that runs your model against others and emits signed benchmark results.** The 14 "districts" are the *scenarios*; the security hive is the *adversarial pressure*; the arena engine is the *scorer*; the jail is the *containment*; the pod is *where it runs*. Most of it is already built — the gap was integration, not invention.

## What exists vs what's missing (evidence-based, from the estate sweep)

| Layer | Component (path) | Status |
|---|---|---|
| **Scorer** | `SOVOS/packages/sovos-city/{bench,tail,durable_board}.py` · `make_leaderboard.py` | **BUILT** — Wilson CIs, correlated-failure, tie-aware, honest UNMEASURED |
| **Arena (model vs others)** | `councilof-ai/arena/functions/api/battle.ts` (live, statute-judged) · `arena.py` · `SOVOS/packages/sovos-arena/` | **BUILT / partly LIVE** |
| **Containment jail** | `rce_sandbox.py` (ASI05: sandbox-exec/firejail, escape detection) | **BUILT** (detection, not OS boundary) |
| **★ Arena × Sandbox seam** | `sandbox_arena.py` — duel inside the jail, one record, escape disqualifies | **BUILT TODAY** — selftest PASS |
| **Security hive** | `sov-hive/src/rainbow.rs` (7-layer) → `councilof-ai/functions/api/security.ts` `hive-lens-detection` | **BUILT / MEASURED** n=40, 0.88 |
| **Red-team board** | `redblue_v2.py` (50 attack cells, durable) | **BUILT, UNSCORED** — grader awaits gold-validation gate |
| **PQC / continuity** | `pqcbench.py` · `build_asi_bank.py` (gspc-asi) | **BUILT** (asi MEASURED n=13, below floor) |
| **Signing** | `sign.py` (Ed25519, key on pod) · OSCAL wrap `oscal_article50.py` | **BUILT / on RunPod** |
| **Compute** | `deploy_secure_pod.py` (A100/H100 targets) · live RTX 3090 pod | infra present; A100 not currently running security sim |

## Districts → what backs each, and build order

| # | District (internal) | Maps to | Backed by | Status |
|---|---|---|---|---|
| 1 | Tool Bazaar | MCP | `gspc-mcp` bank → **MCP scoreboard (PR #147)** | page BUILT, board UNMEASURED (needs diverse fleet) |
| 2 | Transparency Office | EU AI Act Art. 50 | **Article 50 pack (PR #146)** — signed, browser-verifiable | **BUILT + verified** |
| 3 | City Hall / Proving Ground | model-vs-model + robotics | `battle.ts` + **`sandbox_arena.py`** | seam BUILT today |
| 4 | *(security overlay on all)* | red/blue + rainbow | `redblue_v2.py` + `rainbow.rs` hive | hive BUILT; redblue unscored |
| 5 | Embassy Row | A2A | — (arena adapter extends here next) | NOT built |
| 6 | Oracle Market | ERC-8004 | — | NOT built |
| 7 | The Underwriters | insurance evidence | signed-card → questionnaire mapping | NOT built |
| 8–14 | Signal Exchange, Law Quarter, Merge Court, Fleet Gates, The Menagerie, Foundry, Glass Arcade (shelved) | various | scattered | shells / unbuilt |

## Recommended build order (dependency-first)

1. **✅ Arena × Sandbox seam** (`sandbox_arena.py`) — done today. Next: wire it to `battle.ts`/`arena.py`'s real endpoints on the pod (replace stub entrants with live model outputs) and sign each record with `sign.py` on the signing node.
2. **Validate `redblue_v2`'s grader** against its 36-cell gold worksheet → unlock the first *scored* red/blue board. It refuses to publish until this passes — correct; do it, don't bypass it.
3. **Fleet separation** (the recurring blocker) — a diverse cross-lab fleet via OpenRouter on the pod → moves the MCP scoreboard and the duel from UNMEASURED to a real ranking. Needs the OpenRouter key placed on the pod (owner action; secret).
4. **Embassy Row (A2A)** — extend the `Target` adapter to an A2A endpoint; the seam and scorer are reused unchanged.
5. **The Underwriters** — signed-card → insurer-questionnaire converter (Armilla/AIUC field maps).

## Honest constraints (state these on any surface)
- `rce_sandbox` is escape-**detection**, not provable isolation. "Safe sandbox" = *monitored containment*, not *guaranteed*. A `UNKNOWN` backend means containment was not actually enforced.
- `redblue_v2` must stay UNSCORED until its grader passes gold validation.
- Model-scoring boards stay **UNMEASURED** until a diverse fleet separates them — no false rankings.
- `sandbox_arena` records are **UNSIGNED** off the signing node, and labelled so; signing happens on the pod.

## Naming gate (before ANY of this touches a public surface)
- **OK public:** rainbow, arena, battle, scoreboard, MCP, Article 50, sandbox.
- **NEVER public:** `SOVOS`, `sov-hive`, `sov6`, `sov-brain`, `Council-34`-as-"sov", "sovereign OS", any `sov<n>`. Public name for the city is **Council City**, not SOV City. Internal candidate models render as `internal-candidate-NN` (see MCP scoreboard build-time assertion).
