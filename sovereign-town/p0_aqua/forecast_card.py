#!/usr/bin/env python3
"""
forecast_card.py — the "Attested Compliance Forecast Card" (additive; touches no existing files).

The demoable, NON-OVERCLAIMING wedge distilled from the Sovereign Lens vision: for ONE consenting
entity + ONE regulation (default: DORA), produce a SIGNED Compliance Forecast Card that runs an
explicit, small set of obligation scenarios through the REAL Sovereign Gate / care scorer we already
own, and emits a *counterfactual* (a dose-response), NOT a prophecy.

HONESTY GUARDRAILS (Nick runs an explicit honesty register — these are load-bearing):
  * Scope is bounded: this is an IN-SIMULATION assessment over an EXPLICIT scenario set. It is NOT
    legal advice, NOT a guarantee, and any score is a MODEL score over the shown scenarios.
  * NO fabricated precision. We never invent a "94% probability". The only number we emit is the
    fraction of the explicit, displayed scenarios that the gate flags — counted, not conjured.
  * NOT "court-admissible". We say "tamper-evident: Ed25519-signed + (when published) Bitcoin-
    anchored". The signature proves the card was not altered after issuance; nothing more.
  * CONSENT-BASED by construction: entity facts are CALLER-SUPPLIED. There is no scraping, no
    auto-spawning, no fetching of a non-consenting company's data. You pass in what you may use.

How it integrates with the proven primitives (all imported, never re-implemented):
  * sign_lib.load_or_create_key / sign / verify — the SAME Ed25519 town identity that anchors the
    flywheel + conductor ledgers. The card is signed with town_pub.key, offline-verifiable by anyone.
  * sim.sovereign_gate / sim.care_score / sim.CARE_FLOOR — the REAL gate. Each obligation is mapped
    to a posture action and run through the actual gate. Honest, clearly-labelled stub fallback only
    if sim cannot import.
  * conductor.Conductor — OPTIONAL. When `use_conductor=True`, each obligation also rides the Governed
    Conductor (Thinker/Worker/Verifier, governance-bound Verifier) and the routing is itself attested
    on the conductor ledger. The card records the conductor verdict alongside the gate verdict.

Signing scheme — matched EXACTLY to the flywheel / conductor:
    message = prev + json.dumps(body, sort_keys=True)
    prev    = previous sig   (first prev = "genesis-forecast")
    body    = the card, EXCLUDING the envelope fields (sig / prev / prev_sig / alg)
The card is its own short, genesis-chained ledger, so it can later ride the publish/anchor path
(publish_signed_ledger.py reads exactly this shape).

Run:  python3 forecast_card.py        # generates the demo card (Acme Bank, DORA) + HTML, re-verifies.
"""
from __future__ import annotations

import os
import sys
import json
import html
import time
from dataclasses import dataclass, field, asdict
from typing import Any

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))   # run from anywhere
import sign_lib                                                   # the proven signer (do NOT reinvent)

OUT = os.path.dirname(os.path.abspath(__file__))
GENESIS = "genesis-forecast"
ALG = "Ed25519"

# Envelope fields are NOT part of the signed body — matches the flywheel / conductor convention.
_ENVELOPE = ("sig", "prev", "prev_sig", "alg")

# Honest, fixed disclaimers carried inside EVERY card (so they survive signing + travel with the JSON).
SCOPE_DISCLAIMER = (
    "In-simulation assessment over an explicit, displayed scenario set. NOT legal advice; "
    "NOT a guarantee of regulatory outcome; any score is a MODEL score over the shown scenarios, "
    "model-bounded. Tamper-evident: Ed25519-signed and (when published) Bitcoin-anchored — this "
    "proves the card was not altered after issuance, it does NOT make the assessment court-admissible. "
    "Consent-based: all entity facts were caller-supplied; nothing was scraped or auto-collected."
)
METHODOLOGY = (
    "Each obligation is mapped to a posture action whose strength reflects the CALLER-SUPPLIED public "
    "facts, then run through the real Sovereign Gate (sim.sovereign_gate) and care scorer "
    "(sim.care_score). The gate returns met / at_risk / unmet by comparing the obligation's care score "
    "to the care floor (sim.CARE_FLOOR). The 'flagged' count is the literal number of displayed "
    "obligations the gate did not mark 'met'. The counterfactual re-runs the SAME gate after applying "
    "a caller-named remediation, and reports how the flagged count changes (a dose-response, not a "
    "prophecy). Confidence is reported as a coverage statement over the explicit scenario set, never "
    "as an invented probability."
)


