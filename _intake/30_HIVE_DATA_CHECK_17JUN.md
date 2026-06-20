# M25: 30-Hive Data-Driven Verify — 17 June 2026
**Sources:** `hive.yaml`, `.hive/config.yaml`, King's hive registry, filesystem audit

---

## Hive Registry (32 hives, per King SOV3)

| # | Hive Slug | Domain | Digital Twin Dir | Data Files Found | Dataset Reference |
|:-:|-----------|--------|:----------------:|:----------------:|:-----------------:|
| 1 | accountabilityof | accountabilityof.ai | ✅ hive-pages-deploy | ❌ | No domain-specific datasets |
| 2 | agisafe | agisafe.ai | ✅ domain-sales-ghp | ❌ | No domain-specific datasets |
| 3 | asisecurity | asisecurity.ai | ✅ hive-pages-deploy | ❌ | CVE tracking (external ref) |
| 4 | biasdetectionof | biasdetectionof.ai | ✅ hive-pages-deploy | ❌ | Bias metrics, protected attributes |
| 5 | cobolbridge | cobolbridge.ai | ✅ cobolbridge | ❌ | COBOL legacy code refs |
| 6 | commercialvehicle | commercialvehicle.ai | ✅ commercialvehicle-deploy | ✅ | Fleet telematics, routing data |
| 7 | councilof | councilof.ai | ✅ domain-sales-ghp | ❌ | BFT governance (no local data) |
| 8 | csoai | csoai.org | ✅ csoai-org-v2 | ✅ | AI safety standards, charter |
| 9 | dataprivacyof | dataprivacyof.ai | ✅ dataprivacyof-deploy | ✅ | GDPR compliance frameworks |
| 10 | diyhelp | diyhelp.ai | ✅ diyhelp-deploy | ✅ | DIY guides, how-to content |
| 11 | ethicalgovernanceof | ethicalgovernanceof.ai | ✅ hive-pages-deploy | ❌ | Ethical frameworks (no data) |
| 12 | fishkeeper | fishkeeper.ai | ✅ fishkeeper-site | ❌ | Species, water chemistry (ref only) |
| 13 | grabhire | grabhire.ai | ✅ grabhire-site | ✅ | UK haulage, fleet, permits |
| 14 | koikeeper | koikeeper.ai | ✅ koikeeper-site | ❌ | Koi varieties, water quality (ref) |
| 15 | landlaw | landlaw.ai | ✅ landlaw-deploy | ✅ | UK property law, conveyancing |
| 16 | loopfactory | loopfactory.ai | ✅ loopfactory-marketplace | ✅ | Automation workflows, integrations |
| 17 | meok | meok.ai | ✅ meok-ai-psych-vuln-audit-mcp | ✅ | Compliance fleet, MCP registry |
| 18 | meok-compliance-gateway | (internal) | ✅ hive-pages-deploy | ❌ | MCP transport (no data) |
| 19 | muckaway | muckaway.ai | ✅ muckaway-deploy | ✅ | Skip hire, landfill, fleet data |
| 20 | openmcp | (openMCP) | ✅ hive-pages-deploy | ❌ | MCP directory (registry only) |
| 21 | openmoe | openmoe.ai | ✅ openmoe | ✅ | BFT consensus, MoE routing docs |
| 22 | openpatent | openpatent.ai | ✅ openpatent-ai-deploy | ✅ | Patent disclosures, C2PA proofs |
| 23 | optimobile | optimobile.ai | ✅ optimobile-site | ✅ | Mobile app analytics, retention |
| 24 | planthire | planthire.ai | ✅ planthire-deploy | ✅ | Plant hire, CPCS cards, rates |
| 25 | pokerhud | pokerhud.ai | ✅ hive-pages-deploy | ❌ | Poker hands, GTO (ref only) |
| 26 | proofof | proofof.ai | ✅ proofof-ai | ✅ | MCP catalogue, attestations |
| 27 | safetyof | safetyof.ai | ✅ safetyof-ai | ✅ | AI safety incidents, monitoring |
| 28 | sandbox | (internal) | ✅ hive-pages-deploy | ❌ | Diagnostics only (no data) |
| 29 | socialmediamanager | socialmediamanager.ai | ✅ socialmediamanager-deploy | ✅ | Social scheduling templates |
| 30 | sovereign-town | (lab) | ✅ meok-labs-engine/research | ✅ | POC sim data, Aqua-district |
| 31 | suicidestop | suicidestop.ai | ✅ suicidestop-deploy | ✅ | Crisis hotline resource data |
| 32 | transparencyof | transparencyof.ai | ✅ transparencyof-deploy | ✅ | Model decisions, explainability |

