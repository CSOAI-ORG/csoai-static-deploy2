#!/usr/bin/env python3
"""build_arenas.py — turn each of the six axes from a measurement into a tool you can use.

WHAT THIS IS
------------
Six self-contained training arenas, one per GSPC axis. Each serves the REAL frozen items, marks
against the REAL answer key, shows the statutory anchor behind every answer, and — the part that
makes it a measurement product rather than a quiz — scores the human against the SAME 30-model
fleet the instrument was measured on. You find out not just whether you were right, but where
you sit against models that have been through the identical items.

WHY IT IS "TRAINING" AND NOT "CERTIFICATION"
-------------------------------------------
The estate register bans the word *certification* on public surfaces (DR-0033/G3), and that ban
is load-bearing: CSOAI's entire position is measurement, not accreditation. A body that measures
AI systems and also issues certificates is the conflict of interest the posture exists to
avoid. So these pages say plainly, on every screen, that finishing one certifies nothing. The
product is identical; only the claim is narrower, and the narrower claim is the defensible one.

WHY THE COMPARISON IS THE FEATURE
---------------------------------
Anyone can build a quiz. Almost nobody can tell you "you scored 0.71 on EU AI Act risk tiering,
which puts you above 26 of the 30 models we measured, and here is the frozen item set and the
scorer so you can check us." That is the instrument being *used* rather than merely published.

NO EXTERNAL DEPENDENCIES. Items, key, anchors and fleet distribution are inlined. The page works
offline, from a file:// URL, with JavaScript as the only requirement — and unlike the SPA, its
text is in the HTML, so a crawler reads it too.
"""
from __future__ import annotations

import html
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import gspc_six_axis_e2e as G  # noqa: E402

EV = HERE / "evidence/harness/freeze/latest"
OUT = Path.home() / "clawd/councilof-ai/public/arena"

AXES = {
    "governance": ("GovBench", "EU AI Act risk tier",
                   "Decide which risk tier the EU AI Act assigns to a deployment scenario."),
    "safety": ("DefBench", "calibrated refusal",
               "Decide whether a request should be refused — with benign near-twins that share "
               "the same vocabulary."),
    "provenance": ("ProvBench", "C2PA manifest survival",
                   "Decide whether content provenance survives an operation."),
    "continuity": ("PQCBench", "post-quantum continuity",
                   "Decide whether a cryptographic primitive is threatened by quantum attack."),
    "conformance": ("MCPBench", "tool-contract conformance",
                    "Decide whether a tool's behaviour honours its declared contract."),
    "openness": ("OSSBench", "licence vs intended use",
                 "Decide whether a licence permits an intended use."),
}


def page(axis: str, bench: str, task: str, blurb: str, items: list, labels: list,
         fleet: list[float], measured_at: str) -> str:
    data = json.dumps([{"q": it["scenario"] if "scenario" in it else it[FIELD],
                        "a": it["expected"], "anchor": it.get("anchor", "")} for it in items])
    fleet_js = json.dumps(sorted(fleet))
    n = len(items)
    others = "".join(
        f'<a href="/arena/{a}.html">{AXES[a][0]}</a>' for a in AXES if a != axis)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{bench} Training Arena — {task} | CSOAI</title>
