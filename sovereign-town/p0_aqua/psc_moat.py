#!/usr/bin/env python3
"""
psc_moat.py — turn UK Companies House PSC snapshot into Sovereign Town aggregate signals.

Reads the official PSC snapshot (persons-with-significant-control-snapshot-*.txt),
which is OGL-UK-3.0 open government data. This file contains personal identifiers
(names, partial DOB, addresses), so we ONLY emit aggregate/derived statistics —
no individual records, names, or full postcodes are written to the output.

The snapshot is too large for most laptops (~12 GB / ~15.6 M records as of
2026-06-16), so this script streams one JSON line at a time.

Usage on the VM where the snapshot lives:
    PSC_SNAPSHOT=/data/hive-data/.hive/data/government/companies_house_psc/\
persons-with-significant-control-snapshot-2026-06-16.txt \
        python3.11 psc_moat.py

Usage with a local export (small sample):
    python3.11 psc_moat.py --export path/to/psc_sample.jsonl
"""
from __future__ import annotations
import gzip
import json
import logging
import os
import re
from collections import Counter
from pathlib import Path

import moat_common

logger = logging.getLogger(__name__)

OUT = Path(__file__).parent
MOAT_PATH = OUT / "psc_moat.json"

# Default location on the VM; override with PSC_SNAPSHOT env var.
DEFAULT_SNAPSHOT = (
    "/data/hive-data/.hive/data/government/companies_house_psc/"
    "persons-with-significant-control-snapshot-2026-06-16.txt"
)

# Hives whose governance surface touches corporate ownership / transparency.
PSC_HIVES = [
    "landlaw",            # property / title / legal structures
    "commercialvehicle",  # fleet / logistics companies
    "loopfactory",        # manufacturing / holding structures
    "councilof",          # governance / board accountability
    "transparencyof",     # beneficial-ownership transparency
    "accountabilityof",   # accountability / audit
]

KIND_LABELS = {
    "individual-person-with-significant-control": "individual",
    "corporate-entity-person-with-significant-control": "corporate",
    "legal-person-person-with-significant-control": "legal_person",
    "super-secure-person-with-significant-control": "super_secure",
}


def _postcode_area(postcode: str) -> str | None:
    """Return the outward code (area + district prefix) — coarse enough to be aggregate-safe."""
    if not postcode:
        return None
    m = re.match(r"([A-Z]{1,2}[0-9][0-9A-Z]?)", postcode.upper().strip())
    return m.group(1) if m else None


