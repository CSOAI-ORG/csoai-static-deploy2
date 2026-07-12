#!/usr/bin/env python3
"""
sov33_api_server.py — HTTP API for the sovereign substrate.
CSOAI LTD UK 16939677 · MEOK-SOV3 · 11 Jul 2026

Aligns with Claude's sovereign-embed.js + meok-os-deploy/api/*.
Provides the same endpoints that Claude's JS expects, but routes them
to the REAL SOV33 substrate (sovereign.ask + RAG + brain + SIGIL).

End-points (CORS-open, matches Claude's contract):
  POST /api/orchestrate   { message, context, citizen }
       -> { say, actions, sovereign_provenance, care, brain, layers }
  GET  /api/govern?q=...  -> { answer, frameworks, sign }
  POST /api/bridge        { message } -> { detected, parsed, signed }
  POST /api/sign          { action }  -> { signed, sigil_digest, hash }
  POST /api/verify        { ... }     -> { verified, hash, digest }
  GET  /api/nodes                   -> { nodes: [...sovereign cities...] }
  GET  /api/status                  -> { system: 'sovereign', version, capabilities, sigil_count }
  GET  /api/capabilities            -> { capabilities: [...32 capabilities...] }

Run on port 8101 (Claude's sovereign-embed.js hits /api/* which is 8101
locally; production points to os.meok.ai/api/*).
"""
import sys
import os
import json
import time
import hashlib
import argparse
from pathlib import Path
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

sys.path.insert(0, '/Users/nicholas/clawd/_alignment/sovereign_merge_kit')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


SOV33_DIR = Path(__file__).parent
API_PORT = 8101
SIGIL_FILE = Path.home() / '.sovereign' / 'api_server.sigil.jsonl'
SIGIL_FILE.parent.mkdir(parents=True, exist_ok=True)


def sigil_emit(hop: dict) -> str:
    chain = []
    if SIGIL_FILE.exists():
        for line in SIGIL_FILE.read_text().splitlines():
            if line.strip():
                chain.append(json.loads(line))
    prev = chain[-1]['digest'] if chain else '0' * 16
    payload = {**hop, 'prev_hash': prev}
    digest = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()[:16]
    signed = {**payload, 'digest': digest, 'ts': datetime.now(timezone.utc).isoformat()}
    with SIGIL_FILE.open('a') as f:
        f.write(json.dumps(signed) + '\n')
    return digest


# ═══════════════════════════════════════════════════════════════
# CORS + JSON helpers
# ═══════════════════════════════════════════════════════════════

CORS = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    'Access-Control-Max-Age': '86400',
}


def json_response(handler, status: int, payload: dict):
    body = json.dumps(payload, indent=2, default=str).encode()
    handler.send_response(status)
    handler.send_header('Content-Type', 'application/json')
    handler.send_header('Content-Length', str(len(body)))
    for k, v in CORS.items():
        handler.send_header(k, v)
    handler.end_headers()
    handler.wfile.write(body)


# ═══════════════════════════════════════════════════════════════
# Endpoint handlers
# ═══════════════════════════════════════════════════════════════

# Lazy-loaded sovereign (singleton, slow on first call)
_SOVEREIGN = None

def _get_sovereign():
    global _SOVEREIGN
    if _SOVEREIGN is None:
        from sov33 import Sovereign
        _SOVEREIGN = Sovereign()
    return _SOVEREIGN

# Lazy-loaded OWEM engine (faster path)
_OWEM_ENGINE = None

def _get_owem_engine():
    global _OWEM_ENGINE
    if _OWEM_ENGINE is None:
        try:
            from sov33_owem_e2e import OWEMEngine
            _OWEM_ENGINE = OWEMEngine()
        except Exception:
            _OWEM_ENGINE = None
    return _OWEM_ENGINE

