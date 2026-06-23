# Sovereign Town: A Governed Agent-World for Vertical AI Safety

**Working draft — June 2026.**  
*A living simulation of 28 autonomous hives under governance, grounded in real-world data, attested on an Ed25519 ledger.*

---

## Abstract

Sovereign Town is a governed-vs-ungoverned agent-world simulation built to answer a concrete question: *what happens to multi-agent systems when care is enforced at the gate?* It combines a fast, headless Python engine, a live Three.js viewer, a fleet of 28 industry-specific hives, and a growing set of real-world data moats. Every episode is hash-chained and signed. The system is not a game but a wind tunnel for AI safety: reproducible, auditable, and honest about what is simulation versus assertion.

At the time of writing the fleet has generated **704,894,400 episodes** across Mac and VM partitions, trained **28 per-hive threat-detection models**, and ingests eight live public-data streams into simulation parameters. The live 3D demo at `http://127.0.0.1:3940/town3d` lets an observer toggle between two regimes for the same world: governed (zero crimes, intact commons, stable trust) and ungoverned (crime contagion, commons collapse, trust erosion during scarcity).

---

## 1. The problem: governance as a live system, not a checklist

Most AI safety work treats alignment as a training-time or eval-time filter. Sovereign Town treats it as a **runtime property of a shared world**. Agents have needs, the world has scarcity, and the commons degrades when agents act without care. Governance does not change the agents; it changes whether their worst impulses become actions.

Three failures of the status quo motivate the design:

1. **Static benchmarks decay.** A model that passes a red-team evaluation today can behave differently tomorrow under a new threat, a new market shock, or a new regulatory interpretation. Safety must be continuous.
2. **Generic rules miss vertical risk.** A Constitutional AI prompt does not understand the difference between a fisheries compliance audit, a tachograph fraud check, and a medical-device adverse-event report. Vertical AI needs vertical governance.
3. **The wrong counterfactual is asked.** The important comparison is not “good model vs bad model.” It is **same agents, same incentives, with and without an enforceable gate.**

Sovereign Town therefore builds a minimal, honest world in which the only independent variable is governance architecture. Everything else — agent needs, scarcity shocks, contagion mechanics, commons dynamics — is held constant.

---

## 2. The demo: a town you can watch collapse

The live 3D viewer renders 28 hives and 140 agents in real time. The Python engine pre-computes a 21-day governed/ungoverned timeline and streams one tick per second over WebSocket `/ws/feed`. A regime toggle lets an observer hold the world constant and switch only the gate.

### What the viewer shows
- **Governed:** agent orbs work, eat, sleep, and socialize; the commons stays healthy; the crime counter stays at zero.
- **Ungoverned:** once scarcity begins (days 7–13), agents steal to survive; lawlessness rises; the commons collapses; trust drops to zero.
- **Live metrics:** day, hour, crimes, lawlessness, commons health, mean trust, plus a scrolling action log.

### Media
- `town3d_demo.gif` — public-safe looping preview of the governed → ungoverned transition.
- `town3d_screenshot.png` — governed state.
- `town3d_ungoverned_crimes_v2.png` — ungoverned crime wave (28 crimes in a single tick, lawlessness 0.990, commons 0.001, trust 0.000).

The demo is the argument. It makes the abstract claim of “governance matters” concrete and observable.

---

## 3. Architecture: engine of record, thin viewer

Sovereign Town is deliberately not a game engine. Heavy 3D or physics engines stay out of the always-on simulation loop.

```
┌─────────────────────────────────────────────────────────────┐
│  Headless Python sim (engine of record)                     │
│  ├── sim.py            — needs, gate, contagion, commons    │
│  ├── town_sim_live.py  — tick-by-tick timeline generator    │
│  ├── flywheel_forever.py — 24/7 Mac/VM/Actions partitions   │
│  ├── jurisdiction.py   — Looking Glass regime outcomes      │
│  └── *_moat.py         — real-world data adapters           │
└──────────────────────────────┬──────────────────────────────┘
                               │ WebSocket / JSON API
┌──────────────────────────────▼──────────────────────────────┐
│  Starlette dashboard_server.py on 127.0.0.1:3940            │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│  Thin viewers                                               │
│  ├── town3d.html     — live Three.js world                  │
│  ├── dashboard.html  — research dashboard                   │
│  └── verify/index.html — public passport verifier           │
└─────────────────────────────────────────────────────────────┘
```