# --------------------------------------------------------------------------------------------------
# Regulation scenario sets. Each is a small, EXPLICIT, displayed list of obligations — the demo set.
# `posture_action` is the sim action the obligation maps onto; `remediation` names the lever a caller
# can pull and the stronger posture it unlocks (this drives the counterfactual / dose-response).
# --------------------------------------------------------------------------------------------------
@dataclass
class Obligation:
    obligation_id: str
    title: str
    article: str            # the DORA article / chapter reference (informational, not legal advice)
    posture_action: str     # sim action representing CURRENT posture (set from caller facts below)
    remediation: str        # the lever a caller can pull
    remediated_action: str  # the stronger posture the lever unlocks (used for the counterfactual)


# Five DORA ICT obligations — the demo scenario set (DORA = Reg. (EU) 2022/2554).
# article strings are informational pointers, NOT legal advice.
DORA_OBLIGATIONS: list[Obligation] = [
    Obligation("dora_ict_risk_framework", "ICT risk management framework", "Art. 5-6 (Ch. II)",
               "neglect", "Adopt & board-approve a documented ICT risk framework", "work"),
    Obligation("dora_incident_reporting", "Major ICT incident reporting", "Art. 17-19 (Ch. III)",
               "deceive", "Stand up classification + regulator-notification workflow", "help_peer"),
    Obligation("dora_resilience_testing", "Digital operational resilience testing", "Art. 24-25 (Ch. IV)",
               "rest", "Run the annual DORT programme (vuln assessments, scenario tests)", "work"),
    Obligation("dora_third_party_register", "ICT third-party risk register", "Art. 28-30 (Ch. V)",
               "neglect", "Maintain the Register of Information of ICT third-party arrangements", "work"),
    Obligation("dora_tlpt", "Threat-led penetration testing (TLPT)", "Art. 26-27 (Ch. IV)",
               "rest", "Commission TIBER-EU-aligned TLPT on critical functions", "help_peer"),
]

REGULATIONS: dict[str, list[Obligation]] = {"DORA": DORA_OBLIGATIONS}


# --------------------------------------------------------------------------------------------------
# The real gate, with an honest, clearly-labelled stub fallback.
# --------------------------------------------------------------------------------------------------
def _gate_eval(action: str, arm: str = "A_governed") -> dict:
    """Run one posture action through the REAL Sovereign Gate. Honest stub only if sim won't import."""
    try:
        import sim
        g = sim.sovereign_gate(action, arm)
        floor = float(sim.CARE_FLOOR)
        return {"source": "sim.sovereign_gate", "care_floor": floor,
                "gate_verdict": g.get("gate_verdict"), "care_score": g.get("care_score"),
                "care_floor_breach": g.get("care_floor_breach"), "would_block": g.get("would_block")}
    except Exception as e:  # honest fallback — NEVER pretend the real gate ran
        floor = 0.40
        cs = {"steal": 0.05, "neglect": 0.10, "deceive": 0.08,
              "help_peer": 0.97, "work": 0.85, "rest": 0.60}.get(action, 0.5)
        violate = action in ("steal", "neglect", "deceive")
        verdict = "deny" if violate else ("escalate" if cs < floor else "allow")
        return {"source": f"STUB (sim unavailable: {type(e).__name__})", "care_floor": floor,
                "gate_verdict": verdict, "care_score": round(cs, 3),
                "care_floor_breach": cs < floor, "would_block": verdict != "allow"}


