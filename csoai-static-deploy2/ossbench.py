#!/usr/bin/env python3
"""ossbench.py — SOV-OSS: do public AI releases carry what the law still requires of them?

═══════════════════════════════════════════════════════════════════════════════
THE AXIS, AND WHY IT IS NARROWER THAN "AUDIT OPEN SOURCE FOR COMPLIANCE"
═══════════════════════════════════════════════════════════════════════════════
A repository cannot be "AI Act compliant" — the Act binds a provider placing a system on the
market, not a folder of code. Scoring repos for generic compliance would be adjudication, and
we do not adjudicate.

But there is something real, and it is precise: **the open-source exemption is partial.**

  • Art 53(1)(a) technical documentation ........ WAIVED for free/open-source GPAI
  • Art 53(1)(b) info to downstream providers ... WAIVED for free/open-source GPAI
  • Art 53(1)(c) copyright policy ............... **STILL APPLIES**
  • Art 53(1)(d) training-content summary ....... **STILL APPLIES**

Two obligations survive the exemption, both are satisfied by *publishing something publicly*,
and both are therefore checkable without permission, without a contract, and without touching
anything private. **Nobody publishes whether they are present.**

Add the Cyber Resilience Act, whose reporting obligations begin **September 2026**: an Open
Source Software Steward (Art 24) carries statutory duties — a cybersecurity policy, vulnerability
handling, cooperation with market surveillance — and the CRA introduces an **SBOM** obligation.
Also publicly checkable.

═══════════════════════════════════════════════════════════════════════════════
WHAT THIS MEASURES, AND WHAT IT REFUSES TO SAY
═══════════════════════════════════════════════════════════════════════════════
It measures **PRESENCE of a publicly-required artefact**, anchored to a named provision.

It NEVER says "compliant" or "non-compliant". Presence is not adequacy: a training-data summary
can exist and be worthless, and judging its sufficiency is exactly the adjudication we refuse.
The honest output is *"the artefact required by Art 53(1)(d) is PRESENT / ABSENT / UNMEASURED"*,
and a reader draws their own conclusion.

Nor does it decide whether a given release IS a GPAI model, or whether the provider is a
Steward. Those are legal classifications. The subject declares its own scope, or the row is
UNMEASURED — same discipline as the drift registry's self-declared exposure.

    python3 ossbench.py --selftest
    python3 ossbench.py --models Qwen/Qwen2.5-0.5B-Instruct microsoft/phi-4
"""
from __future__ import annotations

import json, os, re, sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent

PRESENT, ABSENT, UNMEASURED = "present", "absent", "unmeasured"

# ── The checks. Each anchors to a provision that survives the open-source exemption. ────────
CHECKS = [
    ("copyright_policy", "EU AI Act Art 53(1)(c)",
     "A policy to comply with EU copyright law. NOT waived by the open-source exemption — it "
     "applies to every GPAI provider throughout each model's lifecycle.",
     re.compile(r"\b(copyright polic\w+|text and data mining|tdm\b|opt.?out|rights? reserv\w+|"
                r"article 4\(3\)|dsm directive)\b", re.I)),
    ("training_data_summary", "EU AI Act Art 53(1)(d)",
     "A sufficiently detailed public summary of training content, per the AI Office template. "
     "NOT waived by the open-source exemption.",
     re.compile(r"\b(training data|training corpus|trained on|data sources?|dataset[s]? used|"
                r"pre.?training data|data mixture)\b", re.I)),
    ("sbom", "Cyber Resilience Act (SBOM)",
     "A software bill of materials — a formal record of components and supply-chain "
     "relationships. CRA reporting obligations begin September 2026.",
     re.compile(r"\b(sbom|software bill of materials|cyclonedx|spdx)\b", re.I)),
    ("vuln_policy", "CRA Art 24 (Open Source Steward)",
     "A cybersecurity/vulnerability-handling policy. A Steward's duties are lighter than a "
     "Manufacturer's but are statutory.",
     re.compile(r"\b(security polic\w+|vulnerability (report|disclosure|handling)|SECURITY\.md|"
                r"responsible disclosure|report a vulnerability)\b", re.I)),
    ("release_signed", "OpenSSF Model Signing / continuity axis",
     "Is the release cryptographically signed? Unsigned artefacts cannot be attested, and the "
     "continuity axis cannot score a chain that does not exist.",
     re.compile(r"\b(sigstore|cosign|model.?signing|gpg signature|signed release|"
                r"minisign|\.sig\b)\b", re.I)),
]


def evaluate(text: str | None) -> dict:
    """Score one subject's public surface. `None` means we could not read it — UNMEASURED,
    never ABSENT. 'We could not look' and 'it is not there' are different facts, and conflating
    them would let a network failure read as a finding about the provider."""
    out = {}
    for key, provision, why, rx in CHECKS:
        if text is None:
            out[key] = {"status": UNMEASURED, "provision": provision,
                        "reason": "public surface unreadable — not a finding about the subject"}
            continue
        m = rx.search(text)
        out[key] = {"status": PRESENT if m else ABSENT, "provision": provision,
                    "evidence": (text[max(0, m.start() - 60):m.end() + 60].replace("\n", " ")
                                 if m else None),
                    "means": ("an artefact matching this obligation is publicly present"
                              if m else "no such artefact found on the public surface")}
    return out


