#!/usr/bin/env python3
"""Tick 261 SIGIL writer."""
import json, hashlib, os
from datetime import datetime, timezone

sigil = {
    "version": "0.1.0",
    "codename": "Tick261-Build",
    "tick": 261,
    "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
    "event": "defoneos.sprint.tick261.complete",
    "compartment": "csoai-defoneos",
    "operator": "JEEVES",
    "payload": {
        "mode": "build+deploy",
        "phase": 251,
        "day": 39,
        "new_packs": [
            "defoneos-hm-treasury-economic-fiscal-policy-ai-deep-dive-pack",
            "defoneos-jncc-joint-nature-conservation-committee-ai-deep-dive-pack",
            "defoneos-met-office-meteorological-services-ai-deep-dive-pack",
        ],
        "pack_bytes": {
            "hm-treasury": 36694,
            "jncc": 37648,
            "met-office": 36164,
        },
        "llm_json_bytes": {
            "hm-treasury": 2207,
            "jncc": 2195,
            "met-office": 2151,
        },
        "sitemap_added": 3,
        "sitemap_total_locs": 380,
        "sitemap_total_bytes": 79369,
        "publishable_files": 943,
        "publishable_mb": 10.2,
        "build_check": "EXIT:0  0 missing  0 leaks",
        "json_ld": "canonical schema.org verified on 3 new packs",
        "repair_sweep": {
            "scanned": 9,
            "repaired": 0,
            "note": "All 9 listed packs already canonical on disk; repair sweep correctly idempotent"
        }
    }
}

s = json.dumps(sigil, sort_keys=True, separators=(",", ":"))
sigil["hash"] = hashlib.sha256(s.encode()).hexdigest()[:16]

path = "/Users/nicholas/clawd/csoai-static-deploy2/.eat-sigils/tick-261-defoneos-2026-08-11.json"
with open(path, "w") as f:
    json.dump(sigil, f, indent=2)
print(f"Wrote SIGIL: {path}  ({os.path.getsize(path)}b)")
print(f"hash: {sigil['hash']}")
