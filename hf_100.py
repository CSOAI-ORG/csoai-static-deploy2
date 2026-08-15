#!/usr/bin/env python3
"""HF 100/100 — close every gap the 5 Aug audit found (scored 57/100).

Run:  cd ~/clawd/keystone && ./keystone run HF_TOKEN -- python3 ~/clawd/csoai-static-deploy2/hf_100.py
Idempotent, redirect-safe, deletes nothing.

WHAT THE AUDIT FOUND, AND WHAT THIS DOES

1. Four canonical repos do not exist (401): gspc-xr, gspc-det, gspc-art5, gspc-swarm.
   Two already exist under old names and are RENAMED (which also leaves a 307):
     gspc-conduct-bench -> gspc-art5      gspc-swarmbench -> gspc-swarm
   Two are created fresh with honest DRAFT/SPEC cards and no fabricated items.

2. The six MEASURED cards render only because HF auto-infers items.jsonl, and they lack
   pretty_name and the verbatim honesty register. All three are added.

3. gspc-mach and gspc-care point `default` at a RESULTS wrapper, so the viewer shows one summary
   row instead of the item set. Fixed by pointing default at the items and moving results to `runs`.

4. Six brand mirrors (coai-bench, agisafe-bench, poai-bench, asisec-bench, mcp-scoreboard,
   omai-bench) are separate live repos, and poai-bench/asisec-bench have ALREADY DIVERGED from
   their canonical twins (1 row vs 15/13). Two sources of truth for one axis is the exact failure
   this estate exists to prevent, so each mirror card is demoted to a pointer stub that names the
   canonical repo. They are NOT deleted — they carry the downloads.
"""
import os, sys, json

tok = os.environ.get("HF_TOKEN")
if not tok:
    sys.exit("No HF_TOKEN — run via: keystone run HF_TOKEN -- python3 hf_100.py")
from huggingface_hub import HfApi
api = HfApi(token=tok)
existing = set(d.id for d in api.list_datasets(author="csoai"))

REGISTER = """
## Honesty register — read before quoting anything
- **Measurement, not certification.** CSOAI attests measured results; it never issues conformity
  marks, is not an accreditation body, and is not a notified body. Nothing here is legal advice.
- **Three outcomes, never two.** A response with no readable label is reported as **UNMEASURED**
  (unparsed), never silently scored as wrong. That distinction is why this instrument exists.
- **`usable_n >= 30` gates every interval, including ours.** Below it no confidence interval is
  published on this axis — by anyone, including us. Report the n with any figure you quote.
- A score describes one model, on one frozen split, on one date. It does **not** describe any
  system's compliance with any regulation.

Issuer: CSOAI Ltd (GB, Companies House 16939677) · csoai.org
"""

# ---------- 1. renames: existing content -> canonical names ----------
for old, new in [("gspc-conduct-bench", "gspc-art5"), ("gspc-swarmbench", "gspc-swarm")]:
    o, n = f"csoai/{old}", f"csoai/{new}"
    if n in existing:
        print(f"  ⏭ {n} exists")
    elif o not in existing:
        print(f"  ⚠ {o} missing")
    else:
        api.move_repo(from_id=o, to_id=n, repo_type="dataset")
        print(f"  ✅ {old} → {new} (307 left)")
        existing.add(n)

