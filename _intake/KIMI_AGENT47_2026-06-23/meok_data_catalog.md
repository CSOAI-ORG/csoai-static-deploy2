# MEOK 47-Industry Simulation: Free Data Source Catalog

> **Version:** 1.0
> **Date:** July 2026
> **Coverage:** 200+ free data sources across 47 industries
> **Organization:** By data category, mapped to industries

---

## Table of Contents

1. [Government Regulatory & Compliance Databases](#1-government-regulatory--compliance-databases)
2. [Financial & Market Data](#2-financial--market-data)
3. [Healthcare, Bio & Pharma Data](#3-healthcare-bio--pharma-data)
4. [Cybersecurity & Defense Data](#4-cybersecurity--defense-data)
5. [Scientific & Research Data](#5-scientific--research-data)
6. [Corporate & Business Data](#6-corporate--business-data)
7. [Economic & Trade Data](#7-economic--trade-data)
8. [Geographic & Satellite Data](#8-geographic--satellite-data)
9. [Patent & Standards Data](#9-patent--standards-data)
10. [News, Sentiment & Social Data](#10-news-sentiment--social-data)
11. [Industry-Specific Data Source Mapping](#11-industry-specific-data-source-mapping)
12. [API Key Summary](#12-api-key-summary)

---

## 1. Government Regulatory & Compliance Databases

### 1.1 CISA (Cybersecurity & Infrastructure Security Agency)

| Field | Details |
|-------|---------|
| **Source** | CISA Known Exploited Vulnerabilities (KEV) Catalog |
| **URL** | https://www.cisa.gov/known-exploited-vulnerabilities-catalog |
| **API** | https://api.cisa.gov/ (STIX/TAXII feeds) |
| **What it provides** | Catalog of CVEs known to be actively exploited in the wild; includes vendor, product, vulnerability type, action due date, date added |
| **How to access** | Open, no API key required for basic CSV/JSON download. STIX/TAXII requires free registration |
| **Rate limits** | No limits for catalog download; 100 req/min for API |
| **Industries covered** | Cybersecurity AI (1), Critical Infrastructure (5), Defense & Military AI (2), AI Governance & Safety (6) |
| **Last updated** | Daily |

```python
import requests
import json

def fetch_cisa_kev():
    """Fetch CISA Known Exploited Vulnerabilities catalog"""
    url = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    return data["vulnerabilities"]  # List of CVE dicts

# Example: Fetch and save
vulns = fetch_cisa_kev()
print(f"Total KEV entries: {len(vulns)}")
# Fields: cveID, vendorProject, product, vulnerabilityName, dateAdded, dueDate, requiredAction
```

---

### 1.2 NVD (National Vulnerability Database)

| Field | Details |
|-------|---------|
| **Source** | NIST National Vulnerability Database |
| **URL** | https://nvd.nist.gov/ |
| **API** | https://services.nvd.nist.gov/rest/json/cves/2.0 |
| **What it provides** | 250,000+ CVE records with CVSS scores, CPE configurations, references, CWE classifications, published/modified dates |
| **How to access** | Open API, no key required (50 req/30s with key, 5 req/30s without) |
| **Rate limits** | 5 requests per 30 seconds (no key); 50 req/30s with free API key |
| **Industries covered** | Cybersecurity AI (1), Critical Infrastructure (5), Defense & Military AI (2), Semiconductor (5) |
| **Last updated** | Continuously |

```python
def fetch_nvd_cves(start_index=0, results_per_page=20, api_key=None):
    """Fetch CVEs from NVD API 2.0"""
    url = "https://services.nvd.nist.gov/rest/json/cves/2.0"
    headers = {"apiKey": api_key} if api_key else {}
    params = {"startIndex": start_index, "resultsPerPage": results_per_page}
    resp = requests.get(url, headers=headers, params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()  # Contains vulnerabilities, totalResults

# Paginated fetching
def fetch_all_nvd_cves(api_key=None):
    """Fetch all CVEs with pagination and rate limiting"""
    all_cves = []
    start = 0
    while True:
        data = fetch_nvd_cves(start, 2000, api_key)
        cves = data.get("vulnerabilities", [])
        if not cves:
            break
        all_cves.extend(cves)
        start += len(cves)
        if start >= data.get("totalResults", 0):
            break
        time.sleep(6 if not api_key else 0.6)  # Rate limit
    return all_cves
```

---

### 1.3 SEC EDGAR

| Field | Details |
|-------|---------|
| **Source** | SEC EDGAR (Electronic Data Gathering, Analysis, and Retrieval) |
| **URL** | https://www.sec.gov/edgar |
| **API** | https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany |
| **Bulk Data** | https://www.sec.gov/Archives/edgar/daily-index/ |
| **What it provides** | All US public company filings (10-K, 10-Q, 8-K, 13F, DEF 14A, etc.); financial statements, insider trading, institutional ownership |
| **How to access** | Open, no key required. Must identify requests with User-Agent header |
| **Rate limits** | 10 requests per second. **REQUIRED**: Set User-Agent with contact info |
| **Industries covered** | AI Banking (1), InsurTech (2), Crypto (3), Algo Trading (4), RegTech (5), Fintech (6), All public companies |
| **Last updated** | Real-time (submissions processed within minutes) |

```python
def fetch_sec_filings(cik, filing_type="10-K"):
    """Fetch SEC filings for a company by CIK"""
    headers = {"User-Agent": "MEOK-Simulation contact@meok.ai"}
    url = "https://www.sec.gov/cgi-bin/browse-edgar"
    params = {
        "action": "getcompany",
        "CIK": cik,
        "type": filing_type,
        "output": "json"
    }
    resp = requests.get(url, headers=headers, params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()

def fetch_company_ticker_map():
    """Fetch CIK-to-ticker mapping"""
    headers = {"User-Agent": "MEOK-Simulation contact@meok.ai"}
    url = "https://www.sec.gov/files/company_tickers.json"
    resp = requests.get(url, headers=headers, timeout=30)
    return resp.json()

# Submissions API (newer JSON API)
def fetch_submissions(cik):
    """Fetch company submissions using new SEC API"""
    headers = {"User-Agent": "MEOK-Simulation contact@meok.ai"}
    cik_padded = str(cik).zfill(10)
    url = f"https://data.sec.gov/submissions/CIK{cik_padded}.json"
    resp = requests.get(url, headers=headers, timeout=30)
    return resp.json()
```

---

### 1.4 FDA Open Data

| Field | Details |
|-------|---------|
| **Source** | openFDA |
| **URL** | https://open.fda.gov/ |
| **API** | https://api.fda.gov/ |
| **What it provides** | 510(k) clearances, adverse events (MAUDE), drug labels, recalls, enforcement reports, drug adverse events (FAERS) |
| **How to access** | Open API, no key required. Free tier: 240 requests/minute. API key: 1000 req/min |
| **Rate limits** | 240 req/min (no key); 1000 req/min (with free API key) |
| **Industries covered** | Healthcare AI (7), Medical Devices (8), Biotech (9), Pharma AI (10) |
| **Last updated** | Weekly (adverse events), Daily (recalls) |

```python
def fetch_fda_510k(skip=0, limit=100):
    """Fetch FDA 510(k) premarket notifications"""
    url = "https://api.fda.gov/device/510k.json"
    params = {"skip": skip, "limit": limit}
    resp = requests.get(url, params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()

def fetch_fda_adverse_events(product="", skip=0, limit=100):
    """Fetch MAUDE adverse event reports"""
    url = "https://api.fda.gov/device/event.json"
    params = {"search": f"product_description:{product}", "limit": limit}
    resp = requests.get(url, params=params, timeout=30)
    return resp.json()

def fetch_fda_recalls(skip=0, limit=100):
    """Fetch FDA enforcement reports/recalls"""
    url = "https://api.fda.gov/food/enforcement.json"
    params = {"skip": skip, "limit": limit}
    resp = requests.get(url, params=params, timeout=30)
    return resp.json()
```

---

### 1.5 EU Open Data Portal (EU ODP)

| Field | Details |
|-------|---------|
| **Source** | European Union Open Data Portal |
| **URL** | https://data.europa.eu/ |
| **API** | https://data.europa.eu/api/hub/search/ |
| **What it provides** | 1M+ datasets from EU institutions: Eurostat statistics, climate data, transport, economy, energy, R&D, health, legal texts (EUR-Lex) |
| **How to access** | Open, no API key required |
| **Rate limits** | 100 requests/minute |
| **Industries covered** | All 47 industries (general statistical backbone) |
| **Last updated** | Continuously |

```python
def fetch_eu_datasets(query="AI", rows=20):
    """Search EU Open Data Portal datasets"""
    url = "https://data.europa.eu/api/hub/search/datasets/search"
    params = {"query": query, "rows": rows}
    resp = requests.get(url, params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()

# Eurostat specific
def fetch_eurostat_indicator(indicator="tec00115"):
    """Fetch Eurostat indicator data (e.g., R&D expenditure)"""
    url = f"https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/{indicator}"
    params = {"format": "JSON", "lang": "EN"}
    resp = requests.get(url, params=params, timeout=30)
    return resp.json()
```

---

### 1.6 US Data.gov

| Field | Details |
|-------|---------|
| **Source** | US Government Open Data |
| **URL** | https://catalog.data.gov/ |
| **API** | CKAN API: https://catalog.data.gov/api/3/ |
| **What it provides** | 250,000+ datasets from federal agencies: census, health, transportation, energy, finance, education, environment |
| **How to access** | Open, no API key required |
| **Rate limits** | No strict limits (be reasonable) |
| **Industries covered** | All 47 industries |
| **Last updated** | Continuously |

```python
def fetch_datagov_datasets(query="artificial intelligence", rows=20):
    """Search Data.gov datasets"""
    url = "https://catalog.data.gov/api/3/action/package_search"
    params = {"q": query, "rows": rows}
    resp = requests.get(url, params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()["result"]["results"]
```

---

### 1.7 ENISA Cybersecurity

| Field | Details |
|-------|---------|
| **Source** | European Union Agency for Cybersecurity |
| **URL** | https://www.enisa.europa.eu/ |
| **API** | RSS/XML feeds available |
| **What it provides** | NIS2 implementation guidance, threat landscapes, cybersecurity reports, policy recommendations |
| **How to access** | Open download |
| **Rate limits** | N/A |
| **Industries covered** | Cybersecurity AI (13), Critical Infrastructure (17), AI Governance (18) |
| **Last updated** | Regularly |

---

### 1.8 ClinicalTrials.gov

| Field | Details |
|-------|---------|
| **Source** | NIH Clinical Trials Registry |
| **URL** | https://clinicaltrials.gov/ |
| **API** | https://clinicaltrials.gov/api/v2/ |
| **What it provides** | 500,000+ clinical trials globally: interventions, conditions, sponsors, locations, outcomes, phases, recruitment status |
| **How to access** | Open API v2, no key required |
| **Rate limits** | No published limits |
| **Industries covered** | Healthcare AI (7), Biotech (9), Pharma AI (10), Medical Devices (8) |
| **Last updated** | Daily |

```python
def fetch_clinical_trials(condition="cancer", limit=100):
    """Fetch clinical trials by condition"""
    url = "https://clinicaltrials.gov/api/v2/studies"
    params = {
        "query.cond": condition,
        "pageSize": limit,
        "filter.overallStatus": "RECRUITING"
    }
    resp = requests.get(url, params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()["studies"]
```

---

### 1.9 EUR-Lex (EU Law Database)

| Field | Details |
|-------|---------|
| **Source** | Official EU Legal Database |
| **URL** | https://eur-lex.europa.eu/ |
| **API** | https://eur-lex.europa.eu/content/help/webservices.html |
| **WS** | SOAP web services available |
| **What it provides** | All EU legislation: AI Act, GDPR, NIS2, DORA, MiCA, MDR/IVDR, Digital Services Act, etc. |
| **How to access** | Open web services, free registration for API |
| **Rate limits** | 1000 requests/day per registered user |
| **Industries covered** | All 47 industries (regulatory framework) |
| **Last updated** | Real-time (new legislation published immediately) |

---

### 1.10 NHTSA / US Vehicle Safety

| Field | Details |
|-------|---------|
| **Source** | National Highway Traffic Safety Administration |
| **URL** | https://www.nhtsa.gov/nhtsa-datasets-and-apis |
| **API** | https://api.nhtsa.gov/ |
| **What it provides** | Vehicle crash data, complaints, recalls, autonomous vehicle guidance, safety ratings, VIN decoder |
| **How to access** | Open API, no key required |
| **Rate limits** | 1000 requests/hour |
| **Industries covered** | Autonomous Vehicles (3), Transport & Logistics (29) |
| **Last updated** | Daily |

```python
def fetch_nhtsa_complaints(make="TESLA", model="MODEL", year=2025):
    """Fetch NHTSA complaints for a vehicle"""
    url = f"https://api.nhtsa.gov/complaints/complaintsByVehicle"
    params = {"make": make, "model": model, "modelYear": year}
    resp = requests.get(url, params=params, timeout=30)
    return resp.json()

def fetch_nhtsa_recalls():
    """Fetch all vehicle recalls"""
    url = "https://api.nhtsa.gov/recalls/recallsByVehicle"
    resp = requests.get(url, timeout=30)
    return resp.json()
```

---

### 1.11 Regulations.gov

| Field | Details |
|-------|---------|
| **Source** | US Federal Regulatory Documents |
| **URL** | https://www.regulations.gov/ |
| **API** | https://open.gsa.gov/api/regulationsgov/ |
| **What it provides** | Federal Register documents, public comments on proposed rules, dockets, regulatory agendas |
| **How to access** | Free API key required (obtain from https://open.gsa.gov/api/regulationsgov/) |
| **Rate limits** | 1000 req/day |
| **Industries covered** | All 47 industries (regulatory tracking) |

---

### 1.12 OFAC Sanctions (US Treasury)

| Field | Details |
|-------|---------|
| **Source** | Office of Foreign Assets Control |
| **URL** | https://sanctionssearch.ofac.treas.gov/ |
| **Data** | https://www.treasury.gov/ofac/downloads |
| **What it provides** | SDN List, Consolidated Sanctions List, SSI List; XML/CSV/CSV downloads |
| **How to access** | Open bulk downloads, no key |
| **Rate limits** | N/A (bulk download) |
| **Industries covered** | Banking (19), Crypto (21), RegTech (23), Defense (14) |
| **Last updated** | Daily |

```python
def fetch_ofac_sdn():
    """Fetch OFAC SDN list (CSV format)"""
    url = "https://www.treasury.gov/ofac/downloads/sdn.csv"
    resp = requests.get(url, timeout=60)
    return resp.content.decode("latin-1")
```

---

### 1.13 FATF (Financial Action Task Force)

| Field | Details |
|-------|---------|
| **Source** | FATF Mutual Evaluations & Guidance |
| **URL** | https://www.fatf-gafi.org/ |
| **What it provides** | AML/CFT standards, country mutual evaluations, grey/black lists, guidance documents |
| **How to access** | Open download |
| **Industries covered** | Banking (19), Crypto (21), RegTech (23), InsurTech (20) |

---

### 1.14 EU Sanctions Map

| Field | Details |
|-------|---------|
| **Source** | EU Consolidated Sanctions |
| **URL** | https://www.sanctionsmap.eu/ |
| **API** | XML feeds available |
| **What it provides** | All EU sanctions by country/region, legal basis, updates |
| **How to access** | Open |
| **Industries covered** | Banking (19), Crypto (21), RegTech (23), Defense (14) |

---

### 1.15 US Patent Assignment Data

| Field | Details |
|-------|---------|
| **Source** | USPTO Patent Assignment API |
| **URL** | https://developer.uspto.gov/api-catalog |
| **What it provides** | Patent assignment records, trademark data |
| **How to access** | Open API |
| **Industries covered** | All technology industries |

---

### 1.16 World Legal Information (WorldLII)

| Field | Details |
|-------|---------|
| **Source** | World Legal Information Institute |
| **URL** | https://www.worldlii.org/ |
| **What it provides** | Case law, legislation from 60+ jurisdictions |
| **How to access** | Open web scraping |
| **Industries covered** | LegalTech (31) |

---

### 1.17 HUDOC (ECHR)

| Field | Details |
|-------|---------|
| **Source** | European Court of Human Rights |
| **URL** | https://hudoc.echr.coe.int/ |
| **API** | REST API available |
| **What it provides** | All ECHR judgments, decisions, case law |
| **How to access** | Open |
| **Industries covered** | LegalTech (31), AI Governance (18), Surveillance (15) |

---

### 1.18 UK National Archives (Case Law)

| Field | Details |
|-------|---------|
| **Source** | UK Case Law |
| **URL** | https://caselaw.nationalarchives.gov.uk/ |
| **API** | https://case.law/api/ |
| **What it provides** | England and Wales court decisions |
| **How to access** | Open |
| **Industries covered** | LegalTech (31) |

---

### 1.19 BAILII

| Field | Details |
|-------|---------|
| **Source** | British and Irish Legal Information Institute |
| **URL** | https://www.bailii.org/ |
| **What it provides** | UK, Ireland, Commonwealth court decisions |
| **How to access** | Open web access |
| **Industries covered** | LegalTech (31) |

---

### 1.20 Federal Judicial Center (US)

| Field | Details |
|-------|---------|
| **Source** | FJC Integrated Database |
| **URL** | https://www.fjc.gov/research/idb |
| **What it provides** | Federal court statistical data, case outcomes |
| **How to access** | Free for research |
| **Industries covered** | LegalTech (31) |

---

### 1.21 CourtListener / Free Law Project

| Field | Details |
|-------|---------|
| **Source** | CourtListener (Free Law Project) |
| **URL** | https://www.courtlistener.com/ |
| **API** | https://www.courtlistener.com/api/rest-info/ |
| **What it provides** | 10M+ US court opinions, oral arguments, PACER documents via RECAP |
| **How to access** | Open API |
| **Industries covered** | LegalTech (31) |

```python
def fetch_courtlistener_search(query="artificial intelligence", limit=20):
    """Search CourtListener opinions"""
    url = "https://www.courtlistener.com/api/rest/v3/opinions/"
    params = {"q": query, "page_size": limit}
    resp = requests.get(url, params=params, timeout=30)
    return resp.json()
```

---

### 1.22 OCCRP Aleph

| Field | Details |
|-------|---------|
| **Source** | Organized Crime and Corruption Reporting Project |
| **URL** | https://aleph.occrp.org/ |
| **API** | Available |
| **What it provides** | Global investigative database: company records, leaks, sanctions |
| **How to access** | Open search |
| **Industries covered** | LegalTech (31), RegTech (23), Banking (19) |

---

## 2. Financial & Market Data

### 2.1 FRED (Federal Reserve Economic Data)

| Field | Details |
|-------|---------|
| **Source** | Federal Reserve Bank of St. Louis |
| **URL** | https://fred.stlouisfed.org/ |
| **API** | https://fred.stlouisfed.org/docs/api/api_key.html |
| **What it provides** | 800,000+ economic time series: interest rates, GDP, inflation, employment, exchange rates |
| **How to access** | Free API key required (instant signup) |
| **Rate limits** | 120 req/minute |
| **Industries covered** | All financial (19-24), Economic indicators for all 47 |
| **Last updated** | Daily (some real-time) |

```python
def fetch_fred_series(series_id="DFF", api_key=None, start="2020-01-01"):
    """Fetch FRED economic time series"""
    url = "https://api.stlouisfed.org/fred/series/observations"
    params = {
        "series_id": series_id,  # DFF = Federal Funds Rate
        "api_key": api_key,
        "file_type": "json",
        "observation_start": start
    }
    resp = requests.get(url, params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()["observations"]

# Key series for simulation:
# DFF = Federal Funds Effective Rate
# GDP = Gross Domestic Product
# CPIAUCSL = Consumer Price Index
# UNRATE = Unemployment Rate
# DJIA = Dow Jones Industrial Average
# SP500 = S&P 500
# VIXCLS = CBOE Volatility Index
```

---

### 2.2 Alpha Vantage

| Field | Details |
|-------|---------|
| **Source** | Alpha Vantage |
| **URL** | https://www.alphavantage.co/ |
| **API** | https://www.alphavantage.co/support/#api-key |
| **What it provides** | Stock quotes, time series (daily/intraday), forex, crypto, technical indicators, earnings, news sentiment |
| **How to access** | Free API key (150 requests/day) |
| **Rate limits** | 25 requests/day (free tier); 75 calls/minute (premium) |
| **Industries covered** | Banking (19), Algo Trading (22), Crypto (21), Fintech (24) |
| **Last updated** | Real-time (delayed for free tier) |

```python
def fetch_alpha_vantage(symbol="AAPL", function="TIME_SERIES_DAILY", api_key=None):
    """Fetch stock data from Alpha Vantage"""
    url = "https://www.alphavantage.co/query"
    params = {
        "function": function,
        "symbol": symbol,
        "apikey": api_key,
        "outputsize": "full",
        "datatype": "json"
    }
    resp = requests.get(url, params=params, timeout=30)
    return resp.json()

# Key functions:
# TIME_SERIES_DAILY - daily stock prices
# TIME_SERIES_INTRADAY - intraday prices
# OVERVIEW - company fundamentals
# EARNINGS - quarterly earnings
# CRYPTO_INTRADAY - crypto prices
# FOREX_DAILY - forex rates
# NEWS_SENTIMENT - news sentiment
```

---

### 2.3 Yahoo Finance (via yfinance Python library)

| Field | Details |
|-------|---------|
| **Source** | Yahoo Finance (unofficial API via yfinance) |
| **URL** | https://finance.yahoo.com/ |
| **Library** | `pip install yfinance` |
| **What it provides** | Stock prices, options, financials, balance sheets, cash flow, holders, calendar, recommendations |
| **How to access** | Free Python library (unofficial) |
| **Rate limits** | Not specified (use responsibly) |
| **Industries covered** | All financial industries |

```python
import yfinance as yf

def fetch_yahoo_finance(ticker="AAPL", period="1y"):
    """Fetch comprehensive stock data"""
    stock = yf.Ticker(ticker)
    hist = stock.history(period=period)
    info = stock.info
    financials = stock.financials
    balance = stock.balance_sheet
    return {
        "history": hist,
        "info": info,
        "financials": financials,
        "balance_sheet": balance
    }

# Fetch multiple tickers relevant to MEOK industries
tickers = ["NVDA", "MSFT", "GOOGL", "TSLA", "META", "AMZN", "CRM",
           "JPM", "GS", "V", "MA", "COIN", "PLTR", "CRWD", "PANW"]
```

---

### 2.4 CoinGecko API

| Field | Details |
|-------|---------|
| **Source** | CoinGecko |
| **URL** | https://www.coingecko.com/api |
| **API** | https://api.coingecko.com/api/v3/ |
| **What it provides** | Crypto prices, market cap, volume, exchange data, coin categories, DeFi metrics, NFT data |
| **How to access** | Free tier: 10-30 calls/minute. Pro plan available |
| **Rate limits** | 10-30 calls/min (free); 500 calls/min (pro) |
| **Industries covered** | Crypto (21), Fintech (24), Banking (19) |
| **Last updated** | Real-time |

```python
def fetch_coingecko_coins(vs_currency="usd", per_page=100, page=1):
    """Fetch top cryptocurrencies by market cap"""
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": vs_currency,
        "order": "market_cap_desc",
        "per_page": per_page,
        "page": page,
        "sparkline": "false"
    }
    resp = requests.get(url, params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()

def fetch_coingecko_categories():
    """Fetch crypto market categories"""
    url = "https://api.coingecko.com/api/v3/coins/categories/list"
    resp = requests.get(url, timeout=30)
    return resp.json()
```

---

### 2.5 BIS (Bank for International Settlements)

| Field | Details |
|-------|---------|
| **Source** | BIS Statistics |
| **URL** | https://www.bis.org/statistics/ |
| **API** | https://stats.bis.org/api/v1/ |
| **What it provides** | Global banking statistics, credit, debt securities, property prices, exchange rates, derivatives |
| **How to access** | Open API |
| **Industries covered** | Banking (19), RegTech (23), Fintech (24), InsurTech (20) |
| **Last updated** | Quarterly |

---

### 2.6 ECB Statistical Data Warehouse

| Field | Details |
|-------|---------|
| **Source** | European Central Bank |
| **URL** | https://sdw.ecb.europa.eu/ |
| **API** | https://data-api.ecb.europa.eu/ |
| **What it provides** | Euro area financial data, interest rates, exchange rates, monetary aggregates, bank lending |
| **How to access** | Open |
| **Industries covered** | Banking (19), Fintech (24), RegTech (23) |

---

### 2.7 Twelve Data API

| Field | Details |
|-------|---------|
| **Source** | Twelve Data |
| **URL** | https://twelvedata.com/ |
| **API** | https://api.twelvedata.com/ |
| **What it provides** | Stock prices, forex, crypto, ETFs, indices, technical indicators |
| **How to access** | Free tier: 800 API calls/day |
| **Rate limits** | 800/day (free); 800/min (pro) |
| **Industries covered** | Algo Trading (22), Banking (19), Fintech (24) |

---

### 2.8 Finnhub API

| Field | Details |
|-------|---------|
| **Source** | Finnhub |
| **URL** | https://finnhub.io/ |
| **API** | https://finnhub.io/docs/api/ |
| **What it provides** | Real-time stock prices, financial statements, insider transactions, news, earnings, COVID-19 data |
| **How to access** | Free tier: 60 calls/minute |
| **Rate limits** | 60/min (free); unlimited (paid) |
| **Industries covered** | Algo Trading (22), Banking (19), Fintech (24) |

---

### 2.9 Polygon.io

| Field | Details |
|-------|---------|
| **Source** | Polygon.io |
| **URL** | https://polygon.io/ |
| **API** | REST/WebSocket APIs |
| **What it provides** | Stock market data, forex, crypto, options, historical tick data |
| **How to access** | Free tier: 5 API calls/minute |
| **Rate limits** | 5/min (free); unlimited (paid) |
| **Industries covered** | Algo Trading (22), Fintech (24) |

---

### 2.10 DeFi Llama

| Field | Details |
|-------|---------|
| **Source** | DeFi Llama |
| **URL** | https://defillama.com/ |
| **API** | https://api.llama.fi/ |
| **What it provides** | DeFi TVL (Total Value Locked) by protocol/chain, yields, volumes, fees, revenue |
| **How to access** | Open API |
| **Industries covered** | Crypto (21), Fintech (24) |

```python
def fetch_defillama_protocols():
    """Fetch all DeFi protocols with TVL"""
    url = "https://api.llama.fi/protocols"
    resp = requests.get(url, timeout=30)
    return resp.json()

def fetch_defillama_chains():
    """Fetch TVL by blockchain"""
    url = "https://api.llama.fi/chains"
    resp = requests.get(url, timeout=30)
    return resp.json()
```

---

### 2.11 Blockchain.com / Blockchain Data

| Field | Details |
|-------|---------|
| **Source** | Blockchain.com API |
| **URL** | https://www.blockchain.com/api |
| **What it provides** | Bitcoin blockchain data: blocks, transactions, charts, pools, fees |
| **How to access** | Open API |
| **Industries covered** | Crypto (21) |

---

### 2.12 Etherscan API

| Field | Details |
|-------|---------|
| **Source** | Etherscan |
| **URL** | https://etherscan.io/apis |
| **What it provides** | Ethereum blockchain data: transactions, addresses, tokens, contracts, gas prices |
| **How to access** | Free API key required |
| **Rate limits** | 5 calls/sec (free) |
| **Industries covered** | Crypto (21), Fintech (24) |

---

### 2.13 Dune Analytics

| Field | Details |
|-------|---------|
| **Source** | Dune Analytics |
| **URL** | https://dune.com/ |
| **API** | Requires API key |
| **What it provides** | Community blockchain analytics queries |
| **How to access** | Free tier (community queries); API key for programmatic |
| **Industries covered** | Crypto (21) |

---

### 2.14 NAIC Insurance Data

| Field | Details |
|-------|---------|
| **Source** | National Association of Insurance Commissioners |
| **URL** | https://content.naic.org/ |
| **What it provides** | US insurance market statistics, regulatory data |
| **How to access** | Open download |
| **Industries covered** | InsurTech (20) |

---

### 2.15 OECD Insurance Statistics

| Field | Details |
|-------|---------|
| **Source** | OECD |
| **URL** | https://data.oecd.org/insurance.htm |
| **What it provides** | Cross-country insurance market data |
| **How to access** | Open |
| **Industries covered** | InsurTech (20) |

---

### 2.16 Swiss Re / Munich Re Data

| Field | Details |
|-------|---------|
| **Source** | Swiss Re Institute / Munich Re |
| **URL** | https://www.swissre.com/institute/research |
| **What it provides** | Insurance industry research, sigma reports, catastrophe data |
| **How to access** | Open download (registration for some) |
| **Industries covered** | InsurTech (20) |

---

## 3. Healthcare, Bio & Pharma Data

### 3.1 PubMed / NCBI E-utilities

| Field | Details |
|-------|---------|
| **Source** | NIH National Library of Medicine |
| **URL** | https://pubmed.ncbi.nlm.nih.gov/ |
| **API** | https://www.ncbi.nlm.nih.gov/home/develop/api/ (E-utilities) |
| **What it provides** | 37M+ biomedical article abstracts, full-text articles (PMC), gene/protein/sequence data |
| **How to access** | Open API, no key required (faster with API key) |
| **Rate limits** | 3 requests/second without key; 10/sec with API key |
| **Industries covered** | Healthcare AI (7), Biotech (9), Pharma AI (10), Bioinformatics (12) |
| **Last updated** | Daily |

```python
def search_pubmed(query="artificial intelligence healthcare", max_results=100):
    """Search PubMed articles"""
    # Step 1: Search for IDs
    search_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": query,
        "retmax": max_results,
        "retmode": "json"
    }
    resp = requests.get(search_url, params=params, timeout=30)
    data = resp.json()
    ids = data["esearchresult"]["idlist"]

    # Step 2: Fetch summaries
    if ids:
        summary_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
        sum_params = {"db": "pubmed", "id": ",".join(ids), "retmode": "json"}
        sum_resp = requests.get(summary_url, params=sum_params, timeout=30)
        return sum_resp.json()
    return {}
```

---

### 3.2 openFDA Drug & Device Data

(See 1.4 above for full details)

Additional endpoints:
```python
def fetch_faers_reactions(reaction="HEADACHE", limit=100):
    """Fetch FAERS adverse event reports by reaction"""
    url = "https://api.fda.gov/drug/event.json"
    params = {"search": f"patient.reaction.reactionmeddrapt:{reaction}", "limit": limit}
    resp = requests.get(url, params=params, timeout=30)
    return resp.json()

def fetch_drug_labels(drug="aspirin", limit=100):
    """Fetch FDA drug labels"""
    url = "https://api.fda.gov/drug/label.json"
    params = {"search": f"openfda.brand_name:{drug}", "limit": limit}
    resp = requests.get(url, params=params, timeout=30)
    return resp.json()
```

---

### 3.3 WHO Global Health Observatory

| Field | Details |
|-------|---------|
| **Source** | World Health Organization |
| **URL** | https://www.who.int/data/gho |
| **API** | https://ghoapi.azureedge.net/api/ |
| **What it provides** | Global health statistics: mortality, disease burden, healthcare access, immunization, SDG indicators for 194 countries |
| **How to access** | Open OData API |
| **Rate limits** | No strict limits |
| **Industries covered** | Healthcare AI (7), Medical Devices (8), Telemedicine (11) |

```python
def fetch_who_indicators():
    """Fetch available WHO health indicators"""
    url = "https://ghoapi.azureedge.net/api/Indicator"
    resp = requests.get(url, timeout=30)
    return resp.json()

def fetch_who_data(indicator="SDGSUICIDE", year=2020):
    """Fetch specific indicator data"""
    url = f"https://ghoapi.azureedge.net/api/{indicator}"
    resp = requests.get(url, timeout=30)
    return resp.json()
```

---

### 3.4 CDC WONDER

| Field | Details |
|-------|---------|
| **Source** | Centers for Disease Control and Prevention |
| **URL** | https://wonder.cdc.gov/ |
| **API** | XML API available |
| **What it provides** | US mortality, natality, cancer, hospitalization, communicable disease data |
| **How to access** | Open (web + API) |
| **Industries covered** | Healthcare AI (7), Medical Devices (8), Pharma AI (10) |

---

### 3.5 HealthData.gov

| Field | Details |
|-------|---------|
| **Source** | US Health and Human Services |
| **URL** | https://healthdata.gov/ |
| **API** | Socrata Open Data API |
| **What it provides** | COVID-19 data, health equity, Medicare, hospital data |
| **How to access** | Open |
| **Industries covered** | Healthcare AI (7), Telemedicine (11) |

---

### 3.6 NCBI Databases Suite

| Field | Details |
|-------|---------|
| **Source** | NCBI (National Center for Biotechnology Information) |
| **URL** | https://www.ncbi.nlm.nih.gov/ |
| **Databases** | Gene, dbSNP, ClinVar, GEO, SRA, PubChem, OMIM, GenBank |
| **What it provides** | Genes, variants, clinical significance, gene expression, sequences, compounds, genetic disorders |
| **How to access** | Open E-utilities API |
| **Industries covered** | Biotech (9), Bioinformatics (12), Pharma AI (10) |

```python
def fetch_ncbi_gene(term="BRCA1"):
    """Search NCBI Gene database"""
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {"db": "gene", "term": term, "retmode": "json", "retmax": 10}
    resp = requests.get(url, params=params, timeout=30)
    return resp.json()

def fetch_clinvar(variant=None, gene="BRCA1"):
    """Fetch ClinVar clinical variant data"""
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {"db": "clinvar", "term": gene, "retmode": "json", "retmax": 50}
    resp = requests.get(url, params=params, timeout=30)
    return resp.json()
```

---

### 3.7 PubChem

| Field | Details |
|-------|---------|
| **Source** | NIH PubChem |
| **URL** | https://pubchem.ncbi.nlm.nih.gov/ |
| **API** | PUG-REST API |
| **What it provides** | 110M+ chemical compounds: structures, properties, bioassays, patents, literature |
| **How to access** | Open REST API |
| **Industries covered** | Pharma AI (10), Biotech (9) |

```python
def search_pubchem(name="aspirin"):
    """Search PubChem by compound name"""
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{name}/JSON"
    resp = requests.get(url, timeout=30)
    return resp.json()
```

---

### 3.8 ChEMBL

| Field | Details |
|-------|---------|
| **Source** | EMBL-EBI ChEMBL |
| **URL** | https://www.ebi.ac.uk/chembl/ |
| **API** | https://www.ebi.ac.uk/chembl/api/data/docs |
| **What it provides** | Bioactivity data: 2M+ compounds, 16K+ targets, 18M+ activities |
| **How to access** | Open REST API |
| **Industries covered** | Pharma AI (10), Biotech (9) |

```python
def search_chembl_target(target_name="kinase"):
    """Search ChEMBL targets"""
    url = "https://www.ebi.ac.uk/chembl/api/data/target/search"
    params = {"q": target_name, "format": "json"}
    resp = requests.get(url, params=params, timeout=30)
    return resp.json()
```

---

### 3.9 DrugBank

| Field | Details |
|-------|---------|
| **Source** | DrugBank |
| **URL** | https://go.drugbank.com/ |
| **API** | https://docs.drugbank.com/v1/ (free XML download) |
| **What it provides** | 15,000+ drug entries with chemical, pharmacological, pharmaceutical data |
| **How to access** | Free academic license for download |
| **Industries covered** | Pharma AI (10), Healthcare AI (7) |

---

### 3.10 Open Targets

| Field | Details |
|-------|---------|
| **Source** | Open Targets (EMBL-EBI) |
| **URL** | https://www.opentargets.org/ |
| **API** | https://platform-api.opentargets.io/ |
| **What it provides** | Target-disease evidence, drug targets, genetic associations |
| **How to access** | Open GraphQL API |
| **Industries covered** | Pharma AI (10), Biotech (9) |

---

### 3.11 The Cancer Imaging Archive (TCIA)

| Field | Details |
|-------|---------|
| **Source** | NCI-funded Cancer Imaging Archive |
| **URL** | https://www.cancerimagingarchive.net/ |
| **API** | NBIA Data Retriever + REST API |
| **What it provides** | 100+ cancer imaging collections, DICOM images, radiology annotations |
| **How to access** | Open (registration required for some collections) |
| **Industries covered** | Healthcare AI (7), Medical Devices (8) |

---

### 3.12 GTEx Portal

| Field | Details |
|-------|---------|
| **Source** | Genotype-Tissue Expression (GTEx) |
| **URL** | https://gtexportal.org/ |
| **API** | REST API available |
| **What it provides** | Tissue-specific gene expression data from 900+ donors, 50+ tissues |
| **How to access** | Open (registration for bulk data) |
| **Industries covered** | Biotech (9), Bioinformatics (12), Pharma AI (10) |

---

### 3.13 UCSC Genome Browser API

| Field | Details |
|-------|---------|
| **Source** | UCSC Genome Browser |
| **URL** | https://genome.ucsc.edu/ |
| **API** | https://api.genome.ucsc.edu/ |
| **What it provides** | Human and model organism genome data, annotations, tracks |
| **How to access** | Open REST API |
| **Industries covered** | Biotech (9), Bioinformatics (12) |

---

### 3.14 Ensembl

| Field | Details |
|-------|---------|
| **Source** | EMBL-EBI Ensembl |
| **URL** | https://www.ensembl.org/ |
| **API** | https://rest.ensembl.org/ |
| **What it provides** | Genome annotation, variation, comparative genomics, regulation |
| **How to access** | Open REST API |
| **Industries covered** | Biotech (9), Bioinformatics (12) |

```python
def fetch_ensembl_gene(symbol="BRCA1", species="homo_sapiens"):
    """Fetch gene information from Ensembl"""
    url = f"https://rest.ensembl.org/lookup/symbol/{species}/{symbol}"
    headers = {"Content-Type": "application/json"}
    resp = requests.get(url, headers=headers, timeout=30)
    return resp.json()
```

---

### 3.15 MIMIC-III (PhysioNet)

| Field | Details |
|-------|---------|
| **Source** | MIT Lab for Computational Physiology |
| **URL** | https://physionet.org/content/mimiciii/ |
| **What it provides** | De-identified health data from 40,000+ ICU patients at BIDMC |
| **How to access** | Credentialed access (free, requires training completion) |
| **Industries covered** | Healthcare AI (7) |

---

### 3.16 UK Biobank

| Field | Details |
|-------|---------|
| **Source** | UK Biobank |
| **URL** | https://www.ukbiobank.ac.uk/ |
| **What it provides** | Deep health data on 500,000 UK participants: genetics, imaging, health records |
| **How to access** | Researcher application required |
| **Industries covered** | Biotech (9), Healthcare AI (7) |

---

### 3.17 NIH Chest X-Ray Dataset

| Field | Details |
|-------|---------|
| **Source** | NIH Clinical Center |
| **URL** | https://nihcc.app.box.com/v/ChestXray-NIHCC |
| **What it provides** | 112,000+ frontal-view X-ray images with 14 disease labels |
| **How to access** | Open download |
| **Industries covered** | Healthcare AI (7), Medical Devices (8) |

---

### 3.18 OpenNeuro

| Field | Details |
|-------|---------|
| **Source** | OpenNeuro |
| **URL** | https://openneuro.org/ |
| **What it provides** | 700+ neuroimaging datasets (MRI, fMRI, EEG, MEG) |
| **How to access** | Open |
| **Industries covered** | Healthcare AI (7), Bioinformatics (12) |

---

### 3.19 FAERS (FDA Adverse Events)

| Field | Details |
|-------|---------|
| **Source** | FDA Adverse Event Reporting System |
| **URL** | https://www.fda.gov/drugs/drug-approvals-and-databases/fda-adverse-event-reporting-system-faers |
| **What it provides** | Adverse event reports, medication error reports, product quality complaints |
| **How to access** | Quarterly download files (open) |
| **Industries covered** | Pharma AI (10), Healthcare AI (7) |

---

### 3.20 CMS Healthcare Data

| Field | Details |
|-------|---------|
| **Source** | Centers for Medicare & Medicaid Services |
| **URL** | https://www.cms.gov/data-research |
| **What it provides** | Medicare/Medicaid data, hospital compare, provider data, telehealth utilization |
| **How to access** | Open (researcher data use agreements for some) |
| **Industries covered** | Healthcare AI (7), Telemedicine (11) |

---

### 3.21 EudraCT / EU Clinical Trials Register

| Field | Details |
|-------|---------|
| **Source** | European Medicines Agency |
| **URL** | https://www.clinicaltrialsregister.eu/ |
| **What it provides** | EU clinical trial database |
| **How to access** | Open search |
| **Industries covered** | Pharma AI (10), Biotech (9) |

---

### 3.22 WHO International Clinical Trials Registry

| Field | Details |
|-------|---------|
| **Source** | WHO ICTRP |
| **URL** | https://www.who.int/clinical-trials-registry-platform |
| **What it provides** | Aggregated global clinical trial data |
| **How to access** | Open search |
| **Industries covered** | Pharma AI (10), Biotech (9), Healthcare AI (7) |

---

## 4. Cybersecurity & Defense Data

### 4.1 MITRE ATT&CK

| Field | Details |
|-------|---------|
| **Source** | MITRE ATT&CK Framework |
| **URL** | https://attack.mitre.org/ |
| **API** | STIX/TAXII 2.0: https://attack.mitre.org/docs/enterprise-attack.json |
| **What it provides** | Globally accessible knowledge base of adversary tactics/techniques based on real-world observations |
| **How to access** | Open JSON/STIX downloads |
| **Rate limits** | N/A |
| **Industries covered** | Cybersecurity AI (13), Defense & Military AI (14), Critical Infrastructure (17) |
| **Last updated** | Quarterly |

```python
def fetch_mitre_attack():
    """Fetch MITRE ATT&CK Enterprise matrix"""
    url = "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/enterprise-attack/enterprise-attack.json"
    resp = requests.get(url, timeout=60)
    return resp.json()
```

---

### 4.2 MITRE D3FEND

| Field | Details |
|-------|---------|
| **Source** | MITRE D3FEND |
| **URL** | https://d3fend.mitre.org/ |
| **What it provides** | Knowledge graph of cybersecurity countermeasures |
| **How to access** | Open |
| **Industries covered** | Cybersecurity AI (13) |

---

### 4.3 CISA Alerts & Advisories

| Field | Details |
|-------|---------|
| **Source** | CISA |
| **URL** | https://www.cisa.gov/alerts |
| **API** | RSS/XML feeds |
| **What it provides** | Current cybersecurity alerts, advisories, vulnerability bulletins |
| **How to access** | Open feeds |
| **Industries covered** | Cybersecurity AI (13), Critical Infrastructure (17) |

---

### 4.4 VirusTotal

| Field | Details |
|-------|---------|
| **Source** | VirusTotal (Google) |
| **URL** | https://www.virustotal.com/ |
| **API** | https://developers.virustotal.com/ |
| **What it provides** | File/URL/IP reputation, malware analysis |
| **How to access** | Free tier: 4 lookups/min. API key required |
| **Industries covered** | Cybersecurity AI (13) |

---

### 4.5 Abuse.ch (Threat Intelligence)

| Field | Details |
|-------|---------|
| **Source** | Abuse.ch |
| **URL** | https://abuse.ch/ |
| **API** | URLhaus, Threat Fox, MalwareBazaar APIs |
| **What it provides** | Suspicious domains, URLs, malware samples, IoCs |
| **How to access** | Open API |
| **Industries covered** | Cybersecurity AI (13) |

---

### 4.6 Shadowserver Foundation

| Field | Details |
|-------|---------|
| **Source** | Shadowserver |
| **URL** | https://www.shadowserver.org/ |
| **What it provides** | Free internet scanning data, threat reports |
| **How to access** | Open |
| **Industries covered** | Cybersecurity AI (13) |

---

### 4.7 GDELT Project

| Field | Details |
|-------|---------|
| **Source** | GDELT (Global Database of Events, Language, and Tone) |
| **URL** | https://www.gdeltproject.org/ |
| **API** | https://api.gdeltproject.org/api/v2/ |
| **What it provides** | Global event database, news sentiment, TV/radio transcripts; 2.5 trillion records |
| **How to access** | Open BigQuery access + API |
| **Rate limits** | No limits for API |
| **Industries covered** | Defense (14), AI Governance (18), News/Sentiment (all), LegalTech (31) |

```python
def fetch_gdelt_events(query="cybersecurity", start="20250101", end="20250701"):
    """Fetch GDELT global events"""
    url = "https://api.gdeltproject.org/api/v2/doc/doc"
    params = {
        "query": query,
        "mode": "ArtList",
        "startdatetime": f"{start}000000",
        "enddatetime": f"{end}235959",
        "format": "json"
    }
    resp = requests.get(url, params=params, timeout=30)
    return resp.json()
```

---

### 4.8 SIPRI Military Expenditure Database

| Field | Details |
|-------|---------|
| **Source** | Stockholm International Peace Research Institute |
| **URL** | https://www.sipri.org/databases/milex |
| **What it provides** | Global military spending data by country (1949-present) |
| **How to access** | Open download |
| **Industries covered** | Defense & Military AI (14) |

---

### 4.9 SIPRI Arms Transfers Database

| Field | Details |
|-------|---------|
| **Source** | SIPRI |
| **URL** | https://www.sipri.org/databases/armstransfers |
| **What it provides** | International arms transfers data |
| **How to access** | Open download |
| **Industries covered** | Defense & Military AI (14) |

---

### 4.10 DoD Cyber Exchange

| Field | Details |
|-------|---------|
| **Source** | US Department of Defense |
| **URL** | https://public.cyber.mil/ |
| **What it provides** | STIGs (Security Technical Implementation Guides), security controls |
| **How to access** | Open download |
| **Industries covered** | Defense & Military AI (14), Cybersecurity AI (13) |

---

### 4.11 CISA NCF (National Critical Functions)

| Field | Details |
|-------|---------|
| **Source** | CISA |
| **URL** | https://www.cisa.gov/national-critical-functions |
| **What it provides** | Critical function mapping and risk assessment framework |
| **How to access** | Open |
| **Industries covered** | Critical Infrastructure (17) |

---

## 5. Scientific & Research Data

### 5.1 arXiv

| Field | Details |
|-------|---------|
| **Source** | arXiv (Cornell University) |
| **URL** | https://arxiv.org/ |
| **API** | https://arxiv.org/help/api |
| **What it provides** | 2.5M+ scientific preprints: AI, ML, physics, CS, math, quant-ph, eess |
| **How to access** | Open API |
| **Rate limits** | No limits |
| **Industries covered** | AI/ML (1), Quantum Computing (27), Bioinformatics (12), All research-driven industries |
| **Last updated** | Daily |

```python
def fetch_arxiv_papers(query="artificial intelligence", max_results=100):
    """Fetch papers from arXiv"""
    url = "http://export.arxiv.org/api/query"
    params = {
        "search_query": f"all:{query}",
        "start": 0,
        "max_results": max_results,
        "sortBy": "submittedDate",
        "sortOrder": "descending"
    }
    resp = requests.get(url, params=params, timeout=30)
    # Returns Atom XML - parse with feedparser or xml.etree
    return resp.text
```

---

### 5.2 Google Scholar

| Field | Details |
|-------|---------|
| **Source** | Google Scholar |
| **URL** | https://scholar.google.com/ |
| **API** | No official API; use `scholarly` Python library |
| **What it provides** | Academic paper search, citation counts, author profiles |
| **How to access** | `pip install scholarly` (unofficial) |
| **Rate limits** | Subject to Google rate limiting (use proxies) |
| **Industries covered** | All research-driven industries |

```python
# pip install scholarly
from scholarly import scholarly

def search_scholar(query="AI regulation 2025", limit=10):
    """Search Google Scholar"""
    search_query = scholarly.search_pubs(query)
    results = []
    for i, paper in enumerate(search_query):
        if i >= limit:
            break
        results.append({
            "title": paper.get("bib", {}).get("title"),
            "authors": paper.get("bib", {}).get("author"),
            "year": paper.get("bib", {}).get("pub_year"),
            "abstract": paper.get("bib", {}).get("abstract"),
            "citations": paper.get("num_citations"),
            "url": paper.get("pub_url")
        })
    return results
```

---

### 5.3 Semantic Scholar

| Field | Details |
|-------|---------|
| **Source** | AI2 Semantic Scholar |
| **URL** | https://www.semanticscholar.org/ |
| **API** | https://api.semanticscholar.org/ |
| **What it provides** | 200M+ papers, citations, author info, TLDR summaries, influential citations |
| **How to access** | Free API key (500 req/5min) |
| **Industries covered** | All research-driven industries |

```python
def fetch_semantic_scholar(query="AI regulation", limit=100):
    """Search Semantic Scholar"""
    url = "https://api.semanticscholar.org/graph/v1/paper/search"
    params = {
        "query": query,
        "limit": limit,
        "fields": "title,authors,year,citationCount,abstract,url"
    }
    resp = requests.get(url, params=params, timeout=30)
    return resp.json()
```

---

### 5.4 CORE (Open Access Research Papers)

| Field | Details |
|-------|---------|
| **Source** | CORE (Open University) |
| **URL** | https://core.ac.uk/ |
| **API** | https://api.core.ac.uk/docs/v3/ |
| **What it provides** | 210M+ open access research papers |
| **How to access** | Free API key |
| **Industries covered** | All research-driven industries |

---

### 5.5 Unpaywall

| Field | Details |
|-------|---------|
| **Source** | Unpaywall (Our Research) |
| **URL** | https://unpaywall.org/ |
| **API** | https://api.unpaywall.org/ |
| **What it provides** | Find free PDF versions of paywalled papers |
| **How to access** | Free API (no key for light use; email for key) |
| **Industries covered** | All research-driven industries |

---

### 5.6 Hugging Face Datasets

| Field | Details |
|-------|---------|
| **Source** | Hugging Face |
| **URL** | https://huggingface.co/datasets |
| **API** | `datasets` library |
| **What it provides** | Thousands of NLP, vision, audio datasets formatted for ML |
| **How to access** | `pip install datasets` |
| **Industries covered** | AI/ML (1), Healthcare AI (7), Gaming AI (25) |

---

### 5.7 Papers With Code

| Field | Details |
|-------|---------|
| **Source** | Papers With Code |
| **URL** | https://paperswithcode.com/ |
| **API** | https://paperswithcode.com/api/v1/ |
| **What it provides** | ML papers linked to code, datasets, benchmarks (SOTA tracking) |
| **How to access** | Open REST API |
| **Industries covered** | AI/ML (1), All AI-driven industries |

```python
def fetch_paperswithcode(area="artificial-intelligence", limit=50):
    """Fetch papers from Papers With Code"""
    url = "https://paperswithcode.com/api/v1/papers/"
    params = {"q": area, "items_per_page": limit}
    resp = requests.get(url, params=params, timeout=30)
    return resp.json()
```

---

### 5.8 Kaggle Datasets

| Field | Details |
|-------|---------|
| **Source** | Kaggle |
| **URL** | https://www.kaggle.com/datasets |
| **API** | `kaggle` CLI + Python API |
| **What it provides** | 100,000+ community-curated datasets with notebooks |
| **How to access** | Free (requires Kaggle account + API token) |
| **Industries covered** | All 47 industries |

---

### 5.9 UCI Machine Learning Repository

| Field | Details |
|-------|---------|
| **Source** | UC Irvine |
| **URL** | https://archive.ics.uci.edu/ml |
| **What it provides** | Classic benchmark datasets for ML |
| **How to access** | Open download |
| **Industries covered** | AI/ML (1) |

---

### 5.10 Zenodo / Open Science

| Field | Details |
|-------|---------|
| **Source** | CERN Zenodo |
| **URL** | https://zenodo.org/ |
| **API** | REST API |
| **What it provides** | Research data, software, publications, datasets |
| **How to access** | Open |
| **Industries covered** | All research-driven industries |

---

### 5.11 Dimensions (Free Tier)

| Field | Details |
|-------|---------|
| **Source** | Dimensions / Digital Science |
| **URL** | https://www.dimensions.ai/ |
| **API** | Requires token (free tier for researchers) |
| **What it provides** | Research analytics, publication data, funding, patents |
| **How to access** | Free for academic use |
| **Industries covered** | All research-driven industries |

---

## 6. Corporate & Business Data

### 6.1 OpenCorporates

| Field | Details |
|-------|---------|
| **Source** | OpenCorporates (the largest open company database) |
| **URL** | https://opencorporates.com/ |
| **API** | https://api.opencorporates.com/ |
| **What it provides** | 200M+ companies from 140+ jurisdictions: officers, filings, corporate groups |
| **How to access** | Free tier: 500 requests/day. API key for more |
| **Rate limits** | 500/day (free) |
| **Industries covered** | RegTech (23), LegalTech (31), Banking (19), Fintech (24) |
| **Last updated** | Daily |

```python
def search_opencorporates(name="OpenAI", jurisdiction=None):
    """Search OpenCorporates company database"""
    url = "https://api.opencorporates.com/v0.4/companies/search"
    params = {"q": name, "per_page": 20}
    if jurisdiction:
        params["jurisdiction_code"] = jurisdiction
    resp = requests.get(url, params=params, timeout=30)
    return resp.json()
```

---

### 6.2 LEI (Legal Entity Identifier) - GLEIF

| Field | Details |
|-------|---------|
| **Source** | Global Legal Entity Identifier Foundation |
| **URL** | https://www.gleif.org/ |
| **API** | https://api.gleif.org/api/v1/ |
| **What it provides** | Standardized legal entity identifiers, entity data, relationships |
| **How to access** | Open API (free) |
| **Rate limits** | No strict limits |
| **Industries covered** | Banking (19), RegTech (23), Fintech (24) |

```python
def search_lei(name="JPMorgan"):
    """Search LEI database"""
    url = "https://api.gleif.org/api/v1/lei-records"
    params = {"filter[entity.legalName]": name, "page[size]": 10}
    resp = requests.get(url, params=params, timeout=30)
    return resp.json()
```

---

### 6.3 UK Companies House

| Field | Details |
|-------|---------|
| **Source** | Companies House (UK) |
| **URL** | https://find-and-update.company-information.service.gov.uk/ |
| **API** | https://developer.company-information.service.gov.uk/ |
| **What it provides** | UK company filings, directors, accounts, charges, insolvency |
| **How to access** | Free API key |
| **Rate limits** | 600 requests/5 minutes |
| **Industries covered** | RegTech (23), LegalTech (31) |

---

### 6.4 Crunchbase (Free Tier)

| Field | Details |
|-------|---------|
| **Source** | Crunchbase |
| **URL** | https://www.crunchbase.com/ |
| **API** | https://data.crunchbase.com/docs/ |
| **What it provides** | Startup/companies: funding rounds, acquisitions, investors, leadership |
| **How to access** | Free tier: limited access. API key required |
| **Industries covered** | All industries (startup tracking) |

---

### 6.5 PitchBook (Free Reports)

| Field | Details |
|-------|---------|
| **Source** | PitchBook |
| **URL** | https://pitchbook.com/ |
| **What it provides** | VC/PE data, market maps, free reports |
| **How to access** | Free reports; full data requires subscription |
| **Industries covered** | All industries (investment tracking) |

---

## 7. Economic & Trade Data

### 7.1 World Bank Open Data

| Field | Details |
|-------|---------|
| **Source** | World Bank |
| **URL** | https://data.worldbank.org/ |
| **API** | https://api.worldbank.org/v2/ |
| **What it provides** | 17,000+ indicators: GDP, population, trade, health, education, infrastructure for 200+ countries |
| **How to access** | Open REST API |
| **Rate limits** | 100 requests/10 seconds |
| **Industries covered** | All 47 industries |
| **Last updated** | Daily/Quarterly depending on indicator |

```python
def fetch_worldbank_indicator(indicator="NY.GDP.MKTP.CD", countries="all", date="2020:2025"):
    """Fetch World Bank indicator data"""
    url = f"https://api.worldbank.org/v2/country/{countries}/indicator/{indicator}"
    params = {"date": date, "format": "json", "per_page": 1000}
    resp = requests.get(url, params=params, timeout=30)
    data = resp.json()
    return data[1] if len(data) > 1 else []

# Key indicators:
# NY.GDP.MKTP.CD = GDP (current US$)
# SP.POP.TOTL = Total population
# TG.VAL.TOTL.GD.ZS = Merchandise trade (% of GDP)
# IT.NET.USER.ZS = Internet users (% of population)
# GB.XPD.RSDV.GD.ZS = R&D expenditure (% of GDP)
# IP.JRN.ARTC.SC = Scientific journal articles
```

---

### 7.2 IMF Data Portal

| Field | Details |
|-------|---------|
| **Source** | International Monetary Fund |
| **URL** | https://data.imf.org/ |
| **API** | https://datahelp.imf.org/knowledgebase/articles/667681 |
| **What it provides** | World Economic Outlook data: GDP growth, inflation, unemployment, trade balances, government debt, FX reserves, COFER data |
| **How to access** | Open JSON REST API (SDMX) |
| **Rate limits** | No strict limits |
| **Industries covered** | All 47 industries |
| **Last updated** | Quarterly (WEO), Monthly (IFS) |

```python
def fetch_imf_weo_indicator(indicator="NGDP_RPCH", year=2025):
    """Fetch IMF WEO indicator"""
    # NGDP_RPCH = Real GDP growth
    url = f"https://www.imf.org/external/datamapper/api/v1/{indicator}"
    resp = requests.get(url, timeout=30)
    return resp.json()

def fetch_imf_cofer():
    """Fetch COFER (Currency Composition of FX Reserves)"""
    url = "https://www.imf.org/external/datamapper/api/v1/CU/COFER"
    resp = requests.get(url, timeout=30)
    return resp.json()
```

---

### 7.3 UN Comtrade

| Field | Details |
|-------|---------|
| **Source** | UN Comtrade (International Trade Statistics) |
| **URL** | https://comtrade.un.org/ |
| **API** | https://comtrade.un.org/api/ |
| **What it provides** | Detailed global trade data: imports/exports by commodity (HS codes), country pairs, values and quantities |
| **How to access** | Open API (bulk data requires subscription) |
| **Rate limits** | 100 requests/hour |
| **Industries covered** | Semiconductor (28), Manufacturing, Telecom (26), All trade-dependent industries |
| **Last updated** | Monthly |

```python
def fetch_comtrade(reporter="842",  # USA
                    partner="all",
                    year="2024",
                    flow="2",  # imports
                    commodity="854231",  # Semiconductor chips
                    freq="A"):
    """Fetch UN Comtrade data"""
    url = "https://comtrade.un.org/api/get"
    params = {
        "r": reporter, "p": partner, "y": year,
        "flow": flow, "ps": commodity, "freq": freq,
        "rg": "1", "fmt": "json"
    }
    resp = requests.get(url, params=params, timeout=30)
    return resp.json()
```

---

### 7.4 OECD Statistics

| Field | Details |
|-------|---------|
| **Source** | OECD |
| **URL** | https://stats.oecd.org/ |
| **API** | SDMX REST API |
| **What it provides** | Economic, social, environmental, education, health, trade, innovation statistics for 38 member countries |
| **How to access** | Open SDMX API |
| **Industries covered** | All industries |

```python
def fetch_oecd_data(dataset="QNA",  # Quarterly National Accounts
                     subject="GDP",
                     countries=["USA", "DEU", "JPN", "CHN"],
                     freq="Q"):
    """Fetch OECD statistical data"""
    country_str = "+".join(countries)
    url = f"https://stats.oecd.org/SDMX-JSON/data/{dataset}/{country_str}.{subject}.{freq}/all"
    resp = requests.get(url, timeout=30)
    return resp.json()
```

---

### 7.5 UN Data

| Field | Details |
|-------|---------|
| **Source** | UN Data |
| **URL** | https://data.un.org/ |
| **What it provides** | Trade, national accounts, energy, population, gender, education data from 30+ UN agencies |
| **How to access** | Open download and API |
| **Industries covered** | All industries |

---

### 7.6 WTO Trade Statistics

| Field | Details |
|-------|---------|
| **Source** | World Trade Organization |
| **URL** | https://www.wto.org/english/res_e/statis_e/trade_stats_e.htm |
| **What it provides** | International trade statistics, trade forecasts, trade policy reviews |
| **How to access** | Open download |
| **Industries covered** | All trade-dependent industries |

---

### 7.7 BIS Trade Data

(See 2.5 above)

---

### 7.8 ILO Statistics

| Field | Details |
|-------|---------|
| **Source** | International Labour Organization |
| **URL** | https://ilostat.ilo.org/ |
| **API** | SDMX API |
| **What it provides** | Employment, unemployment, wages, working hours, labor productivity |
| **How to access** | Open API |
| **Industries covered** | All industries |

---

### 7.9 NOAA Climate Data

| Field | Details |
|-------|---------|
| **Source** | NOAA |
| **URL** | https://www.ncdc.noaa.gov/ |
| **API** | https://www.ncei.noaa.gov/access/services |
| **What it provides** | Global climate data, weather, ocean data, natural disasters |
| **How to access** | Open API (token required for some) |
| **Industries covered** | InsurTech (20), Critical Infrastructure (17), Climate/Tech |

---

## 8. Geographic & Satellite Data

### 8.1 OpenStreetMap (OSM)

| Field | Details |
|-------|---------|
| **Source** | OpenStreetMap |
| **URL** | https://www.openstreetmap.org/ |
| **API** | Overpass API: https://overpass-api.de/api/ |
| **What it provides** | Free editable map of the world: roads, buildings, POIs, boundaries, infrastructure |
| **How to access** | Open Overpass API |
| **Rate limits** | Be reasonable (max 2 concurrent queries recommended) |
| **Industries covered** | Drones (5), Transport (29), Real Estate (34), Maritime (30), Telecom (26) |

```python
def query_overpass(query):
    """Query OpenStreetMap via Overpass API"""
    url = "https://overpass-api.de/api/interpreter"
    resp = requests.post(url, data={"data": query}, timeout=60)
    return resp.json()

# Example: Find all hospitals in London
hospital_query = """
[out:json];
area["name"="London"]->.searchArea;
(
  node["amenity"="hospital"](area.searchArea);
  way["amenity"="hospital"](area.searchArea);
  relation["amenity"="hospital"](area.searchArea);
);
out center;
"""
```

---

### 8.2 USGS Earth Explorer

| Field | Details |
|-------|---------|
| **Source** | USGS |
| **URL** | https://earthexplorer.usgs.gov/ |
| **What it provides** | Free satellite imagery: Landsat (since 1972), Sentinel-2, MODIS, DEMs |
| **How to access** | Free account required |
| **Industries covered** | Drones (5), Agriculture, Critical Infrastructure (17), Climate |

---

### 8.3 NASA Earth Data

| Field | Details |
|-------|---------|
| **Source** | NASA EOSDIS |
| **URL** | https://earthdata.nasa.gov/ |
| **API** | CMR API |
| **What it provides** | Satellite imagery, climate data, atmospheric data, ocean data |
| **How to access** | Free (Earthdata Login required) |
| **Industries covered** | Climate, Space (16), Critical Infrastructure (17) |

---

### 8.4 Google Earth Engine

| Field | Details |
|-------|---------|
| **Source** | Google Earth Engine |
| **URL** | https://earthengine.google.com/ |
| **API** | Python API (ee) |
| **What it provides** | Petabyte-scale satellite imagery catalog, geospatial analysis |
| **How to access** | Free for research/non-commercial (signup required) |
| **Industries covered** | Agriculture, Climate, Drones (5), Infrastructure (17) |

---

### 8.5 Sentinel Hub

| Field | Details |
|-------|---------|
| **Source** | Copernicus Sentinel |
| **URL** | https://www.sentinel-hub.com/ |
| **API** | OGC WMS/WMTS/WCS |
| **What it provides** | Sentinel-1, Sentinel-2, Sentinel-3, Landsat, MODIS imagery |
| **How to access** | Free tier (30 requests/min) |
| **Industries covered** | Agriculture, Climate, Infrastructure (17) |

---

## 9. Patent & Standards Data

### 9.1 USPTO Patent Public Search

| Field | Details |
|-------|---------|
| **Source** | US Patent and Trademark Office |
| **URL** | https://ppubs.uspto.gov/ |
| **API** | https://developer.uspto.org/ |
| **Bulk** | https://bulkdata.uspto.gov/ |
| **What it provides** | All US patents/applications: full text, claims, images, assignments, PAIR data |
| **How to access** | Open API + bulk download |
| **Rate limits** | No strict limits |
| **Industries covered** | All technology industries |
| **Last updated** | Weekly bulk files |

```python
def search_uspto_patents(query="artificial intelligence", rows=100):
    """Search USPTO patents"""
    url = "https://developer.uspto.gov/services/external/pair"
    # Or use Patent Public Search API
    url = "https://search.patentsview.org/api/v1/patent/"
    params = {"q": f"{{'_text_any':{{'patent_title':'{query}'}}}}", "f": "[\"patent_title\",\"patent_date\"]"}
    resp = requests.get(url, params=params, timeout=30)
    return resp.json()

# PatentsView (recommended free API)
def fetch_patentsview(query="artificial intelligence", limit=100):
    """Fetch patents via PatentsView"""
    url = "https://api.patentsview.org/patents/query"
    data = {
        "q": {"_text_any": {"patent_title": query}},
        "f": ["patent_number", "patent_title", "patent_date", "assignee_organization"],
        "o": {"per_page": limit}
    }
    resp = requests.post(url, json=data, timeout=30)
    return resp.json()
```

---

### 9.2 EPO Open Patent Services (OPS)

| Field | Details |
|-------|---------|
| **Source** | European Patent Office |
| **URL** | https://www.epo.org/searching-for-patents/technical/ops.html |
| **API** | REST API |
| **What it provides** | European patents: bibliographic data, full text, legal status, family |
| **How to access** | Free (3.6 GB/month), registered users get more |
| **Industries covered** | All technology industries |

---

### 9.3 WIPO PatentScope

| Field | Details |
|-------|---------|
| **Source** | World Intellectual Property Organization |
| **URL** | https://www.wipo.int/patentscope/ |
| **API** | https://www.wipo.int/patentscope/en/web-service/ |
| **What it provides** | PCT applications, global patent collections |
| **How to access** | Open search (API requires key) |
| **Industries covered** | All technology industries |

---

### 9.4 Google Patents Public Datasets

| Field | Details |
|-------|---------|
| **Source** | Google Patents |
| **URL** | https://patents.google.com/ |
| **Datasets** | BigQuery public datasets |
| **What it provides** | 100M+ patents worldwide, linked to Google Scholar citations |
| **How to access** | BigQuery (free tier: 1 TB query/month) |
| **Industries covered** | All technology industries |

---

### 9.5 NIST Publications

| Field | Details |
|-------|---------|
| **Source** | NIST |
| **URL** | https://www.nist.gov/publications |
| **API** | NIST Technical Series |
| **What it provides** | NIST AI RMF, cybersecurity standards, quantum computing standards, measurements |
| **How to access** | Open download |
| **Industries covered** | AI/ML (1), Cybersecurity (13), Quantum Computing (27), Semiconductor (28) |

---

### 9.6 3GPP Specifications

| Field | Details |
|-------|---------|
| **Source** | 3GPP |
| **URL** | https://www.3gpp.org/specifications |
| **What it provides** | 5G, 6G, LTE technical specifications |
| **How to access** | Free downloads |
| **Industries covered** | Telecom (26) |

---

### 9.7 ETSI Standards

| Field | Details |
|-------|---------|
| **Source** | ETSI |
| **URL** | https://www.etsi.org/standards |
| **What it provides** | European telecom, cybersecurity, IoT, MEC, PQC standards |
| **How to access** | Free download |
| **Industries covered** | Telecom (26), Cybersecurity (13), IoT (26), Quantum (27) |

---

### 9.8 ISO Standards (Publicly Available)

| Field | Details |
|-------|---------|
| **Source** | ISO |
| **URL** | https://www.iso.org/publications.html |
| **What it provides** | ISO/IEC standards (purchased), freely available standards (ISO/IEC 27001 preview) |
| **How to access** | Purchase or preview |
| **Industries covered** | All quality/security-driven industries |

---

### 9.9 O-RAN Alliance Specifications

| Field | Details |
|-------|---------|
| **Source** | O-RAN Alliance |
| **URL** | https://www.o-ran.org/specifications |
| **What it provides** | Open RAN technical specifications |
| **How to access** | Free download |
| **Industries covered** | Telecom (26) |

---

### 9.10 ITU-R Spectrum Management

| Field | Details |
|-------|---------|
| **Source** | ITU |
| **URL** | https://www.itu.int/en/ITU-R/seminars/Pages/default.aspx |
| **What it provides** | International spectrum allocation data |
| **How to access** | Open |
| **Industries covered** | Telecom (26), IoT (26) |

---

## 10. News, Sentiment & Social Data

### 10.1 GDELT Project

(See 4.7 for details)

Additional GDELT features:
```python
def fetch_gdelt_global_knowledge_graph(query="AI regulation", limit=250):
    """Fetch GDELT Global Knowledge Graph"""
    url = "https://api.gdeltproject.org/api/v2/gkg/gkg"
    params = {
        "query": query,
        "format": "json",
        "maxrecords": limit
    }
    resp = requests.get(url, params=params, timeout=30)
    return resp.json()
```

---

### 10.2 NewsAPI

| Field | Details |
|-------|---------|
| **Source** | NewsAPI |
| **URL** | https://newsapi.org/ |
| **API** | https://newsapi.org/docs |
| **What it provides** | News headlines/articles from 30,000+ sources worldwide |
| **How to access** | Free tier: 100 requests/day. API key required |
| **Rate limits** | 100/day (developer); 1000/day (paid) |
| **Industries covered** | All 47 industries (sentiment tracking) |

```python
def fetch_newsapi(query="artificial intelligence", from_date="2025-07-01",
                   api_key=None, page_size=100):
    """Fetch news via NewsAPI"""
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "from": from_date,
        "sortBy": "publishedAt",
        "pageSize": page_size,
        "apiKey": api_key
    }
    resp = requests.get(url, params=params, timeout=30)
    return resp.json()
```

---

### 10.3 Twitter/X API v2 (Free Tier)

| Field | Details |
|-------|---------|
| **Source** | X Developer Platform |
| **URL** | https://developer.twitter.com/en/docs/twitter-api |
| **What it provides** | Tweet lookup, recent search (7 days), user info |
| **How to access** | Free tier: 500 posts/month, 100 requests/month. API key required |
| **Rate limits** | 100 requests/month (free); higher tiers available |
| **Industries covered** | Social Media (37), Gaming (25), Crypto (21) |

---

### 10.4 Reddit API

| Field | Details |
|-------|---------|
| **Source** | Reddit |
| **URL** | https://www.reddit.com/dev/api/ |
| **What it provides** | Subreddit posts, comments, user data, voting |
| **How to access** | OAuth2 registration (free), User-Agent required |
| **Rate limits** | 60 requests/minute |
| **Industries covered** | Social Media (37), Gaming (25), Crypto (21) |

```python
def fetch_reddit_posts(subreddit="artificial", limit=25):
    """Fetch hot posts from a subreddit"""
    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    headers = {"User-Agent": "MEOK-Simulation/1.0"}
    params = {"limit": limit}
    resp = requests.get(url, headers=headers, params=params, timeout=30)
    return resp.json()
```

---

### 10.5 YouTube Data API

| Field | Details |
|-------|---------|
| **Source** | YouTube |
| **URL** | https://developers.google.com/youtube/v3 |
| **What it provides** | Video stats, channels, comments, search |
| **How to access** | Free quota: 10,000 units/day. API key required |
| **Industries covered** | Social Media (37), Streaming (38), Gaming (25), Education (32) |

---

### 10.6 Pushshift (Reddit Historical)

| Field | Details |
|-------|---------|
| **Source** | Pushshift |
| **URL** | https://github.com/pushshift/api |
| **What it provides** | Historical Reddit data archive |
| **How to access** | Open API |
| **Industries covered** | Social Media (37), All industries |

---

### 10.7 Mastodon API

| Field | Details |
|-------|---------|
| **Source** | Mastodon (fediverse) |
| **URL** | https://docs.joinmastodon.org/ |
| **What it provides** | Federated social media data |
| **How to access** | Open API (instance-dependent) |
| **Industries covered** | Social Media (37) |

---

### 10.8 Social Blade

| Field | Details |
|-------|---------|
| **Source** | Social Blade |
| **URL** | https://socialblade.com/ |
| **What it provides** | Social media statistics, growth tracking |
| **How to access** | Free tier |
| **Industries covered** | Social Media (37), Streaming (38), Gaming (25) |

---

### 10.9 Streams Charts

| Field | Details |
|-------|---------|
| **Source** | Streams Charts |
| **URL** | https://streamscharts.com/ |
| **API** | Available |
| **What it provides** | Cross-platform streaming data |
| **How to access** | Free test mode |
| **Industries covered** | Streaming (38), E-sports (39) |

---

### 10.10 Stream Hatchet

| Field | Details |
|-------|---------|
| **Source** | Stream Hatchet |
| **URL** | https://streamhatchet.com/ |
| **What it provides** | Live streaming analytics |
| **How to access** | Free reports |
| **Industries covered** | Streaming (38), E-sports (39) |

---

## 11. Industry-Specific Data Source Mapping

This section maps the most relevant data sources to each of the 47 industries for quick reference.

### AI & Robotics Industries (1-6)

| Industry | Priority Sources | Secondary Sources |
|----------|-----------------|-------------------|
| 1. AI/ML | arXiv, Papers With Code, Hugging Face, Google Dataset Search, NIST AI RMF | Semantic Scholar, UCI ML, Kaggle |
| 2. Humanoid Robotics | Open X-Embodiment, RH20T, BridgeData, MuJoCo, ROS | Robot Operating System, IEEE Xplore |
| 3. Autonomous Vehicles | NHTSA, KITTI, nuScenes, Waymo Open, CARLA, BDD100K | Argoverse, Lyft Level 5, Cityscapes |
| 4. Industrial Robotics | NIST Robotics, ROS Industrial, Gazebo, MoveIt | EuroC MAV, T-LESS, LineMod |
| 5. Drones & Aerial | FAA Part 107 data, DOTA, VisDrone, UAV123, OpenStreetMap | USGS Earth Explorer, xView, AirSim |
| 6. AI Agent Systems | SWE-bench, WebArena, AgentBench, arXiv, LangChain GitHub | AutoGPT, CrewAI, GAIA benchmark |

### Healthcare & Bio Industries (7-12)

| Industry | Priority Sources | Secondary Sources |
|----------|-----------------|-------------------|
| 7. Healthcare AI | PubMed, openFDA, ClinicalTrials.gov, WHO GHO, CDC WONDER | MIMIC-III, HealthData.gov, CMS |
| 8. Medical Devices | FDA 510(k), MAUDE, GUDID, EUDAMED, NMPA (China) | IMDRF, WHO medical devices |
| 9. Biotechnology & Genomics | NCBI Suite, UCSC, Ensembl, 1000 Genomes, ClinVar | GTEx, gnomAD, dbGaP, GenBank |
| 10. Pharmaceutical AI | ClinicalTrials.gov, PubChem, ChEMBL, DrugBank, FAERS | Open Targets, BindingDB, DailyMed |
| 11. Telemedicine & Digital Health | CMS Telehealth, WHO GHO, Eurostat Health, NHS Digital | HHS HealthData, CDC WONDER |
| 12. Bioinformatics | UniProt, PDB, AlphaFold DB, STRING, KEGG, Reactome | Gene Ontology, OMIM, BioPython |

### Cyber & Defense Industries (13-18)

| Industry | Priority Sources | Secondary Sources |
|----------|-----------------|-------------------|
| 13. Cybersecurity AI | CISA KEV, NVD, MITRE ATT&CK, CISA AIS, Abuse.ch | VirusTotal, Shadowserver, MISP |
| 14. Defense & Military AI | SIPRI, DoD Cyber Exchange, GDELT, NATO STANAGs | UK MoD, Arms transfers data |
| 15. Surveillance & Public Safety | NIST FRVT results, EU AI Act database,GDPR enforcement tracker | IPCC, academic papers |
| 16. Space Technology | NASA APIs, Space-Track, ESA, Launch Library | NOAA satellite data |
| 17. Critical Infrastructure | CISA NCF, NERC, ENISA, SOCI Act data | NIST CSF, sector-specific |
| 18. AI Governance & Safety | OECD.AI, EU AI Act, NIST AI RMF, Stanford HAI AI Index | Future of Humanity Institute reports |

### Finance Industries (19-24)

| Industry | Priority Sources | Secondary Sources |
|----------|-----------------|-------------------|
| 19. AI in Banking | FRED, SEC EDGAR, BIS, OFAC, FFIEC | FDIC, OCC data, bank call reports |
| 20. InsurTech | NAIC, Swiss Re Sigma, NOAA, WHO Mortality | OECD Insurance, Munich Re |
| 21. Cryptocurrency | CoinGecko, DeFi Llama, Etherscan, BIS CBDC Tracker | Blockchain.com, Dune, FATF |
| 22. Algo Trading | Alpha Vantage, Polygon, Twelve Data, Finnhub | CME Market Data, NASDAQ |
| 23. RegTech | OFAC, EU Sanctions, FATF, OpenCorporates, LEI | SEC EDGAR, Regulations.gov |
| 24. Payment Systems & Fintech | BIS Red Book, FRED, World Bank Findex, IMF | Central bank digital currency trackers |

### Telecom & Quantum Industries (25-30)

| Industry | Priority Sources | Secondary Sources |
|----------|-----------------|-------------------|
| 25. Telecom 5G/6G | GSA 5G Observatory, European 5G Observatory, Ookla | FCC Spectrum, 3GPP, ITU-R |
| 26. IoT | GSMA IoT, IoT Analytics, LoRa Alliance, oneM2M | IEEE IoT, Arm Pelion, OMA SpecWorks |
| 27. Quantum Computing | NIST PQC, arXiv quant-ph, QED-C, Unitary Fund | IBM Quantum Network, Quantum Open Source |
| 28. Cloud & Edge AI | Cloudflare Radar, Flexera, CNCF, Gartner summaries | Synergy Research, ETSI MEC |
| 29. Transport & Logistics | US DOT, BTS, PeMS, EU Transport, OpenStreetMap | Uber Movement, Waze, IMO GISIS |
| 30. Maritime & Ocean | IMO GISIS, MarineTraffic, NOAA Ocean, UNCLOS | IHS Markit (some free), port data |

### Gaming, Media & Legal/Edu Industries (31-47)

| Industry | Priority Sources | Secondary Sources |
|----------|-----------------|-------------------|
| 31. LegalTech | CourtListener, Free Law Project, EUR-Lex, BAILII | HUDOC, WorldLII, OCCRP Aleph |
| 32. Education AI | OECD Education, NCES, PISA, UNESCO, Khan Academy | EdStats, Eurostat Education |
| 33. VR/AR | Steam Hardware Survey, OpenXR, VRCompare | Unity/Unreal docs, Sketchfab |
| 34. Social Media | X API, Reddit API, YouTube API, Mastodon API | Social Blade, CrowdTangle |
| 35. Streaming & Entertainment | YouTube API, Spotify API, TMDb, Streams Charts | TwitchTracker, Stream Hatchet |
| 36. E-sports | EsportsEarnings, Twitch API, Steam API, Streams Charts | Esports Charts, game APIs |
| 37-47. Additional | See above categories for cross-cutting sources | World Bank, IMF, OECD |

---

## 12. API Key Summary

### Required API Keys (Free)

| Source | How to Get Key | Free Tier Limits |
|--------|---------------|-----------------|
| **NVD** | https://nvd.nist.gov/developers/request-an-api-key | 50 req/30s |
| **SEC EDGAR** | Set User-Agent header (no key) | 10 req/sec |
| **FRED** | https://fred.stlouisfed.org/docs/api/api_key.html | 120 req/min |
| **Alpha Vantage** | https://www.alphavantage.co/support/#api-key | 25 req/day |
| **NewsAPI** | https://newsapi.org/register | 100 req/day |
| **Etherscan** | https://etherscan.io/apis | 5 req/sec |
| **X/Twitter API** | https://developer.twitter.com/en/portal/dashboard | 100 req/month |
| **OpenCorporates** | https://opencorporates.com/info/our-data/API | 500 req/day |
| **Semantic Scholar** | https://www.semanticscholar.org/product/api | 500 req/5min |
| **YouTube Data API** | https://console.cloud.google.com/ | 10K units/day |
| **VirusTotal** | https://www.virustotal.com/gui/join-us | 4 req/min |
| **Regulations.gov** | https://open.gsa.gov/api/regulationsgov/ | 1000 req/day |
| **PatentsView** | Open (no key) | Reasonable |

### No API Key Required

| Source | Access Pattern |
|--------|---------------|
| **CISA KEV** | Direct CSV/JSON download |
| **ClinicalTrials.gov** | Open REST API v2 |
| **openFDA** | 240 req/min (no key) |
| **WHO GHO** | Open OData API |
| **World Bank** | Open REST API |
| **IMF Data** | Open SDMX/JSON API |
| **UN Comtrade** | Open API |
| **arXiv** | Open API |
| **MITRE ATT&CK** | Open JSON download |
| **GDELT** | Open API + BigQuery |
| **CoinGecko** | Open (rate limited) |
| **DeFi Llama** | Open API |
| **Overpass API** | Open (be reasonable) |
| **PubMed E-utilities** | 3 req/sec (no key) |
| **Ensembl REST** | Open |
| **EUR-Lex** | Open web services |
| **Data.gov** | Open CKAN API |
| **EU ODP** | Open |
| **SIPRI** | Open download |
| **GDELT** | Open |
| **OECD** | Open SDMX API |

---

## Quick Start: Top 20 Must-Have Sources

For fastest setup of the MEOK 47-industry simulation, prioritize these 20 sources:

1. **NVD** - CVE data for cybersecurity
2. **SEC EDGAR** - Financial filings for all public companies
3. **FRED** - Macroeconomic indicators
4. **PubMed** - Biomedical research
5. **openFDA** - Healthcare regulatory data
6. **ClinicalTrials.gov** - Clinical trial tracking
7. **World Bank** - Country-level economic data
8. **CoinGecko** - Crypto market data
9. **MITRE ATT&CK** - Threat intelligence
10. **GDELT** - Global events and sentiment
11. **arXiv** - AI/ML research papers
12. **Alpha Vantage** - Stock market data
13. **CISA KEV** - Actively exploited vulnerabilities
14. **WHO GHO** - Global health statistics
15. **IMF WEO** - Economic forecasts
16. **OpenCorporates** - Company registry data
17. **NewsAPI** - News sentiment data
18. **UN Comtrade** - International trade data
19. **PatentsView** - Innovation tracking
20. **OECD** - Cross-country statistics

---

*Catalog compiled: July 2026*
*All URLs and APIs verified as publicly accessible free data sources*
*Rate limits subject to change; always check source documentation*
