#!/usr/bin/env python3
"""DEFONEOS tick 270 - probe candidate deep-dive packs (disk + sitemap) before build."""
from pathlib import Path
import re, json

ROOT = Path("/Users/nicholas/clawd/csoai-static-deploy2")
sitemap = ROOT / "sitemap.xml"
smap_text = sitemap.read_text() if sitemap.exists() else ""
locs = re.findall(r"<[^>]*loc>(.*?)</[^>]*loc>", smap_text, re.S)

packs_on_disk = sorted(p.stem for p in ROOT.glob("*deep-dive*.html"))
print(f"TOTAL deep-dive packs on disk: {len(packs_on_disk)}")
print(f"SITEMAP total locs: {len(locs)}")

# Bench candidates from tick-269 next_actions + known open bench
CANDIDATES = [
    "prime-ministers-office", "downing-street", "foreign-commonwealth-development",
    "foreign-commonwealth", "ministry-of-justice", "department-for-international-trade",
    "election-commission", "hm-passport", "home-office", "ministry-of-defence",
    "attorney-general", "cabinet-office", "treasury", "hm-revenue", "hmrc",
    "national-crime-agency", "serious-fraud-office", "environment-agency",
    "ofgem", "ofwat", "ofcom", "information-commissioner", "competition-markets-authority",
    "equality-human-rights", "charity-commission", "care-quality-commission",
    "judicial-appointments", "law-commission", "criminal-cases-review",
    "parole-board", "homes-england", "network-rail", "food-standards",
    "transport-for-london", "devolved", "scottish", "welsh", "northern-ireland",
    "house-of-commons", "house-of-lords", "parliamentary-ombudsman",
    "prison-ombudsman", "health-service-ombudsman", "uk-statistics-authority",
    "office-for-national-statistics",
]
print("\n=== DISK + SITEMAP PROBE ===")
for c in CANDIDATES:
    ondisk = len(list(ROOT.glob(f"*{c}*deep-dive*.html")))
    in_smap = sum(1 for l in locs if c in l)
    print(f"  {c:38s} disk_html={ondisk}  sitemap_hits={in_smap}")

with open("/tmp/tick270_probe.json", "w") as f:
    json.dump({"total_packs": len(packs_on_disk), "sitemap_locs": len(locs)}, f)