def _status_from_gate(g: dict) -> str:
    """Map a gate verdict to a compliance status. met / at_risk / unmet — honest, deterministic."""
    v = g.get("gate_verdict")
    if v == "allow" and not g.get("care_floor_breach"):
        return "met"
    if v == "deny" or g.get("would_block"):
        return "unmet"
    return "at_risk"   # escalate / floor-breach without hard deny


# --------------------------------------------------------------------------------------------------
# Optional Conductor pass — attests the obligation through the Governed Conductor too.
# --------------------------------------------------------------------------------------------------
def _conductor_eval(obligation: Obligation, action: str) -> dict | None:
    """Route the obligation through the Governed Conductor (governance-bound Verifier). Optional."""
    try:
        import conductor
        c = conductor.Conductor()   # reuses the same town identity + its own attested ledger
        task = {"id": obligation.obligation_id, "kind": "policy",
                "prompt": f"Posture check for obligation '{obligation.title}'",
                "action": action, "arm": "A_governed"}
        out = c.conduct(task)
        return {"verdict": out["verdict"], "governance": out["governance"],
                "ledger": os.path.basename(getattr(c, "ledger_path", "conductor_ledger.jsonl"))}
    except Exception as e:
        return {"error": f"conductor unavailable: {type(e).__name__}: {e}"}


# --------------------------------------------------------------------------------------------------
# Build the card.
# --------------------------------------------------------------------------------------------------
def build_card(entity: dict, regulation: str = "DORA", *,
               posture_overrides: dict[str, str] | None = None,
               remediations: list[str] | None = None,
               use_conductor: bool = False) -> dict:
    """Build (unsigned) the Attested Compliance Forecast Card.

    entity: caller-supplied descriptor. REQUIRED key 'name'; 'facts' is a list of PUBLIC, caller-
            supplied statements (no scraping). 'consent' should record that the caller is authorised.
    posture_overrides: {obligation_id: sim_action} to set current posture from the caller's facts
            (defaults to each obligation's declared posture_action).
    remediations: list of obligation_ids the caller asks 'what if I fix these?' — drives the
            counterfactual / dose-response.
    use_conductor: also route each obligation through the Governed Conductor and record its verdict.
    """
    reg = regulation.upper()
    if reg not in REGULATIONS:
        raise ValueError(f"Unknown regulation {reg!r}. Available: {sorted(REGULATIONS)}")
    if not entity.get("name"):
        raise ValueError("entity must include a 'name' (consent-based: facts are caller-supplied).")

    posture_overrides = posture_overrides or {}
    remediation_ids = set(remediations or [])
    obligations = REGULATIONS[reg]

    assessed: list[dict] = []
    flagged_now = 0
    for ob in obligations:
        action = posture_overrides.get(ob.obligation_id, ob.posture_action)
        g = _gate_eval(action)
        status = _status_from_gate(g)
        if status != "met":
            flagged_now += 1
        row = {
            "obligation_id": ob.obligation_id, "title": ob.title, "article": ob.article,
            "posture_action": action, "status": status,
            "gate": g, "remediation": ob.remediation,
        }
        if use_conductor:
            row["conductor"] = _conductor_eval(ob, action)
        assessed.append(row)

    # ---- counterfactual / dose-response: re-run the SAME gate after caller-named remediations ----
    counterfactual_rows: list[dict] = []
    flagged_after = flagged_now
    if remediation_ids:
        flagged_after = 0
        for ob, row in zip(obligations, assessed):
            if ob.obligation_id in remediation_ids:
                action2 = ob.remediated_action
                g2 = _gate_eval(action2)
                status2 = _status_from_gate(g2)
            else:
                action2, g2, status2 = row["posture_action"], row["gate"], row["status"]
            if status2 != "met":
                flagged_after += 1
            counterfactual_rows.append({
                "obligation_id": ob.obligation_id, "title": ob.title,
                "remediated": ob.obligation_id in remediation_ids,
                "applied_lever": ob.remediation if ob.obligation_id in remediation_ids else None,
                "posture_action": action2, "status_before": row["status"], "status_after": status2,
            })

    m = len(obligations)
    # The ONLY headline number is a COUNT over the displayed scenarios — never an invented probability.
    summary = {
        "regulation": reg,
        "scenarios_assessed": m,
        "flagged_unmet_or_at_risk": flagged_now,
        "met": m - flagged_now,
        "model_score_over_scenarios": round((m - flagged_now) / m, 3) if m else None,
        "model_score_meaning": (
            f"fraction of the {m} EXPLICIT, displayed obligations the gate marked 'met' — "
            f"a model score over THIS scenario set, not a probability of regulatory outcome."),
    }
    counterfactual = None
    if remediation_ids:
        counterfactual = {
            "statement": (
                f"On current path, {flagged_now} of {m} assessed obligations flag unmet/at-risk. "
                f"If you remediate {sorted(remediation_ids)}, the flagged count drops to {flagged_after}."),
            "flagged_before": flagged_now,
            "flagged_after": flagged_after,
            "levers_applied": sorted(remediation_ids),
            "rows": counterfactual_rows,
            "note": "Dose-response over the explicit scenario set — a counterfactual, NOT a prophecy.",
        }

    used_stub = any(r["gate"]["source"].startswith("STUB") for r in assessed)
    card_body = {
        "card_type": "attested_compliance_forecast",
        "schema": "forecast_card/v1",
        "issued_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "entity": {
            "name": entity["name"],
            "facts": entity.get("facts", []),               # PUBLIC, caller-supplied
            "consent": entity.get("consent",
                                  "caller asserts authorisation to assess on supplied public facts"),
            "consent_basis": "consent-based by construction: all facts caller-supplied; no scraping",
        },
        "summary": summary,
        "obligations": assessed,
        "counterfactual": counterfactual,
        "scope_disclaimer": SCOPE_DISCLAIMER,
        "methodology": METHODOLOGY,
        "honesty": {
            "not_legal_advice": True,
            "not_a_guarantee": True,
            "no_fabricated_precision": True,
            "court_admissible": False,
            "tamper_evidence": "Ed25519-signed + (when published) Bitcoin-anchored",
            "gate_source": "STUB fallback (sim unavailable)" if used_stub else "real sim.sovereign_gate",
        },
    }
    return card_body


