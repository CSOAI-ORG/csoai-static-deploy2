#!/usr/bin/env python3
"""
attestation_moat.py — turn MEOK compliance attestations into Sovereign Town training signal.

Reads the MEOK Attestation API audit ledger (public /api/audit endpoint, or a local export)
and maps each regulation/framework to the relevant Sovereign Town hives. Produces
attestation_moat.json with per-hive pass rates and average scores.

Usage:
    # With live API (requires MEOK_MASTER_API_KEY)
    MEOK_MASTER_API_KEY=xxx python3.11 attestation_moat.py

    # With local export
    python3.11 attestation_moat.py --export path/to/audit_export.json

No personal/entity identifiers are emitted in the aggregate output.
"""
from __future__ import annotations
import json
import logging
import os
import urllib.request
import urllib.parse
from pathlib import Path
from collections import defaultdict

import moat_common

logger = logging.getLogger(__name__)

OUT = Path(__file__).parent
EXPORT_PATH = OUT / "attestation_export.json"
MOAT_PATH = OUT / "attestation_moat.json"
API_BASE = os.environ.get("MEOK_ATTESTATION_API", "https://meok-attestation-api.vercel.app")

# Map compliance regimes to the hives whose frameworks include them.
REGIME_TO_HIVES: dict[str, list[str]] = {
    "EU AI Act": ["ethicalgovernanceof", "biasdetectionof", "transparencyof", "accountabilityof"],
    "DORA": ["dataprivacyof", "councilof", "agisafe"],
    "NIS2": ["asisecurity", "agisafe", "councilof"],
    "GDPR": ["dataprivacyof", "transparencyof"],
    "CRA": ["asisecurity", "agisafe", "openmcp"],
    "CSRD": ["transparencyof", "accountabilityof"],
    "UK AI Regulation": ["ethicalgovernanceof", "councilof"],
    "UK AI Bill": ["ethicalgovernanceof", "councilof"],
    "SOC 2": ["accountabilityof", "dataprivacyof"],
    "ISO 42001": ["ethicalgovernanceof"],
    "HIPAA": ["dataprivacyof", "suicidestop"],
    "PCI DSS": ["commercialvehicle", "loopfactory"],
}


def _normalize_regulation(raw: str) -> str | None:
    """Match a free-text regulation field to one of our canonical keys."""
    if not raw:
        return None
    r = raw.upper().strip()
    aliases = {
        "EU AI ACT": "EU AI Act",
        "AI ACT": "EU AI Act",
        "DORA": "DORA",
        "NIS2": "NIS2",
        "NIS 2": "NIS2",
        "GDPR": "GDPR",
        "CRA": "CRA",
        "CSRD": "CSRD",
        "UK AI": "UK AI Regulation",
        "UK AI BILL": "UK AI Bill",
        "SOC2": "SOC 2",
        "SOC 2": "SOC 2",
        "ISO 42001": "ISO 42001",
        "ISO/IEC 42001": "ISO 42001",
        "HIPAA": "HIPAA",
        "PCI DSS": "PCI DSS",
        "PCI-DSS": "PCI DSS",
    }
    for alias, canon in aliases.items():
        if alias in r:
            return canon
    # Fuzzy: if any canonical key appears as substring
    for canon in REGIME_TO_HIVES:
        if canon.upper() in r:
            return canon
    return None


def _is_pass(result: str) -> bool | None:
    r = (result or "").lower()
    if r in ("ok", "valid", "pass", "true"):
        return True
    if r in ("fail", "invalid", "false"):
        return False
    return None


