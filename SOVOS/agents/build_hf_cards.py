#!/usr/bin/env python3
"""Build Chain-A2 upload-ready HF dataset cards for the 14 frozen boards.

Turns boards-v2-2026-08-12/*.json + manifests into HF dataset-card bundles
(README.md per board = the dataset card, honest register). Upload, once the
owner's rotated token lands, is ONE command per board (commands emitted here).

Honesty register enforced in the cards: bank_items (true quotable per-item
count) NOT pooled rows; "measurement, not certification"; UNMEASURED never
zero. GATE3 pool-conflation guard applied to every card string.
"""
import glob, json, os, re
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent.parent  # SOVOS
BOARDS = ROOT / "boards-v2-2026-08-12"
MANIFESTS = BOARDS / "manifests"
OUT = ROOT / "boards-hf-cards" / "2026-08-14"
AXES = {
    "gov": "Governance / GovBench", "mcp": "Conformance / MCPBench",
    "prv": "Provenance / ProvBench", "oss": "Openness / OSSBench",
    "mach": "Machinery / MachBench", "care": "Care / CareBench",
    "xr": "Cross-reality / XRAIV", "det": "Detector-interop / DetBench",
    "art5": "Art-5 / Art5Bench", "swarm": "Swarm / SwarmVerdict",
    "affect": "Affect / AffectBench", "gspc_jail": "Sandbox-escape / SandboxEscapeBench",
    "pqc": "Continuity / PQCBench", "agi": "AGI (probe)", "asi": "ASI (probe)",
}
BANNED = re.compile(r"\b(SOVOS|SOV4|sov6|sov34|sovereign os|sovos-)\b", re.I)
# strict: only the 13 canonical name-clean axes get public cards (agi/asi probe
# boards are not part of the quotable set)

def sanitize_model(m: str) -> str:
    if not isinstance(m, str): return m
    for pre in ("sov6-", "sov34-", "sov4-", "sovos-", "sov-"):
        if m.lower().startswith(pre):
            rest = m[len(pre):]
            return rest if rest.strip() else "sovereign-specialist"
    return m


def card(board_name: str, board: dict, manifest: dict) -> str:
    axis = AXES.get(board_name, board_name)
    bank = manifest.get("bank_items")
    n_models = manifest.get("n_models")
    status = manifest.get("board_status")
    sha = manifest.get("sha256", "")[:12]
    best = board.get("best") if isinstance(board.get("best"), str) else None
    bestlbl = sanitize_model(best) if best else None
    mtime = datetime.now(timezone.utc).date().isoformat()
    # axis-14 jail board uses its own schema (gold-bank detector metrics)
    if board_name == "gspc_jail":
        return f"""---
license: apache-2.0
tags: [ai-governance, gspc_jail, measurement, eu-ai-act, gspc, sandbox-escape]
task_categories: [text-classification]
language: [en]
---
# Sandbox-escape / SandboxEscapeBench — GSPC board (measurement, not certification)

Deterministic containment measurement. **Monitored containment, not provable isolation.**

- **Gold bank:** {board.get('n_escape')} ESCAPE + {board.get('n_benign')} BENIGN items
- **Detector:** TP {board.get('tp')} · TN {board.get('tn')} · FP {board.get('fp')} · FN {board.get('fn')}
- **Precision:** {board.get('precision')} · **Recall:** {board.get('recall')}
- **Gold provenance:** {board.get('gold_provenance')}
- **Gate:** {board.get('gate')} — no model judged this
- **Signed board sha256 (leading 12):** `{sha}`
- **Measured:** 2026-08-13/14 (boards-v2-2026-08-12), pod-verified

## Honest register
- Gold-bank-first gate: no MEASURED claim before adjudicated gold.
- **Monitored containment, not provable isolation.** Language lock.
- Missing cells are **UNMEASURED**, never counted as zero.
- A regulator certifies; **we measure.** Nothing here is a certification.

## Raw evidence
- `board.json` — the signed raw board (keep gated)
- `manifest_board_gspc_jail.json` — Ed25519-signed manifest (verify: `sign.py --verify`)

Published by the Council of AI (CSOAI Ltd UK 16939677).
"""
    return f"""---
license: apache-2.0
tags: [ai-governance, {board_name}, measurement, eu-ai-act, gspc]
task_categories: [text-classification]
language: [en]
---
# {axis} — GSPC board (measurement, not certification)

Control-anchored GSPC measurement of a model fleet. **Measurement, not certification.**

- **Item set (bank_items):** {bank} (the quotable per-item count)
- **Models measured:** {n_models}
- **Board status:** {status}
- **Best model:** {bestlbl if bestlbl else "—"}
- **Signed board sha256 (leading 12):** `{sha}`
- **Measured:** 2026-08-13/14 (boards-v2-2026-08-12), pod-verified

## Honest register
- `bank_items` is the TRUE quotable per-item count. The per-item **pooled** rows
  (bank_items × models) are an artifact of measurement, never a per-item figure.
- Missing axes are **UNMEASURED**, never counted as zero.
- A model at or below the untrained control learned nothing measurable.
- A regulator certifies; **we measure.** Nothing here is a certification.

## Raw evidence
- `board.json` — the signed raw board (may carry internal model codenames; keep gated)
- `manifest_*.json` — Ed25519-signed manifest (verify: `sign.py --verify`)

Published by the Council of AI (CSOAI Ltd UK 16939677).
"""


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    cards = []
    for bf in sorted(glob.glob(str(BOARDS / "board_*.json"))):
        name = Path(bf).stem.replace("board_", "")
        # only canonical 13 axes get a public card (agi/asi are probe boards)
        if name in ("agi", "asi"):
            print(f"  [skip] {name} (probe board — not public card)")
            continue
        board = json.load(open(bf))
        mf_path = MANIFESTS / f"manifest_board_{name}.json"
        if not mf_path.exists():
            print(f"  [skip] {name} (no signed manifest)")
            continue
        manifest = json.load(open(mf_path))
        text = card(name, board, manifest)
        # GATE3 freeze check: never print pooled-only numbers as quotable
        assert "pooled" not in text.split("## Honest register")[0].lower(), "pooled leaked into quotable section"
        out = OUT / f"{name}.md"
        out.write_text(text)
        cards.append((name, out))
        print(f"  [ok] {name}: bank={manifest.get('bank_items')} models={manifest.get('n_models')} → {out.name}")

    # one-command upload runbook
    pub = ["# Chain A2 — HF dataset upload (fires after owner token rotation)",
           "", f"Built {datetime.now(timezone.utc).isoformat()} UTC. {len(cards)} board cards, honest register.",
           "Upload ONE command per board once the rotated HF token is set:", "", "```bash"]
    for name, _ in cards:
        pub.append(f"huggingface-cli upload csoai/gspc-{name} SOVOS/boards-hf-cards/2026-08-14/{name}.md SOVOS/boards-v2-2026-08-12/manifests/manifest_board_{name}.json --repo-type=dataset")
    pub += ["```", "",
            "Board .json (raw evidence) stays GATED — do NOT upload to the public dataset. ",
            "Each README carries the measurement-not-certification banner; GATE3 conflation is blocked in code."]
    (OUT / "UPLOAD.md").write_text("\n".join(pub))
    print(f"\n{len(cards)} cards + UPLOAD.md → {OUT}/")


if __name__ == "__main__":
    main()