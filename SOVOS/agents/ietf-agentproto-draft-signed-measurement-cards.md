# IETF agentproto WG — BoF / Internet-Draft Proposal

## Title
**Signed Measurement Cards for Agentic Systems**
draft-templeman-signed-measurement-cards-00

## Abstract (for IETF 127 BoF scheduling, opens 17 Aug 2026)

Agentic AI systems (autonomous agents, multi-agent swarms, agent-to-agent
commerce) need verifiable audit trails that are independent of any single
system's trust domain. Existing approaches either tie audit evidence to a
specific platform (proprietary formats) or require a centralised notary
(conflicting with agent autonomy).

This document defines a lightweight, self-contained Signed Measurement Card
(SMC) format that binds a set of measurement results (probes across safety,
governance, privacy, and capability axes) to a cryptographic digest of the
agent's identity, weights, and configuration. SMCs are:

- **Transport-agnostic**: can be embedded in HTTP headers (402 Payment
  Required), x402/AP2 payment mandates, MCP tool calls, or A2A agent
  coordination messages.
- **Verifiable offline**: each card carries an Ed25519 signature whose public
  key resolves to a `did:web` or `did:key` identifier. No back-end call is
  required to verify authenticity.
- **Transparency-ready**: cards can be optionally registered with a SCITT
  (RFC 9943) transparency service to prove non-repudiability and issuance
  time.
- **Paired by design**: every measurement produces TWO cards sharing a
  `pair_id` — one signed, one unsigned — so the overhead of cryptographic
  attestation is itself a measurable, publishable number.

## Problem space (for BoF charter justification)

Several IETF-related efforts currently touch on agent identity and audit
but leave a measurement-provenance gap:

- **x402 Foundation** (Linux Foundation, launched July 2026): defines an
  HTTP 402 payment flow for agent transactions but has no built-in mechanism
  for verifying an agent's safety or behaviour before payment release.
- **AP2 (Agent Payments Protocol)**: uses W3C Verifiable Credentials for
  payment mandates; SMCs can extend those mandates with verifiable
  measurement evidence.
- **MCP (Model Context Protocol)**: no standardised way to convey
  measurement results or safety attestations between clients and servers.
- **A2A protocol**: focuses on agent discovery and coordination; audit
  trails are left to each implementation.

A chartered agentproof WG would define a minimal, cross-protocol measurement
card format that any of these protocols can reference, while leaving
domain-specific extensions (payment, content provenance, identity) to other
WGs.

## Author affiliation
CSOAI LTD (UK 16939677) — independent AI measurement body.
Contact: nicholas@csoai.org

## Keywords
agent attestation, measurement card, signed audit trail, GSPC, x402, SCITT