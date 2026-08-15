#!/usr/bin/env python3
"""Kaggle file descriptions — the last gap to full usability.

`kaggle datasets metadata --update` writes title/subtitle/description/licence/tags, but it does NOT
persist `resources` (per-file descriptions). Kaggle ties those to a file *version*, so they only
land via `kaggle datasets version`, which re-uploads the files alongside the metadata.

This downloads each canonical GSPC dataset to a temp dir, writes a full dataset-metadata.json
including a described resource per file, and pushes a new version. Nothing is deleted; a new
version is appended and the dataset keeps its downloads and URL.

    python3 kaggle_version_bump.py            # dry run
    python3 kaggle_version_bump.py --apply    # re-upload with descriptions

Runs one dataset at a time and cleans each temp dir immediately — the Mac is short on disk.
"""
import json, os, shutil, subprocess, sys, tempfile

APPLY = "--apply" in sys.argv
OWNER = "nicktempleman"
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kaggle_100 import AXES, build  # reuse the single source of truth for card copy

def run(cmd, cwd=None, timeout=900):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout)

def bump(slug):
    meta = build(slug)                      # title/subtitle/description/licence/tags/resources
    if not meta["resources"]:
        return f"no files listed — skipped"
    td = tempfile.mkdtemp(prefix=f"kg-{slug}-")
    try:
        d = run(["kaggle", "datasets", "download", "-d", f"{OWNER}/{slug}",
                 "-p", td, "--unzip"], timeout=900)
        if d.returncode != 0:
            return f"download failed: {(d.stdout + d.stderr).strip()[:90]}"
        on_disk = set(os.listdir(td))
        # Only describe files that actually came down; a resource path Kaggle can't find
        # rejects the whole version.
        meta["resources"] = [r for r in meta["resources"] if r["path"] in on_disk]
        if not meta["resources"]:
            return "no matching files after download — skipped"
        json.dump(meta, open(os.path.join(td, "dataset-metadata.json"), "w"), indent=1)
        if not APPLY:
            return f"would version {len(meta['resources'])} described files"
        v = run(["kaggle", "datasets", "version", "-p", td, "-r", "zip",
                 "-m", "Add per-file descriptions + canonical GSPC naming"], timeout=900)
        out = (v.stdout + v.stderr).strip()
        ok = v.returncode == 0 and "error" not in out.lower()
        return ("✅ versioned " + str(len(meta["resources"])) + " described files") if ok else f"✗ {out[:110]}"
    finally:
        shutil.rmtree(td, ignore_errors=True)   # never leave data on the Mac

def main():
    for slug in AXES:
        try:
            print(f"{slug:<18} {bump(slug)}", flush=True)
        except Exception as e:
            print(f"{slug:<18} ✗ {str(e)[:90]}", flush=True)
    if not APPLY:
        print("\nDry run. Re-run with --apply to publish versions.")

if __name__ == "__main__":
    main()
