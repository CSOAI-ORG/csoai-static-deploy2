# CSOAI vs the field — rigorous feature matrix (revised, 2026-06-26)

Re-doing this properly. My prior "sharpened insight" (everything but legacy is commoditized) was an **overcorrection**. The truth is more favourable and more precise: the competitors commoditized the **security plumbing**, NOT the **compliance content** or the **legacy layer**. Here's the honest, feature-by-feature read.

## The key distinction I'd blurred
There are **two different layers** people lump together:
- **Layer A — runtime security plumbing:** agent identity, signing, MCP gateway, policy-at-the-wire, audit log. *(Microsoft toolkit, ServiceNow, Runlayer live here.)*
- **Layer B — regulatory compliance content + legacy reach:** the actual EU AI Act/DORA/HIPAA *articles*, framework crosswalks, **legacy-system bridges**, machine-readable signed compliance artifacts (OSCAL). *(This is where CSOAI lives.)*

Microsoft open-sourcing Layer-A plumbing (MIT, April) does **not** commoditize Layer B. They're complementary — CSOAI could even *run on* Microsoft's identity/gateway and add the compliance + legacy layer on top.

## The matrix
| Capability | MS Agent Gov Toolkit | ServiceNow AI Control Tower | Runlayer ($30M) | Vanta/Credo | **CSOAI** |
|---|---|---|---|---|---|
| Per-agent identity / Ed25519 | ✅ (DIDs) | ✅ | ✅ | — | ✅ |
| MCP gateway / policy-at-wire | ✅ | ✅ | ✅ | — | ✅ |
| Runtime audit log | ✅ | ✅ | ✅ | partial | ✅ (SIGIL hash-chain) |
| Kill-switch | partial | ✅ | ✅ | — | ✅ (orchestrator) |
| **Legacy-system bridges (COBOL/SAP/SCADA/HL7)** | ❌ | ❌ | ❌ | ❌ | **✅ 22 — category of one** |
| **Article-level reg content (EU AI Act/DORA/HIPAA…)** | ❌ (security policy, not law) | partial (GRC) | ❌ | ✅ (assessment) | **✅ 28 reg MCPs + 410-article EU AI Act MCP** |
| **Machine-readable signed compliance artifacts (OSCAL/FedRAMP)** | ❌ | ❌ | ❌ | ❌ | **✅** |
| BFT multi-agent council | ❌ (single-agent policy) | ❌ | ❌ | ❌ | **✅** |
| Sovereign / on-device | ❌ (cloud/SaaS) | ❌ | ❌ | ❌ | **✅** |
| Price / openness | free (MIT) | enterprise $$$ | SaaS | SaaS $$ | open core |
| Funding / logos | Microsoft | incumbent | $30M + F500 | unicorn-ish | pre-seed, 0 logos |

## What this actually means (the honest, revised read)
- **CSOAI is NOT primarily an agent-security tool** (that layer is now free/funded/incumbent — competing there is a loser). **CSOAI is a regulatory-compliance + legacy-governance layer** — and on *those* rows, the competitors are blank.
- **The moat is wider than "just legacy"** (my overcorrection): it's **legacy bridges + article-level compliance content + signed compliance artifacts + BFT + sovereign**. Four of those five rows are ❌ across every competitor.
- **The plumbing rows (identity/gateway/audit) are table-stakes** — keep them as "yes, we have it / we can sit on Microsoft's free toolkit," never as the pitch.

## Why it's not a "sudden blocker" (Nick's point — correct)
Microsoft's toolkit (April) and ServiceNow (May) have been in-market; they don't *block* CSOAI because they occupy **Layer A**, and CSOAI's value + deadline-driven sale is **Layer B**. Nothing changed structurally — the research just made it precise. If anything, MS commoditizing Layer-A plumbing is **good for CSOAI**: the boring security layer is now free, so the buyer's remaining (unmet, regulated, deadline-bound) need is exactly Layer B = ours.

## Revised positioning (supersedes the over-pessimistic "legacy only")
**"The compliance layer for AI on legacy systems."** We don't sell agent security (free now). We sell: *your COBOL/HL7/SCADA AI, mapped to the actual regulations (EU AI Act articles, DORA, HIPAA), with machine-readable signed compliance artifacts, before Aug 2026.* The plumbing can even be Microsoft's — the **compliance + legacy reach is ours alone.**

## Honest correction log
- ❌ Earlier (today): "MS commoditized signing → moat narrows to legacy only." **Overcorrection.**
- ✅ Correct: MS commoditized *Layer-A plumbing*; CSOAI's moat is *Layer B* (legacy + reg-content + signed artifacts + BFT + sovereign) — broader + more defensible than "legacy only," and complementary to (not beaten by) the free toolkit.
