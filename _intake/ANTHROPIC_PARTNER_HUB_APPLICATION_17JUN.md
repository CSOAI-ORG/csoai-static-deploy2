# Anthropic Partner Hub Application

**Company:** CSOAI Ltd (trading as MEOK AI Labs)  
**Company Number:** UK 16939677  
**Date:** 17 June 2026  
**Contact:** nicholas@csoai.org  
**Focus:** EU AI Act compliance + AI safety certification

---

## 1. Overview

CSOAI Ltd operates **MEOK AI Labs**, a London-based AI safety infrastructure company. We have built the largest open-source MCP (Model Context Protocol) server ecosystem — 218 MCP servers — purpose-built for **EU AI Act compliance, AI governance, and safety certification**.

Our keystone product is the **MEOK Sovereignty Stack**: an attestation-gated AI governance layer that uses Claude-powered Ed25519-signed attestations to certify that AI tool invocations comply with the EU AI Act. We are applying to the Anthropic Partner Hub to deepen our integration with the Claude/MCP ecosystem and bring enterprise-grade compliance tooling to every Claude deployment.

### Key Facts

| Field | Value |
|---|---|
| Registered company | CSOAI Ltd, UK |
| Registration number | 16939677 |
| Headquarters | London, UK |
| Active since | Q1 2026 |
| Open-source MCP servers | 218 |
| Compliance fleet | 95 dedicated servers |
| Primary standard | EU AI Act (2024/1689) |

---

## 2. Product

### MEOK Sovereignty Stack

The Sovereignty Stack is a **Claude-powered compliance attestation layer** for MCP tool access. Every MCP tool invocation is cryptographically signed, compliance-checked, and audited in real time.

**Core components:**

1. **218 Open-Source MCP Servers** — covering compliance, governance, data operations, utility, and gaming. All servers implement the Model Context Protocol and are auditable by any Claude instance.

2. **Keystone Attestation Engine** — Ed25519-signed attestations that certify each MCP call meets EU AI Act requirements (risk classification, transparency obligations, human oversight).

3. **95-Server Compliance Fleet** — dedicated servers running continuous EU AI Act conformity assessments, documentation generation, and audit trail maintenance.

4. **x402 Payment Layer** — HTTP 402 Payment Required flow for monetising MCP tool access (£1 per attestation, £25 per batch, £499 per project).

### EU AI Act Coverage

Our compliance fleet maps to every relevant article of the EU AI Act:

- **Title III (High-Risk AI Systems):** Risk classification, conformity assessment, technical documentation
- **Title IV (Transparency):** Provider registration, transparency obligations
- **Title V (General-Purpose AI):** GPAI code of practice, systemic risk assessment
- **Chapter 5 (Human Oversight):** Human-in-the-loop attestation verification

---

## 3. Market Fit

### Problem

Enterprises deploying Claude and other foundation models face a regulatory cliff. The EU AI Act imposes graduated obligations — transparency, risk classification, conformity assessment — with penalties of up to 7% of worldwide annual turnover. Most organisations lack the tooling to operationalise compliance at the API-call level.

### Solution

MEOK provides the missing layer: **compliance-gated API access**. Every MCP tool call includes an Ed25519-signed attestation that proves:

- The caller's identity and authorisation level
- The EU AI Act risk classification for the operation
- The compliance obligations met
- The audit trail reference

### Traction

- **218 open-source MCP servers** publicly available (GitHub, NPM, PyPI)
- **95-server compliance fleet** running continuous assessments
- **EU AI Act first-mover position** — launched before enforcement dates
- **£0 MRR** (pre-revenue — x402 payment layer launching June 2026)

### Target Customers

- EU-based AI providers needing Article 16 compliance
- Non-EU AI providers serving EU users (extraterritorial scope under Article 2)
- Regulated industries (finance, healthcare, legal) deploying Claude for high-risk use cases
- AI audit firms requiring attestation-gated access

---

## 4. Technical Integration

### Anthropic Ecosystem Alignment

MEOK is built **on** and **for** the Anthropic ecosystem:

| Component | Integration Point |
|---|---|
| **MCP Protocol** | 218 servers implement the Model Context Protocol natively |
| **Claude** | Keystone attestations are Claude-powered (prompt engineering + structured output) |
| **MCP Client** | Any Claude/Anthropic MCP client can call our fleet |
| **x402** | Payment-Required flow compatible with Claude's tool-use loop |

### Architecture

```
Claude Client → MCP Request → MEOK Gateway (x402 check)
                                    ↓
                            [Payment Required?]
                           /                  \
                         Yes                  No
                           ↓                    ↓
                   Stripe Checkout      Compliance Fleet
                           ↓                    ↓
                   Attestation Token    EU AI Act Audit
                           ↓                    ↓
                    Replay Request        Signed Result
```

### Security

- **Ed25519 attestations** — all payment and compliance proofs are Ed25519-signed
- **Signing secret verification** — Stripe webhooks secured with signing secrets
- **x402 flow** follows draft RFC for HTTP Payment Required in AI contexts

---

## 5. Partnership Ask

We are seeking an **Anthropic Partner Hub technical partnership** to:

### Distribution

- Featured placement in the Anthropic Partner Hub directory
- Cross-listing on the MCP ecosystem page
- Joint blog post or case study on EU AI Act compliance with Claude

### Co-Marketing

- Joint webinar: "EU AI Act Compliance with Claude + MEOK"
- Reference customer pipeline: MEOK-powered compliance attestations in Claude deployments
- Social media collaboration (case studies, technical deep-dives)

### Technical Partnership

- Early access to Claude API features (structured output, tool-use enhancements)
- Collaboration on MCP protocol extensions for payment/attestation
- Joint reference architecture for EU AI Act compliance with Claude
- Potential MEOK-powered compliance tool as an Anthropic-internal demonstration

### What We Offer in Return

- **First-mover reference** for Claude in EU AI Act compliance use cases
- **218 open-source MCP servers** contributing to MCP ecosystem health
- **Open standard** (x402 attestation flow) compatible with Anthropic's tool-use vision
- **95-server fleet** as a real-world stress test for MCP at scale

---

*"The EU AI Act is the world's first comprehensive AI regulation. Every MCP call needs an audit trail. We built it."*

**CSOAI Ltd** — UK 16939677 — [meok.ai](https://meok.ai) — nicholas@csoai.org
