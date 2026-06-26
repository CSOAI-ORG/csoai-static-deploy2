# Retail, E-commerce, Consumer & Supply Chain Data Sources

> **CSOAI Hive: Retail/E-commerce/Supply Chain Dimension**
> Last Updated: 2026-06-20
> Total Sources: 30+

---

## Table of Contents

1. [Government & Official Statistics - Retail Sales](#1-government--official-statistics---retail-sales)
2. [Consumer Price & Inflation Data](#2-consumer-price--inflation-data)
3. [Consumer Sentiment & Confidence](#3-consumer-sentiment--confidence)
4. [Shipping & Maritime Freight Indices](#4-shipping--maritime-freight-indices)
5. [Logistics & Transportation Data](#5-logistics--transportation-data)
6. [Air Freight & Cargo Data](#6-air-freight--cargo-data)
7. [E-commerce Platform APIs](#7-e-commerce-platform-apis)
8. [Marketplace APIs](#8-marketplace-apis)
9. [Trade Data](#9-trade-data)
10. [Supply Chain Pressure & Risk Indices](#10-supply-chain-pressure--risk-indices)
11. [Economic Indicator Aggregators](#11-economic-indicator-aggregators)
12. [Manufacturing & PMI Data](#12-manufacturing--pmi-data)
13. [Reference Citation Index](#13-reference-citation-index)

---

## 1. Government & Official Statistics - Retail Sales

### 1.1 US Census Bureau - Monthly Retail Trade Survey (MRTS)

| Field | Detail |
|-------|--------|
| **Name** | US Census Bureau Monthly Retail Trade Survey (MRTS) / Advance Monthly Retail Trade Survey (MARTS) |
| **URL** | https://www.census.gov/retail/index.html |
| **API URL** | https://www.census.gov/data/developers/data-sets/economic-indicators.html |
| **Format** | JSON, CSV, XML via API; XLSX/CSV bulk downloads |
| **API** | Census Bureau Economic Indicators API - RESTful, free registration |
| **Coverage** | US national, monthly since 1953; 13,000 firm sample |
| **Key Metrics** | Monthly retail sales, e-commerce sales (quarterly), end-of-month inventories, merchandise inventories |
| **Update Frequency** | Monthly (MARTS ~9 days after close; MRTS ~6 weeks after close) |
| **Access Cost** | Free |
| **CSOAI Use Case** | Core US retail sales KPIs; e-commerce as % of total; inventory-to-sales ratios; seasonal adjustment benchmarking; GDP input tracking |

> **Notes**: MARTS provides early estimates (Principal Federal Economic Indicator). MRTS provides comprehensive data including e-commerce and inventories. Data also available via FRED API (series RSXFS, MRTSSM44000USS). [^1^]

### 1.2 US Census Bureau - Monthly State Retail Sales (MSRS)

| Field | Detail |
|-------|--------|
| **Name** | Monthly State Retail Sales (MSRS) |
| **URL** | https://www.census.gov/retail/mrts/www/mrs_current.pdf |
| **Format** | CSV, JSON via API |
| **API** | Census Bureau API |
| **Coverage** | US state-level, monthly since January 2019 |
| **Key Metrics** | Year-over-year % change by state and 11 NAICS retail subsectors |
| **Update Frequency** | Monthly |
| **Access Cost** | Free |
| **CSOAI Use Case** | State-level retail trend analysis; regional consumer demand forecasting; geographic retail performance comparison |

> **Notes**: Experimental blended data product combining MRTS data, administrative data, and third-party data. [^2^]

### 1.3 EUROSTAT - Retail Trade Statistics

| Field | Detail |
|-------|--------|
| **Name** | EUROSTAT Retail Trade Database |
| **URL** | https://ec.europa.eu/eurostat/databrowser/view/STS_TRTI__custom_123456/default/table |
| **API URL** | https://ec.europa.eu/eurostat/web/user-guides/data-browser/api-data-access/api-introduction |
| **Format** | SDMX-ML, SDMX-CSV, JSON-stat, TSV |
| **API** | REST API (Statistics API, SDMX 3.0, SDMX 2.1, Catalogue API) |
| **Coverage** | EU27 + EFTA countries, monthly/quarterly/annual |
| **Key Metrics** | Retail trade volume/turnover indices, deflated vs nominal, e-commerce share |
| **Update Frequency** | Twice daily at 11:00 and 23:00 CET |
| **Access Cost** | Free |
| **CSOAI Use Case** | EU retail market tracking; cross-country consumer spending comparison; eurozone economic health monitoring |

> **Notes**: Multiple API endpoints available. Supports CORS. Dataset codes: STS_TRTI (retail turnover), STS_TRTV (retail volume). [^3^]

### 1.4 Statistics Canada - Monthly Retail Trade Survey

| Field | Detail |
|-------|--------|
| **Name** | Statistics Canada Monthly Retail Trade Survey (MRTS) |
| **URL** | https://www.statcan.gc.ca/imdb-bmdi/2406-eng.htm |
| **Format** | CSV, SDMX, JSON via API |
| **API** | Statistics Canada Web Data Service (free) |
| **Coverage** | Canada, national and provincial, monthly |
| **Key Metrics** | Retail sales, e-commerce sales, number of retail locations, inventory/sales ratios, sales in volume (constant dollars) |
| **Update Frequency** | Monthly (~52 days after reference period for volume) |
| **Access Cost** | Free |
| **CSOAI Use Case** | Canadian retail benchmarking; provincial e-commerce trends; inventory cycle analysis |

> **Notes**: Uses machine learning (artificial neural networks) to project Retail Services Price Index for volume calculations. Response rate: ~91.4%. [^4^]

### 1.5 UK ONS - Retail Sales Index

| Field | Detail |
|-------|--------|
| **Name** | UK Office for National Statistics Retail Sales Index |
| **URL** | https://www.ons.gov.uk/businessindustryandtrade/retailindustry |
| **Format** | CSV, Excel, JSON, SDMX |
| **API** | ONS API (Beta, free) |
| **Coverage** | UK, monthly since 1996 |
| **Key Metrics** | Retail sales value/volume, internet sales %, 4-weekly moving averages |
| **Update Frequency** | Monthly |
| **Access Cost** | Free |
| **CSOAI Use Case** | UK consumer demand tracking; online vs offline retail shift; pre/post-Brexit retail analysis |

---

## 2. Consumer Price & Inflation Data

### 2.1 US Bureau of Labor Statistics (BLS) - CPI API

| Field | Detail |
|-------|--------|
| **Name** | BLS Consumer Price Index (CPI) Data API |
| **URL** | https://www.bls.gov/cpi/data.htm |
| **API URL** | https://api.bls.gov/publicAPI/v2/timeseries/data/ |
| **Format** | JSON, XML, flat text files (tab-delimited) |
| **API** | BLS Public Data API v1.0 (free) / v2.0 (free registration) |
| **Coverage** | US, monthly since 1913; CPI-U, CPI-W, C-CPI-U |
| **Key Metrics** | CPI for All Urban Consumers, by category, regional CPIs, seasonal factors, relative importance, 1/12-month effects |
| **Update Frequency** | Monthly (released 10th-15th) |
| **Access Cost** | Free (v1.0 unlimited; v2.0 requires free API key, allows 500 queries/day, 20 years data, calculations) |
| **CSOAI Use Case** | Inflation tracking; purchasing power analysis; retail price benchmarking; input cost monitoring |

> **Notes**: API v2.0 adds calculations (1/3/6/12-month inflation rates), annual averages. Series ID format: CUUR0000SA0 (CPI-U, all items). [^5^]

### 2.2 IMF - Consumer Price Index Data

| Field | Detail |
|-------|--------|
| **Name** | IMF Consumer Price Index (CPI) Database |
| **URL** | https://data.imf.org/en/datasets/IMF.STA:CPI |
| **Format** | JSON, CSV, Excel, SDMX via API |
| **API** | IMF RESTful JSON API (free) |
| **Coverage** | 190+ countries, monthly/quarterly/annual |
| **Key Metrics** | National CPI, CPI by component, harmonized indices |
| **Update Frequency** | Monthly |
| **Access Cost** | Free |
| **CSOAI Use Case** | Cross-country inflation comparison; emerging market price monitoring; global purchasing power analysis |

### 2.3 OECD - Consumer Price Indices

| Field | Detail |
|-------|--------|
| **Name** | OECD Consumer Price Index Data |
| **URL** | https://data.oecd.org/price/consumer-prices.htm |
| **Format** | CSV, Excel, JSON, SDMX |
| **API** | OECD.Stat API (via SDMX), DBnomics integration |
| **Coverage** | OECD countries + partners, monthly/quarterly/annual |
| **Key Metrics** | CPI all items, food, energy, core CPI, HICP for EU countries |
| **Update Frequency** | Monthly |
| **Access Cost** | Free |
| **CSOAI Use Case** | Developed market inflation comparison; core vs headline CPI analysis; monetary policy impact on retail |

### 2.4 FRED - CPI & Inflation Data

| Field | Detail |
|-------|--------|
| **Name** | Federal Reserve Economic Data (FRED) - CPI Series |
| **URL** | https://fred.stlouisfed.org/ |
| **API URL** | https://fred.stlouisfed.org/docs/api/fred/ |
| **Format** | JSON, XML, CSV |
| **API** | FRED API v2 (free API key) |
| **Coverage** | US-focused + international, 800,000+ economic time series |
| **Key Metrics** | CPI, core CPI, PCE price index, GDP deflator, retail price series |
| **Update Frequency** | Daily updates as source releases |
| **Access Cost** | Free (120 API calls/minute with key) |
| **CSOAI Use Case** | Retail price trend visualization; inflation dashboard; correlation between retail sales and CPI; automated data pipelines |

> **Notes**: Also available via DBnomics for multi-source aggregation. [^6^]

---

## 3. Consumer Sentiment & Confidence

### 3.1 OECD - Consumer Confidence Index (CCI)

| Field | Detail |
|-------|--------|
| **Name** | OECD Consumer Confidence Index (CCI) / OECD Consumer Barometer |
| **URL** | https://data.oecd.org/leadind/consumer-confidence-index-cci.htm |
| **Format** | CSV, JSON, SDMX |
| **API** | OECD.Stat API, DBnomics API |
| **Coverage** | OECD countries + BRIICS, monthly/quarterly |
| **Key Metrics** | Consumer confidence index (normalized, base=100), monthly growth rate of CCI (Consumer Barometer) |
| **Update Frequency** | Monthly (at beginning of each month) |
| **Access Cost** | Free |
| **CSOAI Use Case** | Consumer sentiment forecasting; retail demand leading indicator; cross-country consumer mood comparison; retail investment timing |

> **Notes**: CCI computed from 4 survey questions: financial situation (past + expected), general economic situation (expected), major purchases (expected). Consumer Barometer = monthly growth rate of normalized CCI. [^7^]

### 3.2 University of Michigan - Consumer Sentiment Index

| Field | Detail |
|-------|--------|
| **Name** | University of Michigan Surveys of Consumers |
| **URL** | https://data.sca.isr.umich.edu/ |
| **Format** | CSV, Excel, text |
| **API** | Direct download (no formal API; data tables downloadable) |
| **Coverage** | US, monthly since 1952 |
| **Key Metrics** | Consumer Sentiment Index, Index of Consumer Expectations, Current Economic Conditions Index, inflation expectations |
| **Update Frequency** | Monthly (preliminary mid-month, final end-month) |
| **Access Cost** | Free (basic series); subscription for detailed breakdowns |
| **CSOAI Use Case** | US consumer psychology tracking; retail spending prediction; inflation expectation monitoring |

### 3.3 Conference Board - Consumer Confidence Index

| Field | Detail |
|-------|--------|
| **Name** | The Conference Board Consumer Confidence Index |
| **URL** | https://www.conference-board.org/data/consumerconfidence.cfm |
| **Format** | CSV, Excel, PDF |
| **API** | No formal API; downloadable via subscription |
| **Coverage** | US, monthly since 1967 |
| **Key Metrics** | Consumer Confidence Index, Present Situation Index, Expectations Index |
| **Update Frequency** | Monthly (last Tuesday of each month) |
| **Access Cost** | Free (headline); detailed data subscription |
| **CSOAI Use Case** | Consumer spending outlook; retail sector investment signal; labor market-consumer spending nexus |

---

## 4. Shipping & Maritime Freight Indices

### 4.1 Freightos Baltic Index (FBX)

| Field | Detail |
|-------|--------|
| **Name** | Freightos Baltic Index (FBX) |
| **URL** | https://www.freightos.com/enterprise/terminal/freightos-baltic-index-global-container-pricing-index/ |
| **Format** | Web charts (free tier); CSV/Excel (subscription); API (subscription) |
| **API** | Available via subscription; also on Thomson Reuters Eikon, JOC Market Data |
| **Coverage** | 12 major global trade lanes (China-NA West Coast, China-NA East Coast, China-Europe, etc.) |
| **Key Metrics** | Daily spot freight rates (FAK), weekly composite index, per-TEU/FEU pricing in USD |
| **Update Frequency** | Daily (calculated 06:00 UTC, published 14:00 UTC); weekly average published Friday |
| **Access Cost** | Free tier: web charts with limited history; Paid: CSV/PNG download, API access |
| **CSOAI Use Case** | Ocean freight cost benchmarking; supply chain cost forecasting; trade lane profitability analysis; inventory carrying cost estimation |

> **Notes**: FBX is IOSCO-compliant and EU-regulated. Only daily freight rate index. Uses 50-70 million price points monthly. Free CSV available upon request to press@freightos.com for journalists/analysts. [^8^]

### 4.2 Drewry World Container Index (WCI)

| Field | Detail |
|-------|--------|
| **Name** | Drewry World Container Index (WCI) / Container Freight Rate Insight |
| **URL** | https://www.drewry.co.uk/supply-chain-advisors/supply-chain-expertise/world-container-index-assessed-by-drewry |
| **API URL** | https://github.com/drewry-uk/openapi (OpenAPI spec) |
| **Format** | Web (free bi-weekly headline); CSV/Excel (subscription); API (subscription $12,350/year) |
| **API** | REST API with OAuth 2.0 authentication (paid) |
| **Coverage** | 7 major east-west maritime lanes; 6,700 global port pairs in Container Freight Rate Insight |
| **Key Metrics** | WCI composite ($/40ft), per-lane spot rates, contract rate indices, cancelled sailings tracker, port throughput indices |
| **Update Frequency** | Bi-weekly (WCI free); real-time (subscription) |
| **Access Cost** | Free: headline index; Paid: CFRI subscription + API $12,350/year |
| **CSOAI Use Case** | Container shipping cost modeling; global trade lane cost comparison; contract vs spot rate benchmarking |

> **Notes**: Drewry also publishes Intra-Asia Container Index (IACI), free bi-weekly for registered users. New IACI launched Sept 2024. [^9^]

### 4.3 Shanghai Containerized Freight Index (SCFI)

| Field | Detail |
|-------|--------|
| **Name** | Shanghai Containerized Freight Index (SCFI) |
| **URL** | https://www.sse.net.cn/index/singleIndex?indexType=scfi (Chinese) / https://container-news.com/scfi/ (English aggregator) |
| **Format** | Web (weekly index values); historical tables |
| **API** | SSE API (containerized freight index futures data via INE) |
| **Coverage** | 13 major trade routes from Shanghai (Europe, Mediterranean, US West/East Coast, Persian Gulf, Australia/NZ, etc.) |
| **Key Metrics** | Weekly composite index, per-route rates in USD/TEU (USD/FEU for US routes) |
| **Update Frequency** | Weekly (published Friday) |
| **Access Cost** | Free (web); container freight index (Europe service) futures traded on INE |
| **CSOAI Use Case** | China export shipping cost tracking; Asia-originated freight forecasting; Red Sea disruption impact monitoring |

> **Notes**: SCFI focuses exclusively on spot rates from Shanghai (not all China ports). Uses API-automated B/L data collection system. Different from CCFI which covers all Chinese ports and includes contract rates. [^10^]

### 4.4 China Containerized Freight Index (CCFI)

| Field | Detail |
|-------|--------|
| **Name** | China Containerized Freight Index (CCFI) |
| **URL** | http://en.ccfi.com.cn/ |
| **Format** | Web, weekly bulletin |
| **API** | None known |
| **Coverage** | 12 trade routes from 10 major Chinese ports (Dalian, Tianjin, Qingdao, Shanghai, Ningbo, Xiamen, Shenzhen, Guangzhou, etc.) |
| **Key Metrics** | Weekly composite index, per-route rates |
| **Update Frequency** | Weekly |
| **Access Cost** | Free |
| **CSOAI Use Case** | Comprehensive China export freight tracking; broader than SCFI; contract + spot rate mix |

---

## 5. Logistics & Transportation Data

### 5.1 Cass Freight Index

| Field | Detail |
|-------|--------|
| **Name** | Cass Freight Index |
| **URL** | https://www.cassinfo.com/freight-audit-payment/cass-transportation-indexes/cass-freight-index |
| **Format** | Excel/CSV download (free with registration) |
| **API** | No public API; data download via website |
| **Coverage** | North America (US-focused), monthly since 1995 |
| **Key Metrics** | Cass Freight Index (shipments), Cass Freight Index (expenditures), inferred freight rates, Cass Truckload Linehaul Index |
| **Update Frequency** | Monthly (typically 13th of month) |
| **Access Cost** | Free (headline indices + historical data download); detailed reports subscription |
| **CSOAI Use Case** | North American freight volume/expenditure tracking; inferred rate calculation; trucking market cycle analysis |

> **Notes**: Derived from $37 billion in annual freight spend, 35 million invoices, hundreds of shippers across CPG, food, automotive, chemical, retail. [^11^]

### 5.2 US Bureau of Transportation Statistics (BTS)

| Field | Detail |
|-------|--------|
| **Name** | US DOT Bureau of Transportation Statistics |
| **URL** | https://www.bts.gov/topics/freight-transportation |
| **Format** | CSV, Excel, JSON via API, interactive maps |
| **API** | BTS Open Data API, Socrata Open Data API |
| **Coverage** | US, monthly/quarterly/annual |
| **Key Metrics** | Freight Transportation Services Index (TSI), Freight Analysis Framework (FAF), TransBorder Freight, Border Crossing Data, Port Performance, Commodity Flow Survey (every 5 years) |
| **Update Frequency** | Monthly (TSI); annual (FAF); monthly (TransBorder) |
| **Access Cost** | Free |
| **CSOAI Use Case** | US freight activity monitoring; cross-border trade flow analysis; port throughput benchmarking; modal shift analysis |

> **Notes**: TSI available on FRED (TSIFRGHT). FAF provides state-to-state freight flows by commodity and mode. Port Performance covers top 50 US ports. [^12^]

### 5.3 World Bank - Logistics Performance Index (LPI)

| Field | Detail |
|-------|--------|
| **Name** | World Bank Logistics Performance Index (LPI) |
| **URL** | https://lpi.worldbank.org/en/home |
| **Format** | CSV, Excel, reports |
| **API** | World Bank API (indicators); DataBank bulk download |
| **Coverage** | 139 countries, biennial (2007-2023 for LPI 1.0; 2023+ for LPI 2.0) |
| **Key Metrics** | LPI overall score (1-5), customs, infrastructure, international shipments, logistics quality, tracking/tracing, timeliness |
| **Update Frequency** | Biennial (survey-based LPI); continuous (LPI 2.0 with operational data) |
| **Access Cost** | Free |
| **CSOAI Use Case** | Country logistics infrastructure benchmarking; supply chain route optimization; emerging market logistics risk assessment |

> **Notes**: LPI 2.0 (2025) redesign uses shipment-level operational data from maritime/aviation/postal operators instead of pure survey data. [^13^]

### 5.4 Transport for London (TfL) - Open Data

| Field | Detail |
|-------|--------|
| **Name** | TfL Open Data API |
| **URL** | https://api.tfl.gov.uk/ |
| **Format** | JSON, XML |
| **API** | REST API (free, rate-limited) |
| **Coverage** | Greater London, real-time |
| **Key Metrics** | Journey times, traffic disruptions, cycle hire usage, public transport crowding |
| **Access Cost** | Free |
| **CSOAI Use Case** | Urban logistics planning; last-mile delivery optimization; city-level transportation trend analysis |

---

## 6. Air Freight & Cargo Data

### 6.1 IATA - Cargo Data / CargoIS

| Field | Detail |
|-------|--------|
| **Name** | IATA Cargo Data / CargoIS (Cargo Intelligence Solutions) |
| **URL** | https://www.iata.org/en/services/data/cargo/ |
| **Format** | Dashboard (web), reports, API (subscription) |
| **API** | Available via subscription products |
| **Coverage** | Global, monthly/annual |
| **Key Metrics** | Air cargo market data, freight tonne-kilometers (FTK), cargo capacity, yield indices, route-specific rates |
| **Update Frequency** | Monthly |
| **Access Cost** | Free: IATA monthly air cargo market analysis reports; Paid: CargoIS full data, API access |
| **CSOAI Use Case** | Air freight market tracking; air cargo rate benchmarking; capacity planning; high-value goods shipping cost analysis |

> **Notes**: IATA also publishes monthly air cargo chartbook freely. CargoIS is transaction-based air cargo intelligence. [^14^]

### 6.2 ICAO - API Data Service

| Field | Detail |
|-------|--------|
| **Name** | ICAO API Data Service |
| **URL** | https://www.icao.int/api-data-service |
| **Format** | CSV, JSON |
| **API** | REST API (free trial: 100 calls; subscription) |
| **Coverage** | Global aviation data |
| **Key Metrics** | Airport codes, airline codes, aircraft codes, aviation safety metrics, traffic data |
| **Update Frequency** | Continuous updates |
| **Access Cost** | Free tier: 100 API calls; Paid: subscription |
| **CSOAI Use Case** | Air cargo route identification; airport capacity analysis; aviation logistics planning |

### 6.3 OpenSky Network

| Field | Detail |
|-------|--------|
| **Name** | OpenSky Network |
| **URL** | https://opensky-network.org/ |
| **API URL** | https://openskynetwork.github.io/opensky-api/rest.html |
| **Format** | JSON (REST API) |
| **API** | REST API (free for non-commercial; rate limits apply) |
| **Coverage** | Global air traffic, real-time and historical |
| **Key Metrics** | Aircraft state vectors (position, altitude, velocity), flight data, arrival/departure times |
| **Update Frequency** | Real-time |
| **Access Cost** | Free (non-commercial, with registration); authenticated users get higher rate limits |
| **CSOAI Use Case** | Air cargo capacity proxy (freighter aircraft tracking); route congestion analysis; logistics network visualization |

> **Notes**: Community-based receiver network. Data kept forever. Scientific datasets available for bulk download. [^15^]

---

## 7. E-commerce Platform APIs

### 7.1 Amazon Selling Partner API (SP-API)

| Field | Detail |
|-------|--------|
| **Name** | Amazon Selling Partner API (SP-API) |
| **URL** | https://developer.amazonservices.com/ |
| **Format** | JSON |
| **API** | REST API (OAuth 2.0 + AWS Signature v4) |
| **Coverage** | 20+ Amazon marketplaces globally |
| **Key Metrics** | Listings, orders, payments, reports, inventory, pricing, fulfillment, catalog data |
| **Update Frequency** | Real-time (most endpoints) |
| **Access Cost** | Free for private sellers (own data only); Third-party developers: $1,400/year + usage fees starting Jan 2026 |
| **CSOAI Use Case** | E-commerce sales analytics; inventory management automation; competitive pricing intelligence; multi-marketplace operations |

> **Important Change**: Starting January 31, 2026, third-party developers pay $1,400/year + monthly GET call fees (Basic tier: 2.5M calls/month included; Pro: $1,000/mo for 25M; Plus: $10,000/mo for 250M). Private sellers using API for own business remain free. [^16^]

### 7.2 Shopify Storefront & Admin APIs

| Field | Detail |
|-------|--------|
| **Name** | Shopify Storefront API / Admin API |
| **URL** | https://shopify.dev/docs/api |
| **Format** | GraphQL (Storefront + Admin), REST (Admin) |
| **API** | GraphQL/REST API (free with Shopify plan) |
| **Coverage** | Individual store data (own store only) |
| **Key Metrics** | Products, collections, orders, customers, inventory, analytics, checkout data |
| **Update Frequency** | Real-time |
| **Access Cost** | Free (included with any Shopify plan); rate limits by plan tier |
| **CSOAI Use Case** | Store performance analytics; inventory automation; headless commerce data; e-commerce trend analysis for owned stores |

> **Note**: Shopify Partner API provides app developer analytics (MRR, churn, retention). Public store data (competitive intelligence) requires third-party services like Netrows. [^17^]

---

## 8. Marketplace APIs

### 8.1 eBay Developer API

| Field | Detail |
|-------|--------|
| **Name** | eBay APIs (Buy API, Sell API, Commerce API) |
| **URL** | https://developer.ebay.com/ |
| **Format** | REST (JSON), traditional SOAP APIs also available |
| **API** | REST API (OAuth 2.0); free developer account |
| **Coverage** | 20+ eBay marketplaces globally |
| **Key Metrics** | Product listings, inventory, orders, pricing, search, category data, deal data, merchandised products |
| **Update Frequency** | Real-time |
| **Access Cost** | Free (eBay Developers Program membership) |
| **CSOAI Use Case** | Marketplace pricing intelligence; product catalog management; cross-platform inventory sync; deal/sale trend analysis |

> **Notes**: Free developer registration at developer.ebay.com. Supports C#, Java, PHP, Python, etc. Sandbox available for testing. [^18^]

### 8.2 Google Trends / PyTrends

| Field | Detail |
|-------|--------|
| **Name** | Google Trends / PyTrends (unofficial Python library) |
| **URL** | https://trends.google.com/trends/ |
| **Python Library** | https://github.com/GeneralMills/pytrends |
| **Format** | CSV download (web), JSON (via PyTrends) |
| **API** | No official API; PyTrends (Python) + SerpApi (paid with free tier) |
| **Coverage** | Global, by country/region/city, since 2004 |
| **Key Metrics** | Search interest over time, interest by region, related queries, related topics, trending searches |
| **Update Frequency** | Daily (trending); weekly/monthly (historical) |
| **Access Cost** | Free (web + PyTrends); SerpApi: 100 free searches/month |
| **CSOAI Use Case** | Consumer interest tracking; product demand forecasting; seasonal trend analysis; brand health monitoring; retail category interest comparison |

> **Notes**: PyTrends is the de facto standard for programmatic Google Trends access. SerpApi offers structured JSON output via official Python library. [^19^]

### 8.3 NielsenIQ / Byzzer (Free Tier)

| Field | Detail |
|-------|--------|
| **Name** | NielsenIQ Byzzer Platform |
| **URL** | https://byzzer.com/ |
| **Format** | Web dashboard, reports (PDF/Excel) |
| **API** | No public API; web platform access |
| **Coverage** | US retail, CPG categories |
| **Key Metrics** | Category trends, brand rank, market share, distribution metrics, consumer panel data (free tier limited) |
| **Update Frequency** | Monthly/Quarterly |
| **Access Cost** | Free tier: 3 free reports + 1 free Business Drivers Waterfall for Foodbevy members; Paid: full subscription |
| **CSOAI Use Case** | CPG retail benchmarking; category performance analysis; brand positioning; distribution gap analysis |

> **Notes**: Free access via partnership programs (e.g., Foodbevy). Designed for small CPG companies. [^20^]

---

## 9. Trade Data

### 9.1 UN Comtrade Database

| Field | Detail |
|-------|--------|
| **Name** | UN Comtrade - United Nations International Trade Statistics Database |
| **URL** | https://comtrade.un.org/ |
| **API URL** | https://comtradeapi.un.org/ |
| **Format** | JSON, CSV, SDMX-ML; bulk data files |
| **API** | Legacy API (free, rate-limited); New API v1 (subscription tiers); Python package `comtradeapicall` |
| **Coverage** | 200+ countries/territories, annual since 1962, monthly since 2000 |
| **Key Metrics** | Merchandise trade by commodity (HS/SITC), trade value/quantity/weight, reporter/partner flows |
| **Update Frequency** | Monthly with 2-month lag |
| **Access Cost** | Free tier: 100 API calls/hour, 1,000 records/query; Premium tiers available |
| **CSOAI Use Case** | Global trade flow analysis; retail import sourcing tracking; commodity-level trade patterns; bilateral trade analysis |

> **Notes**: Python package `comtradeapicall` simplifies API usage. Bulk download available for subscribed users. R package `comtradr` also available. R user limit: 500 records/query (legacy) / 10,000 (new API). [^21^]

### 9.2 USITC DataWeb

| Field | Detail |
|-------|--------|
| **Name** | USITC DataWeb - U.S. Trade & Tariff Data |
| **URL** | https://dataweb.usitc.gov/ |
| **Format** | CSV, Excel, web tables |
| **API** | Available with free account registration |
| **Coverage** | US trade data, monthly since 1989 |
| **Key Metrics** | US imports/exports by HTS/NAICS/SITC, trade balance, tariff rates, customs district data, FTA preference programs |
| **Update Frequency** | Monthly |
| **Access Cost** | Free (web query); API requires free account |
| **CSOAI Use Case** | US retail import tracking; tariff impact analysis; customs district logistics planning; NAFTA/USMCA trade monitoring |

> **Notes**: Official US merchandise trade statistics from US Department of Commerce. Supports 10-digit HTS-level queries. Save queries and receive automated email reports. [^22^]

### 9.3 World Bank - WITS (World Integrated Trade Solution)

| Field | Detail |
|-------|--------|
| **Name** | World Integrated Trade Solution (WITS) |
| **URL** | https://wits.worldbank.org/ |
| **Format** | CSV, Excel, bulk download |
| **API** | Bulk download tool; no formal API |
| **Coverage** | Global, UN Comtrade + UNCTAD TRAINS tariff data |
| **Key Metrics** | Trade flows, tariff rates, trade indicators (RCA, trade intensity), NTM data |
| **Update Frequency** | Annual |
| **Access Cost** | Free (registration required) |
| **CSOAI Use Case** | Retail sourcing country analysis; tariff impact modeling; trade competitiveness assessment; preference utilization |

---

## 10. Supply Chain Pressure & Risk Indices

### 10.1 NY Fed - Global Supply Chain Pressure Index (GSCPI)

| Field | Detail |
|-------|--------|
| **Name** | Federal Reserve Bank of New York Global Supply Chain Pressure Index (GSCPI) |
| **URL** | https://www.newyorkfed.org/research/gscpi.html |
| **Download** | https://www.newyorkfed.org/medialibrary/research/interactives/gscpi/downloads/gscpi_data.xlsx |
| **Format** | Excel (.xlsx) direct download; CSV conversion |
| **API** | No formal API; Excel file downloadable directly |
| **Coverage** | Global, monthly since January 1997 |
| **Key Metrics** | GSCPI composite (standard score), shipping costs (Baltic Dry Index, Harpex), airfreight costs, supply chain components (delivery times, backlogs, inventories from PMI surveys) |
| **Update Frequency** | Monthly |
| **Access Cost** | Free |
| **CSOAI Use Case** | Global supply chain stress monitoring; inflation prediction; inventory planning; procurement timing; risk management |

> **Notes**: GSCPI expressed as standard score (number of standard deviations from mean). Higher = more supply chain pressure. Can be decomposed into country-specific indices. Uses BLS data, Baltic Exchange, IHS Markit, ISM, Haver Analytics. [^23^]

### 10.2 World Bank - Global Supply Chain Stress Index (GSCSI)

| Field | Detail |
|-------|--------|
| **Name** | World Bank Global Supply Chain Stress Index (GSCSI) |
| **URL** | Part of World Bank trade/procurement data |
| **Format** | Data tables, reports |
| **API** | No formal API |
| **Coverage** | Global, monthly |
| **Key Metrics** | Container shipping capacity delayed at global ports, port-level container traffic flow data |
| **Update Frequency** | Monthly |
| **Access Cost** | Free |
| **CSOAI Use Case** | Maritime supply chain congestion tracking; port-level bottleneck identification; Red Sea crisis impact assessment |

> **Notes**: GSCSI focuses specifically on maritime/container shipping delays, contrasting with GSCPI's broader supply chain pressure. Has shown divergence from GSCPI in 2024-25 due to Red Sea diversions. [^24^]

### 10.3 Moody's Analytics - Supply Chain Risk (Free Tools)

| Field | Detail |
|-------|--------|
| **Name** | Moody's Analytics Supply Chain Solutions / Open Supply Hub |
| **URL** | https://opensupplyhub.org/ (free) / https://www.moodys.com/supply-chain (paid) |
| **Format** | Web platform, CSV download |
| **API** | Open Supply Hub API (free) |
| **Coverage** | Global production locations |
| **Key Metrics** | Supplier facility locations, ownership connections, supply chain mapping |
| **Update Frequency** | Continuous (crowdsourced) |
| **Access Cost** | Free (Open Supply Hub); Paid (Moody's Supply Chain Catalyst) |
| **CSOAI Use Case** | Supply chain mapping; supplier risk identification; ESG compliance; supply chain due diligence |

---

## 11. Economic Indicator Aggregators

### 11.1 DBnomics - World's Economic Database

| Field | Detail |
|-------|--------|
| **Name** | DBnomics |
| **URL** | https://db.nomics.world/ |
| **Format** | CSV, Excel, JSON |
| **API** | REST API (free, no registration) |
| **Coverage** | 100+ providers (IMF, World Bank, OECD, Eurostat, BLS, FRED, etc.), 1 billion+ series |
| **Key Metrics** | All economic indicators from major providers in unified format |
| **Update Frequency** | Real-time (as providers publish) |
| **Access Cost** | Free |
| **CSOAI Use Case** | Unified economic data pipeline; multi-source retail indicator dashboard; cross-provider data harmonization; historical revision tracking |

> **Notes**: Provides direct access from R (`rdbnomics` package), Python, Julia, Matlab. Archives revisions for real-time database construction. [^25^]

### 11.2 FRED - Federal Reserve Economic Data

| Field | Detail |
|-------|--------|
| **Name** | FRED - Federal Reserve Economic Data |
| **URL** | https://fred.stlouisfed.org/ |
| **API URL** | https://fred.stlouisfed.org/docs/api/fred/ |
| **Format** | JSON, XML, CSV |
| **API** | FRED API v2 (free API key, 120 requests/minute) |
| **Coverage** | 800,000+ US and international time series from 100+ sources |
| **Key Metrics** | Retail sales, CPI, employment, GDP, interest rates, exchange rates, regional data |
| **Update Frequency** | Daily |
| **Access Cost** | Free |
| **CSOAI Use Case** | Retail-economic correlation analysis; automated data feeds; economic dashboard creation; ALFRED historical revision analysis |

> **Notes**: Also includes ALFRED (Archival Federal Reserve Economic Data) for tracking data revisions. Integrates with DBnomics for multi-provider access. [^26^]

---

## 12. Manufacturing & PMI Data

### 12.1 S&P Global - Manufacturing PMI (Free Headline)

| Field | Detail |
|-------|--------|
| **Name** | S&P Global Manufacturing Purchasing Managers' Index (PMI) |
| **URL** | https://www.spglobal.com/marketintelligence/en/mi/products/pmi.html |
| **Format** | Web (free headline), reports (subscription) |
| **API** | No public free API; data available via subscription |
| **Coverage** | 45+ countries, monthly since 1998 for major economies |
| **Key Metrics** | Manufacturing PMI (headline >50 = expansion), output, new orders, employment, suppliers' delivery times, input/output prices, inventories |
| **Update Frequency** | Monthly (flash PMI mid-month, final end-month) |
| **Access Cost** | Free: headline PMI only; Paid: detailed breakdowns, sub-indices, history |
| **CSOAI Use Case** | Manufacturing health leading indicator; retail inventory pipeline forecasting; input cost pressure monitoring; economic cycle timing |

> **Notes**: Formerly IHS Markit PMI. Widely used composite indicator. Free headline available on website and news releases. Detailed data via subscription or data vendors (Bloomberg, Refinitiv). [^27^]

### 12.2 Institute for Supply Management (ISM) - US Manufacturing PMI

| Field | Detail |
|-------|--------|
| **Name** | ISM Manufacturing Report on Business |
| **URL** | https://www.ismworld.org/supply-management-news-and-reports/reports/ISM-Report-On-Business/ |
| **Format** | PDF report, web tables |
| **API** | No API; data downloadable from website |
| **Coverage** | US, monthly since 1948 |
| **Key Metrics** | PMI, new orders, production, employment, supplier deliveries, inventories, customer inventories, prices, backlog, exports, imports |
| **Update Frequency** | Monthly (1st business day of following month) |
| **Access Cost** | Free (headline); detailed breakdown requires membership |
| **CSOAI Use Case** | US supply chain pressure input (used in GSCPI); manufacturing-retail pipeline analysis; price pressure early warning |

### 12.3 J.P. Morgan Global Manufacturing PMI

| Field | Detail |
|-------|--------|
| **Name** | J.P. Morgan Global Manufacturing PMI (with S&P Global & ISM) |
| **URL** | https://www.spglobal.com/marketintelligence/en/mi/products/pmi/global.html |
| **Format** | Press release, web |
| **API** | No free API |
| **Coverage** | Global composite, monthly since 1998 |
| **Key Metrics** | Global manufacturing PMI, output, new orders, employment, prices |
| **Update Frequency** | Monthly |
| **Access Cost** | Free (headline) |
| **CSOAI Use Case** | Global manufacturing cycle assessment; worldwide demand proxy; retail inventory pipeline globally |

---

## 13. Reference Citation Index

| Citation | Source |
|----------|--------|
| [^1^] | US Census Bureau. Monthly Retail Trade Survey. https://www.census.gov/retail/index.html |
| [^2^] | US Census Bureau. Monthly State Retail Sales Data (Kaggle). https://www.kaggle.com/datasets/umerhaddii/us-census-bureaus-monthly-state-retail-sales-data |
| [^3^] | EUROSTAT. API Introduction - Data Access. https://ec.europa.eu/eurostat/web/user-guides/data-browser/api-data-access/api-introduction |
| [^4^] | Statistics Canada. Monthly Retail Trade Survey. https://www.statcan.gc.ca/imdb-bmdi/2406-eng.htm |
| [^5^] | BLS. Using CPI aspect metadata files with Public Data API. https://www.bls.gov/cpi/factsheets/using-cpi-metadata-aspect-files.htm |
| [^6^] | FRED API Documentation. https://fred.stlouisfed.org/docs/api/fred/ |
| [^7^] | OECD. Consumer Confidence Index (CCI). https://data.oecd.org/leadind/consumer-confidence-index-cci.htm |
| [^8^] | Freightos Baltic Index. https://www.freightos.com/enterprise/terminal/freightos-baltic-index-global-container-pricing-index/ |
| [^9^] | Drewry World Container Index. https://www.drewry.co.uk/supply-chain-advisors/supply-chain-expertise/world-container-index-assessed-by-drewry |
| [^10^] | Shanghai Containerized Freight Index Guide. https://dimerco.com/blog-post/containerized-freight-index-guide/ |
| [^11^] | Cass Freight Index. https://www.cassinfo.com/freight-audit-payment/cass-transportation-indexes/cass-freight-index |
| [^12^] | US BTS Freight Transportation. https://www.bts.gov/topics/freight-transportation |
| [^13^] | World Bank Logistics Performance Index. https://lpi.worldbank.org/en/home |
| [^14^] | IATA Cargo Data. https://www.iata.org/en/services/data/cargo/ |
| [^15^] | OpenSky Network API. https://opensky-network.org/data/api |
| [^16^] | Amazon SP-API Developer Portal. https://developer.amazonservices.com/ |
| [^17^] | Shopify API Documentation. https://shopify.dev/docs/api |
| [^18^] | eBay Developers Program. https://developer.ebay.com/ |
| [^19^] | SerpApi Google Trends API. https://serpapi.com/blog/scraping-google-trends-with-python-pytrends-alternative/ |
| [^20^] | NielsenIQ Byzzer. https://byzzer.com/ |
| [^21^] | UN Comtrade API Package (GitHub). https://github.com/uncomtrade/comtradeapicall |
| [^22^] | USITC DataWeb. https://dataweb.usitc.gov/ |
| [^23^] | NY Fed GSCPI Data. https://www.newyorkfed.org/medialibrary/research/interactives/gscpi/downloads/gscpi_data.xlsx |
| [^24^] | Richmond Fed. How Constrained Are Global Supply Chains? https://www.richmondfed.org/research/national_economy/macro_minute/2025/how_constrained_are_global_supply_chains |
| [^25^] | DBnomics. https://db.nomics.world/ |
| [^26^] | FRED - Federal Reserve Economic Data. https://fred.stlouisfed.org/ |
| [^27^] | S&P Global PMI. https://www.spglobal.com/marketintelligence/en/mi/products/pmi.html |

---

## Quick Access Summary Table

| Category | Source | Free API? | Format | Best For |
|----------|--------|-----------|--------|----------|
| US Retail Sales | Census MRTS | Yes (REST) | JSON/CSV | Core US retail KPIs |
| EU Retail Sales | EUROSTAT | Yes (REST) | SDMX/JSON | European retail tracking |
| Global CPI | IMF/BLS/OECD | Yes | JSON/SDMX | Inflation monitoring |
| Consumer Confidence | OECD CCI | Yes | JSON/CSV | Sentiment forecasting |
| Container Shipping | FBX | Partial (charts free) | CSV/API (paid) | Ocean freight benchmarking |
| Container Shipping | Drewry WCI | Partial (headline free) | JSON/API (paid) | Contract rate analysis |
| China Freight | SCFI | No (web free) | Web tables | China export freight costs |
| North American Freight | Cass Index | No (download free) | Excel/CSV | US freight volume tracking |
| Logistics Performance | World Bank LPI | Yes | CSV/API | Country logistics ranking |
| Air Cargo | IATA | Partial (reports free) | Dashboard/API (paid) | Air freight market analysis |
| E-commerce | Amazon SP-API | Yes (own data) | JSON | Seller analytics |
| Marketplace | eBay API | Yes | REST JSON | Pricing intelligence |
| Search Trends | Google Trends/PyTrends | Yes | JSON/CSV | Consumer interest tracking |
| Global Trade | UN Comtrade | Yes (limited) | JSON/CSV | Trade flow analysis |
| US Trade | USITC DataWeb | Yes (with account) | CSV/Excel | US import/export data |
| Supply Chain Pressure | NY Fed GSCPI | No (Excel download) | Excel | Supply chain stress index |
| Economic Aggregator | DBnomics | Yes (REST) | JSON/CSV | Multi-source harmonization |
| Economic Aggregator | FRED | Yes (API key) | JSON/XML | US economic time series |
| Manufacturing | S&P Global PMI | Partial (headline free) | Web | Manufacturing health |

---

*Document compiled for CSOAI Retail/E-commerce/Supply Chain Hive. All URLs verified as of June 2026.*
