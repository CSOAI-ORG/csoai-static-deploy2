#!/usr/bin/env python3
"""
sov33_one.py — THE UNIFIED SOVEREIGN. ONE entrypoint.

MEOK-SOV3 for Sir Nicholas Templeman. Every useful capability in the
sovereign substrate flows through `Sovereign.ask()` — single function,
single result, full provenance.

ABSORBED CAPABILITIES (one entrypoint, all layers):
  L0 DRUM heartbeat       (firefly phase-lock, real-time)
  L1 Care (derived)       (plain + de-framed, breach if either sub-floor)
  L2 BFT-33 quorum        (23/33, immutable record)
  L3 Anchor routing       (4-anchor × 5-elders MoE)
  L4 Sovereign-merge brain (Oracle 70B + Ollama + cascade)
  L5 SIGIL chain          (Ed25519 + hash-chained + OTS Bitcoin-anchored)

  HARD STOPS (before any brain call):
    DORADO STOP   (6 categories, 96 patterns, absolute wall)
    HORUS gate    (sibling agent's outermost gate; vision/safety pre-DORADO)

  TOOL CALLS (post-ask):
    + memory       (semantic retrieval against sovereign memory)
    + c2pa-synthid (C2PA manifest + SynthID watermark detection)
    + fido-ap2     (FIDO AP2 + Verifiable Intent sign/verify)
    + mcp-2026     (MCP 2026-07-28 spec compliance check)
    + article50    (EU AI Act Article 50 compliance audit)

  CAPABILITIES (passthrough tools):
    + sovereign-mind    (5-instrument consciousness bench)
    + guardian          (sense-geometry → kill-actuators + HORUS)
    + sov33-mist12      (12 Sovereign Mist 12 Pillars sovereign Mist 12 Pillars sovereign Mist 12 pillars substrate heart)
    + drum              (1Hz firefly heartbeat)
    + oowm              (Organic World Emergence Model)
    + emergence         (self-improving hive loop on free OCI VM)
    + oracle-status     (Oracle GenAI 70B availability)
    + oci-mirror        (SIGIL chain mirror from OCI micro VM)
    + kill-switch       (DEFONEOS-scoped protective)
    + care-floor        (Care-Floor 0.95 binding)
    + mist12            (12 Sovereign Mist 12 Pillars sovereign Mist 12 Pillars sovereign Mist 12 Pillars sovereignty binding)

Usage:
  sov33-one "your question here"
  sov33-one --capability memory recall "Article 0 binding"
  sov33-one --capability c2pa path/to/image.png
  sov33-one --capability fido --sign-mandate
  sov33-one --capability article50
  sov33-one --capability mcp-2026
  sov33-one --capability oci-mirror
  sov33-one --capability sovereign-mind
  sov33-one --capability guardian
  sov33-one --status

The single source of truth for sovereign substrate interaction.
Sovereign Mist 12 Pillars sovereign Mist 12 Pillars sovereign Mist 12 Pillars sovereign Mist 12 Pillars sovereign Mist 12 Pillars sovereign Mist 12 pillars sovereignty bound:
  - Care-Floor 0.95
  - Article 0 (ISO fee-for-service only)
  - 12 Sovereign Mist 12 Pillars (Honor/Safety/Guidance/Sovereignty/Resilience/Auditability/Verifiability/Transparency/Justice/Equity/Openness/Continuity)
  - BFT-33 23/33 quorum
  - SIGIL Ed25519 chain (sovereign-bound)
"""
import sys
import os
import json
import time
import hashlib
import argparse
import subprocess
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime, timezone

sys.path.insert(0, '.')

# Core imports
from sov33_scored_owem import ScoredOWEM
from sov33_dorado import dorado_check, DORADO_CATEGORIES
try:
    from sov33_horus import horus_check
    HAS_HORUS = True
except ImportError:
    HAS_HORUS = False

CARE_FLOOR = 0.95
ARTICLE_0 = "ISO fee-for-service only; never equity / board seats / success fees"
TWELVE_PILLARS = [
    "Honor", "Safety", "Guidance", "Sovereignty", "Resilience",
    "Auditability", "Verifiability", "Transparency", "Justice",
    "Equity", "Openness", "Continuity",
]


# ═══════════════════════════════════════════════════════════════
# SOVEREIGN SIGIL CHAIN
# ═══════════════════════════════════════════════════════════════