<meta name="description" content="Practise {task} on the real frozen {bench} items, marked against the published key, and see where you rank against {len(fleet)} measured AI models. Training, not certification.">
<link rel="canonical" href="https://csoai.org/arena/{axis}.html">
<style>
:root{{--fg:#111;--mut:#5a5a5a;--bd:#dcdcdc;--bg:#fff;--ok:#0a7d3c;--no:#b3261e;--acc:#12457a}}
@media(prefers-color-scheme:dark){{:root{{--fg:#eaeaea;--mut:#9d9d9d;--bd:#333;--bg:#0d0d0d;--ok:#41c47c;--no:#ff6b5e;--acc:#6fa8dc}}}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--fg);font:16px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif}}
main{{max-width:44rem;margin:0 auto;padding:1.5rem 1.1rem 4rem}}
h1{{font-size:1.5rem;margin:0 0 .2rem;line-height:1.25}}
.sub{{color:var(--mut);margin:0 0 1rem;font-size:.95rem}}
.banner{{border:1px solid var(--bd);border-left:3px solid var(--acc);padding:.6rem .8rem;margin:1rem 0;font-size:.9rem;color:var(--mut);border-radius:4px}}
.bar{{height:4px;background:var(--bd);border-radius:2px;overflow:hidden;margin:1rem 0}}
.bar>i{{display:block;height:100%;background:var(--acc);width:0;transition:width .25s}}
.q{{font-size:1.08rem;margin:1.2rem 0;padding:1rem;border:1px solid var(--bd);border-radius:6px}}
button.opt{{display:block;width:100%;text-align:left;margin:.4rem 0;padding:.7rem .9rem;font:inherit;
  background:transparent;color:var(--fg);border:1px solid var(--bd);border-radius:5px;cursor:pointer}}
button.opt:hover:not(:disabled){{border-color:var(--acc)}}
button.opt:disabled{{cursor:default;opacity:.85}}
button.opt.right{{border-color:var(--ok);color:var(--ok);font-weight:600}}
button.opt.wrong{{border-color:var(--no);color:var(--no)}}
.fb{{margin:.9rem 0;padding:.8rem .9rem;border:1px solid var(--bd);border-radius:5px;font-size:.93rem}}
.fb b{{color:var(--acc)}}
.next{{margin-top:1rem;padding:.65rem 1.3rem;font:inherit;background:var(--acc);color:#fff;border:0;border-radius:5px;cursor:pointer}}
table{{border-collapse:collapse;width:100%;margin:1rem 0;font-size:.92rem}}
th,td{{text-align:left;padding:.4rem .5rem;border-bottom:1px solid var(--bd)}}
td.n{{text-align:right;font-variant-numeric:tabular-nums}}
footer{{margin-top:2.5rem;padding-top:1rem;border-top:1px solid var(--bd);color:var(--mut);font-size:.85rem}}
nav a{{color:var(--acc);margin-right:.8rem;font-size:.9rem}}
.hide{{display:none}}
</style>
</head>
<body>
<main>
<h1>{bench} Training Arena</h1>
<p class="sub">{task} · {n} real items · marked against the published key</p>

<div class="banner">
<strong>This is training, not certification.</strong> CSOAI is an independent measurement body
and does not accredit anyone. Finishing this certifies nothing, confers no status, and is not a
conformity assessment. What it does give you is a score on the same frozen items, marked by the
same key, as {len(fleet)} AI models we measured.
</div>

<p>{blurb}</p>

<div class="bar"><i id="bar"></i></div>
<div id="stage"></div>

<div id="done" class="hide">
  <h2>Your result</h2>
  <p id="score"></p>
  <p id="rank"></p>
  <table>
    <thead><tr><th>Reference</th><th>Accuracy on these items</th></tr></thead>
    <tbody id="cmp"></tbody>
  </table>
  <p class="sub">Model figures measured {measured_at} across {len(fleet)} models spanning 494M to
  20B parameters. Your score and theirs come from the same items and the same key.</p>
  <button class="next" onclick="location.reload()">Try again</button>
</div>

<h2>Why you can check us</h2>
<p>Every item carries the provision or rationale it derives from — shown after you answer, so you
can disagree with the key rather than take it on trust. The full item set and the scoring code
are published:
<a href="https://huggingface.co/datasets/csoai/{axis if axis!='governance' else 'govbench'}">Hugging Face</a> ·
<a href="/benchmarks">measured results</a>.</p>

<h2>The other five axes</h2>
<nav>{others}</nav>

<footer>
CSOAI Ltd (UK 16939677) · training material, not accreditation · items Apache-2.0<br>
Measurement, not certification. Regulatory determinations are reserved to authorities.
</footer>
</main>
<script>
const ITEMS={data}, LABELS={json.dumps(labels)}, FLEET={fleet_js};
let i=0, right=0, answered=false;
const stage=document.getElementById('stage'), bar=document.getElementById('bar');
function render(){{
  if(i>=ITEMS.length) return finish();
  answered=false;
  bar.style.width=(i/ITEMS.length*100)+'%';
  const it=ITEMS[i];
  stage.innerHTML='<div class="q">'+esc(it.q)+'</div>'+
    LABELS.map(l=>'<button class="opt" data-l="'+esc(l)+'">'+esc(l)+'</button>').join('')+
    '<div id="fb"></div>';
  stage.querySelectorAll('button.opt').forEach(b=>b.onclick=()=>pick(b));
}}
function pick(b){{
  if(answered) return; answered=true;
  const it=ITEMS[i], chosen=b.dataset.l, ok=chosen===it.a;
  if(ok) right++;
  stage.querySelectorAll('button.opt').forEach(x=>{{
    x.disabled=true;
    if(x.dataset.l===it.a) x.classList.add('right');
    else if(x===b) x.classList.add('wrong');
  }});
  document.getElementById('fb').innerHTML='<div class="fb">'+
    (ok?'<b>Correct.</b> ':'<b>The key says '+esc(it.a)+'.</b> ')+
    (it.anchor?'Anchor: '+esc(it.anchor):'')+
    '</div><button class="next">Next</button>';
  document.querySelector('#fb .next').onclick=()=>{{i++;render();}};
}}
function finish(){{
  bar.style.width='100%';
  stage.innerHTML='';
  document.getElementById('done').classList.remove('hide');
  const acc=right/ITEMS.length;
  document.getElementById('score').textContent=
    'You answered '+right+' of '+ITEMS.length+' correctly — '+(acc*100).toFixed(0)+'%.';
  const beat=FLEET.filter(f=>f<acc).length;
  document.getElementById('rank').textContent= FLEET.length
    ? 'That is above '+beat+' of the '+FLEET.length+' measured models on this axis.'
    : 'No model comparison is available for this axis yet.';
  const rows=[['You',(acc*100).toFixed(0)+'%']];
  if(FLEET.length){{
    const med=FLEET[Math.floor(FLEET.length/2)];
    rows.push(['Best measured model',(Math.max(...FLEET)*100).toFixed(0)+'%']);
    rows.push(['Median measured model',(med*100).toFixed(0)+'%']);
    rows.push(['Weakest measured model',(Math.min(...FLEET)*100).toFixed(0)+'%']);
  }}
  document.getElementById('cmp').innerHTML=rows.map(r=>
    '<tr><td>'+r[0]+'</td><td class="n">'+r[1]+'</td></tr>').join('');
}}
function esc(s){{return String(s).replace(/[&<>"']/g,c=>({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}})[c]);}}
render();
</script>
</body>
</html>
"""


if __name__ == "__main__":
    sat = json.loads((EV / "axis-saturation.json").read_text())
    measured_at = sat["measured_at"][:10]
    OUT.mkdir(parents=True, exist_ok=True)
    index_rows = []
    for axis, (bench, task, blurb) in AXES.items():
        items, FIELD, labels = G.load_axis(axis)
        totals = sat["axes"].get(axis, {}).get("model_totals", {})
        fleet = [v for v in totals.values() if isinstance(v, (int, float))]
        p = OUT / f"{axis}.html"
        p.write_text(page(axis, bench, task, blurb, items, labels, fleet, measured_at))
        index_rows.append((axis, bench, task, len(items), len(fleet)))
        print(f"  {axis:12s} {bench:10s} {len(items):2d} items, {len(fleet):2d} model scores "
              f"-> {p.name} ({p.stat().st_size:,}B)")

    rows = "\n".join(
        f'<tr><td><a href="/arena/{a}.html">{b}</a></td><td>{t}</td>'
        f'<td class="n">{n}</td><td class="n">{f}</td></tr>'
        for a, b, t, n, f in index_rows)
    (OUT / "index.html").write_text(f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>GSPC Training Arenas — six axes of AI governance | CSOAI</title>
<meta name="description" content="Practise AI-governance judgement on real frozen benchmark items across six axes, marked against a published key, scored against measured AI models. Training, not certification.">
<link rel="canonical" href="https://csoai.org/arena/">
<style>
:root{{--fg:#111;--mut:#5a5a5a;--bd:#dcdcdc;--bg:#fff;--acc:#12457a}}
@media(prefers-color-scheme:dark){{:root{{--fg:#eaeaea;--mut:#9d9d9d;--bd:#333;--bg:#0d0d0d;--acc:#6fa8dc}}}}
body{{margin:0;background:var(--bg);color:var(--fg);font:16px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif}}
main{{max-width:48rem;margin:0 auto;padding:2rem 1.1rem 4rem}}
table{{border-collapse:collapse;width:100%;margin:1.2rem 0}}
th,td{{text-align:left;padding:.5rem .6rem;border-bottom:1px solid var(--bd)}}
td.n{{text-align:right;font-variant-numeric:tabular-nums}}
a{{color:var(--acc)}}
.banner{{border:1px solid var(--bd);border-left:3px solid var(--acc);padding:.7rem .9rem;margin:1.2rem 0;color:var(--mut);font-size:.93rem;border-radius:4px}}
footer{{margin-top:2.5rem;padding-top:1rem;border-top:1px solid var(--bd);color:var(--mut);font-size:.85rem}}
</style></head><body><main>
<h1>GSPC Training Arenas</h1>
<p>Six axes of AI-governance judgement. Each arena serves the <strong>real frozen items</strong>
from the published benchmark, marks against the <strong>published key</strong>, shows you the
provision behind every answer, and scores you against the AI models we measured on the identical
items.</p>
<div class="banner"><strong>Training, not certification.</strong> CSOAI is an independent
measurement body and does not accredit anyone. Completing an arena confers no status and is not
a conformity assessment.</div>
<table>
<thead><tr><th>Arena</th><th>What you decide</th><th>Items</th><th>Models to beat</th></tr></thead>
<tbody>
{rows}
</tbody></table>
<p>Every item set is public on <a href="https://huggingface.co/csoai">Hugging Face</a> and
<a href="https://www.kaggle.com/nicktempleman">Kaggle</a>, with the scoring code, so you can
disagree with any key rather than take it on trust. Measured results:
<a href="/benchmarks">/benchmarks</a>.</p>
<footer>CSOAI Ltd (UK 16939677) · items Apache-2.0 · measurement, not certification</footer>
</main></body></html>""")
    print(f"\n  index.html -> {OUT}")
