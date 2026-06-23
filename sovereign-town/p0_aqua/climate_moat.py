#!/usr/bin/env python3
"""
climate_moat.py — turn public NOAA global temperature anomalies into Sovereign Town signals.

Fetches annual global land+ocean temperature departures from NOAA Climate at a Glance.
Computes long-term warming trend and recent anomaly to derive climate-pressure indices
that influence agriculture, aqua, and resource scarcity in the simulation.

Sources from the CSOAI Free Data Catalog; no API keys required.
"""
from __future__ import annotations
import json
import logging
import urllib.request
from pathlib import Path
from statistics import linear_regression, StatisticsError

import moat_common

logger = logging.getLogger(__name__)

OUT = Path(__file__).parent
MOAT_PATH = OUT / "climate_moat.json"

NOAA_ANNUAL_URL = (
    "https://www.ncei.noaa.gov/access/monitoring/climate-at-a-glance/"
    "global/time-series/globe/land_ocean/ytd/12/1880-2024.json"
)

CLIMATE_HIVES = [
    "koikeeper",
    "fishkeeper",
    "agriculture",
    "loopfactory",
    "councilof",
]


def fetch_noaa(url: str, timeout: int = 60, retries: int = 2) -> dict:
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    last_err = None
    for _ in range(retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return json.loads(r.read().decode("utf-8", errors="replace"))
        except (urllib.error.URLError, urllib.error.HTTPError, OSError, TimeoutError, json.JSONDecodeError) as e:
            last_err = e
    raise RuntimeError(f"Failed to fetch NOAA data: {last_err}")


def process_noaa(data: dict) -> dict:
    raw = data.get("data", {})
    annual: dict[int, float] = {}
    for year_str, info in raw.items():
        try:
            year = int(year_str)
            departure = info.get("departure") if isinstance(info, dict) else info
            if departure is None:
                continue
            annual[year] = float(departure)
        except (ValueError, TypeError):
            continue

    if not annual:
        raise RuntimeError("No annual temperature anomalies parsed")

    sorted_years = sorted(annual.items())
    latest_year, latest_anomaly = sorted_years[-1]

    # Trend over the last 50 years of data (slope in °C per decade).
    recent = [(y, a) for y, a in sorted_years if y >= latest_year - 50]
    slope_per_decade = 0.0
    if len(recent) >= 10:
        xs = [float(y) for y, _ in recent]
        ys = [a for _, a in recent]
        try:
            reg = linear_regression(xs, ys)
            slope_per_decade = reg.slope * 10.0
        except (ValueError, TypeError, StatisticsError):
            pass

    # Climate pressure: combine recent anomaly and warming trend, normalized 0..1.
    # Typical anomaly range -0.5 to +1.5; typical trend 0 to 0.3 °C/decade.
    anomaly_component = max(0.0, min(1.0, (latest_anomaly + 0.5) / 1.5))
    trend_component = max(0.0, min(1.0, slope_per_decade / 0.25))
    climate_pressure = round(0.6 * anomaly_component + 0.4 * trend_component, 3)

    return {
        "source": "NOAA Climate at a Glance — Global Land and Ocean Temperature Anomalies",
        "url": NOAA_ANNUAL_URL,
        "base_period": data.get("description", {}).get("base_period", "1901-2000"),
        "units": data.get("description", {}).get("units", "Degrees Celsius"),
        "latest_year": latest_year,
        "latest_anomaly_c": round(latest_anomaly, 3),
        "warmest_year": max(annual, key=annual.get),
        "warmest_anomaly_c": round(annual[max(annual, key=annual.get)], 3),
        "trend_per_decade_c": round(slope_per_decade, 4),
        "observations": len(annual),
        "indices": {
            "climate_pressure": climate_pressure,
            "anomaly_component": round(anomaly_component, 3),
            "trend_component": round(trend_component, 3),
        },
    }


def build_moat() -> dict:
    data = fetch_noaa(NOAA_ANNUAL_URL)
    summary = process_noaa(data)
    climate_pressure = summary["indices"]["climate_pressure"]

    moat = {
        "derived_from": {
            "sources": ["NOAA Climate at a Glance"],
            "catalog_ref": "~/Downloads/csoai_free_data_catalog.md",
            "note": "Public global temperature anomaly data only. No individual weather station records emitted.",
        },
        "climate_summary": summary,
        "indices": {
            "climate_pressure": climate_pressure,
        },
        "sim_params": {
            # Climate pressure increases scarcity (water/food stress) and baseline fragility.
            "scarcity_food_mult": round(3.2 + 1.5 * climate_pressure, 3),
            "baseline_lawlessness": round(0.02 + 0.05 * climate_pressure, 3),
            "contagion_step_boost": round(1.0 + 0.3 * climate_pressure, 3),
        },
        "hives": CLIMATE_HIVES,
    }
    if not moat_common.save_json(MOAT_PATH, moat):
        raise RuntimeError(f"Failed to write {MOAT_PATH}")
    return moat


def load_moat(default=None):
    """Load the cached climate moat JSON."""
    return moat_common.load_moat("climate", default=default)


if __name__ == "__main__":
    moat = build_moat()
    summary = moat["climate_summary"]
    print(f"  CLIMATE MOAT — NOAA {summary['observations']} years -> {MOAT_PATH}")
    print(f"  latest_year={summary['latest_year']} anomaly={summary['latest_anomaly_c']}°C "
          f"trend={summary['trend_per_decade_c']}°C/decade climate_pressure={moat['indices']['climate_pressure']}")
