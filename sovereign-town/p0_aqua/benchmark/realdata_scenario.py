#!/usr/bin/env python3
"""
Real-data scenario grounding for the Sovereign OOWM.

Turns a real GDELT signal (UK/EU AI-governance news volume + tone) into a benchmark
scenario config, so the governed world reacts to REAL-WORLD conditions rather than only
synthetic shocks. This is the step from "signed simulation" to "signed instrument".

Mapping rationale (documented, not magic):
  - news VOLUME on regulation/unrest  -> enforcement pressure. More regulatory attention in
    the real world => tighter gate (higher block_rate), mirroring how live scrutiny raises
    compliance pressure. Mapped into a realistic band [0.55, 0.95] (never the perfect gate).
  - mean TONE (GDELT sentiment, roughly -10..+10) -> baseline disorder. More negative tone
    (crisis, conflict) => higher BASELINE_LAWLESSNESS and contagion; positive tone => calmer.

All coefficients are explicit and bounded. The function is pure: pass the parsed GDELT data,
get a scenario dict compatible with benchmark.scenarios. No network here (fetch upstream).
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any


def _clamp(x: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, x))


@dataclass(frozen=True)
class MappingParams:
    """Calibratable coefficients of the GDELT->scenario mapping.

    These are PRIORS, not fitted values. `calibrate_realdata.py` runs a sensitivity
    analysis over them and documents what real ground-truth would be needed to FIT them.
    Every coefficient here is a modelling choice that should be justified against data.
    """
    enf_floor: float = 0.55        # enforcement at zero news volume
    enf_ceiling: float = 0.95      # max enforcement (never a perfect 1.0 gate)
    enf_volume_scale: float = 30.0 # articles at which the volume->enforcement curve saturates
    lawl_intercept: float = 0.25   # baseline disorder at neutral tone
    lawl_tone_coeff: float = 0.03  # how much each tone unit shifts baseline disorder
    contagion_base: float = 0.14   # contagion step at neutral tone
    contagion_tone_coeff: float = 0.04  # how much tone scales contagion
    lawl_bounds: tuple = (0.05, 0.60)
    contagion_bounds: tuple = (0.05, 0.30)


DEFAULT_PARAMS = MappingParams()


def gdelt_to_scenario(gdelt: dict[str, Any], params: MappingParams = DEFAULT_PARAMS) -> dict[str, Any]:
    """
    Map parsed GDELT payload -> scenario config, using calibratable `params`.

    gdelt: {"articles": [...], "tone": [ {value: float}, ... ] (optional)}
    Returns a scenario dict: {block_rate, BASELINE_LAWLESSNESS, CONTAGION_STEP, _provenance}
    """
    articles = gdelt.get("articles", []) or []
    tone_pts = gdelt.get("tone", []) or []

    volume = len(articles)
    tone_vals = [p.get("value") for p in tone_pts if isinstance(p, dict) and p.get("value") is not None]
    mean_tone = sum(tone_vals) / len(tone_vals) if tone_vals else 0.0

    # VOLUME -> enforcement pressure (saturating). regulatory attention tightens the gate,
    # never to a perfect/unrealistic 1.0.
    span = params.enf_ceiling - params.enf_floor
    block_rate = _clamp(params.enf_floor + span * (1.0 - 2.718281828 ** (-volume / params.enf_volume_scale)),
                        params.enf_floor, params.enf_ceiling)

    # TONE -> baseline disorder (negative tone => more lawlessness).
    baseline_lawlessness = _clamp(params.lawl_intercept - mean_tone * params.lawl_tone_coeff,
                                  *params.lawl_bounds)

    # negative TONE also raises contagion (crisis spreads faster).
    contagion_step = _clamp(params.contagion_base * (1.0 - mean_tone * params.contagion_tone_coeff),
                            *params.contagion_bounds)

    return {
        "block_rate": round(block_rate, 4),
        "BASELINE_LAWLESSNESS": round(baseline_lawlessness, 4),
        "CONTAGION_STEP": round(contagion_step, 4),
        "_provenance": {
            "source": "GDELT api.gdeltproject.org",
            "article_volume": volume,
            "mean_tone": round(mean_tone, 3),
            "mapping": "volume->enforcement[floor,ceiling]; tone->baseline_lawlessness & contagion",
            "params_are_priors": True,
        },
    }
