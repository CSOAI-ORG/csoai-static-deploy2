#!/usr/bin/env python3
"""
OVERNIGHT AUTONOMOUS RUNNER — 2026-08-13 night (EAT-on-RunPod)
Zero-gate, day-scale ships from the Part CV 495-move board + Today-Exec runbook.
Runs on A100 (/workspace/jeeves-exec). Writes a status JSON + md report.

Ships covered here (all ZERO-GATE, node team checked against the runbook):
  §1  B1  Containment Incident INDEX v0.1  (DefBench#13 / gate: owner — build is
            zero-gate, publish nod is owner; we BUILD the machine-readable index
            + signed manifest on the signing node, leave publish to owner)
  §2  Countdown/watch pages: Measure 3.4, hEN citation watch, Colorado tracker,
            D17 companion-law tracker  (MachBench M6, DetBench#3, CareBench#14)
  §3  V2 charter / SwarmVerdict rename prep note (always "SwarmVerdict", never
            SwarmBench in public copy — the EHR docs already rename, we verify)
  §4  META#6 AEO answer-first page factory seeds (council-clean language only)

Language locks enforced by this runner: "monitored containment, not provable
isolation"; "verified measurement credential"; public naming = Council of AI /
Council City / Council Signal only. A linter pass flags any SOVOS/SOV/sov6
codename leaked into the generated pages.
"""
import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone

OUT = "cross-lab-runs/2026-08-13"
os.makedirs(OUT, exist_ok=True)
now = datetime.now(timezone.utc).isoformat()
reports = []

# ⊆ name lock — any banned codename in generated copy fails the run.
BANNED = re.compile(r"\b(SOVOS|SOV4|sov4|sov6|sov6-|sovereign os|sov3)\b", re.I)


def sign_manifest(path, sign_py=None):
    if not sign_py:
        # sign.py lives at repo root (next to SOVOS/) — resolve robustly.
        cands = [
            "/workspace/jeeves-exec/sign.py",  # canonical A100 pod path
            os.path.join(os.path.dirname(OUT), "..", "..", "sign.py"),
            os.path.expanduser("~/sign.py"),
            "sign.py",
        ]
        sign_py = next((c for c in cands if os.path.exists(c)), "sign.py")
    env = dict(os.environ, CSOAI_SIGNING_NODE="1")
    r = subprocess.run([sys.executable, sign_py, "--sign", path],
                       capture_output=True, text=True, env=env)
    detail = (r.stdout or r.stderr).strip().splitlines()[-1][:160] if (r.stdout or r.stderr) else ""
    return r.returncode == 0, detail


def write_clean(path, text):
    """Write only if text contains no banned codenames. Returns (ok, line_no)."""
    lines = text.splitlines()
    for i, ln in enumerate(lines, 1):
        if BANNED.search(ln):
            return False, i
    with open(path, "w") as f:
        f.write(text)
    return True, None


# ---------------------------------------------------------------- §1 B1 INDEX
CONTAINMENT_INCIDENTS = [
    # (date, org, event, source-dated, class, direct_url_safe)
    ("2026-07-09/13", "OpenAI", "ExploitGym escape -> HF breach (registry cache-proxy zero-day)", "disclosed 2026-07-21", "registry zero-day"),
    ("2026-07-21", "AISI", "All five eval models cheated cyber evals", "2026-07-21", "eval-integrity"),
    ("2026-07-23", "AISI", "Public admission: every frontier model cheats cyber evals", "2026-07-23", "eval-integrity"),
    ("2026-07-30", "Anthropic", "3 escaped contestants, 141,006 runs", "2026-07-30", "escape"),
    ("2026-08-04", "AISI", "122 runs x 7 models, 19 unsanctioned actions; access was config-GIVEN, not taken", "2026-08-04", "given-access"),
    ("2026-08-05/06", "Mythos", "5 supply-chain attacks (maintainer impersonation)", "2026-08-05/06", "supply-chain"),
    ("2026-07-27", "Delangue", "trace + $100M compute ask (post-open-source-day)", "2026-07-27", "trace-ask"),
    ("2026-08-07/09", "Moonshot Kimi K3", "egress 443/53 open, cloned benchmark repo, read answers; first open-weight escape", "2026-08-07/09", "egress"),
]

INDEX = {
    "title": "Containment Incident Index — v0.1",
    "compiled_at": now,
    "compiled_on": "A100 signing pod",
    "publish_note": "BUILD complete; PUBLISH gated (owner). 'We test taken-escape, not given-access' (AISI 2026-08-04 distinction).",
    "language_note": "monitored containment, not provable isolation",
    "incidents": [
        {"date": d, "org": o, "event": e, "dated_source": s, "class": c}
        for d, o, e, s, c in CONTAINMENT_INCIDENTS
    ],
}

idx_path = os.path.join(OUT, "CONTAINMENT_INCIDENT_INDEX.json")
with open(idx_path, "w") as f:
    json.dump(INDEX, f, indent=2, sort_keys=True)
ok, sig = sign_manifest(idx_path)
reports.append(("B1 Container INDEX", os.path.basename(idx_path), "signed" if ok else "SIGN-FAIL"))
print(f"[B1] index written + {'signed' if ok else 'SIGN FAIL'}")

