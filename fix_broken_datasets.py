#!/usr/bin/env python3
"""Fix the three datasets that still fail the HF viewer — by pinning a config, not by touching data.

Run: cd ~/clawd/keystone && ./keystone run HF_TOKEN -- python3 ~/clawd/csoai-static-deploy2/fix_broken_datasets.py

THE COMMON CAUSE
HF auto-globs every data file in a repo into one `default` config. When a repo holds several files
with incompatible schemas — items beside results, or per-model results keyed by model name — Arrow
cannot unify them and the whole dataset fails to load. The fix is a `configs:` block naming ONE clean
file as `default`, with the rest under separate configs. This is the same fix that took 8 repos from
CastError to loading earlier today.

WHAT IS NOT DONE HERE
No data is rewritten and no result is altered. Where a file genuinely cannot be served (a results
archive whose schema varies per model by design), it is moved OFF the default config and the card
says so, rather than being reshaped until it looks clean.
"""
import os, sys, json

tok = os.environ.get("HF_TOKEN")
if not tok:
    sys.exit("No HF_TOKEN — run via: keystone run HF_TOKEN -- python3 fix_broken_datasets.py")
from huggingface_hub import HfApi
api = HfApi(token=tok)

REGISTER = """
## Honesty register
**Measurement, not certification.** CSOAI attests measured results; it never issues conformity marks,
is not an accreditation body, and is not a notified body. A response with no readable label is
reported as **UNMEASURED** and excluded from the denominator — never scored as wrong. No confidence
interval is published below `usable_n >= 30`, including by us. Nothing here is legal advice.

CSOAI Ltd (GB, Companies House 16939677) · csoai.org
"""

# repo -> (pretty_name, default file, {extra_config: file}, note explaining what default is)
FIX = {
 "aiact-frozen-split-harness": (
   "AI Act frozen-split harness — scenarios + runs",
   "scenarios.json",
   {"provbench_spray": "provbench_spray_2026-08-03.json",
    "dualgate_triangulation": "sov34_dualgate_triangulation_2026-08-03.json"},
   """This repo is declared by the `csoai/sov34-1p5b` model card, so it is the first thing a reviewer
opens. It previously failed to load: the per-model result files key their `models` field by model
name, so every file has a different Arrow schema and the auto-globbed `default` config could not be
unified.

`default` is now the **frozen scenario split** — the stable, uniform part, and the thing a reader
actually wants. The run archives are still here, under their own configs, unaltered. The results were
not reshaped to make them render; they are simply no longer pretending to share a schema."""),

 "gspc-airbench-eu-mandatory-run": (
   "AIRBench — EU mandatory-disclosure run",
   "eu_mandatory.jsonl",
   {"pilot": "airbench_pilot_n20.json"},
   """Previously failed with `SplitsNotFoundError`: the repo mixes a JSONL item stream, a parquet copy,
a checkpoint stream and two differently-shaped JSON result files, and the auto-globbed config could
not resolve a split.

`default` is now the EU mandatory-disclosure item stream. The pilot run sits under its own config.
`airbench_full.json` and the checkpoint stream are left in place but off the configs — they are
run artefacts with varying shape, not an item bank, and saying so is more honest than reshaping them."""),

 "lmeval-official-format": (
   "lm-eval official-format runs — INVALIDATED",
   None,   # deliberately no default: this data is retracted
   {},
   """> **⚠️ INVALIDATED — do not cite any number from this repo.**

These are lm-evaluation-harness runs that were retracted. They are kept because deleting a retracted
result hides the retraction, and this estate publishes its refutations. See `INVALIDATED.md`.

**No `default` config is declared, deliberately.** A dataset viewer that renders these numbers cleanly
would invite exactly the citation the retraction forbids. The files remain browsable in the repo for
anyone auditing what was withdrawn and why."""),
}

for slug, (pretty, default, extras, note) in FIX.items():
    rid = f"csoai/{slug}"
    try:
        files = set(api.list_repo_files(rid, repo_type="dataset"))
    except Exception as e:
        print(f"  ⚠ {rid}: {str(e)[:60]}"); continue

    if default and default not in files:
        print(f"  ⚠ {slug}: {default} absent — skipped"); continue
    extras = {k: v for k, v in extras.items() if v in files}

    if default:
        cfg = ["configs:", "  - config_name: default", "    data_files:",
               "      - split: train", f"        path: {default}"]
        for name, path in extras.items():
            cfg += [f"  - config_name: {name}", "    data_files:",
                    "      - split: train", f"        path: {path}"]
        cfg = "\n".join(cfg) + "\n"
    else:
        cfg = ""   # no viewer config at all — see the note in the card

    # keep whatever body the card already has; only replace the frontmatter
    body = ""
    try:
        p = api.hf_hub_download(rid, "README.md", repo_type="dataset")
        raw = open(p).read()
        body = raw.split("---", 2)[2] if raw.startswith("---") and raw.count("---") >= 2 else raw
    except Exception:
        pass

    card = (f"---\nlicense: apache-2.0\npretty_name: \"{pretty}\"\n"
            f"tags: [ai-governance, benchmark, eu-ai-act, measurement]\n{cfg}---\n\n"
            f"# {pretty}\n\n{note}\n")
    if body.strip() and "Honesty register" not in body:
        card += "\n---\n" + body.strip() + "\n"
    if "Honesty register" not in card:
        card += REGISTER

    api.upload_file(path_or_fileobj=card.encode(), path_in_repo="README.md",
                    repo_id=rid, repo_type="dataset",
                    commit_message="Pin a loadable config; state honestly what default is")
    shown = default or "none (retracted data — deliberately not served)"
    print(f"  ✅ {slug}: default→{shown}" + (f" +{len(extras)} config(s)" if extras else ""))

print("\nDone. Verify with:")
print("  curl -s 'https://datasets-server.huggingface.co/first-rows?dataset=csoai/aiact-frozen-split-harness&config=default&split=train'")
