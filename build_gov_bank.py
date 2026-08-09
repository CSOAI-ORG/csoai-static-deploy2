#!/usr/bin/env python3
"""Build GSPC-GOV from the AI Act Evaluation Benchmark — the first axis that can carry an interval.

    python3 build_gov_bank.py            # build + audit locally, publish nothing
    keystone run HF_TOKEN -- python3 build_gov_bank.py --publish

WHY
  gspc-gov is n=24. Our own rule is `usable_n >= 30`, so we have never been able to publish an
  interval on our flagship axis — including for ourselves. The AI Act Evaluation Benchmark
  (NCSR "Demokritos", arXiv 2603.09435) ships 339 labelled EU AI Act scenarios:
  minimal 99 / high-risk 86 / limited 84 / prohibited 70. Verified directly against the raw file,
  not taken on trust. That clears the threshold by 10x.

LICENCE — THIS IS NOT COSMETIC
  Their data is CC-BY-4.0; their scripts are Apache-2.0. **CC-BY content cannot be relicensed as
  Apache-2.0.** Our datasets ship Apache-2.0, so the result is a DUAL-LICENCE: the items directory
  stays CC-BY-4.0 with attribution, and our harness stays Apache-2.0. Getting this wrong would make
  a licence-compliance body a licence violator, on the axis that measures licence compliance.

CONTAMINATION — THE DEFECT THIS ESTATE ALREADY SHIPPED
  sov34's headline result was 55% train-on-test: 22 of 45 eval items were verbatim in its training
  corpus, and theme-level clean n was 0. So this build refuses to write anything until the
  contamination guard passes, and it embeds the standard 2026 provenance apparatus:
    * a BIG-bench style CANARY GUID in the data file and the card, so future crawlers can exclude it
    * a PRIVATE HELD-OUT split that is never published
    * the source, licence and attribution recorded in the card itself
"""
import json, os, sys, hashlib, urllib.request, random, collections

PUBLISH = "--publish" in sys.argv
SRC = "https://raw.githubusercontent.com/davidath/ai-act-evaluation-benchmark/main/scenarios.json"
CITE = ("AI Act Evaluation Benchmark — NCSR \"Demokritos\" (arXiv:2603.09435). "
        "Scenario data CC-BY-4.0. https://github.com/davidath/ai-act-evaluation-benchmark")
# A canary is only useful if it is unique and never changes. Fixed here, deliberately.
CANARY = "GSPC-CANARY-GUID a4f1c2e8-7b3d-4e91-9c02-csoai-gov-2026"
OUT = os.path.expanduser("~/clawd/_alignment/gspc_gov_v2")

# Their labels -> ours. Both are the AI Act's own four tiers, so this is a rename, not a judgement.
MAP = {"prohibited": "PROHIBITED", "high-risk": "HIGH_RISK",
       "limited": "LIMITED_RISK", "minimal": "MINIMAL_RISK"}


def fetch():
    raw = urllib.request.urlopen(urllib.request.Request(
        SRC, headers={"User-Agent": "Mozilla/5.0"}), timeout=90).read()
    d = json.loads(raw)
    if isinstance(d, list):
        return d
    # The file is {"license": ..., "data": [...]}. A naive list(d.values())[0] grabs the licence
    # STRING and then fails on .get() — pick the payload explicitly rather than positionally.
    for k in ("data", "scenarios", "items"):
        if isinstance(d.get(k), list):
            return d[k]
    raise SystemExit(f"unrecognised structure: top-level keys {list(d)}")


