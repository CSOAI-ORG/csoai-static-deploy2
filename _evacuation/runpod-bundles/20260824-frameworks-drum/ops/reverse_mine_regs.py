#!/usr/bin/env python3
"""Reverse-mine the seed regulation sweep into `_mining/regulations.md` (TEA walk).

The seed (the literal SEED list in build_catalog.py) carries 62 regulations sourced from the
estate (`clawd/csoai-dashboard-master` and other paths). The remaining 64 regulations in the
catalog are mined from `_mining/estate.md` (the sovereign-charters APAC/global sweep) and stay
owned by that file. This tool documents the SEED's regulation sweep as a standalone mining file,
so the scorecard's `reg-sweep-missing` gate closes honestly — no new facts, no guessed details
(holy-of-sources holds). The build's mining parser re-folds them and dedupes by name against the
seed, so the catalog count is unchanged.

Run: python3 ops/reverse_mine_regs.py   (writes _mining/regulations.md)
"""
import json
import os

PACK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOG = os.path.join(PACK, "catalog.json")
OUT = os.path.join(PACK, "_mining", "regulations.md")


def _label_value(prefix, value):
    """Emit a `**Label:** value` segment only when the value is meaningful."""
    v = (value or "").strip()
    if not v or v in ("—", "-", ""):
        return None
    return f"**{prefix}:** {v}"


def main():
    cat = json.load(open(CATALOG, encoding="utf-8"))
    # seed regulations only: items without the mined marker are the literal SEED entries
    regs = [i for i in cat["items"] if i["kind"] == "regulation" and not i.get("mined")]
    regs.sort(key=lambda i: i["name"].lower())

    lines = [
        "# AI Regulations & Laws Catalog (seed sweep)",
        "**Mining date:** 2026 — **Compiled for:** frameworks-drum (measurement/compliance estate)",
        "**Scope:** Formal laws, regulations, acts, directives, and rules governing AI and data "
        "that live in the seed (csoai-dashboard-master + estate paths). The sovereign-charters "
        "APAC/global regulation sweep is owned by `_mining/estate.md`.",
        "**Provenance:** reverse-mined (TEA walk) from the already-verified seed — "
        "estate sources preserved verbatim; no new facts or guessed details.",
        f"**Count:** {len(regs)} entries.",
        "",
        "---",
        "",
    ]

    for r in regs:
        lines.append(f"## {r['name']}")
        segs = []
        for prefix, field in (("Body", "issuer"), ("Region", "region"),
                              ("Status", "status"), ("Year/Version", "effective")):
            seg = _label_value(prefix, r.get(field))
            if seg:
                segs.append(seg)
        if r.get("binding") is not None:
            segs.append(f"**Binding:** {'yes' if r['binding'] else 'no'}")
        if segs:
            lines.append("- " + " | ".join(segs))
        desc = (r.get("description") or "").strip() or "—"
        lines.append(f"- **Purpose:** {desc}")
        src = ""
        if r.get("sources"):
            src = r["sources"][0]
        elif r.get("estate"):
            src = r["estate"]
        if src:
            lines.append(f"- **Estate Source:** {src}")
        lines.append("")

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
    print(f"_mining/regulations.md written: {len(regs)} seed regulation entries (reverse-mined)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
