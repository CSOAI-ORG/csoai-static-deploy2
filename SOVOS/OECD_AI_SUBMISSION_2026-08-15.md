# OECD.AI CATALOGUE SUBMISSION — draft (2026-08-15)

The **OECD.AI Catalogue of Tools & Metrics for Trustworthy AI** is a PRIME
procurement-diligence surface: open submission, free, individuals worldwide
eligible, and the OECD's disclaimer explicitly says tools "are not vetted or
endorsed by the OECD" — so inclusion confers **discoverability and citability
in policy discussion**, which is exactly the neutral citation we want.

Submit THREE separate entries (each links to the Zenodo concept DOI):

## Entry 1 — TOOL: "Council of AI — GSPC Signed Measurement Suite"

- **Name:** Council of AI — GSPC Signed Measurement Suite
- **Type:** Tool (measurement/testing)
- **Organisation:** CSOAI LTD (UK 16939677)
- **Short description:** "An independent 14-axis AI-measurement suite (13 GSPC
  axes + jail) that emits Ed25519-signed, time-anchored measurement cards.
  Every result is recomputable by any third party via a stdlib-only verifier.
  Measures governance, privacy, safety, care, MCP conformance, jail-break
  robustness, and 8 further axes — with Wilson 95% confidence intervals on
  every quotable cell (usable_n >= 30)."
- **URL:** https://github.com/CSAOI-ORG/csoai-static-deploy2
- **Related DOI:** 10.5281/zenodo.21914702 (concept)
- **Key characteristics:** Ed25519 signing, SCITT (RFC 9943) receipts, OSCAL
  1.2.1 assessment results, Inspect AI (UK AISI harness) binding, in-browser
  verification at csoai.org/releases.

## Entry 2 — METRIC: "C2PA credential durability across re-encode"

- **Name:** C2PA Credential Durability Metric (ProvBench)
- **Type:** Metric
- **Organisation:** CSOAI LTD (UK 16939677)
- **Short description:** "Measures whether a C2PA/Content Credentials manifest
  survives standard re-encoding transforms. Baseline finding: 18/105 assets
  (17.14%) survive with verifiable credentials intact across 7 real
  transforms, with COSE-ML-DSA-65 post-quantum binding. Published with the
  DOI and recomputable."
- **URL:** https://github.com/CSAOI-ORG/csoai-static-deploy2
- **Related DOI:** 10.5281/zenodo.21914702

## Entry 3 — USE CASE: "Signed measurement cards in AI procurement diligence"

- **Name:** Signed measurement cards as pre-cleared AI procurement diligence
- **Type:** Use case
- **Organisation:** CSOAI LTD (UK 16939677)
- **Short description:** "A buyer or regulator verifies a supplier's AI
  governance posture in under a minute: paste the signed card, run the
  stdlib-only verifier, confirm digest + signature. No manual audit, no
  vendor-supplied claims. Mirrors the BitSight×CFC cyber-underwriting feed
  model applied to AI safety/governance evidence."

## Submission mechanics

- Portal: https://oecd.ai/en/catalogue (Tools & Metrics)
- Standing catalogue accepts submissions continuously; the OECD secretariat
  vets for accuracy/objectivity, biannual review
- Eligibility: individuals worldwide, free
- Recheck the current open-submission window before submitting

## The citation that then flows

```
A regulator's footnote or buyer's diligence finds us via the OECD catalogue:
"Council of AI (2026). GSPC Signed Measurement Suite. OECD.AI Catalogue.
 Verified card: signature valid, digest recomputes, DOI 10.5281/zenodo.XXXX"
```

---

*Status: draft ready. Owner action: submit 3 entries (tool + metric + use
case) on oecd.ai/en/catalogue — after the Zenodo concept DOI is minted so
all entries anchor to it.*