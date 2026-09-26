"""QD-TER Human-Medium manifold package.

Production rheology module + optional EEG hyperscanning gate.
"""

from .rheology import (
    AetherSubstrateConstants,
    BioelectricState,
    ChiralManifoldRheology,
    OrganismProfile,
    StrategicTopology,
    process_interaction_node,
)

from .EEG_hyperscan import (
    compute_hyperscan_phase_lock,
    SensorMontage,
    SourceSpace,
)

__all__ = [
    "AetherSubstrateConstants",
    "BioelectricState",
    "ChiralManifoldRheology",
    "OrganismProfile",
    "StrategicTopology",
    "process_interaction_node",
    "compute_hyperscan_phase_lock",
    "SensorMontage",
    "SourceSpace",
]
