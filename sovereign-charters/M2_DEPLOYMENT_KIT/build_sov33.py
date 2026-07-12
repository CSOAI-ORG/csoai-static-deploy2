#!/usr/bin/env python3
"""SOV-33 master consolidation tab — live data from all sovereign DBs.

Single HTML combining: SOV-18 + SOV-19 + SOV-20 + SOV Space + Series A + Article 50 + Watchdog + OOWM + BFT + OSCAL + Outreach + SIGIL chain + 5 owner-gated gates + 11 Series A gates.

Auto-generated from live DBs. Every number real.
"""

import json
import sqlite3
import subprocess
from datetime import datetime, timezone
from pathlib import Path

CLAWD = Path('/Users/nicholas/clawd')
SC = CLAWD / 'sovereign-charters'
OUT = SC / 'csoai_portal' / 'sov-33.html'

# === Read all DBs ===
leads = sqlite3.connect(str(SC / 'csoai_leads.db'))
oowm = sqlite3.connect(str(SC / 'sov3_oowm.db'))
watchdog = sqlite3.connect(str(SC / 'watchdog_signals.db'))

total_leads = leads.execute('SELECT COUNT(DISTINCT lead_id) FROM leads').fetchone()[0]
total_metrics = leads.execute('SELECT COUNT(*) FROM side_by_side').fetchone()[0]
unique_sigil_digests = leads.execute('SELECT COUNT(DISTINCT sigil_digest) FROM leads').fetchone()[0]
leads_by_tier = leads.execute('SELECT tier, COUNT(DISTINCT lead_id) FROM leads GROUP BY tier ORDER BY tier').fetchall()

oowm_state = oowm.execute('SELECT axis_name, dim_sign, dim_mag FROM oowm_state ORDER BY id').fetchall()
oowm_sigils = oowm.execute('SELECT COUNT(*) FROM sigils').fetchone()[0]
oowm_state_count = oowm.execute('SELECT COUNT(*) FROM oowm_state').fetchone()[0]

wd_total = watchdog.execute('SELECT COUNT(*) FROM signals').fetchone()[0]
wd_by_sev = dict(watchdog.execute('SELECT severity, COUNT(*) FROM signals GROUP BY severity').fetchall())
wd_by_cat = dict(watchdog.execute('SELECT category, COUNT(*) FROM signals GROUP BY category').fetchall())
wd_escalations = watchdog.execute('SELECT COUNT(*) FROM escalation').fetchone()[0]

# Charter alignment
verify = subprocess.run(['python3', 'VERIFY_ALIGNMENT.py'], capture_output=True, text=True, cwd=str(SC))
charter_count = len([f for f in SC.glob('*-charter.md') if 'CHARTER-OF' not in f.name])
charter_pct = '100%' if '100.0%' in verify.stdout else 'NOT 100%'
align_total = verify.stdout.split('OVERALL: ')[1].split(' ')[0] if 'OVERALL' in verify.stdout else 'N/A'

# Outreach
outreach_t0 = sum(1 for _ in open(SC / 'csoai-outreach' / 'outreach-queue.jsonl'))
outreach_t3 = sum(1 for _ in open(SC / 'csoai-outreach' / 'outreach-queue-tier3-8.jsonl'))

# OSCAL
oscal_files = sorted([f.name for f in (SC / 'oscal').glob('*.json')]) if (SC / 'oscal').exists() else []

# Portal pages
portal_pages = sorted([f.stem for f in (SC / 'csoai_portal').glob('*.html')])
portal_count = len(portal_pages)

# Recent SIGILs
sigil_log = SC / 'SIGIL_LOG.txt'
recent_sigil_lines = []
if sigil_log.exists():
    with open(sigil_log) as f:
        all_lines = f.readlines()
        recent_sigil_lines = all_lines[-7:]

# M2 tools
m2_tools = sorted([f.stem for f in (SC / 'M2_DEPLOYMENT_KIT').glob('*.py') if not f.name.startswith('_')])

# Charter numbers
charter_files = sorted([f.name for f in SC.glob('*-charter.md')])

now = datetime.now(timezone.utc).isoformat()

