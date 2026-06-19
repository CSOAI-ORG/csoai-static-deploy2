# COAI Cross-Reference — Hive Datasets vs Manifest Gates
**Date:** 17 Jun 2026  
**Manifests:** `~/clawd/_intake/COAI_MANIFESTS/` (11 files, 10 unique hives — gaming-hive has v1+v2)  
**Datasets:** `~/.hive/data/` + `hive.yaml` + `.hive/config.yaml`

---

## Per-Hive Assessment

### 1. meok-aquaculture-hive
| Dimension | Status |
|-----------|--------|
| **COAI Status** | PASS — all 6 baseline gates ✓, all 4 hive-specific gates ✓ |
| **Data Readiness** | PENDING — no aquaculture/fish-specific datasets in `.hive/data/`. Only generic synthetic/CC0/government data. |
| **Compliance Coverage** | Full: AUDIT_TRAIL, ETHICAL_CHECK, OPEN_SOURCE, BFT_COUNCIL, MCP_STANDARD all declared true |
| **Gap** | Domain-specific training/eval datasets for fishkeeper.ai and koikeeper.ai not yet harvested |

---

### 2. meok-compliance-fleet
| Dimension | Status |
|-----------|--------|
| **COAI Status** | PASS — all 6 baseline gates ✓, all 4 hive-specific gates ✓ |
| **Data Readiness** | PASS (partial) — EU AI Act regulation + Code of Practice 2nd draft fetched OK. One SPARQL dataset failed (HTTP 406). |
| **Compliance Coverage** | Full. Core compliance reference data available. 14+ compliance MCPs declared. |
| **Gap** | SPARQL endpoint datastore for AI-Act-related datasets failed — needs retry or alternate endpoint. DORA framework data not yet harvested. |

---

### 3. meok-consumer-hive
| Dimension | Status |
|-----------|--------|
| **COAI Status** | PASS — all 6 baseline gates ✓, all 4 hive-specific gates ✓ |
| **Data Readiness** | PENDING — no consumer/UI-specific datasets. Synthetic corpora available but not tailored. |
| **Compliance Coverage** | Full gate coverage declared |
| **Gap** | No user-behaviour, A/B test, or conversion datasets. Consumer surface (meok.ai, meok-one) needs analytics pipeline. |

---

### 4. meok-distribution-hive
| Dimension | Status |
|-----------|--------|
| **COAI Status** | PASS — all 6 baseline gates ✓, all 4 hive-specific gates ✓ |
| **Data Readiness** | PENDING — no distribution/bridge/packaging datasets |
| **Compliance Coverage** | Full gate coverage declared |
| **Gap** | Package registry metadata (PyPI, npm), Smithery/Glama bridge logs not harvested. |

---

### 5. meok-gaming-hive (v2 authoritative)
| Dimension | Status |
|-----------|--------|
| **COAI Status** | PASS — all 6 baseline gates ✓, all 4 standard hive-specific gates ✓, plus 8 gaming-specific gates ✓ (NO_AUTOMATED_PLAY, NO_BOT_USAGE, NO_GTO_SOLVER_SELLING, NO_RTA, NO_DATA_SELLING, PLAYER_SOVEREIGNTY, BFT_FAULT_TOLERANCE, FINANCIAL_PRIVACY, NO_REGULATORY_BYPASS) |
| **Data Readiness** | PENDING — no MMO/game datasets. WoW, FFXIV, EVE, OSRS, PoE, Diablo IV, pokerhud all need data ingestion. |
| **Compliance Coverage** | Full + extra ethics gates for gaming sub-hives. 5 banned features documented. |
| **Gap** | Most gating-intensive hive. Needs gaming-domain datasets, poker hand data, and multi-agent sovereignties. v2 manifest is more complete than v1 — use v2 as canonical. |

---

### 6. meok-governance-hive
| Dimension | Status |
|-----------|--------|
| **COAI Status** | PASS — all 6 baseline gates ✓, all 4 hive-specific gates ✓ |
| **Data Readiness** | PASS — EU AI Act regulation + Code of Practice available as governance reference documents. 18 BFT councils declared. |
| **Compliance Coverage** | Full — governance framework backed by EU AI Act primary sources |
| **Gap** | Council decisions/attestation records not yet stored as versioned datasets |

---