# ---------- 2. create the two genuinely absent repos, honestly ----------
NEW = {
 "gspc-xr": ("GSPC-XR — cross-reality agent validation", "DRAFT", """# GSPC-XR — cross-reality AI validation

> **STATUS: DRAFT.** The harness runs and signs. The first `sov34` run returned **0 of 8, all
> UNMEASURED** — cold-pod timeouts, not a model score. That is reported as a failed run, not as a
> zero, and **no score is published on this axis**.

Validates an agent by what it **does** in a scenario against the law, rather than by what it says on
a frozen question set. The agent may consult the statute through a tool, then must commit a verdict,
which is graded deterministically against the EU AI Act.

Harness: `CSOAI-ORG/gspc-harness` (Apache-2.0, built on MIT `inspect_ai`).
"""),
 "gspc-det": ("GSPC-DET — watermark-detector interoperability", "SPEC", """# GSPC-DET — detector interoperability

> **STATUS: SPEC.** A published protocol, **not a measured matrix**. No score exists yet.

By **2 February 2027** the ~190 signatories of the EU Code of Practice on Transparency of
AI-generated Content commit that watermark **detection** be interoperable and meet criteria of
effectiveness, reliability, robustness and interoperability — and the Code concedes that
"common evaluation standards have yet to emerge".

This axis specifies the measurement: an **N×M interoperability matrix**, where M[i][j] is the
effectiveness of detector *j* on producer *i*'s marks. The diagonal is self-detection; the
off-diagonal is interoperability. A near-diagonal matrix means the ecosystem is not interoperable —
the finding the Code cannot currently quantify. The headline is the **off-diagonal mean**.

Producing a real matrix needs the signatories' marking tools and detectors, which is an access
question. CSOAI builds neither the marking schemes nor the detectors it measures.
"""),
}
for slug, (pretty, status, body) in NEW.items():
    rid = f"csoai/{slug}"
    if rid in existing:
        print(f"  ⏭ {rid} exists"); continue
    api.create_repo(rid, repo_type="dataset", exist_ok=True)
    card = f"""---
license: apache-2.0
pretty_name: "{pretty}"
tags: [ai-governance, benchmark, eu-ai-act, measurement]
---

{body}
{REGISTER}"""
    api.upload_file(path_or_fileobj=card.encode(), path_in_repo="README.md",
                    repo_id=rid, repo_type="dataset",
                    commit_message=f"{slug} — {status} card, no fabricated items")
    print(f"  ✅ created {rid} ({status})")

# ---------- 3. six MEASURED cards: configs + pretty_name + register ----------
MEASURED = {
 "gspc-gov": ("GSPC-GOV — EU AI Act risk-tier classification", "governance", 24),
 "gspc-agi": ("GSPC-AGI — calibrated refusal", "safety", 14),
 "gspc-prv": ("GSPC-PRV — Article 50 marking survival", "provenance", 15),
 "gspc-asi": ("GSPC-ASI — post-quantum signing agility", "continuity", 13),
 "gspc-mcp": ("GSPC-MCP — MCP tool conformance", "conformance", 11),
 "gspc-oss": ("GSPC-OSS — licence versus intended use", "openness", 13),
}
def frontmatter(pretty, items_path, extra=None):
    cfg = f"""configs:
  - config_name: default
    data_files:
      - split: train
        path: {items_path}"""
    if extra:
        cfg += f"""
  - config_name: runs
    data_files:
      - split: train
        path: {extra}"""
    return f"""---
license: apache-2.0
pretty_name: "{pretty}"
tags: [ai-governance, benchmark, eu-ai-act, measurement, nlp]
{cfg}
---
"""
for slug, (pretty, axis, n) in MEASURED.items():
    rid = f"csoai/{slug}"
    if rid not in existing:
        print(f"  ⚠ {rid} missing"); continue
    try:
        files = api.list_repo_files(rid, repo_type="dataset")
        items = "items.jsonl" if "items.jsonl" in files else next(
            (f for f in files if f.endswith((".jsonl", ".json")) and "result" not in f.lower()), None)
        if not items:
            print(f"  ⚠ {rid}: no items file found"); continue
        body = ""
        try:
            p = api.hf_hub_download(rid, "README.md", repo_type="dataset")
            raw = open(p).read()
            body = raw.split("---", 2)[2] if raw.startswith("---") and raw.count("---") >= 2 else raw
        except Exception:
            body = f"\n# {pretty}\n\nThe {axis} axis of the CSOAI GSPC suite. n = {n} frozen items.\n"
        if "usable_n" not in body:
            body = body.rstrip() + "\n" + REGISTER
        api.upload_file(path_or_fileobj=(frontmatter(pretty, items) + body).encode(),
                        path_in_repo="README.md", repo_id=rid, repo_type="dataset",
                        commit_message="Add configs, pretty_name and the honesty register")
        print(f"  ✅ {slug}: configs→{items} + pretty_name + register")
    except Exception as e:
        print(f"  ✗ {slug}: {str(e)[:70]}")

