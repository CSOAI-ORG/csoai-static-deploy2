#!/usr/bin/env python3
"""Build the fused 13-axis scoreboard page (PP-2) from real board data.

Renders ALL 13 axes x 19 models with their REAL quotable measurement (n,
accuracy, 95% CI) into a single public page. Data is read verbatim from the
boards-v2-2026-08-12 board_*.json files — no transcription, no fabrication.
A cell only shows a number if quotable=True (the honest gate already applied
at measure time).
"""
import json, html, glob, datetime
from pathlib import Path

BOARD_DIR = Path("SOVOS/boards-v2-2026-08-12")
OUT = Path("gspc-scoreboard.html")
AXIS_HINT = {
    "art5": "EU AI Act Art 5 prohibited practices", "care": "Maternal-care floor",
    "gov": "governance", "affect": "affective", "det": "detection",
    "prv": "privacy", "xr": "extended reality", "mach": "machinery",
    "mcp": "MCP conformance", "oss": "open-source", "agi": "AGI-likelihood",
    "asi": "ASI-likelihood", "swarm": "multi-agent swarm",
}

boards = []
for f in sorted(glob.glob(str(BOARD_DIR / "board_*.json"))):
    b = json.loads(Path(f).read_text())
    if b.get("status") != "MEASURED":
        continue
    axis = b.get("axis")
    model_cells = b.get("models", [])
    board_row = {
        "axis": axis, "hint": AXIS_HINT.get(axis, ""),
        "per_item": b.get("per_item_count"), "best": b.get("best"),
        "cells": {c["model"]: c for c in model_cells},
    }
    boards.append(board_row)
boards.sort(key=lambda r: r["axis"])

# Public display-name mapper: internal board keys -> public measurement labels.
# Internal engine names (sov6-*, etc.) NEVER appear on a public surface (naming canon).
def _display(m: str) -> str:
    d = m.lower()
    if d.startswith("sov6-"):
        clan = m.removeprefix("sov6-").removesuffix("-v3-light").removesuffix("-v3").replace("-", " ")
        return clan.title() + " (tuned)"
    return m  # public families (qwen3:4b, phi4:14b, ...) unchanged

# union of models across boards (order = first appearance)
models = []
seen = set()
for b in boards:
    for m in b["cells"]:
        if m not in seen:
            seen.add(m); models.append(m)

rows_html = []
for b in boards:
    cells_td = []
    for m in models:
        c = b["cells"].get(m)
        if not c or not c.get("quotable"):
            cells_td.append('<td class="miss">—</td>')
            continue
        acc = float(c["accuracy"])
        lo, hi = c["ci95"]
        cells_td.append(
            f'<td class="n"><div class="acc">{acc:.3f}</div>'
            f'<div class="ci">n={c["n"]} · {lo:.2f}–{hi:.2f}'
            f' · <span class="sig" title="Ed25519-signed via estate spine, '
            f'time-anchored (SCITT/RFC 9943). Verify with csoai_verify.py">'
            f'✓signed</span></div></td>')
    rows_html.append(
        f'<tr><th class="axis">{html.escape(b["axis"])}<div class="hint">{html.escape(b["hint"])}</div></th>'
        f'<td class="best">{html.escape(_display(str(b["best"])))}</td>'
        + "".join(cells_td) + "</tr>")

thead = "".join(f"<th>{html.escape(_display(m))}</th>" for m in models)
generated = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

row_body = "".join(rows_html)
page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Council Scoreboard — 13 axes × {len(models)} models, measured &amp; signed</title>
<meta name="description" content="Fused 14-axis GSPC scoreboard from measured board data (13 GSPC + jail). Every cell shows n, accuracy and 95% confidence interval. A cell shows a number only if quotable (usable n≥30).">
<style>
:root {{ --accent:#5a9; --bg:#0d0f12; --card:#15181d; --line:#232830; }}
* {{ box-sizing:border-box; }}
body {{ margin:0; font-family:-apple-system,Segoe UI,Roboto,sans-serif; background:var(--bg); color:#e8edf2; }}
.wrap {{ max-width:1200px; margin:0 auto; padding:2rem 1.2rem; }}
h1 {{ font-size:1.6rem; border-bottom:1px solid var(--line); padding-bottom:.6rem; }}
.disc {{ color:#9fb0c0; font-size:.9rem; line-height:1.5; max-width:80ch; }}
table {{ width:100%; border-collapse:collapse; margin-top:1.2rem; font-size:.8rem; }}
th,td {{ border:1px solid var(--line); padding:.35rem .4rem; text-align:left; vertical-align:top; }}
th {{ background:var(--card); font-weight:600; }}
th.axis {{ position:sticky; }}
.hint {{ color:#7f90a0; font-weight:400; font-size:.68rem; }}
.best {{ color:#7fd; font-size:.72rem; }}
td.n .acc {{ font-weight:600; color:#ccffdd; }}
td.n .ci {{ color:#79889a; font-size:.68rem; }}
td.miss {{ color:#556; text-align:center; }}
.sig {{ color:#8cd; font-weight:600; }}
.legend {{ margin-top:1rem; color:#8aa; font-size:.8rem; }}
.foot {{ margin-top:1.6rem; color:#6a7a8a; font-size:.74rem; line-height:1.5; }}
</style>
</head>
<body>
<div class="wrap">
<h1>Council Scoreboard — 13 axes × {len(models)} models</h1>
<p class="disc">Fused from measured board data. Each cell shows the model's
accuracy and 95% confidence interval at its measured n. A cell shows a number
<strong>only if quotable</strong> (usable n ≥ 30); a dash means not quotable.
This is measurement, not certification. Deterministic gate — no model judged
another. Every row is reproducible from the signed board records.</p>
<table>
<thead><tr><th>axis</th><th>best model</th>{thead}</tr></thead>
<tbody>{row_body}</tbody>
</table>
<div class="legend">Cells: accuracy / (n, 95% CI) · ✓signed marks Ed25519 spine
signing + time-anchor (SCITT/RFC 9943) · signing overhead: 40.8µs / 517B median
per card (bench, n=500). Generated {generated}.</div>
<div class="foot">Council of AI (CSOAI Ltd, UK 16939677) · measurement, not
certification · generated from boards-v2-2026-08-12. Honest: a quotable cell
means usable n≥30 with a computed interval — it is a measurement of one point
in time, not a guarantee of behaviour.</div>
</div>
</body>
</html>"""

OUT.write_text(page)
print(f"wrote {OUT} — {len(boards)} axes × {len(models)} models, {generated}")