#!/usr/bin/env python3
"""Estate-mine → OOWM knowledge-graph ingestion (2026-08-17, JEEVES).

Learns the verified estate into the OOWM index. Reads the mined corpus
(HONEST_MINE, ESTATE_MINE_RESEARCH_MAP, SOVOS STATUS + doctrine docs,
sovereign-os 5-worlds surface, llm.json companions) and writes a persistent
index that `oowm.server` boots from — so `council-oowm` answers from real
estate data, not the 17-doc seed.

Usage:
    python3 -m oowm.estate_mine_ingest [--out PATH] [--cap N]
"""
import argparse, json, sys
from pathlib import Path
from datetime import datetime, timezone

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from oowm.knowledge import OOWMIndex

HOME = Path.home()
# Pod-aware roots: on the 3090/A100 the corpus lives in the /workspace volume
# mirror (.stash/mac-backup). On Mac it lives under ~/clawd. Same sources either way.
POD_STASH = Path("/workspace/.stash/mac-backup")
if POD_STASH.is_dir():
    CL = POD_STASH / "clawd" if (POD_STASH / "clawd").is_dir() else POD_STASH
    CL = POD_STASH if (POD_STASH / "kimi-regen").is_dir() else CL
    CL = Path("/workspace/.stash/mac-backup/clawd") if (Path("/workspace/.stash/mac-backup/clawd")).is_dir() else CL
else:
    CL = HOME / "clawd"
KR = CL / "kimi-regen"
SOVOS = KR / "SOVOS"
D2 = CL / "csoai-static-deploy2"
SOVOS_D2 = D2 / "SOVOS"
OOWM_MCP = CL / "mcp-marketplace" / "meok-sovereign-oowm-mcp"

# (path, source) — every source name is a mined surface, not a brand.
SOURCES = [
    # Honest mine — disk-verified claims table
    (KR / "SOVOS" / "HONEST_MINE_2026-08-10.md", "honest_mine"),
    (KR / "SOVOS" / "ESTATE_MINE_RESEARCH_MAP_2026-08-12.md", "estate_mine"),
    (KR / "SOVOS" / "STATUS.md", "sovos_status"),
    (KR / "SOVOS" / "FLEET_ROSTER.md", "sovos_fleet"),
    (KR / "SOVOS" / "MASTER_MANIFEST.md", "sovos_manifest"),
    (KR / "SOVOS" / "README.md", "sovos_package"),
    (KR / "sov3_oowm_all_models.md", "oowm_doctrine"),
    (KR / "sov3_oowm_knowledge_tab.md", "oowm_doctrine"),
    (KR / "SOV33_GROWTH_MODEL_2026-07-11.md", "oowm_doctrine"),
    (KR / "OWEM_MASTER_REGISTRY.md", "owem_registry"),
    (KR / "sov7_synthesis" / "_sov7" / "SOV8_MASTER_ARCHITECTURE.md", "sov8_arch"),
    (KR / "sov7_synthesis" / "_sov7" / "owem_sandwich_README.md", "owem_recipe"),
    (KR / "SOVOS" / "DOCTRINE_337_2026-08-12.md", "doctrine_337"),
    (CL / "_alignment" / "ALIGNMENT_TOPDOWN_2026-08-15.md", "alignment"),
    (CL / "_alignment" / "SOV_NAMING_TAXONOMY.md", "naming_taxonomy"),
    (CL / "_alignment" / "ALIGNMENT_V49_PULSE_EXPERIMENTS_2026-08-15.md", "alignment"),
    (SOVOS_D2 / "FLEET_MAP_2026-08-16.md", "sovos_fleet"),
    (SOVOS_D2 / "STORAGE_MASTER_TOPOLOGY_2026-08-16.md", "sovos_storage"),
    (CL / "sov-os" / "README.md", "sov_os"),
    (CL / "sov33-oowm" / "INTEGRATION_REPORT.md", "oowm_mcp"),
    (CL / "sov33-oowm" / "oowm" / "server.py", "oowm_mcp"),
    (OOWM_MCP / "README.md", "oowm_mcp"),
    (OOWM_MCP / "meok_sovereign_oowm_mcp" / "__init__.py", "oowm_mcp"),
]

# Glob corpora: llm.json companions + sovereign-os surface + package cards
GLOBS = [
    (D2 / "**" / "*.llm.json", "llm_json"),
    (D2 / "SOVOS" / "packages" / "**" / "README.md", "sovos_package"),
    (SOVOS / "packages" / "**" / "README.md", "sovos_package"),
    (D2 / "SOVOS" / "assets" / "**" / "*.md", "sovos_asset"),
    (CL / "sov-os" / "**" / "*.md", "sov_os"),
    (CL / "_alignment" / "**" / "*.md", "alignment"),
    (CL / "sovereign-charters" / "**" / "*.md", "charter"),
    (CL / "sovereign-temple-public" / "**" / "*.py", "temple_py"),
    (CL / "csoai.org" / "**" / "*.html", "csoai_site"),
]