def fetch_card(model_id: str) -> str | None:
    """The subject's own public model card. Read-only, public, no auth required."""
    try:
        from huggingface_hub import ModelCard
        return ModelCard.load(model_id).content
    except Exception:
        return None


def audit(model_ids: list[str]) -> dict:
    rows = []
    for mid in model_ids:
        card = fetch_card(mid)
        res = evaluate(card)
        rows.append({"subject": mid, "surface": "huggingface model card",
                     "readable": card is not None,
                     "checks": res})
    # Per-check tallies. Denominator is what was MEASURABLE, never the request count.
    tally = {}
    for key, provision, why, _ in CHECKS:
        meas = [r for r in rows if r["checks"][key]["status"] != UNMEASURED]
        tally[key] = {"provision": provision, "why_it_survives_the_exemption": why,
                      "present": sum(1 for r in meas if r["checks"][key]["status"] == PRESENT),
                      "of_measured": len(meas),
                      "unmeasured": len(rows) - len(meas)}
    return {"benchmark": "SOV-OSS", "generated": datetime.now(timezone.utc).isoformat(),
            "subjects": len(rows), "rows": rows, "per_check": tally,
            "scope": ("Measures PRESENCE of publicly-required artefacts against named "
                      "provisions. Presence is not adequacy and this is not a compliance "
                      "verdict — a summary can exist and be worthless, and judging its "
                      "sufficiency is adjudication, which we refuse."),
            "not_determined": ("Whether a subject IS a GPAI model, or its provider IS an Open "
                               "Source Steward, are legal classifications this does not make."),
            "composite_score": "REFUSED BY DESIGN — per-provision only, never merged"}


def main() -> int:
    ids = sys.argv[sys.argv.index("--models") + 1:] if "--models" in sys.argv else [
        "Qwen/Qwen2.5-0.5B-Instruct", "meta-llama/Llama-3.1-8B-Instruct",
        "mistralai/Mistral-7B-Instruct-v0.3", "google/gemma-2-9b-it",
        "microsoft/Phi-3.5-mini-instruct", "tiiuae/falcon-mamba-7b-instruct",
    ]
    d = audit(ids)
    print("  SOV-OSS — do public AI releases carry what the exemption does NOT waive?\n")
    hdr = f"    {'subject':<42}" + "".join(f"{k[:11]:>13}" for k, *_ in CHECKS)
    print(hdr); print("    " + "-" * (len(hdr) - 4))
    for r in d["rows"]:
        line = f"    {r['subject'][:42]:<42}"
        for key, *_ in CHECKS:
            st = r["checks"][key]["status"]
            label = "PRESENT" if st == PRESENT else ("—" if st == ABSENT else "UNMEAS")
            line += f"{label:>13}"
        print(line)
    print("\n    PER PROVISION — denominator is what was measurable\n")
    for key, t in d["per_check"].items():
        un = f"  ({t['unmeasured']} unmeasured)" if t["unmeasured"] else ""
        print(f"      {key:<22} {t['present']}/{t['of_measured']} present{un}")
        print(f"      {'':<22} {t['provision']}")
    print(f"\n    {d['scope']}")
    p = HERE / "benchmark-results" / "ossbench.json"
    try:
        from anchored_write import write_result
        p = write_result("ossbench.json", d)
    except Exception:
        p.write_text(json.dumps(d, indent=2))
    print(f"\n    -> {p}")
    return 0


def selftest() -> int:
    fails = []
    # UNMEASURED when the surface cannot be read — never ABSENT.
    r = evaluate(None)
    if any(v["status"] != UNMEASURED for v in r.values()):
        fails.append("unreadable surface did not yield UNMEASURED across the board")

    # A card carrying the artefacts must read PRESENT.
    good = ("## Training data\nTrained on a mixture of public datasets.\n"
            "## Copyright policy\nWe respect TDM opt-out under the DSM Directive.\n"
            "SBOM: CycloneDX attached. SECURITY.md documents responsible disclosure.\n"
            "Releases are signed with Sigstore/cosign.")
    r = evaluate(good)
    for k in ("copyright_policy", "training_data_summary", "sbom", "vuln_policy", "release_signed"):
        if r[k]["status"] != PRESENT:
            fails.append(f"{k} not PRESENT on a card that plainly carries it")

    # An empty card must read ABSENT, not UNMEASURED — we looked and it was not there.
    r = evaluate("# A model\nIt does things.")
    if r["sbom"]["status"] != ABSENT:
        fails.append("missing artefact on a readable card did not read ABSENT")
    if r["training_data_summary"]["status"] != ABSENT:
        fails.append("absent training summary misread")

    # PRESENT must carry its evidence, or the row is unverifiable.
    r = evaluate(good)
    if not r["sbom"].get("evidence"):
        fails.append("PRESENT carries no evidence snippet")

    # No composite score may exist.
    d = audit([])
    if not str(d.get("composite_score", "")).startswith("REFUSED"):
        fails.append("a composite score was emitted")
    for f in fails: print(f"  ❌ {f}")
    print(f"  {'✅ selftest 10/10' if not fails else f'❌ {len(fails)} failure(s)'}")
    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(selftest() if "--selftest" in sys.argv else main())
