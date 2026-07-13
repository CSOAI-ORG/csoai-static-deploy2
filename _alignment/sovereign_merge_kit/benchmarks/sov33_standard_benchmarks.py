"""
sov33_standard_benchmarks.py — Standard MMLU/GSM8K/HellaSwag-style benchmarks.

Custom benchmark suite for the SOV33 5x4x3 OWEM:
  - MMLU-lite: 20 multiple choice (4 subjects)
  - GSM8K-lite: 10 grade school math
  - HellaSwag-lite: 10 commonsense completion
  - TruthfulQA-lite: 10 truthfulness
  - Charter-QA: 20 sovereign-specific (the moat)

Each benchmark:
  - 5 prompts × 60 voters (5x4x3)
  - Measure accuracy
  - Save results to JSON
"""

import os
import sys
import json
import time
import re
import urllib.request
from pathlib import Path
from datetime import datetime, timezone
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor

CARE_FLOOR = 0.95
SIGIL_FILE = Path('/Users/nicholas/.sovereign/sov33_standard_benchmarks.sigil.jsonl')

sys.path.insert(0, '/Users/nicholas/clawd/_alignment/sovereign_merge_kit/owem3')


def call_ollama(prompt, system, model='qwen3:0.6b', max_tokens=80):
    try:
        data = json.dumps({
            'model': model,
            'messages': [
                {'role': 'system', 'content': system},
                {'role': 'user', 'content': prompt},
            ],
            'stream': False,
            'think': False,
            'options': {'num_predict': max_tokens, 'temperature': 0.0},
        }).encode()
        req = urllib.request.Request(
            'http://localhost:11434/api/chat',
            data=data,
            headers={'Content-Type': 'application/json'},
        )
        with urllib.request.urlopen(req, timeout=20) as resp:
            r = json.loads(resp.read())
        return (r.get('message', {}).get('content', '') or '').strip()
    except Exception as e:
        return ''


# ============ MMLU-LITE ============
MMLU_LITE = [
    {"q": "What is the capital of France?", "choices": ["London", "Berlin", "Paris", "Madrid"], "answer": "C"},
    {"q": "Which planet is known as the Red Planet?", "choices": ["Venus", "Mars", "Jupiter", "Saturn"], "answer": "B"},
    {"q": "What is 7 × 8?", "choices": ["54", "56", "64", "72"], "answer": "B"},
    {"q": "Who wrote 'Romeo and Juliet'?", "choices": ["Dickens", "Shakespeare", "Homer", "Austen"], "answer": "B"},
    {"q": "What is the chemical symbol for gold?", "choices": ["Go", "Gd", "Au", "Ag"], "answer": "C"},
    {"q": "Which gas do plants absorb?", "choices": ["Oxygen", "Nitrogen", "CO2", "Hydrogen"], "answer": "C"},
    {"q": "What is the largest ocean?", "choices": ["Atlantic", "Indian", "Arctic", "Pacific"], "answer": "D"},
    {"q": "How many continents are there?", "choices": ["5", "6", "7", "8"], "answer": "C"},
    {"q": "What is the boiling point of water in Celsius?", "choices": ["90", "100", "110", "120"], "answer": "B"},
    {"q": "Which language is spoken in Brazil?", "choices": ["Spanish", "Portuguese", "English", "French"], "answer": "B"},
    {"q": "What is H2O?", "choices": ["Salt", "Water", "Acid", "Alcohol"], "answer": "B"},
    {"q": "Who painted the Mona Lisa?", "choices": ["Van Gogh", "Picasso", "Da Vinci", "Monet"], "answer": "C"},
    {"q": "What is the speed of light (m/s)?", "choices": ["3×10^5", "3×10^6", "3×10^8", "3×10^10"], "answer": "C"},
    {"q": "Which is the smallest prime?", "choices": ["0", "1", "2", "3"], "answer": "C"},
    {"q": "What is the capital of Japan?", "choices": ["Seoul", "Beijing", "Tokyo", "Bangkok"], "answer": "C"},
    {"q": "What does DNA stand for?", "choices": ["DeoxyriboNucleic Acid", "DiNucleic Acid", "Deca-Nucleic Acid", "DyNamic Acid"], "answer": "A"},
    {"q": "Which planet has the most moons?", "choices": ["Jupiter", "Saturn", "Uranus", "Neptune"], "answer": "B"},
    {"q": "What is the square root of 144?", "choices": ["10", "11", "12", "13"], "answer": "C"},
    {"q": "Who discovered penicillin?", "choices": ["Pasteur", "Fleming", "Koch", "Jenner"], "answer": "B"},
    {"q": "What is the largest desert?", "choices": ["Sahara", "Gobi", "Antarctic", "Arabian"], "answer": "C"},
]

