# Sovereign Banking & DORA — White Paper

**CSOAI Ltd (UK 16939677) · MIT licensed · 28 Jun 2026**

---

## Executive Summary

EU DORA (Digital Operational Resilience Act, EU 2022/2554) applies to
**~22,000 financial entities** in the EU + third-country providers
servicing EU firms. Critical Third-Party Providers (CTPPs) face
direct designation by ESAs.

This paper shows how the **DORA MCP** delivers the 5-pillar audit
in <1 second, with Ed25519-signed evidence ready for ESAs.

## DORA 5 Pillars (mapped to sovereign MCPs)

| Pillar | Article | Sovereign MCP Coverage |
|---|---|---|
| 1. ICT Risk Management | Art. 5-16 | governance + defence (threat assessment) |
| 2. ICT Incident Reporting | Art. 17-23 | dora (4h/24h/1m tiers) + council (BFT) |
| 3. Digital Operational Resilience Testing | Art. 24-27 | dora (5 tests: vuln, pen, stress, red-team, scenario) |
| 4. ICT Third-Party Risk Management | Art. 28-44 | passport (narrowing invariant) + governance |
| 5. Information Sharing Arrangements | Art. 45 | council (BFT voting) + audit chain |

## CTPP Auto-Classification (sample of 14 entities)

| Entity | Type | Employees | CTPP? | Reason |
|---|---|---|---|---|
| HSBC UK | credit_institution | 200,000 | ✓ YES | ≥ 50 employees threshold |
| Barclays UK | credit_institution | ~85,000 | ✓ YES | ≥ 50 employees threshold |
| ING Bank NV | credit_institution | ~60,000 | ✓ YES | ≥ 50 employees threshold |
| BNP Paribas | credit_institution | ~190,000 | ✓ YES | ≥ 50 employees threshold |
| Deutsche Bank | credit_institution | ~90,000 | ✓ YES | ≥ 50 employees threshold |
| Santander | credit_institution | ~200,000 | ✓ YES | ≥ 50 employees threshold |
| UBS | credit_institution | ~75,000 | ✓ YES | ≥ 50 employees threshold |
| Aviva | insurance | ~31,000 | ✓ YES | ≥ 25 employees threshold |
| Munich Re | insurance | ~30,000 | ✓ YES | ≥ 25 employees threshold |
| Allianz | insurance | ~150,000 | ✓ YES | ≥ 25 employees threshold |

Thresholds: credit_institution 50+ · insurance 25+ · investment 10+ · crypto 10+

## ICT Incident Reporting Tiers

| Severity | Initial Report | Intermediate | Final |
|---|---|---|---|
| Critical | **4 hours** | 24 hours | 1 month |
| High | 4 hours | 72 hours | 1 month |
| Medium | 24 hours | 72 hours | 1 month |
| Low | best effort | best effort | best effort |

Detection heuristics:
- "ransomware" / "data_loss" → critical
- "outage" / "downtime" → high
- >10,000 affected users → high
- >1,000 affected users OR >4h duration → medium

## How to Get Started

```bash
pip install meok-sovereign-dora-mcp

# 5-pillar audit
sovereign dora audit "your-bank" '{"pillar_1": 10, "pillar_2": 10, ...}'
# → compliance_level: sovereign

# CTPP classify
sovereign dora classify "your-bank" '{"entity_type": "credit_institution", "employees": 5000, "is_credit_institution": true}'
# → is_ctpp: true (or false)

# Incident report (ransomware)
sovereign dora incident "Ransomware encrypts customer data" '{"affected_users": 50000}'
# → severity: critical, initial: 4 hours

# Register in CTPP register (DORA Art. 31)
sovereign dora register "your-bank" "20HU8550TFCT4RW2P530" '{"entity_type": "credit_institution"}'
# → register_id, Lei validated
```

## Resilience Testing (Pillar 3)

Required tests: vulnerability, penetration, stress, red-team, scenario.
Sovereign score: all 5 passing = "sovereign" assurance.

## About CSOAI

CSOAI Ltd (UK 16939677). MIT-licensed sovereign stack. The dragon never lies.

**Verify at https://proofof.ai** · **GitHub: https://github.com/CSOAI-ORG**
