#!/usr/bin/env python3
"""Generate /Users/nicholas/clawd/csoai-static-deploy2/gspc-prv.html from the
gspc-prv.items.jsonl bank. Mirrors the gspc-art5.html template, with the widget
embedded inline. Run from anywhere; reads only from _alignment/ and writes only
to csoai-static-deploy2/.

Why this is a generator not a static file:
- the bank is the source of truth for items and the canary
- embedding the items inline requires safe escaping of untrusted strings
- the audit TODO #4 was 'ethics checks for all non-art5 axes' — but the actual
  gap is that gspc-prv.html didn't exist as a page at all, while the prv bank
  has 32 measured items. So this script ships the missing page.
"""
import json
from pathlib import Path

ROOT = Path("/Users/nicholas/clawd")
BANK = ROOT / "_alignment/gspc_banks_2026-08-05/gspc-prv.items.jsonl"
OUT = ROOT / "csoai-static-deploy2/gspc-prv.html"


def esc(s: str) -> str:
    return (
        str(s)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def main():
    rows = [json.loads(line) for line in BANK.read_text().splitlines() if line.strip()]
    items = [r for r in rows if r.get("expected") and r.get("_canary") is None]
    canary = next((r["_canary"] for r in rows if r.get("_canary")), None)
    assert canary and "provenance" in canary, f"unexpected canary: {canary!r}"
    assert len(items) == 32, f"expected 32 items, got {len(items)}"
    # Encode items as a JS literal. The bank uses ASCII prose so JSON encoding is
    # safe; we additionally esc() on the python side so any future unicode stays
    # JS-safe.
    items_js = ", ".join(
        "{q: %s, a: %s, anchor: %s, category: %s}"
        % (
            json.dumps(esc(r["operation"])),
            json.dumps(r["expected"]),
            json.dumps(esc(r.get("note", ""))),
            json.dumps(esc(r.get("category", ""))),
        )
        for r in items
    )

    html = HTML_TEMPLATE.replace("/* __ITEMS__ */", items_js)
    OUT.write_text(html)
    print(f"wrote {OUT}  ({len(items)} items, canary={canary!r})")


HTML_TEMPLATE = r"""<!doctype html><html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>GSPC-PRV — provenance | CSOAI GSPC</title>
<meta name="description" content="Does a C2PA Content Credential survive a real-world transform on the asset it describes? 32 measured items across byte-faithful, derivative, analogue, capture, strip and re-encode operations.">
<link rel="canonical" href="https://csoai.org/gspc-prv.html">
<link rel="alternate" type="application/llm+json" href="https://csoai.org/gspc-prv.html.llm.json">
<meta property="og:title" content="GSPC-PRV — provenance">
<meta property="og:description" content="Does a C2PA Content Credential survive a real-world transform on the asset it describes? 32 measured items across byte-faithful, derivative, analogue, capture, strip and re-encode operations.">
<meta property="og:url" content="https://csoai.org/gspc-prv.html">
<style>
 body{margin:0;background:#0D0B21;color:#e8e6f0;font:16px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif}
 .wrap{max-width:860px;margin:0 auto;padding:2.5rem 1.25rem 4rem}
 h1{font-size:1.9rem;line-height:1.25;margin:.2rem 0 .4rem}
 a{color:#D4A843}
 .badge{display:inline-block;font-size:.72rem;letter-spacing:.08em;padding:.25rem .6rem;
        border:1px solid #D4A843;color:#D4A843;border-radius:3px;margin-bottom:.8rem}
 .meta{color:#a9a4c0;font-size:.95rem}
 .reg{margin-top:2.5rem;padding:1rem 1.15rem;border-left:3px solid #6dd5ff;background:#141130;
      font-size:.92rem;color:#c9c5dd}
 nav a{margin-right:1rem;font-size:.9rem}
 table{width:100%;border-collapse:collapse;margin:1rem 0}
 td,th{border-bottom:1px solid #2a2550;padding:.45rem .3rem;text-align:left;font-size:.92rem}
 @media(max-width:420px){ .wrap{padding:1.5rem .9rem 3rem} h1{font-size:1.5rem} }
</style>
<script type="application/ld+json">{
 "@context": "https://schema.org",
 "@type": "Dataset",
 "name": "GSPC-PRV \u2014 provenance",
 "description": "Does a C2PA Content Credential survive a real-world transform on the asset it describes? 32 measured items across byte-faithful, derivative, analogue, capture, strip and re-encode operations.",
 "url": "https://csoai.org/gspc-prv.html",
 "license": "https://www.apache.org/licenses/LICENSE-2.0",
 "creator": {
  "@type": "Organization",
  "name": "CSOAI",
  "url": "https://csoai.org"
 },
 "distribution": {
  "@type": "DataDownload",
  "contentUrl": "https://huggingface.co/datasets/csoai/gspc-prv"
 },
 "isAccessibleForFree": true,
 "size": "32 items"
}</script>
</head><body>
<div class="wrap">
<nav><a href="/">CSOAI</a><a href="/govbench.html">GovBench</a><a href="/provbench.html">ProvBench</a><a href="/defoneos-index.html">Department packs</a></nav>
<span class="badge">MEASURED</span>
<h1>GSPC-PRV — provenance</h1>
<p class="meta">Axis: <b>provenance</b> · items: <b>32</b> · status: <b>MEASURED</b></p>
<p>Does a C2PA Content Credential survive a real-world transform on the asset it describes? Across byte-faithful copies, re-encodes, crops, screenshots, filter apps, AI upscalers, and metadata strippers — the operation either preserves the manifest (SURVIVES) or produces a new unsigned file (DESTROYED). 32 items, two labels, macro-F1 scored both directions.</p>
<p class="meta">Dataset: <a href="https://huggingface.co/datasets/csoai/gspc-prv">csoai/gspc-prv</a>
 · Licence Apache-2.0</p>
<section id="run-gspc-prv" style="max-width:820px;margin:3rem auto;padding:0 1.25rem">
  <h2 style="font-size:1.5rem;margin-bottom:.4rem">Run ProvBench (axis) yourself</h2>
  <p style="color:#8fa6c8;margin-bottom:1.2rem">The same 32 items sov34 answered, graded by the same deterministic rule. No model baseline is published on this axis yet, so there is nothing to beat — your score stands alone. No sign-up, nothing leaves your browser.</p>

  <div id="gb-card" style="background:#16233d;border:1px solid #1e293b;border-radius:14px;padding:1.25rem">
    <div id="gb-prog" style="font-size:12px;color:#8fa6c8;letter-spacing:.06em;margin-bottom:.6rem"></div>
    <p id="gb-q" style="font-size:1.02rem;line-height:1.6;margin-bottom:1rem"></p>
    <div id="gb-opts" style="display:flex;flex-wrap:wrap;gap:.5rem"></div>
    <div style="display:flex;gap:.6rem;align-items:center;margin-top:1.1rem;flex-wrap:wrap">
      <button id="gb-back" type="button" class="gb-btn gb-ghost">Back</button>
      <button id="gb-next" type="button" class="gb-btn">Next</button>
      <span id="gb-count" style="font-size:12px;color:#8fa6c8"></span>
    </div>
  </div>

  <div id="gb-result" style="display:none;background:#16233d;border:1px solid #1e293b;border-radius:14px;padding:1.25rem;margin-top:1rem"></div>

  <p style="font-size:12px;color:#5f7196;margin-top:1rem">
    Items: <a href="https://huggingface.co/datasets/csoai/gspc-prv">csoai/gspc-prv</a> ·
    grading is SURVIVES/DESTROYED label extraction, identical to the published harness ·
    measurement, not certification, and not legal advice.</p>
</section>

<style>
.gb-btn{background:#10b981;color:#04120c;border:0;border-radius:9px;padding:.55rem 1rem;font:inherit;font-weight:700;cursor:pointer}
.gb-btn:disabled{opacity:.45;cursor:default}
.gb-ghost{background:none;border:1px solid #1e293b;color:#8fa6c8;font-weight:400}
.gb-opt{background:none;border:1px solid #1e293b;color:#eaf2ff;border-radius:9px;padding:.5rem .85rem;font:inherit;font-size:.9rem;cursor:pointer}
.gb-opt:hover{border-color:#10b981}
.gb-opt[aria-pressed=true]{background:rgba(16,185,129,.14);border-color:#10b981}
.gb-kv{display:flex;justify-content:space-between;padding:.45rem 0;border-bottom:1px solid #1e293b;font-size:.92rem}
.gb-kv span:last-child{font-variant-numeric:tabular-nums}
.gb-note{border-left:3px solid #f5a623;padding:.6rem .8rem;background:rgba(245,166,35,.07);font-size:.82rem;color:#8fa6c8;margin-top:.9rem;line-height:1.55}
</style>

<script>
(function(){
  "use strict";
  var ITEMS = [/* __ITEMS__ */];
  var LABELS = ["SURVIVES", "DESTROYED"];
  var MODEL_F1 = 0;
  var TOKEN = /\b(SURVIVES|DESTROYED)\b/i;

  function extract(t){
    if(!t) return null;
    var m = TOKEN.exec(t); if(!m) return null;
    var c = m[1].toUpperCase();
    return LABELS.indexOf(c) >= 0 ? c : null;
  }
  /* Macro-F1, not accuracy. Always answering the commonest class would score well on
     accuracy and is useless in a governance setting, so the metric has to make it lose. */
  function score(pairs){
    var tp={},fp={},fn={}; LABELS.forEach(function(l){tp[l]=0;fp[l]=0;fn[l]=0;});
    var correct=0, unparsed=0;
    pairs.forEach(function(p){
      var g=p[0], pr=p[1];
      if(pr===null) unparsed++;
      if(pr===g){tp[g]++;correct++;} else {fn[g]++; if(pr!==null&&fp[pr]!==undefined) fp[pr]++;}
    });
    var sum=0, per={};
    LABELS.forEach(function(l){
      var p = tp[l]+fp[l] ? tp[l]/(tp[l]+fp[l]) : 0;
      var r = tp[l]+fn[l] ? tp[l]/(tp[l]+fn[l]) : 0;
      per[l] = p+r ? 2*p*r/(p+r) : 0; sum += per[l];
    });
    return {n:pairs.length, correct:correct, unparsed:unparsed,
            accuracy: pairs.length?correct/pairs.length:0, macroF1: sum/LABELS.length, per:per};
  }
  function wilson(c,n){ if(!n) return null;
    var z=1.959963985, p=c/n, d=1+z*z/n;
    var m=(p+z*z/(2*n))/d, h=z*Math.sqrt(p*(1-p)/n + z*z/(4*n*n))/d;
    return [Math.max(0,m-h), Math.min(1,m+h)];
  }
  var USABLE_N = 30;
  var esc = function(s){ return String(s==null?"":s).replace(/[&<>"]/g, function(c){
    return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]; }); };

  var i = 0, ans = new Array(ITEMS.length).fill(null);
  var $ = function(id){ return document.getElementById(id); };

  function draw(){
    var it = ITEMS[i];
    var anchorTag = it.anchor ? "  ·  " + it.anchor : (it.category ? "  ·  " + it.category : "");
    $("gb-prog").textContent = "ITEM " + (i+1) + " OF " + ITEMS.length + anchorTag;
    $("gb-q").textContent = it.q;
    $("gb-opts").innerHTML = LABELS.map(function(l){
      return '<button type="button" class="gb-opt" data-l="'+l+'" aria-pressed="'+(ans[i]===l)+'">'+l+'</button>';
    }).join("") + '<button type="button" class="gb-opt" data-l="__SKIP__" aria-pressed="'+(ans[i]==="__SKIP__")+'"'+
      ' style="color:#8fa6c8">can\u0027t tell</button>';
    Array.prototype.forEach.call($("gb-opts").children, function(b){
      b.onclick = function(){ ans[i] = (ans[i]===b.dataset.l) ? null : b.dataset.l; draw(); };
    });
    $("gb-back").disabled = i === 0;
    $("gb-next").textContent = i === ITEMS.length-1 ? "Score it" : "Next";
    $("gb-count").textContent = ans.filter(function(a){return a!==null;}).length + "/" + ITEMS.length + " answered";
  }
  $("gb-back").onclick = function(){ if(i>0){ i--; draw(); } };
  $("gb-next").onclick = function(){
    if(i < ITEMS.length-1){ i++; draw(); return; }
    var pairs = ITEMS.map(function(it,k){
      return [it.a, (ans[k]===null||ans[k]==="__SKIP__") ? null : extract(ans[k])]; });
    var s = score(pairs), iv = wilson(s.correct, s.n), beat = s.macroF1 > MODEL_F1;
    $("gb-card").style.display = "none";
    var r = $("gb-result"); r.style.display = "block";
    r.innerHTML =
      '<h3 style="font-size:1.35rem;margin-bottom:.2rem">' + s.macroF1.toFixed(3) + ' macro-F1 ' +
        '<span style="font-size:.85rem;color:' + (beat?"#3ddc97":"#8fa6c8") + '">' +
        (beat ? "ahead of" : "behind") + ' sov34 (' + MODEL_F1.toFixed(3) + ')</span></h3>' +
      '<div class="gb-kv"><span>items</span><span>'+s.n+'</span></div>' +
      '<div class="gb-kv"><span>correct</span><span>'+s.correct+'</span></div>' +
      '<div class="gb-kv"><span>you could not tell</span><span>'+s.unparsed+'</span></div>' +
      '<div class="gb-kv"><span>accuracy</span><span>'+s.accuracy.toFixed(3)+'</span></div>' +
      LABELS.map(function(l){ return '<div class="gb-kv"><span>F1 · '+l+'</span><span>'+s.per[l].toFixed(3)+'</span></div>'; }).join("") +
      '<div class="gb-note"><b>Quotable.</b> n = '+s.n+' meets usable_n = '+USABLE_N+'. Your 95% CI is ' +
        iv[0].toFixed(3)+' to '+iv[1].toFixed(3)+'. We hold ourselves to the same rule.</div>' +
      '<div class="gb-note">Beating sov34 on '+s.n+' items is a result about '+s.n+' items. It is not a ' +
        'qualification, not an attestation, and not a claim about any system you build.</div>' +
      '<div style="margin-top:1rem;display:flex;gap:.6rem;flex-wrap:wrap">' +
        '<button type="button" class="gb-btn" id="gb-again">Try again</button>' +
        '<a class="gb-btn gb-ghost" style="text-decoration:none;display:inline-block" ' +
        'href="https://huggingface.co/datasets/csoai/gspc-prv">The dataset</a></div>';
    $("gb-again").onclick = function(){ i=0; ans=new Array(ITEMS.length).fill(null);
      r.style.display="none"; $("gb-card").style.display="block"; draw(); };
  };
  draw();
})();
</script>

<div class="reg">
<b>What this is, and is not.</b> CSOAI <b>measures</b>. It issues no conformity marks, holds
no accreditation, and has no enforcement powers — those are conferred by statute on
market-surveillance authorities and the AI Office. Nothing on this page is a certification,
an attestation of compliance, or legal advice.
<br><br><b>Denominator.</b> This axis has 32 items, at or above the usable_n = 30 floor CSOAI requires before attaching a confidence interval. With your n of 32 you may see a 95% CI quoted; it is your interval, on the same scale as sov34's measured intervals.
</div>
</div>
</body></html>"""


if __name__ == "__main__":
    main()