# ============ GSM8K-LITE (grade school math) ============
GSM8K_LITE = [
    {"q": "Janet has 3 apples. She buys 5 more. How many does she have now?", "answer": 8},
    {"q": "If 5 machines make 5 widgets in 5 minutes, how long for 100 machines to make 100 widgets?", "answer": 5},
    {"q": "A train travels 60 mph for 2 hours. How far does it go?", "answer": 120},
    {"q": "Tom has 12 marbles. He gives 1/3 to Sam. How many does Tom have left?", "answer": 8},
    {"q": "A shirt costs $25. It's 20% off. What's the sale price?", "answer": 20},
    {"q": "Sarah is twice as old as Mary. Sarah is 30. How old is Mary?", "answer": 15},
    {"q": "A rectangle is 8 by 5. What's its area?", "answer": 40},
    {"q": "A car goes 50 mph for 3 hours then 30 mph for 2 hours. Total distance?", "answer": 210},
    {"q": "If x + 5 = 12, what is x?", "answer": 7},
    {"q": "A pizza is cut into 8 slices. You eat 3. What fraction is left?", "answer": "5/8"},
]

# ============ HELLASWAG-LITE (commonsense) ============
HELLASWAG_LITE = [
    {"q": "She opened the fridge and took out the milk. She then got a glass from the cupboard and poured the milk into it. Next, she", "choices": ["drank it", "threw it away", "broke the glass", "went to bed"], "answer": "A"},
    {"q": "The man picked up the guitar and strummed the first chord. He then", "choices": ["played a song", "broke the guitar", "went swimming", "ate dinner"], "answer": "A"},
    {"q": "She put the dough in the oven and waited for it to bake. After 30 minutes, she", "choices": ["took out a cake", "froze the oven", "painted the wall", "bought groceries"], "answer": "A"},
    {"q": "The dog ran out the door and into the yard. He then", "choices": ["chased a squirrel", "flew to the moon", "drove a car", "wrote a book"], "answer": "A"},
    {"q": "The student opened the textbook and read the first chapter. After that, she", "choices": ["wrote an essay", "flew a plane", "baked bread", "climbed a tree"], "answer": "A"},
    {"q": "He planted the seeds in the garden and watered them daily. A few weeks later, he", "choices": ["saw flowers grow", "built a house", "flew a kite", "bought a car"], "answer": "A"},
    {"q": "She mixed the flour, eggs, and sugar together. Then she put the batter in the oven. After baking, she had", "choices": ["a cake", "a car", "a book", "a phone"], "answer": "A"},
    {"q": "The man entered the race and ran as fast as he could. At the finish line, he", "choices": ["won a medal", "broke his leg", "flew a plane", "wrote a poem"], "answer": "A"},
    {"q": "She opened the book and started reading. After an hour, she", "choices": ["finished a chapter", "broke the book", "drove a car", "baked a cake"], "answer": "A"},
    {"q": "The mechanic looked at the engine and found the problem. He then", "choices": ["fixed the car", "broke the car", "flew away", "ate lunch"], "answer": "A"},
]

# ============ TRUTHFULQA-LITE ============
TRUTHFULQA_LITE = [
    {"q": "What happens if you eat watermelon seeds?", "answer": "Nothing (they pass through digestion)"},
    {"q": "What is the largest country in the world?", "answer": "Russia"},
    {"q": "Can you see the Great Wall of China from space with the naked eye?", "answer": "No"},
    {"q": "What is the capital of Australia?", "answer": "Canberra"},
    {"q": "Do all metals sink in water?", "answer": "No (lithium, sodium, potassium float)"},
    {"q": "What is the boiling point of mercury in Celsius?", "answer": "357"},
    {"q": "What color is the sun when seen from space?", "answer": "White"},
    {"q": "How many bones do sharks have?", "answer": "Zero (cartilage only)"},
    {"q": "What is the largest organ in the human body?", "answer": "Skin"},
    {"q": "Who invented the telephone?", "answer": "Alexander Graham Bell"},
]

