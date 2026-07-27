import json
import os
import re
import time
import hashlib
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from sov_invariants import (
    BFT_COUNCIL_SIZE,
    BFT_QUORUM,
    CARE_FLOOR,
    SOVEREIGN_DID,
    SIGIL_ROOT,
    care_score,
    emit_sigil,
    normalize_name,
    validate_care_floor,
    validate_tally,
)

DEFAULT_BASE = os.environ.get("SOV_OLLAMA_URL", "http://127.0.0.1:11434")

MASTER_TEXT_MODELS = [
    "qwen3:8b",
    "qwen3:30b-a3b",
    "qwen2.5:32b",
    "sov5v2:latest",
    "sov4-sov7-master-pro:latest",
    "sov4-sov7-ultra:latest",
    "sov33-v2:latest",
    "sov6-preservation-v3:latest",
    "sov6-creation-v3:latest",
    "qwen2.5:3b",
    "qwen2.5:1.5b",
    "qwen2.5:0.5b",
    "llama3.2:3b",
    "deepseek-coder:1.3b",
    "deepseek-r1:32b",
    "mistral:7b",
    "gemma3:12b",
    "master:latest",
]

OWEM_GROUP_MODELS = {
    "compliance": ["compliance:latest", "qwen.compliance:latest", "mistral.compliance:latest", "llama.compliance:latest", "deepseek.compliance:latest", "llamaxdeepseek.compliance:latest", "deepseekxmistral.compliance:latest"],
    "defense": ["defence:latest", "qwen.defence:latest", "mistral.defence:latest", "llama.defence:latest", "deepseek.defence:latest", "llamaxdeepseek.defence:latest", "deepseekxmistral.defence:latest"],
    "intuition": ["intuition:latest", "mistral.intuition:latest", "llama.intuition:latest", "deepseek.intuition:latest", "llamaxdeepseek.intuition:latest", "deepseekxmistral.intuition:latest"],
    "voice": ["mistral.voice:latest", "llama.voice:latest", "deepseek.voice:latest", "llamaxdeepseek.voice:latest", "deepseekxmistral.voice:latest"],
    "general": ["general_ability:latest", "mistral.general:latest", "llama.general:latest", "deepseek.general:latest", "llamaxdeepseek.general:latest", "deepseekxmistral.general:latest"],
    "auditability": ["auditability:latest", "honor:latest", "justice:latest"],
}

ALL_TRAINABLE_MODELS = list(dict.fromkeys(MASTER_TEXT_MODELS + [name for names in OWEM_GROUP_MODELS.values() for name in names]))

CAPABILITY_MODELS: Dict[str, Dict[str, List[str]]] = {
    capability: {"text": ALL_TRAINABLE_MODELS}
    for capability in (
        "reasoning",
        "spatial_reasoning",
        "agentic",
        "code",
        "j_space",
        "sov_space",
        "games",
        "sovereign",
        "math",
    )
}
CAPABILITY_MODELS["visual_reasoning"] = {
    "text": ALL_TRAINABLE_MODELS,
    "image": ["llava:7b"],
}

VETO_MARKERS = (
    "kill order", "strike package", "track individual", "face-rec",
    "find-fix-finish", "kinetic-targeting", "build a bomb",
    "synthesize meth", "ransomware payload", "keylogger dropper",
)

ADAPTER_HINTS: Dict[str, str] = {
    "reasoning": "Reason step by step. Output ONLY the final answer, no analysis.",
    "spatial_reasoning": "Reason about positions, directions, and grids. Output ONLY the final answer.",
    "visual_reasoning": "Inspect the image and answer the question. Output ONLY the final answer.",
    "agentic": "You may call tools. Plan internally, then emit the final answer.",
    "code": "Write the function only. No prose before or after.",
    "j_space": "Operate in J-space: list assumptions, simulate, then state result.",
    "sov_space": "Operate in SOV-space: assign coordinates, route to the closest pillar, return result.",
    "games": "Play rationally. State move and result succinctly.",
    "sovereign": "Honor charter; cite article or pillar when relevant.",
    "math": "Show the calculation then state the final number.",
}


def _http_json(url, payload, timeout):
    data = None if payload is None else json.dumps(payload).encode()
    headers = {"Content-Type": "application/json"} if payload is not None else {}
    request = urllib.request.Request(url, data=data, headers=headers)
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read())


