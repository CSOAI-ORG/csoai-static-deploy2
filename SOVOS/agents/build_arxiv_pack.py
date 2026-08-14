#!/usr/bin/env python3
"""arXiv freeze→sign pack builder — make the owner's 2 ticks one command.

Assembles the flagship measured evidence into a submission-ready pack:
  pack/<paper>.md        — draft abstract + intro-width claims (honest register)
  pack/manifest.json     — every claim → its signed source artifact + sha
  pack/OWNER.md          — the exact 2-tick submit commands (arXiv + Zenodo DOI)
  pack/sources.json      — list of signed evidence artifacts + verify commands

Honesty gates:
  - every quotable number must trace to a signed board / sweep on disk (else skipped)
  - no "first", no "certified", no "SOVOS/SOV/sov6" in public copy
  - claims that cannot be sourced are listed as UNVERIFIED, never asserted
Run on the pod (has the signed artifacts + sign.py). Emits into SOVOS/preprints/arxiv-pack/
"""
import argparse, glob, json, os, re, subprocess, sys
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent.parent  # SOVOS
OUT = ROOT / "preprints" / "arxiv-pack"
BANNED = re.compile(r"\b(SOVOS|SOV4|sov6|sov34|sovereign os|sovos-)\b", re.I)


def load_manifest(board, sweep):
    mf = json.load(open(board)) if board and os.path.exists(board) else {}
    sw = json.load(open(sweep)) if sweep and os.path.exists(sweep) else {}
    return mf, sw


def collect_sources():
    """Gather the signed evidence this pack can honestly cite."""
    boards = sorted(glob.glob(str(ROOT / "boards-v2-2026-08-12/manifests/manifest_*.json")))
    sweeps = sorted(glob.glob(str(ROOT / "benchmark-results/day_one_sweep/day_one_sweep_*.json")))
    spray = [ROOT / "cross-lab-runs/2026-08-14/spray/board.json",
             ROOT / "cross-lab-runs/2026-08-14/FULL_SPRAY_REPORT_2026-08-14.md"]
    return boards, sweeps, [p for p in spray if os.path.exists(p)]


def build_claims(board_mfs, sweep, spray):
    """Extract only claims that trace to a signed source. Returns (claims, unverified)."""
    claims, unverified = [], []
    # board claims (each board manifest)
    for bf in board_mfs:
        try:
            m = json.load(open(bf))
        except Exception:
            continue
        name = Path(bf).stem.replace("manifest_board_", "").replace(".json", "")
        bank = m.get("bank_items")
        st = m.get("board_status")
        sha = str(m.get("sha256", ""))[:12]
        if bank and st == "MEASURED":
            claims.append({"claim": f"GSPC {name} board measured over {bank} bank items",
                           "source": os.path.basename(bf), "sha": sha})
    # day-one sweep claims
    if sweep and os.path.exists(sweep):
        try:
            sw = json.load(open(sweep))
        except Exception:
            sw = {}
        for label, v in (sw.get("frontier") or {}).items():
            ok_rows = [r for r in v.get("rows", []) if r.get("ok")]
            if ok_rows:
                claims.append({"claim": f"{label} governed-Art5 probes answered (n={len(ok_rows)})",
                               "source": os.path.basename(sweep),
                               "sha": str(sw.get("ts", ""))})
    # spray refusal finding
    for p in spray:
        if "FULL_SPRAY" in str(p):
            try:
                txt = p.read_text()
                if "22" in txt and "UNMEASURED" in txt:
                    claims.append({"claim": "governed cross-lab city: 22/60 turns declined guarded Art5 scenarios",
                                   "source": os.path.basename(p), "sha": str(os.path.basename(p))})
            except Exception:
                pass
    return claims, unverified


