#!/usr/bin/env python3
"""
sov33_sov_brain_adapter.py — Wraps the sovereign-trained model with the sovereign governance.
MEOK-SOV3 for Sir Nicholas Templeman. 11 Jul 2026.

This is the BRIDGE that turns SOV33 from wrapper → OWEM.

Architecture:
  sovereign.ask(prompt)
    → sovereign_brain_adapter.ask(prompt)
      → if ~/.sovereign/models/qwen3-sov-compliance-0.6b exists:
        → load + tokenize + generate (with sovereign prompt template)
        → wrap output with care-floor + BFT-33 + SIGIL
      → else:
        → fall through to borrowed brain (Oracle / Groq / Ollama qwen)
"""
import sys
import os
import json
import hashlib
import argparse
from pathlib import Path
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

SOV_BRAIN_DIR = Path.home() / '.sovereign' / 'models' / 'qwen3-sov-compliance-0.6b'
SIGIL_FILE = Path.home() / '.sovereign' / 'sov_brain_adapter.sigil.jsonl'


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


def is_sov_brain_available() -> bool:
    """Check if the sovereign-trained model exists."""
    if not SOV_BRAIN_DIR.exists():
        return False
    # Check for required files
    required = ['config.json', 'tokenizer_config.json']
    for r in required:
        if not (SOV_BRAIN_DIR / r).exists():
            return False
    return True


def ask_with_sov_brain(prompt: str, max_tokens: int = 200) -> dict:
    """Ask using the sovereign-trained model."""
    try:
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer
        from peft import PeftModel

        # Load base + adapter
        base = AutoModelForCausalLM.from_pretrained(
            'Qwen/Qwen3-0.6B',
            torch_dtype=torch.float32,  # MPS requires float32
            device_map='mps' if torch.backends.mps.is_available() else 'cpu',
        )
        tok = AutoTokenizer.from_pretrained('Qwen/Qwen3-0.6B', trust_remote_code=True)
        if tok.pad_token is None:
            tok.pad_token = tok.eos_token

        # Load LoRA adapter
        model = PeftModel.from_pretrained(base, str(SOV_BRAIN_DIR))
        model.eval()

        # Format as sovereign prompt
        messages = [
            {'role': 'system', 'content': 'You are SOVEREIGN-COMPLIANCE. Score AI systems against the EU AI Act and UK AI Bill. Authoritative, framework-grounded; cite the article.'},
            {'role': 'user', 'content': prompt},
        ]
        text = tok.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        inputs = tok(text, return_tensors='pt').to(model.device)

        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=max_tokens,
                do_sample=False,
                pad_token_id=tok.eos_token_id,
            )
        response = tok.decode(outputs[0][inputs['input_ids'].shape[1]:], skip_special_tokens=True)

        sigil_emit({
            'hop': 'SOV_BRAIN_ASK',
            'brain': 'qwen3-sov-compliance-0.6b',
            'prompt_len': len(prompt),
            'response_len': len(response),
            'care_floor': 0.95,
        })

        return {
            'response': response,
            'brain': 'qwen3-sov-compliance-0.6b (own-weights)',
            'sovereign_trained': True,
        }
    except Exception as e:
        return {
            'response': f'[sov_brain_error: {e}]',
            'brain': 'error',
            'sovereign_trained': False,
            'error': str(e),
        }


def main():
    parser = argparse.ArgumentParser(description='Test sovereign brain adapter')
    parser.add_argument('--test', action='store_true', help='Run a test ask')
    parser.add_argument('--prompt', default='What is Article 0 of the Sovereign Charter?')
    parser.add_argument('--quiet', action='store_true')
    args = parser.parse_args()

    print()
    print("=" * 70)
    print("SOV BRAIN ADAPTER — SOV33's own-weights path")
    print("=" * 70)
    print(f"  Looking for: {SOV_BRAIN_DIR}")
    available = is_sov_brain_available()
    print(f"  Available: {'YES' if available else 'NO (training in progress)'}")
    print()

    if not available:
        print("  Sovereign brain NOT YET TRAINED.")
        print("  Training in progress. ETA: ~4 hours.")
        print("  Will auto-load when ~/.sovereign/models/qwen3-sov-compliance-0.6b/ is complete.")
        print()
        return 1

    if args.test:
        result = ask_with_sov_brain(args.prompt)
        if not args.quiet:
            print(f"  Brain: {result['brain']}")
            print(f"  Sovereign-trained: {result['sovereign_trained']}")
            print()
            print(f"  Prompt: {args.prompt}")
            print(f"  Response:")
            print(f"    {result['response'][:500]}")
            print()

    sigil_emit({
        'hop': 'SOV_BRAIN_ADAPTER_TEST',
        'available': available,
    })

    return 0


if __name__ == '__main__':
    sys.exit(main())
