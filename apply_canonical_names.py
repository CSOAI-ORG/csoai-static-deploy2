#!/usr/bin/env python3
"""Fire the canonical GSPC rename once the HF token is restored to .env (or $HF_TOKEN).
Redirect-safe: move_repo leaves a 307 at every old name. Idempotent: skips if target exists."""
import os, re, sys, glob
tok = os.environ.get("HF_TOKEN")
if not tok:
    for f in glob.glob(os.path.expanduser("~/clawd/csoai-static-deploy2/.env")) + \
             glob.glob(os.path.expanduser("~/clawd/*/.env")):
        m = re.search(r"HF_TOKEN\s*=\s*['\"]?([^'\"\n#]+)", open(f, errors="ignore").read())
        if m: tok = m.group(1).strip(); break
if not tok:
    sys.exit("No HF token found — restore it to csoai-static-deploy2/.env then re-run.")
from huggingface_hub import HfApi
api = HfApi(token=tok)
MOVES = [("gspc-govbench","gspc-gov"),("gspc-defbench","gspc-agi"),("gspc-provbench","gspc-prv"),
         ("gspc-pqcbench","gspc-asi"),("gspc-mcpbench","gspc-mcp"),("gspc-ossbench","gspc-oss")]
existing = set(d.id for d in api.list_datasets(author="csoai"))
for old, new in MOVES:
    oid, nid = f"csoai/{old}", f"csoai/{new}"
    if nid in existing: print(f"  ⏭ {nid} exists"); continue
    if oid not in existing: print(f"  ⚠ {oid} missing"); continue
    try: api.move_repo(from_id=oid, to_id=nid, repo_type="dataset"); print(f"  ✅ {old} → {new}")
    except Exception as e: print(f"  ✗ {old} → {new}: {str(e)[:80]}")
# gen-3 mirror cards → point at canonical
POINTERS = {"coai-bench":"gspc-gov","agisafe-bench":"gspc-agi","poai-bench":"gspc-prv",
            "asisec-bench":"gspc-asi","mcp-scoreboard":"gspc-mcp","omai-bench":"gspc-oss"}
for old, canon in POINTERS.items():
    rid = f"csoai/{old}"
    if rid not in existing: continue
    try:
        p = api.hf_hub_download(rid, "README.md", repo_type="dataset"); card = open(p).read()
        if f"canonical: csoai/{canon}" not in card:
            card = card.replace("---\n", f"---\n", 1)  # keep frontmatter
            card += f"\n\n> **→ Canonical repo: [`csoai/{canon}`](https://huggingface.co/datasets/csoai/{canon})** — this repo holds runs/results; the frozen items live at the canonical name.\n"
            api.upload_file(path_or_fileobj=card.encode(), path_in_repo="README.md", repo_id=rid,
                            repo_type="dataset", commit_message=f"point to canonical csoai/{canon}")
            print(f"  ↳ {old} → points to {canon}")
    except Exception as e: print(f"  ✗ pointer {old}: {str(e)[:60]}")
print("done. Next: create csoai/gspc-mach from machbench/, and rename gspc-care-battery off 'CareBench'.")
