#!/usr/bin/env python3
"""DEFONEOS tick 269 - probe candidate deep-dive packs (disk + sitemap) before build."""
from pathlib import Path
import re, json

ROOT = Path("/Users/nicholas/clawd/csoai-static-deploy2")
sitemap = ROOT / "sitemap.xml"
smap_text = sitemap.read_text() if sitemap.exists() else ""
locs = re.findall(r"<[^>]*loc>(.*?)</[^>]*loc>", smap_text, re.S)

# All deep-dive packs already on disk (by slug)
packs_on_disk = sorted(p.stem for p in ROOT.glob("*deep-dive*.html"))
print(f"TOTAL deep-dive packs on disk: {len(packs_on_disk)}")

# Probe bench candidates (from tick-267/268 next_actions + known open bench)
CANDIDATES = [
    "high-speed-2", "uk-research-and-innovation", "dstl", "defence-science",
    "prime-ministers-office", "downing-street", "home-office", "foreign-commonwealth",
    "hmrc", "department-for-work-pensions", "ministry-of-justice", "hm-passport",
    "attorney-general", "treasury", "bank-of-england", "national-crime-agency",
    "serious-fraud-office", "food-standards-agency", "environment-agency",
    "ofgem", "ofwat", "ofcom", "information-commissioner", "competition-markets-authority",
    "equality-human-rights-commission", "charity-commission", "care-quality-commission",
    "election-commission", "judicial-appointments", "law-commission",
]
print("\n=== DISK + SITEMAP PROBE ===")
for c in CANDIDATES:
    ondisk = len(list(ROOT.glob(f"*{c}*deep-dive*.html")))
    in_smap = sum(1 for l in locs if c in l)
    print(f"  {c:38s} disk_html={ondisk}  sitemap_hits={in_smap}")

with open("/tmp/tick269_probe.json", "w") as f:
    json.dump({"total_packs": len(packs_on_disk), "sitemap_locs": len(locs)}, f)
print(f"\nSITEMAP total locs: {len(locs)}")
