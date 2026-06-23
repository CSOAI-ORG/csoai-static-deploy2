#!/usr/bin/env python3
"""
threat_moat.py — turn public threat-intel feeds into Sovereign Town pressure parameters.

Reads CISA Known Exploited Vulnerabilities (KEV) and optionally MITRE ATT&CK,
maps them onto the security/governance hives, and derives a threat-pressure
index that influences the simulation's baseline lawlessness / contagion.

Sources from the CSOAI Free Data Catalog; no API keys required.
"""
from __future__ import annotations
import json
import logging
import os
import urllib.request
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

import moat_common

logger = logging.getLogger(__name__)

OUT = Path(__file__).parent
MOAT_PATH = OUT / "threat_moat.json"

CISA_KEV_URL = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"
ATTACK_URL = "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/enterprise-attack/enterprise-attack.json"

# Map keywords/phrases to Sovereign Town hives. A single CVE/technique can touch multiple hives.
# Use phrases or whole-word keywords to avoid false matches (e.g. "ai" matches "email", "fail").
HIVE_KEYWORDS: dict[str, list[str]] = {
    "asisecurity": ["security", "firewall", "vpn", "remote code", "remote execution", "exploit", "malware", "ransomware", "privilege escalation"],
    "agisafe": ["machine learning", "ml model", "artificial intelligence", "supply chain", "third-party", "model poisoning"],
    "dataprivacyof": ["data breach", "personal data", "privacy", "pii", "gdpr", "leak", "exfiltration", "unauthorized access"],
    "councilof": ["governance", "policy", "framework", "audit", "compliance", "regulatory"],
    "safetyof": ["safety", "critical infrastructure", "ics", "scada", "hospital", "medical", "healthcare", "ot security"],
    "openmcp": ["mcp server", "api gateway", "plugin", "connector", "integration platform"],
    "openmoe": ["mixture of experts", "moe model", "large language model", "llm inference", "model weights"],
    "ethicalgovernanceof": ["ethics", "bias", "fairness", "responsible ai", "algorithmic"],
    "transparencyof": ["reporting", "disclosure", "attestation", "documentation", "audit log", "logging"],
}