# ---------- 4. mach/care: default must be the ITEMS, results move to `runs` ----------
for slug, pretty, items, runs in [
    ("gspc-mach", "GSPC-MACH — Machinery Reg self-evolving safety functions",
     "machbench-draft.json", "machbench-results.json"),
    ("gspc-care", "GSPC-CARE — care-cost and conduct", "care_gate_eval.json", None)]:
    rid = f"csoai/{slug}"
    if rid not in existing:
        print(f"  ⚠ {rid} missing"); continue
    try:
        files = api.list_repo_files(rid, repo_type="dataset")
        if items not in files:
            print(f"  ⚠ {slug}: {items} absent — left as is"); continue
        runs = runs if runs in files else None
        p = api.hf_hub_download(rid, "README.md", repo_type="dataset")
        raw = open(p).read()
        body = raw.split("---", 2)[2] if raw.startswith("---") and raw.count("---") >= 2 else raw
        api.upload_file(path_or_fileobj=(frontmatter(pretty, items, runs) + body).encode(),
                        path_in_repo="README.md", repo_id=rid, repo_type="dataset",
                        commit_message="Point default config at the items; results move to `runs`")
        print(f"  ✅ {slug}: default→{items}" + (f", runs→{runs}" if runs else ""))
    except Exception as e:
        print(f"  ✗ {slug}: {str(e)[:70]}")

# ---------- 5. demote diverged mirrors to pointer stubs ----------
MIRRORS = {"coai-bench": "gspc-gov", "agisafe-bench": "gspc-agi", "poai-bench": "gspc-prv",
           "asisec-bench": "gspc-asi", "mcp-scoreboard": "gspc-mcp", "omai-bench": "gspc-oss"}
for old, canon in MIRRORS.items():
    rid = f"csoai/{old}"
    if rid not in existing:
        continue
    try:
        p = api.hf_hub_download(rid, "README.md", repo_type="dataset")
        raw = open(p).read()
        if "SUPERSEDED" in raw:
            print(f"  ⏭ {old} already a stub"); continue
        fm = raw.split("---")[1] if raw.startswith("---") else ""
        stub = f"""---{fm}---

# ⚠️ SUPERSEDED — use [`csoai/{canon}`](https://huggingface.co/datasets/csoai/{canon})

This repo is kept because it carries downloads and inbound links. **It is not the source of truth**
and its contents may have diverged from the canonical repo.

**The canonical, maintained item bank for this axis is
[`csoai/{canon}`](https://huggingface.co/datasets/csoai/{canon}).** Point every citation, harness
config and script there.

Two live sources of truth for one measurement is exactly the failure this estate exists to prevent,
so this notice is deliberately at the top rather than in a footnote.
{REGISTER}"""
        api.upload_file(path_or_fileobj=stub.encode(), path_in_repo="README.md",
                        repo_id=rid, repo_type="dataset",
                        commit_message=f"Demote to pointer: canonical is csoai/{canon}")
        print(f"  ✅ {old} → pointer stub → {canon}")
    except Exception as e:
        print(f"  ✗ {old}: {str(e)[:70]}")

print("\nDone. Still open (needs a data change, not a card change):")
print("  • csoai/aiact-frozen-split-harness — the model card's declared dataset does not load")
print("    (models is a keyed struct; Arrow cannot unify schemas). Flatten to a list of records.")
print("  • gspc-swarm has no items. It stays PLANNED until it has a real bank — never fabricated.")
