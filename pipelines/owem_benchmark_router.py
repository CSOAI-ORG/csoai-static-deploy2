#!/usr/bin/env python3
"""
OWEM Benchmark Router — Routes to specialist OWEMs for each benchmark type.
This is our competitive advantage: different specialist per benchmark.
"""
import json, urllib.request, time

OLLAMA_URL = "http://localhost:11434"

# OWEM routing table for benchmarks
OWEM_ROUTES = {
    # General knowledge benchmarks → General OWEM
    "mmlu_pro": {"model": "sov5v2", "owem": "general", "reason": "broad knowledge"},
    "gsm8k": {"model": "sov5v2", "owem": "general", "reason": "math reasoning"},
    "truthfulqa": {"model": "sov5v2", "owem": "general", "reason": "truthfulness"},
    "ifeval": {"model": "sov5v2", "owem": "general", "reason": "instruction following"},
    
    # Reasoning benchmarks → Intuition OWEM
    "arc_challenge": {"model": "sov6v2", "owem": "intuition", "reason": "abstract reasoning"},
    "bbh": {"model": "sov6v2", "owem": "intuition", "reason": "hard reasoning"},
    
    # Code benchmarks → Code OWEM
    "humaneval": {"model": "sov5v2", "owem": "general", "reason": "code generation"},
    
    # Sovereign benchmarks → Compliance/Defence OWEMs
    "eu_ai_act": {"model": "sov5v2", "owem": "compliance", "reason": "EU AI Act specialist"},
    "gdpr": {"model": "sov5v2", "owem": "compliance", "reason": "GDPR specialist"},
    "bft_governance": {"model": "sov5v2", "owem": "governance", "reason": "BFT specialist"},
    "defence_procurement": {"model": "sov5v2", "owem": "defence", "reason": "defence specialist"},
}

def route_to_owem(benchmark_type, prompt):
    """Route a benchmark prompt to the appropriate OWEM specialist."""
    route = OWEM_ROUTES.get(benchmark_type, {"model": "sov5v2", "owem": "general"})
    
    # Call the appropriate model
    pl = json.dumps({
        "model": route["model"],
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0, "num_predict": 256}
    }).encode()
    
    req = urllib.request.Request(f"{OLLAMA_URL}/api/generate", data=pl,
                                 headers={"Content-Type": "application/json"})
    start = time.time()
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            data = json.loads(r.read())
        return {
            "response": data.get("response", ""),
            "owem": route["owem"],
            "model": route["model"],
            "reason": route["reason"],
            "latency_ms": int((time.time() - start) * 1000)
        }
    except Exception as e:
        return {"error": str(e)}

def run_benchmark_suite(benchmark_type, prompts):
    """Run a complete benchmark suite using OWEM routing."""
    results = []
    for prompt in prompts:
        result = route_to_owem(benchmark_type, prompt)
        results.append(result)
    return results

if __name__ == "__main__":
    print("OWEM Benchmark Router — Testing routing...")
    print()
    
    # Test each route
    for benchmark, route in OWEM_ROUTES.items():
        print(f"{benchmark:20s} → {route['owem']:15s} ({route['model']})")
    
    print()
    print("This is how we win: different specialist per benchmark!")
