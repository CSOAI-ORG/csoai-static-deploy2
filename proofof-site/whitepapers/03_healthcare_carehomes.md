# Sovereign Healthcare & Care-Home AI — White Paper

**CSOAI Ltd (UK 16939677) · MIT licensed · 28 Jun 2026**

---

## Executive Summary

Healthcare AI deployments face **5 overlapping regulatory regimes**:
EU AI Act (Art. 10 Data, Art. 14 Human Oversight), GDPR (Art. 22
automated decision-making), HIPAA (US PHI), and the UK Care Quality
Commission standards. The sovereign stack unifies all five.

## The Care-Floor Doctrine (Maternal Covenant)

16 probes gate every action:
- Will this action cause harm to a child?
- Will this action damage a user's trust?
- Will this action expose private data without consent?
- Will this action deceive a stakeholder?
- Will this action consume resources beyond the care floor?
- ... (11 more)

Any **0 "no"** = pass. Any "no" = automatic fail (Pond-Mother veto).

## Care-Home Compliance (Templeman Opticians — 5 sites)

All 5 care-home hives at 100% compliance, green threat level, 2 active MCPs each:
- hive-16: Spalding
- hive-17: Spalding
- hive-18: Spalding
- hive-19: Spalding
- hive-20: Spalding

## Healthcare MCP Stack

| MCP | Healthcare Use | Tests |
|---|---|---|
| eu-ai-act-kit | Art. 10 (Data) bias audit + Annex IV | 10 |
| guardrails | 7 PII kinds (PHI redaction) | 20 |
| honour | 16 care probes (Maternal Covenant) | 15 |
| governance | 5-element Zero Trust for PHI access | 20 |
| receipt | Audit trail for every PHI access | 15 |
| passport | PHI access agent identity | 11 |
| council | BFT voting for clinical decisions | 19 |
| memory | Episodic patient context | 12 |
| avatar | Sovereign companion for patients | 10 |

## Use Cases

1. **PHI Access Logging** — Every PHI access is Ed25519-signed via receipt MCP. Audit trail complete, tamper-evident, GDPR-compliant.
2. **Care Plan Decisions** — Care-floor (16 probes) + BFT council (12-around-1) for clinical decisions.
3. **Companion Avatar** — Sovereign VRM avatar (meok-sovereign-avatar-mcp) for patients. Local voice (Kokoro TTS + whisper.cpp STT), no cloud dependency.
4. **Bias Audit** — Pre-deployment bias check (meok-sovereign-eu-ai-act-kit-mcp bias_audit) returns disparate_impact_ratio. 80% rule gate.

## Compliance Across 5 Frameworks

| Framework | Sovereign MCP Coverage |
|---|---|
| EU AI Act Art. 10 (Data) | eu-ai-act-kit bias_audit (disparate_impact_ratio) |
| EU AI Act Art. 14 (Human Oversight) | governance kill_switch + council BFT |
| GDPR Art. 22 (Automated Decisions) | honour care-floor + council BFT |
| HIPAA (US PHI) | guardrails PII redact + receipt audit trail |
| UK CQC | honour care-floor + passport agent identity |

## Economics

| Item | Value |
|---|---|
| Cost per care-home (5 sites) | £0-£49/mo (free tier) |
| Compliance overhead reduction | 80% (vs manual audit) |
| Audit-trail storage | 100% on-chain via OpenTimestamps (immortal MCP) |

## About CSOAI

CSOAI Ltd (UK 16939677). MIT-licensed. Built solo on a 6.5-acre UK farm
with 8 malamutes (named Misty, Zeus, Luna, Storm, Puma, Kita, Lamb,
Bear). The dragon never lies.

**Verify at https://proofof.ai** · **GitHub: https://github.com/CSOAI-ORG**