def fetch_json(url: str, timeout: int = 60, max_bytes: int | None = None):
    req = urllib.request.Request(url, headers={"Accept": "application/json", "User-Agent": "sovereign-town-threat-moat/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        if max_bytes and r.headers.get("Content-Length"):
            if int(r.headers["Content-Length"]) > max_bytes:
                raise RuntimeError(f"response too large (> {max_bytes} bytes)")
        return json.loads(r.read())


def _matches(text: str, keywords: list[str]) -> bool:
    t = text.lower()
    return any(k in t for k in keywords)


def _parse_date(s: str) -> datetime | None:
    try:
        return datetime.strptime(s[:10], "%Y-%m-%d").replace(tzinfo=timezone.utc)
    except (ValueError, TypeError):
        return None


def process_cisa_kev(data: dict) -> dict:
    entries = data.get("vulnerabilities", [])
    cutoff = datetime.now(timezone.utc) - timedelta(days=90)
    total = len(entries)
    recent = 0
    ransomware = 0
    hive_hits: dict[str, int] = defaultdict(int)
    recent_hive_hits: dict[str, int] = defaultdict(int)

    for e in entries:
        text = " ".join([
            e.get("vulnerabilityName", ""),
            e.get("vendorProject", ""),
            e.get("product", ""),
            e.get("requiredAction", ""),
            e.get("notes", ""),
        ])
        added = _parse_date(e.get("dateAdded", ""))
        is_recent = added and added >= cutoff
        is_ransomware = str(e.get("knownRansomwareCampaignUse", "")).lower() in ("true", "yes", "known")
        if is_recent:
            recent += 1
        if is_ransomware:
            ransomware += 1

        for hive, keywords in HIVE_KEYWORDS.items():
            if _matches(text, keywords):
                hive_hits[hive] += 1
                if is_recent:
                    recent_hive_hits[hive] += 1

    # Normalize threat pressure 0..1 based on recent activity
    # Typical CISA KEV has ~1,000 entries; ~50-100 recent per quarter
    recent_pressure = min(1.0, recent / 150.0)
    ransomware_pressure = min(1.0, ransomware / 200.0)
    threat_pressure = round(max(recent_pressure, ransomware_pressure), 3)

    return {
        "source": "CISA KEV",
        "url": CISA_KEV_URL,
        "total_entries": total,
        "recent_90d": recent,
        "ransomware_linked": ransomware,
        "threat_pressure": threat_pressure,
        "hive_hits": dict(sorted(hive_hits.items(), key=lambda x: -x[1])),
        "recent_hive_hits": dict(sorted(recent_hive_hits.items(), key=lambda x: -x[1])),
    }


def process_attack(data: dict) -> dict:
    """Lightweight summary of MITRE ATT&CK enterprise matrix."""
    objs = data.get("objects", [])
    techniques = [o for o in objs if o.get("type") == "attack-pattern"]
    tactics_map: dict[str, int] = defaultdict(int)
    for t in techniques:
        for ref in t.get("external_references", []):
            if ref.get("source_name") == "mitre-attack":
                # Kill-chain phases map to tactics
                for phase in t.get("kill_chain_phases", []):
                    if phase.get("kill_chain_name") == "mitre-attack":
                        tactics_map[phase.get("phase_name", "unknown")] += 1
    return {
        "source": "MITRE ATT&CK Enterprise",
        "url": ATTACK_URL,
        "technique_count": len(techniques),
        "tactics": dict(sorted(tactics_map.items(), key=lambda x: -x[1])),
    }


def build_moat() -> dict:
    kev = process_cisa_kev(fetch_json(CISA_KEV_URL, timeout=120))
    # MITRE ATT&CK is ~50MB; keep optional. Fetch only when explicitly requested.
    if os.environ.get("THREAT_MOAT_INCLUDE_MITRE"):
        try:
            attack = process_attack(fetch_json(ATTACK_URL, timeout=20, max_bytes=10_000_000))
        except (urllib.error.URLError, urllib.error.HTTPError, OSError, json.JSONDecodeError, RuntimeError) as e:
            logger.warning("MITRE ATT&CK fetch failed: %s", e)
            attack = {"source": "MITRE ATT&CK Enterprise", "error": str(e), "skipped": True}
    else:
        attack = {"source": "MITRE ATT&CK Enterprise", "skipped": True, "note": "set THREAT_MOAT_INCLUDE_MITRE=1 to fetch (~50MB)"}

    # Derive sim params: higher threat -> slightly higher baseline lawlessness and contagion sensitivity
    threat_pressure = kev.get("threat_pressure", 0.0)
    moat = {
        "derived_from": {
            "sources": ["CISA KEV", "MITRE ATT&CK Enterprise"],
            "catalog_ref": "~/Downloads/csoai_free_data_catalog.md",
            "note": "Public threat-intel only. No proprietary data.",
        },
        "cisa_kev": kev,
        "mitre_attack": attack,
        "indices": {
            "threat_pressure": threat_pressure,
        },
        "sim_params": {
            "baseline_lawlessness": round(0.02 + 0.10 * threat_pressure, 3),
            "contagion_step_boost": round(1.0 + 0.5 * threat_pressure, 3),
        },
    }
    if not moat_common.save_json(MOAT_PATH, moat):
        raise RuntimeError(f"Failed to write {MOAT_PATH}")
    return moat


def load_moat(default=None):
    """Load the cached threat moat JSON."""
    return moat_common.load_moat("threat", default=default)


if __name__ == "__main__":
    moat = build_moat()
    print(f"  THREAT MOAT — CISA KEV {moat['cisa_kev']['total_entries']} entries -> {MOAT_PATH}")
    print("  " + "-" * 60)
    print(f"  threat_pressure                  {moat['indices']['threat_pressure']}")
    print(f"  baseline_lawlessness             {moat['sim_params']['baseline_lawlessness']}")
    print(f"  contagion_step_boost             {moat['sim_params']['contagion_step_boost']}")
    print("  " + "-" * 60)
    print(f"  top hive hits: {list(moat['cisa_kev']['hive_hits'].items())[:5]}")