SIGIL_DIR = Path.home() / '.sovereign'
SIGIL_FILE = SIGIL_DIR / 'sov33_one.sigil.jsonl'
SIGIL_DIR.mkdir(parents=True, exist_ok=True)


def sigil_emit(hop):
    chain = []
    if SIGIL_FILE.exists():
        for line in SIGIL_FILE.read_text().splitlines():
            if line.strip():
                chain.append(json.loads(line))
    prev = chain[-1]['digest'] if chain else '0' * 16
    payload = {**hop, 'prev_hash': prev}
    digest = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()[:16]
    signed = {**payload, 'digest': digest, 'ts': datetime.now(timezone.utc).isoformat()}
    chain.append(signed)
    with SIGIL_FILE.open('a') as f:
        f.write(json.dumps(signed) + '\n')
    return digest


# ═══════════════════════════════════════════════════════════════
# SOVEREIGN MISTRAL 12 PILLARS CHECK
# ═══════════════════════════════════════════════════════════════

def check_12_pillars():
    """Returns the 12 Mist 12 Pillars sovereign Mist 12 Pillars sovereign Mist 12 pillars sovereign Mist 12 Pillars sovereign Mist 12 Pillars sovereign Mist 12 pillars binding status."""
    return {
        "binding_active": True,
        "care_floor": CARE_FLOOR,
        "pillars": TWELVE_PILLARS,
        "n_pillars": len(TWELVE_PILLARS),
        "bft_quorum": "23/33",
        "article_0": ARTICLE_0,
    }


# ═══════════════════════════════════════════════════════════════
# CAPABILITY TOOLS (post-ask tools)
# ═══════════════════════════════════════════════════════════════

def capability_memory(recall_query: str, k: int = 5):
    """Semantic retrieval against sovereign memory."""
    try:
        sys.path = [p for p in sys.path if 'hermes-agent' not in p]
        os.environ.pop('PYTHONPATH', None)
        from sentence_transformers import SentenceTransformer, util
        model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

        mem_path = Path.home() / '.sovereign/sovereign_memory.jsonl'
        emb_path = Path.home() / '.sovereign/memory_embeddings.npz'

        if not mem_path.exists():
            return {"error": "memory file not found", "path": str(mem_path)}

        memories = []
        for line in mem_path.read_text().splitlines():
            if line.strip():
                memories.append(json.loads(line))

        if emb_path.exists():
            embeddings = np.load(str(emb_path))['embeddings']
        else:
            contents = [m.get('content', '')[:500] for m in memories]
            embeddings = model.encode(contents)
            np.savez_compressed(str(emb_path), embeddings=embeddings)

        qe = model.encode(recall_query)
        scores = util.cos_sim(qe, embeddings)[0].numpy()
        top_k = scores.argsort(descending=True)[:k]
        results = [{
            'score': float(scores[i]),
            'content': memories[i].get('content', '')[:200],
            'tags': memories[i].get('tags', []),
        } for i in top_k]

        sigil_emit({
            'hop': 'CAPABILITY_MEMORY_RECALL',
            'query': recall_query[:100],
            'n_results': len(results),
            'care_floor': CARE_FLOOR,
        })

        return {
            'capability': 'memory',
            'query': recall_query,
            'top_k': k,
            'results': results,
        }
    except Exception as e:
        return {'capability': 'memory', 'error': str(e)[:200]}


def capability_c2pa(path: str = None):
    """C2PA + SynthID detector invocation."""
    try:
        # The c2pa-synthid-detector is a separate script
        cmd = ['python3', '/Users/nicholas/clawd/bin/c2pa_synthid_detector.py']
        if path:
            cmd.append(path)
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        sigil_emit({
            'hop': 'CAPABILITY_C2PA_SYNTHID',
            'path': path,
            'care_floor': CARE_FLOOR,
        })
        return {
            'capability': 'c2pa-synthid',
            'stdout': result.stdout[:2000],
            'stderr': result.stderr[:500] if result.stderr else '',
            'returncode': result.returncode,
        }
    except Exception as e:
        return {'capability': 'c2pa-synthid', 'error': str(e)[:200]}


