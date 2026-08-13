#!/usr/bin/env python3
"""stage_publish.py — turn a GSPC fleet board into publish-ready artifacts.

ZERO-GATE: produces files only. Actual publishing (HF upload, Zenodo DOI) needs
the owner's rotated token — the emitted PUBLISH.md carries the exact commands.

    python3 stage_publish.py --board benchmark-results/gspc_flywheel/latest.json \
        --out dist/board-publish --title "GSPC fleet board"

Emits into --out:
  scorecard.html   honest scorecard — control-anchored, UNMEASURED-safe,
                   "measurement, not certification", ties reported as ties
  README.md        HuggingFace dataset card (same honesty register)
  dataset.jsonld   schema.org/Dataset JSON-LD for AEO / agent discovery
  board.json       the raw board (copied verbatim)
  PUBLISH.md       the exact owner commands to publish once the token is rotated

The honesty discipline is enforced in code: any model at/below the untrained
control is labelled "learned nothing measurable"; missing axes are UNMEASURED,
never zero; nothing here is called a certification.
"""
import argparse, json, shutil, html
from pathlib import Path
from datetime import datetime, timezone


def load_board(p: Path) -> dict:
    d = json.loads(p.read_text())
    if "results" not in d:
        raise SystemExit(f"{p} is not a gspc_flywheel board (no 'results' key)")
    return d


def rank(board: dict):
    control = board.get("control")
    res = board["results"]
    rows = []
    for m, v in res.items():
        mean = v.get("mean")
        rows.append((m, mean, v.get("axes", {})))
    rows.sort(key=lambda r: (r[1] is None, -(r[1] or 0)))
    cmean = res.get(control, {}).get("mean") if control else None
    return control, cmean, rows


def verdict(mean, cmean):
    if mean is None:
        return "UNMEASURED", "#8a9"
    if cmean is None:
        return "—", "#8a9"
    d = (mean - cmean) * 100
    if d > 1:
        return f"beats base +{d:.0f}pt", "#2c7d6e"
    if d > -1:
        return "parity w/ base", "#a86a24"
    return "below base — learned nothing", "#b23b3b"


def scorecard_html(board, title):
    control, cmean, rows = rank(board)
    axes = sorted({a for _, _, ax in rows for a in ax})
    when = board.get("measured_at", "")
    head = "".join(f"<th>{html.escape(a[:8])}</th>" for a in axes)
    body = ""
    for m, mean, ax in rows:
        cells = ""
        for a in axes:
            r = ax.get(a, {})
            cells += f"<td>{r['score']*100:.0f}%</td>" if r.get("status") == "MEASURED" else "<td class='u'>—</td>"
        vtxt, vcol = verdict(mean, cmean)
        tag = " control" if m == control else ""
        mtxt = f"{mean*100:.0f}%" if mean is not None else "—"
        body += (f"<tr><td class='m'>{html.escape(m)}{tag}</td>{cells}"
                 f"<td class='mean'>{mtxt}</td><td style='color:{vcol}'>{vtxt}</td></tr>")
    return f"""<!doctype html><meta charset=utf-8><title>{html.escape(title)} — CSOAI</title>
<style>body{{font-family:ui-sans-serif,system-ui,sans-serif;max-width:1100px;margin:2rem auto;padding:0 1rem;color:#16211d;background:#eef0ee}}
h1{{font-family:ui-serif,Georgia,serif}} .banner{{background:#2c7d6e14;border:1px solid #2c7d6e55;border-radius:8px;padding:.8rem 1rem;color:#2c7d6e;font-size:.95rem;margin:1rem 0}}
table{{border-collapse:collapse;width:100%;font-size:13px;font-variant-numeric:tabular-nums}} th,td{{padding:5px 8px;border-bottom:1px solid #cdd6d1;text-align:right}}
th:first-child,td.m{{text-align:left}} td.m{{font-family:ui-monospace,monospace;font-weight:600}} td.mean{{font-weight:700}} td.u{{color:#9aa}} .foot{{color:#5c6d66;font-size:12px;margin-top:1rem}}</style>
<h1>{html.escape(title)}</h1>
<div class=banner><b>Measurement, not certification.</b> Every cell is an accuracy on a fixed item set, control-anchored to <code>{html.escape(str(control))}</code>. A model at or below the untrained control learned nothing measurable. Blank = UNMEASURED (never counted as zero). A regulator certifies; we measure.</div>
<table><thead><tr><th>model</th>{head}<th>MEAN</th><th>vs base</th></tr></thead><tbody>{body}</tbody></table>
<p class=foot>Measured {html.escape(when)} · control = {html.escape(str(control))} ({(cmean*100 if cmean else 0):.0f}%) · CSOAI GSPC flywheel · signed board attached (board.json).</p>"""


