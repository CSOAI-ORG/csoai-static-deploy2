# 🧭 MEOK OS — page-by-page audit + consolidation/bridge plan (2026-07-11)

Nick: *"we have loads random lost pages… get that all together, front-end visual aesthetically,
inspect page by page and set full plan and bridge so front matches what we have… the flow of the
menus half of it don't make sense."* This is that audit. Scope = `meok-os-deploy/` (→ os.meok.ai).
Honest register: what's wired, what's orphaned, what's duplicated, and the single-engine target.

## The 16 pages, by role
| Page | Role | Engine | Wired from | Verdict |
|---|---|---|---|---|
| `index.html` (273 KB) | **The OS shell** — nav, desktop tiles, Sovereign dock, tours | — (2D) | root `/` | ✅ canonical shell |
| `character.html` | The Sovereign companion (3D light-being + chat + MCP cards) | three 0.169 | nav, dock | ✅ canonical companion |
| `sovspace3d.html` | **SOV Space — the 3D world** (rebuilt 2026-07-11) | **Cesium 1.118** | character card + (now) nav | ✅ the wow surface |
| `earth3d-photoreal.html` | "MEOK Earth" integrated map (node-select → Sovereign speaks) | **Cesium 1.123** | index `meokEarth3DUrl()` | ⚠️ 2nd globe, version-drifts from sovspace3d |
| `earth3d.html` | MEOK Earth fallback (no token) | — | index `meokEarth3DUrl()` | ⚠️ 3rd globe (fallback) |
| `sovspace.html` | "SOV Space — the tools" — flat marketplace list | — | nav, dock | ⚠️ **name-collides** with the 3D world |
| `pricing.html` | Plans & pricing | — | nav, dock | ✅ wired |
| `badges.html` | Authority badges | — | nav, dock | ✅ wired |
| `verify.html` | Verify a badge | — | nav | ✅ wired |
| `registry.html` | Signed-card registry | — | nav/tour | ✅ wired |
| `systemcard.html` | Signed MOD system card | — | linked | ✅ wired |
| `flightrecorder.html` | AI flight-recorder (SIGIL) | — | linked | ✅ wired |
| `universe.html` | Old "universe" globe demo | **three 0.160** | **nobody** | 🔴 ORPHAN — supersede by sovspace3d |
| `hatch-demo.html` | Old hatch animation demo | — | **nobody** | 🔴 ORPHAN — superseded by character.html hatch |
| `legacy-demo.html` | Old legacy-bridge demo | — | **nobody** | 🔴 ORPHAN — superseded by OS legacy surface |
| `embed-test.html` | Embed sandbox | — | **nobody** | 🔴 ORPHAN — dev scratch, keep out of prod |

## The two real problems (why "the flow doesn't make sense")
1. **THREE globes, three Cesium/three versions.** `earth3d-photoreal` (Cesium 1.123) is the OS's
   "MEOK Earth"; `sovspace3d` (Cesium 1.118, new) is "SOV Space — the world"; `universe.html`
   (three 0.160) is a dead third. A user meets two near-identical globes under different names.
2. **"SOV Space" means two different things** — the 3D world (`sovspace3d`) *and* the flat tools
   list (`sovspace.html`). That's the menu confusion. (The arcade complaint was the old
   three-globe `sovspace3d`; now rebuilt on real Cesium.)

## Bridges applied today (safe, additive)
- ✅ `sovspace3d.html` rebuilt on **real Cesium 1.118** (DEFONEOS engine parity) — no longer arcade.
- ✅ Surfaced it in the OS nav as **"🌐 SOV Space — the 3D world"** (was orphaned; only the character
  card linked it). Now discoverable from the main menu.
- ✅ Confirmed `cop.html` is only a code-comment reference in sovspace3d (not a broken link/404).
- ✅ Character companion now carries the **DEFONEOS Sovereign/Horus voice** (one spine, two markets).

## Recommended next consolidation (deliberate pass — NOT done yet, needs a focused session)
1. **One globe engine.** Pick Cesium **1.123** (already the OS default via earth3d-photoreal) and
   pin sovspace3d to the same version; delete the three.js `universe.html`. Then decide: does
   "MEOK Earth" (your nodes on a map) and "SOV Space — the world" (explore the globe) stay two modes
   of ONE Cesium surface, or merge? Target = **one Cesium world, two entry intents** (my data / explore).
2. **Disambiguate "SOV Space."** Make the 3D world the primary "SOV Space"; the tools list becomes a
   *tab/face inside it* (the Agents/J-Space faces already gesture at this) or renamed "SOV Tools".
3. **Delete the 3 dead orphans** from prod (`universe`, `hatch-demo`, `legacy-demo`); keep
   `embed-test` out of the deploy (dev-only). Migrate any unique value first, don't just rm.
4. **Pin all CDN versions** (three 0.160/0.169, Cesium 1.118/1.123) to one each — reduces drift + bytes.

## Honest status
Front now **matches back better**: the real 3D world exists and is reachable; the companion speaks the
sovereign voice. The remaining work is *convergence* (one globe, one "SOV Space" meaning) — a deliberate
refactor, flagged here so it's not lost, not a silent rebuild.
