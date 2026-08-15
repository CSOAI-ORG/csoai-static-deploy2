"""sovos-projector — the compile pipeline.

Reads assets/ once, projects to every external platform:
  - exports/huggingface/  → model cards, dataset cards, space configs
  - exports/kaggle/       → dataset metadata.json, notebook templates
  - exports/pypi/         → per-package README.md + pyproject.toml overlays
  - exports/arenas/       → submission manifests per arena

Nothing is hand-edited on a platform. If a Kaggle dataset is deprecated,
it's deprecated in assets/MANIFEST.md and the pipeline emits a tombstone.
"""
from __future__ import annotations

import hashlib
import json
import re
import shutil
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


# ---------------------------------------------------------------------------
# Manifest loader
# ---------------------------------------------------------------------------
@dataclass
class AssetRecord:
    asset_id: str
    asset_type: str           # "model_card" | "benchmark" | "sigil" | "card_template" | "space_card"
    source_path: Path         # relative to SOVOS root
    status: str               # "REAL" | "SCAFFOLD"
    description: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)


def load_manifest(sovos_root: Path) -> List[AssetRecord]:
    """Parse assets/MANIFEST.md into structured records.

    The manifest uses Markdown tables; this parser extracts them.
    """
    manifest_path = sovos_root / "assets" / "MANIFEST.md"
    records: List[AssetRecord] = []
    current_section = ""
    if not manifest_path.exists():
        return records
    for line in manifest_path.read_text().splitlines():
        line = line.strip()
        if line.startswith("## "):
            current_section = line[3:].strip()
            continue
        if not line.startswith("|") or "Asset ID" in line or "---" in line:
            continue
        cols = [c.strip() for c in line.strip("|").split("|")]
        if len(cols) < 3:
            continue
        asset_id = cols[0]
        source = cols[1]
        asset_type = cols[2] if len(cols) >= 3 else "unknown"
        status = "REAL"
        if len(cols) >= 4 and ("SCAFFOLD" in cols[3] or "scaffold" in cols[3].lower()):
            status = "SCAFFOLD"
        source_path = (sovos_root / source).resolve()
        records.append(AssetRecord(
            asset_id=asset_id,
            asset_type=asset_type,
            source_path=source_path,
            status=status,
            description=current_section,
        ))
    return records


# ---------------------------------------------------------------------------
# Footer — every projection carries the same identity
# ---------------------------------------------------------------------------
CSOAI_FOOTER = """
---

*CSOAI Ltd · UK Companies House #16939677*
*Generated from SOVOS assets/ — DO NOT hand-edit. Edit MANIFEST.md and re-run `make project`.*
"""


def add_footer(markdown: str) -> str:
    """Append the standard CSOAI footer to a markdown body."""
    if "Generated from SOVOS assets/" in markdown:
        return markdown  # already has footer
    return markdown.rstrip() + "\n" + CSOAI_FOOTER


def add_3kb_sigil_reference(markdown: str, sigil_id: str, sovos_root: Path) -> str:
    """Append a line linking to the 3KB sigil card (the 'visual soul')."""
    sigil_path = sovos_root / "assets" / "cards" / f"{sigil_id}.3kb"
    if not sigil_path.exists():
        return markdown
    sigil_size = sigil_path.stat().st_size
    return (markdown.rstrip() +
            f"\n\n**3KB Sigil:** `{sigil_id}` ({sigil_size} bytes) — "
            f"`assets/cards/{sigil_id}.3kb`\n")


# ---------------------------------------------------------------------------
# HuggingFace projection
# ---------------------------------------------------------------------------
@dataclass
class HFModelCard:
    repo_id: str                # "csoai/sov33-ultimate-sovereign"
    card_markdown: str
    yaml_metadata: Dict[str, Any]
    sha256: str


