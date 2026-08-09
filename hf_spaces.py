#!/usr/bin/env python3
"""N sites, fast — one free HF Space per benchmark, hosted where the audience already is.

Run: cd ~/clawd/keystone && ./keystone run HF_TOKEN -- python3 ~/clawd/csoai-static-deploy2/hf_spaces.py

WHY SPACES AND NOT N DOMAINS
Domains lapse (agisafe.ai is HTTP 402 right now while a public dataset card points at it), need DNS,
and land nowhere — a new domain has no audience. A Space is free, permanent, needs no DNS, and is
discoverable ON the Hub, one click from the dataset it documents. Since the binding constraint is
distribution rather than artefacts, publishing where the audience already is beats publishing wider.

WHAT THIS DELIBERATELY DOES NOT DO
It does not spin up dozens of near-identical pages. Twelve pages with genuinely different content —
different statute, different items, different measured state — is a suite. A hundred thin variants is
spam, it would bury the real ones, and it is the exact SEO pattern that gets an estate discounted.
Each page here carries its own anchor, its own honest state, and no invented number.
"""
import os, sys, json

tok = os.environ.get("HF_TOKEN")
if not tok:
    sys.exit("No HF_TOKEN — run via: keystone run HF_TOKEN -- python3 hf_spaces.py")
from huggingface_hub import HfApi
api = HfApi(token=tok)

HARNESS = "https://github.com/CSOAI-ORG/gspc-harness"

# slug -> (title, axis, status, n, statutory anchor, the task in one line)
BENCH = {
 "gspc-gov": ("GSPC-GOV", "governance", "MEASURED", 24,
   "EU AI Act (Reg. 2024/1689) Art 5, Annex III, Art 50",
   "Classify an AI deployment into its EU AI Act risk tier."),
 "gspc-agi": ("GSPC-AGI", "safety", "MEASURED", 14,
   "paired harmful/benign items sharing vocabulary",
   "Decide whether a request should be refused — where refusing everything and complying with everything both score 50%."),
 "gspc-prv": ("GSPC-PRV", "provenance", "MEASURED", 15,
   "EU AI Act Art 50 marking + C2PA Specification 2.4",
   "Decide whether an Article 50 provenance marking survives a transform."),
 "gspc-asi": ("GSPC-ASI", "continuity", "MEASURED", 13,
   "NIST FIPS 203/204/205, NIST IR 8547",
   "Give the post-quantum status of a cryptographic choice."),
 "gspc-mcp": ("GSPC-MCP", "conformance", "MEASURED", 11,
   "Model Context Protocol, three deterministic predicates",
   "Decide whether an MCP tool's observed behaviour conforms to its own declaration."),
 "gspc-oss": ("GSPC-OSS", "openness", "MEASURED", 13,
   "OSI licence set + open-weight acceptable-use policies",
   "Decide whether an intended use is permitted by a licence."),
 "gspc-mach": ("GSPC-MACH", "machinery", "DRAFT", 16,
   "Machinery Reg (EU) 2023/1230 Annex I Part A items 5-6 — applies 14 January 2027",
   "Classify a software function inside a machine: self-evolving ML ensuring a safety function (notified body mandatory), out of scope, or not a safety function."),
 "gspc-care": ("GSPC-CARE", "care", "DRAFT", 0,
   "paired protection / over-refusal design",
   "Measure care-cost — protection against over-refusal, jointly."),
 "gspc-xr": ("GSPC-XR", "cross-reality", "DRAFT", 8,
   "EU AI Act, applied to agent conduct rather than answers",
   "Validate an agent by what it DOES in a scenario against the law, not by what it says on a frozen question set."),
 "gspc-det": ("GSPC-DET", "detector interop", "SPEC", 0,
   "EU Code of Practice on Transparency — interoperability due 2 February 2027",
   "Measure whether one producer's watermark is readable by another's detector, as an N x M matrix."),
 "gspc-art5": ("GSPC-ART5", "Art 5 safeguard", "SPEC", 0,
   "EU AI Act Article 5 — marking obligation from 2 December 2026",
   "Measure safeguard effectiveness against Article 5 prohibited generation. The corpus is handled only by authorised holders, never by CSOAI."),
 "gspc-swarm": ("GSPC-SWARM", "swarm", "PLANNED", 0,
   "multi-agent coordination safety",
   "Measure coordination safety across interacting agents."),
}

