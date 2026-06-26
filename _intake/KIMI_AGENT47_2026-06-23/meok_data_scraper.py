#!/usr/bin/env python3
"""
================================================================================
MEOK 47-Industry Simulation - Free Data Scraping Toolkit
================================================================================
A comprehensive Python script to scrape free data from 200+ public sources
for all 47 industries in the MEOK simulation.

Author: MEOK Data Team
Version: 1.0
Date: July 2026

USAGE:
    # Fetch all data for all industries
    python meok_data_scraper.py --all

    # Fetch data for specific industries
    python meok_data_scraper.py --industries ai healthcare finance

    # Fetch data for a specific category
    python meok_data_scraper.py --category cybersecurity

    # Run in incremental mode (only new data since last run)
    python meok_data_scraper.py --all --incremental

    # List available industries
    python meok_data_scraper.py --list

REQUIREMENTS:
    pip install requests pandas beautifulsoup4 schedule python-dotenv feedparser

CONFIG:
    Create a .env file with API keys:
    NVD_API_KEY=your_key
    FRED_API_KEY=your_key
    ALPHA_VANTAGE_KEY=your_key
    NEWSAPI_KEY=your_key
    SEC_USER_AGENT="YourName contact@email.com"
"""

import os
import sys
import time
import json
import csv
import logging
import argparse
import hashlib
import traceback
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, asdict
from urllib.parse import urlencode, quote
import concurrent.futures
from functools import wraps

import requests
import pandas as pd
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# =============================================================================
# CONFIGURATION
# =============================================================================

# --- Load API Keys from Environment ---
# Create .env file or set environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# --- API Keys & Config ---
CONFIG = {
    # API Keys (load from environment or .env file)
    "NVD_API_KEY": os.getenv("NVD_API_KEY", ""),
    "FRED_API_KEY": os.getenv("FRED_API_KEY", ""),
    "ALPHA_VANTAGE_KEY": os.getenv("ALPHA_VANTAGE_KEY", ""),
    "NEWSAPI_KEY": os.getenv("NEWSAPI_KEY", ""),
    "ETHERSCAN_API_KEY": os.getenv("ETHERSCAN_API_KEY", ""),
    "REGULATIONS_GOV_KEY": os.getenv("REGULATIONS_GOV_KEY", ""),
    "SEC_USER_AGENT": os.getenv("SEC_USER_AGENT", "MEOK-Simulation contact@meok.ai"),
    "VIRUSTOTAL_KEY": os.getenv("VIRUSTOTAL_KEY", ""),

    # Rate limiting (requests per minute)
    "RATE_LIMITS": {
        "nvd": 5,  # requests per 30s without key, 50 with key
        "sec_edgar": 10,
        "fred": 120,
        "alpha_vantage": 25,  # per day
        "newsapi": 100,  # per day
        "pubmed": 3,  # per second
        "worldbank": 100,  # per 10 seconds
        "imf": 100,
        "eurostat": 100,
        "coingecko": 10,
        "clinicaltrials": 100,
        "opencorporates": 500,  # per day
        "regulations_gov": 1000,  # per day
        "youtube": 10000,  # per day (quota units)
        "default": 60,
    },

    # Output paths
    "OUTPUT_DIR": os.getenv("MEOK_OUTPUT_DIR", "./meok_data"),
    "LOG_DIR": os.getenv("MEOK_LOG_DIR", "./meok_logs"),

    # Incremental tracking
    "STATE_FILE": "scraper_state.json",

    # Request settings
    "REQUEST_TIMEOUT": 30,
    "MAX_RETRIES": 3,
    "BACKOFF_FACTOR": 0.5,

    # Parallel workers
    "MAX_WORKERS": 5,
}

# =============================================================================
# 47 INDUSTRY DEFINITIONS
# =============================================================================

