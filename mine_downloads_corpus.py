#!/usr/bin/env python3
"""
mine_downloads_corpus.py — scan ~/Downloads/ for producer/router/tourer
patterns and route them into honey.

Matches:
  - *.py       — potential producer function
  - *.jsonl    — training data or KB content
  - *.json     — config or KB
  - *.parquet  — large dataset
  - *.csv      — tabular data
  - *.md       — spec / playbook (spec family only)

Outputs: forest/honey_downloads.jsonl
"""

import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

DOWNLOADS = Path.home() / "Downloads"
ROOT = Path.home() / "clawd" / "csoai-static-deploy2"
HONEY = ROOT / "forest" / "honey_downloads.jsonl"

# Try to import sov_route
try:
    sys.path.insert(0, str(ROOT))
    from sov_route import route
    HAS_SOV_ROUTE = True
except ImportError:
    HAS_SOV_ROUTE = False

# Patterns to match
PATTERNS = {
    ".py": "code/producer",
    ".jsonl": "data/training",
    ".json": "data/config",
    ".parquet": "data/dataset",
    ".csv": "data/tabular",
    ".md": "spec",
    ".tar.gz": "archive",
}


def sha256_str(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def classify(filename: str) -> tuple[str, str]:
    """Classify a file by extension. Returns (kind, tag)."""
    for ext, kind in PATTERNS.items():
        if filename.endswith(ext):
            tag = f"[DOWNLOAD:{kind.upper().replace('/', '_')}]"
            return kind, tag
    return "unknown", "[DOWNLOAD]"


def emit_event(path: Path, kind: str, tag: str) -> dict:
    """Emit a single honey event for a downloaded file."""
    try:
        stat = path.stat()
        size = stat.st_size
        mtime = datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).isoformat()
        sample = ""
        if path.suffix in (".jsonl", ".json") and size < 1024 * 1024:
            try:
                with open(path, "r", errors="ignore") as f:
                    sample = f.read(512)
            except Exception:
                pass
    except Exception as e:
        size = 0
        mtime = now_iso()
        sample = f"stat_error: {e}"

    event = {
        "timestamp": now_iso(),
        "kind": "download_file",
        "summary": f"{path.name} ({kind}, {size} bytes)",
        "source": "downloads_corpus",
        "tags": [tag, "[DOWNLOAD]"],
        "payload": {
            "filename": path.name,
            "path": str(path),
            "size": size,
            "mtime": mtime,
            "kind": kind,
            "sample": sample[:256] if sample else "",
        },
        "capture_id": sha256_str(f"download:{path.name}:{size}")[:16],
    }

    if HAS_SOV_ROUTE:
        try:
            return route(event)
        except Exception:
            pass
    return event


def load_cache() -> dict:
    """Load cache of (filename, mtime) -> event_jsonl_line."""
    cache_path = ROOT / "forest" / "mine_downloads_cache.json"
    if cache_path.exists():
        try:
            return json.loads(cache_path.read_text())
        except Exception:
            return {}
    return {}


def save_cache(cache: dict):
    """Save cache to disk for next run."""
    cache_path = ROOT / "forest" / "mine_downloads_cache.json"
    cache_path.write_text(json.dumps(cache, indent=2))


def main():
    parser = argparse.ArgumentParser(description="Mine Downloads corpus")
    parser.add_argument("--limit", type=int, default=None, help="Limit files processed")
    parser.add_argument("--pattern", default=None, help="Only match files matching pattern")
    parser.add_argument("--force", action="store_true", help="Re-mine all files (ignore cache)")
    parser.add_argument("--no-cache", action="store_true", help="Skip cache lookup entirely")
    args = parser.parse_args()

    if not DOWNLOADS.exists():
        print(f"Downloads dir not found: {DOWNLOADS}")
        sys.exit(1)

    print(f"Mining {DOWNLOADS}...")
    print(f"  Output: {HONEY}")
    print(f"  sov_route available: {HAS_SOV_ROUTE}")

    # Get all files
    all_files = []
    for f in DOWNLOADS.iterdir():
        if f.is_file():
            if args.pattern and args.pattern not in f.name:
                continue
            all_files.append(f)

    if args.limit:
        all_files = all_files[:args.limit]

    print(f"  Total files: {len(all_files)}")

    # Classify
    matched = []
    by_kind = {}
    for f in all_files:
        kind, tag = classify(f.name)
        if kind != "unknown":
            matched.append((f, kind, tag))
            by_kind.setdefault(kind, 0)
            by_kind[kind] += 1

    print(f"  Matched: {len(matched)}")
    for k, n in sorted(by_kind.items()):
        print(f"    {k}: {n}")

    # Load cache
    cache = {} if args.no_cache else load_cache()
    if cache:
        print(f"  Cache loaded: {len(cache)} entries")

    # Emit
    HONEY.parent.mkdir(parents=True, exist_ok=True)
    HONEY.write_text("")  # truncate

    written = 0
    cached = 0
    skipped = 0
    new_cache = {}
    for path, kind, tag in matched:
        try:
            mtime = path.stat().st_mtime
        except Exception:
            mtime = 0
        cache_key = path.name

        # Check cache: skip if mtime matches
        if not args.force and not args.no_cache and cache_key in cache:
            cached_entry = cache[cache_key]
            if cached_entry.get("mtime") == mtime:
                # Cache hit — write previously-emitted event
                with open(HONEY, "a") as f:
                    f.write(json.dumps(cached_entry["event"]) + "\n")
                cached += 1
                new_cache[cache_key] = cached_entry
                continue

        # Cache miss or stale — emit fresh
        evt = emit_event(path, kind, tag)
        with open(HONEY, "a") as f:
            f.write(json.dumps(evt) + "\n")
        new_cache[cache_key] = {
            "mtime": mtime,
            "kind": kind,
            "tag": tag,
            "event": evt,
        }
        written += 1
        if written % 100 == 0:
            print(f"    wrote {written}...")
        if args.limit and written >= args.limit:
            break

    # Save cache
    save_cache(new_cache)

    print(f"\n  Total emitted: {written} (cache hits: {cached})")
    print(f"  Saved to: {HONEY}")
    print(f"  Cache saved to: {ROOT / 'forest' / 'mine_downloads_cache.json'}")


if __name__ == "__main__":
    main()