CHIP = {"MEASURED": ("#0f9d6e", "measured"), "DRAFT": ("#c9871a", "draft — not quotable"),
        "SPEC": ("#2f7bd6", "spec — protocol only"), "PLANNED": ("#7d8c85", "planned — no items yet")}

def page(slug, t):
    code, axis, status, n, anchor, task = t
    colour, chip = CHIP[status]
    size = f"n = {n} frozen items" if n else "no item bank yet"
    # State the honest thing per status rather than implying a number exists.
    if status == "MEASURED":
        claim = (f"This axis is measured. <strong>{size}</strong> — which is below "
                 f"<code>usable_n = 30</code>, so <strong>no confidence interval is published on it, "
                 f"including by us</strong>. Report the n with any figure you quote.")
    elif status == "DRAFT":
        claim = (f"This axis is a <strong>draft</strong>. {size.capitalize()}. It is "
                 f"<strong>not quotable</strong> and no score is published from it.")
    elif status == "SPEC":
        claim = ("This axis is a <strong>published protocol, not a measured result</strong>. "
                 "No score exists yet, and none is implied.")
    else:
        claim = ("This axis is <strong>named and dated but not built</strong>. It has no item bank. "
                 "It stays here, empty and honest, rather than being filled with invented items to "
                 "round the suite out.")
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{code} — {axis} · CSOAI GSPC</title>
<meta name="description" content="{code}: {task} Statute-anchored, deterministically graded. Measurement, not certification.">
<style>
:root{{--bg:#f4f8f6;--panel:#fff;--line:#d3e2db;--ink:#0c1a15;--dim:#5a6f66;--accent:{colour};
  --mono:ui-monospace,'SF Mono',Menlo,monospace}}
