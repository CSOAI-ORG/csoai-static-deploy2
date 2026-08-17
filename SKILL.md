---
name: gspc
description: Measure an AI system against GSPC axes and get back a signed, third-party-verifiable measurement card; or verify any signed card offline. Use when asked to evaluate, measure, verify, or check an AI model/system's governance, safety, privacy, or provenance behaviour. Council of AI (CSOAI LTD) — measurement, not certification.
---

# gspc — signed AI measurement

## Verify a card (offline, free, no account)
```bash
python3 verify_offline.py --card <card.json>
```
Recomputes the content id, checks the Ed25519 signature, walks the chain. VALID or the specific mismatch. Tamper any field → fails.

## Measure a system (remote MCP)
Endpoint: `https://csoai-gspc-mcp.nicholastempleman.workers.dev/mcp` (streamable HTTP). Tools: `measure(model, axes)` → signed card; `verify(card)` → verdict. Unmeasured axes return UNMEASURED — never interpolated.

## Rules
- Cards are measurements, not certifications. Say "measured," never "certified."
- The deterministic core decides; narration is presentation, not evidence.

Citation: https://doi.org/10.5281/zenodo.21973003
