"""csoai — the boring CLI. Universal agent rail + CI forcing-function + atom-emitter
+ the first agent-callable signed-record verifier.

    csoai check  --entity <hf-repo> --pack art50 [--sign] [--json]
    csoai verify --record <file.json>

Deterministic output + exit codes so an agent (or a CI gate) acts on the result
without reasoning about the statute from memory. Guardrails: PUBLIC artifacts only
(hiQ/Van Buren); measurement, not certification; signed only with a real key.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from csoai import council_signal

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
    except Exception as e:  # noqa: BLE001
        print(f"FETCH FAILED for {a.entity}: {e}. No card emitted (never fabricated).", file=sys.stderr)
        return 2
    rec["pack"] = a.pack
    missing = [k for k in pack["required"] if not rec["predicates"].get(k)]
    rec["pack_result"] = {"pack": a.pack, "required": pack["required"], "missing": missing, "pass": not missing}
    if a.sign:
        out = a.out or f"csoai_check_{a.entity.replace('/', '_')}.json"
        rec = council_signal.sign_record(rec, out)
    if a.json:
        print(json.dumps(rec, indent=2))
    else:
        print(f"  {a.entity}  pack={a.pack}  pass={rec['pack_result']['pass']}"
              f"  missing={missing or 'none'}  signed={rec.get('signed', bool(a.sign))}")
    return 0 if not missing else 3


def cmd_verify(a) -> int:
    from csoai import sign
    obj = json.loads(Path(a.record).read_text())
    s = obj.get("signature")
    if not s or s.get("kind") != "ed25519":
        print("UNSIGNED — no Ed25519 signature on this record.")
        return 1
    try:
        sign.verify(a.record)
        return 0
    except SystemExit as e:
        return int(e.code) if isinstance(e.code, int) else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="csoai", description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check", help="measure a public artifact → signed card")
    c.add_argument("--entity", required=True)
    c.add_argument("--pack", default="art50", help=f"one of: {', '.join(PACKS)}")
    c.add_argument("--sign", action="store_true")
    c.add_argument("--json", action="store_true")
    c.add_argument("--out")
    c.set_defaults(fn=cmd_check)
    v = sub.add_parser("verify", help="verify a signed record offline")
    v.add_argument("--record", required=True)
    v.set_defaults(fn=cmd_verify)
    a = ap.parse_args(argv)
    return a.fn(a)


if __name__ == "__main__":
    raise SystemExit(main())