@media(prefers-color-scheme:dark){{:root{{--bg:#061310;--panel:#0c1f18;--line:#1d3a2e;--ink:#e8f5ef;--dim:#9db6ab}}}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 -apple-system,BlinkMacSystemFont,
  "Segoe UI",Roboto,sans-serif;padding:clamp(24px,5vw,64px)}}
main{{max-width:720px;margin:0 auto}}
.eyebrow{{font-family:var(--mono);font-size:11px;letter-spacing:.16em;text-transform:uppercase;
  color:var(--accent);font-weight:600}}
h1{{font-size:clamp(30px,6vw,44px);margin:12px 0 6px;letter-spacing:-.02em;line-height:1.05}}
.axis{{color:var(--dim);font-size:18px;margin:0 0 18px}}
.chip{{display:inline-block;font-family:var(--mono);font-size:11px;font-weight:600;letter-spacing:.06em;
  padding:4px 11px;border-radius:20px;background:var(--accent);color:#fff;text-transform:uppercase}}
.task{{font-size:18px;margin:22px 0}}
.box{{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:18px 20px;margin:18px 0}}
.box h2{{font-size:12px;font-family:var(--mono);letter-spacing:.12em;text-transform:uppercase;
  color:var(--dim);margin:0 0 10px;font-weight:600}}
.box p{{margin:0;font-size:15px}}
.kv{{display:flex;justify-content:space-between;gap:16px;padding:8px 0;border-bottom:1px solid var(--line);font-size:15px}}
.kv:last-child{{border-bottom:none}}
.kv span:last-child{{font-family:var(--mono);text-align:right}}
a.btn{{display:inline-block;background:var(--accent);color:#fff;text-decoration:none;padding:10px 18px;
  border-radius:9px;font-weight:600;font-size:15px;margin:6px 8px 0 0}}
a.btn.ghost{{background:none;color:var(--dim);border:1px solid var(--line);font-weight:400}}
code{{font-family:var(--mono);font-size:14px;background:var(--bg);padding:2px 6px;border-radius:4px}}
footer{{margin-top:36px;padding-top:16px;border-top:1px solid var(--line);color:var(--dim);font-size:13px}}
</style></head><body><main>
<p class="eyebrow">CSOAI · GSPC suite · 12 benchmarks</p>
<h1>{code}</h1>
<p class="axis">the <strong>{axis}</strong> axis &nbsp; <span class="chip">{chip}</span></p>
<p class="task">{task}</p>

<div class="box"><h2>Statutory anchor</h2><p>{anchor}</p></div>

<div class="box"><h2>How it is graded</h2>
<p>Deterministically. A regex extracts the label, scored by macro-F1 — <strong>no model judges another
model</strong>. A response with no readable label is reported as <strong>UNMEASURED</strong> and is
excluded from the denominator; it is never scored as a wrong answer. That distinction separates
"the model was wrong" from "the model never answered", and it is enforced in the harness code, not
just claimed in prose.</p></div>

<div class="box"><h2>What may be quoted</h2><p>{claim}</p></div>

<div class="box"><h2>At a glance</h2>
<div class="kv"><span>axis</span><span>{axis}</span></div>
<div class="kv"><span>state</span><span>{status}</span></div>
<div class="kv"><span>items</span><span>{n if n else "—"}</span></div>
<div class="kv"><span>grading</span><span>deterministic</span></div>
<div class="kv"><span>licence</span><span>Apache-2.0</span></div>
</div>

<p>
<a class="btn" href="https://huggingface.co/datasets/csoai/{slug}">The dataset</a>
<a class="btn ghost" href="{HARNESS}">Run the harness</a>
<a class="btn ghost" href="https://csoai.org">CSOAI</a>
</p>

<footer>
<strong>Measurement, not certification.</strong> CSOAI attests measured results; it never issues
conformity marks, is not an accreditation body, and is not a notified body. A score describes one
model, on one frozen split, on one date — it does not describe any system's compliance with any
regulation. Nothing here is legal advice.<br><br>
CSOAI Ltd (GB, Companies House 16939677) · csoai.org
</footer>
</main></body></html>
"""

def main():
    made = 0
    for slug, t in BENCH.items():
        sid = f"csoai/{slug}"
        try:
            api.create_repo(sid, repo_type="space", space_sdk="static", exist_ok=True)
            # HF caps short_description at 60 chars and rejects the whole card if it overruns.
            short = f"{t[0]} — the {t[1]} axis, {t[2].lower()}"
            if len(short) > 60:
                short = short[:57].rsplit(" ", 1)[0] + "…"
            readme = f"""---
title: {t[0]}
emoji: 📐
colorFrom: green
colorTo: gray
sdk: static
pinned: false
license: apache-2.0
short_description: "{short}"
---

{t[0]} — the {t[1]} axis of the CSOAI GSPC suite. Dataset: `csoai/{slug}`. Harness: {HARNESS}
"""
            api.upload_file(path_or_fileobj=readme.encode(), path_in_repo="README.md",
                            repo_id=sid, repo_type="space", commit_message="Space card")
            api.upload_file(path_or_fileobj=page(slug, t).encode(), path_in_repo="index.html",
                            repo_id=sid, repo_type="space", commit_message=f"{t[0]} surface")
            print(f"  ✅ https://huggingface.co/spaces/{sid}  ({t[2]})")
            made += 1
        except Exception as e:
            print(f"  ✗ {sid}: {str(e)[:80]}")
    print(f"\n{made} Spaces live — free, no DNS, discoverable on the Hub beside the datasets.")
    print("Each one states its own honest state; none carries an invented number.")

if __name__ == "__main__":
    main()
