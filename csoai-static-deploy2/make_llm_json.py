#!/usr/bin/env python3
"""make_llm_json.py — minimal llm.json generator (EAT PHASE_8_DEPLOY dependency)."""
import json, sys, glob, os, hashlib
def gen(path):
    try:
        html = open(path, encoding="utf-8", errors="replace").read()
    except Exception:
        return None
    title = ""
    t = html.split("<title>")
    if len(t) > 1: title = t[1].split("</title>")[0][:140]
    out = {"type": "LLMPageSummary", "title": title or os.path.basename(path),
           "url": "/" + os.path.relpath(path, ".").replace("\\", "/"),
           "chars": len(html), "hash": hashlib.sha256(html.encode()).hexdigest()[:16]}
    return out
if __name__ == "__main__":
    for p in sorted(glob.glob("*.html") + glob.glob("_site/*.html") + glob.glob("_dist/*.html")):
        j = gen(p)
        if j:
            out = os.path.splitext(p)[0] + ".llm.json"
            try: json.dump(j, open(out, "w"))
            except Exception: pass
    print("llm.json generated")