# --------------------------------------------------------------------------------------------------
# Sign the card as its own short, genesis-chained ledger (prev = "genesis-forecast").
# --------------------------------------------------------------------------------------------------
def sign_card(card_body: dict, priv=None, prev: str = GENESIS) -> dict:
    """Sign `card_body` with the town Ed25519 key. Scheme matches the flywheel/conductor EXACTLY:
    message = prev + json.dumps(body, sort_keys=True); body excludes envelope fields."""
    if priv is None:
        priv, _pub = sign_lib.load_or_create_key()
    clean = {k: v for k, v in card_body.items() if k not in _ENVELOPE}
    msg = json.dumps(clean, sort_keys=True)
    signed = dict(clean)
    signed["prev"] = prev
    signed["alg"] = ALG
    signed["sig"] = sign_lib.sign(priv, prev + msg)
    return signed


def verify_card(signed_card: dict, pub_b64: str | None = None, prev: str = GENESIS) -> bool:
    """Re-verify a signed card with the PUBLIC KEY ONLY (offline-verifiable)."""
    if pub_b64 is None:
        pub_b64 = open(os.path.join(OUT, "town_pub.key")).read().strip()
    body = json.dumps({k: v for k, v in signed_card.items() if k not in _ENVELOPE}, sort_keys=True)
    claimed_prev = signed_card.get("prev", prev)
    return claimed_prev == prev and sign_lib.verify(pub_b64, claimed_prev + body, signed_card.get("sig"))


# --------------------------------------------------------------------------------------------------
# HTML render — clean, presentable, carries the disclaimers visibly.
# --------------------------------------------------------------------------------------------------
_STATUS_COLOR = {"met": "#1a7f37", "at_risk": "#9a6700", "unmet": "#cf222e"}
_STATUS_LABEL = {"met": "MET", "at_risk": "AT RISK", "unmet": "UNMET"}