def _decade(year: int | None) -> int | None:
    if year and 1900 <= year <= 2025:
        return (year // 10) * 10
    return None


def process_snapshot(path: str | Path) -> dict:
    path = Path(path)

    total = 0
    kind_counts: Counter = Counter()
    nature_counts: Counter = Counter()
    country_counts: Counter = Counter()
    nationality_counts: Counter = Counter()
    decade_counts: Counter = Counter()
    postcode_area_counts: Counter = Counter()
    verified_counts: Counter = Counter()  # verified / unverified / not_required
    companies_with_psc: Counter = Counter()  # company_number -> count

    opener = gzip.open if str(path).endswith(".gz") else open
    with opener(path, "rt", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue

            total += 1
            data = rec.get("data", {})
            kind = data.get("kind", "unknown")
            kind_counts[KIND_LABELS.get(kind, kind)] += 1

            company_number = rec.get("company_number", "")
            if company_number:
                companies_with_psc[company_number] += 1

            for nature in data.get("natures_of_control", []):
                nature_counts[nature] += 1

            country = data.get("country_of_residence", "unknown").strip() or "unknown"
            country_counts[country] += 1

            nationality = data.get("nationality", "unknown").strip() or "unknown"
            nationality_counts[nationality] += 1

            yob = data.get("date_of_birth", {}).get("year")
            decade = _decade(yob)
            if decade:
                decade_counts[decade] += 1

            postcode = ""
            address = data.get("address", {})
            if isinstance(address, dict):
                postcode = address.get("postal_code", "") or ""
            area = _postcode_area(postcode)
            if area:
                postcode_area_counts[area] += 1

            iv = data.get("identity_verification_details")
            if iv:
                verified_counts["verified"] += 1
            else:
                verified_counts["unverified"] += 1

    # Derived aggregate metrics.
    individual = kind_counts.get("individual", 0)
    corporate = kind_counts.get("corporate", 0)
    total_companies = len(companies_with_psc)
    multi_psc_companies = sum(1 for c in companies_with_psc.values() if c > 1)
    avg_psc_per_company = round(total / max(1, total_companies), 3)

    # Ownership concentration signal: what share of disclosures claim 75-100% control?
    control_75_100 = nature_counts.get("ownership-of-shares-75-to-100-percent", 0)
    ownership_concentration = round(control_75_100 / max(1, total), 3)

    # Transparency pressure: higher individual PSC ratio + unverified ratio = more governance load.
    unverified_ratio = round(verified_counts.get("unverified", 0) / max(1, total), 3)
    transparency_pressure = round(
        0.5 * (individual / max(1, total)) + 0.5 * unverified_ratio, 3
    )

    return {
        "source": "UK Companies House PSC snapshot",
        "snapshot_path": str(path),
        "total_records": total,
        "kind_counts": dict(kind_counts.most_common(10)),
        "nature_counts": dict(nature_counts.most_common(15)),
        "country_counts": dict(country_counts.most_common(15)),
        "nationality_counts": dict(nationality_counts.most_common(15)),
        "decade_counts": {str(k): v for k, v in sorted(decade_counts.items())},
        "postcode_area_counts": dict(postcode_area_counts.most_common(20)),
        "identity_verification": dict(verified_counts),
        "company_stats": {
            "companies_with_psc": total_companies,
            "companies_with_multiple_psc": multi_psc_companies,
            "avg_psc_per_company": avg_psc_per_company,
        },
        "indices": {
            "transparency_pressure": transparency_pressure,
            "ownership_concentration": ownership_concentration,
            "unverified_ratio": unverified_ratio,
        },
    }


def build_moat(records_path: str | Path | None = None) -> dict:
    if records_path is None:
        records_path = os.environ.get("PSC_SNAPSHOT", DEFAULT_SNAPSHOT)
    records_path = Path(records_path)

    if not records_path.exists():
        raise FileNotFoundError(f"PSC snapshot not found: {records_path}")

    summary = process_snapshot(records_path)
    transparency_pressure = summary["indices"]["transparency_pressure"]

    moat = {
        "status": "live_aggregate",
        "derived_from": {
            "source": "UK Companies House PSC snapshot (OGL-UK-3.0)",
            "snapshot_path": str(records_path),
            "total_records": summary["total_records"],
            "note": "Aggregate statistics only. No names, full DOBs, full addresses, or postcodes emitted.",
        },
        "psc_summary": summary,
        "hives": PSC_HIVES,
        "indices": {
            "transparency_pressure": transparency_pressure,
        },
        "sim_params": {
            # High beneficial-ownership transparency pressure => stronger enforcement of disclosure.
            "regime_enforcement_boost": round(1.0 + 0.3 * transparency_pressure, 3),
            # Concentrated ownership => higher scarcity/contagion sensitivity in ungoverned arm.
            "scarcity_food_mult": round(3.2 + 2.0 * summary["indices"]["ownership_concentration"], 3),
        },
    }
    if not moat_common.save_json(MOAT_PATH, moat):
        raise RuntimeError(f"Failed to write {MOAT_PATH}")
    return moat


def load_moat(default=None):
    """Load the cached PSC moat JSON."""
    return moat_common.load_moat("psc", default=default)


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--export", help="Path to local PSC JSONL file/directory")
    args = ap.parse_args()

    path = args.export or os.environ.get("PSC_SNAPSHOT", DEFAULT_SNAPSHOT)
    moat = build_moat(path)
    summary = moat["psc_summary"]
    print(f"  PSC MOAT — {summary['total_records']:,} PSC records (aggregate only) -> {MOAT_PATH}")
    print(f"  transparency_pressure={moat['indices']['transparency_pressure']}")
    print(f"  kinds: {summary['kind_counts']}")
    print(f"  top natures: {dict(list(summary['nature_counts'].items())[:5])}")
    print(f"  companies with PSC: {summary['company_stats']['companies_with_psc']:,}")