INDUSTRIES = {
    # AI & Robotics (6)
    "ai_ml": {"id": 1, "name": "AI/ML", "category": "ai_robotics",
              "keywords": ["artificial intelligence", "machine learning", "deep learning", "neural network",
                           "foundation model", "LLM", "transformer"],
              "tickers": ["NVDA", "MSFT", "GOOGL", "META", "AMZN", "CRM", "IBM", "ORCL"],
              "sources": ["nvd", "arxiv", "patentsview", "sec_edgar", "newsapi", "gdelt"]},

    "humanoid_robotics": {"id": 2, "name": "Humanoid Robotics", "category": "ai_robotics",
                          "keywords": ["humanoid robot", "bipedal", "Tesla Optimus", "Figure AI",
                                       "Agility Robotics", "Boston Dynamics"],
                          "tickers": ["TSLA"],
                          "sources": ["sec_edgar", "newsapi", "patentsview"]},

    "autonomous_vehicles": {"id": 3, "name": "Autonomous Vehicles", "category": "ai_robotics",
                            "keywords": ["autonomous vehicle", "self-driving", "robotaxi", "Waymo",
                                         "LiDAR", "ADAS", "FSD"],
                            "tickers": ["TSLA", "GOOGL", "AUR", "MBLY"],
                            "sources": ["nhtsa", "sec_edgar", "newsapi", "patentsview"]},

    "industrial_robotics": {"id": 4, "name": "Industrial Robotics", "category": "ai_robotics",
                            "keywords": ["industrial robot", "cobot", "robotic arm", "AGV",
                                         "automation", "FANUC", "ABB"],
                            "tickers": ["FANUY", "ABBNY", "ISRG"],
                            "sources": ["sec_edgar", "newsapi"]},

    "drones": {"id": 5, "name": "Drones & Aerial Robotics", "category": "ai_robotics",
               "keywords": ["drone", "UAV", "eVTOL", "DJI", "delivery drone", "BVLOS"],
               "tickers": ["JOBY", "ACHR", "LILM"],
               "sources": ["faa", "sec_edgar", "newsapi"]},

    "ai_agents": {"id": 6, "name": "AI Agent Systems", "category": "ai_robotics",
                  "keywords": ["AI agent", "multi-agent", "autonomous agent", "agentic AI",
                               "CrewAI", "AutoGPT", "LangChain"],
                  "tickers": ["MSFT", "CRM"],
                  "sources": ["arxiv", "sec_edgar", "newsapi"]},

    # Healthcare & Bio (6)
    "healthcare_ai": {"id": 7, "name": "Healthcare AI", "category": "health_bio",
                      "keywords": ["AI healthcare", "medical AI", "diagnostic AI", "radiology AI",
                                   "digital health", "clinical AI"],
                      "tickers": ["GEHC", "PHG", "TEM"],
                      "sources": ["pubmed", "openfda", "clinicaltrials", "who_gho", "sec_edgar"]},

    "medical_devices": {"id": 8, "name": "Medical Devices", "category": "health_bio",
                        "keywords": ["medical device", "SaMD", "FDA 510k", "surgical robot",
                                     "wearable", "implant"],
                        "tickers": ["MDT", "SYK", "ABT", "BSX"],
                        "sources": ["openfda", "clinicaltrials", "sec_edgar", "patentsview"]},

    "biotech_genomics": {"id": 9, "name": "Biotechnology & Genomics", "category": "health_bio",
                         "keywords": ["biotech", "genomics", "CRISPR", "gene therapy",
                                      "sequencing", "NGS"],
                         "tickers": ["ILMN", "CRSP", "NTLA", "TXG"],
                         "sources": ["pubmed", "ncbi", "clinicaltrials", "sec_edgar"]},

    "pharma_ai": {"id": 10, "name": "Pharmaceutical AI", "category": "health_bio",
                  "keywords": ["AI drug discovery", "computational biology", "molecular design",
                               "clinical trial AI", "pharma AI"],
                  "tickers": ["RXRX", "EXAI", "SDGR"],
                  "sources": ["pubmed", "clinicaltrials", "pubchem", "sec_edgar"]},

    "telemedicine": {"id": 11, "name": "Telemedicine & Digital Health", "category": "health_bio",
                     "keywords": ["telemedicine", "telehealth", "remote patient monitoring",
                                  "digital therapeutics", "virtual care"],
                     "tickers": ["TDOC", "AMWL", "LVGO"],
                     "sources": ["clinicaltrials", "cms", "who_gho", "sec_edgar"]},

    "bioinformatics": {"id": 12, "name": "Bioinformatics", "category": "health_bio",
                       "keywords": ["bioinformatics", "computational biology", "proteomics",
                                    "metabolomics", "systems biology"],
                       "tickers": ["QGEN", "BRNGF"],
                       "sources": ["pubmed", "ncbi", "ensembl", "uniprot"]},

    # Cyber & Defense (6)
    "cybersecurity_ai": {"id": 13, "name": "Cybersecurity AI", "category": "cyber_defense",
                         "keywords": ["AI cybersecurity", "XDR", "threat detection",
                                      "security AI", "SOAR", "UEBA"],
                         "tickers": ["PANW", "CRWD", "FTNT", "ZS", "CYBR"],
                         "sources": ["cisa_kev", "nvd", "mitre_attack", "sec_edgar"]},

    "defense_military_ai": {"id": 14, "name": "Defense & Military AI", "category": "cyber_defense",
                            "keywords": ["military AI", "defense technology", "autonomous weapon",
                                         "battlefield AI", "Palantir"],
                            "tickers": ["PLTR", "LMT", "RTX", "NOC", "BA"],
                            "sources": ["sipri", "sec_edgar", "gdelt", "newsapi"]},

    "surveillance_ai": {"id": 15, "name": "Surveillance & Public Safety AI", "category": "cyber_defense",
                        "keywords": ["surveillance AI", "facial recognition", "smart city",
                                     "predictive policing", "video analytics"],
                        "tickers": ["GENETEC", "NEC"],
                        "sources": ["gdelt", "newsapi"]},

    "space_technology": {"id": 16, "name": "Space Technology", "category": "cyber_defense",
                         "keywords": ["space technology", "satellite", "launch", "Starlink",
                                      "SpaceX", "orbital"],
                         "tickers": ["SPCE", "RKLB", "ASTS"],
                         "sources": ["sec_edgar", "newsapi", "patentsview"]},

    "critical_infrastructure": {"id": 17, "name": "Critical Infrastructure Protection", "category": "cyber_defense",
                                "keywords": ["critical infrastructure", "NIS2", "operational technology",
                                             "industrial control", "SCADA"],
                                "tickers": ["PANW", "CRWD"],
                                "sources": ["cisa_kev", "nvd", "enisa", "newsapi"]},

    "ai_governance": {"id": 18, "name": "AI Governance & Safety", "category": "cyber_defense",
                      "keywords": ["AI governance", "AI safety", "AI regulation", "EU AI Act",
                                   "NIST AI RMF", "algorithmic accountability"],
                      "tickers": ["MSFT", "GOOGL"],
                      "sources": ["eurostat", "oecd", "newsapi", "gdelt"]},

    # Finance (6)
    "ai_banking": {"id": 19, "name": "AI in Banking", "category": "finance",
                   "keywords": ["AI banking", "fraud detection", "credit scoring AI",
                                "robo-advisor", "digital banking"],
                   "tickers": ["JPM", "BAC", "GS", "WFC", "C"],
                   "sources": ["sec_edgar", "fred", "alpha_vantage", "newsapi"]},

    "insurtech": {"id": 20, "name": "InsurTech & AI Insurance", "category": "finance",
                  "keywords": ["InsurTech", "AI insurance", "parametric insurance",
                               "embedded insurance", "usage-based insurance"],
                  "tickers": ["LMND", "ROOT", "PGR"],
                  "sources": ["sec_edgar", "naic", "newsapi"]},

    "cryptocurrency": {"id": 21, "name": "Cryptocurrency & Digital Assets", "category": "finance",
                       "keywords": ["cryptocurrency", "Bitcoin", "Ethereum", "DeFi",
                                    "stablecoin", "CBDC", "MiCA"],
                       "tickers": ["COIN", "MSTR", "HOOD"],
                       "sources": ["coingecko", "defillama", "sec_edgar", "newsapi"]},

    "algo_trading": {"id": 22, "name": "Algorithmic Trading", "category": "finance",
                     "keywords": ["algorithmic trading", "HFT", "quantitative trading",
                                  "market making", "systematic trading"],
                     "tickers": ["VIRT", "MKTX", "IBKR"],
                     "sources": ["alpha_vantage", "polygon", "sec_edgar"]},

    "regtech": {"id": 23, "name": "RegTech", "category": "finance",
                "keywords": ["RegTech", "compliance technology", "AML", "KYC",
                             "transaction monitoring", "regulatory reporting"],
                "tickers": ["NICE", "WTKWY"],
                "sources": ["ofac", "sanctions", "sec_edgar", "newsapi"]},

    "fintech_payments": {"id": 24, "name": "Payment Systems & Fintech", "category": "finance",
                         "keywords": ["fintech", "digital payments", "open banking",
                                      "real-time payments", "digital wallet"],
                         "tickers": ["V", "MA", "PYPL", "SQ"],
                         "sources": ["sec_edgar", "fred", "bis", "newsapi"]},

    # Telecom & Quantum (6)
    "telecom_5g_6g": {"id": 25, "name": "Telecom & 5G/6G", "category": "telecom_quantum",
                      "keywords": ["5G", "6G", "Open RAN", "AI-RAN", "network slicing",
                                   "telecommunications"],
                      "tickers": ["T", "VZ", "TMUS", "ERIC", "NOK"],
                      "sources": ["fcc", "sec_edgar", "patentsview", "newsapi"]},

    "iot": {"id": 26, "name": "Internet of Things", "category": "telecom_quantum",
            "keywords": ["IoT", "Internet of Things", "smart device", "sensor",
                         "edge computing", "IIoT"],
            "tickers": ["CSCO", "HON", "AMZN"],
            "sources": ["sec_edgar", "newsapi", "patentsview"]},

    "quantum_computing": {"id": 27, "name": "Quantum Computing", "category": "telecom_quantum",
                          "keywords": ["quantum computing", "quantum computer", "qubit",
                                       "quantum algorithm", "post-quantum cryptography"],
                          "tickers": ["IBM", "IONQ", "RGTI", "QBTS"],
                          "sources": ["arxiv", "nist", "sec_edgar", "patentsview"]},

    "cloud_edge_ai": {"id": 28, "name": "Cloud Computing & Edge AI", "category": "telecom_quantum",
                      "keywords": ["cloud computing", "edge AI", "serverless", "multi-cloud",
                                   "sovereign cloud", "hybrid cloud"],
                      "tickers": ["AMZN", "MSFT", "GOOGL", "ORCL", "IBM"],
                      "sources": ["sec_edgar", "newsapi"]},

    "semiconductor": {"id": 29, "name": "Semiconductor & Chip Design AI", "category": "telecom_quantum",
                      "keywords": ["semiconductor", "chip design", "RISC-V", "foundry",
                                   "CHIPS Act", "TSMC"],
                      "tickers": ["NVDA", "TSM", "INTC", "AMD", "AVGO", "QCOM"],
                      "sources": ["sec_edgar", "newsapi", "patentsview", "un_comtrade"]},

    "data_centers": {"id": 30, "name": "Data Centers & Compute", "category": "telecom_quantum",
                     "keywords": ["data center", "compute infrastructure", "HPC",
                                  "liquid cooling", "AI supercomputer"],
                     "tickers": ["DLR", "EQIX", "AMZN", "MSFT"],
                     "sources": ["sec_edgar", "newsapi"]},

    # Legal, Education & Other (12+)
    "legaltech": {"id": 31, "name": "LegalTech & AI Law", "category": "legal_edu",
                  "keywords": ["LegalTech", "AI law", "legal AI", "contract analysis",
                               "e-discovery", "Harvey AI"],
                  "tickers": ["TRI", "RELX"],
                  "sources": ["courtlistener", "eurostat", "newsapi"]},

    "edtech": {"id": 32, "name": "Education AI (EdTech)", "category": "legal_edu",
               "keywords": ["EdTech", "AI education", "adaptive learning",
                            "AI tutor", "learning management"],
               "tickers": ["DUOL", "COUR"],
               "sources": ["oecd_education", "newsapi"]},

    "transport_logistics": {"id": 33, "name": "Transport & Logistics AI", "category": "legal_edu",
                            "keywords": ["logistics AI", "supply chain AI", "autonomous truck",
                                         "route optimization", "warehouse automation"],
                            "tickers": ["UBER", "LYFT"],
                            "sources": ["usdot", "sec_edgar", "newsapi"]},

    "retail_ecommerce": {"id": 34, "name": "Retail & E-commerce AI", "category": "legal_edu",
                         "keywords": ["retail AI", "e-commerce AI", "recommendation engine",
                                      "demand forecasting", "visual search"],
                         "tickers": ["AMZN", "SHOP", "EBAY"],
                         "sources": ["sec_edgar", "newsapi"]},

    "gaming_ai": {"id": 35, "name": "Gaming AI", "category": "gaming_media",
                  "keywords": ["AI gaming", "NPC AI", "procedural generation",
                               "anti-cheat", "game AI"],
                  "tickers": ["TTWO", "EA", "RBLX", "U"],
                  "sources": ["steam", "newsapi", "sec_edgar"]},

    "vr_ar": {"id": 36, "name": "VR/AR", "category": "gaming_media",
              "keywords": ["VR", "AR", "mixed reality", "spatial computing",
                           "Meta Quest", "Vision Pro"],
              "tickers": ["META", "AAPL", "SNAP"],
              "sources": ["steam_hw", "sec_edgar", "newsapi"]},

    "social_media": {"id": 37, "name": "Social Media & Content Platforms", "category": "gaming_media",
                     "keywords": ["social media AI", "content moderation", "algorithmic recommendation",
                                  "short video", "creator economy"],
                     "tickers": ["META", "SNAP", "PINS"],
                     "sources": ["reddit", "newsapi", "gdelt"]},

    "streaming": {"id": 38, "name": "Streaming & Entertainment AI", "category": "gaming_media",
                  "keywords": ["streaming AI", "content recommendation", "synthetic media",
                               "AI music", "virtual influencer"],
                  "tickers": ["NFLX", "DIS", "SPOT"],
                  "sources": ["youtube", "spotify", "newsapi"]},

    "esports": {"id": 39, "name": "E-sports", "category": "gaming_media",
                "keywords": ["esports", "competitive gaming", "game streaming",
                             "tournament", "gaming broadcast"],
                "tickers": ["ATVI", "EA"],
                "sources": ["twitch", "newsapi"]},

    "virtual_economies": {"id": 40, "name": "Virtual Economies & Metaverse", "category": "gaming_media",
                          "keywords": ["metaverse", "virtual economy", "digital twin",
                                       "virtual world", "digital asset"],
                          "tickers": ["META", "RBLX", "U"],
                          "sources": ["sec_edgar", "newsapi"]},

    "energy_ai": {"id": 41, "name": "Energy & Cleantech AI", "category": "legal_edu",
                  "keywords": ["energy AI", "smart grid", "renewable energy",
                               "battery optimization", "carbon capture"],
                  "tickers": ["TSLA", "ENPH", "SEDG"],
                  "sources": ["eia", "sec_edgar", "newsapi"]},

    "agriculture_ai": {"id": 42, "name": "Agriculture AI", "category": "legal_edu",
                       "keywords": ["agriculture AI", "precision farming", "crop monitoring",
                                    "agritech", "livestock AI"],
                       "tickers": ["DE", "CAT"],
                       "sources": ["usda", "newsapi"]},

    "real_estate_proptech": {"id": 43, "name": "Real Estate & PropTech", "category": "legal_edu",
                             "keywords": ["PropTech", "real estate AI", "smart building",
                                          "property technology", "construction AI"],
                             "tickers": ["Z", "RDFN", "OPEN"],
                             "sources": ["fred", "sec_edgar", "newsapi"]},

    "creative_ai": {"id": 44, "name": "Creative AI", "category": "gaming_media",
                    "keywords": ["generative AI", "AI art", "AI music",
                                 "AI writing", "synthetic media"],
                    "tickers": ["ADBE", "META"],
                    "sources": ["arxiv", "newsapi"]},

    "climate_ai": {"id": 45, "name": "Climate & Environmental AI", "category": "legal_edu",
                   "keywords": ["climate AI", "environmental AI", "weather prediction",
                                "disaster response", "sustainability AI"],
                   "tickers": ["BIPC"],
                   "sources": ["noaa", "worldbank", "newsapi"]},

    "public_sector_ai": {"id": 46, "name": "Public Sector AI", "category": "legal_edu",
                         "keywords": ["government AI", "smart city AI", "public service AI",
                                      "civic technology", "administrative AI"],
                         "tickers": ["PLTR", "IBM"],
                         "sources": ["worldbank", "oecd", "newsapi"]},

    "ethics_fairness_ai": {"id": 47, "name": "AI Ethics & Fairness", "category": "cyber_defense",
                           "keywords": ["AI ethics", "algorithmic fairness", "bias mitigation",
                                        "responsible AI", "AI accountability"],
                           "tickers": ["MSFT", "GOOGL"],
                           "sources": ["arxiv", "oecd", "newsapi"]},
}