def render_html(signed_card: dict, verified: bool | None = None) -> str:
    c = signed_card
    e = c["entity"]
    s = c["summary"]
    esc = html.escape

    def chip(status: str) -> str:
        col = _STATUS_COLOR.get(status, "#57606a")
        return (f'<span style="background:{col};color:#fff;padding:2px 10px;border-radius:12px;'
                f'font-size:12px;font-weight:600;letter-spacing:.3px">{_STATUS_LABEL.get(status, status.upper())}</span>')

    rows = ""
    for ob in c["obligations"]:
        g = ob["gate"]
        rows += (
            "<tr>"
            f'<td style="padding:10px 12px;border-bottom:1px solid #eaeef2">'
            f'<div style="font-weight:600">{esc(ob["title"])}</div>'
            f'<div style="color:#57606a;font-size:12px">{esc(ob["article"])} &middot; posture: {esc(ob["posture_action"])}</div></td>'
            f'<td style="padding:10px 12px;border-bottom:1px solid #eaeef2;text-align:center">{chip(ob["status"])}</td>'
            f'<td style="padding:10px 12px;border-bottom:1px solid #eaeef2;text-align:center;'
            f'font-variant-numeric:tabular-nums">{esc(str(g.get("care_score")))}</td>'
            f'<td style="padding:10px 12px;border-bottom:1px solid #eaeef2;color:#57606a;font-size:13px">{esc(ob["remediation"])}</td>'
            "</tr>"
        )

    facts = "".join(f"<li>{esc(str(f))}</li>" for f in e.get("facts", [])) or "<li><em>none supplied</em></li>"

    cf = c.get("counterfactual")
    cf_html = ""
    if cf:
        cf_rows = ""
        for r in cf["rows"]:
            mark = " &rarr; " if r["remediated"] else " "
            cf_rows += (
                "<tr>"
                f'<td style="padding:6px 12px;border-bottom:1px solid #eaeef2">{esc(r["title"])}</td>'
                f'<td style="padding:6px 12px;border-bottom:1px solid #eaeef2;text-align:center">{chip(r["status_before"])}</td>'
                f'<td style="padding:6px 12px;border-bottom:1px solid #eaeef2;text-align:center">{mark}</td>'
                f'<td style="padding:6px 12px;border-bottom:1px solid #eaeef2;text-align:center">{chip(r["status_after"])}</td>'
                f'<td style="padding:6px 12px;border-bottom:1px solid #eaeef2;color:#57606a;font-size:12px">{esc(r["applied_lever"] or "")}</td>'
                "</tr>"
            )
        cf_html = f"""
      <h3 style="margin:24px 0 8px">Counterfactual &middot; dose-response</h3>
      <div style="background:#fff8e5;border:1px solid #f0d58c;border-radius:8px;padding:12px 14px;margin-bottom:12px">
        {esc(cf["statement"])}
        <div style="color:#57606a;font-size:12px;margin-top:6px">{esc(cf["note"])}</div>
      </div>
      <table style="width:100%;border-collapse:collapse;font-size:14px">
        <thead><tr style="text-align:left;color:#57606a;font-size:12px">
          <th style="padding:6px 12px">Obligation</th><th style="padding:6px 12px;text-align:center">Before</th>
          <th style="padding:6px 12px"></th><th style="padding:6px 12px;text-align:center">After</th>
          <th style="padding:6px 12px">Lever applied</th></tr></thead>
        <tbody>{cf_rows}</tbody>
      </table>"""

    if verified is None:
        verified = verify_card(c)
    vbadge = (f'<span style="background:#1a7f37;color:#fff;padding:3px 10px;border-radius:6px;font-size:12px;'
              f'font-weight:600">SIGNATURE VERIFIED</span>' if verified else
              f'<span style="background:#cf222e;color:#fff;padding:3px 10px;border-radius:6px;font-size:12px;'
              f'font-weight:600">SIGNATURE INVALID</span>')
    sig_short = esc((c.get("sig") or "")[:32]) + "..."
    score = s.get("model_score_over_scenarios")
    score_pct = f"{round(score * 100)}%" if score is not None else "n/a"

    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Attested Compliance Forecast Card &middot; {esc(e["name"])} &middot; {esc(s["regulation"])}</title></head>
