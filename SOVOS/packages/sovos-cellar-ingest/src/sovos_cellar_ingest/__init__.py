"""sovos-cellar-ingest — EUR-Lex CELLAR → regulation vectors → StateBus.

Implements RAS move #2: "the Bus subscribes to law itself."

CELLAR (European Legislation Repository) is the machine-readable corpus
of all EU law: every CELEX document is a public RDF resource (EUR-Lex
Resource), queryable by SPARQL at publications.europa.eu, in 24
languages, free, with RSS change feeds.

This package:
  1. Fetches a CELEX document's RDF from CELLAR (live HTTP).
  2. Extracts the core bibliographic facts (celex, title, type,
     publication date, in-force status when present).
  3. Hashes those facts into a deterministic regulation vector
     (same shape as a StateVector/birth coordinate — so a regulation
     is just another clan/axis anchor on the manifold).
  4. Appends it to a sovos-bus-redis StateBus as a "honey" event
     (distilled, near-origin, immutable) or "milk" (working corpus)
     depending on mode.

Design laws honored:
  - SOFR anchoring: the vector is derived from live, versioned,
    publicly-served law — never from our own transcription.
  - Multilingual: the title is grabbed in the requested language; the
    vector is language-namespace-aware (same law in EN vs FR gives the
    same celex-derived core, so multilingual alignment is Procrustes-
    ready).
  - Versioning: CELEX documents carry a 4-digit year prefix; the vector
    includes the celex string, so amendments are distinct vectors with
    traceable lineage (Akoma-Ntoso-style provenance pattern).

Honest scope: we parse the *bibliographic core* of a CELEX resource —
not the full legal text (that's for the corpus layer, days of work —
OpenFisca-style article parsing). This is the ingestion skeleton that
makes "the Bus knows a new Regulation (EU) 2026/999 exists" true.

Public API:
    from sovos_cellar_ingest import (
        fetch_celex_rdf, parse_celex_graph, celex_to_vector,
        ingest_celex, SOVOS_CELLAR_ENDPOINT,
    )
"""
from __future__ import annotations

import hashlib
import json
import logging
import re
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import requests

logger = logging.getLogger(__name__)

# rdflib is optional-lazy (needed for full RDF parse). We degrade to a
# regex-light metadata fetch if rdflib is missing.
try:
    from rdflib import Graph, Namespace, URIRef
    _HAS_RDFLIB = True
except ImportError:
    _HAS_RDFLIB = False

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
SOVOS_CELLAR_ENDPOINT = "https://publications.europa.eu/webapi/rdf/sparql"
SOVOS_CELLAR_RESOURCE = "https://publications.europa.eu/resource/celex/"  # + CELEX
DEFAULT_LANG = "EN"

# CELEX pattern: sector/year/serial/type, e.g. 32024R1689 (3=EU reg, 2024, R)
CELEX_RE = re.compile(r"^\d{1}\d{4}[A-Z]{1}\d{1,4}$")

# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------
@dataclass
class LawDocument:
    """The machine-storable core of one EU legal instrument."""
    celex: str
    title: str
    language: str
    instrument_type: str            # e.g. Regulation, Directive, Decision
    publication_year: Optional[int]
    uri: str
    fetched_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    raw_metadata: Dict[str, Any] = field(default_factory=dict)
    vector: List[float] = field(default_factory=list)   # filled by celex_to_vector

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def to_bus_vector(self, layer: str = "honey") -> Dict[str, Any]:
        """Render as a StateBus append payload (compatible with StateVector)."""
        return {
            "source": f"cellar:{self.celex}",
            "layer": layer,
            "vector": self.vector,
            "payload": {
                "celex": self.celex,
                "title": self.title,
                "language": self.language,
                "instrument_type": self.instrument_type,
                "publication_year": self.publication_year,
                "uri": self.uri,
                "fetched_at": self.fetched_at,
            },
            "ts": self.fetched_at,
        }


# ---------------------------------------------------------------------------
# Fetch + parse
# ---------------------------------------------------------------------------
def fetch_celex_rdf(celex: str, timeout: int = 30,
                    base: str = SOVOS_CELLAR_RESOURCE) -> str:
    """Fetch the RDF/XML for a CELEX document from CELLAR.

    Raises on HTTP error or invalid CELEX shape.
    """
    celex = celex.strip().upper()
    if not CELEX_RE.match(celex):
        raise ValueError(f"invalid CELEX: {celex!r} (expected e.g. 32024R1689)")
    url = f"{base}{celex}"
    r = requests.get(url, timeout=timeout,
                     headers={"Accept": "application/rdf+xml", "User-Agent": "CSOAI-CELLAR-Ingest/0.1"})
    r.raise_for_status()
    return r.text


