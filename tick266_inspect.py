#!/usr/bin/env python3
"""Inspect what the live domain actually serves for a new pack."""
import subprocess

for u in [
    "https://csoai-site.pages.dev/defoneos-court-of-appeal-appellate-justice-ai-deep-dive-pack.html",
]:
    r = subprocess.run(["curl", "-s", "-L", "-m", "25", u], capture_output=True, text=True, timeout=30)
    body = r.stdout
    print(f"URL: {u}")
    print(f"len={len(body)}")
    print("FIRST 400 chars:")
    print(body[:400])
    print("...")
    print("contains 'Entry Point 01':", "Entry Point 01" in body)
    print("contains 'Court of Appeal AI Deep-Dive Pack':", "Court of Appeal AI Deep-Dive Pack" in body)
    print("contains '@type':", "@type" in body)
    # find DOCTYPE
    print("DOCTYPE at start:", body.lstrip().startswith("<!DOCTYPE"))
