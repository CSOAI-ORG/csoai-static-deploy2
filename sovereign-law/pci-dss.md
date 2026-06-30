# PCI DSS 4.0 — Payment Card Industry Data Security Standard (sovereign crosswalk)

> **Published March 2022 · 12 requirements · PCI SSC.**

## The 12 requirements

| # | Requirement | Sovereign component |
|---|---|---|
| 1 | Install + maintain network security controls | sov.pci_req1 + sov.firewall |
| 2 | Apply secure configurations | sov.pci_req2 + sov.zero_trust |
| 3 | Protect stored account data | sov.pci_req3 + sov.crypto |
| 4 | Protect cardholder data with strong cryptography during transmission | sov.pci_req4 + sov.tls + sov.pqc |
| 5 | Protect all systems from malicious software | sov.pci_req5 + sov.antimalware |
| 6 | Develop + maintain secure systems + software | sov.pci_req6 + sov.sdlc |
| 7 | Restrict access to system components + cardholder data | sov.pci_req7 + sov.access_control |
| 8 | Identify users + authenticate access | sov.pci_req8 + sov.mfa |
| 9 | Restrict physical access | sov.pci_req9 + sov.physical_security |
| 10 | Log + monitor all access | sov.pci_req10 + sov.audit_log |
| 11 | Test security systems + processes regularly | sov.pci_req11 + sov.testing |
| 12 | Support information security with organisational policies | sov.pci_req12 + sov.policy |

## The 4 levels of PCI compliance

| Level | Applies to | Sovereign response |
|---|---|---|
| Level 1 | >6M transactions/year | Full Report on Compliance (ROC) by QSA |
| Level 2 | 1-6M transactions/year | Self-assessment + quarterly scans |
| Level 3 | 20K-1M transactions/year | Self-assessment |
| Level 4 | <20K transactions/year | Self-assessment |

The CSOAI substrate's x402 + MiCA + PSD2 protocol supports all 4 levels.

## The 6 test categories (4.0 new)

| # | Category | Sovereign component |
|---|---|---|
| 1 | Network security controls | sov.pci_test_1 |
| 2 | Vulnerability scanning | sov.pci_test_2 |
| 3 | Penetration testing | sov.pci_test_3 + sov.bft_red_team |
| 4 | Social engineering | sov.pci_test_4 |
| 5 | Internal vulnerability scans | sov.pci_test_5 |
| 6 | Segmentation testing | sov.pci_test_6 |

## The CSOAI crosswalk

| PCI DSS Requirement | Substrate component |
|---|---|
| Req 1 (Network security) | sov.firewall + sov.network_segmentation |
| Req 2 (Default credentials) | sov.zero_trust + sov.config_mgmt |
| Req 3 (Stored data) | sov.crypto + sov.tokenization |
| Req 4 (Encryption in transit) | sov.tls + sov.pqc + sov.mtls |
| Req 5 (Anti-malware) | sov.antimalware |
| Req 6 (Secure dev) | sov.sdlc + sov.secure_coding |
| Req 7 (RBAC) | sov.rbac + sov.zero_trust |
| Req 8 (Authentication) | sov.mfa + sov.biometric |
| Req 9 (Physical) | sov.physical_security |
| Req 10 (Logging) | sov.audit_log + sov.sigil_chain |
| Req 11 (Testing) | sov.pentesting + sov.red_team |
| Req 12 (Policy) | sov.security_policy |

## x402 + MiCA integration

The substrate's x402 protocol (HTTP 402 + on-chain + MiCA-compliant) is the natural payment layer for sovereign AI. PCI DSS 4.0 + MiCA + x402 = the sovereign payments stack.

---

**Built 30 Jun 2026 · M4 · CSOAI Ltd UK 16939677 · MIT**

— 🜏 Solve et Coagula