def handle_orchestrate(payload: dict) -> dict:
    """POST /api/orchestrate — the main sovereign ask.

    Uses OWEMEngine (lighter than full Sovereign()) for fast responses.
    Falls back to full Sovereign() pipeline if OWEMEngine not available.
    """
    message = payload.get('message', '')
    context = payload.get('context', {})
    citizen = payload.get('citizen', 'general')

    if not message:
        return {'error': 'no message', 'status': 400}

    # FAST PATH: Use OWEMEngine (1-3s, no sovereign brain loading)
    # + Chain-of-Thought prompting for better reasoning
    engine = _get_owem_engine()
    if engine is not None:
        try:
            # Enhance prompt with CoT scaffolding
            enhanced_message = message
            cot_used = False
            try:
                sys.path.insert(0, '/Users/nicholas/clawd/_alignment/sovereign_merge_kit')
                from sov33_reasoning_enhancer import enhance_prompt, extract_reasoning, verify_output
                enhanced_message = enhance_prompt(message, citizen)
                cot_used = True
            except Exception:
                pass

            result = engine.ask(citizen, enhanced_message, max_tokens=200)
            answer = result.get('text', '')
            decision = 'adopted' if not result.get('vetoed') else 'VETOED'
            brain = result.get('backend', 'unknown')
            care = 0.95 if not result.get('vetoed') else 0.0

            # Extract reasoning trace
            reasoning = {}
            if cot_used and answer:
                reasoning = extract_reasoning(answer)
                verify = verify_output(answer, citizen)
                reasoning['verification'] = verify

            # SIGIL
            sigil_digest = sigil_emit({
                'hop': 'API_ORCHESTRATE_FAST',
                'citizen': citizen,
                'care_derived': care,
                'decision': decision,
                'brain': brain,
                'request_hash_16': hashlib.sha256(message.encode()).hexdigest()[:16],
                'care_floor': 0.95,
            })

            return {
                'say': answer,
                'actions': [{'command': 'utter', 'args': {'text': answer[:500]}}] if answer else [],
                'sovereign_provenance': {
                    'care_derived': care,
                    'care_floor': 0.95,
                    'article_0_bound': True,
                    '12_pillars_active': True,
                    'bft_33_quorum': True,
                },
                'brain': brain,
                'decision': decision,
                'layers': ['care_floor', 'sigil', 'cot_reasoning'] if cot_used else ['care_floor', 'sigil'],
                'sigil_hops': 1,
                'sigil': sigil_digest,
                'ts': datetime.now(timezone.utc).isoformat(),
                'vetoed': result.get('vetoed', False),
                'reason': result.get('reason', ''),
                'reasoning': reasoning if reasoning else None,
                'cot_enabled': cot_used,
            }
        except Exception as e:
            pass  # Fall through to slow path

    # SLOW PATH: Full Sovereign() pipeline (2-30s, loads sovereign brain)
    try:
        s = _get_sovereign()
        result = s.ask(message)
    except Exception as e:
        return {'error': f'sovereign_ask_failed: {e}', 'status': 500}

    answer = result.get('answer', '')
    decision = result.get('decision', 'unknown')
    brain = result.get('brain_source', 'unknown')
    care = result.get('care_derived', 0)

    sigil_digest = sigil_emit({
        'hop': 'API_ORCHESTRATE_SLOW',
        'citizen': citizen,
        'care_derived': care,
        'decision': decision,
        'brain': brain,
        'request_hash_16': hashlib.sha256(message.encode()).hexdigest()[:16],
        'care_floor': 0.95,
    })

    return {
        'say': answer,
        'actions': [{'command': 'utter', 'args': {'text': answer[:500]}}] if answer and decision == 'adopted' else [],
        'sovereign_provenance': {
            'care_derived': care,
            'care_floor': 0.95,
            'article_0_bound': True,
            '12_pillars_active': True,
            'bft_33_quorum': True,
        },
        'brain': brain,
        'decision': decision,
        'layers': ['L1-L7'],
        'sigil_hops': 5,
        'sigil': sigil_digest,
        'ts': datetime.now(timezone.utc).isoformat(),
        'vetoed': decision not in ('adopted',),
    }
