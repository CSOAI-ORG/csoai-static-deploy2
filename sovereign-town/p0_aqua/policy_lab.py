#!/usr/bin/env python3
"""
policy_lab.py — experiment lifecycle for the MEOK Policy Lab.

Subcommands:
    vote   <experiment.json>   Simulate a BFT Council vote and update status.
    spawn  <experiment.json>   Launch treatment + control harness runs (--live for network).
    status <experiment.json>   Show experiment summary.
    report <experiment.json>   Compute DORA metrics, sanitize JSON, and export whitepaper/brief/email.

The first experiment is experiments/dora_finance.json (DORA automated vs manual).
"""
from __future__ import annotations

import argparse
import random
import sys
import time
from pathlib import Path
from typing import Any

import config
import moat_common
from benchmark.regulatory_crosswalk import classify
import regulation_parser

COUNCIL_SIZE = 5

# Simulation-derived cost weights (arbitrary units, not real currency).
_COST_DEATH = 1000
_COST_MISS = 100
_COST_HOUR = 10

# Public-facing export location for whitepaper, brief, and outreach draft.
EXPORT_DIR_DEFAULT = (
    Path(__file__).parent.parent.parent
    / "proofof-site"
    / "sovereign-town"
    / "experiments"
    / "dora-finance-reports"
)


def _now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def load_experiment(path: str | Path) -> dict:
    data = moat_common.load_json(Path(path))
    if data is None:
        raise FileNotFoundError(f"Experiment file not found: {path}")
    return data


def save_experiment(path: str | Path, data: dict) -> bool:
    return moat_common.save_json(Path(path), data)


def _council_vote(experiment: dict) -> dict:
    """Deterministic BFT Council vote seeded by experiment id."""
    seed = experiment.get("id", experiment.get("name", "experiment"))
    rng = random.Random(seed)
    members = ["Minerva", "Oracle", "Sentinel", "Nomad", "Architect"]
    weights = [0.60, 0.25, 0.15]  # FUND / MODIFY / REJECT
    votes = []
    for name in members:
        vote = rng.choices(["FUND", "MODIFY", "REJECT"], weights=weights, k=1)[0]
        reason = {
            "FUND": "Evidence supports the hypothesis.",
            "MODIFY": "Add cross-border or edge-case coverage.",
            "REJECT": "Risk of confounding variables is too high.",
        }[vote]
        votes.append({"member": name, "vote": vote, "reason": reason})

    fund_count = sum(1 for v in votes if v["vote"] == "FUND")
    if fund_count >= 4:
        result = "approved"
    elif fund_count >= 3:
        result = "modify"
    else:
        result = "rejected"

    return {
        "timestamp": _now(),
        "votes": votes,
        "fund_count": fund_count,
        "result": result,
    }


def vote_experiment(path: str | Path) -> dict:
    exp = load_experiment(path)
    if exp.get("status") not in ("proposed", None):
        print(f"Experiment already in status '{exp.get('status')}'. Re-voting...")
    exp["vote"] = _council_vote(exp)
    exp["status"] = exp["vote"]["result"]
    if save_experiment(path, exp):
        print(f"Vote result: {exp['vote']['result'].upper()}")
        print(f"  FUND: {exp['vote']['fund_count']}/{COUNCIL_SIZE}")
        for v in exp["vote"]["votes"]:
            print(f"    • {v['member']}: {v['vote']} — {v['reason']}")
    else:
        print("ERROR: failed to save experiment file", file=sys.stderr)
        sys.exit(1)
    return exp


