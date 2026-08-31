"""QD-TER Human-Medium manifold package.

Production rheology module for dielectric fluid dynamics
and bioelectric state computation.
"""

from .rheology import (
    AetherSubstrateConstants,
    BioelectricState,
    ChiralManifoldRheology,
    OrganismProfile,
    StrategicTopology,
    process_interaction_node,
)

__all__ = [
    "AetherSubstrateConstants",
    "BioelectricState",
    "ChiralManifoldRheology",
    "OrganismProfile",
    "StrategicTopology",
    "process_interaction_node",
]