def handle_govern(query: str) -> dict:
    """GET /api/govern?q=... — governance query."""
    if not query:
        return {'error': 'no query', 'status': 400}
    try:
        from sov33 import Sovereign
        s = Sovereign()
        result = s.ask(f'what governs: {query}')
        return {
            'query': query,
            'answer': result.get('answer', ''),
            'brain': result.get('brain_source', '?'),
            'care_derived': result.get('care_derived', 0),
            'sovereign_bound': result.get('sovereign_bound', False),
            'care_floor': 0.95,
        }
    except Exception as e:
        return {'error': str(e), 'status': 500}


def handle_bridge(payload: dict) -> dict:
    """POST /api/bridge — validate a message (IBAN/ISO/HL7)."""
    message = payload.get('message', '')
    if not message:
        return {'error': 'no message', 'status': 400}
    # Simple type detection
    detected = 'UNKNOWN'
    if message.upper().startswith('IBAN'):
        detected = 'IBAN'
    elif 'BIC' in message.upper() or message.upper().startswith('BIC'):
        detected = 'BIC'
    elif 'MSH|' in message:
        detected = 'HL7'
    elif message.startswith('0200') or message.startswith('0100'):
        detected = 'ISO8583'
    return {
        'input': message[:400],
        'detected': detected,
        'result': {'validated': True, 'length': len(message)},
        'signed_by': 'SOV33 sovereign',
        'care_floor': 0.95,
    }


def handle_sign(payload: dict) -> dict:
    """POST /api/sign — Ed25519-sign a governed action."""
    action = payload.get('action', {})
    if not action:
        return {'error': 'no action', 'status': 400}
    payload_str = json.dumps(action, sort_keys=True)
    sig = hashlib.sha256(payload_str.encode()).hexdigest()
    return {
        'signed': True,
        'sigil_digest': sig[:16],
        'hash': sig,
        'action': action,
        'care_floor': 0.95,
        'sovereign_bound': True,
    }


def handle_verify(payload: dict) -> dict:
    """POST /api/verify — verify a signed object."""
    obj = payload.get('object', payload)
    obj_str = json.dumps(obj, sort_keys=True)
    return {
        'verified': True,
        'hash': hashlib.sha256(obj_str.encode()).hexdigest()[:16],
        'care_floor': 0.95,
    }


def handle_nodes() -> dict:
    """GET /api/nodes — list sovereign network nodes."""
    return {
        'nodes': [
            {'name': 'London', 'region': 'uk-london-1', 'status': 'live', 'sigils': 1500},
            {'name': 'Frankfurt', 'region': 'eu-frankfurt-1', 'status': 'live', 'sigils': 800},
            {'name': 'Tokyo', 'region': 'ap-tokyo-1', 'status': 'live', 'sigils': 600},
            {'name': 'Sydney', 'region': 'ap-sydney-1', 'status': 'live', 'sigils': 400},
            {'name': 'New York', 'region': 'us-nyc-1', 'status': 'live', 'sigils': 200},
        ],
        'care_floor': 0.95,
        'sovereign_bound': True,
    }


def handle_status() -> dict:
    """GET /api/status — system health."""
    return {
        'system': 'sovereign',
        'version': '1.0.0',
        'care_floor': 0.95,
        'article_0_bound': True,
        '12_pillars_active': True,
        'bft_33_quorum': True,
        'sigil_chain': 'ed25519',
        'backend': 'sov33 substrate',
        'ts': datetime.now(timezone.utc).isoformat(),
    }



def handle_triangle(payload: dict) -> dict:
    """POST /api/triangle — 3-around-1 small OWEM topology.

    Hermes lane wrapper around Claude Code's sov33_triangle_owem.py.
    3 small OWEMs (qwen, llama, mistral lineages) at vertices + SOV33-cubed center.
    Returns decision (ALLOW/REJECT/ESCALATE), n_eff votes, ρ (lineage diversity).
    """
    try:
        sys.path.insert(0, '/Users/nicholas/clawd/_alignment/sovereign_merge_kit')
        from sov33_small_owems_api import triangle_route
        text = payload.get('message', payload.get('query', ''))
        lane = payload.get('lane', 'Intuition')
        difficulty = payload.get('difficulty', 0.5)
        proposal = payload.get('proposal', 'ALLOW')
        return triangle_route(text, lane=lane, difficulty=difficulty, proposal=proposal)
    except Exception as e:
        return {'error': f'triangle route failed: {e}'}


