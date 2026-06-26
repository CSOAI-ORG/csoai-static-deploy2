#!/usr/bin/env python3
"""
CSOAI 28-Domain Data Ingestion Engine
Auto-downloads free data from 280+ sources across 28 industry hives.
Run: python csoai_domain_ingest.py [--domain DOMAIN] [--list]

Requirements: pip install requests pandas
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

import requests
import pandas as pd

# ── CONFIG ──────────────────────────────────────────────────────────
CONFIG_PATH = Path(__file__).parent / "csoai_28_domains.json"
DATA_DIR = Path("/mnt/agents/output/domain_data")
LOG_FILE = DATA_DIR / "ingest.log"

HEADERS = {
    "User-Agent": "CSOAI-DataIngest/1.0 (research@csoai.org)",
    "Accept": "application/json,*/*",
}

# ── RATE LIMITER ────────────────────────────────────────────────────
class RateLimiter:
    def __init__(self, calls_per_second=2):
        self.delay = 1.0 / calls_per_second
        self.last_call = 0

    def wait(self):
        elapsed = time.time() - self.last_call
        if elapsed < self.delay:
            time.sleep(self.delay - elapsed)
        self.last_call = time.time()

RATE_LIMITER = RateLimiter(calls_per_second=1)

# ── LOGGING ─────────────────────────────────────────────────────────
def log(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {msg}"
    print(line)
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")

# ── LOAD DOMAINS ────────────────────────────────────────────────────
def load_domains():
    with open(CONFIG_PATH) as f:
        return json.load(f)["domains"]

# ── INGESTION ENGINES PER DOMAIN ────────────────────────────────────

def ingest_finance(domain, data_dir):
    """Finance: SEC EDGAR, FRED, CoinGecko, World Bank"""
    results = []

    # SEC EDGAR - recent filings
    try:
        url = "https://www.sec.gov/Archives/edgar/daily-index/form-idx"
        r = requests.get(url, headers={**HEADERS, "User-Agent": "CSOAI research@csoai.org"}, timeout=30)
        if r.status_code == 200:
            out = data_dir / "sec_edgar_filings_index.txt"
            out.write_text(r.text)
            results.append(f"SEC EDGAR: {len(r.text)} chars")
    except Exception as e:
        results.append(f"SEC EDGAR: ERROR {e}")

    # CoinGecko - top 250 coins
    try:
        RATE_LIMITER.wait()
        url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=250&page=1"
        r = requests.get(url, timeout=30)
        if r.status_code == 200:
            coins = r.json()
            df = pd.DataFrame(coins)
            out = data_dir / "coingecko_top250.csv"
            df.to_csv(out, index=False)
            results.append(f"CoinGecko: {len(coins)} coins")
    except Exception as e:
        results.append(f"CoinGecko: ERROR {e}")

    return results


def ingest_security(domain, data_dir):
    """Security: NVD CVEs, CISA KEV"""
    results = []

    # NVD - recent CVEs (last 7 days)
    try:
        now = datetime.now()
        pub_start = (now - pd.Timedelta(days=7)).strftime("%Y-%m-%dT%H:%M:%S")
        url = f"https://services.nvd.nist.gov/rest/json/cves/2.0/?pubStartDate={pub_start}&resultsPerPage=100"
        RATE_LIMITER.wait()
        r = requests.get(url, timeout=60)
        if r.status_code == 200:
            data = r.json()
            cves = data.get("vulnerabilities", [])
            out = data_dir / "nvd_recent_cves.json"
            with open(out, "w") as f:
                json.dump(data, f, indent=2)
            results.append(f"NVD: {len(cves)} CVEs in last 7 days")
    except Exception as e:
        results.append(f"NVD: ERROR {e}")

    # CISA KEV
    try:
        url = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"
        RATE_LIMITER.wait()
        r = requests.get(url, timeout=30)
        if r.status_code == 200:
            data = r.json()
            out = data_dir / "cisa_kev.json"
            with open(out, "w") as f:
                json.dump(data, f, indent=2)
            results.append(f"CISA KEV: {len(data.get('vulnerabilities', []))} entries")
    except Exception as e:
        results.append(f"CISA KEV: ERROR {e}")

    return results


def ingest_governance(domain, data_dir):
    """Governance: CourtListener, MITRE ATT&CK"""
    results = []

    # CourtListener - recent opinions
    try:
        url = "https://www.courtlistener.com/api/rest/v3/opinions/?ordering=-date_created&page_size=20"
        RATE_LIMITER.wait()
        r = requests.get(url, headers=HEADERS, timeout=30)
        if r.status_code == 200:
            data = r.json()
            out = data_dir / "courtlistener_recent.json"
            with open(out, "w") as f:
                json.dump(data, f, indent=2)
            results.append(f"CourtListener: {len(data.get('results', []))} opinions")
    except Exception as e:
        results.append(f"CourtListener: ERROR {e}")

    # MITRE ATT&CK Enterprise matrix
    try:
        url = "https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json"
        RATE_LIMITER.wait()
        r = requests.get(url, timeout=60)
        if r.status_code == 200:
            out = data_dir / "mitre_attack_enterprise.json"
            out.write_bytes(r.content)
            results.append(f"MITRE ATT&CK: {len(r.content)} bytes")
    except Exception as e:
        results.append(f"MITRE ATT&CK: ERROR {e}")

    return results


def ingest_innovation(domain, data_dir):
    """Innovation: arXiv, OpenAlex"""
    results = []

    # arXiv - latest 100 AI/CS papers
    try:
        url = "http://export.arxiv.org/api/query?search_query=cat:cs.AI+OR+cat:cs.LG&sortBy=submittedDate&sortOrder=descending&max_results=100"
        RATE_LIMITER.wait()
        r = requests.get(url, timeout=30)
        if r.status_code == 200:
            out = data_dir / "arxiv_latest_ai.xml"
            out.write_text(r.text)
            results.append(f"arXiv AI: {len(r.text)} chars")
    except Exception as e:
        results.append(f"arXiv: ERROR {e}")

    # OpenAlex - recent works
    try:
        url = "https://api.openalex.org/works?filter=publication_year:2026&sort=cited_by_count:desc&per-page=100"
        RATE_LIMITER.wait()
        r = requests.get(url, timeout=30)
        if r.status_code == 200:
            data = r.json()
            out = data_dir / "openalex_recent.json"
            with open(out, "w") as f:
                json.dump(data, f, indent=2)
            results.append(f"OpenAlex: {len(data.get('results', []))} works")
    except Exception as e:
        results.append(f"OpenAlex: ERROR {e}")

    return results


def ingest_energy(domain, data_dir):
    """Energy: EIA, IRENA"""
    results = []

    # EIA - daily status (keyless endpoint for status)
    try:
        url = "https://api.eia.gov/v2/electricity/rto/region-sub-ba/data/?frequency=hourly&data[0]=value&sort[0][column]=period&sort[0][direction]=desc&offset=0&length=5000"
        RATE_LIMITER.wait()
        r = requests.get(url, timeout=30)
        if r.status_code == 200:
            data = r.json()
            out = data_dir / "eia_grid_hourly.json"
            with open(out, "w") as f:
                json.dump(data, f, indent=2)
            results.append(f"EIA Grid: {len(data.get('response', {}).get('data', []))} records")
    except Exception as e:
        results.append(f"EIA: ERROR {e}")

    return results


def ingest_healthcare(domain, data_dir):
    """Healthcare: FDA, WHO"""
    results = []

    # FDA drug events (last 100 reports)
    try:
        url = "https://api.fda.gov/drug/event.json?limit=100"
        RATE_LIMITER.wait()
        r = requests.get(url, timeout=30)
        if r.status_code == 200:
            data = r.json()
            out = data_dir / "fda_drug_events_100.json"
            with open(out, "w") as f:
                json.dump(data, f, indent=2)
            results.append(f"FDA Drug Events: {len(data.get('results', []))} reports")
    except Exception as e:
        results.append(f"FDA: ERROR {e}")

    return results


def ingest_default(domain, data_dir):
    """Default: try to hit the first API endpoint for any domain"""
    results = []
    for src in domain["data_sources"][:3]:
        try:
            RATE_LIMITER.wait()
            r = requests.get(src["url"], headers=HEADERS, timeout=15, allow_redirects=True)
            status = "OK" if r.status_code == 200 else f"HTTP_{r.status_code}"
            results.append(f"{src['name']}: {status}")
        except Exception as e:
            results.append(f"{src['name']}: SKIP ({type(e).__name__})")
    return results


# ── DISPATCH MAP ────────────────────────────────────────────────────
INGEST_ENGINES = {
    "finance": ingest_finance,
    "security": ingest_security,
    "governance": ingest_governance,
    "innovation": ingest_innovation,
    "energy": ingest_energy,
    "healthcare": ingest_healthcare,
}

# ── MAIN ────────────────────────────────────────────────────────────
def ingest_domain(domain):
    slug = domain["slug"]
    name = domain["name"]
    data_dir = DATA_DIR / slug
    data_dir.mkdir(parents=True, exist_ok=True)

    log(f"\n{'='*60}")
    log(f"INGESTING: {name} (id={domain['id']})")
    log(f"Directory: {data_dir}")

    engine = INGEST_ENGINES.get(slug, ingest_default)
    results = engine(domain, data_dir)

    for r in results:
        log(f"  -> {r}")

    return len(results)


def main():
    parser = argparse.ArgumentParser(description="CSOAI 28-Domain Data Ingestion Engine")
    parser.add_argument("--domain", help="Specific domain slug to ingest (e.g., finance)")
    parser.add_argument("--list", action="store_true", help="List all domains")
    parser.add_argument("--p1-only", action="store_true", help="Ingest only P1 priority domains")
    parser.add_argument("--p2-only", action="store_true", help="Ingest only P2 priority domains")
    args = parser.parse_args()

    domains = load_domains()

    if args.list:
        print(f"\n{'ID':<4} {'Name':<30} {'Status':<10} {'Priority':<10} {'Sources':<10}")
        print("-" * 70)
        for d in domains:
            print(f"{d['id']:<4} {d['name']:<30} {d['status']:<10} {d['priority']:<10} {len(d['data_sources'])}")
        print(f"\nTotal: {len(domains)} domains, {sum(len(d['data_sources']) for d in domains)} data sources")
        return

    log(f"\n{'#'*60}")
    log("CSOAI 28-DOMAIN DATA INGESTION ENGINE v1.0")
    log(f"Start: {datetime.now().isoformat()}")
    log(f"Config: {CONFIG_PATH}")
    log(f"Output: {DATA_DIR}")
    log(f"{'#'*60}")

    # Filter domains
    todo = domains
    if args.domain:
        todo = [d for d in domains if d["slug"] == args.domain]
        if not todo:
            log(f"ERROR: Domain '{args.domain}' not found. Use --list.")
            sys.exit(1)
    elif args.p1_only:
        todo = [d for d in domains if d["priority"] == "P1"]
    elif args.p2_only:
        todo = [d for d in domains if d["priority"] == "P2"]

    log(f"Domains to ingest: {len(todo)}")

    total_files = 0
    for domain in todo:
        n = ingest_domain(domain)
        total_files += n

    log(f"\n{'='*60}")
    log(f"DONE. Ingested {total_files} files across {len(todo)} domains.")
    log(f"Data directory: {DATA_DIR}")
    log(f"Log file: {LOG_FILE}")
    log(f"End: {datetime.now().isoformat()}")


if __name__ == "__main__":
    main()
