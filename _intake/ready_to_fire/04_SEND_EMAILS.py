#!/usr/bin/env python3
"""Sends 5 design-partner emails via Resend API.

Prereq: RESEND_API_KEY env var set + mail.meok.ai domain verified.
"""
import os
import json
import urllib.request
import urllib.error

# Design-partner email drafts (from DESIGN_PARTNER_EMAILS.md)
EMAILS = [
    {
        "segment": "REGULATOR",
        "to": "ai-act-team@digital-strategy.ec.europa.eu",
        "subject": "A wind-tunnel for your AI rule — test the effect before you finalise it",
        "body": """Hi,

We've built something directly useful to a regulator: a simulation that pre-computes how a governance rule plays out across archetypal firms *before* it's finalised — a wind-tunnel for regulation.

It's run, not theory. Same agents, governance on vs off: the governed arm holds at 0 violations and full operational resilience under shock; the ungoverned arm collapses. Robust across 15 parameter settings, every run cryptographically signed and verifiable by anyone offline (here, with no account: https://proofof.ai/passport).

Public archetypes only — no firm data, no named-entity profiling, everything labelled as simulation. 30-minute look?

Nick Templeman — CSOAI.org / meok.ai
""",
    },
    {
        "segment": "ENTERPRISE — CERA",
        "to": "compliance-tech@cera.org",
        "subject": "Your EU AI Act compliance outcome, simulated before you spend",
        "body": """Hi,

Most compliance work is a guess until the deadline. We built a Looking Glass that, from public archetypes, pre-computes the likely outcome for a care-sector firm like Cera under EU AI Act — exposure, scenario runs, and the single ranked move that maximises resilience — delivered as a signed report.

No data from you to start (we run on archetypes; you opt in to refine with your own). Verify the signing tech yourself right now: https://proofof.ai/passport.

Open to being a design partner on a one-framework pilot?

Nick Templeman — CSOAI.org / meok.ai
""",
    },
    {
        "segment": "ENTERPRISE — SAP",
        "to": "ai-governance@sap.com",
        "subject": "Your EU AI Act + DORA compliance outcome, simulated before you spend",
        "body": """Hi,

We built a Looking Glass that, from public archetypes, pre-computes the likely outcome for an enterprise software firm like SAP under EU AI Act + DORA — exposure, scenario runs, ranked moves — signed report.

No data from you to start. Verify offline: https://proofof.ai/passport.

Open to a one-framework pilot?

Nick Templeman — CSOAI.org / meok.ai
""",
    },
    {
        "segment": "ENTERPRISE — SIEMENS",
        "to": "ai-governance@siemens.com",
        "subject": "Your EU AI Act + NIS2 compliance outcome, simulated before you spend",
        "body": """Hi,

We built a Looking Glass that, from public archetypes, pre-computes the likely outcome for an industrial-firm like Siemens under EU AI Act + NIS2 — exposure, scenario runs, ranked moves — signed report.

No data from you to start. Verify offline: https://proofof.ai/passport.

Open to a one-framework pilot?

Nick Templeman — CSOAI.org / meok.ai
""",
    },
    {
        "segment": "ENTERPRISE — IBM",
        "to": "ai-governance@ibm.com",
        "subject": "Your EU AI Act + watsonx compliance outcome, simulated before you spend",
        "body": """Hi,

We built a Looking Glass that, from public archetypes, pre-computes the likely outcome for an enterprise-AI firm like IBM under EU AI Act — exposure, scenario runs, ranked moves — signed report.

No data from you to start. Verify offline: https://proofof.ai/passport.

Open to a one-framework pilot?

Nick Templeman — CSOAI.org / meok.ai
""",
    },
]


def send_email(api_key, to, subject, body):
    """Send one email via Resend API."""
    req = urllib.request.Request(
        "https://api.resend.com/emails",
        data=json.dumps({
            "from": "Nick Templeman <nicholas@meok.ai>",
            "to": [to],
            "subject": subject,
            "text": body,
        }).encode(),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
    )
    try:
        resp = urllib.request.urlopen(req, timeout=15)
        return {"status": "sent", "id": json.loads(resp.read())["id"]}
    except urllib.error.HTTPError as e:
        return {"status": "failed", "error": e.read().decode()[:200]}


def main():
    api_key = os.environ.get("RESEND_API_KEY")
    if not api_key:
        print("❌ Set RESEND_API_KEY env var first")
        print("   export RESEND_API_KEY=re_...")
        return

    print(f"Sending {len(EMAILS)} design-partner emails via Resend...")
    results = []
    for e in EMAILS:
        result = send_email(api_key, e["to"], e["subject"], e["body"])
        result["segment"] = e["segment"]
        result["to"] = e["to"]
        results.append(result)
        status_emoji = "✅" if result["status"] == "sent" else "❌"
        print(f"  {status_emoji} {e['segment']:30s} → {e['to']:50s} {result.get('id', result.get('error', '?'))[:30]}")

    sent = sum(1 for r in results if r["status"] == "sent")
    print(f"\n✅ Sent {sent}/{len(EMAILS)} emails")
    print(f"   Results saved to ~/clawd/_intake/ready_to_fire/email_results.json")

    with open(os.path.expanduser("~/clawd/_intake/ready_to_fire/email_results.json"), "w") as f:
        json.dump(results, f, indent=2)


if __name__ == "__main__":
    main()
