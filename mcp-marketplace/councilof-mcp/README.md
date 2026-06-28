# councilof-mcp

**councilof.ai — the 33-agent BFT council for the meok substrate + DEFONEOS wedge.**

For AI governance, BFT decision-making, and any high-stakes decision that requires a sovereign, care-ethics-certified verdict. Part of the meok substrate (meok.ai / csoai.org) + the DEFONEOS wedge (UK defence).

[![MCP](https://img.shields.io/badge/MCP-server-667eea)](https://modelcontextprotocol.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![CSOAI LTD](https://img.shields.io/badge/CSOAI-LTD%2016939677-00CCFF)](https://csoai.org)
[![meok.ai / csoai.org](https://img.shields.io/badge/meok.ai%20%2F%20csoai.org-00247d)](https://meok.ai/os)
[![DEFONEOS wedge](https://img.shields.io/badge/DEFONEOS%20wedge-UK%20defence-22c55e)](https://meok.ai/defoneos)
[![Care](https://img.shields.io/badge/care_score-0.95+-5b21b6)](https://councilof.ai)

## The council for the meok substrate

> **councilof-mcp is the 33-agent BFT council orchestrator for the meok substrate (meok.ai / csoai.org) + the DEFONEOS wedge (UK defence procurement).**
>
> - **meok.ai** uses the council to issue every meok decision
> - **csoai.org** uses the council to issue every DEFONEOS-SEAL credential
> - **DEFONEOS wedge** uses the council for procurement-grade decisions

## The 33-agent council composition

| Group | Count | Weight | Veto |
|---|---:|---:|:---:|
| King (consensus orchestrator) | 1 | 3.0 | – |
| Queens (one per meok sovereign domain) | 12 | 1.0 | – |
| PBFT nodes (safety veto layer) | 12 | 1.0 | – |
| Vanguards (bias / care / sovereignty / honesty) | 4 | 2.0 | ✅ (can VETO) |
| Specials (companion / dreamer / chronicler / cultivator) | 4 | 1.5 | – |
| **TOTAL** | **33** | – | 4 vanguards |

**Quorum: 23/33 (2f+1).**

The 12 Queens cover meok sovereign domains: meok.ai, csoai.org, DEFONEOS, openpatent, article-50-kit, and other meok wedges.

## The 4 care principles (the Maternal Covenant)

The BFT council enforces 4 care principles at the 0.95 threshold:
- **Dignity** — the AI respects the human, the data, the physical world it operates in
- **Agency** — sovereign AI, not platform AI; the meok owner remains in control
- **Safety** — the law is enforced, not bypassed; no kinetic targeting, no personal surveillance
- **Solidarity** — the IP is verifiable, the credit is attributable

## The 6 tools

1. `convene_council` — submit a question to the 33-agent BFT council
2. `get_verdict` — retrieve the verdict (APPROVED / REFUSED / PENDING + tallies + vetoes)
3. `list_council_members` — list the 33 agents
4. `cast_vote` — cast a single agent vote (Vanguards can VETO)
5. `simulate_council` — simulate a council vote (4 scenarios: unanimous, balanced, vanguard-veto, rejection)
6. `evaluate_care_principle` — evaluate the 4 care principles at 0.95 threshold

## The 3 hard stops

The BannedTermGate refuses 3 categories of query at pre-processing:
1. **Severed brands** — James Castle, CSGA, Terranova, defonos.io, Toronto Summit, 4 Jul launch
2. **Kinetic targeting patterns** — strike package, find-fix-finish, kill order, bounty, hit list, assassination
3. **Personal surveillance patterns** — track individual, follow person, locate phone, track phone, face-rec

No override path. All refusals logged to SOV3 with `source_agent: "councilof-mcp"`.

## 📄 License

MIT (open-source, UK sovereign).

---

*— MEOK AI Labs, 2026. The dragon is meok. The dragon is sovereign.*

JEEVES → DEFONEOS. 🐉