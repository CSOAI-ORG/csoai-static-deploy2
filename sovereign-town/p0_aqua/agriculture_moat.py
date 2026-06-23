#!/usr/bin/env python3
"""
agriculture_moat.py — turn public FAOSTAT food-balance data into Sovereign Town signals.

Downloads the FAOSTAT Food Balance Sheets bulk ZIP (no API key required), streams the
csv, and emits aggregate-only statistics: global food supply, production by category,
import dependency, and fish/aquatic share. No individual farm, country, or firm data is
emitted.

The dataset is large (~52 MB zip / ~300 MB csv), so the script downloads to a temporary
file, extracts, and streams one row at a time.

Usage:
    python3.11 agriculture_moat.py

To use an already-downloaded zip:
    AGRICULTURE_ZIP=/path/to/FoodBalanceSheets_E_All_Data_(Normalized).zip python3.11 agriculture_moat.py
"""
from __future__ import annotations
import csv
import json
import logging
import os
import shutil
import tempfile
import urllib.request
import zipfile
from collections import defaultdict
from pathlib import Path

import moat_common

logger = logging.getLogger(__name__)

OUT = Path(__file__).parent
MOAT_PATH = OUT / "agriculture_moat.json"

FBS_URL = (
    "https://fenixservices.fao.org/faostat/static/bulkdownloads/"
    "FoodBalanceSheets_E_All_Data_%28Normalized%29.zip"
)

AGRICULTURE_HIVES = [
    "koikeeper",
    "fishkeeper",
    "loopfactory",
    "muckaway",
    "commercialvehicle",
    "councilof",
]

# Broad FAOSTAT item groups we care about for the moat.
BROAD_CATEGORIES = {
    "Cereals - Excluding Beer",
    "Meat",
    "Fish, Seafood",
    "Milk - Excluding Butter",
    "Eggs",
    "Vegetables",
    "Fruits - Excluding Wine",
    "Pulses",
    "Starchy Roots",
    "Sugar & Sweeteners",
    "Vegetable Oils",
    "Animal fats",
}

CATEGORY_MAP = {
    "Cereals - Excluding Beer": "cereals",
    "Wheat and products": "cereals",
    "Rice and products": "cereals",
    "Maize and products": "cereals",
    "Barley and products": "cereals",
    "Meat": "meat",
    "Bovine Meat": "meat",
    "Poultry Meat": "meat",
    "Pigmeat": "meat",
    "Mutton & Goat Meat": "meat",
    "Fish, Seafood": "fish_seafood",
    "Freshwater Fish": "fish_seafood",
    "Marine Fish, Other": "fish_seafood",
    "Pelagic Fish": "fish_seafood",
    "Demersal Fish": "fish_seafood",
    "Meat, Aquatic Mammals": "fish_seafood",
    "Milk - Excluding Butter": "dairy",
    "Eggs": "dairy",
    "Vegetables": "fruit_veg",
    "Fruits - Excluding Wine": "fruit_veg",
    "Pulses": "pulses",
    "Starchy Roots": "roots",
    "Sugar & Sweeteners": "sugar",
    "Vegetable Oils": "oils",
    "Animal fats": "oils",
}

FISH_ITEMS = {
    "Fish, Seafood", "Freshwater Fish", "Marine Fish, Other",
    "Pelagic Fish", "Demersal Fish", "Fish, Body Oil", "Fish, Liver Oil",
    "Meat, Aquatic Mammals",
}


def download_zip(url: str, dest: Path, timeout: int = 180) -> None:
    req = urllib.request.Request(url, headers={"Accept": "application/zip"})
    last_err = None
    for attempt in range(2):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                with open(dest, "wb") as f:
                    shutil.copyfileobj(r, f)
            return
        except (urllib.error.URLError, urllib.error.HTTPError, OSError, TimeoutError) as e:
            last_err = e
    raise RuntimeError(f"Failed to download {url}: {last_err}")


def _float(v: str) -> float | None:
    if v is None:
        return None
    v = v.strip()
    if v in ("", ".", "NaN"):
        return None
    try:
        return float(v)
    except ValueError:
        return None


