#!/usr/bin/env python3
"""oscal_export.py — map a signed CSOAI measurement card to an OSCAL
assessment-results skeleton (NIST OSCAL assessment-results model v1.x).

Why: FedRAMP's OSCAL mandate lands September 2026 — US federal tooling ingests
OSCAL, not bespoke JSON. A signed card becomes an OSCAL `result` with the
measurement rows as `observations`, so the estate's cards pipe directly into
the federal assessment toolchain.

Honest scope: this emits an OSCAL *skeleton* (valid shape, our namespaces for
the CSOAI-specific props). It is a measurement export, not an authorization
artifact; an assessor still owns the assessment. The signed card travels by
reference (content_id + public verify URL), so the OSCAL consumer can
re-verify the source measurement without trusting us.

Usage:
    python3 oscal_export.py card.json > assessment-results.json
"""
import json
import sys
import uuid
from datetime import datetime, timezone

OSCAL_VERSION = "1.1.3"
VERIFY_BASE = "https://csoai.org/verify"


def card_to_oscal(card: dict) -> dict:
    cid = card.get("content_id", "")
    body = card.get("body", {})
    board = body.get("board", {})
    now = datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")

    observations = []
    per_model = board.get("per_model") or board.get("crosslab_results") or {}
    for subject, res in per_model.items():
        if not isinstance(res, dict):
            continue
        props = [{"name": k, "value": str(v), "ns": "https://csoai.org/ns/gspc"}
                 for k, v in res.items() if not isinstance(v, (dict, list))]
        observations.append({
            "uuid": str(uuid.uuid5(uuid.NAMESPACE_URL, f"csoai:{cid}:{subject}")),
            "title": f"Measurement: {subject}",
            "description": f"Axis: {board.get('axis', body.get('axes', ['?']))}. "
                           f"Benchmark: {board.get('benchmark', body.get('bank_version', '?'))}.",
            "methods": ["TEST"],
            "subjects": [{"type": "component", "title": subject}],
            "props": props,
            "remarks": board.get("honest_note", ""),
        })

    return {
        "assessment-results": {
            "uuid": str(uuid.uuid5(uuid.NAMESPACE_URL, f"csoai:ar:{cid}")),
            "metadata": {
                "title": f"CSOAI measurement export — {board.get('axis', 'gspc')}",
                "last-modified": now,
                "version": "1.0",
                "oscal-version": OSCAL_VERSION,
                "props": [
                    {"name": "claim-type", "value": "measurement-credential-not-certification",
                     "ns": "https://csoai.org/ns/gspc"},
                    {"name": "source-card-content-id", "value": cid,
                     "ns": "https://csoai.org/ns/gspc"},
                    {"name": "source-card-verify", "value": VERIFY_BASE,
                     "ns": "https://csoai.org/ns/gspc"},
                    {"name": "source-card-signer", "value": card.get("signer", ""),
                     "ns": "https://csoai.org/ns/gspc"},
                ],
            },
            "results": [{
                "uuid": str(uuid.uuid5(uuid.NAMESPACE_URL, f"csoai:result:{cid}")),
                "title": board.get("benchmark", "CSOAI measurement"),
                "description": board.get("headline_finding", ""),
                "start": now,
                "end": now,
                "observations": observations,
            }],
        }
    }


if __name__ == "__main__":
    card = json.load(open(sys.argv[1]))
    json.dump(card_to_oscal(card), sys.stdout, indent=2)
    sys.stdout.write("\n")
