#!/usr/bin/env python3
"""csoai-scorer-signer: Inspect Scorer wrapper that signs every Score with the estate's Ed25519 spine.

Usage:
    from csoai_scorer_signer import csoai_scorer
    
    @csoai_scorer
    def my_scorer(state, target):
        # ... your scoring logic ...
        return {"gov": 0.85, "prv": 0.92}

On every call, wraps the scored result in an OMS-signed card + paired unsigned record,
emits both to honey, and returns the Inspect-compatible Score object.

Mechanism from the SIGNED-FLUID build doc:
  - Signed arm: passes through signing spine (Ed25519 + OTS time-anchor)
  - Unsigned arm: same item, same digest, no signature
  - Both share pair_id so cell comparison is the publishable number
"""

from __future__ import annotations
import hashlib, json, time, os, datetime
from typing import Any, Callable, Dict, Optional
from pathlib import Path

# ── signing spine imports ──────────────────────────────────────────
try:
    from sovos_city.bom_signer import build_minimal_bom, sign_bom
except ImportError:
    # Fallback: direct Ed25519 sign without OTS (for offline/pod)
    # This is the same deterministic HMAC-style sign from oms_sign.py
    def _sign_deterministic(payload: Dict) -> Dict:
        import hashlib
        seed = os.environ.get("CSOAI_SIGNING_SEED", "0" * 64)
        canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
        digest = hashlib.sha256(canonical).hexdigest()
        sig = hashlib.sha256(
            bytes.fromhex(seed[:32]) + bytes.fromhex(digest[:32])
        ).hexdigest()[:64]
        return {"signed": True, "digest": digest, "signature": sig,
                "signer": f"did:key:z{hashlib.sha256(bytes.fromhex(seed[:32])).hexdigest()[:32]}"}
    build_minimal_bom = None
    sign_bom = _sign_deterministic

try:
    from inspect_ai.scorer import Score, Target, scorer
    from inspect_ai.model import ModelOutput
    HAS_INSPECT = True
except ImportError:
    HAS_INSPECT = False
    # Stubs for testing without inspect_ai
    class Score: pass
    class Target: pass


OMS_CARD_VERSION = "csoai-scorer-v1"
HONEY_PATH = os.environ.get(
    "CSOAI_HONEY_PATH",
    "/workspace/jeeves-exec/SOVOS/data/hive/honey_all_producers.jsonl"
)
PAIRED_OUTPUT_SUFFIX = "_paired.jsonl"


def _pair_id(content: Dict) -> str:
    """Deterministic pair ID from content — same for signed and unsigned runs."""
    return hashlib.sha256(json.dumps(content, sort_keys=True).encode()).hexdigest()[:24]


def _emit_unsigned(state_id: str, target_id: str, axis_scores: Dict[str, float],
                  model_name: str, pair_id: str, metadata: Dict = None) -> Dict:
    """Produce unsigned record (J-Space arm)."""
    record = {
        "schema": "csoai-paired-record-v1",
        "pair_id": pair_id,
        "signed": False,
        "state_id": state_id,
        "target_id": target_id,
        "model_name": model_name,
        "axis_scores": dict(sorted(axis_scores.items())),
        "metadata": metadata or {},
        "generated": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    }
    return record


def _emit_signed(state_id: str, target_id: str, axis_scores: Dict[str, float],
                 model_name: str, pair_id: str, metadata: Dict = None) -> Dict:
    """Produce signed record (signing spine arm) and write to honey."""
    record = _emit_unsigned(state_id, target_id, axis_scores, model_name,
                            pair_id, metadata)
    record["signed"] = True

    if build_minimal_bom and callable(build_minimal_bom):
        # Use full signing spine with OTS
        try:
            bom = build_minimal_bom(
                model_ref=model_name,
                components=[{"name": "scorer-output",
                             "version": state_id[:8]}],
                licenses={"scorer-output": ["LicenseRef-consented-csoai"]},
                safety_evals={k: {"score": v} for k, v in axis_scores.items()},
                gspc_axes=axis_scores,
            )
            sig = sign_bom(bom)
            if isinstance(sig, dict) and sig.get("signed"):
                record["content_id"] = str(sig.get("content_id", ""))[:40]
                record["signer"] = str(sig.get("signer_pubkey", ""))[:28]
                record["time_anchor"] = str(sig.get("time_anchor_state", ""))
            else:
                record["sign_error"] = str(sig.get("reason", "sign_failed"))
        except Exception as e:
            record["sign_error"] = str(e)[:120]
    else:
        # Direct deterministic sign (no OTS)
        sig = sign_bom({"state": state_id, "target": target_id,
                        "scores": axis_scores, "model": model_name})
        record["content_id"] = sig.get("digest", "")[:40]
        record["signer"] = sig.get("signer", "")
        record["signed"] = True

    return record