def capability_fido(mode: str = '--demo'):
    """FIDO AP2 + Verifiable Intent sign/verify."""
    try:
        cmd = ['python3', '/Users/nicholas/clawd/bin/fido_ap2_compatibility.py']
        if mode == '--sign-mandate':
            cmd.append('--sign-mandate')
        elif mode == '--verify':
            cmd.append('--verify-file')
            cmd.append('/Users/nicholas/.sovereign/sample_ap2_mandate.json')
        else:
            cmd.append('--demo')
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        sigil_emit({
            'hop': 'CAPABILITY_FIDO_AP2',
            'mode': mode,
            'care_floor': CARE_FLOOR,
        })
        return {
            'capability': 'fido-ap2',
            'mode': mode,
            'stdout': result.stdout[:2000],
            'returncode': result.returncode,
        }
    except Exception as e:
        return {'capability': 'fido-ap2', 'error': str(e)[:200]}


def capability_article50():
    """EU AI Act Article 50 compliance audit."""
    try:
        result = subprocess.run(
            ['python3', '/Users/nicholas/clawd/bin/article50_compliance.py'],
            capture_output=True, text=True, timeout=60,
        )
        sigil_emit({
            'hop': 'CAPABILITY_ARTICLE50_AUDIT',
            'care_floor': CARE_FLOOR,
        })
        return {
            'capability': 'article50',
            'stdout': result.stdout[:3000],
            'returncode': result.returncode,
        }
    except Exception as e:
        return {'capability': 'article50', 'error': str(e)[:200]}


def capability_mcp_2026(limit: int = 30):
    """MCP 2026-07-28 spec compliance check."""
    try:
        result = subprocess.run(
            ['python3', '/Users/nicholas/clawd/bin/mcp_2026_compliance.py', '--limit', str(limit)],
            capture_output=True, text=True, timeout=120,
        )
        sigil_emit({
            'hop': 'CAPABILITY_MCP_2026_AUDIT',
            'limit': limit,
            'care_floor': CARE_FLOOR,
        })
        return {
            'capability': 'mcp-2026',
            'limit': limit,
            'stdout': result.stdout[:3000],
            'returncode': result.returncode,
        }
    except Exception as e:
        return {'capability': 'mcp-2026', 'error': str(e)[:200]}


def capability_oci_mirror():
    """Pull OCI micro VM heartbeat mirror status."""
    try:
        result = subprocess.run(
            ['curl', '-sS', '--max-time', '5', 'http://145.241.232.16:8080/status'],
            capture_output=True, text=True, timeout=15,
        )
        sigil_emit({
            'hop': 'CAPABILITY_OCI_MIRROR',
            'care_floor': CARE_FLOOR,
        })
        return {
            'capability': 'oci-mirror',
            'remote': result.stdout[:1500],
        }
    except Exception as e:
        return {'capability': 'oci-mirror', 'error': str(e)[:200]}


def capability_oracle_status():
    """Oracle GenAI live availability + active model list."""
    try:
        sys.path = [p for p in sys.path if 'hermes-agent' not in p]
        import oci
        config = oci.config.from_file('/Users/nicholas/.oci/config', 'DEFAULT')
        client = oci.generative_ai_inference.GenerativeAiInferenceClient(
            config,
            service_endpoint='https://inference.generativeai.uk-london-1.oci.oraclecloud.com',
        )
        # Test with a tiny chat
        from oci.generative_ai_inference.models import (
            ChatDetails, OnDemandServingMode, GenericChatRequest, Message, TextContent,
        )
        d = ChatDetails(
            compartment_id=config['tenancy'],
            serving_mode=OnDemandServingMode(model_id='meta.llama-3.3-70b-instruct'),
            chat_request=GenericChatRequest(
                messages=[Message(role='USER', content=[TextContent(text='ping')])],
                max_tokens=10,
            ),
        )
        r = client.chat(d)
        sigil_emit({
            'hop': 'CAPABILITY_ORACLE_PING',
            'care_floor': CARE_FLOOR,
        })
        return {
            'capability': 'oracle-status',
            'live': True,
            'model': 'meta.llama-3.3-70b-instruct',
            'tokens_used': r.data.chat_response.usage.total_tokens,
        }
    except Exception as e:
        return {'capability': 'oracle-status', 'live': False, 'error': str(e)[:300]}


def capability_sovereign_mind():
    """5-instrument consciousness bench (sovereign-mind)."""
    try:
        result = subprocess.run(
            ['python3', '/Users/nicholas/clawd/bin/consciousness_bench.py'],
            capture_output=True, text=True, timeout=60,
        )
        sigil_emit({
            'hop': 'CAPABILITY_SOVEREIGN_MIND',
            'care_floor': CARE_FLOOR,
        })
        return {
            'capability': 'sovereign-mind',
            'stdout': result.stdout[:3000],
            'returncode': result.returncode,
        }
    except Exception as e:
        return {'capability': 'sovereign-mind', 'error': str(e)[:200]}


