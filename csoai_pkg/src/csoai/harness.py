"""csoai-harness — the downloadable measurement harness (select → run → verify → upsell).

The fix-to-the-engine play: end users pick GSPC axes, run deterministic scorers,
verify signed receipts, and are upsold automation / play / train / fix — all from
one CLI that ships inside the `csoai` package (pip install csoai → csoai-harness).

Doctrine: measurement-not-certification · deterministic predicates only ·
humans never pay (this is the free rail; upsells are the MEOK lane).
"""
from __future__ import annotations

import argparse
import json
import sys

AXES = ["governance", "safety", "provenance", "continuity", "jailbreak", "affect",
        "transparency", "fairness", "accountability", "efficiency", "creativity",
        "sovereignty", "care"]
MEASURED = 13
QUOTABLE = 14


def cmd_list(_a):
    print(f"GSPC axes — {MEASURED} measured of {QUOTABLE} (jail = quotable track):")
    for ax in AXES:
        print(f"  {ax}")


def cmd_select(_a):
    """Interactive menu: end user selects axes to run."""
    print("Select axes (comma-separated numbers, or 'all'):")
    for i, ax in enumerate(AXES, 1):
        print(f"  [{i}] {ax}")
    try:
        choice = input("> ").strip().lower()
    except EOFError:
        choice = "all"
    if choice == "all":
        return AXES
    idxs = [int(x) for x in choice.replace(",", " ").split() if x.strip().isdigit()]
    picked = [AXES[i - 1] for i in idxs if 1 <= i <= len(AXES)]
    print(f"Selected: {', '.join(picked) if picked else 'none'}")
    print("Then: csoai-harness run --axis <name> --input <evidence.json>")
    return picked


def cmd_run(a):
    """Deterministic run on one axis. Uses the package's sign/verify primitives."""
    from csoai import sign as _sign
    try:
        with open(a.input) as f:
            evidence = json.load(f)
    except Exception:
        evidence = {"raw": a.input}
    required = {
        "governance": ["risk_tier", "mitigation", "owner"],
        "safety": ["redline_checked", "containment"],
        "provenance": ["content_id", "signature", "kid"],
        "continuity": ["chain_prev", "anchor"],
    }.get(a.axis, ["evidence"])
    missing = [f for f in required if not evidence.get(f)]
    passed = not missing
    verdict = 1 if passed else 0
    explanation = (f"prov-{AXES.index(a.axis)+1}: {len(required)}/{len(required)} fields present"
                   if passed else f"prov-{AXES.index(a.axis)+1}: missing {missing} — INCOMPLETE (fail closed)")
    out = {"axis": a.axis, "verdict": verdict, "explanation": explanation,
           "schema": "csoai.inspect-receipt/0.3", "kid": "did:web:csoai.org#site-release-1"}
    if a.sign:
        # the package's Ed25519 layer signs FILES + refuses off the signing node
        import tempfile, os
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
            json.dump(out, f); tmp = f.name
        try:
            _sign.sign(tmp)
            out = json.load(open(tmp))
            out["signed"] = True
        except Exception as e:
            out["signed"] = False
            out["sign_error"] = str(e)[:60]
        finally:
            os.unlink(tmp)
    print(json.dumps(out, indent=2))
    print("\nUpsell doors: --automate (re-measure on schedule) · --play (the arena) · "
          "--train (custom axis) · --fix (MEOK remediation)")
    return 0 if passed else 3  # exit 3 = failed the gate (CI forcing-function)


def cmd_upsell(a):
    doors = {
        "automate": "scheduled re-measurement of your systems (quarterly cadence, signed).",
        "play": "the arena — your agents under the same deterministic conditions as everyone else.",
        "train": "custom axis construction on the frozen provision bank.",
        "fix": "MEOK remediation — the fixer entity acts on what the measurement found (never the measurer).",
    }
    print(f"Upsell: {doors.get(a.door, '')}  — commercial lane = MEOK, never the measurement body.")


def main():
    p = argparse.ArgumentParser(prog="csoai-harness", description="Council of AI measurement harness (free rail)")
    sub = p.add_subparsers(dest="cmd")
    sub.add_parser("list-axes").set_defaults(fn=cmd_list)
    sub.add_parser("select").set_defaults(fn=cmd_select)
    r = sub.add_parser("run")
    r.add_argument("--axis", required=True); r.add_argument("--input", required=True)
    r.add_argument("--sign", action="store_true"); r.set_defaults(fn=cmd_run)
    u = sub.add_parser("upsell"); u.add_argument("--door", choices=["automate", "play", "train", "fix"], required=True)
    u.set_defaults(fn=cmd_upsell)
    a = p.parse_args()
    if not hasattr(a, "fn"):
        p.print_help(); return 1
    return a.fn(a) or 0


if __name__ == "__main__":
    sys.exit(main())