def fetch_from_api(master_key: str, base_url: str = API_BASE, per_page: int = 500) -> tuple[list[dict], dict]:
    """Paginate the MEOK Attestation API audit endpoint.

    Returns (events, api_meta) where api_meta includes backend/status diagnostics.
    """
    events = []
    api_meta: dict = {"base_url": base_url}
    since_ts = 0
    max_pages = 20
    for _ in range(max_pages):
        url = f"{base_url}/api/audit?since={since_ts}&limit={per_page}"
        req = urllib.request.Request(
            url,
            headers={"X-Master-Key": master_key, "Accept": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read())
        # Capture backend diagnostics on first page only.
        if "stats" not in api_meta:
            api_meta["stats"] = data.get("stats", {})
            api_meta["since"] = data.get("since")
            api_meta["limit"] = data.get("limit")
        batch = data.get("events", [])
        if not batch:
            break
        events.extend(batch)
        # advance since_ts just past the latest event timestamp
        ts_vals = [int(e.get("ts", 0)) for e in batch if e.get("ts")]
        if ts_vals:
            since_ts = max(ts_vals) + 1
        else:
            # fall back to issued_at epoch ms
            iso_vals = [e.get("issued_at", "") for e in batch if e.get("issued_at")]
            if iso_vals:
                from datetime import datetime
                since_ts = int(max(
                    datetime.fromisoformat(i.replace("Z", "+00:00")).timestamp() * 1000
                    for i in iso_vals
                )) + 1
        if len(batch) < per_page:
            break
    return events, api_meta


def load_export(path: str | Path) -> list[dict]:
    data = moat_common.load_json(path, default=[])
    if isinstance(data, dict):
        return data.get("events", [])
    return data


def process_events(events: list[dict]) -> dict:
    """Aggregate events into per-regime and per-hive statistics."""
    regime_stats: dict[str, dict] = defaultdict(lambda: {"pass": 0, "fail": 0, "score_sum": 0.0, "score_n": 0, "events": 0})
    hive_stats: dict[str, dict] = defaultdict(lambda: {"pass": 0, "fail": 0, "score_sum": 0.0, "score_n": 0, "events": 0, "regimes": set()})

    for e in events:
        reg = _normalize_regulation(e.get("regulation", ""))
        if not reg:
            continue
        passed = _is_pass(e.get("result", ""))
        score = e.get("score")
        try:
            score_f = float(score) if score is not None else None
        except (ValueError, TypeError):
            score_f = None

        rs = regime_stats[reg]
        rs["events"] += 1
        if passed is True:
            rs["pass"] += 1
        elif passed is False:
            rs["fail"] += 1
        if score_f is not None:
            rs["score_sum"] += score_f
            rs["score_n"] += 1

        for hive in REGIME_TO_HIVES.get(reg, []):
            hs = hive_stats[hive]
            hs["events"] += 1
            hs["regimes"].add(reg)
            if passed is True:
                hs["pass"] += 1
            elif passed is False:
                hs["fail"] += 1
            if score_f is not None:
                hs["score_sum"] += score_f
                hs["score_n"] += 1

    def finalize(stats: dict) -> dict:
        total = stats["pass"] + stats["fail"]
        return {
            "events": stats["events"],
            "pass": stats["pass"],
            "fail": stats["fail"],
            "pass_rate": round(stats["pass"] / total, 3) if total else None,
            "avg_score": round(stats["score_sum"] / stats["score_n"], 3) if stats["score_n"] else None,
        }

    return {
        "regimes": {k: finalize(v) for k, v in regime_stats.items()},
        "hives": {k: {**finalize(v), "regimes": sorted(v["regimes"])} for k, v in hive_stats.items()},
    }


def load_moat(default=None):
    """Load the cached attestation moat JSON."""
    return moat_common.load_moat("attestation", default=default)


def build_moat(events: list[dict] | None = None) -> dict:
    api_meta: dict | None = None
    if events is None:
        master_key = os.environ.get("MEOK_MASTER_API_KEY", "")
        if master_key:
            events, api_meta = fetch_from_api(master_key)
            source = "MEOK Attestation API audit ledger"
            status = "live" if events else "live_empty"
        elif EXPORT_PATH.exists():
            events = load_export(EXPORT_PATH)
            source = f"local export {EXPORT_PATH.name}"
            status = "sample"
        else:
            events = []
            source = "none"
            status = "empty"
    else:
        source = "provided"
        status = "sample" if events else "empty"

    aggregated = process_events(events)
    moat = {
        "status": status,
        "derived_from": {
            "source": source,
            "event_count": len(events),
            "api_meta": api_meta,
            "note": "Aggregate pass rates and scores per regime/hive. No entity identifiers emitted.",
        },
        **aggregated,
    }
    if not moat_common.save_json(MOAT_PATH, moat):
        raise RuntimeError(f"Failed to write {MOAT_PATH}")
    return moat


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--export", help="Path to local audit export JSON")
    args = ap.parse_args()

    events = None
    if args.export:
        events = load_export(args.export)

    moat = build_moat(events)
    print(f"  ATTESTATION MOAT — status={moat['status']}, events={moat['derived_from']['event_count']} -> {MOAT_PATH}")
    api_stats = (moat['derived_from'].get('api_meta') or {}).get('stats')
    if api_stats:
        print(f"  API backend: {api_stats}")
    print("  " + "-" * 60)
    print(f"  {'regime':<20}{'events':>8}{'pass rate':>12}{'avg score':>12}")
    for reg, s in sorted(moat["regimes"].items(), key=lambda x: -x[1]["events"]):
        print(f"  {reg:<20}{s['events']:>8}{(str(s['pass_rate']) if s['pass_rate'] is not None else '-'):>12}{(str(s['avg_score']) if s['avg_score'] is not None else '-'):>12}")
    print("  " + "-" * 60)
    print(f"  hives covered: {len(moat['hives'])}")
