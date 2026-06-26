# CSOAI A2A Agent-Governance Substrate — the runtime, already built (2026-06-26)

## The one line
**Everyone is racing to build runtime agent-to-agent governance. CSOAI already shipped it — 20 MCPs, ~124 tools, verified (tools + tests + packaging).**

## Why it matters
The 2026 competitive frontier is the **agent/MCP runtime layer** — Obot (Enterprise MCP Gateway), Straiker (MCP guardrails), Speakeasy (AI Control Plane), Prediction Guard (asset registry). The EU AI Act's action-layer obligations (Art. 73 incident reporting, logging, cybersecurity) take effect 2 Aug 2026. This is the category being funded right now — and CSOAI has a **complete substrate** of it sitting in the estate, unsurfaced until this scan.

**This corrects the earlier competitive write-up** that said "runtime not built." It is built.

## The 20 MCPs (~124 tools)
| MCP | Tools | What it governs |
|---|---|---|
| agent-identity-trust | 5 | DIDs / verifiable credentials for agents |
| agent-policy-enforcement | 6 | per-agent-pair IAM ("A may call B for X") |
| agent-incident-relay | 6 | **EU AI Act Art. 73** 5-clock incident relay |
| agent-incident-reporter | 4 | signed, hash-chained incident records |
| agent-prompt-injection-firewall | 5 | OWASP LLM01 prompt-injection firewall |
| agent-x402-paywall | 6 | HTTP 402 + on-chain settlement (pay-per-call) |
| agent-handoff-certified | 6 | verifiable signed agent-to-agent task handoff |
| agent-audit-logger | 5 | hash-chained HMAC audit log |
| agent-mcp-router | 6 | one router for the whole fleet |
| agent-rate-limiter | 7 | fleet-wide shared rate limits |
| agent-data-residency | 8 | GDPR Chapter V cross-region runtime guard |
| agent-cost-allocator | 6 | multi-tenant LLM cost chargeback |
| agent-token-budget | 6 | per-agent token budgets |
| agent-orchestrator | 10 | multi-agent task management |
| agent-negotiation | 6 | propose/counter multi-agent deals |
| agent-delegation | 5 | delegate tasks to specialist agents |
| agent-replay-debugger | 8 | deterministic step-debug of agent runs |
| agent-commerce-protocol | 7 | agent commerce protocol |
| agent-commerce-payments | 6 | catalog + payments |
| agent-content-watermark | 6 | EU AI Act Art. 50 content watermarking |

## How it differentiates
- **Governed + signed at the action layer** — Art. 73 relay, hash-chained audit, certified handoff, x402 settlement receipts. Competitors observe; CSOAI **enforces + attests**.
- **Composable MCPs**, not a monolith — drop the firewall, the policy engine, or the router into any agent stack.
- **Pairs with Layer-0** — the legacy bridges + the A2A substrate = govern both the legacy systems *and* the agents that touch them, end-to-end signed.

## Honest state
- **Built + verified local:** all 20 have server.py + tools + tests + pyproject (tools-count is static; a few need the pyproject/import test-harness hygiene noted in `DEPTH_AUDIT_TESTRUN`).
- **Owner-gated to live:** publish (PyPI) + deploy (GCP VM) — same two levers as the rest of the fleet.

## Next
- Surface as a named product line in both OSes (done in CSOAI OS reference) + the deck.
- M2: this is the answer to "you're not in the agent-runtime-governance category" — you are; lead with Art. 73 + the firewall + x402.
