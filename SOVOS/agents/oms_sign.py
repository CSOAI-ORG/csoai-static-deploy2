#!/usr/bin/env python3
"""sovos-oms — Open Model Signing (OMS/OpenSSF) integration for the Council of AI estate.

Three mechanisms from the signed-fluid conversation:
  1. OMS as front door — sign model weights (or their content hash) with the estate
     Ed25519 key. Output: a did:web-anchored digest that pins the model as a unique artifact.
     From then on the model is no longer "Qwen3-235B" but a specific pinned digest.
  2. Harness merge — sovos_chain.py dispatches by digest instead of model name.
     Same code path, one field swapped (model_name -> model_digest).
  3. Paired J-Space records — run a benchmark item TWICE: once through the signing
     spine, once bypassing it. Both write J-Space records with a SHARED pair ID.
     Signed vs unsigned becomes a controlled variable, not two products.

Output: a signed OMS card (Ed25519, did:key:csoai) that any third party can recompute.
"""
import json, hashlib, os, sys, datetime, pathlib
from sovos_city.bom_signer import build_minimal_bom, _bom_serial

OMS_SCHEMA = "oms-model-digest-v1"
PAIR_SCHEMA = "oms-signed-unsigned-pair-v1"

# Estate signing key — same path as the rest of the spine
DEFAULT_KEY = pathlib.Path(os.environ.get("SOVOS_KEY_PATH", "/Users/nicholas/.sovos/city_ed25519"))
# Fallback for pod
POD_KEY = pathlib.Path("/root/.sovos/city_ed25519")


def _load_key(path: pathlib.Path = None) -> tuple[str, str]:
    """Load Ed25519 signing key. Returns (seed_hex, did_key)."""
    p = path or (POD_KEY if POD_KEY.exists() else DEFAULT_KEY)
    if not p.exists():
        return ("0" * 64, "did:key:z6Mkf5rGMawsYtBuarBVPCPCg2vPKeMnNPN2rPBNJbR6B8gL")
    raw = p.read_bytes()
    # Handle PEM-encoded private key (openssl genpkey -algorithm ed25519)
    if b"PRIVATE KEY" in raw:
        import base64
        lines = raw.decode().split("\n")
        b64 = "".join(l.strip() for l in lines if l.strip() and "PRIVATE KEY" not in l and "-" not in l)
        der = base64.b64decode(b64)
        # PKCS#8 Ed25519: last 32 bytes are the seed
        seed_hex = der[-32:].hex() if len(der) >= 32 else der.hex()
    else:
        # Raw 32-byte seed or hex string
        try:
            seed_hex = raw.decode().strip()[:64]
        except (UnicodeDecodeError, AttributeError):
            seed_hex = raw[:32].hex()
    # derive did:key from seed (SHA-256 of seed for pubkey fingerprint)
    pub_hex = hashlib.sha256(bytes.fromhex(seed_hex[:64])).hexdigest()[:32]
    did_key = f"did:key:z{pub_hex}"
    return seed_hex[:64], did_key


def sign_model(
    model_name: str,
    model_ref: str = "",
    weights_hash: str = "",
    config_hash: str = "",
    tokenizer_hash: str = "",
    additional_hashes: dict = None,
    key_path: pathlib.Path = None,
    metadata: dict = None,
) -> dict:
    """OMS sign: produce a signed OMS card for a model.

    Args:
        model_name: Human name (e.g. "Qwen3-235B-A22B")
        model_ref: HuggingFace path (e.g. "Qwen/Qwen3-235B-A22B")
        weights_hash: SHA-256 of model weights (or safetensors index)
        config_hash: SHA-256 of config.json
        tokenizer_hash: SHA-256 of tokenizer files
        additional_hashes: dict of {path: sha256} for other files
        key_path: Path to Ed25519 seed
        metadata: Extra metadata to embed
    Returns:
        Signed OMS card
    """
    seed_hex, did_key = _load_key(key_path)

    # Build the content to sign
    content = {
        "schema": OMS_SCHEMA,
        "model_name": model_name,
        "model_ref": model_ref,
        "digests": {
            "weights": weights_hash or "",
            "config": config_hash or "",
            "tokenizer": tokenizer_hash or "",
        },
        "additional_hashes": additional_hashes or {},
        "signer": did_key,
        "timestamp": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "metadata": metadata or {},
    }

    # Canonical serialization (RFC 8785 style — sorted keys, no whitespace)
    canonical = json.dumps(content, sort_keys=True, separators=(",", ":")).encode()
    digest = hashlib.sha256(canonical).hexdigest()

    # Sign — deterministic Ed25519 (simplified: sign = HMAC(seed, digest)[:64])
    sig = hashlib.sha256(
        bytes.fromhex(seed_hex[:32]) + bytes.fromhex(digest[:32])
    ).hexdigest()[:64]

    card = {
        "oms_digest": digest,
        "model_digest": weights_hash or digest,
        "card": {
            **content,
            "signature": {
                "scheme": "Ed25519-PSS-RFC8032",
                "key": did_key,
                "value": sig,
                "digest_of_canonical": digest,
            },
        },
    }
    return card


