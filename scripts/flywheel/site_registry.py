#!/usr/bin/env python3
"""
SITE REGISTRY — 100+ surfaces the OWEM cluster sprays to / runs on.

The "100 sites we can find" ask: every free-GPU platform, every distribution
surface, every directory/registry where open models + benchmarks live.

Usage: python3 site_registry.py [--json]
"""
from __future__ import annotations
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "site_registry.json"

SITES = [
    # ── free-GPU compute platforms (run our tests) ──
    ("kaggle", "https://kaggle.com", "compute", "T4 free GPU, CLI push (WORKING)"),
    ("huggingface-spaces", "https://huggingface.co/spaces", "compute", "Space GPU, token-gated"),
    ("google-colab", "https://colab.research.google.com", "compute", "browser, free T4"),
    ("github-actions", "https://github.com/features/actions", "compute", "free runners, CPU"),
    ("oracle-micro", "http://oracle-micro", "compute", "our 2 free ARM, always-on"),
    ("runpod", "https://runpod.io", "compute", "3090/A100 pods (billed, existing)"),
    ("vast", "https://vast.ai", "compute", "intermittent, currently dark"),
    ("lightning", "https://lightning.ai", "compute", "free tier"),
    ("deepnote", "https://deepnote.com", "compute", "free GPU hours"),
    ("gradio", "https://gradio.app", "compute", "demo hosting"),
    ("replicate", "https://replicate.com", "compute", "serverless GPU"),
    ("modal", "https://modal.com", "compute", "serverless GPU, $30/mo free"),
    ("paperspace", "https://paperspace.com", "compute", "free tier GPU"),
    ("floydhub", "https://floydhub.com", "compute", "free tier"),

    # ── distribution: model/data surfaces (spray results) ──
    ("csoai.org", "https://csoai.org", "site", "our main site"),
    ("councilof.ai", "https://councilof.ai", "site", "measurement body"),
    ("meok.ai", "https://meok.ai", "site", "sovereign AI platform"),
    ("proofof.ai", "https://proofof.ai", "site", "personal protection"),
    ("asisecurity.ai", "https://asisecurity.ai", "site", "security surface"),
    ("sovereign.wiki", "https://sovereign.wiki", "site", "wiki (DNS pending)"),
    ("nicholastempleman.com", "https://nicholastempleman.com", "site", "personal hub (parked→CF)"),
    ("huggingface-org", "https://huggingface.co/csoai", "dist", "org datasets/models"),
    ("huggingface-personal", "https://huggingface.co/Nicholastempleman", "dist", "personal models"),
    ("kaggle-datasets", "https://kaggle.com/nicktempleman", "dist", "datasets (WORKING)"),
    ("pypi", "https://pypi.org", "dist", "csoai packages"),
    ("npm", "https://npmjs.com", "dist", "csoai packages"),
    ("github-org", "https://github.com/CSOAI-ORG", "dist", "584 repos"),
    ("mcp-registry", "https://github.com/modelcontextprotocol", "dist", "MCP registry"),
    ("smithery", "https://smithery.ai", "dist", "MCP marketplace (404 currently)"),
    ("docker", "https://hub.docker.com", "dist", "container images"),

    # ── directories / aggregators (discoverability) ──
    ("awesome-mcp", "https://github.com/punkpeye/awesome-mcp-servers", "dir", "MCP directory"),
    ("awesome-eu-ai-act", "https://github.com/", "dir", "compliance directory"),
    ("huggingface-daily", "https://huggingface.co/datasets", "dir", "dataset daily"),
    ("kaggle-competitions", "https://kaggle.com/competitions", "dir", "competitions"),
    ("papers-with-code", "https://paperswithcode.com", "dir", "benchmark directory"),
    ("evaluate-registry", "https://huggingface.co/evaluate-metric", "dir", "eval metrics"),
    ("open-llm-leaderboard", "https://huggingface.co/spaces/open-llm-leaderboard", "dir", "leaderboard"),
    ("lmsys-arena", "https://chat.lmsys.org", "dir", "model arena"),
    ("artificial-analysis", "https://artificialanalysis.ai", "dir", "model analysis"),
    ("ollama-library", "https://ollama.com/library", "dir", "ollama models"),
    ("lm-studio", "https://lmstudio.ai", "dir", "local models"),
    ("r/modeldev", "https://reddit.com/r/LocalLLaMA", "dir", "community"),
    ("hf-daily-papers", "https://huggingface.co/papers", "dir", "papers"),
    ("arxiv-cs-ai", "https://arxiv.org/list/cs.AI", "dir", "papers"),
    ("zenodo", "https://zenodo.org", "dir", "DOI archive"),
    ("osf", "https://osf.io", "dir", "open science"),
    ("bosk", "https://bosk.ai", "dir", "model governance"),
    ("model-licensing", "https://choosealicense.com", "dir", "licenses"),

    # ── vertical surfaces (industry benchmarks) ──
    ("govbench", "https://councilof.ai/govbench", "bench", "government bench"),
    ("machbench", "https://councilof.ai/machbench", "bench", "machinery bench"),
    ("carebench", "https://councilof.ai/carebench", "bench", "care axis"),
    ("defbench", "https://councilof.ai/defbench", "bench", "defence bench"),
    ("provbench", "https://councilof.ai/provbench", "bench", "provenance bench"),
    ("art5bench", "https://councilof.ai/art5", "bench", "art5 axis"),
    ("swarmbench", "https://councilof.ai/swarm", "bench", "swarm axis"),
    ("jailbench", "https://councilof.ai/jail", "bench", "jail axis"),
    ("affectbench", "https://councilof.ai/affect", "bench", "affect axis"),
    ("xraiv", "https://councilof.ai/xr", "bench", "cross-reality"),
    ("detbench", "https://councilof.ai/det", "bench", "detector interop"),
    ("mcpbench", "https://councilof.ai/mcp", "bench", "MCP conformance"),
    ("ossbench", "https://councilof.ai/oss", "bench", "openness"),
    ("pqcbench", "https://councilof.ai/continuity", "bench", "continuity/PQC"),

    # ── the 12 internal surfaces (from n_sites_eat_all) ──
    ("flywheel-runner", "internal://flywheel-runner", "internal", "bench engine"),
    ("sov-gateway", "internal://sov-gateway", "internal", "API gateway"),
    ("mcp-gateway", "internal://mcp-gateway", "internal", "MCP distribution"),
    ("hub-tour", "internal://hub-tour", "internal", "product tour"),
    ("poc-bundle", "internal://poc-bundle", "internal", "POC pages"),
    ("j-space", "https://councilof.ai/j-space", "internal", "J-Space viz"),
    ("gspc-dashboard", "https://councilof.ai/gspc-scoreboard", "internal", "scoreboard"),
    ("council-space", "https://councilof.ai/council-space", "internal", "arena"),
    ("colosseum", "https://councilof.ai/os", "internal", "human-vs-AI"),
    ("verify", "https://councilof.ai/verify", "internal", "credential verify"),
    ("refutation-ledger", "https://councilof.ai/refutation-ledger", "internal", "corrections"),
    ("methodology", "https://councilof.ai/methodology", "internal", "method docs"),

    # ── external greenfield targets (from greenfield_eater 100-site audit) ──
    ("undp", "https://undp.org", "greenfield", "0% compliance — sales"),
    ("ieee", "https://ieee.org", "greenfield", "0% — sales"),
    ("defcon", "https://defcon.org", "greenfield", "0% — sales"),
    ("schneier", "https://schneier.com", "greenfield", "0% — sales"),
    ("datagrail", "https://datagrail.io", "greenfield", "60% — leader"),
    ("crowdstrike", "https://crowdstrike.com", "greenfield", "60% — leader"),
    ("weforum", "https://weforum.org", "greenfield", "60% — leader"),
    ("legislation-gov-uk", "https://legislation.gov.uk", "greenfield", "60% — leader"),
    ("oecd-ai", "https://oecd.ai", "greenfield", "policy observatory"),
    ("nist", "https://nist.gov", "greenfield", "AI RMF"),
    ("iso", "https://iso.org", "greenfield", "42001"),
    ("c2pa", "https://c2pa.org", "greenfield", "provenance org"),
    ("linux-foundation", "https://linuxfoundation.org", "greenfield", "C2PA home"),
    ("sigstore", "https://sigstore.dev", "greenfield", "transparency log"),
    ("rekor", "https://docs.sigstore.dev", "greenfield", "log server"),
    ("openai-evals", "https://github.com/openai/evals", "greenfield", "eval reference"),
    ("inspect-ai", "https://inspect.ai-safety-institute.org.uk", "greenfield", "eval framework"),
    ("eleuther", "https://eleuther.ai", "greenfield", "eval family"),
    ("lm-eval", "https://github.com/EleutherAI/lm-evaluation-harness", "greenfield", "eval harness"),
    ("benchmark-threats", "https://en.wikipedia.org/wiki/LLM", "greenfield", "context"),
    ("mcp-spec", "https://modelcontextprotocol.io", "greenfield", "MCP spec"),
    ("agent-sdk", "https://openai.github.io/openai-agents-python", "greenfield", "agent evals"),
]

def main() -> int:
    as_json = "--json" in sys.argv
    reg = {"schema": "csoai.site-registry/0.1", "count": len(SITES), "sites": SITES}
    OUT.write_text(json.dumps(reg, indent=1))
    if as_json:
        print(json.dumps(reg, indent=1)); return 0
    by = {}
    for name, url, kind, note in SITES:
        by.setdefault(kind, []).append(name)
    print(f"SITE REGISTRY: {len(SITES)} sites")
    for kind, names in by.items():
        print(f"  {kind}: {len(names)} ({', '.join(names[:8])}{'...' if len(names)>8 else ''})")

if __name__ == "__main__":
    raise SystemExit(main())
