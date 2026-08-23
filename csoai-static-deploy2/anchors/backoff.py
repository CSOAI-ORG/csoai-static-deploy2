#!/usr/bin/env python3
"""
anchors/backoff.py — cached HTTP with retry, written after CELLAR throttled the daily poll.

The lesson that produced this file: EUR-Lex's CELLAR endpoint rate-limits, and a watcher that
hammers it gets nothing back for hours. The naive fix is a retry loop, which is also the way to
get blocked for longer. So: bounded exponential backoff, a disk cache keyed on the URL, and a
conditional request when we have an ETag or Last-Modified.

A 304 Not Modified is a genuine, cheap UNCHANGED — the server is telling us the document is
byte-identical, and we return the cached body so the digest is computed the same way as always
rather than being inferred from the status code.

Everything here raises FetchFailed on the way out. Callers get a typed exception, never a
sentinel value that could be hashed into a false digest.
"""

from __future__ import annotations

import hashlib
import json
import time
import urllib.error
import urllib.request
from pathlib import Path

from anchors.base import FetchFailed

CACHE_DIR = Path.home() / ".cache" / "csoai" / "anchors"

USER_AGENT = (
    "csoai-layer0-watcher/1.0 (+https://csoai.org/ai-transparency; "
    "polls public legal corpora once daily)"
)

RETRIES = 3
BASE_DELAY = 2.0  # seconds; doubled each attempt


def _slot(url: str) -> Path:
    return CACHE_DIR / (hashlib.sha256(url.encode()).hexdigest()[:24])


def get(url: str, timeout: int = 30, accept: str | None = None) -> bytes:
    """Fetch `url`, honouring the cache. Raises FetchFailed with the reason attached."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    slot = _slot(url)
    meta_f, body_f = slot.with_suffix(".json"), slot.with_suffix(".body")

    meta = {}
    if meta_f.is_file():
        try:
            meta = json.loads(meta_f.read_text())
        except (json.JSONDecodeError, OSError):
            meta = {}

    headers = {"User-Agent": USER_AGENT}
    if accept:
        headers["Accept"] = accept
    if meta.get("etag") and body_f.is_file():
        headers["If-None-Match"] = meta["etag"]
    if meta.get("last_modified") and body_f.is_file():
        headers["If-Modified-Since"] = meta["last_modified"]

    last = ""
    for attempt in range(RETRIES):
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                body = r.read()
                meta_f.write_text(
                    json.dumps(
                        {
                            "etag": r.headers.get("ETag"),
                            "last_modified": r.headers.get("Last-Modified"),
                            "fetched_at": time.time(),
                            "status": r.status,
                            "url": url,
                        }
                    )
                )
                body_f.write_bytes(body)
                return body
        except urllib.error.HTTPError as e:
            if e.code == 304 and body_f.is_file():
                # Server says unchanged. Return the cached bytes so the digest is computed by
                # the same path as a fresh fetch — never inferred from the status alone.
                return body_f.read_bytes()
            last = f"HTTP {e.code}"
            # 4xx other than 429 will not become 2xx by asking again.
            if e.code != 429 and 400 <= e.code < 500:
                break
        except urllib.error.URLError as e:
            last = f"URLError: {e.reason}"
        except (TimeoutError, OSError) as e:
            last = f"{type(e).__name__}: {e}"

        if attempt < RETRIES - 1:
            time.sleep(BASE_DELAY * (2**attempt))

    raise FetchFailed(f"{url} — {last} after {RETRIES} attempts")
