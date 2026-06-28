# Reddit r/MCPservers — 12 Sovereign MCPs for trustworthy AI agents

**Title:** 12 Sovereign MCPs — passport, guardrails, governance, council, x402-payment, avatar + more (MIT)

I've shipped 12 MCP servers over the past week as part of the CSOAI sovereign substrate. Each one wraps a proven open-source project (aetherproof, superagent-ai, cognee, CesiumJS, etc.) with CSOAI's Ed25519 sigil chain + proofof.ai verification.

**Why this matters:**
- MCPs are eating the agent world, but most lack identity, audit trails, and compliance
- EU AI Act August 2 2026 deadline = urgency for any EU business shipping AI
- Sovereignty = the agent refuses to spend money or send email without your authority

**The stack (all MIT, 167 tests pass):**

1. **passport** — Ed25519-signed agent identity, narrowing-invariant delegation (authority can only DECREASE at each transfer)
2. **guardrails** — 16 prompt injection patterns, 7 PII kinds, repo poisoning scanner (wraps superagent-ai)
3. **receipt** — tamper-evident hash-chained receipts (wraps aetherproof + sphragis)
4. **governance** — 5-element Zero Trust governance + 4-level maturity (wraps Microsoft AGT + ATF)
5. **x402-payment** — HTTP 402 micropayments for 20 sovereign tools
6. **supply-chain** — SBOM + SLSA attestation + Bitcoin anchor (wraps chainloop)
7. **globe** — 33-hive geo-located registry + Cesium + deck.gl + WebGPU particles
8. **council** — 12-around-1 BFT council with 4 quorum thresholds (wraps gordian-engine)
9. **memory** — episodic + knowledge graph + Ebbinghaus temporal decay (wraps cognee)
10. **avatar** — VRM embodied sovereign character + local voice (wraps virtual-avatar SDK)
11. **skills** — CREATE→EVAL→EDIT→REVIEW→PACKAGE lifecycle (wraps MemTensor skills-vote)
12. **eu-ai-act-kit** — Aug 2 2026 Survival Kit (Annex IV, OSCAL, bias audit)

Every output is Ed25519-signed and verifiable at https://proofof.ai/passport.

Install all: `pip install meok-sovereign-passport-mcp meok-sovereign-guardrails-mcp ...`

This is part of the CSOAI sovereign substrate (https://csoai.org) — built solo on a 6.5-acre UK farm, MIT licensed.

Would love feedback from anyone shipping EU AI Act compliance, BFT council governance, or agent observability.
