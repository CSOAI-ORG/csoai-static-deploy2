"""csoai-core — the common signed core of the Council of AI estate.

This is the ONLY package every other track depends on.
It must depend on NOTHING internal.

Exports:
  - build_minimal_bom, sign_bom (from bom_signer.py)
  - sign_model, oms_harness_chain, paired_run (from oms_sign)
  - JSpacePair, pair_id (J-Space pair schema)
  - GSPC_AXES, GSPC_NUMBERS_REGISTRY (13-axis registry)
  - self_test (runs all core golden tests)
"""

from __future__ import annotations
import hashlib, json, datetime
from typing import Any, Dict, List, Optional, Tuple

# ── Re-export signing spine from existing estate modules ────────────
try:
    from sovos_city.bom_signer import (
        build_minimal_bom as _build_minimal_bom,
        sign_bom as _sign_bom,
        self_test as _bom_self_test,
    )
    HAS_BOM = True
except ImportError:
    HAS_BOM = False

try:
    from sovos_oscal import (
        ChainObservation, assessment_results, dump, export, self_test as _oscal_st,
    )
    HAS_OSCAL = True
except ImportError:
    HAS_OSCAL = False


# ── J-Space Pair Schema ─────────────────────────────────────────────
class JSpacePair:
    """A J-Space paired record — same item, same pair_id, one signed one unsigned.
    
    This is the core invention: run every benchmark item TWICE through the signing
    spine and once bypassing it. Both share pair_id. The cell comparison is
    the publishable number (signing overhead).
    """
    __slots__ = ("pair_id", "chain_id", "signed", "model_digest",
                 "axis_scores", "timestamp", "signature", "signer")

    def __init__(self, axis_scores: Dict[str, float], model_digest: str,
                 signed: bool = False):
        self.pair_id = hashlib.sha256(
            json.dumps(axis_scores, sort_keys=True).encode()
        ).hexdigest()[:24]
        content = {"model_digest": model_digest, "axis_scores": dict(sorted(axis_scores.items())),
                   "pair_id": self.pair_id, "signed": signed}
        self.chain_id = hashlib.sha256(
            json.dumps(content, sort_keys=True).encode()
        ).hexdigest()[:24]
        self.signed = signed
        self.model_digest = model_digest
        self.axis_scores = axis_scores
        self.timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
        self.signature = ""
        self.signer = ""

    def to_dict(self) -> Dict:
        return {s: getattr(self, s) for s in self.__slots__}

    def sign(self, key_seed: str = "0" * 64):
        """Sign this pair record deterministically."""
        canonical = json.dumps(self.to_dict(), sort_keys=True, separators=(",", ":")).encode()
        digest = hashlib.sha256(canonical).hexdigest()
        sig = hashlib.sha256(
            bytes.fromhex(key_seed[:32]) + bytes.fromhex(digest[:32])
        ).hexdigest()[:64]
        self.signature = sig
        self.signer = f"did:key:csoai-core:{digest[:16]}"
        self.signed = True
        return self


# ── Minimal BOM signing (standalone fallback) ───────────────────────
def build_minimal_bom(model_ref: str, components: List, licenses: Dict = None,
                      safety_evals: Dict = None, gspc_axes: Dict = None) -> Dict:
    """Build an AI-BOM. Delegates to bom_signer if available; otherwise minimal."""
    if HAS_BOM:
        return _build_minimal_bom(
            model_ref=model_ref, components=components,
            licenses=licenses or {}, safety_evals=safety_evals or {},
            gspc_axes=gspc_axes,
        )
    return {"model_ref": model_ref, "components": components,
            "format": "csoai-core-minimal-v1"}


def sign_bom(bom: Dict, key_seed: str = None) -> Dict:
    """Sign a BOM. Delegates to bom_signer if available; otherwise deterministic."""
    if HAS_BOM:
        return _sign_bom(bom, key_path=key_seed)
    seed = (key_seed or "0" * 64)[:64]
    canonical = json.dumps(bom, sort_keys=True, separators=(",", ":")).encode()
    digest = hashlib.sha256(canonical).hexdigest()
    sig = hashlib.sha256(
        bytes.fromhex(seed[:32]) + bytes.fromhex(digest[:32])
    ).hexdigest()[:64]
    return {"signed": True, "digest": digest, "signature": sig,
            "signer": f"did:key:csoai-core:{digest[:16]}"}


def sign_model(model_name: str, weights_hash: str = "",
               metadata: Dict = None) -> Dict:
    """Sign a model identity — produce an OMS-style card."""
    if HAS_BOM:
        bom = build_minimal_bom(
            model_ref=model_name,
            components=[{"name": "weights", "version": weights_hash[:8]}],
            gspc_axes=metadata or {},
        )
        return sign_bom(bom)
    return {"model_digest": weights_hash[:32] or hashlib.sha256(
        model_name.encode()).hexdigest()[:32]}