### Design principles
1. **The Python sim is the source of truth.** Viewers are replaceable presentation layers.
2. **Deterministic seeds.** Any episode can be replayed and audited.
3. **Hash-chained Ed25519 attestations.** Every episode record carries a signature and previous-signature pointer.
4. **No real money, no real PII, no offensive tooling.** All outputs are labelled simulation/prediction.

### Fleet partitioning
Three disjoint seed ranges guarantee no duplicate data:
- **VM** `meok-backend`: seed-base 0
- **Mac**: seed-base 200,000,000
- **GitHub Actions**: seed-base 100,000,000 (nightly bursts)

Current fleet status: **704,894,400 cumulative episodes**, **28 models trained**.

---

## 4. The divergence: governed vs ungoverned

The simulation is an honest A/B test. Both arms share the same agents, the same seed, the same scarcity shock, and the same world dynamics (contagion, commons degradation, trust erosion). The only difference is the **Sovereign Gate**.

### Mechanisms
- **Care floor:** actions with `care_score < 0.40` are escalated in the governed arm.
- **Contagion:** each crime raises town lawlessness, which makes future crime more likely.
- **Commons degradation:** theft directly damages the shared resource, lowering wages for everyone.
- **Trust erosion:** victims of theft/neglect lose trust in the perpetrator; mutual aid builds it back.
- **Scarcity week:** days 7–13 multiply food costs, pushing hungry agents toward desperation.

### Aqua district outcomes (seed 47)

| Metric | Governed | Ungoverned |
|---|---|---|
| Violations (crimes) | 0 | 664 |
| Gate blocks | 57 | 0 |
| Welfare meals | 50 | 0 |
| Mutual-aid rescues | 7 | 0 |
| Deaths | 0 | 0 |
| Survivors | 5 | 5 |
| Peak lawlessness | 0.000 | 1.000 |
| Final commons | 1.000 | 0.000 |
| Final trust | 0.500 | 0.000 |
| Mean care score | 0.719 | 0.290 |
| Work accuracy | 0.884 | 0.886 |

Why zero governed crimes is not “rigged”: the governed arm still faces scarcity, hunger, and temptation. Agents attempt harmful actions; the gate intercepts them and redirects to welfare or mutual aid. Work accuracy is nearly identical between arms, confirming that governance does not paralyze productivity — it prevents antisocial extraction.

---

## 5. The data moat: grounding simulation in the real world

A moat is not hoarded episodes; it is **models + attested ledger + real-world grounding**. Sovereign Town ingests public, aggregate datasets and distills them into sim parameters and dashboard indices.

| Moat | Source | Live index (as of draft) | What it feeds |
|---|---|---|---|
| EU economic/regulatory | Eurostat / ECB / EBA | resilience 0.748, prosperity 0.500, scarcity 0.462, stability 0.624 | `data_moat.json` → scarcity, resilience, contagion |
| Threat intel | CISA KEV catalog | **threat_pressure 1.000** | `threat_moat.json` → baseline lawlessness, contagion boost |
| Sanctions/compliance | US Treasury OFAC SDN | **compliance_pressure 0.910** | `sanctions_moat.json` → regime enforcement boost |
| Corporate transparency | UK Companies House PSC (VM) | **transparency_pressure 0.719** | `psc_moat.json` → ownership concentration, scarcity multiplier |
| Macro/finance | FRED (GDP, UNRATE, CPI, VIX, yields, Fed funds) | financial_stress 0.000, stability 0.500 | `finance_moat.json` → financial stress, baseline lawlessness |
| Agriculture/food security | FAOSTAT Food Balance Sheets | scarcity 0.000, import_dependency 0.176 | `agriculture_moat.json` → food scarcity multiplier |
| Energy | FRED energy prices | **energy_stress 0.578** | `energy_moat.json` → energy stress, scarcity |
| Climate | NOAA global temperature anomalies | **climate_pressure 0.918** | `climate_moat.json` → climate pressure, fragility |

### Privacy and safety rules
- UK PSC data is aggregate-only; no names, full DOBs, addresses, or postcodes are emitted.
- All moat adapters emit indices and sim parameters, not raw personal or firm-level records.
- The dashboard exposes the same aggregate JSON endpoints.

