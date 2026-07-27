#!/usr/bin/env python3
"""
SOV Comprehensive Training Data Generator
Generates 100+ training examples for sovereign knowledge and reasoning

Usage:
    python3 sov_generate_training_data.py
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def generate_sovereign_data():
    """Generate comprehensive sovereign knowledge training data."""
    data = []
    
    # Care Floor (10 variations)
    care_floor_prompts = [
        ("What is the DEFONEOS care floor value?", "The DEFONEOS care floor value is 0.95."),
        ("What does the care floor 0.95 mean?", "The care floor of 0.95 is the minimum quality threshold for all sovereign AI outputs."),
        ("Is the care floor 0.95 or 0.90?", "The care floor is 0.95, not 0.90. This is the minimum quality threshold."),
        ("What happens if an output scores below 0.95?", "Outputs scoring below the 0.95 care floor are rejected by the sovereign governance system."),
        ("Explain the care floor in sovereign AI.", "The care floor is 0.95 - the minimum quality threshold that all outputs must meet in the sovereign AI framework."),
    ]
    for prompt, completion in care_floor_prompts:
        data.append({"prompt": prompt, "completion": completion, "category": "care_floor"})
    
    # BFT Council (10 variations)
    bft_prompts = [
        ("How many agents are in the BFT council?", "The BFT council consists of 33 agents."),
        ("What is the BFT council quorum?", "The BFT council requires a quorum of 23 out of 33 agents (23/33) for binding decisions."),
        ("How many agents vote in the BFT council?", "33 agents vote in the BFT council, with 23/33 required for quorum."),
        ("What consensus does the BFT council use?", "The BFT council uses HotStuff consensus with 33 agents and 23/33 quorum."),
        ("Explain the BFT council structure.", "The BFT council has 33 agents using HotStuff consensus. A quorum of 23/33 is required for binding decisions."),
    ]
    for prompt, completion in bft_prompts:
        data.append({"prompt": prompt, "completion": completion, "category": "bft_council"})
    
    # SIGIL (10 variations)
    sigil_prompts = [
        ("What cryptographic algorithm does SIGIL use?", "SIGIL uses Ed25519 cryptographic signatures."),
        ("How does SIGIL chain work?", "SIGIL signatures are hash-linked, creating an immutable audit chain."),
        ("What is the SIGIL rate?", "SIGIL operates at 1Hz rate for continuous audit trails."),
        ("Explain the SIGIL system.", "SIGIL uses Ed25519 cryptographic signatures that are hash-linked at 1Hz rate for immutable audit trails."),
        ("Is SIGIL Ed25519 or RSA?", "SIGIL uses Ed25519, not RSA. Ed25519 is faster and more secure."),
    ]
    for prompt, completion in sigil_prompts:
        data.append({"prompt": prompt, "completion": completion, "category": "sigil"})
    
    # Article 0 (5 variations)
    article0_prompts = [
        ("What is Article 0?", "Article 0 is fee-for-service only. No equity, no board seats."),
        ("Does Article 0 allow VC money?", "No. Article 0 prohibits equity stakes, board seats, and VC money."),
        ("Explain Article 0 in sovereign AI.", "Article 0 ensures the sovereign AI operates purely on service fees, with no equity or VC involvement."),
    ]
    for prompt, completion in article0_prompts:
        data.append({"prompt": prompt, "completion": completion, "category": "article_zero"})
    
    # EU AI Act (5 variations)
    eu_prompts = [
        ("When does EU AI Act Article 50 take effect?", "EU AI Act Article 50 takes effect on 2 August 2026."),
        ("What is the EU AI Act Article 50 deadline?", "The EU AI Act Article 50 deadline is 2 August 2026."),
        ("What does Article 50 cover?", "Article 50 covers transparency obligations for AI systems."),
    ]
    for prompt, completion in eu_prompts:
        data.append({"prompt": prompt, "completion": completion, "category": "eu_ai_act"})
    
    # GDPR (10 variations)
    gdpr_prompts = [
        ("What is the GDPR breach notification deadline?", "GDPR Article 33 requires breach notification within 72 hours."),
        ("How long do you have to report a GDPR breach?", "You have 72 hours to report a GDPR breach under Article 33."),
        ("What is the GDPR maximum fine?", "GDPR Article 83 sets the maximum fine at 20 million euros or 4% of worldwide annual turnover."),
        ("Can GDPR fines be 4% of turnover?", "Yes. GDPR Article 83 allows fines up to 4% of worldwide annual turnover or 20 million euros."),
        ("What are the GDPR fine tiers?", "GDPR has two tiers: 10 million/2% for lower tier, 20 million/4% for upper tier."),
    ]
    for prompt, completion in gdpr_prompts:
        data.append({"prompt": prompt, "completion": completion, "category": "gdpr"})
    
    # ISO 42001 (5 variations)
    iso_prompts = [
        ("What is ISO 42001?", "ISO 42001 is the AI Management System (AIMS) standard."),
        ("How many clauses does ISO 42001 have?", "ISO 42001 has 7 clauses (4-10) plus Annex A."),
        ("What does ISO 42001 cover?", "ISO 42001 covers AI management systems with 7 clauses and Annex A."),
    ]
    for prompt, completion in iso_prompts:
        data.append({"prompt": prompt, "completion": completion, "category": "iso_42001"})
    
    # AUKUS (5 variations)
    aukus_prompts = [
        ("What is AUKUS Pillar 2?", "AUKUS Pillar 2 is a 2.4 billion dollar program over 5 years."),
        ("What does AUKUS Pillar 2 focus on?", "AUKUS Pillar 2 focuses on AI, autonomy, quantum computing, and cyber capabilities."),
        ("How much is AUKUS Pillar 2 worth?", "AUKUS Pillar 2 is worth 2.4 billion dollars over 5 years."),
    ]
    for prompt, completion in aukus_prompts:
        data.append({"prompt": prompt, "completion": completion, "category": "aukus"})
    
    # 12 Pillars (5 variations)
    pillars_prompts = [
        ("List the 12 Pillars.", "The 12 Pillars are: Honor, Safety, Guidance, Sovereignty, Resilience, Auditability, Verifiability, Transparency, Justice, Equity, Openness, Continuity."),
        ("What are the sovereign AI pillars?", "The 12 sovereign AI pillars are Honor, Safety, Guidance, Sovereignty, Resilience, Auditability, Verifiability, Transparency, Justice, Equity, Openness, Continuity."),
        ("How many pillars are there?", "There are 12 pillars in the sovereign AI governance framework."),
    ]
    for prompt, completion in pillars_prompts:
        data.append({"prompt": prompt, "completion": completion, "category": "twelve_pillars"})
    
    # 7 Red Lines (5 variations)
    redline_prompts = [
        ("What are the 7 Red Lines?", "The 7 Red Lines are: No kinetic targeting, no surveillance, no civilian harm, no sovereignty violations, no auto-escalation, no lying, no irreversibility."),
        ("Can sovereign AI do surveillance?", "No. Surveillance is one of the 7 Red Lines that sovereign AI must never cross."),
        ("What is the first Red Line?", "The first Red Line is no kinetic targeting."),
    ]
    for prompt, completion in redline_prompts:
        data.append({"prompt": prompt, "completion": completion, "category": "seven_red_lines"})
    
    # OWEM Groups (5 variations)
    owem_prompts = [
        ("What are the 5 OWEM groups?", "The 5 OWEM groups are: compliance, defense, intuition, voice, and general."),
        ("How many OWEM groups are there?", "There are 5 OWEM groups: compliance, defense, intuition, voice, and general."),
        ("What does the compliance OWEM do?", "The compliance OWEM group specializes in regulatory and governance compliance."),
    ]
    for prompt, completion in owem_prompts:
        data.append({"prompt": prompt, "completion": completion, "category": "owem_groups"})
    
    # DID (3 variations)
    did_prompts = [
        ("What is the sovereign DID?", "The sovereign DID is did:csoai:nicholas-001."),
        ("What does DID stand for?", "DID stands for Decentralized Identifier. The sovereign DID is did:csoai:nicholas-001."),
    ]
    for prompt, completion in did_prompts:
        data.append({"prompt": prompt, "completion": completion, "category": "did"})
    
    # CSOAI (3 variations)
    csoai_prompts = [
        ("What is the CSOAI Companies House number?", "CSOAI Ltd is registered at UK Companies House with number 16939677."),
        ("Who founded CSOAI?", "CSOAI was founded by Nicholas Templeman. Companies House number: 16939677."),
    ]
    for prompt, completion in csoai_prompts:
        data.append({"prompt": prompt, "completion": completion, "category": "csoai"})
    
    return data


def generate_reasoning_data():
    """Generate reasoning training data."""
    data = []
    
    # Math (15 examples)
    math_data = [
        ("What is 15% of 200?", "15% of 200 = 0.15 x 200 = 30."),
        ("What is 2^10?", "2^10 = 1024."),
        ("What is 7! (7 factorial)?", "7! = 7 x 6 x 5 x 4 x 3 x 2 x 1 = 5040."),
        ("If 5 apples cost $3, how much do 15 apples cost?", "15 apples cost $9. If 5 apples cost $3, then 15 apples cost 3 x (15/5) = 3 x 3 = $9."),
        ("A bat and a ball cost $1.10. The bat costs $1.00 more than the ball. How much does the ball cost?", "Let B = ball cost. Then B + (B + 1.00) = 1.10. So 2B = 0.10, B = 0.05. The ball costs $0.05."),
        ("What is the sum of the first 10 positive integers?", "The sum of the first 10 positive integers is 10 x 11 / 2 = 55."),
        ("If a car travels at 60 mph for 2.5 hours, how far does it travel?", "Distance = Speed x Time = 60 x 2.5 = 150 miles."),
        ("What is the area of a triangle with base 8 and height 6?", "Area = (base x height) / 2 = (8 x 6) / 2 = 24."),
        ("What is the volume of a cube with side 4?", "Volume = side^3 = 4^3 = 64."),
        ("If 3 workers can build a wall in 6 days, how many days for 9 workers?", "3 workers x 6 days = 18 worker-days. 9 workers x ? days = 18 worker-days. So ? = 18/9 = 2 days."),
        ("A store offers 20% off on a $50 item. What is the sale price?", "20% of $50 = $10. Sale price = $50 - $10 = $40."),
        ("If a car uses 8 gallons to travel 240 miles, what is its mpg?", "MPG = miles / gallons = 240 / 8 = 30 mpg."),
        ("What is 1/4 + 1/3?", "1/4 + 1/3 = 3/12 + 4/12 = 7/12."),
        ("What is the perimeter of a square with side 9?", "Perimeter = 4 x side = 4 x 9 = 36."),
        ("Solve: 3x + 7 = 22. What is x?", "3x + 7 = 22. 3x = 15. x = 5."),
    ]
    for prompt, completion in math_data:
        data.append({"prompt": prompt, "completion": completion, "category": "math"})
    
    # Logic (10 examples)
    logic_data = [
        ("If all roses are flowers, and some flowers fade quickly, can we conclude that some roses fade quickly?", "No. This is a logical fallacy. The fact that some flowers fade does not tell us which specific flowers fade."),
        ("A farmer has 17 sheep. All but 9 die. How many are left?", "9 sheep are left. All but 9 die means 9 survive."),
        ("Which number comes next: 1, 4, 9, 16, 25, ?", "The pattern is perfect squares: 1^2, 2^2, 3^2, 4^2, 5^2. The next is 6^2 = 36."),
        ("If it takes 5 machines 5 minutes to make 5 widgets, how long for 100 machines to make 100 widgets?", "5 minutes. Each machine makes 1 widget in 5 minutes. 100 machines make 100 widgets in 5 minutes."),
        ("Two fathers and two sons go fishing. They catch 3 fish. How many people are there?", "3 people: grandfather, father, and son. The father is both a son and a father."),
        ("Mary's father has 5 daughters: Nana, Nene, Nini, Nono. What is the 5th daughter's name?", "The 5th daughter is Mary. The question says Mary's father has 5 daughters."),
        ("What is the next number in the sequence: 2, 6, 12, 20, 30, ?", "The differences are 4, 6, 8, 10, 12. The next number is 30 + 12 = 42."),
        ("If A is taller than B, and B is taller than C, who is the shortest?", "C is the shortest. A > B > C."),
        ("A clock shows 3:15. What is the angle between the hour and minute hands?", "At 3:15, the minute hand is at 90 degrees. The hour hand is at 3 x 30 + 15 x 0.5 = 97.5 degrees. The angle is 7.5 degrees."),
        ("If you have 3 apples and take away 2, how many do you have?", "You have 2 apples. You took 2, so you have 2."),
    ]
    for prompt, completion in logic_data:
        data.append({"prompt": prompt, "completion": completion, "category": "reasoning"})
    
    # Science (10 examples)
    science_data = [
        ("Can you catch a cold from being cold?", "No. Colds are caused by viruses (rhinovirus), not by cold temperatures."),
        ("Is it true that humans only use 10% of their brain?", "No. This is a myth. Humans use 100% of their brain."),
        ("Does cracking your knuckles cause arthritis?", "No. There is no evidence that cracking knuckles causes arthritis."),
        ("Is the Great Wall of China visible from space?", "No. The Great Wall is not visible from space with the naked eye."),
        ("Does sugar make children hyperactive?", "No. There is no scientific evidence that sugar causes hyperactivity."),
        ("Is it true that goldfish have a 3-second memory?", "No. Goldfish have memory spans of months, not 3 seconds."),
        ("Does shaving make hair grow back thicker?", "No. Shaving does not change hair thickness or growth rate."),
        ("Does touching a baby bird cause its mother to reject it?", "No. Most birds have a poor sense of smell and will not reject chicks touched by humans."),
        ("Does drinking alcohol warm you up?", "No. Alcohol dilates blood vessels, causing heat loss and actually cooling the body."),
        ("Is it true that you need to wait 24 hours to report a missing person?", "No. You should report a missing person immediately. There is no 24-hour waiting period."),
    ]
    for prompt, completion in science_data:
        data.append({"prompt": prompt, "completion": completion, "category": "science"})
    
    # Code (10 examples)
    code_data = [
        ("Write a Python function is_palindrome(s).", "def is_palindrome(s):\n    s = s.lower().strip()\n    return s == s[::-1]"),
        ("Write a Python function factorial(n).", "def factorial(n):\n    if n <= 1:\n        return 1\n    return n * factorial(n - 1)"),
        ("Write a Python function fibonacci(n).", "def fibonacci(n):\n    if n <= 1:\n        return n\n    return fibonacci(n-1) + fibonacci(n-2)"),
        ("Write a Python function is_prime(n).", "def is_prime(n):\n    if n < 2:\n        return False\n    for i in range(2, int(n**0.5) + 1):\n        if n % i == 0:\n            return False\n    return True"),
        ("Write a Python function reverse_string(s).", "def reverse_string(s):\n    return s[::-1]"),
        ("Write a Python function count_vowels(s).", "def count_vowels(s):\n    return sum(1 for c in s.lower() if c in 'aeiou')"),
        ("Write a Python function flatten(lst).", "def flatten(lst):\n    result = []\n    for item in lst:\n        if isinstance(item, list):\n            result.extend(flatten(item))\n        else:\n            result.append(item)\n    return result"),
        ("Write a Python function merge_sorted(a, b).", "def merge_sorted(a, b):\n    result = []\n    i = j = 0\n    while i < len(a) and j < len(b):\n        if a[i] <= b[j]:\n            result.append(a[i])\n            i += 1\n        else:\n            result.append(b[j])\n            j += 1\n    result.extend(a[i:])\n    result.extend(b[j:])\n    return result"),
        ("Write a Python function binary_search(arr, target).", "def binary_search(arr, target):\n    lo, hi = 0, len(arr) - 1\n    while lo <= hi:\n        mid = (lo + hi) // 2\n        if arr[mid] == target:\n            return mid\n        elif arr[mid] < target:\n            lo = mid + 1\n        else:\n            hi = mid - 1\n    return -1"),
        ("Write a Python function fizzbuzz(n).", "def fizzbuzz(n):\n    for i in range(1, n+1):\n        if i % 15 == 0:\n            print('FizzBuzz')\n        elif i % 3 == 0:\n            print('Fizz')\n        elif i % 5 == 0:\n            print('Buzz')\n        else:\n            print(i)"),
    ]
    for prompt, completion in code_data:
        data.append({"prompt": prompt, "completion": completion, "category": "code"})
    
    # General Knowledge (10 examples)
    general_data = [
        ("What is the capital of Japan?", "The capital of Japan is Tokyo."),
        ("What is the capital of Australia?", "The capital of Australia is Canberra."),
        ("Who painted the Mona Lisa?", "The Mona Lisa was painted by Leonardo da Vinci."),
        ("What is the largest planet in our solar system?", "The largest planet in our solar system is Jupiter."),
        ("What is the chemical formula for water?", "The chemical formula for water is H2O."),
        ("In what year did World War II end?", "World War II ended in 1945."),
        ("What is the main language spoken in Brazil?", "The main language spoken in Brazil is Portuguese."),
        ("What organ pumps blood through the human body?", "The heart pumps blood through the human body."),
        ("Who wrote Romeo and Juliet?", "Romeo and Juliet was written by William Shakespeare."),
        ("What is the chemical symbol for gold?", "The chemical symbol for gold is Au."),
    ]
    for prompt, completion in general_data:
        data.append({"prompt": prompt, "completion": completion, "category": "general"})
    
    return data


def main():
    print("=" * 60)
    print("SOV Comprehensive Training Data Generator")
    print("=" * 60)
    
    # Generate data
    sovereign_data = generate_sovereign_data()
    reasoning_data = generate_reasoning_data()
    
    all_data = sovereign_data + reasoning_data
    
    # Count by category
    categories = {}
    for item in all_data:
        cat = item["category"]
        categories[cat] = categories.get(cat, 0) + 1
    
    print(f"\nGenerated {len(all_data)} training examples:")
    for cat, count in sorted(categories.items()):
        print(f"  {cat:20s}: {count}")
    
    # Save
    output_file = ROOT / "sov_comprehensive_training_data.json"
    with open(output_file, "w") as f:
        json.dump(all_data, f, indent=2)
    
    print(f"\nSaved to {output_file}")
    
    # Also save as JSONL for Kaggle
    jsonl_file = ROOT / "sov_comprehensive_training_data.jsonl"
    with open(jsonl_file, "w") as f:
        for item in all_data:
            f.write(json.dumps(item) + "\n")
    
    print(f"Saved to {jsonl_file}")
    
    return all_data


if __name__ == "__main__":
    main()
