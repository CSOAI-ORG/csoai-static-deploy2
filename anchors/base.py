#!/usr/bin/env python3
"""
anchors/base.py — the fail-closed watcher contract.

WHY THIS FILE IS BEING WRITTEN NOW RATHER THAN BEING FOUND
The build map dated 2026-07-29 marks anchors/uk_legislation.py, eu_aiact.py, c2pa_spec.py,
rfc_editor.py, crosswalk_registry.py, base.py and backoff.py as "✅ LIVE". None of them existed
on disk. Only corpus_anchor.py — the frozen normaliser — was real. A planning document that
reports components live when they are absent is the same defect this estate keeps finding in its
own code, one layer up.

THE CONTRACT
Every watcher answers one question about one document: has the text we anchored to changed?

Three states, never two:

  UNCHANGED  fetched, valid, digest matches the stored digest
  CHANGED    fetched, valid, digest differs — a drift event, with both digests recorded
  UNKNOWN    could not fetch, or fetched something that failed the content guard

UNKNOWN is not UNCHANGED. That distinction is the whole file. A watcher that reports "no drift"
because the request failed has made a claim about the law from a fact about the network. The
first poll of a new source is also not UNCHANGED — it is CHANGED from nothing, recorded as
`first_observation`, because we have no basis to say it is the same as anything.

NORMALISATION IS THE WHOLE GAME
Digests are taken over corpus_anchor.normalise() at a pinned version, and NORMALISER_VERSION is
written into every record. If the normaliser changes, the digest changes, and that must be
legible as "we changed how we read" rather than "the law changed". A record without the
normaliser version cannot distinguish the two, so the field is mandatory, not optional.

THE CONTENT GUARD
`is_valid()` exists because a 200 response is not evidence of a document. Anti-bot interstitials,
JavaScript shells and maintenance pages all return 200 with a body. A watcher that hashes those
records daily false drift and is worse than no watcher. The default guard rejects responses that
are implausibly short or that look like an HTML shell where a legal instrument was expected;
subclasses tighten it.
"""

from __future__ import annotations

import hashlib
import json
import sys
from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

from corpus_anchor import normalise, NORMALISER_VERSION  # noqa: E402

STATE_DIR = HERE / "state"

UNCHANGED = "UNCHANGED"
CHANGED = "CHANGED"
UNKNOWN = "UNKNOWN"


class FetchFailed(Exception):
    """Raised by fetch(). A typed exception, so a bare `except` cannot turn it into a verdict."""


class ContentRejected(Exception):
    """Raised when a response arrived but is not the document (shell page, interstitial, stub)."""


@dataclass
class Observation:
    watcher: str
    source_uri: str
    licence: str
    state: str
    observed_at: str
    normaliser_version: str
    digest: str | None = None
    previous_digest: str | None = None
    byte_length: int | None = None
    first_observation: bool = False
    reason: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