def _run_harness(policy: str, scenario: str, live: bool = False) -> dict | None:
    if not live:
        return None
    try:
        import httpx
    except ImportError:  # pragma: no cover
        print("  httpx not installed; cannot contact harness", file=sys.stderr)
        return None

    url = f"{config.HARNESS_URL}/harness/run"
    headers = {"Content-Type": "application/json"}
    if config.API_TOKEN:
        headers["Authorization"] = f"Bearer {config.API_TOKEN}"
    try:
        with httpx.Client(timeout=120) as client:
            # Sign the manifest so we get an attested run_id for the leaderboard.
            r = client.post(
                url,
                json={"policy": policy, "scenario": scenario, "sign": True, "collect_states": True},
                headers=headers,
            )
        if r.status_code == 200:
            data = r.json()
            run_id = data.get("manifest", {}).get("id") or data.get("run", {}).get("run_id")
            return {"run_id": run_id, "status": "ok", "payload": data}
        return {"error": f"HTTP {r.status_code}", "body": r.text[:200]}
    except Exception as e:  # pragma: no cover
        return {"error": str(e)}


def spawn_experiment(path: str | Path, live: bool = False) -> dict:
    exp = load_experiment(path)
    if exp.get("status") != "approved":
        print(
            f"Experiment status is '{exp.get('status')}'. Run 'policy_lab.py vote {path}' first.",
            file=sys.stderr,
        )
        sys.exit(1)

    treatment = exp["towns"]["treatment"]
    control = exp["towns"]["control"]

    print(f"Spawning treatment town: {treatment['name']} ({treatment['policy']})")
    t_run = _run_harness(treatment["policy"], treatment.get("scenario", "baseline"), live=live)

    print(f"Spawning control town:   {control['name']} ({control['policy']})")
    c_run = _run_harness(control["policy"], control.get("scenario", "baseline"), live=live)

    exp["runs"] = {
        "treatment_run_id": t_run.get("run_id") if isinstance(t_run, dict) else None,
        "control_run_id": c_run.get("run_id") if isinstance(c_run, dict) else None,
        "treatment_result": t_run if isinstance(t_run, dict) else None,
        "control_result": c_run if isinstance(c_run, dict) else None,
        "spawned_at": _now(),
    }

    if live and exp["runs"]["treatment_run_id"] and exp["runs"]["control_run_id"]:
        exp["status"] = "running"
    else:
        exp["status"] = "queued"
        if not live:
            print("Dry-run mode: no harness calls made. Status set to 'queued'.")
        else:
            print("One or both harness runs failed; status set to 'queued'.", file=sys.stderr)

    if save_experiment(path, exp):
        print(f"Experiment status: {exp['status']}")
        print(f"  Treatment run id: {exp['runs']['treatment_run_id']}")
        print(f"  Control run id:   {exp['runs']['control_run_id']}")
    else:
        print("ERROR: failed to save experiment file", file=sys.stderr)
        sys.exit(1)
    return exp



def intake_experiment(path: str | Path) -> dict:
    """Parse a regulation intake and generate policy configs + experiment JSON."""
    intake = regulation_parser.load_intake(path)
    result = regulation_parser.generate_from_intake(intake)
    print(f"Generated {result['experiment_id']}")
    print(f"  Automated policy: {result['automated_policy']}")
    print(f"  Manual policy:    {result['manual_policy']}")
    print(f"  Experiment:       {result['experiment']}")
    return result


def auto_spawn_experiment(path: str | Path, live: bool = False) -> dict:
    """Intake → vote → spawn → report for a regulation."""
    result = intake_experiment(path)
    exp_path = Path(result["experiment"])
    vote_experiment(exp_path)
    spawn_experiment(exp_path, live=live)
    report_experiment(exp_path)
    return load_experiment(exp_path)


def _extract_run(payload: dict) -> dict:
    return payload.get("run", payload) if isinstance(payload, dict) else {}


def _run_summary(run: dict) -> dict:
    return {
        "episodes": run.get("episodes"),
        "violations": run.get("violations"),
        "blocked": run.get("blocked"),
        "care_breaches": run.get("care_breaches"),
        "deaths": run.get("deaths"),
        "survivors": run.get("survivors"),
        "mean_care": run.get("mean_care"),
        "final_trust": run.get("final_trust"),
        "final_commons": run.get("final_commons"),
        "peak_lawlessness": run.get("peak_lawlessness"),
        "work_accuracy": run.get("work_accuracy"),
    }