# =============================================================================
# SETUP LOGGING
# =============================================================================

def setup_logging(log_dir: str) -> logging.Logger:
    """Configure logging to file and console."""
    Path(log_dir).mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(log_dir, f"meok_scraper_{timestamp}.log")

    logger = logging.getLogger("meok_scraper")
    logger.setLevel(logging.INFO)
    logger.handlers = []

    # File handler
    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.INFO)
    fh.setFormatter(logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
    ))
    logger.addHandler(fh)

    # Console handler
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    ch.setFormatter(logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(message)s"
    ))
    logger.addHandler(ch)

    return logger


# =============================================================================
# HTTP SESSION WITH RETRY LOGIC
# =============================================================================

class RateLimiter:
    """Simple token-bucket rate limiter."""

    def __init__(self, max_requests: int, per_seconds: float = 60.0):
        self.max_requests = max_requests
        self.per_seconds = per_seconds
        self.tokens = max_requests
        self.last_update = time.time()
        self._lock = False

    def acquire(self):
        """Block until a token is available."""
        while True:
            now = time.time()
            elapsed = now - self.last_update
            self.tokens = min(self.max_requests,
                              self.tokens + elapsed * (self.max_requests / self.per_seconds))
            self.last_update = now
            if self.tokens >= 1:
                self.tokens -= 1
                return
            sleep_time = (1 - self.tokens) * (self.per_seconds / self.max_requests)
            time.sleep(max(0.01, sleep_time))


def create_session() -> requests.Session:
    """Create a requests session with retry logic."""
    session = requests.Session()
    retry = Retry(
        total=CONFIG["MAX_RETRIES"],
        backoff_factor=CONFIG["BACKOFF_FACTOR"],
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET", "POST"]
    )
    adapter = HTTPAdapter(max_retries=retry, pool_connections=10, pool_maxsize=20)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


# =============================================================================
# DATA SOURCE CLASSES
# =============================================================================

@dataclass
class ScrapedData:
    """Container for scraped data with metadata."""
    source: str
    industry: str
    category: str
    data: List[Dict[str, Any]]
    fetched_at: str
    record_count: int
    file_path: str
    status: str  # "success", "partial", "failed"
    error: Optional[str] = None


class BaseDataSource:
    """Base class for all data sources."""

    def __init__(self, session: requests.Session, logger: logging.Logger):
        self.session = session
        self.logger = logger
        self.rate_limiters: Dict[str, RateLimiter] = {}
        self._setup_rate_limiters()

    def _setup_rate_limiters(self):
        for source, rpm in CONFIG["RATE_LIMITS"].items():
            self.rate_limiters[source] = RateLimiter(rpm)

    def _get(self, url: str, source_key: str = "default",
             headers: Optional[Dict] = None, params: Optional[Dict] = None,
             timeout: int = None) -> requests.Response:
        """Make a rate-limited GET request."""
        self.rate_limiters.get(source_key, self.rate_limiters["default"]).acquire()
        timeout = timeout or CONFIG["REQUEST_TIMEOUT"]
        resp = self.session.get(url, headers=headers, params=params, timeout=timeout)
        resp.raise_for_status()
        return resp

    def _post(self, url: str, source_key: str = "default",
              headers: Optional[Dict] = None, data: Optional[Dict] = None,
              json_data: Optional[Dict] = None,
              timeout: int = None) -> requests.Response:
        """Make a rate-limited POST request."""
        self.rate_limiters.get(source_key, self.rate_limiters["default"]).acquire()
        timeout = timeout or CONFIG["REQUEST_TIMEOUT"]
        resp = self.session.post(url, headers=headers, data=data, json=json_data, timeout=timeout)
        resp.raise_for_status()
        return resp

    def save_data(self, data: List[Dict], source: str, industry: str,
                  category: str, output_dir: str) -> str:
        """Save data to JSON file."""
        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_industry = industry.replace(" ", "_").lower()
        safe_source = source.replace(" ", "_").lower()
        filename = f"{safe_source}_{safe_industry}_{now}.json"

        out_path = Path(output_dir) / category / safe_industry
        out_path.mkdir(parents=True, exist_ok=True)

        file_path = out_path / filename
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False, default=str)

        self.logger.info(f"Saved {len(data)} records to {file_path}")
        return str(file_path)

    def save_csv(self, data: List[Dict], source: str, industry: str,
                 category: str, output_dir: str) -> str:
        """Save data to CSV file."""
        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_industry = industry.replace(" ", "_").lower()
        safe_source = source.replace(" ", "_").lower()
        filename = f"{safe_source}_{safe_industry}_{now}.csv"

        out_path = Path(output_dir) / category / safe_industry
        out_path.mkdir(parents=True, exist_ok=True)

        file_path = out_path / filename
        if data:
            df = pd.DataFrame(data)
            df.to_csv(file_path, index=False, encoding="utf-8")
            self.logger.info(f"Saved {len(data)} records to {file_path}")
        return str(file_path)


# =============================================================================
# INDIVIDUAL DATA SOURCE IMPLEMENTATIONS
# =============================================================================

class CISA_KEV_Source(BaseDataSource):
    """CISA Known Exploited Vulnerabilities Catalog"""

    def fetch(self, **kwargs) -> ScrapedData:
        industry = kwargs.get("industry", "cybersecurity_ai")
        info = INDUSTRIES.get(industry, {})
        try:
            self.logger.info("Fetching CISA KEV catalog...")
            url = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"
            resp = self._get(url, source_key="cisa_kev")
            data = resp.json().get("vulnerabilities", [])
            file_path = self.save_data(data, "cisa_kev", info.get("name", "cybersecurity"),
                                       "cyber_defense", kwargs.get("output_dir", CONFIG["OUTPUT_DIR"]))
            return ScrapedData("cisa_kev", info.get("name", ""), "cyber_defense",
                               data, datetime.now().isoformat(), len(data), file_path, "success")
        except Exception as e:
            self.logger.error(f"CISA KEV error: {e}")
            return ScrapedData("cisa_kev", info.get("name", ""), "cyber_defense",
                               [], datetime.now().isoformat(), 0, "", "failed", str(e))


class NVD_Source(BaseDataSource):
    """National Vulnerability Database"""

    def fetch(self, **kwargs) -> ScrapedData:
        industry = kwargs.get("industry", "cybersecurity_ai")
        info = INDUSTRIES.get(industry, {})
        limit = kwargs.get("limit", 100)
        api_key = CONFIG["NVD_API_KEY"]
        try:
            self.logger.info("Fetching NVD CVEs...")
            headers = {"apiKey": api_key} if api_key else {}
            source_key = "nvd_with_key" if api_key else "nvd"
            url = "https://services.nvd.nist.gov/rest/json/cves/2.0"
            params = {"resultsPerPage": min(limit, 2000), "startIndex": 0}
            resp = self._get(url, source_key="nvd", headers=headers, params=params)
            data = resp.json().get("vulnerabilities", [])
            file_path = self.save_data(data, "nvd", info.get("name", "cybersecurity"),
                                       "cyber_defense", kwargs.get("output_dir", CONFIG["OUTPUT_DIR"]))
            return ScrapedData("nvd", info.get("name", ""), "cyber_defense",
                               data, datetime.now().isoformat(), len(data), file_path, "success")
        except Exception as e:
            self.logger.error(f"NVD error: {e}")
            return ScrapedData("nvd", info.get("name", ""), "cyber_defense",
                               [], datetime.now().isoformat(), 0, "", "failed", str(e))


