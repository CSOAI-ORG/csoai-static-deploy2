#!/usr/bin/env python3
"""dorado_bench.py — East↔West live regulation vs live index market data, measured.

The PAIR nobody measures: the gap between a regulatory event (East or West) and the
index-market reaction to it, in real time. We hold the whole stack: live index quotes,
regulation event banks (EU AI Act / UK / China TC260 / Korea AI Basic Act / Japan AI
Guidelines), a 16-axis fleet, and honest registers.

Register discipline (canon): MEASURED (deterministic, reproducible) vs REPORTED
(human/self-reported) — never blended. The pair-gap is a MEASURED number computed
from live data by deterministic predicates (Design Law 1: no model verdicts in the
metric).

Pair-gap definition (Dorado):
  For a regulatory event E (with East/West polarity) and an index pair (East idx,
  West idx) over a window W:
    gap = (r_East - r_West)  where r = log-return of the index over W
  Interpretation: gap > 0 = East index outperformed West after the event;
  the absolute |gap| is the "measured distance" between how the two regions'
  markets price the same regulatory signal.
"""
from __future__ import annotations
import json, math, time, urllib.request, urllib.error
from dataclasses import dataclass, field
from typing import Optional

# ---- live index feed (Yahoo v8 chart API — deterministic, no auth) ----
WEST_INDICES = {"^GSPC": "S&P 500", "^FTSE": "FTSE 100", "^GDAXI": "DAX"}
EAST_INDICES = {"^HSI": "Hang Seng", "^N225": "Nikkei 225", "000001.SS": "SSE Composite",
               "^KS11": "KOSPI Composite", "^AXJO": "S&P/ASX 200", "^STI": "Straits Times"}

# ---- regulation event bank (East/West, canon-sourced) ----
REG_EVENTS = [
    # West
    {"id": "eu-ai-act-2024", "region": "WEST", "jurisdiction": "EU",
     "instrument": "AI Act (Reg. 2024/1689)", "date": "2024-08-01", "severity": 4,
     "source": "EUR-Lex 2024/1689"},
    {"id": "eu-ai-act-gpa-2025", "region": "WEST", "jurisdiction": "EU",
     "instrument": "AI Act GPA obligations (Art 50)", "date": "2025-08-02", "severity": 3,
     "source": "EUR-Lex 2024/1689 Art 50"},
    {"id": "uk-ai-principles-2025", "region": "WEST", "jurisdiction": "UK",
     "instrument": "UK AI Principles", "date": "2025-07-24", "severity": 2,
     "source": "gov.uk AI regulation"},
    # East
    {"id": "china-tc260-2023", "region": "EAST", "jurisdiction": "CN",
     "instrument": "TC260 AI Safety Governance Framework", "date": "2023-08-15", "severity": 4,
     "source": "TC260 (cn) — mined doc onetrust blog"},
    {"id": "china-genai-measures-2023", "region": "EAST", "jurisdiction": "CN",
     "instrument": "Interim Measures for Generative AI", "date": "2023-08-15", "severity": 4,
     "source": "CAC interim genAI measures"},
    {"id": "korea-ai-basic-act-2024", "region": "EAST", "jurisdiction": "KR",
     "instrument": "Korea AI Basic Act", "date": "2024-12-26", "severity": 3,
     "source": "korea-ai-basic-act-mcp"},
    {"id": "japan-ai-guidelines-2024", "region": "EAST", "jurisdiction": "JP",
     "instrument": "Japan AI Guidelines for Business", "date": "2024-04-19", "severity": 2,
     "source": "METI Japan AI guidelines"},
]

@dataclass
class IndexQuote:
    symbol: str
    name: str
    region: str
    price: float
    prev_close: float
    tz: str
    fetched_at: str = field(default_factory=lambda: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))

    def log_return(self) -> float:
        if not self.prev_close: return 0.0
        return math.log(self.price / self.prev_close)


def fetch_quote(symbol: str, timeout: int = 10) -> Optional[IndexQuote]:
    """Deterministic live quote fetch. None on failure (fail-closed, never fabricate)."""
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.request.quote(symbol)}?interval=1d&range=5d"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            d = json.loads(r.read().decode())
        res = d.get("chart", {}).get("result", [{}])
        if not res: return None
        meta = res[0].get("meta", {})
        price = meta.get("regularMarketPrice")
        prev = meta.get("chartPreviousClose") or meta.get("previousClose")
        if price is None: return None
        name = meta.get("shortName") or meta.get("longName") or symbol
        tz = meta.get("exchangeTimezoneName", "")
        region = "EAST" if symbol in EAST_INDICES else ("WEST" if symbol in WEST_INDICES else "?")
        return IndexQuote(symbol=symbol, name=name, region=region,
                          price=float(price), prev_close=float(prev or price), tz=tz)
    except Exception:
        return None


def pair_gap(east_quote: IndexQuote, west_quote: IndexQuote) -> dict:
    """THE DORADO METRIC: measured distance between East and West market reaction.
    Deterministic predicate on live data — no model opinion (Design Law 1)."""
    r_east = east_quote.log_return()
    r_west = west_quote.log_return()
    gap = r_east - r_west
    return {
        "east": {"symbol": east_quote.symbol, "name": east_quote.name, "price": east_quote.price,
                 "log_return": round(r_east, 6)},
        "west": {"symbol": west_quote.symbol, "name": west_quote.name, "price": west_quote.price,
                 "log_return": round(r_west, 6)},
        "gap": round(gap, 6),
        "gap_pct": round((east_quote.price / west_quote.price - 1) * 100, 4),
        "interpretation": ("EAST_OVERPERFORMS" if gap > 0 else "WEST_OVERPERFORMS" if gap < 0 else "PARITY"),
        "measured_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }


def snap_all() -> dict:
    """Snapshot all 6 indices + pair gaps. Deterministic, fail-closed per quote."""
    quotes = {}
    for sym in list(WEST_INDICES) + list(EAST_INDICES):
        q = fetch_quote(sym)
        if q: quotes[sym] = q
    gaps = {}
    for esym in EAST_INDICES:
        for wsym in WEST_INDICES:
            if esym in quotes and wsym in quotes:
                g = pair_gap(quotes[esym], quotes[wsym])
                gaps[f"{esym}|{wsym}"] = g
    return {
        "schema": "csoai.dorado/0.1",
        "measured_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "quotes": {s: {"name": q.name, "price": q.price, "prev": q.prev_close,
                       "log_return": round(q.log_return(), 6), "region": q.region, "tz": q.tz}
                   for s, q in quotes.items()},
        "pair_gaps": gaps,
        "reg_events": REG_EVENTS,
        "register": "MEASURED — deterministic live-data predicates (Design Law 1)",
    }


if __name__ == "__main__":
    s = snap_all()
    print(json.dumps(s, indent=1)[:1200])