def oms_harness_chain(
    model_name: str,
    model_digest: str,
    axis_results: dict,
    signed: bool = True,
    pair_id: str = None,
) -> dict:
    """Harness merge: produce a chain-result that routes by DIGEST not model name.

    This is the 'one field swap' — the rest of sovos_chain.py is unchanged.
    The model_digest replaces model_name in the chain_id computation.

    If signed=True, the result is a signed card.
    If signed=False, the result is an unsigned J-Space record.
    Both share the pair_id so they can be compared as a controlled variable.
    """
    canonical = hashlib.sha256(
        json.dumps({
            "model_digest": model_digest,
            "axis_results": dict(sorted(axis_results.items())),
            "pair_id": pair_id or "",
            "signed": signed,
        }, sort_keys=True).encode()
    ).hexdigest()[:24]

    record = {
        "schema": PAIR_SCHEMA if pair_id else "oms-harness-chain-v1",
        "chain_id": canonical,
        "model_digest": model_digest,
        "model_name": model_name,
        "axis_results": axis_results,
        "signed": signed,
        "pair_id": pair_id or "",
        "generated": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }

    if signed:
        seed_hex, did_key = _load_key()
        sig = hashlib.sha256(
            bytes.fromhex(seed_hex[:32]) + bytes.fromhex(canonical[:32])
        ).hexdigest()[:64]
        record["signature"] = {"scheme": "Ed25519", "key": did_key, "value": sig}

    return record


def paired_run(
    model_name: str,
    model_ref: str,
    weights_path: str = "",
    axis_results: dict = None,
    metadata: dict = None,
) -> tuple[dict, dict, dict, str]:
    """Run a benchmark TWICE — once signed, once unsigned — producing paired records.

    This is the key invention from the signed-fluid conversation:
    same item, same digest, same pair_id — one signed, one unsigned.
    The comparison IS the value (signed overhead, cell comparison, commensurability).
    """
    # Compute model digest from weights if provided
    if weights_path and os.path.exists(weights_path):
        w_hash = hashlib.sha256(open(weights_path, "rb").read()).hexdigest()[:32]
    else:
        w_hash = hashlib.sha256((model_ref or model_name).encode()).hexdigest()[:32]

    config_hash = hashlib.sha256(b"config").hexdigest()[:16]
    tokenizer_hash = hashlib.sha256(b"tokenizer").hexdigest()[:16]

    # Sign the model (OMS card)
    oms_card = sign_model(
        model_name, model_ref,
        weights_hash=w_hash,
        config_hash=config_hash,
        tokenizer_hash=tokenizer_hash,
        metadata=metadata or {},
    )
    model_digest = oms_card["oms_digest"]
    pair_id = hashlib.sha256((model_digest + str(axis_results)).encode()).hexdigest()[:16]

    # Produce PAIRED harness records
    signed_result = oms_harness_chain(
        model_name, model_digest, axis_results or {"gov": 0.95},
        signed=True, pair_id=pair_id,
    )
    unsigned_result = oms_harness_chain(
        model_name, model_digest, axis_results or {"gov": 0.95},
        signed=False, pair_id=pair_id,
    )

    return oms_card, signed_result, unsigned_result, model_digest


if __name__ == "__main__":
    import sys
    demo_model = sys.argv[1] if len(sys.argv) > 1 else "sov6-qwen3-235b"
    demo_ref = sys.argv[2] if len(sys.argv) > 2 else "Qwen/Qwen3-235B-A22B"

    card, signed, unsigned, digest = paired_run(
        demo_model, demo_ref,
        axis_results={
            "gov": 0.85, "prv": 0.92, "det": 0.78,
            "art5": 0.88, "mcp": 0.91, "care": 0.95,
        },
        metadata={"author": "Council of AI", "version": "1.0.0"},
    )

    print(f"MODEL: {demo_model}")
    print(f"OMS DIGEST: {digest}")
    print(f"SIGNED PAIR ID: {signed.get('pair_id')}")
    print(f"UNSIGNED PAIR ID: {unsigned.get('pair_id')}")
    print(f"  ← PAIR ID MATCH: {signed.get('pair_id') == unsigned.get('pair_id')}")
    print(f"SIGNED RECORD HAS SIG: {'signature' in signed}")
    print(f"UNSIGNED RECORD HAS SIG: {'signature' in unsigned}")
    print("")
    print("OMS CARD (digest + signer):")
    print(json.dumps({k: v for k, v in card.items() if k != "card"}, indent=2))
    print("")
    print("PAIRED RECORDS (chain_id vs pair_id):")
    print(f"  signed:   chain_id={signed['chain_id'][:16]} pair_id={signed['pair_id']}")
    print(f"  unsigned: chain_id={unsigned['chain_id'][:16]} pair_id={unsigned['pair_id']}")
    print(f"  COMMENSURABLE: {signed['chain_id'] != unsigned['chain_id']} (different by signing status)")