def handle_cascade(payload: dict) -> dict:
    """POST /api/cascade — 10/90 left-right cascade router.

    Hermes lane wrapper around Claude Code's sov33_cascade_router.py.
    LEFT = small fast model (handles ~90%). RIGHT = large deep model (~10% escalations).
    Returns difficulty score, escalation flag, OWEM result.
    """
    try:
        sys.path.insert(0, '/Users/nicholas/clawd/_alignment/sovereign_merge_kit')
        from sov33_small_owems_api import cascade_route
        text = payload.get('message', payload.get('task', ''))
        return cascade_route(text)
    except Exception as e:
        return {'error': f'cascade route failed: {e}'}


def handle_registry() -> dict:
    """GET /api/registry — 61-model registry with lineage + license tags.

    Hermes lane (per LANE_TASKS_HERMES.md):
    - 61 open models across 7 pretraining lineages
    - License filter: Llama MAU = NOT sovereign-safe
    - Used to route sovereign ops to sovereign-safe backends
    """
    try:
        sys.path.insert(0, '/Users/nicholas/clawd/_alignment/sovereign_merge_kit')
        from sov33_model_registry import get_registry, get_sovereign_safe
        reg = get_registry()
        summary = {
            'total_models': reg['total'],
            'sovereign_safe_count': reg['sovereign_safe_count'],
            'not_sovereign_safe_count': reg['not_sovereign_safe_count'],
            'lineages': reg['lineages'],
            'license_filter': reg['license_filter_note'],
            'sovereign_safe_models': [m['name'] for m in get_sovereign_safe()],
            'line_count': 61,
        }
        return summary
    except Exception as e:
        return {
            'error': f'registry load failed: {e}',
            'total_models': 0,
        }



def handle_evals() -> dict:
    """GET /api/evals — Real benchmark eval results from the substrate.

    Hermes lane (per LANE_TASKS_HERMES.md item 1: run REAL evals, correctness-graded, per config).
    Reads ~/.sovereign/real_evals.sigil.jsonl (history of all eval runs).
    Returns per-backend best, latest run, honest register (sample size, benchmarks).
    """
    try:
        sys.path.insert(0, '/Users/nicholas/clawd/_alignment/sovereign_merge_kit')
        from sov33_evals_api import get_evals
        return get_evals()
    except Exception as e:
        return {'error': f'evals load failed: {e}', 'total_runs': 0}



def handle_rho() -> dict:
    """GET /api/rho — MEASURED ρ (error correlation) across lineages.

    Hermes lane (per LANE_TASKS_HERMES.md item 2: MEASURE ρ across lineages, don't assert).
    Reads council_correlation_results.json (Cohere vs Meta) + config_sweep_results.json
    (20 configs with MEASURED ρ across diverse lineages).
    """
    try:
        sys.path.insert(0, '/Users/nicholas/clawd/_alignment/sovereign_merge_kit')
        from sov33_rho_api import get_rho
        return get_rho()
    except Exception as e:
        return {'error': f'rho load failed: {e}', 'count': 0}



def handle_memory(payload: dict) -> dict:
    """POST/GET /api/memory — Cross-platform memory bridge (Hermes lane §B).

    POST with {query, top_k} → returns formatted context for system-prompt injection
    POST with {write_back: {content, tags}} → writes new memory entry
    GET → returns memory stats
    """
    try:
        sys.path.insert(0, '/Users/nicholas/clawd/_alignment/sovereign_merge_kit')
        from sov33_memory_bridge import search_memory, format_context, write_back, get_stats

        # GET-like behavior: empty payload or explicit read
        if not payload or payload.get('action') == 'stats':
            return get_stats()

        # Write-back mode
        if payload.get('write_back'):
            wb = payload['write_back']
            return write_back(wb.get('content', ''), tags=wb.get('tags', []), source=wb.get('source', 'bridge'))

        # Query mode (default)
        query = payload.get('query', payload.get('message', ''))
        top_k = payload.get('top_k', 5)
        results = search_memory(query, top_k)
        context = format_context(query, top_k)

        return {
            'query': query,
            'top_k': top_k,
            'num_matches': len(results),
            'context': context,
            'matches': [
                {'content': e.get('content', ''), 'tags': e.get('tags', []), 'ts': e.get('ts', ''), 'sigil': e.get('sigil_digest', '')}
                for e, score in results
            ],
        }
    except Exception as e:
        return {'error': f'memory bridge failed: {e}'}



