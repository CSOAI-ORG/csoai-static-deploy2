# COUNCIL OF AI — OPERATING PLAYBOOK
### How a measurement body actually runs: oversight bodies × market infrastructure × startup discipline (2026-08-15)

**Status line:** estate verified tonight — monorepo 55/55 live on GitHub (K3-checked), 14 axes measured, releases page + stdlib verifier live, honey 100% signed (2,693 rows), 3 DOIs, packages on PyPI/npm/MCP-registry. This playbook is the OPERATIONS layer: how the institution runs, not what it builds.

---

## Part 0 — Tonight's receipts (register)

| Claim | Check | Verdict |
|-------|-------|---------|
| Monorepo 55/55 on GitHub (040da97) | api.github.com: `CSOAI-ORG/councilof-ai-monorepo`, pushed 2026-08-15T08:07Z | REAL |
| releases.html + csoai_verify.py live | pages.dev mirror 200; **csoai.org/releases = 522 — stale A record still unfixed** | REAL, with owner gate now CRITICAL |
| 14 axes / honey 2,693 / 105 tests / DPIA draft / IETF draft | Lane-reported | LANE-REAL |
| Distribution Kit (Compass) | Absorbed: Zenodo concept-DOI anchor; OECD.AI + DSIT Portfolio = prime diligence surfaces; **OSF phase-out (read-only 19 Feb 2027)**; TechRxiv closed; arXiv endorsement hardened 21 Jan 2026 (personal endorsement now mandatory) | REAL |

**Distribution doctrine (locked from the Kit):** anchor = ONE Zenodo concept DOI; mirrors everywhere point back; archives first, press never before external recompute; one artifact = one genuine record; verifiability is the distribution.

---

## Part 1 — Measurement-body operations (FAA · UL · NRSRO · 17025 · FDA · Lloyd's)

Seven bodies dissected by lane A, mechanisms extracted. Each row: the mechanism, why it works, and the Council-of-AI adaptation.

### FAA — delegated authority + confidential reporting + continued airworthiness

| FAA mechanism | Working detail | CoAI adaptation |
|---|---|---|
| **Designee/ODA system** (14 CFR Part 183) | FAA can't certify everything → delegates to vetted individuals (DER/DAR) and **organizations** (ODA). ODA = FAA-approved procedures manual, prescreened "unit members," signed exec MOU, dedicated FAA oversight team; 2-yr grants renewable to 5; annual assessment + on-site inspection every 2 years. Order 8100.15C (Oct 2025) shifts oversight from thousands of individuals to fewer organizations — **regulate systems, not people** | Founding-attestor program structured as a *delegated measurement* scheme: approved attestation orgs get a signed procedures manual, a scoped grant, an annual review, and revocation. Scope-bounded grants, not blanket endorsement |
| **ASRS — confidential incident reporting with limited immunity** | Deliberately run by **NASA, not FAA**: FAA funds, NASA de-identifies, FAA never sees identities. Immunity if inadvertent, non-criminal, no accident, filed within **10 days**. ~2,900 reports/month for decades; punitive channels provably suppress data | The honey/refusals pipeline already rhymes with this. Add: a **confidential measurement-error intake** where a measured org can self-report a card error within N days and get correction (not revocation) — third-party-custody the intake if volume ever justifies it |
| **Continued operational safety → Airworthiness Directives** | Certificate holders have an *affirmative duty* to report failures (21.3); Service Difficulty Reports centralize; Corrective Action Review Board triages; ADs are legally enforceable, non-compliance grounds the aircraft | Measurement is never one-shot: re-attestation duty sits on the *card holder*; anomaly reports feed a triage board; **revocation/correction notices are the AD equivalent — machine-readable and public** |

### UL Solutions — the mark is licensed, never granted

