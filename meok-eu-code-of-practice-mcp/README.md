# meok-eu-code-of-practice-mcp

A [Model Context Protocol](https://modelcontextprotocol.io/) server that wraps C2PA Content Credentials and watermarking into a single, signed **two-layer attestation manifest** compliant with the **EU Code of Practice on AI content marking (draft 2, finalising June 2026)**, which operationalises **EU AI Act Article 50(2)** transparency obligations (enforceable 2 August 2026 for new systems).

[![CSOAI](https://img.shields.io/badge/Built%20by-CSOAI%20%7C%20MEOK%20AI%20Labs-blue)](https://meok.ai)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Why this matters

A [Model Context Protocol](https://modelcontextprotocol.io/) server that wraps C2PA Content Credentials and watermarking into a single, signed **two-layer attestation manifest** compliant with the **EU Code of Practice on AI content marking (draft 2, finalising June 2026)**, which operationalises **EU AI Act Article 50(2)** transparency obligations (enforceable 2 August 2026 for new systems).

## Installation

```bash
pip install meok-eu-code-of-practice-mcp
```

## Tools (exactly 4)

| # | Tool | Purpose |
|---|------|---------|
| 1 | `mark_content(content, content_type, generator)` | Produce a signed two-layer attestation manifest for a piece of content. |
| 2 | `verify_attestation(manifest)` | Verify a manifest's C2PA layer, watermark layer, and Ed25519 signature. |
| 3 | `detect_ai_content(content)` | Heuristically score whether content appears AI-generated and optionally match a fingerprint. |
| 4 | `compliance_check(operator)` | Return a Code-of-Practice compliance posture for a given operator. |

All tools return JSON with: `status`, `manifest` (where applicable), `compliance_posture`, `recommendations`, `signature`, `code_of_practice_version`.

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
