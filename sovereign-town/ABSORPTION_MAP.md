# Sovereign Temple → Sovereign Town Absorption Map

**Date:** 2026-06-21  
**Agent:** JEEVES (Kimi Code CLI)  
**Status:** Full takeover executed. Older `sovereign-temple*` runtimes are kept alive as substrate primitives while governance logic migrates into the `sovereign-town` simulation engine.

---

## Why absorb?

`sovereign-temple` and `sovereign-temple-live` were built as the live SOV3 assistant / consciousness runtime. `sovereign-town` is the governed agent-world research engine that turns the same principles into a reproducible, Ed25519-attested data flywheel. The old stack is **source primitives + live runtime**, not waste.

---

## Mapping

| Temple primitive | Town successor | Files |
|---|---|---|
| Care membrane / Sovereign Gate | In-simulation zero-trust gate + pheromone alarm | `p0_aqua/gate_access.py`, `p0_aqua/pheromone_bus.py` |
| 12-around-1 BFT council | VM `sovereign_bft.py` + in-simulation council vote | VM `/home/nicholas/sov3/sovereign_bft.py`, `p0_aqua/sim.py` council dynamics |
| Ed25519 sigil / attestation | Agent passports + signed ledger + public verifier | `p0_aqua/agent_passport.py`, `p0_aqua/sign_lib.py`, `verify/index.html` |
| Agent identity / passports | King + 28 hive passports, offline-verifiable | `p0_aqua/passports/`, `p0_aqua/verify_chain.py` |
| Overnight learner / dream engine | `flywheel_forever.py` auto train+report cycle | `p0_aqua/flywheel_forever.py`, `p0_aqua/flywheel_train.py` |
| Memory / insights | Signed ledger + per-hive whitepapers in MEOK Labs | `p0_aqua/flywheel_ledger_*.jsonl`, `../meok-labs-engine/research/sovereign-town/` |
| Content / video / media engine | Future P2 town show layer (not yet built) | `sovereign-temple-live/content_engine.py` (reference) |
| Adversarial corpus | Retained as-is; feeds red-team signals | `sovereign-temple/security/adversarial_corpus_server.py` |

---

## What stays running

- `sovereign-temple` SOV3 MCP server on Mac `:3101` (legacy fallback)
- `sovereign-temple-live` overnight learner (kept until town show layer replaces it)
- `sovereign-temple` security adversarial corpus server
- VM SOV3 substrate (SOV3, OLM brain, King Hive, EU gateway, council)

## What is now deprecated

- Hermes sovereign cron jobs (paused, backed up)
- Claude Desktop `sovereign-*` scheduled skills (renamed to `_migrated-sovereign-*`)
- One-off research scripts in `sovereign-temple-live/` (moved to `_archived/`)

---

## Daily flow under Kimi management

1. **Mac + VM flywheels** generate disjoint seed ranges 24/7.
2. **Kimi-managed launchd runners** collect status every 10 min, pulse SOV3 at 09:00, morning briefing at 07:00, consciousness integrity at 06:00, tunnel watchdog every 2 min.
3. **GitHub Actions** nightly free-CPU matrix produces corpus shards.
4. **VM cron at 04:00** runs `merge-and-sign-corpus.sh` to aggregate shards, sign, and stage for training.
5. **`report.py`** publishes per-hive whitepapers to MEOK Labs.
6. **Manual Kimi CLI sync** copies runner logs into shared-knowledge (launchd cannot write iCloud paths).

---

## Bright lines (unchanged)

- Public data only · simulation labels only · opt-in before contact · defensive-only · no real money without legal sign-off · honest counts.


---

## 2026-07-05 — Kimi Defoneos research absorbed
- 15 safe governance/defensive/sovereign/MEOK-science files → `research/kimi-2026-07/`
- Runnable Dorado data-sovereignty scenario → `p0_aqua/benchmark/dorado_sovereign_scenario.py` (two-arm, 87% block-rate)
- EXCLUDED (offensive-AI / EW-arsenal / ransomware / bio-swarm): NOT absorbed — treated as a refuse-on-sight category per care-floor. See `research/kimi-2026-07/_ABSORPTION_NOTE.md`.
- signed_compliance_report.py → gym run emits a canonical-Ed25519 signed compliance report (verifies in CSOAI /verify). "The governed world proves its own compliance."
