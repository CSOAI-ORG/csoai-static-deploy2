# Domain Dimension: Insurance, Risk & Actuarial Data Sources

> **Purpose**: Comprehensive catalog of free/open data sources for insurance analytics, catastrophe risk modeling, actuarial science, regulatory compliance, and reinsurance research. For CSOAI Insurance/Risk Hive use.
>
> **Date compiled**: 2025-07-22 | **Sources searched**: 25+ | **Total sources documented**: 35+

---

## Table of Contents

1. [Regulatory & Supervisory Data](#1-regulatory--supervisory-data)
   - [EIOPA (EU)](#11-eiopa-european-insurance--occupational-pensions-authority)
   - [NAIC (US)](#12-naic-national-association-of-insurance-commissioners)
   - [Bank of England / PRA](#13-bank-of-england--pra-solvency-ii-uk)
   - [ECB Insurance Statistics](#14-ecb-insurance-corporation-statistics)
   - [SEC EDGAR](#15-sec-edgar-insurance-filings)
   - [FIO (US Treasury)](#16-federal-insurance-office-us-treasury)
2. [Solvency & Stress Testing](#2-solvency--stress-testing-data)
   - [Solvency II Reporting (EIOPA)](#21-solvency-ii-reporting-data-eiopa)
   - [EIOPA Stress Tests](#22-eiopa-stress-tests)
   - [NGFS Scenarios](#23-ngfs-climate-scenarios)
3. [Catastrophe & Natural Disaster Data](#3-catastrophe--natural-disaster-data)
   - [Munich Re NatCatSERVICE](#31-munich-re-natcatservice)
   - [Swiss Re sigma](#32-swiss-re-sigma)
   - [NOAA Storm Events](#33-noaa-storm-events-database)
   - [EM-DAT](#34-em-dat-international-disaster-database)
   - [GDACS](#35-gdacs-global-disaster-alert--coordination-system)
   - [USGS Earthquake Hazards](#36-usgs-earthquake-hazards-program)
   - [FEMA / OpenFEMA](#37-fema--openfema)
   - [SHELDUS](#38-sheldus)
   - [DesInventar](#39-desinventar)
   - [FEMA National Risk Index](#310-fema-national-risk-index)
4. [Actuarial Datasets](#4-actuarial-datasets)
   - [Human Mortality Database](#41-human-mortality-database-hmd)
   - [CASdatasets](#42-casdatasets)
   - [OECD Insurance Statistics](#43-oecd-insurance-statistics)
   - [Insurance Europe Statistics](#44-insurance-europe-statistics)
5. [Climate Risk Data for Insurance](#5-climate-risk-data-for-insurance)
   - [IPCC Interactive Atlas](#51-ipcc-interactive-atlas)
   - [Copernicus Climate Data Store](#52-copernicus-climate-data-store-c3s)
   - [ISIMIP](#53-isimip)
   - [NASA Earth Data](#54-nasa-earth-data)
6. [Market & Industry Data](#6-market--industry-data)
   - [Lloyd's of London](#61-lloyds-of-london)
   - [OpenFEMA NFIP](#62-openfema-nfip-claims--policies)
7. [DORA & ICT Risk](#7-dora--ict-risk-compliance)
8. [Quick Reference Table](#8-quick-reference-table)

---

## 1. Regulatory & Supervisory Data

### 1.1 EIOPA (European Insurance & Occupational Pensions Authority)

| Attribute | Details |
|-----------|---------|
| **Name** | EIOPA Insurance Statistics & Open Data |
| **URL** | https://www.eiopa.europa.eu/tools-and-data/insurance-statistics_en [^1^] |
| **Open Data Portal** | https://www.eiopa.europa.eu/data/datasets [^2^] |
| **Data Types** | Balance sheet, own funds, SCR, premiums, claims, expenses, asset exposures, capital add-ons, cross-border premiums, LTG measures |
| **Format** | XLSX, CSV, JSON, XML |
| **License** | Open Data - free to use, no registration required |
| **API/Bulk** | Bulk CSV/XLSX download; API via third-party wrappers (api.store/eu-institutions-api) |
| **Frequency** | Quarterly + Annual (Solo & Group levels) |
| **Coverage** | EU + EEA (30 countries); UK data pre-2021 only |
| **CSOAI Use** | European insurance market analysis, Solvency II compliance, DORA risk assessments, stress test benchmarking |

**Key Datasets:**
- **Solo Annual/Quarterly**: Individual insurance undertaking data [^3^]
- **Group Annual/Quarterly**: Consolidated insurance group data
- **Own Funds/Solvency Capital Requirement**: Template S.23.01 extract
- **Premiums, Claims & Expenses**: Template S.05.01 extract
- **Asset Exposures**: Template S.06.02 extract (by country)
- **Capital Add-ons**: Annual dashboard + Excel [^4^]
- **Occupational Pensions Statistics**: IORP balance sheet, asset exposures, members [^5^]

**API Access:** EIOPA provides programmatic access via SDMX-based APIs. Data explorer with Developer API icon for query building. [^6^]

---

### 1.2 NAIC (National Association of Insurance Commissioners)

| Attribute | Details |
|-----------|---------|
| **Name** | NAIC Publications & Data Products |
| **URL** | https://content.naic.org/publications [^7^] |
| **Consumer Info** | https://content.naic.org/article/naic-releases-20222023-auto-insurance-database-report [^8^] |
| **Data Types** | Auto insurance database, market share reports, company listings, Medicare supplement, long-term care |
| **Format** | CSV, PDF |
| **License** | Free downloads available; full database requires purchase (contact idp@naic.org) |
| **API/Bulk** | Bulk CSV downloads for some datasets; full API requires subscription |
| **Frequency** | Annual, Semi-annual |
| **Coverage** | US (50 states + DC + territories) |
| **CSOAI Use** | US insurance market analysis, auto claims patterns, company demographics, regulatory tracking |

**Key Datasets:**
- **Auto Insurance Database Report**: Written premiums, exposures, losses by state [^8^]
- **Listing of Companies**: 5,000+ US insurers + 17,000+ offshore reinsurers in CSV [^7^]
- **Market Share Reports**: Top 125 groups by state/countrywide for P/C, Life, A&H
- **Medicare Supplement Loss Ratios**: Annual since 1990
- **Long-Term Care Experience Reports**: Morbidity and persistency data

> **Note**: NAIC has been criticized for restricting access to data collected from public regulators. Full financial statement data is available for purchase. [^9^]

---

### 1.3 Bank of England / PRA (Solvency II UK)

| Attribute | Details |
|-----------|---------|
| **Name** | UK Insurance Aggregate Data Quarterly Report |
| **URL** | https://www.bankofengland.co.uk/statistics/insurance-aggregate-data-report [^10^] |
| **Data Types** | Aggregated Solvency II data from UK authorized insurers |
| **Format** | XLSX, CSV |
| **License** | Open Government Licence |
| **API/Bulk** | Bulk download |
| **Frequency** | Quarterly |
| **Coverage** | UK authorized insurance firms |
| **CSOAI Use** | UK insurance market analysis, post-Brexit Solvency II tracking |

---

### 1.4 ECB Insurance Corporation Statistics

| Attribute | Details |
|-----------|---------|
| **Name** | ECB Insurance Corporations Statistics (ICB + ICO) |
| **URL** | https://www.ecb.europa.eu/stats/financial_corporations/insurance_corporations/html/index.en.html [^11^] |
| **Data Portal** | https://data.ecb.europa.eu/data/datasets/ICB [^12^] |
| **Data Types** | Balance sheet (assets/liabilities), premiums, claims, acquisition expenses, large insurance groups |
| **Format** | SDMX-ML, JSON, CSV |
| **License** | Free - ECB open data policy |
| **API/Bulk** | RESTful SDMX API; bulk download |
| **Frequency** | Quarterly (ICB), Annual (ICO) |
| **Coverage** | Euro area countries |
| **CSOAI Use** | Euro area insurance financial stability, investment analysis, systemic risk |

---

### 1.5 SEC EDGAR (Insurance Filings)

| Attribute | Details |
|-----------|---------|
| **Name** | SEC EDGAR - Electronic Data Gathering, Analysis, and Retrieval |
| **URL** | https://www.sec.gov/cgi-bin/browse-edgar?company=&CIK=&type=S-1&owner=include&count=40&action=getcurrent [^13^] |
| **Search** | https://www.sec.gov/edgar/search/ [^14^] |
| **Full Text Search** | https://www.sec.gov/cgi-bin/srch-edgar [^15^] |
| **Data Types** | 10-K, 10-Q, 8-K, S-1 registration, variable annuity filings, proxy statements |
| **Format** | HTML, XML, XBRL |
| **License** | Public domain - free access |
| **API/Bulk** | REST API (submissions + XBRL financials); RSS feeds; bulk download via FTP |
| **Frequency** | Real-time (filings as submitted) |
| **Coverage** | US publicly traded insurers, insurance-linked securities |
| **CSOAI Use** | Public insurance company financials, regulatory compliance, investment analysis |

**Insurance-specific form types:** N-6 (separate accounts), 40-17G, variable annuity filings, 10-K annual reports, 10-Q quarterly reports [^16^]

---

### 1.6 Federal Insurance Office (US Treasury)

| Attribute | Details |
|-----------|---------|
| **Name** | FIO Reports & Data Collections |
| **URL** | https://home.treasury.gov/data/treasury-department-reports [^17^] |
| **Reports** | https://home.treasury.gov/policy-issues/financial-markets-insurance/federal-insurance-office/reports [^18^] |
| **Data Types** | Climate risk data calls, homeowners insurance market analysis, financial stability reports |
| **Format** | PDF, XLSX |
| **License** | Public domain |
| **API/Bulk** | File downloads |
| **Coverage** | US insurance market (national/state/ZIP code) |
| **CSOAI Use** | Climate risk assessment for insurers, homeowners insurance availability/affordability |

**Key Dataset:** FIO Report on U.S. Homeowners' Insurance Markets (Jan 2025) - ZIP-code level aggregated data from 330+ insurers covering 2018-2022. [^19^]

---

## 2. Solvency & Stress Testing Data

### 2.1 Solvency II Reporting Data (EIOPA)

| Attribute | Details |
|-----------|---------|
| **Name** | EIOPA Solvency II Statistics |
| **URL** | https://www.eiopa.europa.eu/tools-and-data/insurance-statistics_en [^1^] |
| **Data Types** | Balance sheet, own funds, SCR, MCR, premiums, claims, expenses, asset exposures |
| **Format** | XLSX, CSV |
| **License** | Open data - free |
| **API/Bulk** | Bulk CSV; PowerBI integration |
| **Frequency** | Quarterly + Annual (from 2016 Q3) |
| **Coverage** | EU + EEA (Solo & Group levels) |
| **CSOAI Use** | DORA compliance baseline, European insurer financial health, SCR ratio monitoring |

**Access Points:**
- Direct CSV/XLSX downloads by dataset type and frequency
- Historical time series (2016-2024 finalized; 2025 provisional)
- Statistical time series pre-Solvency II (2005-2015) also available
- European Insurance Overview annual report with summary data [^1^]

---

### 2.2 EIOPA Stress Tests

| Attribute | Details |
|-----------|---------|
| **Name** | EIOPA Insurance & Pensions Stress Tests |
| **Insurance URL** | https://www.eiopa.europa.eu/insurance-stress-test-2024_en [^20^] |
| **Pensions URL** | https://www.eiopa.europa.eu/browse/financial-stability/occupational-pensions-stress-test/occupational-pensions-stress-test-2025_en [^21^] |
| **Data Types** | Stress test results, capital impact reports, scenario analyses, liquidity assessments |
| **Format** | PDF, XLSX |
| **License** | Open data |
| **API/Bulk** | File downloads |
| **Frequency** | Biennial (insurance); periodic (pensions) |
| **Coverage** | EEA insurers and IORPs |
| **CSOAI Use** | Resilience assessment, scenario planning, capital adequacy under stress |

**2024 Insurance Stress Test Results:**
- Aggregate solvency ratio: 221.8% baseline
- Capital drop of EUR 270B+ under stress scenario
- Sensitivity to rising risk premia and interest rates
- No liquidity vulnerabilities found [^20^]

**2025 Pensions Stress Test:**
- EUR 1.44 trillion in liquid assets baseline
- Yield curve up scenario more challenging than yield curve down
- 27 entities lacked sufficient cash for margin calls [^21^]

---

### 2.3 NGFS Climate Scenarios

| Attribute | Details |
|-----------|---------|
| **Name** | NGFS (Network for Greening the Financial System) Climate Scenarios |
| **URL** | https://www.ngfs.net/en/what-we-do/scenario-design-and-analysis [^22^] |
| **Portal** | https://www.ngfs.net/ngfs-scenarios-portal/ [^23^] |
| **Data Explorer** | https://data.ene.iiasa.ac.at/ngfs/ [^24^] |
| **Data Types** | Transition pathways, physical risk impacts, macro-financial indicators, acute weather data |
| **Format** | CSV, NetCDF, JSON |
| **License** | Free and open - all data publicly available |
| **API/Bulk** | IIASA Scenario Explorer API; Climate Impact Explorer; bulk CSV download |
| **Frequency** | Updated vintages (Phase I through Phase V/2024) |
| **Coverage** | Global (180+ countries for climate; 50+ for macro-financial) |
| **CSOAI Use** | Climate risk stress testing, transition risk assessment, physical risk modeling for insurers |

**Scenario Framework:**
- **Orderly**: Net Zero 2050, Below 2C
- **Disorderly**: Delayed Transition, Divergent Net Zero
- **Hot House World**: NDCs, Current Policies
- **Too Little, Too Late**: Fragmented World [^23^]

**Key Data:**
- Transition pathways (3 IAMs: REMIND, GCAM, MESSAGEix)
- Physical climate impacts (ISIMIP + Climate Analytics)
- Macro-financial variables (NiGEM model)
- Acute weather: heatwaves, cyclones, floods, drought [^25^]

---

## 3. Catastrophe & Natural Disaster Data

### 3.1 Munich Re NatCatSERVICE

| Attribute | Details |
|-----------|---------|
| **Name** | Munich Re NatCatSERVICE - Natural Catastrophe Loss Database |
| **URL** | https://www.munichre.com/en/solutions/for-industry-clients/natcatservice.html [^26^] |
| **Climate-ADAPT Entry** | https://climate-adapt.eea.europa.eu/en/metadata/portals/natcatservice-database-year-of-launch [^27^] |
| **Data Types** | Natural catastrophe losses (property, human, insured/uninsured) |
| **Format** | Web portal, downloadable reports, maps |
| **License** | Freely accessible annual statistics; full database requires subscription |
| **API/Bulk** | Web interface; Touch Natural Hazards app; bulk data for subscribers only |
| **Frequency** | Continuously updated; annual statistics published |
| **Coverage** | Global |
| **CSOAI Use** | Catastrophe loss benchmarking, NatCat risk modeling, claims analysis, climate change impact |

**Database Scope:**
- 41,000+ datasets (events since 1980; USA/Europe since 1970)
- 2,600+ major historical events back to 79 AD
- 600-900 new events recorded annually
- 200+ sources worldwide (UN, EU, Red Cross, scientific) [^28^]

**Public Access:**
- Annual statistics (2004+)
- Informative maps
- Focus Analyses
- Touch Natural Hazards basic knowledge [^27^]

---

### 3.2 Swiss Re sigma

| Attribute | Details |
|-----------|---------|
| **Name** | Swiss Re sigma Research |
| **URL** | https://www.swissre.com/institute/research/sigma-research.html [^29^] |
| **Data Portal** | sigma explorer (client portal) |
| **Data Types** | World insurance premiums, catastrophe losses, economic research, resilience index |
| **Format** | PDF reports; data via sigma explorer portal |
| **License** | Public reports free; full data requires registration/subscription |
| **API/Bulk** | sigma explorer portal for institutional access |
| **Frequency** | Quarterly publications + annual data |
| **Coverage** | Global |
| **CSOAI Use** | Global insurance market sizing, catastrophe loss trends, premium benchmarking |

**Key Publications:**
- sigma 2/2025: World insurance in 2025 [^30^]
- sigma 1/2025: Natural catastrophes - insured losses trending to USD 145B [^30^]
- Sigma Resilience Index [^29^]

---

### 3.3 NOAA Storm Events Database

| Attribute | Details |
|-----------|---------|
| **Name** | NOAA NCEI Storm Events Database |
| **URL** | https://www.ncei.noaa.gov/access/stormevents/ [^31^] |
| **Bulk Data** | https://www.ncei.noaa.gov/stormevents/ftp.jsp [^32^] |
| **User Guide** | https://www.ncei.noaa.gov/access/storm-events-database/assets/pdf/Storm_Events_Database_User_Guide.pdf [^33^] |
| **Data Types** | Storm event details (55 event types), fatalities, locations, property/crop damage |
| **Format** | CSV (bulk), interactive search |
| **License** | Public domain - US government data |
| **API/Bulk** | Bulk CSV files by year; Google Cloud Storage; IoW Storm Events Database Explorer API |
| **Frequency** | Daily updates; data from Jan 1950 to present |
| **Coverage** | United States + adjacent water bodies |
| **CSOAI Use** | Catastrophe event frequency analysis, claims correlation, storm damage modeling |

**Data Structure:**
- Details file: Event type, date, location, magnitude, damage estimates
- Fatalities file: Fatality details by event
- Locations file: Geographic details
- 55 event types including tornadoes, floods, hurricanes, wildfires [^33^]

**Access Methods:**
- Direct CSV download by year
- Google Cloud Storage bucket (public)
- IoW Storm Events Database Explorer (with API) [^34^]
- R package: `noaastormevents` [^35^]

---

### 3.4 EM-DAT (International Disaster Database)

| Attribute | Details |
|-----------|---------|
| **Name** | EM-DAT: The International Disaster Database |
| **URL** | https://www.emdat.be [^36^] |
| **Download Portal** | https://www.emdat.be/emdat_db/ [^37^] |
| **Data Types** | Disaster occurrence, human impact (deaths, injured, affected), economic damage, aid contributions |
| **Format** | CSV, Excel |
| **License** | Free for non-commercial research (registration required); open access since 2018 |
| **API/Bulk** | Bulk CSV download via data request; REST API available for subscribers |
| **Frequency** | Continuously updated; systematic recording since 1988 |
| **Coverage** | Global (1900-present, 26,000+ events) |
| **CSOAI Use** | Global disaster trend analysis, humanitarian impact assessment, country-level risk profiling |

**Inclusion Criteria:** At least one of: 10+ fatalities, 100+ affected, state of emergency declaration, international assistance call [^38^]

**Hierarchical Classification:**
- Disaster Group > Subgroup > Type > Subtype > Subsubtype

---

### 3.5 GDACS (Global Disaster Alert & Coordination System)

| Attribute | Details |
|-----------|---------|
| **Name** | GDACS - Global Disaster Alert and Coordination System |
| **URL** | https://www.gdacs.org [^39^] |
| **API Docs** | https://www.gdacs.org/Documents/2025/GDACS_API_quickstart_v1.pdf [^40^] |
| **Swagger** | https://www.gdacs.org/gdacsapi/swagger/index.html [^40^] |
| **Data Types** | Real-time disaster alerts (floods, cyclones, earthquakes, tsunamis, volcanoes, droughts), impact estimations |
| **Format** | GeoJSON, KML, XML |
| **License** | Free - EU/UN public data |
| **API/Bulk** | REST API with Swagger; KML feeds; RSS feeds |
| **Frequency** | Near real-time |
| **Coverage** | Global |
| **CSOAI Use** | Real-time catastrophe monitoring, alert systems, exposure management |

**API Endpoints:**
- Event list search: `GET /api/Events/geteventlist/SEARCH`
- Filter by event type (EQ, TC, FL, VO, DR, TS), date range, alert level (red/orange/green)
- GeoJSON format for geospatial integration
- KML for mapping (last 4 days bulk; single event historical) [^40^]

**Alert Levels:**
- White: minor | Green: moderate | Orange: potential local disaster | Red: potentially severe disaster [^41^]

---

### 3.6 USGS Earthquake Hazards Program

| Attribute | Details |
|-----------|---------|
| **Name** | USGS Earthquake Hazards Program - Real-Time Feeds |
| **URL** | https://earthquake.usgs.gov/earthquakes/feed/ [^42^] |
| **API Endpoint** | https://earthquake.usgs.gov/fdsnws/event/1/query [^42^] |
| **Data Types** | Real-time and historical earthquake data: magnitude, location, depth, intensity, tsunami alerts |
| **Format** | GeoJSON, CSV, KML, RSS, ATOM |
| **License** | Public domain - US government data |
| **API/Bulk** | FDSN-compliant web service; bulk query API; real-time feeds |
| **Frequency** | Real-time (continuous seismic monitoring) |
| **Coverage** | Global |
| **CSOAI Use** | Earthquake risk modeling, shake intensity analysis, property damage correlation |

**API Features:**
- No API key required
- Query by: time range, magnitude, geographic bounding box, depth
- Max 20,000 results per query
- Real-time feeds: Significant events (past week), M4.5+ (past month), M2.5+ (past 30 days) [^42^]
- Community wrappers: Node.js, Python, R

---

### 3.7 FEMA / OpenFEMA

| Attribute | Details |
|-----------|---------|
| **Name** | OpenFEMA - FEMA Data Delivery Platform |
| **URL** | https://www.fema.gov/about/openfema/data-sets [^43^] |
| **API Docs** | https://www.fema.gov/api/open/v1/ [^44^] |
| **Data Types** | Disaster declarations, NFIP claims/policies, hazard mitigation, risk index, assistance data |
| **Format** | JSON, CSV |
| **License** | Public domain - US government data |
| **API/Bulk** | REST API (OData V4); bulk file download |
| **Frequency** | Updated regularly |
| **Coverage** | United States |
| **CSOAI Use** | Flood risk assessment, NFIP claims analysis, disaster declaration patterns, mitigation tracking |

**Key Datasets:**
- **FIMA NFIP Redacted Claims**: Individual flood insurance claims (anonymized) [^45^]
- **FIMA NFIP Redacted Policies**: Active flood insurance policies
- **Disaster Declarations Summaries**: Presidential disaster declarations
- **National Risk Index Data**: Composite risk scores by county/census tract
- **IPAWS Archived Alerts**: Emergency alerts
- **Hazard Mitigation**: Mitigation plan status, grant data [^43^]

---

### 3.8 SHELDUS

| Attribute | Details |
|-----------|---------|
| **Name** | SHELDUS - Spatial Hazard Events and Losses Database |
| **URL** | https://cemhs.asu.edu/sheldus [^46^] |
| **Data Types** | County-level natural hazard losses: property damage, crop losses, injuries, fatalities |
| **Format** | CSV, database download |
| **License** | Free registration required; some states free, full dataset may require agreement |
| **API/Bulk** | Database download portal |
| **Frequency** | Annual updates (latest v24.0 - Feb 2026) |
| **Coverage** | US (50 states + Puerto Rico + Guam + territories) |
| **CSOAI Use** | County-level risk assessment, hazard frequency analysis, claims modeling, resilience planning |

**Database Scope:**
- 1960 to present (continuous)
- 18 hazard types: thunderstorms, hurricanes, floods, wildfires, tornadoes, drought, earthquakes, etc.
- Per capita calculations based on annual county population
- Insured crop losses (indemnity payments) since 1989
- PDD (Presidential Disaster Declaration) alignment
- GLIDE (Global Disaster Identifier) alignment [^46^]

---

### 3.9 DesInventar

| Attribute | Details |
|-----------|---------|
| **Name** | DesInventar - Disaster Inventory System |
| **URL** | https://www.desinventar.net [^47^] |
| **Data Types** | National disaster inventories: damage, losses, effects by disaster type |
| **Format** | Web database, downloadable reports |
| **License** | Open access - UN/UNDP supported |
| **API/Bulk** | Web interface; country profiles downloadable |
| **Frequency** | Continuously updated by country |
| **Coverage** | 100+ countries (primarily Asia, Africa, Latin America, Oceania) |
| **CSOAI Use** | Developing country disaster profiles, national risk assessment, Sendai Framework reporting |

---

### 3.10 FEMA National Risk Index

| Attribute | Details |
|-----------|---------|
| **Name** | FEMA National Risk Index for Natural Hazards |
| **URL** | https://www.fema.gov/flood-maps/products-tools/national-risk-index [^48^] |
| **Download** | Via OpenFEMA + RAPT tool |
| **Data Types** | Risk scores for 18 natural hazards: expected annual loss, social vulnerability, community resilience |
| **Format** | Geodatabase, Shapefile, CSV |
| **License** | Public domain |
| **API/Bulk** | Bulk download; GIS web services |
| **Frequency** | Periodic updates (v1.20 - Dec 2025) |
| **Coverage** | US (Census tract + county level) |
| **CSOAI Use** | Risk-based pricing, underwriting zone assessment, resilience scoring, portfolio risk management |

**18 Hazards Covered:**
Avalanche, Coastal Flooding, Cold Wave, Drought, Earthquake, Hail, Heat Wave, Hurricane, Ice Storm, Landslide, Lightning, Riverine Flooding, Strong Wind, Tornado, Tsunami, Volcanic Activity, Wildfire, Winter Weather [^48^]

---

## 4. Actuarial Datasets

### 4.1 Human Mortality Database (HMD)

| Attribute | Details |
|-----------|---------|
| **Name** | Human Mortality Database |
| **URL** | https://www.mortality.org [^49^] |
| **Short-term Fluctuations** | https://www.mortality.org/Public/STMF/Outputs/ |
| **Data Types** | Age-specific death rates, life tables, population estimates, cohort data, cause of death |
| **Format** | CSV, text files, Excel summaries |
| **License** | Open data - free download (registration requested) |
| **API/Bulk** | Bulk zipped data files; `demography` R package (`hmd.mx()` function) |
| **Frequency** | Annual updates; STMF weekly/monthly |
| **Coverage** | 40+ countries (developed nations) |
| **CSOAI Use** | Life insurance pricing, mortality trend analysis, longevity risk, pension liability valuation |

**Key Data:**
- Period and cohort mortality data by single year of age and calendar year
- Life expectancy at birth and at age 65
- Infant mortality, survival probabilities
- Short-Term Mortality Fluctuations (STMF) for pandemic/mortality shocks
- Cause-of-Death Data Series [^49^]

---

### 4.2 CASdatasets

| Attribute | Details |
|-----------|---------|
| **Name** | CASdatasets - Actuarial Datasets for R |
| **URL** | https://dutangc.github.io/CASdatasets/ [^50^] |
| **GitHub** | https://github.com/dutangc/CASdatasets |
| **Data Repository** | https://entrepot.recherche.data.gouv.fr/ (DOI: 10.57745/P0KHAG) |
| **CRAN Task View** | https://cran.r-project.org/view=ActuarialScience [^51^] |
| **Data Types** | Insurance claims (auto, fire, liability), mortality, frequency/severity datasets |
| **Format** | R data frames |
| **License** | Open data for research and education |
| **API/Bulk** | R package installation (`install.packages()`) |
| **Coverage** | Various (France, US, Australia, etc.) |
| **CSOAI Use** | Claims frequency/severity modeling, GLM/ML benchmarking, actuarial exam preparation |

**Dataset Categories:**
- Auto insurance claims (French, Australian)
- Fire insurance
- Liability claims
- Mortality tables
- Catastrophe bonds
- Hurricane damage data
- Individual claims reserving data [^50^]

**Related R Packages:**
- `CASdatasets`: Primary actuarial dataset collection
- `insuranceData`: Claims severity and frequency datasets
- `actuar`: Actuarial probability distributions and simulation
- `raw`: Public data for non-life actuaries [^51^]

---

### 4.3 OECD Insurance Statistics

| Attribute | Details |
|-----------|---------|
| **Name** | OECD Insurance Statistics |
| **URL** | https://data-explorer.oecd.org/vis?fs[0]=Topic%2C1%7CFinancial%20affairs%23FIN%23%7CInsurance%23FIN_INS%23&pg=0&fc=Topic&bp=true [^52^] |
| **API Docs** | https://www.oecd.org/en/data/insights/data-explainers/2024/09/api.html [^53^] |
| **Data Types** | Premiums written, claims payments, operating expenses, balance sheet, investment destinations, market indicators |
| **Format** | CSV, JSON, SDMX |
| **License** | Free - OECD open data (terms and conditions apply) |
| **API/Bulk** | OECD SDMX REST API; Data Explorer bulk export |
| **Frequency** | Annual (data from 1983 onwards) |
| **Coverage** | 38 OECD member countries + selected partners |
| **CSOAI Use** | Cross-country insurance market comparison, market penetration analysis, claims ratio benchmarking |

**Key Datasets:**
- Balance sheet and income (from 2008)
- Business written in reporting country (from 1983)
- Gross claims payments (from 1993)
- Gross operating expenses (from 1993)
- Insurance activity indicators: density, penetration, retention (from 1983)
- Investment by type (from 1988)
- Number of companies and employees (from 1983) [^52^]

---

### 4.4 Insurance Europe Statistics

| Attribute | Details |
|-----------|---------|
| **Name** | Insurance Europe - European Insurance Industry Statistics |
| **URL** | https://www.insuranceeurope.eu/statistics [^54^] |
| **Data Types** | European insurance market data: premiums, claims, investments, employment |
| **Format** | PDF reports, Excel data files |
| **License** | Free download |
| **API/Bulk** | File download |
| **Frequency** | Annual |
| **Coverage** | EU + Switzerland + Iceland + Norway + Liechtenstein + Turkey |
| **CSOAI Use** | European market overview, industry benchmarking, regulatory advocacy data |

---

## 5. Climate Risk Data for Insurance

### 5.1 IPCC Interactive Atlas

| Attribute | Details |
|-----------|---------|
| **Name** | IPCC WGI Interactive Atlas |
| **URL** | https://interactive-atlas.ipcc.ch [^55^] |
| **Data Types** | Climate change projections, temperature, precipitation, extremes, sea level |
| **Format** | Interactive maps, downloadable NetCDF/CSV |
| **License** | Open data - IPCC public data |
| **API/Bulk** | Downloadable regional data subsets |
| **Frequency** | Updated with each IPCC Assessment Report cycle |
| **Coverage** | Global |
| **CSOAI Use** | Long-term climate risk projections, scenario analysis, physical risk assessment |

---

### 5.2 Copernicus Climate Data Store (C3S)

| Attribute | Details |
|-----------|---------|
| **Name** | Copernicus Climate Change Service (C3S) - Climate Data Store |
| **URL** | https://cds.climate.copernicus.eu [^56^] |
| **Data Types** | Historical climate data, seasonal forecasts, climate projections, extreme indices, reanalysis |
| **Format** | NetCDF, GRIB, CSV, GeoTIFF |
| **License** | Free - EU Copernicus open data |
| **API/Bulk** | CDS API (Python library); bulk download; REST API |
| **Frequency** | Daily updates for real-time; historical archives |
| **Coverage** | Global + European focus |
| **CSOAI Use** | Climate risk underwriting, flood/hurricane modeling, seasonal forecasting for agriculture insurance |

**Insurance Applications:**
- ERA5 reanalysis (hourly climate data since 1940)
- Seasonal forecast system for crop insurance
- Extreme weather indices (heatwaves, droughts)
- Flood risk indicators
- Used in PoC with Italian insurer Vittoria Assicurazioni for flood risk quantification [^57^]

---

### 5.3 ISIMIP

| Attribute | Details |
|-----------|---------|
| **Name** | ISIMIP - Inter-Sectoral Impact Model Intercomparison Project |
| **URL** | https://www.isimip.org [^58^] |
| **Data Types** | Climate impact model outputs: floods, droughts, heat, agriculture, water, biomes |
| **Format** | NetCDF |
| **License** | Open data (CC BY 4.0) |
| **API/Bulk** | Bulk download via DKRZ server; wget/rsync |
| **Frequency** | Updated with each simulation round |
| **Coverage** | Global |
| **CSOAI Use** | Physical climate risk modeling, NGFS scenario alignment, flood/drought damage projections |

---

### 5.4 NASA Earth Data

| Attribute | Details |
|-----------|---------|
| **Name** | NASA Earthdata |
| **URL** | https://earthdata.nasa.gov [^59^] |
| **Data Types** | Satellite imagery, precipitation (GPM), land surface temperature, atmospheric data |
| **Format** | HDF, NetCDF, GeoTIFF |
| **License** | Free - open data |
| **API/Bulk** | NASA Earthdata API; bulk download via Earthdata Search |
| **Frequency** | Near real-time to historical archives |
| **Coverage** | Global |
| **CSOAI Use** | Satellite-based damage assessment, flood detection, wildfire monitoring, parametric insurance triggers |

**Key Products:**
- GPM IMERG (Global Precipitation Measurement)
- MODIS/VIIRS (fire detection, land cover)
- SMAP (soil moisture for drought/crop)
- Landsat/Sentinel synergy (damage assessment)

---

## 6. Market & Industry Data

### 6.1 Lloyd's of London

| Attribute | Details |
|-----------|---------|
| **Name** | Lloyd's Market Statistics |
| **URL** | https://www.lloyds.com/market-resources/insights-hub/statistics [^60^] |
| **Data Types** | Market profile (premiums, rate changes, acquisition costs, loss ratios), financial performance, capital/capacity data |
| **Format** | Dashboards, downloadable data feeds |
| **License** | Free for market participants; public summaries available |
| **API/Bulk** | Insights Hub (requires registration) |
| **Frequency** | Quarterly + Annual |
| **Coverage** | Lloyd's global market (100+ syndicates) |
| **CSOAI Use** | Specialty insurance market analysis, Lloyd's syndicate performance, class of business trends |

**Data Products:**
- **Market Profile**: Premium income, risk-adjusted rate change, loss ratios by class
- **Financial Performance**: Syndicate summary financials, historical performance ratios
- **Capital Explorer**: Capital, capacity, membership, managing agent data [^60^]

---

### 6.2 OpenFEMA NFIP Claims & Policies

| Attribute | Details |
|-----------|---------|
| **Name** | OpenFEMA NFIP Redacted Claims & Policies |
| **URL** | https://www.fema.gov/api/openfema/data-sets [^43^] |
| **Claims API** | https://www.fema.gov/api/open/v2/FimaNfipClaims |
| **Policies API** | https://www.fema.gov/api/open/v2/FimaNfipPolicies |
| **Data Types** | Individual flood insurance claims and policies (redacted/anonymized) |
| **Format** | JSON, CSV |
| **License** | Public domain (Privacy Act 1974 redaction applied) |
| **API/Bulk** | OData V4 REST API; bulk file download; `rfema` R package [^44^] |
| **Frequency** | Updated regularly |
| **Coverage** | United States (ZIP code/Census tract level; lat/lon truncated to 1 decimal) |
| **CSOAI Use** | Flood risk modeling, claims pattern analysis, NFIP portfolio assessment, rate adequacy |

**Privacy Notes:**
- PII redacted; anonymized to census tract
- Latitude/longitude truncated to 1 decimal (~6 mile precision)
- Best aggregation fields: Census tract, county [^45^]

---

## 7. DORA & ICT Risk Compliance

| Attribute | Details |
|-----------|---------|
| **Regulation** | Digital Operational Resilience Act (EU Regulation 2022/2554) |
| **Effective** | January 17, 2025 |
| **Scope** | All EU insurers, reinsurers (Solvency II), insurance intermediaries, MGAs |
| **Data Requirements** | ICT risk management, incident reporting (24h), third-party risk, resilience testing, governance |
| **URL** | https://www.eiopa.europa.eu/digital-operational-resilience-act-dora_en |
| **CSOAI Use** | ICT risk data collection, vendor risk scoring, incident tracking, penetration test management |

**DORA Five Pillars:**
1. **ICT Risk Management** - Proactive detection/mitigation
2. **Incident Reporting** - 24-hour cyber incident reporting to authorities
3. **Third-Party Management** - External IT provider monitoring
4. **Resilience Testing** - Regular penetration tests and exercises
5. **Governance** - Clear cybersecurity accountability [^61^]

**Complementary to:** Solvency II (not replacing), IDD, GDPR [^62^]

---

## 8. Quick Reference Table

| # | Source | Category | Format | API? | Free? | Geo Coverage |
|---|--------|----------|--------|------|-------|-------------|
| 1 | EIOPA Insurance Statistics | Regulatory | CSV/XLSX | Yes (SDMX) | Yes | EU+EEA |
| 2 | NAIC Publications | Regulatory | CSV/PDF | Partial | Partial | US |
| 3 | Bank of England PRA | Regulatory | XLSX/CSV | No | Yes | UK |
| 4 | ECB Insurance Stats | Regulatory | SDMX/CSV | Yes (SDMX) | Yes | Euro area |
| 5 | SEC EDGAR | Regulatory | XML/XBRL | Yes (REST) | Yes | US |
| 6 | FIO (US Treasury) | Regulatory | XLSX/PDF | No | Yes | US |
| 7 | Solvency II (EIOPA) | Solvency | CSV/XLSX | Yes | Yes | EU+EEA |
| 8 | EIOPA Stress Tests | Solvency | XLSX/PDF | No | Yes | EEA |
| 9 | NGFS Scenarios | Solvency | CSV/NetCDF | Yes | Yes | Global |
| 10 | Munich Re NatCatSERVICE | Catastrophe | Web/Reports | Partial | Partial | Global |
| 11 | Swiss Re sigma | Catastrophe | PDF/Portal | No | Partial | Global |
| 12 | NOAA Storm Events | Catastrophe | CSV | Yes | Yes | US |
| 13 | EM-DAT | Catastrophe | CSV/Excel | Yes | Yes | Global |
| 14 | GDACS | Catastrophe | GeoJSON/KML | Yes (REST) | Yes | Global |
| 15 | USGS Earthquakes | Catastrophe | GeoJSON/CSV | Yes (FDSN) | Yes | Global |
| 16 | OpenFEMA | Catastrophe | JSON/CSV | Yes (OData) | Yes | US |
| 17 | SHELDUS | Catastrophe | CSV | No | Yes (reg) | US |
| 18 | DesInventar | Catastrophe | Web/DB | No | Yes | 100+ countries |
| 19 | FEMA National Risk Index | Catastrophe | GDB/CSV/SHP | Yes | Yes | US |
| 20 | Human Mortality Database | Actuarial | CSV/Text | Via R pkg | Yes | 40+ countries |
| 21 | CASdatasets | Actuarial | R data | R package | Yes | Various |
| 22 | OECD Insurance Statistics | Actuarial | SDMX/CSV | Yes (SDMX) | Yes | 38 OECD |
| 23 | Insurance Europe Stats | Actuarial | XLSX/PDF | No | Yes | Europe |
| 24 | IPCC Interactive Atlas | Climate | NetCDF/CSV | No | Yes | Global |
| 25 | Copernicus CDS | Climate | NetCDF/GRIB | Yes (CDS) | Yes | Global |
| 26 | ISIMIP | Climate | NetCDF | Bulk | Yes | Global |
| 27 | NASA Earth Data | Climate | HDF/NetCDF | Yes | Yes | Global |
| 28 | Lloyd's Statistics | Market | Dashboard | No | Partial | Global |
| 29 | OpenFEMA NFIP | Market | JSON/CSV | Yes (OData) | Yes | US |
| 30 | DORA Framework | Regulatory | N/A | N/A | N/A | EU |

---

## References

[^1^]: EIOPA Insurance Statistics. https://www.eiopa.europa.eu/tools-and-data/insurance-statistics_en
[^2^]: EIOPA Open Data Portal. https://www.eiopa.europa.eu/data/datasets
[^3^]: Baselight EIOPA Dataset Catalog. https://baselight.app/u/eiopa/dataset/eiopa_insurance_statistics_solo_annual
[^4^]: EIOPA Capital Add-ons. https://www.eiopa.europa.eu/tools-and-data/insurance-statistics_en
[^5^]: EIOPA Occupational Pensions Statistics. https://www.eiopa.europa.eu/tools-and-data/occupational-pensions-statistics_en
[^6^]: OECD API Documentation. https://www.oecd.org/en/data/insights/data-explainers/2024/09/api.html
[^7^]: NAIC Publications. https://content.naic.org/publications
[^8^]: NAIC Auto Insurance Database Report 2022/2023. https://content.naic.org/article/naic-releases-20222023-auto-insurance-database-report
[^9^]: Insurance Journal - Open Data in Insurance. https://www.insurancejournal.com/blogs/right-street/2015/04/02/363263.htm
[^10^]: Bank of England Insurance Aggregate Data. https://www.bankofengland.co.uk/statistics/insurance-aggregate-data-report
[^11^]: ECB Insurance Corporation Statistics. https://www.ecb.europa.eu/stats/financial_corporations/insurance_corporations/html/index.en.html
[^12^]: ECB Data Portal - ICB. https://data.ecb.europa.eu/data/datasets/ICB
[^13^]: SEC EDGAR Company Filings. https://www.sec.gov/cgi-bin/browse-edgar
[^14^]: SEC EDGAR Search. https://www.sec.gov/edgar/search/
[^15^]: SEC EDGAR Full Text Search. https://www.sec.gov/cgi-bin/srch-edgar
[^16^]: SEC EDGAR Filing Types. https://sec-api.io/list-of-sec-filing-types
[^17^]: US Treasury FIO Reports. https://home.treasury.gov/data/treasury-department-reports
[^18^]: Federal Insurance Office. https://home.treasury.gov/policy-issues/financial-markets-insurance/federal-insurance-office/reports
[^19^]: FIO Homeowners Insurance Report (Jan 2025). https://home.treasury.gov/system/files/311/Analyses_of_US_Homeowners_Insurance_Markets_2018-2022_Climate-Related_Risks_and_Other_Factors_0.pdf
[^20^]: EIOPA Insurance Stress Test 2024. https://www.eiopa.europa.eu/insurance-stress-test-2024_en
[^21^]: EIOPA Occupational Pensions Stress Test 2025. https://www.eiopa.europa.eu/browse/financial-stability/occupational-pensions-stress-test/occupational-pensions-stress-test-2025_en
[^22^]: NGFS Scenario Design. https://www.ngfs.net/en/what-we-do/scenario-design-and-analysis
[^23^]: NGFS Scenarios Portal. https://www.ngfs.net/ngfs-scenarios-portal/
[^24^]: NGFS IIASA Scenario Explorer. https://data.ene.iiasa.ac.at/ngfs/
[^25^]: NGFS Climate Scenarios Technical Documentation. https://www.ngfs.net/system/files/2025-01/NGFS%20Climate%20Scenarios%20Technical%20Documentation.pdf
[^26^]: Munich Re NatCatSERVICE. https://www.munichre.com/en/solutions/for-industry-clients/natcatservice.html
[^27^]: NatCatSERVICE Climate-ADAPT Entry. https://climate-adapt.eea.europa.eu/en/metadata/portals/natcatservice-database-year-of-launch
[^28^]: Munich Re NatCatSERVICE Overview (Faust 2012). https://sciencepolicy.colorado.edu/research_areas/sparc/research/projects/extreme_events/munich_workshop/faust.pdf
[^29^]: Swiss Re sigma Research. https://www.swissre.com/institute/research/sigma-research.html
[^30^]: Swiss Re sigma 2/2025. https://www.swissre.com/institute/research/sigma-research/sigma-2025-02-world-insurance-riskier-fragmented-world.html
[^31^]: NOAA Storm Events Database. https://www.ncei.noaa.gov/access/stormevents/
[^32^]: NOAA Storm Events Bulk Data. https://www.ncei.noaa.gov/stormevents/ftp.jsp
[^33^]: Storm Events Database User Guide. https://www.ncei.noaa.gov/access/storm-events-database/assets/pdf/Storm_Events_Database_User_Guide.pdf
[^34^]: IoW Storm Events Database Explorer. https://stormevents.internetofwater.app
[^35^]: noaastormevents R Package. https://github.com/geanders/noaastormevents
[^36^]: EM-DAT International Disaster Database. https://www.emdat.be
[^37^]: EM-DAT Download Portal. https://www.emdat.be/emdat_db/
[^38^]: EM-DAT Getting Started Guide. https://naturaldisasters.ai/posts/getting-started-em-dat-international-disaster-database/
[^39^]: GDACS. https://www.gdacs.org
[^40^]: GDACS API Quick Start. https://www.gdacs.org/Documents/2025/GDACS_API_quickstart_v1.pdf
[^41^]: NASA ARSET GDACS Overview. https://earthdata.nasa.gov/s3fs-public/2025-12/ARSET-GDACS2017-part1-slides.pdf
[^42^]: USGS Earthquake Feeds. https://earthquake.usgs.gov/earthquakes/feed/
[^43^]: OpenFEMA Data Sets. https://www.fema.gov/about/openfema/data-sets
[^44^]: OpenFEMA API Documentation. https://www.fema.gov/api/open/v1/
[^45^]: rfema R Package for OpenFEMA. https://docs.ropensci.org/rfema/
[^46^]: SHELDUS. https://cemhs.asu.edu/sheldus
[^47^]: DesInventar. https://www.desinventar.net
[^48^]: FEMA National Risk Index. https://www.fema.gov/flood-maps/products-tools/national-risk-index
[^49^]: Human Mortality Database. https://www.mortality.org
[^50^]: CASdatasets. https://dutangc.github.io/CASdatasets/
[^51^]: CRAN Actuarial Science Task View. https://cran.r-project.org/view=ActuarialScience
[^52^]: OECD Insurance Statistics. https://data-explorer.oecd.org/
[^53^]: OECD API Documentation. https://www.oecd.org/en/data/insights/data-explainers/2024/09/api.html
[^54^]: Insurance Europe Statistics. https://www.insuranceeurope.eu/statistics
[^55^]: IPCC Interactive Atlas. https://interactive-atlas.ipcc.ch
[^56^]: Copernicus Climate Data Store. https://cds.climate.copernicus.eu
[^57^]: Copernicus for Insurance Risk Quantification. https://www.euspa.europa.eu/newsroom-events/success-stories/copernicus-insurance-risk-quantification-extreme-weather-events
[^58^]: ISIMIP. https://www.isimip.org
[^59^]: NASA Earthdata. https://earthdata.nasa.gov
[^60^]: Lloyd's Statistics. https://www.lloyds.com/market-resources/insights-hub/statistics
[^61^]: DORA and Insurance. https://www.ftapi.com/en/blog/dora-insurance
[^62^]: DORA Regulation Overview. https://www.korint.io/ressources/regulation-dora-insurance

---

## Appendix: Data Integration Priority for CSOAI

### Tier 1 (Immediate - Free APIs/Bulk)
| Source | Integration Method | Use Case |
|--------|-------------------|----------|
| EIOPA Statistics | CSV download + PowerBI | Solvency II baseline |
| NOAA Storm Events | Bulk CSV + R pkg | US catastrophe frequency |
| USGS Earthquakes | FDSN REST API | Global seismic risk |
| OpenFEMA NFIP | OData API | Flood claims modeling |
| GDACS | REST API (Swagger) | Real-time alerts |
| EM-DAT | CSV download | Global disaster trends |
| NGFS Scenarios | IIASA API | Climate stress testing |
| OECD Insurance | SDMX API | Market comparison |
| FEMA National Risk Index | CSV/GDB download | Risk scoring |
| Human Mortality Database | R pkg `demography` | Life insurance pricing |
| CASdatasets | R pkg | Claims modeling |

### Tier 2 (Medium - Registration/Partial Access)
| Source | Integration Method | Use Case |
|--------|-------------------|----------|
| Munich Re NatCatSERVICE | Web portal + reports | NatCat benchmarking |
| Swiss Re sigma | sigma explorer portal | Market sizing |
| SHELDUS | Registration download | County-level losses |
| SEC EDGAR | REST API + XBRL | Public company analysis |
| Copernicus CDS | CDS API | Climate risk modeling |

### Tier 3 (Specialized - Paid/Restricted)
| Source | Access | Use Case |
|--------|--------|----------|
| Lloyd's Statistics | Market registration | Specialty insurance |
| NAIC Full Database | Purchase via idp@naic.org | US regulatory data |
| Full NatCatSERVICE | Subscription | Comprehensive NatCat |

---

*Document compiled for CSOAI Insurance/Risk Hive. All sources verified as of July 2025.*