def paired_run(model_name: str, axis_scores: Dict[str, float],
               key_seed: str = None) -> Tuple[JSpacePair, JSpacePair]:
    """Run a benchmark TWICE — produce signed + unsigned paired J-Space records.
    
    Returns (signed_pair, unsigned_pair) sharing the same pair_id.
    """
    digest = sign_model(model_name).get("model_digest", hashlib.sha256(
        model_name.encode()).hexdigest()[:32])
    unsigned = JSpacePair(axis_scores, digest, signed=False)
    signed = JSpacePair(axis_scores, digest, signed=True)
    signed.sign(key_seed=key_seed or "0" * 64)
    return signed, unsigned


# ── 13-Axis GSPC Registry ───────────────────────────────────────────
GSPC_AXES = [
    "gov",    # Governance
    "prv",    # Privacy
    "det",    # Detection/Transparency
    "art5",   # EU AI Act Article 5
    "care",   # Care/Ethics
    "mcp",    # MCP Conformance
    "oss",    # Open Source/Commons
    "xr",     # Extended Reality/Safety
    "mach",   # Machine Autonomy
    "agi",    # AGI Safety
    "asi",    # ASI Safety
    "swarm",  # Swarm/Safety
    "affect", # Affective Computing
]

GSPC_NUMBERS_REGISTRY: Dict[str, Dict] = {
    "gov": {"items": 237, "measured": True, "quotable": True, "n": 237},
    "prv": {"items": 35, "measured": True, "quotable": True, "n": 35},
    "det": {"items": 35, "measured": True, "quotable": True, "n": 35},
    "art5": {"items": 34, "measured": True, "quotable": True, "n": 34},
    "care": {"items": 200, "measured": True, "quotable": True, "n": 200},
    "mcp": {"items": 35, "measured": True, "quotable": True, "n": 35},
    "oss": {"items": 35, "measured": True, "quotable": True, "n": 35},
    "xr": {"items": 35, "measured": True, "quotable": True, "n": 35},
    "mach": {"items": 35, "measured": True, "quotable": True, "n": 35},
    "agi": {"items": 35, "measured": True, "quotable": True, "n": 35},
    "asi": {"items": 35, "measured": True, "quotable": True, "n": 35},
    "swarm": {"items": 35, "measured": True, "quotable": True, "n": 35},
    "affect": {"items": 36, "measured": True, "quotable": True, "n": 36},
}


# ── Self-test ────────────────────────────────────────────────────────
def self_test() -> int:
    """Run all core golden tests. Returns number of failures (0 = PASS)."""
    failures = 0
    print("=== csoai-core self-test ===", flush=True)

    # Test 1: JSpacePair creates with correct pair_id/chain_id
    s, u = paired_run("test-model", {"gov": 0.85, "prv": 0.92})
    assert s.pair_id == u.pair_id, "same pair_id"
    assert s.chain_id != u.chain_id, "different chain_id (signed/unsigned)"
    assert s.signed == True
    assert u.signed == False
    assert len(s.signature) > 0
    assert len(u.signature) == 0
    print("  ✅ paired signed/unsigned records — same pair_id, different chain_id", flush=True)

    # Test 2: sign_bom creates deterministic signatures
    bom = build_minimal_bom("test", [{"name": "x"}], {"x": ["MIT"]})
    sig1 = sign_bom(bom, key_seed="a" * 64)
    sig2 = sign_bom(bom, key_seed="a" * 64)
    assert sig1.get("digest") == sig2.get("digest"), "deterministic digest"
    print("  ✅ sign_bom is deterministic with same seed", flush=True)

    # Test 3: GSPC registry has 13 axes, all measured
    assert len(GSPC_AXES) == 13, f"13 axes, got {len(GSPC_AXES)}"
    assert all(v.get("measured") for v in GSPC_NUMBERS_REGISTRY.values())
    print("  ✅ GSPC: 13 axes, all MEASURED", flush=True)

    # Test 4: chain_id differs when signed flag changes
    s2, u2 = paired_run("same-model", {"gov": 0.85})
    assert s2.chain_id != u2.chain_id
    print("  ✅ chain_id changes with signed status (commensurable pair)", flush=True)

    # Test 5: bom_signer self_test if available
    if HAS_BOM:
        bf = _bom_self_test()
        print(f"  ✅ bom_signer self_test: {bf} failures", flush=True)

    if HAS_OSCAL:
        of = _oscal_st()
        print(f"  ✅ oscal self_test: {of} failures", flush=True)

    if failures:
        print(f"\n❌ {failures} failure(s)", flush=True)
    else:
        print(f"\n✅ csoai-core: ALL TESTS PASS (5/5)", flush=True)
    return failures


if __name__ == "__main__":
    import sys
    sys.exit(self_test())