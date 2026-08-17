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


def collect(cap):
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
            for p in sorted(Path().glob(str(pattern)))[:400]:
                if p.is_file() and p.stat().st_size < 200_000:
                    try:
                        push(p, source, p.read_text(errors="replace"))
                    except OSError:
                        pass
        except Exception:
            pass

    # llm.json companions are JSON — flatten to a readable text card
    for p in sorted(D2.glob("**/*.llm.json"))[:300]:
        if p in seen:
            continue
        try:
            data = json.loads(p.read_text(errors="replace"))
            text = json.dumps(data, indent=1)[:4000]
            push(p, "llm_json", text)
        except Exception:
            pass

    push(Path("sovereign-os-5-worlds"), "sovereign_os", WORLDS)
    return items[:cap]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(Path(__file__).resolve().parent / "index" / "estate_mine_index.json"))
    ap.add_argument("--cap", type=int, default=1500)
    args = ap.parse_args()

    items = collect(args.cap)
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
    print(json.dumps(stats, indent=2))
    # smoke: prove the mine answers
    for q in ("OOWM", "GSPC axes", "care floor", "sovereign hives"):
        r = ix.query(q, k=1)
        print(f"  '{q}' -> {r[0]['source']}/{Path(r[0]['path']).name}" if r else f"  '{q}' -> (no hit)")


if __name__ == "__main__":
    main()