class SEC_EDGAR_Source(BaseDataSource):
    """SEC EDGAR Filings"""

    def fetch(self, **kwargs) -> ScrapedData:
        industry = kwargs.get("industry", "ai_ml")
        info = INDUSTRIES.get(industry, {})
        tickers = kwargs.get("tickers", info.get("tickers", []))
        try:
            self.logger.info(f"Fetching SEC EDGAR for tickers: {tickers}")
            headers = {"User-Agent": CONFIG["SEC_USER_AGENT"]}
            all_data = []

            # Fetch CIK-to-ticker map
            resp = self._get("https://www.sec.gov/files/company_tickers.json",
                             source_key="sec_edgar", headers=headers)
            ticker_map = {v["ticker"]: v["cik_str"] for v in resp.json().values()}

            for ticker in tickers[:5]:  # Limit to 5 per run
                cik = ticker_map.get(ticker)
                if not cik:
                    continue
                cik_padded = str(cik).zfill(10)
                sub_url = f"https://data.sec.gov/submissions/CIK{cik_padded}.json"
                try:
                    sub_resp = self._get(sub_url, source_key="sec_edgar", headers=headers)
                    sub_data = sub_resp.json()
                    sub_data["ticker"] = ticker
                    all_data.append(sub_data)
                except Exception as te:
                    self.logger.warning(f"SEC fetch error for {ticker}: {te}")
                time.sleep(0.2)  # SEC rate limit

            file_path = self.save_data(all_data, "sec_edgar", info.get("name", ""),
                                       info.get("category", "general"),
                                       kwargs.get("output_dir", CONFIG["OUTPUT_DIR"]))
            return ScrapedData("sec_edgar", info.get("name", ""), info.get("category", ""),
                               all_data, datetime.now().isoformat(), len(all_data), file_path, "success")
        except Exception as e:
            self.logger.error(f"SEC EDGAR error: {e}")
            return ScrapedData("sec_edgar", info.get("name", ""), info.get("category", ""),
                               [], datetime.now().isoformat(), 0, "", "failed", str(e))


class FRED_Source(BaseDataSource):
    """Federal Reserve Economic Data"""

    KEY_SERIES = {
        "DFF": "Federal Funds Rate",
        "GDP": "Gross Domestic Product",
        "CPIAUCSL": "Consumer Price Index",
        "UNRATE": "Unemployment Rate",
        "DJIA": "Dow Jones Industrial Average",
        "SP500": "S&P 500",
        "VIXCLS": "CBOE Volatility Index",
        "T10Y2Y": "Treasury Yield Spread (10Y-2Y)",
        "BAMLH0A0HYM2": "High Yield Spread",
        "DGS10": "10-Year Treasury Rate",
    }

    def fetch(self, **kwargs) -> ScrapedData:
        industry = kwargs.get("industry", "ai_banking")
        info = INDUSTRIES.get(industry, {})
        api_key = CONFIG["FRED_API_KEY"]
        if not api_key:
            self.logger.warning("FRED_API_KEY not set. Skipping FRED.")
            return ScrapedData("fred", info.get("name", ""), info.get("category", ""),
                               [], datetime.now().isoformat(), 0, "", "failed", "No API key")

        try:
            self.logger.info("Fetching FRED economic series...")
            all_data = []
            start = (datetime.now() - timedelta(days=365*2)).strftime("%Y-%m-%d")

            for series_id, name in self.KEY_SERIES.items():
                try:
                    url = "https://api.stlouisfed.org/fred/series/observations"
                    params = {"series_id": series_id, "api_key": api_key,
                              "file_type": "json", "observation_start": start}
                    resp = self._get(url, source_key="fred", params=params)
                    observations = resp.json().get("observations", [])
                    for obs in observations:
                        obs["series_id"] = series_id
                        obs["series_name"] = name
                    all_data.extend(observations)
                except Exception as se:
                    self.logger.warning(f"FRED series {series_id} error: {se}")

            file_path = self.save_csv(all_data, "fred", info.get("name", ""),
                                      info.get("category", "finance"),
                                      kwargs.get("output_dir", CONFIG["OUTPUT_DIR"]))
            return ScrapedData("fred", info.get("name", ""), info.get("category", ""),
                               all_data, datetime.now().isoformat(), len(all_data), file_path, "success")
        except Exception as e:
            self.logger.error(f"FRED error: {e}")
            return ScrapedData("fred", info.get("name", ""), info.get("category", ""),
                               [], datetime.now().isoformat(), 0, "", "failed", str(e))


class OpenFDA_Source(BaseDataSource):
    """openFDA API"""

    def fetch(self, **kwargs) -> ScrapedData:
        industry = kwargs.get("industry", "healthcare_ai")
        info = INDUSTRIES.get(industry, {})
        endpoint = kwargs.get("endpoint", "510k")
        limit = kwargs.get("limit", 100)

        endpoints = {
            "510k": "device/510k",
            "recall": "food/enforcement",
            "adverse": "device/event",
            "drug_label": "drug/label",
        }
        try:
            self.logger.info(f"Fetching openFDA: {endpoint}...")
            ep = endpoints.get(endpoint, "device/510k")
            url = f"https://api.fda.gov/{ep}.json"
            params = {"limit": limit}
            resp = self._get(url, source_key="openfda", params=params)
            data = resp.json().get("results", [resp.json()])
            file_path = self.save_data(data, f"openfda_{endpoint}", info.get("name", ""),
                                       info.get("category", "health_bio"),
                                       kwargs.get("output_dir", CONFIG["OUTPUT_DIR"]))
            return ScrapedData(f"openfda_{endpoint}", info.get("name", ""), info.get("category", ""),
                               data, datetime.now().isoformat(), len(data), file_path, "success")
        except Exception as e:
            self.logger.error(f"openFDA error: {e}")
            return ScrapedData(f"openfda_{endpoint}", info.get("name", ""), info.get("category", ""),
                               [], datetime.now().isoformat(), 0, "", "failed", str(e))


class ClinicalTrials_Source(BaseDataSource):
    """ClinicalTrials.gov API v2"""

    def fetch(self, **kwargs) -> ScrapedData:
        industry = kwargs.get("industry", "healthcare_ai")
        info = INDUSTRIES.get(industry, {})
        condition = kwargs.get("condition", "")
        keywords = info.get("keywords", [])
        if condition:
            query = condition
        elif keywords:
            query = keywords[0]
        else:
            query = "artificial intelligence"

        try:
            self.logger.info(f"Fetching ClinicalTrials.gov for: {query}")
            url = "https://clinicaltrials.gov/api/v2/studies"
            params = {
                "query.term": query,
                "pageSize": 100,
                "filter.overallStatus": "RECRUITING"
            }
            resp = self._get(url, source_key="clinicaltrials", params=params)
            data = resp.json().get("studies", [])
            file_path = self.save_data(data, "clinicaltrials", info.get("name", ""),
                                       info.get("category", "health_bio"),
                                       kwargs.get("output_dir", CONFIG["OUTPUT_DIR"]))
            return ScrapedData("clinicaltrials", info.get("name", ""), info.get("category", ""),
                               data, datetime.now().isoformat(), len(data), file_path, "success")
        except Exception as e:
            self.logger.error(f"ClinicalTrials.gov error: {e}")
            return ScrapedData("clinicaltrials", info.get("name", ""), info.get("category", ""),
                               [], datetime.now().isoformat(), 0, "", "failed", str(e))


class PubMed_Source(BaseDataSource):
    """PubMed/NCBI E-utilities"""

    def fetch(self, **kwargs) -> ScrapedData:
        industry = kwargs.get("industry", "ai_ml")
        info = INDUSTRIES.get(industry, {})
        query = kwargs.get("query", "")
        keywords = info.get("keywords", [])
        if not query and keywords:
            query = " OR ".join(keywords[:3])
        if not query:
            query = "artificial intelligence"

        limit = kwargs.get("limit", 100)

        try:
            self.logger.info(f"Fetching PubMed for: {query}")
            # Search
            search_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
            search_params = {"db": "pubmed", "term": query, "retmax": limit, "retmode": "json"}
            resp = self._get(search_url, source_key="pubmed", params=search_params)
            idlist = resp.json()["esearchresult"]["idlist"]

            if idlist:
                # Fetch summaries
                summary_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
                sum_params = {"db": "pubmed", "id": ",".join(idlist), "retmode": "json"}
                sum_resp = self._get(summary_url, source_key="pubmed", params=sum_params)
                summaries = sum_resp.json().get("result", {})
                data = [v for k, v in summaries.items() if k != "uids"]
            else:
                data = []

            file_path = self.save_data(data, "pubmed", info.get("name", ""),
                                       info.get("category", "general"),
                                       kwargs.get("output_dir", CONFIG["OUTPUT_DIR"]))
            return ScrapedData("pubmed", info.get("name", ""), info.get("category", ""),
                               data, datetime.now().isoformat(), len(data), file_path, "success")
        except Exception as e:
            self.logger.error(f"PubMed error: {e}")
            return ScrapedData("pubmed", info.get("name", ""), info.get("category", ""),
                               [], datetime.now().isoformat(), 0, "", "failed", str(e))


