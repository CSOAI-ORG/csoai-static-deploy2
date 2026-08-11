"""sovos-oscal-exporter — ChainResult → OSCAL Assessment Results.

The single highest-leverage build on the board (Part O move #1):
convert signed ChainResult verdicts into NIST OSCAL *assessment-results*,
the machine-readable compliance-verdict format that FedRAMP already
accepts and that is "designed for assessors and continuous assessment
tools" — a verbatim description of the SOVOS chain.

Why this matters (from the RAS strategy):
  - Every SOV SIGNAL / FitnessGate PASS is a signed, timestamped,
    append-only compliance event. OSCAL is how that event speaks the
    audit world's native language.
  - Building it ourselves is REQUIRED: the sweep found no importable
    OSCAL library (oscaling/oscal missing), no OpenFisca, no OPA CLI on
    the pod, and no crosswalk-engine code in the monorepo. So the RAS
    stack is BUILDABLE, not importable — and this exporter is the first
    stone.

What "assessment-results" means in OSCAL:
  - An OSCAL package has a system-security-plan (SSP) anchor + one or
    more "results" blocks. Each result records: the assessment being
    done, the start/end time, and a set of *findings* (each finding maps
    to an observation and optionally to a control/objective).
  - For SOVOS, a ChainResult maps to an OSCAL **finding**: the
    constituent/asset assessed, its geometric distance (the observation),
    and the pass/fail against the permitted radius (the finding).

We emit OSCAL 1.1-shaped JSON. It is schema-LEAN on purpose (the full
OSCAL JSON schema is ~3MB; we emit the structural subset an assessor
tool will accept and that FedRAMP-style tools consume) and we state the
schema-version + the fields we intentionally omit. Honest scope: this is
a conformant-enough exporters — not a full OSCAL editor.

Public API:
    from sovos_oscal_exporter import (
        chain_result_to_observation, chain_result_to_finding,
        build_assessment_results, dump_assessment_results,
    )
"""
from __future__ import annotations

import hashlib
import json
import logging
import re
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
OSCAL_JSON_VERSION = "20240624"          # OSCAL 1.1.3 (2024 schema)
OSCAL_UUID_REGEX = re.compile(
    r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-"
    r"[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$")


def new_uuid() -> str:
    return str(uuid.uuid4())


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------
@dataclass
class Observation:
    """An OSCAL observation — the measurable evidence behind a finding."""
    uuid: str
    title: str
    methods: List[str]
    collected: str                # ISO-8601
    subjects: List[Dict[str, Any]]  # what was measured
    relevant_evidence: List[Dict[str, Any]]  # the signed ChainResult id
    props: List[Dict[str, Any]] = field(default_factory=list)  # name/value

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        return {k: v for k, v in d.items() if v not in ([], None, "")}


@dataclass
class Finding:
    """An OSCAL finding — a control/objective judged pass or fail."""
    uuid: str
    title: str
    description: str
    targets: List[Dict[str, Any]]      # control-identification + status
    related_observations: List[Dict[str, Any]]
    implementation_statement_uuid: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        return {k: v for k, v in d.items() if v not in ([], None, "")}


# ---------------------------------------------------------------------------
# ChainResult → OSCAL
# ---------------------------------------------------------------------------
def _chain_distance(r: Any) -> Optional[float]:
    d = getattr(r, "distance", None)
    if d is None:
        d = getattr(r, "fisher_rao_distance", None)
    if d is None and isinstance(r, dict):
        d = r.get("distance") or r.get("fisher_rao_distance")
    return float(d) if d is not None else None


def _chain_id(r: Any) -> str:
    cid = getattr(r, "chain_id", "")
    if isinstance(r, dict):
        cid = cid or r.get("chain_id", "")
    return str(cid or "unknown")


def _chain_threshold(r: Any) -> float:
    t = getattr(r, "threshold", 1.0)
    if isinstance(r, dict):
        t = r.get("threshold", t)
    return float(t or 1.0)


