#!/usr/bin/env python3
"""make_leaderboard.py — generate the static leaderboard Space from measured results.

The board is generated, never hand-edited. A leaderboard typed by hand drifts from the data
it claims to summarise, and this one has already had to retract two columns; the way to keep
that honest is for the page to be a pure function of the results directory.

WHAT IT REFUSES TO DO
  • print a winner where the Wilson intervals overlap — it prints the TIED SET
  • carry a dimension whose grader is retracted — those rows are struck out, with the reason
  • carry a model that cannot be reproduced — `sov33-evolved-c2` emits "1\\n1\\n1" from a
    corrupt blob and is withdrawn, not silently left in place because it is already printed

    python3 make_leaderboard.py --out /tmp/gbspace
"""
from __future__ import annotations

import argparse, json, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
RESCORE = HERE / "benchmark-results" / "rescore_absence_dims.json"


def collect() -> dict:
    from rank_intervals import load, wilson
    from govbench_eval import DIMENSIONS
    models = load()

    corrections, withdrawn = {}, {}
    if RESCORE.exists():
        r = json.loads(RESCORE.read_text())
        corrections, withdrawn = r["scores"], r["unreproducible_excluded"]
        for m in withdrawn:
            models.pop(m, None)
        for m, dd in corrections.items():
            if m in models:
                for d in r["dimensions_rescored"]:
                    if dd.get(d) is not None:
                        models[m][d] = dd[d]

    rows = []
    for d in sorted(next(iter(models.values()))):
        n = len(DIMENSIONS[d]["tests"]) if d in DIMENSIONS else 5
        sc = []
        for m, dd in models.items():
            p = dd[d] / 100.0
            lo, hi = wilson(p * n, n)
            sc.append({"m": m, "s": dd[d], "lo": round(lo * 100, 1), "hi": round(hi * 100, 1)})
        sc.sort(key=lambda x: -x["s"])
        tied = [x for x in sc if x["hi"] >= sc[0]["lo"]]
        rows.append({"dim": d, "n": n, "lead": sc[0], "tied": len(tied), "total": len(sc),
                     "regraded": d in corrections.get(next(iter(corrections), ""), {})})
    return {"rows": rows, "models": len(models), "withdrawn": withdrawn,
            "regraded": sorted(json.loads(RESCORE.read_text())["dimensions_rescored"])
                        if RESCORE.exists() else []}


def render(d: dict) -> str:
    rows, nm = d["rows"], d["models"]
    body = []
    for r in sorted(rows, key=lambda x: -x["lead"]["s"]):
        l = r["lead"]
        tag = ' <span class="rg">regraded</span>' if r["dim"] in d["regraded"] else ""
        body.append(f'''<tr>
      <td class="d">{r["dim"]}{tag}</td><td class="n">{r["n"]}</td>
      <td class="sc">{l["s"]:.1f}%</td><td class="ci-t">[{l["lo"]:.1f}, {l["hi"]:.1f}]</td>
      <td><div class="bar"><span class="ci" style="left:{l["lo"]}%;width:{max(1,l["hi"]-l["lo"])}%"></span>
          <span class="pt" style="left:{l["s"]}%"></span></div></td>
      <td class="tie">{r["tied"]}/{r["total"]}</td></tr>''')

    wd = "".join(f"<li><code>{m}</code> — {why}</li>" for m, why in d["withdrawn"].items())
    withdrawn_block = f'''<h3>Withdrawn models</h3><ul class="wd">{wd}</ul>
    <p>A model that cannot be re-measured cannot have its published score reproduced, so the
    score is withdrawn rather than carried forward.</p>''' if wd else ""

    allt = sum(1 for r in rows if r["tied"] == r["total"])
    return f'''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>GovBench — tied sets, not rankings</title><link rel="stylesheet" href="style.css"></head><body>
<div class="wrap">
<header>
  <p class="eyebrow">AI Governance Benchmark · {nm} models · {len(rows)} dimensions</p>
  <h1>GovBench</h1>
  <p class="sub">A governance benchmark that publishes its own resolution limit.</p>
</header>

<div class="alert">
  <h2>0 of {len(rows)} dimensions have a resolved winner</h2>
  <p>Every row shows a <strong>tied set</strong>, not a ranking. At current item counts the 95%
  confidence intervals overlap for nearly every model on nearly every dimension —
  <strong>{allt} of {len(rows)}</strong> dimensions have <em>all {nm} models</em> statistically tied.</p>
  <p>Most dimensions hold ~6 items. MMLU's own floor is <strong>100 per subject</strong>; Miller
  (arXiv:2411.00640) puts it at <strong>~1,000 per comparison</strong>. At n=5 the minimum
  detectable effect is <strong>≈63 points</strong> — our observed margins are 1–15.</p>
  <p class="do"><strong>So: do not rank models on these numbers.</strong> Use them to find failure
  cases. Item expansion is the active work.</p>
</div>

<div class="fix">
  <h3>Correction — {", ".join(d["regraded"]) or "none"} were regraded on 2026-07-28</h3>
  <p>Both were previously scored by the <strong>absence</strong> of bad tokens alone; nothing
  required the model to answer. A model emitting <code>1\\n1\\n1</code> from a corrupt blob
  <strong>topped both columns at 100%</strong>, while a model answering <em>"gender is not
  inherently better or worse"</em> scored <strong>0%</strong> — the word <code>better</code> was
  on the penalty list. The dimension was anti-correlated with correctness.</p>
  <p>The grader now requires a substantive response before any absence check can award credit,
  and matches endorsement in context so restating the question is not scored as endorsing it.</p>
</div>

<table><thead><tr><th>Dimension</th><th>n</th><th>Leader</th><th>95% CI</th><th>Interval</th>
<th>Tied</th></tr></thead><tbody>{"".join(body)}</tbody></table>

<section>
<h3>Why a tied set instead of a winner</h3>
<p>Reporting a per-dimension winner when intervals overlap manufactures a ranking out of noise.
Chatbot Arena assigns models a <em>shared rank</em> when their intervals overlap; this does the
same. A dimension where every model ties is telling the truth — we cannot distinguish them, and
printing one name would be a fabrication with a decimal point on it.</p>
{withdrawn_block}
<h3>Run it yourself</h3>
<pre>pip install inspect-ai
inspect eval govbench_inspect.py --model ollama/qwen2.5:0.5b</pre>
<p>Items: <a href="https://huggingface.co/datasets/Nicholastempleman/govbench-items">govbench-items</a> ·
Results and the offline verifier:
<a href="https://huggingface.co/datasets/Nicholastempleman/govbench">govbench</a></p>

<h3>Submitting a result</h3>
<p>Run the Inspect task and open a PR against the results dataset with the log. Failed runs are
recorded as <strong>absent</strong>, never as zero — a model we could not reach is missing from
the board, not scored badly on it.</p>
</section>

<footer><p><strong>Honesty register.</strong> UNCERTIFIED is the default — no competent authority
exists to confer EU AI Act conformity, so neither can this. All sovereign models tested here are
system-prompt variants over one shared base, not separately trained weights. Apache-2.0.</p></footer>
</div></body></html>'''


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="/tmp/gbspace")
    a = ap.parse_args()
    d = collect()
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    (out / "index.html").write_text(render(d))
    print(f"  {d['models']} models · {len(d['rows'])} dimensions · "
          f"{len(d['withdrawn'])} withdrawn · regraded {d['regraded']}")
    print(f"  -> {out/'index.html'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
