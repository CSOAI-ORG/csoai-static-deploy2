# FLEET_SCORE Preparation — 17 June 2026

**Purpose:** Prepare scoring framework for MEOK's 14 flagship MCP servers + keystone attestation engine. Scores will be computed automatically by the FLEET_SCORE system once Sprint 3 revenue activation is live.

---

## Scoring Criteria (100 pts total)

| Category | Weight | Description |
|---|---|---|
| **Test Coverage** | 25 pts | Unit + integration test coverage of MCP tools and handlers |
| **Documentation** | 25 pts | README completeness, API docs, examples, changelog |
| **Uptime** | 20 pts | Historical availability (99%+ = 20pts, 95%+ = 10pts, below = 0) |
| **Performance** | 15 pts | P50/P95 latency, throughput under load, response size efficiency |
| **Security** | 15 pts | Input validation, auth implementation, dependency scanning, secret hygiene |

### Scoring Scale

| Level | Range | Meaning |
|---|---|---|
| 🟢 **Excellent** | 85-100 | Production-ready, fully documented, well-tested |
| 🟡 **Good** | 65-84 | Functional, minor gaps in docs or test coverage |
| 🟠 **Adequate** | 40-64 | Core features work, significant coverage/docs gaps |
| 🔴 **Needs Work** | 0-39 | Missing critical components (tests, docs, security) |

---

## Fleet Inventory

### Keystone

| # | Name | Category | Test Coverage Est. | Docs Status | Score | Notes |
|---|---|---|---|---|---|---|
| 0 | **keystone-attestation** | compliance | ~70% | Draft v2 | — | Ed25519 attestation engine; core of x402 payment flow |

### Flagship MCP Servers

| # | Name | Category | Test Coverage Est. | Docs Status | Score | Notes |
|---|---|---|---|---|---|---|
| 1 | **mcp-eu-ai-act** | compliance | ~60% | Draft v1 | — | EU AI Act risk classification, conformity assessment mapping |
| 2 | **mcp-governance-audit** | governance | ~55% | Draft v1 | — | Audit trail generation, compliance evidence collection |
| 3 | **mcp-attestation-verify** | compliance | ~75% | Draft v2 | — | Ed25519 attestation verification, signature validation |
| 4 | **mcp-data-moat** | data | ~50% | Draft v1 | — | 49 GB reference data store, schema registry |
| 5 | **mcp-compliance-fleet** | governance | ~45% | Outline | — | 95-server compliance fleet orchestration |
| 6 | **mcp-risk-classifier** | compliance | ~65% | Draft v1 | — | EU AI Act risk tier classification (minimal/low/high/GPAI) |
| 7 | **mcp-transparency-register** | compliance | ~50% | Outline | — | Provider registration, transparency obligation tracking |
| 8 | **mcp-human-oversight** | governance | ~40% | Outline | — | Human-in-the-loop attestation workflow |
| 9 | **mcp-x402-gateway** | utility | ~35% | Draft v1 | — | HTTP 402 Payment Required gateway for MCP access |
| 10 | **mcp-kv-store** | data | ~80% | Final v1 | — | Key-value persistence for attestation state |
| 11 | **mcp-prompt-auditor** | utility | ~60% | Draft v1 | — | Prompt injection detection, output validation |
| 12 | **mcp-sov3-health** | utility | ~70% | Final v1 | — | SOV3 health check, King hive status reporting |
| 13 | **mcp-sigil-seal** | governance | ~55% | Outline | — | Sprint seal generation, SEAL protocol implementation |
| 14 | **mcp-hex-gaming** | gaming | ~30% | Outline | — | Hex-based gaming MCP (demonstrator / ecosystem reach) |

---

## Fleet Scorecard Template

```json
{
  "fleet_score": {
    "timestamp": "2026-06-17T00:00:00Z",
    "generated_by": "FLEET_SCORE v0.1",
    "criteria": {
      "test_coverage": {"weight": 25, "description": "Unit + integration test coverage of MCP tools and handlers"},
      "documentation": {"weight": 25, "description": "README completeness, API docs, examples, changelog"},
      "uptime": {"weight": 20, "description": "Historical availability percentage"},
      "performance": {"weight": 15, "description": "P50/P95 latency and throughput"},
      "security": {"weight": 15, "description": "Input validation, auth, dependency scanning"}
    },
    "servers": [
      {
        "id": 0,
        "name": "keystone-attestation",
        "category": "compliance",
        "scores": {
          "test_coverage": null,
          "documentation": null,
          "uptime": null,
          "performance": null,
          "security": null
        },
        "total": null,
        "grade": null
      }
    ],
    "summary": {
      "total_servers": 15,
      "average_score": null,
      "top_server": null,
      "bottom_server": null,
      "recommendations": []
    }
  }
}
```

---

## Next Steps

1. Complete scoring for all 15 entries (14 MCPs + 1 keystone)
2. Implement FLEET_SCORE automated evaluator (test runner + doc scraper + uptime monitor)
3. Publish first fleet scorecard alongside Sprint 3 revenue launch
4. Set minimum score threshold for production listing (target: ≥80 for public listing)
5. Establish weekly scoring cadence

---

*Document version: 1.0 · Prepared: 17 June 2026 · Owner: MEOK AI Labs / CSOAI Ltd*
