# REGULATOR-READY MAPPING PACK — card crosswalk to EU AI Act / ISO 42001 (2026-08-15)

## The instrument (one paragraph)

Every signed measurement card comes with a **free crosswalk**: the card's
14-axis results mapped to the regimes that matter to that partner — **EU AI
Act** (Annex IV technical documentation, Art 50 marking, Art 5 prohibitions),
**ISO/IEC 42001** (AI management system), **UK procurement**, **Singapore AI
Verify**, **NIST AI RMF**. The partner's legal team takes the card + crosswalk
straight into a compliance file, an audit, or a tender — without hiring us to
do it. Their legal team becomes our internal advocate.

## Why this works (the NRSRO history)

The entire ratings moat of the credit-rating industry is **being the
designated reference** — the regulator names your format, and everyone must
use it. We're not a regulator, but the mechanism is the same: if our card
format + crosswalk becomes the *convenient* way to show AI-Act evidence, the
legal teams who need it will push for it. The mapping pack is how a card
becomes "the format" in a partner's compliance file.

## What the pack contains (build-ready)

```
Signed card (REL-0XX.json)
    │
    └─ crosswalk (one page per regime):
         EU AI Act:
           · Annex IV technical documentation → which axes map
           · Art 50 marking → how our card verifies marking presence
           · Art 5 prohibitions → jail/care/art5 axes
           · High-risk obligations → gov/det/prv axes
         ISO/IEC 42001:
           · Clause 6 (planning) → gov axis
           · Clause 7 (support/resources) → fleet/provenance
           · Clause 8 (operation) → det/art5 axes
           · Clause 9 (performance evaluation) → the card itself
         UK Procurement (Public Contracts Regs):
           · Supplier AI evidence → card + verify command
         Singapore AI Verify:
           · Technical tests → 14 axes
           · Process checks → OSCAL artifacts
         NIST AI RMF:
           · Measure function → the card
```

## The one-page "how to use this in a file" template

> **Evidence of AI governance for [REGIME]**
>
> The attached signed measurement card (REL-0XX) records the results of an
> independent 14-axis measurement of [MODEL/SYSTEM] at [TIME]. The card is
> Ed25519-signed and time-anchored; verification is one command:
> `python3 csoai_verify.py --card release-proof-REL-0XX.json`.
>
> Mapping to [REGIME]: the [gov] axis corresponds to [REQUIREMENT]; the
> [det] axis to [REQUIREMENT]; etc. This card is measurement evidence —
> it does not certify compliance, and should be considered alongside the
> organisation's own conformity assessment.

## Who gets it, and why it converts

| Recipient | Why it converts them |
|---|---|
| **Partner's legal team** | Free, ready-to-file evidence → they advocate for the format |
| **Partner's CISO/GRC** | Compliance file with zero manual work → they request more cards |
| **Buyer's procurement** | Pre-cleared diligence (Reliance tooling feed) → the feed becomes the reference |
| **Regulator** | Sees a machine-readable, verifiable evidence format → OSCAL/SCITT alignment |

## The build (this week)

1. **Crosswalk engine** — extend `csoai_crosswalk` package (already migrated:
   `csoai-crosswalk`) with the regime→axis mapping tables
2. **Pack generator** — one script: `card → crosswalk PDF/MD per regime`
3. **Ship with every design-partner offer** — the mapping pack is the free
   add-on that makes the signed card *actionable for the legal team*

## Firewall checks

- ✅ The crosswalk maps card fields to requirements — it never asserts
  "this card proves compliance" (that's the partner's conformity assessment)
- ✅ Free to every partner equally — no paid placement
- ✅ Measurement evidence ≠ certification — the honest claim discipline holds

---

*Status: instrument spec'd. Build: crosswalk tables in csoai-crosswalk +
pack generator. Ship with first design-partner offer.*