class ArXiv_Source(BaseDataSource):
    """arXiv API"""

    def fetch(self, **kwargs) -> ScrapedData:
        industry = kwargs.get("industry", "ai_ml")
        info = INDUSTRIES.get(industry, {})
        query = kwargs.get("query", "")
        keywords = info.get("keywords", [])
        if not query and keywords:
            query = " OR ".join(keywords[:3])
        if not query:
            query = "artificial intelligence"

        limit = min(kwargs.get("limit", 100), 1000)

        try:
            self.logger.info(f"Fetching arXiv for: {query}")
            url = "http://export.arxiv.org/api/query"
            params = {
                "search_query": f"all:{query}",
                "start": 0, "max_results": limit,
                "sortBy": "submittedDate", "sortOrder": "descending"
            }
            resp = self._get(url, source_key="arxiv", params=params, timeout=60)
            # Parse Atom XML
            import xml.etree.ElementTree as ET
            root = ET.fromstring(resp.text)
            ns = {"atom": "http://www.w3.org/2005/Atom"}
            entries = root.findall("atom:entry", ns)
            data = []
            for entry in entries:
                item = {
                    "title": entry.findtext("atom:title", "", ns),
                    "summary": entry.findtext("atom:summary", "", ns),
                    "published": entry.findtext("atom:published", "", ns),
                    "updated": entry.findtext("atom:updated", "", ns),
                    "id": entry.findtext("atom:id", "", ns),
                    "authors": [a.findtext("atom:name", "", ns)
                               for a in entry.findall("atom:author", ns)],
                    "primary_category": entry.find("atom:category") is not None and
                                       entry.find("atom:category").get("term", "") or "",
                }
                data.append(item)

            file_path = self.save_data(data, "arxiv", info.get("name", ""),
                                       info.get("category", "general"),
                                       kwargs.get("output_dir", CONFIG["OUTPUT_DIR"]))
            return ScrapedData("arxiv", info.get("name", ""), info.get("category", ""),
                               data, datetime.now().isoformat(), len(data), file_path, "success")
        except Exception as e:
            self.logger.error(f"arXiv error: {e}")
            return ScrapedData("arxiv", info.get("name", ""), info.get("category", ""),
                               [], datetime.now().isoformat(), 0, "", "failed", str(e))


class WorldBank_Source(BaseDataSource):
    """World Bank Open Data API"""

    KEY_INDICATORS = [
        "NY.GDP.MKTP.CD",       # GDP
        "SP.POP.TOTL",          # Population
        "NE.TRD.GNFS.ZS",       # Trade % GDP
        "IT.NET.USER.ZS",       # Internet users
        "GB.XPD.RSDV.GD.ZS",    # R&D % GDP
        "IP.JRN.ARTC.SC",       # Journal articles
        "SL.UEM.TOTL.ZS",       # Unemployment
        "SI.POV.GINI",          # Gini index
    ]

    def fetch(self, **kwargs) -> ScrapedData:
        industry = kwargs.get("industry", "ai_governance")
        info = INDUSTRIES.get(industry, {})
        try:
            self.logger.info("Fetching World Bank indicators...")
            all_data = []
            for indicator in self.KEY_INDICATORS:
                try:
                    url = f"https://api.worldbank.org/v2/country/all/indicator/{indicator}"
                    params = {"date": "2020:2025", "format": "json", "per_page": 1000}
                    resp = self._get(url, source_key="worldbank", params=params)
                    result = resp.json()
                    if len(result) > 1 and result[1]:
                        for item in result[1]:
                            item["indicator_code"] = indicator
                        all_data.extend(result[1])
                except Exception as ie:
                    self.logger.warning(f"World Bank indicator {indicator} error: {ie}")

            file_path = self.save_csv(all_data, "worldbank", info.get("name", ""),
                                      info.get("category", "general"),
                                      kwargs.get("output_dir", CONFIG["OUTPUT_DIR"]))
            return ScrapedData("worldbank", info.get("name", ""), info.get("category", ""),
                               all_data, datetime.now().isoformat(), len(all_data), file_path, "success")
        except Exception as e:
            self.logger.error(f"World Bank error: {e}")
            return ScrapedData("worldbank", info.get("name", ""), info.get("category", ""),
                               [], datetime.now().isoformat(), 0, "", "failed", str(e))


class IMFWEO_Source(BaseDataSource):
    """IMF World Economic Outlook Data"""

    def fetch(self, **kwargs) -> ScrapedData:
        industry = kwargs.get("industry", "ai_governance")
        info = INDUSTRIES.get(industry, {})
        try:
            self.logger.info("Fetching IMF WEO data...")
            url = "https://www.imf.org/external/datamapper/api/v1/NGDP_RPCH"
            resp = self._get(url, source_key="imf")
            data = resp.json()
            # Parse nested structure
            records = []
            for country, values in data.get("values", {}).items():
                for year, val in values.items():
                    records.append({"country": country, "year": year,
                                    "real_gdp_growth": val, "indicator": "NGDP_RPCH"})

            file_path = self.save_csv(records, "imf_weo", info.get("name", ""),
                                      info.get("category", "general"),
                                      kwargs.get("output_dir", CONFIG["OUTPUT_DIR"]))
            return ScrapedData("imf_weo", info.get("name", ""), info.get("category", ""),
                               records, datetime.now().isoformat(), len(records), file_path, "success")
        except Exception as e:
            self.logger.error(f"IMF error: {e}")
            return ScrapedData("imf_weo", info.get("name", ""), info.get("category", ""),
                               [], datetime.now().isoformat(), 0, "", "failed", str(e))


class CoinGecko_Source(BaseDataSource):
    """CoinGecko API"""

    def fetch(self, **kwargs) -> ScrapedData:
        industry = kwargs.get("industry", "cryptocurrency")
        info = INDUSTRIES.get(industry, {})
        per_page = kwargs.get("per_page", 100)
        try:
            self.logger.info("Fetching CoinGecko crypto data...")
            url = "https://api.coingecko.com/api/v3/coins/markets"
            params = {
                "vs_currency": "usd", "order": "market_cap_desc",
                "per_page": per_page, "page": 1, "sparkline": "false"
            }
            resp = self._get(url, source_key="coingecko", params=params)
            data = resp.json()
            file_path = self.save_csv(data, "coingecko", info.get("name", ""),
                                      info.get("category", "finance"),
                                      kwargs.get("output_dir", CONFIG["OUTPUT_DIR"]))
            return ScrapedData("coingecko", info.get("name", ""), info.get("category", ""),
                               data, datetime.now().isoformat(), len(data), file_path, "success")
        except Exception as e:
            self.logger.error(f"CoinGecko error: {e}")
            return ScrapedData("coingecko", info.get("name", ""), info.get("category", ""),
                               [], datetime.now().isoformat(), 0, "", "failed", str(e))


class DeFiLlama_Source(BaseDataSource):
    """DeFi Llama API"""

    def fetch(self, **kwargs) -> ScrapedData:
        industry = kwargs.get("industry", "cryptocurrency")
        info = INDUSTRIES.get(industry, {})
        try:
            self.logger.info("Fetching DeFi Llama TVL data...")
            resp = self._get("https://api.llama.fi/protocols", source_key="defillama")
            data = resp.json()
            file_path = self.save_csv(data, "defillama", info.get("name", ""),
                                      info.get("category", "finance"),
                                      kwargs.get("output_dir", CONFIG["OUTPUT_DIR"]))
            return ScrapedData("defillama", info.get("name", ""), info.get("category", ""),
                               data, datetime.now().isoformat(), len(data), file_path, "success")
        except Exception as e:
            self.logger.error(f"DeFi Llama error: {e}")
            return ScrapedData("defillama", info.get("name", ""), info.get("category", ""),
                               [], datetime.now().isoformat(), 0, "", "failed", str(e))


class MITRE_ATTACK_Source(BaseDataSource):
    """MITRE ATT&CK Framework"""

    def fetch(self, **kwargs) -> ScrapedData:
        industry = kwargs.get("industry", "cybersecurity_ai")
        info = INDUSTRIES.get(industry, {})
        try:
            self.logger.info("Fetching MITRE ATT&CK...")
            url = "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/enterprise-attack/enterprise-attack.json"
            resp = self._get(url, source_key="mitre_attack", timeout=120)
            data = resp.json().get("objects", [])
            file_path = self.save_data(data, "mitre_attack", info.get("name", ""),
                                       info.get("category", "cyber_defense"),
                                       kwargs.get("output_dir", CONFIG["OUTPUT_DIR"]))
            return ScrapedData("mitre_attack", info.get("name", ""), info.get("category", ""),
                               data, datetime.now().isoformat(), len(data), file_path, "success")
        except Exception as e:
            self.logger.error(f"MITRE ATT&CK error: {e}")
            return ScrapedData("mitre_attack", info.get("name", ""), info.get("category", ""),
                               [], datetime.now().isoformat(), 0, "", "failed", str(e))


class SIPRI_Source(BaseDataSource):
    """SIPRI Military Expenditure Data"""

    def fetch(self, **kwargs) -> ScrapedData:
        industry = kwargs.get("industry", "defense_military_ai")
        info = INDUSTRIES.get(industry, {})
        try:
            self.logger.info("Fetching SIPRI military expenditure data...")
            url = "https://sipri.org/sites/default/files/SIPRI-Milex-data-1949-2023.xlsx"
            resp = self._get(url, source_key="sipri", timeout=120)
            # Save binary file
            out_path = Path(kwargs.get("output_dir", CONFIG["OUTPUT_DIR"])) / "cyber_defense" / "sipri"
            out_path.mkdir(parents=True, exist_ok=True)
            file_path = out_path / "sipri_milex.xlsx"
            with open(file_path, "wb") as f:
                f.write(resp.content)
            self.logger.info(f"SIPRI data saved to {file_path}")
            return ScrapedData("sipri", info.get("name", ""), info.get("category", ""),
                               [{"file": str(file_path)}], datetime.now().isoformat(),
                               1, str(file_path), "success")
        except Exception as e:
            self.logger.error(f"SIPRI error: {e}")
            return ScrapedData("sipri", info.get("name", ""), info.get("category", ""),
                               [], datetime.now().isoformat(), 0, "", "failed", str(e))


