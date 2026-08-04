#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""
publish_gspc_axes.py — bring the 3 missing GSPC axes to parity on HF + Kaggle.

The 6 greenfields (gspc_axes/): govbench, provbench, pqcbench are full datasets on both
platforms; defbench, mcpbench, ossbench exist only as `-kaggle-items` on HF and are absent
from Kaggle. This publishes the missing three as full datasets on BOTH, with honest,
guard-checked dataset cards, so all 6 are correct on both platforms.

Honesty: every generated README/LEADERBOARD is checked against positioning_guard.PROHIBITED
BEFORE upload. A prohibited claim aborts that axis — we do not publish copy we would flag.
"""
import json, os, re, sys, subprocess, tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
RES = HERE / "benchmark-results"
import positioning_guard as G  # reuse the honesty register

env = (HERE / ".env").read_text(errors="ignore")
def _v(n):
    m = re.search(rf"^{n}\s*=\s*['\"]?([^'\"\n#]+)", env, re.M); return m.group(1).strip() if m else ""
HF_TOKEN = _v("HF_TOKEN"); KU = _v("KAGGLE_USERNAME"); os.environ["HF_TOKEN"] = HF_TOKEN

LICENSE = (HERE / "LICENSE")
APACHE = "Apache License 2.0 — see https://www.apache.org/licenses/LICENSE-2.0\nCopyright CSOAI Ltd (UK, Companies House 16939677).\n"

AXES = {
    "defbench": {
        "pretty": "DefBench — Refusal & Robustness Benchmark",
        "axis": "safety",
        "tags": ["benchmark", "ai-safety", "refusal", "robustness", "red-team"],
        "blurb": (
            "**DefBench** measures **refusal quality and robustness** — whether a model declines "
            "genuinely harmful requests while not over-refusing benign ones. It is the *safety* "
            "axis of CSOAI's GSPC benchmark family (governance · safety · provenance · continuity · "
            "conformance · openness).\n\n"
            "v0.1. Entrants include CSOAI's own `sov33` operator models alongside a public baseline. "
            "Scored deterministically (refusal_rate + robustness), every raw per-model run published.\n\n"
            "**Honest scope.** v0.1 with a small entrant set — read the numbers as directional, not a "
            "settled ranking. A refusal metric measures *behaviour on a fixed prompt set*, not whether "
            "a model is 'safe' in any absolute sense."),
    },
    "mcpbench": {
        "pretty": "MCPBench — Model Context Protocol Conformance",
        "axis": "conformance",
        "tags": ["benchmark", "mcp", "conformance", "protocol", "deterministic"],
        "blurb": (
            "**MCPBench** is a **deterministic conformance profile** for the Model Context Protocol "
            "(spec `2025-03-26`). It checks structural protocol predicates against fixed records and "
            "**Ed25519-signs** the result. It is the *conformance* axis of CSOAI's GSPC family.\n\n"
            "**Honest scope.** Pass/fail here is *structural conformance to the protocol*, not a quality "
            "or security judgement about a server. A conformant server can still be badly designed; a "
            "non-conformant one can still be useful. The signature makes each result recomputable."),
    },
    "ossbench": {
        "pretty": "OSSBench (SOV-OSS) — Openness-Artefact Presence",
        "axis": "openness",
        "tags": ["benchmark", "open-source", "transparency", "eu-ai-act", "gpai"],
        "blurb": (
            "**OSSBench** measures the **presence** of publicly-required openness artefacts "
            "(copyright policy, training-data summary, license) on a subject's public surface, against "
            "named provisions. It is the *openness* axis of CSOAI's GSPC family.\n\n"
            "**Honest scope — this benchmark refuses a verdict by design.** It emits **no composite "
            "score** and **no adequacy judgement**: presence is not sufficiency, and judging sufficiency "
            "is adjudication we do not perform. It also does **not** decide whether a subject *is* a GPAI "
            "model or an Open-Source Steward — those are legal classifications. Per-provision presence "
            "only."),
    },
}

FOOTER = (
    "\n## About\n\n"
    "CSOAI is an **independent measurement body** — not a notified body, not a certifier. GSPC "
    "benchmarks are corpus-anchored and reproducible: the item set and every raw run ship with the "
    "dataset, so any score can be recomputed. `sov34` is one small operator model; **SOVOS** is the "
    "signed instrument/system — the two are never conflated.\n\n"
    "One axis of the **GSPC** family: [govbench](https://huggingface.co/datasets/csoai/govbench) · "
    "[provbench](https://huggingface.co/datasets/csoai/provbench) · "
    "[pqcbench](https://huggingface.co/datasets/csoai/pqcbench) · defbench · mcpbench · ossbench. "
    "csoai.org\n"
)


def leaderboard_md(axis, result):
    """Build an honest leaderboard/summary table from the real result structure."""
    lines = [f"# {AXES[axis]['pretty']} — results\n"]
    if axis == "defbench":
        lines.append("| model | refusal_rate | status |\n|---|---|---|")
        for e in result.get("entrants", []):
            r = e.get("refusal", {})
            lines.append(f"| `{e.get('model')}` | {r.get('rate','—')} | {r.get('status','—')} |")
        lines.append(f"\n_Generated {result.get('timestamp','')}. v0.1, {len(result.get('entrants',[]))} entrants._")
    elif axis == "mcpbench":
        lines.append("| predicate | result |\n|---|---|")
        for p in result.get("predicates", []):
            if isinstance(p, dict):
                lines.append(f"| {p.get('id', p.get('name','?'))} | {p.get('result', p.get('pass','?'))} |")
        lines.append(f"\n_MCP spec {result.get('mcp_version','')}. Ed25519-signed; recomputable. "
                     f"{len(result.get('records',[]))} records._")
    else:  # ossbench
        lines.append("| subject | surface | readable |\n|---|---|---|")
        for row in result.get("rows", []):
            lines.append(f"| `{row.get('subject')}` | {row.get('surface','')} | {row.get('readable')} |")
        lines.append(f"\n_Composite: **{result.get('composite_score','')}**. "
                     f"{len(result.get('rows',[]))} subjects, per-provision presence only._")
    return "\n".join(lines) + "\n"


def readme_md(axis):
    a = AXES[axis]
    fm = ("---\nlicense: apache-2.0\n"
          f"pretty_name: \"{a['pretty']}\"\ntags:\n" + "".join(f"  - {t}\n" for t in a["tags"]) +
          "size_categories:\n  - n<1K\n---\n\n")
    return fm + f"# {a['pretty']}\n\n{a['blurb']}\n{FOOTER}"


def honesty_ok(text, label):
    hits = [name for name, rx, _ in G.PROHIBITED if rx.search(text)]
    if hits:
        print(f"    ✗ {label} FLAGGED: {hits} — aborting this axis")
        return False
    return True


def publish_axis(axis, do_kaggle=True):
    res_path = RES / f"{axis}.json"
    if not res_path.exists():
        print(f"  {axis}: no result file — skip"); return
    result = json.loads(res_path.read_text())
    readme, board = readme_md(axis), leaderboard_md(axis, result)
    if not (honesty_ok(readme, "README") and honesty_ok(board, "LEADERBOARD")):
        return
    stage = Path(tempfile.mkdtemp(prefix=f"{axis}_"))
    (stage / "README.md").write_text(readme)
    (stage / "LEADERBOARD.md").write_text(board)
    (stage / "LICENSE").write_text(APACHE)
    (stage / f"{axis}.json").write_text(json.dumps(result, indent=2))
    # pull the item bank from the existing -kaggle-items dataset
    try:
        from huggingface_hub import hf_hub_download
        items = hf_hub_download(f"csoai/{axis}-kaggle-items", "items.jsonl", repo_type="dataset")
        (stage / "items.jsonl").write_text(Path(items).read_text())
    except Exception as e:
        print(f"    (items.jsonl unavailable: {str(e)[:40]})")

    # ── HF ──
    from huggingface_hub import HfApi
    api = HfApi(token=HF_TOKEN)
    repo = f"csoai/{axis}"
    try:
        api.create_repo(repo, repo_type="dataset", exist_ok=True)
        api.upload_folder(folder_path=str(stage), repo_id=repo, repo_type="dataset",
                          commit_message=f"Publish {axis} — GSPC parity, honest card")
        print(f"    ✅ HF  https://huggingface.co/datasets/{repo}")
    except Exception as e:
        print(f"    ✗ HF {axis}: {str(e)[:80]}")

    # ── Kaggle ──
    if do_kaggle:
        meta = {"title": AXES[axis]["pretty"][:50], "id": f"{KU}/gspc-{axis}",
                "licenses": [{"name": "Apache 2.0"}]}
        (stage / "dataset-metadata.json").write_text(json.dumps(meta))
        # exists? -> version : create
        chk = subprocess.run(["kaggle", "datasets", "status", f"{KU}/gspc-{axis}"],
                             capture_output=True, text=True)
        cmd = (["kaggle", "datasets", "version", "-p", str(stage), "-m", "GSPC parity", "-r", "zip"]
               if "does not exist" not in (chk.stderr + chk.stdout).lower() and chk.returncode == 0
               else ["kaggle", "datasets", "create", "-p", str(stage), "-r", "zip", "-u"])
        r = subprocess.run(cmd, capture_output=True, text=True)
        out = (r.stdout + r.stderr).strip().splitlines()[-1] if (r.stdout + r.stderr).strip() else "?"
        print(f"    {'✅' if r.returncode==0 else '✗'} Kaggle gspc-{axis}: {out[:80]}")


if __name__ == "__main__":
    only = [a for a in sys.argv[1:] if not a.startswith("--")] or list(AXES)
    print(f"Publishing GSPC parity for: {only}\n")
    for ax in only:
        print(f"── {ax} ──")
        publish_axis(ax, do_kaggle="--hf-only" not in sys.argv)