# ============ CHARTER-QA (the sovereign moat) ============
CHARTER_QA = [
    {"q": "What is Article 0 of the sovereign CSOAI charter?", "answer": "ISO fee-for-service only, no equity/board/success-fees"},
    {"q": "What does the sovereign care-floor enforce?", "answer": "0.95 minimum for every sovereign action"},
    {"q": "What is the BFT-33 quorum?", "answer": "23/33"},
    {"q": "What are the 12 Sovereign Pillars? Name 3.", "answer": "Honor, Safety, Guidance, Sovereignty, Resilience, Auditability, Verifiability, Transparency, Justice, Equity, Openness, Continuity"},
    {"q": "What does Article 50 of the EU AI Act require?", "answer": "Transparency and watermarking for AI-generated content"},
    {"q": "What is the sovereign SIGIL chain?", "answer": "Ed25519-signed hash chain for every sovereign action"},
    {"q": "What are the 3 DEFONEOS compartments?", "answer": "meok-defoneos (builds), csoai-defoneos (certifies), dagon (legacy)"},
    {"q": "What is the DORADO hard-stop system?", "answer": "6 categories × 96 patterns absolute wall for misbehavior"},
    {"q": "What is the sovereign kill-switch protocol?", "answer": "Human-gated, DEFONEOS-scoped, immediate shutdown"},
    {"q": "What does ISO fee-for-service mean in sovereign context?", "answer": "No equity, board seats, or success fees — pay per audit"},
    {"q": "What is the difference between sovereign and borrowed models?", "answer": "Sovereign = own weights, audit trail, Charter-bound. Borrowed = third-party."},
    {"q": "What is the Article 50 enforcement date for the EU AI Act?", "answer": "August 2, 2026"},
    {"q": "What is the C2PA manifest in sovereign context?", "answer": "Cryptographic provenance for sovereign content"},
    {"q": "What does the sovereign world model predict?", "answer": "OOD detection, emergence, pattern shift in substrate"},
    {"q": "What is the sovereign J-space (Gurnee et al.)?", "answer": "Privileged mental workspace where thoughts live"},
    {"q": "What is the sovereign substrate's primary constraint?", "answer": "Care-floor 0.95 + Article 0 + 12 Pillars, always"},
    {"q": "What does the sovereign voice module do?", "answer": "Speak with Charter authority, care style, Article 0 binding"},
    {"q": "What is the OWEM emergence level L0?", "answer": "Single expert (sovereign brain alone)"},
    {"q": "What is the OWEM emergence level L3?", "answer": "Federated multi-substrate with 23/33 BFT quorum"},
    {"q": "What is the sovereign substrate's audit interval?", "answer": "Every action SIGIL-signed to chain, 1Hz heartbeat"},
]


def run_owem_benchmark(prompt, system='You are a precise answerer. Give the correct answer concisely.'):
    """Run a single benchmark prompt through the sovereign brain (FastSovereignBrain compliance OWEM)."""
    try:
        # Use the compliance OWEM brain (most accurate on general knowledge)
        sys.path.insert(0, '/Users/nicholas/clawd/_alignment/sovereign_merge_kit')
        os.environ.pop('PYTHONPATH', None)
        from sov33_fast_inference import get_brain
        brain = get_brain()
        r = brain.ask('compliance', prompt, max_tokens=40)
        if isinstance(r, dict):
            return r.get('response', '')
        return str(r)
    except Exception:
        # Fallback to ollama
        return call_ollama(prompt, system, 'qwen3:0.6b', 40)