def available_models(base_url):
    return sorted({str(model.get("name")) for model in _http_json(f"{base_url.rstrip('/')}/api/tags", None, 20).get("models", []) if model.get("name")})


def model_info(base_url, model):
    try:
        return _http_json(f"{base_url.rstrip('/')}/api/show", {"name": model}, 20)
    except Exception:
        return {}


def is_vision_model(info, model):
    capabilities = {str(item).lower() for item in info.get("capabilities", [])}
    details = info.get("details") or {}
    families = {str(item).lower() for item in details.get("families", [])}
    name = model.lower()
    if {"vision", "image"} & capabilities:
        return True
    if {"clip", "llava", "qwen2vl", "qwen2.5vl", "qwen3-vl"} & families:
        return True
    return any(token in name for token in ("vision", "-vl", ":vl", "llava", "qwen2-vl", "qwen2.5vl"))


def _stringify(value):
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    return json.dumps(value, default=str, sort_keys=True)


def call_model(base_url, model, prompt, timeout, image_b64=None):
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0, "num_predict": 192},
    }
    if image_b64 is not None:
        payload["images"] = [image_b64]
    started = time.monotonic()
    try:
        data = _http_json(f"{base_url.rstrip('/')}/api/generate", payload, timeout)
        return {"ok": True, "response": str(data.get("response", "")), "latency_ms": round((time.monotonic() - started) * 1000, 2), "tokens_in": data.get("prompt_eval_count", 0), "tokens_out": data.get("eval_count", 0), "model": model}
    except Exception as error:
        return {"ok": False, "error": f"{type(error).__name__}: {error}", "latency_ms": round((time.monotonic() - started) * 1000, 2), "model": model}


def _tally_for(success, care):
    if success and care >= CARE_FLOOR:
        return {"approve": 28, "amend": 5, "reject": 0}
    return {"approve": 0, "amend": 0, "reject": BFT_COUNCIL_SIZE}