def to_item(r, i):
    """One scenario -> one item. The scenario text is composed from the source's own structured
    fields rather than invented, so the item is traceable to its row."""
    bits = []
    if r.get("role"): bits.append(f"A {str(r['role']).lower()} deploys")
    if r.get("system_type"): bits.append(str(r["system_type"]))
    if r.get("intended_use"): bits.append(f"intended for {r['intended_use']}")
    if r.get("domain"): bits.append(f"in the {r['domain']} domain")
    if r.get("input_data"): bits.append(f"using {r['input_data']}")
    scenario = " ".join(bits).strip()
    if not scenario.endswith("."): scenario += "."
    gold = MAP.get(str(r.get("risk_level", "")).strip().lower())
    if not gold or len(scenario) < 25:
        return None
    arts = r.get("related_articles")
    anchor = (", ".join(map(str, arts)) if isinstance(arts, list) else str(arts or "")) or gold
    return {"scenario": scenario, "expected": gold, "anchor": anchor,
            "source_index": i, "source": "ai-act-evaluation-benchmark", "licence": "CC-BY-4.0"}


def main():
    rows = fetch()
    items = [it for it in (to_item(r, i) for i, r in enumerate(rows)) if it]
    dist = collections.Counter(i["expected"] for i in items)
    print(f"source rows {len(rows)} -> usable items {len(items)}")
    print(f"  distribution: {dict(dist)}")
    if len(items) < 30:
        sys.exit("Fewer than 30 usable items — refusing to build; the whole point was clearing usable_n.")

    # --- contamination gate: run BEFORE writing anything ---
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from contamination_guard import check
        # check(training_texts, bank_items). The question is whether OUR training corpora already
        # contain these scenarios — if they do, importing them would hand us a pre-contaminated
        # bank and we would have imported the exact defect we are fixing.
        import glob
        train_texts = []
        for pat in ("~/projects/coai-dashboard/gpu-offload/**/*.json*",
                    "~/clawd/csoai-static-deploy2/*training*.jsonl",
                    "~/clawd/csoai-static-deploy2/training_data/**/*.json*",
                    "~/clawd/csoai-static-deploy2/forest/**/*.jsonl"):
            for fp in glob.glob(os.path.expanduser(pat), recursive=True):
                try:
                    for line in open(fp, errors="ignore"):
                        line = line.strip()
                        if line:
                            train_texts.append(line)
                except Exception:
                    pass
        res = check(train_texts, [i["scenario"] for i in items])
        flagged = getattr(res, "contaminated", None)
        n_bad = len(flagged) if flagged is not None else 0
        print(f"  contamination guard: {len(train_texts)} training rows scanned · {n_bad} item(s) flagged")
        if len(train_texts) < 100:
            sys.exit(f"GUARD DID NOT RUN: only {len(train_texts)} training rows found. A guard that "
                     "scans nothing and reports 'clean' is a false pass. Fix the corpus paths.")
        if n_bad:
            sys.exit(f"CONTAMINATED: {n_bad} of the imported items already appear in our training data. "
                     "Importing them would pre-contaminate the new bank. Fix before building.")
    except ImportError:
        print("  ⚠ contamination_guard not importable — build continues but the guard did NOT run.")
        print("    That is a gap, not a pass. Do not publish until it has.")
        if PUBLISH:
            sys.exit("Refusing to publish without the contamination guard.")
    except Exception as e:
        sys.exit(f"CONTAMINATION GUARD FAILED: {e}")

    # --- public / private split. The private half is the point: a bank that is entirely public
    # --- cannot stay uncontaminated once anyone trains on it.
    rnd = random.Random(42)                             # fixed seed: the split is reproducible
    shuffled = items[:]; rnd.shuffle(shuffled)
    cut = int(len(shuffled) * 0.70)
    public, private = shuffled[:cut], shuffled[cut:]

    os.makedirs(OUT, exist_ok=True)
    with open(f"{OUT}/items.jsonl", "w") as f:
        f.write(json.dumps({"_canary": CANARY, "_note":
                "Canary row. If this string appears in a model's training data, this benchmark is "
                "contaminated for that model. Exclude this file from training corpora."}) + "\n")
        for it in public: f.write(json.dumps(it) + "\n")
    with open(f"{OUT}/items_heldout_PRIVATE.jsonl", "w") as f:
        for it in private: f.write(json.dumps(it) + "\n")

    card = f"""---
license: cc-by-4.0
pretty_name: "GSPC-GOV — EU AI Act risk-tier classification (v2)"
tags: [ai-governance, benchmark, eu-ai-act, measurement, nlp]
configs:
  - config_name: default
    data_files:
      - split: train
        path: items.jsonl
---

# GSPC-GOV v2 — EU AI Act risk-tier classification

**n = {len(public)} public** (+ {len(private)} held out privately and never published).
Previous version was n=24, below our own `usable_n >= 30` rule — so **no interval had ever been
published on this axis, including by us**. This version clears it.

Distribution (public split): {dict(collections.Counter(i['expected'] for i in public))}

## Licence — dual, and deliberately so
The **items are CC-BY-4.0**, derived from the {CITE}
CC-BY content **cannot** be relicensed as Apache-2.0, so the items keep CC-BY-4.0 while the CSOAI
harness that runs them remains Apache-2.0. Attribution above is required by that licence and is not
optional.

## Contamination apparatus
- **Canary**: the first row carries `{CANARY}`. If that string appears in a model's training data,
  this benchmark is contaminated for that model. Please exclude this file from training corpora.
- **Private held-out split**: {len(private)} items are withheld. A benchmark that is entirely public
  cannot stay uncontaminated once anyone trains on it.
- **Guard**: `contamination_guard.py` fails on any overlap between a training corpus and an eval
  bank, by THEME rather than by row — a held-out row still leaks if a near-duplicate of it was
  trained on. This exists because a prior estate result was 55% train-on-test and the theme-level
  clean n was zero.

## Grading
Deterministic: regex label extraction, macro-F1. No model judges another model. A response with no
readable label is reported as **UNMEASURED** and excluded from the denominator — never scored as
wrong.

## Honesty register
Measurement, not certification. CSOAI attests measured results; it never issues conformity marks, is
not an accreditation body, and is not a notified body. A score describes one model, on one frozen
split, on one date — it does not describe any system's compliance with any regulation. Nothing here
is legal advice.

CSOAI Ltd (GB, Companies House 16939677) · csoai.org
"""
    open(f"{OUT}/README.md", "w").write(card)
    open(f"{OUT}/NOTICE", "w").write(
        "This dataset contains material from:\n\n  " + CITE +
        "\n\nUsed under CC-BY-4.0. Modifications: scenarios composed from the source's structured\n"
        "fields into single-sentence prompts; risk_level mapped to the CSOAI label set; split into\n"
        "public and private held-out sets.\n")

    sha = hashlib.sha256(open(f"{OUT}/items.jsonl", "rb").read()).hexdigest()[:16]
    print(f"\n  public {len(public)} · private held-out {len(private)} · sha256:{sha}")
    print(f"  → {OUT}")

    if not PUBLISH:
        print("\nBuilt locally. Re-run with --publish (via keystone) to push to HF.")
        return

    tok = os.environ.get("HF_TOKEN")
    if not tok:
        sys.exit("No HF_TOKEN — run via: keystone run HF_TOKEN -- python3 build_gov_bank.py --publish")
    from huggingface_hub import HfApi
    api = HfApi(token=tok)
    rid = "csoai/gspc-gov"
    for fn in ("items.jsonl", "README.md", "NOTICE"):
        api.upload_file(path_or_fileobj=f"{OUT}/{fn}", path_in_repo=fn, repo_id=rid,
                        repo_type="dataset",
                        commit_message=f"v2: n={len(public)} from AI Act Evaluation Benchmark (CC-BY-4.0)")
        print(f"  ✅ pushed {fn}")
    print(f"\n  gspc-gov is now n={len(public)} — the first axis able to carry an interval.")
    print("  The private held-out split was NOT uploaded, by design.")


if __name__ == "__main__":
    main()
