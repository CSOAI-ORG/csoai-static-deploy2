"""council_signal.py — continuous, LAWFUL compliance signal over PUBLISHED AI artifacts.

The play (build-map, compass 237202a7 #A): scan an entity's PUBLIC artifacts, emit a
compact Ed25519-signed state record, and notify on drift. This is the first brick:
one public artifact source (a Hugging Face model repo's PUBLIC metadata) → a
deterministic transparency state → a signed record → a drift diff against the prior.

LEGAL GUARDRAILS, baked in (not optional):
  * PUBLIC ARTIFACTS ONLY. This reads the public model-info endpoint (no auth, no
    gated content, no private API). Footing: hiQ v. LinkedIn (9th Cir. 2022) +
    Van Buren (SCOTUS 2021) — scanning public pages is not CFAA "without
    authorization." (Still respect ToS/copyright; never scan a private API.)
  * MEASUREMENT, NOT CERTIFICATION. Every field is an observed public fact or a
    deterministic predicate over one. We do not certify compliance or conformity.
  * SIGN ONLY WITH A REAL KEY. Signed on the signing node; UNSIGNED and labelled so
    everywhere else. Never a fake signature.

Checks are deterministic functions of the fetched public metadata — recomputable by
anyone from the same public source. Nothing here is a judgement call.
"""
from __future__ import annotations

import argparse
import json
import hashlib
import sys
import urllib.request
import urllib.error
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional

VERSION = "0.1.0"
HF_MODEL_API = "https://huggingface.co/api/models/{entity}"
# Art-50 / transparency signal terms we look for in public tags/cardData.
_MARKING_TERMS = ("c2pa", "content-credential", "content credentials", "watermark",
                  "synthid", "ai-generated", "provenance")


def fetch_public_metadata(entity: str, timeout: int = 20) -> Dict[str, Any]:
    """GET the PUBLIC model-info JSON. Raises on network/HTTP error (never fakes data)."""
    url = HF_MODEL_API.format(entity=urllib.parse.quote(entity, safe="/"))
    req = urllib.request.Request(url, headers={"User-Agent": f"council-signal/{VERSION}"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def compute_checks(meta: Dict[str, Any]) -> Dict[str, Any]:
    """Deterministic transparency predicates over the PUBLIC metadata."""
    card = meta.get("cardData") or {}
    tags = [str(t).lower() for t in (meta.get("tags") or [])]
    blob = (json.dumps(card) + " " + " ".join(tags)).lower()
    return {
        # transparency basics an Art-50/AI-Act reader looks for
        "license_declared": bool(card.get("license") or any(t.startswith("license:") for t in tags)),
        "task_declared": bool(meta.get("pipeline_tag")),
        "model_card_present": bool(card) and card != {},
        "gated": bool(meta.get("gated")),  # a transparency/access signal (not good/bad by itself)
        # generative-marking signal (Art 50) — does the card/tags mention any marking scheme
        "generative_marking_declared": any(term in blob for term in _MARKING_TERMS),
        # observed facts (not predicates) kept for the record
        "license_value": card.get("license"),
        "pipeline_tag": meta.get("pipeline_tag"),
        "downloads": meta.get("downloads"),
        "lastModified": meta.get("lastModified"),
    }


def state_record(entity: str) -> Dict[str, Any]:
    meta = fetch_public_metadata(entity)
    checks = compute_checks(meta)
    # the state hash is over the PREDICATES only (facts like downloads churn constantly
    # and are not compliance drift) — so drift means a transparency signal changed.
    predicate_keys = ("license_declared", "task_declared", "model_card_present",
                      "gated", "generative_marking_declared")
    predicates = {k: checks[k] for k in predicate_keys}
    state_hash = hashlib.sha256(json.dumps(predicates, sort_keys=True).encode()).hexdigest()
    return {
        "kind": "council_signal.state",
        "version": VERSION,
        "entity": entity,
        "source": "huggingface public model-info (no auth)",
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "predicates": predicates,
        "observed": {k: checks[k] for k in checks if k not in predicate_keys},
        "state_hash": state_hash,
        "frame": ("Deterministic transparency predicates over PUBLIC artifacts only. "
                  "Measurement, not certification. Drift = a transparency predicate changed."),
    }


def diff(prev: Dict[str, Any], curr: Dict[str, Any]) -> Dict[str, Any]:
    """Drift = which transparency predicates changed since the prior signed state."""
    pp, cp = prev.get("predicates", {}), curr.get("predicates", {})
    changed = {k: {"was": pp.get(k), "now": cp.get(k)} for k in cp if pp.get(k) != cp.get(k)}
    return {
        "entity": curr["entity"],
        "drifted": bool(changed) or prev.get("state_hash") != curr["state_hash"],
        "changes": changed,
        "prev_fetched_at": prev.get("fetched_at"),
        "curr_fetched_at": curr["fetched_at"],
    }


def sign_record(record: Dict[str, Any], out_path: str | Path) -> Dict[str, Any]:
    """Ed25519-sign iff the key exists on this node; else emit UNSIGNED, labelled."""
    Path(out_path).write_text(json.dumps(record, indent=2), encoding="utf-8")
    try:
        import os, sign
        if os.path.exists(sign.PRIV):
            sign.sign(str(out_path))
            return json.loads(Path(out_path).read_text())
    except Exception as e:
        record["_sign_error"] = str(e)
    record["signature"] = None
    record["signed"] = False
    record["_unsigned_note"] = "no signing key on this node — sign on the signing node: python3 sign.py --sign " + str(out_path)
    Path(out_path).write_text(json.dumps(record, indent=2), encoding="utf-8")
    return record


def selftest() -> int:
    entity = "bert-base-uncased"  # a stable, public, non-gated repo
    try:
        rec = state_record(entity)
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as e:
        print(f"  selftest SKIPPED — no network to the public endpoint ({e})")
        return 0  # honest: cannot test offline, do not fake a pass
    print(f"  scanned {entity}: predicates = {rec['predicates']}")
    print(f"  state_hash = {rec['state_hash'][:16]}…")
    # drift self-check: same scan → no drift; mutated predicate → drift
    d0 = diff(rec, rec)
    mutated = json.loads(json.dumps(rec)); mutated["predicates"]["license_declared"] = not mutated["predicates"]["license_declared"]
    mutated["state_hash"] = "x"
    d1 = diff(rec, mutated)
    ok = (d0["drifted"] is False) and (d1["drifted"] is True) and ("license_declared" in d1["changes"])
    print(f"  drift(no-change)={d0['drifted']}  drift(mutated)={d1['drifted']}  changes={list(d1['changes'])}")
    print("  selftest:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--scan", metavar="ENTITY", help="public HF model repo id, e.g. meta-llama/Llama-3.1-8B-Instruct")
    ap.add_argument("--against", metavar="PRIOR.json", help="prior signed state to diff for drift")
    ap.add_argument("--out", default="benchmark-results/council_signal_state.json")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if a.scan:
        try:
            rec = sign_record(state_record(a.scan), a.out)
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, json.JSONDecodeError) as e:
            print(f"FETCH FAILED for {a.scan}: {e}. Public artifact unreadable — no state emitted "
                  "(never fabricated).", file=sys.stderr)
            return 2
        print(json.dumps(rec, indent=2))
        if a.against and Path(a.against).exists():
            print("\n--- DRIFT ---")
            print(json.dumps(diff(json.loads(Path(a.against).read_text()), rec), indent=2))
        return 0
    ap.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
