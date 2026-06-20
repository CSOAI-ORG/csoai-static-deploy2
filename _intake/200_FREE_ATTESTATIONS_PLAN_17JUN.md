# M50: 200 Free Keystone Attestations Plan — 17 June 2026

**Scope:** Batch-generation plan for 200 free keystone attestations across 20 industry verticals.

**Status:** Draft planning

---

## 1. Overview

| Metric | Value |
|--------|-------|
| Total attestations needed | **200** |
| Vertical count | **20** |
| Attestations per vertical | **10** |
| Serial rate (manual) | ~3/day = 67 days |
| **Batch approach** | Generate in parallel batches of 40–50 per run |
| Target completion | **4 July 2026 (launch-ready)** |

**Decision:** Manual serial generation at 3/day is impractical for launch. Use batch generation approach — generate all 200 attestations via the Hermes Agent keystone pipeline in parallel batches of 40–50 per run. Total: 4–5 batch runs.

### Batch Schedule

| Batch | Verticals | Certs | Est. Time |
|-------|-----------|:-----:|:----------:|
| Batch 1 | Healthcare, Finance, Legal, Govt | 40 | 2–3 hr |
| Batch 2 | Education, Retail, Manufacturing, Energy | 40 | 2–3 hr |
| Batch 3 | Telecom, Insurance, Real Estate, Gaming | 40 | 2–3 hr |
| Batch 4 | Transport, Pharma, Media, Defense | 40 | 2–3 hr |
| Batch 5 | Agriculture, Construction, Hospitality, Non-profit | 40 | 2–3 hr |

---

## 2. The 20 Verticals

| # | Vertical | Cert Prefix | Target Audience | Distribution Channel |
|:-:|----------|-------------|-----------------|---------------------|
| 1 | **Healthcare** | `HLTH-` | Hospitals, clinics, healthtech startups, NHS trusts | Lead magnet /nhs, direct outreach, compliance portals |
| 2 | **Finance** | `FIN-` | Banks, fintech, neobanks, asset managers | Lead magnet /monzo, banking compliance networks |
| 3 | **Legal** | `LEGL-` | Law firms, legaltech, bar associations | Legal compliance directories, law society newsletters |
| 4 | **Government** | `GOVT-` | Public sector, councils, agencies, EU institutions | Gov.uk / EU portal referrals, procurement lists |
| 5 | **Education** | `EDU-` | Universities, EdTech, training providers | Education compliance networks, EdTech forums |
| 6 | **Retail** | `RTL-` | E-commerce, omnichannel retailers, marketplaces | Retail compliance programmes, trade bodies |
| 7 | **Manufacturing** | `MFR-` | OEMs, supply chain, industrial automation | Industry 4.0 compliance, ISO networks |
| 8 | **Energy** | `ENR-` | Utilities, renewables, oil & gas, smart grid | Energy sector compliance, Smart Energy associations |
| 9 | **Telecom** | `TCOM-` | ISPs, mobile networks, satellite operators | GSMA compliance, telecom regulatory bodies |
| 10 | **Insurance** | `INS-` | Insurers, brokers, insurtech | Insurance compliance directories, actuarial bodies |
| 11 | **Real Estate** | `RE-` | Property platforms, agencies, PropTech | Property compliance portals, real estate associations |
| 12 | **Gaming** | `GAME-` | Game studios, publishers, esports, iGaming | Lead magnet /for-gaming, PEGI/ESRA networks |
| 13 | **Transport** | `TRANS-` | Logistics, ride-share, aviation, rail, shipping | Transport compliance, IATA/logistics bodies |
| 14 | **Pharma** | `PHAR-` | Pharmaceutical, biotech, clinical research | FDA/EMA compliance, pharma regulatory networks |
| 15 | **Media** | `MED-` | Publishers, broadcasters, streaming, social | Media compliance, press associations |
| 16 | **Defense** | `DEF-` | Defence contractors, cybersecurity, aerospace | Defence procurement, NATO/industry standards |
| 17 | **Agriculture** | `AGR-` | Agritech, farming, food supply chain | Agricultural compliance, DEFRA / EU CAP networks |
| 18 | **Construction** | `CON-` | Builders, contractors, engineering firms | Construction compliance, Build UK / CIOB |
| 19 | **Hospitality** | `HOSP-` | Hotels, restaurants, travel, events | Hospitality compliance, AA / VisitBritain |
| 20 | **Non-profit** | `NFP-` | Charities, NGOs, foundations, social enterprises | Charity compliance, NCVO / EU funding bodies |

---

## 3. Keystone Cert — JSON Structure Template

