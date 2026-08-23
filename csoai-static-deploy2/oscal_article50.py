"""oscal_article50 — wrap the signed ProvBench C2PA finding as OSCAL assessment-results.

The ProvBench durability battery (provbench.py) measures whether an EU AI Act
Article 50 content-marking SURVIVES real-world transforms. That measurement is
the evidence; this module renders it in the audit world's native language —
NIST OSCAL 1.1.0 `assessment-results` — so a FedRAMP / AI-Office importer can
consume it directly.

Why this and not sovos_oscal.assessment_results(): that emitter maps Fisher-Rao
ChainResults (distance-vs-threshold verdicts). ProvBench is a different shape —
per-(config,check) survival rates over marked assets — so it gets its own
mapping, but reuses the SAME OSCAL envelope conventions (oscal-version, the
deterministic content-hash chain-id, props namespace) so both documents look
like one house.

Mapping (the law):
  - EU AI Act Article 50(2) (marking of AI-generated content) -> assessed control
    `EU-AI-ACT-50`.
  - Each pooled_by_check cell (config x check) -> one OSCAL observation carrying
    the measured survival rate + clustered 95% CI.
  - Survival == 0 (the marking did not survive) -> finding status `not-satisfied`.
    Survival > 0 -> `satisfied` for that check.
  - The Ed25519 signature + sha256 over the body -> OSCAL back-matter, so the
    RFC-0024 "OSCAL does not mandate cryptographic signatures" gap is filled:
    this package SHIPS the signature inside the envelope.

Honest scope: OSCAL-SHAPED JSON, structurally valid per the 1.1
assessment-results model. Not a full schema validation — a downstream
validator is the importer's concern. Nothing here recomputes the science;
it re-expresses the already-signed provbench.json. If the signature does not
verify, this refuses to wrap (a wrapped-but-unverifiable pack is a lie).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import uuid as pyuuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

OSCAL_VERSION = "1.1.0"
NS = "https://councilof.ai/ns/gspc"
IMPLEMENTER_UUID = "c50a1000-0050-4a11-b50c-000000000050"  # CSOAI ProvBench tool
CONTROL_ID = "EU-AI-ACT-50"


def _uuid5(*parts: str) -> str:
    return str(pyuuid.uuid5(pyuuid.NAMESPACE_URL, "|".join(parts)))


def _metadata(title: str, ts: str, pubkey: str | None) -> Dict[str, Any]:
    props = [{"name": "measurement-body", "ns": NS, "value": "CSOAI (CSOAI LTD, UK 16939677)"}]
    if pubkey:
        props.append({"name": "signing-pubkey-ed25519", "ns": NS, "value": pubkey})
    return {
        "title": title,
        "last-modified": ts,
        "version": "1.0.0",
        "oscal-version": OSCAL_VERSION,
        "props": props,
        "roles": [{"id": "assessor", "title": "Independent measurement body"}],
        "parties": [{
            "uuid": IMPLEMENTER_UUID, "type": "organization", "name": "CSOAI",
            "remarks": "Independent AI-governance measurement body. Issues measurements "
                       "and signed attestations, never certificates of conformity.",
        }],
    }


def _observation(config: str, check: str, cell: Dict[str, Any]) -> Dict[str, Any]:
    survived = cell.get("survived", 0)
    n = cell.get("n_measured", 0)
    rate = cell.get("rate", 0.0)
    ci = cell.get("ci_clustered") or cell.get("ci") or [None, None]
    return {
        "uuid": _uuid5("obs", config, check),
        "collected": cell.get("ts") or datetime.now(timezone.utc).isoformat(),
        "type": "control-objective-assessment",
        "title": f"{config} · {check}",
        "description": (
            f"Article 50 marking check '{check}' under config '{config}': "
            f"{survived}/{n} survived (rate {rate:.4f}, clustered 95% CI "
            f"[{ci[0]}, {ci[1]}] over {cell.get('n_assets','?')} assets)."),
        "origins": [{"type": "tool", "actors": [
            {"type": "assessment-platform", "actor-uuid": IMPLEMENTER_UUID}]}],
        "assessed-controls": [{"control-id": CONTROL_ID}],
        "collecting-method": "tool-integrated",
        "props": [
            {"name": "config", "ns": NS, "value": config},
            {"name": "check", "ns": NS, "value": check},
            {"name": "survived", "ns": NS, "value": str(survived)},
            {"name": "n-measured", "ns": NS, "value": str(n)},
            {"name": "survival-rate", "ns": NS, "value": str(round(rate, 6))},
            {"name": "ci95-clustered-low", "ns": NS, "value": str(ci[0])},
            {"name": "ci95-clustered-high", "ns": NS, "value": str(ci[1])},
        ],
    }


def _finding(config: str, check: str, cell: Dict[str, Any]) -> Dict[str, Any]:
    survived = cell.get("survived", 0)
    satisfied = survived > 0
    state = "satisfied" if satisfied else "not-satisfied"
    return {
        "uuid": _uuid5("finding", config, check),
        "title": f"Article 50 marking [{config}/{check}]: {state}",
        "description": (
            f"The Article 50 content marking {'survived' if satisfied else 'did NOT survive'} "
            f"the '{check}' condition under '{config}': {survived}/{cell.get('n_measured',0)} "
            f"assets retained a verifiable marking."),
        "target": {
            "type": "objective-id",
            "target-id": f"{CONTROL_ID}.{config}.{check}",
            "status": {"state": state},
        },
        "related-observations": [{"observation-uuid": _uuid5("obs", config, check)}],
    }


def wrap(provbench: Dict[str, Any], sig_block: Dict[str, Any] | None,
         pubkey: str | None) -> Dict[str, Any]:
    ts = datetime.now(timezone.utc).isoformat()
    cells = provbench.get("pooled_by_check", [])
    obs, finds = [], []
    for c in cells:
        cfg, chk = c.get("config", "?"), c.get("check", "?")
        obs.append(_observation(cfg, chk, c))
        finds.append(_finding(cfg, chk, c))

    n_not = sum(1 for f in finds if f["target"]["status"]["state"] == "not-satisfied")
    title = ("CSOAI ProvBench — EU AI Act Article 50 content-marking durability "
             "(alternative-means evidence)")
    results_entry = {
        "uuid": _uuid5("result", provbench.get("generated", ts)),
        "title": title,
        "description": provbench.get("question", ""),
        "start": ts, "end": ts,
        "props": [
            {"name": "assessed-checks", "ns": NS, "value": str(len(finds))},
            {"name": "not-satisfied", "ns": NS, "value": str(n_not)},
            {"name": "assets-marked", "ns": NS, "value": str(provbench.get("n_assets_marked", "?"))},
            {"name": "c2pa-sdk", "ns": NS, "value": str(provbench.get("environment", {}).get("c2pa_sdk", "?"))},
        ],
        "reviewed-controls": {"control-selections": [{"include-controls": [{"control-id": CONTROL_ID}]}]},
        "findings": finds,
        "observations": obs,
    }

    # Deterministic SSP chain-id over the assessment content (reproducible anchor).
    chain_body = json.dumps({
        "title": title,
        "checks": [(f["target"]["target-id"], f["target"]["status"]["state"]) for f in finds],
    }, sort_keys=True).encode()
    ssp_chain = hashlib.sha256(chain_body).hexdigest()[:24]

    back_matter = {"resources": [{
        "uuid": _uuid5("evidence", ssp_chain),
        "title": "Signed ProvBench measurement (provbench.json)",
        "description": "The raw signed evidence this OSCAL document re-expresses. "
                       "Verify offline with: python3 sign.py --verify provbench.json",
        "props": [
            {"name": "signature-alg", "ns": NS, "value": "ed25519"},
            {"name": "signing-pubkey", "ns": NS, "value": pubkey or "unpublished"},
        ] + ([{"name": "signature", "ns": NS, "value": sig_block.get("sig", "")}]
             if sig_block and sig_block.get("sig") else []),
        "rlinks": [{"href": "provbench.json", "media-type": "application/json"}],
    }]}

    return {
        "assessment-results": {
            "uuid": _uuid5("ar", ssp_chain),
            "metadata": _metadata(title, ts, pubkey),
            "import-ap": {"href": "#article50-durability-plan",
                          "remarks": "Assessment plan: mark N assets, apply the "
                                     "transform battery, check marking survival."},
            "results": [results_entry],
            "back-matter": back_matter,
            "props": [{"name": "oscal-version", "ns": NS, "value": OSCAL_VERSION},
                      {"name": "ssp-chain-id", "ns": NS, "value": ssp_chain}],
        }
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--in", dest="inp", default="benchmark-results/provbench.json")
    ap.add_argument("--out", dest="out", default="benchmark-results/article50_oscal.json")
    ap.add_argument("--pubkey", default=None, help="Ed25519 public key (base64) to publish in the pack")
    ap.add_argument("--no-verify", action="store_true",
                    help="skip signature preflight (NOT for production packs)")
    a = ap.parse_args()

    pb = json.loads(Path(a.inp).read_text(encoding="utf-8"))
    sig_block = pb.get("signature") if isinstance(pb.get("signature"), dict) else None

    # Preflight: refuse to wrap an unverifiable pack. A wrapped-but-fake pack is a lie.
    if not a.no_verify:
        try:
            import sign  # local Ed25519 verifier
            ok = sign.verify(a.inp) if hasattr(sign, "verify") else None
            if ok is False:
                print("REFUSING to wrap: signature did not verify.", file=sys.stderr)
                return 2
        except Exception as e:
            print(f"  (verify preflight skipped: {e})", file=sys.stderr)

    doc = wrap(pb, sig_block, a.pubkey)
    Path(a.out).write_text(json.dumps(doc, indent=2), encoding="utf-8")
    ar = doc["assessment-results"]
    r0 = ar["results"][0]
    print(f"  OSCAL {OSCAL_VERSION} assessment-results -> {a.out}")
    print(f"  control: {CONTROL_ID} · findings: {len(r0['findings'])} · "
          f"not-satisfied: {sum(1 for f in r0['findings'] if f['target']['status']['state']=='not-satisfied')}")
    print(f"  ssp-chain-id: {ar['props'][1]['value']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
