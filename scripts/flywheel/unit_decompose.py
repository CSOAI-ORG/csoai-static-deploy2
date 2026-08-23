#!/usr/bin/env python3
"""
3KB-UNIT DECOMPOSITION ENGINE — turn canon into dense signed units.

The data-annuity mechanic: every research deliverable ships as BOTH the human
doc AND its 3KB-unit decomposition (trainable / composable / verifiable).
Each unit: id (content-hash), class (REAL/THEORY/UNVERIFIED/KILLED), axis,
body (dense finding), sources, sig.

Source: ~/Downloads/SOVOS-MASTER.md + the key finding docs. Emits units to
the living corpus (~/clawd/csoai-static-deploy2/SOVOS/living/units/).

Usage: python3 unit_decompose.py   # build units from canon key sections
       python3 unit_decompose.py --show
"""
from __future__ import annotations
import json, os, re, sys, hashlib
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
UNITS_DIR = Path.home() / "clawd/csoai-static-deploy2/SOVOS/living/units"
CANON = Path.home() / "Downloads/SOVOS-MASTER.md"
AXIS_KEYS = {
    "governance": ["Article", "EU AI Act", "high-risk", "conformity", "framework"],
    "safety": ["refus", "harm", "defense", "adversarial", "jailbreak"],
    "provenance": ["provenance", "C2PA", "signature", "watermark", "Ed25519"],
    "continuity": ["PQC", "quantum", "crypto", "ML-DSA", "sigil"],
    "conformance": ["MCP", "protocol", "conformance", "tool"],
    "openness": ["open source", "license", "MIT", "PyPI"],
    "care": ["care", "protect", "harm reduction", "Maternal"],
    "jail": ["jail", "containment", "sandbox", "escape"],
}

def ts() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def extract_sections(text: str) -> list[str]:
    """Split canon into ~3KB chunks at heading boundaries."""
    sections = []
    current = []
    for line in text.splitlines():
        if line.startswith("#") and current:
            sections.append("\n".join(current))
            current = [line]
        else:
            current.append(line)
    if current:
        sections.append("\n".join(current))
    return [s for s in sections if len(s.strip()) > 200]

def classify(body: str) -> str:
    """REAL if it cites a verifiable source; THEORY if speculative; else note."""
    if re.search(r"(verified|REAL|2026-0|http|benchmark|measured)", body, re.I):
        return "REAL"
    if re.search(r"(THEORY|should|could|proposal)", body, re.I):
        return "THEORY"
    return "UNVERIFIED"

def axis_of(body: str) -> str:
    b = body.lower()
    best, score = "meta", 0
    for ax, keys in AXIS_KEYS.items():
        s = sum(1 for k in keys if k.lower() in b)
        if s > score:
            best, score = ax, s
    return best

def build_units() -> list[dict]:
    text = CANON.read_text(errors="ignore")
    units = []
    for sec in extract_sections(text):
        # dedupe: skip tiny / skip headers-only
        if len(sec) < 200:
            continue
        body = sec.strip()[:2500]  # ~2.5KB per unit body (fits 3KB with fields)
        cls = classify(body)
        ax = axis_of(body)
        uid = hashlib.sha256(body.encode()).hexdigest()[:8]
        units.append({
            "id": uid,
            "class": cls,
            "axis": ax,
            "body": body,
            "sources": ["SOVOS-MASTER.md"],
            "sig": None,  # unsigned until keystone signs the corpus
            "ts": ts(),
        })
    return units

def main() -> int:
    units = build_units()
    UNITS_DIR.mkdir(parents=True, exist_ok=True)
    by_axis = {}
    for u in units:
        by_axis.setdefault(u["axis"], []).append(u)
    manifest = {
        "schema": "csoai.units/0.1",
        "ts": ts(),
        "count": len(units),
        "by_axis": {k: len(v) for k, v in by_axis.items()},
        "note": "3KB units from SOVOS-MASTER canon; sig field fills when keystone signs",
    }
    (UNITS_DIR / "manifest.json").write_text(json.dumps(manifest, indent=1))
    # write units as jsonl (the trainable corpus)
    with open(UNITS_DIR / "units.jsonl", "w") as f:
        for u in units:
            f.write(json.dumps(u) + "\n")
    print(f"UNITS: {len(units)} 3KB units from canon")
    for ax, n in manifest["by_axis"].items():
        print(f"  {ax}: {n}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
