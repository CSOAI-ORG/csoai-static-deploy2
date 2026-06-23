#!/usr/bin/env python3
"""
finance_moat.py — turn public US financial/economic indicators into Sovereign Town pressure signals.

Reads the St. Louis Fed FRED public CSV endpoints (no API key required) for a
small basket of macro series, computes growth, stress, and stability indices,
and maps them onto finance-relevant hives.

Sources from the CSOAI Free Data Catalog; no API keys required.
"""
from __future__ import annotations
import csv
import io
import json
import logging
import urllib.request
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from statistics import mean, stdev

import moat_common

logger = logging.getLogger(__name__)

OUT = Path(__file__).parent
MOAT_PATH = OUT / "finance_moat.json"

FRED_BASE = "https://fred.stlouisfed.org/graph/fredgraph.csv?id="

SERIES = {
    "GDP": {"label": "Gross Domestic Product", "freq": "quarterly", "unit": "Billions USD"},
    "UNRATE": {"label": "Unemployment Rate", "freq": "monthly", "unit": "%"},
    "CPIAUCSL": {"label": "Consumer Price Index", "freq": "monthly", "unit": "Index"},
    "VIXCLS": {"label": "CBOE Volatility Index", "freq": "daily", "unit": "Index"},
    "T10Y2Y": {"label": "10Y minus 2Y Treasury Spread", "freq": "daily", "unit": "%"},
    "DGS10": {"label": "10-Year Treasury Yield", "freq": "daily", "unit": "%"},
    "FEDFUNDS": {"label": "Federal Funds Effective Rate", "freq": "monthly", "unit": "%"},
}

FINANCE_HIVES = [
    "loopfactory",
    "commercialvehicle",
    "councilof",
    "accountabilityof",
    "dataprivacyof",
    "landlaw",
]


def fetch_series(series_id: str, timeout: int = 45, retries: int = 2) -> list[tuple[str, float | None]]:
    url = f"{FRED_BASE}{series_id}"
    # FRED blocks some User-Agent strings; send only Accept.
    req = urllib.request.Request(url, headers={"Accept": "text/csv"})
    out: list[tuple[str, float | None]] = []
    last_err = None
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                text = r.read().decode("utf-8", errors="replace")
            reader = csv.reader(io.StringIO(text))
            header = next(reader, None)
            if not header or len(header) < 2:
                return out
            for row in reader:
                if len(row) < 2:
                    continue
                date_str, val_str = row[0], row[1]
                if val_str in (".", "", "NaN"):
                    out.append((date_str, None))
                else:
                    try:
                        out.append((date_str, float(val_str)))
                    except ValueError:
                        out.append((date_str, None))
            return out
        except (urllib.error.URLError, urllib.error.HTTPError, OSError, TimeoutError) as e:
            last_err = e
    # Fail-open: return empty list so the moat can still build with defaults.
    logger.warning("FRED %s fetch failed: %s", series_id, last_err)
    return out


def _latest(values: list[tuple[str, float | None]]) -> tuple[str, float] | None:
    for date_str, val in reversed(values):
        if val is not None:
            return date_str, val
    return None


def _year_ago(values: list[tuple[str, float | None]]) -> tuple[str, float] | None:
    """Return the point closest to but not newer than 365 days before latest."""
    latest = _latest(values)
    if not latest:
        return None
    latest_dt = datetime.strptime(latest[0], "%Y-%m-%d")
    target = latest_dt.replace(year=latest_dt.year - 1)
    best = None
    best_diff = None
    for date_str, val in values:
        if val is None:
            continue
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        if dt > target:
            continue
        diff = (target - dt).days
        if best_diff is None or diff < best_diff:
            best_diff = diff
            best = (date_str, val)
    return best


def _yoy_change(values: list[tuple[str, float | None]]) -> float | None:
    latest = _latest(values)
    ago = _year_ago(values)
    if not latest or not ago or ago[1] == 0:
        return None
    return (latest[1] - ago[1]) / abs(ago[1])


def _volatility(values: list[tuple[str, float | None]], years: int = 5) -> float | None:
    """Std-dev of YoY log changes over the last N years of observations."""
    numeric = [(d, v) for d, v in values if v is not None]
    if len(numeric) < years + 2:
        return None
    numeric.sort(key=lambda x: x[0])
    # Use annual sampling: one point per calendar year (latest available)
    by_year: dict[int, float] = {}
    for date_str, val in numeric:
        year = int(date_str[:4])
        by_year[year] = val
    years_sorted = sorted(by_year.items())[-(years + 1):]
    if len(years_sorted) < 3:
        return None
    changes = []
    for i in range(1, len(years_sorted)):
        prev, cur = years_sorted[i - 1][1], years_sorted[i][1]
        if prev > 0:
            changes.append((cur - prev) / prev)
    if len(changes) < 2:
        return None
    return stdev(changes) if len(changes) > 1 else 0.0


