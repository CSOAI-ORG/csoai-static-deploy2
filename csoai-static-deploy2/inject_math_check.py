#!/usr/bin/env python3
"""inject_math_check.py — minimal math-sanity injector (EAT PHASE_8_DEPLOY dependency)."""
import json, glob, os, re
def check(path):
    try: html = open(path, encoding="utf-8", errors="replace").read()
    except Exception: return None
    # detect common miscalculation patterns (honest check, no claim)
    hits = re.findall(r"\d+\s*[+\-*/]\s*\d+\s*=\s*\d+", html)
    bad = [h for h in hits if not eval(h.replace("=", "=="))] if hits else []
    return {"page": path, "math_expressions": len(hits), "suspicious": len(bad)}
for p in sorted(glob.glob("*.html") + glob.glob("_site/*.html") + glob.glob("_dist/*.html")):
    r = check(p)
    if r and r["suspicious"]: print("  !", r)
print("math check complete")