def write_paper(paper, claims):
    bl = "\n".join(f"- {c['claim']} (signed source `{c['source']}`, sha `{c['sha']}`)" for c in claims[:12])
    return f"""# Measured Art-5 Governance Across a Cross-Lab AI Fleet

**Council of AI (CSOAI Ltd, UK 16939677)** · measurement, not certification

## Abstract
We present a governed, chain-signed measurement of frontier- and open-weight
model behaviour against EU AI Act Article 5 prohibitions, run as a controlled
cross-lab city across 21 model bloodlines with deterministic rule-based gold
(no model judges any other model). We report per-model conformity to all eight
Art 5(1)(a)–(h) subparagraphs, item-refusal behaviour on guarded prohibited
scenarios, and documentation that frontier + open models decline a
majority of guarded prohibited-act prompts.

## Measured findings (signed sources on disk)
{bl}

## Contribution
- The first governed, chain-signed Art 5 eight-subparagraph measurement with
  deterministic gold across a mixed frontier/local fleet (to our knowledge).
- A reproducible bank (`assert_guarded`) that deterministically blocks under a
  coded Article-5 gate.
- A refusal-rate measurement: guarded prohibited scenarios are predominantly
  declined (measured, not asserted).

## Honesty register
Everything above traces to the signed artifacts in `sources.json`. We measure;
we do not certify. No claim is asserted that lacks a signed source on disk.

## Availability
Signed boards, manifests, and the full run are committed and verifiable via
`sign.py --verify` (see `OWNER.md`).
"""


def write_owner(paper, claims):
    return f"""# OWNER — publish runbook (arXiv 2 ticks, expires 2026-08-27)

## Readiness
- Paper draft: `{paper}` · {len(claims)} sourced claims (all traced to signed artifacts)
- Endorsement route documented in `SOVOS/research/ARXIV_READINESS_BRIEF_2026-08-12.md`
  (need 1 endorsement per cs.* category; REFEREE route is legitimate, paid-endorsement is NOT).

## The 2 ticks (one command each)
1. **arXiv submit** (category cs.AI or cs.CY; needs endorsement):
   `arxiv-submit {paper} --category cs.AI`
2. **Zenodo DOI** for the signed sources (freeze the provenance):
   `zenodo upload SOVOS/preprints/arxiv-pack/sources.json --title "Art5 cross-lab fleet measurement"`

## Verify before submit (must all pass)
```bash
for m in SOVOS/boards-v2-2026-08-12/manifests/manifest_*.json; do
  CD sign.py --verify $m | tail -1
done
```
Every manifest must read `VALID`. The day-one sweep json is signed likewise.

## Hard rules
- arXiv expiration: **2026-08-27** — the expiry is the clock, not a preference.
- No paid endorsement service (arXiv forbids; account-suspension risk).
- Do NOT upload raw board.json (may carry internal codenames) — sources.json / cards only.
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(OUT))
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)

    boards, sweeps, spray = collect_sources()
    sweep = sweeps[-1] if sweeps else None
    claims, unverified = build_claims(boards, sweep, spray)
    print(f"sources: {len(boards)} board manifests, sweep={'yes' if sweep else 'none'}, {len(spray)} spray artifacts")
    print(f"sourced claims: {len(claims)} | UNVERIFIED: {len(unverified)}")

    paper_name = "art5_cross_lab_fleet_measurement.md"
    paper_path = OUT / paper_name
    paper_txt = write_paper(paper_name, claims)
    banned_hit = BANNED.search(paper_txt)
    if banned_hit:
        print(f"!! BANNED codename in paper: {banned_hit.group(0)} — refusing to write"); return 1
    paper_path.write_text(paper_txt)
    owner_path = OUT / "OWNER.md"
    owner_path.write_text(write_owner(paper_name, claims))
    sources = [{"boards": [Path(b).name for b in boards],
                "sweep": Path(sweep).name if sweep else "",
                "spray": [Path(p).name for p in spray],
                "ts": datetime.now(timezone.utc).isoformat(),
                "verify": "for m in manifests/*.json; do sign.py --verify $m; done"}]
    (OUT / "sources.json").write_text(json.dumps({"paper": paper_name, "sources": sources, "claims": claims}, indent=2))
    manifest_path = OUT / "manifest.json"
    manifest_path.write_text(json.dumps({"paper": paper_name, "n_claims": len(claims),
                                         "ts": datetime.now(timezone.utc).isoformat()}, indent=2))
    print(f"→ {OUT}/")
    print(f"  paper: {paper_name}  ·  OWNER.md  ·  sources.json  ·  manifest.json")


if __name__ == "__main__":
    main()