#!/usr/bin/env python3
"""Canon unit decomposer — turns a research doc into 3KB units (T1-2 / G3).

Usage: python3 canon/decompose.py <doc.md> [--axis N] [--class REAL|THEORY|UNVERIFIED]

Splits on markdown headings; each section becomes a candidate unit, classed,
content-hashed, and Merkle-linked to its predecessor. Units over ~2.8KB are
split further. Output: canon/units/<doc-stem>/<id>.unit.json

Doctrine: every deliverable ships doc + units. This is the machine half of the
two-form rule. Measurement, not certification — units are verified measurement
data, never certifications.
"""
import argparse, hashlib, json, os, re, sys

def content_hash(s):
    return hashlib.sha256(s.encode()).hexdigest()[:8]

def split_doc(text):
    # split on ATX headings, keep heading with its body
    parts = re.split(r"(\n#{1,4} )", text)
    units, buf = [], ""
    for p in parts:
        if p.startswith("\n#"):
            if buf.strip():
                units.append(buf.strip())
            buf = p.strip() + "\n"
        else:
            buf += p
    if buf.strip():
        units.append(buf.strip())
    # split oversized
    out = []
    for u in units:
        while len(u) > 2800:
            cut = u.rfind("\n\n", 0, 2700)
            cut = cut if cut > 400 else 2700
            out.append(u[:cut])
            u = u[cut:]
        out.append(u)
    return [u for u in out if len(u.strip()) > 40]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("doc")
    ap.add_argument("--axis", default="meta")
    ap.add_argument("--klass", default="UNVERIFIED")
    ap.add_argument("--sources", default="")
    a = ap.parse_args()
    text = open(a.doc).read()
    stem = os.path.splitext(os.path.basename(a.doc))[0]
    outdir = os.path.join("canon", "units", stem)
    os.makedirs(outdir, exist_ok=True)
    sources = [s.strip() for s in a.sources.split(",") if s.strip()] or ["K3-internal"]
    prev = None
    n = 0
    for u in split_doc(text):
        uid = content_hash(u)
        unit = {"id": uid, "class": a.klass, "axis": a.axis, "body": u,
                "sources": sources, "links": ([prev] if prev else [])}
        json.dump(unit, open(os.path.join(outdir, uid + ".unit.json"), "w"), indent=2)
        prev = uid
        n += 1
    print(f"{n} units -> {outdir}")

if __name__ == "__main__":
    main()
