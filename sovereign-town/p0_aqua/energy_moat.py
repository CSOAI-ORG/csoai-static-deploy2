#!/usr/bin/env python3
"""
energy_moat.py — turn public US energy price series into Sovereign Town pressure signals.

Reads energy-relevant FRED CSV endpoints (no API key required) for crude oil, natural
gas, gasoline, and electricity prices. Computes an energy-stress index that influences
scarcity, contagion, and baseline lawlessness in the simulation.

Sources from the CSOAI Free Data Catalog; no API keys required.
"""
from __future__ import annotations
import csv
import io
import json
import logging
import urllib.request
from datetime import datetime
from pathlib import Path

import moat_common

logger = logging.getLogger(__name__)

OUT = Path(__file__).parent
MOAT_PATH = OUT / "energy_moat.json"

FRED_BASE = "https://fred.stlouisfed.org/graph/fredgraph.csv?id="

SERIES = {
    "DCOILWTICO": {"label": "Crude Oil (WTI)", "unit": "USD per barrel"},
    "DHHNGSP": {"label": "Natural Gas (Henry Hub)", "unit": "USD per MMBtu"},
    "GASREGM": {"label": "US Regular Gasoline", "unit": "USD per gallon"},
    "CUSR0000SETB01": {"label": "Electricity CPI", "unit": "Index"},
}

ENERGY_HIVES = [
    "loopfactory",
    "commercialvehicle",
    "muckaway",
    "councilof",
    "agriculture",
]


def fetch_series(series_id: str, timeout: int = 45, retries: int = 2) -> list[tuple[str, float | None]]:
    url = f"{FRED_BASE}{series_id}"
    req = urllib.request.Request(url, headers={"Accept": "text/csv"})
    out: list[tuple[str, float | None]] = []
    last_err = None
    for _ in range(retries + 1):
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
    logger.warning("FRED %s fetch failed: %s", series_id, last_err)
    return out


def _latest(values: list[tuple[str, float | None]]) -> tuple[str, float] | None:
    for date_str, val in reversed(values):
        if val is not None:
            return date_str, val
    return None


def _year_ago(values: list[tuple[str, float | None]]) -> tuple[str, float] | None:
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


def process_series(series_id: str, meta: dict) -> dict:
    values = fetch_series(series_id)
    latest = _latest(values)
    yoy = _yoy_change(values)
    return {
        "series_id": series_id,
        "label": meta["label"],
        "unit": meta["unit"],
        "latest": {"date": latest[0] if latest else None, "value": latest[1] if latest else None},
        "yoy_change": round(yoy, 4) if yoy is not None else None,
        "observations": len([v for _, v in values if v is not None]),
    }


def build_moat() -> dict:
    series_data = {sid: process_series(sid, meta) for sid, meta in SERIES.items()}

    wti = series_data["DCOILWTICO"]
    gas = series_data["DHHNGSP"]
    gasoline = series_data["GASREGM"]
    elec = series_data["CUSR0000SETB01"]

    stress_components = []
    # Normalize WTI 0..1 around $40-$120
    if wti["latest"]["value"] is not None:
        stress_components.append(max(0.0, min(1.0, (wti["latest"]["value"] - 40.0) / 80.0)))
    # Normalize Henry Hub 0..1 around $2-$10
    if gas["latest"]["value"] is not None:
        stress_components.append(max(0.0, min(1.0, (gas["latest"]["value"] - 2.0) / 8.0)))
    # Normalize gasoline 0..1 around $2-$6
    if gasoline["latest"]["value"] is not None:
        stress_components.append(max(0.0, min(1.0, (gasoline["latest"]["value"] - 2.0) / 4.0)))
    # Electricity CPI YoY as stress signal
    elec_yoy = elec.get("yoy_change")
    if elec_yoy is not None:
        stress_components.append(max(0.0, min(1.0, elec_yoy / 0.20)))

    energy_stress = round(sum(stress_components) / len(stress_components), 3) if stress_components else 0.0

    moat = {
        "derived_from": {
            "sources": ["FRED — Federal Reserve Economic Data"],
            "catalog_ref": "~/Downloads/csoai_free_data_catalog.md",
            "note": "Public US energy price series only. No proprietary data.",
        },
        "series": series_data,
        "indices": {
            "energy_stress": energy_stress,
        },
        "sim_params": {
            # Energy stress raises food/operational scarcity and contagion risk.
            "scarcity_food_mult": round(3.2 + 1.5 * energy_stress, 3),
            "contagion_step_boost": round(1.0 + 0.4 * energy_stress, 3),
            "baseline_lawlessness": round(0.02 + 0.08 * energy_stress, 3),
        },
        "hives": ENERGY_HIVES,
    }
    if not moat_common.save_json(MOAT_PATH, moat):
        raise RuntimeError(f"Failed to write {MOAT_PATH}")
    return moat


def load_moat(default=None):
    """Load the cached energy moat JSON."""
    return moat_common.load_moat("energy", default=default)


if __name__ == "__main__":
    moat = build_moat()
    print(f"  ENERGY MOAT — FRED {len(moat['series'])} series -> {MOAT_PATH}")
    print(f"  energy_stress={moat['indices']['energy_stress']}")
    for sid, s in moat["series"].items():
        print(f"    {sid}: latest={s['latest']['value']} ({s['latest']['date']}) yoy={s['yoy_change']}")
