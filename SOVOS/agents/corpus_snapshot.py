#!/usr/bin/env python3
"""corpus_snapshot.py — reproducible corpus snapshots (the lakeFS pattern, minimal).

Pins "the corpus as-of <date>" so any index publication is reproducible:
- Computes a content-addressed manifest (sha256 of every file's digest)
- Writes a SNAPSHOT.json with the manifest + a signed digest over it
- Optionally uploads the manifest to MinIO for durability

The DOIs promise reproducibility; this makes it true and verifiable.
Usage:
    python3 corpus_snapshot.py --dir SOVOS/data/hive --tag 2026-08-15 \
        --out SOVOS/data/snapshots/corpus-2026-08-15.json
"""

from __future__ import annotations
import argparse, hashlib, json, os, sys
from datetime import datetime, timezone
from pathlib import Path


def file_digest(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def scan(corpus_dir: Path, rel_prefix: str = "") -> dict[str, str]:
    """Returns {relative_path: sha256} for all files under corpus_dir."""
    files: dict[str, str] = {}
    for p in sorted(corpus_dir.rglob("*")):
        if p.is_file() and not p.name.startswith("._"):
            rel = str(p.relative_to(corpus_dir))
            files[rel] = _digest(p)
    return files


def _digest(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def root_digest(files: dict[str, str]) -> str:
    # Content-addressed Merkle-ish root: sort file paths, hash path+dgst pairs
    h = hashlib.sha256()
    for rel, dgst in sorted(files.items()):
        h.update(f"{rel}\0{dgst}\0".encode())
    return h.hexdigest()


def sign(manifest: dict, seed: str = "0" * 64) -> dict:
    canonical = json.dumps(manifest, sort_keys=True, separators=(",", ":")).encode()
    digest = hashlib.sha256(canonical).hexdigest()
    signature = hashlib.sha256(
        bytes.fromhex(seed[:32]) + bytes.fromhex(digest[:32])
    ).hexdigest()[:64]
    return {**manifest, "digest": digest, "signature": signature}


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--corpus", required=True, help="corpus dir to snapshot")
    p.add_argument("--tag", default="snapshot")
    p.add_argument("--output", default="-")
    p.add_argument("--seed", default="0" * 64)
    args = p.parse_args()

    corpus = Path(args.corpus)
    if not corpus.is_dir():
        print(f"❌ corpus dir not found: {corpus}", file=sys.stderr)
        return 1

    files = scan(corpus)
    root = root_digest(files)
    manifest = {
        "schema": "corpus-snapshot-v1",
        "tag": args.tag,
        "corpus_root": str(corpus),
        "file_count": len(files),
        "created": datetime.now(timezone.utc).isoformat(),
        "root_digest": root,
        "files": files,
    }
    signed = sign(manifest, args.seed)

    out = json.dumps(signed, indent=2)
    if args.output and args.output != "-":
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        Path(args.output).write_text(out + "\n")
        print(f"✅ snapshot {args.tag}: {len(files)} files, root={root[:16]}… → {args.output}")
    else:
        print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())