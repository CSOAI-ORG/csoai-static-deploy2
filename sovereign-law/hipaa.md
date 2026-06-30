# HIPAA — Health Insurance Portability and Accountability Act (sovereign crosswalk)

> **Published 1996 · amended 2013 · 45 CFR Parts 160, 162, 164.**

## The 18 HIPAA identifiers (de-identification)

1. Names
2. Geographic subdivisions smaller than a state
3. Dates (except year) related to an individual
4. Telephone numbers
5. Fax numbers
6. Email addresses
7. Social security numbers
8. Medical record numbers
9. Health plan beneficiary numbers
10. Account numbers
11. Certificate / license numbers
12. Vehicle identifiers + serial numbers + license plate
13. Device identifiers + serial numbers
14. URLs
15. IP addresses
16. Biometric identifiers (finger + voice prints)
17. Full-face photographs
18. Any other unique identifying number, characteristic, or code

## The 3 safeguards (Security Rule)

| Type | Description | Sovereign component |
|---|---|---|
| **Administrative** | Policies + procedures + workforce training | sov.hipaa_admin + sov.training |
| **Physical** | Facility access controls + workstation use | sov.hipaa_physical + sov.physical_security |
| **Technical** | Access control + audit controls + integrity + transmission security | sov.hipaa_tech + sov.sigil_chain + sov.crypto |

## The 4 implementation specs (Privacy Rule)

| Spec | Subject | Sovereign component |
|---|---|---|
| Notice | Right to be informed | sov.hipaa_notice + sov.transparency |
| Access | Right to inspect + copy | sov.hipaa_access + sov.i_character_export |
| Amendment | Right to amend | sov.hipaa_amendment |
| Accounting | Right to accounting of disclosures | sov.hipaa_accounting + sov.audit_log |

## The CSOAI crosswalk

| HIPAA Citation | Substrate component |
|---|---|
| 45 CFR 164.308 (Admin safeguards) | sov.hipaa_admin |
| 45 CFR 164.310 (Physical safeguards) | sov.hipaa_physical |
| 45 CFR 164.312 (Technical safeguards) | sov.hipaa_tech + sov.sigil_chain |
| 45 CFR 164.316 (Documentation) | sov.hipaa_docs |
| 45 CFR 164.402 (Notification) | sov.hipaa_breach + sov.gdpr_breach |
| 45 CFR 164.412 (Law enforcement delay) | sov.hipaa_delay |
| 45 CFR 164.414 (Administrative requirements) | sov.hipaa_admin_req |
| 18 HIPAA identifiers | sov.hipaa_deidentify + sov.pseudonymization |
| Article 9 GDPR ↔ HIPAA | sov.gdpr_hipaa_bridge |

## Healthcare MCP coverage

The CSOAI substrate has 11 healthcare MCPs:
- hl7-fhir-bridge
- healthcare-ai-governance
- proofof-ai (for medical AI)
- care-membrane (Care Floor 0.95)
- SaMD classification (EU MDR + FDA)
- EU MDR bridge
- HIPAA safeguards
- WHO ICOPE (Integrated Care for Older People)
- Medical device
- Telemedicine
- Opticians (Templeman lineage)

---

**Built 30 Jun 2026 · M4 · CSOAI Ltd UK 16939677 · MIT**

— 🜏 Solve et Coagula