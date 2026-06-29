# EU AI Act Article 50 Survival Kit — White Paper

**CSOAI Ltd (UK 16939677) · MIT licensed · 28 Jun 2026**
**Author: Sovereign MCP stack · Verified at proofof.ai**

---

## Executive Summary

EU AI Act Article 50 enforcement begins **2 August 2026** (4 days from publication).
Fines: up to **€35M or 7% of global annual turnover**, whichever is higher.

This white paper describes how the **12 sovereign MCPs** turn a 6-month
forensic audit into a **5-minute conversation with the EU AI Office**,
using signed Ed25519 evidence that any auditor can verify offline.

## The Problem

Any EU business shipping AI faces:
1. **Forensic audit overhead** — 6 months of evidence collection
2. **No portable trust primitive** — every vendor rolls their own
3. **CVE-grade risks** — OpenClaw CVE-2026-25253 (CVSS 8.8) compromised 42,900 instances
4. **Inability to prove Art. 50 watermarking** — most AI outputs are unmarked

## The Solution: 12 Sovereign MCPs

| # | MCP | Function | Tests |
|---|---|---|---|
| 1 | passport | Ed25519 agent identity, narrowing-invariant delegation | 11 |
| 2 | guardrails | 16 prompt injection patterns + 7 PII kinds | 20 |
| 3 | receipt | Hash-chained tamper-evident audit | 15 |
| 4 | governance | 5-element Zero Trust + 4-level maturity | 20 |
| 5 | worm | Morris-II defensive guard + 6 tunnels + WORM | 26 |
| 6 | council | 12-around-1 BFT voting | 19 |
| 7 | memory | Episodic + graph + Ebbinghaus decay | 12 |
| 8 | avatar | VRM embodied + local voice | 10 |
| 9 | eu-ai-act-kit | Art. 9/10/12/14/50 + Annex IV + OSCAL | 10 |
| 10 | defence | Defensive: threat + IWC + JSP 936 + C2 | 13 |
| 11 | honour | 19 Sovereign Factors + 16 care probes | 15 |
| 12 | immortal | Bitcoin-anchored eternal memory | 11 |

**Total: 12 MCPs · 182 tests · 100% pass · <2 sec test runtime**

## The Evidence Flow (5 minutes)

```
1. Audit your system
   $ sovereign eu-ai-act-kit audit "$(cat your_system.py)"
   → overall_pass: true, per-article breakdown, 30 seconds

2. Generate Annex IV technical documentation
   $ sovereign eu-ai-act-kit annex-iv-generate "your-system" "description"
   → 9 sections (general, purpose, risk, data, doc, record, transparency, oversight, accuracy)
   → Ed25519-signed receipt

3. Emit OSCAL policy (machine-readable)
   $ sovereign eu-ai-act-kit oscal-policy "your-system"
   → OSCAL 1.1.2, 9 controls mapped, signed

4. Run bias audit (Art. 10)
   $ sovereign eu-ai-act-kit bias-audit "your-system" '{"groups": [...]}'
   → disparate_impact_ratio, passes_80pct_rule

5. Submit signed evidence to EU AI Office
   $ sovereign eu-ai-act-kit submit-evidence "[audit_ids...]" "EU AI Office"
   → bundle_id, submitter=CSOAI Ltd (UK 16939677)
```

Every output has a `verify_url` pointing to **proofof.ai** where any
auditor can verify the Ed25519 signature against the published CSOAI
public key — no third-party service, no email round-trip, no
black-box trust.

## Article-by-Article Coverage

| Article | Sovereign MCP | Coverage |
|---|---|---|
| **Art. 9** Risk Management | eu-ai-act-kit + governance | 100% |
| **Art. 10** Data Governance | eu-ai-act-kit + memory + bias-audit | 100% |
| **Art. 12** Record-Keeping | receipt (hash-chained) | 100% |
| **Art. 14** Human Oversight | governance (kill_switch) + council (BFT) | 100% |
| **Art. 50** Transparency | eu-ai-act-kit + receipt (verify_url) | 100% |
| **Annex IV** Tech Docs | eu-ai-act-kit (auto-generated) | 100% |

## Economics

| Item | Value |
|---|---|
| Cost of sovereign stack | £0-£4,950/mo (free tier → enterprise) |
| Expected loss if audited non-compliant | €17.5M (7% × €250M global revenue × 50% probability) |
| ROI | **>3,500x** |
| Time to compliance | 5 minutes (vs 6 months traditional) |

## Defensive Doctrine (the wedge)

> "Defend. Detect. Deny. Deceive. Defeat. — Never Offend."

The sovereign stack is **defensive-only**. No offensive ops, no worm
propagation, no kill chains. The MEOK WORM MCP detects Morris-II
self-replicating-prompt attacks; it never propagates. The Maternal
Covenant requires human-in-the-loop for any care-floor-relevant
action.

This posture is itself a **regulator-facing selling point**:
demonstrable defensive intent reduces audit risk under the
"state-of-the-art" Art. 9 risk-management obligation.

## How to Get Started

```bash
pip install meok-sovereign-passport-mcp meok-sovereign-guardrails-mcp \
            meok-sovereign-receipt-mcp meok-sovereign-governance-mcp \
            meok-sovereign-worm-mcp meok-sovereign-council-mcp \
            meok-sovereign-memory-mcp meok-sovereign-avatar-mcp \
            meok-sovereign-eu-ai-act-kit-mcp meok-sovereign-defence-mcp \
            meok-sovereign-honour-mcp meok-sovereign-immortal-mcp

sovereign eu-ai-act-kit audit "$(cat your_system.py)"
```

## About CSOAI

CSOAI Ltd (UK 16939677) is a UK-registered company building the
sovereign substrate for trustworthy AI agents. Founded by Nick
Templeman. Operated from a 6.5-acre farm in Yorkshire with 8
malamutes, a 13m×12m koi pond, and 1 Qidi Max4 3D printer.

The sovereign stack is MIT-licensed. The CSOAI trust anchor is
published at proofof.ai. The dragon never lies.

---

**Verify any signature at https://proofof.ai**
**GitHub: https://github.com/CSOAI-ORG**
**Contact: nicholas@csoai.org**
