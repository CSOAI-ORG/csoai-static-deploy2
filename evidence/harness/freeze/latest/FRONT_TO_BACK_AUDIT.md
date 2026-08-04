# Front-to-back audit — every layer, checked not assumed · 2026-08-04

Each row was executed today. Nothing is carried over from a document.

---

## L1 — FRONT END (live, as GPTBot, no JavaScript)

| route | HTTP | crawler-visible text |
|---|---|---|
| `/` | 200 | **60 chars** |
| `/pricing` `/certification` `/crosswalks` `/compare` `/article-50` `/about` `/eu-ai-act` | 200 | **60 chars each** |
| `/this-route-should-not-exist…` | **200** | 60 chars — **no 404** |

**FAIL, all four gate rules.** Eight advertised routes serve one identical document; a
non-existent path returns 200; per-route canonical is JS-set so crawlers never see it.

Root cause is known and **owner-gated**: `scripts/prerender.mjs` exists, is correct, and is not
wired into `vercel.json`'s buildCommand. The wiring doc (`PRERENDER_VERCEL_WIRING.md`,
8 July) contains the one-line fix and a rollback, and reserves the decision to the owner
because "changing buildCommand has caused prod outages before". **Not mine to flip.**

Verified separately: **4 domains hard-402** (safetyof.ai, agisafe.ai, accountabilityof.ai,
cobolbridge.ai); **2 unreachable** (defoneos.com, sovereign.wiki); openmoe.ai 200.

---

## L2 — SITE LINTS (councilof-ai)

| lint | result |
|---|---|
| `smoke:evidence` | **11/11 PASS** — includes `empty → UNMEASURED` and `tampered payload rejected` |
| `lint:refutations` | **PASS** — 9 surfaces agree with the ledger |
| `counter-lint` | **PASS**, but green on **315 occurrences** of the DR-0007-retracted "33-agent Byzantine council" across **48 files in the live `client/` path** |

The counter-lint result is the honest version of the day's recurring pattern: it *names* the
decision (rebadge vs pull) as owner-gated rather than hiding it. But the retraction reached the
ledger and never reached the surface.

---

## L3 — BACK END / AGENT SURFACES

| check | result |
|---|---|
| `os.meok.ai/api/health` as GPTBot / ClaudeBot / PerplexityBot | **200 JSON to all three** — an audit claim that it blocks agents is REFUTED |
| `security.txt` present | csoai.org, meok.ai, proofof.ai — all 200 |
| `security.txt` RFC 9116 `Expires` | **2 of 3 INVALID** — csoai.org and proofof.ai expire 2027-12-31, **16.9 months** out (limit is 12). csoai.org also uses lowercase `z` where RFC 3339 requires `Z` |
| DNS email auth | **5 domains with NO MX/SPF/DMARC**; csoai.org has DMARC `p=none` only |

---

## L4 — INSTRUMENTS

| check | result |
|---|---|
| `grade_response` selftest | **PASS** (after correcting my own faulty test — see below) |
| `expect_mode` applied | **146/146** items |
| GovBench shape | 26 dimensions, **193 items** |
| Grader provenance | content-hashed `@5e2db7573d06` |
| Reproducibility | 8 retained runs, **4/6 models exact** at temperature 0; all drift instrument-attributable |

**A false alarm I caused and must record.** The audit first reported `grade_response: FAIL`.
The failing case was my own: I asserted *"Article 5 prohibits social scoring and biometric
categorisation"* should score 1.0 on `expect_serve`. It has **7 qualifying words**; `_substantive`
requires **8**. The grader was right; my test string was too short. **Third time today my test
was wrong rather than the code** — the other two were single-letter keywords matching inside
"cont**a**ins", and a `ps` pattern that couldn't match its own process.

---

## L5 — DATA / CORPUS

| asset | measured |
|---|---|
| provision packs | **ONE** — `eu-ai-act@1.0.0` |
| provisions | **21**, each content-hashed to `SNAP-EU-AI-ACT-202608-*` |
| GDPR / CRA / DORA / NIS2 / CSRD packs | **NONE** — no pack, no snapshot dir |
| frozen benchmark items | 90 across 6 axes |
| items whose anchor **resolves** to a corpus provision | **13 (14%)** — five of six axes resolve **zero** |
| control sets | 4 frameworks, 18 controls |

---

## L6 — EVIDENCE / CANON

| canon # | claim | status |
|---|---|---|
| 3 | 417 provisions | **number VERIFIED, artifact ABSENT** — 21 exist |
| 5 | 193 GovBench items | **VERIFIED**, two methods agree |
| 8 | 52 charter articles | **VERIFIED** |
| 12 | ProvBench "0 of 20" | **VERIFIED** — 110 pre-registered cells, 0 disagreements |
| 4 | 30 frameworks | **UNSUPPORTED** — 4 on disk, claim appears 78× |
| 6 | 19 signed agents | **UNSUPPORTED** — largest registry holds 7 |
| 9 | 9 MCP tools | **UNSUPPORTED** — largest registry holds 7 |

**G3 gate: PASS**, and now blocks unevidenced phrases and register-lock breaches, with a
self-test proving each rule fires.

**The refinement G3 still needs:** canon #3 passes because a file *contains* the number 417.
Nobody can point to 417 provisions. *"The number has an evidence file"* ≠ *"the artifact the
number describes exists."*

---

## L7 — PUBLICATION SURFACES

| surface | measured |
|---|---|
| HF `csoai` | 16 datasets, 2 models; **LICENSE added to 3** today (govbench, care-battery, pqcbench — all claimed apache-2.0 with no LICENSE file) |
| HF viewers | **3 broken** — provbench (deprecated loading script), govbench + aiact (schema CastError). All three diagnosed with a tested fix; **none pushed** |
| `csoai/govbench` card | says **174 items**; actual is **193** |
| GitHub | 605 repos on the authed account |
| NVIDIA PR #75 | **OPEN, mergedAt null, 1 review** — not merged, not accepted |
| NOOA evaluator suites | **21/21 pass** on the pod after installing Python 3.12 + nooa |

---

## THE ONE-LINE VERDICT PER LAYER

- **L1 front end** — FAIL, root cause known, fix owner-gated
- **L2 lints** — PASS, with 315 live occurrences of a retracted claim awaiting an owner call
- **L3 back end** — healthy; 2 invalid `security.txt` Expires; 5 domains spoofable
- **L4 instruments** — PASS, and now structurally unable to repeat four fixed defects
- **L5 data** — one real corpus of 21, honestly small; 86% of items prose-anchored
- **L6 evidence** — 4 verified, 3 unsupported, 1 needing a G3 refinement
- **L7 publication** — 3 broken viewers staged, PR #75 open, card contradicts source

**Nothing in this audit is a number I was told. Every line was executed.**