def project_huggingface(record: AssetRecord, sovos_root: Path) -> HFModelCard:
    """Project a model_card asset to HuggingFace format.

    The HF model card format requires YAML frontmatter at the top
    (between --- markers). We parse the existing card or generate a
    minimal one from the asset_id + status.
    """
    text = record.source_path.read_text() if record.source_path.exists() else ""
    # Extract YAML frontmatter if present
    yaml_meta: Dict[str, Any] = {}
    body = text
    m = re.match(r"^---\n(.+?)\n---\n(.*)", text, flags=re.DOTALL)
    if m:
        try:
            import yaml  # optional
            yaml_meta = yaml.safe_load(m.group(1)) or {}
        except ImportError:
            # Fallback: naive parsing
            for line in m.group(1).splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    yaml_meta[k.strip()] = v.strip()
        body = m.group(2)

    # Ensure required HF keys
    yaml_meta.setdefault("license", "apache-2.0")
    yaml_meta.setdefault("tags", [])
    if isinstance(yaml_meta["tags"], list) and "sov-governed" not in yaml_meta["tags"]:
        yaml_meta["tags"].append("sov-governed")
    yaml_meta.setdefault("library_name", "transformers")
    yaml_meta["asset_id"] = record.asset_id
    yaml_meta["asset_status"] = record.status
    yaml_meta["generated_at"] = datetime.now(timezone.utc).isoformat()

    # Reassemble with the standard footer
    body = add_footer(body)
    body = add_3kb_sigil_reference(body, "sovos_GOV", sovos_root)
    new_text = f"---\n{json.dumps(yaml_meta, indent=2)}\n---\n{body}"

    # Deterministic sha: hash the content WITHOUT the generated_at timestamp
    deterministic_yaml = {k: v for k, v in yaml_meta.items() if k != "generated_at"}
    sha_input = f"---\n{json.dumps(deterministic_yaml, indent=2)}\n---\n{body}"
    sha = hashlib.sha256(sha_input.encode()).hexdigest()
    return HFModelCard(
        repo_id=f"csoai/{record.asset_id}",
        card_markdown=new_text,
        yaml_metadata=yaml_meta,
        sha256=sha,
    )


def project_huggingface_all(records: List[AssetRecord], sovos_root: Path,
                             export_dir: Path) -> List[HFModelCard]:
    """Project all model_card and space_card assets to HF."""
    export_dir.mkdir(parents=True, exist_ok=True)
    cards: List[HFModelCard] = []
    for rec in records:
        if rec.asset_type not in ("model_card", "space_card", "card_template"):
            continue
        card = project_huggingface(rec, sovos_root)
        card_path = export_dir / "cards" / f"{rec.asset_id}.README.md"
        card_path.parent.mkdir(parents=True, exist_ok=True)
        card_path.write_text(card.card_markdown)
        cards.append(card)
    # Write a manifest of what was projected
    manifest_out = export_dir / "projection_manifest.json"
    manifest_out.write_text(json.dumps({
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "platform": "huggingface",
        "n_projected": len(cards),
        "cards": [{"asset_id": c.repo_id, "sha256": c.sha256,
                    "status": next((r.status for r in records
                                    if c.repo_id.endswith(r.asset_id)), "?")}
                   for c in cards],
    }, indent=2))
    return cards


# ---------------------------------------------------------------------------
# Kaggle projection
# ---------------------------------------------------------------------------
@dataclass
class KaggleDatasetMetadata:
    slug: str                  # "nicktempleman/govbench-sov-v0-1"
    title: str
    subtitle: str
    description: str
    total_bytes: int
    file_count: int
    licenses: List[str]
    keywords: List[str]
    collaborators: List[str]


def project_kaggle(record: AssetRecord, sovos_root: Path) -> KaggleDatasetMetadata:
    """Project a benchmark asset to Kaggle dataset-metadata.json format."""
    text = ""
    if record.source_path.exists():
        text = record.source_path.read_text()
    # Try to extract dataset info from JSON benchmark
    if record.source_path.suffix == ".json":
        try:
            data = json.loads(text)
            text = data.get("description", json.dumps(data, indent=2))
            n_items = sum(1 for _ in (record.source_path.read_text().splitlines()[1:] or []))
        except json.JSONDecodeError:
            n_items = 0
    else:
        n_items = 0
    total_bytes = record.source_path.stat().st_size if record.source_path.exists() else 0
    desc = (text[:500] if text else f"SOVOS {record.asset_id} — projected from assets/.")
    desc = add_footer(desc)
    return KaggleDatasetMetadata(
        slug=f"nicktempleman/{record.asset_id}",
        title=record.asset_id,
        subtitle=f"From SOVOS monorepo — {record.status}",
        description=desc,
        total_bytes=total_bytes,
        file_count=1 if record.source_path.exists() else 0,
        licenses=["apache-2.0"],
        keywords=["sov", "governance", "compliance", "csoai"] + ([record.asset_id]),
        collaborators=["nicktempleman"],
    )


def project_kaggle_all(records: List[AssetRecord], sovos_root: Path,
                        export_dir: Path) -> List[KaggleDatasetMetadata]:
    """Project benchmark assets to Kaggle dataset-metadata.json."""
    export_dir.mkdir(parents=True, exist_ok=True)
    out: List[KaggleDatasetMetadata] = []
    for rec in records:
        if rec.asset_type != "benchmark":
            continue
        meta = project_kaggle(rec, sovos_root)
        meta_path = export_dir / "metadata" / f"{rec.asset_id}.dataset-metadata.json"
        meta_path.parent.mkdir(parents=True, exist_ok=True)
        meta_path.write_text(json.dumps(meta.__dict__, indent=2))
        out.append(meta)
    return out


