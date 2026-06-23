# FLEET_SCORE Final Preparation — 17 June 2026

**Purpose:** Finalised scoring framework for MEOK's 14 flagship MCP servers + keystone attestation engine. Combines Sprint 3 subagent work with initial computed scores. Source: `_intake/FLEET_SCORE_PREP_17JUN.md`

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

## Keystone

| # | Name | Category | Test Coverage | Docs | Uptime | Perf | Security | **Total** | Grade |
|---|------|----------|:------------:|:----:|:-----:|:----:|:--------:|:---------:|:-----:|
| 0 | **keystone-attestation** | compliance | 17 | 20 | 15 | 12 | 14 | **78** | 🟡 Good |

## Flagship MCP Servers

| # | Name | Category | Test Coverage | Docs | Uptime | Perf | Security | **Total** | Grade |
|---|------|----------|:------------:|:----:|:-----:|:----:|:--------:|:---------:|:-----:|
| 1 | **mcp-eu-ai-act** | compliance | 15 | 15 | 15 | 12 | 12 | **69** | 🟡 Good |
| 2 | **mcp-governance-audit** | governance | 14 | 15 | 15 | 11 | 12 | **67** | 🟡 Good |
| 3 | **mcp-attestation-verify** | compliance | 19 | 20 | 15 | 13 | 14 | **81** | 🟡 Good |
| 4 | **mcp-data-moat** | data | 13 | 15 | 15 | 10 | 12 | **65** | 🟡 Good |
| 5 | **mcp-compliance-fleet** | governance | 11 | 10 | 15 | 11 | 12 | **59** | 🟠 Adequate |
| 6 | **mcp-risk-classifier** | compliance | 16 | 15 | 15 | 12 | 12 | **70** | 🟡 Good |
| 7 | **mcp-transparency-register** | compliance | 13 | 10 | 15 | 11 | 12 | **61** | 🟠 Adequate |
| 8 | **mcp-human-oversight** | governance | 10 | 10 | 15 | 11 | 12 | **58** | 🟠 Adequate |
| 9 | **mcp-x402-gateway** | utility | 9 | 15 | 15 | 12 | 12 | **63** | 🟠 Adequate |
| 10 | **mcp-kv-store** | data | 20 | 25 | 20 | 14 | 13 | **92** | 🟢 Excellent |
| 11 | **mcp-prompt-auditor** | utility | 15 | 15 | 15 | 12 | 12 | **69** | 🟡 Good |
| 12 | **mcp-sov3-health** | utility | 18 | 25 | 20 | 13 | 13 | **89** | 🟢 Excellent |
| 13 | **mcp-sigil-seal** | governance | 14 | 10 | 15 | 11 | 12 | **62** | 🟠 Adequate |
| 14 | **mcp-hex-gaming** | gaming | 8 | 10 | 10 | 10 | 10 | **48** | 🟠 Adequate |

## Summary

| Metric | Value |
|--------|:-----:|
| **Total scored entries** | 15 (14 MCPs + 1 keystone) |
| **Average score** | **67.5** |
| **Top server** | mcp-kv-store (92) 🟢 |
| **Bottom server** | mcp-hex-gaming (48) 🟠 |
| **Excellent (85+)** | 2 (kv-store, sov3-health) |
| **Good (65-84)** | 7 (keystone, eu-ai-act, governance-audit, attestation-verify, data-moat, risk-classifier, prompt-auditor) |
| **Adequate (40-64)** | 5 (compliance-fleet, transparency-register, human-oversight, x402-gateway, sigil-seal, hex-gaming) |
| **Needs Work (0-39)** | 0 |

## Fleet Scorecard (JSON Template)

```json
{
  "fleet_score": {
    "timestamp": "2026-06-17T12:00:00Z",
    "generated_by": "FLEET_SCORE v0.1 (Sprint 4 final prep)",
    "sprint": "Sprint 3 — REVENUE ACTIVATION (carried forward)",
    "criteria": {
      "test_coverage": {"weight": 25, "description": "Unit + integration test coverage of MCP tools and handlers"},
      "documentation": {"weight": 25, "description": "README completeness, API docs, examples, changelog"},
      "uptime": {"weight": 20, "description": "Historical availability percentage"},
      "performance": {"weight": 15, "description": "P50/P95 latency and throughput"},
      "security": {"weight": 15, "description": "Input validation, auth, dependency scanning"}
    },
    "servers": [
      {"id": 0, "name": "keystone-attestation", "category": "compliance", "total": 78, "grade": "Good"},
      {"id": 1, "name": "mcp-eu-ai-act", "category": "compliance", "total": 69, "grade": "Good"},
      {"id": 2, "name": "mcp-governance-audit", "category": "governance", "total": 67, "grade": "Good"},
      {"id": 3, "name": "mcp-attestation-verify", "category": "compliance", "total": 81, "grade": "Good"},
      {"id": 4, "name": "mcp-data-moat", "category": "data", "total": 65, "grade": "Good"},
      {"id": 5, "name": "mcp-compliance-fleet", "category": "governance", "total": 59, "grade": "Adequate"},
      {"id": 6, "name": "mcp-risk-classifier", "category": "compliance", "total": 70, "grade": "Good"},
      {"id": 7, "name": "mcp-transparency-register", "category": "compliance", "total": 61, "grade": "Adequate"},
      {"id": 8, "name": "mcp-human-oversight", "category": "governance", "total": 58, "grade": "Adequate"},
      {"id": 9, "name": "mcp-x402-gateway", "category": "utility", "total": 63, "grade": "Adequate"},
      {"id": 10, "name": "mcp-kv-store", "category": "data", "total": 92, "grade": "Excellent"},
      {"id": 11, "name": "mcp-prompt-auditor", "category": "utility", "total": 69, "grade": "Good"},
      {"id": 12, "name": "mcp-sov3-health", "category": "utility", "total": 89, "grade": "Excellent"},
      {"id": 13, "name": "mcp-sigil-seal", "category": "governance", "total": 62, "grade": "Adequate"},
      {"id": 14, "name": "mcp-hex-gaming", "category": "gaming", "total": 48, "grade": "Adequate"}
    ],
    "summary": {
      "total_servers": 15,
      "average_score": 67.5,
      "top_server": "mcp-kv-store",
      "bottom_server": "mcp-hex-gaming",
      "recommendations": [
        "Raise hex-gaming (48): needs test coverage + docs — target ≥65",
        "Raise compliance-fleet (59): docs need upgrade from Outline → Draft",
        "Raise human-oversight (58): core governance MCP, needs testing + docs",
        "Publish first fleet scorecard alongside Sprint 4 launch",
        "Set minimum threshold ≥75 for public listing",
        "Establish weekly scoring cadence via FLEET_SCORE automated evaluator"
      ]
    }
  }
}
```

## Next Steps

1. Implement FLEET_SCORE automated evaluator (test runner + doc scraper + uptime monitor)
2. Publish first fleet scorecard alongside Sprint 4 launch
3. Set minimum score threshold for production listing (target: ≥80 for public listing)
4. Establish weekly scoring cadence

---

*Document version: 1.1 · Final prep (Sprint 3+4 combined) · Generated: 17 June 2026 · Owner: MEOK AI Labs / CSOAI Ltd*
