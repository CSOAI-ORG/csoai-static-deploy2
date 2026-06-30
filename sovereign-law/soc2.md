# SOC 2 (AICPA TSC 2017, updated 2022) — sovereign crosswalk

> **AICPA Trust Services Criteria · 5 categories · US audit standard.**

## The 5 Trust Services Categories

| # | Category | Subject | Sovereign component |
|---|---|---|---|
| CC | Common Criteria | All 33 common criteria | sov.soc2_cc |
| A | Availability | System uptime + disaster recovery | sov.soc2_a |
| C | Confidentiality | Confidential information protection | sov.soc2_c |
| PI | Processing Integrity | Completeness + accuracy + timeliness | sov.soc2_pi |
| P | Privacy | Personal information handling | sov.soc2_p |

## The 5 Trust Services Principles

| # | Principle | Sovereign component |
|---|---|---|
| 1 | Security | sov.soc2_security + sov.zero_trust |
| 2 | Availability | sov.soc2_availability + sov.bcp |
| 3 | Processing integrity | sov.soc2_pi + sov.sigil_chain |
| 4 | Confidentiality | sov.soc2_confidentiality |
| 5 | Privacy | sov.soc2_privacy + sov.gdpr |

## The 33 Common Criteria (CC1–CC9)

| Group | Number | Subject | Sovereign component |
|---|---|---|---|
| CC1 | 5 criteria | Control environment | sov.soc2_cc1_1 to sov.soc2_cc1_5 |
| CC2 | 3 criteria | Communication + information | sov.soc2_cc2_1 to sov.soc2_cc2_3 |
| CC3 | 4 criteria | Risk assessment | sov.soc2_cc3_1 to sov.soc2_cc3_4 |
| CC4 | 2 criteria | Monitoring activities | sov.soc2_cc4_1 to sov.soc2_cc4_2 |
| CC5 | 3 criteria | Control activities | sov.soc2_cc5_1 to sov.soc2_cc5_3 |
| CC6 | 8 criteria | Logical + physical access | sov.soc2_cc6_1 to sov.soc2_cc6_8 |
| CC7 | 5 criteria | System operations | sov.soc2_cc7_1 to sov.soc2_cc7_5 |
| CC8 | 2 criteria | Change management | sov.soc2_cc8_1 to sov.soc2_cc8_2 |
| CC9 | 1 criterion | Risk mitigation | sov.soc2_cc9_1 |

## The CSOAI crosswalk

| SOC 2 Category | Substrate component |
|---|---|
| CC1 (Control environment) | sov.governance + sov.bft_council |
| CC2 (Communication) | sov.transparency + sov.article_13 |
| CC3 (Risk assessment) | sov.risk_assessment |
| CC4 (Monitoring) | sov.monitoring + sov.sigil_chain |
| CC5 (Control activities) | sov.control_activities |
| CC6 (Access) | sov.access_control + sov.mfa + sov.pqc |
| CC7 (System ops) | sov.system_ops + sov.incident_response |
| CC8 (Change mgmt) | sov.change_mgmt + sov.audit_log |
| CC9 (Risk mitigation) | sov.risk_mitigation |
| Availability | sov.availability + sov.bcp |
| Confidentiality | sov.confidentiality + sov.zero_trust |
| Processing integrity | sov.processing_integrity |
| Privacy | sov.privacy + sov.gdpr |

## Audit + report

The CSOAI substrate's SOC 2 Type II audit (in progress) covers all 33 Common Criteria + the 4 applicable Trust Services Categories (Security + Availability + Confidentiality + Privacy).

---

**Built 30 Jun 2026 · M4 · CSOAI Ltd UK 16939677 · MIT**

— 🜏 Solve et Coagula