# ---------------------------------------------------------------------------
# PyPI projection
# ---------------------------------------------------------------------------
def project_pypi_all(sovos_root: Path, export_dir: Path) -> List[Path]:
    """Project SOVOS package READMEs to PyPI-friendly format.

    For each package/*/pyproject.toml in the monorepo, copy its README
    (if present) into exports/pypi/<pkg_name>/README.md and add the footer.
    """
    export_dir.mkdir(parents=True, exist_ok=True)
    out_paths: List[Path] = []
    pkg_root = sovos_root / "packages"
    if not pkg_root.exists():
        return out_paths
    for pkg_dir in sorted(pkg_root.iterdir()):
        if not pkg_dir.is_dir():
            continue
        readme = pkg_dir / "README.md"
        if not readme.exists():
            continue
        text = add_footer(readme.read_text())
        out_path = export_dir / pkg_dir.name / "README.md"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(text)
        out_paths.append(out_path)
    return out_paths


# ---------------------------------------------------------------------------
# Arenas projection
# ---------------------------------------------------------------------------
@dataclass
class ArenaSubmission:
    arena_id: str              # "lmarena" | "safebench" | "fli-index" | "open-llm"
    asset_id: str              # which asset is being submitted
    submission_yaml: str       # the manifest to send
    deadline: Optional[str] = None


def project_arenas(records: List[AssetRecord], sovos_root: Path,
                    export_dir: Path) -> List[ArenaSubmission]:
    """Generate per-arena submission manifests.

    For each model asset, emit a YAML manifest describing the submission:
    - model card pointer (sha256)
    - GovBench scores
    - SOV SIGNAL composite
    """
    export_dir.mkdir(parents=True, exist_ok=True)
    out: List[ArenaSubmission] = []
    arenas = ["lmarena", "safebench", "fli-index", "open-llm-leaderboard", "kaggle-competition"]
    for rec in records:
        if rec.asset_type not in ("model_card", "benchmark"):
            continue
        for arena in arenas:
            sha = hashlib.sha256(rec.asset_id.encode()).hexdigest()[:16]
            yaml = (
                f"arena: {arena}\n"
                f"asset_id: {rec.asset_id}\n"
                f"asset_status: {rec.status}\n"
                f"asset_sha256: {sha}\n"
                f"submission_type: {rec.asset_type}\n"
                f"sovereign_org: CSOAI-ORG\n"
                f"submitted_at: {datetime.now(timezone.utc).isoformat()}\n"
                f"# NOTE: generated from SOVOS assets/ — do not hand-edit\n"
            )
            yaml_path = export_dir / arena / f"{rec.asset_id}.submission.yaml"
            yaml_path.parent.mkdir(parents=True, exist_ok=True)
            yaml_path.write_text(yaml)
            out.append(ArenaSubmission(arena_id=arena, asset_id=rec.asset_id,
                                       submission_yaml=yaml))
    return out


# ---------------------------------------------------------------------------
# Full projection orchestrator
# ---------------------------------------------------------------------------
@dataclass
class ProjectionResult:
    hf_cards: List[HFModelCard]
    kaggle_datasets: List[KaggleDatasetMetadata]
    pypi_readmes: List[Path]
    arena_submissions: List[ArenaSubmission]
    elapsed_seconds: float
    timestamp: str


def project_all(sovos_root: Path) -> ProjectionResult:
    """Run the full projection: assets/ → exports/{huggingface,kaggle,pypi,arenas}/."""
    t0 = datetime.now(timezone.utc)
    records = load_manifest(sovos_root)
    hf_cards = project_huggingface_all(records, sovos_root, sovos_root / "exports" / "huggingface")
    kaggle = project_kaggle_all(records, sovos_root, sovos_root / "exports" / "kaggle")
    pypi = project_pypi_all(sovos_root, sovos_root / "exports" / "pypi")
    arenas = project_arenas(records, sovos_root, sovos_root / "exports" / "arenas")
    t1 = datetime.now(timezone.utc)
    return ProjectionResult(
        hf_cards=hf_cards,
        kaggle_datasets=kaggle,
        pypi_readmes=pypi,
        arena_submissions=arenas,
        elapsed_seconds=(t1 - t0).total_seconds(),
        timestamp=t1.isoformat(),
    )


__all__ = [
    "AssetRecord", "load_manifest",
    "HFModelCard", "project_huggingface", "project_huggingface_all",
    "KaggleDatasetMetadata", "project_kaggle", "project_kaggle_all",
    "project_pypi_all",
    "ArenaSubmission", "project_arenas",
    "ProjectionResult", "project_all",
    "add_footer", "add_3kb_sigil_reference",
]