| UL mechanism | Working detail | CoAI adaptation |
|---|---|---|
| **Follow-Up Services** | UL's S-1: **ongoing certification ≈ 33% of revenue vs 26% for initial testing** — the surveillance annuity exceeds the assessment. The mark is a licensed trademark, revocable by contract | The business model is *continued verification*, not one-off scores. Re-attestation subscriptions are the annuity; revocation is the enforcement lever |
| **Unannounced inspections + Initial Production Inspection** | Field engineers get "unannounced and immediate access"; random production-line sampling; nothing ships marked until an IPI confirms production matches the certified configuration | Spot re-measurement without notice: re-run a probe subset against a card-holding model at random intervals; a card is only issuable after the measured artifact is confirmed identical to what ships (hash-pin) |
| **Variation Notice graduated enforcement** | Documented VN → corrective action → escalation → appeal channel → mark removal on standards-change non-response | Graduated anomaly ladder (see Part 2 circuit-breaker row) with a published appeal path |

### NRSRO (credit rating agencies) — the closest regulatory cousin

| NRSRO mechanism | Working detail | CoAI adaptation |
|---|---|---|
| **Form NRSRO radical disclosure** | Annual certification within 90 days; **prompt update** on any material inaccuracy; full registration file + Exhibits **public and free on the agency's own website** | Annual "state of the measurement body" filing on our own site: methods, conflicts, funding, error statistics. Update-on-inaccuracy as a norm, not a legal duty |
| **Ratings by committee, not analyst** | S&P: vote of a Rating Committee, chairperson attests constitution + conflict-freedom; Fitch: consensus, dissent triggers mandatory internal appeal with a **new committee** (≥2 new members) within ~2 business days; minutes kept for regulators | Multi-model/multi-run measurement already diffuses single-run capture. For high-stakes cards: a **measurement committee rule** — card issues only when ≥2 independent scorer configurations concur; dissent = automatic re-run with fresh config |
| **Exhibit 1 performance accountability** | Agencies must publish **transition-and-default matrices** — the audited track record of their own accuracy, annually | Publish **card-performance statistics**: revocation rate, correction rate, dispute outcomes, drift between card claims and re-measurement. Self-published error stats = the credibility moat (this is the BMR/IOSCO discipline too — Part 2) |
| **Bounded appeal** | Issuer pre-notified (fact-check window, MNPI only); appeal only on material new information; delay-tactic appeals rejected; no editorial control surrendered | Dispute process: measured org gets a fact-check window pre-publication; appeal only on new evidence or material misinterpretation; decision final; card on "watch" status during appeal |
| **17g-5 conflict engineering** | Conflicts *regulated, not eliminated*: analysts barred from fee negotiation; compliance officer barred from analytical work; structured-finance disclosure enables unsolicited counter-ratings as a check on ratings-shopping | Already locked as firewall doctrine: no referral fees tied to ratings, no paid placement, no rating-for-listing. Structural separation: whoever sells re-attestation subscriptions never sets thresholds |

### ISO/IEC 17025 + NVLAP/UKAS — scope-bounded competence

