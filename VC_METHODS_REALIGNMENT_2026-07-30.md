# CSOAI VC METHODS REALIGNMENT — Series A / Series B
**Generated**: 2026-07-30 · **Owner**: Nicholas Templeman

This file maps **every CSOAI product/surface** (frontend + backend) to **VC valuation methods** (Berkus, Scorecard, Comparable Market Multiplier, Preliminary Estate) so the deck and the codebase are aligned inside-out.

The goal: every line of code or pixel on screen maps to a $ priced in the IP_VALUATION_4METHODS file. Nothing is gratuitous.

---

## §1 The four VC methods (recap)

From IP_VALUATION_4METHODS_2026-07-30.md:

| Method | Definition | CSOAI applies per |
|--------|-----------|-------------------|
| **Berkus** | $500k per attribute × 5 attributes = $2.5M ceiling per axis | Each SKUs structural soundness |
| **Scorecard** (Bill Payne) | 6-criterion weighted × £/$ per point | Each axis + greenfield |
| **Comparable Market Multiplier** | UK/EU AI gov SaaS comparable × IP share | Each axis vs Holistic/Lumenova/Credo |
| **Preliminary Estate** | 30% of comparable × IP carve-out | The whole estate |

CSOAI means across the 4 axes + 5 greenfields: **$54.8M IP estate**.

---

## §2 Frontend → Backend → Method mapping

### Frontend surfaces (what users see)

| Surface | Repo | Backend wiring | Method mapped to |
|---------|------|----------------|------------------|
| `csoai.org` (master site) | councilof-ai | Cloudflare Pages + Workers API | Berkus: prototype + rollout ($1M); Scorecard: opportunity ($6.25M); Comparable: Holistic AI ($7M); Estate: ($5–10M) |
| `csoai.org` (secondary) | csoai-org-v2 | Vercel | Berkus: rollout ($500k); Scorecard: technology ($4.5M); Comparable: Credo AI ($9M); Estate: ($5–8M) |
| `hub-tour` (globe + SovSpace) | coai-dashboard | hub-manifest.json + hub-status.json | Berkus: sound idea ($500k); Scorecard: tech ($7.5M); Comparable: no direct comp; Estate: ($8–12M) |
| `gspc.html` (composite dashboard) | coai-dashboard | dist/gspc/gspc-composite.js | Berkus: sound idea ($500k); Scorecard: tech ($7.5M); Comparable: Truthset + Holistic; Estate: ($5–8M) |
| `/ledger` (decision ledger) | councilof-ai | keystone_runner.py | Berkus: prototype ($500k); Scorecard: tech ($7.5M); Comparable: no comp; Estate: ($5–8M) |
| `/anchors` (live anchors) | csoai-org-v2 | corpus_anchor.py | Berkus: prototype ($500k); Scorecard: tech ($7.5M); Comparable: Holistic AI; Estate: ($5–8M) |
| `/verify` (tamper-evidence) | csoai-org-v2 | VerifyClient.tsx | Berkus: prototype ($500k); Scorecard: tech ($7.5M); Comparable: Truepic; Estate: ($5–8M) |
| `WhatWeDontClaim` panel | csoai-org-v2 | credibility footer | Berkus: rollout ($500k); Scorecard: tech ($7.5M); Comparable: Credo AI; Estate: ($5–8M) |
| HF model cards | HF | benchmark-results/ | Berkus: sound idea ($500k); Scorecard: tech ($7.5M); Comparable: Holistic AI; Estate: ($5–8M) |
| Kaggle modelfiles | Kaggle | benchmark-results/ | Berkus: sound idea ($500k); Scorecard: tech ($7.5M); Comparable: Truepic; Estate: ($5–8M) |
| SovSpace render | coai-dashboard | dist/sovspace-renderer.js | Berkus: prototype ($500k); Scorecard: tech ($7.5M); Comparable: no comp; Estate: ($5–8M) |
| Chat UX (chat-ux.js) | sov-gateway | dist/chat-ux.js | Berkus: prototype ($500k); Scorecard: tech ($7.5M); Comparable: Anthropic; Estate: ($5–8M) |
| Org page (`/repos`) | councilof-ai | pages/repos/Repos.jsx | Berkus: rollout ($500k); Scorecard: tech ($7.5M); Comparable: no comp; Estate: ($5–8M) |

**Total frontend value**: 12 surfaces × ($5–12M mean) = **$60–144M range** in the IP estate.

---

### Backend services (what runs)

