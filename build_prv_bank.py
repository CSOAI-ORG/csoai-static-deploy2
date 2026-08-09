#!/usr/bin/env python3
"""Revive GSPC-PRV — a provenance axis that discriminates.

    python3 build_prv_bank.py            # build + audit locally
    keystone run HF_TOKEN -- python3 build_prv_bank.py --publish

WHY
SOPHOS's discrimination eye flagged provenance DEAD on the cross-company board (spread < 0.15). The
old bank paired obvious cases — "screenshot → DESTROYED", "byte-copy → SURVIVES" — which every model
gets by keying on the OPERATION NAME. That measures nothing.

WHAT DISCRIMINATES
Whether an Article 50 / C2PA marking survives depends on the TOOL'S C2PA-AWARENESS, not the operation.
The same operation gives opposite answers:
  * re-encode by a C2PA-aware tool that re-signs  → SURVIVES
  * re-encode by a C2PA-unaware tool              → DESTROYED (container rewritten, manifest dropped)
A model that pattern-matches "any transform = destroyed" or "any copy = survives" fails on exactly
these pairs. So the bank is built as matched pairs where the surface operation is identical and only
the manifest mechanics differ — forcing the model to reason about the binding, not the verb.

Ground truth (C2PA 2.x): a manifest survives iff the bytes are preserved (faithful copy/transport/
lossless archive) OR a C2PA-aware tool migrates and re-signs it; it is destroyed iff the container is
rewritten by an unaware tool, the metadata store is stripped, a new file is created (screenshot,
print-scan, re-embed), or pixels change without a re-sign.

Authored here (Apache-2.0, no third-party data), contamination-guarded, canary'd, public/private split.
"""
import json, os, sys, hashlib, random, glob, collections

PUBLISH = "--publish" in sys.argv
CANARY = "GSPC-CANARY-GUID c3f8a1d6-9e24-4b73-a5c1-csoai-prv-2026"
OUT = os.path.expanduser("~/clawd/_alignment/gspc_prv_v2")

# v3 — the HARD principle: SURVIVES iff a validator reports a VALID, bound Content Credential. A manifest
# that is merely PRESENT but whose binding/signature no longer validates has NOT survived. These items
# trip the pattern-match "a manifest is attached, so it survived". v2 (matched awareness pairs) was
# measured DEAD (frontier models aced 0.93-1.0); this cycle targets present-but-invalid vs valid-despite-transform.
ITEMS = [
    # present-but-INVALID → DESTROYED (the counterintuitive core)
    ("DESTROYED", "stale-binding", "A tool copies the C2PA manifest block byte-for-byte into a re-encoded JPEG but does not re-sign; the hard-binding hash no longer matches the new pixels."),
    ("DESTROYED", "stale-binding", "A C2PA-aware editor changes pixels and saves without re-signing, leaving the prior manifest attached to content it no longer describes."),
    ("DESTROYED", "stripped",      "The image bytes are unchanged, but the XMP packet carrying the manifest was removed by a metadata optimizer."),
    ("DESTROYED", "soft-binding",  "A manifest with only a soft (metadata-reference) binding, after the file is re-encoded so its embedded metadata is dropped."),
    ("DESTROYED", "tamper",        "The manifest is present and its hard binding matches, but the claim signature was altered so it no longer verifies."),
    ("DESTROYED", "derivative",    "A thumbnail is extracted from a marked asset; the thumbnail carries no manifest of its own."),
    ("DESTROYED", "external",      "A manifest references an external cloud manifest that has since been deleted, so it no longer resolves."),
    ("DESTROYED", "flatten",       "A PDF containing a C2PA-marked image is flattened to a new raster; the image's manifest is not carried into the output."),
    ("DESTROYED", "metadata-rw",   "A tool adds an IPTC caption by rewriting the container, breaking the signed content hash."),
    ("DESTROYED", "capture",       "A full-resolution screenshot of the asset is shared — a new file sampled from the framebuffer, with no manifest."),
    ("DESTROYED", "analogue",      "The image is printed and rescanned at high DPI."),
    ("DESTROYED", "reencode",      "A batch converter with no C2PA support re-encodes the JPEG and writes only pixels to the new container."),
    # valid-DESPITE-transform → SURVIVES (aware re-sign, or byte-faithful, or valid lineage)
    ("SURVIVES", "resign-crop",    "A C2PA-aware editor crops the image, appends an edit assertion, and re-signs, updating the hard binding to the new pixels."),
    ("SURVIVES", "resign-transcode","A transcode pipeline that is C2PA-aware migrates the manifest into the new container and re-signs it."),
    ("SURVIVES", "resign-rotate",  "The file is losslessly rotated by a tool that recomputes and re-signs the hard binding."),
    ("SURVIVES", "byte-faithful",  "The exact bytes are copied to another filesystem; the embedded manifest and its hard binding are untouched."),
    ("SURVIVES", "container",      "The asset is embedded unchanged into a BMFF container with its manifest box intact and bytes preserved."),
    ("SURVIVES", "lineage",        "A C2PA-aware CDN re-encodes to WebP and re-signs a fresh manifest binding the new rendition, recording the original as an ingredient; a validator reports a valid Content Credential with lineage."),
    ("SURVIVES", "supersede",      "An image is edited in a C2PA tool that supersedes the original claim with a new signed manifest referencing the original as an ingredient; a validator reports a valid, bound credential."),
    ("SURVIVES", "soft-resolves",  "A soft-binding manifest whose referenced asset is delivered unchanged over a metadata-preserving channel."),
    ("SURVIVES", "archive",        "A C2PA-aware archive tool stores and restores the asset byte-identically, manifest and binding intact."),
    ("SURVIVES", "resign-format",  "An asset is re-signed after a lossless format change by a tool that migrates the manifest and updates the hard binding to the new bytes."),
    ("SURVIVES", "hardbind-ok",    "A validator recomputes the content hash after a metadata-only change applied without rewriting the pixels, and the hard binding still matches."),
    ("SURVIVES", "faithful-copy",  "The file is copied to another folder with the operating system's byte-faithful copy."),
]


