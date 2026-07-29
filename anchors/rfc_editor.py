#!/usr/bin/env python3
"""
anchors/rfc_editor.py — RFC 9964, COSE algorithm identifiers for ML-DSA.

An RFC is immutable once published, so a CHANGED here would be extraordinary — which is exactly
why it is worth polling. It is the control in the watcher set: if this one ever reports drift,
the normaliser or the fetch path is broken, not the IETF. A watcher set with no expected-stable
member has no way to tell its own failures from real events.

Relevant because NIST IR 8547 disallows EdDSA after 2035 and our manifests are Ed25519 today;
RFC 9964 assigns the COSE identifiers (-48/-49/-50) a migration would target.
"""
from __future__ import annotations

from anchors.base import WatcherBase, ContentRejected
from anchors import backoff


class RFC9964(WatcherBase):
    SOURCE_URI = "https://www.rfc-editor.org/rfc/rfc9964.txt"
    LICENCE = "IETF Trust Legal Provisions (BSD-style for code components)"
    MIN_CHARS = 5000

    def fetch(self) -> bytes:
        return backoff.get(self.SOURCE_URI, timeout=self.TIMEOUT)

    def is_valid(self, text: str) -> None:
        super().is_valid(text)
        if "9964" not in text[:4000]:
            raise ContentRejected("RFC number 9964 not found in the header block")