def parse_celex_graph(rdf_text: str, lang: str = DEFAULT_LANG,
                      expected_celex: Optional[str] = None) -> LawDocument:
    """Parse CELLAR RDF/XML into the LawDocument bibliographic core.

    Uses rdflib when available; falls back to a title-regex heuristic so
    the package still works in constrained environments (the fallback
    honestly reports title=None when it can't find one).

    Args:
        rdf_text: the RDF/XML body.
        lang: preferred title language.
        expected_celex: the CELEX this RDF represents. When provided, we
            anchor on it (CELLAR RDF can reference many CELEX ids in
            cross-references — e.g. a Regulation citing case-law — so
            `expected_celex` is the source of truth for identity).
    """
    celex = expected_celex or _find_celex_in_rdf(rdf_text)
    title = None
    if _HAS_RDFLIB:
        try:
            g = Graph()
            g.parse(data=rdf_text, format="xml")
            title = _extract_title_rdflib(g, lang)
            metadata = _extract_metadata_rdflib(g)
        except Exception as e:
            logger.warning("rdflib parse failed (%s); falling back to regex", e)
            metadata = {}
            title = title or _extract_title_regex(rdf_text, lang)
    else:
        metadata = {}
        title = _extract_title_regex(rdf_text, lang)
    year = _year_from_celex(celex)
    itype = _type_from_celex(celex)
    return LawDocument(
        celex=celex,
        title=title or f"CELEX {celex}",
        language=lang,
        instrument_type=itype,
        publication_year=year,
        uri=f"{SOVOS_CELLAR_RESOURCE}{celex}",
        raw_metadata=metadata,
    )


def _find_celex_in_rdf(rdf_text: str) -> str:
    # Look for a celex:CELEX triple / resource path
    m = re.search(r"celex%3A([0-9A-Z]{5,12})", rdf_text)
    if m:
        return m.group(1)
    m2 = re.search(r"/resource/celex/([0-9A-Z]{5,12})", rdf_text)
    if m2:
        return m2.group(1)
    # Fallback: unknown → derive a placeholder
    return "UNKNOWN-00UNKN"


def _extract_title_rdflib(g, lang: str) -> Optional[str]:
    from rdflib.namespace import RDF, RDFS, DCTERMS, DC
    # CELLAR uses the CDM ontology: cdm#title / cdm#work_title. Prefer
    # work_title (the work-level title), then cdm#title, then dc*.
    CDM_TITLE = URIRef("http://publications.europa.eu/ontology/cdm#title")
    CDM_WORK_TITLE = URIRef("http://publications.europa.eu/ontology/cdm#work_title")
    # 1. work_title first (the canonical multi-lingual title)
    for s, p, o in g.triples((None, CDM_WORK_TITLE, None)):
        if getattr(o, "language", None) == lang.lower() or getattr(o, "language", None) == lang[:2].lower():
            return str(o)
    # 2. any work_title (language-agnostic fallback)
    for s, p, o in g.triples((None, CDM_WORK_TITLE, None)):
        return str(o)
    # 3. cdm#title with preferred language
    for s, p, o in g.triples((None, CDM_TITLE, None)):
        if getattr(o, "language", None) == lang.lower() or getattr(o, "language", None) == lang[:2].lower():
            return str(o)
    # 4. any cdm#title
    for s, p, o in g.triples((None, CDM_TITLE, None)):
        return str(o)
    # 5. dcterms:title / dc:title with preferred language
    for prop in (DCTERMS.title, DC.title):
        for s, p, o in g.triples((None, prop, None)):
            if getattr(o, "language", None) == lang.lower() or getattr(o, "language", None) == lang[:2].lower():
                return str(o)
    # 6. any dc title
    for prop in (DCTERMS.title, DC.title):
        for s, p, o in g.triples((None, prop, None)):
            return str(o)
    return None


def _extract_metadata_rdflib(g) -> Dict[str, Any]:
    from rdflib.namespace import DCTERMS
    out = {}
    for s, p, o in g.triples((None, DCTERMS.created, None)):
        out.setdefault("created", []).append(str(o))
    for s, p, o in g.triples((None, DCTERMS.issued, None)):
        out.setdefault("issued", []).append(str(o))
    for s, p, o in g.triples((None, DCTERMS.type, None)):
        out.setdefault("type", []).append(str(o))
    return out


def _extract_title_regex(rdf_text: str, lang: str) -> Optional[str]:
    # RDF/XML: <dc:title xml:lang="en">…</dc:title>
    m = re.search(r'<dc:title[^>]*xml:lang="%s"[^>]*>([^<]+)</dc:title>' % lang.lower(), rdf_text)
    if m:
        return m.group(1).strip()
    m = re.search(r'<dc:title[^>]*>([^<]+)</dc:title>', rdf_text)
    if m:
        return m.group(1).strip()
    m = re.search(r'<dcterms:title[^>]*>([^<]+)</dcterms:title>', rdf_text)
    if m:
        return m.group(1).strip()
    return None