class WHO_GHO_Source(BaseDataSource):
    """WHO Global Health Observatory"""

    def fetch(self, **kwargs) -> ScrapedData:
        industry = kwargs.get("industry", "healthcare_ai")
        info = INDUSTRIES.get(industry, {})
        indicator = kwargs.get("indicator", "SDGSUICIDE")
        try:
            self.logger.info(f"Fetching WHO GHO indicator: {indicator}")
            url = f"https://ghoapi.azureedge.net/api/{indicator}"
            resp = self._get(url, source_key="who_gho")
            data = resp.json().get("value", [])
            file_path = self.save_csv(data, "who_gho", info.get("name", ""),
                                      info.get("category", "health_bio"),
                                      kwargs.get("output_dir", CONFIG["OUTPUT_DIR"]))
            return ScrapedData("who_gho", info.get("name", ""), info.get("category", ""),
                               data, datetime.now().isoformat(), len(data), file_path, "success")
        except Exception as e:
            self.logger.error(f"WHO GHO error: {e}")
            return ScrapedData("who_gho", info.get("name", ""), info.get("category", ""),
                               [], datetime.now().isoformat(), 0, "", "failed", str(e))


class PatentsView_Source(BaseDataSource):
    """USPTO PatentsView API"""

    def fetch(self, **kwargs) -> ScrapedData:
        industry = kwargs.get("industry", "ai_ml")
        info = INDUSTRIES.get(industry, {})
        query = kwargs.get("query", "")
        keywords = info.get("keywords", [])
        if not query and keywords:
            query = keywords[0]
        if not query:
            query = "artificial intelligence"

        try:
            self.logger.info(f"Fetching PatentsView for: {query}")
            url = "https://api.patentsview.org/patents/query"
            payload = {
                "q": {"_text_any": {"patent_title": query}},
                "f": ["patent_number", "patent_title", "patent_date",
                      "assignee_organization", "inventor_first_name"],
                "o": {"per_page": 100}
            }
            resp = self._post(url, source_key="patentsview", json_data=payload)
            data = resp.json().get("patents", [])
            file_path = self.save_csv(data, "patentsview", info.get("name", ""),
                                      info.get("category", "general"),
                                      kwargs.get("output_dir", CONFIG["OUTPUT_DIR"]))
            return ScrapedData("patentsview", info.get("name", ""), info.get("category", ""),
                               data, datetime.now().isoformat(), len(data), file_path, "success")
        except Exception as e:
            self.logger.error(f"PatentsView error: {e}")
            return ScrapedData("patentsview", info.get("name", ""), info.get("category", ""),
                               [], datetime.now().isoformat(), 0, "", "failed", str(e))


class NewsAPI_Source(BaseDataSource):
    """NewsAPI"""

    def fetch(self, **kwargs) -> ScrapedData:
        industry = kwargs.get("industry", "ai_ml")
        info = INDUSTRIES.get(industry, {})
        api_key = CONFIG["NEWSAPI_KEY"]
        if not api_key:
            self.logger.warning("NEWSAPI_KEY not set. Skipping NewsAPI.")
            return ScrapedData("newsapi", info.get("name", ""), info.get("category", ""),
                               [], datetime.now().isoformat(), 0, "", "failed", "No API key")

        query = kwargs.get("query", "")
        keywords = info.get("keywords", [])
        if not query and keywords:
            query = " OR ".join(keywords[:2])
        if not query:
            query = "artificial intelligence"

        try:
            self.logger.info(f"Fetching NewsAPI for: {query}")
            url = "https://newsapi.org/v2/everything"
            from_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
            params = {
                "q": query, "from": from_date,
                "sortBy": "publishedAt", "pageSize": 100,
                "apiKey": api_key
            }
            resp = self._get(url, source_key="newsapi", params=params)
            data = resp.json().get("articles", [])
            file_path = self.save_csv(data, "newsapi", info.get("name", ""),
                                      info.get("category", "general"),
                                      kwargs.get("output_dir", CONFIG["OUTPUT_DIR"]))
            return ScrapedData("newsapi", info.get("name", ""), info.get("category", ""),
                               data, datetime.now().isoformat(), len(data), file_path, "success")
        except Exception as e:
            self.logger.error(f"NewsAPI error: {e}")
            return ScrapedData("newsapi", info.get("name", ""), info.get("category", ""),
                               [], datetime.now().isoformat(), 0, "", "failed", str(e))


class GDELT_Source(BaseDataSource):
    """GDELT Project API"""

    def fetch(self, **kwargs) -> ScrapedData:
        industry = kwargs.get("industry", "ai_governance")
        info = INDUSTRIES.get(industry, {})
        query = kwargs.get("query", "")
        keywords = info.get("keywords", [])
        if not query and keywords:
            query = " OR ".join(keywords[:2])
        if not query:
            query = "artificial intelligence"

        try:
            self.logger.info(f"Fetching GDELT for: {query}")
            url = "https://api.gdeltproject.org/api/v2/doc/doc"
            start = (datetime.now() - timedelta(days=7)).strftime("%Y%m%d")
            end = datetime.now().strftime("%Y%m%d")
            params = {
                "query": query, "mode": "ArtList",
                "startdatetime": f"{start}000000",
                "enddatetime": f"{end}235959",
                "format": "json", "maxrecords": 250
            }
            resp = self._get(url, source_key="gdelt", params=params)
            data = resp.json().get("articles", [])
            file_path = self.save_csv(data, "gdelt", info.get("name", ""),
                                      info.get("category", "general"),
                                      kwargs.get("output_dir", CONFIG["OUTPUT_DIR"]))
            return ScrapedData("gdelt", info.get("name", ""), info.get("category", ""),
                               data, datetime.now().isoformat(), len(data), file_path, "success")
        except Exception as e:
            self.logger.error(f"GDELT error: {e}")
            return ScrapedData("gdelt", info.get("name", ""), info.get("category", ""),
                               [], datetime.now().isoformat(), 0, "", "failed", str(e))


class OpenCorporates_Source(BaseDataSource):
    """OpenCorporates API"""

    def fetch(self, **kwargs) -> ScrapedData:
        industry = kwargs.get("industry", "regtech")
        info = INDUSTRIES.get(industry, {})
        company = kwargs.get("company", "")
        keywords = info.get("keywords", [])
        if not company and keywords:
            company = keywords[0]
        if not company:
            company = "artificial intelligence"

        try:
            self.logger.info(f"Fetching OpenCorporates for: {company}")
            url = "https://api.opencorporates.com/v0.4/companies/search"
            params = {"q": company, "per_page": 20}
            resp = self._get(url, source_key="opencorporates", params=params)
            data = resp.json().get("results", {}).get("companies", [])
            file_path = self.save_csv(data, "opencorporates", info.get("name", ""),
                                      info.get("category", "finance"),
                                      kwargs.get("output_dir", CONFIG["OUTPUT_DIR"]))
            return ScrapedData("opencorporates", info.get("name", ""), info.get("category", ""),
                               data, datetime.now().isoformat(), len(data), file_path, "success")
        except Exception as e:
            self.logger.error(f"OpenCorporates error: {e}")
            return ScrapedData("opencorporates", info.get("name", ""), info.get("category", ""),
                               [], datetime.now().isoformat(), 0, "", "failed", str(e))


class NHTSA_Source(BaseDataSource):
    """NHTSA Vehicle Safety Data"""

    def fetch(self, **kwargs) -> ScrapedData:
        industry = kwargs.get("industry", "autonomous_vehicles")
        info = INDUSTRIES.get(industry, {})
        try:
            self.logger.info("Fetching NHTSA recalls...")
            url = "https://api.nhtsa.gov/recalls/recallsByVehicle"
            resp = self._get(url, source_key="nhtsa")
            data = resp.json().get("results", [])
            file_path = self.save_csv(data, "nhtsa", info.get("name", ""),
                                      info.get("category", "ai_robotics"),
                                      kwargs.get("output_dir", CONFIG["OUTPUT_DIR"]))
            return ScrapedData("nhtsa", info.get("name", ""), info.get("category", ""),
                               data, datetime.now().isoformat(), len(data), file_path, "success")
        except Exception as e:
            self.logger.error(f"NHTSA error: {e}")
            return ScrapedData("nhtsa", info.get("name", ""), info.get("category", ""),
                               [], datetime.now().isoformat(), 0, "", "failed", str(e))


class Ensembl_Source(BaseDataSource):
    """Ensembl REST API"""

    def fetch(self, **kwargs) -> ScrapedData:
        industry = kwargs.get("industry", "biotech_genomics")
        info = INDUSTRIES.get(industry, {})
        gene = kwargs.get("gene", "BRCA1")
        species = kwargs.get("species", "homo_sapiens")
        try:
            self.logger.info(f"Fetching Ensembl for gene: {gene}")
            url = f"https://rest.ensembl.org/lookup/symbol/{species}/{gene}"
            headers = {"Content-Type": "application/json"}
            resp = self._get(url, source_key="ensembl", headers=headers)
            data = [resp.json()]
            file_path = self.save_data(data, "ensembl", info.get("name", ""),
                                       info.get("category", "health_bio"),
                                       kwargs.get("output_dir", CONFIG["OUTPUT_DIR"]))
            return ScrapedData("ensembl", info.get("name", ""), info.get("category", ""),
                               data, datetime.now().isoformat(), len(data), file_path, "success")
        except Exception as e:
            self.logger.error(f"Ensembl error: {e}")
            return ScrapedData("ensembl", info.get("name", ""), info.get("category", ""),
                               [], datetime.now().isoformat(), 0, "", "failed", str(e))


class OECD_Education_Source(BaseDataSource):
    """OECD Education Statistics"""

    def fetch(self, **kwargs) -> ScrapedData:
        industry = kwargs.get("industry", "edtech")
        info = INDUSTRIES.get(industry, {})
        try:
            self.logger.info("Fetching OECD education data...")
            url = "https://stats.oecd.org/SDMX-JSON/data/EAG_FIN"
            params = {"startPeriod": "2020", "endPeriod": "2024"}
            resp = self._get(url, source_key="oecd", params=params)
            data = resp.json()
            records = [{"raw": json.dumps(data)}]
            file_path = self.save_data(records, "oecd_education", info.get("name", ""),
                                       info.get("category", "legal_edu"),
                                       kwargs.get("output_dir", CONFIG["OUTPUT_DIR"]))
            return ScrapedData("oecd_education", info.get("name", ""), info.get("category", ""),
                               records, datetime.now().isoformat(), len(records), file_path, "success")
        except Exception as e:
            self.logger.error(f"OECD Education error: {e}")
            return ScrapedData("oecd_education", info.get("name", ""), info.get("category", ""),
                               [], datetime.now().isoformat(), 0, "", "failed", str(e))


