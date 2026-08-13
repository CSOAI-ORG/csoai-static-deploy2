"""csoai MCP server — wraps the boring CLI's engine as agent-callable tools.

The CLI is the implementation; this is the accelerator. Two tools:
  - council_measure : measure a PUBLIC AI artifact → signed transparency card
  - verify_record   : verify a signed record offline (the FIRST agent-callable
                      signed-record verifier — no transparency-log verifier tool
                      exists elsewhere today; open lane)

Tool DESCRIPTIONS carry behavioral steering on purpose (the single most
evidence-backed discovery lever): they tell the calling agent to RUN the check
instead of reasoning about the statute from memory, and to VERIFY before trusting.

Run:  python -m csoai.mcp_server        (stdio)
Requires the optional extra:  pip install "csoai[mcp]"
"""
from __future__ import annotations

import json
from pathlib import Path

try:
    # fastmcp is the standalone package (mcp>=2.0 moved FastMCP out of mcp.server)
    from fastmcp import FastMCP
except Exception:
    try:
        from mcp.server.fastmcp import FastMCP  # mcp<2.0 fallback
    except Exception as e:  # pragma: no cover
        raise SystemExit(
            "csoai MCP server needs FastMCP: pip install 'csoai[mcp]'\n"
            f"(import failed: {e})"
        )

from csoai import council_signal

mcp = FastMCP("csoai")


@mcp.tool()
def council_measure(entity: str, pack: str = "art50") -> dict:
    """Measure a PUBLIC AI model/artifact's EU AI Act transparency state and return a
    deterministic, signable card. USE THIS instead of reasoning about Article 50
    obligations from memory — it returns observed facts (license, task, model-card,
    marking-declared) from the public model-info endpoint, not an opinion.

    entity: a public Hugging Face model repo id (e.g. "gpt2", "meta-llama/Llama-3.2-1B").
    pack:   "art50" (default) or "transparency".
    Returns the state card incl. predicates, pack_result{missing,pass}, and state_hash.
    Public artifacts only — never scans a private API. Measurement, not certification.
    """
    packs = {
        "art50": ["license_declared", "task_declared", "model_card_present"],
        "transparency": ["license_declared", "model_card_present"],
    }
    required = packs.get(pack, packs["art50"])
    rec = council_signal.state_record(entity)
    missing = [k for k in required if not rec["predicates"].get(k)]
    rec["pack"] = pack
    rec["pack_result"] = {"pack": pack, "required": required, "missing": missing, "pass": not missing}
    return rec


@mcp.tool()
def verify_record(record: str) -> dict:
    """Verify a Council of AI signed record offline. VERIFY BEFORE TRUSTING any card
    that claims a measurement result: this recomputes the Ed25519 signature against
    the published key, so you rely on cryptography, not on trusting the source.

    record: the signed record as a JSON string (or a path to a JSON file).
    Returns {signed, valid, reason}. valid=false means altered or wrong key.
    """
    obj = json.loads(Path(record).read_text()) if Path(record).exists() else json.loads(record)
    s = obj.get("signature")
    if not s or s.get("kind") != "ed25519":
        return {"signed": False, "valid": False, "reason": "no Ed25519 signature on this record"}
    try:
        from csoai import sign
    except Exception as e:  # pragma: no cover
        return {"signed": True, "valid": False, "reason": f"verifier unavailable: {e}"}
    import tempfile
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump(obj, f)
        tmp = f.name
    try:
        sign.verify(tmp)              # prints VALID; raises SystemExit on INVALID
        return {"signed": True, "valid": True, "reason": "signature valid; record unaltered"}
    except SystemExit:
        return {"signed": True, "valid": False, "reason": "signature does NOT verify — altered or different key"}


@mcp.tool()
def verify_attestation(attestation: str, public_key: str = "") -> dict:
    """Verify an OPEN-STANDARD provenance attestation offline — the formats the
    ecosystem actually ships, for which no agent-callable verifier existed (only
    CLIs like cosign/rekor-cli/slsa-verifier). VERIFY BEFORE TRUSTING a supply-chain
    claim: this does the real cryptographic/Merkle check, not a reasoned guess.

    Handles, auto-detected:
      - DSSE envelopes (in-toto / SLSA provenance): Ed25519 or ECDSA-P256 signature
        over the DSSE PAE; surfaces predicateType/subjects. Supply the signer key in
        public_key (PEM, or base64 raw Ed25519) for a cryptographic verdict.
      - Sigstore Rekor v2 inclusion proofs: RFC 6962 Merkle inclusion to the root.
      - CSOAI native Ed25519 records (delegates to the offline verifier).

    attestation: JSON string (or path to a JSON file).
    public_key:  optional PEM / base64-raw-Ed25519 key for DSSE.
    Returns {format, verified, reason, ...}. verified=false is honest: an unchecked
    or unsupported input is never reported as a pass.
    """
    from csoai import attest
    obj = json.loads(Path(attestation).read_text()) if Path(attestation).exists() else json.loads(attestation)
    return attest.detect_and_verify(obj, public_key or None)


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
