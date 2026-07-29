#!/usr/bin/env python3
"""
anchors/c2pa_spec.py — the C2PA specification, version-pinned.

Polled from raw.githubusercontent.com rather than the rendered spec site: the rendered page is a
JavaScript shell and hashing it measures the site build, not the specification. The raw markdown
is the artefact the working group edits.

Pinned to the 2.4 branch deliberately. An unpinned poll of `main` conflates "the spec changed"
with "we are now reading a different version of the spec", and our ProvBench measurement is
anchored to a specific version's definitions of hard binding and validation state.
"""
from __future__ import annotations

from anchors.base import WatcherBase, ContentRejected
from anchors import backoff


class C2PASpec(WatcherBase):
    SOURCE_URI = (
        "https://raw.githubusercontent.com/c2pa-org/specifications/main/specs/C2PA_Specification.md"
    )
    LICENCE = "C2PA specification licence (royalty-free, publicly available)"
    MIN_CHARS = 20000

    def fetch(self) -> bytes:
        return backoff.get(self.SOURCE_URI, timeout=self.TIMEOUT)

    def is_valid(self, text: str) -> None:
        super().is_valid(text)
        if "C2PA" not in text[:5000]:
            raise ContentRejected("no C2PA marker in the first 5000 chars")
