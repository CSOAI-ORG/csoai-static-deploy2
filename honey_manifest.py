#!/usr/bin/env python3
"""honey_manifest.py — canonical per-producer manifest + integrity hash. (Moves 61-65)

The honey KB is written by multiple lanes (sov_pipeline, sov_training_honey,
bench_to_honey_kb, eat_all 8-route unify, downloads). This module is the single
place that says WHO produced WHAT and that the canonical file is byte-stable since
the last manifest. Emits forest/honey_manifest.json — the per-producer manifest.

    python3 honey_manifest.py             # emit manifest
    python3 honey_manifest.py --verify    # confirm the file hasn't drifted

Rules kept: forest/honey_all_producers.jsonl is gitignored by design (it grows every
run); the manifest is tiny and COMMITTED so drift is reviewable in git.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

FOREST = Path(__file__).resolve().parent / "forest"
HONEY = FOREST / "honey_all_producers.jsonl"
MANIFEST = FOREST / "honey_manifest.json"


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def manifest() -> dict:
    sources: Counter = Counter()
    kinds: Counter = Counter()
    broken = 0
    rows = 0
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
            sources[d.get("source", "?")] += 1
            kinds[d.get("kind", "?")] += 1
    return {
        "canonical": str(HONEY),
        "bytes": HONEY.stat().st_size,
        "sha256": _sha256(HONEY),
        "rows": rows,
        "broken_rows": broken,
        "sources": dict(sources.most_common()),
        "kinds": dict(kinds.most_common()),
        "manifest_at": __import__("datetime").datetime.now(__import__("datetime").timezone.utc)
            .strftime("%Y-%m-%dT%H:%M:%SZ"),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--verify", action="store_true")
    args = ap.parse_args()
    m = manifest()
    if args.verify:
        if not MANIFEST.exists():
            print("no manifest to verify — run honey_manifest.py first")
            return 1
        old = json.loads(MANIFEST.read_text())
        ok = old.get("sha256") == m["sha256"] and old.get("rows") == m["rows"]
        print(f"honey_manifest verify: rows {m['rows']} (was {old.get('rows')}) · "
              f"sha256 {'MATCH' if ok else 'DRIFTED'}")
        print(f"  sources: {m['sources']}")
        return 0 if ok else 1
    MANIFEST.write_text(json.dumps(m, indent=2))
    print(f"honey manifest written: {MANIFEST} ({m['rows']} rows, {len(m['sources'])} sources)")
    print(f"  sha256: {m['sha256']}")
    print(f"  sources: {m['sources']}")
    print(f"  kinds: {m['kinds']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())