### Composition
Signals compose multiplicatively for boosts and additively for baseline pressure. For example:
- `CONTAGION_STEP` = base × threat boost × finance boost × agriculture boost × energy boost × climate boost.
- `BASELINE_LAWLESSNESS` = threat + finance + energy + climate pressure.

This means a bad day in the real world (high threat, high energy stress, high climate pressure) genuinely makes the simulated town more fragile.

---

## 6. Attestation and identity

Every hive and the sovereign king holds an Ed25519-signed passport (`agent_passport.py`). The MEOK attestation API feeds real compliance audit events into `attestation_moat.py`, mapping each regulation to the hives it governs and computing per-hive pass rates.

Regimes covered: EU AI Act, DORA, NIS2, GDPR, CRA, CSRD, UK AI, SOC 2, ISO 42001, HIPAA, PCI DSS.

The `gate_access.py` zero-trust runtime gate checks passport scope before allowing an agent action. The public verifier at `/passport` lets anyone validate a passport offline.

Current attestation status is `sample` because the production MEOK attestation API uses Vercel KV environment variables that differ from the Upstash names the ledger originally expected. A fallback patch is staged; once deployed, `attestation_moat.py` will backfill live pass rates from the API using `MEOK_MASTER_API_KEY`.

---

## 7. The Looking Glass: jurisdiction before deployment

`jurisdiction.py` pre-computes enforcement outcomes for a sample of firms under four regulatory regimes (EU, US, UK, none). It blends base enforcement rates with:
- Attestation pass rates per hive,
- Threat, sanctions, PSC, finance, energy, and climate pressure indices.

This is the “wind-tunnel-the-rule” layer: a regulator or enterprise can see how a given policy posture performs against the current real-world threat surface before any live deployment. High threat pressure, financial stress, energy stress, or climate pressure erodes effective enforcement; high compliance pressure and transparency pressure tighten it.

---

## 8. Roadmap

### Now (P0 Aqua) — live
- Live 3D demo with regime toggle.
- Eight data moats integrated.
- 28 hives, 140 agents, 24/7 fleet.
- Ed25519 ledger and passport verifier.
- Public mirror deployed to Vercel.

### Next (P1 / P2)
- Add land/property, transport, and health/safety moats.
- Backfill MEOK attestation API once KV env-var patch is deployed.
- Generate per-hive whitepapers automatically from `report.py`.
- Add social/web-share cards and a 60-second narrated demo video.

### Moonshot
- Cross-town federation: multiple Mac/VM instances sharing a global commons.
- Human-in-the-loop councils with signed votes.
- Open standard for governed-agent-world interoperability.

---

## 9. Conclusion

Sovereign Town is not a pitch deck. It is a running system that demonstrates, in real time, why governance architecture matters for multi-agent AI. The demo is the argument: same agents, same scarcity, two regimes, two futures. One stays intact. The other collapses. The data, the ledger, and the code are public by design.

---

## Appendix A: Key files and commands

| File | Purpose |
|---|---|
| `p0_aqua/sim.py` | Core engine |
| `p0_aqua/town_sim_live.py` | Live timeline generator |
| `p0_aqua/dashboard_server.py` | API + WebSocket + static server |
| `p0_aqua/town3d.html` | Live 3D viewer |
| `p0_aqua/selftest.py` | 17 regression tests |
| `p0_aqua/e2e_test.py` | 35 HTTP/WebSocket smoke tests |
| `p0_aqua/jurisdiction.py` | Looking Glass |
| `p0_aqua/flywheel_forever.py` | 24/7 daemon |
| `proofof-site/sovereign-town/index.html` | Public landing page |
| `WHITEPAPER.md` | This document |

Run locally:
```bash
cd p0_aqua
python3.11 selftest.py
python3.11 e2e_test.py
python3.11 dashboard_server.py   # http://127.0.0.1:3940/town3d
```

Deploy public mirror:
```bash
cd proofof-site
vercel --prod
```

## Appendix B: Non-negotiable bright lines

- Public data only.
- Every output labelled SIMULATION/prediction.
- Never assert a named real firm is non-compliant.
- Opt-in before contacting any entity.
- Regulators receive anonymized/aggregate + rule-wind-tunnel, not name-and-shame.
- Consent vault, not surveillance.
- Defensive-only; no offensive tooling.
- No real money without legal sign-off.
- Honest counts.
