#!/usr/bin/env python3
"""Full surface audit: check ALL 102 deploy dirs against BOTH URL patterns.
Pattern 1: {name}.vercel.app  (strip -deploy)
Pattern 2: meok-{name%-deploy}-ai.vercel.app
Marks: LIVE (200), DEAD (no response/error), REDIRECT (3xx), OTHER (non-200).
Output: deploy-census-17jun.csv
"""

import csv
import os
import subprocess
import sys
import time
from datetime import datetime, timezone

CLAWD = os.path.expanduser("~/clawd")

def get_all_deploy_dirs():
    """Return sorted list of all *-deploy directories."""
    dirs = []
    for entry in os.listdir(CLAWD):
        full = os.path.join(CLAWD, entry)
        if os.path.isdir(full) and entry.endswith("-deploy"):
            dirs.append(entry)
    dirs.sort()
    return dirs

def strip_deploy(dirname):
    """Strip trailing -deploy from dir name."""
    if dirname.endswith("-deploy"):
        return dirname[:-7]
    return dirname

def check_url(url, timeout=5):
    """Check a URL with curl. Returns (http_code, effective_url, content_size)."""
    try:
        result = subprocess.run(
            ["curl", "-s", "-m", str(timeout), "-o", "/dev/null", "-w", "%{http_code}|%{url_effective}|%{size_download}",
             "-L", "--max-redirs", "5", url],
            capture_output=True, text=True, timeout=timeout+2
        )
        parts = result.stdout.strip().split("|")
        if len(parts) >= 3:
            code = parts[0]
            eff_url = parts[1]
            size = parts[2]
            return code, eff_url, size
        return "000", "", "0"
    except Exception as e:
        return "ERR", str(e), "0"

def classify_status(code):
    """Classify HTTP code."""
    if code == "ERR":
        return "dead"
    try:
        icode = int(code)
        if 200 <= icode < 300:
            return "live"
        elif 300 <= icode < 400:
            return "redirect"
        elif icode == 404 or icode == 410:
            return "dead"
        else:
            return f"other({icode})"
    except:
        return "dead"

def check_vercel_linked(dirpath):
    """Check if there's a .vercel dir or vercel.json."""
    has_vercel_dir = os.path.isdir(os.path.join(dirpath, ".vercel"))
    has_vercel_json = os.path.isfile(os.path.join(dirpath, "vercel.json"))
    has_project_json = os.path.isfile(os.path.join(dirpath, ".vercel", "project.json"))
    return "yes" if (has_vercel_dir or has_vercel_json) else "no"

def main():
    dirs = get_all_deploy_dirs()
    print(f"Found {len(dirs)} deploy directories.")
    
    rows = []
    
    for i, d in enumerate(dirs):
        name = strip_deploy(d)
        fullpath = os.path.join(CLAWD, d)
        vercel_linked = check_vercel_linked(fullpath)
        
        # Pattern 1: {name}.vercel.app
        url1 = f"https://{name}.vercel.app"
        code1, eff1, size1 = check_url(url1)
        status1 = classify_status(code1)
        
        # Pattern 2: meok-{name}-ai.vercel.app
        url2 = f"https://meok-{name}-ai.vercel.app"
        code2, eff2, size2 = check_url(url2)
        status2 = classify_status(code2)
        
        # Determine primary live URL
        live_urls = []
        if status1 == "live":
            live_urls.append(url1)
        if status2 == "live":
            live_urls.append(url2)
        
        live_url = "|".join(live_urls) if live_urls else "none"
        
        # Content type determination
        live_count = len(live_urls)
        if live_count == 0:
            content_type = "dead"
        elif live_count == 2:
            content_type = "enhanced"
        elif live_count == 1:
            # Check which one is live and classify
            try:
                sz = int(size1) if status1 == "live" else int(size2)
                content_type = "basic" if sz < 8000 else "enhanced"
            except:
                content_type = "basic"
        else:
            content_type = "basic"
        
        # Get best size
        best_size = size1 if status1 == "live" else (size2 if status2 == "live" else "0")
        
        row = {
            "dir": d,
            "vercel_linked": vercel_linked,
            "name": name,
            "url1": url1,
            "code1": code1,
            "status1": status1,
            "url2": url2,
            "code2": code2,
            "status2": status2,
            "live_url": live_url,
            "content_type": content_type,
            "size_bytes": best_size,
        }
        rows.append(row)
        
        # Progress
        marker = "LIVE" if live_url != "none" else "DEAD"
        print(f"[{i+1:3d}/{len(dirs)}] {d:40s} {marker:6s} | {code1:>3s} @ {url1} | {code2:>3s} @ {url2}")
        
        # Small delay to not hammer
        time.sleep(0.05)
    
    # Write CSV
    csv_path = os.path.join(CLAWD, "deploy-census-17jun.csv")
    fieldnames = ["dir", "vercel_linked", "name", "url1", "code1", "status1",
                  "url2", "code2", "status2", "live_url", "content_type", "size_bytes"]
    
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    
    # Summary
    live_count = sum(1 for r in rows if r["live_url"] != "none")
    dead_count = sum(1 for r in rows if r["live_url"] == "none")
    redirect_count = sum(1 for r in rows if r["status1"] == "redirect" or r["status2"] == "redirect")
    enhanced = sum(1 for r in rows if r["content_type"] == "enhanced")
    
    print(f"\n=== CENSUS SUMMARY ===")
    print(f"Total deploy dirs: {len(dirs)}")
    print(f"Live (at least 1 URL): {live_count}")
    print(f"Dead (no URL live): {dead_count}")
    print(f"With redirects: {redirect_count}")
    print(f"Enhanced (both URLs): {enhanced}")
    print(f"CSV written to: {csv_path}")
    
    # Print dead ones for easy reference
    dead_list = [r for r in rows if r["live_url"] == "none"]
    if dead_list:
        print(f"\n--- DEAD DEPLOYS ({len(dead_list)}) ---")
        for r in dead_list:
            print(f"  {r['dir']} | codes: {r['code1']}/{r['code2']}")
    
    return rows

if __name__ == "__main__":
    main()
