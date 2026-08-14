---
name: council-gspc-measure
description: Measure or verify AI governance using the Council of AI GSPC endpoint. Run a model/agent through GSPC axes to get a signed measurement credential, or verify a signed card. Issue is a measurement, never a certification. Use when asked to assess, grade, verify, or measure AI governance behavior.
version: 1.0.0
metadata:
  provider: Council of AI (CSOAI Ltd, UK 16939677)
  author: councilof.ai
  homepage: https://councilof.ai
  license: measurement-not-certification
---

# Council GSPC Measure

Call the Council of AI GSPC MCP endpoint to measure or verify AI governance.

## Endpoint

- Transport: streamable HTTP (MCP)
- URL: `https://csoai-gspc-mcp.nicholastempleman.workers.dev/mcp`
- Register: `io.github.CSOAI-ORG/gspc` (Official MCP Registry)

## Tools

### measure
Run a subject through GSPC governance axes. Returns a **signed measurement credential**.
- Honesty: this is a *measurement*, never a certification or compliance claim.
- Unmeasured axes are reported as `UNMEASURED`, never as zero.
- Signed issuance is metered (free to verify, paid to issue).

Parameters:
- `model`: subject to measure (string, required)
- `axes`: GSPC axes to run (array of strings, optional)

### verify
Verify a signed card: recompute `content_id`, check the Ed25519 signature + time-anchor.
- Free, anonymous, no trust in us required.
- Offline verifier: `https://csoai-attest-verify.nicholastempleman.workers.dev/verify`

## Guardrails (bind)

1. Never represent a measurement credential as certification, compliance, or "board-grade."
2. Never quote an index number without its confidence interval + caveats.
3. Missing cells are `UNMEASURED`, never zero.
4. Do not claim BFT councils or certification bodies exist unless CI-verified.
5. Do not reference SOVOS/SOV-*/sov6 codenames on any public surface.

## Register

- `REAL` verified/live · `DEMO` works-with-demo-data · `THEORY` unverified · `GATED` owner/keys