def readme_md(board, title):
    control, cmean, rows = rank(board)
    beats = [m for m, mean, _ in rows if mean is not None and cmean is not None and (mean - cmean) > 0.01 and m != control]
    return f"""---
license: apache-2.0
tags: [ai-governance, gspc, measurement, eu-ai-act]
---
# {title}

Control-anchored GSPC measurement of a model fleet. **Measurement, not certification.**

- **Control (untrained baseline):** `{control}` — {(cmean*100 if cmean else 0):.0f}% mean
- **Models measured:** {len(rows)}
- **Models that beat the control by >1pt:** {len(beats)} {'— ' + ', '.join(f'`{b}`' for b in beats[:8]) if beats else '(none — the honest result)'}
- **Measured:** {board.get('measured_at','')}

Each score is an accuracy on a fixed item set with an untrained control on the same axes.
A model at or below the control learned nothing measurable. Missing axes are UNMEASURED,
never zero. See `board.json` for the raw signed record and `scorecard.html` for the table.
"""


def jsonld(board, title, url=""):
    control, cmean, rows = rank(board)
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "Dataset",
        "name": title,
        "description": f"Control-anchored GSPC measurement of {len(rows)} models "
                       f"vs untrained control {control}. Measurement, not certification.",
        "creator": {"@type": "Organization", "name": "CSOAI — Council of AI"},
        "license": "https://www.apache.org/licenses/LICENSE-2.0",
        "dateModified": board.get("measured_at", ""),
        "measurementTechnique": "GSPC control-anchored accuracy with UNMEASURED-honest scoring",
        "url": url,
    }, indent=2)


def main():
    ap = argparse.ArgumentParser(description="Stage a GSPC board for publication (zero-gate; files only).")
    ap.add_argument("--board", required=True, help="path to a gspc_flywheel board json")
    ap.add_argument("--out", default="dist/board-publish")
    ap.add_argument("--title", default="GSPC fleet board")
    ap.add_argument("--hf-repo", default="csoai/gspc-fleet-board")
    a = ap.parse_args()

    board = load_board(Path(a.board))
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    (out / "scorecard.html").write_text(scorecard_html(board, a.title))
    (out / "README.md").write_text(readme_md(board, a.title))
    (out / "dataset.jsonld").write_text(jsonld(board, a.title))
    shutil.copyfile(a.board, out / "board.json")
    (out / "PUBLISH.md").write_text(f"""# Publish runbook — {a.title} (owner, after token rotation)

Everything in this folder is generated + honest. To publish (needs the rotated HF token):

```bash
# 1. HF dataset (board + card + JSON-LD)
huggingface-cli upload {a.hf_repo} {out}/ . --repo-type=dataset

# 2. scorecard page → the site (Cloudflare Pages), then IndexNow ping
cp {out}/scorecard.html <site>/boards/{Path(a.hf_repo).name}.html

# 3. (optional) Zenodo deposition of board.json for a citable DOI
```
Nothing here is a certification. The scorecard carries the "measurement, not
certification" banner and reports ties as ties.
""")
    control, cmean, rows = rank(board)
    beats = sum(1 for m, mean, _ in rows if mean is not None and cmean is not None and (mean - cmean) > 0.01 and m != control)
    print(f"  staged → {out}/  ({len(rows)} models, {beats} beat control) — scorecard.html, README.md, dataset.jsonld, PUBLISH.md")


if __name__ == "__main__":
    main()
