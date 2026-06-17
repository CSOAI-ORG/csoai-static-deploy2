#!/usr/bin/env python3
"""SEO Check: verify sitemap.xml, robots.txt, meta description on 10 random deploys.
Output: SEO_CHECK_17JUN.md
"""

import csv
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timezone

CLAWD = os.path.expanduser("~/clawd")
OUTPUT_MD = os.path.join(CLAWD, "_intake", "SEO_CHECK_17JUN.md")

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

def fetch_url(url, timeout=8):
    """Fetch content and return (status_code, body)."""
    try:
        result = subprocess.run(
            ["curl", "-s", "-m", str(timeout), "-L", "--max-redirs", "5",
             "-A", "Mozilla/5.0 (compatible; HermesBot/1.0)", "-w", "%{http_code}",
             url],
            capture_output=True, text=True, timeout=timeout+3
        )
        # Last 3 chars are status code if we use -w
        raw = result.stdout
        # The -w appends at end, so body is everything except last 3 chars
        if len(raw) >= 3:
            code = raw[-3:]
            body = raw[:-3]
        else:
            code = raw
            body = ""
        return code, body
    except:
        return "ERR", ""

def check_sitemap(base_url):
    """Check if sitemap.xml exists."""
    sitemap_url = base_url.rstrip("/") + "/sitemap.xml"
    code, body = fetch_url(sitemap_url)
    if code == "200":
        return "present", sitemap_url, len(body)
    return f"missing (HTTP {code})", sitemap_url, 0

def check_robots(base_url):
    """Check if robots.txt exists."""
    robots_url = base_url.rstrip("/") + "/robots.txt"
    code, body = fetch_url(robots_url)
    if code == "200":
        return "present", robots_url, body[:500]
    return f"missing (HTTP {code})", robots_url, ""

def check_meta(base_url):
    """Check meta description on the page."""
    code, body = fetch_url(base_url)
    if code != "200":
        return f"page not accessible (HTTP {code})", ""
    
    # Extract meta description
    patterns = [
        r'<meta\s+name\s*=\s*["\']description["\']\s+content\s*=\s*["\']([^"\']+)["\']',
        r'<meta\s+content\s*=\s*["\']([^"\']+)["\']\s+name\s*=\s*["\']description["\']',
        r'<meta\s+property\s*=\s*["\']og:description["\']\s+content\s*=\s*["\']([^"\']+)["\']',
    ]
    for pattern in patterns:
        match = re.search(pattern, body, re.IGNORECASE)
        if match:
            desc = match.group(1)
            if len(desc) > 200:
                desc = desc[:197] + "..."
            return "present", desc
    
    return "missing", ""

def check_title(base_url):
    """Check page title."""
    code, body = fetch_url(base_url)
    if code != "200":
        return f"HTTP {code}"
    match = re.search(r'<title>([^<]+)</title>', body, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return "missing"

def main():
    live_entries = read_census()
    print(f"Found {len(live_entries)} live entries.")
    
    import random
    sample_size = min(10, len(live_entries))
    sample = random.sample(live_entries, sample_size)
    
    results = []
    
    for i, entry in enumerate(sample):
        url = entry["live_url"].split("|")[0]
        dirname = entry["dir"]
        name = entry["name"]
        
        print(f"\n[{i+1}/{sample_size}] Checking SEO: {dirname} -> {url}")
        
        # Sitemap
        sitemap_status, sitemap_url, sitemap_size = check_sitemap(url)
        print(f"  Sitemap: {sitemap_status}")
        
        # Robots.txt
        robots_status, robots_url, robots_content = check_robots(url)
        print(f"  Robots: {robots_status}")
        
        # Meta description
        meta_status, meta_desc = check_meta(url)
        print(f"  Meta desc: {meta_status}")
        
        # Title
        title = check_title(url)
        print(f"  Title: {title[:80]}")
        
        results.append({
            "dir": dirname,
            "name": name,
            "url": url,
            "sitemap_status": sitemap_status,
            "sitemap_url": sitemap_url,
            "sitemap_size": sitemap_size,
            "robots_status": robots_status,
            "robots_url": robots_url,
            "robots_content_sample": robots_content[:100] if robots_status == "present" else "",
            "meta_status": meta_status,
            "meta_desc": meta_desc,
            "title": title,
        })
        
        time.sleep(0.3)
    
    # Write markdown
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    sitemap_ok = sum(1 for r in results if r["sitemap_status"] == "present")
    robots_ok = sum(1 for r in results if r["robots_status"] == "present")
    meta_ok = sum(1 for r in results if r["meta_status"] == "present")
    title_ok = sum(1 for r in results if r["title"] not in ("missing", "") and not r["title"].startswith("HTTP"))
    
    md = f"""# SEO CHECK — {now}

**Scope:** Sampled {sample_size} live deployments, verified sitemap.xml, robots.txt, and meta description.

## Summary

| Check | Pass Rate |
|-------|-----------|
| Sitemap.xml | {sitemap_ok}/{sample_size} ({sitemap_ok/sample_size*100:.0f}%) |
| Robots.txt | {robots_ok}/{sample_size} ({robots_ok/sample_size*100:.0f}%) |
| Meta Description | {meta_ok}/{sample_size} ({meta_ok/sample_size*100:.0f}%) |
| Page Title | {title_ok}/{sample_size} ({title_ok/sample_size*100:.0f}%) |

## Detailed Results

"""
    
    for i, r in enumerate(results):
        s_icon = "✅" if r["sitemap_status"] == "present" else "❌"
        r_icon = "✅" if r["robots_status"] == "present" else "❌"
        m_icon = "✅" if r["meta_status"] == "present" else "❌"
        
        md += f"### {i+1}. {r['dir']}\n\n"
        md += f"- **URL:** {r['url']}\n"
        md += f"- **Title:** {r['title']}\n"
        md += f"- **Sitemap:** {s_icon} {r['sitemap_status']}"
        if r["sitemap_size"]:
            md += f" ({r['sitemap_size']:,} bytes)"
        md += f"\n"
        md += f"- **Robots.txt:** {r_icon} {r['robots_status']}"
        if r["robots_content_sample"]:
            md += f"\n  ```\n  {r['robots_content_sample']}\n  ```"
        md += f"\n"
        md += f"- **Meta Description:** {m_icon} {r['meta_status']}"
        if r["meta_desc"]:
            md += f" — \"{r['meta_desc']}\""
        md += "\n\n"
    
    # Recommendations
    md += "## Recommendations\n\n"
    issues = []
    if sitemap_ok < sample_size:
        issues.append(f"- **Sitemap missing on {sample_size - sitemap_ok} sites.** Add sitemap.xml for better indexing.")
    if robots_ok < sample_size:
        issues.append(f"- **Robots.txt missing on {sample_size - robots_ok} sites.** Add robots.txt to control crawler access.")
    if meta_ok < sample_size:
        issues.append(f"- **Meta description missing on {sample_size - meta_ok} sites.** Add meta descriptions for better SERP snippets.")
    
    for issue in issues:
        md += issue + "\n"
    
    if not issues:
        md += "All checks passed! ✅\n"
    
    md += f"\n---\n*Generated by Hermes Agent on {now}*\n"
    
    with open(OUTPUT_MD, "w") as f:
        f.write(md)
    
    print(f"\n=== SEO CHECK COMPLETE ===")
    print(f"Report written to: {OUTPUT_MD}")

if __name__ == "__main__":
    main()