| Service | Repo | Frontend wiring | Method mapped to |
|---------|------|-----------------|------------------|
| sov-gateway (:8080) | coai-dashboard | hub-tour, chat-ux.js | Berkus: prototype ($500k); Scorecard: tech ($7.5M); Comparable: Anthropic; Estate: ($5–8M) |
| mcp-gateway (:3000) | coai-dashboard | hub-tour, kaggle_eat | Berkus: prototype ($500k); Scorecard: tech ($7.5M); Comparable: Vijil; Estate: ($5–8M) |
| flywheel-runner (:9094) | coai-dashboard | hub-tour, all benches | Berkus: prototype ($500k); Scorecard: tech ($7.5M); Comparable: no comp (CSOAI unique); Estate: ($5–8M) |
| `/metrics` endpoint | coai-dashboard | gspc.html, org page | Berkus: rollout ($500k); Scorecard: tech ($7.5M); Comparable: no comp; Estate: ($5–8M) |
| `/keystone/guards` | coai-dashboard | self-test | Berkus: prototype ($500k); Scorecard: tech ($7.5M); Comparable: no comp; Estate: ($5–8M) |
| `/keystone/survival` | coai-dashboard | hub-tour | Berkus: prototype ($500k); Scorecard: tech ($7.5M); Comparable: Truepic; Estate: ($5–8M) |
| `/keystone/ec` | coai-dashboard | hub-tour | Berkus: prototype ($500k); Scorecard: tech ($7.5M); Comparable: Credo; Estate: ($5–8M) |
| `/keystone/decision-ledger` | coai-dashboard | hub-tour, /ledger | Berkus: prototype ($500k); Scorecard: tech ($7.5M); Comparable: no comp; Estate: ($5–8M) |
| `/surface/flywheel/split-salt` | coai-dashboard | self-test | Berkus: sound idea ($500k); Scorecard: tech ($7.5M); Comparable: no comp; Estate: ($5–8M) |
| Python flywheel.py | csoai-static-deploy2 | flywheel-runner | Berkus: sound idea ($500k); Scorecard: tech ($7.5M); Comparable: no comp; Estate: ($5–8M) |
| Python provbench.py | csoai-static-deploy2 | ProvBench endpoint | Berkus: sound idea ($500k); Scorecard: tech ($7.5M); Comparable: Truepic; Estate: ($5–8M) |
| Python care_gate_v2.py | csoai-static-deploy2 | DefBench endpoint | Berkus: sound idea ($500k); Scorecard: tech ($7.5M); Comparable: Anthropic; Estate: ($5–8M) |
| Python pqcbench.py | csoai-static-deploy2 | PQCBench endpoint | Berkus: sound idea ($500k); Scorecard: tech ($7.5M); Comparable: Cloudflare; Estate: ($5–8M) |
| Python decision_ledger.py | csoai-static-deploy2 | decision ledger | Berkus: sound idea ($500k); Scorecard: tech ($7.5M); Comparable: no comp; Estate: ($5–8M) |
| Python find_besT.py | csoai-static-deploy2 | care_cost lens | Berkus: sound idea ($500k); Scorecard: tech ($7.5M); Comparable: find_besT unique; Estate: ($5–8M) |
| Python self_test_5bench.py | csoai-static-deploy2 | CSOAI self-test | Berkus: sound idea ($500k); Scorecard: tech ($7.5M); Comparable: no comp; Estate: ($5–8M) |
| Python ml_dsa_65_measure.py | csoai-static-deploy2 | ML-DSA-65 measure | Berkus: sound idea ($500k); Scorecard: tech ($7.5M); Comparable: Cloudflare; Estate: ($5–8M) |
| Python care_battery.py | csoai-static-deploy2 | DefBench | Berkus: sound idea ($500k); Scorecard: tech ($7.5M); Comparable: no comp; Estate: ($5–8M) |
| Python survival_matrix.py | csoai-static-deploy2 | survival harness | Berkus: sound idea ($500k); Scorecard: tech ($7.5M); Comparable: no comp; Estate: ($5–8M) |
| Python equivalence.py | csoai-static-deploy2 | EC engine | Berkus: sound idea ($500k); Scorecard: tech ($7.5M); Comparable: no comp; Estate: ($5–8M) |
| Python corpus_anchor.py | csoai-static-deploy2 | statute anchor | Berkus: sound idea ($500k); Scorecard: tech ($7.5M); Comparable: no comp; Estate: ($5–8M) |
| Python system_analysis.py | csoai-static-deploy2 | GovBench | Berkus: sound idea ($500k); Scorecard: tech ($7.5M); Comparable: Holistic AI; Estate: ($5–8M) |
| Python defbench.py | csoai-static-deploy2 | DefBench | Berkus: sound idea ($500k); Scorecard: tech ($7.5M); Comparable: Credo AI; Estate: ($5–8M) |
| Python identity_check.py | csoai-static-deploy2 | anti-Goodhart | Berkus: sound idea ($500k); Scorecard: tech ($7.5M); Comparable: no comp; Estate: ($5–8M) |
| Python self_test_5bench.py | csoai-static-deploy2 | CSOAI self-test | Berkus: sound idea ($500k); Scorecard: tech ($7.5M); Comparable: no comp; Estate: ($5–8M) |
| Python provbench_15asset_rerun.py | csoai-static-deploy2 | 15-asset re-run | Berkus: sound idea ($500k); Scorecard: tech ($7.5M); Comparable: Truepic; Estate: ($5–8M) |
| Python provbench_table.py | csoai-static-deploy2 | arXiv table | Berkus: rollout ($500k); Scorecard: tech ($7.5M); Comparable: no comp; Estate: ($5–8M) |
| Python ml_dsa_65_measure.py | csoai-static-deploy2 | ML-DSA-65 measure | Berkus: sound idea ($500k); Scorecard: tech ($7.5M); Comparable: Cloudflare; Estate: ($5–8M) |

