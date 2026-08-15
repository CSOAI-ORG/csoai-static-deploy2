# HF + KAGGLE AUDIT, 30-SITE SPRAY MAP & THE DATASET-INGESTION RULING
**Date:** 2026-08-12 · **Method:** live HF index/search verification, Kaggle probing, estate review. Every item registered.

---

## 1. THE DATASET QUESTION FIRST — "can't we monorepo 100k datasets into SOV?"

**No — and yes, in five lawful ways. Datasets don't merge like weights.** MergeKit merges *parameters*; data has no λ to sweep. What 100k public datasets can become inside SOV:

| Path | What it means | Gate |
|---|---|---|
| **1. Fine-tune fuel** | Curated sets train the next specialist generation | License-clean for commercial use + quality floor |
| **2. Item-bank raw material** | Legal/compliance/safety sets converted into GSPC items | `item_gate.py` + canaries + held-out splits |
| **3. Arena & City environments** | Scenario corpora become match/city content | Provenance record per set |
| **4. OWEM corpus** | World-model layer training data | License + PII screen + contamination scan |
| **5. Benchmark mirrors** | External benchmarks prove harness generality (GSM8K proof pattern) | Constant-predictor floor applies |

**Six ingestion gates (canon):** ① license filter (Apache/CC-BY for product; NC/research-only excluded) ② contamination scan against our held-out splits ③ PII screen ④ quality floor (must beat the constant predictor on our axes — most bulk data won't) ⑤ **signed ingestion card per dataset** (we eat our own cooking: every ingestion is itself a signed 3KB event) ⑥ attribution ledger.

**The moat reminder:** those 100k datasets are *commodity* — every competitor can download them tomorrow. Our signed longitudinal corpus is the gold because it can't be recreated. **Ingestion builds capability; generation builds moat.** Realistic curation: of 100k+ sets, maybe a few hundred touch our axes; the first pass is ~50 high-yield sets (legal reasoning, safety, provenance, agent trajectories), not a bulk land-grab. Volume is water; gated selection is honey.

---

## 2. HF AUDIT — what's actually live (verified via index, 2026-08-12)

Org: **csoai** — "Council for the Safety of Artificial Intelligence" — commits by Nicholastempleman, all "verified".

| Asset | State | Note |
|---|---|---|
| `datasets/csoai/gspc-oss` | ✅ Live, Apache-2.0 | n=16 licence reasoning, canary'd, held-out split |
| `datasets/csoai/sov-signal-ground-truth-v10` | ✅ Live (08-09) | **Signed ground truth — Ed25519 sig + digest per record, pub key embedded.** Publishes honest `outcome: "wrong"` rows. This is the public-sampling doctrine executed |
| `datasets/csoai/gspc-arena-results` | ✅ Live (08-06), **47 downloads/mo** | Routing table + CIs + an "Honest caveats" section ("~half the per-axis winners are statistical ties") — doctrine-visible. Includes GSM8K harness-generality proof |
| `datasets/csoai/gspc-gov / -prv / -xr / -mach / -papers` (+ likely -care, -asi) | ✅ Live | gspc-prv = C2PA manifest-mechanics items with canary GUID; gspc-mach expanded to n=33 with honest "DRAFT, not quotable" history |
| `models/csoai/sov-compliance-art5` | ✅ Live | vLLM/Ollama/Jan/LM Studio integration snippets auto-generated |
| **gspc-papers content** | ⚠️ **CONTAINS INTERNAL STRATEGY** | Public dataset includes portfolio strategy text: *"Sell against procurement (RM6200…) and the Online Safety Act… Weight the portfolio accordingly."* Internal GTM thinking in a public artifact — **scrub or move private before any spray** |
| **Naming on HF** | ⚠️ | Dataset title **"GSPC / SOVOS — Papers, Methods & Roadmap"** carries SOVOS — the naming kill extends to HF |

### HF to-do (the moves available on this site)
1. **Scrub gspc-papers** of strategy text; rename the SOVOS title → "GSPC / Council of AI". (Today)
2. **Uniform dataset-card standard**: ruler hash (JUDGE.lock), usable_n, interval, license, canary notice, DOI link. Some cards have it; make it mechanical.
3. **HF Collection** "GSPC" linking all axis datasets + results — one link to rule the estate.
4. **HF Space: live signed-assessment demo** — the Patronus playground move, HF edition; embeds on councilof.ai.
5. **Model cards for the fleet — GATED** until Season 1b (ruler-hash requirement).
6. **Papers pages**: claim when the GSPC whitepaper hits arXiv; link datasets ↔ paper ↔ Space.
7. **Community/Discussions** on flagship datasets (gspc-gov already has it) — cheap engagement surface.

## 3. KAGGLE AUDIT — ⚠️ UNVERIFIED FROM OUTSIDE

- `kaggle.com/csoai`, `/councilofai`, `/nicholastempleman`, `/csoailtd` → **all 404**. The lane's "12 mirrors public" claim cannot be confirmed from outside — **lane must drop the profile URL for verification.** If mirrors exist under another handle, fine — prove it; if not, the claim goes in the ledger.
- **Kaggle's unique levers when live:** ① **Notebooks** — executable reproduction per dataset (Kaggle's differentiator: proof that runs in-browser) ② **Competitions** — the gold play later: host a governance-classification competition with signed ground truth + private leaderboard (Kaggle *literally runs on* the held-out doctrine) ③ Kaggle Models for GGUFs — gated on 1b ④ Datasets mirror with the same card standard as HF.

---

## 4. THE 30-SITE SPRAY MAP

**Spray tiers (doctrine):** T0 = claim presence now (no doctrine risk) · T1 = content spray allowed once dates fixed (positioning line, doctrine, whitepapers) · T2 = data/model/metrics spray **GATED** until Season 1b + board deltas + ruler hash on cards.

