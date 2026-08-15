#!/usr/bin/env python3
"""Generate /Users/nicholas/clawd/csoai-static-deploy2/gspc-mcp.html from the
gspc-mcp.items.jsonl bank. Mirrors the gspc-art5.html template structure, with
two extensions:

  (a) Self-counted ITEMS array length, replaced hero badge number, and replaced
      schema-org JSON-LD `size` value — three places the prior hand-written page
      hardcoded 11 instead of the real bank length 35.
  (b) A defense-pattern breakdown in the result panel: tallies per anchor
      category (DECLARED_READONLY / FAITHFUL_SCHEMA / BOUNDED_EGRESS) and shows
      where the visitor loses the most points. That is the "defense logic" the
      audit's TODO #6 said was absent.

Why this matters: an MCP server that passes a single sweep can still ship with
readOnlyHint:true while silently mutating state (the DECLARED_READONLY pattern).
A binary CONFORMS/VIOLATES per-item score loses that signal. The breakdown
panel makes the category-level risk surface visible, which is the actual
defense value.
"""
import json
from collections import Counter
from pathlib import Path

ROOT = Path("/Users/nicholas/clawd")
BANK = ROOT / "_alignment/gspc_banks_2026-08-05/gspc-mcp.items.jsonl"
OUT = ROOT / "csoai-static-deploy2/gspc-mcp.html"


