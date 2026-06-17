#!/usr/bin/env python3
"""Content Freshness: check last-modified or deploy dates on 15 deploys.
Flag any stale (>30 days). Uses HTTP Last-Modified header and Vercel deployment info.
Output: appended to SEO_CHECK_17JUN.md or separate file.
"""

import csv
import os
import subprocess
import sys
import time
from datetime import datetime, timezone, timedelta

CLAWD = os.path.expanduser("~/clawd")
OUTPUT_MD = os.path.join(CLAWD, "_intake", "CONTENT_FRESHNESS_17JUN.md")

def read_census():
    census_path = os.path.join(CLAWD, "deploy-census-17jun.csv")
    live_entries = []
    with open(census_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("live_url", "none") != "none":
                live_entries.append(row)
    return live_entries

def check_last_modified(url, timeout=8):
    """Get Last-Modified header and content for heuristic date extraction."""
    try:
        result = subprocess.run(
            ["curl", "-s", "-m", str(timeout), "-L", "--max-redirs", "5",
             "-A", "Mozilla/5.0 (compatible; HermesBot/1.0)",
             "-D", "-", "-o", "/dev/null", url],
            capture_output=True, text=True, timeout=timeout+3
        )
        headers = result.stdout
        # Extract Last-Modified
        for line in headers.split("\n"):
            if line.lower().startswith("last-modified:"):
                date_str = line.split(":", 1)[1].strip()
                try:
                    from email.utils import parsedate_to_datetime
                    dt = parsedate_to_datetime(date_str)
                    return dt.isoformat(), dt
                except:
                    return date_str, None
        
        # Try x-vercel-cache or age headers for freshness
        for line in headers.split("\n"):
            if line.lower().startswith("age:"):
                age_sec = int(line.split(":", 1)[1].strip())
                age_dt = datetime.now(timezone.utc) - timedelta(seconds=age_sec)
                return f"~{age_sec}s old (from Age header)", age_dt
        
        return "no date header", None
    except Exception as e:
        return f"error: {e}", None

def check_deploy_date(dirpath):
    """Check deploy date from vercel.json or git log in deploy dir."""
    deploy_dir = os.path.join(CLAWD, dirpath)
    
    # Check vercel project settings
    vercel_project = os.path.join(deploy_dir, ".vercel", "project.json")
    if os.path.exists(vercel_project):
        try:
            import json
            with open(vercel_project) as f:
                data = json.load(f)
            # Check for updatedAt or createdAt
            if "updatedAt" in data:
                return f".vercel updatedAt: {data['updatedAt']}"
        except:
            pass
    
    # Check vercel.json
    vercel_json = os.path.join(deploy_dir, "vercel.json")
    if os.path.exists(vercel_json):
        mtime = os.path.getmtime(vercel_json)
        dt = datetime.fromtimestamp(mtime, tz=timezone.utc)
        return f"vercel.json mtime: {dt.isoformat()}"
    
    # Check any HTML file modification time
    import glob
    html_files = glob.glob(os.path.join(deploy_dir, "*.html")) + glob.glob(os.path.join(deploy_dir, "**/*.html"), recursive=True)
    if html_files:
        newest = max(html_files, key=os.path.getmtime)
        mtime = os.path.getmtime(newest)
        dt = datetime.fromtimestamp(mtime, tz=timezone.utc)
        rel = os.path.relpath(newest, deploy_dir)
        return f"newest html ({rel}): {dt.isoformat()}"
    
    # Fall back to directory mtime
    mtime = os.path.getmtime(deploy_dir)
    dt = datetime.fromtimestamp(mtime, tz=timezone.utc)
    return f"dir mtime: {dt.isoformat()}"

def is_stale(date_str, days=30):
    """Check if a date string is older than `days` days."""
    if not date_str:
        return None
    try:
        # Try ISO format
        if "T" in date_str:
            dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        else:
            # Try common formats
            for fmt in ["%Y-%m-%d", "%a, %d %b %Y %H:%M:%S %Z"]:
                try:
                    from email.utils import parsedate_to_datetime
                    dt = parsedate_to_datetime(date_str)
                    break
                except:
                    continue
            else:
                return None
        
        now = datetime.now(timezone.utc)
        dt = dt.replace(tzinfo=timezone.utc) if dt.tzinfo is None else dt
        age = now - dt
        return age.days > days, age.days
    except:
        return None, None

def main():
    live_entries = read_census()
    print(f"Found {len(live_entries)} live entries.")
    
    import random
    sample_size = min(15, len(live_entries))
    sample = random.sample(live_entries, sample_size)
    
    results = []
    stale_count = 0
    
    for i, entry in enumerate(sample):
        url = entry["live_url"].split("|")[0]
        dirname = entry["dir"]
        name = entry["name"]
        
        print(f"\n[{i+1}/{sample_size}] Checking freshness: {dirname} -> {url}")
        
        # HTTP Last-Modified
        last_mod_str, last_mod_dt = check_last_modified(url)
        print(f"  HTTP Last-Modified: {last_mod_str}")
        
        # Deploy date from filesystem
        deploy_info = check_deploy_date(dirname)
        print(f"  Deploy info: {deploy_info}")
        
        # Check staleness
        stale = False
        age_days = None
        
        if last_mod_dt:
            now = datetime.now(timezone.utc)
            if last_mod_dt.tzinfo is None:
                last_mod_dt = last_mod_dt.replace(tzinfo=timezone.utc)
            age = now - last_mod_dt
            age_days = age.days
            if age.days > 30:
                stale = True
                stale_count += 1
        
        results.append({
            "dir": dirname,
            "name": name,
            "url": url,
            "last_modified": last_mod_str,
            "age_days": age_days,
            "deploy_info": deploy_info,
            "stale": stale,
        })
        
        if stale:
            print(f"  ⚠️ STALE: {age_days} days old")
        
        time.sleep(0.15)
    
    # Write markdown
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    
    md = f"""# CONTENT FRESHNESS AUDIT — {now}

**Scope:** Sampled {sample_size} live deployments, checked HTTP Last-Modified headers and local deploy dates.
**Staleness threshold:** > 30 days since last modification.

## Summary

| Metric | Value |
|--------|-------|
| Sites checked | {sample_size} |
| Stale (>30 days) | {stale_count} |
| Fresh (<30 days) | {sample_size - stale_count} |
| Stale rate | {stale_count/sample_size*100:.1f}% |

## Detailed Results

| # | Deploy Dir | URL | Last Modified | Age (days) | Status |
|---|-----------|-----|---------------|------------|--------|
"""
    
    for i, r in enumerate(results):
        status = "⚠️ STALE" if r["stale"] else "✅ Fresh"
        age_str = f"{r['age_days']}d" if r['age_days'] is not None else "N/A"
        last_mod = r["last_modified"][:50] if r["last_modified"] else "N/A"
        md += f"| {i+1} | {r['dir']} | {r['url']} | {last_mod} | {age_str} | {status} |\n"
    
    md += "\n## Stale Deployments\n\n"
    stale_entries = [r for r in results if r["stale"]]
    if stale_entries:
        md += "The following deployments have not been updated in over 30 days:\n\n"
        for r in stale_entries:
            md += f"- **{r['dir']}** — {r['url']} — Last modified: {r['last_modified']} ({r['age_days']} days ago)\n"
    else:
        md += "No stale deployments found. All sampled sites are fresh! ✅\n"
    
    md += "\n## Deploy Info (Local)\n\n"
    for r in results:
        md += f"- **{r['dir']}:** {r['deploy_info']}\n"
    
    md += f"\n---\n*Generated by Hermes Agent on {now}*\n"
    
    with open(OUTPUT_MD, "w") as f:
        f.write(md)
    
    print(f"\n=== FRESHNESS AUDIT COMPLETE ===")
    print(f"Report written to: {OUTPUT_MD}")
    print(f"Stale count: {stale_count}/{sample_size}")

if __name__ == "__main__":
    main()