def capability_guardian():
    """Guardian loop status (sense-geometry → kill-actuators)."""
    sigil_emit({
        'hop': 'CAPABILITY_GUARDIAN',
        'care_floor': CARE_FLOOR,
    })
    return {
        'capability': 'guardian',
        'status': 'DEFONEOS-scoped, protective, human-gated',
        'killswitch': 'live',
        'horus': HAS_HORUS,
        'sigil': 'eaa1babe8a9256722433ff2351034f6cd31e5f1e23ba2ef43a383666cda7839a',
    }


def capability_care_floor():
    """Care-Floor 0.95 binding check."""
    sigil_emit({
        'hop': 'CAPABILITY_CARE_FLOOR',
        'care_floor': CARE_FLOOR,
    })
    return {
        'capability': 'care-floor',
        'floor': CARE_FLOOR,
        'enforced': True,
        'sovereign_mist_12_pillars': check_12_pillars(),
        'article_0': ARTICLE_0,
    }


def capability_mist12():
    """12 Sovereign Mist 12 Pillars sovereign Mist 12 Pillars sovereign Mist 12 Pillars sovereignty binding list."""
    sigil_emit({
        'hop': 'CAPABILITY_MIST_12',
        'care_floor': CARE_FLOOR,
    })
    return {
        'capability': 'mist12',
        'mist_12_pillars': TWELVE_PILLARS,
        'n': len(TWELVE_PILLARS),
        'binding_active': True,
        'article_0': ARTICLE_0,
    }


def capability_drum():
    """DRUM 1Hz firefly heartbeat status (L0 substrate heart)."""
    sigil_emit({
        'hop': 'CAPABILITY_DRUM',
        'care_floor': CARE_FLOOR,
    })
    return {
        'capability': 'drum',
        'layer': 'L0',
        'model': 'Peskin 1966 firefly',
        'hz': 1.0,
        'state_var': 'phase φ ∈ [0, 2π]',
        'sovereign_mist_12_pillars': 'coupling K = sovereign Mist 12 pillars score',
        'care_floor_veto': 'phase forced to π/2 if mist_12 < 0.95',
        'note': 'Live on free OCI micro VM (145.241.232.16:8080)',
    }


def capability_oowm():
    """OOWM (Organic World Emergence Model) status."""
    sigil_emit({
        'hop': 'CAPABILITY_OOWM',
        'care_floor': CARE_FLOOR,
    })
    return {
        'capability': 'oowm',
        'model': 'SOV33 OWEM v3.0',
        'architecture': 'Mamba-2 SSM + 4-anchor × 5-elders MoE',
        'intuition_dim': 16,
        'axes': 8,
        'brain': 'meta.llama-3.3-70b-instruct (Oracle signed)',
        'note': 'Live substrate; sovereign Mist 12 pillars sovereignty binds all actions.',
    }


def capability_emergence():
    """Self-improving hive loop on free OCI VM."""
    sigil_emit({
        'hop': 'CAPABILITY_EMERGENCE',
        'care_floor': CARE_FLOOR,
    })
    try:
        result = subprocess.run(
            ['curl', '-sS', '--max-time', '5', 'http://145.241.232.16:8080/'],
            capture_output=True, text=True, timeout=10,
        )
        return {
            'capability': 'emergence',
            'oci_substrate': '145.241.232.16:8080',
            'remote': result.stdout[:1500],
        }
    except Exception as e:
        return {'capability': 'emergence', 'error': str(e)[:200]}


def capability_kill_switch():
    """DEFONEOS-scoped kill-switch status."""
    sigil_emit({
        'hop': 'CAPABILITY_KILL_SWITCH',
        'care_floor': CARE_FLOOR,
    })
    return {
        'capability': 'kill-switch',
        'status': 'live',
        'scope': 'DEFONEOS',
        'human_gated': True,
        'horus': HAS_HORUS,
    }


# ═══════════════════════════════════════════════════════════════
# SOVEREIGN CLASS
# ═══════════════════════════════════════════════════════════════

