"""
Peptidein Load Dynamics — v9.0 mechanism-layer sub-document.

SPECIFICATION
    QD-TER_HumanMedium_v9.0/Theory/Peptidein_load_dynamics.md
    "Peptidein Load Dynamics: Number–Location Criticality and
    Sigma-1 Clearance."

DESIGN INVARIANTS
    - Channel count (8) is INHERITED from the physics suite's residual
      V_4 action on the 36-mode waist. It is NOT derived here.
      See QD-TER_HumanMedium_v9.0/Theory/Residual_integer_8.md.
    - This module does NOT import from rheology.py. It accepts
      Re_epsilon and bio_decoupling as scalar inputs, consistent with
      the design invariant of Endocrine_chromatin.py.

WHAT THIS MODULE ADDS
    1. PeptideinLoad: 8-channel peptidein state vector with per-channel
       leaky-kernel accumulation dynamics.
    2. Number–Location diagnostics: separates binding-site saturation
       (Number) from ectopic accumulation (Location).
    3. Sigma1Gateway: mode-specific clearance operator. Corrects
       density by accelerated degradation, location by re-trafficking.

EMPIRICAL GROUNDING
    TransCODE Consortium (2026): ~1,785 peptideins from 7,264 ncORFs;
    3,116 HLA-I-presented ncORF peptides; 51 pan-essential ncORFs.
    OLMALINC (Channel 8): chromatin looping, cell-cycle regulation.
    Sigma-1R: ER chaperine, translocates to nuclear envelope,
    recruits chromatin-remodeling factors.

REFERENCES
    Deutsch et al. (2026), TransCODE Consortium.
    Hayashi & Su (2007), Sigma-1 receptor chaperones.
    Richter et al. (2007), Macromolecular crowding.
    McEwen (1998), Allostatic load.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import numpy as np


# ----------------------------------------------------------------------
# Constants
# ----------------------------------------------------------------------

#: Inherited channel count from the physics suite.
DEFAULT_N_CHANNELS: int = 8

#: Topology slices.
GLUE_CHANNELS: slice = slice(0, 4)       # pi1-pi4: surface glue
IMMUNE_CHANNELS: slice = slice(4, 7)     # pi5-pi7: secreted immune
STRUCTURAL_CHANNEL: int = 7              # pi8: OLMALINC anchor

#: Diagnostic thresholds. Derived from the binding-site model:
#: local jamming > 1.0 means a channel has exceeded capacity;
#: global jamming > 0.85 means the system is near capacity;
#: location error > 0.30 is a significant shift away from the
#: design topology.
LOCAL_JAMMING_THRESHOLD: float = 1.0
GLOBAL_JAMMING_THRESHOLD: float = 0.85
LOCATION_ERROR_THRESHOLD: float = 0.30

#: Abyss threshold: glue peptidein density below which the system
#: loses cognitive glue.
GLUE_DEPLETION_THRESHOLD: float = 0.25


# ----------------------------------------------------------------------
# Channel profile
# ----------------------------------------------------------------------

@dataclass
class PeptideinChannelProfile:
    """Binding-site profile for one peptidein channel.

    Attributes:
        channel_id: Index in [0, n_channels).
        binding_capacity: Maximum sustainable concentration before
            excluded-volume jamming at this channel.
        expected_fraction: Expected fraction of the total peptidein
            population under Ridge conditions. Used to compute the
            ectopic shift (Location error).
        gamma: Baseline degradation rate. Glue channels fastest;
            structural channel slowest.
    """

    channel_id: int
    binding_capacity: float
    expected_fraction: float
    gamma: float

    def __post_init__(self) -> None:
        if self.channel_id < 0:
            raise ValueError("channel_id must be non-negative.")
        if self.binding_capacity <= 0:
            raise ValueError("binding_capacity must be positive.")
        if self.expected_fraction < 0:
            raise ValueError("expected_fraction must be non-negative.")
        if self.gamma <= 0:
            raise ValueError("gamma must be positive.")


def default_channel_profiles() -> List[PeptideinChannelProfile]:
    """Return the canonical 8-channel peptidein profile.

    Capacities reflect chromatin topology: glue channels high
    (surface, high turnover), immune channels medium (secreted,
    persistent), structural channel low (chromatin-associated).

    Expected fractions sum to 1.0: glue 0.50, immune 0.20,
    structural 0.30.

    Gamma encodes half-lives: glue channels most responsive,
    structural channel slowest.
    """
    return [
        PeptideinChannelProfile(0, 2.0, 0.15, 0.45),  # pi1 surface glue
        PeptideinChannelProfile(1, 2.0, 0.15, 0.45),  # pi2 surface glue
        PeptideinChannelProfile(2, 2.0, 0.12, 0.40),  # pi3 gap-junction mod
        PeptideinChannelProfile(3, 2.0, 0.08, 0.40),  # pi4 oxytocin viscosity
        PeptideinChannelProfile(4, 1.5, 0.08, 0.15),  # pi5 immune marker
        PeptideinChannelProfile(5, 1.5, 0.06, 0.15),  # pi6 immune marker
        PeptideinChannelProfile(6, 1.5, 0.06, 0.10),  # pi7 immune boundary
        PeptideinChannelProfile(7, 0.8, 0.30, 0.05),  # pi8 OLMALINC anchor
    ]


# ----------------------------------------------------------------------
# PeptideinLoad
# ----------------------------------------------------------------------

class PeptideinLoad:
    """8-channel peptidein state vector with Number–Location diagnostics.

    Args:
        inherited_load: Baseline epigenetic constraint on the
            non-coding landscape. Sets the initial state of every
            channel.
        channel_profiles: Optional override. If None, uses the
            default 8-channel profile. Any other length is rejected.

    Attributes:
        states: Current peptidein concentration vector, shape (8,).
        gamma: Working degradation rates. Recomputed by the
            Sigma1Gateway on each call. Baseline is stored in
            `_gamma_baseline`.
        binding_capacity: Per-channel binding-site capacity.
        expected_distribution: Per-channel expected fraction under
            Ridge conditions.
        allostatic_residue: Sum of the current state vector.
    """

    def __init__(
        self,
        inherited_load: float = 0.1,
        channel_profiles: Optional[List[PeptideinChannelProfile]] = None,
    ) -> None:
        if inherited_load < 0:
            raise ValueError("inherited_load must be non-negative.")

        self.profiles = (
            channel_profiles if channel_profiles is not None
            else default_channel_profiles()
        )
        self.n_channels = len(self.profiles)

        if self.n_channels != DEFAULT_N_CHANNELS:
            raise ValueError(
                f"Expected {DEFAULT_N_CHANNELS} channels (inherited), "
                f"got {self.n_channels}."
            )

        self.states = np.full(
            self.n_channels, float(inherited_load), dtype=float
        )
        self.binding_capacity = np.array(
            [p.binding_capacity for p in self.profiles], dtype=float
        )
        self.expected_distribution = np.array(
            [p.expected_fraction for p in self.profiles], dtype=float
        )
        self._gamma_baseline = np.array(
            [p.gamma for p in self.profiles], dtype=float
        )
        self.gamma = self._gamma_baseline.copy()
        self.allostatic_residue: float = float(np.sum(self.states))

    # ------------------------------------------------------------------
    # Gamma management
    # ------------------------------------------------------------------

    def reset_gamma(self) -> None:
        """Restore working gamma to the inherited baseline."""
        self.gamma = self._gamma_baseline.copy()

    # ------------------------------------------------------------------
    # Core dynamics
    # ------------------------------------------------------------------

    def compute_write_vector(
        self,
        re_epsilon: float,
        bio_decoupling: float,
    ) -> np.ndarray:
        """Step the peptidein state vector forward by one tick.

        Args:
            re_epsilon: Dielectric Reynolds number. RIDGE: 10-100.
                VALLEY: < 10.
            bio_decoupling: Bioelectric decoupling severity in [0, 1].
                0 = fully coupled; 1 = fully decoupled.

        Returns:
            Updated 8-channel state vector (copy).

        Raises:
            ValueError: If bio_decoupling is outside [0, 1].
        """
        if bio_decoupling < 0 or bio_decoupling > 1:
            raise ValueError("bio_decoupling must be in [0, 1].")

        # Non-linear activation. Sinusoidal in Re_epsilon because
        # gap-junction coupling has phase dependence. Modulated by
        # bioelectric decoupling.
        activation = float(
            np.sin(re_epsilon * np.pi / 2.0) * (1.0 - bio_decoupling)
        )

        # Channel-specific generation profile.
        # Glue channels activated by coupling.
        # Immune channels activated by decoupling (stress response).
        # Structural channel activated by both (anchor).
        generation_profile = np.array([
            activation * 1.2,
            activation * 1.0,
            activation * 0.8,
            activation * 0.5,
            (1.0 - activation) * 1.5,
            (1.0 - activation) * 1.1,
            (1.0 - activation) * 0.9,
            activation * 2.0,
        ], dtype=float)

        # Leaky-kernel step (Euler).
        self.states = self.states + (
            generation_profile - (self.gamma * self.states)
        )
        self.states = np.clip(self.states, 0.0, None)
        self.allostatic_residue = float(np.sum(self.states))
        return self.states.copy()