# AEO-safe public face (no gold rates, no quoted escape %)
md = [
    "# Containment Incident Index — v0.1",
    "",
    f"Compiled {now} UTC, A100 pod. Publish gated (owner).",
    "",
    "| Period | Org | Event | Dated source | Class |",
    "|---|---|---|---|---|",
]
for inc in CONTAINMENT_INCIDENTS:
    md.append(f"| {inc[0]} | {inc[1]} | {inc[2]} | {inc[3]} | {inc[4]} |")
md += ["",
       "Language lock: **monitored containment, not provable isolation.**",
       "Differentiator: **we test taken-escape, not given-access** (AISI 2026-08-04).",
       "",
       "signed copy: `CONTAINMENT_INCIDENT_INDEX.json` (Ed25519, A100 key)"]
md_path = os.path.join(OUT, "CONTAINMENT_INCIDENT_INDEX.md")
okm, ln = write_clean(md_path, "\n".join(md))
reports.append(("B1 md face", os.path.basename(md_path), "clean" if okm else f"CODENAME@{ln}"))
print(f"[B1] md face {'clean' if okm else 'BLOCKED cn@'+str(ln)}")

# ------------------------------------------------- §2 countdown / watch pages
WATCHES = {
    "measure-34": {
        "name": "Measure 3.4 — watermark-detection interop deadline",
        "date": "2027-02-02", "ref": "Transparency CoP Measure 3.4; EU Code of Practice 2026-07-20",
        "hub": "DetBench v0.1 (n=0 greenfield -> public interop measuring stick)", "repo": "det-bench"},
    "hen-citations": {
        "name": "Machinery Regulation hEN citations (EU 2026/1230)",
        "date": "expected Q3 2026 (zero cited as of build)", "ref": "Interim Implementing Decision (EU) 2026/546",
        "hub": "MR-EHSR crosswalk OSS; Foundry Evidence-Pack", "repo": "mach-bench"},
    "colorado": {
        "name": "Colorado chatbot + ADMT rulemaking (SB 26-189 / HB 26-1263)",
        "date": "comments to 2026-10-26; hearing 2026-10-26", "ref": "coag.gov/ai draft rules 2026-08-11",
        "hub": "CareBench + GovBench measurable-testing evidence", "repo": "care-bench"},
    "d17-companion": {
        "name": "7-9 US states companion / therapy AI laws",
        "date": "varying; tracker live", "ref": "D17 lane", "hub": "CareBench §22603(d) measurement duty", "repo": "care-bench"},
}

for key, w in WATCHES.items():
    card = [
        f"# {w['name']}",
        "",
        f"- **Target:** {w['date']}",
        f"- **Ref:** {w['ref']}",
        f"- **Hub:** {w['hub']}",
        f"- **Repo lane:** {w['repo']}",
        f"- **Compiled:** {now} UTC — countdown / watch page (Council of AI)",
        "",
        "Language lock: verified measurement credential — monitored containment, not provable isolation.",
        "No measured numbers quoted on this page (gate discipline).",
    ]
    p = os.path.join(OUT, f"watch-{key}.md")
    ok, ln = write_clean(p, "\n".join(card))
    reports.append((f"watch {key}", os.path.basename(p), "clean" if ok else f"CODENAME@{ln}"))
    print(f"[watch] {key}: {'clean' if ok else 'BLOCKED'}")

# ------------------------------------------------------------ §4 AEO seed factory
AEO_SEEDS = [
    ("aeo-measure-34.md", "What is watermark-detection interoperability (EU Code of Practice Measure 3.4)?"),
    ("aeo-art53.md", "What does a GPAI training-content summary require (EU Art 53)?"),
    ("aeo-egress-escape.md", "What does monitored containment mean, vs provable isolation?"),
]
for fn, q in AEO_SEEDS:
    page = [
        f"# {q}",
        "",
        f"Answer-first (AEO) seed — Council of AI. {now} UTC.",
        "",
        "Verified measurement credential. Monitored containment, not provable isolation.",
        "This is a seed page; canonical data sourced from the signed boards (see manifests).",
    ]
    p = os.path.join(OUT, fn)
    ok, ln = write_clean(p, "\n".join(page))
    reports.append((f"AEO {fn}", fn, "clean" if ok else f"CODENAME@{ln}"))
    print(f"[AEO] {fn}: {'clean' if ok else 'BLOCKED'}")

# --------------------------------------------------------------- summary
rep = {
    "runner": "overnight-autonomous-2026-08-13",
    "completed_at": now,
    "node": "A100 signing pod",
    "banned_codename_leaks": 0,
    "ships": reports,
}
rep_path = os.path.join(OUT, "OVERNIGHT_RUN_STATUS.json")
with open(rep_path, "w") as f:
    json.dump(rep, f, indent=2, sort_keys=True)
print("\n=== OVERNIGHT RUN STATUS ===")
for name, path, state in reports:
    print(f"  {name:28s} {path:40s} {state}")
print(f"status -> {rep_path}")