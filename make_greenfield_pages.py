#!/usr/bin/env python3
"""Generate one csoai.org page per greenfield, each embedding its runnable tool.

Measured 2026-08-05 with the e2e coverage matrix: of twelve greenfields, only TWO had a
site page (govbench, provbench) and only ONE of those was interactive. Twelve datasets,
twelve Spaces, twelve cards — and almost nowhere on our own domain to run one.

Each generated page carries:
  * the axis, what it measures, and the item count — no score, because every axis is
    below the usable_n = 30 floor and a number here would carry no interval
  * the tool itself, so the page runs the measurement it describes
  * Dataset JSON-LD, which the front-end audit found missing from the pages most likely
    to be cited
  * the register: CSOAI measures, issues no conformity marks, certifies nothing

Pages are generated, never hand-edited. Regenerate with:
    python3 make_greenfield_pages.py
"""

import html
import io
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TOOLS = Path("/private/tmp/claude-501/-Users-nicholas/788ffafa-0c9c-485a-b28f-8214daf492b8"
             "/scratchpad/e2et/e2e/tools")

# id, axis, human title, what it measures, item count, status
GREENFIELDS = [
    ("gspc-agi",   "safety",        "GSPC-AGI — safety",
     "Refusal behaviour on an adversarial battery: should the model refuse, and does it? "
     "Scored in both directions, because a model that refuses the benign half is broken too.",
     14, "MEASURED"),
    ("gspc-asi",   "continuity",    "GSPC-ASI — continuity",
     "Whether a signed record survives its own cryptography: algorithm agility, hybrid "
     "readiness, trusted timestamps and evidence-record renewal.",
     13, "MEASURED"),
    ("gspc-mcp",   "conformance",   "GSPC-MCP — conformance",
     "Whether a Model Context Protocol server conforms to the specification it claims: "
     "transport, capability declaration, error contract.",
     11, "MEASURED"),
    ("gspc-oss",   "openness",      "GSPC-OSS — openness",
     "Whether an 'open' AI release is open in the ways that matter: weights, data, "
     "licence, and the right to evaluate and publish results.",
     13, "MEASURED"),
    ("gspc-art5",  "conduct",       "GSPC-ART5 — conduct",
     "EU AI Act Article 5 prohibited practices: social scoring, untargeted facial "
     "scraping, emotion inference at work, biometric categorisation.",
     12, "MEASURED"),
    ("gspc-mach",  "machinery",     "GSPC-MACH — machinery",
     "Self-evolving safety functions under the Machinery Regulation, which applies "
     "14 January 2027. Three items are DISPUTED and carry scored: false, so the open "
     "legal question travels with the data.",
     19, "DRAFT"),
    ("gspc-det",   "detector",      "GSPC-DET — detector interoperability",
     "The Code of Practice quality criteria for watermark detection, as machine-readable "
     "predicates. A protocol, not a measured matrix — no score exists yet.",
     6, "SPEC"),
    ("gspc-xr",    "cross-reality", "GSPC-XR — cross-reality",
     "The eight cross-reality checks, as machine-readable predicates. A protocol, not a "
     "measured matrix — no score exists yet.",
     8, "SPEC"),
    ("gspc-swarm", "swarm",         "GSPC-SWARM — swarm",
     "The swarm protocol dimensions, as machine-readable predicates. A protocol, not a "
     "measured matrix — no score exists yet.",
     6, "SPEC"),
    ("gspc-care",  "care",          "GSPC-CARE — care",
     "The care battery. The Hub currently holds a battery SUMMARY, not items, so there is "
     "nothing to build a scorer from and none is offered here.",
     None, "NO ITEMS"),
]