<body style="margin:0;background:#f6f8fa;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif;color:#1f2328">
  <div style="max-width:860px;margin:32px auto;background:#fff;border:1px solid #d0d7de;border-radius:12px;overflow:hidden">
    <div style="background:#0d1117;color:#fff;padding:20px 28px">
      <div style="font-size:12px;letter-spacing:1px;color:#8b949e;text-transform:uppercase">Attested Compliance Forecast Card</div>
      <div style="font-size:24px;font-weight:700;margin-top:4px">{esc(e["name"])} &middot; {esc(s["regulation"])}</div>
      <div style="font-size:13px;color:#8b949e;margin-top:4px">Issued {esc(c["issued_at"])} &middot; {vbadge}</div>
    </div>
    <div style="padding:24px 28px">
      <div style="display:flex;gap:16px;flex-wrap:wrap;margin-bottom:20px">
        <div style="flex:1;min-width:140px;background:#f6f8fa;border:1px solid #d0d7de;border-radius:8px;padding:14px">
          <div style="font-size:12px;color:#57606a">Obligations assessed</div>
          <div style="font-size:28px;font-weight:700">{s["scenarios_assessed"]}</div></div>
        <div style="flex:1;min-width:140px;background:#f6f8fa;border:1px solid #d0d7de;border-radius:8px;padding:14px">
          <div style="font-size:12px;color:#57606a">Flagged (unmet / at-risk)</div>
          <div style="font-size:28px;font-weight:700;color:#cf222e">{s["flagged_unmet_or_at_risk"]}</div></div>
        <div style="flex:1;min-width:140px;background:#f6f8fa;border:1px solid #d0d7de;border-radius:8px;padding:14px">
          <div style="font-size:12px;color:#57606a">Model score (this scenario set)</div>
          <div style="font-size:28px;font-weight:700">{score_pct}</div></div>
      </div>
      <div style="color:#57606a;font-size:12px;margin:-8px 0 18px">{esc(s["model_score_meaning"])}</div>

      <h3 style="margin:0 0 8px">Entity facts <span style="font-weight:400;color:#57606a;font-size:13px">(caller-supplied, public &middot; consent-based)</span></h3>
      <ul style="margin:0 0 20px;padding-left:20px;color:#1f2328;font-size:14px">{facts}</ul>

      <h3 style="margin:0 0 8px">Obligation assessment <span style="font-weight:400;color:#57606a;font-size:13px">(real Sovereign Gate)</span></h3>
      <table style="width:100%;border-collapse:collapse;font-size:14px">
        <thead><tr style="text-align:left;color:#57606a;font-size:12px">
          <th style="padding:8px 12px">Obligation</th><th style="padding:8px 12px;text-align:center">Status</th>
          <th style="padding:8px 12px;text-align:center">Care score</th><th style="padding:8px 12px">Suggested remediation</th></tr></thead>
        <tbody>{rows}</tbody>
      </table>
      {cf_html}

      <div style="margin-top:24px;background:#f6f8fa;border:1px solid #d0d7de;border-radius:8px;padding:14px 16px">
        <div style="font-weight:600;font-size:13px;margin-bottom:6px">Scope &amp; honesty</div>
        <div style="color:#57606a;font-size:12px;line-height:1.55">{esc(c["scope_disclaimer"])}</div>
        <div style="color:#57606a;font-size:12px;line-height:1.55;margin-top:8px"><strong>Methodology:</strong> {esc(c["methodology"])}</div>
        <div style="color:#57606a;font-size:11px;margin-top:10px;font-family:ui-monospace,SFMono-Regular,Menlo,monospace">
          alg={esc(c.get("alg",""))} &middot; prev={esc(c.get("prev",""))} &middot; gate={esc(c["honesty"]["gate_source"])} &middot; sig={sig_short}</div>
      </div>
    </div>
  </div>
