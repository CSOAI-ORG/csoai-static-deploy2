"""csoai_check — the boring CLI. The universal agent rail (shell is every agent's
native capability), the CI forcing-function, and the atom-emitter, in one command.

Per the agent-discovery flywheel (2026-08-13): "boring CLI first" is the highest-
evidence consumption rail (semgrep/trestle pattern); the MCP server wraps THIS.
Deterministic output + exit codes = an agent (or a CI gate) can run it and act on
the result without reasoning about the statute from memory.

Subcommands:
  csoai check  --entity <hf-repo> --pack art50 [--sign] [--json]
      → measure a PUBLIC artifact's transparency state, emit a signed card.
        Exit 0 = scanned & compliant-shaped; 3 = a transparency predicate MISSING
        (the CI gate fails the build on 3); 2 = could not fetch (never fabricates).
  csoai verify --record <file.json>
      → the FIRST agent-callable signed-record verifier (open lane: no Rekor/
        transparency-log MCP/CLI verifier exists today). Verifies Ed25519 offline.

Guardrails (baked in): PUBLIC artifacts only (hiQ/Van Buren); measurement, not
certification; signed only with a real key, else UNSIGNED and labelled. Public
naming only.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import council_signal  # reuse the lawful public-artifact scanner + state model


# packs map a public-facing obligation name → the predicates that must hold.
# Extend per axis; art50 is the live obligation (in force 2026-08-02).
PACKS = {
    "art50": {
        "title": "EU AI Act Article 50 transparency (public-artifact signals)",
        "required": ["license_declared", "task_declared", "model_card_present"],
    },
    "transparency": {
        "title": "Baseline transparency",
        "required": ["license_declared", "model_card_present"],
    },
}


def cmd_check(a) -> int:
    pack = PACKS.get(a.pack)
    if not pack:
        print(f"unknown pack '{a.pack}'; known: {', '.join(PACKS)}", file=sys.stderr)
        return 64
    try:
        rec = council_signal.state_record(a.entity)
    except Exception as e:  # noqa: BLE001 — surface any fetch/parse failure honestly
        print(f"FETCH FAILED for {a.entity}: {e}. No card emitted (never fabricated).", file=sys.stderr)
        return 2

    rec["pack"] = a.pack
    missing = [k for k in pack["required"] if not rec["predicates"].get(k)]
    rec["pack_result"] = {"pack": a.pack, "required": pack["required"],
                          "missing": missing, "pass": not missing}

    if a.sign:
        out = a.out or f"benchmark-results/csoai_check_{a.entity.replace('/', '_')}.json"
        rec = council_signal.sign_record(rec, out)

    if a.json:
        print(json.dumps(rec, indent=2))
    else:
        print(f"  {a.entity}  pack={a.pack}  pass={rec['pack_result']['pass']}"
              f"  missing={missing or 'none'}  signed={rec.get('signed', bool(a.sign))}")
    # exit 3 on a missing transparency predicate → the CI gate fails the build here.
    return 0 if not missing else 3


def cmd_verify(a) -> int:
    try:
        import sign
    except Exception as e:  # noqa: BLE001
        print(f"verifier unavailable: {e}", file=sys.stderr)
        return 70
    obj = json.loads(Path(a.record).read_text())
    s = obj.get("signature")
    if not s or s.get("kind") != "ed25519":
        print("UNSIGNED — this record carries no Ed25519 signature (honest checksum record, or sign it on the signing node).")
        return 1
    # sign.verify() prints VALID/exits on INVALID; run it against the file.
    try:
        sign.verify(a.record)   # prints ✅ VALID or exits non-zero on INVALID
        return 0
    except SystemExit as e:
        return int(e.code) if isinstance(e.code, int) else 1


def main() -> int:
    ap = argparse.ArgumentParser(prog="csoai", description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("check", help="measure a public artifact → signed card")
    c.add_argument("--entity", required=True, help="public HF model repo id")
    c.add_argument("--pack", default="art50", help=f"one of: {', '.join(PACKS)}")
    c.add_argument("--sign", action="store_true", help="Ed25519-sign the card (signing node only)")
    c.add_argument("--json", action="store_true", help="emit the full card as JSON")
    c.add_argument("--out", help="path for the signed card")
    c.set_defaults(fn=cmd_check)

    v = sub.add_parser("verify", help="verify a signed record offline (first agent-callable verifier)")
    v.add_argument("--record", required=True, help="path to a signed card/record JSON")
    v.set_defaults(fn=cmd_verify)

    a = ap.parse_args()
    return a.fn(a)


if __name__ == "__main__":
    raise SystemExit(main())
