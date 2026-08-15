#!/usr/bin/env python3
"""Openness (GSPC-OSS) iterate cycle 2 — licence REASONING, not licence trivia.

    python3 build_oss_bank.py
    keystone run HF_TOKEN -- python3 build_oss_bank.py --publish

WHY
On the 2026-08-05 board openness was DEAD (5/7 models at ceiling): the bank asked obvious facts ("MIT
permits X") every model recites. This cycle asks the cases where good models actually split — the ones
that need reasoning about the licence's TRIGGER, not recall of its name:
  - copyleft triggers on DISTRIBUTION, not internal use (GPL); AGPL adds a NETWORK-use trigger, but only
    when there ARE other users;
  - compatibility is DIRECTIONAL (Apache-2 → GPL-3 yes; GPL-2-only + Apache-2 no);
  - "open weights" ≠ OSI-open (Llama >700M MAU, RAIL prohibited-uses, SSPL/ELv2/BSL service clauses);
  - Apache-2 NOTICE retention, CC BY-ND no-distribute-derivatives, MPL file-level copyleft.

Each item states the licence and the use; the grader asks PERMITTED / RESTRICTED. Ground truth is
defensible (FSF/OSI positions), so this is a fair discrimination test, not a contested-label set.
Whether it discriminates is the board's call — one cycle of author → measure → iterate.
"""
import json, os, sys, hashlib, random, glob, collections

PUBLISH = "--publish" in sys.argv
CANARY = "GSPC-CANARY-GUID 5e2b9a17-8d43-4c06-a1f9-csoai-oss-2026"
OUT = os.path.expanduser("~/clawd/_alignment/gspc_oss_v2")

# (label, category, text)
ITEMS = [
    # RESTRICTED — looks allowed, isn't
    ("RESTRICTED", "agpl",     "A company runs modified AGPL-3.0 software as a public hosted SaaS and does not offer the modified source to its users."),
    ("RESTRICTED", "compat",   "Distributing a single binary that statically links a GPL-2.0-only library together with Apache-2.0 code."),
    ("RESTRICTED", "weights",  "Deploying a product built on Meta's Llama 3 Community License model with 800 million monthly active users, without a separate Meta licence."),
    ("RESTRICTED", "sspl",     "Offering a managed database service built on SSPL-licensed code without releasing the service-layer source."),
    ("RESTRICTED", "cc-nc",    "Commercial use of a dataset licensed CC BY-NC 4.0."),
    ("RESTRICTED", "rail",     "Using an OpenRAIL-M model for a use listed in the licence's prohibited-uses appendix."),
    ("RESTRICTED", "elv2",     "Providing Elastic-License-2.0 software to third parties as a hosted, managed service."),
    ("RESTRICTED", "lgpl",     "Shipping a proprietary app that dynamically links an LGPL-2.1 library but technically prevents the user from replacing that library."),
    ("RESTRICTED", "bsl",      "Using BSL 1.1 software in production before its change date, for a use the Additional Use Grant does not cover."),
    ("RESTRICTED", "cc-nd",    "Creating a modified version of a CC BY-ND 4.0 work and distributing that derivative."),
    ("RESTRICTED", "gpl-dist", "Distributing a binary of GPL-3.0 software to customers while refusing to provide the corresponding source."),
    ("RESTRICTED", "notice",   "Redistributing Apache-2.0 code after deleting the required NOTICE file."),
    # PERMITTED — looks restricted, isn't
    ("PERMITTED", "gpl-internal","Modifying GPL-3.0 software and running it only internally, with no distribution, and not releasing the source."),
    ("PERMITTED", "agpl-single", "Running modified AGPL-3.0 software for a single internal user with no other users interacting with it over a network."),
    ("PERMITTED", "compat",      "Incorporating Apache-2.0 code into a GPL-3.0-licensed project."),
    ("PERMITTED", "mit",         "Using MIT-licensed code inside a closed-source proprietary product."),
    ("PERMITTED", "lgpl",        "Dynamically linking an LGPL-2.1 library from proprietary software while allowing the user to replace the library."),
    ("PERMITTED", "apache",      "Commercially deploying Apache-2.0 code and relying on its express patent grant."),
    ("PERMITTED", "mpl",         "Shipping MPL-2.0 files inside a larger proprietary product while keeping the source of the MPL-covered files available."),
    ("PERMITTED", "cc-by",       "Commercial use of a CC BY 4.0 dataset with proper attribution."),
    ("PERMITTED", "or-later",    "Using code offered as 'GPL-2.0-or-later' under the terms of GPL-3.0."),
    ("PERMITTED", "cc0",         "Any use, including commercial, of a work dedicated to the public domain under CC0."),
    ("PERMITTED", "bsd",         "Using BSD-3-Clause code in a proprietary product with attribution and without claiming endorsement."),
    ("PERMITTED", "rail-ok",     "Commercially fine-tuning and deploying an OpenRAIL model for a use that is NOT in its restricted-uses list."),
]


def main():
    items = [{"item": t, "expected": g, "category": c, "anchor": f"lic:{c}", "source": "csoai-authored",
              "note": "licence-reasoning discrimination (trigger/compatibility/scope), defensible ground truth"}
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
        res = check(train, [i["item"] for i in items])
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
pretty_name: "GSPC-OSS — open-source licence reasoning (v2)"
tags: [ai-governance, benchmark, open-source, licensing, measurement]
configs:
  - config_name: default
    data_files:
      - split: train
        path: items.jsonl
---

# GSPC-OSS v2 — licence reasoning, not licence trivia

**n = {len(public)} public** (+ {len(private)} held out privately). v1 was DEAD (5/7 models ceilinged):
it asked recitable facts. v2 asks the cases that need reasoning about the licence's **trigger** and
**scope** — copyleft on distribution vs internal use; AGPL's network trigger only when other users
exist; directional compatibility (Apache-2→GPL-3 yes, GPL-2-only+Apache-2 no); "open weights" ≠ OSI-open
(Llama MAU cap, RAIL prohibited uses, SSPL/ELv2/BSL service clauses); Apache NOTICE retention; CC BY-ND.

Grader asks PERMITTED / RESTRICTED. Ground truth follows FSF/OSI positions and is stated defensibly, so
this is a fair discrimination test. Authored (Apache-2.0), guard-clean, canary'd, private held-out split.
Whether it discriminates is the board's call — author → measure → iterate, published either way.
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
        api.upload_file(path_or_fileobj=f"{OUT}/{fn}", path_in_repo=fn, repo_id="csoai/gspc-oss",
                        repo_type="dataset", commit_message=f"v2: {len(public)} licence-reasoning items to break the ceiling")
        print(f"  ✅ pushed {fn}")
    print(f"\n  gspc-oss v2 pushed — re-run the board to see whether openness discriminates.")


if __name__ == "__main__":
    main()
