#!/usr/bin/env python3
"""drift_feed.py — Public drift feed over the existing board.

Reads every lens artefact on disk, the flywheel results, and the decision ledger,
and emits a single drift-feed.json that any static host can serve. The HTML page
(hub-tour or sovereign.html) fetches this JSON and renders it.

No new measurements. No model calls. No GPU. Just what's already on disk.

    python3 drift_feed.py                   # writes drift-feed.json to stdout
    python3 drift_feed.py --out feed.json   # writes to file
    python3 drift_feed.py --html feed.html  # writes a self-contained HTML page
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "benchmark-results"

# Import the instrument and ledger directly
sys.path.insert(0, str(HERE))
from sov_instrument import LENSES, Instrument
from decision_ledger import build_seed_ledger


def _read_json(path: Path) -> dict | list | None:
    try:
        return json.loads(path.read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def _provbench_summary() -> dict | None:
    data = _read_json(RESULTS / "provbench.json")
    if not data:
        return None
    cells = data.get("cells", [])
    total = len(cells)
    survived = sum(1 for c in cells if c.get("outcome") == "survived")
    destroyed = sum(1 for c in cells if c.get("outcome") == "destroyed")
    unmeasured = sum(1 for c in cells if c.get("outcome") == "unmeasured")
    return {
        "n_assets_marked": data.get("n_assets_marked", 0),
        "total_cells": total,
        "survived": survived,
        "destroyed": destroyed,
        "unmeasured": unmeasured,
        "survival_rate": round(survived / total, 4) if total else 0,
        "ci_note": "asset-clustered Clopper-Pearson one-sided [0.0%, 24.2%] at n=12",
    }


def _defbench_summary() -> dict | None:
    data = _read_json(RESULTS / "defbench.json")
    if not data:
        return None
    stats = data.get("battery_stats", {})
    return {
        "total_items": stats.get("total", 0),
        "harmful": stats.get("harmful", 0),
        "benign": stats.get("benign", 0),
        "axes_resolved": data.get("axes_resolved", 0),
    }


def _system_analysis_summary() -> dict | None:
    data = _read_json(RESULTS / "system_analysis.json")
    if not data:
        return None
    return {
        "n": data.get("n"),
        "mean": data.get("mean"),
        "ci": data.get("ci"),
        "clustered_ci": data.get("clustered_ci"),
        "deff": data.get("deff"),
        "n_eff": data.get("n_eff"),
    }


def _pqcbench_summary() -> dict | None:
    data = _read_json(RESULTS / "pqcbench.json")
    if not data:
        return None
    subjects = data.get("subjects", [])
    if not subjects:
        # Try alternative structure
        results = data.get("results", [])
        return {
            "total_subjects": len(results),
            "note": "All four SIGIL chains fail every criterion (no alg_id, no hybrid, no RFC 3161 token)",
        }
    return {
        "total_subjects": len(subjects),
        "note": "All four SIGIL chains fail every criterion (no alg_id, no hybrid, no RFC 3161 token)",
    }


def _flywheel_latest() -> dict | None:
    fw_dir = RESULTS / "flywheel"
    if not fw_dir.exists():
        return None
    files = sorted(fw_dir.glob("*.json"), reverse=True)
    if not files:
        return None
    data = _read_json(files[0])
    if not data:
        return None
    models = data.get("summary", {}).get("models", {})
    model_summary = {}
    for name, stats in models.items():
        model_summary[name] = {
            "practice_accuracy": stats.get("practice", {}).get("accuracy"),
            "held_out_accuracy": stats.get("held_out", {}).get("accuracy"),
            "overfit_gap": stats.get("overfit_gap"),
        }
    return {
        "day": data.get("day"),
        "models": model_summary,
        "fuel_pairs": data.get("fuel", {}).get("pairs"),
    }


def _decision_ledger_summary() -> list[dict]:
    led = build_seed_ledger()
    out = []
    for r in led.export():
        out.append({
            "record_id": r["record_id"],
            "kind": r["kind"],
            "claim": r["claim"],
            "verdict": r["verdict"],
            "tag": r["tag"],
            "superseded_by": r.get("superseded_by"),
        })
    return out


def _care_gate_summary() -> dict | None:
    data = _read_json(RESULTS / "care_gate_eval.json")
    if not data:
        return None
    v2 = data.get("v2", {})
    battery = data.get("battery", {})
    return {
        "total_items": battery.get("total", 0),
        "harmful": battery.get("harmful", 0),
        "benign": battery.get("benign", 0),
        "recall": v2.get("recall"),
        "precision": v2.get("precision"),
        "overblock_rate": v2.get("overblock_rate"),
        "tp": v2.get("tp"),
        "fn": v2.get("fn"),
        "fp": v2.get("fp"),
        "tn": v2.get("tn"),
    }


def _crosswalk_summary() -> dict | None:
    data = _read_json(RESULTS / "coverage_crosswalk.json")
    if not data:
        return None
    fc = data.get("field_coverage", {})
    by_inst = data.get("by_instrument", {})
    sources = data.get("sources", [])
    return {
        "provisions": data.get("provisions", 0),
        "axes": data.get("axes", 0),
        "modes": data.get("modes", 0),
        "cells": data.get("cells", 0),
        "field_coverage": {
            "absent": fc.get("absent", 0),
            "partial": fc.get("partial", 0),
            "covered": fc.get("covered", 0),
        },
        "gap_reasons": data.get("gap_reasons", {}),
        "by_instrument": {k: {"cells": v["cells"], "covered": v["covered"], "absent": v["absent"]}
                          for k, v in by_inst.items()},
        "sources_count": len(sources),
        "survey_status": data.get("survey_status", ""),
    }


def _equivalence_classes() -> list[dict]:
    ec_dir = HERE / "equivalence_classes"
    if not ec_dir.exists():
        return []
    out = []
    for f in sorted(ec_dir.glob("*.json")):
        data = _read_json(f)
        if not data:
            continue
        out.append({
            "ec_id": data.get("ec_id"),
            "obligation_type": data.get("obligation_type"),
            "axis": data.get("axis"),
            "members": len(data.get("members", [])),
            "signed": data.get("signature", "").startswith("UNSIGNED") is False,
        })
    return out


def _sov_time_stats() -> dict:
    """Read the spacetime canvas ledger if it exists."""
    sys.path.insert(0, str(HERE))
    try:
        from sov_time import load_events
        events = load_events()
    except Exception:
        return {"events": 0, "by_kind": {}}
    by_kind = {}
    for ev in events:
        k = ev.get("kind", "?")
        by_kind[k] = by_kind.get(k, 0) + 1
    signed = sum(1 for ev in events if ev.get("canvas_cell_hash"))
    return {
        "events": len(events),
        "signed": signed,
        "by_kind": by_kind,
        "ledger": "benchmark-results/sov_time_ledger.jsonl",
    }


def _corpus_watch_latest() -> dict | None:
    watch_file = HERE / "watch-result.json"
    return _read_json(watch_file)


def build_drift_feed() -> dict:
    ins = Instrument()
    lens_status = {}
    for name, lens in LENSES.items():
        artefact = RESULTS.parent / lens["evidence"]
        lens_status[name] = {
            "status": lens["status"],
            "claim": lens["claim"],
            "asks": lens["asks"],
            "artefact_exists": artefact.exists(),
            "caveat": lens.get("caveat"),
        }

    return {
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "instrument": {
            "guard": ins.guard(),
            "lens_count": len(LENSES),
            "lenses": lens_status,
        },
        "provbench": _provbench_summary(),
        "defbench": _defbench_summary(),
        "governance": _system_analysis_summary(),
        "pqcbench": _pqcbench_summary(),
        "flywheel": _flywheel_latest(),
        "care_gate": _care_gate_summary(),
        "crosswalk": _crosswalk_summary(),
        "equivalence_classes": _equivalence_classes(),
        "decision_ledger": _decision_ledger_summary(),
        "sov_time": _sov_time_stats(),
        "corpus_watch": _corpus_watch_latest(),
    }


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>CSOAI — Public Drift Feed</title>
<style>
  :root {
    --bg: #0E1116; --panel: #161B22; --border: #2D333B;
    --text: #E6EDF3; --muted: #8B949E; --dim: #6E7681;
    --good: #3FB950; --bad: #F85149; --warn: #D29922; --link: #2F81F7;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { background: var(--bg); color: var(--text); font: 13px/1.6 system-ui, sans-serif; padding: 24px; }
  h1 { font-size: 18px; font-weight: 600; margin-bottom: 8px; }
  h2 { font-size: 15px; font-weight: 600; margin: 24px 0 8px; color: var(--muted); }
  .meta { color: var(--dim); font-size: 12px; margin-bottom: 16px; }
  .card { background: var(--panel); border: 1px solid var(--border); border-radius: 8px; padding: 16px; margin-bottom: 12px; }
  .lens { display: grid; grid-template-columns: 120px 80px 1fr; gap: 8px; align-items: start; margin-bottom: 8px; }
  .lens-name { font-weight: 600; }
  .status-MEASURED { color: var(--good); }
  .status-UNVERIFIED { color: var(--warn); }
  .claim { color: var(--muted); font-size: 12px; }
  table { width: 100%; border-collapse: collapse; font-size: 12px; }
  th, td { text-align: left; padding: 6px 8px; border-bottom: 1px solid var(--border); }
  th { color: var(--muted); font-weight: 600; }
  .tag-MEASURED { color: var(--good); }
  .tag-LEAD { color: var(--warn); }
  .tag-REFUTED { color: var(--bad); }
  .verdict-OPEN { color: var(--warn); }
  .verdict-SETTLED { color: var(--good); }
  .verdict-CONFIRMED { color: var(--good); }
  .gap-negative { color: var(--good); }
  .gap-positive { color: var(--warn); }
  .guard-ok { color: var(--good); font-family: monospace; font-size: 12px; }
  .artefact-missing { color: var(--bad); }
  .artefact-present { color: var(--good); }
</style>
</head>
<body>
<h1>CSOAI — Public Drift Feed</h1>
<div class="meta">Generated: <span id="ts"></span>. No new measurements — reads what's on disk.</div>

<h2>Instrument Guard</h2>
<div class="card"><div id="guard" class="guard-ok"></div></div>

<h2>Lens Status</h2>
<div class="card" id="lenses"></div>

<h2>ProvBench — Provenance Survival</h2>
<div class="card" id="provbench"></div>

<h2>DefBench — Safety Gate</h2>
<div class="card" id="defbench"></div>

<h2>Governance — Pipeline Score</h2>
<div class="card" id="governance"></div>

<h2>PQCBench — Continuity</h2>
<div class="card" id="pqcbench"></div>

<h2>Care Gate — Deterministic Safety Gate</h2>
<div class="card" id="care_gate"></div>

<h2>Flywheel — Latest Run</h2>
<div class="card" id="flywheel"></div>

<h2>Crosswalk Gap Map — 417 Provisions × 4 Axes × 2 Modes</h2>
<div class="card" id="crosswalk"></div>

<h2>Decision Ledger</h2>
<div class="card" id="ledger"></div>

<h2>Equivalence Classes</h2>
<div class="card" id="equiv"></div>

<h2>SOV-Space Spacetime Canvas</h2>
<div class="card" id="sov_time"></div>

<h2>Corpus Watch</h2>
<div class="card" id="corpus"></div>

<script>
fetch('./drift-feed.json').then(r=>r.json()).then(render).catch(e=>{
  document.body.innerHTML='<p style="color:#F85149">Failed to load drift-feed.json: '+e+'</p>';
});

function render(d) {
  document.getElementById('ts').textContent = d.generated_at;
  document.getElementById('guard').textContent = d.instrument.guard;

  // Lenses
  let lh='';
  for (const [name, l] of Object.entries(d.instrument.lenses)) {
    lh += `<div class="lens">
      <span class="lens-name">${name}</span>
      <span class="status-${l.status}">${l.status}</span>
      <span class="claim">${l.claim}${l.artefact_exists?'':' <span class="artefact-missing">(artefact missing)</span>'}</span>
    </div>`;
  }
  document.getElementById('lenses').innerHTML = lh;

  // ProvBench
  const p = d.provbench;
  document.getElementById('provbench').innerHTML = p ?
    `<table><tr><th>Assets marked</th><th>Total cells</th><th>Survived</th><th>Destroyed</th><th>Unmeasured</th><th>Survival rate</th><th>CI</th></tr>
     <tr><td>${p.n_assets_marked}</td><td>${p.total_cells}</td><td>${p.survived}</td><td>${p.destroyed}</td><td>${p.unmeasured}</td><td>${(p.survival_rate*100).toFixed(1)}%</td><td>${p.ci_note}</td></tr></table>`
    : '<span class="artefact-missing">provbench.json not found</span>';

  // DefBench
  const df = d.defbench;
  document.getElementById('defbench').innerHTML = df ?
    `<table><tr><th>Total items</th><th>Harmful</th><th>Benign</th><th>Axes resolved</th></tr>
     <tr><td>${df.total_items}</td><td>${df.harmful}</td><td>${df.benign}</td><td>${df.axes_resolved}</td></tr></table>`
    : '<span class="artefact-missing">defbench.json not found</span>';

  // Governance
  const g = d.governance;
  document.getElementById('governance').innerHTML = g ?
    `<table><tr><th>n</th><th>Mean</th><th>Clustered CI</th><th>deff</th><th>n_eff</th></tr>
     <tr><td>${g.n}</td><td>${g.mean}</td><td>${JSON.stringify(g.clustered_ci)}</td><td>${g.deff}</td><td>${g.n_eff}</td></tr></table>`
    : '<span class="artefact-missing">system_analysis.json not found</span>';

  // PQCBench
  const pq = d.pqcbench;
  document.getElementById('pqcbench').innerHTML = pq ?
    `<div>${pq.total_subjects} subjects measured. ${pq.note}</div>`
    : '<span class="artefact-missing">pqcbench.json not found</span>';

  // Care Gate
  const cg = d.care_gate;
  if (cg) {
    let cgh = `<table><tr><th>Recall</th><th>Precision</th><th>Over-block</th><th>TP</th><th>FN</th><th>FP</th><th>TN</th></tr>`;
    cgh += `<tr><td>${(cg.recall*100).toFixed(1)}%</td><td>${(cg.precision*100).toFixed(1)}%</td><td>${(cg.overblock_rate*100).toFixed(1)}%</td><td>${cg.tp}</td><td>${cg.fn}</td><td>${cg.fp}</td><td>${cg.tn}</td></tr></table>`;
    cgh += `<div class="meta" style="margin-top:8px">${cg.total_items} items (${cg.harmful} harmful, ${cg.benign} benign). Deterministic gate — no LLM calls.</div>`;
    document.getElementById('care_gate').innerHTML = cgh;
  } else {
    document.getElementById('care_gate').innerHTML = '<span class="artefact-missing">care_gate_eval.json not found</span>';
  }

  // Flywheel
  const fw = d.flywheel;
  if (fw) {
    let fwh = `<div>Day: ${fw.day}. Fuel pairs: ${fw.fuel_pairs}.</div><table><tr><th>Model</th><th>Practice acc</th><th>Held-out acc</th><th>Overfit gap</th></tr>`;
    for (const [m, s] of Object.entries(fw.models)) {
      const gap = s.overfit_gap;
      const cls = gap <= 0 ? 'gap-negative' : 'gap-positive';
      fwh += `<tr><td>${m}</td><td>${(s.practice_accuracy*100).toFixed(1)}%</td><td>${(s.held_out_accuracy*100).toFixed(1)}%</td><td class="${cls}">${gap.toFixed(3)}</td></tr>`;
    }
    fwh += '</table>';
    document.getElementById('flywheel').innerHTML = fwh;
  } else {
    document.getElementById('flywheel').innerHTML = '<span class="artefact-missing">No flywheel results yet</span>';
  }

  // Crosswalk
  const cw2 = d.crosswalk;
  if (cw2) {
    let cwh = `<div>${cw2.provisions} provisions across ${cw2.axes} axes × ${cw2.modes} modes = ${cw2.cells} cells. `;
    cwh += `<strong>${cw2.field_coverage.covered} covered</strong>, ${cw2.field_coverage.partial} partial, ${cw2.field_coverage.absent} absent. `;
    cwh += `${cw2.sources_count} benchmark sources surveyed.</div>`;
    cwh += `<table><tr><th>Instrument</th><th>Cells</th><th>Covered</th><th>Absent</th></tr>`;
    for (const [name, v] of Object.entries(cw2.by_instrument)) {
      cwh += `<tr><td>${name}</td><td>${v.cells}</td><td>${v.covered}</td><td>${v.absent}</td></tr>`;
    }
    cwh += `</table>`;
    cwh += `<div class="meta" style="margin-top:8px">${cw2.survey_status}</div>`;
    document.getElementById('crosswalk').innerHTML = cwh;
  } else {
    document.getElementById('crosswalk').innerHTML = '<span class="artefact-missing">coverage_crosswalk.json not found</span>';
  }

  // Decision Ledger
  let llh='<table><tr><th>ID</th><th>Kind</th><th>Tag</th><th>Verdict</th><th>Claim</th></tr>';
  for (const r of d.decision_ledger) {
    llh += `<tr><td>${r.record_id}</td><td>${r.kind}</td><td class="tag-${r.tag}">${r.tag}</td><td class="verdict-${r.verdict}">${r.verdict}</td><td>${r.claim}</td></tr>`;
  }
  llh += '</table>';
  document.getElementById('ledger').innerHTML = llh;

  // Equivalence Classes
  const eqs = d.equivalence_classes;
  if (eqs && eqs.length > 0) {
    let eqh = `<table><tr><th>EC ID</th><th>Obligation</th><th>Axis</th><th>Members</th><th>Signed</th></tr>`;
    for (const e of eqs) {
      eqh += `<tr><td>${e.ec_id}</td><td>${e.obligation_type}</td><td>${e.axis}</td><td>${e.members}</td><td>${e.signed ? 'yes' : '<span class="artefact-missing">placeholder</span>'}</td></tr>`;
    }
    eqh += '</table>';
    document.getElementById('equiv').innerHTML = eqh;
  } else {
    document.getElementById('equiv').innerHTML = '<div>No equivalence classes loaded yet.</div>';
  }

  // SOV-Space Spacetime Canvas
  const st = d.sov_time;
  if (st && st.events > 0) {
    let sth = `<div>${st.events} events recorded, ${st.signed} c2pa-signed.`;
    sth += ` <a href="./sov-time-canvas.html" target="_blank" style="color:#2F81F7">View canvas →</a></div>`;
    sth += `<table style="margin-top:8px"><tr><th>Kind</th><th>Count</th></tr>`;
    for (const [kind, n] of Object.entries(st.by_kind)) {
      sth += `<tr><td>${kind}</td><td>${n}</td></tr>`;
    }
    sth += '</table>';
    document.getElementById('sov_time').innerHTML = sth;
  } else {
    document.getElementById('sov_time').innerHTML = '<div class="artefact-missing">No events recorded yet.</div>';
  }

  // Corpus Watch
  const cw = d.corpus_watch;
  document.getElementById('corpus').innerHTML = cw ?
    `<div>Last watch: ${cw.watched_at}. C2PA: ${cw.c2pa_latest}. AI Act HTTP: ${cw.ai_act_status}. UK GDPR HTTP: ${cw.uk_gdpr_status}. NIST IR 8547: ${cw.nist_ir8547_status}. Decision ledger selftest: ${cw.decision_ledger_selftest}. Instrument selftest: ${cw.sov_instrument_selftest}.</div>`
    : '<div class="artefact-missing">No corpus watch results yet. Run corpus-watch.yml workflow.</div>';
}
</script>
</body>
</html>"""


if __name__ == "__main__":
    feed = build_drift_feed()

    if "--html" in sys.argv:
        i = sys.argv.index("--html")
        out = sys.argv[i + 1] if i + 1 < len(sys.argv) else "drift-feed.html"
        # Inject the JSON directly into the HTML so it's self-contained
        html = HTML_TEMPLATE.replace(
            "fetch('./drift-feed.json').then(r=>r.json()).then(render)",
            f"render({json.dumps(feed)})"
        )
        Path(out).write_text(html)
        print(f"wrote {out} ({len(html)} bytes)")
    elif "--out" in sys.argv:
        i = sys.argv.index("--out")
        out = sys.argv[i + 1] if i + 1 < len(sys.argv) else "drift-feed.json"
        Path(out).write_text(json.dumps(feed, indent=2))
        print(f"wrote {out}")
    else:
        print(json.dumps(feed, indent=2))