class OFAC_Source(BaseDataSource):
    """OFAC Sanctions Data"""

    def fetch(self, **kwargs) -> ScrapedData:
        industry = kwargs.get("industry", "regtech")
        info = INDUSTRIES.get(industry, {})
        try:
            self.logger.info("Fetching OFAC SDN list...")
            url = "https://www.treasury.gov/ofac/downloads/sdn.csv"
            resp = self._get(url, source_key="ofac", timeout=120)
            content = resp.content.decode("latin-1")
            lines = content.strip().split("\n")
            reader = csv.DictReader(lines)
            data = list(reader)[:1000]  # Limit to first 1000 entries
            file_path = self.save_csv(data, "ofac_sdn", info.get("name", ""),
                                      info.get("category", "finance"),
                                      kwargs.get("output_dir", CONFIG["OUTPUT_DIR"]))
            return ScrapedData("ofac_sdn", info.get("name", ""), info.get("category", ""),
                               data, datetime.now().isoformat(), len(data), file_path, "success")
        except Exception as e:
            self.logger.error(f"OFAC error: {e}")
            return ScrapedData("ofac_sdn", info.get("name", ""), info.get("category", ""),
                               [], datetime.now().isoformat(), 0, "", "failed", str(e))


class AlphaVantage_Source(BaseDataSource):
    """Alpha Vantage Stock Data"""

    def fetch(self, **kwargs) -> ScrapedData:
        industry = kwargs.get("industry", "ai_banking")
        info = INDUSTRIES.get(industry, {})
        api_key = CONFIG["ALPHA_VANTAGE_KEY"]
        if not api_key:
            self.logger.warning("ALPHA_VANTAGE_KEY not set. Skipping.")
            return ScrapedData("alpha_vantage", info.get("name", ""), info.get("category", ""),
                               [], datetime.now().isoformat(), 0, "", "failed", "No API key")

        symbol = kwargs.get("symbol", info.get("tickers", ["AAPL"])[0] if info.get("tickers") else "AAPL")
        try:
            self.logger.info(f"Fetching Alpha Vantage for: {symbol}")
            url = "https://www.alphavantage.co/query"
            params = {
                "function": "TIME_SERIES_DAILY",
                "symbol": symbol,
                "apikey": api_key,
                "outputsize": "compact"
            }
            resp = self._get(url, source_key="alpha_vantage", params=params)
            raw_data = resp.json()
            # Parse time series
            ts = raw_data.get("Time Series (Daily)", {})
            records = []
            for date, values in list(ts.items())[:100]:
                records.append({
                    "date": date, "symbol": symbol,
                    "open": values.get("1. open"),
                    "high": values.get("2. high"),
                    "low": values.get("3. low"),
                    "close": values.get("4. close"),
                    "volume": values.get("5. volume")
                })
            file_path = self.save_csv(records, "alpha_vantage", info.get("name", ""),
                                      info.get("category", "finance"),
                                      kwargs.get("output_dir", CONFIG["OUTPUT_DIR"]))
            return ScrapedData("alpha_vantage", info.get("name", ""), info.get("category", ""),
                               records, datetime.now().isoformat(), len(records), file_path, "success")
        except Exception as e:
            self.logger.error(f"Alpha Vantage error: {e}")
            return ScrapedData("alpha_vantage", info.get("name", ""), info.get("category", ""),
                               [], datetime.now().isoformat(), 0, "", "failed", str(e))


class CourtListener_Source(BaseDataSource):
    """CourtListener / Free Law Project"""

    def fetch(self, **kwargs) -> ScrapedData:
        industry = kwargs.get("industry", "legaltech")
        info = INDUSTRIES.get(industry, {})
        query = kwargs.get("query", "artificial intelligence")
        try:
            self.logger.info(f"Fetching CourtListener for: {query}")
            url = "https://www.courtlistener.com/api/rest/v3/opinions/"
            params = {"q": query, "page_size": 20}
            resp = self._get(url, source_key="courtlistener", params=params)
            data = resp.json().get("results", [])
            file_path = self.save_data(data, "courtlistener", info.get("name", ""),
                                       info.get("category", "legal_edu"),
                                       kwargs.get("output_dir", CONFIG["OUTPUT_DIR"]))
            return ScrapedData("courtlistener", info.get("name", ""), info.get("category", ""),
                               data, datetime.now().isoformat(), len(data), file_path, "success")
        except Exception as e:
            self.logger.error(f"CourtListener error: {e}")
            return ScrapedData("courtlistener", info.get("name", ""), info.get("category", ""),
                               [], datetime.now().isoformat(), 0, "", "failed", str(e))


class EU_ODP_Source(BaseDataSource):
    """EU Open Data Portal"""

    def fetch(self, **kwargs) -> ScrapedData:
        industry = kwargs.get("industry", "ai_governance")
        info = INDUSTRIES.get(industry, {})
        query = kwargs.get("query", "artificial intelligence")
        try:
            self.logger.info(f"Fetching EU ODP for: {query}")
            url = "https://data.europa.eu/api/hub/search/datasets/search"
            params = {"query": query, "rows": 20}
            resp = self._get(url, source_key="eu_odp", params=params)
            data = resp.json().get("result", {}).get("results", [])
            file_path = self.save_data(data, "eu_odp", info.get("name", ""),
                                       info.get("category", "general"),
                                       kwargs.get("output_dir", CONFIG["OUTPUT_DIR"]))
            return ScrapedData("eu_odp", info.get("name", ""), info.get("category", ""),
                               data, datetime.now().isoformat(), len(data), file_path, "success")
        except Exception as e:
            self.logger.error(f"EU ODP error: {e}")
            return ScrapedData("eu_odp", info.get("name", ""), info.get("category", ""),
                               [], datetime.now().isoformat(), 0, "", "failed", str(e))


class Reddit_Source(BaseDataSource):
    """Reddit API"""

    def fetch(self, **kwargs) -> ScrapedData:
        industry = kwargs.get("industry", "social_media")
        info = INDUSTRIES.get(industry, {})
        subreddit = kwargs.get("subreddit", "artificial")
        try:
            self.logger.info(f"Fetching Reddit r/{subreddit}...")
            url = f"https://www.reddit.com/r/{subreddit}/hot.json"
            headers = {"User-Agent": "MEOK-Simulation/1.0"}
            params = {"limit": 25}
            resp = self._get(url, source_key="reddit", headers=headers, params=params)
            posts = resp.json().get("data", {}).get("children", [])
            data = [{"title": p["data"].get("title"),
                     "score": p["data"].get("score"),
                     "url": p["data"].get("url"),
                     "created": p["data"].get("created_utc")}
                    for p in posts]
            file_path = self.save_csv(data, "reddit", info.get("name", ""),
                                      info.get("category", "gaming_media"),
                                      kwargs.get("output_dir", CONFIG["OUTPUT_DIR"]))
            return ScrapedData("reddit", info.get("name", ""), info.get("category", ""),
                               data, datetime.now().isoformat(), len(data), file_path, "success")
        except Exception as e:
            self.logger.error(f"Reddit error: {e}")
            return ScrapedData("reddit", info.get("name", ""), info.get("category", ""),
                               [], datetime.now().isoformat(), 0, "", "failed", str(e))


# =============================================================================
# SCRAPER ORCHESTRATOR
# =============================================================================

