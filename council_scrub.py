#!/usr/bin/env python3
"""council_scrub.py — rename Sov* product CODENAMES → Council on the public site.

Bucket ① only. DRY-RUN by default; pass --apply to write.

DOES:   display product names — "Sov City 3D" → "Council City 3D", "Sovereign OS" → "Council OS", etc.
SKIPS:  (a) descriptive "Sovereign AI / UK-sovereign / Sovereign Public …" (bucket ③, counsel-pending)
        (b) code/dir/package names in <code> or URLs — sovos-arena, SOVOS/packages, github tree paths
             (the internal "SOVOS I say" reality; renaming those is the package refactor, not a display swap)
        (c) slug/file renames (sov-city-3d.html → …) — reported, not auto-done (needs file moves + link fixups)

Usage:
    python3 council_scrub.py            # dry-run: per-file counts + sample diffs
    python3 council_scrub.py --apply    # write the display renames in place
"""
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
APPLY = "--apply" in sys.argv
EXCLUDE = {"_site", "_archive", "_plans", "SOVOS", "benchmark-results", "node_modules", ".git", "assets"}

# Display product names only (title-case-with-spaces forms; these never appear inside code refs or URLs,
# which use the lowercase-hyphen slugs — so replacing these is collision-free). Longest first.
DISPLAY = [
    ("Sov Globe Portal", "Council Globe Portal"),
    ("Sov Space VWM",    "Council Space VWM"),
    ("Sov Suburb 3D",    "Council Suburb 3D"),
    ("Sov Globe 3D",     "Council Globe 3D"),
    ("Sov City 3D",      "Council City 3D"),
    ("Sov 5D Engine",    "Council Engine"),
    ("SOV Arena City",   "Council Arena City"),
    ("Sovereign OS",     "Council OS"),
    ("SOV SIGNAL",       "Council Signal"),
    ("SOV Suburb",       "Council Suburb"),
    ("Sov Suburb",       "Council Suburb"),
    ("Sov Globe",        "Council Globe"),
    ("Sov Space",        "Council Space"),
    ("SOV Portal",       "Council Portal"),
    ("Sov Portal",       "Council Portal"),
]

# Guard: descriptive "Sovereign X" that must NOT be touched (bucket ③). If a display key would match one
# of these, we skip it. (None of the DISPLAY keys above collide, but the guard documents intent.)
DESCRIPTIVE = re.compile(r"Sovereign (AI|Public|Guarantee|Infrastructure|Charter|Hub|Red|Governance"
                         r"|Pillars|Cloud|Autonomy|Experiments|Pulse)")
# Lines carrying a real code/dir/package ref are left entirely alone.
CODE_REF = re.compile(r"sovos-arena|sovos-signal-index|SOVOS/packages|tree/main/SOVOS|<code>")

def html_files():
    for p in ROOT.rglob("*.html"):
        if any(part in EXCLUDE for part in p.relative_to(ROOT).parts):
            continue
        yield p

def scrub(text):
    changes = []
    out_lines = []
    for ln in text.splitlines(keepends=True):
        if CODE_REF.search(ln):            # never edit a line with a package/dir/code ref
            out_lines.append(ln); continue
        new = ln
        for old, rep in DISPLAY:
            if old in new:
                new = new.replace(old, rep)
        if new != ln:
            changes.append((ln.strip()[:90], new.strip()[:90]))
        out_lines.append(new)
    return "".join(out_lines), changes

def main():
    total_files = total_changes = 0
    for p in html_files():
        text = p.read_text(encoding="utf-8", errors="replace")
        new, changes = scrub(text)
        if not changes:
            continue
        total_files += 1; total_changes += len(changes)
        rel = p.relative_to(ROOT)
        print(f"\n{rel}  ({len(changes)} change{'s' if len(changes)!=1 else ''})")
        for a, b in changes[:3]:
            print(f"   - {a}\n   + {b}")
        if APPLY:
            p.write_text(new, encoding="utf-8")
    verb = "APPLIED" if APPLY else "DRY-RUN (no files written; use --apply)"
    print(f"\n=== {verb}: {total_changes} display renames across {total_files} files ===")
    print("Left untouched (by design): descriptive 'Sovereign AI' (bucket ③, counsel) and "
          "code/dir names sovos-arena / SOVOS/packages (package refactor, separate).")

if __name__ == "__main__":
    main()
