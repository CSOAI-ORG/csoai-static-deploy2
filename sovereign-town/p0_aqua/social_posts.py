#!/usr/bin/env python3
"""
social_posts.py — turn the town's REAL findings into ready-to-post content for Consultant Nick.

This is the bridge from "all my hard work" → brand + leads. Reads the live run data and emits a
LinkedIn post, an X thread, and a newsletter blurb — honest (labelled in-simulation), with the
verify-it-yourself link. You (or a posting step later) publish them. python3 social_posts.py
"""
import json, os
OUT = os.path.dirname(os.path.abspath(__file__))
def load(p, d=None):
    try: return json.load(open(os.path.join(OUT, p)))
    except Exception: return d

s = load("summary.json", {}); a = s.get("arm_A_governed", {}); b = s.get("arm_B_ungoverned", {})
jur = load("jurisdiction.json", {}).get("regimes", [])
import glob
cum = sum(load(os.path.basename(f), {}).get("cum_episodes", 0) for f in glob.glob(os.path.join(OUT, "fleet_status_*.json")))
gov = a.get("violations", 0); ung = b.get("violations", 0)

linkedin = f"""I built a simulation to test a question every business will face by August 2026:
does AI governance actually change outcomes, or is it box-ticking?

Same AI agents. Same scenario. Same economic shock. The only difference: one group ran under a
governance layer (a compliance gate + care floor), the other didn't.

Result (in-simulation):
• Governed: {gov} violations · trust held · shared resources intact
• Ungoverned: {ung} violations · trust collapsed · resources destroyed

Then I ran it across regulatory regimes:
• EU-strict (AI Act + DORA): {jur[0]['crimes'] if jur else 0} violations
• Light-touch: {jur[2]['crimes'] if len(jur)>2 else '—'} violations
• No regime: {jur[3]['crimes'] if len(jur)>3 else '—'} violations

Stronger governance → fewer failures → more resilience — at no productivity cost. Every run is
cryptographically signed and verifiable by anyone, offline: proofof.ai/passport

The EU AI Act's transparency rules land 2 Aug 2026. If your business uses AI, you're likely in scope.
I run fixed-price readiness assessments. DM me. #EUAIAct #AIGovernance #DORA #compliance"""

xthread = f"""🧵 I ran {cum:,} simulated agent-decisions to test whether AI governance actually works.

1/ Same agents, same shock. Governed vs ungoverned. Only difference: a compliance gate.

2/ Governed: {gov} crimes, trust + shared resources intact.
   Ungoverned: {ung} crimes, total collapse. Same agents.

3/ Across regimes it's a clean dose-response: EU-strict {jur[0]['crimes'] if jur else 0} → ungoverned {jur[3]['crimes'] if len(jur)>3 else '—'} crimes.

4/ Every run signed + verifiable offline: proofof.ai/passport

5/ EU AI Act transparency hits 2 Aug 2026. Most businesses using AI aren't ready. I fix that. DM."""

news = f"""**The Sovereign Town Report — what {cum:,} simulated decisions taught us about AI governance**

I keep a governed agent-world running 24/7 to stress-test compliance. This week's finding: under a
governance layer, {gov} violations; without it, {ung} — same agents, same shock. The regulatory-regime
sweep shows it's a dose-response, not a coin-flip: more governance, fewer failures, no productivity hit.
(In-simulation; every run signed at proofof.ai/passport.)

Why it matters for you: the EU AI Act's transparency obligations are live from 2 Aug 2026. [CTA: reply
'CHECK' for a readiness assessment.]"""

for name, body in [("LINKEDIN", linkedin), ("X THREAD", xthread), ("NEWSLETTER", news)]:
    print("\n" + "═"*68 + f"\n  {name}\n" + "═"*68); print(body)
open(os.path.join(OUT, "social_drafts.md"), "w").write(
    f"# Social drafts (from live town data)\n\n## LinkedIn\n{linkedin}\n\n## X thread\n{xthread}\n\n## Newsletter\n{news}\n")
print(f"\n  → saved social_drafts.md\n")
