#!/usr/bin/env python3
"""
anchors/eu_aiact.py — EU AI Act Article 50, the article that binds on 2 August 2026.

Source choice is the whole design decision here. EUR-Lex's CELLAR SPARQL endpoint is the
canonical machine interface and it throttles hard; a daily poll against it spent more time in
backoff than fetching. The HTML consolidated text at eur-lex.europa.eu is served directly and
carries the operative text.

That makes this watcher structurally weaker than the UK one, and the record says so: EUR-Lex
wraps the provision in page chrome, so the extract step narrows to the article body before
hashing. If that narrowing ever fails to find its markers, this raises ContentRejected rather
than hashing the whole page — a watcher that silently widens its scope reports drift whenever
the site's navigation changes, and the alarm that follows trains people to ignore it.

Article 50 specifically, because it is the live obligation: 50(1) interaction disclosure and
50(2) synthetic-content marking apply from 2 August 2026, and the Digital Omnibus deferral
reached the Annex III high-risk regime, not this.
"""

from __future__ import annotations

import re

from anchors.base import WatcherBase, ContentRejected
from anchors import backoff


class EUAIActArticle50(WatcherBase):
    # CELEX 32024R1689 — Regulation (EU) 2024/1689, consolidated English text.
    SOURCE_URI = "https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32024R1689"
    LICENCE = "Commission reuse policy, Decision 2011/833/EU"
    MIN_CHARS = 3000

    #: The provision this watcher is anchored to. Recorded so a reader knows the scope of a
    #: CHANGED — "the AI Act changed" and "Article 50 changed" are different claims.
    PROVISION = "Article 50"

    def fetch(self) -> bytes:
        return backoff.get(self.SOURCE_URI, timeout=self.TIMEOUT, accept="text/html")

    def extract(self, raw: bytes) -> str:
        html = raw.decode("utf-8", errors="replace")

        # Narrow to Article 50 before hashing. The whole-regulation text would report drift on
        # any amendment anywhere, which tells us nothing about the obligation we anchor to.
        start = re.search(
            r"Article\s*50\b.{0,200}?Transparency obligations", html, re.S | re.I
        )
        if not start:
            raise ContentRejected("Article 50 heading not found — page structure changed")
        end = re.search(r"Article\s*51\b", html[start.start():], re.I)
        body = html[start.start(): start.start() + (end.start() if end else 60000)]

        # Strip tags and entities: the operative text is what binds, not the markup carrying it.
        body = re.sub(r"<[^>]+>", " ", body)
        body = body.replace("&nbsp;", " ").replace("&#160;", " ").replace("&amp;", "&")
        return body

    def is_valid(self, text: str) -> None:
        super().is_valid(text)
        # A positive liveness requirement, not just an absence check: the extracted span must
        # actually contain the operative language, or we narrowed onto the table of contents.
        if "transparency" not in text.lower():
            raise ContentRejected("extracted span has no 'transparency' — likely the contents list")
