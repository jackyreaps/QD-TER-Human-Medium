"""
QD-TER Manifold Rheology & Fluid Dynamics Module (Doc 7.0).

DESIGN INVARIANT: Aether is an immutable substrate. This module only computes
downstream rheological responses (fluid perturbations) acting over that fixed
substrate. Do not attempt to rederive or alter fundamental aether fields here.

BIOELECTRIC EXTENSION (Levin 2026): Organism profiles include empirically
measurable bioelectric state variables. These are boundary conditions on the
pre-existing substrate, not cascade-derived quantities.
"""
from dataclasses import dataclass
from enum import Enum
from typing import Dict, Any, Tuple
import numpy as np


class StrategicTopology(Enum):
    ABYSS = "Abyss of Decoherence: Hyper-fluid strategy fragmentation."
    RIDGE = "The Ridge of Optimal Function: Balanced, credible strategic signaling."
    VALLEY = "The Valley of Ossification: Catastrophic structural engine-lock."
    TURBULENT = "Turbulent Decoupling: High velocity, low coherence."


@dataclass(frozen=True)
class AetherSubstrateConstants:
    """
    PRE-EXISTING SUBSTRATE. DO NOT REDERIVE.
    Static properties of the local polaritonic medium.
    """
    PERMITTIVITY_VACUUM: float = 8.8541878128e-12
    PERMEABILITY_VACUUM: float = 1.2566370621e-06
    AETHER_DENSITY_CONSTANT: float = 1.0


@dataclass(frozen=True)
class BioelectricState:
    """
    Empirically measurable bioelectric boundary conditions (Levin 2026).
    Hardware-level observables: resting-potential deviation from species baseline,
    gap-junction density (electrical synapse substrate), and relative ion-channel
    expression. These are inputs to the rheology layer, not outputs of it.
    """
    resting_potential_deviation_mv: float = 0.0
    gap_junction_density: float = 0.5
    ion_channel_expression: float = 1.0


@dataclass(frozen=True)
class OrganismProfile:
    """
    Represents the biophysical constraints inherited from Doc 6.0 layers,
    extended with the bioelectric memory substrate.
    """
    nr3c1_density: float
    coherence_credit: float
    bioelectric: BioelectricState = BioelectricState()


class ChiralManifoldRheology:
    def __init__(
        self,
        substrate: AetherSubstrateConstants,
        min_re_threshold: float = 10.0,
        max_re_threshold: float = 100.0,
        characteristic_node_dimension: float = 0.05,
        bioelectric_decoupling_threshold: float = 0.15,
    ) -> None:
        self.substrate = substrate
        self.min_re_threshold = min_re_threshold
        self.max_re_threshold = max_re_threshold
        self.node_dim = characteristic_node_dimension
        self.bioelectric_decoupling_threshold = bioelectric_decoupling_threshold

    def calculate_metabolic_demethylation_cost(
        self,
        substrate_density: float,
        chromatin_tension: float,
        enzymatic_efficiency: float
    ) -> float:
        if substrate_density < 0 or chromatin_tension < 0 or enzymatic_efficiency < 0:
            raise ValueError("Physical inputs for metabolic calculation must be non-negative.")
        delta_g_reconfig = (enzymatic_efficiency * substrate_density) + chromatin_tension
        return float(delta_g_reconfig)

    def compute_cognitive_glue_index(
        self,
        oxtr_activation: float,
        gap_junction_density: float
    ) -> float:
        oxtr_clamped = max(float(oxtr_activation), 1e-5)
        gj_clamped = max(float(gap_junction_density), 1e-5)
        return float(np.sqrt(oxtr_clamped * gj_clamped))

    def compute_dielectric_reynolds_number(
        self,
        charge_density: float,
        phase_velocity: float,
        oxtr_activation: float,
        gap_junction_density: float = 1.0
    ) -> float:
        if charge_density < 0 or phase_velocity < 0 or oxtr_activation < 0:
            raise ValueError("Physical metrics cannot be negative values.")

        glue_index = self.compute_cognitive_glue_index(oxtr_activation, gap_junction_density)
        effective_viscosity = 1.0 / glue_index
        effective_phase_velocity = phase_velocity * (1.0 + 0.5 * gap_junction_density)

        re_epsilon = (
            charge_density * effective_phase_velocity * self.node_dim
        ) / effective_viscosity
        return float(re_epsilon)

    def assess_bioelectric_decoupling(self, bioelectric: BioelectricState) -> Tuple[bool, float]:
        gj_severity = max(
            0.0, self.bioelectric_decoupling_threshold - bioelectric.gap_junction_density
        )
        pot_severity = abs(bioelectric.resting_potential_deviation_mv) / 20.0
        severity = float(np.sqrt(gj_severity ** 2 + pot_severity ** 2))
        is_decoupled = severity > 0.5
        return is_decoupled, severity

    def determine_strategic_state(
        self, re_epsilon: float, current_credit: float
    ) -> StrategicTopology:
        current_credit = max(0.0, min(current_credit, 1.0))

        if current_credit < 0.3:
            return StrategicTopology.ABYSS
        if (
            self.min_re_threshold <= re_epsilon <= self.max_re_threshold
            and current_credit >= 0.7
        ):
            return StrategicTopology.RIDGE
        elif re_epsilon < self.min_re_threshold:
            return StrategicTopology.VALLEY
        else:
            return StrategicTopology.TURBULENT


def process_interaction_node(
    player_a: OrganismProfile,
    player_b: OrganismProfile,
    external_oxtr_stimulus: float,
    engine: ChiralManifoldRheology,
) -> Dict[str, Any]:
    external_oxtr_stimulus = max(0.0, external_oxtr_stimulus)

    alignment_delta = abs(player_a.nr3c1_density - player_b.nr3c1_density)

    bioelectric_delta = abs(
        player_a.bioelectric.resting_potential_deviation_mv
        - player_b.bioelectric.resting_potential_deviation_mv
    )

    combined_delta = 0.7 * alignment_delta + 0.3 * (bioelectric_delta / 20.0)
    base_phase_velocity = 1.0 / (combined_delta + 1e-3)

    mean_gj = (
        player_a.bioelectric.gap_junction_density
        + player_b.bioelectric.gap_junction_density
    ) / 2.0

    re_epsilon = engine.compute_dielectric_reynolds_number(
        charge_density=engine.substrate.AETHER_DENSITY_CONSTANT,
        phase_velocity=base_phase_velocity,
        oxtr_activation=external_oxtr_stimulus,
        gap_junction_density=mean_gj,
    )

    strategic_topology = engine.determine_strategic_state(
        re_epsilon=re_epsilon, current_credit=player_a.coherence_credit
    )

    is_phase_locked = (
        re_epsilon >= engine.min_re_threshold
        and alignment_delta < 0.2
        and bioelectric_delta < 10.0
    )

    decoupled_a, severity_a = engine.assess_bioelectric_decoupling(player_a.bioelectric)
    decoupled_b, severity_b = engine.assess_bioelectric_decoupling(player_b.bioelectric)

    return {
        "dielectric_reynolds_number": re_epsilon,
        "topology_status": strategic_topology,
        "phase_locked": is_phase_locked,
        "chromatin_alignment_delta": alignment_delta,
        "bioelectric_alignment_delta": bioelectric_delta,
        "bioelectric_decoupled": decoupled_a or decoupled_b,
        "max_decoupling_severity": max(severity_a, severity_b),
        "cognitive_glue_index": engine.compute_cognitive_glue_index(
            external_oxtr_stimulus, mean_gj
        ),
    }
