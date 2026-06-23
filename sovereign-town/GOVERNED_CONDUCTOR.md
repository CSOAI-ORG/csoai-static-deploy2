# Governed Conductor — the attested answer to Sakana Fugu

*Design note, 2026-06-23. Honest scope: this is an orchestration **layer** built on assets we already have, not a trained foundation model. Where it beats Fugu is governance/heterogeneity/no-lock-in — NOT raw reasoning-benchmark quality (Fugu spent RL compute we don't have).*

## What Fugu is (the thing we're answering)
A **learned orchestrator** sold as "multi-agent system as a model," built on two ICLR-2026 papers:
- **TRINITY** — evolved lightweight coordinator assigning **Thinker / Worker / Verifier** roles across a model pool.
- **Conductor** — RL-trained natural-language coordination (no hardcoded routing).
- Recursive self-calling for test-time scaling.
Moat = the *trained routing weights*, deliberately hidden. Proprietary hosted API ($5/$30 per-M-tokens), LLM-only, no governance, vendor lock-in.

## Why we're already ~70% there
Fugu's TRINITY roles map onto what Sovereign Town already runs:
- **Thinker / Worker** ← the 12-around-1 council agents.
- **Verifier** ← the **Sovereign Gate** (deterministic) + council quorum. This is *better than* Fugu's verifier: ours is a hard gate, not a soft check.
What we DON'T have: a *learned* router. Ours is rule-based today. That's fine — we earn the learned one later (see §4).

## The three axes where we beat Fugu (and the one where we don't)
| Axis | Fugu | Governed Conductor |
|---|---|---|
| Routing transparency | black box *by design* | **every Thinker→Worker→Verifier handoff signed into the ledger** → auditable (EU AI Act Art-12) |
| Model pool | LLMs only | **heterogeneous**: LLMs + world-model sim + risk models |
| Vendor | one proprietary API | **swappable / sovereign** (FreeLLMAPI + local) |
| Raw reasoning quality | RL-trained, strong | ❌ we do **not** claim parity — be honest |

## 1. Roles over the existing council
Wrap the council in an explicit `Conductor` that assigns per-task roles (Thinker/Worker/Verifier). Verifier is non-negotiable = the Sovereign Gate. Keep the pool swappable.

## 2. Heterogeneous pool (the real differentiator — Fugu can't follow here)
The Conductor can route to:
- **LLMs** (language/reasoning) via an OpenAI-compatible pool. **Production pool must be license-clean / self-hosted** (e.g. local VibeThinker-3B-class reasoners, or paid APIs under proper terms). **FreeLLMAPI is dev/experimentation ONLY** — its own description says "personal use," and stacking provider free tiers likely violates several providers' ToS. Do NOT put FreeLLMAPI in the sovereign/production path (it would undercut the very no-lock-in/clean-provenance claim).
- **World model** = the Sovereign Town sim itself, called as a "what-if" planner ("simulate this policy for N ticks, return outcome").
- **Risk models** = the per-hive threat models, called as scorers.
2026 research consensus: LLMs for language/orchestration, world models for simulation/planning/control, **hybrid is where useful agents live.** Fugu is LLM-only; we already own a world model and risk models.

## 3. Attested routing (the moat — now real, not vaporware)
Every routing decision + outcome is written as a **signed episode** into the flywheel ledger — the SAME ledger that is now **Bitcoin-anchored and browser-verifiable** (proofof.ai/sovereign-town: `ledger_head.json` + `anchor.json`, issuer key `53kc24fq…`, scheme = `prev + json.dumps(sort_keys=True)` spaced). So "auditable orchestration" is a property we can *demonstrate*, not just claim. This is the EU-AI-Act/DORA wedge.

## 3a. Lead with this: their router is a black box *by their own admission*
Sakana's **own published risk table** says: *"proprietary routing — cannot see which models are called."* Fugu's orchestration is opaque by design (the routing patterns are their hidden IP). Our entire moat is the **inverse**: every routing decision is a signed, anchored, offline-verifiable ledger entry. So the one-line positioning is **"auditable router vs. their black box,"** NOT "sovereign / export-control-free" — that latter pitch is *Sakana's own* and rides the Anthropic-ban news cycle (Fable 5 + Mythos were export-controlled June 12 2026; verified). Our durable wedge is signed-ledger + risk-model-in-the-loop, which holds regardless of export politics.
Two more openings, both confirmed from Fugu's current limits:
- **Govern *any* agent, not just LLM calls.** Fugu routes only frontier LLMs; it can't orchestrate arbitrary agent frameworks. We govern any callable (LLM, sim, tool, robot policy). Treat as a current-state gap, not a permanent moat.
- **Verifier = governance gate.** TRINITY uses the Verifier role for *correctness only*; we bind it to the risk-model + Sovereign Gate + signed attestation, turning a quality check into a control point.

## 4. Path to a *learned* router (our honest version of Conductor)
Don't pay for a frontier RL run. Instead: log Thinker/Worker/Verifier traces as signed episodes (we already do), then **distill a small learned router from the logged traces.** The flywheel is the training loop; the Bitcoin-anchored ledger is what makes that training data trustworthy. This rides the existing moat thesis instead of replacing it — and it's a story no one else can tell, because no one else has an externally-anchored attested corpus.

## 5. Edge runtime (the clean seam, from the Mastra eval)
- **Python keeps the core**: council, Sovereign Gate, Ed25519 ledger, sim. The moat never leaves Python.
- **Mastra (TS, Apache-2.0)** optionally hosts the outward web/UI + MCP-exposure agent layer, models pointed at FreeLLMAPI. Telemetry OFF (`MASTRA_TELEMETRY_DISABLED=1`, firewall us.posthog.com).
- Mastra/edge calls *into* the Python governance core via MCP/tool boundary; the core calls out to nothing TS. Single vendor avoided, offline-verifiability preserved.

## Build order
1. `Conductor` wrapper assigning TRINITY roles over the existing council (pool stays swappable). Rule-based routing.
2. Add world-model + risk-model as routable pool members (sim-as-planner, threat-models-as-scorers).
3. Sign every routing decision into the ledger (reuse the existing signer; it's already anchored).
4. Expose via MCP so the Mastra/edge layer (and external agents) can drive it.
5. *Later*: distill the learned router from logged signed traces.

## Anti-hype guardrails
- Never claim "better than Fugu at coding/math/reasoning." We compete on **governance, heterogeneity, no-lock-in**, not trained quality.
- "Our One model" is realistically an orchestration **layer** first, a learned router second.
- Sakana Fugu is a *benchmark comparison*, never a dependency (proprietary, paid, lock-in — antithetical to the thesis).
