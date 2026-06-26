# Governance & Public Sector Data Sources - CSOAI.org Governance Hive

> **Last updated**: 2025-07  
> **Status**: Active research compilation  
> **License**: All sources listed are FREE / OPEN DATA with public access  
> **Priority tiers**: P1 = Mission-critical, P2 = High-value, P3 = Specialized  

---

## Table of Contents

1. [Inter-Governmental & International Organization Data](#1-inter-governmental--international-organization-data)
2. [World Bank Governance Indicators (WGI)](#2-world-bank-worldwide-governance-indicators-wgi)
3. [OECD Government at a Glance](#3-oecd-government-at-a-glance)
4. [Open Government Partnership (OGP)](#4-open-government-partnership-ogp)
5. [Municipal / Open City Data Portals](#5-municipal--open-city-data-portals)
6. [Parliamentary Record APIs](#6-parliamentary-record-apis)
7. [Public Procurement Data](#7-public-procurement-data)
8. [Government Spending / Budget Data](#8-government-spending--budget-data)
9. [Voting Records & Election Data](#9-voting-records--election-data)
10. [Transparency International Corruption Perceptions Index](#10-transparency-international-corruption-perceptions-index)
11. [UN E-Government Survey](#11-un-e-government-survey)
12. [European Court of Human Rights (HUDOC)](#12-european-court-of-human-rights-echr--hudoc)
13. [International Court of Justice (ICJ)](#13-international-court-of-justice-icj)
14. [WTO Dispute Settlement Database](#14-wto-dispute-settlement-database)
15. [OpenStates / Plural - US State Legislative Data](#15-openstates--plural---us-state-legislative-data)
16. [Bonus Sources](#16-bonus-sources)

---

## 1. Inter-Governmental & International Organization Data

### 1.1 UN Official Document System (ODS)
| Field | Details |
|-------|---------|
| **URL** | https://documents.un.org/  |
| **Alt access** | https://undocs.org/ (short URL resolver: undocs.org + document symbol, e.g. `undocs.org/A/RES/67/1`) |
| **API available** | Yes - REST API via UN Digital Library integration |
| **Format** | HTML, PDF, XML; bulk data via scraping |
| **Coverage** | All UN documents from 1993+; resolutions of principal organs & Security Council from 1946+ |
| **License** | UN Terms of Use - generally public for official documents |
| **Bulk access** | No direct bulk download; accessible via document symbol URLs |
| **CSOAI use case** | Track UN resolutions, policy positions, global governance documents |
| **Priority** | P2 |

**Key collections** [^1805^][^1813^][^1824^]:
- All UN documents 1993+
- GA resolutions 1946+
- Security Council plenary documents 1946+
- Meeting records, voting data, speeches

### 1.2 UN Digital Library (UNDL)
| Field | Details |
|-------|---------|
| **URL** | https://digitallibrary.un.org/ |
| **API** | Yes - web scraping supported; structured data available |
| **Format** | PDF, HTML; voting data extractable as CSV/Excel |
| **Coverage** | 1946+ for documents; voting data for GA and SC resolutions |
| **License** | Public access |
| **Bulk access** | Voting data bulk downloadable; documents via search |
| **CSOAI use case** | UN voting pattern analysis, document retrieval, resolution tracking |
| **Priority** | P2 |

**Key features** [^1813^][^1814^][^1815^]:
- Voting Data collection (23,600+ voting records)
- Linked data between resolutions, meeting records, and voting
- Searchable by UN body, agency, document type
- All General Assembly resolutions with country-level voting positions

### 1.3 UN Data Portal (data.un.org)
| Field | Details |
|-------|---------|
| **URL** | https://data.un.org/ |
| **API** | Yes - REST API available |
| **Format** | CSV, XML, JSON |
| **Coverage** | UN system data across all agencies |
| **License** | Open - public data |
| **Bulk access** | Yes - bulk download available |
| **CSOAI use case** | Cross-agency UN data, SDG indicators, development statistics |
| **Priority** | P1 |

### 1.4 UN Comtrade Database
| Field | Details |
|-------|---------|
| **URL** | https://comtrade.un.org/ |
| **API** | Yes - REST API (`comtrade.un.org/api/get?...`) |
| **Format** | JSON, CSV, XML; bulk download as .gz |
| **Coverage** | International trade data 1962+ (annual), 2000+ (monthly) |
| **License** | Free (premium for bulk/batch) |
| **Bulk access** | Yes - bulk files for premium; API limit 10,000 records for guest users |
| **Python library** | `comtradeapicall` (PyPI) [^1829^] |
| **CSOAI use case** | Trade flow analysis, economic governance, dispute correlation |
| **Priority** | P2 |

---

## 2. World Bank Worldwide Governance Indicators (WGI)

| Field | Details |
|-------|---------|
| **URL** | https://www.worldbank.org/en/publication/worldwide-governance-indicators |
| **Data portal** | https://data360.worldbank.org/en/dataset/WB_WGI |
| **API** | Yes - World Bank Data API + DataBank |
| **Format** | Excel, Stata, SDMX CSV, JSON (via API) |
| **Coverage** | 215+ economies, 1996-2024, updated annually (September) |
| **License** | Creative Commons BY 4.0 |
| **Bulk access** | Full Excel/Stata downloads available |
| **CSOAI use case** | Cross-country governance benchmarking, rule-of-law metrics, corruption indicators |
| **Priority** | P1 |

**Six composite indicators** [^1705^][^1714^][^1834^]:
1. Voice and Accountability
2. Political Stability and Absence of Violence/Terrorism
3. Government Effectiveness
4. Regulatory Quality
5. Rule of Law
6. Control of Corruption

---

## 3. OECD Government at a Glance

| Field | Details |
|-------|---------|
| **URL** | https://www.oecd.org/en/data/datasets/oecd-government-at-a-glance-database.html |
| **API** | Yes - OECD.Stat API; REST API via data portal |
| **Format** | CSV, Excel, JSON, SDMX, Parquet |
| **Coverage** | 36+ OECD countries, annual updates |
| **License** | OECD Terms and Conditions (generally free for research) |
| **Bulk access** | Yes - theme-based CSV/Excel downloads |
| **CSOAI use case** | Government spending analysis, public employment, procurement data, integrity indicators |
| **Priority** | P1 |

**Available datasets** [^1708^][^1703^][^1716^]:
- Public finance main indicators (2025 edition)
- Public employment and representation
- Procurement size data
- Public integrity indicators
- OURdata Index (Open Government Data)
- Digital government indexes
- Budget frameworks & spending reviews
- Regulatory governance
- Trust survey data

---

## 4. Open Government Partnership (OGP)

| Field | Details |
|-------|---------|
| **URL** | https://www.opengovpartnership.org/ |
| **Data explorer** | https://www.opengovpartnership.org/broken-links/data-explorer/ |
| **API** | Data available via bulk download; no central API but datasets downloadable |
| **Format** | CSV, Excel, JSON |
| **Coverage** | 75+ member countries, policy area assessments |
| **License** | Open |
| **Bulk access** | Yes - Global Data Barometer data available for download |
| **CSOAI use case** | Open government benchmarking, country commitments tracking, transparency scoring |
| **Priority** | P1 |

**Key datasets** [^1712^][^1812^]:
- OGP country action plans & commitments
- Global Data Barometer (political finance, lobbying, beneficial ownership)
- Open contracting adoption tracking (59% of OGP countries publish OCDS data)
- Legislative open data metrics

---

## 5. Municipal / Open City Data Portals

### 5.1 Global Directory - DataPortals.org
| Field | Details |
|-------|---------|
| **URL** | https://dataportals.org/search/ |
| **API** | Browseable catalog |
| **Format** | Various (CKAN, Socrata, OpenDataSoft) |
| **Coverage** | 500+ city/regional portals worldwide |
| **License** | Varies by portal |
| **CSOAI use case** | Discover city-level governance data globally |
| **Priority** | P2 |

### 5.2 CKAN-Powered Portals (open source)
| Field | Details |
|-------|---------|
| **URL** | https://ckan.org/ |
| **API** | CKAN RESTful API - all portals provide unified API |
| **Format** | JSON, CSV, XML, RDF |
| **Notable portals** | data.gov (US), data.gov.uk, Berlin, Helsinki, Bonn, EU ODP, Brazil |
| **License** | Open Source (AGPL) + portal-specific data licenses |
| **Bulk access** | Yes - package_list, package_show, datastore_search APIs |
| **CSOAI use case** | Municipal budget data, transportation, crime, permits, elections |
| **Priority** | P1 |

**Key CKAN municipal portals** [^1728^][^1730^]:
- **data.gov** - US federal + city data aggregator
- **data.gov.uk** - UK government data
- **Berlin Open Data** - `daten.berlin.de`
- **Barcelona Open Data** - `opendata-ajuntament.barcelona.cat`
- **Helsinki Region Infoshare** - `hri.fi`
- **Chicago Data Portal** - `data.cityofchicago.org`
- **City of Cape Town** - `web1.capetown.gov.za`
- **Baltimore Open Data** - `data.baltimorecity.gov`
- **Stockholm Open Data** - `open.stockholm.se`

### 5.3 Socrata / Tyler Data Platform
| Field | Details |
|-------|---------|
| **URL** | Platform (commercial, hosts many city portals) |
| **API** | SODA API (Socrata Open Data API) - RESTful |
| **Format** | JSON, CSV, RDF-XML |
| **Notable portals** | Chicago, NYC, San Francisco, Los Angeles, Seattle |
| **License** | Varies by city |
| **Bulk access** | Yes via SODA API |
| **CSOAI use case** | US city governance data, budgets, 311, crime, permits |
| **Priority** | P2 |

### 5.4 OpenDataSoft
| Field | Details |
|-------|---------|
| **URL** | https://www.opendatasoft.com/ |
| **API** | ODS Records API |
| **Format** | JSON, CSV |
| **Notable portals** | Paris, Brussels, Toulouse, Lombardia |
| **License** | Varies by portal |
| **CSOAI use case** | European city governance data |
| **Priority** | P2 |

---

## 6. Parliamentary Record APIs

### 6.1 US Congress.gov API
| Field | Details |
|-------|---------|
| **URL** | https://api.congress.gov/ |
| **Docs** | https://github.com/LibraryOfCongress/api.congress.gov |
| **API** | REST API, requires free API key from api.data.gov |
| **Format** | XML (default), JSON |
| **Coverage** | Bills from 1799+ (full metadata from 1973+), votes, members, committees |
| **License** | Public domain (US government) |
| **Bulk access** | Endpoint-based; GPO also provides bulk XML downloads |
| **CSOAI use case** | US legislative tracking, voting analysis, bill monitoring |
| **Priority** | P1 |

**Endpoints** [^1745^][^1746^][^1750^]:
- `/bill` - Bill data
- `/amendments` - Amendment data
- `/summaries` - Bill summaries
- `/member` - Member profiles
- `/house-vote` / `senate-vote` - Roll call votes
- `/committee` - Committee data
- `/congressional-record` - Congressional Record
- `/crsreport` - CRS reports
- `/treaty` - Treaty data

### 6.2 UK Parliament API
| Field | Details |
|-------|---------|
| **URL** | https://data.parliament.uk/ |
| **API** | REST API - Members Data Platform (MNIS) + data.parliament.uk |
| **Format** | XML, JSON, RDF |
| **Coverage** | Westminster Parliament data, members, divisions, committees |
| **License** | Open Government License |
| **Bulk access** | Yes - via API endpoints |
| **CSOAI use case** | UK parliamentary voting records, member research, debates |
| **Priority** | P1 |

### 6.3 TheyWorkForYou API (mySociety)
| Field | Details |
|-------|---------|
| **URL** | https://www.theyworkforyou.com/api/ |
| **Data source** | https://data.mysociety.org/datasets/uk-hansard/ |
| **API** | REST API with key |
| **Format** | JSON, XML |
| **Coverage** | UK parliamentary debates 1918+, voting records, member info |
| **License** | Open Data; some datasets require attribution |
| **Bulk access** | Yes - ParlParse formatted XML bulk downloads |
| **CSOAI use case** | UK parliamentary speech analysis, voting behavior research |
| **Priority** | P1 |

**Available data** [^1795^][^1797^][^1752^]:
- Hansard speeches and questions (XML, 1918+)
- MP voting records
- Written questions & answers
- Members' register of interests
- Constituency information
- Division (vote) results with individual MP positions

### 6.4 German Bundestag API (DIP)
| Field | Details |
|-------|---------|
| **URL** | https://search.dip.bundestag.de/api/v1 |
| **Docs** | https://data4parliaments.poltextlab.com/documents/2022-06-API-Documentation-for-DIP_EN.pdf |
| **Python lib** | `bundestag-api` (PyPI) [^1793^] |
| **API** | RESTful API, requires free API key |
| **Format** | JSON, XML |
| **Coverage** | Documents, procedures, plenary protocols, members, activities |
| **License** | Open Data - Bundestag |
| **Bulk access** | Yes - via API queries |
| **CSOAI use case** | German legislative tracking, plenary speech analysis, voting patterns |
| **Priority** | P1 |

**Main data types**:
- Documents (drucksache) - Bills, reports, proposals
- Procedures (vorgang) - Legislative processes
- Activities (aktivitaet) - Parliamentary actions
- Persons (person) - MPs
- Plenary Protocols (plenarprotokoll) - Session transcripts

### 6.5 Hansard R Package (UK Parliament)
| Field | Details |
|-------|---------|
| **URL** | https://cran.r-project.org/package=hansard |
| **Docs** | https://docs.evanodell.com/hansard/ |
| **Format** | R data frames (CSV exportable) |
| **License** | MIT (package); Open Government License (data) |
| **Bulk access** | Full API via R functions |
| **CSOAI use case** | UK parliamentary data analysis in R |
| **Priority** | P2 |

**Available functions** [^1742^][^1744^]:
- Bills, divisions, oral/written questions
- Early day motions, elections results
- Lords attendance, amendments, interests
- MP voting records, research briefings

### 6.6 European Parliament
| Field | Details |
|-------|---------|
| **URL** | https://data.europarl.europa.eu/ |
| **Alt** | https://www.europarl.europa.eu/doceo/document/ |
| **API** | OData API available |
| **Format** | XML, JSON, CSV |
| **License** | Creative Commons BY 4.0 |
| **Bulk access** | Yes |
| **CSOAI use case** | EU legislative process tracking, plenary votes, MEP activities |
| **Priority** | P2 |

---

## 7. Public Procurement Data

### 7.1 EU Tenders Electronic Daily (TED)
| Field | Details |
|-------|---------|
| **URL** | https://ted.europa.eu/ |
| **Developers** | https://ted.europa.eu/en/simap/developers-corner-for-reusers |
| **OCDS data** | https://data.open-contracting.org/en/publication/150 |
| **API** | Yes - TED Search API (public, no key required) |
| **OCDS bulk** | JSON, CSV, Excel by year (2011-2024); all-time ~1.8GB |
| **Format** | XML (notices), JSON (OCDS), CSV |
| **Coverage** | All EU public procurement notices |
| **License** | EU Open Data |
| **Bulk access** | Yes - CSV packages and OCDS bulk downloads |
| **CSOAI use case** | EU procurement market analysis, vendor competition, spending patterns |
| **Priority** | P1 |

**Data access** [^1741^][^1747^]:
- TED Search API: `700 requests/minute limit`
- CSV subsets at data.europa.eu
- Linked Open Data (LOD) available
- OCDS formatted bulk downloads via Open Contracting Partnership

### 7.2 UK Contracts Finder
| Field | Details |
|-------|---------|
| **URL** | https://www.contractsfinder.service.gov.uk/ |
| **API** | Yes - OCDS-compliant API |
| **Format** | JSON (OCDS) |
| **Coverage** | UK public sector contracts |
| **License** | UK Open Government Licence |
| **Bulk access** | Yes via API |
| **CSOAI use case** | UK procurement tracking, contract award analysis |
| **Priority** | P1 |

### 7.3 US SAM.gov (System for Award Management)
| Field | Details |
|-------|---------|
| **URL** | https://sam.gov/ |
| **API** | Yes - SAM.gov Public API |
| **Format** | JSON |
| **Coverage** | All US federal contracts, grants, awards |
| **License** | Public (US government) |
| **Bulk access** | Yes via API with key |
| **CSOAI use case** | US federal procurement analysis, vendor tracking |
| **Priority** | P1 |

### 7.4 Open Contracting Data Standard (OCDS) Registry
| Field | Details |
|-------|---------|
| **URL** | https://data.open-contracting.org/ |
| **Format** | JSON, Excel, CSV |
| **Coverage** | 100+ publishers worldwide |
| **License** | Apache 2.0 (standard); varies by publisher |
| **Bulk access** | Yes - bulk download in multiple formats |
| **CSOAI use case** | Cross-country procurement comparison, red-flag detection |
| **Priority** | P1 |

### 7.5 Ukraine ProZorro
| Field | Details |
|-------|---------|
| **URL** | https://prozorro.gov.ua/ |
| **API** | Yes - OpenProcurement API |
| **OCDS** | http://ocds.prozorro.openprocurement.io/ |
| **Format** | JSON (OCDS) |
| **License** | Open |
| **Bulk access** | Yes - weekly OCDS releases |
| **CSOAI use case** | Post-conflict procurement transparency model |
| **Priority** | P3 |

### 7.6 Mexico City Contrataciones Abiertas
| Field | Details |
|-------|---------|
| **URL** | http://www.contratosabiertos.cdmx.gob.mx/ |
| **Format** | JSON (OCDS) |
| **API** | Yes - documented API |
| **CSOAI use case** | Latin American procurement transparency |
| **Priority** | P3 |

---

## 8. Government Spending / Budget Data

### 8.1 OpenSpending / OpenBudgets.eu
| Field | Details |
|-------|---------|
| **URL** | http://next.openspending.org/ |
| **Viewer** | http://next.openspending.org/viewer/ |
| **API** | OS API for querying fiscal data |
| **Packager** | http://next.openspending.org/packager/ |
| **Format** | Fiscal Data Package (JSON), CSV |
| **License** | Open |
| **Bulk access** | Yes - dataset upload and download |
| **CSOAI use case** | Government budget analysis, fiscal transparency comparison |
| **Priority** | P1 |

**Components** [^1749^]:
- OS Packager: Data annotation into semantic fiscal models
- OS Viewer: Budget visualization
- OS API: Query fiscal data programmatically
- OS Explorer: Search and discover datasets

### 8.2 OpenBudgets.eu
| Field | Details |
|-------|---------|
| **URL** | https://openbudgets.eu/ |
| **Format** | RDF, JSON, CSV |
| **API** | SPARQL endpoint + OpenSpending-compatible API |
| **CSOAI use case** | EU budget transparency, comparative fiscal analysis |
| **Priority** | P2 |

### 8.3 World Bank BOOST
| Field | Details |
|-------|---------|
| **URL** | https://boost.worldbank.org/ |
| **Format** | Excel, CSV |
| **Coverage** | 60+ countries' budget data |
| **CSOAI use case** | Cross-country budget analysis, spending efficiency |
| **Priority** | P2 |

### 8.4 USASpending.gov
| Field | Details |
|-------|---------|
| **URL** | https://www.usaspending.gov/ |
| **API** | Yes - REST API |
| **Format** | JSON, CSV |
| **License** | Public (US government) |
| **Bulk download** | Yes - monthly delta files, full dumps |
| **CSOAI use case** | US federal spending tracking, grant/contract analysis |
| **Priority** | P1 |

---

## 9. Voting Records & Election Data

### 9.1 UN General Assembly Voting Data
| Field | Details |
|-------|---------|
| **Source** | UN Digital Library |
| **URL** | https://digitallibrary.un.org/ |
| **Scholarly dataset** | https://doi.org/10.7910/DVN/LEJUQZ (Harvard Dataverse) |
| **Format** | CSV (unga-res.csv, unga-res_positions.csv) |
| **Coverage** | 1946+; country-level positions on all GA resolutions |
| **License** | Open |
| **Bulk access** | Full downloadable datasets |
| **CSOAI use case** | Country voting alignment analysis, diplomatic position tracking |
| **Priority** | P1 |

**Key variables** [^1823^][^1825^]:
- Country, ISO code, session, year, vote date
- Resolution title, vote position (yes/no/abstain/non-voting)
- Authorship, regional group membership
- Yes/no/abstention counts

### 9.2 International IDEA Voter Turnout Database
| Field | Details |
|-------|---------|
| **URL** | https://www.idea.int/data-tools/data/voter-turnout-database |
| **Disputed Elections** | https://www.idea.int/data-tools/data/disputed-elections |
| **Format** | Excel (XLSX), web interface |
| **Coverage** | Global, election-level turnout data |
| **License** | Open with citation requirement |
| **Bulk access** | Yes - full export via "World" search + Export button |
| **CSOAI use case** | Election participation analysis, democratic health metrics |
| **Priority** | P2 |

**Other IDEA datasets** [^1828^][^1799^][^1803^]:
- Electoral System Design
- Electoral Management Design
- Gender Quotas
- Political Finance
- ICTs in Elections
- Disputed Elections (2020-2024)

### 9.3 OpenStates / Plural - US State Voting
| Field | Details |
|-------|---------|
| **URL** | https://v3.openstates.org/ |
| **Bulk data** | https://open.pluralpolicy.com/data/ |
| **API** | REST API v3 (key required) |
| **Format** | JSON (API), CSV, YAML, JSON (bulk) |
| **Coverage** | All 50 US states + DC + Puerto Rico |
| **License** | Public domain (CC-0) |
| **Bulk access** | Full PostgreSQL dumps, CSV bill/vote archives |
| **CSOAI use case** | US state-level voting analysis, bill tracking, legislator research |
| **Priority** | P1 |

**Bulk datasets** [^1757^][^1762^]:
- Legislator data (YAML/CSV)
- Bill & Vote CSV (per-session archives)
- Bill & Vote JSON (per-session with full text)
- Geographic boundary data (JSON)
- PostgreSQL public data dumps (monthly)

### 9.4 MySociety - EveryPolitician (archived)
| Field | Details |
|-------|---------|
| **URL** | https://everypolitician.org/ (archived) |
| **GitHub** | https://github.com/everypolitician |
| **Format** | Popolo-standard JSON, CSV |
| **Coverage** | 233 countries' politicians (archived 2019) |
| **License** | Wikimedia/CC |
| **CSOAI use case** | Global politician data, party affiliations, term data |
| **Priority** | P3 |

### 9.5 Constituency-Level Election Archive (CLEA)
| Field | Details |
|-------|---------|
| **URL** | https://electiondataarchive.org/ |
| **Format** | Stata, CSV, SPSS |
| **Coverage** | Lower house elections 1950+ in 150+ countries |
| **License** | Academic use (free registration) |
| **CSOAI use case** | Election result analysis, party system research |
| **Priority** | P2 |

---

## 10. Transparency International Corruption Perceptions Index

| Field | Details |
|-------|---------|
| **URL** | https://www.transparency.org/cpi |
| **Data GitHub** | https://github.com/datasets/corruption-perceptions-index |
| **Format** | CSV, Excel |
| **Coverage** | 180+ countries, 1995-2024 (annual) |
| **License** | Open Data (with attribution) |
| **Bulk access** | Full historical CSV download |
| **Scale** | 0-100 (0 = highly corrupt, 100 = very clean) |
| **CSOAI use case** | Corruption benchmarking, governance risk assessment, cross-country comparison |
| **Priority** | P1 |

**Notes** [^1755^]:
- Scores 1995-2011 on 0-10 scale; 2012+ on 0-100 scale
- The GitHub repository provides normalized data (0-10 across all years)
- Updated annually

---

## 11. UN E-Government Survey

| Field | Details |
|-------|---------|
| **URL** | https://publicadministration.un.org/egovkb |
| **UNeGovKB** | Interactive Knowledge Base for browsing/downloading |
| **Format** | PDF (reports), Excel, web interface |
| **Coverage** | 193 UN Member States, biennial (2004-2024) |
| **License** | Public |
| **Bulk access** | Country data downloadable; full reports available |
| **CSOAI use case** | Digital government maturity assessment, e-service benchmarking |
| **Priority** | P2 |

**Key indices** [^1709^][^1713^]:
- E-Government Development Index (EGDI)
- Online Service Index (OSI)
- Telecommunication Infrastructure Index (TII)
- Human Capital Index (HCI)
- Local Online Service Index (LOSI) - city-level since 2022

---

## 12. European Court of Human Rights (ECHR) / HUDOC

| Field | Details |
|-------|---------|
| **URL** | https://hudoc.echr.coe.int/ |
| **Python lib** | `echr-extractor` (PyPI) |
| **API** | Yes - HUDOC web API (queryable) |
| **Format** | HTML, CSV, JSON (via extractor); full text downloadable |
| **Coverage** | All ECHR judgments and decisions (1968+); ~50,000 cases |
| **License** | Public (court decisions) |
| **Bulk access** | Full corpus extractable via Python library |
| **CSOAI use case** | Human rights jurisprudence analysis, Article violation patterns, country compliance |
| **Priority** | P1 |

**Features** [^1753^][^1761^][^1767^]:
- Case metadata (applicant, respondent state, articles, outcome)
- Full text of judgments in English and French
- Citation network extraction (nodes and edges)
- Article-level violation filtering
- Date range batching for large downloads
- Languages: ENG, FRE, and other ECHR languages

**Academic dataset**: European Court of Human Rights Mapping Project [^1761^]
- Full judgments through October 2021
- CSV with case name, application number, country, conclusion, article number

---

## 13. International Court of Justice (ICJ)

| Field | Details |
|-------|---------|
| **URL** | https://www.icj-cij.org/cases |
| **Dataset** | https://zenodo.org/records/3826445 (CD-ICJ Corpus) |
| **Format** | PDF, TXT, CSV (academic corpus); HTML (official) |
| **Coverage** | All ICJ decisions 1947+ (2,169+ documents in English) |
| **License** | Public Domain (CC-Zero 1.0) for CD-ICJ |
| **Bulk access** | Full corpus download via Zenodo |
| **CSOAI use case** | International law analysis, state dispute patterns, advisory opinion research |
| **Priority** | P2 |

**CD-ICJ Corpus features** [^1764^]:
- 27 variables per case
- Judgments, advisory opinions, orders
- All appended minority opinions (declarations, separate opinions, dissenting)
- Compatible with CD-PCIJ (Permanent Court)
- Updated twice per year
- Peer-reviewed, published in Journal of Empirical Legal Studies

**Official ICJ resources** [^1759^][^1763^]:
- Reports of Judgments, Advisory Opinions and Orders
- Pleadings, Oral Arguments, Documents
- Cases searchable by state, topic, date

---

## 14. WTO Dispute Settlement Database

| Field | Details |
|-------|---------|
| **Portal** | https://data.wto.org/ |
| **Dispute DB** | https://data.wto.org/dataset/disputedb |
| **Dataset** | https://globalgovernanceprogramme.eui.eu/project/wto-dispute-settlement-and-case-law-project-2/ |
| **Format** | HTML (searchable), Excel, CSV |
| **Coverage** | All WTO disputes 1995-2020 (updated periodically) |
| **License** | Open |
| **Bulk access** | Downloadable dataset with user guide |
| **CSOAI use case** | Trade dispute analysis, member state compliance, economic governance |
| **Priority** | P2 |

**Key data components** [^1817^][^1821^][^1830^]:
- Dispute titles, members involved
- WTO agreements and articles cited
- Panel/Appellate Body proceedings
- Panellist participation
- Statistical reports on member participation

**Related datasets**:
- Trade Flows and Trade Disputes Dataset (Chad Bown)
- Temporary Trade Barriers Database
- WTO Trade Monitoring Database
- Regional Trade Agreements Database

---

## 15. OpenStates / Plural - US State Legislative Data

| Field | Details |
|-------|---------|
| **URL** | https://open.pluralpolicy.com/ |
| **API docs** | https://docs.openstates.org/api-v3/ |
| **API** | REST API v3 + GraphQL API |
| **GitHub** | https://github.com/openstates |
| **Format** | JSON (API), CSV, YAML, JSON (bulk), PostgreSQL dumps |
| **Coverage** | All 50 US states, DC, Puerto Rico; federal, state, local legislators |
| **License** | Public domain dedication (CC-0) |
| **Bulk access** | Full PostgreSQL monthly dumps, CSV/JSON session archives |
| **CSOAI use case** | US state governance analysis, bill tracking, legislator voting patterns |
| **Priority** | P1 |

**API endpoints** [^1755^][^1762^][^1754^]:
- `/jurisdictions` - Available jurisdictions
- `/people` - Legislators, governors (searchable)
- `/people.geo` - Find legislators by location
- `/bills` - Search bills by criteria
- `/committees` - Committee listings
- `/events` - Legislative events

**Bulk datasets**:
- Legislator Data: 25,508 entities (YAML/CSV)
- Bill & Vote CSV: Monthly session archives
- PostgreSQL dump: Nearly complete public database

---

## 16. Bonus Sources

### 16.1 UN OCHA Humanitarian Data Exchange (HDX)
| Field | Details |
|-------|---------|
| **URL** | https://data.humdata.org/ |
| **API** | HDX HAPI (Humanitarian API) - https://hapi.humdata.org/ |
| **Format** | CSV, JSON, API |
| **Coverage** | 250+ locations, humanitarian indicators |
| **CSOAI use case** | Crisis governance, humanitarian response tracking |
| **Priority** | P2 |

### 16.2 European Union Open Data Portal
| Field | Details |
|-------|---------|
| **URL** | https://data.europa.eu/ |
| **API** | Yes - CKAN API |
| **Format** | Various |
| **CSOAI use case** | EU policy data, high-value datasets, procurement |
| **Priority** | P1 |

### 16.3 USAspending.gov
| Field | Details |
|-------|---------|
| **URL** | https://www.usaspending.gov/ |
| **API** | Yes |
| **Format** | JSON, CSV |
| **CSOAI use case** | US federal spending analysis |
| **Priority** | P1 |

### 16.4 OpenCorporates
| Field | Details |
|-------|---------|
| **URL** | https://opencorporates.com/ |
| **API** | Yes |
| **Format** | JSON |
| **Coverage** | 200+ million companies in 140+ jurisdictions |
| **CSOAI use case** | Beneficial ownership, company-government linkages |
| **Priority** | P2 |

### 16.5 Global Legal Impact Dataset (CourtListener)
| Field | Details |
|-------|---------|
| **URL** | https://www.courtlistener.com/ |
| **API** | Yes - REST API + bulk data |
| **Format** | JSON, XML, bulk downloads |
| **Coverage** | US federal/state court opinions, PACER data |
| **CSOAI use case** | (Already in CSOAI baseline) Legal precedent analysis |
| **Priority** | P1 (baseline) |

### 16.6 LegiScan
| Field | Details |
|-------|---------|
| **URL** | https://legiscan.com/ |
| **API** | Yes |
| **Format** | JSON |
| **Coverage** | 50 US states + Congress |
| **CSOAI use case** | Alternative US legislative data source |
| **Priority** | P3 |

### 16.7 National Conference of State Legislatures (NCSL)
| Field | Details |
|-------|---------|
| **URL** | https://www.ncsl.org/ |
| **Format** | Web data, reports |
| **CSOAI use case** | US state policy comparison |
| **Priority** | P3 |

### 16.8 Varieties of Democracy (V-Dem)
| Field | Details |
|-------|---------|
| **URL** | https://v-dem.net/ |
| **Format** | CSV, R, Stata |
| **Coverage** | 202 countries, 1789-2024 |
| **License** | CC BY 4.0 |
| **CSOAI use case** | Democratic quality measurement, regime classification |
| **Priority** | P1 |

### 16.9 Polity V
| Field | Details |
|-------|---------|
| **URL** | https://www.systemicpeace.org/polityproject.html |
| **Format** | Excel, CSV |
| **Coverage** | All major independent states, 1800-2023 |
| **CSOAI use case** | Regime type classification, authority trends |
| **Priority** | P2 |

### 16.10 Quality of Government (QoG) Institute
| Field | Details |
|-------|---------|
| **URL** | https://www.gu.se/en/quality-government |
| **Data** | https://datafinder.qog.gu.se/ |
| **Format** | CSV, Stata, R, SPSS, Excel |
| **Coverage** | 150+ countries, multiple years |
| **License** | Open |
| **CSOAI use case** | Cross-country governance quality data compilation |
| **Priority** | P1 |

---

## Summary Matrix

| # | Source | URL | API | Bulk | Format | Priority |
|---|--------|-----|-----|------|--------|----------|
| 1 | UN ODS | documents.un.org | Yes | Partial | PDF/XML | P2 |
| 2 | World Bank WGI | worldbank.org/wgi | Yes | Yes | CSV/JSON/Excel | P1 |
| 3 | OECD Gov at Glance | oecd.org/gov | Yes | Yes | CSV/JSON/Excel | P1 |
| 4 | OGP | opengovpartnership.org | Partial | Yes | CSV/JSON | P1 |
| 5 | Municipal Portals | dataportals.org | Yes (CKAN) | Yes | Various | P1 |
| 6 | Congress.gov API | api.congress.gov | Yes | Yes | JSON/XML | P1 |
| 7 | UK Parliament API | data.parliament.uk | Yes | Yes | XML/JSON | P1 |
| 8 | Bundestag API | search.dip.bundestag.de | Yes | Yes | JSON/XML | P1 |
| 9 | TheyWorkForYou | theyworkforyou.com/api | Yes | Yes | JSON/XML | P1 |
| 10 | EU TED | ted.europa.eu | Yes | Yes | JSON/CSV/XML | P1 |
| 11 | SAM.gov | sam.gov | Yes | Yes | JSON | P1 |
| 12 | OCDS Registry | data.open-contracting.org | Yes | Yes | JSON/CSV | P1 |
| 13 | OpenSpending | openspending.org | Yes | Yes | JSON/CSV | P1 |
| 14 | UN Voting Data | digitallibrary.un.org | Yes | Yes | CSV | P1 |
| 15 | IDEA Turnout | idea.int | No | Yes | Excel | P2 |
| 16 | OpenStates | v3.openstates.org | Yes | Yes | JSON/CSV/SQL | P1 |
| 17 | TI CPI | transparency.org/cpi | No | Yes | CSV | P1 |
| 18 | UN E-Gov Survey | un.org/egovkb | Partial | Yes | Excel | P2 |
| 19 | ECHR HUDOC | hudoc.echr.coe.int | Yes | Yes | CSV/JSON | P1 |
| 20 | ICJ (CD-ICJ) | zenodo.org/records/3826445 | No | Yes | CSV/TXT/PDF | P2 |
| 21 | WTO Disputes | data.wto.org/disputedb | Partial | Yes | Excel/CSV | P2 |
| 22 | HDX | data.humdata.org | Yes | Yes | CSV/JSON | P2 |
| 23 | V-Dem | v-dem.net | No | Yes | CSV/R/Stata | P1 |
| 24 | QoG | datafinder.qog.gu.se | No | Yes | Multiple | P1 |
| 25 | USASpending | usaspending.gov | Yes | Yes | JSON/CSV | P1 |

---

## CSOAI Integration Roadmap

### Phase 1 (Immediate - P1 sources)
1. World Bank WGI - automated ingestion via API
2. OECD.Stat - API connector for governance indicators
3. Congress.gov API - US legislative monitoring
4. UK Parliament API + TheyWorkForYou - Westminster tracking
5. TED / OCDS - procurement transparency
6. ECHR HUDOC - human rights jurisprudence
7. Transparency International CPI - annual refresh
8. OpenStates - US state legislative data

### Phase 2 (Medium-term - P2 sources)
1. UN Digital Library - voting record analysis
2. UN E-Government Survey - digital maturity tracking
3. ICJ corpus - international law research
4. WTO disputes - trade governance
5. IDEA election data - voter turnout analysis
6. HDX - humanitarian governance
7. Municipal CKAN aggregator - city-level data

### Phase 3 (Specialized - P3 sources)
1. Bundestag deep integration - German federal analysis
2. ProZorro model - procurement best practices
3. Regional court systems - expansion

---

*Document compiled for CSOAI.org Governance Hive. All sources verified as free/open access as of compilation date. URLs and APIs subject to change; please verify current status before integration.*