class WatcherBase:
    """Subclasses set SOURCE_URI and LICENCE and implement fetch(). Everything else is here."""

    #: The exact URL polled. Recorded on every observation so a reader can repeat the request.
    SOURCE_URI: str = ""
    #: Reuse terms of the source — OGL v3.0, EU reuse decision, PD, CC-BY. Recorded, and shown
    #: in the site's attribution block. A source we cannot attribute is a source we do not poll.
    LICENCE: str = ""
    #: Minimum plausible size of the normalised document, in characters.
    MIN_CHARS: int = 400

    #: Seconds. Kept short: a watcher that blocks the cron is a watcher that gets removed.
    TIMEOUT = 30

    def __init__(self, state_dir: Path | None = None) -> None:
        if not self.SOURCE_URI or not self.LICENCE:
            raise ValueError(f"{type(self).__name__} must declare SOURCE_URI and LICENCE")
        self.name = type(self).__name__
        self.state_dir = state_dir or STATE_DIR
        self.state_dir.mkdir(parents=True, exist_ok=True)

    # ── subclass surface ──────────────────────────────────────────────────────────────────
    def fetch(self) -> bytes:
        """Return the raw document bytes, or raise FetchFailed. Never return a sentinel."""
        raise NotImplementedError

    def extract(self, raw: bytes) -> str:
        """Raw bytes -> the text that is actually the provision. Default: decode as UTF-8."""
        return raw.decode("utf-8", errors="replace")

    def is_valid(self, text: str) -> None:
        """Raise ContentRejected if this is not the document. Subclasses call super() first."""
        if len(text) < self.MIN_CHARS:
            raise ContentRejected(f"{len(text)} chars, below MIN_CHARS={self.MIN_CHARS}")
        low = text[:2000].lower()
        for marker in (
            "enable javascript",
            "checking your browser",
            "access denied",
            "are you a robot",
            "cf-browser-verification",
            "503 service unavailable",
        ):
            if marker in low:
                raise ContentRejected(f"interstitial marker: {marker!r}")

    # ── the fixed part ────────────────────────────────────────────────────────────────────
    @property
    def state_file(self) -> Path:
        return self.state_dir / f"{self.name}.json"

    def _load_state(self) -> dict:
        if not self.state_file.is_file():
            return {}
        try:
            return json.loads(self.state_file.read_text())
        except (json.JSONDecodeError, OSError):
            # Corrupt state is not "no previous digest" — treating it as such would silently
            # convert a real CHANGED into a first_observation. Refuse and let health.py alarm.
            return {"corrupt": True}

    def poll(self) -> Observation:
        now = datetime.now(timezone.utc).isoformat(timespec="seconds")
        state = self._load_state()
        previous = state.get("digest")

        base = dict(
            watcher=self.name,
            source_uri=self.SOURCE_URI,
            licence=self.LICENCE,
            observed_at=now,
            normaliser_version=NORMALISER_VERSION,
            previous_digest=previous,
        )

        if state.get("corrupt"):
            return Observation(state=UNKNOWN, reason="state file is corrupt", **base)

        try:
            raw = self.fetch()
        except FetchFailed as e:
            return Observation(state=UNKNOWN, reason=f"fetch failed: {e}", **base)
        except Exception as e:  # a watcher bug must not become a verdict about the law
            return Observation(state=UNKNOWN, reason=f"{type(e).__name__}: {e}", **base)

        try:
            text = self.extract(raw)
            self.is_valid(text)
        except ContentRejected as e:
            return Observation(state=UNKNOWN, reason=f"content rejected: {e}", **base)
        except Exception as e:
            return Observation(state=UNKNOWN, reason=f"extract failed: {type(e).__name__}: {e}", **base)

        norm = normalise(text)
        digest = hashlib.sha256(
            f"{NORMALISER_VERSION}\x00{norm}".encode("utf-8")
        ).hexdigest()

        first = previous is None
        obs = Observation(
            state=CHANGED if (first or digest != previous) else UNCHANGED,
            digest=digest,
            byte_length=len(raw),
            first_observation=first,
            reason="no prior digest" if first else "",
            **base,
        )

        # State is written only on a successful, valid read. An UNKNOWN must never overwrite a
        # good digest — otherwise the next successful poll reports CHANGED against nothing and
        # a network outage manufactures a drift event.
        self.state_file.write_text(
            json.dumps(
                {
                    "digest": digest,
                    "normaliser_version": NORMALISER_VERSION,
                    "last_success": now,
                    "source_uri": self.SOURCE_URI,
                },
                indent=2,
            )
        )
        return obs


def registry() -> list[type[WatcherBase]]:
    """Every watcher that should run in the daily poll. Import errors surface here, loudly."""
    from anchors.uk_legislation import UKLegislation
    from anchors.eu_aiact import EUAIActArticle50
    from anchors.c2pa_spec import C2PASpec
    from anchors.rfc_editor import RFC9964
    from anchors.us_federal_register import USFederalRegisterAI

    return [UKLegislation, EUAIActArticle50, C2PASpec, RFC9964, USFederalRegisterAI]