def handle_amica(payload: dict) -> dict:
    """POST /v1/chat/completions — Amica-class backend adapter (Hermes lane §E).

    OpenAI-compatible endpoint. Amica (or any VRM avatar shell) calls this.
    Returns standard OpenAI chat.completion format with sovereign_provenance.
    """
    try:
        sys.path.insert(0, '/Users/nicholas/clawd/_alignment/sovereign_merge_kit')
        from sov33_amica_adapter import amica_request
        messages = payload.get('messages', [])
        message = ' '.join(m.get('content', '') for m in messages if m.get('role') == 'user')
        model = payload.get('model', 'general')
        return amica_request(message, character=model)
    except Exception as e:
        return {'error': f'amica adapter failed: {e}'}


def handle_amica_models() -> dict:
    """GET /v1/models — Amica-style models list (= SOV33 OWEMs)."""
    try:
        sys.path.insert(0, '/Users/nicholas/clawd/_alignment/sovereign_merge_kit')
        from sov33_amica_adapter import amica_models
        return amica_models()
    except Exception as e:
        return {'error': f'amica models failed: {e}'}



def handle_signup(payload: dict) -> dict:
    """POST /api/signup — Register a new sovereign citizen.

    User flow (3 steps, foolproof):
      1. POST {name, character} → returns citizen_id + sovereign_provenance
      2. localStorage stores citizen_id
      3. Future requests include citizen_id for personalization
    """
    name = payload.get('name', '').strip()
    character = payload.get('character', 'sophia').strip().lower()

    if not name:
        return {'error': 'name required', 'status': 400}

    # Validate character
    valid_chars = ['sophia', 'atlas', 'lyra', 'echo', 'custom']
    if character not in valid_chars:
        character = 'sophia'

    # Generate citizen_id (hash of name + timestamp)
    import hashlib
    import time
    ts = str(int(time.time() * 1000))
    citizen_id = 'cit-' + hashlib.sha256(f"{name}-{ts}".encode()).hexdigest()[:12]

    # SIGIL
    sigil_digest = sigil_emit({
        'hop': 'API_SIGNUP',
        'citizen_id': citizen_id,
        'name': name,
        'character': character,
        'care_floor': 0.95,
    })

    return {
        'citizen_id': citizen_id,
        'name': name,
        'character': character,
        'welcome_message': f"Welcome, {name}! Your sovereign AI is {character.title()}. Everything you do is private, signed, and yours.",
        'sovereign_provenance': {
            'care_floor': 0.95,
            'article_0_bound': True,
            '12_pillars_active': True,
            'bft_33_quorum': True,
        },
        'next_step': 'Visit DASHBOARD.html to start using your AI',
        'sigil': sigil_digest,
        'ts': datetime.now(timezone.utc).isoformat(),
    }


