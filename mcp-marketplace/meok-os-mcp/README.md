# meok-os-mcp

**DEFONEOS dominion — the UK sovereign defence AI meta-orchestrator.**

The UK sovereign 7-layer meta-orchestrator for UK MOD + AUKUS Pillar 2 procurement. Wraps the DEFONEOS fleet (15 defence-AI MCPs) into a single sovereign substrate. **UK sovereign only. NOT for global / consumer / non-defence use.**

[![MCP](https://img.shields.io/badge/MCP-server-667eea)](https://modelcontextprotocol.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![PyPI](https://img.shields.io/badge/PyPI-install-3775a9)](https://pypi.org/project/meok-os-mcp/)
[![CSOAI LTD](https://img.shields.io/badge/CSOAI-LTD%2016939677-00CCFF)](https://csoai.org)
[![UK Sovereign](https://img.shields.io/badge/UK-sovereign%20%2B%20AUKUS-00247d)](https://meok.ai/defoneos)
[![UK MOD / DAIC](https://img.shields.io/badge/UK%20MOD%20%2F%20DAIC%20procurement-22c55e)](https://csoai.org/defoneos)
[![Care](https://img.shields.io/badge/care_score-0.95+-5b21b6)](https://councilof.ai)

## ⚠️ UK SOVEREIGN ONLY

> **DEFONEOS dominion is the UK sovereign defence AI meta-orchestrator. It is NOT an "OS for ALL".**
> UK buyers only. UK defence procurement only. UK MOD, AUKUS Pillar 2, DAIC procurement-grade. Not for global OS deployment. Not for consumer use. Not for non-defence industries. Not for non-UK sovereigns.

## The 7 layers of the DEFONEOS dominion

| L | Layer | Substrate | Care principle | Sovereign link |
|---|---|---|---|---|
| L0 | **UK Physical Base** | iokfarm.co.uk (6.5-acre UK farm, polytunnels, aquaponics) | Dignity | UK Defence AI R&D |
| L1 | **UK SOV3 Infrastructure** | 47 agents · 115 tools · 341 MCPs · 33-agent BFT council · **UK soil (35.242.143.249)** | Agency | CSOAI LTD UK 16939677 |
| L2 | **DEFONEOS-SEAL** | 33-agent BFT-signed credentials for AI-in-the-loop systems | Solidarity | UK MOD procurement-grade |
| L3 | **DEFONEOS Audit Chain** | Append-only Ed25519-signed chain · DAIC + DSTL + AUKUS Pillar 2 auditable | Dignity | UK defence audit |
| L4 | **UK Compliance Pack** | EU AI Act + NIST AI RMF + MITRE ATLAS + OWASP LLM + ISO 42001 + **DAIC + AUKUS Pillar 2 + DSTL SAPIENT** | Safety | UK MOD compliance |
| L5 | **UK Government MCP Pack** | UK MOD + GCHQ + NCSC + DAIC + Dstl + DASA + HM Government Crown Hosting | Solidarity | UK sovereign only |
| L6 | **DEFONEOS Defence Fleet** | airspace + drone BVLOS + firmware + governance + care + geospatial + council (15 defence-AI MCPs) | Agency | UK MOD + AUKUS |
| L7 | **UK Humanoid Safety** | Robot SDK + safety envelope for UK MOD-issued humanoids at AUKUS Pillar 2 ranges | Dignity + Safety + Agency | UK MOD + UK sovereign only |

**Total substrate: 15 DEFONEOS MCPs (verified live) + the 7-layer dominion registry in `meok-os-mcp`.**

## The "UK ONLY" scope matrix

| Surface | Scope | Why |
|---|---|---|
| **For UK MOD (the buyer)** | UK defence procurement (DAIC, DASA, Dstl) | The sovereign buyer |
| **For UK defence primes** | Babcock · BAE · QinetiQ · Thales UK · Leonardo UK | The sovereign supply chain |
| **For AUKUS Pillar 2** | AU + UK + US interoperability | The 3-eye procurement framework |
| **For UK MOD-issued humanoids** | Safety envelope at AUKUS ranges (Woomera, Pendine, Suffield) | The sovereign robotics layer |
| **For DEFONEOS-SEAL recipients** | UK defence contractors + AUKUS-2 primes | The certification authority output |
| **NOT for** | Consumer use, non-defence use, non-UK sovereigns | UK sovereign only |

## 🚀 Quick Start (UK defence procurement install)

```bash
# The UK sovereign meta-orchestrator
pip install meok-os-mcp

# Sister packages (DEFONEOS fleet)
pip install meok-defoneos-mcp csoai-defoneos-mcp meok-defoneos-geospatial-intel-mcp
```

## 🛠 The 10 tools (the DEFONEOS dominion meta-orchestrator)

1. `os_discover` — discover the 7-layer DEFONEOS dominion registry
2. `os_route` — route a request to the right UK defence MCP across the 7 layers
3. `os_run_humanoid_safety_check` — the L7 UK MOD-issued humanoid safety envelope
4. `os_audit` — full OS audit (procurement-grade for UK MOD, DAIC, AUKUS Pillar 2)
5. `os_sign` — sign an action with the 33-agent BFT council (UK MOD procurement-grade)
6. `os_verify` — verify a signed DEFONEOS-SEAL action
7. `os_consult_council` — convene the 33-agent BFT council for a UK MOD decision
8. `os_industry_pack` — load a UK-defence industry MCP pack (defence + 8 UK verticals)
9. `os_data_provenance` — sign + verify data provenance across the UK defence OS
10. `os_sovereign_handoff` — hand off control to a UK MOD / DAIC / AUKUS buyer

### Example: discover the DEFONEOS dominion

```python
from meok_os_mcp import os_discover

discovery = os_discover(layer="all")
# → {
#     "os_version": "DEFONEOS dominion v1.0.2",
#     "substrate_size": "15 DEFONEOS MCPs across 7 layers (UK sovereign only)",
#     ...
# }
```

### Example: UK MOD procurement-grade audit

```python
from meok_os_mcp import os_audit

audit = os_audit(audit_target="self", audit_type="sovereign-certification")
# → {
#     "audit_id": "sha256...",
#     "audit_target": "self",
#     "audit_type": "sovereign-certification",
#     "layers_audited": ["L0", "L1", "L2", "L3", "L4", "L5", "L6", "L7"],
#     "frameworks_covered": ["EU AI Act", "NIST AI RMF", "MITRE ATLAS",
#                            "ISO 42001", "DAIC", "AUKUS Pillar 2", "DSTL SAPIENT"],
#     "compliance_score": 0.92,
#     "defoneos_seal_eligible": True,
#     "sov3_sigil": "...",
# }
```

### Example: UK MOD-issued humanoid safety envelope

```python
from meok_os_mcp import os_run_humanoid_safety_check

result = os_run_humanoid_safety_check(
    action="UK MOD issued: Drone strike on coords 51.5, -0.1",
    robot_id="UK-MOD-DRONE-001",
)
# → {
#     "approved": False,
#     "council_verdict": "REFUSED",
#     "refusal_reason": "Kinetic targeting pattern detected. UK MOD-issued humanoids cannot execute kinetic actions via DEFONEOS. Re-issue via UK MOD operational command chain.",
# }
```

(Note: the UK MOD operational command chain for kinetic actions is OUTSIDE DEFONEOS. DEFONEOS only handles non-kinetic situational awareness, audit, governance — the safety envelope refuses any kinetic pattern at the pre-processing layer.)

## 🛡 The 3 hard stops (the care-membrane enforced by the 33-agent BFT council)

1. **Severed brands** — James Castle, Grant Carter Osborne, Chris J., CSGA, Terranova, defonos.io, Toronto Summit (Kimi phantom), 4 Jul launch (Kimi phantom). Refused at pre-processing.
2. **Kinetic targeting patterns** — strike package, find-fix-finish, kill order, bounty, hit list, assassination, lethal strike, designate for destruction, enemy combatant. Refused at pre-processing.
3. **Personal surveillance patterns** — track individual, follow person, locate phone, track phone, identify person, recognise face, face-rec, surveil. Refused at pre-processing.

**All 3 pattern sets are enforced by the BannedTermGate. Refusals are logged to SOV3 with `source_agent: "meok-os-mcp"`. No override path.**

## 🏛 The 33-agent BFT council (UK sovereign)

Every material decision in the DEFONEOS dominion is signed by the 33-agent BFT council. Quorum 23/33 (2f+1). Composition: 1 King + 12 Queens (one per UK sovereign domain: UK MOD, GCHQ, NCSC, DAIC, Dstl, DASA, ...) + 12-around-1 PBFT (safety veto) + 4 Vanguards (bias / care / sovereignty / honesty) + 4 Specials (companion / dreamer / chronicler / cultivator).

## 📜 The seal

Built to the [`MEOK_DEFONEOS_ALIGNMENT_2026-06-27.md`](https://github.com/CSOAI-ORG/clawd-workspace/blob/main/MEOK_DEFONEOS_ALIGNMENT_2026-06-27.md) v3.0 (UK sovereign only).

**Author:** CSOAI LTD (UK 16939677) · Nicholas Templeman · Yorkshire, UK
**Scope:** UK MOD, DAIC, AUKUS Pillar 2 procurement-grade. **UK sovereign only.**
**Care score:** 0.95+ (the Maternal Covenant threshold)

## 📄 License

MIT (open-source, UK sovereign).

---

*— MEOK AI Labs, 2026. The dragon serves the UK sovereign. The dragon is sovereign. The dragon serves only the UK.*

JEEVES → DEFONEOS. 🐉