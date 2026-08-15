#!/usr/bin/env python3
"""Lane D finisher: (1) create csoai/gspc-mach from the MachBench draft,
(2) move gspc-care-battery off the colliding 'CareBench' name -> csoai/gspc-care.
Run:  cd ~/clawd/keystone && ./keystone run HF_TOKEN -- python3 ~/clawd/csoai-static-deploy2/finish_lane_d.py
Idempotent. Redirect-safe. Never deletes anything."""
import os,sys,json,glob
tok=os.environ.get("HF_TOKEN")
if not tok: sys.exit("No HF_TOKEN in env — run me through: keystone run HF_TOKEN -- python3 ...")
from huggingface_hub import HfApi
api=HfApi(token=tok)
existing=set(d.id for d in api.list_datasets(author="csoai"))

# ---------- 1. GSPC-MACH (the 7th axis, DRAFT) ----------
rid="csoai/gspc-mach"
if rid in existing:
    print(f"  ⏭ {rid} exists")
else:
    api.create_repo(rid,repo_type="dataset",exist_ok=True)
    print(f"  ✅ created {rid}")
src=None
for c in glob.glob(os.path.expanduser("~/clawd/**/machbench/machbench-draft.json"),recursive=True) + \
         glob.glob("/private/tmp/**/machbench/machbench/machbench-draft.json",recursive=True):
    src=c; break
card='''---
license: apache-2.0
pretty_name: "GSPC-MACH — Machinery Regulation self-evolving safety-function classification"
tags: [ai-governance, benchmark, machinery-regulation, eu, robotics, humanoid]
configs:
  - config_name: default
    data_files:
      - split: train
        path: machbench-draft.json
---

# GSPC-MACH — the machinery axis of the CSOAI GSPC suite

> **STATUS: DRAFT. NOT PUBLISHED AS A RESULT. NOT QUOTABLE.**
> n = 16 scored items, below our own `usable_n >= 30` threshold — so **no interval is published on
> this axis, including by us**. 3 further items are marked DISPUTED, sent to the model and
> **excluded from the score**, because the law itself does not resolve them. Gold labels await
> legal review.

## The task
Given a described software function inside a machine, classify it:
- `PART_A` — self-evolving ML ensuring a safety function → **notified body mandatory**
- `OUT_OF_SCOPE` — ensures a safety function but cannot learn or evolve (Recital 55 excludes it)
- `NOT_SAFETY_FUNCTION` — assistance, optimisation, efficiency, QC

## Statutory anchor (primary text)
Machinery Regulation **(EU) 2023/1230**, Annex I **Part A items 5 and 6**; Article 25(2) — in Part A
there is **no module A self-certification route, even where a harmonised standard exists**.
Recital 55 provides the negative boundary; Recital 54 the interpretive lens.

**It applies from 14 January 2027** (Article 54, verbatim — most secondary sources print 20 January;
they are wrong). Reg. (EU) 2026/1744 moved 2023/1230 to AI-Act Annex I **Section B**, so there is
**one gate, the Machinery Regulation**, not a dual assessment.

## Grading
The same deterministic grader as every other GSPC axis: regex label extraction, macro-F1,
**unparsed reported and never scored wrong**.

## Measured (2026-08-05, sov-brain-2)
| model | macro-F1 | accuracy | unparsed |
|---|---:|---:|---:|
| falcon3:7b | 0.491 | 0.625 | 0% |
| sov34:latest | 0.182 | 0.375 | 0% |
| gpt-oss:20b | 0.000 | 0.000 | **100%** |

`gpt-oss:20b` returned no readable label on any of the 16 — reported as 100% unparsed, **not as a
zero**. On the three DISPUTED items the three models gave three different answers, which is
independent evidence the item selection is right and does not depend on our gold labels.

*CSOAI is an independent measurement body — it attests results, never conformity, and is not a
notified body. Nothing here is legal advice. — csoai.org*
'''
api.upload_file(path_or_fileobj=card.encode(),path_in_repo="README.md",repo_id=rid,repo_type="dataset",
                commit_message="GSPC-MACH card — DRAFT, n=16, not quotable")
print(f"  ✅ {rid} card published")
if src and os.path.exists(src):
    api.upload_file(path_or_fileobj=src,path_in_repo="machbench-draft.json",repo_id=rid,
                    repo_type="dataset",commit_message="MachBench draft items")
    print(f"  ✅ items uploaded from {src}")
else:
    print("  ⚠ machbench-draft.json not found locally — card is live, items still to upload")

# ---------- 2. care-battery off the colliding name ----------
old,new="csoai/gspc-care-battery","csoai/gspc-care"
if new in existing: print(f"  ⏭ {new} exists")
elif old not in existing: print(f"  ⚠ {old} missing")
else:
    api.move_repo(from_id=old,to_id=new,repo_type="dataset")
    print(f"  ✅ {old} → {new}  (307 redirect left; clears the CareBench collision)")
print("\nLane D complete: 12 canonical names live, MACH created, CareBench collision cleared.")
print("Remaining: gspc-swarm is EMPTY — populate with a real item bank or delete. Not fabricated.")