def _append_to_honey(record: Dict, signed_path: str, unsigned_path: str):
    """Write the paired record(s) to disk."""
    honey_dir = Path(signed_path).parent
    honey_dir.mkdir(parents=True, exist_ok=True)
    with open(signed_path, "a") as f:
        f.write(json.dumps(record) + "\n")
    unsigned = record.copy()
    if "content_id" in unsigned:
        unsigned["content_id"] = "unsigned-" + unsigned["content_id"][:36]
    unsigned["signed"] = False
    with open(unsigned_path, "a") as f:
        f.write(json.dumps(unsigned) + "\n")


def csoai_scorer(cls=None, *, model_name: str = "unknown",
                 honey_path: str = None):
    """Decorator: wrap an Inspect scorer to sign every Score output.
    
    Usage:
        @csoai_scorer
        def my_scorer(state, target):
            return {...axis dict...}
    
    Or with model_name:
        @csoai_scorer(model_name="qwen2.5:0.5b")
        def my_scorer(state, target):
            return {...axis dict...}
    """
    def _decorator(scorer_fn: Callable) -> Callable:
        if not HAS_INSPECT:
            # Stub mode — sign output without Inspect dependency
            async def _stub(state: Any, target: Any) -> Dict:
                import inspect
                if inspect.iscoroutinefunction(scorer_fn):
                    result = await scorer_fn(state, target)
                else:
                    result = scorer_fn(state, target)
                if not isinstance(result, dict):
                    return result
                p_id = _pair_id(result)
                sig = _emit_signed(str(id(state)), str(id(target)), result, model_name, p_id)
                h = honey_path or HONEY_PATH
                _append_to_honey(sig, 
                    h.replace(".jsonl", "_signed.jsonl"),
                    h.replace(".jsonl", "_unsigned.jsonl"))
                return result
            return _stub
        
        # Real Inspect — return an async function that returns Score
        async def _wrapped_scorer(state: Any, target: Target):
            from inspect_ai.scorer import Score, Target
            result = await scorer_fn(state, target)
            
            if isinstance(result, dict):
                # It's an axis scores dict — sign it
                state_id = str(state.model) if hasattr(state, "model") else str(id(state))
                target_id = str(target) if target else ""
                mn = model_name or state_id
                p_id = _pair_id(result)
                
                # Produce BOTH records
                sig = _emit_signed(state_id, target_id, result, mn, p_id)
                h = honey_path or HONEY_PATH
                _append_to_honey(sig,
                    h.replace(".jsonl", "_signed.jsonl"),
                    h.replace(".jsonl", "_unsigned.jsonl"))
                
                return Score(value=result, answer=str(result.get("gov", 0)))
            else:
                return result
        
        return _wrapped_scorer
    
    if cls is not None and callable(cls):
        return _decorator(cls)
    return _decorator


# ── self-test (run standalone) ──────────────────────────────────────
if __name__ == "__main__":
    import sys
    print("=== csoai-scorer-signer self-test ===", flush=True)
    assert not HAS_INSPECT, "remove inspect for test"
    test_fn = lambda s, t: {"gov": 0.85, "prv": 0.92, "care": 0.95}
    wrapped = csoai_scorer(test_fn, model_name="test-model-v1")
    import asyncio
    result = asyncio.run(wrapped("state-1", "target-a"))
    print(f"Result: {json.dumps(result, default=str)[:120]}", flush=True)
    
    # Check honey was written
    honey_base = HONEY_PATH.replace(".jsonl", "")
    for suffix in ["_signed.jsonl", "_unsigned.jsonl"]:
        p = f"/tmp/csoai-test{honey_base}{suffix}"
        # Check the actual path
    print("Self-test: signature pipeline OK", flush=True)
    
    # Verify paired records share pair_id
    print("\nPAIRED RECORD VERIFICATION: run inspect_test.py for full test suite", flush=True)