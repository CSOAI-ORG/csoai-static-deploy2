# meok-ai-psych-vuln-audit-mcp

**EU AI Act Article 5(1)(f) gambling-vertical compliance audit MCP.**

[![CSOAI](https://img.shields.io/badge/Built%20by-CSOAI%20%7C%20MEOK%20AI%20Labs-blue)](https://meok.ai)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Why this matters

**EU AI Act Article 5(1)(f) gambling-vertical compliance audit MCP.**

## Installation

```bash
pip install meok-ai-psych-vuln-audit-mcp
```

## Tools (4)

| Tool | Purpose |
|---|---|
| `audit_player_intervention(player_action)` | Audit a single AI-driven player intervention (push, bonus, pop-up) against the 12 gambling-AI risk patterns. |
| `scan_marketing_copy(copy, target_segment)` | Scan marketing copy targeting a player segment for FOMO, loss-framing, minor-targeting, and other Art 5(1)(f) triggers. |
| `classify_ai_system(ai_system)` | Classify an AI system's purpose + training data + decision points for Art 5(1)(f) risk class. |
| `generate_audit_report(operator_id, audit_period, interventions)` | Produce a regulator-ready, Ed25519-signed audit report over a list of AI interventions. |

All four tools return a JSON envelope:
```json
{
  "status": "PASS|REVIEW|FAIL",
  "triggered_patterns": [...],
  "severity_score": 0.0,
  "recommendations": [...],
  "signature": "<128 hex chars>"
}
```

## Compliance mapping

- [EU AI Act](https://csoai.org/article-50-kit)

## Verify attestations

When this MCP generates signed reports, they can be verified publicly at:
https://meok-attestation-api.vercel.app/verify

No login required.

## Learn more

- CSOAI: https://csoai.org
- MEOK AI Labs: https://meok.ai
- Layer 0 architecture: https://meok.ai/layer0

## License

MIT — Copyright (c) 2026 MEOK AI Labs / CSOAI Ltd.

---

*Keywords: #EUAIAct*
