# MEOK MASTER — Consolidated Source of Truth
**Date:** 2026-06-23 · **T-11 to July 4 2026 (23:59 BST)** · **Machine:** this one = MEOK build host (CSOAI work lives on the M2)

> This is the **index that ties the scattered masters together** — not a replacement for them. When a section says "see X", X is the canonical detail doc. Point other agents/tabs at THIS file first.

---

## 0. The machine split (decided)
- **This machine (here)** = **MEOK** build/run host. Flywheel, hives, gaming, Hermes, sovereign-town all run here.
- **M2 MacBook** = **CSOAI** (site, compliance, GTM). Hand-off doc: `CSOAI_M2_HANDOFF_2026-06-23.md` (pushed to `CSOAI-ORG/clawd-workspace`).
- Coordination across machines is via the **`CSOAI-ORG/clawd-workspace` git repo** + the **swarm ledger** (`/api/swarm/emit` → sovereign-town).

## 1. Architecture (layered — the one true stack)
```
sovereign-town  → Ed25519 episode ledger (THE MOAT: governed-vs-ungoverned, attested)
      ↑ reads/anchors
meok-saas       → product dashboard + billing (Clerk+Stripe, attestation-gated)  ← canonical product surface
meok-ai (/ui)   → marketing flagship (meok.ai live)                               ← canonical marketing surface
meok-town-view  → 3D town viz (Vite+R3F, embedded in meok-ai)                     ← presentation only, reads ledger
```
Rule (binding): **the society sim stays headless; renderers/engines read the ledger, never run the sim.** See `sovereign-town/ARCHITECTURE_GUARDRAIL.md`.

## 2. Canonical sub-docs (don't duplicate these — update them)
| Doc | Owns |
|---|---|
| `SOVEREIGN_TOWN_MASTER_PLAN_2026-06-19.md` | The flywheel moat: 24/7 towns, ledger, openpatent, MEOK Labs publishing |
| `JULY4_MASTER_PLAN_2026-06-16.md` | The 29-hives → 100/100 launch rollout |
| `MASTER_EXECUTION_PLAN_D31.md` | Daily gates + cluster schedule to July 4 |
| `CSOAI_LAYER0_UP_MASTER_STACK_2026-06-19.md` | The layered architecture (above) |
| `CSOAI_CANONICAL_MAP_2026-06-23.md` | MEOK↔CSOAI boundary / surface reconciliation |
| `CSOAI_ALIGNMENT_AND_BRIDGE_2026-06-23.md` | Swarm wiring (G6: claude/hermes/kimi) |
| `sovereign-town/ARCHITECTURE_GUARDRAIL.md` | Sim-vs-renderer decoupling + reusable-OSS license table |

## 3. July 4 plan (T-11) — what "ready" means
**Launch gate:** 29 hives at 100/100 by 4 Jul 23:59 BST. **Proof points (the demo):** (1) one verified compliance report, (2) one openpatent disclosure, (3) one real revenue transaction — each Ed25519-signed into the ledger.
**Gates still on Nick (deploys/creds):** Vercel deploy, API key, Hermes bridge live, WhatsApp/Telegram channel, `/signup` flow. (Per `MASTER_EXECUTION_PLAN_D31`.)

## 4. The BIG 3 (gaming) — VERIFIED 3/3
`meok-gaming/mcp-gaming-empress`, verified via `scripts/big3.mjs`:
- **blizzard-wow-mcp** (10 tools) — private AzerothCore/TrinityCore, intelligence-only.
- **fortnite-uefn-mcp** (7 tools) — authoring only, runs outside island (UEFN §2).
- **gta-fivem-mcp** (6 tools) — private FiveM RP only.
All compile, pass handshake, emit Ed25519 attestations to the ledger. ⚠️ Marketing copy ("$200B / 6 MMOs / zero competitors") is **unverified** — superseded by this honest status.

## 5. Hermes + swarm
- **Hermes** = multi-platform agent gateway, **running now** (daemon PID 1197). Model: OpenAI `gpt-4o-mini` → local Ollama `gemma3:4b` fallback. Code: `~/.hermes/hermes-agent/`.
- Wired two ways: **(a) MCP tools** `hermes_ask`/`hermes_research`; **(b) swarm emitter** via `/api/swarm/emit` (server-held per-agent Ed25519 key).
- Swarm = **claude + hermes + kimi** → all produce `verified_done` with anchor ids.
- ⚠️ **Honest gap:** Hermes' emit is contract-built but **not E2E-tested** (no emit script in the gateway repo; manual cross-check only). WhatsApp channel timing out (non-blocking).

## 6. Recently shipped (by parallel agents, today)
- **Protocol 0** router hardened on csoai-platform (identity/comms/trust/txn/governance + snapshot), Stripe payments real, JSON state store, server `@shared/const` startup bug fixed → pushed `clawd-workspace` (b4fdd566).
- **MEOK design system** (`meok-tokens.css`, warm sovereign palette + orb) → new `meok.ai/index.html`, `csoai-org/meok-ai.html`, platform `meok-theme` → pushed (5c8034d7 / f9a8387).

## 7. Honesty register — hard truths to carry (do NOT bury these)
- **Council** still ~37% default-A ties in some paths; moat claims must filter `attestable=True`.
- **csoai.org `/verify`** currently validates nothing; public export ships nothing signed (self-attestation gap).
- **🔴 SECURITY:** `.town_priv.key` (canonical King key) sits **unencrypted on a mac** — contradicts "King key never on machine"; reconcile before any local King signature.
- **proofof.ai** stuck on wrong Vercel account (team_4Ik vs niks-projects).
- **M4 can't host the 80GB backbone** — don't promise local hosting of it.
- **EU AI Act** high-risk obligations moved to **2027**; lead with in-force DORA/NIS2/GDPR. Kill the recurring "Aug 2 countdown" hype.
- **LiteLLM CVE-2026-42271 (CVSS10)** in meok-agent-zero — PATCHED ≥1.83.7 (keep pinned).
- **meok-os has no git remote** — M2 cannot pull it; set a remote before relying on it.

## 8. Open blockers / next (in priority order)
1. Set `meok-os` git remote + commit its 11 dirty files (unblocks M2).
2. E2E-test the Hermes `/api/swarm/emit` path (close the "untested" gap).
3. Commit/push the dirty MEOK repos (meok-ai, meok-saas, meok-ai-frontend, meok-compliance-gateway) so M2 sees current state.
4. Reconcile the King-key security finding before any local King signature.
5. Drive the 5 July-4 gates (all need Nick).
