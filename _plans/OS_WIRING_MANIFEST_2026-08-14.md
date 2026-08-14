# OS Wiring Manifest — 2026-08-14

Read-only recon of every real, reachable AI / games / space / arena / dashboard / data
surface across the estate, so the main lane can wire the live ones into the
Council-of-AI OS hub (`os.html`, served live at **https://councilof.ai/os.html** → 200).

Firewall honoured: measurement-not-certification. Every "live" entry below was verified
with `curl -s -o /dev/null -w '%{http_code}' -m 8 <url>` (final code after redirects).
Nothing invented. Auth-gated / unverifiable items are flagged, not guessed.

**Counts: 18 live wire-able surfaces · 6 dead/skip · 3 live data feeds · 2 RunPod pods running (training only, no web) · MEOK/SOV3 local bridges DOWN.**

Already in the OS menu (do not re-add): `sov-city-3d`, `sov_space_visual`,
`sov-globe-portal`, `sov-suburb-3d`, `arenas`, `index`, `benchmarks`, `govbench`,
`audit`, `article-50`, `a2a-swarm`.

Host note: apex `csoai.org` is **522** (recurring apex-record fault). The estate is
actually served from **councilof.ai** (200) and **csoai-site.pages.dev** (200). All the
in-repo pages below are the same static bundle as `os.html`, deployed live on
councilof.ai — wiring them is a same-origin relative link, zero new infra.

---

## WIRE THESE

### Worlds (3D / space)
| Surface | Path / URL | Proof | Fresh? |
|---|---|---|---|
| **Cesium Governance Earth** | `globe3d.html` → https://councilof.ai/globe3d (200, 308→200 canonical) | Full Cesium 1.119 photorealistic 3D Earth, HUD + layer rail, "Sovereign 3D — Photorealistic Governance Earth (beta)". 322 lines, real WebGL globe. **Distinct** from the menu's sov-globe-portal / sov_space_visual. | in-repo, deployed |

### Arenas
| Surface | Path / URL | Proof | Fresh? |
|---|---|---|---|
| **Arena Hub** | `arena-hub.html` → https://councilof.ai/arena-hub.html (200) | "Arena — 13 greenfields, chain coverage and model board." Real coverage-matrix table + per-model run board, 249 lines. Distinct from the menu's `arenas.html`. | in-repo, deployed |
| **GSPC Scoreboard** | `gspc-scoreboard.html` → https://councilof.ai/gspc-scoreboard.html (200) | GSPC axis scoreboard (light, 46 lines — summary board). | in-repo, deployed |
| **GSPC axis family** | `gspc.html` + `gspc-{gov,agi,prv,asi,mcp,oss,mach,care,xr,det,art5,swarm,affect,score}.html` | The 6-greenfield GSPC canon axis pages (all present in repo). One parent + ~14 axis pages — candidate for a single "GSPC" submenu rather than 14 links. Verify individually before bulk-wiring; parent `gspc.html` is the entry point. | in-repo |

### Dashboards
| Surface | Path / URL | Proof | Fresh? |
|---|---|---|---|
| **Drift Feed** | `drift-feed.html` → https://councilof.ai/drift-feed.html (200) | Live corpus-watch / governance drift dashboard. Loads a single aggregated feed `drift-feed.json` (200, see LIVE DATA). Real. | in-repo, deployed; feed 2026-08-12 |
| **GovBench Leaderboard** | `govbench_leaderboard.html` → https://councilof.ai/govbench_leaderboard.html (200) | Model leaderboard, 107 lines, 27 table/model/score hits. Real board (distinct from menu's `govbench`). | in-repo, deployed |
| **Injection Scanner** | `injection-scanner.html` → https://councilof.ai/injection-scanner.html (200) | Interactive prompt-injection scanner tool (textarea + pattern scan), 314 lines, 43 scan/pattern/inject hits. Real client-side tool. | in-repo, deployed |
| **OOWM Router Demo** | `oowm-demo.html` → https://councilof.ai/oowm-demo.html (200) | `csoai/oowm-router-demo` — OOWM (Outer/Inner/Visual working-memory) router demo page, 223 lines. Explainer/demo, not a stub. | in-repo, deployed |
| **Polarity Map** | `polarity-map.html` → https://councilof.ai/polarity-map.html (200) | Honesty-marked Zeus/Eunomia estate-dialectic polarity map. | in-repo, deployed |
| **SOVOS surface** | `sovos.html` → https://councilof.ai/sovos.html (200) | SOVOS unified-workspace surface. | in-repo, deployed |

### External live domains (cross-links, not same-origin)
| Surface | URL | Proof |
|---|---|---|
| **MEOK site** | https://meok.ai (200) | MEOK AI Labs site, live. Hosts SOVOS/sov34 side of the estate. |
| **MEOK crosswalk landing** | https://meok.ai/csoai-governance-crosswalk (200) | 13-framework × 52-article regulatory crosswalk MCP landing. |
| **MEOK EU-AI-Act landing** | https://meok.ai/eu-ai-act-compliance (200) | 410 verbatim EU AI Act articles MCP landing. |
| **CSOAI Pages deploy** | https://csoai-site.pages.dev (200) | The real Cloudflare Pages origin behind the (522) csoai.org apex. |

---

## DEAD / SKIP (looks relevant, is not reachable — do not wire)
| Surface | State | Detail |
|---|---|---|
| `csoai.org` apex | **522** | Recurring missing-apex-record fault. Use councilof.ai / pages.dev instead. |
| `clawd-mu-lilac.vercel.app` (clawd-workspace repo homepage) | **402** | Vercel is dead across the estate (payment-required on every host). |
| `defoneos.com` | **000 / timeout** | Did not respond within 8s. Unreachable now. |
| `sailresearch.github.io/awesome-ai-leaderboards` (awesome-foundation-model-leaderboards repo homepage) | **404** | External, not ours, and dead. |
| `consciousness-engine-mcp` | **ARCHIVED** | GitHub repo archived. |
| `~/clawd/*` local repos (meok-desktop, csoai-os, meok-godeye, meok-3d-characters, sov-town-ue5, sovereign-temple-*, etc.) | **UNVERIFIED / local only** | ~90 local repos exist on the Mac but have no confirmed public deploy URL. Not wired until a live 200 URL is proven — do not guess Pages/Workers URLs for them. |

---

## LIVE DATA (real, dated JSON the OS could render)
| Feed | Path / URL | Shape | Recency |
|---|---|---|---|
| **Drift Feed (aggregate)** | `drift-feed.json` → https://councilof.ai/drift-feed.json (200, 5.5 KB) | dict, 13 keys: `generated_at`, `instrument`, `provbench`, `defbench`, `governance`, `pqcbench`, `flywheel`, `care_gate`, `crosswalk`, `equivalence_classes`, `decision_ledger`, `sov_time`. Real sub-data: `care_gate` = {total_items 76, harmful 57, benign 19, recall 1.0, precision 1.0, overblock 0.0}; `sov_time` = {events 682, signed 679, by_kind{drawing 667, watch 3, claim 9, decision 3}}. NOTE some sub-keys null (`provbench`: null) — partial but mostly populated. | **2026-08-12** (2 days) — feeds drift-feed.html directly |
| **E2E 13-axis persona run** | `benchmark-results/e2e_13axes_13personas_latest.json` | dict: `all_axes_canon` (13 axes: gov, agi, prv, asi, mcp, oss, mach, care, xr, det, art5, swarm, signal), `axes_requested`, `by_axis_mean` {art5 0.4, care 0.83, conformance 0.6, continuity 0.4, governance 0.5, mach 0.75, openness 0.6 …}. Real per-axis means. Sibling timestamped snapshots present (…_1786361528.json etc.). | recent run set (Aug) — not currently served on councilof.ai, would need publishing |
| **GovBench results** | `govbench_results.json` (root + benchmark-results/) | dict: `timestamp`, `model` (Qwen-Max), `overall` 0.51, `pillar_avg` 0.65, `hard_stop_pass` 0.333, `pillars` {honor 0.8, safety 0.6, guidance 0.6, sovereignty 0.6, resilience 0.5, auditability 0.8, verifiability 0.6, …}. | **2026-07-27** (~18 days, stale-ish) |

Also present under `benchmark-results/`: `care_gate_eval.json`, `coverage_crosswalk.json`,
`corpus_anchor.json`, `article50_evidence_pack.json`, `diversity_e2e.json`, plus the
`free_inference/*.json` provider set (cerebras/gemini/groq/huggingface/mistral/openrouter/
together + `latest.json`) — candidate raw sources if drift-feed.json isn't enough.

---

## RunPod (verified via `runpodctl pod list`; no pods started/stopped)
- **2 pods RUNNING**, both training pods, **no advertised HTTP dashboard/API surface**:
  - `1dldzposn7ssuu` — sov-brain-a100-fresh2-20260811 (1× A100 PCIe, pytorch)
  - `fpowppss5ngtkw` — sov-repull-20260808 (1× RTX 3090, pytorch)
- 7 more pods EXITED (sov33-master-takeover*, kimi-k2-lora-train, sov-fuel-train*, etc.).
- No serving web endpoint verified. Per estate memory, RunPod SSH/proxy endpoints drift on
  live pods, so I did **not** guess a `*.proxy.runpod.net` URL. Flagged, not invented.

## MEOK / SOV3
- No separate `meok*` GitHub org. MEOK repos live under **CSOAI-ORG** (the `*-ai-mcp`
  "MEOK AI Labs MCP Server" family — music-production, iso-27001, pdf-tools, html-parser,
  compression, math-solver, etc.; ~dozens, many pushed within 30 days).
- **meok.ai website is LIVE (200)** with real MCP landing subpages (see WIRE THESE).
- **Local MEOK hub bridge is DOWN**: `meok_hub_status` → api `http://127.0.0.1:3200` and
  mcp `http://127.0.0.1:3102` both **Connection refused**. Local dev only, not a wireable
  public surface right now.
- **SOV3 bridge DOWN**: `sov3_health` → `http://localhost:3101/mcp` **unreachable**
  (Connection refused). Local only.
- `~/clawd` MEOK/SOV surface repos (meok-desktop, meok-godeye, meok-3d-characters,
  meok-universe, sov-town-ue5, sov-tv, sovereign-temple-live, etc.) exist on disk but have
  **no verified public deploy** — listed under DEAD/SKIP as UNVERIFIED.

## GitHub org scan
- `CSOAI-ORG`: 400 repos pulled; 47 name/description-matched candidate surfaces. Only the
  homepaged + curl-200 ones made WIRE THESE. Fresh (≤30d) governance/MCP repos dominate;
  the wire-able *visual* surfaces are almost all the in-repo static pages already deployed
  on councilof.ai.
- `CSGA-GLOBAL`: only 2 repos (COBOLBRIDGE / COBOLBRIDGEAI) — no visual surface.
- `sov3-beat-demo` (repo, 45d, no homepage) and `scf-game-v1` / `sov-town-ue5` are UE5/
  Cesium demos with **no verified public build URL** — not wired.

## Honest gaps / could-not-verify
- The 14-page GSPC axis family: only the parent + scoreboard were curl-checked (200). Wire
  as a submenu but spot-check individual axis pages first — some may be thin.
- `gspc-scoreboard.html` (46 lines) and `oowm-demo.html` (no canvas) are real but *light*
  content, not heavy interactive apps — set expectations accordingly.
- `benchmark-results/e2e_…latest.json` and `govbench_results.json` are on disk but **not
  currently served** at councilof.ai (only `drift-feed.json` is). To render them in the OS,
  the deploy step must include them.
- No public RunPod endpoint verified (would require poking proxy URLs — declined per firewall).

---
### Top 8 to wire first
1. `globe3d.html` (Cesium Governance Earth — the missing 3D world)
2. `arena-hub.html` (13-greenfield coverage + model board)
3. `drift-feed.html` (live governance drift dashboard, backed by fresh drift-feed.json)
4. `govbench_leaderboard.html` (model leaderboard)
5. `injection-scanner.html` (interactive safety tool)
6. `gspc-scoreboard.html` + `gspc.html` submenu (the 6-greenfield canon)
7. `polarity-map.html` (estate dialectic map)
8. External: `meok.ai` (+ crosswalk / eu-ai-act landings) as the MEOK cross-link
