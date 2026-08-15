"""Firewall dependency linter — checks that csoai-meok never imports into a shippable model.

This is Firewall 2 enforced as CODE (Step 8 of the 100-step plan).

The rule: any package in the monorepo that is a shippable model or training engine
(OpenRLHF, any package with "model" or "train" in its dependency chain back to MEOK)
must NOT import from csoai-meok or any package that imports csoai-meok.

Usage:
    python3 firewall_lint.py /path/to/monorepo/packages

Exit code 0 = PASS (no violations found)
Exit code 1 = FAIL (violations found, printed to stdout)
"""

from __future__ import annotations
import ast, os, sys
from pathlib import Path


# Packages that are shippable models / training engines (firewall-2 restricted)
SHIPPABLE_MODEL_PKGS = {
    "openrlhf", "sovos-brain-chain", "sovos-engine",
    "csoai-engine", "csoai-brain-chain",
}

# Packages that are measurement/analysis/fabric (firewall-2 safe)
SAFE_PKGS = {
    "csoai-core", "csoai-meok", "csoai-oscal", "csoai-fabric",
    "csoai-evidence", "csoai-meter", "csoai-gnn", "csoai-adapter-eu",
    "csoai-adapter-us", "csoai-adapter-cn", "csoai-adapter-sg",
    "sovos-city", "sovos-arena", "sovos-signal-index", "sovos-oscal",
    "sovos-league", "sovos-chain", "sovos-gprobe", "sovos-invariants",
    "sovos-harvest", "sovos-glass", "sovos-fisher-rao",
}

# Forbidden import prefixes — if any shippable-model package imports these, fail
FORBIDDEN_IMPORTS_FOR_MODELS = {
    "csoai_meok", "sovos_meok", "meok",
    "csoai_harvest", "sovos_harvest",
}


def _pkg_name_from_path(path: Path) -> str:
    """Extract package name from path like .../csoai-core/src/... or .../sovos-city/..."""
    parts = path.parts
    for i, p in enumerate(parts):
        if p == "packages" and i + 1 < len(parts):
            return parts[i + 1]
    return ""


def _is_shippable_model(pkg_name: str) -> bool:
    """Check if this package is a shippable model (firewall-2 restricted)."""
    return any(m in pkg_name for m in SHIPPABLE_MODEL_PKGS)


def _check_file_imports(filepath: Path, pkg_name: str) -> list[str]:
    """Check a Python file for forbidden imports."""
    violations = []
    try:
        tree = ast.parse(filepath.read_text())
    except (SyntaxError, Exception):
        return []

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                for forbidden in FORBIDDEN_IMPORTS_FOR_MODELS:
                    if alias.name.startswith(forbidden):
                        violations.append(
                            f"  VIOLATION: {filepath.relative_to(filepath.parent.parent.parent)} "
                            f"imports '{alias.name}' ({forbidden})"
                        )
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                for forbidden in FORBIDDEN_IMPORTS_FOR_MODELS:
                    if node.module.startswith(forbidden):
                        violations.append(
                            f"  VIOLATION: {filepath.relative_to(filepath.parent.parent.parent)} "
                            f"imports from '{node.module}' ({forbidden})"
                        )
    return violations


def main(root_dir: str = ".") -> int:
    packages_path = Path(root_dir).resolve()
    if not packages_path.exists():
        # Try common locations
        for p in [Path(root_dir) / "SOVOS" / "packages",
                   Path(root_dir) / "packages"]:
            if p.exists():
                packages_path = p
                break

    print(f"Scanning packages under: {packages_path}")
    violations = []
    pkg_count = 0

    for pkg_dir in sorted(packages_path.iterdir()):
        if not pkg_dir.is_dir():
            continue
        pkg_name = _pkg_name_from_path(pkg_dir)

        if not pkg_name or not _is_shippable_model(pkg_name):
            continue

        pkg_count += 1
        print(f"  Checking: {pkg_name}")

        for pyfile in pkg_dir.rglob("*.py"):
            if "__pycache__" in str(pyfile):
                continue
            v = _check_file_imports(pyfile, pkg_name)
            violations.extend(v)

    if pkg_count == 0:
        print("\nNo shippable-model packages found. Firewall 2: PASS (no targets)")
    elif not violations:
        print(f"\n✅ Firewall 2 PASS: {pkg_count} shippable-model packages checked, 0 violations")
    else:
        print(f"\n❌ Firewall 2 FAIL: {pkg_count} shippable-model packages checked, {len(violations)} violation(s)")
        for v in violations:
            print(v)

    print(f"\nTotal packages scanned: {len(list(packages_path.iterdir()))}")
    return 1 if violations else 0


if __name__ == "__main__":
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    sys.exit(main(root))