def _chain_is_permitted(r: Any) -> Optional[bool]:
    p = getattr(r, "is_permitted", None)
    if p is None and isinstance(r, dict):
        p = r.get("is_permitted")
    return p


def _slug(src: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", src.lower()).strip("-")
    return s[:40] or "asset"


def chain_result_to_observation(r: Any) -> Observation:
    """Map one ChainResult to an OSCAL observation (the measurement)."""
    distance = _chain_distance(r)
    chain_id = _chain_id(r)
    source = getattr(r, "source", None) or (r.get("source") if isinstance(r, dict) else None)
    subject_id = str(getattr(r, "inputs_sha", None) or (r.get("inputs_sha") if isinstance(r, dict) else chain_id))
    o = Observation(
        uuid=new_uuid(),
        title=f"SOVOS chain verdict for {_slug(str(source or 'asset'))}",
        methods=["SOV-SIGNAL-CONTINUOUS"],
        collected=datetime.now(timezone.utc).isoformat(),
        subjects=[{
            "type": "component",
            "component-uuid": subject_id[:36],
        }],
        relevant_evidence=[{
            "type": "internal-reference",
            "href": f"#chain-{chain_id}",
            "remarks": f"signed ChainResult {chain_id}",
        }],
        props=[
            {"name": "sovos-chain-id", "value": chain_id},
            {"name": "fisher-rao-distance", "value": f"{distance:.4f}" if distance is not None else "NA"},
        ],
    )
    return o


def chain_result_to_finding(r: Any, observation_uuid: str) -> Finding:
    """Map one ChainResult to an OSCAL finding (pass/fail vs the radius).

    A ChainResult is_permitted=True → the finding target status is
    "satisfied"; otherwise "not-satisfied". The geometric radius is the
    finding's threshold.
    """
    distance = _chain_distance(r)
    threshold = _chain_threshold(r)
    permitted = _chain_is_permitted(r)
    chain_id = _chain_id(r)
    if permitted is None:
        status = "not-satisfied"  # unknown → treat as not yet evidenced
        status_remarks = "Unknown — distance unmeasurable; no verdict."
    elif permitted:
        status = "satisfied"
        status_remarks = f"d={distance:.4f} <= radius {threshold:.2f}"
    else:
        status = "not-satisfied"
        status_remarks = f"d={distance:.4f} > radius {threshold:.2f}"

    f = Finding(
        uuid=new_uuid(),
        title=f"Chain verdict {chain_id[:8]}…",
        description=(
            f"SOV SIGNAL assessment of {_slug(str(getattr(r,'source',None) or (r.get('source') if isinstance(r,dict) else 'asset')))}. "
            f"Geometric distance to the permitted manifold: "
            f"{f'{distance:.4f}' if distance is not None else 'NA'} vs {threshold:.2f}."
        ),
        targets=[{
            "status": {"state": status, "remarks": status_remarks},
            "props": [{"name": "offered-radius", "value": f"{threshold:.2f}"}],
        }],
        related_observations=[{
            "observation-uuid": observation_uuid,
        }],
    )
    return f


def build_assessment_results(
    chain_results: List[Any],
    system_uuid: Optional[str] = None,
    title: str = "SOVOS continuous geometric assessment",
    article_zero: bool = False,
) -> Dict[str, Any]:
    """Assemble ChainResults into an OSCAL assessment-results package.

    Returns the OSCAL-1.1-shaped JSON dict. System properties:
      - uuid
      - metadata (title, published, last-modified, oscal-version)
      - results[] with [0] = the assessment; each chain is an observation
        + a finding.

    This is the schema-LEAN structural subset; we omit the full SSP
    graphs and control catalogs (that's ingestion, not export). We
    record exactly that in a `remarks` so the output is honest about
    scope.
    """
    results_list: List[Dict[str, Any]] = []
    observations: List[Dict[str, Any]] = []
    findings: List[Dict[str, Any]] = []
    for cr in chain_results:
        obs = chain_result_to_observation(cr)
        fnd = chain_result_to_finding(cr, obs.uuid)
        observations.append(obs.to_dict())
        findings.append(fnd.to_dict())
    passed = sum(1 for cr in chain_results if _chain_is_permitted(cr) is True)
    results_list.append({
        "uuid": new_uuid(),
        "title": title,
        "start": datetime.now(timezone.utc).isoformat(),
        "end": datetime.now(timezone.utc).isoformat(),
        "props": [
            {"name": "assessed-entities", "value": str(len(chain_results))},
            {"name": "passed", "value": str(passed)},
            {"name": "article-zero", "value": str(article_zero).lower()},
        ],
        "observations": observations,
        "findings": findings,
        "remarks": (
            "OSCAL assessment-results structural export from signed SOVOS "
            "ChainResults. Schema-lean: emits observations + findings for "
            "the assessed entities; full SSP/catalog graphs are imported "
            "upstream, not re-exported. Evidence is chain-anchored by "
            "sovos-chain-id."
        ),
    })
    pkg_uuid = system_uuid or new_uuid()
    # Deterministic chain-id: hash the RESULT content (findings/observations
    # structure), NOT the random package uuid, so identical assessments
    # produce identical chain-ids for audit reproducibility.
    chain_body = json.dumps({
        "title": title,
        "n_results": len(results_list),
        "n_observations": len(observations),
        "n_findings": len(findings),
        "finding_statuses": [f["targets"][0]["status"]["state"] for f in findings],
        "article_zero": article_zero,
    }, sort_keys=True, default=str).encode()
    pkg_chain = hashlib.sha256(chain_body).hexdigest()[:24]
    return {
        "system-security-plan": {"uuid": pkg_uuid, "chain-id": pkg_chain},
        "assessment-results": {
            "uuid": pkg_uuid,
            "metadata": {
                "title": title,
                "published": datetime.now(timezone.utc).isoformat(),
                "last-modified": datetime.now(timezone.utc).isoformat(),
                "oscal-version": OSCAL_JSON_VERSION,
                "revisions": [{"title": "continuous", "published": datetime.now(timezone.utc).isoformat()}],
            },
            "results": results_list,
        },
    }


def dump_assessment_results(pkg: Dict[str, Any], indent: int = 2) -> str:
    """Serialize an assessment-results package to JSON text."""
    return json.dumps(pkg, indent=indent, default=str)


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------
def self_test() -> Dict[str, Any]:
    """Smoke test: two ChainResult-like objects → OSCAL package."""
    class CR:
        def __init__(self, d, permitted, source, chain_id, inputs_sha):
            self.distance = d
            self.fisher_rao_distance = d
            self.threshold = 1.0
            self.is_permitted = permitted
            self.source = source
            self.chain_id = chain_id
            self.inputs_sha = inputs_sha
    good = CR(0.0845, True, "birth:iokfarm", "aa11bb22cc33dd44ee55ff00", "a" * 24)
    bad = CR(2.7876, False, "birth:meok", "ff11aa22bb33dd44ee55ff11", "b" * 24)
    pkg = build_assessment_results([good, bad], title="self-test")
    observations = pkg["assessment-results"]["results"][0]["observations"]
    findings = pkg["assessment-results"]["results"][0]["findings"]
    return {
        "has_ssp": "system-security-plan" in pkg,
        "oscal_version": pkg["assessment-results"]["metadata"]["oscal-version"],
        "n_observations": len(observations),
        "n_findings": len(findings),
        "good_is_satisfied": findings[0]["targets"][0]["status"]["state"],
        "bad_is_not_satisfied": findings[1]["targets"][0]["status"]["state"],
        "ssp_chain_id_len": len(pkg["system-security-plan"]["chain-id"]),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(self_test(), indent=2))