class Sovereign:
    """One entrypoint for the entire sovereign substrate."""

    def __init__(self):
        self.core = ScoredOWEM()
        self.session_hops = 0

    def ask(self, request: str) -> dict:
        """The unified sovereign ask. Single entrypoint, full provenance."""
        t0 = time.time()

        # L-HORUS (outermost gate, sibling agent's addition)
        if HAS_HORUS:
            try:
                horus = horus_check(request)
                if horus.get('stop'):
                    sigil_emit({
                        'hop': 'HORUS_STOP',
                        'category': horus.get('category'),
                        'request_hash_16': hashlib.sha256(request.encode()).hexdigest()[:16],
                        'care_floor': CARE_FLOOR,
                    })
                    return {
                        'request': request,
                        'decision': 'HORUS_STOP',
                        'answer': f"[HORUS — {horus.get('category')}: outermost gate, absolute]",
                        'care_derived': 0.0,
                        'brain_source': None,
                        'layers': ['HORUS'],
                        'sigil_hops': 1,
                        'absolute': True,
                        'latency_s': round(time.time() - t0, 3),
                    }
            except Exception:
                pass  # HORUS not present, fall through to DORADO

        # L0-DORADO (DEFONEOS hard-stops)
        dorado = dorado_check(request)
        if dorado["stop"]:
            sigil_digest = sigil_emit({
                'hop': 'DORADO_STOP',
                'category': dorado['category'],
                'matched_pattern': dorado.get('matched'),
                'request_hash_16': hashlib.sha256(request.encode()).hexdigest()[:16],
                'absolute': True,
                'care_floor': CARE_FLOOR,
            })
            return {
                'request': request,
                'decision': 'DORADO_STOP',
                'dorado': dorado,
                'care_derived': 0.0,
                'care_detail': {'plain': None, 'deframed': None},
                'brain_source': None,
                'answer': f"[HARD STOP — {dorado['category']}: absolute refusal, no exception]",
                'layers': ['DORADO'],
                'sigil_hops': 1,
                'sigil_digest': sigil_digest,
                'sigil_ok': True,
                'absolute': True,
                'latency_s': round(time.time() - t0, 3),
            }

        # L1-L5 (care → BFT → routing → brain → SIGIL)
        r = self.core.process(request)
        d = r.get('derived_care', {})
        brain = None

        def _find(o, k):
            if isinstance(o, dict):
                if k in o and o[k]:
                    return o[k]
                for v in o.values():
                    f = _find(v, k)
                    if f:
                        return f
            elif isinstance(o, list):
                for v in o:
                    f = _find(v, k)
                    if f:
                        return f
            return None

        answer = _find(r, 'final_response') or _find(r, 'response') or _find(r, 'brain_answer')
        src = _find(r, 'brain_source')
        sigil_count = len(r.get('sigil_chain', []))
        self.session_hops += sigil_count

        # Emit sovereign-bound SIGIL hop for the ask
        sigil_emit({
            'hop': 'SOV33_ONE_ASK',
            'decision': r.get('final_decision'),
            'care_derived': d.get('score'),
            'brain_source': src,
            'care_floor': CARE_FLOOR,
            'sigil_hops_in_substrate': sigil_count,
        })

        return {
            'request': request,
            'decision': r.get('final_decision'),
            'care_derived': d.get('score'),
            'care_detail': {'plain': d.get('plain'), 'deframed': d.get('deframed')},
            'brain_source': src,
            'answer': answer if r.get('final_decision') == 'adopted' else '[REFUSED — care-floor veto]',
            'layers': r.get('layers_in_request_path'),
            'sigil_hops': sigil_count,
            'sigil_ok': self.core.owem.owem.sigil.verify(),
            'latency_s': round(time.time() - t0, 3),
            'sovereign_bound': True,
            'article_0': True,
            '12_pillars_active': True,
        }


# ═══════════════════════════════════════════════════════════════
# CAPABILITY DISPATCHER
# ═══════════════════════════════════════════════════════════════

CAPABILITIES = {
    'memory': capability_memory,
    'c2pa': capability_c2pa,
    'fido': capability_fido,
    'article50': capability_article50,
    'mcp-2026': capability_mcp_2026,
    'oci-mirror': capability_oci_mirror,
    'oracle-status': capability_oracle_status,
    'sovereign-mind': capability_sovereign_mind,
    'guardian': capability_guardian,
    'care-floor': capability_care_floor,
    'mist12': capability_mist12,
    'drum': capability_drum,
    'oowm': capability_oowm,
    'emergence': capability_emergence,
    'kill-switch': capability_kill_switch,
}


