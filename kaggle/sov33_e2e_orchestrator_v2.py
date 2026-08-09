#!/usr/bin/env python3
"""
sov33_e2e_orchestrator_v2.py — restore of the provider registry contract.

The sov33_staged_train / sov33_distill / sov33_self_train scripts import
`PROVIDERS` from this module. Only that symbol is required:

    PROVIDERS = {
        "<provider>": {"key": "<ENV_VAR>", "base": "<openai-compat url>", "model": "<default>"},
    }

Keys are read from the environment at call time (never embedded here).
"""
from __future__ import annotations

PROVIDERS = {
    "groq": {
        "key": "GROQ_API_KEY",
        "base": "https://api.groq.com/openai/v1",
        "model": "llama-3.3-70b-versatile",
    },
    "deepseek": {
        "key": "DEEPSEEK_API_KEY",
        "base": "https://api.deepseek.com/v1",
        "model": "deepseek-chat",
    },
    "openrouter": {
        "key": "OPENROUTER_API_KEY",
        "base": "https://openrouter.ai/api/v1",
        "model": "auto",
    },
}

__all__ = ["PROVIDERS"]