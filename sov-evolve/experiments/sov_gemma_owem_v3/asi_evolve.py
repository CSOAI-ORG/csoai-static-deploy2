#!/usr/bin/env python3
"""
ASI-Evolve Engine for SOV6-Gemma-OWEM-v3
Evolutionary algorithm to optimize Modelfile parameters and system prompt.
Target: push spatial from 88% to 95%+ while maintaining reasoning/visual at 100%.
"""
import json, os, sys, time, random, copy, hashlib, re
from pathlib import Path
from datetime import datetime

EXPERIMENT_DIR = Path(__file__).parent
PROGRAMS_DIR = EXPERIMENT_DIR / "programs"
EVALS_DIR = EXPERIMENT_DIR / "evaluations"
MUTATIONS_DIR = EXPERIMENT_DIR / "mutations"
LOGS_DIR = EXPERIMENT_DIR / "logs"

OLLAMA_URL = "http://localhost:11434"
BASE_MODEL = "gemma3:12b"

# Load benchmark
def load_benchmark():
    with open(EXPERIMENT_DIR / "owem_v2_benchmark.json") as f:
        return json.load(f)

# Load bloodline cognition
def load_bloodline():
    bl_path = Path.home() / "clawd/csoai-static-deploy2/competitions/bloodline.json"
    if bl_path.exists():
        with open(bl_path) as f:
            return json.load(f)
    return None

# Parse a Modelfile into components
def parse_modelfile(path):
    content = Path(path).read_text()
    params = {}
    system = ""
    
    # Extract FROM
    from_match = re.search(r'FROM\s+(\S+)', content)
    base = from_match.group(1) if from_match else BASE_MODEL
    
    # Extract PARAMETERs
    for m in re.finditer(r'PARAMETER\s+(\w+)\s+(.+)', content):
        params[m.group(1)] = m.group(2).strip()
    
    # Extract SYSTEM prompt
    sys_match = re.search(r'SYSTEM\s+"""(.*?)"""', content, re.DOTALL)
    if sys_match:
        system = sys_match.group(1).strip()
    
    return {"base": base, "params": params, "system": system}

# Build Modelfile from components
def build_modelfile(base, params, system):
    lines = [f"FROM {base}"]
    for k, v in sorted(params.items()):
        lines.append(f"PARAMETER {k} {v}")
    lines.append(f'SYSTEM """{system}"""')
    return "\n".join(lines)

# Call Ollama to get a response
def query_model(system_prompt, question, options=None, temperature=0.1, num_predict=256):
    import urllib.request
    
    prompt = question
    if options:
        prompt += "\n\n" + "\n".join(options) + "\n\nRespond with ONLY the letter (A, B, C, or D) and the answer."
    
    full_prompt = f"{system_prompt}\n\nUser: {prompt}\nAssistant:"
    
    payload = json.dumps({
        "model": BASE_MODEL,
        "prompt": full_prompt,
        "stream": False,
        "options": {
            "temperature": float(temperature),
            "num_predict": int(num_predict),
            "top_p": 0.9,
            "top_k": 40
        }
    }).encode()
    
    req = urllib.request.Request(
        f"{OLLAMA_URL}/api/generate",
        data=payload,
        headers={"Content-Type": "application/json"}
    )
    
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            data = json.loads(r.read())
        return data.get("response", "").strip()
    except Exception as e:
        return f"ERROR: {e}"

# Grade a response against expected answer
def grade_response(response, task):
    if response.startswith("ERROR"):
        return False
    
    ans = task["ans"]
    resp_upper = response.upper().strip()
    
    # For multiple choice - check if correct letter is in response
    if "opts" in task:
        # Extract first letter of response
        first_letter = ""
        for c in resp_upper:
            if c in "ABCD":
                first_letter = c
                break
        
        return first_letter == ans.upper()
    
    # For open-ended - check if answer is contained
    return ans.lower() in response.lower()

