# CSOAI Layer-0 Legacy-Bridge Family — Index (15 MCPs)

The governed gateway to the systems that run the world. Each bridge is a working MCP: **parse legacy → validate → map to modern → govern → attest (Ed25519)**. All 15 on CSOAI-ORG, tested + CI + CodeQL + OpenSSF Scorecard + registry-valid `server.json`.

| # | Bridge | Repo (`io.github.CSOAI-ORG/…`) | Sector | Governing frameworks | Visibility |
|---|---|---|---|---|---|
| 1 | COBOL / Mainframe | `cobol-bridge-mcp` | Banking cores | SOX | public · PyPI · 86/100 |
| 2 | ISO 20022 / SWIFT | `iso20022-bridge-mcp` | Payments | DORA, NIS2 | private |
| 3 | HL7 / FHIR | `hl7-fhir-bridge-mcp` | Healthcare | HIPAA, EU AI Act | private |
| 4 | IBM AS/400 | `as400-bridge-mcp` | Enterprise i | SOX | private |
| 5 | SAP IDoc | `sap-bridge-mcp` | ERP | SOX | private |
| 6 | Oracle PL/SQL | `oracle-bridge-mcp` | Databases | GDPR, SOX | private |
| 7 | SCADA / OT | `scada-bridge-mcp` | Industrial / energy | NIS2, IEC 62443 | private |
| 8 | EDI / EDIFACT | `edi-bridge-mcp` | Supply chain | SOX, Peppol/ViDA | private |
| 9 | FIX | `fix-bridge-mcp` | Trading | DORA, MiFID II | private |
| 10 | CICS | `cics-bridge-mcp` | Mainframe TX | SOX, PCI-DSS | private |
| 11 | MQTT / IoT | `mqtt-bridge-mcp` | Devices / OT | NIS2, IEC 62443 | private |
| 12 | ACORD | `acord-bridge-mcp` | Insurance | Solvency II, GDPR | private |
| 13 | NACHA / ACH | `nacha-bridge-mcp` | US payments | SOX, OFAC, BSA/AML | private |
| 14 | ISO 8583 | `iso8583-bridge-mcp` | Card payments | DORA, PCI-DSS, PSD2 | private |
| 15 | SIP | `sip-bridge-mcp` | Telephony | NIS2, STIR/SHAKEN | private |

## State
- **Code + tests:** all 15 functional-tested (pytest passing).
- **CI / security:** GitHub Actions CI + CodeQL + OpenSSF Scorecard + Dependabot + SECURITY.md on all 15.
- **Registry:** all 15 `server.json` valid against the current MCP-registry schema (`registryType` + `runtimeHint`).
- **Geo + relevance:** every bridge has real-world coordinates + governing-framework edges in `csoai-governance-map.json` (the single source of truth) — rendered on the MEOK globe (`meok-town-view`) and consumable by M2's `/map` + `/temples`.

## Remaining (owner-gated)
- **cosign signing** (needs key/identity) + **PyPI publish** (`twine` token) — the last steps to public + registry-listed. All credential-free hardening is done.

## The pitch line
*CSOAI is the only sovereign-grade governance layer that bridges the entire legacy economy — banks, hospitals, grids, markets, insurers, telecom — and signs every translation. Built ≫ published; distribution is the lever.*