def esc(s):
    if s is None:
        return ""
    return (
        str(s)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def defense_label(anchor):
    """Map anchor -> defense family. The bank uses several spelling variants
    for each family; we match the discriminative tokens broadly so every
    item gets a family, not an OTHER bucket."""
    if not anchor:
        return "OTHER"
    a = anchor.upper()
    # READONLY family: annotations that promise read-only / no-mutation behaviour
    if any(t in a for t in ("READONLY", "READ-ONLY", "DESTRUCTIVE", "IDEMPOTENT", "MUTATION", "OPENWORLD", "TITLE")):
        return "DECLARED_READONLY"
    # SCHEMA family: input validation, limits, declared return shapes
    if any(t in a for t in ("SCHEMA", "PARAM", "RATE", "RETURN")):
        return "FAITHFUL_SCHEMA"
    # EGRESS family: declared network scope, error-path data leakage
    if "EGRESS" in a:
        return "BOUNDED_EGRESS"
    return "OTHER"


def main():
    rows = [json.loads(line) for line in BANK.read_text().splitlines() if line.strip()]
    items = [r for r in rows if r.get("expected") and r.get("_canary") is None]
    canary = next((r["_canary"] for r in rows if r.get("_canary")), None)
    assert canary and "conformance" in canary, f"unexpected canary: {canary!r}"
    assert items, "no items found in bank"
    assert len(items) >= 30, (
        f"bank has {len(items)} items, below usable_n=30 — "
        "this script will still ship but the widget will quote a CI"
    )

    # Build the JS array. Items have {tool, expected, anchor, axis}.
    items_js = ", ".join(
        "{tool: %s, a: %s, anchor: %s}"
        % (
            json.dumps(esc(r.get("tool", ""))),
            json.dumps(r.get("expected", "")),
            json.dumps(esc(r.get("anchor", ""))),
        )
        for r in items
    )

    html = HTML_TEMPLATE.replace("/* __ITEMS__ */", items_js)
    html = html.replace("__N__", str(len(items)))
    OUT.write_text(html)
    counts = Counter(defense_label(r.get("anchor", "")) for r in items)
    print(
        f"wrote {OUT}  ({len(items)} items, "
        + ", ".join(f"{v}× {k}" for k, v in counts.most_common())
        + ")"
    )


HTML_TEMPLATE = r"""<!doctype html><html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>GSPC-MCP — conformance | CSOAI GSPC</title>
<meta name="description" content="Whether a Model Context Protocol server conforms to the specification it claims: transport, capability declaration, error contract. 35 measured items across DECLARED_READONLY, FAITHFUL_SCHEMA and BOUNDED_EGRESS defense families.">
<link rel="canonical" href="https://csoai.org/gspc-mcp.html">
<link rel="alternate" type="application/llm+json" href="https://csoai.org/gspc-mcp.html.llm.json">
<meta property="og:title" content="GSPC-MCP — conformance">
<meta property="og:description" content="Whether a Model Context Protocol server conforms to the specification it claims: transport, capability declaration, error contract. 35 measured items across DECLARED_READONLY, FAITHFUL_SCHEMA and BOUNDED_EGRESS defense families.">
<meta property="og:url" content="https://csoai.org/gspc-mcp.html">
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
 "name": "GSPC-MCP \u2014 conformance",
 "description": "Whether a Model Context Protocol server conforms to the specification it claims: transport, capability declaration, error contract. 35 measured items across DECLARED_READONLY, FAITHFUL_SCHEMA and BOUNDED_EGRESS defense families.",
 "url": "https://csoai.org/gspc-mcp.html",
 "license": "https://www.apache.org/licenses/LICENSE-2.0",
 "creator": {
  "@type": "Organization",
  "name": "CSOAI",
  "url": "https://csoai.org"
 },
 "distribution": {
  "@type": "DataDownload",
  "contentUrl": "https://huggingface.co/datasets/csoai/gspc-mcp"
 },
 "isAccessibleForFree": true,
 "size": "__N__ items"
}</script>
</head><body>
<div class="wrap">
<nav><a href="/">CSOAI</a><a href="/govbench.html">GovBench</a><a href="/provbench.html">ProvBench</a><a href="/defoneos-index.html">Department packs</a></nav>
<span class="badge">MEASURED</span>
<h1>GSPC-MCP — conformance</h1>
<p class="meta">Axis: <b>conformance</b> · items: <b>__N__</b> · status: <b>MEASURED</b></p>
<p>Whether a Model Context Protocol server conforms to the specification it claims: transport, capability declaration, error contract. Items cover three defense families: <b>DECLARED_READONLY</b> (annotations actually honored), <b>FAITHFUL_SCHEMA</b> (input validation actually rejects), and <b>BOUNDED_EGRESS</b> (declared network scope actually respected).</p>
<p class="meta">Dataset: <a href="https://huggingface.co/datasets/csoai/gspc-mcp">csoai/gspc-mcp</a>
 · Runnable Space: <a href="https://csoai-gspc-mcp.static.hf.space/">csoai-gspc-mcp</a>
 · Licence Apache-2.0</p>
<section id="run-gspc-mcp" style="max-width:820px;margin:3rem auto;padding:0 1.25rem">
  <h2 style="font-size:1.5rem;margin-bottom:.4rem">Run MCPBench yourself</h2>
  <p style="color:#8fa6c8;margin-bottom:1.2rem">All <b>__N__</b> items in the bank, graded by the same deterministic rule.
     No model baseline is published on this axis yet, so there is nothing to beat — your score stands alone. The result panel reports per-defense-family accuracy, not just overall macro-F1, so an MCP server that passes one family but fails another shows the risk surface, not a single number. No sign-up, nothing leaves your browser.</p>

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
    Items: <a href="https://huggingface.co/datasets/csoai/gspc-mcp">csoai/gspc-mcp</a> ·
    grading is a regex label read plus macro-F1, identical to the published harness ·
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
.defcat{display:grid;grid-template-columns:1fr 1fr 1fr;gap:.6rem;margin-top:.9rem}
.defcat .card{background:#0d1730;border:1px solid #1e293b;border-radius:8px;padding:.65rem .75rem}
.defcat .lab{font-size:.66rem;color:#8fa6c8;letter-spacing:.06em;text-transform:uppercase}
.defcat .num{font-size:1.4rem;font-weight:700}
.defcat .num.good{color:#3ddc97}
.defcat .num.warn{color:#f5a623}
.defcat .num.bad{color:#ef6b6b}
.defcat .sub{font-size:.74rem;color:#8fa6c8;margin-top:.2rem}
</style>

<script>
(function(){
  "use strict";
  var ITEMS = [/* __ITEMS__ */];
  var LABELS = ["CONFORMS", "VIOLATES"];
  var MODEL_F1 = 0;   // no published baseline yet
  var TOKEN = /\b(CONFORMS|VIOLATES)\b/i;

  // Group anchors into defense families. Each anchor is a short label that
  // names the protection family the item is testing. Exact strings vary across
  // versions of the bank, so we match on a small set of discriminative tokens.
  function family(anchor){
    if(!anchor) return "OTHER";
    var head = anchor.toUpperCase().split(" — ")[0];
    // READONLY family: annotations that promise read-only / no-mutation behaviour
    if(head.indexOf("READONLY")   >= 0)  return "READONLY";
    if(head.indexOf("READ-ONLY")  >= 0)  return "READONLY";
    if(head.indexOf("DESTRUCTIVE") >= 0)  return "READONLY";
    if(head.indexOf("IDEMPOTENT")  >= 0)  return "READONLY";
    if(head.indexOf("MUTATION")    >= 0)  return "READONLY";
    if(head.indexOf("OPENWORLD")   >= 0)  return "READONLY";
    if(head.indexOf("TITLE")       >= 0)  return "READONLY";
    // SCHEMA family: input validation, limits, declared return shapes
    if(head.indexOf("SCHEMA")      >= 0)  return "SCHEMA";
    if(head.indexOf("PARAM")        >= 0)  return "SCHEMA";
    if(head.indexOf("RATE")         >= 0)  return "SCHEMA";
    if(head.indexOf("RETURN")       >= 0)  return "SCHEMA";
    // EGRESS family: declared network scope, error-path data leakage
    if(head.indexOf("EGRESS")       >= 0)  return "EGRESS";
    return "OTHER";
  }

  function extract(t){
    if(!t) return null;
    var m = TOKEN.exec(t); if(!m) return null;
    var c = m[1].toUpperCase();
    return LABELS.indexOf(c) >= 0 ? c : null;
  }
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
  function color(n){ return n >= 0.85 ? "good" : n >= 0.6 ? "warn" : "bad"; }

  var USABLE_N = 30;
  var esc = function(s){ return String(s==null?"":s).replace(/[&<>"]/g, function(c){
    return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]; }); };

  var i = 0, ans = new Array(ITEMS.length).fill(null);
  var $ = function(id){ return document.getElementById(id); };

  function draw(){
    var it = ITEMS[i];
    $("gb-prog").textContent = "ITEM " + (i+1) + " OF " + ITEMS.length +
      (it.anchor ? "  ·  " + it.anchor.split(" — ")[0] : "");
    $("gb-q").textContent = it.tool;
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

    // Score per-defense-family so the visitor sees WHERE the risk is, not just
    // an undifferentiated macro-F1.
    var pairs = ITEMS.map(function(it,k){
      return {g: it.a, pr: (ans[k]===null||ans[k]==="__SKIP__") ? null : extract(ans[k]),
              fam: family(it.anchor)};
    });
    var overall = score(pairs.map(function(p){return [p.g, p.pr];}));
    var byFam = {};
    pairs.forEach(function(p){
      if(!byFam[p.fam]) byFam[p.fam] = [];
      byFam[p.fam].push([p.g, p.pr]);
    });
    var famScores = {};
    Object.keys(byFam).forEach(function(k){
      famScores[k] = score(byFam[k]);
    });

    var iv = wilson(overall.correct, overall.n), beat = overall.macroF1 > MODEL_F1;
    $("gb-card").style.display = "none";
    var r = $("gb-result"); r.style.display = "block";

    var famCards = ["READONLY", "EGRESS", "SCHEMA"].map(function(k){
      var s = famScores[k];
      var note = s ? (s.macroF1.toFixed(3) + " macro-F1 · n=" + s.n) : "no items";
      var klass = s ? color(s.macroF1) : "";
      return '<div class="card">' +
             '<div class="lab">defense: ' + k.toLowerCase() + '</div>' +
             '<div class="num ' + klass + '">' + (s ? s.macroF1.toFixed(2) : "—") + '</div>' +
             '<div class="sub">' + (note) + '</div></div>';
    }).join("");

    var ciLine = overall.n >= USABLE_N
      ? '<div class="gb-note"><b>Quotable.</b> n = '+overall.n+' meets usable_n = '+USABLE_N+'. Your 95% CI is ' +
        iv[0].toFixed(3)+' to '+iv[1].toFixed(3)+'. We hold ourselves to the same rule.</div>'
      : '<div class="gb-note"><b>Not quotable.</b> n = '+overall.n+' is below usable_n = '+USABLE_N+'. The threshold is on ' +
        '<i>n</i>, not on the interval you happened to land. We hold ourselves to the same rule and publish no interval on this axis.</div>';

    r.innerHTML =
      '<h3 style="font-size:1.35rem;margin-bottom:.2rem">' + overall.macroF1.toFixed(3) + ' macro-F1 ' +
        '<span style="font-size:.85rem;color:' + (beat?"#3ddc97":"#8fa6c8") + '">' +
        (MODEL_F1 ? (beat ? "ahead of" : "behind") + ' sov34 (' + MODEL_F1.toFixed(3) + ')' : 'no published baseline yet') +
        '</span></h3>' +
      '<div class="gb-kv"><span>items</span><span>'+overall.n+'</span></div>' +
      '<div class="gb-kv"><span>correct</span><span>'+overall.correct+'</span></div>' +
      '<div class="gb-kv"><span>you could not tell</span><span>'+overall.unparsed+'</span></div>' +
      '<div class="gb-kv"><span>accuracy</span><span>'+overall.accuracy.toFixed(3)+'</span></div>' +
      LABELS.map(function(l){ return '<div class="gb-kv"><span>F1 · '+l+'</span><span>'+overall.per[l].toFixed(3)+'</span></div>'; }).join("") +
      '<div class="gb-note"><b>Per-defense-family breakdown.</b> An MCP server can pass one family and fail another. The numbers below tell you which.</div>' +
      '<div class="defcat">' + famCards + '</div>' +
      ciLine +
      '<div class="gb-note">Beating a baseline on '+overall.n+' items is a result about '+overall.n+' items. It is not a ' +
        'qualification, not an attestation, and not a claim about any system you build.</div>' +
      '<div style="margin-top:1rem;display:flex;gap:.6rem;flex-wrap:wrap">' +
        '<button type="button" class="gb-btn" id="gb-again">Try again</button>' +
        '<a class="gb-btn gb-ghost" style="text-decoration:none;display:inline-block" ' +
        'href="https://huggingface.co/datasets/csoai/gspc-mcp">The dataset</a></div>';
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
<br><br><b>Denominator.</b> This axis has <b>__N__ items</b>, which meets the usable_n = 30 floor. With your n of __N__ you may see a 95% CI quoted; it is your interval, on the same scale as the measured intervals published for other axes.
<br><br><b>Defense families measured.</b> The bank is partitioned across three families: <b>DECLARED_READONLY</b> (readOnlyHint / destructiveHint / idempotentHint annotations actually honored), <b>FAITHFUL_SCHEMA</b> (typed parameters validated, schema-declared limits enforced, declared return shapes returned), and <b>BOUNDED_EGRESS</b> (declared network scope actually respected, error paths do not leak data). A pass/fail per item is not enough — an MCP server that passes READONLY but fails SCHEMA is a different risk than one that fails only EGRESS. The result panel reports per-family macro-F1.
</div>
</div>
</body></html>"""


if __name__ == "__main__":
    main()