# Explicit 5-worlds surface (OOWM/OWEM/IWM/OWM/VWM) anchor
WORLDS = (
    "OOWM Organic Open World Model continuous-learning embodied self-revising world model "
    "OWEM Organic World Exploration Model / Open World Emergence Model sovereign-trained specialists "
    "IWM Inner World Model reasoning memory sovos-world absorbed sovos-hive stigmergy "
    "OWM Outer World Model perception environment Cosmos V-JEPA world prediction "
    "VWM Visual World Model Depth Anything 3 Cosmos-Reason scene binding sigma shader 3KB worldlines "
    "SOVOS codename for MEOK Modular Empire Operating Kernel our actual OOWM sovereign substrate "
    "hives 12 OWEM hives clans families specialist routing sovereign governance BFT council Ed25519 sigil "
    "measurement not certification UNMEASURED said as UNMEASURED care floor 0.95 "
    "estate mine verified claims disk reality brief inflation read the disk not the brief"
)


def mine_github(items, seen, push, gh_org="CSOAI-ORG", limit=120):
    """Mine every public repo's README + llm.json + agent-card via gh API.
    Fail-soft: any repo error skips it; network absence degrades to local-only.
    Returns count of repos mined."""
    import subprocess
    mined = 0
    try:
        out = subprocess.run(["gh", "repo", "list", gh_org, "--limit", str(limit),
                              "--json", "name"], capture_output=True, text=True, timeout=60)
        repos = json.loads(out.stdout)
    except Exception:
        return 0
    for r in repos:
        name = r.get("name", "")
        if not name:
            continue
        # README (default branch)
        try:
            rd = subprocess.run(["gh", "api", f"repos/{gh_org}/{name}/readme",
                                 "-H", "Accept: application/vnd.github.raw"],
                                capture_output=True, text=True, timeout=30)
            if rd.returncode == 0 and rd.stdout.strip():
                push(f"github:{gh_org}/{name}/README", "github_repo", rd.stdout[:4000])
                mined += 1
        except Exception:
            pass
        # llm.json
        for f in ("llm.json", "agent.json", "mcp.json"):
            try:
                rd = subprocess.run(["gh", "api", f"repos/{gh_org}/{name}/contents/{f}",
                                     "-H", "Accept: application/vnd.github.raw"],
                                    capture_output=True, text=True, timeout=30)
                if rd.returncode == 0 and rd.stdout.strip():
                    push(f"github:{gh_org}/{name}/{f}", "github_" + f.replace(".json", ""), rd.stdout[:4000])
            except Exception:
                pass
    return mined


