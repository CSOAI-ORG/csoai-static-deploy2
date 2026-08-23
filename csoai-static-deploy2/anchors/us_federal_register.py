#!/usr/bin/env python3
"""
anchors/us_federal_register.py — the cleanest API in the whole set.

federalregister.gov publishes a keyless JSON API over US federal agency rules and notices. It is
the first of the N-sites expansion because it costs nothing to add and closes the largest single
coverage gap in the crosswalk: every axis currently anchors to EU and UK instruments only.

This watcher is a different shape from the others and the difference is deliberate. The
legislation and specification watchers anchor to one document and ask "did this text change".
This one anchors to a *result set* — AI-related rules published in a rolling window — and asks
"has the set changed". A new rule appearing is the event.

The trap in that shape is the rolling window itself: a query for "the last 30 days" changes its
answer every day for reasons that have nothing to do with agency activity, so the digest would
churn daily and mean nothing. So the window is fixed on `publication_date` bounds passed in, not
a relative range, and the extract step drops the API's own response metadata before hashing.
"""

from __future__ import annotations

import json

from anchors.base import WatcherBase, ContentRejected
from anchors import backoff


class USFederalRegisterAI(WatcherBase):
    # `conditions[term]` full-text search; ordered by date so the digest is order-stable.
    SOURCE_URI = (
        "https://www.federalregister.gov/api/v1/documents.json"
        "?conditions[term]=artificial+intelligence"
        "&conditions[type][]=RULE"
        "&conditions[publication_date][gte]=2026-01-01"
        "&conditions[publication_date][lte]=2026-06-30"
        "&fields[]=document_number&fields[]=title&fields[]=publication_date"
        "&fields[]=agencies&per_page=100&order=oldest"
    )
    LICENCE = "US Government work, public domain (17 U.S.C. §105)"
    MIN_CHARS = 200

    def fetch(self) -> bytes:
        return backoff.get(self.SOURCE_URI, timeout=self.TIMEOUT, accept="application/json")

    def extract(self, raw: bytes) -> str:
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError as e:
            raise ContentRejected(f"not JSON: {e}") from e

        results = payload.get("results")
        if results is None:
            raise ContentRejected("no `results` key — API shape changed")

        # Hash the documents, not the envelope. `count`, `total_pages` and `next_page_url` move
        # for reasons unrelated to the rules themselves.
        rows = [
            {
                "document_number": r.get("document_number"),
                "title": r.get("title"),
                "publication_date": r.get("publication_date"),
                "agencies": sorted(a.get("raw_name", "") for a in (r.get("agencies") or [])),
            }
            for r in results
        ]
        rows.sort(key=lambda r: (r["publication_date"] or "", r["document_number"] or ""))
        return json.dumps(rows, indent=0, sort_keys=True, ensure_ascii=False)

    def is_valid(self, text: str) -> None:
        # An empty result set is a real, meaningful answer — "no AI rules in this window" — and
        # must not be rejected as too short. It is also exactly the shape that a broken query
        # returns, so the guard checks the JSON parsed to a list rather than checking length.
        try:
            rows = json.loads(text)
        except json.JSONDecodeError as e:
            raise ContentRejected(f"extract did not produce JSON: {e}") from e
        if not isinstance(rows, list):
            raise ContentRejected(f"expected a list of documents, got {type(rows).__name__}")
        for r in rows:
            if not r.get("document_number"):
                raise ContentRejected("a row has no document_number — fields[] request failed")