def process_fbs_csv(csv_path: Path) -> dict:
    # Pass 1: find latest year and collect per-area population + grand totals.
    latest_year = 0
    populations: dict[tuple[str, int], float] = {}  # (area, year) -> 1000 persons
    totals: dict[tuple[str, int, str], float] = {}  # (area, year, element) -> value

    with open(csv_path, newline="", encoding="utf-8", errors="replace") as f:
        reader = csv.DictReader(f)
        for row in reader:
            year = int(row.get("Year", 0) or 0)
            if year == 0:
                continue
            if year > latest_year:
                latest_year = year

    if latest_year == 0:
        raise RuntimeError("No valid years found in FBS CSV")

    # Pass 2: aggregate for latest year.
    with open(csv_path, newline="", encoding="utf-8", errors="replace") as f:
        reader = csv.DictReader(f)
        for row in reader:
            year = int(row.get("Year", 0) or 0)
            if year != latest_year:
                continue
            area = row.get("Area", "").strip()
            item = row.get("Item", "").strip()
            element = row.get("Element", "").strip()
            val = _float(row.get("Value", ""))
            if val is None or not area or not item or not element:
                continue

            if item == "Population" and element == "Total Population - Both sexes":
                populations[(area, year)] = val  # 1000 persons
            elif item == "Grand Total":
                totals[(area, year, element)] = val

    # Global population from population rows.
    total_pop = sum(populations.get((a, latest_year), 0) for a in {k[0] for k in populations})

    # Production / trade are not present on Grand Total in this dataset, so we
    # aggregate the broad category items to avoid double-counting sub-items.
    production = 0.0
    imports = 0.0
    exports = 0.0
    domestic_supply = 0.0

    # Weighted global kcal and protein per capita.
    weighted_kcal_num = 0.0
    weighted_prot_num = 0.0
    for (area, year, element), val in totals.items():
        pop = populations.get((area, year), 0)
        if pop <= 0:
            continue
        if element == "Food supply (kcal/capita/day)":
            weighted_kcal_num += pop * val
        elif element == "Protein supply quantity (g/capita/day)":
            weighted_prot_num += pop * val

    global_kcal = weighted_kcal_num / total_pop if total_pop else 0.0
    global_protein = weighted_prot_num / total_pop if total_pop else 0.0

    # Production by category (latest year, global).
    category_production: dict[str, float] = defaultdict(float)
    fish_production = 0.0
    with open(csv_path, newline="", encoding="utf-8", errors="replace") as f:
        reader = csv.DictReader(f)
        for row in reader:
            year = int(row.get("Year", 0) or 0)
            if year != latest_year:
                continue
            item = row.get("Item", "").strip()
            element = row.get("Element", "").strip()
            val = _float(row.get("Value", ""))
            if val is None:
                continue
            if item in BROAD_CATEGORIES:
                if element == "Production":
                    production += val
                    cat = CATEGORY_MAP.get(item)
                    if cat:
                        category_production[cat] += val
                elif element == "Import quantity":
                    imports += val
                elif element == "Export quantity":
                    exports += val
                elif element == "Domestic supply quantity":
                    domestic_supply += val
            if item in FISH_ITEMS and element == "Production":
                fish_production += val

    # Food security index: 2500 kcal/capita/day as benchmark.
    food_security_index = round(min(1.0, global_kcal / 2500.0), 3)
    scarcity_pressure = round(1.0 - food_security_index, 3)

    # Import dependency: imports / (production + imports) globally.
    import_dependency = round(imports / (production + imports), 3) if (production + imports) > 0 else 0.0

    return {
        "source": "FAOSTAT Food Balance Sheets",
        "url": FBS_URL,
        "latest_year": latest_year,
        "global": {
            "population_thousands": round(total_pop, 0),
            "production_1000_t": round(production, 0),
            "imports_1000_t": round(imports, 0),
            "exports_1000_t": round(exports, 0),
            "domestic_supply_1000_t": round(domestic_supply, 0),
            "food_supply_kcal_per_capita_day": round(global_kcal, 1),
            "protein_supply_g_per_capita_day": round(global_protein, 1),
        },
        "category_production_1000_t": dict(sorted(category_production.items(), key=lambda x: -x[1])),
        "fish_production_1000_t": round(fish_production, 0),
        "indices": {
            "food_security_index": food_security_index,
            "scarcity_pressure": scarcity_pressure,
            "import_dependency": import_dependency,
        },
    }


def load_moat(default=None):
    try:
        with open(MOAT_PATH) as f:
            return json.load(f)
    except Exception:
        return default


def build_moat(zip_path: str | Path | None = None) -> dict:
    if zip_path is None:
        zip_path = os.environ.get("AGRICULTURE_ZIP", "")
    zip_path = Path(zip_path) if zip_path else None

    tmpdir = Path(tempfile.mkdtemp(prefix="agriculture_moat_"))
    try:
        if zip_path and zip_path.exists():
            local_zip = zip_path
        else:
            local_zip = tmpdir / "fbs.zip"
            print(f"  Downloading FAOSTAT Food Balance Sheets...")
            download_zip(FBS_URL, local_zip)

        with zipfile.ZipFile(local_zip, "r") as z:
            csv_name = next(n for n in z.namelist() if n.endswith(".csv"))
            z.extract(csv_name, tmpdir)
        csv_path = tmpdir / csv_name

        summary = process_fbs_csv(csv_path)
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)

    scarcity_pressure = summary["indices"]["scarcity_pressure"]
    import_dependency = summary["indices"]["import_dependency"]

    moat = {
        "status": "live_aggregate",
        "derived_from": {
            "source": "FAOSTAT Food Balance Sheets",
            "url": FBS_URL,
            "latest_year": summary["latest_year"],
            "note": "Aggregate global statistics only. No farm-, country-, or firm-level data emitted.",
        },
        "agriculture_summary": summary,
        "hives": AGRICULTURE_HIVES,
        "indices": {
            "scarcity_pressure": scarcity_pressure,
            "import_dependency": import_dependency,
        },
        "sim_params": {
            # Higher scarcity pressure -> higher food-cost multiplier during scarcity shocks.
            "scarcity_food_mult": round(3.2 + 2.0 * scarcity_pressure, 3),
            # Higher import dependency -> slightly higher contagion sensitivity (supply-chain fragility).
            "contagion_step_boost": round(1.0 + 0.3 * import_dependency, 3),
        },
    }
    with open(MOAT_PATH, "w") as f:
        json.dump(moat, f, indent=2)
    return moat


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--zip", help="Path to local FAOSTAT FoodBalanceSheets zip")
    args = ap.parse_args()

    moat = build_moat(args.zip)
    summary = moat["agriculture_summary"]
    print(f"  AGRICULTURE MOAT — year {summary['latest_year']}, "
          f"{summary['global']['production_1000_t']:,.0f} kt production -> {MOAT_PATH}")
    print(f"  scarcity_pressure={moat['indices']['scarcity_pressure']} "
          f"food_security_index={summary['indices']['food_security_index']}")
    print(f"  top categories: {dict(list(summary['category_production_1000_t'].items())[:5])}")
    print(f"  fish/seafood production: {summary['fish_production_1000_t']:,.0f} kt")