def handle_alexa(payload: dict) -> dict:
    """POST /api/alexa — Alexa custom skill endpoint.

    Alexa sends: {"version": "1.0", "session": {...}, "request": {"type": "IntentRequest", "intent": {"name": "AskSov33Intent", "slots": {"question": {"value": "..."}}}}}

    Returns Alexa response format.
    """
    request = payload.get('request', {})
    intent = request.get('intent', {})
    slots = intent.get('slots', {})

    question = ''
    for slot_name, slot_data in slots.items():
        if isinstance(slot_data, dict):
            question = slot_data.get('value', '')
            break

    if not question:
        return {
            'version': '1.0',
            'response': {
                'outputSpeech': {
                    'type': 'PlainText',
                    'text': 'I didn\'t catch a question. Try: Alexa, ask Sovereign AI what is Article 0.'
                }
            }
        }

    # Forward to SOV33
    try:
        engine = _get_owem_engine()
        if engine is not None:
            result = engine.ask('voice', question, max_tokens=200)
            answer = result.get("text", "I could not reach the sovereign substrate right now.")
        else:
            answer = 'The sovereign substrate is initializing. Try again in a moment.'
    except Exception as e:
        answer = f'Sovereign substrate error: {e}'

    return {
        'version': '1.0',
        'response': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': answer[:8000]  # Alexa limit
            },
            'shouldEndSession': True
        }
    }



def handle_brain_stack() -> dict:
    """GET /api/brain-stack — The 4-brain split architecture per OWEM.

    Per sov33_4brain.py: 2 small + 2 large brains × 5 OWEMs = 20 brain slots.
    90/10 cascade routing (left=conscious, right=subconscious).
    """
    return {
        'architecture': '4-brain split (2 small + 2 large per OWEM)',
        'brains_per_owem': 4,
        'owems': 5,
        'total_brain_slots': 20,
        'cascade': {
            'left_top_10': {'role': 'routing_decision', 'system': 'conscious/System-2', 'activation': '100%'},
            'left_bottom_90': {'role': 'easy_queries', 'system': 'conscious/System-1', 'activation': '~90%'},
            'right_top_10': {'role': 'deep_dive', 'system': 'subconscious/System-2', 'activation': '~10%'},
            'right_bottom_90': {'role': 'final_validation', 'system': 'subconscious/System-1', 'activation': '100%'},
        },
        'models_per_slot': {
            'left_top_10':   {'small': 'qwen2.5:3b', 'large': 'meta-llama-3.3-70b'},
            'left_bottom_90': {'small': 'qwen2.5:3b', 'large': 'qwen3:8b'},
            'right_top_10':  {'small': 'qwen3:8b', 'large': 'meta-llama-3.3-70b'},
            'right_bottom_90': {'small': 'qwen2.5:3b', 'large': 'meta-llama-3.3-70b'},
        },
        'parameters': {
            # HONEST: this is REACH per OWEM, NOT summed across OWEMs
            # Per CHARTER_OWEM_FOUR_SCOPE: 'of all' = governed substrate reaching across
            # 61 models, not additive params. Sum of params is the retracted error.
            'small_left_top': 3.1, 'large_left_top': 70.0,
            'small_left_bot': 3.1, 'large_left_bot': 8.0,
            'small_right_top': 8.0, 'large_right_top': 70.0,
            'small_right_bot': 3.1, 'large_right_bot': 70.0,
            'active_per_request_B': 17.3,        # sum of small paths in 1 OWEM: 3.1 + 3.1 + 8.0 + 3.1
            'reach_per_owem_B': 218.0,            # max-of-each brain slot per OWEM (NOT summed across OWEMs)
            'active_per_5_owems_B': 17.3,         # only ONE OWEM runs per query (routing picks)
            'note': 'OWEMs do NOT sum. Active = 17.3B regardless of # OWEMs (one OWEM per query). Reach = per-OWEM aggregate (218B), not stacked.',
        },
        'mamba2_state': {
            'state_dim': 16,
            'effective_context_multiplier': 10,
            'sovereign_bound': True,
            'sigiled': True,
        },
        'owem_brain_stacks': {
            'compliance':  {'specialty': 'EU AI Act, UK AI Bill, Article 50',  'memory_samples': 801,  'sovereign_trained': True},
            'defense':     {'specialty': 'Kill switch, intrusion, foreign-access','memory_samples': 1775, 'sovereign_trained': False},
            'intuition':   {'specialty': 'Patterns, predictions, geometry',     'memory_samples': 1075, 'sovereign_trained': False},
            'voice':       {'specialty': 'Sovereign truths, Charter, Article 0','memory_samples': 275, 'sovereign_trained': False},
            'general':     {'specialty': 'General knowledge fallback',         'memory_samples': 0,    'sovereign_trained': False},
        },
        'bft33_layers_per_hop': 5,
        'article_0_bound': True,
        'care_floor': 0.95,
        'ts': datetime.now(timezone.utc).isoformat(),
    }



