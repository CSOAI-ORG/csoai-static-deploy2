#!/usr/bin/env python3
"""build_hub.py — regenerate arena-hub.html from arena.json, so the two cannot drift.

WHY THIS EXISTS. arena-hub.html was written once by hand from a coverage run. Within a
day of the multi-model merge it was quoting 0.386 for GovBench while the globe quoted
0.468 and the tool ranked four runs — three surfaces, three different numbers for the
same greenfield, and no way to tell which was current. A page that disagrees with the
measurement it reports is worse than no page.

Everything below derives from arena.json. There is no number in this file.

It also adds the thing the hand-written page could not have: a per-greenfield model
board. The hub is the only public surface where all twelve greenfields and every run on
them are visible at once, so the honest form of it is a leaderboard, not a single column.

    python3 build_hub.py
"""
import json, pathlib, html, datetime

HERE = pathlib.Path(__file__).parent
ARENA = json.loads((HERE / "arena.json").read_text(encoding="utf-8"))
OUT = HERE / "arena-hub.html"

COLS = [("dataset", "items"), ("card", "card"), ("space", "Space"), ("spaceTool", "Space tool"),
        ("kaggle", "Kaggle"), ("page", "page"), ("pageTool", "page tool"),
        ("lmeval", "lm-eval"), ("inspect", "Inspect"), ("measured", "measured")]
E = html.escape


def chain(g):
    return sum(1 for k, _ in COLS if g["marks"].get(k))


def dot(g):
    if g["status"] == "INSTRUMENT_FAILED": return "#f5a623"
    if g["status"] != "MEASURED": return "#8fa6c8"
    f = g.get("macro_f1")
    if f is None: return "#60a5fa"
    return "#3ddc97" if f >= 0.6 else "#f5a623" if f >= 0.4 else "#ff6b6b"


gfs = sorted(ARENA["greenfields"], key=lambda g: (-chain(g), -(g.get("macro_f1") or 0)))
total = sum(chain(g) for g in gfs)
pct = round(total / (len(gfs) * len(COLS)) * 100)
models = ARENA.get("models_seen", [])

rows = []
for g in gfs:
    c = chain(g)
    f = g.get("macro_f1")
    score = (f"{f:.3f}" if f is not None
             else f'<span class="st">{E(g["status"].replace("_", " "))}</span>')
    who = (f'<br><span class="ax">{E(g.get("measured_model", ""))}</span>'
           + ('<br><span style="color:var(--acc);font-size:.68rem;letter-spacing:.06em">'
              'QUOTABLE n\u2265\u200930</span>' if g.get("quotable") else "")
           if f is not None and g.get("measured_model") else "")
    marks = "".join(
        f'<td class="m {"on" if g["marks"].get(k) else "off"}" title="{E(lab)}">'
        f'{"●" if g["marks"].get(k) else "○"}</td>' for k, lab in COLS)
    tool = (f'<td><a class="run" href="{E(g["tool"])}">Run it →</a></td>'
            if g.get("tool") else '<td><span class="none">no tool yet</span></td>')

    # the per-greenfield board, folded away so the matrix stays readable
    runs = g.get("runs") or []
    dropped = g.get("dropped_runs") or []
    det = ""
    if runs or dropped:
        body = ""
        if runs:
            body += ('<table class="bd"><tr><th>model</th><th class="n">macro-F1</th>'
                     '<th class="n">accuracy 95% CI</th>'
                     '<th class="n">unreadable</th><th class="n">n</th><th>harness</th></tr>')
            for r in runs:
                rf = r.get("macro_f1")
                # An interval is printed only where n cleared 30. Below that the cell says
                # so, rather than showing a wide interval that invites reading anyway.
                iv = r.get("accuracy_ci95")
                ci = (f'{r["accuracy"]:.3f} [{iv[0]:.3f}, {iv[1]:.3f}]'
                      if r.get("quotable") and iv and r.get("accuracy") is not None
                      else '<span class="ax">n&lt;30</span>')
                body += (f'<tr><td>{E(r["model"])}</td>'
                         f'<td class="n">{rf:.3f}</td>'
                         f'<td class="n">{ci}</td>'
                         f'<td class="n">{round((r.get("unparsed_rate") or 0) * 100)}%</td>'
                         f'<td class="n">{r.get("n_scored") or "—"}</td>'
                         f'<td class="ax">{E(r.get("harness", ""))}</td></tr>')
            body += "</table>"
        if dropped:
            # The same three runs were dropped on every axis, so spelling each out per row
            # six times buries the one fact that matters. Compress to the range and the
            # failure kind; the per-run detail lives in robust_results.json.
            rates = sorted(round((r.get("instrument_error_rate") or 0) * 100) for r in dropped)
            kinds = sorted({k for r in dropped for k in (r.get("error_reasons") or {})})
            span = f"{rates[0]}%" if rates[0] == rates[-1] else f"{rates[0]}–{rates[-1]}%"
            body += ('<p class="drop"><b>' + str(len(dropped)) + " run" +
                     ("s" if len(dropped) > 1 else "") + " dropped</b> — " +
                     E(", ".join(r["model"] for r in dropped)) + " at " + span +
                     " instrument error" +
                     (" (all " + E(", ".join(kinds)) + ")" if kinds else "") +
                     ". A dropped connection is not a wrong answer, so these contribute no score.</p>")
        det = (f'<tr class="bdrow"><td colspan="{len(COLS) + 5}"><details><summary>'
               f'{len(runs)} scored run{"s" if len(runs) != 1 else ""}'
               + (f" · {len(dropped)} dropped" if dropped else "") +
               f'</summary>{body}</details></td></tr>')

    rows.append(f'''<tr>
      <td class="gf"><span class="dot" style="background:{dot(g)}"></span>
        <b>{E(g["bench"])}</b><br><span class="ax">{E(g["axis"])} · {E(g["seat"])}</span></td>
      <td class="n">{g.get("n") if g.get("n") is not None else "—"}</td>
      <td class="n">{score}{who}</td>
      {marks}
      <td class="n"><b>{c}/{len(COLS)}</b></td>
      {tool}</tr>{det}''')