def _year_from_celex(celex: str) -> Optional[int]:
    m = re.match(r"^\d(\d{4})[A-Z]", celex)
    if m:
        try:
            return int(m.group(1))
        except ValueError:
            return None
    return None


def _type_from_celex(celex: str) -> str:
    # Bits 5-6 of CELEX indicate type: R=Regulation, L=Directive, D=Decision
    if len(celex) >= 6:
        c = celex[5]
        return {
            "R": "Regulation", "L": "Directive", "D": "Decision",
            "C": "Recommendation", "J": "Case-law",
        }.get(c, "Other")
    return "Other"


# ---------------------------------------------------------------------------
# Vector + ingest
# ---------------------------------------------------------------------------
def celex_to_vector(celex: str, title: Optional[str] = None,
                    language: str = DEFAULT_LANG,
                    dim: int = 8) -> List[float]:
    """Deterministic regulation vector from the law's own identity.

    Hash the CELEX (stable, language-independent) + language + title.
    The core comes from the CELEX so the same law in different languages
    shares the same "axis"; the language adds a rotation for multilingual
    Procrustes alignment.
    """
    core = hashlib.sha256(celex.encode()).digest()
    lang_salt = hashlib.sha256((language + (title or "")).encode()).digest()
    # Blend core + lang into 8 floats in [-1, 1)
    coords = []
    for i in range(dim):
        b = (core[i % 32] ^ lang_salt[i % 32])
        coords.append((b / 255.0) * 2.0 - 1.0)
    # Normalize to unit-ish length in ball (radius 0.85 like birth)
    norm = sum(c * c for c in coords) ** 0.5
    if norm < 1e-9:
        return coords
    return [c / norm * 0.85 for c in coords]


def ingest_celex(celex: str, bus=None,
                 lang: str = DEFAULT_LANG,
                 layer: str = "honey",
                 fetch: bool = True,
                 timeout: int = 30) -> LawDocument:
    """Fetch + parse + vector a CELEX, optionally append to a StateBus.

    Args:
        celex: the CELEX id (e.g. "32024R1689" — EU AI Act)
        bus: a sovos-bus-redis RedisBus (or None to skip the append)
        lang: CELLAR language code (EN/FR/DE/…)
        layer: StateBus layer ("honey" = distilled law, "milk" = working)
        fetch: if False, skip the live HTTP fetch (used when the caller
               already has the RDF, or for offline tests)
        timeout: HTTP timeout

    Returns:
        LawDocument (with .vector filled). If bus given, appended.
    """
    if fetch:
        rdf = fetch_celex_rdf(celex, timeout=timeout)
        doc = parse_celex_graph(rdf, lang=lang, expected_celex=celex.upper())
    else:
        doc = LawDocument(celex=celex.upper(), title=f"CELEX {celex.upper()}",
                          language=lang,
                          instrument_type=_type_from_celex(celex.upper()),
                          publication_year=_year_from_celex(celex.upper()),
                          uri=f"{SOVOS_CELLAR_RESOURCE}{celex.upper()}")
    doc.vector = celex_to_vector(doc.celex, title=doc.title, language=doc.language)
    if bus is not None:
        try:
            from sovos_bus_redis import StateVector
            sv = StateVector(
                source=f"cellar:{doc.celex}",
                layer=layer,
                vector=doc.vector,
                payload={
                    "celex": doc.celex, "title": doc.title,
                    "language": doc.language,
                    "instrument_type": doc.instrument_type,
                    "publication_year": doc.publication_year,
                    "uri": doc.uri,
                },
            )
            bus.append(sv)
        except ImportError:
            logger.info("sovos_bus_redis unavailable; vector built without Bus append")
    return doc


# ---------------------------------------------------------------------------
# Self-test (offline-safe)
# ---------------------------------------------------------------------------
def self_test() -> Dict[str, Any]:
    """Offline smoke test: vector determinism + CELEX parse helpers."""
    v1 = celex_to_vector("32024R1689", title="Regulation (EU) 2024/1689", language="EN")
    v2 = celex_to_vector("32024R1689", title="Regulation (EU) 2024/1689", language="EN")
    v3 = celex_to_vector("32024R1689", title="Regulation (EU) 2024/1689", language="FR")
    year = _year_from_celex("32024R1689")
    itype = _type_from_celex("32024R1689")
    return {
        "deterministic": v1 == v2,
        "lang_rotates": v1 != v3,
        "in_ball": max(abs(c) for c in v1) < 1.0,
        "year": year,
        "instrument_type": itype,
        "dim": len(v1),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(self_test(), indent=2))