#!/usr/bin/env python3
"""Tick 266 SIGIL writer."""
import json, hashlib, os
from datetime import datetime, timezone

sigil = {
    "version": "0.1.0",
    "codename": "Tick266-Build",
    "tick": 266,
    "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
    "event": "defoneos.sprint.tick266.complete",
    "compartment": "csoai-defoneos",
    "operator": "JEEVES",
    "payload": {
        "mode": "build+deploy",
        "phase": 253,
        "day": 40,
        "new_packs": [
            "defoneos-court-of-appeal-appellate-justice-ai-deep-dive-pack",
            "defoneos-judicial-appointments-commission-ai-deep-dive-pack",
            "defoneos-british-academy-humanities-social-sciences-ai-deep-dive-pack",
        ],
        "pack_bytes": {
            "court-of-appeal": 34695,
            "jac": 35039,
            "british-academy": 35157,
        },
        "llm_json_bytes": {
            "court-of-appeal": 2070,
            "jac": 2309,
            "british-academy": 2153,
        },
        "sitemap_added": 3,
        "sitemap_total_locs": 787,
        "sitemap_total_bytes": 200537,
        "publishable_files": 981,
        "publishable_mb": 11.2,
        "build_check": "EXIT:0  0 real missing  0 leaks",
        "json_ld": "canonical schema.org verified on 3 new packs",
        "build_site_fix": {
            "found": "regex read 0 sitemap URLs -> vacuous 0 missing",
            "patched": "namespace-agnostic <[^>]*loc> regex",
            "repaired": "393 bogus /_site/-prefixed URLs stripped (0 unfixable)",
            "pruned": "5 genuinely non-publishable URLs (excluded dirs)",
            "result": "787 URLs, REAL 0-missing (--check EXIT 0)"
        },
        "deploy": {
            "method": "direct wrangler pages deploy _site --project-name csoai-site",
            "deployment": "e815af59",
            "new_files_uploaded": 9,
            "verified_live": "true (packs 34666/35011/35130b, llm.json served, sitemap 787)"
        }
    }
}

s = json.dumps(sigil, sort_keys=True, separators=(",", ":"))
sigil["hash"] = hashlib.sha256(s.encode()).hexdigest()[:16]

path = "/Users/nicholas/clawd/csoai-static-deploy2/.eat-sigils/tick-266-defoneos-2026-08-12.json"
with open(path, "w") as f:
    json.dump(sigil, f, indent=2)
print(f"Wrote SIGIL: {path}  ({os.path.getsize(path)}b)")
print(f"hash: {sigil['hash']}")
