"""
IWM — Inner World Model: Sovereign Swarm Intelligence

Architecture:
  SOV SPACE (top level)
  ├── G-SPACE (GNN lives here, learns routing from all outcomes)
  │   ├── Knowledge Graph (19 families × capabilities)
  │   └── GNN (learns win patterns, routes to best clan)
  ├── CLAN ENGINE (spawns family swarms)
  │   ├── J-SPACE (per-family simulation)
  │   │   ├── Frozen (base model weights)
  │   │   └── Fluid (honey-trained variant)
  │   └── C-SPACE (composite of family J-spaces)
  ├── BFT QUORUM (cross-clan voting)
  └── ARENA (Kaggle/competition entry point)
"""

from .g_space import GSpace
from .j_space import JSpace
from .clan_engine import ClanEngine
from .bft_quorum import BFTQuorum
from .owm import OWM
from .iwm import IWM

__all__ = ["GSpace", "JSpace", "ClanEngine", "BFTQuorum", "OWM", "IWM"]
