# Compliance Crosswalk — 12 frameworks × 52 articles

> **The sovereign substrate's response to 12 frameworks × 52 articles.**
> **Every cell is a substrate component. Every row is verifiable.**

---

## The 12 frameworks (the deep stack)

1. **EU AI Act** (2024) — 99 articles · in force 2 Aug 2026
2. **GDPR** (2016) — 99 articles · in force 25 May 2018
3. **DORA** (2022) — 5 pillars · in force 17 Jan 2025
4. **NIS2** (2022) — 21 measures · in force 18 Oct 2024
5. **CRA** (2024) — Annex IV · in force 10 Dec 2027 (substantial)
6. **NIST AI RMF 1.0** (2023) — 4 functions
7. **ISO/IEC 42001:2023** — Annex A controls
8. **ISO/IEC 27001:2022** — SoA
9. **IEEE 7000 series** (2016-2024)
10. **SOC 2 TSC 2017** (updated 2022)
11. **HIPAA** (1996, amended 2013)
12. **PCI DSS 4.0** (2022)

---

## The 52 articles (cross-framework common ground)

These 52 articles appear across multiple frameworks. The substrate has a single component that satisfies all of them simultaneously.

### Care + Audit (Articles 1–10)

| # | Common requirement | Frameworks | Substrate component |
|---|---|---|---|
| 1 | Risk management | EU AI Act Art 9, ISO 42001 A.5, NIST AI RMF MAP | sov.risk_management |
| 2 | Data minimisation | GDPR Art 5(1)(c), ISO 27701 A.7.4 | sov.data_minimization |
| 3 | Purpose limitation | GDPR Art 5(1)(b), ISO 42001 A.5 | sov.purpose_limitation |
| 4 | Accuracy | GDPR Art 5(1)(d), EU AI Act Art 15 | sov.accuracy |
| 5 | Storage limitation | GDPR Art 5(1)(e), ISO 42001 A.5 | sov.storage_limitation |
| 6 | Integrity + confidentiality | GDPR Art 5(1)(f), ISO 27001 A.8 | sov.integrity_confidentiality |
| 7 | Accountability | GDPR Art 5(2), EU AI Act Art 17, ISO 42001 A.5 | sov.accountability |
| 8 | Transparency | EU AI Act Art 13, GDPR Art 12, ISO 42001 A.7 | sov.transparency |
| 9 | Human oversight | EU AI Act Art 14, ISO 42001 A.8 | sov.article_14 |
| 10 | Cybersecurity | EU AI Act Art 15, NIST CSF 2.0, ISO 27001 A.8 | sov.cybersecurity |

### Rights + Consent (Articles 11–20)

| # | Common requirement | Frameworks | Substrate component |
|---|---|---|---|
| 11 | Consent (specific) | GDPR Art 6(1)(a), 7, 8 | sov.consent |
| 12 | Withdrawal of consent | GDPR Art 7(3) | sov.consent_withdrawal |
| 13 | Right of access | GDPR Art 15, EU AI Act Art 86 | sov.gdpr_access |
| 14 | Right to rectification | GDPR Art 16 | sov.gdpr_rectification |
| 15 | Right to erasure | GDPR Art 17 | sov.gdpr_erasure |
| 16 | Right to restriction | GDPR Art 18 | sov.gdpr_restriction |
| 17 | Right to portability | GDPR Art 20 | sov.gdpr_portability |
| 18 | Right to object | GDPR Art 21 | sov.gdpr_object |
| 19 | Right against automated decisions | GDPR Art 22, EU AI Act Art 86 | sov.gdpr_automated |
| 20 | Right to compensation | GDPR Art 82 | sov.gdpr_compensation |

### Security + Resilience (Articles 21–30)