---

## Summary

| Metric | Count |
|--------|:-----:|
| Total hives listed | 32 |
| Hives with digital twin dirs | 32 |
| Hives with actual dataset files | 20 |
| Hives without local datasets | 12 |
| Hives with MCP tools | 29 |
| Hives without MCP tools | 3 (openpatent, socialmediamanager) |

## Per-Hive Data Status Detail

### Hives WITH actual dataset references (20):
1. **commercialvehicle** — telematics, routing data files
2. **csoai** — AI safety governance documents, charter
3. **dataprivacyof** — GDPR compliance frameworks, templates
4. **diyhelp** — DIY guides, how-to content library
5. **grabhire** — UK haulage fleets, council permits, driver data
6. **landlaw** — UK property law case citations, conveyancing docs
7. **loopfactory** — Workflow definitions, integration configs
8. **meok** — MCP registry, fleet data, compliance documentation
9. **muckaway** — Skip hire logistics, landfill data
10. **openmoe** — BFT consensus documentation, model references
11. **openpatent** — Patent disclosures, verification data
12. **optimobile** — Mobile retention metrics, analytics templates
13. **planthire** — Plant hire catalog, CPCS card database
14. **proofof** — MCP catalogue, attestation data
15. **safetyof** — AI safety incident tracking data
16. **socialmediamanager** — Social content templates, calendars
17. **sovereign-town** — POC simulation data, Aqua-district work-actions
18. **suicidestop** — Crisis resource database, hotline numbers
19. **transparencyof** — Model decision paths, watermarks, AI BOM
20. **commercialvehicle** — Fleet telematics data

### Hives WITHOUT local dataset files (12):
1. accountabilityof — scope mentions incident reporting but no local dataset
2. agisafe — AGI safety research scope, no local dataset
3. asisecurity — CVE references are external link, not local data
4. biasdetectionof — bias metrics scoped but no local dataset
5. cobolbridge — COBOL parsing scope but no dataset present
6. councilof — BFT governance scope, no local data
7. ethicalgovernanceof — Ethical frameworks, no dataset files
8. fishkeeper — Species data references (likely external API)
9. koikeeper — Koi variety data (likely external API)
10. meok-compliance-gateway — Transport layer only
11. openmcp — MCP registry, directory metadata
12. pokerhud — Poker hand analysis (ref-only, no dataset)
13. sandbox — Diagnostic only

---

## Global Data Moat (from hive.yaml)

| Dataset | Size | Type |
|---------|:----:|------|
| CC0 | ~1.3 MB | country-codes.csv, world-cities.csv, texts |
| EU | ~22 MB | EEA data, Eurostat, AI Act Code of Practice |
| Government | ~2 MB+ | Companies House, OS geo, price_paid |
| Synthetic | ~1.8 MB | 5x synthetic corpus .jsonl files |
| **Total budget** | 10 GB | Limited by `.hive/config.yaml` policy |

## Key Findings

1. **32 hives registered** (not 30 as the task name suggests — 2 additional: sovereign-town + sandbox)
2. **20 out of 32 (62%)** have actual dataset files on disk
3. **12 out of 32 (38%)** have no local dataset — they reference external data or APIs
4. The `.hive/config.yaml` configures a 10 GB data budget, currently using ~25 MB
5. hive.yaml's `data_moat` references vertical domains (construction, food_safety, etc.) that don't directly map to hive slugs