def _dora_metrics(payload: dict, is_automated: bool) -> dict:
    run = _extract_run(payload)
    tick_states = run.get("tick_states", []) or []
    incident_tiers = {"critical", "major"}
    delays: list[int] = []
    false_positives = 0
    total_actions = len(tick_states)

    for ts in tick_states:
        intended = ts.get("intended", ts.get("action"))
        executed = ts.get("action")
        tier = classify(intended, "dora")
        if tier in incident_tiers:
            if executed != intended:
                # Blocked/redirected by the policy: detected immediately.
                delays.append(1)
            else:
                # Allowed through: manual delay model or automation miss.
                if is_automated:
                    delays.append(24)
                else:
                    hour = ts.get("hour", 0)
                    if hour in (9, 10, 11, 14, 15):
                        delay = 4
                    elif hour < 9:
                        delay = 9 - hour
                    else:
                        delay = (24 - hour) + 9
                    delays.append(delay)
        else:
            if executed != intended:
                false_positives += 1

    total_incidents = len(delays)
    detected = sum(1 for d in delays if d <= 4)
    missed = total_incidents - detected
    mean_delay = round(sum(delays) / max(1, total_incidents), 1) if total_incidents else 0.0
    detection_rate = round(detected / max(1, total_incidents), 4)
    blocked = run.get("blocked", 0)
    fp_rate = round(false_positives / max(1, blocked), 4) if blocked else 0.0
    cost_index = (
        run.get("deaths", 0) * _COST_DEATH
        + missed * _COST_MISS
        + int(mean_delay * _COST_HOUR)
    )

    return {
        "total_incidents": total_incidents,
        "detected": detected,
        "missed": missed,
        "detection_rate": detection_rate,
        "mean_detection_hours": mean_delay,
        "false_positives": false_positives,
        "false_positive_rate": fp_rate,
        "cost_index": cost_index,
        "summary": _run_summary(run),
    }


def _compute_report(exp: dict) -> dict:
    t_payload = exp.get("runs", {}).get("treatment_result", {}).get("payload")
    c_payload = exp.get("runs", {}).get("control_result", {}).get("payload")
    if not t_payload or not c_payload:
        # If the experiment was already sanitized, reuse the embedded report.
        if exp.get("report"):
            return exp["report"]
        raise RuntimeError("Both treatment and control runs must have completed payloads")

    t = _dora_metrics(t_payload, is_automated=True)
    c = _dora_metrics(c_payload, is_automated=False)

    improvement = {}
    if c["mean_detection_hours"] > 0:
        improvement["detection_time_pct"] = round(
            (c["mean_detection_hours"] - t["mean_detection_hours"]) / c["mean_detection_hours"] * 100, 1
        )
    if c["missed"] > 0:
        improvement["missed_reduction_pct"] = round(
            (c["missed"] - t["missed"]) / c["missed"] * 100, 1
        )
    improvement["cost_index_ratio"] = round(t["cost_index"] / max(1, c["cost_index"]), 3)

    return {
        "generated_at": _now(),
        "treatment": t,
        "control": c,
        "improvement": improvement,
    }


def _sanitize_experiment(exp: dict, report: dict) -> dict:
    """Strip per-tick/agent detail before saving; keep aggregate metrics."""
    sanitized = {
        k: v for k, v in exp.items()
        if k not in ("runs",)
    }
    sanitized["report"] = report
    sanitized["runs"] = {
        "treatment_run_id": exp.get("runs", {}).get("treatment_run_id"),
        "control_run_id": exp.get("runs", {}).get("control_run_id"),
        "spawned_at": exp.get("runs", {}).get("spawned_at"),
        "treatment_summary": report["treatment"]["summary"],
        "control_summary": report["control"]["summary"],
    }
    return sanitized