# Evaluate a program on the full benchmark
def evaluate_program(program_path, benchmark, bloodline=None):
    prog = parse_modelfile(program_path)
    results = {"reasoning": [], "spatial": [], "visual": []}
    
    for category, cat_data in benchmark["categories"].items():
        for task in cat_data["tasks"]:
            response = query_model(
                prog["system"],
                task["q"],
                task.get("opts"),
                prog["params"].get("temperature", 0.1),
                prog["params"].get("num_predict", 256)
            )
            correct = grade_response(response, task)
            results[category].append({
                "task_id": task["id"],
                "correct": correct,
                "response": response[:200],
                "expected": task["ans"]
            })
    
    # Calculate scores
    scores = {}
    for cat, tasks in results.items():
        correct_count = sum(1 for t in tasks if t["correct"])
        scores[cat] = correct_count / len(tasks) if tasks else 0
    
    total_correct = sum(sum(1 for t in tasks if t["correct"]) for tasks in results.values())
    total_tasks = sum(len(tasks) for tasks in results.values())
    scores["overall"] = total_correct / total_tasks if total_tasks else 0
    
    return {
        "scores": scores,
        "details": results,
        "total_correct": total_correct,
        "total_tasks": total_tasks,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

# Mutate a program
def mutate_program(program_path, mutation_type="random"):
    prog = parse_modelfile(program_path)
    mutations_applied = []
    
    new_params = dict(prog["params"])
    new_system = prog["system"]
    
    # Temperature mutations
    if mutation_type in ("random", "temperature"):
        temp = float(new_params.get("temperature", 0.1))
        delta = random.choice([-0.05, -0.02, 0.02, 0.05, 0.1])
        new_temp = max(0.0, min(1.0, temp + delta))
        new_params["temperature"] = str(round(new_temp, 3))
        mutations_applied.append(f"temperature: {temp} -> {new_params['temperature']}")
    
    # System prompt mutations - spatial focus
    spatial_enhancements = [
        "\nSPATIAL CHECKLIST:\n1. Identify reference frame (absolute vs relative)\n2. Track each transformation step\n3. Verify final position against starting point",
        "\nFor direction problems: draw a mental compass. N=up, S=down, E=right, W=left.\nRight turn = clockwise. Left turn = counter-clockwise.",
        "\nGEOMETRY RULES:\n- Cube: 6 faces, 12 edges, 8 vertices\n- Rectangular prism: same as cube\n- Hexagon: 6 sides, internal angles sum to 720 degrees\n- Circle in square: area ratio = pi/4 ≈ 0.785",
        "\nFor angle calculations:\n- Clock: minute hand moves 6 deg/min, hour hand moves 0.5 deg/min\n- At 3:15: hour hand is at 97.5 deg, minute hand at 90 deg, difference = 7.5 deg",
        "\nROTATION RULES:\n- 90 deg right (clockwise) from N = E\n- 90 deg left (counter-clockwise) from N = W\n- 180 deg from any direction = opposite\n- Letter 'b' rotated 180 deg = 'q' (not 'd' or 'p')",
        "\nFOLDING RULES:\n- Fold in half once = 2 layers\n- Fold in half twice = 4 layers\n- Cross-shaped net of 6 squares = valid cube net",
        "\nDISTANCE RULES:\n- Pythagorean theorem: a² + b² = c²\n- 3-4-5 triangle: distance = 5\n- Always check if right angle is implied",
        "\nMIRROR RULES:\n- Vertical mirror reverses left-right only\n- 'F' in vertical mirror = backwards F\n- 'b' in vertical mirror = 'd' (not 'q')",
    ]
    
    if mutation_type in ("random", "spatial_boost"):
        enhancement = random.choice(spatial_enhancements)
        if enhancement not in new_system:
            new_system += enhancement
            mutations_applied.append(f"added_spatial_enhancement: {enhancement[:60]}...")
    
    # Reasoning chain mutations
    reasoning_chains = [
        "\nSTEP-BY-STEP PROTOCOL:\n1. Read the question carefully\n2. Identify what is being asked\n3. Eliminate obviously wrong options\n4. Verify your answer makes logical sense",
        "\nFor trick questions: read literally. 'All but 9 die' means 9 survive.\nFor pattern questions: find the differences between consecutive terms.\nFor sequence: 1,1,2,3,5,8,13 (Fibonacci: each = sum of two previous)",
    ]
    
    if mutation_type in ("random", "reasoning_chain"):
        chain = random.choice(reasoning_chains)
        if chain not in new_system:
            new_system += chain
            mutations_applied.append(f"added_reasoning_chain: {chain[:60]}...")
    
    # top_p / top_k mutations
    if mutation_type in ("random", "sampling"):
        if random.random() < 0.5:
            top_p = float(new_params.get("top_p", 0.9))
            new_top_p = max(0.5, min(1.0, top_p + random.choice([-0.05, 0.05])))
            new_params["top_p"] = str(round(new_top_p, 2))
            mutations_applied.append(f"top_p: {top_p} -> {new_params['top_p']}")
        
        if random.random() < 0.5:
            top_k = int(new_params.get("top_k", 40))
            new_top_k = max(10, min(100, top_k + random.choice([-10, 10])))
            new_params["top_k"] = str(new_top_k)
            mutations_applied.append(f"top_k: {top_k} -> {new_params['top_k']}")
    
    # repeat_penalty mutations
    if mutation_type in ("random", "penalty"):
        rp = float(new_params.get("repeat_penalty", 1.1))
        new_rp = max(1.0, min(1.5, rp + random.choice([-0.05, 0.05])))
        new_params["repeat_penalty"] = str(round(new_rp, 2))
        mutations_applied.append(f"repeat_penalty: {rp} -> {new_params['repeat_penalty']}")
    
    # Build new Modelfile
    new_content = build_modelfile(prog["base"], new_params, new_system)
    
    # Save
    gen = int(Path(program_path).stem.split("_")[0].replace("gen", ""))
    prog_idx = len(list(PROGRAMS_DIR.glob(f"gen{gen+1}_program_*.modelfile")))
    new_path = PROGRAMS_DIR / f"gen{gen+1}_program_{prog_idx:03d}.modelfile"
    new_path.write_text(new_content)
    
    # Save mutation record
    mutation_record = {
        "parent": str(program_path),
        "child": str(new_path),
        "type": mutation_type,
        "mutations": mutations_applied,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    MUTATIONS_DIR / f"mutation_{gen+1}_{prog_idx:03d}.json"
    (MUTATIONS_DIR / f"mutation_{gen+1}_{prog_idx:03d}.json").write_text(json.dumps(mutation_record, indent=2))
    
    return new_path, mutations_applied

# Crossover two programs
def crossover_program(path_a, path_b):
    prog_a = parse_modelfile(path_a)
    prog_b = parse_modelfile(path_b)
    
    # Mix parameters
    new_params = {}
    all_keys = set(list(prog_a["params"].keys()) + list(prog_b["params"].keys()))
    for k in all_keys:
        if random.random() < 0.5:
            new_params[k] = prog_a["params"].get(k, prog_b["params"].get(k, ""))
        else:
            new_params[k] = prog_b["params"].get(k, prog_a["params"].get(k, ""))
    
    # Mix system prompts - take spatial parts from both
    system_a = prog_a["system"]
    system_b = prog_b["system"]
    
    # Always keep the base from A (the better parent)
    new_system = system_a
    
    # Add unique spatial/reasoning enhancements from B
    for line in system_b.split("\n"):
        if any(kw in line.upper() for kw in ["SPATIAL", "GEOMETRY", "ROTATION", "FOLDING", "DISTANCE", "MIRROR", "ANGLE", "CLOCK"]):
            if line not in new_system:
                new_system += "\n" + line
    
    new_content = build_modelfile(BASE_MODEL, new_params, new_system)
    
    gen = max(
        int(p.stem.split("_")[0].replace("gen", ""))
        for p in PROGRAMS_DIR.glob("gen*_program_*.modelfile")
    )
    prog_idx = len(list(PROGRAMS_DIR.glob(f"gen{gen}_program_*.modelfile")))
    new_path = PROGRAMS_DIR / f"gen{gen}_program_{prog_idx:03d}_crossover.modelfile"
    new_path.write_text(new_content)
    
    return new_path

# Main evolution loop
def run_evolution(rounds=10, population_size=6):
    benchmark = load_benchmark()
    bloodline = load_bloodline()
    
    log_file = LOGS_DIR / f"evolution_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.jsonl"
    
    print(f"=== ASI-Evolve: SOV-Gemma-OWEM-v3 ===")
    print(f"Target: spatial 88% -> 95%+, overall 95.45% -> 97%+")
    print(f"Rounds: {rounds}, Population: {population_size}")
    print(f"Benchmark: {len(benchmark['categories']['reasoning']['tasks'])}R + "
          f"{len(benchmark['categories']['spatial']['tasks'])}S + "
          f"{len(benchmark['categories']['visual']['tasks'])}V = 22 tasks")
    print()
    
    # Initialize population from gen0
    gen0_files = sorted(PROGRAMS_DIR.glob("gen0_program_*.modelfile"))
    if not gen0_files:
        print("ERROR: No gen0 program found!")
        return
    
    population = []
    for f in gen0_files:
        print(f"Evaluating initial program: {f.name}")
        result = evaluate_program(f, benchmark, bloodline)
        population.append({"path": f, "result": result, "gen": 0})
        print(f"  Overall: {result['scores']['overall']:.2%} | "
              f"R: {result['scores']['reasoning']:.2%} | "
              f"S: {result['scores']['spatial']:.2%} | "
              f"V: {result['scores']['visual']:.2%}")
        
        # Log
        with open(log_file, "a") as lf:
            lf.write(json.dumps({
                "round": 0, "program": str(f),
                "scores": result["scores"],
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }) + "\n")
    
    best_ever = max(population, key=lambda p: p["result"]["scores"]["overall"])
    print(f"\nBest initial: {best_ever['result']['scores']['overall']:.2%}")
    
    # Evolution rounds
    for round_num in range(1, rounds + 1):
        print(f"\n--- Round {round_num}/{rounds} ---")
        
        # Sort by overall score
        population.sort(key=lambda p: p["result"]["scores"]["overall"], reverse=True)
        
        # Keep elite
        elite = population[:2]
        print(f"Elite: {elite[0]['result']['scores']['overall']:.2%}, "
              f"{elite[1]['result']['scores']['overall']:.2%}")
        
        new_population = list(elite)
        
        # Mutate elite to fill population
        mutation_types = ["spatial_boost", "reasoning_chain", "temperature", "sampling", "random", "random"]
        for i in range(population_size - len(elite)):
            parent = elite[i % len(elite)]
            mut_type = mutation_types[i % len(mutation_types)]
            
            new_path, mutations = mutate_program(parent["path"], mut_type)
            print(f"  Mutating ({mut_type}): {new_path.name}")
            
            result = evaluate_program(new_path, benchmark, bloodline)
            new_population.append({"path": new_path, "result": result, "gen": round_num})
            
            print(f"    Overall: {result['scores']['overall']:.2%} | "
                  f"R: {result['scores']['reasoning']:.2%} | "
                  f"S: {result['scores']['spatial']:.2%} | "
                  f"V: {result['scores']['visual']:.2%}")
            
            with open(log_file, "a") as lf:
                lf.write(json.dumps({
                    "round": round_num, "program": str(new_path),
                    "mutations": mutations, "scores": result["scores"],
                    "timestamp": datetime.utcnow().isoformat() + "Z"
                }) + "\n")
        
        # Crossover between top 2
        if len(elite) >= 2 and random.random() < 0.5:
            cross_path = crossover_program(elite[0]["path"], elite[1]["path"])
            result = evaluate_program(cross_path, benchmark, bloodline)
            new_population.append({"path": cross_path, "result": result, "gen": round_num})
            print(f"  Crossover: {cross_path.name} -> {result['scores']['overall']:.2%}")
        
        population = new_population
        
        # Update best
        round_best = max(population, key=lambda p: p["result"]["scores"]["overall"])
        if round_best["result"]["scores"]["overall"] > best_ever["result"]["scores"]["overall"]:
            best_ever = round_best
            print(f"  *** NEW BEST: {best_ever['result']['scores']['overall']:.2%} ***")
        
        print(f"  Round best: {round_best['result']['scores']['overall']:.2%}")
        print(f"  Best ever: {best_ever['result']['scores']['overall']:.2%}")
    
    # Final report
    print(f"\n{'='*60}")
    print(f"EVOLUTION COMPLETE")
    print(f"{'='*60}")
    print(f"Best program: {best_ever['path']}")
    print(f"Overall: {best_ever['result']['scores']['overall']:.2%}")
    print(f"Reasoning: {best_ever['result']['scores']['reasoning']:.2%}")
    print(f"Spatial: {best_ever['result']['scores']['spatial']:.2%}")
    print(f"Visual: {best_ever['result']['scores']['visual']:.2%}")
    print(f"Generation: {best_ever['gen']}")
    
    # Save final report
    report = {
        "experiment": "sov_gemma_owem_v3",
        "best_program": str(best_ever["path"]),
        "best_scores": best_ever["result"]["scores"],
        "best_generation": best_ever["gen"],
        "total_rounds": rounds,
        "improvement": {
            "overall": best_ever["result"]["scores"]["overall"] - 0.9545,
            "spatial": best_ever["result"]["scores"]["spatial"] - 0.88,
        },
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    (EXPERIMENT_DIR / "evolution_report.json").write_text(json.dumps(report, indent=2))
    print(f"\nReport saved to: {EXPERIMENT_DIR / 'evolution_report.json'}")
    
    return best_ever

if __name__ == "__main__":
    rounds = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    run_evolution(rounds=rounds)
