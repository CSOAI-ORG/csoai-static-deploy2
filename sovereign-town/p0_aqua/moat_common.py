#!/usr/bin/env python3
"""
moat_common.py — shared helpers for all data-moat modules.

Before: every moat module copy-pasted `load_moat(default=None)` and used bare
`except Exception:` around file/network operations. Now there is one safe loader,
one safe saver, and reusable fetch helpers with narrow exception handling.
"""
from __future__ import annotations

import json
import logging
import os
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

MOAT_DIR = Path(__file__).parent


def load_json(path: str | Path, default: Any = None) -> Any:
    """Load JSON from disk; return default on IO/decode errors."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError, ValueError) as e:
        logger.debug("load_json failed for %s: %s", path, e)
        return default


def save_json(path: str | Path, data: Any, indent: int = 2) -> bool:
    """Write JSON to disk atomically-ish; flush and fsync. Return success."""
    path = Path(path)
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=indent)
            f.flush()
            os.fsync(f.fileno())
        return True
    except (OSError, TypeError, ValueError) as e:
        logger.warning("save_json failed for %s: %s", path, e)
        return False


def load_moat(name: str, default: Any = None) -> Any:
    """Load a `<name>_moat.json` file from the p0_aqua directory."""
    return load_json(MOAT_DIR / f"{name}_moat.json", default=default)


def fetch_text(
    url: str,
    timeout: int = 60,
    max_bytes: int | None = None,
    headers: dict[str, str] | None = None,
) -> str:
    """Fetch a URL and return its text body. Raises on failure."""
    req_headers = {"User-Agent": "sovereign-town-moat/1.0"}
    if headers:
        req_headers.update(headers)
    req = urllib.request.Request(url, headers=req_headers)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        if max_bytes and r.headers.get("Content-Length"):
            if int(r.headers["Content-Length"]) > max_bytes:
                raise RuntimeError(f"response too large (> {max_bytes} bytes)")
        return r.read().decode("utf-8", errors="replace")


def fetch_csv_text(url: str, timeout: int = 60, max_bytes: int | None = None) -> str:
    return fetch_text(url, timeout=timeout, max_bytes=max_bytes, headers={"Accept": "text/csv"})


def fetch_json(
    url: str,
    timeout: int = 60,
    max_bytes: int | None = None,
    headers: dict[str, str] | None = None,
) -> dict[str, Any]:
    """Fetch a JSON URL and return the parsed object. Raises on failure."""
    req_headers = {"Accept": "application/json"}
    if headers:
        req_headers.update(headers)
    text = fetch_text(url, timeout=timeout, max_bytes=max_bytes, headers=req_headers)
    return json.loads(text)


def safe_env_int(name: str, default: int) -> int:
    raw = os.environ.get(name)
    if raw is None:
        return default
    try:
        return int(raw)
    except ValueError:
        logger.warning("Invalid int for %s: %r; using default %s", name, raw, default)
        return default


def safe_env_str(name: str, default: str) -> str:
    return os.environ.get(name, default)
