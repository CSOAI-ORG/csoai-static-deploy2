# Legal & Professional Services Data Sources — CSOAI Hive Dimension

> **Research Date**: 2025-07-10
> **Purpose**: Free/open data sources for the CSOAI Legal/Professional Services Hive
> **Coverage**: Case law, court records, legal analytics, law firm data, IP litigation, regulatory enforcement, arbitration, human rights, and trade dispute data

---

## Table of Contents

1. [U.S. Case Law](#1-us-case-law)
   - 1.1 [CourtListener (Free Law Project)](#11-courtlistener-free-law-project)
   - 1.2 [Harvard Caselaw Access Project (CAP)](#12-harvard-caselaw-access-project-cap)
2. [U.S. Federal Court Records](#2-us-federal-court-records)
   - 2.1 [PACER & RECAP](#21-pacer--recap)
   - 2.2 [SEC EDGAR / SEC-API](#22-sec-edgar--sec-api)
3. [UK & Commonwealth Legislation & Case Law](#3-uk--commonwealth-legislation--case-law)
   - 3.1 [UK legislation.gov.uk](#31-uk-legislationgovuk)
   - 3.2 [BAILII](#32-bailii)
   - 3.3 [CanLII (Canada)](#33-canlii-canada)
4. [European Union Legal Data](#4-european-union-legal-data)
   - 4.1 [EUR-Lex & Cellar](#41-eur-lex--cellar)
   - 4.2 [IUROPA CJEU Database](#42-iuropa-cjeu-database)
5. [Intellectual Property Data](#5-intellectual-property-data)
   - 5.1 [WIPO IP Statistics Data Center](#51-wipo-ip-statistics-data-center)
   - 5.2 [USPTO Open Data Portal & Bulk Data](#52-uspto-open-data-portal--bulk-data)
   - 5.3 [EUIPO Open Data](#53-euipo-open-data)
   - 5.4 [IP Australia (IPGOD/IPGOLD)](#54-ip-australia-ipgodipgold)
6. [IP Litigation & Patent Analytics](#6-ip-litigation--patent-analytics)
   - 6.1 [USPTO Patent Litigation API](#61-uspto-patent-litigation-api)
   - 6.2 [EPO Open Patent Services (OPS)](#62-epo-open-patent-services-ops)
7. [Regulatory Enforcement Actions](#7-regulatory-enforcement-actions)
   - 7.1 [SEC Enforcement Actions](#71-sec-enforcement-actions)
   - 7.2 [FINRA Disciplinary Actions](#72-finra-disciplinary-actions)
   - 7.3 [FTC Enforcement Actions](#73-ftc-enforcement-actions)
   - 7.4 [DOJ Open Data](#74-doj-open-data)
8. [State Bar & Attorney Discipline](#8-state-bar--attorney-discipline)
9. [Arbitration & Dispute Resolution](#9-arbitration--dispute-resolution)
   - 9.1 [UNCTAD ISDS Navigator](#91-unctad-isds-navigator)
   - 9.2 [ICSID Case Law Database](#92-icsid-case-law-database)
   - 9.3 [italaw](#93-italaw)
   - 9.4 [LCIA Challenge Decision Database](#94-lcia-challenge-decision-database)
10. [Human Rights Case Databases](#10-human-rights-case-databases)
    - 10.1 [ECtHR HUDOC](#101-ecthr-hudoc)
    - 10.2 [African Human Rights Case Law Analyser](#102-african-human-rights-case-law-analyser)
    - 10.3 [Inter-American Human Rights (IACHR)](#103-inter-american-human-rights-iachr)
11. [WTO & Trade Disputes](#11-wto--trade-disputes)
    - 11.1 [WTO Dispute Settlement Documents](#111-wto-dispute-settlement-documents)
12. [Law Firm & Legal Industry Data](#12-law-firm--legal-industry-data)
    - 12.1 [ALM Rankings (Am Law, Global 200)](#121-alm-rankings-am-law-global-200)
    - 12.2 [ABA Legal Technology Survey](#122-aba-legal-technology-survey)
    - 12.3 [Vault / Firsthand Rankings](#123-vault--firsthand-rankings)

---

## 1. U.S. Case Law

### 1.1 CourtListener (Free Law Project)

| Attribute | Detail |
|-----------|--------|
| **Name** | CourtListener by Free Law Project |
| **URL** | https://www.courtlistener.com/ |
| **API Docs** | https://www.courtlistener.com/help/api/ |
| **Format** | REST API (JSON), Bulk CSV, PostgreSQL replication, Webhooks |
| **License** | Free of known copyright restrictions; some membership tiers for high-volume access [^1697^] |
| **API/Bulk Access** | Multiple tiers: Database replication (instant), Bulk CSV dumps (~54GB compressed, ~350GB decompressed), REST API, Webhooks, MCP Server [^1688^] [^1697^] |
| **Coverage** | ~9+ million U.S. federal and state court opinions from 360+ years; includes Harvard CAP data + additional cases scraped from 2,000+ courts |
| **CSOAI Use Case** | Foundation U.S. case law dimension; citation network analysis, judge analytics, oral argument analysis, financial disclosure integration |

**Data Types Available:** [^1688^]
- Case law (opinions, clusters, citations map, parentheticals)
- Dockets (millions of rows with high-level case info)
- Judges database (32,336+ financial disclosures, 1,901,720+ investments)
- Oral arguments (largest database in the world)
- Financial disclosures (judge investment data)
- Case law embeddings (~2TB for semantic search)
- RECAP Archive (federal court documents from PACER)

**Partnership Note:** CourtListener incorporates and enhances Harvard CAP data — they have cleaned/fixed 1M+ items from Harvard's dataset [^1697^].

---

### 1.2 Harvard Caselaw Access Project (CAP)

| Attribute | Detail |
|-----------|--------|
| **Name** | Caselaw Access Project (CAP) |
| **URL** | https://case.law/ |
| **API Docs** | https://case.law/docs/ |
| **Format** | REST API, Bulk ZIP downloads, JSON, XML |
| **License** | CC0 License (as of 2024); some jurisdictions had prior commercial restrictions through LexisNexis/Ravel [^1685^] [^1686^] |
| **API/Bulk Access** | API at api.case.law; bulk data downloads for whitelisted (open) jurisdictions freely; restricted jurisdictions require registration (500 cases/day) [^1685^] [^1693^] |
| **Coverage** | 6.7 million U.S. cases, 40 million+ pages, spanning 1658–2018; all federal and state jurisdictions |
| **CSOAI Use Case** | Historical case law analysis; pre-2018 baseline dataset; bulk NLP training data |

**Open vs. Restricted Jurisdictions:** Unregistered users get full access to open jurisdictions and all metadata. Researchers can apply for unrestricted access to all jurisdictions [^1685^].

**Hugging Face Mirror:** https://huggingface.co/datasets/free-law/Caselaw_Access_Project [^1686^]

---

## 2. U.S. Federal Court Records

### 2.1 PACER & RECAP

| Attribute | Detail |
|-----------|--------|
| **Name** | PACER (Public Access to Court Electronic Records) / RECAP |
| **PACER URL** | https://pacer.uscourts.gov/ |
| **RECAP URL** | https://free.law/recap/ |
| **RECAP Archive** | https://www.courtlistener.com/recap/ |
| **Format** | PDF dockets, JSON feeds, XML feeds, REST API |
| **License** | Federal court records are public domain; RECAP archive freely accessible |
| **API/Bulk Access** | PACER: PCL API + Authentication API for programmatic access (fee-based, $0.08/page). RECAP: Free browser extension + bulk archive via CourtListener API [^1805^] [^1809^] |
| **Coverage** | 1 billion+ federal court records (District, Appellate, Bankruptcy); RECAP has tens of millions of liberated documents |
| **CSOAI Use Case** | Federal litigation tracking; docket analytics; document-level analysis; real-time case monitoring via alerts |

**Key APIs:** [^1809^]
- PACER Authentication API (auto-login tokens)
- PACER Case Locator (PCL) API (nationwide case search)
- CourtListener RECAP API + bulk data (free mirror)
- CM/ECF JSON/XML court lookup feeds

---

### 2.2 SEC EDGAR / SEC-API

| Attribute | Detail |
|-----------|--------|
| **Name** | SEC EDGAR Filings API |
| **Official URL** | https://www.sec.gov/search-filings/edgar-application-programming-interfaces |
| **data.sec.gov** | https://data.sec.gov/submissions/CIK##########.json |
| **SEC-API (3rd party)** | https://sec-api.io/ |
| **Format** | JSON (REST), XBRL-JSON, bulk ZIP archives |
| **License** | U.S. public domain; free, no API key required for official APIs |
| **API/Bulk Access** | Official EDGAR: REST API (real-time JSON), bulk ZIP nightly at ~3am ET. SEC-API: Python/JS SDKs, bulk dataset downloads [^1628^] [^1541^] |
| **Coverage** | 20M+ filings since 1993; 100M+ exhibits; all SEC-regulated entities |
| **CSOAI Use Case** | Corporate disclosure analysis; enforcement action tracking; insider trading monitoring; financial statement XBRL parsing |

**Official SEC APIs (Free, No Key):** [^1628^]
- Submissions history by CIK: `data.sec.gov/submissions/CIK##########.json`
- Company facts: `data.sec.gov/api/xbrl/companyfacts/CIK##########.json`
- Frames (aggregated financials): `data.sec.gov/api/xbrl/frames/...`
- Bulk ZIP updated nightly

**SEC-API.io (Commercial with free tier):** [^1541^]
- 20M+ EDGAR filings, 100M+ exhibits
- Enforcement actions, litigation releases, administrative proceedings
- Insider trading (Forms 3/4/5), 13F holdings, Form ADV
- XBRL-to-JSON converter, full-text search, real-time filing stream

---

## 3. UK & Commonwealth Legislation & Case Law

### 3.1 UK legislation.gov.uk

| Attribute | Detail |
|-----------|--------|
| **Name** | UK Legislation API (The National Archives) |
| **URL** | https://www.legislation.gov.uk/ |
| **Data Docs** | https://legislation.github.io/data-documentation/ |
| **Format** | XML (Crown Legislation Markup Language / Akoma Ntoso), RDF, HTML, JSON feeds (Atom), PDF |
| **License** | Open Government Licence — free for commercial and non-commercial use [^1691^] [^1695^] |
| **API/Bulk Access** | RESTful API with content negotiation; append `/data.xml`, `/data.rdf`, `/data.akn`, `/data.feed` to any URL; no registration required [^1691^] [^1699^] |
| **Coverage** | Complete UK statute book — all legislation from medieval period to present; 1.9 billion+ triples in LOD cloud [^1700^] |
| **CSOAI Use Case** | UK legislation tracking; regulatory change monitoring; legal NLP training on structured legislative XML |

**Key Features:** [^1702^]
- Original "as enacted" and "revised" versions
- Point-in-time views via timeline
- Multiple formats: CLML XML, Akoma Ntoso XML, HTML5, RDF
- Full SPARQL endpoint access available
- GitHub transforms repo: https://github.com/legislation/legislation/

---

### 3.2 BAILII

| Attribute | Detail |
|-----------|--------|
| **Name** | British and Irish Legal Information Institute |
| **URL** | https://www.bailii.org/ |
| **Format** | HTML, searchable web interface |
| **License** | Free access; donations requested for commercial/educational users |
| **API/Bulk Access** | Web search interface; bulk data licensing available for research; member of WorldLII network |
| **Coverage** | 90+ databases across 7 jurisdictions: UK, England & Wales, Scotland, Northern Ireland, Ireland, EU, and other jurisdictions; ~297,513+ searchable documents [^1847^] [^1848^] |
| **CSOAI Use Case** | UK/Irish case law research; Commonwealth precedent analysis; free alternative to Westlaw/Lexis for UK materials |

---

### 3.3 CanLII (Canada)

| Attribute | Detail |
|-----------|--------|
| **Name** | Canadian Legal Information Institute |
| **URL** | https://www.canlii.org/ |
| **Backend** | Lexum |
| **Format** | HTML, PDF, structured metadata |
| **License** | Free public access; funded by Federation of Law Societies of Canada |
| **API/Bulk Access** | CanLII Connects API for commentary; bulk data available via partnership; 3.7M+ legal documents hosted [^1858^] |
| **Coverage** | All Canadian federal, provincial, and territorial statutes, regulations, and court decisions; 200+ collections |
| **CSOAI Use Case** | Canadian legal market analysis; cross-jurisdictional precedent comparison; bilingual (EN/FR) legal NLP |

---

## 4. European Union Legal Data

### 4.1 EUR-Lex & Cellar

| Attribute | Detail |
|-----------|--------|
| **Name** | EUR-Lex (Official EU Legal Database) |
| **URL** | https://eur-lex.europa.eu/ |
| **Reuse Docs** | https://eur-lex.europa.eu/content/help/data-reuse/reuse-contents-eurlex-details.html |
| **Cellar** | https://publications.europa.eu/webapi/rdf/sparql (SPARQL endpoint) |
| **Format** | XML, HTML, PDF, JSON, RDF, Formex; REST webservices; SPARQL endpoint |
| **License** | Free reuse subject to EU copyright conditions; source documents in public domain [^1652^] |
| **API/Bulk Access** | REST webservice (registered users); bulk data dump for legal acts in force (CELEX sector 3) via EU login; SPARQL endpoint; RSS feeds; data.europa.eu portal [^1652^] |
| **Coverage** | All EU legal acts, CJEU case law, Official Journal, national transposition measures, treaties — 50+ years |
| **CSOAI Use Case** | EU regulatory compliance tracking; CJEU precedent analysis; cross-border legislation comparison; AI Act and digital regulation monitoring |

**Access Methods:** [^1652^]
1. **Webservice** — XML search for registered users
2. **Bulk Data Dump** — all legal acts in force per language
3. **Cellar SPARQL** — semantic query of all metadata and content
4. **Cellar RESTful API** — retrieve specific metadata sets and documents
5. **RSS feeds** — real-time change notifications
6. **LexAPI (3rd party)** — developer-friendly REST wrapper with JSON, 50 free calls/day [^1651^]

---

### 4.2 IUROPA CJEU Database

| Attribute | Detail |
|-----------|--------|
| **Name** | IUROPA CJEU Database |
| **URL** | https://iuropa.org/ |
| **Format** | CSV downloads, Parquet files, SQL query interface, natural language queries |
| **License** | Research database; free access to query and download |
| **API/Bulk Access** | Web-based query tool; bulk CSV/Parquet downloads of curated tables; AI assistant for data preparation [^1801^] |
| **Coverage** | All CJEU, General Court, and Civil Service Tribunal cases since 1952; every proceeding, decision, judge, AG, party |
| **CSOAI Use Case** | EU judicial analytics; CJEU citation network analysis; judge/AG career tracking; preliminary ruling patterns |

**Tables Available:** cases, procedures, decisions, parties, lawyers, judges + AGs, referrals, hearings, assignments [^1801^]

---

## 5. Intellectual Property Data

### 5.1 WIPO IP Statistics Data Center

| Attribute | Detail |
|-----------|--------|
| **Name** | WIPO IP Statistics Data Center |
| **URL** | https://www.wipo.int/en/web/ip-statistics/datacenter |
| **Format** | Web interface, downloadable CSV/Excel, API |
| **License** | Free; users agree not to republish or commercially resell datasets; citation required [^1726^] |
| **API/Bulk Access** | Free online service with indicator-based search; bulk download of historical and latest data; no registration required |
| **Coverage** | 190+ countries; patents, utility models, trademarks, industrial designs; PCT, Madrid, Hague systems; data from 1980 (PCT/Madrid/Hague from 2004) [^1719^] [^1726^] |
| **CSOAI Use Case** | Global IP filing trend analysis; country-level innovation benchmarking; technology sector IP monitoring |

**Key Reports:**
- World Intellectual Property Indicators (annual, 2025 edition available)
- IP Facts and Figures (quick reference)
- Statistical country profiles

---

### 5.2 USPTO Open Data Portal & Bulk Data

| Attribute | Detail |
|-----------|--------|
| **Name** | USPTO Open Data Portal (ODP) |
| **URL** | https://data.uspto.gov/ |
| **Bulk Data** | https://developer.uspto.gov/ |
| **PatentsView** | https://patentsview.uspto.gov/ |
| **Format** | REST API (JSON), bulk XML, CSV, Stata (.dta), BigQuery |
| **License** | U.S. public domain; free |
| **API/Bulk Access** | ODP REST APIs (API key required), Bulk Data Storage System (BDSS), PatentsView API, BigQuery datasets [^1778^] [^1774^] [^1780^] |
| **Coverage** | All U.S. patents (1790–present), applications (2001–present), assignments, PTAB proceedings, office actions, maintenance fees |
| **CSOAI Use Case** | Patent landscape analysis; prior art search; patent valuation; examination outcome prediction; IP portfolio analytics |

**Key Datasets (50+ bulk products):** [^1780^]
- Patent grants full text XML (weekly)
- Patent applications full text XML (weekly)
- Patent assignment daily/annual XML (1980–present, 9.6M+ assignments)
- Office actions data (4.4M office actions, 2008–2017)
- PTAB proceedings API (IPR/PGR/CBM decisions)
- Patent litigation API (74,000+ district court cases)
- AI Patent Dataset (13.2M patents classified by ML)
- Historical patent data (2 centuries of applications/grants)

---

### 5.3 EUIPO Open Data

| Attribute | Detail |
|-----------|--------|
| **Name** | EUIPO Open Data Platform |
| **URL** | https://euipo.europa.eu/ohimportal/en/open-data |
| **API Portal** | https://dev.euipo.europa.eu/product |
| **Format** | XML (daily bulk), JSON, CSV |
| **License** | No license required; free for all uses [^1722^] |
| **API/Bulk Access** | Bulk XML download (full dataset or partial); eSearch plus API; TMview/DSview APIs; updated daily [^1722^] [^1771^] |
| **Coverage** | All EU trade marks (~135,000 registered annually), designs (~100,000 annually), representatives, international registrations, applicants, case law |
| **CSOAI Use Case** | EU trademark portfolio monitoring; brand conflict detection; EU IP registration trend analysis |

---

### 5.4 IP Australia (IPGOD/IPGOLD)

| Attribute | Detail |
|-----------|--------|
| **Name** | IP Australia Open Data |
| **URL** | https://www.ipaustralia.gov.au/about-us/data-and-research |
| **Format** | CSV, bulk downloads |
| **License** | Creative Commons BY 4.0 |
| **API/Bulk Access** | Bulk annual dataset (IPGOD) + weekly updated version (IPGOLD) [^1722^] |
| **Coverage** | 100+ years of Australian IP: patents, trade marks, designs, plant breeder's rights; linked to business numbers |
| **CSOAI Use Case** | Australian IP market analysis; SME IP activity tracking; longitudinal IP innovation studies |

---

## 6. IP Litigation & Patent Analytics

### 6.1 USPTO Patent Litigation API

| Attribute | Detail |
|-----------|--------|
| **Name** | USPTO Patent Litigation API |
| **URL** | https://data.uspto.gov/ |
| **Format** | REST API (JSON), CSV |
| **License** | Free; API key required |
| **API/Bulk Access** | ODP API endpoint; 74,000+ district court patent cases searchable and downloadable [^1774^] |
| **Coverage** | U.S. district court patent litigation cases |
| **CSOAI Use Case** | Patent litigation trend analysis; NPE (patent troll) tracking; venue analytics; case outcome prediction |

---

### 6.2 EPO Open Patent Services (OPS)

| Attribute | Detail |
|-----------|--------|
| **Name** | EPO Open Patent Services (OPS) |
| **URL** | https://developers.epo.org/ |
| **Format** | REST API (XML) |
| **License** | Free for non-commercial use; registration required; rate limits apply |
| **API/Bulk Access** | REST API with bibliographic, legal status, and document retrieval endpoints; 140M+ patent records |
| **Coverage** | Worldwide patent data via INPADOC: EPO, WIPO, and 100+ national patent offices |
| **CSOAI Use Case** | Global patent family mapping; legal status monitoring; European patent landscape analysis |

**Also Available:** PATSTAT (Worldwide Patent Statistical Database) — subscription-based bulk data [^1722^]

---

## 7. Regulatory Enforcement Actions

### 7.1 SEC Enforcement Actions

| Attribute | Detail |
|-----------|--------|
| **Name** | SEC Enforcement Actions Database |
| **URL** | https://www.sec.gov/enforcement-litigation/administrative-proceedings |
| **Litigation Releases** | https://www.sec.gov/enforcement-litigation/litigation-releases |
| **AAERs** | https://www.sec.gov/accounting-and-auditing-enforcement-releases |
| **Format** | HTML, PDF; accessible via SEC-API in structured JSON |
| **License** | U.S. public domain |
| **API/Bulk Access** | SEC-API.io provides structured access: Enforcement Actions API, Litigation Releases API, Administrative Proceedings API, AAER Database API [^1541^] |
| **Coverage** | All SEC enforcement actions, administrative proceedings, litigation releases, accounting/auditing enforcement releases |
| **CSOAI Use Case** | Securities fraud tracking; enforcement trend analysis; compliance risk scoring; accounting irregularity detection |

---

### 7.2 FINRA Disciplinary Actions

| Attribute | Detail |
|-----------|--------|
| **Name** | FINRA Disciplinary Actions / BrokerCheck |
| **Disciplinary Actions URL** | https://www.finra.org/investors/have-problem/disciplinary-actions |
| **BrokerCheck URL** | https://brokercheck.finra.org/ |
| **OpenSanctions** | https://www.opensanctions.org/datasets/us_finra_actions/ |
| **Format** | Web search, PDF documents; structured via OpenSanctions |
| **License** | Public regulatory data |
| **API/Bulk Access** | No official public API; data accessible via: (1) FINRA's new public Disciplinary Actions Online Database (launched Dec 2024) — searchable by case number, date range, CRD number, firm/individual name [^1721^]; (2) OpenSanctions weekly-updated bulk exports (JSON, CSV, FollowTheMoney) [^1717^]; (3) Parse.bot wrapper API; (4) Apify scraper |
| **Coverage** | 33,390+ disciplinary actions; 600,000+ registered brokers; 3,500+ registered firms |
| **CSOAI Use Case** | Broker-dealer compliance screening; regulatory due diligence; financial advisor background checks; enforcement trend analysis |

**OpenSanctions Export Formats:** [^1717^]
- `entities.ftm.json` (27.71 MB)
- `targets.simple.csv` (2.77 MB)
- `targets.nested.json` (27.91 MB)
- Updated weekly

---

### 7.3 FTC Enforcement Actions

| Attribute | Detail |
|-----------|--------|
| **Name** | FTC Enforcement Actions Datasets |
| **URL** | https://www.ftc.gov/policy-notices/open-government/data-sets |
| **Data.gov** | https://catalog.data.gov/dataset/ftc-nonmerger-enforcement-actions |
| **Format** | CSV |
| **License** | U.S. public domain |
| **API/Bulk Access** | Direct CSV download from FTC.gov and Data.gov; no API key required [^1775^] [^1783^] |
| **Coverage** | Nonmerger enforcement actions (FY1996–FY2019); Merger enforcement actions (FY2000–Q2 FY2019); Civil penalty actions; HSR merger filings by month (FY1990–present) |
| **CSOAI Use Case** | Antitrust enforcement trend analysis; merger review analytics; consumer protection monitoring; Hart-Scott-Rodino filing trend analysis |

**Available Datasets:** [^1783^]
- FTC Nonmerger Enforcement Actions (CSV, 31.6 KB)
- FTC Merger Enforcement Actions (CSV, 80.89 KB)
- BC Civil Penalty Actions (CSV, 6.24 KB)
- BCP Civil Penalty Actions
- HSR Merger Filings by Month (CSV, 4.44 KB)

---

### 7.4 DOJ Open Data

| Attribute | Detail |
|-----------|--------|
| **Name** | DOJ Open Data Portal |
| **URL** | https://www.justice.gov/open/open-data |
| **Format** | CSV, JSON, HTML, PDF; varies by dataset |
| **License** | U.S. public domain |
| **API/Bulk Access** | Direct download; Data.gov indexing; no API key required [^1800^] |
| **Coverage** | BIA Precedent Decisions; ADA Enforcement Activities; Antitrust Division case filings; Attorney Discipline; Annual Statistical Reports (U.S. Attorneys); Sherman Act violations |
| **CSOAI Use Case** | DOJ enforcement pattern analysis; immigration appeal analytics; ADA compliance litigation trends; antitrust fine analytics |

---

## 8. State Bar & Attorney Discipline

| Attribute | Detail |
|-----------|--------|
| **Name** | State Bar Association Disciplinary Data |
| **Format** | Varies by state — typically web search, PDF, some structured data |
| **License** | Public regulatory data |
| **API/Bulk Access** | No unified national API. Individual state bars provide online lookup tools. Some aggregators: (1) CourtListener judge database includes some bar data; (2) OpenSanctions includes some regulatory actions; (3) ABA Center for Professional Discipline maintains national lawyer regulatory data bank (restricted access) |
| **Coverage** | 50 state bars + D.C.; attorney admission status, disciplinary history, voluntary resignations, suspensions, disbarments |
| **CSOAI Use Case** | Attorney compliance verification; disciplinary trend analysis by jurisdiction; legal malpractice risk assessment |

**Key State Bar URLs:**
- California State Bar: https://www.calbar.ca.gov/ (Attorney Search)
- New York: https://www.nybarexam.org/ / Attorney Detail
- Texas: https://www.texasbar.com/ (Member Search)
- Illinois: https://www.isba.org/ / ARDC
- Florida: https://www.floridabar.org/

**Note:** Most state bars provide web-based individual lookup only. Bulk data access requires direct arrangement with each state's attorney regulatory authority.

---

## 9. Arbitration & Dispute Resolution

### 9.1 UNCTAD ISDS Navigator

| Attribute | Detail |
|-----------|--------|
| **Name** | UNCTAD Investment Dispute Settlement (ISDS) Navigator |
| **URL** | https://investmentpolicy.unctad.org/investment-dispute-settlement |
| **Format** | Web database; Excel bulk download |
| **License** | Free for all users; citation required |
| **API/Bulk Access** | Full Excel data release (bulk download); web search with advanced filters [^1845^] [^1846^] |
| **Coverage** | 1,368 known treaty-based ISDS cases (1987–July 2024); covers ICSID, UNCITRAL, SCC, ICC, LCIA, PCA, and ad hoc proceedings |
| **CSOAI Use Case** | Investor-state dispute trend analysis; treaty regime effectiveness; damages award analytics; arbitrator appointment patterns |

**Data Fields Include:** [^1861^]
- Applicable IIA, arbitral rules, administering institution
- Economic sector, investment details, dispute summary
- Status/outcome, amounts claimed and awarded (in USD)
- IIA breaches alleged and found
- Arbitrator appointments

---

### 9.2 ICSID Case Law Database

| Attribute | Detail |
|-----------|--------|
| **Name** | ICSID Case Law Database |
| **URL** | https://icsid.worldbank.org/cases/case-database |
| **Format** | Web search, PDF documents |
| **License** | Free open access |
| **API/Bulk Access** | Web-based search by case number, party, nationality; PDF download of materials tab; no bulk API [^1756^] |
| **Coverage** | All ICSID-administered cases (1966–present); concluded and pending cases; awards, decisions, procedural documents |
| **CSOAI Use Case** | ICSID-specific jurisprudence analysis; investor-state award outcome prediction; annulment proceeding analytics |

---

### 9.3 italaw

| Attribute | Detail |
|-----------|--------|
| **Name** | Investment Treaty Arbitration Law (italaw) |
| **URL** | https://www.italaw.com/ |
| **Format** | Web search, PDF documents |
| **License** | Free open access; maintained by University of Victoria |
| **API/Bulk Access** | Searchable by keyword, party, proceeding type, legal instrument; browse by treaty, institution, respondent state [^1798^] |
| **Coverage** | Largest open-access repository of investment arbitration materials: awards, decisions, pleadings, legal memoranda, amicus briefs; best coverage for cases resolved in last 5–10 years |
| **CSOAI Use Case** | Investment arbitration research; treaty interpretation analysis; arbitral reasoning pattern extraction; counsel and arbitrator performance analytics |

---

### 9.4 LCIA Challenge Decision Database

| Attribute | Detail |
|-----------|--------|
| **Name** | LCIA Challenge Decision Database |
| **URL** | https://www.lcia.org/challenge-decision-database.aspx |
| **Format** | PDF digests |
| **License** | Free open access |
| **API/Bulk Access** | Individual PDF downloads; consolidated texts available by period [^1760^] |
| **Coverage** | LCIA arbitrator challenge decisions from October 2010 to December 2022; 50+ challenge decisions with anonymized excerpts |
| **CSOAI Use Case** | Arbitrator challenge outcome analysis; conflict of interest standard research; LCIA arbitration practice analytics |

---

## 10. Human Rights Case Databases

### 10.1 ECtHR HUDOC

| Attribute | Detail |
|-----------|--------|
| **Name** | HUDOC (European Court of Human Rights) |
| **URL** | https://www.echr.coe.int/hudoc-database |
| **Python Library** | https://pypi.org/project/echr-extractor/ |
| **OpenICPSR** | https://www.openicpsr.org/openicpsr/project/155781 |
| **Format** | Web search, XML, JSON (via API); CSV (via extractor) |
| **License** | Free open access; Council of Europe public documents |
| **API/Bulk Access** | HUDOC web API (searchable); echr-extractor Python library for bulk metadata + full text (50,000+ cases); OpenICPSR historical dataset (1968–2021) [^1797^] [^1808^] |
| **Coverage** | All ECtHR judgments and decisions (Grand Chamber, Chamber, Committee); European Commission of Human Rights decisions; Committee of Ministers resolutions; 36,000+ case law translations in 34 languages [^1811^] [^1813^] |
| **CSOAI Use Case** | Human rights jurisprudence analysis; Article violation prediction; country-specific compliance monitoring; cross-jurisdictional rights comparison |

**echr-extractor Features:** [^1797^]
- Metadata extraction with batching
- Full text download with parallel processing
- Citation network generation (nodes + edges)
- Multiple language support (ENG, FRE, etc.)
- Output: CSV, JSON, pandas DataFrame

---

### 10.2 African Human Rights Case Law Analyser

| Attribute | Detail |
|-----------|--------|
| **Name** | African Human Rights Case Law Analyser |
| **URL** | https://hudoc.ihrda.org/ |
| **Format** | Web search with filters |
| **License** | Free open access; developed by IHRDA with HURIDOCS support |
| **API/Bulk Access** | Web-based search and filter; no bulk API |
| **Coverage** | Decisions from: African Commission on Human and Peoples' Rights, African Committee of Experts on the Rights and Welfare of the Child, African Court on Human and Peoples' Rights, ECOWAS Community Court of Justice, SADC Tribunal, East African Court of Justice [^1761^] |
| **CSOAI Use Case** | African regional human rights analysis; comparative human rights jurisprudence; regional court effectiveness assessment |

---

### 10.3 Inter-American Human Rights (IACHR / IACtHR)

| Attribute | Detail |
|-----------|--------|
| **Name** | IACHR / Inter-American Court of Human Rights Case Law |
| **IACHR URL** | https://www.oas.org/en/iachr/decisions/court.asp |
| **IACtHR URL** | https://www.corteidh.or.cr/ |
| **Format** | Web search, PDF |
| **License** | Free open access |
| **API/Bulk Access** | Web-based case databases; individual document downloads |
| **Coverage** | All IACtHR judgments, advisory opinions, provisional measures; IACHR merits reports, friendly settlements |
| **CSOAI Use Case** | Inter-American human rights analysis; regional comparative law; reparations award analytics |

---

## 11. WTO & Trade Disputes

### 11.1 WTO Dispute Settlement Documents

| Attribute | Detail |
|-----------|--------|
| **Name** | WTO Dispute Settlement Documents Dataset |
| **URL** | https://data.wto.org/dataset/ds_db |
| **Dispute Gateway** | https://www.wto.org/English/Tratop_e/dispu_e/dispu_e.htm |
| **Format** | Structured dataset; PDF reports; JSON/XML via data portal |
| **License** | WTO public documents; free access |
| **API/Bulk Access** | WTO Data portal (data.wto.org) with comprehensive case profiles; procedural timelines; official document links; keyword tags [^1753^] |
| **Coverage** | 631+ requests for consultations (1995–end of 2024); 350+ rulings issued; panel reports, Appellate Body reports, arbitration awards, Article 21.3/22.6 decisions |
| **CSOAI Use Case** | Trade dispute outcome prediction; WTO agreement interpretation analysis; complainant/respondent pattern analytics; sector-specific trade conflict monitoring |

**Data Components:** [^1753^]
- Comprehensive case profiles (DS number, parties, agreements cited)
- Procedural timeline with timestamped milestones
- Official document library with links to all public documents
- Participation data per WTO Member
- Subject-matter indicators (anti-dumping, agriculture, IP, services, etc.)
- Interactive disputes map

---

## 12. Law Firm & Legal Industry Data

### 12.1 ALM Rankings (Am Law, Global 200)

| Attribute | Detail |
|-----------|--------|
| **Name** | The American Lawyer Rankings (ALM) |
| **URL** | https://www.law.com/americanlawyer/ |
| **Format** | Published rankings; some data in articles |
| **License** | Published rankings (public); underlying data proprietary |
| **API/Bulk Access** | No public API; rankings published annually in September; aggregate revenue data reported in press coverage |
| **Coverage** | Am Law 100 (U.S., since 1987), Am Law 200 (since 1999), Global 200 (since 2018); revenue, headcount, PPP, RPL metrics |
| **CSOAI Use Case** | Legal market sizing; firm growth trend analysis; competitive benchmarking; M&A deal flow correlation |

**2025 Global 200 Highlights:** Aggregate revenue exceeded $200 billion, 11.8% YoY growth [^1758^]

---

### 12.2 ABA Legal Technology Survey

| Attribute | Detail |
|-----------|--------|
| **Name** | ABA Legal Technology Survey Report |
| **URL** | https://www.americanbar.org/groups/legal-technology-resource-center.html |
| **Format** | Published reports; summary statistics in press coverage |
| **License** | Purchase required for full report ($1,600; $1,400 ABA members); summary data public |
| **API/Bulk Access** | No API; annual published report with statistical tables; key findings reported in legal media [^1851^] [^1854^] |
| **Coverage** | Five volumes: Online Research, Technology Basics & Security, Law Office Technology, Marketing & Communication, Litigation Technology |
| **CSOAI Use Case** | Legal tech adoption trend analysis; cloud computing penetration; AI adoption benchmarking; cybersecurity posture assessment |

**2024 Key Findings:** [^1851^] [^1862^]
- 67% use fee-based online research; 55% use free platforms
- 73% use cloud-based legal tools
- 85% of litigators use electronic court filings
- 60% have formal cybersecurity policies
- 35% use legal analytics for research
- 13% say AI is "already mainstream" (up from 4% in 2023)

---

### 12.3 Vault / Firsthand Rankings

| Attribute | Detail |
|-----------|--------|
| **Name** | Vault Law 100 / Firsthand Rankings |
| **URL** | https://www.firsthand.com/ |
| **Format** | Published rankings |
| **License** | Publicly published rankings |
| **API/Bulk Access** | No API; annual published rankings |
| **Coverage** | Prestige-based firm rankings; practice area rankings; quality-of-life metrics |
| **CSOAI Use Case** | Firm prestige trend analysis; associate satisfaction benchmarking; law school placement analytics |

---

## Summary Matrix

| # | Source | Domain | Format | API | Bulk | Free |
|---|--------|--------|--------|-----|------|------|
| 1 | CourtListener | U.S. Case Law | JSON, CSV, SQL | Yes | Yes | Yes* |
| 2 | Harvard CAP | U.S. Case Law | JSON, XML | Yes | Yes | Yes |
| 3 | PACER/RECAP | Fed. Court Records | PDF, JSON | Yes | Yes | RECAP free |
| 4 | SEC EDGAR | Securities Filings | JSON, XBRL | Yes | Yes | Yes |
| 5 | UK legislation.gov.uk | UK Legislation | XML, RDF | Yes | Yes | Yes |
| 6 | BAILII | UK/IE Case Law | HTML | No | Partial | Yes |
| 7 | CanLII | Canadian Law | HTML | Limited | Partial | Yes |
| 8 | EUR-Lex | EU Law | XML, RDF, JSON | Yes | Yes | Yes |
| 9 | IUROPA | CJEU Cases | CSV, Parquet | Query | Yes | Yes |
| 10 | WIPO Stats | IP Statistics | CSV, Web | Yes | Yes | Yes |
| 11 | USPTO ODP | U.S. Patents | JSON, XML | Yes | Yes | Yes |
| 12 | EUIPO Open Data | EU TM/Designs | XML | Yes | Yes | Yes |
| 13 | IP Australia | AU IP Data | CSV | No | Yes | Yes |
| 14 | FINRA Actions | Broker Discipline | Web, CSV | No | Via OS | Yes |
| 15 | FTC Data | Antitrust/Consumer | CSV | No | Yes | Yes |
| 16 | DOJ Open Data | Federal Prosecution | CSV, PDF | No | Yes | Yes |
| 17 | UNCTAD ISDS | Investment Arbitration | Excel | No | Yes | Yes |
| 18 | ICSID DB | ICSID Cases | PDF | No | No | Yes |
| 19 | italaw | Investment Arb. | PDF | No | No | Yes |
| 20 | ECtHR HUDOC | Human Rights | XML, CSV | Yes | Yes | Yes |
| 21 | African HR CLA | African HR | Web | No | No | Yes |
| 22 | WTO DS Docs | Trade Disputes | JSON, PDF | Yes | Yes | Yes |
| 23 | ALM Rankings | Law Firm Data | Published | No | No | Partial |

*CourtListener: free tier available; high-volume access requires Free Law Project membership
**OS = OpenSanctions provides structured bulk exports

---

## CSOAI Integration Recommendations

### Priority Tier 1 (Immediate)
1. **CourtListener** — Foundation U.S. case law dimension; start with bulk CSV imports
2. **SEC EDGAR** — Real-time corporate disclosure stream via official APIs
3. **UK legislation.gov.uk** — Structured legislative XML for regulatory NLP
4. **EUR-Lex** — EU regulatory corpus via SPARQL/REST APIs
5. **WIPO Stats** — Global IP indicator time series

### Priority Tier 2 (Near-term)
6. **Harvard CAP** — Historical U.S. case law baseline (CC0 license)
7. **USPTO ODP** — Patent analytics and litigation tracking
8. **FINRA + FTC** — Regulatory enforcement pattern analysis
9. **UNCTAD ISDS + italaw** — Investment arbitration intelligence
10. **ECtHR HUDOC** — Human rights jurisprudence dimension

### Priority Tier 3 (Specialized)
11. **WTO DS** — International trade dispute tracking
12. **EUIPO Open Data** — EU trademark/design monitoring
13. **PACER/RECAP** — Federal docket-level analytics
14. **ICSID + LCIA** — Arbitration institution-specific analysis
15. **Law firm rankings** — Legal market intelligence overlay

---

## References

[^1628^] SEC EDGAR APIs — https://www.sec.gov/search-filings/edgar-application-programming-interfaces
[^1541^] SEC-API.io Python Library — https://pypi.org/project/sec-api/
[^1651^] LexAPI (EUR-Lex wrapper) — https://lex-api.com/
[^1652^] EUR-Lex Reuse Documentation — https://eur-lex.europa.eu/content/help/data-reuse/reuse-contents-eurlex-details.html
[^1685^] CAP Guide 2024 — https://blog.counselstack.com/case-law-access-project-guide-2024/
[^1686^] Hugging Face CAP Dataset — https://huggingface.co/datasets/free-law/Caselaw_Access_Project
[^1688^] CourtListener Bulk Data — https://wiki.free.law/c/courtlistener/help/api/bulk-data/bulk-legal-data/bulk-legal-data
[^1691^] legislation.gov.uk Data Reuse — https://legislation.github.io/data-documentation/
[^1695^] legislation.gov.uk on Data.gov.uk — https://www.data.gov.uk/dataset/a2416481-271a-42b2-ace8-fc247dd251be/legislation-api
[^1697^] CourtListener API Overview — https://wiki.free.law/c/courtlistener/help/api
[^1699^] GDS legislation.gov.uk API Blog — https://gds.blog.gov.uk/2012/03/30/putting-apis-first-legislation-gov-uk/
[^1700^] UK Legislation LOD Cloud — https://lod-cloud.net/dataset/uk-legislation-api
[^1702^] TNA Legislation API Presentation — https://cdn.nationalarchives.gov.uk/documents/cas-82049-presentation-notes.pdf
[^1717^] OpenSanctions FINRA Actions — https://www.opensanctions.org/datasets/us_finra_actions/
[^1719^] WIPO IP Statistics — https://www.wipo.int/en/web/ip-statistics
[^1721^] FINRA Disciplinary Actions Database — https://investorclaims.com/blog/finra-launches-a-new-public-access-disciplinary-actions-database/
[^1722^] IP Dataset Resources (4IPCouncil) — https://www.4ipcouncil.com/research/useful-dataset-resources
[^1726^] WIPO Statistics Data Center About — https://www.wipo.int/en/web/ip-statistics/about
[^1753^] WTO Dispute Settlement Documents — https://data.wto.org/dataset/ds_db
[^1756^] ICSID Case Law Database — https://unimelb.libguides.com/c.php?g=929887&p=6719577
[^1758^] Am Law Global 200 — https://grokipedia.com/page/List_of_largest_law_firms_by_revenue
[^1760^] LCIA Challenge Decision Database — https://www.lcia.org/challenge-decision-database.aspx
[^1761^] African Human Rights Case Law Analyser — https://huridocs.org/resource-library/human-rights-research-databases/african-human-rights-case-law-analyser/
[^1774^] USPTO Patent MCP Server — https://lobehub.com/zh-TW/mcp/riemannzeta-patent_mcp_server
[^1775^] FTC Nonmerger Enforcement Actions (Data.gov) — https://catalog.data.gov/dataset/ftc-nonmerger-enforcement-actions
[^1778^] USPTO Open Data Portal — https://data.uspto.gov/
[^1780^] USPTO Bulk Data Products — https://patent-client.readthedocs.io/en/latest/user_guide/bulk_data.html
[^1783^] FTC Data Sets — https://www.ftc.gov/policy-notices/open-government/data-sets
[^1797^] echr-extractor Python Library — https://pypi.org/project/echr-extractor/
[^1798^] International Investment Law Research Guide — https://guides.ll.georgetown.edu/c.php?g=371540&p=4194930
[^1800^] DOJ Open Data — https://www.justice.gov/open/open-data
[^1801^] IUROPA CJEU Database — https://iuropa.org/
[^1805^] RECAP Suite — https://free.law/recap/
[^1808^] ECtHR Mapping Project (OpenICPSR) — https://www.openicpsr.org/openicpsr/project/155781
[^1809^] PACER Developer Resources — https://pacer.uscourts.gov/file-case/developer-resources
[^1811^] HUDOC Database — https://www.echr.coe.int/hudoc-database
[^1813^] HUDOC Romanian Launch — https://eucrim.eu/news/launch-of-hudoc-case-law-database-in-romanian/
[^1845^] UNCTAD ISDS Full Data Release — https://investmentpolicy.unctad.org/publications/1303/investment-dispute-settlement-navigator-full-isds-data-release-as-of-31-12-2023-in-excel-format-
[^1846^] UNCTAD ISDS Navigator Update — https://investmentpolicy.unctad.org/news/hub/1764/20250210-isds-navigator-update-new-cases-andawards-available
[^1847^] BAILII at IALS — https://ials.sas.ac.uk/digital-publications/bailii
[^1848^] BAILII Land Portal — https://landportal.org/organization/british-and-irish-legal-information-institute
[^1851^] ABA Legal Tech Survey — https://legalnews.com/Home/Articles?DataId=1583035
[^1854^] ABA 2024 Legal Technology Survey — https://www.advocatecapital.com/blog/aba-releases-2024-legal-technology-survey/
[^1858^] CanLII by Lexum — https://lexum.com/en/blog/case-studies/canlii
[^1861^] UNCTAD ISDS Methodology — https://investmentpolicy.unctad.org/pages/1057/isds-navigator-about-and-methodology
[^1862^] ABA AI Adoption — https://www.lawnext.com/2025/03/aba-tech-survey-finds-growing-adoption-of-ai-in-legal-practice-with-efficiency-gains-as-primary-driver.html
