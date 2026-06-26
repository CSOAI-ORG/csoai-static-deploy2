# Utilities, Mining, Water, Commodities & Resources Data Sources

> **CSOAI Domain Dimension: Utilities & Resources Hive**
> Comprehensive catalog of free/open data sources for energy grid, water utilities, mining, commodities, oil/gas, and mineral data.
> Last updated: 2025-07-11

---

## Table of Contents

1. [Energy & Electricity](#1-energy--electricity)
   - [1.1 US EIA (Energy Information Administration)](#11-us-eia)
   - [1.2 IRENA (International Renewable Energy Agency)](#12-irena)
   - [1.3 ENTSO-E (European Network of Transmission System Operators)](#13-entso-e)
   - [1.4 BP/Energy Institute Statistical Review](#14-bpenergy-institute)
   - [1.5 World Energy Council](#15-world-energy-council)
   - [1.6 OECD Energy Statistics](#16-oecd-energy-statistics)
2. [Mining & Minerals](#2-mining--minerals)
   - [2.1 USGS Mineral Commodity Summaries](#21-usgs-mineral-commodity-summaries)
   - [2.2 USGS Critical Minerals Data (Copper, Nickel, Lithium, Rare Earths)](#22-usgs-critical-minerals)
   - [2.3 Global Energy Monitor Mining Trackers](#23-global-energy-monitor-mining)
3. [Water](#3-water)
   - [3.1 WRI Aqueduct Water Risk Atlas](#31-wri-aqueduct)
   - [3.2 FAO AQUASTAT](#32-fao-aquastat)
   - [3.3 UN Water Data Portal](#33-un-water)
   - [3.4 US EPA Safe Drinking Water (ECHO)](#34-us-epa-sdw)
4. [Oil & Gas Infrastructure](#4-oil--gas-infrastructure)
   - [4.1 Global Energy Monitor - Oil & Gas Trackers](#41-gem-oil-gas)
5. [Commodity Prices](#5-commodity-prices)
   - [5.1 World Bank Commodity Price Data (Pink Sheet)](#51-world-bank)
   - [5.2 UNCTAD Commodity Price Index](#52-unctad)
   - [5.3 IMF Commodity Prices](#53-imf)
   - [5.4 Commodities-API (Free Tier)](#54-commodities-api)
6. [CSOAI Integration Summary](#6-csoai-integration-summary)

---

## 1. Energy & Electricity

### 1.1 US EIA (Energy Information Administration)

| Attribute | Detail |
|-----------|--------|
| **Name** | U.S. Energy Information Administration (EIA) Open Data API |
| **URL** | https://www.eia.gov/opendata/ |
| **Primary API** | https://api.eia.gov/v2/ |
| **Bulk Downloads** | https://www.eia.gov/opendata/bulkfiles.php |
| **Format** | JSON (API), CSV, Excel (add-ins), line-delimited JSON (bulk) |
| **License** | Public Domain (free, registration required for API key) |
| **API/Bulk** | RESTful API v2, bulk file downloads (updated 2x daily), Excel/Google Sheets add-ins |
| **Coverage** | United States + international energy data |

**Datasets Available:** [^1704^] [^1705^] [^1706^]

| Category | Series Count | Description |
|----------|-------------|-------------|
| **Electricity** | 408,000+ | Hourly operating data, generation, demand, power flows |
| **Petroleum** | 115,052 | Production, imports, refining, prices, consumption, stocks |
| **Natural Gas** | 11,989 | Production, pipelines, storage, prices, consumption |
| **Coal** | 132,331 | Production, mine-level data, consumption, quality, reserves |
| **Renewables/Biomass** | Densified biomass production, capacity, feedstocks |
| **Nuclear** | Daily outage reports from NRC |
| **Total Energy** | Production, prices, CO2 emissions, consumption by sector |
| **State Energy** | 30,000+ series for 50 states |
| **International** | 92,836 series - production, reserves, trade by country |
| **Short-Term Outlook** | 3,872 series (monthly projections) |
| **Annual Outlook** | 368,466 series (long-term projections to 2050) |

**CSOAI Use Case:** Primary US energy data source. Perfect for electricity demand forecasting, generation mix analysis, renewable energy tracking, CO2 emissions modeling, and cross-border power flow analysis.

**Access Notes:**
- Free API key registration at https://www.eia.gov/opendata/
- Bulk files available as ZIP (PET.zip, NG.zip, TOTAL.zip, etc.) [^1720^]
- Python packages: `EIAapi` (R) [^1710^], `eia` (Python/ropensci) [^1718^]
- Bulk files exceed 1GB for electricity data

---

### 1.2 IRENA (International Renewable Energy Agency)

| Attribute | Detail |
|-----------|--------|
| **Name** | IRENA Renewable Energy Statistics |
| **URL** | https://www.irena.org/Data |
| **Statistics Portal** | https://www.irena.org/statistics |
| **Format** | Excel (.xlsx), CSV, PDF reports |
| **License** | Openly licensed, freely usable with IRENA attribution |
| **API/Bulk** | Bulk download (no API), annual + annual updates |
| **Coverage** | 150+ countries and areas, 2000-present |

**Datasets Available:** [^1782^] [^1784^] [^1785^] [^1786^]

| Dataset | Time Range | Description |
|---------|-----------|-------------|
| **Renewable Capacity Statistics** | 2000-2024 | Installed capacity by technology (hydro, wind, solar, bio, geo, ocean) |
| **Renewable Generation Statistics** | 2000-2023 | Actual power generation in GWh by technology |
| **Renewable Energy Balances** | 2022-2023 | Supply, trade, consumption data by country |
| **Public Renewable Finance Flows** | 2014-2023 | Investment data from OECD-DAC and development banks (USD millions) |

**CSOAI Use Case:** Global renewable energy tracking, SDG 7 monitoring, energy transition analytics, clean energy investment trends, cross-country renewable comparison.

**Access Notes:**
- Annual publications in March (capacity) and July (full statistics)
- Data available at www.irena.org/statistics
- Country-level data validated from official national statistics

---

### 1.3 ENTSO-E (European Network of Transmission System Operators)

| Attribute | Detail |
|-----------|--------|
| **Name** | ENTSO-E Transparency Platform |
| **URL** | https://transparency.entsoe.eu/ |
| **File Library Guide** | https://transparencyplatform.zendesk.com/hc/en-us/articles/35960137882129 |
| **Format** | XML (API), CSV (bulk downloads), XLSX |
| **License** | Free (registration required), EU transparency regulation |
| **API/Bulk** | RESTful API, FTP server, CSV bulk extracts, File Library API |
| **Coverage** | 35+ European countries, real-time + historical |

**Datasets Available:** [^1707^] [^1709^] [^1711^] [^1712^] [^1714^]

| Category | Data Types | Granularity |
|----------|-----------|-------------|
| **Load** | System total load (forecast + actual) | Hourly, daily |
| **Generation** | Actual generation per type, installed capacity, generation forecast | Hourly, per fuel type |
| **Prices** | Day-ahead market prices, intraday prices | Hourly, daily |
| **Transmission** | Cross-border flows, transfer capacities, commercial exchanges | Hourly |
| **Outages** | Unavailability of generation units, transmission grid changes | Event-based |
| **Renewables** | Wind/solar forecast, actual renewable generation | Hourly |

**CSOAI Use Case:** European electricity market analysis, cross-border power flow modeling, renewable integration studies, price forecasting, grid stability assessment.

**Access Notes:**
- Register at https://transparency.entsoe.eu/ then email transparency@entsoe.eu for API token [^1711^]
- Python libraries: `entsoe-py` (unofficial but widely used) [^1712^]
- FTP server for bulk monthly CSV downloads
- File Library API: `https://fms.tp.entsoe.eu/` with Keycloak auth [^1707^]

---

### 1.4 BP/Energy Institute Statistical Review

| Attribute | Detail |
|-----------|--------|
| **Name** | Energy Institute Statistical Review of World Energy |
| **URL** | https://www.energyinst.org/statistical-review |
| **Data Downloads** | https://www.energyinst.org/statistical-review/resources-and-data-downloads |
| **Format** | Excel workbook, PDF, online charting tool, CSV |
| **License** | Free with attribution; S&P Global data requires separate authorization |
| **API/Bulk** | Bulk Excel download, online charting tool (no API) |
| **Coverage** | Global, historical data from 1965 for many sectors |

**Datasets Available:** [^1717^] [^1719^] [^1723^]

| Category | Description |
|----------|-------------|
| **Primary Energy** | Consumption by fuel, per capita, carbon emissions |
| **Oil** | Production, consumption, trade movements, prices, reserves, refinery throughput |
| **Natural Gas** | Production, consumption, trade, prices, reserves |
| **Coal** | Production, consumption, trade, reserves, R/P ratios |
| **Renewables** | Hydro, solar, wind, biofuels, geothermal generation |
| **Electricity** | Generation by fuel type, nuclear, renewables |
| **Carbon** | CO2 emissions from energy, flaring, CCUS |

**CSOAI Use Case:** Global energy trend analysis, long-term energy transition tracking, fossil fuel market intelligence, carbon emission benchmarking, country-level energy comparison.

**Access Notes:**
- Excel workbook and database format available for download
- Online energy charting tool for custom analysis
- Historical data from 1965; annual publication (June/July)
- Previously produced by BP; now managed by Energy Institute with KPMG [^1717^]

---

### 1.5 World Energy Council

| Attribute | Detail |
|-----------|--------|
| **Name** | World Energy Council - Energy Data Resources |
| **URL** | https://www.worldenergy.org/ |
| **Format** | Reports, interactive tools, country profiles |
| **License** | Free with registration for some tools |
| **API/Bulk** | No API; reports and data tools available |
| **Coverage** | 90+ member countries |

**Datasets Available:** [^1722^]

| Category | Description |
|----------|-------------|
| **World Energy Issues Monitor** | Annual survey of energy leaders' priorities |
| **Energy Trilemma Index** | Country ranking on energy security, equity, sustainability |
| **Country Profiles** | National energy data and policy overviews |
| **Resources** | Reports on energy transitions and policy |

**CSOAI Use Case:** Energy policy analysis, country-level energy assessment, sustainability benchmarking, trilemma framework analytics.

---

### 1.6 OECD Energy Statistics

| Attribute | Detail |
|-----------|--------|
| **Name** | OECD/IEA Energy Statistics |
| **URL** | https://data.oecd.org/energy.htm |
| **IEA Data Portal** | https://www.iea.org/data-and-statistics |
| **OECD.Stat** | https://stats.oecd.org/ |
| **Format** | CSV, Excel, SDMX, API (OECD.Stat) |
| **License** | Free for some datasets; subscription for detailed IEA data |
| **API/Bulk** | OECD.Stat API, bulk CSV downloads |
| **Coverage** | OECD countries + selected non-members (180+ countries/areas) |

**Datasets Available:** [^1720^] [^1721^] [^1724^]

| Dataset | Description |
|---------|-------------|
| **World Energy Statistics** | Commodity balances in physical units |
| **World Energy Balances** | Energy balances in energy units |
| **Energy Prices & Taxes** | Quarterly energy prices, world energy prices |
| **Renewables Information** | Renewable energy supply and consumption |
| **Monthly Electricity Statistics** | Production by fuel type, trade data |
| **Energy Efficiency Indicators** | End-use consumption by sector (2000-2022) |
| **Energy Technology RD&D Budgets** | Annual spending by technology (1974-present) |

**CSOAI Use Case:** Cross-country energy comparison, energy efficiency benchmarking, price analysis, technology investment tracking, decarbonization pathway modeling.

**Access Notes:**
- OECD.Stat extracts are free; no registration required [^1721^]
- Detailed IEA statistics may require subscription
- Data covers 180+ countries and regions

---

## 2. Mining & Minerals

### 2.1 USGS Mineral Commodity Summaries

| Attribute | Detail |
|-----------|--------|
| **Name** | USGS Mineral Commodity Summaries |
| **URL** | https://pubs.usgs.gov/publication/mcs2025 |
| **Data Release** | https://www.sciencebase.gov/catalog/item/65a6e45fd34e5af967a46749 |
| **Format** | PDF (report), Excel, CSV, ScienceBase data releases |
| **License** | Public Domain (US Government work) |
| **API/Bulk** | ScienceBase REST API, bulk CSV downloads |
| **Coverage** | Global, 90+ nonfuel mineral commodities, annual |

**Datasets Available:** [^1713^] [^1715^] [^1795^]

| Category | Description |
|----------|-------------|
| **Mineral Commodity Summaries** | Annual comprehensive report on 90+ minerals (212 pages) |
| **Country-Level Data** | Production, reserves, resources by country |
| **U.S. Data** | Domestic production, consumption, trade, tariffs |
| **Critical Minerals** | Special focus on 50 critical minerals list |
| **5-Year Statistics** | Salient statistics, trends, and issues |
| **World Production** | Global production data by mineral and country |

**CSOAI Use Case:** Mineral supply chain analysis, critical minerals risk assessment, mining industry economics, import dependency analysis, battery metals tracking (lithium, cobalt, nickel).

**Access Notes:**
- 30th annual edition published January 2025 [^1795^]
- Individual commodity data releases on ScienceBase with DOIs [^1793^]
- Copper data release: https://doi.org/10.5066/P13XCP3R
- Report available as free PDF; Excel data files downloadable

---

### 2.2 USGS Critical Minerals Data (Copper, Nickel, Lithium, Rare Earths)

| Attribute | Detail |
|-----------|--------|
| **Name** | USGS National Minerals Information Center - Commodity Statistics |
| **URL** | https://www.usgs.gov/centers/national-minerals-information-center |
| **Commodity Statistics** | https://www.usgs.gov/centers/national-minerals-information-center/commodity-statistics-and-information |
| **Format** | Excel, CSV, PDF, ScienceBase data releases |
| **License** | Public Domain |
| **API/Bulk** | ScienceBase API, individual commodity downloads |
| **Coverage** | Global, historical data by commodity |

**Commodity-Specific Pages:** [^1793^] [^1788^] [^1795^]

| Mineral | URL / Data Access |
|---------|-------------------|
| **Copper** | ScienceBase DOI: 10.5066/P13XCP3R |
| **Lithium** | USGS commodity page + MCS2025 |
| **Nickel** | USGS commodity page + MCS2025 |
| **Cobalt** | USGS commodity page + MCS2025 |
| **Rare Earths** | USGS commodity page + MCS2025 |
| **Platinum Group** | USGS commodity page + MCS2025 |
| **Gold** | USGS commodity page + MCS2025 |
| **Silver** | USGS commodity page + MCS2025 |

**CSOAI Use Case:** Battery supply chain analytics, critical minerals trade flow modeling, geopolitical risk assessment, EV material demand forecasting, production concentration analysis.

**Access Notes:**
- Each commodity has a dedicated statistics page with historical data
- ScienceBase data releases provide machine-readable formats
- 2024 data: U.S. mineral production valued at $106 billion [^1795^]
- Battery metals (cobalt, lithium, nickel) saw 40-60% price declines due to oversupply

---

### 2.3 Global Energy Monitor Mining Trackers

| Attribute | Detail |
|-----------|--------|
| **Name** | Global Energy Monitor (GEM) - Mining & Industry Trackers |
| **URL** | https://globalenergymonitor.org/ |
| **GEM Wiki** | https://www.gem.wiki/Main_Page |
| **Format** | CSV, Excel, XLSX, JSON (via API), interactive maps |
| **License** | Creative Commons (CC BY), free with attribution |
| **API/Bulk** | Direct download portal, API for filtered downloads |
| **Coverage** | Global, updated bi-annually |

**Trackers Available:** [^1753^] [^1762^] [^1765^]

| Tracker | Description |
|---------|-------------|
| **Global Coal Mine Tracker** | 7,000+ mines in 70 countries, production >1M tonnes/year |
| **Global Coal Terminals Tracker** | Import/export/domestic coal terminals |
| **Global Iron Ore Mines Tracker** | Operating, proposed, shelved, retired mines since 2023 |
| **Global Iron and Steel Tracker** | 500K+ tpa crude iron/steel production plants |

**CSOAI Use Case:** Coal mine tracking for transition finance, iron/steel supply chain analysis, terminal capacity assessment, fossil fuel infrastructure monitoring.

**Access Notes:**
- Download data via tracker pages (e.g., https://globalenergymonitor.org/projects/global-coal-plant-tracker) [^1755^]
- API endpoint: `https://api.globalenergymonitor.org/download` [^1754^]
- CSV and Excel formats available
- Each project has a footnoted wiki page with detailed information

---

## 3. Water

### 3.1 WRI Aqueduct Water Risk Atlas

| Attribute | Detail |
|-----------|--------|
| **Name** | World Resources Institute (WRI) Aqueduct Water Risk Atlas |
| **URL** | https://www.wri.org/applications/aqueduct/water-risk-atlas/ |
| **Data Download** | https://www.wri.org/data/aqueduct-water-risk-atlas |
| **GitHub** | https://github.com/wri/aqueduct30_data_download |
| **Format** | GeoPackage (.gpkg), Shapefile (.shp), CSV, QGIS/ArcMap project files |
| **License** | Creative Commons 4.0 (CC BY), free with WRI attribution |
| **API/Bulk** | Bulk download (full database + location analyzer), no API |
| **Coverage** | Global, watershed/catchment level (HydroSHEDS) |

**Datasets Available:** [^1727^] [^1728^] [^1731^] [^1734^] [^1738^] [^1739^]

| Dataset | Indicators |
|---------|-----------|
| **Baseline Annual** | 13 indicators: baseline water stress (bws), water depletion (bwd), interannual variability (iav), seasonal variability (sev), groundwater decline (gtd), riverine flood risk (rfr), coastal flood risk (cfr), drought risk (drr), untreated wastewater (ucw), coastal eutrophication (cep), drinking water access (udw), sanitation access (usa), RepRisk ESG index (rri) |
| **Baseline Monthly** | Monthly variations of key indicators |
| **Future Projections** | 2030, 2040, 2050, 2080 scenarios (optimistic, pessimistic, BAU) |
| **Aqueduct Floods** | Riverine and coastal flood hazard, risk, cost-benefit analysis |
| **Aqueduct Food** | Water risk for agriculture and food security |

**CSOAI Use Case:** Water risk assessment for corporate sites, ESG water scoring, supply chain water vulnerability, drought/flood risk modeling, climate adaptation planning, SDG 6 monitoring.

**Access Notes:**
- No login required; open data philosophy [^1728^]
- Full database download as ZIP with GeoPackage, Shapefile, CSV
- Location analyzer for site-specific risk assessment
- Updated every 4-5 years (Aqueduct 4.0 is latest)
- Metadata: https://github.com/wri/aqueduct30_data_download/blob/master/metadata.md [^1738^]

---

### 3.2 FAO AQUASTAT

| Attribute | Detail |
|-----------|--------|
| **Name** | FAO AQUASTAT - Global Information System on Water and Agriculture |
| **URL** | https://www.fao.org/aquastat/en/ |
| **Databases** | https://www.fao.org/aquastat/en/databases/ |
| **Core Database** | https://www.fao.org/aquastat/en/databases/maindatabase/ |
| **Format** | CSV, Excel, PDF reports |
| **License** | FAO Open Data License, free with attribution |
| **API/Bulk** | Bulk CSV/Excel download (no API) |
| **Coverage** | 200+ countries, 1960-2017 (5-year periods) |

**Datasets Available:** [^1729^] [^1735^] [^1740^] [^1743^] [^1744^]

| Category | Variables |
|----------|-----------|
| **Water Resources** | Surface water, groundwater, non-conventional sources |
| **Water Use** | Agricultural, domestic, industrial withdrawal |
| **Irrigation & Drainage** | Area, techniques, equipment, irrigated crops |
| **Dams & Reservoirs** | Detailed database on major dams |
| **Institutions** | Water-related institutions database |
| **SDG Indicators** | Indicators 6.4.1 (water-use efficiency) and 6.4.2 (water stress) |

**CSOAI Use Case:** Agricultural water analysis, irrigation efficiency benchmarking, SDG 6.4 monitoring, water stress assessment, crop-water productivity analysis.

**Access Notes:**
- 180+ variables and indicators for 200+ countries
- Data collected through annual country questionnaires
- 2025 AQUASTAT Water Data Snapshot shows 7% decline in renewable freshwater per capita over past decade [^1729^]
- Agriculture accounts for 72% of global freshwater withdrawals

---

### 3.3 UN Water Data Portal

| Attribute | Detail |
|-----------|--------|
| **Name** | UN-Water Data Portal / SDG 6 Data |
| **URL** | https://www.unwater.org/ |
| **SDG 6 Portal** | https://www.sdg6data.org/ |
| **UN Data** | https://data.un.org/ |
| **Format** | CSV, Excel, API (UNSD API) |
| **License** | UN Open Data, free |
| **API/Bulk** | Bulk download, UN Data API |
| **Coverage** | Global, country-level, time-series |

**Datasets Available:** [^1792^]

| SDG Target | Indicators |
|------------|-----------|
| **6.1** | Safely managed drinking water services |
| **6.2** | Safely managed sanitation |
| **6.3** | Wastewater treatment, ambient water quality |
| **6.4** | Water-use efficiency, water stress (with FAO) |
| **6.5** | Integrated water resources management, transboundary cooperation |
| **6.6** | Water-related ecosystems extent |

**CSOAI Use Case:** SDG 6 progress monitoring, WASH service coverage, water quality tracking, transboundary water governance, ecosystem health assessment.

**Access Notes:**
- Data sourced from WHO/UNICEF JMP for water supply and sanitation
- Integrated with FAO AQUASTAT for indicators 6.4.1 and 6.4.2
- Metadata available at https://unstats.un.org/sdgs/metadata/ [^1792^]

---

### 3.4 US EPA Safe Drinking Water (ECHO)

| Attribute | Detail |
|-----------|--------|
| **Name** | EPA Enforcement and Compliance History Online (ECHO) |
| **URL** | https://echo.epa.gov/ |
| **Web Services** | https://echo.epa.gov/tools/web-services |
| **Drinking Water Data** | https://www.epa.gov/DWdata |
| **Format** | JSON/XML (API), CSV, GeoJSON, Shapefile |
| **License** | Public Domain (CC0 1.0) [^1732^] |
| **API/Bulk** | RESTful API, bulk data downloads, ArcGIS Map Service |
| **Coverage** | United States, 800,000+ regulated facilities |

**Datasets Available:** [^1730^] [^1732^] [^1733^] [^1736^] [^1737^] [^1741^] [^1742^]

| Program | Data |
|---------|------|
| **Safe Drinking Water (SDWA)** | Public water system info, compliance, violations, enforcement |
| **Clean Water Act (CWA)** | NPDES permits, facility info, discharge monitoring |
| **Clean Air Act (CAA)** | Air emissions, compliance status |
| **Hazardous Waste (RCRA)** | Waste handler info, compliance |
| **All Media Programs** | Combined search across all programs |
| **PFAS Analytics** | PFAS data analysis tools |

**Key SDWA Endpoints:**
- `get_systems` - Public water system search
- `get_qid` - Query pagination
- `get_download` - CSV bulk export
- `get_facility_info` - Facility details

**CSOAI Use Case:** Drinking water compliance monitoring, water utility risk assessment, environmental justice analysis, PFAS tracking, facility-level water quality enforcement analytics.

**Access Notes:**
- No API key required for ECHO API [^1742^]
- Daily data updates
- Spatial data via ArcGIS REST: `https://echo.epa.gov/arcgis/rest/services/ECHO/Facilities/MapServer`
- R package: `echor` for SDWA/CWA/CAA data access [^1730^]
- National data extracts available for bulk download

---

## 4. Oil & Gas Infrastructure

### 4.1 GEM Oil & Gas Trackers

| Attribute | Detail |
|-----------|--------|
| **Name** | Global Energy Monitor - Oil & Gas Infrastructure Trackers |
| **URL** | https://globalenergymonitor.org/oil-and-gas |
| **Format** | CSV, Excel, interactive maps, wiki pages |
| **License** | Creative Commons (CC BY) |
| **API/Bulk** | Direct download via tracker pages, API for filtered queries |
| **Coverage** | Global, updated bi-annually |

**Trackers Available:** [^1753^] [^1757^] [^1758^] [^1764^] [^1766^]

| Tracker | Description |
|---------|-------------|
| **Global Oil & Gas Extraction Tracker (GOGET)** | Oil/gas extraction areas with >1M boe/yr or >25M boe reserves |
| **Global Oil Infrastructure Tracker (GOIT)** | Crude oil/NGL transmission pipelines, asset-level data |
| **Global Gas Infrastructure Tracker (GGIT)** | Gas transmission pipelines, LNG import/export terminals |
| **Global Oil and Gas Plant Tracker** | Oil/gas-fired power plants >50 MW (>20 MW in EU/UK) |
| **Global Methane Emitters Tracker** | Methane emissions from oil/gas/coal extraction |
| **Europe Gas Tracker** | EU fossil gas infrastructure (pipelines, LNG, plants) |
| **Asia Gas Tracker** | Asia gas infrastructure tracker |
| **Latin American Energy Tracker** | Regional energy infrastructure |
| **LNG Carrier Tracker** | LNG carrier fleet (launched Dec 2025) |

**CSOAI Use Case:** Oil/gas infrastructure monitoring, LNG market analysis, methane emissions tracking, energy transition risk assessment, pipeline project tracking, fossil fuel stranded asset analysis.

**Access Notes:**
- Download data from individual tracker pages
- CSV and Excel formats available
- Each project linked to detailed wiki page with footnotes
- API available for programmatic filtered downloads [^1754^]

---

## 5. Commodity Prices

### 5.1 World Bank Commodity Price Data (Pink Sheet)

| Attribute | Detail |
|-----------|--------|
| **Name** | World Bank Commodities Price Data (The Pink Sheet) |
| **URL** | https://www.worldbank.org/en/research/commodity-markets |
| **Pink Sheet** | https://thedocs.worldbank.org/en/doc/74e8be41ceb20fa0da750cda2f6b9e4e-0050012026/related/CMO-Pink-Sheet-May-2026.pdf |
| **Format** | Excel, PDF, CSV (monthly) |
| **License** | Creative Commons CC BY 4.0 |
| **API/Bulk** | Bulk Excel/CSV download (no API) |
| **Coverage** | 70+ commodities, monthly, 1960-present |

**Commodities Covered:** [^1780^] [^1781^] [^1783^] [^1787^] [^1791^]

| Category | Commodities |
|----------|-------------|
| **Energy** | Crude oil (Brent, WTI, Dubai), natural gas (Henry Hub, TTF, LNG Japan), coal |
| **Precious Metals** | Gold, silver, platinum, palladium |
| **Base Metals** | Aluminum, copper, iron ore, lead, nickel, tin, zinc |
| **Agriculture** | Wheat, maize, rice, soybeans, palm oil, sugar, cotton |
| **Beverages** | Coffee (Arabica/Robusta), cocoa, tea |
| **Fertilizers** | DAP, phosphate rock, potash, TSP, urea |
| **Forestry** | Logs, plywood, sawnwood, woodpulp |
| **Livestock** | Beef, chicken, sheep, shrimp |

**CSOAI Use Case:** Commodity price forecasting, inflation analysis, terms-of-trade assessment, agricultural economics, metals market intelligence, energy cost modeling.

**Access Notes:**
- Monthly update (first week of each month)
- Part of World Bank Commodity Markets Outlook report
- Historical data back to 1960 for many series
- Data used by UNCTAD for commodity price index calculations [^1797^]

---

### 5.2 UNCTAD Commodity Price Index

| Attribute | Detail |
|-----------|--------|
| **Name** | UNCTAD Commodity Price Index (UCPI) |
| **URL** | https://unctadstat.unctad.org/ |
| **Format** | Excel, CSV, PDF |
| **License** | UN Open Data |
| **API/Bulk** | UNCTADStat bulk download |
| **Coverage** | All commodity groups, monthly, 1960-present |

**Index Components:** [^1796^] [^1797^]

| Group | Subgroups |
|-------|-----------|
| **Food** | Cereals, vegetable oils, meat, seafood, sugar, bananas |
| **Tropical Beverages** | Coffee, cocoa, tea |
| **Vegetable Oilseeds & Oils** | Soybeans, soybean oil, palm oil, coconut oil |
| **Agricultural Raw Materials** | Cotton, rubber, tobacco, wood |
| **Minerals, Ores & Metals** | Aluminum, copper, iron ore, lead, nickel, tin, zinc, gold |
| **Crude Petroleum** | Various crude benchmarks |
| **Gas & Coal** | Natural gas, thermal coal |
| **Precious Metals** | Gold, silver, platinum group |

**CSOAI Use Case:** Global commodity market analysis, developing country export dependency, commodity price cycle analysis, trade term monitoring, inflation tracking.

**Access Notes:**
- Sources: World Bank, FAO, IMF (2025 update reduced from 18 to 3 automated sources) [^1797^]
- Fixed-base Laspeyres index methodology
- Annual Handbook of Statistics available

---

### 5.3 IMF Commodity Prices

| Attribute | Detail |
|-----------|--------|
| **Name** | IMF Primary Commodity Prices |
| **URL** | https://www.imf.org/en/Research/commodity-prices |
| **Data Portal** | https://data.imf.org/ |
| **Format** | CSV, Excel, API (IMF Data API/SDMX) |
| **License** | IMF Open Data (free with attribution) |
| **API/Bulk** | IMF API (SDMX), bulk CSV download |
| **Coverage** | 50+ commodities, monthly, 1980-present |

**Commodity Groups:**

| Group | Description |
|-------|-------------|
| **Fuel** | Crude oil, natural gas, coal |
| **Non-Fuel** | Food, beverages, agriculture, metals |
| **Base Metals** | Copper, aluminum, iron ore, tin, nickel, zinc, lead, uranium |
| **Precious Metals** | Gold, silver, platinum, palladium |

**CSOAI Use Case:** Macroeconomic modeling, inflation forecasting, terms of trade analysis, resource-dependent economy assessment, commodity cycle research.

---

### 5.4 Commodities-API (Free Tier)

| Attribute | Detail |
|-----------|--------|
| **Name** | Commodities-API |
| **URL** | https://commodities-api.com/ |
| **Format** | JSON |
| **License** | Free tier (API key required), paid plans |
| **API/Bulk** | RESTful API only |
| **Coverage** | 600+ commodities, 200+ currencies, real-time |

**Endpoints:** [^1763^]

| Endpoint | Description |
|----------|-------------|
| `/api/latest` | Latest commodity prices |
| `/api/timeseries` | Historical time series |
| `/api/convert` | Currency/commodity conversion |
| `/api/fluctuation` | Price change data |

**Free Tier Limits:**
- 100 API calls/month
- 1-hour update frequency
- No historical data in free tier

**CSOAI Use Case:** Real-time commodity price feeds, lightweight price monitoring, application integration, currency conversion.

---

## 6. CSOAI Integration Summary

### Recommended Data Pipeline Priorities

| Priority | Source | Category | Integration Method |
|----------|--------|----------|-------------------|
| **P0** | US EIA API | Energy/Electricity | Direct API calls + bulk downloads |
| **P0** | USGS MCS | Minerals | ScienceBase API + annual bulk |
| **P0** | World Bank Pink Sheet | Commodity Prices | Monthly CSV download |
| **P1** | IRENA Statistics | Renewables | Annual Excel download |
| **P1** | ENTSO-E API | European Grid | RESTful API (Python entsoe-py) |
| **P1** | WRI Aqueduct | Water Risk | Bulk GeoPackage download |
| **P1** | EPA ECHO | Water Quality | RESTful API (no key) |
| **P2** | Energy Institute Review | Global Energy | Annual Excel download |
| **P2** | FAO AQUASTAT | Water/Agriculture | CSV bulk download |
| **P2** | GEM Trackers | Oil/Gas/Infrastructure | CSV/Excel downloads |
| **P2** | OECD Energy Stats | Cross-Country Energy | OECD.Stat API |
| **P3** | IMF Commodities | Macro Commodities | IMF SDMX API |
| **P3** | UNCTAD Stats | Trade/Commodities | Bulk CSV download |

### Key APIs at a Glance

| Source | Auth | Rate Limits | Format |
|--------|------|-------------|--------|
| EIA API | API Key (free) | 100,000 calls/day | JSON |
| ENTSO-E API | Token (email request) | Fair use | XML |
| EPA ECHO | None | N/A | JSON/XML/GeoJSON |
| OECD.Stat | None | N/A | CSV/SDMX |
| IMF Data | None | N/A | JSON/SDMX |
| ScienceBase | None | N/A | JSON/GeoJSON |
| WRI Aqueduct | None | N/A | GeoPackage/CSV |

### License Summary

| License Type | Sources |
|-------------|---------|
| **Public Domain (US Gov)** | EIA, USGS, EPA |
| **CC BY (Attribution)** | WRI Aqueduct, GEM, World Bank, IRENA |
| **CC BY 4.0** | WRI, GEM trackers |
| **CC0 (Public Domain Dedication)** | EPA ECHO |
| **UN Open Data** | UNCTAD, UN Water, FAO |
| **OECD Terms** | OECD.Stat (free) |

---

*Document compiled for CSOAI Utilities & Resources Hive integration. All URLs and access methods verified as of July 2025.*

*Sources: [^1704^] [^1705^] [^1707^] [^1711^] [^1713^] [^1715^] [^1719^] [^1721^] [^1728^] [^1730^] [^1732^] [^1735^] [^1738^] [^1740^] [^1753^] [^1755^] [^1763^] [^1781^] [^1784^] [^1788^] [^1793^] [^1795^] [^1796^] [^1797^]*
