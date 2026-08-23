#!/usr/bin/env python3
"""EAT ALL session close-out — write final state to repo, clean stray file."""
import os, subprocess

ROOT = "/workspace/csoai-static-deploy2"
os.chdir(ROOT)

# stray $LOG file — check content before touching (56B, likely empty artifact)
p = os.path.join(ROOT, "$LOG")
if os.path.exists(p):
    with open(p) as f:
        content = f.read().strip()
    print("$LOG content:", repr(content[:80]))
    # if it's an empty/trivial artifact from a lane, remove via git (trash-safe: add to .gitignore instead)
    with open(os.path.join(ROOT, ".gitignore"), "a") as g:
        g.write("\n$LOG\n")
        subprocess.run(["git", "add", ".gitignore"], check=False)
    print("$LOG ignored")