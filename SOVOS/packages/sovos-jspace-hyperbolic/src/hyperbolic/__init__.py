"""Hyperbolic package — Poincaré + Procrustes combined."""
from .poincare import (
    Axis, axis_anchor, HyperbolicPiece,
    hierarchy_depth, mobius_add, poincare_distance, project_to_ball,
)
from .procrustes import (
    LoraPair, merge_loras_linear, merge_loras_procrustes,
    procrustes_alignment, rotation_distance,
)

__version__ = "0.1.0"
__all__ = [
    "Axis", "axis_anchor", "HyperbolicPiece",
    "hierarchy_depth", "mobius_add", "poincare_distance", "project_to_ball",
    "LoraPair", "merge_loras_linear", "merge_loras_procrustes",
    "procrustes_alignment", "rotation_distance",
]