ths = "".join(f'<th class="rot"><span>{E(l)}</span></th>' for _, l in COLS)

jsonld = {
    "@context": "https://schema.org", "@type": "Dataset",
    "name": "GSPC — 13 greenfields, chain coverage and model board",
    "description": f"Thirteen AI-governance measurement greenfields with end-to-end chain "
                   f"coverage measured live. Chain {pct}% complete. "
                   f"Scored against {len(models)} models: {', '.join(models)}.",
    "creator": {"@type": "Organization", "name": "CSOAI Ltd", "identifier": "UK 16939677"},
    "license": "https://www.apache.org/licenses/LICENSE-2.0",
    "measurementTechnique": "regex label extraction and macro-F1, identical to the published harness",
    "variableMeasured": [
        {"@type": "PropertyValue", "name": g["bench"],
         "value": g["macro_f1"] if g.get("macro_f1") is not None else g["status"],
         "description": f'{g["axis"]} · n={g.get("n") or "—"} · chain {chain(g)}/{len(COLS)}'
                        + (f' · best: {g["measured_model"]}' if g.get("measured_model") else "")}
        for g in gfs],
}

OUT.write_text(f'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Arena — 13 greenfields, chain coverage and model board | CSOAI</title>
<meta name="description" content="Thirteen AI-governance measurement greenfields, with end-to-end chain coverage measured live and every measured model run on each of them.">
<style>
:root{{--bg:#0b1220;--panel:#16233d;--ink:#eaf2ff;--mut:#8fa6c8;--line:#1e293b;--acc:#10b981}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:var(--bg);color:var(--ink);font:15px/1.6 Inter,system-ui,-apple-system,sans-serif;padding:2rem 1.25rem}}
.wrap{{max-width:1180px;margin:0 auto}}
h1{{font-size:1.9rem;margin-bottom:.4rem}}
.lede{{color:var(--mut);max-width:74ch;margin-bottom:1.4rem}}
.bar{{height:6px;border-radius:3px;background:#0d1730;overflow:hidden;margin:.8rem 0 1.6rem;max-width:520px}}
.bar i{{display:block;height:100%;background:var(--acc);width:{pct}%}}
table{{width:100%;border-collapse:collapse;font-size:.86rem}}
th,td{{padding:.5rem .45rem;border-bottom:1px solid var(--line);text-align:left;vertical-align:middle}}
th{{color:var(--mut);font-size:.7rem;letter-spacing:.06em;text-transform:uppercase;font-weight:600}}
th.rot{{height:100px;white-space:nowrap;width:34px}}
th.rot span{{display:block;transform:rotate(-60deg);transform-origin:left bottom;width:26px}}
td.m{{text-align:center;font-size:1rem;width:34px}}
td.m.on{{color:var(--acc)}} td.m.off{{color:#33415c}}
td.n{{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}}
.gf{{min-width:190px}} .ax{{color:var(--mut);font-size:.76rem}}
.dot{{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:.45rem;vertical-align:middle}}
.st{{color:#f5a623;font-size:.74rem;letter-spacing:.05em}}
.run{{color:var(--acc);text-decoration:none;font-weight:600;white-space:nowrap}}
.run:hover{{text-decoration:underline}} .none{{color:#33415c;font-size:.8rem}}
.bdrow td{{padding:0 .45rem .6rem;border-bottom:1px solid var(--line)}}
.bdrow summary{{color:var(--mut);font-size:.76rem;cursor:pointer;padding:.35rem 0}}
.bdrow summary:hover{{color:var(--ink)}}
table.bd{{margin:.3rem 0 .2rem;max-width:640px;font-size:.8rem}}
table.bd th,table.bd td{{border-bottom:1px solid #131c2e;padding:.3rem .5rem}}
.drop{{color:var(--mut);font-size:.78rem;margin:.4rem 0 .2rem;max-width:80ch;line-height:1.6}}
.note{{border-left:3px solid #f5a623;padding:.7rem .9rem;background:rgba(245,166,35,.07);
  color:var(--mut);font-size:.82rem;margin-top:1.6rem;line-height:1.6;max-width:80ch}}
@media(max-width:820px){{th.rot{{height:auto;width:auto}}th.rot span{{transform:none;width:auto}}}}
</style></head><body><div class="wrap">
<h1>Arena — 12 greenfields</h1>
<p class="lede">Every greenfield, and how much of its chain is actually complete: items published and
loadable, a card with a licence, a Hugging Face Space, a <b>runnable</b> Space, Kaggle, a page on
this site, a <b>runnable</b> page, an lm-eval task, an Inspect task, and a measurement against a
named model. Measured live, not asserted.</p>
<div class="bar"><i></i></div>
<p class="lede"><b>{total}/{len(gfs) * len(COLS)} = {pct}% chain complete.</b>
The macro-F1 column is the best score any measured run reached, and it names the model that
reached it — open a row to see every run on that greenfield. Colour follows that score; grey
means nothing is measured yet.{(" Scored against " + str(len(models)) + " models: " + E(", ".join(models)) + ".") if models else ""}</p>
<div style="overflow-x:auto"><table>
<thead><tr><th>greenfield</th><th class="n">n</th><th class="n">macro-F1</th>{ths}<th class="n">chain</th><th>tool</th></tr></thead>
<tbody>
{"".join(rows)}
</tbody></table></div>
<div class="note"><b>What the numbers do not say.</b> No axis reaches usable_n = 30, so no confidence
interval is publishable on any of them — including by us. A greenfield marked SPEC or DRAFT has no
score at all: the protocol is published so a harness can consume it, and that is the whole claim.
A run whose instrument error rate exceeded threshold is listed as dropped and contributes no score,
because a dropped connection is not a wrong answer and must never be published as one.
Measurement, not certification, and not legal advice.</div>
<p class="lede" style="font-size:.78rem;margin-top:1.2rem">Generated from arena.json on {datetime.date.today().isoformat()}.
CSOAI Ltd · UK 16939677 · <a href="https://huggingface.co/csoai" style="color:var(--acc)">huggingface.co/csoai</a></p>
</div>
<script type="application/ld+json">
{json.dumps(jsonld, indent=1)}
</script>
</body></html>''', encoding="utf-8")

print(f"arena-hub.html · {len(gfs)} greenfields · chain {total}/{len(gfs)*len(COLS)} = {pct}% · "
      f"{sum(len(g.get('runs') or []) for g in gfs)} scored runs · "
      f"{sum(len(g.get('dropped_runs') or []) for g in gfs)} dropped · "
      f"{len(models)} models · {OUT.stat().st_size if OUT.exists() else 0} bytes")
