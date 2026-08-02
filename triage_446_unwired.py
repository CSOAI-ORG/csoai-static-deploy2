#!/usr/bin/env python3
"""triage_446_unwired.py — module triage manifest.

Walks all *.py in ~/clawd/csoai-static-deploy2/ and writes
benchmark-results/triage_2026-07-30.json with three buckets:
  - KEEP    (imported by ≥1 other file in the estate)
  - ARCHIVE (not imported, but flagged with MODELED/RUNNING/BUILT keywords,
             or has measurable side effects via __main__)
  - DELETE  (not imported, no tag, no __main__, no docstring)

The user owns the DELETE bucket. We never auto-delete. We only enumerate.

The "446 unwired" headline in the Production Sweep refers to the broader
csoai-static-deploy2 estate (Python + JS + HTML). This script covers the
Python module subset, since that is the operational risk surface.

Usage:
    python3 triage_446_unwired.py [--output PATH]
"""
from __future__ import annotations

import ast
import json
import os
import re
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT_DEFAULT = HERE / "benchmark-results" / "triage_2026-07-30.json"

# Tag keywords for "ARCHIVE if it has any of these"
TAG_KEYWORDS = re.compile(
    r"\b(MODELED|RUNNING|BUILT|HARVEST|HONEY_PIPE|GUARD|BINDING|CARE_GATE|"
    r"PREDICTED|WRITTEN BEFORE RUNNING|selftest|GOVBENCH|EAT|DEFONEOS)\b"
)


def has_main(path: Path, tree: ast.AST) -> bool:
    """File has `if __name__ == '__main__':` block — runs as script."""
    for node in ast.walk(tree):
        if isinstance(node, ast.If):
            try:
                test = node.test
                if isinstance(test, ast.Compare):
                    left = test.left
                    if (
                        isinstance(left, ast.Name)
                        and left.id == "__name__"
                        and len(test.ops) == 1
                        and isinstance(test.ops[0], ast.Eq)
                    ):
                        comp = test.comparators[0]
                        if isinstance(comp, ast.Constant) and comp.value == "__main__":
                            return True
            except (AttributeError, IndexError):
                pass
    return False


def module_name(path: Path, root: Path) -> str:
    rel = path.relative_to(root).with_suffix("")
    parts = rel.parts
    if parts[-1] == "__init__":
        parts = parts[:-1]
    return ".".join(parts) if parts else rel.stem


def main() -> int:
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=str(HERE))
    ap.add_argument("--output", default=str(OUT_DEFAULT))
    args = ap.parse_args()

    root = Path(args.root).resolve()
    out_path = Path(args.output).resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # 1. Walk all .py files (not in .git, not in __pycache__, not in node_modules)
    py_files = []
    for p in root.rglob("*.py"):
        if any(part.startswith(".") for part in p.parts):
            continue
        if "__pycache__" in p.parts:
            continue
        if "node_modules" in p.parts:
            continue
        if "benchmark-results" in p.parts:
            continue
        if "logs" in p.parts:
            continue
        py_files.append(p)

    # 2. First pass: collect import targets from each file
    imported_by = defaultdict(set)  # module_name → set of importing file paths
    file_modules: dict[Path, str] = {}

    for p in py_files:
        try:
            tree = ast.parse(p.read_text(errors="replace"))
        except SyntaxError:
            file_modules[p] = module_name(p, root)
            continue
        file_modules[p] = module_name(p, root)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imported_by[alias.name.split(".")[0]].add(p)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imported_by[node.module.split(".")[0]].add(p)

    # 3. Second pass: classify each file
    keep, archive, delete = [], [], []

    for p in sorted(py_files):
        try:
            text = p.read_text(errors="replace")
            tree = ast.parse(text)
        except (SyntaxError, OSError):
            continue
        name = file_modules[p]
        importers = {ip for ip in imported_by.get(name, set()) if ip != p}
        # Also count importers of sibling names (foo.py is imported as foo)
        base = p.stem
        for ip in imported_by.get(base, set()):
            if ip != p:
                importers.add(ip)
        size = p.stat().st_size
        loc = text.count("\n") + 1
        has_doc = ast.get_docstring(tree) is not None
        is_main = has_main(p, tree)
        tag_matches = TAG_KEYWORDS.findall(text)
        tags = sorted(set(tag_matches))[:5]  # cap to top 5

        rec = {
            "path": str(p.relative_to(root)),
            "module": name,
            "size_bytes": size,
            "loc": loc,
            "doc": has_doc,
            "importers_count": len(importers),
            "is_main": is_main,
            "tags": tags,
        }

        if importers:
            rec["importers"] = sorted(str(ip.relative_to(root)) for ip in importers)[:5]
            keep.append(rec)
        elif is_main or tags or has_doc:
            rec["reason"] = (
                "is_main (runs as script)"
                if is_main
                else f"tagged ({', '.join(tags)})" if tags else "has docstring"
            )
            archive.append(rec)
        else:
            rec["reason"] = "no importers, no tags, no docstring, no __main__"
            delete.append(rec)

    # 4. Write manifest
    manifest = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "root": str(root),
        "total_files": len(py_files),
        "buckets": {
            "keep": {"count": len(keep), "files": keep},
            "archive": {"count": len(archive), "files": archive},
            "delete": {"count": len(delete), "files": delete},
        },
        "notes": [
            "KEEP = imported by ≥1 other file in the estate (live dependency).",
            "ARCHIVE = not imported, but tagged / has __main__ / has docstring.",
            "DELETE = not imported, no tags, no __main__, no docstring.",
            "User owns the DELETE bucket. This script never deletes anything.",
            "The '446 unwired' headline in the Production Sweep covers the broader "
            "estate (Python + JS + HTML + JSON). This script is the Python subset.",
        ],
    }
    out_path.write_text(json.dumps(manifest, indent=2))

    # 5. Print summary
    print(f"triage: {len(py_files)} .py files scanned in {root}")
    print(f"  KEEP:    {len(keep):4d}")
    print(f"  ARCHIVE: {len(archive):4d}")
    print(f"  DELETE:  {len(delete):4d}  (user owns this bucket)")
    print(f"  → {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())