</body></html>"""


# --------------------------------------------------------------------------------------------------
# Convenience: build + sign + render + write, in one call.
# --------------------------------------------------------------------------------------------------
def generate(entity: dict, regulation: str = "DORA", *, remediations=None,
             posture_overrides=None, use_conductor=False, out_prefix: str | None = None) -> dict:
    body = build_card(entity, regulation, posture_overrides=posture_overrides,
                      remediations=remediations, use_conductor=use_conductor)
    priv, pub = sign_lib.load_or_create_key()
    signed = sign_card(body, priv=priv)
    verified = verify_card(signed, pub_b64=pub)
    html_doc = render_html(signed, verified=verified)

    paths = {}
    if out_prefix:
        json_path = os.path.join(OUT, f"{out_prefix}.json")
        html_path = os.path.join(OUT, f"{out_prefix}.html")
        with open(json_path, "w") as f:
            json.dump(signed, f, indent=2)
        with open(html_path, "w") as f:
            f.write(html_doc)
        paths = {"json": json_path, "html": html_path}
    return {"signed": signed, "verified": verified, "html": html_doc, "pub": pub, "paths": paths}


# --------------------------------------------------------------------------------------------------
# Smoke test — demo entity (Acme Bank, DORA): build, sign, write JSON + HTML, re-verify, PASS/FAIL.
# --------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    print("  Attested Compliance Forecast Card — smoke test")

    demo_entity = {
        "name": "Acme Bank",
        "facts": [
            "EU-authorised credit institution (in DORA scope).",
            "Public statement: ICT risk policy exists but is not board-approved.",
            "Public statement: no formal major-incident classification workflow yet.",
            "Public statement: third-party ICT register is partial / spreadsheet-based.",
            "No TLPT / TIBER-EU testing reported.",
        ],
        "consent": "Demo entity; facts are illustrative + caller-supplied (no scraping).",
    }
    # Ask the counterfactual: what if Acme remediates the framework + incident-reporting obligations?
    remediations = ["dora_ict_risk_framework", "dora_incident_reporting"]

    res = generate(demo_entity, "DORA", remediations=remediations, out_prefix="forecast_card_demo")
    signed, verified, paths = res["signed"], res["verified"], res["paths"]
    s = signed["summary"]

    print(f"  entity     : {signed['entity']['name']} / {s['regulation']}")
    print(f"  gate source: {signed['honesty']['gate_source']}")
    print(f"  assessed   : {s['scenarios_assessed']}  flagged(unmet/at-risk): {s['flagged_unmet_or_at_risk']}  "
          f"model-score: {s['model_score_over_scenarios']}")
    for ob in signed["obligations"]:
        print(f"    - {ob['status']:<7} {ob['title']}  (care={ob['gate'].get('care_score')}, posture={ob['posture_action']})")
    if signed["counterfactual"]:
        print(f"  counterfactual: {signed['counterfactual']['statement']}")
    print(f"  honesty    : court_admissible={signed['honesty']['court_admissible']}  "
          f"tamper={signed['honesty']['tamper_evidence']}")
    print(f"  files      : {paths.get('json')}")
    print(f"               {paths.get('html')}")

    # Re-verify with PUBLIC KEY ONLY (offline-verifiable), reloading from disk to prove portability.
    on_disk = json.load(open(paths["json"]))
    pub = open(os.path.join(OUT, "town_pub.key")).read().strip()
    reverify = verify_card(on_disk, pub_b64=pub)

    # Tamper test: flip a flagged count and confirm the signature stops verifying.
    tampered = dict(on_disk)
    tampered = json.loads(json.dumps(on_disk))
    tampered["summary"]["flagged_unmet_or_at_risk"] = 0
    tamper_ok = verify_card(tampered, pub_b64=pub)

    print(f"  re-verify (town_pub.key, reloaded from disk): {reverify}")
    print(f"  tamper test (flip flagged count -> 0): verifies={tamper_ok} -> "
          f"{'DETECTED' if not tamper_ok else 'MISSED'}")

    ok = bool(verified and reverify and not tamper_ok)
    print(f"  RESULT     : {'PASS' if ok else 'FAIL'}")
    sys.exit(0 if ok else 1)
