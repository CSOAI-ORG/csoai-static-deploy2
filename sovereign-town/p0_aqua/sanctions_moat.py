#!/usr/bin/env python3
"""
sanctions_moat.py — turn public sanctions/compliance lists into Sovereign Town pressure signals.

Reads the US Treasury OFAC Specially Designated Nationals (SDN) list and maps
sanction programs onto governance, security, and privacy hives. Produces
sanctions_moat.json with compliance-pressure indices used by sim.py and
jurisdiction.py.

Sources from the CSOAI Free Data Catalog; no API keys required.
"""
from __future__ import annotations
import csv
import io
import json
import logging
import urllib.request
from collections import defaultdict
from pathlib import Path

import moat_common

logger = logging.getLogger(__name__)

OUT = Path(__file__).parent
MOAT_PATH = OUT / "sanctions_moat.json"

OFAC_SDN_CSV_URL = "https://www.treasury.gov/ofac/downloads/sdn.csv"

# OFAC SDN CSV columns ( Treasury does not ship a header row ):
# 0 ent_num, 1 SDN_Name, 2 SDN_Type, 3 Program, 4 Title, 5 Call_Sign,
# 6 Vess_Type, 7 Tonnage, 8 GRT, 9 Vess_Flag, 10 Vess_Owner, 11 DOB
COL_ENT_NUM = 0
COL_NAME = 1
COL_TYPE = 2
COL_PROGRAM = 3

# Map sanction-program tokens/keywords to Sovereign Town hives.
# A single program can map to multiple hives.
PROGRAM_TO_HIVES: dict[str, list[str]] = {
    "CYBER2": ["asisecurity", "agisafe", "dataprivacyof"],
    "CYBER": ["asisecurity", "agisafe", "dataprivacyof"],
    "CAATSA": ["asisecurity", "councilof"],
    "E.O. 13694": ["asisecurity", "agisafe", "dataprivacyof"],
    "E.O. 13985": ["asisecurity", "agisafe", "dataprivacyof"],
    "IRAN": ["councilof", "ethicalgovernanceof", "transparencyof"],
    "IRGC": ["councilof", "asisecurity"],
    "RUSSIA": ["councilof", "ethicalgovernanceof", "transparencyof"],
    "UKRAINE": ["councilof", "ethicalgovernanceof"],
    "DPRK": ["councilof", "asisecurity"],
    "NORTH KOREA": ["councilof", "asisecurity"],
    "CHINA": ["councilof", "ethicalgovernanceof"],
    "SYRIA": ["councilof", "ethicalgovernanceof"],
    "CUBA": ["councilof", "ethicalgovernanceof"],
    "VENEZUELA": ["councilof", "ethicalgovernanceof"],
    "BELARUS": ["councilof", "ethicalgovernanceof"],
    "BURMA": ["councilof", "ethicalgovernanceof"],
    "SOMALIA": ["councilof", "ethicalgovernanceof"],
    "SUDAN": ["councilof", "ethicalgovernanceof"],
    "HAITI": ["councilof", "ethicalgovernanceof"],
    "FTO": ["councilof", "asisecurity"],
    "SDGT": ["councilof", "asisecurity"],
    "SDN": ["councilof"],
    "TCO": ["councilof", "commercialvehicle"],
    "NARCOTRAFFICKING": ["councilof", "commercialvehicle"],
    "COUNTER NARCOTICS": ["councilof", "commercialvehicle"],
    "MAGNITSKY": ["councilof", "ethicalgovernanceof", "transparencyof"],
    "CORRUPT": ["councilof", "ethicalgovernanceof", "transparencyof", "accountabilityof"],
    "ILLICIT DRUGS": ["councilof", "commercialvehicle"],
}


