"""
sovos-pyproject-aggregator.py — regenerate the [tool.setuptools] packages
list in pyproject.toml from disk reality.

Single source of truth: every directory under SOVOS/packages/ with a
src/<pkg>/__init__.py is a package. Run this to refresh pyproject.

Honest: ignores sovos.egg-info and tests/ — they are not packages.
"""
import os
import re
from pathlib import Path

REPO = Path("/Users/nicholas/clawd/csoai-static-deploy2")
PKG_ROOT = REPO / "SOVOS" / "packages"
PYPROJECT = REPO / "SOVOS" / "pyproject.toml"

# Find every package with a src/<name>/__init__.py
packages = []
for child in sorted(PKG_ROOT.iterdir()):
    if not child.is_dir():
        continue
    if child.name in ("sovos.egg-info", "tests"):
        continue
    if child.name.startswith("."):
        continue
    # conventional: src/<pkgname>/__init__.py
    src = child / "src"
    if not src.is_dir():
        continue
    # look inside src/<sub>/__init__.py (the actual layout)
    has_init = False
    for sub in src.iterdir():
        if sub.is_dir() and (sub / "__init__.py").exists():
            has_init = True
            break
    if not has_init:
        continue
    packages.append(child.name)

# dedupe
packages = sorted(set(packages))
print(f"discovered {len(packages)} packages:")
for p in packages:
    print(f"  - {p}")

# Build pyproject packages list (use single quotes for inner strings
# to avoid breaking the outer TOML double-quoted string)
pkg_lines = []
for p in packages:
    line = "    '" + p + " = { include = ['" + p + "*'], from = 'src' }'"
    pkg_lines.append(line)
new_pkgs = ',\n'.join(pkg_lines)

# Read existing pyproject
content = PYPROJECT.read_text()

# Find & replace the [tool.setuptools] packages = [...] block
pattern = re.compile(
    r"(\[tool\.setuptools\][^\[]*?packages\s*=\s*\[)([^\]]*?)(\])",
    re.DOTALL,
)
def repl(m):
    return f"{m.group(1)}\n{new_pkgs}\n{m.group(3)}"

if pattern.search(content):
    new_content = pattern.sub(repl, content, count=1)
else:
    # add a new [tool.setuptools] block before [project]
    new_content = content.replace(
        "[project]",
        f"[tool.setuptools]\npackages = [\n{new_pkgs}\n]\n\n[project]",
        1,
    )

PYPROJECT.write_text(new_content)
print(f"\nwritten {PYPROJECT}")
print(f"now has {len(packages)} packages listed")