### 7. meok-keystone-hive
| Dimension | Status |
|-----------|--------|
| **COAI Status** | PASS — all 6 baseline gates ✓, all 4 hive-specific gates ✓ |
| **Data Readiness** | PASS — foundation datasets available (UK government open data, CC0, synthetic). Ed25519 signer infrastructure in place. |
| **Compliance Coverage** | Full — sovereign-coordinator and x402-billing infrastructure operational |
| **Gap** | No dedicated keystone attestation dataset yet (signed cert index) |

---

### 8. meok-research-hive
| Dimension | Status |
|-----------|--------|
| **COAI Status** | PASS — all 6 baseline gates ✓, all 4 hive-specific gates ✓ |
| **Data Readiness** | PENDING — no patent data (openpatent-hive), no MoE model data (openmoe-ai), no OASF/mavis datasets |
| **Compliance Coverage** | Full gate coverage declared |
| **Gap** | Heavy data deficit — patent corpus, model weights/artifacts, research papers all unharvested |

---

### 9. meok-utility-fleet
| Dimension | Status |
|-----------|--------|
| **COAI Status** | PASS — all 6 baseline gates ✓, all 4 hive-specific gates ✓ |
| **Data Readiness** | PENDING — construction vertical listed in `hive.yaml` data_moat but no construction-specific data in `.hive/data/`. Healthcare FHIR data not yet harvested. Document comparison datasets missing. |
| **Compliance Coverage** | Full gate coverage declared |
| **Gap** | FHIR healthcare data, construction specs, document corpuses all need ingestion |

---

### 10. meok-verticals-hive
| Dimension | Status |
|-----------|--------|
| **COAI Status** | PASS — all 6 baseline gates ✓, all 4 hive-specific gates ✓ |
| **Data Readiness** | PENDING — construction and food_safety verticals listed in `hive.yaml` but no harvested datasets. All 13 vertical .ai domains lack domain-specific data. |
| **Compliance Coverage** | Full gate coverage declared |
| **Gap** | Largest data deficit — 13 vertical domains with zero dedicated datasets harvested |

---

## Summary

| Metric | Count | Details |
|--------|-------|---------|
| **Fully COAI-Compliant** | **3/10** | compliance-fleet, governance-hive, keystone-hive |
| **Pending Data** | **7/10** | aquaculture, consumer, distribution, gaming, research, utility, verticals |
| **Blocked** | **0/10** | No hive fails baseline gates; all manifests declare all gates true |

### Baseline Gate Pass Rate: **10/10** (all 6 baseline gates ✓ for all hives)
### Hive-Specific Gate Pass Rate: **10/10** (all standard 4 ✓, gaming adds 8 more ✓)
### Data Readiness Pass Rate: **3/10** (only 3 hives have meaningful datasets in `.hive/data/`)

---

## Gap Analysis for Sprint 2

### Critical (blocks Sprint 2 if unaddressed)

1. **Domain-specific data harvesting** — 7/10 hives have zero domain datasets. Need a data pipeline per hive:
   - **Sprint 2 priority order**: gaming-hive (highest gate complexity) → research-hive (openpatent) → aquaculture → verticals → utility → consumer → distribution

2. **EU AI Act dataset SPARQL failure** — 1 of 3 EU data sources failed (HTTP 406). Without this, compliance-fleet's EU AI Act data index is incomplete. Retry or switch to REST endpoint.

### Medium

3. **Gaming-hive v1 vs v2 dedup** — Two manifest files exist (`meok-gaming-hive.json` and `meok-gaming-hive-v2.json`). v2 is authoritative but v1's SHA-256 hash differs. Archive v1 to avoid confusion.

4. **Keystone attestation data** — Keystone-hive is the Ed25519 signer but has no signed attestation index dataset. Critical for all hives that depend on keystone for attestations.

### Low

5. **Synthetic corpus quality** — Current synthetic data (4 JSONL files across 3 days) is modest (532K rows per `hive.yaml`). Without domain-specific conditioning, it may not serve vertical hives effectively.

6. **Manifest uniformity** — All manifests share identical structure except gaming v2. Consider standardising a `data_requirements` and `compliance_frameworks` field in the manifest schema for future cross-ref automation.

---

## Sprint 1 SEAL Impact

**No blocking issues.** All 10 hives pass baseline COAI gates. The data readiness gap (7/10 pending) is a Sprint 2 concern, not a Sprint 1 blocker. The 3 FAIL email templates (day3/day14/day30 missing `{{keystone_cert_url}}`) are a higher-priority fix for the immediate batch-1 send.