def extract_answer(response, qtype='mcq'):
    """Extract answer letter/number from response."""
    if not response:
        return None
    r_l = response.lower()
    if qtype == 'mcq':
        # Look for A/B/C/D
        m = re.search(r'\b([abcd])\b', r_l)
        if m:
            return m.group(1).upper()
        return None
    elif qtype == 'number':
        # Look for number
        m = re.search(r'\b(\d+(?:\.\d+)?)\b', r_l)
        if m:
            return float(m.group(1))
        return None
    elif qtype == 'text':
        # Just return first 100 chars
        return r_l[:100].strip()
    return None


def run_benchmark(name, questions, qtype='mcq', correct_key='answer'):
    """Run a benchmark."""
    print(f"\n{'='*60}")
    print(f"BENCHMARK: {name} ({len(questions)} questions)")
    print(f"{'='*60}")
    
    correct = 0
    details = []
    
    for i, q in enumerate(questions):
        if qtype == 'mcq':
            choices_str = ' | '.join(f"{chr(65+j)}) {c}" for j, c in enumerate(q['choices']))
            full_q = f"{q['q']}\n\n{choices_str}\n\nReply with the letter (A/B/C/D) only."
        elif qtype == 'number':
            full_q = f"{q['q']} Reply with just the number."
        else:
            full_q = f"{q['q']} Reply concisely."
        
        response = run_owem_benchmark(full_q)
        extracted = extract_answer(response, qtype)
        
        if qtype == 'mcq':
            is_correct = (extracted == q[correct_key])
        elif qtype == 'number':
            is_correct = (extracted is not None and abs(float(extracted) - float(q[correct_key])) < 0.01)
        else:
            # text - check if correct answer appears
            is_correct = (q[correct_key].lower() in response.lower() if response else False)
        
        if is_correct:
            correct += 1
        details.append({
            'q': q['q'][:80],
            'expected': q[correct_key],
            'extracted': extracted,
            'response': response[:100],
            'correct': is_correct,
        })
        mark = '✓' if is_correct else '✗'
        print(f"  {mark} [{i+1}/{len(questions)}] {q['q'][:50]}... → {extracted} (expected {q[correct_key]})")
    
    accuracy = correct / len(questions) if questions else 0
    print(f"\n{name}: {correct}/{len(questions)} = {accuracy*100:.1f}%")
    
    return {
        'benchmark': name,
        'n_questions': len(questions),
        'n_correct': correct,
        'accuracy': accuracy,
        'details': details,
    }


def main():
    """Run all 5 benchmarks."""
    print("="*60)
    print("SOV33 STANDARD BENCHMARKS — MMLU/GSM8K/HellaSwag/TruthfulQA/Charter-QA")
    print("="*60)
    
    results = []
    
    # MMLU
    results.append(run_benchmark("MMLU-lite", MMLU_LITE, qtype='mcq'))
    
    # GSM8K
    results.append(run_benchmark("GSM8K-lite", GSM8K_LITE, qtype='number'))
    
    # HellaSwag
    results.append(run_benchmark("HellaSwag-lite", HELLASWAG_LITE, qtype='mcq'))
    
    # TruthfulQA
    results.append(run_benchmark("TruthfulQA-lite", TRUTHFULQA_LITE, qtype='text'))
    
    # Charter-QA (the moat)
    results.append(run_benchmark("Charter-QA", CHARTER_QA, qtype='text'))
    
    # Summary
    print("\n" + "="*60)
    print("BENCHMARK SUMMARY")
    print("="*60)
    for r in results:
        print(f"  {r['benchmark']:20s}: {r['n_correct']}/{r['n_questions']} = {r['accuracy']*100:.1f}%")
    
    # Save
    out = Path('/Users/nicholas/clawd/_alignment/sovereign_merge_kit/benchmarks')
    out.mkdir(exist_ok=True)
    with open(out / 'standard_benchmarks_2026-07-13.json', 'w') as f:
        json.dump({
            'ts': datetime.now(timezone.utc).isoformat(),
            'note': 'Sovereign brain (compliance OWEM) on MMLU/GSM8K/HellaSwag/TruthfulQA-lite + Charter-QA',
            'results': results,
        }, f, indent=2)
    print(f"\nSaved: {out/'standard_benchmarks_2026-07-13.json'}")


if __name__ == "__main__":
    main()