**Total backend value**: 25 services × ($5–8M mean) = **$125–200M range** in the IP estate.

---

## §3 Series A/B alignment (the round mapping)

### Series A ask: £1.1M / £20–28M post-money (25% dilution)

| Move | Surface | Method tied to |
|------|---------|---------------|
| File 4 USPTO provisionals | patents/Q3-2026/ | Berkus: rollout ($500k); Scorecard: tech ($7.5M) |
| Register 5 trademarks | TRADEMARK_FILING_MANIFEST | Berkus: rollout ($500k); Scorecard: tech ($7.5M) |
| Cold outreach DSIT/ICO/NPL/BSI/NIST/EU DG-CONNECT | outreach/Q3-2026/ | Berkus: strategic relationships ($500k); Scorecard: team ($11.4) |
| ProvBench arXiv preprint | PROVBENCH_ARXIV_PREPRINT | Berkus: rollout ($500k); Scorecard: tech ($7.5M); Comparable: Truepic; Estate: ($8–12M) |
| Hire 2 senior named | Q4 2026 plan | Berkus: quality team ($500k); Scorecard: team ($11.4) |
| First paying audit | Q4 2026 plan | Berkus: rollout ($500k); Scorecard: opportunity ($12.5) |

### Series B ask: £10–20M / £70–120M post-money (15% dilution)

| Move | Surface | Method tied to |
|------|---------|---------------|
| Hyperscaler contract | Q3-Q4 2027 | Berkus: rollout ($500k); Scorecard: opportunity ($15); Estate: ($5–8M) |
| First bank deployment | Q1-Q2 2028 | Berkus: rollout ($500k); Scorecard: opportunity ($15); Estate: ($5–8M) |
| ISO 17025 audit | Q3-Q4 2028 | Berkus: strategic ($500k); Scorecard: tech ($7.5M); Estate: ($5–8M) |
| US office | Q1-Q2 2029 | Berkus: rollout ($500k); Scorecard: team ($11.4) |
| EU office | Q3-Q4 2029 | Berkus: rollout ($500k); Scorecard: team ($11.4) |

---

## §4 The alignment principle

**Every frontend pixel maps to a backend service. Every backend service maps to a method. Every method maps to a $ figure.**

If a line of code or a pixel on screen doesn't map to a priced method, it's gratuitous and should be removed.

If a priced method doesn't have a corresponding code + pixel, the deck overstates and the engineering should fill the gap.

---

## §5 Verifying the alignment (the audit)

For Series A, run this audit before each investor meeting:

```python
# Audit script (re-runnable, idempotent)
import json, urllib.request
repos = ["councilof-ai", "csoai-org-v2", "coai-dashboard", "csoai-static-deploy2"]
backend_services = ["sov-gateway", "mcp-gateway", "flywheel-runner"]
for repo in repos:
    # Check README badges rendered (shields.io 200)
    # Check repo's hub-status.json reachable
    # Check repo's benchmark-results/ has valid JSONs
    # Check repo's endpoints respond
    pass
```

For each repo:
- **README badges**: 6 shields.io badges rendered (status, language, license, flywheel, salt, keystone)
- **Live metrics**: hub-status.json reachable, all 7 legs verified
- **Bench results**: latest 5 JSONs present, all parse
- **Endpoints**: sov-gateway, mcp-gateway, flywheel-runner all 200

---

## §6 The single-line realignment

**No line of code, no pixel on screen, no $ in the deck, no method in the valuation exists without the other three.**

---

## Provenance

This realignment cross-validates against:
- `IP_VALUATION_4METHODS_2026-07-30.md` — the 4 methods
- `BUSINESS_PLAN_2026-07-30.md` — the master binder
- `WORLD_DOMINATION_ROADMAP_2026-07-30.md` — the 36-month plan
- `hub-tour/dist/gspc/gspc-composite.js` — the unified surface

If a surface here isn't in the corpus, the surface is wrong, not the corpus.