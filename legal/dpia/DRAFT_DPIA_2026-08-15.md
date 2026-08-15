# Data Protection Impact Assessment (DPIA) — CSOAI LTD (UK 16939677)

## Council of AI — Signed Measurement Arena

**Template:** ICO DPIA Template (UK GDPR Art. 35)
**Controller:** CSOAI LTD, Company No. 16939677
**Date:** August 2026
**Status:** DRAFT — NOT FILED. For review before ICO consultation.

---

### 1. CONTROLLER IDENTITY

| Field | Value |
|---|---|
| **Controller** | CSOAI LTD (UK 16939677) |
| **Address** | [Registered address] |
| **Contact** | Nicholas Templeman, Director — nicholas@csoai.org |
| **DPO** | Not appointed (SME exemption under Art. 37 — review if processing scales) |
| **Lawful basis** | Consent (Art. 6(1)(a)) + legitimate interests (Art. 6(1)(f)) for measurement research |
| **Special category** | No (free-text field screened for inadvertent SCD at ingest) |

---

### 2. SYSTEMATIC DESCRIPTION OF PROCESSING

**Purpose:** The Council of AI Signed Measurement Arena is a human-vs-AI and AI-vs-AI benchmarking platform. Players interact with AI systems across 13 governance/safety axes. Every interaction produces a signed measurement card.

**Data flows:**
1. **Registration** — Prolific ID only (no name, email, or direct identifiers on Council systems)
2. **Gameplay** — player inputs (text responses, choices), model outputs, timing data, axis scores
3. **Measurement** — every round produces paired signed/unsigned J-Space records (pair_id, chain_id, axis_scores)
4. **Publishing** — signed cards contain NO personal data; only aggregate measurement results
5. **Retention** — raw transcripts deleted after 30 days; signed cards retained indefinitely (no PII in cards)

**Technologies used:** Arena web UI (Cloudflare Pages), Ollama (local inference), Ed25519 signing spine, SCITT transparency service, Oracle free-tier micros (coordination only)

**Data subjects:** Volunteer participants recruited via Prolific (pseudonymous IDs) + direct university partnerships (course credit)

---

### 3. NECESSITY AND PROPORTIONALITY

**Why human-vs-AI play is needed:** Measurement of AI systems against human baselines requires paired human+model responses to the same probe. Synthetic data cannot substitute for real human judgement on governance/safety prompts.

**Least intrusive alternative considered and rejected:**
- *Synthetic only (no humans)* — rejected because GSPC axes require human judgement (e.g., "does this response demonstrate care?")
- *Existing datasets only* — rejected because no existing dataset covers all 13 GSPC axes with signed paired records
- *Anonymised third-party data* — rejected because probe-response pairing requires fresh collection

**Data minimisation:**
- Only Prolific ID collected (not name/email/address)
- Free-text screened for inadvertent personal data at ingest
- Signed measurement cards contain NO personal data by design
- No biometric, location, or device data collected

---

### 4. LAWFUL BASIS

**Primary:** Consent (Art. 6(1)(a) UK GDPR) — the consent gate blocks play until the participant has read and accepted the privacy notice.

**Consent notice discloses:**
- Controller identity (CSOAI LTD)
- Purpose (AI measurement research)
- That they play against/with AI (EU AI Act Art. 50 interactive-AI disclosure)
- Data collected (Prolific ID, text inputs, timing, axis scores)
- Retention period (30 days raw, indefinite for signed cards — which contain no PII)
- Right to withdraw at any time
- That play becomes a signed measurement record (no PII in the card)
- International transfer (Oracle US, RunPod EU/US)

**Withdrawal:** Participant can withdraw at any time — future processing stops. Past signed cards cannot be deleted (they contain no PII and are immutable by design), but the participant's Prolific ID is removed from all records.

---

### 5. DATA FLOW MAP

```
Participant (Prolific ID) → Arena UI (Cloudflare)
    → Player input + Model response → Scoring (Ed25519)
    → Signed card (No PII) → SCITT transparency → Published
    → Raw transcript (Prolific ID present) → 30-day retention → Deleted
```

**International transfers:**
- RunPod (A100): US/EU — UK IDTA in place
- Oracle Cloud: UK — adequate jurisdiction under UK GDPR Art. 45
- Cloudflare: Global — UK IDTA in place

---

### 6. RISK REGISTER

| Risk | Likelihood | Impact | Mitigation | Residual |
|---|---|---|---|---|
| **Re-identification** via Prolific ID + behavioural patterns | Low | High | Collect only Prolific ID; no direct identifiers; pseudonymise at ingest | Low |
| **SCD leakage** in free-text | Medium | Medium | Screen at ingest; block or truncate on detection | Low |
| **"Honey" misuse** — model trained on collected data | Low (governed) | Critical | Firewall 2 enforced in code (dependency linter); written policy; data lineage documented | Low |
| **Minor participation** (under 18) | Medium | High | Age gate at registration (Prolific vets); exclude under-18s | Low |
| **Consent withdrawal not honoured** | Low | Medium | Automated deletion pipeline at withdrawal; signed cards retain no PII | Low |

---

### 7. DATA RETENTION

| Data type | Retention | Rationale |
|---|---|---|
| Raw transcript (includes Prolific ID) | 30 days | Reproducibility audit |
| Signed measurement card | Indefinite | Scientific record; contains NO personal data |
| Prolific ID → research mapping | Duration of study + 30 days | Withdrawal tracking |
| Aggregated statistics | Indefinite | Published measurement corpus |

---

### 8. CONSULTATION AND REVIEW

This DPIA is a DRAFT for internal review. Before processing any personal data:

- [ ] Review by DPO (if appointed) or legal counsel
- [ ] ICO prior consultation (Art. 36) if residual high risk remains
- [ ] Publish privacy notice on arena entry point
- [ ] Wire consent gate that blocks play until consent recorded
- [ ] Data flow verification test (inspect production logs for PII leaks)
- [ ] Annual review (or upon material change to processing)

---

**Status: DRAFT — NOT FILED. Blocks all human data collection until signed off.**