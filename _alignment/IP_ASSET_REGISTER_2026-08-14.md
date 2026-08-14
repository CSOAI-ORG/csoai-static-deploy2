# CSOAI IP ASSET REGISTER & DISCLOSURE INVENTORY
**Generated**: 2026-08-14 · **Owner**: Nicholas Templeman / CSOAI Ltd (UK 16939677)
**Purpose**: The investor/counsel-grade inventory (IP Plan §H). One row per asset: what it
is, when first public-disclosed, jurisdiction, ownership, protectability, commercial value,
and the dated proof that backs it. This is the shared input for a valuer, a counsel call,
and an investor. It upgrades — does not replace — `IP_REGISTRATION_2026-07-30.md` (the
technical ledger with per-artefact SIGIL witnesses).

---

## §0 Register discipline (read first)
Every claim is tagged **REAL / DEMO / THEORY / GATED**. Protectability assumes UK/EU
**absolute novelty** (no grace period — public disclosure anywhere defeats patenting)
and the **US 1-year grace** (35 USC 102(b)(1)) for the US-only window. Nothing in this
register is legal advice; handoff dates/URLs to counsel for verification.

**Three honest axioms from the legal analysis:**
1. **Disclosed inventions are largely unpatentable in UK/EU** (hundreds of public
   GitHub/PyPI repos, Zenodo DOI, pending arXiv). Not reversible.
2. **Your real portfolio = trade secrets (never published) + trademarks + copyright +
   database right + defensive prior art.**
3. **One US window remains** for anything first disclosed <12 months ago → US-first
   provisional, **counsel-gated**, collides with the ~27 Aug 2026 arXiv clock.

---

## §1 TRADE SECRETS (primary, protectable, never published) — REAL

| # | Asset | What it is | Created | First disclosure | Juris. | Ownership | Protection | Protectability | Commercial | Proof |
|---|-------|-----------|---------|------------------|--------|-----------|------------|----------------|-----------|-------|
| TS-01 | **49 GB organic data corpus** | 198 sources / 30 live feeds, 16+ datasets (Land Registry, Companies House, OS Names, DfT, EA, HSE, Met Office, FSA, NHS) | ongoing | **UNDISCLOSED** | UK/EU | CSOAI Ltd | trade secret — needs OTS timestamp + access log | **Strong** (sui generis DB right + TS if controls) | Core moat | pending OTS |
| TS-02 | **Unpublished axis definitions + calibration data** | GSPC axis internals, cal weights, scoring internals | 2026-06/07 | **UNDISCLOSED** | UK/EU/US | sole → CSOAI | trade secret | Strong | Core | OTS to-mint |
| TS-03 | **Anti-Goodhart internals** (SPLIT_SALT, FlywheelLeak guard, negative-control selftests) | IP-AG-001..003 | 2026-07-01 | **UNDISCLOSED** (salt public as stability mechanism per 2 Aug note) | UK/EU/US | sole → CSOAI | trade secret | Strong | Core differentiator | IP-DL |

> **Note (register-relevant):** The split salt `csoai-flywheel-v1` is deliberately PUBLIC
> (stability, not secrecy) per the 2026-08-02 ruling. Anti-Goodhart *mechanism* stays
> secret; the salt is not the secret.

## §2 COPYRIGHT (automatic, UK; optional US eCO) — REAL

| # | Asset | What it is | Created | First disclosure | Ownership | Protection | Protectability | Commercial | Proof |
|---|-------|-----------|---------|------------------|-----------|------------|----------------|-----------|-------|
| CP-01 | **GSPC measurement spine** (measure API, correctness gate, Ed25519 sign, COSE wrap) | 11/11 wires verified pod-side | 2026-07/08 | public repos | CSOAI | automatic; eCO optional | Strong | Core | git + verifier |
| CP-02 | **GovBench grader** (`system_analysis.py` IP-GOV-001) | 15-dim grader | 2026-06-15 | git commit | sole→CSOAI | automatic | Strong | Core | IP reg |
| CP-03 | **care/def/prov/pqc benches** (IP-SAF/PROV/CON) | harnesses + canonical bounds | 2026-07 | git commit | sole→CSOAI | automatic | Strong | Core | IP reg |
| CP-04 | **Whitepapers (8)** (IP-WP-001..008) | DEFONEOS arch, governance, security, Series A, valuation | 2026-06/07 | Zenodo + repos | sole→CSOAI | automatic | Strong (disclosed) | High | DOI |
| CP-05 | **Agent-economy Go-Machine** + catapult docs | distribution/strategy | 2026-08-14 | (attached, in-repo) | sole→CSOAI | automatic | Medium | High | git |

