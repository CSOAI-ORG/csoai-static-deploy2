#!/usr/bin/env python3
"""replay_instrument.py — signed/unsigned replay lineage for sim forks.

Block B #10: instrument AgentSociety / ai-town / meltingpot experiment
manifests + replay logs so any simulation run produces PAIRED signed/unsigned
lineage records through the estate spine. The fork stays upstream-faithful;
the instrumenter sits at the boundary.

Design:
- consume an experiment manifest + replay log dir
- compute 3 digests: manifest, replay events, full lineage root
- emit unsigned record (content) + signed record (Ed25519 via keys/)
- write BOTH into a paired JSONL so downstream can A/B the trust delta

Usage:
    python3 replay_instrument.py --manifest <exp.json> --replay-dir <dir> \
        --issuer did:web:csoai.org --out <output.jsonl>
    python3 replay_instrument.py --dry-test
"""

from __future__ import annotations
import argparse, hashlib, json, sys
from datetime import datetime, timezone
from pathlib import Path

try:
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
    from cryptography.hazmat.primitives import serialization
    HAVE_CRYPTO = True
except ImportError:  # pragma: no cover — pod has it
    HAVE_CRYPTO = False
    serialization = None  # type: ignore

KEY_DIR = Path(__file__).resolve().parent.parent / "keys"
KEY_NAME = "oms-signing-ed25519"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _priv():
    if not HAVE_CRYPTO:
        sys.exit("❌ cryptography not installed: /workspace/venv-test/bin/pip install cryptography")
    return serialization.load_pem_private_key(
        (KEY_DIR / f"{KEY_NAME}.pem").read_bytes(), password=None)


def _digest_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def lineage(manifest_path: Path, replay_dirs: list[Path]) -> dict:
    files: dict[str, str] = {}
    for d in replay_dirs:
        if d.is_file():
            files[str(d)] = _digest_file(d)
        elif d.is_dir():
            for fp in sorted(d.rglob("*")):
                if fp.is_file() and not fp.name.startswith("._"):
                    files[str(fp.relative_to(d))] = _digest_file(fp)
    manifest = _digest_file(manifest_path)
    root = hashlib.sha256(
        json.dumps({"manifest": manifest, "replay": files},
                   sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    return {"manifest_digest": manifest, "replay_files": files,
            "lineage_digest": root}


def build_records(manifest_path: Path, replay_dirs: list[Path],
                  issuer: str, note: str = "") -> list[dict]:
    priv = _priv()
    ds = lineage(manifest_path, replay_dirs)
    base = {
        "schema": "sim-replay-lineage-v1",
        "manifest": str(manifest_path),
        "replay_roots": [str(p) for p in replay_dirs],
        "manifest_digest": ds["manifest_digest"],
        "replay_file_count": len(ds["replay_files"]),
        "lineage_digest": ds["lineage_digest"],
        "issuer": issuer,
        "created": _now(),
        "note": note,
    }
    unsigned = {**base, "signed": False,
                "card_type": "sim-replay-lineage-unsigned"}
    signed = {**base, "signed": True, "card_type": "sim-replay-lineage-signed-oms"}
    payload = json.dumps(signed, sort_keys=True, separators=(",", ":")).encode()
    signed["signature"] = _priv().sign(payload).hex()
    signed["signer"] = "oms-signing-ed25519 (SOVOS/keys)"
    return [unsigned, signed]


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--manifest", help="experiment manifest file")
    p.add_argument("--replay-dir", action="append", default=[])
    p.add_argument("--out", default="-")
    p.add_argument("--issuer", default="did:web:csoai.org")
    p.add_argument("--dry-test", action="store_true")
    a = p.parse_args()

    if a.dry_test:
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            m = root / "exp.json"
            m.write_text(json.dumps({"experiment": "dry", "seeds": 3}))
            r = root / "replay"
            r.mkdir()
            (r / "events.jsonl").write_text(
                json.dumps({"t": 0, "action": "start"}) + "\n")
            recs = build_records(m, [r], a.issuer, note="dry-test")
            print(json.dumps(recs, indent=2))
        return 0

    if not a.manifest or not a.replay_dir:
        p.error("--manifest and at least one --replay-dir required (or --dry-test)")
    recs = build_records(Path(a.manifest), [Path(x) for x in a.replay_dir],
                         a.issuer, note="instrumented replay lineage (signed/unsigned pair)")
    out = json.dumps(recs, indent=2)
    if a.out and a.out != "-":
        Path(a.out).parent.mkdir(parents=True, exist_ok=True)
        Path(a.out).write_text(out + "\n")
        print(f"✅ paired lineage written: {a.out} ({len(out)} bytes)")
    else:
        print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())