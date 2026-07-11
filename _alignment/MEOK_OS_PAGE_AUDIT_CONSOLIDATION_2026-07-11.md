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

## Bridges applied (safe, additive)
- ✅ `sovspace3d.html` rebuilt on **real Cesium** (DEFONEOS engine parity) — no longer arcade.
- ✅ Surfaced it in the OS nav as **"🌐 SOV Space — the 3D world"** (was orphaned; only the character
  card linked it). Now discoverable from the main menu.
- ✅ Confirmed `cop.html` is only a code-comment reference in sovspace3d (not a broken link/404).
- ✅ Character companion now carries the **DEFONEOS Sovereign/Horus voice** (one spine, two markets).

## Convergence executed 2026-07-11 (Nick: "eat/absorb into ONE, one by one")
- ✅ **One Cesium version.** Pinned `sovspace3d` 1.118 → **1.123** to match `earth3d-photoreal` (the
  OS's other globe). Re-verified render on 1.123.1 (globe + labels + fly-to intact). No version drift.
- ✅ **Killed the duplicate 3rd globe.** `universe.html` (old three.js "Sovereign Universe") is now a
  **redirect → `/sovspace3d.html`** (canonical + reversible; old links keep working). Down to ONE
  three.js-globe = zero; the WebGL globe engine is now Cesium everywhere.
- ▢ `hatch-demo.html` / `legacy-demo.html` = **real standalone demos, NOT globe dupes** — surface
  (link) them rather than delete; `embed-test.html` = dev-only, keep out of nav.

## Remaining deliberate step (the big ONE — needs its own careful pass)
- **Merge the two Cesium globes.** `earth3d-photoreal` ("MEOK Earth", node-select → Sovereign speaks,
  iframed into the OS) and `sovspace3d` ("SOV Space world", standalone) still overlap. Target = **one
  Cesium world, two entry intents** (🌍 *my data/nodes* vs 🌐 *explore*). Requires porting the
  node-select + trust overlay wiring into sovspace3d — real work, do it as one focused change, not a
  silent half-merge. Until then both are pinned to Cesium 1.123 so there's no drift.
- **Disambiguate "SOV Space"** fully: fold the tools list (`sovspace.html`) into the world's
  Agents/J-Space face so "SOV Space" means ONE thing.

## Honest status
Front now **matches back better**: the real 3D world exists and is reachable; the companion speaks the
sovereign voice. The remaining work is *convergence* (one globe, one "SOV Space" meaning) — a deliberate
refactor, flagged here so it's not lost, not a silent rebuild.