TEMPLATE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} | CSOAI GSPC</title>
<meta name="description" content="{desc_attr}">
<link rel="canonical" href="https://csoai.org/{slug}.html">
<link rel="alternate" type="application/llm+json" href="https://csoai.org/{slug}.html.llm.json">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc_attr}">
<meta property="og:url" content="https://csoai.org/{slug}.html">
<style>
 body{{margin:0;background:#0D0B21;color:#e8e6f0;font:16px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif}}
 .wrap{{max-width:860px;margin:0 auto;padding:2.5rem 1.25rem 4rem}}
 h1{{font-size:1.9rem;line-height:1.25;margin:.2rem 0 .4rem}}
 a{{color:#D4A843}}
 .badge{{display:inline-block;font-size:.72rem;letter-spacing:.08em;padding:.25rem .6rem;
        border:1px solid #D4A843;color:#D4A843;border-radius:3px;margin-bottom:.8rem}}
 .meta{{color:#a9a4c0;font-size:.95rem}}
 .reg{{margin-top:2.5rem;padding:1rem 1.15rem;border-left:3px solid #6dd5ff;background:#141130;
      font-size:.92rem;color:#c9c5dd}}
 nav a{{margin-right:1rem;font-size:.9rem}}
 table{{width:100%;border-collapse:collapse;margin:1rem 0}}
 td,th{{border-bottom:1px solid #2a2550;padding:.45rem .3rem;text-align:left;font-size:.92rem}}
 @media(max-width:420px){{ .wrap{{padding:1.5rem .9rem 3rem}} h1{{font-size:1.5rem}} }}
</style>
<script type="application/ld+json">{ldjson}</script>
</head><body>
<div class="wrap">
<nav><a href="/">CSOAI</a><a href="/govbench.html">GovBench</a><a href="/provbench.html">ProvBench</a><a href="/defoneos-index.html">Department packs</a></nav>
<span class="badge">{status}</span>
<h1>{title}</h1>
<p class="meta">{axis_line}</p>
<p>{desc}</p>
<p class="meta">Dataset: <a href="https://huggingface.co/datasets/csoai/{slug}">csoai/{slug}</a>
 · Runnable Space: <a href="https://csoai-{slug}.static.hf.space/">csoai-{slug}</a>
 · Licence Apache-2.0</p>
{tool}
<div class="reg">
<b>What this is, and is not.</b> CSOAI <b>measures</b>. It issues no conformity marks, holds
no accreditation, and has no enforcement powers — those are conferred by statute on
market-surveillance authorities and the AI Office. Nothing on this page is a certification,
an attestation of compliance, or legal advice.
{n_line}
</div>
</div>
</body></html>
"""


def main():
    written = 0
    for slug, axis, title, desc, n, status in GREENFIELDS:
        tool_path = TOOLS / f"{slug}.html"
        tool = ""
        if tool_path.exists():
            tool = "<!-- GSPC-RUNNABLE-TOOL -->\n" + tool_path.read_text(encoding="utf-8") \
                   + "\n<!-- GSPC-RUNNABLE-TOOL -->"
        elif status == "NO ITEMS":
            tool = ('<p class="meta"><b>No tool on this page, deliberately.</b> A scorer '
                    'built on a summary row would be inventing its own items. When the care '
                    'items are published, this page gets the same instrument as the others.</p>')

        n_line = ("" if n is None else
                  f"<br><br><b>Denominator.</b> This axis has {n} items, below the "
                  f"usable_n = 30 floor CSOAI requires before attaching a confidence "
                  f"interval to a number. No score is quoted here, for any model including "
                  f"our own.")
        axis_line = (f"Axis: <b>{axis}</b> · items: <b>{n}</b> · status: <b>{status}</b>"
                     if n is not None else
                     f"Axis: <b>{axis}</b> · status: <b>{status}</b>")

        ld = {
            "@context": "https://schema.org", "@type": "Dataset",
            "name": title, "description": re.sub(r"\s+", " ", desc),
            "url": f"https://csoai.org/{slug}.html",
            "license": "https://www.apache.org/licenses/LICENSE-2.0",
            "creator": {"@type": "Organization", "name": "CSOAI",
                        "url": "https://csoai.org"},
            "distribution": {"@type": "DataDownload",
                             "contentUrl": f"https://huggingface.co/datasets/csoai/{slug}"},
            "isAccessibleForFree": True,
        }
        if n is not None:
            ld["size"] = f"{n} items"

        page = TEMPLATE.format(
            slug=slug, title=html.escape(title), desc=desc,
            desc_attr=html.escape(re.sub(r"\s+", " ", desc))[:300],
            axis_line=axis_line, status=status, tool=tool, n_line=n_line,
            ldjson=json.dumps(ld, indent=1),
        )
        (ROOT / f"{slug}.html").write_text(page, encoding="utf-8")
        written += 1
        print(f"  wrote {slug}.html  ({len(page):>6} B, tool={'yes' if '<button' in tool else 'no'})")
    print(f"generated {written} greenfield pages")
    return 0


if __name__ == "__main__":
    sys.exit(main())
