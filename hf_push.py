"""hf_push.py — publish this session's signed artifacts to Hugging Face.

Staged and ready. Runs in ONE command the moment a token is present on this node:

    huggingface-cli login          # (owner does this once — or set HF_TOKEN)
    python3 hf_push.py             # publishes; prints exactly what landed

It reads the token via HfApi()'s own resolution (HF_TOKEN env or the CLI cache) —
this script never takes, prints, or embeds the token. If no token is available it
REFUSES and says how to add one; it never fabricates a push.

Targets the owner's own org (csoai). Publishes the signed measurement artifacts and
the MEASURED cross-lab board.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

PUSHES = [
    # (local path on the pod, dataset repo, path in repo)
    ("/runpod/article50/benchmark-results/provbench.json",          "csoai/gspc-provbench", "provbench.json"),
    ("/runpod/article50/benchmark-results/article50_oscal.json",    "csoai/gspc-provbench", "article50_oscal.json"),
    ("/runpod/article50/benchmark-results/sandbox_escape_poc.json",  "csoai/gspc-provbench", "sandbox_escape_poc.json"),
    ("/runpod/article50/council_signal_gpt2.json",                   "csoai/gspc-provbench", "council_signal_gpt2.json"),
    ("/runpod/board/board_mcp_openrouter.json",                      "csoai/gspc-boards",    "board_mcp_openrouter.json"),
]
PUBKEY_NOTE = ("sovos_ed25519 public key — verify any file offline with `python3 sign.py --verify`:\n"
               "ZnF3DZUFc5QOoy+y07rvzNUyxJgza2kUQmn1nv4S9SY=\n")


def main() -> int:
    try:
        from huggingface_hub import HfApi
    except Exception:
        print("huggingface_hub not installed: pip install huggingface_hub", file=sys.stderr)
        return 1

    api = HfApi()  # resolves HF_TOKEN env or the CLI-cached token itself
    has_token = bool(os.environ.get("HF_TOKEN") or (Path.home() / ".cache/huggingface/token").exists())
    if not has_token:
        print("NO HF TOKEN on this node. REFUSING to push (never fabricates a publish).\n"
              "  Add one first:  huggingface-cli login   (or export HF_TOKEN=...)\n"
              "  then re-run:     python3 hf_push.py", file=sys.stderr)
        return 2
    try:
        who = api.whoami().get("name")
        print(f"  hf whoami: {who}")
    except Exception as e:
        print(f"token present but whoami failed ({e}) — not pushing.", file=sys.stderr)
        return 2

    pushed, missing = [], []
    made_pubkey = set()
    for path, repo, dst in PUSHES:
        if not os.path.exists(path):
            missing.append(path)
            continue
        api.create_repo(repo, repo_type="dataset", exist_ok=True)
        api.upload_file(path_or_fileobj=path, path_in_repo=dst, repo_id=repo, repo_type="dataset")
        pushed.append(f"{repo}/{dst}")
        # publish the verification pubkey once per repo
        if repo not in made_pubkey:
            tmp = f"/tmp/SIGNING_PUBKEY.txt"
            Path(tmp).write_text(PUBKEY_NOTE)
            api.upload_file(path_or_fileobj=tmp, path_in_repo="SIGNING_PUBKEY.txt", repo_id=repo, repo_type="dataset")
            made_pubkey.add(repo)

    print("  PUSHED:")
    for p in pushed:
        print("   ", p)
    if missing:
        print("  MISSING (not on this node — not pushed):")
        for m in missing:
            print("   ", m)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
