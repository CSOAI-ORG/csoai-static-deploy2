# SOVOS MCP Server Index — 26 servers, PyPI-published

Each row is a PyPI package. Install with `pip install <name>`. The monorepo
ships deployment configs (`<name>/Dockerfile`, `<name>/sovos.yaml`) and one
fully-built reference (`mcp-governance-crosswalk/`).

| # | PyPI Package | What It Does | Sector |
|---|---|---|---|
| 01 | csoai-governance-crosswalk-mcp | EU AI Act / NIST RMF / ISO 42001 / DORA / GDPR / NIS2 cross-walk | Cross-sector |
| 02 | ai-bom-mcp | AI Bill of Materials (CycloneDX + SPDX) | Cross-sector |
| 03 | mcp-injection-scanner | Prompt-injection detection + supply-chain RCE rules | Cross-sector |
| 04 | csoai-c2pa-signer | C2PA manifest generation + Ed25519 signing | Cross-sector |
| 05 | mcp-sov-signal | 13-axis SOV SIGNAL governance scoring | Cross-sector |
| 06 | csoai-refusalbench-mcp | RefusalBench 2026 evaluation suite | Cross-sector |
| 07 | mcp-jspace | J-Space chess board state inspection | Cross-sector |
| 08 | mcp-3kb | 3KB sigil conversion endpoint | Cross-sector |
| 09 | csoai-error-mergekit-mcp | Crash signature mining + avoidance LoRA registry | Cross-sector |
| 10 | yaml-ai-mcp | YAML/AML financial compliance | Finance |
| 11 | dlms-bridge-mcp | Smart meter governance | Energy |
| 12 | education-ai-mcp | Education sector compliance (UK DfE) | Education |
| 13 | fishkeeper-mcp | Koi health AI (Fish Clan) | Aquaculture |
| 14 | grabhire-mcp | Construction logistics (Builder Clan) | Construction |
| 15 | asi-security-mcp | Defence AI (Watchdog Clan) | Defence |
| 16 | meok-mcp | Parent brand MCP gateway | Cross-sector |
| 17 | safetyof-ai-mcp | Healthcare safety (Care Clan) | Healthcare |
| 18 | biasdetectionof-mcp | Algorithmic fairness (ART5 axis) | Cross-sector |
| 19 | dataprivacyof-mcp | Data protection (PRV axis) | Cross-sector |
| 20 | accountabilityof-mcp | Cross-industry audit trail | Cross-sector |
| 21 | proofof-ai-mcp | Provenance attestation | Cross-sector |
| 22 | sovereignof-ai-mcp | Sovereign AI compliance | Defence / Public sector |
| 23 | govbench-mcp | 479-item governance benchmark runner | Research |
| 24 | defoneos-meok-counterdrone-mcp | Counter-UAS defensive recommendation | Defence |
| 25 | defoneos-csoai-threat-model-mcp | AI threat-modelling framework | Defence |
| 26 | csoai-llm-eval-harness-mcp | Generic lm-eval-harness wrapper | Research |

## Reference implementation

`mcp-servers/mcp-governance-crosswalk/` is the only server fully implemented
in the monorepo. All others are deployed from their PyPI source.

## Live MCP Worker endpoints (streamable HTTP)

| # | Worker | What It Does | Endpoint |
|---|---|---|---|
| 01 | csoai-gspc-mcp | measure + verify signed governance credentials | `https://csoai-gspc-mcp.nicholastempleman.workers.dev/mcp` |
| 02 | csoai-city-3d-mcp | Cesium 3D city / colosseum / arena / index / IP Paper District (14 assets) | `https://csoai-city-3d-mcp.nicholastempleman.workers.dev/mcp` |

## Verification

```bash
# Verify the registry is reachable
pip install csoai-governance-crosswalk-mcp
python3 -c "import governance_crosswalk_mcp; print('OK', governance_crosswalk_mcp.__version__)"
```

## Total install base

~16,300 monthly downloads across the 26 packages (verified Aug 2026).
