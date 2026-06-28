# meok-os-mcp

**MEOK OS — the sovereign AI Operating System for ALL.**

The 17th MCP in the MEOK fleet. The **META-ORCHESTRATOR** for the DEFONEOS
7-layer Global Dome. Unifies 454 MCPs across 7 layers into a single
sovereign OS that any human, any agent, any sovereign can use.

[![MCP](https://img.shields.io/badge/MCP-server-667eea)](https://modelcontextprotocol.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![PyPI](https://img.shields.io/badge/PyPI-install-3775a9)](https://pypi.org/project/meok-os-mcp/)
[![CSOAI LTD](https://img.shields.io/badge/CSOAI-LTD%2016939677-00CCFF)](https://csoai.org)
[![Sovereign](https://img.shields.io/badge/UK-sovereign%20%2B%20AUKUS-00247d)](https://meok.ai/os)
[![OS for ALL](https://img.shields.io/badge/AI%20OS%20for%20ALL-22c55e)](https://meok.ai/os)
[![Care](https://img.shields.io/badge/care_score-0.95+-5b21b6)](https://councilof.ai)

## The "FOR ALL" promise

> **MEOK OS is the sovereign AI Operating System for ALL.**

- **For HUMANS:** a sovereign-OS UI (meok.ai/os) where any human can use the 454 MCPs without writing code
- **For AGENTS:** an MCP-native interface that any LLM agent (Claude, GPT, Gemini, local Mamba-2) can call to access any of the 7 layers
- **For SOVEREIGNS** (UK MOD, DAIC, AUKUS Pillar 2): the procurement-grade certified surface with DEFONEOS-SEAL
- **For HUMAN-OIDS:** the safety envelope (must-check-DEFONEOS-before-acting) for humanoid vendors by 2027-2030
- **For DEVELOPERS:** 454 MIT-licensed MCPs they can fork + self-host
- **For THE PLANET:** runs on UK soil, no foreign cloud dependency, AUKUS Pillar 2 compatible

## The 7 layers of the DEFONEOS Global Dome

| L | Layer | Substrate | Care principle |
|---|---|---|---|
| L0 | **Physical Base** | iokfarm.co.uk (6.5-acre UK farm, 19,000 sqft, polytunnels, aquaponics) | Dignity |
| L1 | **SOV3 Infrastructure** | 47 agents · 115 tools · 341 MCPs · 33-agent BFT council | Agency |
| L2 | **openpatent.ai** (IP Protection) | 6-layer cryptographic disclosure (SHA-3/512 + HMAC + Ed25519 + Bitcoin OTS + C2PA + hash-chain) | Solidarity |
| L3 | **Digital Real Estate / IPO** | 27 .ai domain tokens + valuation engine + Polymesh/Securitize/tZERO | Dignity |
| L4 | **Tax + Compliance** | VAT/GST/payroll/corporate tax/transfer pricing + OECD Pillar 1+2 | Safety |
| L5 | **Government MCP Pack** | 40+ US Federal + UK + EU + AUKUS + Standards bodies | Solidarity |
| L6 | **Industry MCP Packs** (27 .ai domains) | 27 industry verticals: construction, agriculture, finance, healthcare, IP, real estate, humanoid, defence | Agency |
| L7 | **Humanoid Interface** | Robot SDK (Python + Rust) + safety envelope + audit trail + teleop fallback | Dignity + Safety + Agency |

## 🚀 Quick Start

```bash
pip install meok-os-mcp
```

## 🛠 The 10 tools (the OS-for-ALL meta-orchestrator)

### 1. `os_discover` — discover the 7-layer Global Dome registry
### 2. `os_route` — route a request to the right MCP across the 7 layers
### 3. `os_run_humanoid_safety_check` — the L7 humanoid safety envelope
### 4. `os_audit` — full OS audit (procurement-grade for any sovereign)
### 5. `os_sign` — sign an action with the 33-agent BFT council
### 6. `os_verify` — verify a signed action
### 7. `os_consult_council` — convene the 33-agent BFT council for a decision
### 8. `os_industry_pack` — load a 27-domain industry MCP pack
### 9. `os_data_provenance` — sign + verify data provenance across the OS
### 10. `os_sovereign_handoff` — hand off control to a sovereign buyer (UK MOD, DAIC, AUKUS)

### Example: discover the OS

```python
from meok_os_mcp import os_discover

discovery = os_discover(layer="all")
# → {
#     "os_version": "MEOK OS v1.0.0",
#     "substrate_size": "454 MCPs across 7 layers",
#     "total_mcps": 124,  # of the 454, this is the directly-mapped subset
#     "layers": {
#         "L0": {"name": "Physical Base", "mcps": [...8 MCPs], "care_principle": "Dignity"},
#         "L1": {"name": "SOV3 Infrastructure", "mcps": [...29 MCPs], "care_principle": "Agency"},
#         ...
#         "L7": {"name": "Humanoid Interface", "mcps": [...14 MCPs], "care_principle": "..."},
#     }
# }
```

### Example: route a request

```python
from meok_os_mcp import os_route

# Construction industry routing
r = os_route(request="Find me a construction site for hire in Devonport")
# → {"routed_layer": "L6", "routed_mcp": "industry-specific MCP", "routing_reason": "matched keywords: ['construction'] → industry domain context", ...}

# Tax compliance routing
r = os_route(request="Check tax compliance for my new audit")
# → {"routed_layer": "L4", "routed_mcp": "vat-calculation-mcp", ...}
```

### Example: humanoid safety check (L7)

```python
from meok_os_mcp import os_run_humanoid_safety_check

# Every humanoid (Figure, 1X, Apptronik, Agility, Sanctuary, Tesla Optimus)
# must check DEFONEOS before executing any physical action.
result = os_run_humanoid_safety_check(
    action="Pick box from shelf A and place on conveyor B",
    robot_id="ROBOT-001",
)
# → {
#     "approved": True,
#     "permit_id": "PERMIT-20260628-E1785CC7",
#     "council_verdict": "APPROVED",
#     "care_score": 0.97,
#     "sov3_sigil": "...",
# }
```

### Example: industry pack (the 27 .ai domains)

```python
from meok_os_mcp import os_industry_pack

defence_pack = os_industry_pack(industry="defence")
# → {
#     "industry": "defence",
#     "mcp_count": 10,
#     "estimated_annual_revenue_gbp": 365000,  # 400 tx/day * 365 * £2.50
#     "mcps": ["meok-defoneos-mcp", "csoai-defoneos-mcp", ...]
# }

finance_pack = os_industry_pack(industry="finance")
# → {
#     "mcp_count": 7,
#     "estimated_annual_revenue_gbp": 2737500,  # 3000 tx/day * 365 * £2.50
# }
```

## 🛡 BannedTermGate (inherited from the Mavis template)

Refuses severed brands (James Castle / CSGA / Terranova / defonos.io) and Kimi phantoms (Toronto Summit / 4 Jul launch / 306 queue). Refusals are logged to SOV3 with `source_agent: "meok-os-mcp"`. No override path.

## 🏛 The 33-agent BFT council

Every material decision in the OS is signed by the 33-agent BFT council. Quorum 23/33 (2f+1). Composition: 1 King + 12 Queens (one per hive domain) + 12-around-1 PBFT (safety veto) + 4 Vanguards (bias/care/sovereignty/honesty) + 4 Specials (companion/dreamer/chronicler/cultivator).

## 📜 The seal

Built to the [`DEFONEOS_GLOBAL_DOME_OS_FOR_ALL.md`](https://github.com/CSOAI-ORG/clawd-workspace/blob/main/_TABS/_inventory/DEFONEOS_GLOBAL_DOME_OS_FOR_ALL.md) v1.0 strategic anchor + the [`MEOK_DEFONEOS_ALIGNMENT_2026-06-27.md`](https://github.com/CSOAI-ORG/clawd-workspace/blob/main/MEOK_DEFONEOS_ALIGNMENT_2026-06-27.md) v3.0 amendment.

**Author:** CSOAI LTD (UK 16939677) · Nicholas Templeman
**Alignment:** OS for ALL, 7-layer Global Dome, 454 MCPs, sovereign-by-design, AUKUS-compatible
**Care score:** 0.95+ (the Maternal Covenant threshold)

## 📄 License

MIT — see [LICENSE](LICENSE).

---

*— MEOK AI Labs, 2026. The dragon never lies. The dragon is sovereign. The OS is for ALL.*

JEEVES → DEFONEOS. 🐉