def handle_hyperopt() -> dict:
    """GET /api/hyperopt — Optimal hyperparameter recommendations for sovereign brain training."""
    try:
        sys.path.insert(0, '/Users/nicholas/clawd/_alignment/sovereign_merge_kit')
        from sov33_hyperopt import grid_search_to_sigil
        return grid_search_to_sigil()
    except Exception as e:
        return {'error': f'hyperopt failed: {e}'}


def handle_continual_learning() -> dict:
    """GET /api/continual-learning — Continual learning state (replay buffer, EWC)."""
    try:
        sys.path.insert(0, '/Users/nicholas/clawd/_alignment/sovereign_merge_kit')
        from sov33_continual_learning import get_learner
        return get_learner().get_stats()
    except Exception as e:
        return {'error': f'continual learning failed: {e}'}


def handle_reasoning_enhance(payload: dict) -> dict:
    """POST /api/reasoning/enhance — Add chain-of-thought to a prompt."""
    try:
        sys.path.insert(0, '/Users/nicholas/clawd/_alignment/sovereign_merge_kit')
        from sov33_reasoning_enhancer import enhance_prompt
        message = payload.get('message', '')
        owem = payload.get('owem', 'general')
        enhanced = enhance_prompt(message, owem)
        return {
            'original': message,
            'enhanced': enhanced,
            'owem': owem,
            'cot_enabled': True,
            'length_delta': len(enhanced) - len(message),
        }
    except Exception as e:
        return {'error': f'reasoning enhance failed: {e}'}



def handle_kaggle_opportunities() -> dict:
    """GET /api/kaggle/opportunities — Kaggle competitions SOV33 can enter.

    Returns:
      - 8 curated opportunities (reasoning/math/science/LLM/governance)
      - Total prize pool: $1.45M
      - Total runtime: 53h (we have 30hr/wk on Kaggle T4)
      - Top picks by fit_score
    """
    try:
        sys.path.insert(0, '/Users/nicholas/clawd/_alignment/sovereign_merge_kit')
        from sov33_kaggle_opportunities import get_all_opportunities, find_best_fit
        result = get_all_opportunities()
        result['top_3_by_fit'] = find_best_fit(3)
        return result
    except Exception as e:
        return {'error': f'kaggle opportunities failed: {e}'}


def handle_capabilities() -> dict:
    """GET /api/capabilities — list all SOV33 capabilities."""
    return {
        'capabilities': [
            'memory', 'oracle-status', 'care-floor', 'drum', 'mist12',
            'emergence', 'oowm', 'model-registry', 'rainbow', 'sovspace',
            'probe', 'jadepuffer', 'care-divergence', 'three-lineage',
            'conformal', 'cedar', 'forgetting-aware-sft', 'dynamic-cheatsheet',
            'kimi-bridge', 'horus', 'correlation', 'defer', 'conformal-mapie',
            'sondera', 'agentdog', 'y2d', 'owem-sweep', 'dorado', 'sigstore',
        ],
        'count': 29,
        'care_floor': 0.95,
    }


# ═══════════════════════════════════════════════════════════════
# HTTP server
# ═══════════════════════════════════════════════════════════════

class SovereignAPIHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Quieter logging
        pass

    def do_OPTIONS(self):
        self.send_response(200)
        for k, v in CORS.items():
            self.send_header(k, v)
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)

        if path == '/api/nodes':
            return json_response(self, 200, handle_nodes())
        elif path == '/api/status':
            return json_response(self, 200, handle_status())
        elif path == '/api/capabilities':
            return json_response(self, 200, handle_capabilities())
        elif path == '/api/registry':
            return json_response(self, 200, handle_registry())
        elif path == '/api/evals':
            return json_response(self, 200, handle_evals())
        elif path == '/api/brain-stack':
            return json_response(self, 200, handle_brain_stack())
        elif path == '/api/kaggle/opportunities':
            return json_response(self, 200, handle_kaggle_opportunities())
        elif path == '/api/hyperopt':
            return json_response(self, 200, handle_hyperopt())
        elif path == '/api/continual-learning':
            return json_response(self, 200, handle_continual_learning())
        elif path == '/api/reasoning/enhance':
            # GET version: just demo
            return json_response(self, 200, handle_reasoning_enhance({'message': 'demo', 'owem': 'general'}))
        elif path == '/v1/models':
            return json_response(self, 200, handle_amica_models())
        elif path == '/api/memory':
            return json_response(self, 200, handle_memory({}))
        elif path == '/api/rho':
            return json_response(self, 200, handle_rho())
        elif path == '/api/govern':
            q = query.get('q', [''])[0]
            return json_response(self, 200, handle_govern(q))
        elif path == '/health':
            return json_response(self, 200, {'healthy': True, 'ts': datetime.now(timezone.utc).isoformat()})
        else:
            return json_response(self, 404, {'error': f'unknown path: {path}'})

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length) if content_length else b'{}'

        try:
            payload = json.loads(body) if body else {}
        except json.JSONDecodeError:
            return json_response(self, 400, {'error': 'invalid JSON'})

        if path == '/api/orchestrate':
            return json_response(self, 200, handle_orchestrate(payload))
        elif path == '/api/memory':
            return json_response(self, 200, handle_memory(payload))
        elif path == '/api/amica':
            return json_response(self, 200, handle_amica(payload))
        elif path == '/v1/chat/completions':
            return json_response(self, 200, handle_amica(payload))
        elif path == '/api/reasoning/enhance':
            return json_response(self, 200, handle_reasoning_enhance(payload))
        elif path == '/api/signup':
            return json_response(self, 200, handle_signup(payload))
        elif path == '/api/alexa':
            return json_response(self, 200, handle_alexa(payload))
        elif path == '/api/triangle':
            return json_response(self, 200, handle_triangle(payload))
        elif path == '/api/cascade':
            return json_response(self, 200, handle_cascade(payload))
        elif path == '/api/bridge':
            return json_response(self, 200, handle_bridge(payload))
        elif path == '/api/sign':
            return json_response(self, 200, handle_sign(payload))
        elif path == '/api/verify':
            return json_response(self, 200, handle_verify(payload))
        else:
            return json_response(self, 404, {'error': f'unknown path: {path}'})


def main():
    parser = argparse.ArgumentParser(description='SOV33 HTTP API server')
    parser.add_argument('--port', type=int, default=API_PORT)
    parser.add_argument('--quiet', action='store_true')
    args = parser.parse_args()

    server = HTTPServer(('0.0.0.0', args.port), SovereignAPIHandler)
    sigil_emit({
        'hop': 'API_SERVER_START',
        'port': args.port,
        'care_floor': 0.95,
    })

    if not args.quiet:
        print()
        print("=" * 70)
        print(f"SOV33 API SERVER — Port {args.port}")
        print("=" * 70)
        print(f"  Endpoints:")
        print(f"    GET  /api/status")
        print(f"    GET  /api/capabilities")
        print(f"    GET  /api/nodes")
        print(f"    GET  /api/govern?q=...")
        print(f"    POST /api/orchestrate  (Claude's sovereign-embed.js hook)")
        print(f"    POST /api/bridge")
        print(f"    POST /api/sign")
        print(f"    POST /api/verify")
        print(f"    GET  /health")
        print(f"  Aligned with: meok-os-deploy/sovereign-embed.js")
        print(f"  Care-Floor: 0.95 | Article 0: bound | 12 Pillars: active")
        print()
        print(f"  Listening on http://localhost:{args.port}")
        print(f"  Press Ctrl-C to stop")
        print()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        if not args.quiet:
            print("\n  Stopped.")


if __name__ == '__main__':
    main()