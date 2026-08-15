#!/usr/bin/env python3
"""build_index_page.py — render the GSPC Daily Index into a public page.

The settlement price of the agent economy is INVISIBLE today (the mining
finding). This generator renders the signed daily-index JSON into a
public-facing page: the current value, the CI, axis cells, the
constitution, and a mini time-series when history accumulates.

Usage: python3 build_index_page.py   (writes gspc-index.html)
"""

from __future__ import annotations
import glob, html, json, os
from datetime import datetime, timezone
from pathlib import Path

INDEX_DIR = Path("SOVOS/register/index")
OUT = Path("gspc-index.html")


def load_indexes() -> list[dict]:
    out = []
    for f in sorted(glob.glob(str(INDEX_DIR / "*.json"))):
        try:
            d = json.loads(Path(f).read_text())
            if d.get("index") is not None:
                out.append(d)
        except Exception:
            continue
    return sorted(out, key=lambda d: d.get("date", ""))


def axis_rows(d: dict) -> str:
    rows = []
    for c in d.get("cells", []):
        if not c.get("measured"):
            rows.append(
                f'<tr><td class="ax">{html.escape(c["axis"])}</td>'
                f'<td class="miss">UNMEASURED</td>'
                f'<td class="dim">—</td></tr>')
            continue
        rows.append(
            f'<tr><td class="ax">{html.escape(c["axis"])}</td>'
            f'<td class="n">{c["accuracy"]:.4f}</td>'
            f'<td class="dim">n={c.get("usable_n", 0)} · '
            f'CI {c["ci"][0]:.3f}–{c["ci"][1]:.3f}</td></tr>')
    return "".join(rows)


def series_chart(indexes: list[dict]) -> str:
    if not indexes:
        return "<p>One closing-cross recorded — history accumulates daily.</p>"
    pts = ", ".join(f"{{x:'{d['date']}', y:{d['index']}}}" for d in indexes)
    if len(indexes) < 2:
        return "<p>One closing-cross recorded — <b>index history builds daily.</b></p>"
    return f"""<canvas id="ix" height="140"></canvas>
<script>
  const pts = [{pts}];
  const cv = document.getElementById('ix'); const g = cv.getContext('2d');
  const w = cv.width=560, h = cv.height=140;
  g.strokeStyle='#4f8cff'; g.lineWidth=2; g.beginPath();
  pts.forEach((p,i) => {{
    const x = 40 + i*(w-80)/Math.max(pts.length-1,1);
    const y = h-20 - ((p.y-50)/15)*(h-40);
    i===0 ? g.moveTo(x,y) : g.lineTo(x,y);
  }}); g.stroke();
  pts.forEach((p,i) => {{
    const x = 40 + i*(w-80)/Math.max(pts.length-1,1);
    const y = h-20 - ((p.y-50)/15)*(h-40);
    g.fillStyle='#e8edf2'; g.fillText(p.y.toFixed(2), x-10, y-6);
    g.fillStyle='#7f90a0'; g.fillText(p.x.slice(5), x-8, h-6);
  }});
</script>"""


def build() -> None:
    indexes = load_indexes()
    latest = indexes[-1] if indexes else {}
    date = latest.get("date", "—")
    value = latest.get("index", None)
    ci = latest.get("ci95")
    axes_m = latest.get("axes_measured", 0)
    axes_t = latest.get("axes_total", 14)

    page = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>GSPC Daily Index — Council of AI</title>
<meta name="description" content="The GSPC Daily Index — one signed agent-economy
settlement value per day, computed from measured 14-axis board data.">
<style>
:root {{ --accent:#5a9; --bg:#0d0f12; --card:#15181d; --line:#232830; }}
* {{ box-sizing:border-box; }} body {{ margin:0; font-family:-apple-system,Segoe UI,Roboto,sans-serif;
background:var(--bg); color:#e8edf2; }} .wrap {{ max-width:760px; margin:0 auto; padding:2rem 1.2rem; }}
h1 {{ font-size:1.6rem; border-bottom:1px solid var(--line); padding-bottom:.6rem; }}
.big {{ font-size:4rem; font-weight:700; color:#ccffdd; letter-spacing:.02em; }}
.meta {{ color:#9fb0c0; }} .card {{ background:var(--card); border:1px solid var(--line); border-radius:10px;
padding:1.4rem; margin-top:1.4rem; }} table {{ width:100%; border-collapse:collapse; font-size:.85rem; }}
th,td {{ border:1px solid var(--line); padding:.3rem .45rem; text-align:left; }}
.ax {{ color:#8cd; font-weight:600; }} .n {{ color:#ccffdd; font-weight:600; }}
.miss {{ color:#556; }} .dim {{ color:#79889a; font-size:.8rem; }}
.foot {{ margin-top:2rem; color:#6a7a8a; font-size:.74rem; line-height:1.5; }}
a {{ color:#8cd; }}
</style></head><body><div class="wrap">
<h1>GSPC Daily Index <span style="font-size:.9rem;color:#7f90a0">— settlement infrastructure for the agent economy</span></h1>
<p class="meta">One official signed value per day, computed at the closing cross from
the day's measured 14-axis board. Research statistic — not a financial benchmark.
<a href="https://github.com/CSAOI-ORG/csoai-static-deploy2/tree/main/SOVOS/register/indexes">Source records.</a></p>

<div class="card">
  <div class="meta">Closing value · {html.escape(date)}</div>
  <div class="big">{value if value is not None else "—"}</div>
  <div class="meta">95% CI [{ci[0]:.3f}, {ci[1]:.3f}] · {axes_m}/{axes_t} axes measured · signed + time-anchored</div>
</div>

<div class="card">
  <h2>Axis cells</h2>
  <table><thead><tr><th>axis</th><th>accuracy</th><th>detail</th></tr></thead>
  <tbody>{axis_rows(latest)}</tbody></table>
</div>

<div class="card"><h2>History</h2>{series_chart(indexes)}</div>

<div class="card">
  <h2>Constitution</h2>
  <p style="color:#9fb0c0;font-size:.9rem">{html.escape(latest.get("constitution") or "Equal-weighted mean of axis accuracies; fixed weights; change via methodology consultation.")}</p>
  <p class="meta">Measured by deterministic gates only — no model judges another. Issuance policy,
  revocation ladder, appeals and error statistics are public.
  This is measurement, not certification.</p>
</div>

<div class="foot">Council of AI (CSOAI Ltd, UK 16939677) · daily index produced by a 23:30 UTC cron ·
each value signed with the estate Ed25519 spine + SCITT/RFC 9943 anchor · the daily root hash
is the closing. Generated {datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}.</div>
</div></body></html>"""
    OUT.write_text(page)
    print(f"✅ index page written: {OUT} — value {value} ({date}), {len(indexes)} records")


def main() -> int:
    build()
    return 0


if __name__ == "__main__":
    main()