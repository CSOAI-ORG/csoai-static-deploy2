"""
IWM — Inner World Model: Sovereign Swarm Intelligence

Architecture:
  SOV SPACE (top level)
  ├── 12 OWEM Hives (domain clusters)
  │   ├── 12 Clan Layers per hive (144 total)
  │   │   ├── 12 Families per clan (1,728 total)
  │   │   │   └── 4 Models per family (6,912 total)
  │   │   │       ├── OWM-Frozen (perception, stable)
  │   │   │       ├── OWM-Fluid (perception, adapting)
  │   │   │       ├── IWM-Frozen (reasoning, stable)
  │   │   │       └── IWM-Fluid (reasoning, evolving)
  ├── Stigmergy (Pheromone + Waggle + Pollen)
  ├── Spine Drum (heartbeat synchronizer)
  ├── Constitutional AI (safety layer)
  ├── RAG Pipeline (knowledge retrieval)
  └── G-Space (knowledge graph + GNN)
"""

from .g_space import GSpace
from .j_space import JSpace
from .clan_engine import ClanEngine
from .bft_quorum import BFTQuorum
from .owm import OWM
from .iwm import IWM
from .owem_brain import OWEMBrain
from .owem_hive import OWEMHive
from .sov_router import SOVRouter
from .sov_space import SOVSpace
from .stigmergy import DistributedStigmergy, LocalStigmergy, GossipProtocol, DistributedSpineDrum
from .constitutional_ai import ConstitutionalAI
from .rag_pipeline import RAGPipeline
from .arena_integration import ArenaIntegration
from .arena_trainer import ArenaTrainer
from .unified_gnn import UnifiedGNN, InnerGNN, OuterGNN, Dreamer

__all__ = [
    "GSpace", "JSpace", "ClanEngine", "BFTQuorum", "OWM", "IWM",
    "OWEMBrain", "OWEMHive", "SOVRouter", "SOVSpace",
    "DistributedStigmergy", "LocalStigmergy", "GossipProtocol", "DistributedSpineDrum",
    "ConstitutionalAI", "RAGPipeline", "ArenaIntegration", "ArenaTrainer",
    "UnifiedGNN", "InnerGNN", "OuterGNN", "Dreamer",
]
