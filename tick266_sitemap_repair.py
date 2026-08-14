#!/usr/bin/env python3
"""Tick 266 — repair sitemap.xml + sitemap-ai.xml: strip bogus /_site/ path prefix.

Root cause: /_site/ is the DEPLOY root (build_site.py copies root -> _site and CF
Pages serves _site). So a sitemap loc of https://csoai.org/_site/X.html resolves to
_site/_site/X.html = 404. All 393 such URLs have a valid root counterpart; stripping
the prefix makes each loc point at the real public page. Repairs without dropping any
loc count. Host (csoai.org vs www.csoai.org) left untouched — pre-existing, not a 404.
"""
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path("/Users/nicholas/clawd/csoai-static-deploy2")
SM_NS = "http://www.sitemaps.org/schemas/sitemap/0.9"


def strip_site_prefix(path):
    if not path.exists():
        print(f"  MISSING {path}")
        return 0, 0
    tree = ET.parse(path)
    root = tree.getroot()
    changed = 0
    total = 0
    for e in root.iter():
        if e.tag.endswith("loc") and e.text:
            total += 1
            if "/_site/" in e.text:
                e.text = e.text.replace("/_site/", "/")
                changed += 1
    new_text = ET.tostring(root, encoding="unicode", xml_declaration=False)
    new_text = '<?xml version="1.0" encoding="UTF-8"?>\n' + new_text
    path.write_text(new_text)
    print(f"  {path.name}: {total} locs, stripped /_site/ on {changed}, {path.stat().st_size}b")
    return total, changed


def main():
    for f in ("sitemap.xml", "sitemap-ai.xml"):
        strip_site_prefix(ROOT / f)


if __name__ == "__main__":
    main()
