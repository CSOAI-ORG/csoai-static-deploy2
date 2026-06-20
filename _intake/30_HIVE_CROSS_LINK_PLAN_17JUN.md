# M29: 30-Hive Cross-Link Plan — 17 June 2026
**Scope:** Cross-link strategy for the 32-hive fleet, BFT councils, and COAI manifests

---

## Hive Clusters & Natural Affinity Groups

### Cluster A: Compliance & Governance (Core Backbone)
These hives enforce the EU AI Act + regulatory stack. Every vertical hive should link here.

| Hive | Domain | Should Link To |
|------|--------|----------------|
| **meok** | meok.ai | All compliance hives, proofof, councilof, csoai |
| **csoai** | csoai.org | meok, proofof, councilof, all compliance sub-hives |
| **proofof** | proofof.ai | meok, csoai, councilof, openpatent |
| **accountabilityof** | accountabilityof.ai | meok, csoai, transparencyof, safetyof |
| **dataprivacyof** | dataprivacyof.ai | meok, csoai, ethicalgovernanceof, transparencyof |
| **ethicalgovernanceof** | ethicalgovernanceof.ai | meok, csoai, biasdetectionof, transparencyof |
| **transparencyof** | transparencyof.ai | meok, csoai, ethicalgovernanceof, accountabilityof |
| **safetyof** | safetyof.ai | meok, csoai, agisafe, asisecurity |
| **biasdetectionof** | biasdetectionof.ai | meok, csoai, ethicalgovernanceof, dataprivacyof |

### Cluster B: Security & Safety
| Hive | Domain | Should Link To |
|------|--------|----------------|
| **agisafe** | agisafe.ai | safetyof, asisecurity, meok, councilof |
| **asisecurity** | asisecurity.ai | agisafe, safetyof, meok, csoai |

### Cluster C: Vertical Industry Hives (Revenue-Producing)
Each vertical hive should link to Cluster A for compliance + to sibling verticals.

| Hive | Domain | Should Link To |
|------|--------|----------------|
| **commercialvehicle** | commercialvehicle.ai | meok, csoai, muckaway, grabhire, planthire |
| **grabhire** | grabhire.ai | meok, csoai, muckaway, planthire, commercialvehicle |
| **muckaway** | muckaway.ai | meok, csoai, grabhire, planthire, commercialvehicle |
| **planthire** | planthire.ai | meok, csoai, grabhire, muckaway, commercialvehicle |
| **landlaw** | landlaw.ai | meok, csoai, dataprivacyof, proofof |
| **cobolbridge** | cobolbridge.ai | meok, csoai, openpatent, proofof |
| **openpatent** | openpatent.ai | meok, csoai, proofof, cobolbridge, openmoe |

### Cluster D: Data, Knowledge & Consumer
| Hive | Domain | Should Link To |
|------|--------|----------------|
| **diyhelp** | diyhelp.ai | meok (compliance for AI-generated DIY), loopfactory |
| **fishkeeper** | fishkeeper.ai | koikeeper, meok, optimobile |
| **koikeeper** | koikeeper.ai | fishkeeper, meok |
| **pokerhud** | pokerhud.ai | meok, optimobile |
| **optimobile** | optimobile.ai | meok, socialmediamanager, loopfactory |
| **openmoe** | openmoe.ai | meok, openpatent, csoai, councilof |

### Cluster E: Platform & Infrastructure
| Hive | Domain | Should Link To |
|------|--------|----------------|
| **loopfactory** | loopfactory.ai | meok, meok-compliance-gateway, openmcp |
| **meok-compliance-gateway** | (internal) | meok, loopfactory, openmcp |
| **openmcp** | (openMCP) | meok, all hives with MCP tools |
| **councilof** | councilof.ai | meok, csoai, all BFT-using hives |

### Cluster F: Social & Community
| Hive | Domain | Should Link To |
|------|--------|----------------|
| **socialmediamanager** | socialmediamanager.ai | meok, csoai, loopfactory |
| **suicidestop** | suicidestop.ai | meok, safetyof, ethicalgovernanceof |

### Cluster G: Labs & Internal
| Hive | Domain | Should Link To |
|------|--------|----------------|
| **sovereign-town** | (lab) | meok, councilof, sandbox |
| **sandbox** | (internal) | meok, councilof, sovereign-town |

---

## BFT Council Cross-Links

### Currently registered BFT councils (from `_intake/BFT_RATIFICATION_REPORTS/`):

