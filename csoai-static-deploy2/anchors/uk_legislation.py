#!/usr/bin/env python3
"""
anchors/uk_legislation.py — legislation.gov.uk, the cleanest source in the set.

Why this one first: legislation.gov.uk serves Crown copyright material under the Open Government
Licence v3.0 and exposes every item as CLML XML at a stable `/data.xml` suffix. The XML is
byte-stable in a way the HTML rendering is not — the HTML carries navigation chrome, a "last
updated" banner and session-varying markup, all of which produce daily false drift.

Anchored: the Data Protection Act 2018, Part 2 — the UK's automated-decision-making provisions,
which the crosswalk maps against EU AI Act Article 22 GDPR-equivalents.
"""
from __future__ import annotations

import re

from anchors.base import WatcherBase, ContentRejected
from anchors import backoff


class UKLegislation(WatcherBase):
    SOURCE_URI = "https://www.legislation.gov.uk/ukpga/2018/12/part/2/data.xml"
    LICENCE = "Open Government Licence v3.0"
    MIN_CHARS = 2000

    def fetch(self) -> bytes:
        return backoff.get(self.SOURCE_URI, timeout=self.TIMEOUT, accept="application/xml")

    def extract(self, raw: bytes) -> str:
        text = raw.decode("utf-8", errors="replace")
        # Strip the CLML metadata block: it carries a fetch timestamp and revision counters that
        # change without the law changing. Hashing them would report drift every single day.
        text = re.sub(r"<ukm:Metadata\b.*?</ukm:Metadata>", "", text, flags=re.S)
        return text

    def is_valid(self, text: str) -> None:
        super().is_valid(text)
        if "<Legislation" not in text:
            raise ContentRejected("no <Legislation> root element — not CLML")