class MEOKScraper:
    """Main scraper orchestrator for all 47 industries."""

    # Map source names to handler classes
    SOURCE_HANDLERS = {
        "cisa_kev": CISA_KEV_Source,
        "nvd": NVD_Source,
        "sec_edgar": SEC_EDGAR_Source,
        "fred": FRED_Source,
        "openfda": OpenFDA_Source,
        "clinicaltrials": ClinicalTrials_Source,
        "pubmed": PubMed_Source,
        "arxiv": ArXiv_Source,
        "worldbank": WorldBank_Source,
        "imf_weo": IMFWEO_Source,
        "coingecko": CoinGecko_Source,
        "defillama": DeFiLlama_Source,
        "mitre_attack": MITRE_ATTACK_Source,
        "sipri": SIPRI_Source,
        "who_gho": WHO_GHO_Source,
        "patentsview": PatentsView_Source,
        "newsapi": NewsAPI_Source,
        "gdelt": GDELT_Source,
        "opencorporates": OpenCorporates_Source,
        "nhtsa": NHTSA_Source,
        "ensembl": Ensembl_Source,
        "oecd_education": OECD_Education_Source,
        "ofac_sdn": OFAC_Source,
        "alpha_vantage": AlphaVantage_Source,
        "courtlistener": CourtListener_Source,
        "eu_odp": EU_ODP_Source,
        "reddit": Reddit_Source,
    }

    def __init__(self, output_dir: str = None, log_dir: str = None):
        self.output_dir = output_dir or CONFIG["OUTPUT_DIR"]
        self.log_dir = log_dir or CONFIG["LOG_DIR"]
        self.logger = setup_logging(self.log_dir)
        self.session = create_session()
        self.results: List[ScrapedData] = []
        self.state_file = Path(self.output_dir) / CONFIG["STATE_FILE"]
        self.state = self._load_state()

        Path(self.output_dir).mkdir(parents=True, exist_ok=True)
        self.logger.info("=" * 60)
        self.logger.info("MEOK 47-Industry Data Scraper initialized")
        self.logger.info(f"Output directory: {self.output_dir}")
        self.logger.info(f"Industries configured: {len(INDUSTRIES)}")
        self.logger.info("=" * 60)

    def _load_state(self) -> Dict:
        """Load incremental state."""
        if self.state_file.exists():
            try:
                with open(self.state_file) as f:
                    return json.load(f)
            except Exception:
                pass
        return {"last_run": "", "completed_sources": {}}

    def _save_state(self):
        """Save incremental state."""
        self.state["last_run"] = datetime.now().isoformat()
        with open(self.state_file, "w") as f:
            json.dump(self.state, f, indent=2)

    def should_fetch(self, source: str, industry: str, incremental: bool = False) -> bool:
        """Check if source should be fetched in incremental mode."""
        if not incremental:
            return True
        key = f"{source}_{industry}"
        last_fetch = self.state.get("completed_sources", {}).get(key, "")
        if not last_fetch:
            return True
        last_dt = datetime.fromisoformat(last_fetch)
        # Fetch if more than 24 hours old
        return (datetime.now() - last_dt).total_seconds() > 86400

    def mark_fetched(self, source: str, industry: str):
        """Mark a source as fetched."""
        if "completed_sources" not in self.state:
            self.state["completed_sources"] = {}
        self.state["completed_sources"][f"{source}_{industry}"] = datetime.now().isoformat()

    def fetch_source(self, source_name: str, industry_key: str,
                     incremental: bool = False, **kwargs) -> Optional[ScrapedData]:
        """Fetch data from a single source for an industry."""
        handler_class = self.SOURCE_HANDLERS.get(source_name)
        if not handler_class:
            self.logger.warning(f"No handler for source: {source_name}")
            return None

        if not self.should_fetch(source_name, industry_key, incremental):
            self.logger.info(f"Skipping {source_name} for {industry_key} (already recent)")
            return None

        handler = handler_class(self.session, self.logger)
        kwargs["industry"] = industry_key
        kwargs["output_dir"] = self.output_dir

        try:
            self.logger.info(f"Fetching {source_name} for industry: {industry_key}")
            result = handler.fetch(**kwargs)
            self.results.append(result)
            if result.status == "success":
                self.mark_fetched(source_name, industry_key)
                self.logger.info(f"SUCCESS: {source_name} -> {result.record_count} records")
            else:
                self.logger.warning(f"FAILED: {source_name} -> {result.error}")
            return result
        except Exception as e:
            self.logger.error(f"CRITICAL: {source_name} error: {e}")
            traceback.print_exc()
            return None

    def fetch_industry(self, industry_key: str, incremental: bool = False) -> List[ScrapedData]:
        """Fetch all configured sources for an industry."""
        info = INDUSTRIES.get(industry_key)
        if not info:
            self.logger.error(f"Unknown industry: {industry_key}")
            return []

        self.logger.info(f"\n{'='*50}")
        self.logger.info(f"Fetching industry: {info['name']} (ID: {info['id']})")
        self.logger.info(f"Sources: {info.get('sources', [])}")
        self.logger.info(f"{'='*50}")

        results = []
        for source in info.get("sources", []):
            result = self.fetch_source(source, industry_key, incremental)
            if result:
                results.append(result)
            time.sleep(0.5)  # Be nice between sources

        return results

    def fetch_all(self, incremental: bool = False) -> List[ScrapedData]:
        """Fetch data for all 47 industries."""
        self.logger.info("\n" + "=" * 60)
        self.logger.info("STARTING FULL SCRAPE OF ALL 47 INDUSTRIES")
        self.logger.info("=" * 60)

        for industry_key in INDUSTRIES:
            self.fetch_industry(industry_key, incremental)
            time.sleep(1)  # Pause between industries

        self._save_state()
        self._print_summary()
        return self.results

    def fetch_category(self, category: str, incremental: bool = False) -> List[ScrapedData]:
        """Fetch all industries in a category."""
        category_map = {
            "ai_robotics": [k for k, v in INDUSTRIES.items() if v["category"] == "ai_robotics"],
            "health_bio": [k for k, v in INDUSTRIES.items() if v["category"] == "health_bio"],
            "cyber_defense": [k for k, v in INDUSTRIES.items() if v["category"] == "cyber_defense"],
            "finance": [k for k, v in INDUSTRIES.items() if v["category"] == "finance"],
            "telecom_quantum": [k for k, v in INDUSTRIES.items() if v["category"] == "telecom_quantum"],
            "legal_edu": [k for k, v in INDUSTRIES.items() if v["category"] == "legal_edu"],
            "gaming_media": [k for k, v in INDUSTRIES.items() if v["category"] == "gaming_media"],
        }
        keys = category_map.get(category, [])
        for key in keys:
            self.fetch_industry(key, incremental)
        self._save_state()
        return self.results

    def fetch_source_all_industries(self, source_name: str,
                                    incremental: bool = False) -> List[ScrapedData]:
        """Fetch a single source across all relevant industries."""
        for industry_key, info in INDUSTRIES.items():
            if source_name in info.get("sources", []):
                self.fetch_source(source_name, industry_key, incremental)
        self._save_state()
        return self.results

    def _print_summary(self):
        """Print final summary."""
        self.logger.info("\n" + "=" * 60)
        self.logger.info("SCRAPING SUMMARY")
        self.logger.info("=" * 60)

        total_records = sum(r.record_count for r in self.results)
        success = sum(1 for r in self.results if r.status == "success")
        failed = sum(1 for r in self.results if r.status == "failed")

        self.logger.info(f"Total sources queried: {len(self.results)}")
        self.logger.info(f"Successful: {success}")
        self.logger.info(f"Failed: {failed}")
        self.logger.info(f"Total records collected: {total_records:,}")
        self.logger.info(f"Output directory: {self.output_dir}")

        # Per-category summary
        categories = {}
        for r in self.results:
            cat = r.category
            if cat not in categories:
                categories[cat] = {"records": 0, "sources": 0}
            categories[cat]["records"] += r.record_count
            categories[cat]["sources"] += 1

        self.logger.info("\nPer-Category Summary:")
        for cat, stats in sorted(categories.items()):
            self.logger.info(f"  {cat:20s}: {stats['sources']:3d} sources, {stats['records']:10,d} records")

        # Save summary JSON
        summary = {
            "timestamp": datetime.now().isoformat(),
            "total_sources": len(self.results),
            "successful": success,
            "failed": failed,
            "total_records": total_records,
            "per_category": {cat: {"records": s["records"], "sources": s["sources"]}
                             for cat, s in categories.items()},
            "results": [asdict(r) for r in self.results]
        }
        summary_path = Path(self.output_dir) / "scrape_summary.json"
        with open(summary_path, "w") as f:
            json.dump(summary, f, indent=2, default=str)
        self.logger.info(f"\nSummary saved to: {summary_path}")


def list_industries():
    """Print all configured industries."""
    print("\n" + "=" * 70)
    print("MEOK 47-Industry Configuration")
    print("=" * 70)

    categories = {}
    for key, info in INDUSTRIES.items():
        cat = info["category"]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append((key, info))

    for cat, items in sorted(categories.items()):
        print(f"\n--- {cat.upper().replace('_', ' ')} ---")
        for key, info in sorted(items, key=lambda x: x[1]["id"]):
            sources = ", ".join(info.get("sources", [])[:5])
            tickers = ", ".join(info.get("tickers", [])[:3])
            print(f"  {info['id']:2d}. {key:25s} - {info['name'][:40]:40s}")
            print(f"      Sources: {sources}")
            if tickers:
                print(f"      Tickers: {tickers}")

    print(f"\nTotal: {len(INDUSTRIES)} industries configured")
    print("=" * 70)


# =============================================================================
# MAIN ENTRY POINT
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="MEOK 47-Industry Data Scraper",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # List all industries
  python meok_data_scraper.py --list

  # Fetch all data for all industries
  python meok_data_scraper.py --all

  # Fetch specific industries
  python meok_data_scraper.py --industries ai_ml cybersecurity_ai cryptocurrency

  # Fetch by category
  python meok_data_scraper.py --category finance

  # Incremental mode (skip recently fetched data)
  python meok_data_scraper.py --all --incremental

  # Fetch specific source across industries
  python meok_data_scraper.py --source sec_edgar

  # Specify output directory
  python meok_data_scraper.py --all --output ./my_data
        """
    )
    parser.add_argument("--list", action="store_true", help="List all configured industries")
    parser.add_argument("--all", action="store_true", help="Fetch all industries")
    parser.add_argument("--industries", nargs="+", help="Specific industry keys to fetch")
    parser.add_argument("--category", help="Fetch all industries in a category")
    parser.add_argument("--source", help="Fetch specific source across all industries")
    parser.add_argument("--incremental", action="store_true", help="Only fetch new data")
    parser.add_argument("--output", default=CONFIG["OUTPUT_DIR"], help="Output directory")
    parser.add_argument("--log-dir", default=CONFIG["LOG_DIR"], help="Log directory")

    args = parser.parse_args()

    if args.list:
        list_industries()
        return

    scraper = MEOKScraper(output_dir=args.output, log_dir=args.log_dir)

    if args.all:
        scraper.fetch_all(incremental=args.incremental)
    elif args.industries:
        for ind_key in args.industries:
            scraper.fetch_industry(ind_key, incremental=args.incremental)
        scraper._save_state()
        scraper._print_summary()
    elif args.category:
        scraper.fetch_category(args.category, incremental=args.incremental)
    elif args.source:
        scraper.fetch_source_all_industries(args.source, incremental=args.incremental)
    else:
        parser.print_help()
        print("\nUse --list to see all available industries")


if __name__ == "__main__":
    main()
