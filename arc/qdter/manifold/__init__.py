"""QD-TER Human-Medium manifold package.

Reference rheology module + optional EEG hyperscanning gate.
"""

from .rheology import (
    AetherSubstrateConstants,
    BioelectricState,
    ChiralManifoldRheology,
    OrganismProfile,
    StrategicTopology,
    process_interaction_node,
)

from .eeg_hyperscan import (
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
