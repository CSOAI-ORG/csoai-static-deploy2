#!/usr/bin/env python3
"""
SOV Router — Routes to best model (online/offline)
"""
import json, urllib.request, time

OLLAMA = "http://localhost:11434"

MODELS = {
    "sov5v2": {"score": 95, "offline": True, "online": True},
    "sov6v2": {"score": 90, "offline": True, "online": True},
    "sov-ultimate": {"score": 95, "offline": True, "online": True},
    "qwen3:30b-a3b": {"score": 86, "offline": False, "online": True},
    "llama3.2:3b": {"score": 76.8, "offline": True, "online": True},
}

def check_ollama():
    """Check if Ollama is running"""
    try:
        urllib.request.urlopen(OLLAMA + '/api/tags', timeout=5)
        return True
    except:
        return False

def route(task_type):
    """Route to best model based on task type"""
    if check_ollama():
        # Offline mode - use local models
        return "sov5v2" if task_type == "general" else "sov6v2"
    else:
        # Online mode - use API models
        return "qwen3:30b-a3b"

def get_status():
    """Get router status"""
    return {
        "ollama": check_ollama(),
        "models": MODELS,
        "routing": "offline" if check_ollama() else "online"
    }

if __name__ == "__main__":
    status = get_status()
    print(json.dumps(status, indent=2))