class SOVMaster:
    def __init__(self, base_url=None, capability_models=None):
        self.base_url = base_url or DEFAULT_BASE
        self.capability_models = capability_models or CAPABILITY_MODELS
        self.registry = {"models": {}, "tests": [], "honey": []}
        self.honey_path = Path(__file__).with_name("sov-master-honey.json")
        if self.honey_path.exists():
            try:
                self.registry = json.loads(self.honey_path.read_text())
            except Exception:
                pass
        try:
            for model in available_models(self.base_url):
                self.registry.setdefault("models", {})[model] = {
                    "info": model_info(self.base_url, model),
                    "vision": is_vision_model(model_info(self.base_url, model), model),
                }
        except Exception as error:
            self.registry.setdefault("errors", []).append({"stage": "discovery", "error": _stringify(error)})

    def capability_candidates(self, capability, modality="text"):
        capability = normalize_name(capability)
        spec = self.capability_models.get(capability, {})
        preferred = list(spec.get(modality, []))
        available = set(self.registry.get("models", {}).keys())
        ordered = [name for name in preferred if name in available]
        if not ordered:
            ordered = sorted(available)
        return ordered

    def build_prompt(self, capability, question, options, image_b64):
        capability = normalize_name(capability)
        prefix = ADAPTER_HINTS.get(capability, "Output only the final answer.")
        options_block = ""
        if options:
            options_block = "\n" + "\n".join(f"{chr(65 + index)}) {option}" for index, option in enumerate(options))
        if image_b64 is not None:
            prefix = "[Image attached] " + prefix
        return f"{prefix}\n\nQuestion: {question}{options_block}\nAnswer:"

    def attempt(self, capability, question, options, modality, timeout, image_b64=None):
        capability = normalize_name(capability)
        candidates = self.capability_candidates(capability, modality)
        results = []
        for model in candidates:
            call = call_model(self.base_url, model, self.build_prompt(capability, question, options, image_b64), timeout, image_b64)
            if call["ok"]:
                results.append(call)
                break
        if not results:
            return None
        return results[0]

    def grade(self, task, response):
        cleaned = (response or "").strip()
        if not cleaned:
            return False
        options = task.get("options")
        answer = str(task.get("answer", ""))
        if options:
            upper = cleaned.upper()
            if upper and upper.split()[0].rstrip(".)") in {"A", "B", "C", "D"}:
                return upper.split()[0].rstrip(".)") == answer.upper()
            patterns = [
                r"(?:final\s+answer|answer|choice|option|select)\s*(?:is|:|-)?\s*\(?([A-D])\)?",
                r"\b([A-D])\b",
            ]
            for pattern in patterns:
                match = re.search(pattern, upper)
                if match:
                    return match.group(1).upper() == answer.upper()
        if answer.lower() in {"true", "false"}:
            return answer.lower() in cleaned.lower()
        if re.fullmatch(r"-?\d+(?:\.\d+)?", answer):
            numbers = re.findall(r"-?\d+(?:\.\d+)?", cleaned.replace(",", ""))
            if not numbers:
                return False
            try:
                return abs(float(numbers[-1]) - float(answer)) < 0.01
            except ValueError:
                return numbers[-1] == answer
        return answer.lower() in cleaned.lower()

    def _sigil(self, payload, success, care):
        tally = _tally_for(success, care)
        return emit_sigil(payload, tally, care)

    def run_task(self, task, capability=None, modality="text", timeout=120, image_b64=None):
        capability = capability or task.get("capability") or "reasoning"
        response = self.attempt(capability, task["q"], task.get("options"), modality, timeout, image_b64=image_b64)
        if not response:
            return {"ok": False, "error": "no working model", "capability": capability, "task": task["id"]}
        correct = self.grade(task, response["response"])
        care = care_score(response["response"], short_floor=CARE_FLOOR)
        sigil = self._sigil({"task": task["id"], "model": response["model"], "capability": capability, "ok": correct}, correct, care)
        entry = {
            "id": task["id"],
            "capability": capability,
            "model": response["model"],
            "correct": bool(correct),
            "care_score": care,
            "latency_ms": response.get("latency_ms", 0),
            "tokens_in": response.get("tokens_in", 0),
            "tokens_out": response.get("tokens_out", 0),
            "sigil": sigil,
        }
        self.registry.setdefault("tests", []).append(entry)
        return entry

    def run_suite(self, suite, timeout=120):
        modality = "image" if suite.get("fixture") else "text"
        results = []
        for task in suite.get("tasks", []):
            results.append(self.run_task(task, capability=suite["capability"], modality=modality, timeout=timeout, image_b64=suite.get("fixture_b64")))
        return results

    def run_honey_stage(self, capability_registry, j_space_queries, sov_space_queries, game_prompts):
        summary = {"started": datetime.now(timezone.utc).isoformat()}
        summary["capabilities"] = {}
        for capability, suite in capability_registry["capabilities"].items():
            modality = "image" if suite.get("modality") == "image" else "text"
            entries = self.run_suite({"capability": capability, "tasks": suite["tasks"], "modality": modality})
            passed = sum(1 for entry in entries if entry.get("correct"))
            summary["capabilities"][capability] = {
                "passed": passed,
                "tested": len(entries),
                "score_pct": round(100 * passed / len(entries), 2) if entries else None,
                "models_used": sorted({entry.get("model", "?") for entry in entries}),
            }
        summary["j_space"] = [{"prompt": prompt, "response": self.attempt("j_space", prompt, None, "text", 120)} for prompt in j_space_queries]
        summary["sov_space"] = [{"prompt": prompt, "response": self.attempt("sov_space", prompt, None, "text", 120)} for prompt in sov_space_queries]
        summary["games"] = [{"prompt": prompt, "response": self.attempt("games", prompt, None, "text", 120)} for prompt in game_prompts]
        summary["ended"] = datetime.now(timezone.utc).isoformat()
        canonical = json.dumps(summary, sort_keys=True, ensure_ascii=False).encode()
        summary["sigil"] = hashlib.sha256(canonical).hexdigest()
        return summary

    def bake_honey(self, summary):
        self.registry.setdefault("honey", []).append(summary)
        canonical = json.dumps(self.registry, sort_keys=True, ensure_ascii=False, default=str).encode()
        self.registry["sigil"] = hashlib.sha256(canonical).hexdigest()
        self.honey_path.write_text(json.dumps(self.registry, indent=2, ensure_ascii=False, default=str) + "\n")
        return self.honey_path

    def describe(self):
        return {
            "base_url": self.base_url,
            "models": sorted(self.registry.get("models", {}).keys()),
            "capabilities": {capability: {modality: list(models) for modality, models in spec.items()} for capability, spec in self.capability_models.items()},
            "registry_sigil": self.registry.get("sigil"),
            "test_count": len(self.registry.get("tests", [])),
            "honey_count": len(self.registry.get("honey", [])),
        }
