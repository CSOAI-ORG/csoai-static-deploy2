#!/usr/bin/env python3
"""
data_moat.py — turn the hive's real-world data collection into Sovereign Town parameters.

Reads public EU datasets from ~/clawd/eu_data/ and derives a small set of
jurisdiction / simulation indices.  The output (data_moat.json) is consumed by
jurisdiction.py (regime strength) and sim.py (scarcity/contagion pressure).

No personal data is used.  Only aggregate EU27 economic indicators.
"""
from __future__ import annotations
import json
import logging
import os
import statistics
from pathlib import Path

import moat_common

logger = logging.getLogger(__name__)

OUT = os.path.dirname(os.path.abspath(__file__))
EU_DATA_DIR = Path(OUT).parent.parent / "eu_data"
OUT_FILE = Path(OUT) / "data_moat.json"


def _dim_index(value_idx: int, dim_order: list, dim_sizes: dict, target_dim: str) -> int:
    """Return the category index for `target_dim` at flattened position `value_idx`."""
    stride = 1
    for d in reversed(dim_order):
        if d == target_dim:
            return (value_idx // stride) % dim_sizes[d]
        stride *= dim_sizes[d]
    raise KeyError(target_dim)


def _parse_eurostat(path: Path):
    """Parse Eurostat SDMX-like JSON and return EU27_2020 time series {year: value}."""
    try:
        with open(path, encoding="utf-8") as f:
            payload = json.load(f)
    except (OSError, json.JSONDecodeError, ValueError) as e:
        logger.warning("Failed to parse Eurostat file %s: %s", path, e)
        return {"error": str(e)}

    data = payload.get("data", {})
    dims = data.get("dimension", {})
    if not dims:
        return {"error": "no dimensions"}

    dim_order = list(dims.keys())
    dim_sizes = {d: len(dims[d]["category"]["index"]) for d in dim_order}

    # Find EU27_2020 geo index
    geo_idx = None
    if "geo" in dims:
        for cat, idx in dims["geo"]["category"]["index"].items():
            if cat in ("EU27_2020", "EU"):
                geo_idx = idx
                break

    # Map time index -> year label
    time_map = {}
    if "time" in dims:
        time_map = {v: k for k, v in dims["time"]["category"]["index"].items()}

    values = data.get("value", {})
    series = {}
    for raw_idx, val in values.items():
        idx = int(raw_idx)
        if geo_idx is not None and _dim_index(idx, dim_order, dim_sizes, "geo") != geo_idx:
            continue
        if "time" in dims:
            tidx = _dim_index(idx, dim_order, dim_sizes, "time")
            year = time_map.get(tidx)
            if year and isinstance(val, (int, float)):
                series[year] = float(val)
        else:
            if isinstance(val, (int, float)):
                series[str(idx)] = float(val)

    # Sort by year and return latest + average of last 5 available years
    sorted_items = sorted(series.items(), key=lambda x: x[0])
    latest = sorted_items[-1] if sorted_items else (None, None)
    recent = [v for _, v in sorted_items[-5:]]
    return {
        "label": payload.get("label") or data.get("label"),
        "latest_year": latest[0],
        "latest_value": latest[1],
        "recent_5yr_avg": round(statistics.mean(recent), 2) if recent else None,
        "series": sorted_items,
    }


def _clamp(v, lo=0.0, hi=1.0):
    return max(lo, min(hi, v))


def build_moat():
    datasets = {}
    for path in sorted(EU_DATA_DIR.glob("*.json")):
        if path.name == "manifest.json":
            continue
        key = path.stem
        datasets[key] = _parse_eurostat(path)

    # Employment rate (EU27, % of population 20-64 employed)
    emp = datasets.get("eurostat_employment_tesem010", {})
    employment_rate = emp.get("recent_5yr_avg") or 70.0

    # GDP per capita in PPS (EU27 = 100)
    gdp = datasets.get("eurostat_gdp_tec00114", {})
    gdp_per_capita = gdp.get("recent_5yr_avg") or 100.0

    # Population on 1 January (actual persons; convert to thousands)
    pop = datasets.get("eurostat_population_tps00001", {})
    population_thousands = (pop.get("latest_value") or 450000000) / 1000.0

    # Energy balance — gross inland consumption in ktoe
    nrg = datasets.get("eurostat_energy_balance_nrg_bal_s?freq=A&nrg_bal=G3000&unit=KTOE&geo=EU27_2020", {})
    energy_ktoe = nrg.get("latest_value") or 1300000

    # Normalize into simulation indices (0..1, higher = more pressure / more strength)
    # EU employment ~70% historically; 75% = very resilient
    resilience_index = _clamp((employment_rate - 60) / 20)
    # GDP per capita PPS: 80 = weak, 120 = strong
    prosperity_index = _clamp((gdp_per_capita - 80) / 40)
    # Energy consumption per capita (toe/person) as proxy for supply-chain stress.
    # ktoe / population_in_thousands == toe per person because 1 ktoe = 1000 toe and pop is in 1000s.
    energy_per_capita = energy_ktoe / population_thousands if population_thousands else 3.0
    scarcity_pressure = _clamp((energy_per_capita - 1.5) / 3.0)

    # Composite: high prosperity + high resilience = lower scarcity shock amplification
    economic_stability = _clamp((resilience_index + prosperity_index) / 2)

    moat = {
        "derived_from": {
            "eu_data_dir": str(EU_DATA_DIR),
            "datasets": list(datasets.keys()),
            "note": "Aggregate EU27 indicators only. No personal data.",
        },
        "raw": {
            "employment_rate": round(employment_rate, 2),
            "gdp_per_capita_pps": round(gdp_per_capita, 2),
            "population_thousands": round(population_thousands, 1),
            "energy_gross_inland_ktoe": round(energy_ktoe, 1),
            "energy_per_capita_ktoe": round(energy_per_capita, 4),
        },
        "indices": {
            "eu_resilience_index": round(resilience_index, 3),
            "eu_prosperity_index": round(prosperity_index, 3),
            "eu_scarcity_pressure": round(scarcity_pressure, 3),
            "eu_economic_stability": round(economic_stability, 3),
        },
        "sim_params": {
            # Higher economic stability -> smaller scarcity food-price spike
            "scarcity_food_mult": round(3.2 - 1.2 * economic_stability, 3),
            # Higher energy dependence / scarcity pressure -> higher contagion step
            "contagion_step": round(0.03 + 0.06 * scarcity_pressure, 3),
            # Strong EU regime anchored to real economic resilience
            "eu_regime_enforcement": round(0.85 + 0.15 * resilience_index, 3),
        },
        "jurisdiction_regimes": {
            "EU  — AI Act + DORA (data-grounded)": round(0.85 + 0.15 * resilience_index, 3),
            "US  — NIST RMF (risk-based)": 0.70,
            "UK  — light-touch / sandbox": 0.40,
            "—   — ungoverned (no regime)": 0.00,
        },
        "datasets_detail": datasets,
    }

    if not moat_common.save_json(OUT_FILE, moat):
        raise RuntimeError(f"Failed to write {OUT_FILE}")
    return moat


def load_moat(default=None):
    """Load the cached data moat JSON."""
    return moat_common.load_moat("data", default=default)


if __name__ == "__main__":
    moat = build_moat()
    print(f"  DATA MOAT — derived {len(moat['derived_from']['datasets'])} EU datasets -> {OUT_FILE}")
    print("  " + "-" * 60)
    for k, v in moat["indices"].items():
        print(f"  {k:<30} {v}")
    print("  " + "-" * 60)
    for k, v in moat["sim_params"].items():
        print(f"  {k:<30} {v}")