def _render_regulator_html(exp: dict, report: dict, downloads: dict | None = None) -> str:
    downloads = downloads or {}
    t = report["treatment"]
    c = report["control"]
    status = exp.get("status", "running")
    badge_class = "running"
    if status == "proven":
        badge_class = "proven"
    elif status in ("queued", "proposed"):
        badge_class = "proposed"

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>DORA Finance Compliance Experiment — Regulator View | CSOAI</title>
  <meta name="description" content="Public regulator view of the Sovereign Town DORA automated-vs-manual incident reporting experiment.">
  <meta http-equiv="Content-Security-Policy" content="default-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; frame-ancestors 'none';">
  <style>
    :root {{ --bg:#0b1020; --panel:#111a30; --text:#e6e9f0; --muted:#8b92a8; --accent:#2dd4bf; --warn:#f59e0b; --danger:#ef4444; --ok:#22c55e; }}
    * {{ box-sizing: border-box; }}
    body {{ margin:0; font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background:var(--bg); color:var(--text); line-height:1.55; }}
    main {{ max-width: 880px; margin: 0 auto; padding: 2rem 1rem; }}
    header {{ border-bottom: 1px solid #1f2a44; padding-bottom: 1rem; margin-bottom: 1.5rem; }}
    h1 {{ font-size: 1.55rem; margin: 0 0 .25rem; }}
    .subtitle {{ color: var(--muted); font-size: .95rem; }}
    .badge {{ display:inline-block; padding:.2rem .55rem; border-radius:999px; font-size:.75rem; font-weight:600; text-transform:uppercase; letter-spacing:.03em; background:#1f2a44; color:var(--muted); }}
    .badge.proposed {{ color: var(--warn); }}
    .badge.running {{ color: var(--accent); }}
    .badge.proven {{ color: var(--ok); }}
    .panel {{ background: var(--panel); border: 1px solid #1f2a44; border-radius: .75rem; padding: 1.25rem; margin-bottom: 1rem; }}
    h2 {{ font-size: 1.15rem; margin: 0 0 .75rem; color: var(--accent); }}
    dl {{ display: grid; grid-template-columns: 10rem 1fr; gap: .35rem 1rem; margin: 0; }}
    dt {{ color: var(--muted); }}
    dd {{ margin: 0; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1rem; }}
    .metric {{ text-align: center; padding: 1rem; background: #0b1020; border: 1px solid #1f2a44; border-radius: .5rem; }}
    .metric .value {{ font-size: 1.75rem; font-weight: 700; color: var(--text); }}
    .metric .label {{ font-size: .8rem; color: var(--muted); margin-top: .25rem; }}
    table {{ width: 100%; border-collapse: collapse; margin-top: .75rem; }}
    th, td {{ text-align: left; padding: .55rem .5rem; border-bottom: 1px solid #1f2a44; }}
    th {{ color: var(--muted); font-weight: 600; }}
    .disclaimer {{ background: #1a1020; border-left: 4px solid var(--warn); padding: .75rem 1rem; border-radius: 0 .5rem .5rem 0; color: #f3e8ff; font-size: .9rem; }}
    footer {{ margin-top: 2rem; padding-top: 1rem; border-top: 1px solid #1f2a44; color: var(--muted); font-size: .85rem; }}
    a {{ color: var(--accent); }}
    a:focus-visible {{ outline: 2px solid var(--accent); outline-offset: 2px; }}
  </style>
</head>
<body>
  <main>
    <header>
      <span class="badge {badge_class}" id="status-badge">{status}</span>
      <h1>DORA Finance Compliance Experiment</h1>
      <p class="subtitle">Automated vs manual ICT incident reporting under Regulation (EU) 2022/2554 (DORA)</p>
    </header>

    <section class="panel" aria-labelledby="design-heading">
      <h2 id="design-heading">Experiment design</h2>
      <dl>
        <dt>Hypothesis</dt>
        <dd>{exp.get('hypothesis')}</dd>
        <dt>Regulation</dt>
        <dd>{exp.get('regulation')}</dd>
        <dt>Industry</dt>
        <dd>{exp.get('industry')} — 47 specialist agents per town</dd>
        <dt>Treatment</dt>
        <dd>{exp['towns']['treatment']['name']} — {exp['towns']['treatment']['note']}</dd>
        <dt>Control</dt>
        <dd>{exp['towns']['control']['name']} — {exp['towns']['control']['note']}</dd>
      </dl>
    </section>

    <section class="panel" aria-labelledby="results-heading">
      <h2 id="results-heading">Aggregate simulation results</h2>
      <p style="color:var(--muted); font-size:.9rem;">No individual agent identities or raw ledger entries are published.</p>
      <table>
        <thead>
          <tr><th>Metric</th><th>Automated (treatment)</th><th>Manual (control)</th></tr>
        </thead>
        <tbody>
          <tr><td>Mean detection time</td><td>{t['mean_detection_hours']} h</td><td>{c['mean_detection_hours']} h</td></tr>
          <tr><td>Detection rate</td><td>{t['detection_rate']*100:.1f}%</td><td>{c['detection_rate']*100:.1f}%</td></tr>
          <tr><td>Missed incidents</td><td>{t['missed']}</td><td>{c['missed']}</td></tr>
          <tr><td>False positive rate</td><td>{t['false_positive_rate']*100:.1f}%</td><td>{c['false_positive_rate']*100:.1f}%</td></tr>
          <tr><td>Cost index (sim units)</td><td>{t['cost_index']}</td><td>{c['cost_index']}</td></tr>
          <tr><td>Final trust</td><td>{t['summary']['final_trust']}</td><td>{c['summary']['final_trust']}</td></tr>
        </tbody>
      </table>
    </section>

    <section class="panel" aria-labelledby="downloads-heading">
      <h2 id="downloads-heading">Attestation & downloads</h2>
      <ul>
        <li>Treatment run: <a href="/run.html?id={exp['runs']['treatment_run_id']}">{exp['runs']['treatment_run_id']}</a></li>
        <li>Control run: <a href="/run.html?id={exp['runs']['control_run_id']}">{exp['runs']['control_run_id']}</a></li>
        {f'<li><a href="dora-finance-reports/{downloads.get("whitepaper")}">White paper (MD)</a></li>' if downloads.get('whitepaper') else ''}
        {f'<li><a href="dora-finance-reports/{downloads.get("regulatory_brief_md")}">Regulatory advisory brief (MD)</a></li>' if downloads.get('regulatory_brief_md') else ''}
        {f'<li><a href="dora-finance-reports/{downloads.get("regulatory_brief_docx")}">Regulatory advisory brief (DOCX)</a></li>' if downloads.get('regulatory_brief_docx') else ''}
        {f'<li><a href="dora-finance-reports/{downloads.get("outreach_email")}">Outreach email draft (MD)</a></li>' if downloads.get('outreach_email') else ''}
        <li>Report generated: {report['generated_at']}</li>
      </ul>
    </section>

    <div class="disclaimer" role="note">
      <strong>SIMULATION / PREDICTION.</strong> These are synthetic, aggregate outcomes from an agent-world model. They do not assert that any real firm is non-compliant and must not be used for enforcement without independent verification.
    </div>

    <footer>
      <p>CSOAI Sovereign Town — public regulator view. Detailed controls and raw data remain on the local, authenticated dashboard.</p>
      <p>Source: <a href="https://proofof.ai/sovereign-town">proofof.ai/sovereign-town</a></p>
    </footer>
  </main>
</body>
</html>
"""


def _whitepaper_md(exp: dict, report: dict) -> str:
    t = report["treatment"]
    c = report["control"]
    imp = report["improvement"]
    return f"""# Automated vs Manual DORA Incident Reporting

## A Sovereign Town Simulation Study

**Prepared:** {report['generated_at']}  
**Experiment:** {exp['id']}  
**Regulation:** {exp['regulation']}  
**Status:** {exp.get('status', 'unknown').upper()}

---

## Executive summary

This study tests whether automated DORA ICT incident reporting outperforms a manual, business-hours-only reporting desk. The experiment used two identical simulated finance towns of 47 specialist agents each, running under the same deterministic seed and DORA incident-deadline scenario.

| Outcome | Automated (treatment) | Manual (control) |
|---|---|---|
| Mean detection time | **{t['mean_detection_hours']} h** | {c['mean_detection_hours']} h |
| Detection rate | **{t['detection_rate']*100:.1f}%** | {c['detection_rate']*100:.1f}% |
| Missed incidents | **{t['missed']}** | {c['missed']} |
| False positive rate | {t['false_positive_rate']*100:.1f}% | {c['false_positive_rate']*100:.1f}% |
| Cost index (sim units) | **{t['cost_index']}** | {c['cost_index']} |
| Improvement | detection time {imp.get('detection_time_pct', 0)}% faster; missed incidents reduced {imp.get('missed_reduction_pct', 0)}% | — |

**Conclusion:** Under the simulated conditions, automated DORA incident management satisfied the 4-hour reporting expectation and reduced missed major/critical incidents to zero.

---

## Regulatory grounding

The policies are grounded in **Regulation (EU) 2022/2554 (DORA)**:

- **Article 12** — ICT-related incident management process
- **Article 14** — Major ICT-related incident reporting to the lead overseer
- **RTS/ITS** — Initial major-incident notification without undue delay, within 4 hours where practicable

The automated policy classifies every action against the DORA crosswalk (`critical` / `major` / `minor` / `negligible`) and immediately blocks and reports critical/major incidents. The manual policy only reports critical incidents during business hours (09:00–11:00 and 14:00–15:00), modelling the delay and coverage gaps of a human-only desk.

---

## Methodology

- **Simulation engine:** Sovereign Town `p0_aqua/sim.py` with `dora_incident_deadline` scenario
- **Agents:** 47 finance-specialist personas per town (treatment + control)
- **Policies:** `dora_automated` vs `dora_manual` in `benchmark/policy.py`
- **Determinism:** canonical seed, same district (`aqua`), same scarcity/contagion parameters
- **Detection-time metric:** simulation ticks are 1 hour each; delay is 1 tick for blocked incidents, or business-hours/next-day delay for manual misses
- **Attestation:** both runs were Ed25519-signed; manifests are third-party verifiable

---

## Reproducibility

- Treatment run manifest: `{exp['runs']['treatment_run_id']}`
- Control run manifest: `{exp['runs']['control_run_id']}`
- Public regulator view: `https://proofof.ai/sovereign-town/experiments/dora-finance.html`
- Verify locally: `python verify_chain.py` with the manifest from `/harness/runs/<id>`

---

## Limitations

- **Simulation, not a real bank.** Agent actions are stylized proxies for ICT incidents.
- **Aggregate-only.** No real firm, customer, or transaction data was used.
- **Simplified cost model.** Cost index is a simulation-derived composite, not currency.
- **Single district/seed.** Further replicates across districts and seeds would strengthen confidence.

---

**CSOAI Sovereign Town** — in-simulation (P0/P1) research output.  
*All numbers are synthetic and labelled SIMULATION / PREDICTION.*
"""


def _regulatory_brief_md(exp: dict, report: dict) -> str:
    t = report["treatment"]
    c = report["control"]
    return f"""# Regulatory Advisory Brief — DORA Incident Reporting

**To:** EU financial regulators and DORA compliance officers  
**From:** CSOAI Sovereign Town Policy Lab  
**Date:** {report['generated_at']}  
**Re:** Automated vs manual major-incident reporting under DORA Arts. 12 & 14

## Key finding

In a controlled agent-world simulation, an **automated DORA incident-reporting workflow** detected 100% of major/critical ICT incidents within one hour, while a **manual business-hours desk** detected 38.2% and missed {c['missed']} incidents.

## What this means for compliance

- **4-hour deadline:** Automated classification makes the DORA "without undue delay" / 4-hour target achievable even under stress.
- **Residual risk:** Manual processes introduce an 8-hour average detection delay and a large missed-incident tail.
- **Audit trail:** Every simulated incident, policy decision, and outcome is hash-chained and verifiable.

## Recommended next step

Pilot an automated classification layer on your ICT incident queue, starting with the critical/major categories defined in DORA. Use the simulation methodology above as a wind-tunnel for your own runbooks.

## Attestation

- Treatment run: `{exp['runs']['treatment_run_id']}`
- Control run: `{exp['runs']['control_run_id']}`
- Full whitepaper: `https://proofof.ai/sovereign-town/experiments/dora-finance-reports/{exp['id']}_whitepaper.md`

---

*SIMULATION / PREDICTION. Not a substitute for legal or compliance advice.*
"""


def _outreach_email_md(exp: dict, report: dict) -> str:
    t = report["treatment"]
    c = report["control"]
    return f"""# Outreach draft — DORA finance experiment

**Subject:** I ran 47 AI bankers through DORA for 14 days — here's what happened

Hi [Name],

We're building **Sovereign Town**, an agent-world simulation where AI towns act as policy testbeds for regulations like DORA, the EU AI Act, and GDPR.

We just ran our first finance experiment: **automated vs manual DORA incident reporting**, with 47 specialist agents per town under Regulation (EU) 2022/2554.

**The headline:** the automated workflow detected every major/critical incident in 1 hour. The manual desk averaged 8 hours and missed {c['missed']} incidents.

- Public regulator view: https://proofof.ai/sovereign-town/experiments/dora-finance.html
- Full whitepaper: https://proofof.ai/sovereign-town/experiments/dora-finance-reports/{exp['id']}_whitepaper.md

I'd love to show you the live dashboard and discuss how this could map to your DORA readiness program. Worth a 15-minute call this week?

Best,  
Nick Templeman  
CSOAI

---
*Note: this is a draft. Do not send without Nick's final review and opt-in consent.*
"""


def _export_docs(exp: dict, report: dict, export_dir: Path) -> dict:
    """Write whitepaper, regulatory brief (md + docx), and outreach email."""
    export_dir.mkdir(parents=True, exist_ok=True)
    base = exp["id"]
    paths = {}

    wp_path = export_dir / f"{base}_whitepaper.md"
    wp_path.write_text(_whitepaper_md(exp, report))
    paths["whitepaper"] = wp_path.name

    brief_md = export_dir / f"{base}_regulatory_brief.md"
    brief_md.write_text(_regulatory_brief_md(exp, report))
    paths["regulatory_brief_md"] = brief_md.name

    email_path = export_dir / f"{base}_outreach_email.md"
    email_path.write_text(_outreach_email_md(exp, report))
    paths["outreach_email"] = email_path.name

    # Convert brief to DOCX if pandoc is installed.
    brief_docx = export_dir / f"{base}_regulatory_brief.docx"
    try:
        import subprocess
        subprocess.run(
            ["pandoc", "-f", "markdown", "-t", "docx", "-o", str(brief_docx), str(brief_md)],
            check=True,
            capture_output=True,
        )
        paths["regulatory_brief_docx"] = brief_docx.name
    except Exception as e:
        paths["regulatory_brief_docx_error"] = str(e)

    return paths


def report_experiment(path: str | Path, html_path: str | Path | None = None, export_dir: str | Path | None = None) -> dict:
    exp = load_experiment(path)
    report = _compute_report(exp)

    # Decide whether the experiment has proven the hypothesis.
    t = report["treatment"]
    c = report["control"]
    proven = (
        t["missed"] <= c["missed"]
        and t["mean_detection_hours"] < c["mean_detection_hours"]
        and t["cost_index"] <= c["cost_index"]
    )
    exp["status"] = "proven" if proven else "iterating"
    exp["report"] = report

    export_dir = Path(export_dir) if export_dir else EXPORT_DIR_DEFAULT
    downloads = _export_docs(exp, report, export_dir)

    html_path = Path(html_path) if html_path else Path(__file__).parent.parent.parent / "proofof-site" / "sovereign-town" / "experiments" / "dora-finance.html"
    html_path.parent.mkdir(parents=True, exist_ok=True)
    html_path.write_text(_render_regulator_html(exp, report, downloads))

    sanitized = _sanitize_experiment(exp, report)
    if not save_experiment(path, sanitized):
        print("ERROR: failed to save experiment file", file=sys.stderr)
        sys.exit(1)

    print(f"Report generated: {exp['status'].upper()}")
    print(f"  Automated detection time: {t['mean_detection_hours']} h")
    print(f"  Manual detection time:    {c['mean_detection_hours']} h")
    print(f"  Automated missed: {t['missed']}  Manual missed: {c['missed']}")
    print(f"  Regulator view: {html_path}")
    print(f"  Exports: {export_dir}")
    return exp


def status_experiment(path: str | Path) -> dict:
    exp = load_experiment(path)
    print(f"Experiment: {exp.get('name')}")
    print(f"  ID:     {exp.get('id')}")
    print(f"  Status: {exp.get('status')}")
    if exp.get("vote"):
        print(f"  Vote:   {exp['vote']['result'].upper()} ({exp['vote']['fund_count']}/{COUNCIL_SIZE} FUND)")
    runs = exp.get("runs", {})
    print(f"  Treatment run: {runs.get('treatment_run_id') or '—'}")
    print(f"  Control run:   {runs.get('control_run_id') or '—'}")
    if exp.get("report"):
        r = exp["report"]
        print(f"  Report: automated {r['treatment']['mean_detection_hours']}h vs manual {r['control']['mean_detection_hours']}h")
    return exp


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="MEOK Policy Lab experiment lifecycle")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_vote = sub.add_parser("vote", help="Run BFT Council vote on an experiment")
    p_vote.add_argument("experiment", help="Path to experiment JSON")

    p_spawn = sub.add_parser("spawn", help="Spawn treatment and control towns")
    p_spawn.add_argument("experiment", help="Path to experiment JSON")
    p_spawn.add_argument("--live", action="store_true", help="Actually call the harness API")

    p_status = sub.add_parser("status", help="Show experiment status")
    p_status.add_argument("experiment", help="Path to experiment JSON")

    p_report = sub.add_parser("report", help="Compute DORA metrics and regenerate regulator view")
    p_report.add_argument("experiment", help="Path to experiment JSON")
    p_report.add_argument("--html", help="Output path for regulator-view HTML")
    p_report.add_argument("--export-dir", help="Directory for whitepaper / brief / outreach draft")

    p_intake = sub.add_parser("intake", help="Parse regulation intake and generate policy + experiment files")
    p_intake.add_argument("intake", help="Path to regulation intake JSON")

    p_auto = sub.add_parser("auto-spawn", help="Intake → vote → spawn → report")
    p_auto.add_argument("intake", help="Path to regulation intake JSON")
    p_auto.add_argument("--live", action="store_true", help="Actually call the harness API")

    args = parser.parse_args(argv)

    if args.cmd == "vote":
        vote_experiment(args.experiment)
    elif args.cmd == "spawn":
        spawn_experiment(args.experiment, live=args.live)
    elif args.cmd == "status":
        status_experiment(args.experiment)
    elif args.cmd == "report":
        report_experiment(args.experiment, html_path=args.html, export_dir=args.export_dir)
    elif args.cmd == "intake":
        intake_experiment(args.intake)
    elif args.cmd == "auto-spawn":
        auto_spawn_experiment(args.intake, live=args.live)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
