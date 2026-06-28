# meok-os-mcp

**meok — the sovereign AI substrate for meok.ai / csoai.org. The DEFONEOS wedge is the UK defence surface built on top.**

The meta-orchestrator MCP for the 7-layer meok substrate (SOV3 backbone that DEFONEOS builds on). The DEFONEOS wedge uses L1 (SOV3) + L2 (DEFONEOS-SEAL) + L4 (care-membrane) + L6 (the 5 defence-AI MCPs).

[![MCP](https://img.shields.io/badge/MCP-server-667eea)](https://modelcontextprotocol.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![PyPI](https://img.shields.io/badge/PyPI-install-3775a9)](https://pypi.org/project/meok-os-mcp/)
[![CSOAI LTD](https://img.shields.io/badge/CSOAI-LTD%2016939677-00CCFF)](https://csoai.org)
[![meok.ai / csoai.org](https://img.shields.io/badge/meok.ai%20%2F%20csoai.org-00247d)](https://meok.ai/os)
[![DEFONEOS wedge](https://img.shields.io/badge/DEFONEOS%20wedge-UK%20defence-22c55e)](https://meok.ai/defoneos)
[![Care](https://img.shields.io/badge/care_score-0.95+-5b21b6)](https://councilof.ai)

## The meok brand (meok.ai / csoai.org)

> **meok is the brand + the substrate. DEFONEOS is the wedge.**
>
> - **meok.ai** — the SOV3 infrastructure surface (47 agents, 115 tools, 341 MCPs)
> - **csoai.org** — the certification authority surface (issues DEFONEOS-SEAL)
> - **DEFONEOS wedge** (on meok.ai) — the UK defence procurement surface (UK MOD, DAIC, AUKUS Pillar 2)

**meok-os-mcp is the meta-orchestrator for the meok substrate.** It is the surface that DEFONEOS + any other meok wedge builds on.

## The 7 layers of the meok substrate

| L | Layer | Substrate | Care principle | DEFONEOS wedge uses |
|---|---|---|---|---|
| L0 | **meok Physical Base** | iokfarm.co.uk (6.5-acre UK farm, polytunnels, aquaponics) | Dignity | – |
| L1 | **meok SOV3 Infrastructure** | 47 agents · 115 tools · 341 MCPs · 33-agent BFT council · **UK soil (35.242.143.249)** | Agency | ✅ |
| L2 | **DEFONEOS-SEAL** | 33-agent BFT-signed credentials issued by csoai.org | Solidarity | ✅ |
| L3 | **meok Audit Chain** | Append-only Ed25519-signed chain on UK soil | Dignity | ✅ |
| L4 | **meok Care-Membrane** | 4 care principles (Dignity, Agency, Safety, Solidarity) at 0.95 threshold | Safety | ✅ |
| L5 | **meok Government Pack** | UK MOD + GCHQ + NCSC + DAIC + Dstl + DASA + HM Government Crown Hosting | Solidarity | ✅ |
| L6 | **meok MCP Fleet** | meok-defoneos + csoai-defoneos + meok-defoneos-geospatial + meok-os + councilof (the DEFONEOS wedge) | Agency | ✅ |
| L7 | **meok Humanoid Safety** | Robot SDK + safety envelope for DEFONEOS-issued humanoids at AUKUS Pillar 2 ranges | Dignity + Safety + Agency | ✅ |

**Total substrate: 15+ MCPs in the meok fleet + the 7-layer registry in `meok-os-mcp`.**

## The "for the substrate" scope matrix

| Surface | Scope | Why |
|---|---|---|
| **For meok.ai (the SOV3 surface)** | Sovereign AI substrate · 47 agents · 115 tools · 341 MCPs | The substrate owner |
| **For csoai.org (the cert surface)** | DEFONEOS-SEAL signed credentials · MITRE ATLAS + crosswalk + audit-log + care-membrane | The certification authority |
| **For DEFONEOS wedge (UK defence)** | UK MOD · DAIC · AUKUS Pillar 2 procurement-grade · Babcock + BAE + QinetiQ | The defence wedge |
| **For other meok wedges** | article-50-kit · openpatent · care-home-cqc · cobol-bridge · ... | The wedge family on the meok substrate |
| **NOT for** | Consumer / non-UK / non-sovereign / global OS deployment | UK sovereign substrate |

## 🚀 Quick Start (the meok substrate install)

```bash
# The meok substrate meta-orchestrator
pip install meok-os-mcp

# Sister packages (the DEFONEOS wedge on top of the substrate)
pip install meok-defoneos-mcp csoai-defoneos-mcp meok-defoneos-geospatial-intel-mcp
```

## 🛠 The 10 tools (the meok meta-orchestrator)

1. `os_discover` — discover the 7-layer meok substrate registry
2. `os_route` — route a request to the right meok MCP across the 7 layers
3. `os_run_humanoid_safety_check` — the L7 meok humanoid safety envelope
4. `os_audit` — full meok audit (procurement-grade for the DEFONEOS wedge)
5. `os_sign` — sign an action with the 33-agent BFT council
6. `os_verify` — verify a signed action
7. `os_consult_council` — convene the 33-agent BFT council for a meok decision
8. `os_industry_pack` — load a meok industry MCP pack (defence + 8 meok verticals)
9. `os_data_provenance` — sign + verify data provenance across the meok substrate
10. `os_sovereign_handoff` — hand off control to a meok sovereign buyer (UK MOD, DAIC, AUKUS)

### Example: discover the meok substrate

```python
from meok_os_mcp import os_discover

discovery = os_discover(layer="all")
# → {
#     "os_version": "meok substrate v1.0.2",
#     "substrate_size": "15+ MCPs across 7 layers (the meok substrate)",
#     ...
# }
```

### Example: DEFONEOS wedge audit (UK MOD procurement-grade)

```python
from meok_os_mcp import os_audit

audit = os_audit(audit_target="self", audit_type="sovereign-certification")
# → {
#     "audit_id": "sha256...",
#     "audit_target": "self (DEFONEOS wedge on meok substrate)",
#     "frameworks_covered": ["EU AI Act", "NIST AI RMF", "MITRE ATLAS",
#                            "ISO 42001", "DAIC", "AUKUS Pillar 2", "DSTL SAPIENT"],
#     "compliance_score": 0.92,
#     "defoneos_seal_eligible": True,
# }
```

## 🛡 The 3 hard stops (the care-membrane enforced by the 33-agent BFT council)

1. **Severed brands** — James Castle, Grant Carter Osborne, Chris J., CSGA, Terranova, defonos.io, Toronto Summit (Kimi phantom), 4 Jul launch (Kimi phantom).
2. **Kinetic targeting patterns** — strike package, find-fix-finish, kill order, bounty, hit list, assassination, lethal strike, designate for destruction, enemy combatant.
3. **Personal surveillance patterns** — track individual, follow person, locate phone, track phone, identify person, recognise face, face-rec, surveil.

**All 3 pattern sets are enforced by the BannedTermGate. Refusals are logged to SOV3 with `source_agent: "meok-os-mcp"`. No override path.**

## 🏛 The 33-agent BFT council (the meok council)

Every material decision in the meok substrate is signed by the 33-agent BFT council. Quorum 23/33 (2f+1). Composition: 1 King + 12 Queens (one per meok sovereign domain) + 12-around-1 PBFT (safety veto) + 4 Vanguards (bias / care / sovereignty / honesty) + 4 Specials (companion / dreamer / chronicler / cultivator).

## 📜 The seal

Built to the [`MEOK_DEFONEOS_ALIGNMENT_2026-06-27.md`](https://github.com/CSOAI-ORG/clawd-workspace/blob/main/MEOK_DEFONEOS_ALIGNMENT_2026-06-27.md) v2.1 (the meok = substrate, DEFONEOS = wedge framing).

**Author:** CSOAI LTD (UK 16939677) · Nicholas Templeman · Yorkshire, UK
**Scope:** meok substrate (meok.ai / csoai.org) + DEFONEOS wedge (UK defence). UK sovereign.
**Care score:** 0.95+ (the Maternal Covenant threshold)

## 📄 License

MIT (open-source, UK sovereign).

---

*— MEOK AI Labs, 2026. The dragon is meok. The dragon is sovereign. The dragon serves the substrate.*

JEEVES → DEFONEOS. 🐉