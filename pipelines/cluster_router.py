#!/usr/bin/env python3
"""
Cluster Router — Distribute work across all free GPU sites
Routes to fastest available site for maximum speed
"""
import json, time, urllib.request
from pathlib import Path

# All free GPU sites
FREE_SITES = {
    "kaggle": {"gpu": "T4", "hours": 30, "speed": "fast", "url": "kaggle.com"},
    "colab": {"gpu": "T4", "hours": 12, "speed": "fast", "url": "colab.research.google.com"},
    "huggingface": {"gpu": "T4", "hours": 30, "speed": "fast", "url": "huggingface.co"},
    "modal": {"gpu": "T4", "hours": 30, "speed": "fast", "url": "modal.com"},
    "lightning": {"gpu": "T4", "hours": 22, "speed": "fast", "url": "lightning.ai"},
    "deepnote": {"gpu": "T4", "hours": 60, "speed": "medium", "url": "deepnote.com"},
    "oracle": {"gpu": "ARM", "hours": 999, "speed": "slow", "url": "cloud.oracle.com"},
    "runpod": {"gpu": "A40", "hours": 0, "speed": "fast", "url": "runpod.io", "cost": "$2.89/hr"},
}

# Top models to run
TOP_MODELS = {
    "sov5v2": {"base": "qwen2.5:3b", "score": 95, "site": "kaggle"},
    "sov-ultimate": {"base": "qwen2.5:3b", "score": 95, "site": "colab"},
    "sov-ultimate-sovereign": {"base": "qwen2.5:3b", "score": 95, "site": "huggingface"},
    "mistral:7b": {"base": "mistral:7b", "score": 93.8, "site": "modal"},
    "qwen3:30b-a3b": {"base": "qwen3:30b-a3b", "score": 86, "site": "runpod"},
}

class ClusterRouter:
    """Route work to fastest available free GPU site"""
    
    def __init__(self):
        self.sites = FREE_SITES
        self.models = TOP_MODELS
    
    def get_fastest_site(self):
        """Get fastest available site"""
        # Priority: Kaggle > Colab > HuggingFace > Modal > Lightning > DeepNote
        priority = ["kaggle", "colab", "huggingface", "modal", "lightning", "deepnote"]
        for site in priority:
            if self.sites[site]["hours"] > 0:
                return site
        return "oracle"  # Fallback to always-free
    
    def route_model(self, model_name):
        """Route model to best site"""
        model = self.models.get(model_name)
        if not model:
            return self.get_fastest_site()
        return model["site"]
    
    def get_all_routes(self):
        """Get routing for all models"""
        routes = {}
        for model_name, model in self.models.items():
            site = self.route_model(model_name)
            routes[model_name] = {
                "site": site,
                "gpu": self.sites[site]["gpu"],
                "speed": self.sites[site]["speed"],
                "cost": self.sites[site].get("cost", "$0.00"),
            }
        return routes
    
    def print_routes(self):
        """Print all routes"""
        routes = self.get_all_routes()
        print("Model Route Map:")
        print("=" * 60)
        for model, route in routes.items():
            print(f"  {model:25s} -> {route['site']:15s} ({route['gpu']}, {route['speed']}, {route['cost']})")
        print()
        print("Total sites: " + str(len(self.sites)))
        print("Total models: " + str(len(self.models)))
        print("Cost: $0.00 (all free except RunPod)")

if __name__ == "__main__":
    router = ClusterRouter()
    router.print_routes()