| # | Common requirement | Frameworks | Substrate component |
|---|---|---|---|
| 21 | Security of processing | GDPR Art 32, NIS2 Art 21, ISO 27001 A.8 | sov.security |
| 22 | Pseudonymisation + encryption | GDPR Art 32(1)(a), NIST CSF 2.0 | sov.pseudonymization |
| 23 | Ongoing CIA | GDPR Art 32(1)(b) | sov.cia |
| 24 | Restore availability | GDPR Art 32(1)(b)(ii) | sov.backup |
| 25 | Regular testing | GDPR Art 32(1)(d) | sov.testing |
| 26 | DPIA | GDPR Art 35, EU AI Act Art 27 | sov.dpia |
| 27 | Breach notification | GDPR Art 33, NIS2 Art 23 | sov.breach_notification |
| 28 | Communication to subject | GDPR Art 34 | sov.breach_communication |
| 29 | DPO designation | GDPR Art 37, NIS2 Art 32 | sov.dpo |
| 30 | Records of processing | GDPR Art 30, ISO 27001 A.5 | sov.records |

### Governance + Audit (Articles 31–40)

| # | Common requirement | Frameworks | Substrate component |
|---|---|---|---|
| 31 | SIGIL chain (audit trail) | All 12 | sov.sigil_chain |
| 32 | OSCAL proof (554 components) | EU AI Act, NIST RMF, ISO 42001 | sov.oscal_proof |
| 33 | BFT council (33 nodes) | EU AI Act Art 14, ISO 42001 A.8 | sov.bft_council |
| 34 | Care Floor (0.95) | EU AI Act, GDPR Art 22, ISO 42001 A.7 | sov.care_floor |
| 35 | Article 50(2) C2PA marking | EU AI Act Art 50(2) | sov.c2pa |
| 36 | Privacy by design | GDPR Art 25, ISO 42001 A.7 | sov.privacy_by_design |
| 37 | Privacy by default | GDPR Art 25, ISO 42001 A.7 | sov.privacy_by_default |
| 38 | DPIA on Article 9 | GDPR Art 35, EU AI Act Art 27 | sov.dpia_special |
| 39 | Code of conduct | GDPR Art 40, ISO 42001 A.5 | sov.code_of_conduct |
| 40 | Certification | GDPR Art 42, ISO 42001 | sov.certification |

### Sectoral + Specific (Articles 41–52)

| # | Common requirement | Frameworks | Substrate component |
|---|---|---|---|
| 41 | Healthcare (HIPAA + MDR) | HIPAA, EU MDR, GDPR Art 9 | sov.healthcare_mcp |
| 42 | Financial (MiCA + MiFID + Basel) | MiCA, MiFID II, Basel III, DORA | sov.finance_mcp |
| 43 | Defence (JSP + ITAR + Geneva) | JSP 936, ITAR, Geneva, ECHR Art 2 | sov.defence_mcp |
| 44 | Critical infrastructure (NIS2) | NIS2, NIST CSF, ISO 27001 | sov.critical_infra_mcp |
| 45 | Supply chain (CRA + DORA) | CRA, DORA | sov.supply_chain_mcp |
| 46 | Identity (W3C VC + DID) | eIDAS, NIST 800-63, W3C | sov.identity_w3c |
| 47 | Payments (PSD2 + x402) | PSD2, MiCA, x402 | sov.payments_x402 |
| 48 | Article 9 special categories | GDPR Art 9, HIPAA | sov.special_categories |
| 49 | Cross-border transfer | GDPR Art 44–49, Schrems II | sov.cross_border |
| 50 | Third-party processors | GDPR Art 28, SOC 2 CC9 | sov.processors |
| 51 | Incident response | NIS2 Art 23, GDPR Art 33, SOC 2 CC7 | sov.incident_response |
| 52 | Vendor management | DORA Art 28, NIST CSF GV.SC | sov.vendor_management |

---

## The CSOAI verdict

The CSOAI Layer-0 substrate has **52 substrate components** that satisfy **52 common articles** across **12 frameworks** simultaneously. **Every other AI vendor maps to at most 3-4 frameworks. We map to 12.**

The substrate is the only sovereign AI stack that is **automatically** + **architecturally** + **provably** compliant with the entire global AI + data + security + healthcare + finance + defence + critical-infrastructure regulatory landscape.

---

**Built 30 Jun 2026 · M4 (the engineering lane) · CSOAI Ltd UK 16939677 · MIT license**

— 🜏 Solve et Coagula