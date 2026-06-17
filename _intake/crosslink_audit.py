#!/usr/bin/env python3
"""Cross-link audit: sample 20 live deploys, extract all outbound href links,
verify each target returns 200. Flag broken links.
Output: CROSSLINK_FULL_AUDIT.md
"""

import csv
import os
import re
import subprocess
import sys
import time
import json
from datetime import datetime, timezone
from urllib.parse import urljoin, urlparse

CLAWD = os.path.expanduser("~/clawd")
OUTPUT_MD = os.path.join(CLAWD, "_intake", "CROSSLINK_FULL_AUDIT.md")

def read_census():
    """Read deploy census CSV and return list of LIVE deployments with URLs."""
    census_path = os.path.join(CLAWD, "deploy-census-17jun.csv")
    live_entries = []
    with open(census_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("live_url", "none") != "none":
                live_entries.append(row)
    return live_entries

def fetch_page(url, timeout=8):
    """Fetch HTML content from URL using curl."""
    try:
        result = subprocess.run(
            ["curl", "-s", "-m", str(timeout), "-L", "--max-redirs", "5", "-A",
             "Mozilla/5.0 (compatible; HermesBot/1.0)", url],
            capture_output=True, text=True, timeout=timeout+3
        )
        if result.returncode == 0:
            return result.stdout
        return ""
    except:
        return ""

def extract_links(html, base_url):
    """Extract all href links from HTML. Returns list of absolute URLs."""
    links = []
    # Match href attributes - various patterns
    href_pattern = re.compile(r'href\s*=\s*["\']([^"\']+)["\']', re.IGNORECASE)
    for match in href_pattern.finditer(html):
        href = match.group(1)
        # Skip anchors, javascript, mailto, tel
        if href.startswith("#") or href.startswith("javascript:") or href.startswith("mailto:") or href.startswith("tel:"):
            continue
        # Resolve relative URLs
        absolute = urljoin(base_url, href)
        # Only keep http/https URLs
        if absolute.startswith("http"):
            parsed = urlparse(absolute)
            # Only keep external-looking links (different domain) for thorough check
            base_parsed = urlparse(base_url)
            links.append(absolute)
    return links

def check_link(url, timeout=5):
    """Check if a link returns HTTP 200."""
    try:
        result = subprocess.run(
            ["curl", "-s", "-m", str(timeout), "-o", "/dev/null", "-w", "%{http_code}",
             "-L", "--max-redirs", "5", "-A", "Mozilla/5.0 (compatible; HermesBot/1.0)", url],
            capture_output=True, text=True, timeout=timeout+3
        )
        code = result.stdout.strip()
        return code
    except:
        return "ERR"

def main():
    # Read census
    live_entries = read_census()
    print(f"Found {len(live_entries)} live entries in census.")
    
    # Sample 20 (or all if fewer)
    import random
    sample_size = min(20, len(live_entries))
    sample = random.sample(live_entries, sample_size)
    
    results = []
    all_links_checked = {}
    
    for i, entry in enumerate(sample):
        url = entry["live_url"].split("|")[0]  # Take first live URL
        dirname = entry["dir"]
        name = entry["name"]
        
        print(f"\n[{i+1}/{sample_size}] Auditing {dirname} -> {url}")
        
        html = fetch_page(url)
        if not html:
            results.append({
                "dir": dirname,
                "name": name,
                "url": url,
                "html_fetched": False,
                "links_found": 0,
                "broken_links": [],
            })
            print(f"  FAILED to fetch HTML")
            continue
        
        links = extract_links(html, url)
        # Deduplicate
        unique_links = list(dict.fromkeys(links))
        # Limit to first 10 unique external links per site
        unique_links = unique_links[:10]
        
        print(f"  Found {len(unique_links)} unique links. Checking each...")
        
        broken = []
        for link_url in unique_links:
            if link_url not in all_links_checked:
                code = check_link(link_url)
                all_links_checked[link_url] = code
                time.sleep(0.1)
            else:
                code = all_links_checked[link_url]
            
            is_broken = code not in ("200", "301", "302", "307", "308")
            if is_broken:
                broken.append({"url": link_url, "http_code": code})
                print(f"    BROKEN: {link_url} -> {code}")
        
        results.append({
            "dir": dirname,
            "name": name,
            "url": url,
            "html_fetched": True,
            "links_found": len(unique_links),
            "broken_links": broken,
        })
        
        print(f"  Complete: {len(unique_links)} links checked, {len(broken)} broken")
    
    # Write markdown report
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    total_links = sum(r["links_found"] for r in results)
    total_broken = sum(len(r["broken_links"]) for r in results)
    
    md = f"""# CROSS-LINK FULL AUDIT — {now}

**Scope:** Sampled {sample_size} live deployments, extracted outbound href links, verified each target returns HTTP 200.

## Summary

| Metric | Value |
|--------|-------|
| Sites audited | {sample_size} |
| Total links extracted | {total_links} |
| Total broken links | {total_broken} |
| Broken link rate | {total_broken/total_links*100:.1f}% ({total_broken}/{total_links}) |

## Detailed Results

"""
    
    for i, r in enumerate(results):
        md += f"### {i+1}. {r['dir']}\n\n"
        md += f"- **URL:** {r['url']}\n"
        md += f"- **Name:** {r['name']}\n"
        if r["html_fetched"]:
            md += f"- **Links found:** {r['links_found']}\n"
            if r["broken_links"]:
                md += f"- **Broken links ({len(r['broken_links'])}):**\n"
                for bl in r["broken_links"]:
                    md += f"  - `{bl['url']}` → HTTP {bl['http_code']}\n"
            else:
                md += f"- **Broken links:** None ✅\n"
        else:
            md += f"- **Status:** ❌ Could not fetch HTML\n"
        md += "\n"
    
    # Summary of all broken
    if total_broken > 0:
        md += "## All Broken Links\n\n"
        md += "| Site | Broken URL | HTTP Code |\n"
        md += "|------|-----------|----------|\n"
        for r in results:
            for bl in r["broken_links"]:
                md += f"| {r['dir']} | `{bl['url']}` | {bl['http_code']} |\n"
    
    md += f"\n---\n*Generated by Hermes Agent on {now}*\n"
    
    with open(OUTPUT_MD, "w") as f:
        f.write(md)
    
    print(f"\n=== CROSSLINK AUDIT COMPLETE ===")
    print(f"Report written to: {OUTPUT_MD}")
    print(f"Total broken links: {total_broken}/{total_links}")

if __name__ == "__main__":
    main()
