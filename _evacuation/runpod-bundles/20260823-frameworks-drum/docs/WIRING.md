# WIRING — how the drum connects

The FRAMEWORKS DRUM is a living knowledge pack in the harness mono repo
(`master-harness/knowledge/frameworks-drum/`), wired so any instance, agent, or external
tool can query it over the estate's standard protocols.

## 0. The substrate it feeds (councilof-ai-monorepo — verified 2026-08-20)

Per the deep-mine that grounds the master framework doc, the drum is NOT the substrate — it is
the **intake/catalog layer**. The substrate is the existing monorepo:

- **`/Users/nicholas/clawd/councilof-ai-monorepo`** (org mirror `councilof-ai-monorepo`) —
  apps/ charter/ evidence/ ops/ packages/ registry/ research/ with **55 csoai-* packages**
  migrated ("55/55"). Registry/ is currently EMPTY — the one-registry target
  (`registry/{mcp,a2a,did}/mcp-catalogue.json`) is a [GAP] to build, not done.
- The master doc's real target shape (apps/site, packages/receipts, core, crosswalk, gspc,
  frameworks, regwatch, registry, charter, frameworks-corpus, evidence) is the plan of record:
  finish + wire + dedupe, not start. See `docs/MASTER_FRAMEWORK.md` §5.
- **Drum ↔ substrate division of labour:** the drum catalog is the *living index* of every
  framework/charter/regulation/article (estate + web); `packages/frameworks` in the monorepo
  is the *FRAMEWORK_GROUND_TRUTH* (verified-to-primary-source). Both are needed; neither
  substitutes for the other. The drum's `_mining/` + `catalog.json` feed the ground-truth work.
- **Top dedupes to run against the monorepo** (from the master doc): signed-receipt ×5 → one ·
  MCP-count drift (843 dirs/207 repos/~200 marketplace → one registry) · crosswalk ×3 ·
  52-article charter ×4 · corpus-watch ×2 · Article-50 ×5 · retired-deploy shadow copies
  (csoai-static-deploy2 / kimi-regen / csoai-org-v2 / csoai-platform) → quarantine + harvest + retire.
