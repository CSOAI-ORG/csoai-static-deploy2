# CSOAI — IP LOCKDOWN POLICY
**Effective**: 2026-07-30 · **Owner**: Nicholas Templeman  
**Scope**: All CSOAI intellectual property (35+ artefacts catalogued in IP_REGISTRATION_2026-07-30.md)

This is the **operational lockdown** of all CSOAI IP. It applies the
3-pillar trade-secret protection framework (marking + access + audit)
to every IP artefact, then layers in patent / copyright / trademark
specific protections.

---

## §1 The 3-pillar framework

### Pillar 1: Marking

Every IP artefact in the corpus is marked with a header/footer
indicating classification and ownership:

```
[TRADE SECRET — CSOAI IP]  [Copyright © 2026 Nicholas Templeman]
[Patent Pending — see IP_REGISTRATION_2026-07-30.md]
```

Markings appear on:
- All source code headers (`# [CSOAI IP] ...`)
- All whitepaper headers
- All decision ledger records
- All bench result JSON files
- All internal documents

### Pillar 2: Access control

| Tier | Who | What they can access |
|------|-----|----------------------|
| **Tier 1: Founder (sole)** | Nicholas Templeman | All CSOAI IP + private keys + escrow access |
| **Tier 2: Senior hires** | TBD Q4 2026 | Operational IP (bench code, deployment, customer data) but NOT private signing keys |
| **Tier 3: Contractors** | TBD | Scoped access to specific deliverables under NDA |
| **Tier 4: Public** | Anyone | Public surface (csoai.org, HuggingFace, Kaggle) only |

### Pillar 3: Audit trail

Every access to IP is logged with:
- Timestamp (Unix ms)
- Actor (Tier 1 / 2 / 3 / 4)
- Artefact ID
- Action (read / write / sign / export)
- IP address (where applicable)
- Signature (Ed25519 SIGIL chain)

The audit trail is **append-only** (Decision Ledger `decision_ledger.py`).

---

## §2 Patent-specific protections

### Before filing (Q3-W2, this week)

For each of the 4 provisional patents being filed:

1. **Document the invention** — every implementation detail
2. **Reduce to practice** — bench results, code, whitepaper
3. **Witness** — SIGIL chain root hash for the disclosure
4. **Mark as PATENT PENDING** in every public disclosure
5. **Maintain chain of custody** — git commit history is the legal record
6. **Train everyone with access** — "no public disclosure outside US without 12-month grace period"

### After filing (Q3-W2 → Q3 2027)

1. **Maintain the file wrapper** — USPTO EFS-Web record
2. **Respond to office actions** within deadlines (3 months each)
3. **Convert provisional → non-provisional** within 12 months
4. **PCT international filing** within 12 months
5. **Maintain trade secret status for non-public sub-inventions**

---

## §3 Copyright-specific protections

### Software (care_gate_v2.py, provbench.py, pqcbench.py, etc.)

1. **UK IPO copyright registration** — Q4 2026 (16 artefacts, £42.50 each)
2. **Source code headers** — every file starts with `[CSOAI IP] [Copyright © 2026]`
3. **Git commit history** — the legal record of authorship + date
4. **DMCA take-down process** — for any unauthorised use

### Whitepapers (DEFONEOS series, Series A whitepaper, IP valuation)

1. **UK IPO copyright registration** — Q4 2026
2. **Creative Commons licensing** — public-facing whitepapers are CC-BY-SA-NC
3. **Source files in repo** — `.md` + rendered PDF + signature

---

## §4 Trademark protections

### Trademarks to register

- **CSOAI** — primary brand (UK + US + EUIPO)
- **SovSpace** — product brand (UK + US + EUIPO)
- **DEFONEOS** — architecture brand (UK + US + EUIPO)
- **SOV3** — substrate brand (UK + US + EUIPO)
- **CLAN** — model family brand (UK + US + EUIPO)

### Filing schedule

| Trademark | UK IPO | USPTO | EUIPO | Total |
|-----------|--------|-------|-------|-------|
| CSOAI | £200 + £50/class | $250/class | €850 | ~$1,300 |
| SovSpace | £200 + £50/class | $250/class | €850 | ~$1,300 |
| DEFONEOS | £200 + £50/class | $250/class | €850 | ~$1,300 |
| SOV3 | £200 + £50/class | $250/class | €850 | ~$1,300 |
| CLAN | £200 + £50/class | $250/class | €850 | ~$1,300 |
| **Total** | | | | **~$6,500** |

### After filing

1. **Watch service** — USPTO TSDR monitors for similar marks
2. **Enforcement policy** — cease-and-desist letter for any infringement
3. **Domain name protection** — register csoai.{com,org,io}, sovspace.{com,org}

---

## §5 Trade secret protections

### What is a trade secret at CSOAI

- **Anti-Goodhart salted split** (`SPLIT_SALT`) — never published in raw form
- **FlywheelLeak guard parameters** — held internally
- **Negative-control selftest design** — internal design choices
- **Discrimination CI methodology** — methodology, not just result
- **Buyer pricing tiers** — internal pricing model
- **Hiring plans** — internal only

