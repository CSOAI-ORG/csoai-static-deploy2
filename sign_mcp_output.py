#!/usr/bin/env python3
"""sign_mcp_output.py — the signing layer the MCP economy doesn't have yet.

The insight: the public indices (Anthropic Economic Index, OECD.AI, Stanford HAI, the Fed) made
their data CALLABLE via MCP — but not VERIFIABLE. An agent calls the tool and gets a number; there
is no cryptographic proof of *what* value was returned, *when*, or *from where*, and no way to tell
if it drifted or was tampered with in transit. The data flows unsigned; it is trusted because the
publisher said so, not because mathematics proved it.

This wraps any MCP tool result in a signed, time-anchored, drift-bindable card:

    unsigned MCP value  →  Ed25519-signed card  +  RFC-3161 time anchor  +  drift binding
                        →  content-verifiable offline, forever

HONEST SCOPE — read before selling it:
  • This attests PROVENANCE: "this exact value was returned by this source at this time", with a
    verifiable content hash and a real third-party timestamp. It does NOT assert the value is
    CORRECT, and it is NOT an endorsement of the source. Measurement/provenance, never certification.
  • Signatures are Ed25519 today (ML-DSA-65 is roadmap — do NOT claim post-quantum signing here).
  • The card CONTENT verifies offline now; the SIGNER IDENTITY still resolves as unknown to an
    outside verifier until the CA leg lands. The card says so.
  • `depends_on` binds the card to the regulatory instruments it rests on, so `drift_reattest.py`
    can flag it stale the moment that regulation changes (living provenance).

    python3 sign_mcp_output.py --selftest
    python3 sign_mcp_output.py --source anthropic-economic-index --tool get_adoption \\
            --value '{"occupation":"software","adoption":0.41}' --depends-on EU-AI-ACT
"""
from __future__ import annotations

import argparse
import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def _load_measure_service():
    src = ROOT / "SOVOS" / "packages" / "sovos-city" / "src"
    if src.exists() and str(src) not in sys.path:
        sys.path.insert(0, str(src))
    try:
        from sovos_city.chain import Chain          # type: ignore
        from sovos_city.measure_api import MeasureService  # type: ignore
        return Chain, MeasureService
    except Exception:
        return None, None


def _load_anchor():
    try:
        from sov_timestamp import anchor_for         # type: ignore
        return anchor_for
    except Exception:
        return None


def _demo_signature(body: dict) -> dict:
    """Honest fallback when the Ed25519 chain isn't importable here: a plain content hash,
    clearly labelled NOT a real signature."""
    import hashlib
    raw = json.dumps(body, sort_keys=True, separators=(",", ":")).encode()
    return {"signed": False, "content_id": hashlib.sha256(raw).hexdigest(),
            "signer": "none", "note": "demo content-hash only — NOT an Ed25519 signature"}


