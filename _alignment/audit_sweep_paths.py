#!/usr/bin/env python3
"""Audit sweep corruption: find rewritten filesystem paths in git diff."""
import subprocess, re

out = subprocess.run(["git", "diff"], capture_output=True, text=True).stdout
added = [l[1:] for l in out.split("\n") if l.startswith("+")]
# look for path-like strings containing internal words rewritten by sweep
patterns = [
    (r"(?i)[`\"'/].{0,40}Council OS.{0,40}[`\"'/]", "Council OS in path"),
    (r"(?i)[`\"'/].{0,40}council OS.{0,40}[`\"'/]", "council OS in path"),
    (r"(?i)\.council[/._-]", ".council path (was .sovos?)"),
    (r"(?i)council[-_][a-z]+\.(sh|py|json|yml|plist|toml)", "council-* filename (was sov-*)?"),
    (r"(?i)/root/[^ \"']+", "root path"),
    (r"(?i)~/[^ \"']+", "home path"),
]
seen = set()
for line in added:
    for pat, label in patterns:
        for m in re.findall(pat, line):
            key = (label, m[:90])
            if key not in seen:
                seen.add(key)
                print(f"[{label}] {m[:110]}")

print("---done---")