| BFT Council | Type | Should Be Linked From |
|-------------|------|----------------------|
| d40-climatech-bft | Climate Tech | commercialvehicle, planthire |
| d40-cybersec-bft | Cybersecurity | asisecurity, agisafe |
| d40-edtech-bft | Education | meok, diyhelp |
| d40-foodtech-bft | Food Tech | fishkeeper, koikeeper |
| d40-insurtech-bft | InsurTech | all verticals |
| d40-proptech-bft | Proptech | landlaw |
| d40-spacetech-bft | Space Tech | openmoe |
| meok-aquaculture-hive-bft | Aquaculture | fishkeeper, koikeeper |
| meok-compliance-fleet-bft | Compliance | all Cluster A hives |
| meok-consumer-hive-bft | Consumer | diyhelp, optimobile |
| meok-conversion-funnel-bft | Conversion | socialmediamanager, optimobile |
| meok-cross-council-bft | Cross-Council | councilof |
| meok-d10-bft | D10 Special | meok, csoai |
| meok-distribution-hive-bft | Distribution | commercialvehicle, muckaway |
| meok-gaming-hive-bft | Gaming | pokerhud |
| meok-governance-hive-bft | Governance | all Cluster A |
| meok-keystone-hive-bft | Keystone | meok, csoai |
| meok-research-hive-bft | Research | openmoe, openpatent |
| meok-utility-fleet-bft | Utility | loopfactory, meok-compliance-gateway |
| meok-verticals-hive-bft | Verticals | all Cluster C |

**Cross-link rule:** Every hive whose domain matches a BFT council name should link to that council's ratification report/landing page.

---

## COAI Manifest Cross-Links

### COAI Manifests (from `_intake/COAI_MANIFESTS/`):

| Manifest | Focus | Should Link From |
|----------|-------|------------------|
| meok-aquaculture-hive.json | Aquaculture MCPs | fishkeeper, koikeeper |
| meok-compliance-fleet.json | Compliance MCP fleet | all Cluster A |
| meok-consumer-hive.json | Consumer AI products | diyhelp, optimobile |
| meok-distribution-hive.json | Distribution MCPs | commercialvehicle, muckaway |
| meok-gaming-hive.json | Gaming MCPs | pokerhud |
| meok-gaming-hive-v2.json | Gaming MCPs v2 | pokerhud |
| meok-governance-hive.json | Governance MCPs | councilof, ethicalgovernanceof |
| meok-keystone-hive.json | Keystone MCPs | meok, csoai |
| meok-research-hive.json | Research MCPs | openmoe, openpatent |
| meok-utility-fleet.json | Utility MCPs | loopfactory |
| meok-verticals-hive.json | Vertical MCPs | all Cluster C |

**Cross-link rule:** Each hive should link to the COAI manifest covering its domain for discoverability.

---

## Priority Cross-Link Implementation

### Phase 1 (Immediate — fix missing sibling links)
1. All Article 50 pages → link to each other (see M19)
2. meok.ai homepage → link to `/article-50/` and `/eu-code-of-practice`
3. csoai.org → add meok.ai and proofof.ai links in footer
4. openpatent.ai → add JSON-LD + link to meok.ai and csoai.org

### Phase 2 (Each hive homepage)
5. Every `*.ai` domain → add a "Compliance by MEOK" footer link
6. Every `*.ai` domain → add a "Certified by CSOAI" footer link
7. Vertical hives → add BFT council badge with link to ratification report

### Phase 3 (COAI + BFT mesh)
8. Add COAI manifest links to each hive's landing page
9. Add BFT council links to corresponding hive documentation
10. councilof.ai → become the hub listing all BFT councils

---

## Cross-Link Architecture Diagram

```
                    ┌──────────────────────────────────────────┐
                    │              councilof.ai                │
                    │         (BFT Governance Hub)             │
                    └────┬──────┬──────┬──────┬──────┬────────┘
                         │      │      │      │      │
         ┌───────────────┘      │      │      │      └───────────────┐
         ▼                       ▼      ▼      ▼                      ▼
   ┌──────────┐          ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
   │  meok.ai │◄────────►│csoai.org │ │proofof.ai│ │openmoe.ai│ │openpatent│
   │(Central) │          │(Watchdog)│ │(Registry)│ │(Research)│ │ .ai (IP) │
   └────┬─────┘          └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘
        │                     │            │            │            │
        ▼                     ▼            ▼            ▼            ▼
   ┌───────────────────────────────────────────────────────────────────────┐
   │                   Vertical Hive Fleet (Clusters C-F)                  │
   │  grabhire  muckaway  planthire  landlaw  fishkeeper  koikeeper  ...  │
   └───────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
                   ┌─────────────────────────┐
                   │   BFT Council Reports    │
                   │   COAI Manifests         │
                   └─────────────────────────┘
```

Each vertical hive → links to meok.ai + csoai.org + councilof.ai + its BFT council + its COAI manifest.
meok.ai → links to all hives.
csoai.org → certifies all hives.
councilof.ai → convenes BFT councils for all hives.