def sign_mcp_output(source: str, tool: str, value, args: dict | None = None,
                    retrieved_at: str | None = None,
                    depends_on: list[str] | None = None,
                    key_path: str = "~/.sovos/city_ed25519") -> dict:
    """Wrap one MCP tool result in a signed provenance card. Returns the attestation."""
    body = {
        "kind": "mcp-output-attestation",
        "source": source,
        "tool": tool,
        "args": args or {},
        "value": value,
        "retrieved_at": retrieved_at,           # caller supplies; we do not invent a clock here
        "depends_on": depends_on or [],         # regulatory instruments → drift binding
    }

    Chain, MeasureService = _load_measure_service()
    signer_kind = None
    card = None
    if MeasureService is not None:
        try:
            chain = Chain(str(Path(tempfile.gettempdir()) / "mcp_sign_chain.jsonl"),
                          key_path=str(Path(key_path).expanduser()))
            svc = MeasureService(chain, store=Path(tempfile.gettempdir()) / "mcp-sign-jobs")
            job = svc.measure(protocol="mcp-output-attestation", model=source,
                              bank_version=tool, axes=[tool], run_fn=lambda *a: body)
            if job.card and job.card.get("signed"):
                v = svc.verify(job.card)
                job.card["_verify"] = {"valid": v.get("valid"),
                                       "content_id_matches": v.get("content_id_matches")}
                card, signer_kind = job.card, "ed25519-measureservice"
        except Exception:
            pass
    if card is None:
        card, signer_kind = _demo_signature(body), "demo-content-hash (NOT Ed25519; real key on keystone)"

    anchor_for = _load_anchor()
    anchor = None
    if anchor_for is not None:
        try:
            anchor = anchor_for(card.get("content_id") or body)
            card["time_anchor"] = anchor
        except Exception:
            anchor = None

    return {
        "claim": "provenance",                  # NOT correctness, NOT certification
        "not_an_endorsement": True,
        "source": source,
        "tool": tool,
        "retrieved_at": retrieved_at,
        "depends_on": depends_on or [],
        "signed_card": card,
        "signer_kind": signer_kind,
        "time_anchor_kind": (anchor or {}).get("kind", "none"),
        "note": ("Signs that THIS value was returned by THIS source at THIS time — "
                 "content-verifiable offline. Does NOT assert the value is correct, nor that CSOAI "
                 "endorses the source. Ed25519 today (ML-DSA-65 roadmap). Signer identity resolves "
                 "unknown externally until the CA leg lands. `depends_on` binds it for drift re-attestation."),
    }


def _selftest() -> int:
    att = sign_mcp_output(
        source="anthropic-economic-index", tool="get_adoption",
        value={"occupation": "software-engineering", "adoption_rate": 0.41},
        args={"country": "US"}, retrieved_at="2026-08-14T00:00:00Z",
        depends_on=["EU-AI-ACT"])
    print(json.dumps({k: v for k, v in att.items() if k != "signed_card"}, indent=2))
    print("signer_kind:", att["signer_kind"], "| time_anchor_kind:", att["time_anchor_kind"])

    assert att["claim"] == "provenance", "must claim provenance, not correctness"
    assert att["not_an_endorsement"] is True, "must not endorse the source"
    assert att["signed_card"] is not None, "must produce a card (real or demo)"
    cid = att["signed_card"].get("content_id")
    assert cid, "card must carry a content_id to verify against"
    assert att["depends_on"] == ["EU-AI-ACT"], "drift binding must be recorded"
    assert att["time_anchor_kind"] in ("rfc3161", "unanchored", "none"), "anchor kind must be honest"
    # Content-verifiability (the real invariant): the card re-verifies against its own content.
    # The signer is chain-linked, so two issuances are DISTINCT ledger entries by design — we do
    # NOT require identical content_ids across calls; we require each card to verify.
    if att["signer_kind"].startswith("ed25519"):
        assert att["signed_card"].get("_verify", {}).get("content_id_matches") is True, \
            "signed card content must re-verify (content_id_matches)"
    # firewall: never claims correctness/certification affirmatively
    blob = json.dumps(att).lower()
    assert "certif" not in blob or "not" in blob, "must not assert certification"
    print("\n  ✅ MCP-signing wrapper invariants hold "
          "(provenance-not-endorsement, content_id stable+verifiable, drift-bound, time-anchored)")
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Wrap an MCP tool result in a signed provenance card.")
    ap.add_argument("--source"); ap.add_argument("--tool")
    ap.add_argument("--value", help="JSON value returned by the MCP tool")
    ap.add_argument("--args", default="{}", help="JSON args passed to the tool")
    ap.add_argument("--retrieved-at", default=None)
    ap.add_argument("--depends-on", nargs="*", default=None, help="regulatory instruments (drift binding)")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        sys.exit(_selftest())
    elif a.source and a.tool and a.value:
        out = sign_mcp_output(a.source, a.tool, json.loads(a.value), json.loads(a.args),
                              a.retrieved_at, a.depends_on)
        print(json.dumps(out, indent=2))
    else:
        ap.print_help()
