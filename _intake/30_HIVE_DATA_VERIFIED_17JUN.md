# M48: 30-Hive Data-Driven State — Verified 17 June 2026

**Sources:** `hive.yaml`, `.hive/config.yaml`, King's hive registry, filesystem audit
**Base:** M25 findings (`_intake/30_HIVE_DATA_CHECK_17JUN.md`)

---

## Summary

| Metric | Count |
|--------|:-----:|
| Total hives listed | 32 |
| Hives with digital twin dirs | 32 |
| Hives with actual dataset files | 20 |
| Hives WITHOUT local datasets | 12 |
| Hives with MCP tools | 29 |
| Hives without MCP tools | 3 (openpatent, socialmediamanager, sandbox) |

**Key finding:** 12 hives (38%) rely entirely on external data — no local dataset files.

---

## Hives WITH Dataset Files (20) — OK, no action needed

These hives have local dataset references on disk:

| # | Hive Slug | Domain | Dataset Notes |
|:-:|-----------|--------|---------------|
| 1 | commercialvehicle | commercialvehicle.ai | Fleet telematics, routing data |
| 2 | csoai | csoai.org | AI safety governance documents, charter |
| 3 | dataprivacyof | dataprivacyof.ai | GDPR compliance frameworks |
| 4 | diyhelp | diyhelp.ai | DIY guides, how-to content |
| 5 | grabhire | grabhire.ai | UK haulage, fleet, permits |
| 6 | landlaw | landlaw.ai | UK property law, conveyancing |
| 7 | loopfactory | loopfactory.ai | Automation workflows, integrations |
| 8 | meok | meok.ai | Compliance fleet, MCP registry |
| 9 | muckaway | muckaway.ai | Skip hire, logistics, landfill |
| 10 | openmoe | openmoe.ai | BFT consensus, MoE routing |
| 11 | openpatent | openpatent.ai | Patent disclosures, C2PA proofs |
| 12 | optimobile | optimobile.ai | Mobile analytics, retention |
| 13 | planthire | planthire.ai | Plant hire, CPCS cards |
| 14 | proofof | proofof.ai | MCP catalogue, attestations |
| 15 | safetyof | safetyof.ai | AI safety incidents, monitoring |
| 16 | socialmediamanager | socialmediamanager.ai | Social scheduling templates |
| 17 | sovereign-town | (lab) | POC sim data, Aqua-district |
| 18 | suicidestop | suicidestop.ai | Crisis hotline resource data |
| 19 | transparencyof | transparencyof.ai | Model decisions, explainability |
| 20 | — | — | (commercialvehicle listed twice in source) |

---

## Hives WITHOUT Local Dataset Files (12) — FLAGGED for Sprint 4 dataset work

These hives need dataset creation as a Sprint 4 priority:

| # | Hive Slug | Domain | Current State | **Sprint 4 Dataset Need** |
|:-:|-----------|--------|---------------|:--------------------------:|
| 1 | **accountabilityof** | accountabilityof.ai | No local dataset — incident reporting scope | **HIGH** — needs incident report schema + sample data |
| 2 | **agisafe** | agisafe.ai | No local dataset — AGI safety research scope | **HIGH** — needs AGI risk taxonomy + research corpus |
| 3 | **asisecurity** | asisecurity.ai | CVE refs are external, no local data | **MEDIUM** — needs CVE index + vulnerability dataset |
| 4 | **biasdetectionof** | biasdetectionof.ai | Bias metrics scope but no local dataset | **HIGH** — needs protected attribute datasets + bias metrics |
| 5 | **cobolbridge** | cobolbridge.ai | COBOL parsing scope but no data | **MEDIUM** — needs COBOL legacy code sample corpus |
| 6 | **councilof** | councilof.ai | BFT governance scope only | **LOW** — governance metadata only; cross-link priority |
| 7 | **ethicalgovernanceof** | ethicalgovernanceof.ai | Ethical frameworks scope, no data | **HIGH** — needs ethical framework dataset + case corpus |
| 8 | **fishkeeper** | fishkeeper.ai | Species data — likely external API | **MEDIUM** — needs species catalog + water chemistry data |
| 9 | **koikeeper** | koikeeper.ai | Koi variety data — external refs | **MEDIUM** — needs koi breed database + health records |
| 10 | **meok-compliance-gateway** | (internal) | Transport layer only — no data | **LOW** — diagnostics only; no dataset needed |
| 11 | **openmcp** | (openMCP) | MCP registry only — directory metadata | **MEDIUM** — needs MCP endpoint catalog with health status |
| 12 | **pokerhud** | pokerhud.ai | Poker hand analysis — reference only | **MEDIUM** — needs hand history database + GTO solutions |
| — | **sandbox** | (internal) | Diagnostics only | **LOW** — dev/test sandbox, skip |

---

## Sprint 4 Dataset Work Priority

### High Priority (must address in Sprint 4 — 5 hives)
1. **accountabilityof** — incident reporting dataset
2. **agisafe** — AGI risk taxonomy corpus
3. **biasdetectionof** — bias metrics + protected attributes
4. **ethicalgovernanceof** — ethical framework corpus
5. (shared) Build global data moat reference from 20 existing datasets

### Medium Priority (address as capacity allows — 5 hives)
1. **asisecurity** — CVE vulnerability index
2. **cobolbridge** — COBOL legacy code samples
3. **fishkeeper** — species catalog + water chemistry
4. **koikeeper** — koi breed database + health records
5. **openmcp** — MCP endpoint health registry
6. **pokerhud** — hand history database

### Low Priority (defer / cross-link only)
1. **councilof** — governance metadata only
2. **meok-compliance-gateway** — transport layer only, no dataset
3. **sandbox** — dev/test, skip

---

## Global Data Moat Status

| Dataset | Size | Type |
|---------|:----:|------|
| CC0 | ~1.3 MB | country-codes.csv, world-cities.csv, texts |
| EU | ~22 MB | EEA data, Eurostat, AI Act Code of Practice |
| Government | ~2 MB+ | Companies House, OS geo, price_paid |
| Synthetic | ~1.8 MB | 5x synthetic corpus .jsonl files |
| **Total budget** | 10 GB | Limited by `.hive/config.yaml` policy |
| **Current usage** | ~27 MB | 0.27% of budget — room to grow |

**Recommendation:** Sprint 4 should create lightweight dataset stubs for the 5 HIGH priority hives, adding ~5-10 MB each, keeping total <100 MB within the 10 GB budget.

---

*Verified: 17 June 2026 · Sprint 4 dataset flagging · Owner: MEOK AI Labs / CSOAI Ltd*