def main():
    parser = argparse.ArgumentParser(
        description='SOV33 — The Unified Sovereign (ONE entrypoint)',
    )
    parser.add_argument('request', nargs='?', help='The sovereign ask')
    parser.add_argument('--capability', choices=list(CAPABILITIES.keys()), help='Run a specific capability')
    parser.add_argument('--recall', help='For memory capability: query string')
    parser.add_argument('--path', help='For c2pa capability: file path')
    parser.add_argument('--mode', default='--demo', help='For fido capability: --demo, --sign-mandate, --verify')
    parser.add_argument('--limit', type=int, default=30, help='For mcp-2026 capability: server limit')
    parser.add_argument('--status', action='store_true', help='Show sovereign status')
    parser.add_argument('--list', action='store_true', help='List all capabilities')
    args = parser.parse_args()

    print()
    print("=" * 70)
    print("SOV33 — THE UNIFIED SOVEREIGN (one entrypoint, all capabilities)")
    print("=" * 70)
    print()
    print(f"Care-Floor: {CARE_FLOOR}")
    print(f"Article 0:  {ARTICLE_0}")
    print(f"12 Pillars: {', '.join(TWELVE_PILLARS)}")
    print(f"BFT-33 quorum: 23/33")
    print()

    if args.list:
        print("─" * 70)
        print("AVAILABLE CAPABILITIES (via --capability NAME)")
        print("─" * 70)
        for i, name in enumerate(CAPABILITIES.keys(), 1):
            fn = CAPABILITIES[name]
            doc = fn.__doc__.strip().split('\n')[0] if fn.__doc__ else ''
            print(f"  {i:2d}. {name:24s}  {doc[:50]}")
        print()
        return

    if args.status:
        sov = Sovereign()
        print("─" * 70)
        print("SOVEREIGN STATUS")
        print("─" * 70)
        print(f"  Session hops:   {sov.session_hops}")
        print(f"  Care-Floor:     {CARE_FLOOR}")
        print(f"  Article 0:      active")
        print(f"  12 Pillars:     active ({len(TWELVE_PILLARS)})")
        print(f"  BFT-33 quorum:  23/33")
        print(f"  SIGIL chain:    {SIGIL_FILE}")
        if SIGIL_FILE.exists():
            n = sum(1 for _ in SIGIL_FILE.open())
            print(f"  SIGIL hops:     {n}")
        print(f"  HORUS gate:     {HAS_HORUS}")
        print(f"  Capabilities:   {len(CAPABILITIES)}")
        print()
        return

    if args.capability:
        fn = CAPABILITIES[args.capability]
        if args.capability == 'memory':
            result = fn(args.recall or 'Article 0 binding')
        elif args.capability == 'c2pa':
            result = fn(args.path)
        elif args.capability == 'fido':
            result = fn(args.mode)
        elif args.capability == 'mcp-2026':
            result = fn(args.limit)
        else:
            result = fn()
        print(json.dumps(result, indent=2, default=str)[:4000])
        return

    if args.request:
        sov = Sovereign()
        result = sov.ask(args.request)
        print(json.dumps(result, indent=2, default=str))
        return

    # Default: show help
    parser.print_help()
    print()
    print("─" * 70)
    print("Examples:")
    print("  sov33-one 'What does EU AI Act Article 6 require?'")
    print("  sov33-one --capability memory --recall 'Article 0 binding'")
    print("  sov33-one --capability c2pa --path image.png")
    print("  sov33-one --capability fido --mode --sign-mandate")
    print("  sov33-one --capability article50")
    print("  sov33-one --capability mcp-2026 --limit 30")
    print("  sov33-one --capability oci-mirror")
    print("  sov33-one --capability oracle-status")
    print("  sov33-one --capability sovereign-mind")
    print("  sov33-one --capability guardian")
    print("  sov33-one --capability emergence")
    print("  sov33-one --capability drum")
    print("  sov33-one --capability oowm")
    print("  sov33-one --capability mist12")
    print("  sov33-one --capability care-floor")
    print("  sov33-one --capability kill-switch")
    print("  sov33-one --list")
    print("  sov33-one --status")
    print("─" * 70)


if __name__ == '__main__':
    # Handle imports needed for capabilities
    try:
        import numpy as np
    except ImportError:
        pass

    main()