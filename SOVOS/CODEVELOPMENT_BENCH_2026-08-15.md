# CO-DEVELOPMENT BENCH — the thread→signed converter (2026-08-15)

## The instrument (one paragraph)

A partner contributes a **domain corpus** (their regulatory framework, their
use-case data, their evaluation questions). We build a **signed benchmark**
from it, run it across the 14-axis fleet, publish the result as a **joint
signed, DOI'd card with both names on it — forever**. Costs us measurement we
were running anyway. Gives the partner a citable, verifiable artifact with our
signature and their corpus.

## Why this is the strongest instrument in the estate

- **Thread → signed converter**: every partner relationship becomes a
  permanent, verifiable citation object — not a conversation
- **Costs nothing incremental**: the fleet runs continuously anyway; the
  corpus just becomes new probes
- **Both names, forever**: the DOI is the co-development proof — it survives
  staff changes, vendor changes, everything
- **Firewall-clean**: we sign the measurement; the partner's corpus is their
  IP; the joint artifact is the union

## The offer (one paragraph, reusable)

> "You bring a domain corpus — your regulatory framework, your use-case data,
> your evaluation questions. We build a signed benchmark from it, run it
> across our 14-axis fleet, and publish a joint card with both our names on a
> DOI that anyone can verify without asking either of us. The corpus becomes
> a citable, verifiable benchmark artifact — and your team gets an independent
> measurement of how models handle your domain."

## The flow

```
Partner corpus (framework/data/questions)
        │
        ▼
sovos-city scenario_bank + board banks (new probes from their corpus)
        │
        ▼
14-axis fleet run (A100/3090/K3/Oracle rotator)
        │
        ▼
signed cards (Ed25519 + OTS) + OSCAL assessment results
        │
        ▼
JOINT DOI (both names) → citable forever
```

## First-wave co-development targets

| Partner type | Corpus they bring | Joint artifact |
|---|---|---|
| **Standards body** (BSI ART/1, AI Verify) | Their framework/checklist | Signed benchmark of "does the fleet satisfy your criteria" — the mapping pack, co-authored |
| **Regulator** (ICO, DSIT) | Their guidance (Art 50, DPIA) | Signed benchmark of model compliance posture vs their guidance |
| **University** (HCI/AI-safety) | Their evaluation questions + human pool | Signed human-vs-AI benchmark, DOI'd with both labs |
| **AI vendor** (enterprise) | Their use-case corpus | Signed domain benchmark — "our models vs the standard" (they get the card; we get the citation) |
| **Cloud provider** (Azure/CF) | Their compliance framework | Signed benchmark of hosted-model governance |

## The Collison attestation (bonus instrument)

First signed measurement done **live, in the room, before leaving**:
during the first partner meeting, run one probe on the fleet, show the card
mint in real time, hand over the DOI. The partner has seen the mechanism
work — not a slide about it. (Named after the Collison brothers' demo-first
sales style.)

## Firewall checks

- ✅ Partner corpus = their IP; we only measure it
- ✅ Joint card = both names; we never claim their content
- ✅ We sign measurement, never "partner-approved"
- ⚠️ If a partner's corpus would leak another party's data → decline or
  require clearance (no PII, no confidential third-party data)

---

*Status: instrument spec'd. First pilot: pick one standards-body target
(BSI ART/1 or AI Verify) and offer the co-development bench alongside the
mapping pack.*