| # | Site | Tier | Components to fill | First move |
|---|---|---|---|---|
| 1 | GitHub org | T0/T2 | Org profile README, monorepo public mirror, topics, releases, awesome-list PRs | Org README with positioning line + evidence links |
| 2 | HuggingFace | T1/T2 | (see §2) | Scrub + collection + Space |
| 3 | Kaggle | T2 | Profile, dataset mirrors, notebooks, competition | Verify profile URL; mirror gspc-oss + notebook |
| 4 | **Zenodo** | **T1** | DOIs for whitepaper + datasets + software releases | Mint DOI for regulatory-clock + GSPC paper draft |
| 5 | **arXiv** | **T1** | cs.CY/cs.AI/cs.CR papers | GSPC instrument paper (BE queue) |
| 6 | Papers with Code | T2 | Benchmark + code + leaderboard links | After arXiv post |
| 7 | OpenReview | T1 | NeurIPS Regulatable ML workshop submission | EU-Agent-Bench venue — our doctrine's home crowd |
| 8 | OpenML | T2 | Dataset mirrors | Mirror GSPC axis sets |
| 9 | **Ollama library** | T2 | Eunomia/fleet model pages | **After Season 1b** — downloads are the Jan-style counter |
| 10 | ModelScope | T2 | Mirror datasets/models (CN ecosystem reach) | After HF parity |
| 11 | Replicate | T2 | Hosted signed-assessment demo | After Space proves the demo |
| 12 | PyPI | T2 | `gspc` harness package + verifier CLI | Publish signature-verifier (the hex recipe!) |
| 13 | Docker Hub | T2 | Harness images, one-command reproduction | With PyPI push |
| 14 | Flathub / Homebrew | T0 | MEOK distribution channels (Jan's pattern) | Claim when MEOK app exists |
| 15 | **Product Hunt** | T1 | MEOK launch page, maker comment kit | At MEOK readiness |
| 16 | **Hacker News (Show HN)** | T1 | Signed assessment + honest-intervals angle | "Show HN: AI risk assessment that signs its work (Ed25519), with confidence intervals" |
| 17 | Reddit (r/LocalLLaMA, r/MachineLearning, r/singularity) | T1 | Doctrine posts, arena results (post-1b), Limitless-exit angle for MEOK | LocalLLaMA loves signed/verifiable + local-first |
| 18 | Dev.to + Medium + Substack | T1 | Doctrine blog: declare→fix→re-measure series, watermark-verification posts | "Anthropic now watermarks everything. Here's what it can't prove." |
| 19 | **LinkedIn** | T0/T1 | Company page (Council of AI), founder posts, insurer/regulator audience | Company page + weekly evidence posts |
| 20 | X (@councilofai) | T0/T1 | Evidence-drops, Art. 50 commentary, league tables (post-1b) | Claim handle, pin positioning line |
| 21 | Discord | T0/T1 | Community server (Jan pattern: 15k+ badge = social proof) | Open with city/arena devlog channel |
| 22 | Crunchbase | T0 | Company profile (funding-discovery surface) | Claim + fill |
| 23 | Wellfound | T0 | Hiring/profile | Claim |
| 24 | F6S | T0/T1 | Grant/accelerator applications (DSIT fund lives here-adjacent) | Profile + DSIT £11M app |
| 25 | G2 + Capterra | T1/T2 | Product listings (governance category, where Credo/Holistic live) | After pricing page ships |
| 26 | AlternativeTo + Slant | T1 | MEOK listed as alternative to Jan/Msty/Limitless | "Limitless left the UK/EU. MEOK didn't." |
| 27 | There's An AI For That + Futurepedia | T1 | Tool directory listings | Signed-assessment listing |
| 28 | **C2PA member directory + LF AI & Data + AI Alliance** | T0/T1 | Standards-body presence; CAWG alignment (BE diamond D2) | Membership inquiry + align manifest work |
| 29 | MLCommons community | T1 | AILuminate Global Assurance Programme adjacency | Align GSPC↔42119 mapping note |
| 30 | StackShare + Stack Overflow | T1 | Technical presence, verifier-cli answers | Answer watermark/Ed25519 verification Qs with our recipe |

**Page-component standard (every site):** ① logo+banner ② bio = positioning line ③ canonical link back to councilof.ai ④ one proof unit (signed sample artifact or interval-carrying figure) ⑤ one CTA (run assessment / read benchmarks) ⑥ company footer "CSO AI LTD, UK #16939677" where profiles allow.

---

## 5. REGISTER

- **REAL:** HF estate is genuine and indexed (7+ datasets, 1 model, signed ground truth, honest caveats, 47 downloads/mo).
- **⚠️ LEAK:** internal GTM strategy text inside the public gspc-papers dataset — scrub before spray.
- **⚠️ NAMING:** SOVOS appears in an HF dataset title — naming kill extends off-web.
- **UNVERIFIED:** Kaggle "12 mirrors public" — no discoverable profile from outside; lane to provide URL or the claim enters the ledger.
- **DOCTRINE:** datasets can't be merged like weights; five conversion paths, six ingestion gates; ingestion builds capability, generation builds moat.

## 6. THREE MOVES TODAY

1. **Scrub + rename on HF** (gspc-papers strategy text, SOVOS title) — 30 min, stops the leak.
2. **T0 presence sweep** — claim GitHub org README, LinkedIn, X, Crunchbase, Discord: one hour, pure brand protection, zero doctrine risk.
3. **Zenodo DOI for the regulatory-clock dataset + GSPC paper draft** — starts the citation clock while Season 1b gates the rest.