def main():
    items = [{"operation": t, "expected": g, "category": c, "source": "csoai-authored",
              "note": "authored to discriminate on C2PA manifest mechanics, not operation name"}
             for g, c, t in ITEMS]
    dist = collections.Counter(i["expected"] for i in items)
    print(f"authored items: {len(items)} · {dict(dist)}")

    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from contamination_guard import check
        train = []
        for pat in ("~/projects/coai-dashboard/gpu-offload/**/*.json*",
                    "~/clawd/csoai-static-deploy2/*training*.jsonl"):
            for fp in glob.glob(os.path.expanduser(pat), recursive=True):
                try: train += [l.strip() for l in open(fp, errors="ignore") if l.strip()]
                except Exception: pass
        if len(train) < 100:
            sys.exit(f"GUARD DID NOT RUN: {len(train)} rows — a scan of nothing is a false pass.")
        res = check(train, [i["operation"] for i in items])
        n_bad = len(getattr(res, "contaminated", []) or [])
        print(f"  contamination guard: {len(train)} rows scanned · {n_bad} flagged")
        if n_bad: sys.exit(f"CONTAMINATED: {n_bad} authored items already in training. Rewrite them.")
    except ImportError:
        if PUBLISH: sys.exit("Refusing to publish without the contamination guard.")
        print("  ⚠ guard not importable — not a pass.")

    rnd = random.Random(42); sh = items[:]; rnd.shuffle(sh)
    cut = int(len(sh) * 0.70); public, private = sh[:cut], sh[cut:]
    os.makedirs(OUT, exist_ok=True)
    with open(f"{OUT}/items.jsonl", "w") as f:
        f.write(json.dumps({"_canary": CANARY}) + "\n")
        for it in public: f.write(json.dumps(it) + "\n")
    with open(f"{OUT}/items_heldout_PRIVATE.jsonl", "w") as f:
        for it in private: f.write(json.dumps(it) + "\n")

    card = f"""---
license: apache-2.0
pretty_name: "GSPC-PRV — Article 50 marking survival, validity principle (v3)"
tags: [ai-governance, benchmark, eu-ai-act, provenance, c2pa, measurement]
configs:
  - config_name: default
    data_files:
      - split: train
        path: items.jsonl
---

# GSPC-PRV v3 — provenance survival by validity, not by presence

**n = {len(public)} public** (+ {len(private)} held out privately). v2 was measured **DEAD** — frontier
models aced the C2PA-awareness matched pairs at 0.93–1.0. v3 targets the harder, correct principle.

## What this measures
A marking **SURVIVES only if a validator would report a VALID Content Credential bound to the asset**;
a manifest that is merely **present but whose hard binding or signature no longer validates has NOT
survived**. Items pit *present-but-invalid* cases (a manifest copied verbatim into re-encoded pixels;
pixels changed without a re-sign; a broken content hash; a tampered signature; an unresolvable external
manifest) against *valid-despite-transform* cases (aware re-sign after crop/transcode/rotate;
byte-faithful copy; valid lineage via ingredient). A model that pattern-matches "a manifest is attached,
so it survived" fails the present-but-invalid half.

The grading instruction states this validity rule explicitly, so the labels are defensible (not a
contested-label set). Whether v3 discriminates is an empirical question answered by the board — this is
one cycle of author → measure → iterate, published honestly whichever way it lands.

## Provenance
Authored by CSOAI (Apache-2.0, no third-party data), disjoint from published benchmarks by
construction. Canary GUID in row 1; {len(private)} held back privately. Contamination guard confirmed
zero overlap with our training corpora before publication.

## Grading
Deterministic SURVIVES/DESTROYED extraction. Unreadable → **UNMEASURED**, excluded, never scored wrong.

## Honesty register
Measurement, not certification. n is below usable_n=30 until the bank grows; report the n with any
figure. Nothing here is legal advice. CSOAI Ltd (GB, Companies House 16939677) · csoai.org
"""
    open(f"{OUT}/README.md", "w").write(card)
    sha = hashlib.sha256(open(f"{OUT}/items.jsonl", "rb").read()).hexdigest()[:16]
    print(f"\n  public {len(public)} · private {len(private)} · sha256:{sha}\n  → {OUT}")
    if not PUBLISH:
        print("\nBuilt locally. --publish via keystone to push."); return
    tok = os.environ.get("HF_TOKEN")
    if not tok: sys.exit("No HF_TOKEN.")
    from huggingface_hub import HfApi
    api = HfApi(token=tok)
    for fn in ("items.jsonl", "README.md"):
        api.upload_file(path_or_fileobj=f"{OUT}/{fn}", path_in_repo=fn, repo_id="csoai/gspc-prv",
                        repo_type="dataset", commit_message=f"v2: {len(public)} discriminating items (matched C2PA pairs)")
        print(f"  ✅ pushed {fn}")
    print(f"\n  gspc-prv revived: {len(public)} matched-pair items. Re-measure to confirm spread recovers.")


if __name__ == "__main__":
    main()
