#!/usr/bin/env python3
"""Tick 259 (post-rename) — fix sitemap slugs to the -ai-deep-dive-pack convention."""
import re
from pathlib import Path

ROOT = Path("/Users/nicholas/clawd/csoai-static-deploy2")

OLD = [
    "defoneos-insolvency-service-corporate-insolvency",
    "defoneos-money-pensions-service-guidance",
    "defoneos-sports-grounds-safety-authority",
]
NEW = [
    "defoneos-insolvency-service-corporate-insolvency-ai-deep-dive-pack",
    "defoneos-money-pensions-service-guidance-ai-deep-dive-pack",
    "defoneos-sports-grounds-safety-authority-ai-deep-dive-pack",
]

for target in (ROOT / "sitemap.xml", ROOT / "sitemap-ai.xml"):
    text = target.read_text()
    for old, new in zip(OLD, NEW):
        text = text.replace(old, new)
    target.write_text(text)
    count = len(re.findall(r"<loc>", text))
    print(f"{target.name}: <loc>={count}  bytes={target.stat().st_size}")