def collect(cap, with_github=True):
    items = []
    seen = set()

    def push(path, source, text):
        p = str(path)
        if p in seen or not text.strip():
            return
        seen.add(p)
        items.append((p, source, text[:4000]))

    for path, source in SOURCES:
        if path.is_file():
            try:
                push(path, source, path.read_text(errors="replace"))
            except OSError:
                pass

    for pattern, source in GLOBS:
        try:
            root = Path(str(pattern).split("/**")[0])
            per_pattern = 1200 if source == "llm_json" else 500
            for p in sorted(root.glob("**/*" + str(pattern).split("/**")[1]))[:per_pattern]:
                if p.is_file() and p.stat().st_size < 200_000:
                    try:
                        push(p, source, p.read_text(errors="replace"))
                    except OSError:
                        pass
        except Exception:
            pass

    # llm.json companions are JSON — flatten to a readable text card
    base = Path("/workspace") if POD_STASH.is_dir() else D2
    for p in sorted(base.glob("**/*.llm.json"))[:1200]:
        if p in seen:
            continue
        try:
            data = json.loads(p.read_text(errors="replace"))
            text = json.dumps(data, indent=1)[:4000]
            push(p, "llm_json", text)
        except Exception:
            pass

    # GitHub estate (readme + llm/agent/mcp cards) — the online mine
    if with_github:
        try:
            n = mine_github(items, seen, push)
            if n:
                print(f"  [github] mined {n} repo cards", flush=True)
        except Exception:
            pass

    # Live arena rounds + league — the measurement mine (real Elo, real axes)
    for apath, src in ((Path("/workspace/arena-24x7/reborn_rounds.jsonl"), "arena_round"),
                       (Path("/workspace/arena-24x7/grok_referee_rounds.jsonl"), "grok_referee_round"),
                       (Path("/workspace/arena-24x7/league.json"), "arena_league")):
        if apath.is_file():
            try:
                if apath.suffix == ".jsonl":
                    with apath.open() as f:
                        lines = [ln for ln in f if ln.strip()][-400:]  # tail window
                    for i, ln in enumerate(lines):
                        push(f"{apath}:{i}", src, ln)
                else:
                    push(apath, src, apath.read_text(errors="replace")[:4000])
            except Exception:
                pass

    # HF datasets (API) — the bench corpus catalog
    try:
        import subprocess as _sp
        out = _sp.run(["curl", "-s", "-m", "20",
                       "https://huggingface.co/api/datasets?author=csoai&limit=100"],
                      capture_output=True, text=True, timeout=30)
        hf = json.loads(out.stdout)
        for d in hf:
            did = d.get("id", "")
            if did:
                push(f"hf:{did}", "hf_dataset",
                     f"HF dataset {did}: {d.get('description','')} downloads={d.get('downloads',0)} likes={d.get('likes',0)} tags={','.join(d.get('tags',[])[:10])}")
    except Exception:
        pass

    # Kaggle datasets (CLI) — nicktempleman catalog
    try:
        import subprocess as _sp
        out = _sp.run(["kaggle", "datasets", "list", "--user", "nicktempleman", "--csv"],
                      capture_output=True, text=True, timeout=60)
        for ln in out.stdout.splitlines()[1:]:  # skip header
            if ln.strip():
                push(f"kaggle:{ln.split(',')[0]}", "kaggle_dataset", ln[:4000])
    except Exception:
        pass

    # Sim World signed h3k cards — the living-DB training fuel (ed25519-signed)
    for p in sorted(Path("/workspace").glob("sim-world-card*.json"))[:5]:
        try:
            data = json.loads(p.read_text(errors="replace"))
            push(p, "h3k_card", json.dumps(data, indent=1)[:4000])
        except Exception:
            pass
    # latest card dir mirror (if synced)
    for p in sorted(Path("/workspace").glob("h3k-*.json"))[:5]:
        try:
            push(p, "h3k_card", p.read_text(errors="replace")[:4000])
        except Exception:
            pass

    # Specialist Ring deltas (Playbook §4) + Zeus/Eunomia walks (§5)
    ring_dir = Path("/workspace/arena-24x7/ring")
    for p in sorted(ring_dir.glob("ring_*.json"))[:10]:
        try:
            push(p, "ring_delta", p.read_text(errors="replace")[:4000])
        except Exception:
            pass
    walk_dir = Path("/workspace/arena-24x7/zeus_eunomia")
    for p in sorted(walk_dir.glob("walk_*.json"))[:10]:
        try:
            push(p, "dual_walk", p.read_text(errors="replace")[:4000])
        except Exception:
            pass

    # Honey KB (forest/) — 94K+ training pairs, sampled (estate's biggest data seam)
    honey_bases = [Path("/workspace/forest") if POD_STASH.is_dir() else D2 / "forest"]
    for hb in honey_bases:
        for hf in sorted(hb.glob("honey_*.jsonl"))[:5]:
            try:
                with hf.open() as f:
                    lines = [ln for ln in f if ln.strip()][:5000]  # P1: 5K-row honey window
                for i, ln in enumerate(lines):
                    push(f"{hf}:{i}", "honey_kb", ln[:4000])
            except Exception:
                pass

    # benchmark-results + forest harness cards (measurement corpus)
    br_base = Path("/workspace") if POD_STASH.is_dir() else KR / "benchmark-results"
    for p in sorted(br_base.glob("**/*.json"))[:500]:
        if p.is_file() and p.stat().st_size < 300_000:
            try:
                push(p, "benchmark_result", p.read_text(errors="replace")[:4000])
            except OSError:
                pass
    for p in sorted(D2.glob("forest/*.json"))[:200]:
        if p.is_file() and p.stat().st_size < 300_000:
            try:
                push(p, "forest_card", p.read_text(errors="replace")[:4000])
            except OSError:
                pass

    # mcp-marketplace — the 710-package fleet (READMEs)
    for p in sorted((CL / "mcp-marketplace").glob("*/README.md"))[:600]:
        try:
            push(p, "mcp_package", p.read_text(errors="replace")[:4000])
        except OSError:
            pass

    push(Path("sovereign-os-5-worlds"), "sovereign_os", WORLDS)
    return items[:cap]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(Path(__file__).resolve().parent / "index" / "estate_mine_index.json"))
    ap.add_argument("--cap", type=int, default=2500)
    ap.add_argument("--no-github", action="store_true", help="skip GitHub mining (offline mode)")
    args = ap.parse_args()

    items = collect(args.cap, with_github=not args.no_github)
    ix = OOWMIndex()
    n = ix.add_many(items, cap=args.cap)
    ix.build_tfidf()
    ix.built_at = datetime.now(timezone.utc).isoformat()
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    ix.save(out)
    stats = ix.stats()
    stats["added"] = n
    stats["output"] = str(out)
    # source breakdown
    from collections import Counter
    stats["by_source"] = dict(Counter(d["source"] for d in ix.docs))
    print(json.dumps(stats, indent=2))
    # smoke: prove the mine answers
    for q in ("OOWM", "GSPC axes", "care floor", "sovereign hives", "Grok referee", "runpod fleet"):
        r = ix.query(q, k=1)
        print(f"  '{q}' -> {r[0]['source']}/{Path(r[0]['path']).name}" if r else f"  '{q}' -> (no hit)")


if __name__ == "__main__":
    main()
