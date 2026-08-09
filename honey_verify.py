#!/usr/bin/env python3
"""honey_verify.py — verifier-class integrity bot for the honey KB. (Moves 51-55)

Runs anywhere (Mac, Oracle micro, pod): it only READS. Verifies the canonical honey
file against its committed manifest, checks schema conformance, and detects:
  - held-out contamination markers in flywheel-derived rows (the P1 law)
  - duplicate (source, kind, summary) fingerprints (re-feed signals)
Returns non-zero if any violation is found. Meant to be cron-installed on Oracle as
a verifier bot (it costs nothing and needs no GPU).

    python3 honey_verify.py            # verify against committed forest/honey_manifest.json
    python3 honey_verify.py --json     # machine-readable summary
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path

FOREST = Path(__file__).resolve().parent / "forest"
HONEY = Path(os.environ.get("HONEY_FILE", FOREST / "honey_all_producers.jsonl"))
MANIFEST = Path(os.environ.get("HONEY_MANIFEST", FOREST / "honey_manifest.json"))

# Flywheel-derived rows must never carry held-out content (flywheel.py Law 2 / P1).
HELD_OUT_MARKERS = ("held_out", "held-out", '"split": "held_out"')


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def verify() -> dict:
    issues: list[str] = []
    rows = 0
    broken = 0
    fingerprints: set[tuple] = set()
    dupes = 0

    if not HONEY.exists():
        return {"ok": False, "issues": ["honey file missing"], "rows": 0,
                "broken": 0, "dupes": 0}

    with HONEY.open() as f:
        for line in f:
            if not line.strip():
                continue
            rows += 1
            try:
                d = json.loads(line)
            except Exception:
                broken += 1
                continue
            # schema: every row needs source + kind
            if not isinstance(d, dict) or "source" not in d or "kind" not in d:
                issues.append(f"row {rows}: missing source/kind")
                continue
            # P1 law: no held-out content in fuel-derived rows
            blob = json.dumps(d)
            if any(m in blob for m in HELD_OUT_MARKERS):
                issues.append(f"row {rows}: held-out marker in honey (P1 violation)")
            # duplicate fingerprint
            fp = (d.get("source"), d.get("kind"),
                  str(d.get("summary"))[:80], str(d.get("tags"))[:80])
            if fp in fingerprints:
                dupes += 1
                if dupes <= 5:
                    issues.append(f"row {rows}: duplicate fingerprint {fp}")
            fingerprints.add(fp)

    # manifest drift
    if MANIFEST.exists():
        m = json.loads(MANIFEST.read_text())
        if m.get("rows") != rows:
            issues.append(f"manifest rows {m.get('rows')} != actual {rows}")
        if m.get("sha256") != _sha256(HONEY):
            issues.append("manifest sha256 drifted")
    else:
        issues.append("no manifest — run honey_manifest.py first")

    return {"ok": not issues, "issues": issues[:20], "rows": rows, "broken": broken,
            "dupes": dupes}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    r = verify()
    if args.json:
        print(json.dumps(r, indent=2))
    else:
        print(f"honey verify: {'OK' if r['ok'] else 'VIOLATIONS'} · rows {r['rows']} · "
              f"broken {r['broken']} · dupes {r['dupes']}")
        for i in r["issues"]:
            print(f"  ✗ {i}")
    return 0 if r["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())