```json
{
  "$schema": "https://meok.ai/schemas/keystone-attestation-v1.json",
  "meok_version": "1.0.0",
  "attestation": {
    "id": "M50-{VERTICAL_PREFIX}-{NUM}",
    "type": "keystone-attestation",
    "category": "free-tier",
    "vertical": "{VERTICAL_NAME}",
    "vertical_prefix": "{PREFIX}",
    "issue_date": "{YYYY-MM-DD}",
    "expiry_date": "{YYYY-MM-DD + 1 year}",
    "status": "issued"
  },
  "subject": {
    "entity_type": "organization",
    "entity_name": "{TARGET_ENTITY_NAME}",
    "industry": "{VERTICAL_NAME}",
    "jurisdiction": "EU/UK",
    "ai_act_relevance": ["article-50", "transparency", "code-of-practice"]
  },
  "attestations": [
    {
      "article": "50.1",
      "statement": "Transparency obligation: AI system output is clearly marked as AI-generated.",
      "compliant": true,
      "evidence_required": true,
      "evidence_url": null
    },
    {
      "article": "50.2",
      "statement": "Deepfake disclosure: Any AI-generated or manipulated content is disclosed.",
      "compliant": true,
      "evidence_required": true,
      "evidence_url": null
    },
    {
      "article": "50.3",
      "statement": "Bot disclosure: AI system intended to interact with natural persons is disclosed.",
      "compliant": true,
      "evidence_required": true,
      "evidence_url": null
    },
    {
      "article": "50.4",
      "statement": "Code of Practice: Entity adheres to the EU AI Act Code of Practice provisions.",
      "compliant": true,
      "evidence_required": true,
      "evidence_url": null
    }
  ],
  "metadata": {
    "generator": "MEOK Attestation Engine v1",
    "generation_batch": "M50-BATCH-{BATCH_NUM}",
    "generation_date": "{YYYY-MM-DD}",
    "meok_free_tier": true,
    "honest_accounting": {
      "mrr_contribution": "£0 (free tier — no revenue attributed)",
      "note": "Free attestations are a marketing investment, not a revenue line."
    }
  },
  "signature": {
    "method": "hermes-agent-keystone",
    "signed_by": "MEOK Sovereign (SOV3)",
    "verification_url": "https://meok.ai/verify/{ATTESTATION_ID}"
  }
}
```

### Per-Vertical Fields to Vary

| Field | Variation |
|-------|-----------|
| `attestation.id` | `M50-{PREFIX}-{001..010}` |
| `subject.entity_name` | Rotate through 10 realistic org names per vertical |
| `subject.industry` | Vertical name |
| `metadata.generation_batch` | Batch number |
| `signature.verification_url` | Unique per cert |

---

## 4. Entity Name Generation (10 per Vertical)

Each vertical gets 10 realistic organisation names. Examples:

**Healthcare:** NHS South London, Barts Health AI, Genomics England, Babylon Health, Cera Care, Huma, DeepMind Health (alphabet), Kheiron Medical, Skin Analytics, Thriva

**Finance:** Monzo, Revolut, Starling Bank, Klarna, Wise, ClearBank, OakNorth, Tide, Atom Bank, Plum

**Legal:** Allen & Overy, Clifford Chance, Linklaters, Freshfields, Slaughter and May, Magic Circle AI, Lawhive, Robin AI, Legl, Juro

*(Full entity name lists to be expanded per vertical during batch generation.)*

---

## 5. Pipeline / Batch Generation Command

```bash
# Batch command template (Hermes Agent terminal):
python3 -m meok.attestation.batch \
  --vertical healthcare \
  --count 10 \
  --prefix HLTH- \
  --batch 1 \
  --output-dir ~/clawd/meok.ai/public/attestations/free/
```

Or via King/Queen:

```
king ask: "Generate batch 1 — Healthcare, Finance, Legal, Govt — 40 keystone attestations"
```

---

## 6. Distribution Channels (Operational Plan)

| Channel | Verticals Served | Launch Day? | Owner |
|---------|------------------|:-----------:|-------|
| Lead magnets (NHS, Monzo, Gaming) | Healthcare, Finance, Gaming | ✅ Yes | Sprint 2 |
| Public cert directory `/attestations/` | All 20 | ✅ Yes | Post-launch |
| Direct email outreach | Finance, Legal, Govt, Non-profit | ⏳ Day 2+ | TBD |
| Compliance portal partnerships | Healthcare, Education, Energy | ⏳ Week 2+ | TBD |
| LinkedIn / social | All | ⏳ Week 2+ | TBD |
| Industry body referrals | All | ⏳ Week 4+ | TBD |

---

## 7. Honest Accounting

| Item | Value |
|------|-------|
| Revenue from free attestations | **£0.00** |
| Attestations as marketing cost | **~£0 (automated generation)** |
| MRR impact of free tier | **£0 (no monetisation on free tier)** |
| Strategic purpose | Pipeline building, brand authority, trust signals |

---

*Prepared: 17 June 2026 · Sprint 4 DRAGON MODE · STOP_DEPLOY — staged only*