| 17025 mechanism | Working detail | CoAI adaptation |
|---|---|---|
| **Scope-of-accreditation schedule** | Accreditation attests competence for *exactly listed methods/ranges*; work outside scope cannot be represented as accredited — **the anti-credential-inflation mechanism** | Every card carries an explicit scope block: which axes, which probes, which model version, which date range. Anything outside scope is unmeasured, full stop. (Already true of card schema — enforce it in the verifier) |
| **Proficiency testing / interlaboratory comparison** | §7.7.2: validity monitored "by comparison with results of other laboratories"; **unsatisfactory PT or non-participation → suspension** for those methods; PT providers themselves graded under ISO/IEC 17043 — *the graders are graded* | Cross-check our measurements against external evals (Inspect, HELM, published leaderboards) on overlapping models and **publish the deltas** (Delta Note #2 is exactly this). Non-convergence on an axis → suspend that axis's cards until root-caused |
| **Technical assessors, not generalist auditors** | Assessment teams pair a lead assessor with discipline-specific technical assessors; assessors observe methods actually being run, review uncertainty budgets and traceability chains | When design partners arrive, audits of *their* usage require axis-literate reviewers, not checklist auditors |

### FDA — lifecycle authority

| FDA mechanism | Working detail | CoAI adaptation |
|---|---|---|
| **Risk-tiered review** | Class I/II/III with evidence burden scaling with risk; De Novo for novel low/moderate | Card tiers by deployment risk: a chatbot card ≠ an agentic-payments card. Evidence depth (probe count, rep count, judge config) scales with claimed-risk tier |
| **MAUDE public adverse-event DB** | Mandatory manufacturer/user-facility reporting into a public database since 1996; underreporting acknowledged openly | Public **measurement-event feed**: corrections, revocations, anomalies — the reputational-enforcement engine costs nothing to run |
| **Section 522 orderable post-market surveillance** | FDA can *order* a surveillance study post-clearance on defined triggers; plan due 30 days; results public | Reserve the contractual right (in the mark licence) to require re-measurement on trigger events: weights update, license change, incident report |
| **Recall classification** | Class I/II/III by hazard probability; data shows pathway rigor correlates with downstream safety (510(k) ~11.6% recall vs 2.3% PMA) | Revocation classes by severity; publish the correlation between card tier and correction rate as our own performance data |

### Lloyd's — center holds brand, risk sits at the edge

| Lloyd's mechanism | Working detail | CoAI adaptation |
|---|---|---|
| **Marketplace separation** | Corporation of Lloyd's sets rules/brand/oversight; syndicates carry risk; single market rating (S&P A+) applies to all because supervision is centralized | The Council sets methodology and issues cards; insurers/enterprises take reliance decisions. Never underwrite, never certify — Firewall 1 is exactly this separation |
| **Coverholder delegated authority** | ~2,500+ coverholders bind risk under registered scopes in DCOM; **monthly bordereaux reporting, escalated frequency as early-warning sanction**; annual audits; from Jan 2026 each managing agent gets a dedicated oversight manager | Attestor/delegated-measurement program: registered scopes, monthly signed-data reporting, escalation = more frequent reporting before suspension |
| **Performance Management Directorate** | Every managing agent files an **annual business plan**; PMD monitors against it and can exit underperformers (Decile-10 exits are canonical) | Annual attestor review against a filed measurement plan; underperforming attestors lose scope |
| **Chain of security / Central Fund** | Three capital tiers ending in a mutualized Central Fund (~£4.3bn) — the backstop that makes the single brand credible | Long-horizon: a relying-party protection fund is the mutualized version. Near-term honest version: escrowed bonds per card family (Part 2, waterfall row) — **do not claim a fund that has no money in it** |

### ISO CASCO — honest vocabulary

The lane confirmed the category map: we operate as a **measurement/attestation body issuing verified measurement credentials** (CASCO-adjacent to testing + validation), explicitly NOT certification, NOT accreditation. Language lock stands: "verified measurement credential," never "certification."

**Part 1 verdict — the five patterns worth stealing wholesale:** (1) scope-bounded grants with revocation; (2) surveillance annuity economics (UL's 33% > 26% split is the business-model proof); (3) confidential self-report intake with a cure window; (4) self-published error statistics as the credibility moat; (5) committee-dissued high-stakes cards.

---

## Part 2 — Market-infrastructure operations (exchanges · CCPs · banks · insurers · index providers)

Lane B dissected exchanges, CCPs, banks/payments, insurers, index providers, and regulators' public registers. Fourteen mechanisms mapped; the strongest nine below, hype-kills first.

**Hype-kill caveats (locked):** (a) a "default fund" analog means nothing without real escrowed money — no insurance theater; (b) circuit breakers need pre-committed numeric bands — discretionary suspension degrades to arbitrary censorship; (c) registry "finality" is a *governance-defined* immutability point, not a blockchain property — PFMI's lesson is that finality must be stated ex ante and survive disputes; (d) the CME end-of-day relicensing revolt shows data-licensing terms are where ecosystems revolt — publish derived-data rights unambiguously at day one (already a locked owner gate: Nasdaq "Derived Data — New Original Works" template).

| # | Market mechanism (source institution) | Working detail | CoAI adaptation |
|---|---|---|---|
| 1 | **Listing standards + deficiency/cure process** (NYSE/Nasdaq) | Quantitative continued-listing thresholds; deficiency letter; ~6-month cure with milestone plans; then suspension | Card issuance bar + ongoing attestation compliance: published thresholds, written deficiency notice, published cure window with milestones, then suspension |
| 2 | **Delisting ladder + immediate-delisting trigger** (NYSE $0.25 rule) | Graduated ladder with due process — but one codified *immediate* trigger for egregious cases, bypassing cure | Revocation ladder with a codified **immediate-revocation trigger for fabricated measurements**; appeal path preserved |
| 3 | **Market surveillance** (Nasdaq SMARTS; insider-ring clustering) | Cross-event anomaly detection; coordinated-ring detection | Registry surveillance: drift between card claims and re-measured behavior; coordinated fake-attestation rings; per-family baselines. (This is GNN-monoculture v0's operational sibling — DO move 89) |
| 4 | **Consolidated Audit Trail** (SEC Rule 613) | Full order-lifecycle logging, unique IDs, 50ms clock sync, fully replayable | The registry's own CAT: append-only lifecycle log of every card event (issue / verify / re-attest / dispute / revoke), synchronized timestamps, stable IDs. Already half-built via signed cards + ledger — formalize the event schema |
| 5 | **Circuit breakers** (7/13/20% tiers; LULD bands) | Pre-announced numeric bands, automatic action, defined resumption | Pre-committed anomaly bands: Tier 1 = pause re-attestations for a card family; Tier 2 = auto-suspend the family; Tier 3 = halt that day's index publication; published resumption procedure |
| 6 | **Closing auction / official closing price** (Nasdaq Closing Cross + NOII) | Fixed-time batch discovery; indicative values pre-published; **one official closing value** everyone cites | **The daily index as a closing cross:** fixed-time batch aggregation of the day's verified measurements, indicative pre-publication values, one official signed value downstream parties cite. This reframes the index from "a dashboard" into "the settlement price of the agent economy" — the strongest single framing steal in this Part |
| 7 | **Corporate actions processing** (DTC: record dates, ISO 20022 events) | ~1.4M securities' lifecycle events processed as structured events: announcement → record date → entitlement → allocation | Model lifecycle events (weights update, merge, deprecation, licence change) processed as **corporate actions on cards**: record date fixes which card applies; machine-readable event feed to relying parties |
| 8 | **Default waterfall** (CCP: defaulter IM → SITG → Cover-2 mutual fund) | Codified loss-absorption order; CCP skin-in-the-game exists explicitly to align incentives | Layered failure-compensation, only as money allows: issuer bond → issuer escrow → Council's own reserve (skin-in-the-game) → mutualized fund from card fees, sized to simultaneous failure of the two largest card families. **No escrow, no claim** — caveat (a) governs |
| 9 | **Settlement finality + netting + reconciliation + EOD close** (PFMI P8; double-entry banking) | Ex-ante defined irrevocability point (insolvency-proof); corrections only via compensating entries; daily reconciliation blocks the close on unresolved breaks | Define the exact moment a card becomes final (signature + transparency-log anchor); after it, **forward-only corrections via superseding entries — never silent rewrites**; daily reconciliation of registry ledger vs public verification API vs transparency log; unresolved breaks block index publication; signed end-of-day root hash = the daily close |
| 10 | **LEI/GLEIF + ISO 20022 migration** (GLEIF; SWIFT MT→MX) | Open, daily-updated global identity index; Validation Agent program; 3-year coexistence, in-flow translation, reject-on-invalid validation, published usage guidelines | Persistent open IDs for measured orgs/models (the registry already keys them — publish the ID scheme); card schema managed like ISO 20022: versioned, phased migrations, coexistence windows, reject-on-invalid validation in the verifier |
| 11 | **IOSCO Benchmark Principles + BMR** (IOSCO 2013; EU 2016/1011) | Published methodology with input hierarchy; independent oversight; **material methodology changes require advance public consultation**; documented error/correction policy; **benchmark cessation policy**; annual independent assurance (S&P DJI on its 12th annual review) | The index governance file, verbatim: methodology doc, oversight function, consultation-before-change rule, error policy, **cessation policy** (nobody trusts a benchmark that can't say how it dies), annual external assurance when revenue allows. Reinforces the standing BMR gate: bright line is USE — "research statistic, not for use as a financial benchmark" on every card until this file exists |
| 12 | **Rebalance calendars as public commitment** (FTSE Russell) | Reconstitution dates published far ahead; the 2026 annual→semi-annual shift was itself run as a **public consultation**; fast-entry rules for large IPOs | Publish the index methodology-change calendar; fast-entry rule for major model launches (a GPT-6 class launch enters the index within N days, pre-committed) |
| 13 | **External model adoption under validation discipline** (post-Andrew cat models; Solvency II use-test; **NAIC Dec-2025 draft: vendor registration for third-party data/models used in pricing**) | Insurers industrialized third-party models but regulators forced formal validation AND are now building **registries of measurement vendors** | We ARE the third-party vendor the NAIC-style registries will register. Design partner + insurance-evidence packs (DO moves 69/72) should be built to slot into vendor-registration questionnaires by default |
| 14 | **Regulators' public registers** (FINRA BrokerCheck; FCA FS Register + enforcement publicity) | Free public registers keyed to stable IDs; retain barred/former entities; enforcement notices as a public dataset used for due diligence | The public model register: free, stable IDs, retains revoked cards (a revoked card stays visible, marked revoked — never deleted); enforcement/correction notices published as a dataset. **Deletion = destroying institutional evidence** |

**Part 2 verdict:** the index is the settlement price; the registry is the CAT + BrokerCheck; the card lifecycle is corporate-actions processing; and BMR/IOSCO discipline (consultation, error policy, cessation policy) is what separates a benchmark from a leaderboard. The money mechanisms (waterfall, margin) stay locked behind caveat (a) until real escrow exists.

---

## Part 3 — Forkable ops tooling + operating rituals

Lane C verified licences and 2026 maintenance signals against primary sources. Fork order follows the playbook Parts above.

### Workstream A — forkable tooling (verdicts)

| # | Tool | Licence / 2026 status | Mission | Verdict |
|---|---|---|---|---|
| 1 | **Upptime** + **Gatus** | MIT / Apache-2.0; Gatus very active (commits Apr 2026) | Status page + uptime for registry, index, Pages sites. Upptime = zero-infra (GitHub Actions+Pages), fits the estate's posture | **Fork Upptime now**; Gatus if one binary on Oracle/RunPod wanted. Cachet SKIP (v3 never GA'd); openstatus AGPL — self-host only |
| 2 | **release-please** (or Changesets) | Apache-2.0; ships but Google stewardship minimal — pin versions | Public changelog for the 55-package monorepo: automated "Version Packages" PR = audit trail per release; Python-native | **Fork** — pairs with the 15 signed release proofs |
| 3 | **OneUptime** | Apache-2.0; very active | Full incident lifecycle (status + on-call + post-mortems) | Skip until on-call rituals exist; row 1 suffices |
| 4 | **lakeFS** (+ DVC optional) | Apache-2.0; active, explicit OSS commitment | **Corpus versioning on MinIO**: git-like branches over S3-compatible storage — reproduce "the corpus as-of 2026-08-01" for any index publication | **Fork for the corpus** — this is the reproducibility layer the DOIs promise |
| 5 | **OpenLineage events** (defer Marquez server) | Apache-2.0; LF AI & Data Graduate, active. Marquez slowing (issues unanswered since May 2025) | Emit lineage events from measurement/index pipelines → every daily index value traces to raw measurements | **Adopt the spec now, server later** |
| 6 | **Backstage** | Apache-2.0; healthy CNCF project | Public model register | **SKIP — wrong scale.** Register = signed JSON records + static site on Pages (pattern: Artifact Hub if a fork is ever wanted). We have Ed25519 cards already |
| 7 | **Probo** | MIT; active (Aug 2026) | Open-source GRC with built-in public trust-center portal + CAPA/risk registers | Static /trust page today; **fork Probo when SOC 2/ISO 27001 work starts** |
| 8 | **shields.io** (self-host) + Uptime Kuma badges | CC0 / MIT; both active (Kuma pin ≥2.2.0, CVE-2026-32230) | "Council-verified ✓ card-valid" conformance badges per measured model | Fork shields endpoint or generate SVGs at build time (badge deploy = DO move 90, owner-gated on CF token) |
| 9 | **Sloth** + OpenSLO + Grafana Cloud free tier | Apache-2.0 (Sloth; revived 2025); Grafana AGPL — use the hosted free tier | SLOs-as-code: registry API availability, daily-index on-time rate, card-verification success | **Fork Sloth**; error-budget policy is a Workstream-B artifact |
| 10 | **Fider** / GitHub Discussions; **OPA** later | AGPL / Apache-2.0; both active | Public roadmap+feedback; badge-eligibility rules as executable policy | GitHub Discussions = zero-infra MVP; OPA only when badge rules outgrow YAML |

**Also verified:** dbt metrics-layer licence risk RESOLVED — MetricFlow and the Fusion engine core are Apache-2.0 (Oct 2025 / Jun 2026); optional, DuckDB+SQL in-repo is the cheaper start.

### Workstream B — operating rituals (the institutional behaviors)

| # | Ritual | Who proves it | Minimum-viable version | Effort |
|---|---|---|---|---|
| 1 | **Public status + monthly availability report** | GitHub monthly availability report (running since 2020, still publishing missed targets — *mixed news is the trust signal*); Stripe per-component history | Upptime page + one-page monthly "registry availability & index timeliness" note committed to git | Low |
| 2 | **Annual transparency report** | Cloudflare semi-annual since 2013; GitHub annual | "Council Transparency Report": # measurements, # cards revoked/corrected, disputes received + resolution, funding sources | Low |
| 3 | **security.txt + VDP** | RFC 9116; disclose.io safe harbor; ISO/IEC 29147/30111; 90-day coordinated-disclosure norm | `/.well-known/security.txt` (10 min) + VDP page: safe harbor, scope, ack 5 business days | Hours |
| 4 | **CVE-style IDs for measurement findings** | AI Incident Database sequential IDs (1→746+); OSV JSON / GHSA schemas to copy. (CVE CNA route is free but covers vulns only) | `COAI-2026-0001` scheme; one signed OSV-style JSON per finding in a public `advisories/` repo. **IDs make corrections citable — cheap and compounding** | Low |
| 5 | **ISO 9001-lite QMS** | ISO 9001 clauses 9.2/9.3/10.2: internal audit, management review, CAPA with *verified* closure | `qms/` in monorepo: CAPA log as GitHub Issues (trigger → root cause → action → verified closure); quarterly self-review MD; annual self-audit vs published methods | Low |
| 6 | **Changelog + deprecation/versioning policy** | Stripe dated API versions (breaking changes ≤2×/yr, per-account pinning, sunset windows); RFC 8594 `Sunset` header | release-please CHANGELOGs + one DEPRECATION.md: dated versions, ≥6-month sunset notice, Sunset header on API responses | Low |
| 7 | **Governance docs-as-code, publicly** | github/site-policy (CC0, full git history of ToS changes) | Public `policies` repo: methodology, scoring rules, appeals, conflicts policy — every change a signed commit. **The diff history IS the institutional evidence** | Low |
| 8 | **Public SLOs with error budgets** | Google SRE workbook; GitHub/Stripe publish availability | 2–3 SLOs only (registry availability, index on-time, verification success); Sloth rules; freeze non-essential changes when budget burns — and say so publicly | Medium |
| 9 | **Trust center** | Vanta/Drata category; Probo open-source | Static `/trust` now: security.txt, VDP, policies links, subprocessors (Cloudflare, MinIO host, RunPod, Oracle), **Ed25519 key fingerprints + rotation log** | Low → Medium |
| 10 | **Compliance calendar as artifact** | UK small-co obligations: ICO fee annual (Tier 1 **£52/yr** post-17-Feb-2025 rise — note canon had £40; verify at payment), Companies House confirmation statement + accounts, CT600; domain/TLS/key-rotation dates | `compliance-calendar.md` in policies repo + monthly GitHub Actions cron opening reminder issues 30 days out | Hours |

**Negative results (do not adopt):** Cachet (v3 vapor), LogChimp (unmaintained), badgen classic (stale), Backstage (wrong scale), Marquez server (maintainer responsiveness degraded), dbt Fusion binary (proprietary login-gated features — core only if ever needed).

---

## Part 4 — The integrated "what we are NOT doing" list + 30/60/90 ops sequence

### What serious institutions do that we are NOT doing yet (the honest gap list)

| # | Gap | Which body does it | Cost to close | Priority |
|---|---|---|---|---|
| 1 | **No published card-event lifecycle log** (issue/verify/re-attest/dispute/revoke as replayable append-only feed) | CAT (SEC 613); DTC corporate actions | Schema + emitter on existing ledger — days of lane work | P0 — this is what makes the registry an institution rather than a spreadsheet |
| 2 | **No published deficiency/cure/revocation ladder** | NYSE continued-listing; UL Variation Notice | One policy doc + one enum in card schema | P0 |
| 3 | **No self-published error statistics** (revocation/correction/drift rates) | NRSRO Exhibit 1; IOSCO assurance | Aggregate from ledger — the data already exists | P0 |
| 4 | **No formal dispute/appeal process** (fact-check window, new-evidence-only appeal, watch status) | NRSRO bounded appeal | One policy doc + `status: watch` in schema | P0 |
| 5 | **No methodology-change consultation + cessation policy** | IOSCO Principles; FTSE rebalance consultation | One governance doc | P0 — unlocks the BMR conversation honestly |
| 6 | **No status page / SLOs / availability report** | GitHub/Stripe availability reports | Upptime fork (zero infra) + monthly note | P1 |
| 7 | **No security.txt / VDP / advisories with IDs** | RFC 9116; OSV schema | Hours | P1 |
| 8 | **No governance-as-code public policies repo** (signed-commit diff history) | github/site-policy | Hours — policies exist in drafts | P1 |
| 9 | **No corpus versioning tied to publications** (reproduce "corpus as-of date X") | 17025 traceability; lakeFS pattern | lakeFS fork on MinIO — medium lane effort | P1 — the DOIs promise this; make it true |
| 10 | **No delegated-measurement (attestor) program docs** (scoped grants, bordereaux-style reporting, annual review) | FAA ODA; Lloyd's coverholders | Docs only until first attestor exists | P2 — write now, activate with first design partner |
| 11 | **No confidential self-report intake with cure window** | NASA ASRS (10-day immunity window) | Intake form + policy; third-party custody only at volume | P2 |
| 12 | **No failure-compensation layers** (bonds/escrow/reserve) | CCP waterfall; Lloyd's Central Fund | **GATED — no escrow, no claim.** First dollar of card revenue defines the reserve policy | P2/GATED |
| 13 | **No public register retaining revoked entries** | BrokerCheck retains barred brokers | Register keeps revoked cards visible-marked-revoked | P1 — deletion destroys institutional evidence |
| 14 | **No compliance calendar artifact** | Standard UK small-co discipline | `compliance-calendar.md` + Actions cron — hours | P1 (ICO £52/yr verify-at-payment; CH statement; key rotation; domain/TLS) |
| 15 | **No annual transparency report** | Cloudflare/GitHub cadence | One MD per year, first one cheap | P2 (first edition after first full quarter of index) |

### 30 / 60 / 90 ops sequence (overlaid on the DO 61–93 move clock, not replacing it)

| Window | Ops-layer deliverables (this playbook) | Cross-refs |
|---|---|---|
| **Days 0–30** | Gap 1 event-schema + emitter; gaps 2–5 as ONE governance bundle (`policies` repo v1: issuance bar, revocation ladder, dispute process, methodology-change + cessation, error-stats format); gap 7 security.txt+VDP; gap 14 compliance calendar; gap 6 Upptime fork | Unlocks move 83 (BMR line) honestly; supports moves 61–67 standards bids (a body with published governance is a credible IETF/W3C participant) |
| **Days 31–60** | Gap 9 lakeFS corpus versioning; gap 3 first error-statistics page (from ledger); gap 13 revoked-retention in register; gap 8 SLOs via Sloth; gap 4 advisories repo (`COAI-2026-NNNN` + OSV JSON) | Feeds move 75 (Delta Note #2) and move 84 (trust deltas) with institutional plumbing underneath |
| **Days 61–90** | Gap 10 attestor-program docs (ODA/coverholder pattern); gap 11 self-report intake; gap 15 transparency report #1 if a full quarter elapsed; gap 12 reserve POLICY (money-gated) | Positions moves 68–73 (attestor slots: Workday, AIUC-1, SG Sandbox, insurance evidence) with a real delegated-authority framework behind the asks |

### Distribution rail — "be on all agents and boards" (locked doctrine from the Kit, ops-layer execution)

The ask maps to a concrete channel plan. **Anchor = ONE Zenodo concept DOI; every mirror points back; archives first; press never before external recompute; one artifact = one genuine record.**

| Tier | Venues | Mechanism / status |
|---|---|---|
| T1 — authoritative archives | **Zenodo** (3 DOIs already live: 21914702, 21914151, 21914194 — concept-DOI for the index is move 76) · **Software Heritage** (SWHID = ISO/IEC 18670:2025; archive the monorepo) · **arXiv** (shell 7946050 — **owner gate: 2 checkboxes + "ndependent Researcher" typo fix BEFORE submit; endorsement hardened 21 Jan 2026, expires Aug 27**) · OSF (**phase-out: no new projects 16 Nov 2026, read-only 19 Feb 2027 — deprioritize**) · **OECD.AI + DSIT Portfolio** (prime diligence surfaces) | Largely owner-gated clicks |
| T2 — discovery surfaces | Hugging Face (YAML + Croissant metadata) · Kaggle (**/csoai claim — owner gate**) · GitHub releases + Zenodo webhook · OpenML · SSRN | Posting kit exists in Compass artifact |
| T3 — machine-readability for agents (the "all agents" half) | MCP registry `io.github.CSOAI-ORG/*` (**live**) · npm `@meok-labs/csoai` (**live**; **bare `csoai` still 404 — squat owner gate**) · PyPI `council-signal-mcp` 0.1.2 + `csoai` 0.2.0 (**live**) · Rekor/SCITT transparency anchors (DO move 66) · C2PA (DO move 79; Conformance EOI = cheapest thread→signed) | This is how agents *find* us: the registry entries, the verify endpoint, the signed cards |
| T4 — press | **Last, and never before external recompute** (distribution transcript: "PR wire = trap before recompute") | Blocked on DQ tier-mover #1 |

**Killed channel canon:** TechRxiv closed; Papers-with-Code defunct (sunset Jul 24 2025); Dryad charges unaffiliated $150+; OSF winding down. Don't spend clicks there.

### Standing constraints reaffirmed (ops layer touches none of these)

Fallback-signer seam stays flagged: **published cards must never come from HMAC fallback/stub mode** (dev_stub assert pending); private key only on pod signing node; SOVOS-family names never public; Firewall 1 (rails not certification) and Firewall 2 (analyse, never train champion on honey) govern every pattern above — Lloyd's/UL adaptations are *oversight* patterns, never underwriting or certification; killed claims (NVIDIA-PR-as-partnership, CSGA, 33 agents, $2T framing) never recur in any playbook artifact.

---

*Playbook compiled from three verified research lanes (measurement bodies / market infrastructure / tooling+rituals), 2026-08-15. Mechanism facts primary-sourced by the lanes; analog column is design judgment, flagged as such throughout.*