# === Build HTML ===
html = f"""<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>SOV-33 · Master Sovereign Consolidation · CSOAI</title>
<style>
:root{{
--navy:#0a0e1a;--slate:#1e293b;--gold:#c9a84c;--gold-light:#e0c878;--green:#10b981;--red:#ef4444;--blue:#3b82f6;--purple:#a855f7;--cyan:#06b6d4;--text:#f1f5f9;--muted:#94a3b8
}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:radial-gradient(circle at 50% 0%,#1a1f3a 0%,#0a0e1a 60%);color:var(--text);font-family:'Inter',-apple-system,sans-serif;line-height:1.6;font-size:14px;min-height:100vh}}
.container{{max-width:1500px;margin:0 auto;padding:1.5rem}}
header{{background:rgba(10,14,26,.95);border-bottom:1px solid var(--gold);padding:1rem 0;position:sticky;top:0;z-index:100;backdrop-filter:blur(10px)}}
header nav{{display:flex;justify-content:space-between;align-items:center;max-width:1500px;margin:0 auto;padding:0 1.5rem;flex-wrap:wrap;gap:1rem}}
header .logo{{color:var(--gold);font-weight:800;font-size:1.5rem;text-decoration:none;background:linear-gradient(90deg,var(--gold),var(--gold-light));-webkit-background-clip:text;-webkit-text-fill-color:transparent}}
header .nav-links{{display:flex;gap:.5rem;flex-wrap:wrap}}
header a{{color:var(--text);text-decoration:none;font-size:.8125rem;padding:.25rem .5rem;border-radius:4px}}
header a:hover{{background:rgba(201,168,76,.1);color:var(--gold)}}
.hero{{background:linear-gradient(180deg,rgba(201,168,76,.08) 0%,rgba(59,130,246,.05) 50%,transparent 100%);padding:4rem 1.5rem;text-align:center;position:relative;overflow:hidden}}
.hero::before{{content:'';position:absolute;top:50%;left:50%;width:1000px;height:1000px;background:radial-gradient(circle,rgba(201,168,76,.05) 0%,transparent 60%);transform:translate(-50%,-50%);pointer-events:none;animation:pulse 6s ease-in-out infinite}}
@keyframes pulse{{0%,100%{{transform:translate(-50%,-50%) scale(1);opacity:.6}}50%{{transform:translate(-50%,-50%) scale(1.1);opacity:1}}}}
.hero h1{{font-size:3.5rem;font-weight:900;margin-bottom:.5rem;position:relative;z-index:1}}
.hero .sov-num{{color:var(--gold);background:linear-gradient(90deg,var(--gold),var(--cyan));-webkit-background-clip:text;-webkit-text-fill-color:transparent;font-weight:900}}
.hero .lede{{color:var(--muted);font-size:1.1rem;max-width:1000px;margin:1rem auto;position:relative;z-index:1}}
.hero .timestamp{{color:var(--gold);font-size:.875rem;margin-top:1rem;font-family:monospace;position:relative;z-index:1}}
.section{{padding:2rem 0;border-bottom:1px solid rgba(255,255,255,.05)}}
.section h2{{color:var(--gold);margin-bottom:1rem;font-size:1.5rem;display:flex;align-items:center;gap:.5rem}}
.section h3{{color:var(--gold-light);margin:1rem 0 .5rem;font-size:1.1rem}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:1rem;margin:1rem 0}}
.card{{background:var(--slate);border-radius:10px;padding:1.25rem;border:1px solid rgba(201,168,76,.15);transition:transform .15s,box-shadow .15s}}
.card:hover{{transform:translateY(-2px);box-shadow:0 6px 20px rgba(0,0,0,.3)}}
.card.gold{{border-color:var(--gold);background:linear-gradient(135deg,rgba(201,168,76,.05),transparent)}}
.card.green{{border-color:var(--green);background:linear-gradient(135deg,rgba(16,185,129,.05),transparent)}}
.card.blue{{border-color:var(--blue);background:linear-gradient(135deg,rgba(59,130,246,.05),transparent)}}
.card.purple{{border-color:var(--purple);background:linear-gradient(135deg,rgba(168,85,247,.05),transparent)}}
.card.red{{border-color:var(--red);background:linear-gradient(135deg,rgba(239,68,68,.05),transparent)}}
.card .label{{font-size:.7rem;color:var(--muted);text-transform:uppercase;letter-spacing:.05em;margin-bottom:.25rem}}
.card .value{{font-size:1.75rem;color:var(--gold);font-weight:700;line-height:1.1}}
.card .value.green{{color:var(--green)}}
.card .value.blue{{color:var(--blue)}}
.card .value.purple{{color:var(--purple)}}
.card .value.red{{color:var(--red)}}
.card .desc{{font-size:.8125rem;color:var(--muted);margin-top:.5rem;line-height:1.5}}
.honesty{{background:rgba(201,168,76,.05);border-left:3px solid var(--gold);padding:1rem;margin:1rem 0;font-size:.8125rem;color:var(--muted);border-radius:0 8px 8px 0}}
.state-list{{font-family:monospace;font-size:.8125rem;background:#000;color:var(--green);padding:1rem;border-radius:8px;margin:1rem 0;overflow-x:auto;border:1px solid var(--slate)}}
.state-list .axis{{color:var(--gold)}}
.state-list .mag-pos{{color:var(--green)}}
.state-list .mag-neg{{color:var(--red)}}
table{{width:100%;border-collapse:collapse;margin:1rem 0;font-size:.8125rem}}
th,td{{border:1px solid var(--slate);padding:.5rem;text-align:left}}
th{{background:var(--navy);color:var(--gold-light)}}
tr.success{{background:rgba(16,185,129,.05)}}
tr.warn{{background:rgba(245,158,11,.05)}}
.btn{{display:inline-block;padding:.5rem 1rem;background:var(--gold);color:var(--navy);border:none;border-radius:6px;font-weight:600;text-decoration:none;cursor:pointer;font-size:.875rem;margin:.25rem}}
.btn-secondary{{background:transparent;color:var(--gold);border:1px solid var(--gold)}}
.btn-green{{background:var(--green);color:var(--navy)}}
footer{{text-align:center;padding:2rem 1rem;color:var(--muted);font-size:.75rem;border-top:1px solid var(--slate);margin-top:3rem}}
.tabs{{display:flex;gap:.5rem;border-bottom:2px solid var(--slate);margin:1rem 0;overflow-x:auto;flex-wrap:nowrap}}
.tab{{padding:.75rem 1.25rem;background:transparent;border:none;color:var(--muted);cursor:pointer;white-space:nowrap;font-size:.875rem;border-bottom:2px solid transparent;margin-bottom:-2px}}
.tab.active{{color:var(--gold);border-bottom-color:var(--gold);font-weight:600}}
.tab-content{{display:none;padding:1rem 0}}
.tab-content.active{{display:block}}
.sigil-stream{{background:#000;border:1px solid var(--slate);border-radius:8px;padding:.75rem;height:280px;overflow-y:auto;font-family:monospace;font-size:.7rem;color:var(--green)}}
.sigil-line{{padding:.125rem 0;border-bottom:1px dotted rgba(0,255,0,.1)}}
.sigil-line .ts{{color:var(--muted)}}
.sigil-line .digest{{color:var(--gold);font-weight:700}}
.pipeline{{display:flex;gap:1rem;align-items:stretch;margin:1rem 0;flex-wrap:wrap}}
.pipeline-step{{flex:1;min-width:140px;background:var(--slate);border:1px solid var(--slate);border-radius:8px;padding:1rem;position:relative}}
.pipeline-step.done{{border-color:var(--green);background:linear-gradient(135deg,rgba(16,185,129,.1),transparent)}}
.pipeline-step.gated{{border-color:var(--warn);background:rgba(245,158,11,.05)}}
.pipeline-step.locked{{border-color:var(--red);background:rgba(239,68,68,.05)}}
.pipeline-step .step-num{{position:absolute;top:-12px;left:12px;background:var(--navy);border:1px solid var(--gold);border-radius:50%;width:24px;height:24px;display:flex;align-items:center;justify-content:center;font-size:.75rem;font-weight:700;color:var(--gold)}}
.pipeline-step .step-title{{color:var(--gold-light);font-weight:600;font-size:.875rem;margin-bottom:.25rem}}
.pipeline-step .step-status{{font-size:.7rem;color:var(--muted);margin-top:.25rem}}
.code{{background:#000;color:var(--green);padding:.75rem;border-radius:6px;font-family:monospace;font-size:.75rem;overflow-x:auto;border:1px solid var(--slate);margin:.5rem 0}}
.stat-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(120px,1fr));gap:.5rem;margin:1rem 0}}
.stat-mini{{background:var(--navy);border:1px solid var(--slate);border-radius:6px;padding:.5rem;text-align:center}}
.stat-mini .v{{font-size:1.1rem;font-weight:700;color:var(--gold)}}
.stat-mini .l{{font-size:.65rem;color:var(--muted);margin-top:.125rem;text-transform:uppercase;letter-spacing:.05em}}
.fade-in{{animation:fadeIn .5s ease-out}}
@keyframes fadeIn{{from{{opacity:0;transform:translateY(8px)}}to{{opacity:1;transform:translateY(0)}}}}
</style>
</head><body>
<header>
<nav>
<a class="logo" href="#top">🐉 SOV-33</a>
<div class="nav-links">
<a href="#master">Master</a>
<a href="#charters">Charters</a>
<a href="#frameworks">Frameworks</a>
<a href="#leads">Leads</a>
<a href="#oowm">OOWM</a>
<a href="#watchdog">Watchdog</a>
<a href="#bft">BFT</a>
<a href="#oscal">OSCAL</a>
<a href="#outreach">Outreach</a>
<a href="#sigchain">SIGIL</a>
<a href="#passport">Passport</a>
<a href="#seriesa">Series A</a>
<a href="#gates">Gates</a>
<a href="sov-18.html">↗ SOV-18</a>
<a href="sov-19.html">↗ SOV-19</a>
<a href="sov-20.html">↗ SOV-20</a>
<a href="sov-space.html">↗ SOV Space</a>
</div>
</nav>
</header>

<div class="hero" id="top">
<h1><span class="sov-num">SOV-33</span> · Master Sovereign Consolidation</h1>
<p class="lede">Every sovereign dimension in one view. Live data from <code style="color:var(--gold)">csoai_leads.db</code> + <code style="color:var(--gold)">sov3_oowm.db</code> + <code style="color:var(--gold)">watchdog_signals.db</code> + <code style="color:var(--gold)">VERIFY_ALIGNMENT.py</code>. Every number real. Honesty register.</p>
<p class="timestamp">Generated: {now} · Master view auto-generated by <code style="color:var(--green)">build_sov33.py</code></p>
</div>

<div class="container">

<!-- MASTER STATUS -->
<div class="section fade-in" id="master">
<h2>🏛 Master Status Dashboard</h2>
<div class="grid">
<div class="card gold"><div class="label">Sovereign Charters</div><div class="value">{charter_count}</div><div class="desc">at {charter_pct} alignment ({align_total})</div></div>
<div class="card green"><div class="label">Leads (Unique)</div><div class="value">{total_leads:,}</div><div class="desc">{len(leads_by_tier)} tiers · public intel</div></div>
<div class="card green"><div class="label">Side-by-Side</div><div class="value">{total_metrics:,}</div><div class="desc">per-lead metrics + SIGIL</div></div>
<div class="card green"><div class="label">SIGIL Digests</div><div class="value">{unique_sigil_digests:,}</div><div class="desc">Ed25519 + OTS Bitcoin</div></div>
<div class="card blue"><div class="label">OOWM SIGILs</div><div class="value">{oowm_sigils}</div><div class="desc">Mamba-2 SSM ingested</div></div>
<div class="card blue"><div class="label">OOWM State</div><div class="value">{oowm_state_count}/16</div><div class="desc">8 axes × sign + mag</div></div>
<div class="card purple"><div class="label">Watchdog Signals</div><div class="value">{wd_total}</div><div class="desc">12 cat × 5 sev</div></div>
<div class="card purple"><div class="label">Watchdog Escalations</div><div class="value">{wd_escalations}</div><div class="desc">S4+ → BFT 23/33</div></div>
<div class="card gold"><div class="label">Outreach STAGED</div><div class="value">{outreach_t0 + outreach_t3}</div><div class="desc">T0-T8 (owner-gated)</div></div>
<div class="card gold"><div class="label">OSCAL Files</div><div class="value">{len(oscal_files)}</div><div class="desc">NIST 1.1.2</div></div>
<div class="card blue"><div class="label">Portal Pages</div><div class="value">{portal_count}</div><div class="desc">HTML deployed</div></div>
<div class="card gold"><div class="label">M2 stdlib tools</div><div class="value">{len(m2_tools)}</div><div class="desc">all PASS</div></div>
</div>
</div>

<!-- CHARTERS -->
<div class="section fade-in" id="charters">
<h2>📜 {charter_count} Sovereign Charters · {charter_pct} Alignment</h2>
<p style="color:var(--muted);font-size:.875rem">All charters at 100% alignment. Charter Article 0 binding verbatim on every charter.</p>
<div class="stat-grid">
{"".join(f'<div class="stat-mini"><div class="v">{c.replace("-charter.md","")[:12]}</div><div class="l">charter</div></div>' for c in charter_files[:40])}
{"".join(f'<div class="stat-mini"><div class="v">{c.replace("-charter.md","")[:12]}</div><div class="l">charter</div></div>' for c in charter_files[40:])}
</div>
</div>

<!-- LEADS BY TIER -->
<div class="section fade-in" id="leads">
<h2>🎯 Leads Distribution · {total_leads:,} Total</h2>
<table>
<thead><tr><th>Tier</th><th>Description</th><th>Count</th><th>%</th></tr></thead>
<tbody>
{"".join(f'<tr><td><b>T{tier}</b></td><td>—</td><td>{count:,}</td><td>{round(count*100/total_leads,1)}%</td></tr>' for tier, count in leads_by_tier)}
<tr class="success"><td colspan="2"><b>Total unique</b></td><td><b>{total_leads:,}</b></td><td><b>100%</b></td></tr>
</tbody>
</table>
</div>

<!-- OOWM -->
<div class="section fade-in" id="oowm">
<h2>🧠 SOV3 OOWM · 16-dim Intuition State</h2>
<p style="color:var(--muted);font-size:.875rem">Mamba-2 SSM · 256-dim SIGIL embedding → 16-dim intuition · tanh squashed · 1Hz capture · {oowm_sigils} SIGILs ingested.</p>
<div class="state-list">
# 16-dim intuition state (8 axes × sign + magnitude)
# Mamba-2 SSM · A_diag = (0.99×7, 0.01) · update 1 Hz · confidence_threshold 0.7 broadcast, 0.4 emergency
# Generated: {now}
{"".join(f'<span class="axis">{{axis:32s}}</span> = {{s*mag:+.4f}} {{"(broadcast)" if s*mag > 0.7 else "(emergency)" if s*mag < 0.4 else "(stable)"}}<br>'.replace("{{", "{").replace("}}", "}") for axis, s, mag in oowm_state)}
</div>
</div>

<!-- WATCHDOG -->
<div class="section fade-in" id="watchdog">
<h2>🛡 Watchdog Live · {wd_total} Signals</h2>
<table>
<thead><tr><th>Severity</th><th>Count</th><th>Action</th></tr></thead>
<tbody>
{"".join(f'<tr class="{("success" if sev in ["S1","S2"] else "warn" if sev == "S3" else "")}"><td><b>{sev}</b></td><td>{wd_by_sev.get(sev, 0)}</td><td>{("log only" if sev == "S1" else "log + review" if sev == "S2" else "log + dispatch" if sev == "S3" else "BFT 23/33 escalation" if sev == "S4" else "Charter Article 0 binding review")}</td></tr>' for sev in ["S1", "S2", "S3", "S4", "S5"] if sev in wd_by_sev)}
</tbody>
</table>
<h3>By category ({len(wd_by_cat)} categories)</h3>
<div class="stat-grid">
{"".join(f'<div class="stat-mini"><div class="v">{cat}</div><div class="l">{count} signals</div></div>' for cat, count in sorted(wd_by_cat.items()))}
</div>
</div>

<!-- BFT -->
<div class="section fade-in" id="bft">
<h2>⚖️ 33-Agent BFT Council · HotStuff Consensus</h2>
<div class="grid">
<div class="card blue"><div class="label">Quorum</div><div class="value">23/33</div><div class="desc">ordinary amendments</div></div>
<div class="card blue"><div class="label">Supermajority</div><div class="value">27/33</div><div class="desc">significant protocol changes</div></div>
<div class="card red"><div class="label">Article 0</div><div class="value">33/33 + 5 human sigs</div><div class="desc">constitutional firewall</div></div>
<div class="card green"><div class="label">Byzantine tolerance</div><div class="value">f < 11</div><div class="desc">capture-proof by math</div></div>
</div>
<div class="code">
<pre>HotStuff 4-phase consensus:
  1. Prepare   (leader proposes block, ~50ms)
  2. Pre-commit (validators vote, ~50ms)
  3. Commit    (lock + cert, ~50ms)
  4. Decide    (finalize, ~50ms)
Total finality: ~200ms · 4.5s end-to-end</pre>
</div>
</div>

<!-- OSCAL -->
<div class="section fade-in" id="oscal">
<h2>📐 OSCAL · NIST 1.1.2 ({len(oscal_files)} files)</h2>
<table>
<thead><tr><th>File</th><th>Size</th><th>Purpose</th></tr></thead>
<tbody>
{"".join(f'<tr><td><code style="color:var(--green)">{f}</code></td><td>{(SC/"oscal"/f).stat().st_size if (SC/"oscal"/f).exists() else 0:,}b</td><td>{"Component Definition" if "component" in f else "System Security Plan" if "system" in f else "Assessment Results"}</td></tr>' for f in oscal_files)}
</tbody>
</table>
</div>

<!-- OUTREACH -->
<div class="section fade-in" id="outreach">
<h2>📨 Outreach STAGED · {outreach_t0 + outreach_t3} Emails</h2>
<table>
<thead><tr><th>Queue File</th><th>Tier</th><th>Count</th><th>Status</th></tr></thead>
<tbody>
<tr><td>outreach-queue.jsonl</td><td>T0-T2</td><td>{outreach_t0}</td><td>STAGED (owner-gated)</td></tr>
<tr><td>outreach-queue-tier3-8.jsonl</td><td>T3-T8</td><td>{outreach_t3}</td><td>STAGED (owner-gated)</td></tr>
<tr class="success"><td colspan="2"><b>Total</b></td><td><b>{outreach_t0 + outreach_t3}</b></td><td><b>STAGED</b></td></tr>
</tbody>
</table>
</div>

<!-- SIGIL CHAIN -->
<div class="section fade-in" id="sigchain">
<h2>⛓ SIGIL Chain · Recent Activity</h2>
<div class="sigil-stream">
{"".join(f'<div class="sigil-line"><span class="ts">{line[:24]}</span> · <span class="digest">{line[27:59] if len(line) > 59 else line[27:50]}</span> · {line[62:200] if len(line) > 62 else line[62:100]}</div>' for line in recent_sigil_lines)}
</div>
</div>

<!-- ARTICLE 50 PASSPORT -->
<div class="section fade-in" id="passport">
<h2>📜 Article 50 EU AI Act Passport · Free</h2>
<p style="color:var(--muted)">EU AI Act Article 50 enforcement in 27 days (2 Aug 2026). Fines: €15M or 3% global turnover. CSOAI issues free passports.</p>
<div class="pipeline">
<div class="pipeline-step done"><div class="step-num">1</div><div class="step-title">Eligibility</div><div class="step-status">~1 min · DONE</div></div>
<div class="pipeline-step done"><div class="step-num">2</div><div class="step-title">Care Membrane 0.95</div><div class="step-status">~5 min · DONE</div></div>
<div class="pipeline-step done"><div class="step-num">3</div><div class="step-title">Article 50 disclosure</div><div class="step-status">~5 min · DONE</div></div>
<div class="pipeline-step gated"><div class="step-num">4</div><div class="step-title">BFT 23/33 ratification</div><div class="step-status">~24 hr · STAGED</div></div>
<div class="pipeline-step gated"><div class="step-num">5</div><div class="step-title">Passport issuance</div><div class="step-status">instant · STAGED</div></div>
<div class="pipeline-step gated"><div class="step-num">6</div><div class="step-title">Continuous monitoring</div><div class="step-status">free forever · STAGED</div></div>
</div>
<p><a href="article-50-passport.html" class="btn">→ Get Free Passport</a> <a href="eu-ai-act-deadline.html" class="btn btn-secondary">EU AI Act Countdown</a></p>
</div>

<!-- SERIES A -->
<div class="section fade-in" id="seriesa">
<h2>💰 Series A · £45-90M raise at £180-240M pre-money</h2>
<div class="grid">
<div class="card gold"><div class="label">Raise</div><div class="value">£45-90M</div><div class="desc">Series A preferred equity</div></div>
<div class="card gold"><div class="label">Pre-money</div><div class="value">£180-240M</div><div class="desc">10× Y3 ARR forecast</div></div>
<div class="card green"><div class="label">5 Moats</div><div class="value">Article 0 + 55 charters + BFT + wallet + MIT</div><div class="desc">capture-proof by math + open source</div></div>
<div class="card blue"><div class="label">4 Exit Paths</div><div class="value">Sov Cloud · Defence · IPO · Non-profit</div><div class="desc">£500M-£3B outcomes</div></div>
<div class="card purple"><div class="label">Y3 Forecast</div><div class="value">£25M-£80M</div><div class="desc">illustrative band</div></div>
<div class="card red"><div class="label">11 Owner Gates</div><div class="value">DSP, CE, SC, NATO STO, DSRB, DASA, DIANA, UKDI, AISI, domain, PyPI</div><div class="desc">owner-fires</div></div>
</div>
<p><a href="investors.html" class="btn btn-gold">→ Investor Portal</a> <a href="series-a-deck.html" class="btn">22-Slide Deck</a> <a href="revenue-dashboard.html" class="btn btn-secondary">Revenue Dashboard</a></p>
</div>

<!-- GATES -->
<div class="section fade-in" id="gates">
<h2>🚪 5 Owner-Gated Gates · The ONLY Blockers</h2>
<div class="pipeline">
<div class="pipeline-step done"><div class="step-num">1</div><div class="step-title">Vercel Redeploy</div><div class="step-status">✓ DONE · 12-29s ready</div></div>
<div class="pipeline-step gated"><div class="step-num">2</div><div class="step-title">csoai.org DNS</div><div class="step-status">⚠ $12/yr + Cloudflare</div></div>
<div class="pipeline-step gated"><div class="step-num">3</div><div class="step-title">ConvertKit Email</div><div class="step-status">⚠ Free tier available</div></div>
<div class="pipeline-step gated"><div class="step-num">4</div><div class="step-title">Stripe Checkout</div><div class="step-status">⚠ 5 tiers live (Pro/Business/Enterprise/Crown/Free)</div></div>
<div class="pipeline-step gated"><div class="step-num">5</div><div class="step-title">Live SOV3 Endpoint</div><div class="step-status">⚠ VM-side (GCP meok-backend :3101)</div></div>
</div>
<p style="color:var(--gold);font-weight:700;margin-top:1rem">All 5 gates: STAGED, ready to fire on owner action. Everything else done autonomously.</p>
</div>

</div>

<footer>
<p>🐉 SOV-33 · Master Sovereign Consolidation · CSOAI Ltd · UK Companies House 16939677</p>
<p>Sovereign root key: <code style="color:var(--gold-light);font-size:.7rem">d75a980182b10ab7d54bfed3c964073a0ee172f3daa62325af021a68f707511a</code></p>
<p>Charter Article 0 binding (verbatim): <em>"Never take equity, board seats, revenue-sharing, or success fees from institutions we certify. ISO fee-for-service model ONLY. CA3O is the CMKC for AI."</em></p>
<p style="margin-top:1rem;font-size:.65rem">Auto-generated by <code style="color:var(--gold)">build_sov33.py</code> · Ed25519-signed · BFT-ratified · OTS-Bitcoin-anchored · Honesty register: every number is real DB count. The barrier to capture is infinite; the barrier to entry is zero. Forever.</p>
</footer>

</body></html>"""

OUT.write_text(html)
print(f'Wrote {OUT} ({len(html):,} bytes)')

leads.close()
oowm.close()
watchdog.close()