def fetch_csv(url: str, timeout: int = 60) -> str:
    req = urllib.request.Request(
        url,
        headers={
            "Accept": "text/csv",
            "User-Agent": "sovereign-town-sanctions-moat/1.0",
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", errors="replace")


def _program_tokens(program_field: str) -> list[str]:
    """Split OFAC program field into individual program tokens."""
    raw = (program_field or "").replace(";", ",").replace(" and ", ",")
    return [t.strip().upper() for t in raw.split(",") if t.strip()]


def _map_program_to_hives(program: str) -> list[str]:
    p = program.upper()
    # Exact token match first.
    if p in PROGRAM_TO_HIVES:
        return PROGRAM_TO_HIVES[p]
    # Keyword containment fallback.
    for token, hives in PROGRAM_TO_HIVES.items():
        if token in p:
            return hives
    return ["councilof", "dataprivacyof"]


def process_sdn_csv(text: str) -> dict:
    reader = csv.reader(io.StringIO(text))
    rows = list(reader)

    program_counts: dict[str, int] = defaultdict(int)
    hive_hits: dict[str, int] = defaultdict(int)
    entity_types: dict[str, int] = defaultdict(int)
    total = 0

    for row in rows:
        if len(row) < 4:
            continue
        total += 1
        name = row[COL_NAME].strip().strip('"')
        ent_type = row[COL_TYPE].strip().strip('"')
        program_field = row[COL_PROGRAM].strip().strip('"')

        if ent_type and ent_type != "-0-":
            entity_types[ent_type] += 1

        programs = _program_tokens(program_field)
        if not programs or programs == ["-0-"]:
            programs = ["SDN"]

        for prog in programs:
            if prog and prog != "-0-":
                program_counts[prog] += 1
                for hive in _map_program_to_hives(prog):
                    hive_hits[hive] += 1

    # Compliance pressure: normalize against a baseline of ~20,000 SDN entries.
    # More entries + more cyber-focused programs -> higher pressure.
    cyber_programs = {"CYBER2", "CYBER", "CAATSA", "E.O. 13694", "E.O. 13985"}
    cyber_count = sum(program_counts.get(p, 0) for p in cyber_programs)
    compliance_pressure = round(min(1.0, total / 25_000.0 + cyber_count / 1_000.0), 3)

    return {
        "source": "US Treasury OFAC SDN",
        "url": OFAC_SDN_CSV_URL,
        "total_entries": total,
        "program_counts": dict(sorted(program_counts.items(), key=lambda x: -x[1])[:50]),
        "entity_types": dict(sorted(entity_types.items(), key=lambda x: -x[1])),
        "cyber_sanctions_count": cyber_count,
        "compliance_pressure": compliance_pressure,
        "hive_hits": dict(sorted(hive_hits.items(), key=lambda x: -x[1])),
    }


def load_moat(default=None):
    try:
        with open(MOAT_PATH) as f:
            return json.load(f)
    except Exception:
        return default


def build_moat() -> dict:
    sdn = process_sdn_csv(fetch_csv(OFAC_SDN_CSV_URL, timeout=120))
    pressure = sdn.get("compliance_pressure", 0.0)

    moat = {
        "derived_from": {
            "sources": ["US Treasury OFAC SDN"],
            "catalog_ref": "~/Downloads/csoai_free_data_catalog.md",
            "note": "Public sanctions data only. Aggregate counts; no individual PII emitted.",
        },
        "ofac_sdn": sdn,
        "indices": {
            "compliance_pressure": pressure,
        },
        "sim_params": {
            # Higher sanctions pressure -> stronger enforcement signal in the simulation.
            "regime_enforcement_boost": round(1.0 + 0.5 * pressure, 3),
            "ungoverned_penalty_mult": round(1.0 + 0.3 * pressure, 3),
        },
    }
    with open(MOAT_PATH, "w") as f:
        json.dump(moat, f, indent=2)
    return moat


if __name__ == "__main__":
    moat = build_moat()
    sdn = moat["ofac_sdn"]
    print(f"  SANCTIONS MOAT — {sdn['total_entries']} OFAC SDN entries -> {MOAT_PATH}")
    print(f"  compliance_pressure={moat['indices']['compliance_pressure']}")
    print("  top programs:")
    for prog, n in list(sdn["program_counts"].items())[:8]:
        print(f"    {prog:<24} {n:>6}")
    print(f"  hives touched: {len(sdn['hive_hits'])}")
