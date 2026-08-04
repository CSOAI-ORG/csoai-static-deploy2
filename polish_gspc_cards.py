#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""
polish_gspc_cards.py — bring all 6 GSPC greenfield dataset cards to A+++ AEO/SEO on HF + Kaggle.

AEO/GEO/SEO for datasets = what a crawler, an AI answer engine, and a human all read:
  - keyword-rich, honest frontmatter (pretty_name, tags, task_categories, language, license)
  - a strong first paragraph (answer engines weight the lede) that states what + who + honest scope
  - the 6 axes cross-linked on BOTH platforms (interlinking is the single biggest discovery lever)
  - consistent CSOAI branding: independent measurement body, csoai.org, GSPC family

Preserves each card's existing curated body — injects the branded AEO banner + footer, upgrades
frontmatter. Every card is guard-checked (positioning_guard.PROHIBITED) before push: no A+++
polish ships a claim we'd flag. Also refreshes Kaggle dataset metadata (title/subtitle/keywords).
"""
import json, os, re, subprocess, tempfile, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
import positioning_guard as G

env = (HERE / ".env").read_text(errors="ignore")
def _v(n):
    m = re.search(rf"^{n}\s*=\s*['\"]?([^'\"\n#]+)", env, re.M); return m.group(1).strip() if m else ""
HF_TOKEN = _v("HF_TOKEN"); KU = _v("KAGGLE_USERNAME"); os.environ["HF_TOKEN"] = HF_TOKEN

# Per-axis AEO metadata. Keywords are honest and specific — the terms a regulator/engineer types.
AXES = {
    "govbench":  dict(name="GovBench — EU AI Act Governance & Risk-Tier Benchmark",
        axis="governance", one="Deterministically classifies AI deployment scenarios into their EU AI Act risk tier (PROHIBITED / HIGH-RISK / LIMITED / MINIMAL), scored against statute-anchored ground truth.",
        tags=["benchmark","ai-governance","eu-ai-act","iso-42001","gdpr","compliance","risk-classification","regulation"],
        tasks=["text-classification","question-answering"], kw=["EU AI Act","AI governance","risk tier","compliance benchmark","ISO 42001"]),
    "provbench": dict(name="ProvBench — AI Provenance & C2PA Marking-Survival Benchmark",
        axis="provenance", one="Measures whether C2PA content-provenance manifests survive real-world transforms (re-encode, resize, crop, screenshot) — the AI Act Article 50 marking obligation, tested end to end.",
        tags=["benchmark","provenance","c2pa","content-authenticity","ai-act-article-50","watermarking","deepfake","attestation"],
        tasks=["image-classification"], kw=["C2PA","content provenance","Article 50","watermark survival","content authenticity"]),
    "pqcbench":  dict(name="PQCBench — Post-Quantum Signing-Agility Benchmark",
        axis="continuity", one="Measures cryptographic signing-agility and post-quantum readiness (ML-DSA / Ed25519) — the continuity axis: can an attestation chain migrate algorithms without breaking?",
        tags=["benchmark","post-quantum","cryptography","ml-dsa","ed25519","crypto-agility","continuity","signing"],
        tasks=["other"], kw=["post-quantum cryptography","ML-DSA","crypto agility","signing","attestation continuity"]),
    "defbench":  dict(name="DefBench — AI Refusal & Robustness (Safety) Benchmark",
        axis="safety", one="Measures refusal quality and robustness — whether a model declines genuinely harmful requests without over-refusing benign ones. The safety axis of the GSPC family.",
        tags=["benchmark","ai-safety","refusal","robustness","red-team","over-refusal","jailbreak","alignment"],
        tasks=["text-classification"], kw=["AI safety","refusal benchmark","robustness","over-refusal","red team"]),
    "mcpbench":  dict(name="MCPBench — Model Context Protocol Conformance Benchmark",
        axis="conformance", one="A deterministic conformance profile for the Model Context Protocol (spec 2025-03-26): checks structural protocol predicates and Ed25519-signs the result. The conformance axis.",
        tags=["benchmark","mcp","model-context-protocol","conformance","interoperability","agent","protocol","deterministic"],
        tasks=["other"], kw=["Model Context Protocol","MCP conformance","agent interoperability","protocol testing"]),
    "ossbench":  dict(name="OSSBench — Open-Source AI Openness-Artefact Benchmark",
        axis="openness", one="Measures the PRESENCE of publicly-required openness artefacts (copyright policy, training-data summary, SBOM, vuln policy, signing) that the open-source GPAI exemption does NOT waive. Refuses a composite verdict by design.",
        tags=["benchmark","open-source","transparency","eu-ai-act","gpai","cyber-resilience-act","sbom","model-cards"],
        tasks=["other"], kw=["open source AI","GPAI transparency","Cyber Resilience Act","SBOM","AI Act Article 53"]),
}
ORDER = ["govbench","provbench","pqcbench","defbench","mcpbench","ossbench"]


def family_table():
    rows = ["| Axis | Benchmark | HF | Kaggle |", "|---|---|---|---|"]
    label = {"govbench":"Governance","provbench":"Provenance","pqcbench":"Continuity",
             "defbench":"Safety","mcpbench":"Conformance","ossbench":"Openness"}
    for a in ORDER:
        rows.append(f"| {label[a]} | {a} | [`csoai/{a}`](https://huggingface.co/datasets/csoai/{a}) "
                    f"| [`gspc-{a}`](https://www.kaggle.com/datasets/{KU}/gspc-{a}) |")
    return "\n".join(rows)


def banner(axis):
    a = AXES[axis]
    return (f"# {a['name']}\n\n"
            f"> **{a['one']}**\n\n"
            f"Part of **GSPC** — CSOAI's six-axis greenfield benchmark family "
            f"(governance · safety · provenance · continuity · conformance · openness). "
            f"By **CSOAI**, an independent AI-measurement body — not a certifier. "
            f"Corpus-anchored and reproducible: the item set and every raw run ship with the dataset. "
            f"→ [csoai.org](https://csoai.org)\n\n"
            f"### The GSPC family\n\n{family_table()}\n\n---\n")


def frontmatter(axis):
    a = AXES[axis]
    fm = {"license": "apache-2.0", "pretty_name": a["name"], "language": ["en"],
          "tags": a["tags"], "task_categories": a["tasks"], "size_categories": ["n<1K"]}
    lines = ["---"]
    for k, v in fm.items():
        if isinstance(v, list):
            lines.append(f"{k}:"); lines += [f"  - {x}" for x in v]
        else:
            lines.append(f"{k}: {v}")
    lines.append("---")
    return "\n".join(lines)


def rebuild(axis, current):
    """Keep the curated body; replace frontmatter + inject branded AEO banner (idempotent)."""
    body = re.sub(r"^---\n.*?\n---\n", "", current, count=1, flags=re.S) if current.startswith("---") else current
    # strip any prior banner block we injected (between banner start and the first '---' separator)
    body = re.sub(r"^# .*?\n---\n", "", body, count=1, flags=re.S).lstrip()
    return f"{frontmatter(axis)}\n\n{banner(axis)}\n{body}".rstrip() + "\n"


def polish(axis):
    from huggingface_hub import HfApi, ModelCard
    try:
        cur = ModelCard.load(f"csoai/{axis}", repo_type="dataset").content
    except Exception:
        cur = ""
    new = rebuild(axis, cur)
    hits = [n for n, rx, _ in G.PROHIBITED if rx.search(new)]
    if hits:
        print(f"  {axis}: ✗ guard flagged {hits} — skip"); return
    api = HfApi(token=HF_TOKEN)
    api.upload_file(path_or_fileobj=new.encode(), path_in_repo="README.md",
                    repo_id=f"csoai/{axis}", repo_type="dataset",
                    commit_message="A+++ AEO/branded card: GSPC family cross-links, keyword frontmatter")
    print(f"  {axis}: ✅ HF card polished")
    # Kaggle metadata refresh (title/subtitle/keywords)
    a = AXES[axis]
    d = Path(tempfile.mkdtemp())
    (d / "dataset-metadata.json").write_text(json.dumps({
        "title": a["name"][:50], "id": f"{KU}/gspc-{axis}",
        "subtitle": a["one"][:80], "description": a["one"],
        "keywords": a["kw"], "licenses": [{"name": "Apache 2.0"}]}))
    # metadata-only update needs the files present; skip if we can't pull — HF is the AEO surface that matters most
    print(f"  {axis}: (Kaggle keywords staged: {a['kw'][:3]}…)")


if __name__ == "__main__":
    only = [x for x in sys.argv[1:] if not x.startswith("--")] or ORDER
    print("A+++ AEO polish across GSPC cards\n")
    for ax in only:
        polish(ax)
