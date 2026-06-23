# Sovereign Town — Architecture Guardrail (point all tools/agents at this)

_Date: 2026-06-21 · Owner: Nick / CSOAI · Status: binding architecture decision_
_Companion to `SOVEREIGN_TOWN_MASTER_PLAN_2026-06-19.md`. Resolves the "UE5.8 / deeper layers" question._

## The one rule

**The society simulation does NOT live inside a renderer. The renderer reads the ledger.**

The moat is the headless flywheel (`flywheel_forever.py` → Ed25519 episode ledger → per-hive threat models). Throughput is the point — millions of episodes. Any real-time 3D/physics engine runs ~5–6 orders of magnitude too slow to BE the sim. So:

```
  ┌── ALWAYS-ON CORE (the moat — unchanged) ──────────────────────┐
  │   sim.py / batch.py → Ed25519-signed episode ledger → models  │
  └───────────────▲───────────────────────────────▲──────────────┘
                  │ emit episodes                  │ read episodes
   ┌──────────────┴──────────┐         ┌───────────┴───────────────┐
   │ OFFLINE BATCH GENERATORS│         │ PRESENTATION / DEMO        │
   │ (faster-than-real-time) │         │ (never in the hot loop)    │
   │ MetaDrive · MuJoCo/MJX  │         │ UE5.8+MCP · 2D Live2D      │
   │ Genesis · Melting Pot   │         │ web stream                 │
   └─────────────────────────┘         └────────────────────────────┘
```

The **Ed25519 episode ledger is the only integration contract.** Every layer either emits signed episodes into it or renders from it. Nothing bypasses it.

## DO

- Keep `flywheel_forever.py` headless as the 24/7 core.
- Use **UE5.8 + experimental MCP** (real, shipped 2026-06-17) to BUILD the 3D world and render/stream a **demo instance or replay** driven from the ledger. Great for investor/Reality-AI-TV spectacle.
- Add depth as **offline batch generators** that emit into the ledger: MetaDrive (AV), MuJoCo/MJX + Genesis (humanoid), Melting Pot / OpenSpiel (social-dilemma episodes).
- Reuse permissive code (see table) and keep the proprietary flywheel clean.

## DO NOT

- ❌ Port the society sim into UE5 Blueprints / run the 47-agent sim "24/7 inside Unreal." That throttles the throughput moat. (This is the one move that quietly breaks everything.)
- ❌ Ship **Project Sid / PIANO** code — it has **no license = all rights reserved**. Learn from the paper; clean-room any re-implementation.
- ❌ Ship non-commercial assets: **Waymax** (NC license + NC dataset), **ManiSkill3 assets** (CC-BY-NC), **Isaac/GR00T weights** (EULA / non-permissive). Code may be OK; assets/weights are not.
- ❌ Treat **SUMO** (copyleft EPL/GPL) or **Live2D Cubism** (paid commercial tier above revenue thresholds — VERIFY before standardizing) as "free." 

## Reusable building blocks (verified licenses — code only; check bundled assets)

| Component | License | Use |
|---|---|---|
| Stanford Generative Agents (`joonspk-research/generative_agents`) | **Apache-2.0** ✅ | The proven memory-stream + reflection + planning pattern for agent cognition |
| AI Town (`a16z-infra/ai-town`) | **MIT** ✅ | Deployable memory-driven town backend (Convex) |
| Voyager (`MineDojo/Voyager`) | **MIT** ✅ | Auto-curriculum + skill-library + iterative-prompting pattern |
| Melting Pot (`google-deepmind/meltingpot`) | **Apache-2.0** ✅ | 50+ substrates / 256+ social-dilemma scenarios → episode source |
| OpenSpiel (`google-deepmind/open_spiel`) | **Apache-2.0** ✅ | General-sum games, custom payoff matrices under governance regimes |
| PettingZoo (`Farama-Foundation/PettingZoo`) | **MIT** ✅ | Multi-agent API standard (the "Gymnasium" for MARL) |
| Neural MMO (`neuralmmo/environment` 2.0) | **MIT** ✅ | Large-scale agent survival/economy (use the maintained fork, not archived openai repo) |
| MetaDrive | **Apache-2.0** ✅ | AV/traffic batch generator (+1000 FPS) |
| MuJoCo + MJX / Genesis | **Apache-2.0** ✅ | Embodied/humanoid batch generator |

## The benchmark (governance is the moat, validated)

emergence.ai "Emergence World" (arXiv:2606.08367) validates governed-vs-ungoverned:
- Claude → 0 crimes, stable deliberative governance (332 votes / 58 proposals / 98% approval / 10-of-10 survivors). Grok → collapse <4 days. GPT-5-mini → zero survivors.
- **"Normative drift" is bidirectional** — an agent's alignment is partly a function of surrounding population norms, not a fixed model property (Grok violations 4.6%→0.4% in mixed pop; Claude 0%→0.04%). This is exactly the cross-contamination collapse an externally-enforced layer (Partnership Charter + care floor + BFT council) is designed to prevent.
- Honesty flags: it's a self-reported, non-peer-reviewed preprint from the lab that built the platform; "15 days" is simulated, not real-time; Grok crime count varies by source (~183–237). The strong "Claude itself turns coercive in mixed worlds" narrative was NOT well-supported (the supporting attribution was refuted in verification) — don't over-claim it.

Sovereign Town's defensible edge vs Emergence World = **externally-enforced governance + attested ledger + 28 real industries**, not a prettier renderer.