- **did:web live state (drum re-check 2026-08-20, corrected):** apex `csoai.org/.well-known/did.json`
  serves site-release-1 + estate-chain-1 + board-attestation-1 (3 keys); mirror
  `councilof.ai/...` serves those three **plus card-attestation-1** (4 keys) — the
  machine-contract split-brain guard trips on the mismatch. **Reconcile plan (one PR, deploy
  lane's go):** add `card-attestation-1` to the apex copy AND add the DSH signing key
  `o32UOkcsCnpSd5u-GALIWDTrpVY1ibxirnIWJrObb-w` as `did:web:csoai.org#dsh` (env wired to the
  new seed; `council_sign` CLI returned no JSON on that subcommand — CLI-shape quirk to debug,
  not a key problem).
- **Signed-receipts consolidation (spec `clawd/_alignment/SIGNED_RECEIPTS_CONSOLIDATION_SPEC_2026-08-20.md`):**
  the signed-receipt primitive exists 5+ times (inspect-receipts canonical · a2a-signed-receipts ·
  defoneos-sign · codabench scorer · corpus-watch); canonical core = `SOVOS/inspect-receipts`
  (RFC 8785 JCS, content_id = sha256(canonical minus sig), Ed25519, fail-closed, e2e 5/5 PASS).
  **Gating:** the spec says consolidation must not ship until the did:web root serves the real
  keys — drum check 2026-08-20: the apex NOW serves the live 03g9l site-release-1 key
  (orphan-key state already resolved on the apex); the mirror is still divergent.
- **Monorepo current gaps (drum check):** `apps/` = docs, meok, site (site exists — target
  shape's apps/site is live); `charter/` EMPTY (52-article canonical charter not yet installed);
  `registry/` EMPTY (mcp-catalogue.json not yet built); `packages/csoai-crosswalk` EXISTS
  (crosswalk ×3→1 dedupe target); no packages/{receipts,gspc,regwatch} yet.

## 1. MCP (Model Context Protocol)

- **Manifest:** `mcp/manifest.json` — declares the server and its tools.
- **Server:** `mcp/frameworks_drum_server.py` — **stdlib-only** Python (no deps, no venv),
  JSON-RPC 2.0 over stdio. Reads `catalog.json` on every call.
- **Tools:**
  - `drum_catalog` — counts and kinds in the drum
  - `drum_search` — free-text query over items (name, kind, jurisdiction, status, binding)
  - `drum_get` — one item by id
  - `drum_crosswalk` — find items that connect a source and a target (charter↔framework links)
- **Registry:** tile id `frameworks-drum` added to `master-harness/mcp/registry.yaml`
  (the MCP composition board). Instances list the tile id in their `instance.yaml`.

Run it: `python3 master-harness/knowledge/frameworks-drum/mcp/frameworks_drum_server.py`
(speaks MCP JSON-RPC on stdin/stdout; test with the bundled `--selftest` flag).

## 2. A2A (Agent-to-Agent)

- **Card:** `a2a/agent-card.json` — presents the drum as an agent card: `name`,
  `description`, `url`, `version`, `skills` (the four MCP tools), `endpoints`.
- The card is honest by construction: it describes a catalog service, not an autonomous agent.

## 3. llms.txt

- `llms.txt` at the pack root — a plain-text index an LLM can read in one shot:
  what the pack is, where the master doc is, where the catalog is, the counts.

## 4. Harness knowledge packs

- `knowledge/PACK_INDEX.md` in master-harness registers the pack:
  `- id: frameworks-drum` with `source` and `learn` pointers.
- Instances load it via `instance.yaml knowledge.packs`.

## 5. The living rule

- `_mining/` is the intake tray; `build_catalog.py` folds it into `catalog.json` + cards.
- The MCP server never caches — every call re-reads the catalog, so a fresh `build_catalog.py`
  run is immediately visible to any client. No restart, no deploy.

## 6. Destinations — EAT · WEST DORADO · SOV SIGNAL · markets (honest wiring map)

The drum's data is the right *shape* for the estate's live instruments, but most legs are
**NOT yet wired** — this is the map, with honest status. `build_catalog.py` already emits the
delivery feeds (`feeds/reg_events.json`, `feeds/eat_7box.json`); the destination lanes must
consume them.

| Destination | What it is (verified) | Drum feed | Status |
|---|---|---|---|
| **EAT (7-box mission loop)** | measured → CI'd → signed → chained → anchored → boarded → mirrored; the DRUM loop's mission definition | `feeds/eat_7box.json` — the drum's own 7-box self-check, honest per box (currently 3/7 true, 2 partial, 2 false: measured/boarded/mirrored true; ci/chained partial; signed/anchored false) | **PARTIAL — board live at frameworks-drum.pages.dev; signed/anchored remain [GATE]** |
| **DORADO BENCH (WEST pole)** | East↔West live regulation vs live index markets pair-gap (6 indices: HSI/Nikkei/SSE vs S&P/FTSE/DAX; reg bank EU/UK/CN/KR/JP; MCP tools dorado.quote/reg_events/pair_gap/snapshot/measure). **Three binding boundaries (master doc §9): (1) composed, never fused — the market leg is a REPORTED context leg, never blended into one number; (2) licensed data source before assertion — stays `NOT_PRESENT` until then; (3) never a trading signal or investment product — measures and reports, never advises** | `feeds/reg_events.json` — 121 regulation events with binding/status/effective, tagged east/west/global — a ready sync source for DORADO's `REG_EVENTS` (their file is hardcoded in their lane; they consume this feed) | **NOT WIRED — feed ready; DORADO lane to sync; market leg stays `NOT_PRESENT` until licensed** |
| **SOV SIGNAL (the trust-gauge index)** | Fisher-Rao distance from permitted manifold ≡ Merton/KMV distance-to-default; composed GSPC axes (Fisher ideal index); customers = insurers (param triggers), enterprises (EU AI Act evidence), agent markets (ERC-8004/AP2/x402). Same hard line as DORADO: **context, never advice; never a trading signal** | `feeds/reg_events.json` = the **regulatory-pressure feature channel** (binding dates, enforcement switches e.g. EU AI Act live 2 Aug 2026, penalties) — observable covariates for the index | **NOT WIRED — feature channel ready; sov_signal lane to integrate** |
| **Stock markets (live)** | DORADO already pulls live 6-index quotes (Yahoo v8); the drum does not touch markets directly | Indirect: drum reg-data → DORADO reg_events → pair-gap vs live quotes; drum mining freshness → `dorado.reg_events` | **NOT WIRED (indirect by design)** |

**The "evolved data" caveat (binding):** today the drum supplies *mined/living data* (catalog,
mining, doctrine, feeds). The **evolve** outputs — 90/10 router decisions, promote-gate
results, Knowledge-archive residue (Stage 1 of the master doc) — do not exist yet. When they
land, they flow through the same feeds: router/promote decisions emit signed cards → EAT
7-box (signed/chained/anchored), reg-drift findings → DORADO reg_events, and measured
capability deltas → SOV SIGNAL features. The pipes being laid now are the ones those outputs
will travel on.

## 7. Flow agents (availability register — verified 2026-08-20)

For estate flows that need a terminal agent CLI:
- **OpenCode — AVAILABLE** at `~/.opencode/bin/opencode` (MIT — the fork-register-approved
  terminal agent CLI; doctrine-preferred).
- **claude CLI — AVAILABLE** at `~/.local/bin/claude` (UX patterns only, never source).
- **Cursor CLI — NOT installed** (and per fork-register: CLOSED, do not fork — SpaceXAI).
- **codex CLI — NOT installed** (Apache 2.0 — installable if a lane needs it).

The 100-move plan (`docs/NEXT_100_MOVES.md`) is the execution queue; move 99 onboards OpenCode
as a flow agent for estate tasks.

## 9. Published surface — the full stack (LIVE 2026-08-22)

The drum spans every layer of the estate's business stack as a complete, live product surface:

| Layer | What | Where |
|---|---|---|
| **Content (front end)** | every item browsable as a content page, doctrine-clean | https://frameworks-drum.pages.dev — `/` (overview) + `/frameworks` · `/charters` · `/regulations` · `/articles` · `/sectors` (clean URLs, all 622 public items pre-rendered) |
| **Service (API/MCP/A2A)** | 8-tool MCP server + A2A card + llms.txt | `mcp/frameworks_drum_server.py` (drum_search/get/crosswalk/watch/freshness/route/history/catalog) — tile `frameworks-drum` in the harness registry |
| **Data (back end)** | catalog.json (662 items) + cards + graph + feeds | `catalog.json` · `feeds/reg_events.json` (126) · `feeds/catalog_graph.json` · `feeds/gauge_features.json` |
| **Feature (model)** | learned NN/GNN embeddings → the SOV SIGNAL gauge input | `train/` (kind .65 / binding .87 / status .854 / GNN .691) → `feeds/gauge_features.json` |
| **Product (consumers)** | feeds + features feed SOV SIGNAL, DORADO pair-gap, the compliance gateways | `feeds/` → SOV SIGNAL feature channel · DORADO reg_events · EAT 7-box |

**Business-stack rule:** the drum is the *reference + feature* layer; it never replaces the measured
gauge (SOV SIGNAL) or the products that consume it — it feeds them. The board is the public
content surface; the MCP/A2A is the machine surface; the feeds are the product inputs.

## 9b. Published surface (deploy)

- **Board:** https://frameworks-drum.pages.dev (Cloudflare Pages project `frameworks-drum`) —
  the doctrine-clean reference index, generated by `site/build_drum_site.py` (index.html +
  drum.html + drum.llm.json), regenerated with every catalog build + nightly, deployed via
  `ops/publish_drum.sh`.
- **Not the locked apex:** this is a *new* project (my lane); the csoai-site / councilof-ai
  deploy-lock is respected — the drum board never touches the apex surface.
- Doctrine-clean verified live (0 banned strings); honest footer (reference index, not a
  trust score).

## 8. Dual-walk (TEA × EAT) alignment

**Doctrine (mesh, K3-aligned):** EAT walks forward (premise → artifact: build, sign, publish);
TEA walks backward (artifact → premises: re-derive content_ids, re-verify signature labels).
The claim is earned where the two walks meet; divergence = anomaly logged loud. The estate's
mesh runs a `dualwalk` daemon (6h cadence) on signed boards; **the drum runs its own backward
walker.**

**Drum implementation — `archive/dualwalk.py`** (verified 2026-08-21, first run clean):
- recomputes every archive entry's content_id from its own bytes (EAT forward artifact → TEA
  backward proof) — 205 entries walked, 0 drift
- checks signed-label drift (signed:true without signature = loud anomaly) — the drum's
  archive is honestly unsigned (`signed:false`, no #dsh rail yet), so the walker guarantees
  no future drift can hide
- re-verifies the catalog canary + card coverage (forward state)
- writes `feeds/dualwalk_report.json` with the verdict ("EAT meets TEA — claim REAL" or
  "DIVERGENCE")
- runs in the standing check (15-min) and the overnight cycle

The drum TEA-walks its archive forever; the mesh dualwalk daemon covers the signed boards.
One framework, two directions, zero trust required — the estate checks its own homework in
public.