def process_series(series_id: str, meta: dict) -> dict:
    values = fetch_series(series_id)
    latest = _latest(values)
    yoy = _yoy_change(values)
    vol = _volatility(values)
    return {
        "series_id": series_id,
        "label": meta["label"],
        "freq": meta["freq"],
        "unit": meta["unit"],
        "latest": {"date": latest[0] if latest else None, "value": latest[1] if latest else None},
        "yoy_change": round(yoy, 4) if yoy is not None else None,
        "volatility_5y": round(vol, 4) if vol is not None else None,
        "observations": len([v for _, v in values if v is not None]),
    }


def build_moat() -> dict:
    series_data = {sid: process_series(sid, meta) for sid, meta in SERIES.items()}

    gdp = series_data["GDP"]
    unrate = series_data["UNRATE"]
    cpi = series_data["CPIAUCSL"]
    vix = series_data["VIXCLS"]
    t10y2y = series_data["T10Y2Y"]
    dgs10 = series_data["DGS10"]
    fedfunds = series_data["FEDFUNDS"]

    # Stress index: high unemployment, high VIX, inverted yield curve, high fed funds.
    stress_components = []
    if unrate["latest"]["value"] is not None:
        # normalize unemployment 0..1 around 0-10%
        stress_components.append(min(1.0, unrate["latest"]["value"] / 10.0))
    if vix["latest"]["value"] is not None:
        # VIX 0..1 around 0-40
        stress_components.append(min(1.0, vix["latest"]["value"] / 40.0))
    if t10y2y["latest"]["value"] is not None:
        # inverted curve adds stress (0..1 when -2% to +2%)
        stress_components.append(max(0.0, min(1.0, (-t10y2y["latest"]["value"] + 2.0) / 4.0)))
    if fedfunds["latest"]["value"] is not None:
        # high rates add stress 0..1 around 0-6%
        stress_components.append(min(1.0, fedfunds["latest"]["value"] / 6.0))

    financial_stress = round(mean(stress_components), 3) if stress_components else 0.0

    # Inflation pressure: CPI YoY normalized 0..1 around 0-10%
    inflation_pressure = 0.0
    if cpi["yoy_change"] is not None:
        inflation_pressure = min(1.0, max(0.0, cpi["yoy_change"] / 0.10))
    inflation_pressure = round(inflation_pressure, 3)

    # Growth health: GDP YoY normalized -1..1; positive is healthy
    growth_health = 0.0
    if gdp["yoy_change"] is not None:
        growth_health = max(-1.0, min(1.0, gdp["yoy_change"] / 0.05))
    growth_health = round(growth_health, 3)

    # Economic stability: combines growth and low volatility
    stability = round(0.5 * (1.0 + growth_health) - 0.3 * financial_stress, 3)

    moat = {
        "derived_from": {
            "sources": ["FRED — Federal Reserve Economic Data"],
            "catalog_ref": "~/Downloads/csoai_free_data_catalog.md",
            "note": "Public US macroeconomic time series only. No proprietary data.",
        },
        "series": series_data,
        "indices": {
            "financial_stress": financial_stress,
            "inflation_pressure": inflation_pressure,
            "growth_health": growth_health,
            "economic_stability": stability,
        },
        "sim_params": {
            # High financial stress -> higher baseline lawlessness and contagion sensitivity.
            "baseline_lawlessness": round(0.02 + 0.12 * financial_stress, 3),
            "contagion_step_boost": round(1.0 + 0.6 * financial_stress, 3),
            "scarcity_food_mult": round(3.2 + 1.5 * inflation_pressure, 3),
        },
        "hives": FINANCE_HIVES,
    }
    if not moat_common.save_json(MOAT_PATH, moat):
        raise RuntimeError(f"Failed to write {MOAT_PATH}")
    return moat


def load_moat(default=None):
    """Load the cached finance moat JSON."""
    return moat_common.load_moat("finance", default=default)


if __name__ == "__main__":
    moat = build_moat()
    idx = moat["indices"]
    print(f"  FINANCE MOAT — FRED {len(moat['series'])} series -> {MOAT_PATH}")
    print(f"  financial_stress={idx['financial_stress']} inflation_pressure={idx['inflation_pressure']} growth_health={idx['growth_health']}")
    for sid, s in moat["series"].items():
        print(f"    {sid}: latest={s['latest']['value']} ({s['latest']['date']}) yoy={s['yoy_change']}")
