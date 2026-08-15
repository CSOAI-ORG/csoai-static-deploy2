#!/usr/bin/env python3
"""kaggle_refresh.py — push the CURRENT published HF banks to Kaggle as new versions.

The Kaggle datasets were last built 08:34 (old banks). The afternoon updates — gov 24->237,
asi 13->33, prv v3, oss v2, xr v0, art5 v0 — never reached Kaggle. version_bump.py re-uploads the
OLD downloaded files; this fetches the current HF items.jsonl (cache-busted, the source of truth) and
versions each Kaggle dataset with it. Content refresh, not a metadata touch.

    python3 kaggle_refresh.py            # dry run
    python3 kaggle_refresh.py --apply    # push new versions

Disk is tight — each temp dir is cleaned immediately.
"""
import json, os, shutil, subprocess, sys, tempfile, urllib.request

APPLY = "--apply" in sys.argv
OWNER = "nicktempleman"
# kaggle dataset slug -> HF bank slug
REFRESH = {
    "gspc-govbench": "gspc-gov", "gspc-defbench": "gspc-agi", "gspc-provbench": "gspc-prv",
    "gspc-pqcbench": "gspc-asi", "gspc-mcpbench": "gspc-mcp", "gspc-ossbench": "gspc-oss",
    "gspc-conduct-bench": "gspc-art5", "gspc-xr": "gspc-xr",
}


def fetch(hf_slug):
    url = f"https://huggingface.co/datasets/csoai/{hf_slug}/raw/main/items.jsonl?cb={os.urandom(6).hex()}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0", "Cache-Control": "no-cache"})
    return urllib.request.urlopen(req, timeout=60).read().decode()


def refresh(kg_slug, hf_slug):
    try:
        body = fetch(hf_slug)
    except Exception as e:
        return f"HF fetch failed: {str(e)[:60]}"
    n = sum(1 for l in body.splitlines() if l.strip() and '"expected"' in l)
    td = tempfile.mkdtemp(prefix=f"kgr-{kg_slug}-")
    try:
        # pull existing metadata so the version keeps title/licence/description
        subprocess.run(["kaggle", "datasets", "metadata", "-d", f"{OWNER}/{kg_slug}", "-p", td],
                       capture_output=True, text=True, timeout=300)
        mp = os.path.join(td, "dataset-metadata.json")
        # FORCE a valid id regardless of what the download wrote (newer CLI omits it -> version fails)
        try:
            meta = json.load(open(mp)) if os.path.exists(mp) else {}
        except Exception:
            meta = {}
        meta["id"] = f"{OWNER}/{kg_slug}"
        meta.setdefault("title", kg_slug)
        json.dump(meta, open(mp, "w"), indent=1)
        open(os.path.join(td, "items.jsonl"), "w").write(body)
        if not APPLY:
            return f"would refresh {hf_slug} -> {kg_slug} with n={n} items"
        v = subprocess.run(["kaggle", "datasets", "version", "-p", td, "-r", "zip",
                            "-m", f"Refresh to current published bank (n={n}, from HF csoai/{hf_slug})"],
                           capture_output=True, text=True, timeout=900)
        out = (v.stdout + v.stderr).strip()
        return (f"✅ versioned n={n}" if v.returncode == 0 and "error" not in out.lower() else f"✗ {out[:110]}")
    finally:
        shutil.rmtree(td, ignore_errors=True)


def main():
    for kg, hf in REFRESH.items():
        try:
            print(f"{kg:<20} {refresh(kg, hf)}", flush=True)
        except Exception as e:
            print(f"{kg:<20} ✗ {str(e)[:80]}", flush=True)
    if not APPLY:
        print("\nDry run. --apply to push new versions.")


if __name__ == "__main__":
    main()