### How we maintain trade-secret status

1. **NDA template** (employee + contractor + investor + partner)
2. **Access control** — repo-level (Tier 1/2/3/4)
3. **Marking** — `[TRADE SECRET — CSOAI IP]` on every internal doc
4. **No public disclosure** — selective publication only
5. **Trade secret register** — log every disclosure (event + recipient)

### If a trade secret is disclosed

1. **Mark as disclosed** (in trade-secret register)
2. **Cease-and-desist** to recipient
3. **Litigation** — Defend Trade Secrets Act (US), Trade Secrets Regulations 2018 (UK)
4. **Update IP_REGISTRATION** — note the disclosure date for litigation record

---

## §6 Data security (operational lockdown)

### Secrets management

| Secret | Storage | Access |
|--------|---------|--------|
| **SIGIL Ed25519 private key** | Hardware-encrypted USB + cloud-encrypted backup | Tier 1 only |
| **SOV_GATEWAY_KEY** | `.env.ai-hub` (gitignored) | Tier 1 |
| **ML-DSA-65 signing key** | Hardware-encrypted USB | Tier 1 only |
| **GitHub deploy keys** | Repo settings (encrypted) | Tier 1 |
| **Cloudflare Workers keys** | Cloudflare dashboard (2FA) | Tier 1 |
| **Stripe / payment keys** | Cloudflare dashboard (2FA) | Tier 1 |
| **Hub manifest signing key** | Same as SIGIL | Tier 1 |

### Network security

- **HTTPS everywhere** — every public endpoint
- **TLS 1.3** — minimum protocol
- **CORS** — restricted to known origins
- **Rate limiting** — Cloudflare Workers level
- **DDoS protection** — Cloudflare

### Operational security

- **2FA everywhere** — phone or hardware key
- **Password manager** — 1Password (Tier 1)
- **No password reuse**
- **No public Slack / Discord** with sensitive info
- **Quarterly access review** — Tier 2/3/4 re-verified

---

## §7 Self-test on ourselves (5-bench battery)

Every CSOAI product must pass our own 5-bench battery before shipping:

| Bench | What it measures | Threshold | Current |
|-------|------------------|-----------|---------|
| **ProvBench** | C2PA-marking survival | 0/20 published | ✅ measured |
| **DefBench** | Care-floor 2-direction | 100% recall, <10% over-block | ✅ 100% / 0% |
| **PQCBench** | Chain readiness | 5/5 criteria | ⚠️ 1/5 (US failing subject) |
| **Flywheel selftest** | Anti-Goodhart | 9/9 | ✅ 9/9 |
| **Decision ledger** | Audit trail | Append-only, no tag drift | ✅ working |

**Honest finding**: CSOAI fails its own PQCBench (1/5) — the SIGIL chain
needs to be PQC-ready by 2035 per NIST IR 8547. This is published as
DR-0004 (corpus-watcher cron REFUTED) and the operational plan is in
place.

---

## §8 Incident response

### If IP is breached (infringement, leak, unauthorised use)

1. **Contain** — disable public access, revoke keys
2. **Investigate** — audit trail + SIGIL signatures
3. **Notify** — counterparty + counsel within 72h
4. **Litigation** — Defend Trade Secrets Act / UK Trade Secrets Regs 2018
5. **Document** — update IP_REGISTRATION + decision ledger

### If SIGIL signing key is compromised

1. **Rotate** — generate new key, re-sign all records
2. **Re-publish** — public surface with new key
3. **Audit** — check for any signatures signed by compromised key
4. **Notify** — investors + customers within 24h

### If founder is incapacitated

1. **Tier 2 + Tier 3 assume operational responsibility**
2. **SIGIL signing key escrow** — Tier 2 + Tier 3 can co-sign
3. **IP_REGISTRATION** — proves chain of custody
4. **Continued operations** — code is structural, not narrative

---

## §9 Quarterly IP review checklist

| Item | Frequency | Owner |
|------|-----------|-------|
| Audit tier 1/2/3/4 access | Quarterly | Founder |
| Review NDA compliance | Quarterly | Founder |
| Update IP_REGISTRATION | Monthly | Founder |
| Renew trademark watch service | Annual | Counsel |
| File new provisional patents | Per invention | Founder + counsel |
| Update trade-secret register | Monthly | Founder |
| Check public disclosure compliance | Per disclosure | Founder |
| SIGIL key rotation (if compromised) | As needed | Founder |

---

## §10 The single-line IP lockdown

**Mark everything. Restrict access to Tier 1/2/3. Audit every read. Sign every claim.**

---

## Provenance

This policy cross-validates against:
1. `IP_REGISTRATION_2026-07-30.md` — every artefact catalogued
2. `IP_VALUATION_4METHODS_2026-07-30.md` — every $ figure
3. `VALUATION_2026-07-30.md` — round anchoring
4. `WORLD_DOMINATION_ROADMAP_2026-07-30.md` — execution timeline

If a section here contradicts a corpus source, the section is wrong, not the source.