#!/usr/bin/env python3
"""Inject /assets/defoneos-math-check.js into every DEFONEOS pack HTML page in
_site/. Idempotent — safe to re-run. Skips files that aren't real packs (no EP
sections, no MCP chips). Counts priorities per EP from the rendered DOM rather
than parsing hero text, because the badge markup varies across pack
generations.
"""
import re
from pathlib import Path

SITE = Path("/Users/nicholas/clawd/csoai-static-deploy2/_site")
SCRIPT = '<script src="/assets/defoneos-math-check.js" defer></script>'

EP_RE = re.compile(r'id="ep\d+"')


def has_real_pack_structure(text):
    """A real DEFONEOS pack has <div class='s' id='ep1'> ... ep12> plus MCP chips."""
    if not EP_RE.search(text):
        return False
    if "MCP Servers" not in text and "MCP Tools" not in text and '"t">' not in text:
        return False
    if "Entry Point" not in text:
        return False
    return True


n_total, n_done, n_skip = 0, 0, 0
for f in sorted(SITE.glob("defoneos-*.html")):
    text = f.read_text()
    n_total += 1
    if not has_real_pack_structure(text):
        n_skip += 1
        continue
    if "defoneos-math-check.js" in text:
        n_skip += 1
        continue
    if "</body>" in text:
        text = text.replace("</body>", SCRIPT + "\n</body>", 1)
        f.write_text(text)
        n_done += 1

print(f"defoneos files scanned: {n_total}")
print(f"  injected:           {n_done}")
print(f"  skipped:            {n_skip} (not a pack, or already injected)")