## §3 TRADEMARKS — **ACTION REQUIRED (DIY today)** — GATED-by-decision

| # | Mark | Intended classes | Status | Action | Risk |
|---|------|------------------|--------|--------|------|
| TM-01 | **"Council of AI"** | 9, 42 (+35/45 consider) | **US CLEARED 2026-08-14** (no exact mark; AI COUNCIL variants in cl.41 only) | Clear UK/EU + file UK £205+£60/class | watch descriptiveness disclaimer |
| TM-02 | **"MEOK"** | 9, 42 | **US CLEARED 2026-08-14** (no MEOK in cl.9/42; only cl.006 China + cl.043 dead) | Clear UK/EU + file | low |
| TM-03 | **"SOVOS"** | — | **ABANDON (confirmed conflict — Sovos Compliance LLC live US regs in 42+9)** | **retire from ALL external surfaces** | direct conflict — do NOT file |
| TM-04 | "DEFONEOS" | 9,42 | per prior dossier | file once cleared | — |

> **Clearance checkboxes (Step 2):** UK IPO search · EUIPO TMview · USPTO tmsearch —
> identical + visual/phonetic variants, Classes 9/42/35/45. UK IPO does NOT search relative
> grounds — self-search is YOUR responsibility.

> **USPTO CLEARANCE RUN 2026-08-14 (tmsearch.uspto.gov, live register) — findings:**
> - **SOVOS — CONFIRMED LIVE CONFLICT.** Serial **97035423**, wordmark "SOVOS",
>   status LIVE/REGISTERED, Classes **009, 035, 042**, owner **Sovos Compliance, LLC
>   (Delaware, USA)**. Direct hit in Classes 42 + 9 — the classes we need. Retire "SOVOS"
>   from all external surfaces (matches IP plan finding #2). DO NOT file.
> - **"Council of AI" — NO exact mark registered** in US. Only "X AI COUNCIL" variants
>   (Massachusetts/Ohio/Virginia AI Council, Class 041, owner Randolph Kennedy, LIVEPENDING).
>   Exact "COUNCIL OF AI" appears clear in US — but consult on descriptiveness/disclaimer
>   ("Council"+descriptive could draw a §2(e) descriptiveness or disclaimer office action).
> - **MEOK — clear in relevant classes.** Live MEOK marks are Class 006 (metal statuettes,
>   Sanjun Zhu/China) and Class 043 (restaurants, DEAD/abandoned). **No competing US MEOK in
>   Class 9/42.** Filable.

## §4 DATABASE RIGHT (49 GB corpus) — REAL, automatic, no registration

- **Right:** UK/EU sui generis database right, automatic, 15 years (new substantial
  investment restarts term). Prevents extraction/re-utilisation of a substantial part.
- **Threshold:** must show **substantial investment in obtaining/verifying/presenting**
  (NOT in *creating*) the data — CJEU British Horseracing Board distinguishes this.
- **What to assemble (Step 4):** sources list (198), feeds (30), collection playbooks,
  QA/verification checklists, version logs, vendor invoices, person-hours. This paper-trail
  is what proves the right.

## §5 POTENTIAL PATENT — the ONE counsel-gated US window — GATED (counsel, ~27 Aug clock)

Per IP Plan §E + prior dossier: **do NOT self-file; engage a patent attorney with the dated
inventory + arXiv draft BEFORE the arXiv deadline.** Candidate inventions first disclosed
<12 months ago (capturable US-only via provisional, $65 micro / $130 small / $325 large):

| # | Candidate invention | First disclosure | In US 12-mo window? | Fee path |
|---|--------------------|------------------|---------------------|----------|
| PP-01 | ProvBench 0/20 measurement | ~2026-07-29 | ✅ if <12mo | US provisional $130 small |
| PP-02 | Salted HELD_OUT split + FlywheelLeak guard | 2026-07-01 | ✅ | US provisional |
| PP-03 | COSE ML-DSA-65 chain measurement | 2026-07-30 | ✅ | US provisional |
| PP-04 | 4-method × 4-axis valuation method | 2026-07-30 | ✅ | US provisional |

> **Warning:** the arXiv paper (~27 Aug 2026) newly discloses material → starts/extends
> its own 12-mo US clocks. Any invention you decide NOT to patent after counsel → pivot to
> **defensive publication** (TDCommons/Zenodo/IP.com) to lock prior-art blocking value.

## §6 DEFENSIVE PRIOR ART (already live — free value) — REAL

| Asset | Dated proof | Function |
|-------|-------------|----------|
| Zenodo DOI | minted (citable, archived, dated) | blocks third-party patents on disclosed work |
| OpenTimestamps sigils | Bitcoin-anchored `.ots` proofs | dated proof-of-existence/creation |
| Public GitHub/PyPI | 100+ CSOAI-ORG repos indexed | prior art for competitors |
| **arXiv (pending ~27 Aug)** | preprint timestamp | scholarly prior art + visibility |

> **Do NOT defensively-publish new candidate inventions until the counsel US-provisional
> decision (caution from plan §C).**

---

## §7 What's UNPROTECTABLE (honest — burns no money)
Under absolute novelty, all publicly-disclosed inventions are unpatentable UK/EU. The
corpus *contents* (pre-existing public data like Land Registry) are not ownable as
copyright, but the **collected/verified/presented database** is (DB right) and the
unpublished **processing pipeline / axes / weights** are trade secrets. Do not spend on
patents for disclosed matter.

---

## §8 Open follow-ups from THIS register
- [ ] **TS-01/TS-02**: mint OpenTimestamps proofs for corpus + unpublished axis docs
  (Step 3) — `.ots` file stored beside originals. **Done 2026-08-14 for 5 crown jewels**
  (`_ip/ots/`); extend to full corpus versions + axis docs.
- [x] **TM-01/02/03**: USPTO clearance RUN complete 2026-08-14 — SOVOS confirmed conflict
  (retire), Council of AI + MEOK clear in 9/42 (see §3 findings). **Todo:** UK IPO + EUIPO
  TMview sweeps remain + UK filing (£205/1st class + £60/extra from 1 Apr 2026 — **UNVERIFIED
  on web, quoting plan**).
- [ ] **DB-01**: assemble the "substantial investment" evidence pack for the corpus (Step 4).
- [ ] **Trade-secret program**: live (`TRADE_SECRET_PROGRAM_2026-08-14.md` on disk — blocked
  from git by global `*_secret*` rule, intentionally); NDA + contractor assignment templates
  committed (`LEGAL_TEMPLATES_2026-08-14.md`).
- [ ] **PP-01..04**: package candidate inventions + dates + arXiv draft for counsel (Stage 2).
- [ ] **Valuation (Stage 4, when raising)**: IVS-compliant cost-approach by a recognised firm
  (Inngot/EverEdge/Metis/Stout/Kroll); supply THIS register + R&D cost + corpus
  cost-to-recreate. Reject instant-calculator outputs for investor use.

## §9 Verification status (honesty ledger — what's confirmed vs cited)
| Fact | Status 2026-08-14 |
|------|-------------------|
| SOVOS live US conflict (Sovos Compliance, cl.9/35/42) | ✅ **VERIFIED** via live USPTO tmsearch |
| Council of AI / MEOK clear in US 9/42 | ✅ **VERIFIED** via USPTO tmsearch |
| Uk IPO fee £205/£60 from 1 Apr 2026 | ⚠️ UNVERIFIED (web down) — cite plan |
| WIPO PROOF discontinued 2022-01-31 | ⚠️ UNVERIFIED (web down) — cite plan |
| GSPC MCP endpoint live + healthy | ✅ VERIFIED (probe 2026-08-14) |
| Dated OTS proof-of-existence minted | ✅ VERIFIED (5 stamps, calendar_commit) |
| FTO/prior-art patent landscape | 🔄 **DELEGATED** — subagent running; results pending |

---
*Layout intentionally matches IP Plan §H columns so a valuer/counsel/investor can consume
it without translation. Proof links: `IP_REGISTRATION_2026-07-30.md` (technical ledger),
`IP_NOTICE.md`, `.well-known/agent-card.json` (signed identity), did:web `csoai.org#keys-1`.*
