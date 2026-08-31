import pytest
from src.manifold.rheology import (
    AetherSubstrateConstants,
    BioelectricState,
    ChiralManifoldRheology,
    OrganismProfile,
    StrategicTopology,
    process_interaction_node,
)


@pytest.fixture
def setup_engine():
    substrate = AetherSubstrateConstants()
    return ChiralManifoldRheology(substrate=substrate, characteristic_node_dimension=0.5)


def test_reynolds_number_scaling_with_oxtr(setup_engine):
    """Re_ε rises monotonically as OXTR activation increases."""
    engine = setup_engine
    re_low = engine.compute_dielectric_reynolds_number(
        charge_density=1.0, phase_velocity=5.0, oxtr_activation=0.1, gap_junction_density=0.5
    )
    re_high = engine.compute_dielectric_reynolds_number(
        charge_density=1.0, phase_velocity=5.0, oxtr_activation=0.8, gap_junction_density=0.5
    )
    assert re_high > re_low


def test_gap_junction_effect_on_reynolds(setup_engine):
    """Re_ε rises with gap-junction density (cognitive glue propagation)."""
    engine = setup_engine
    re_low_gj = engine.compute_dielectric_reynolds_number(
        charge_density=1.0, phase_velocity=5.0, oxtr_activation=0.5, gap_junction_density=0.1
    )
    re_high_gj = engine.compute_dielectric_reynolds_number(
        charge_density=1.0, phase_velocity=5.0, oxtr_activation=0.5, gap_junction_density=0.9
    )
    assert re_high_gj > re_low_gj


def test_low_credit_forces_abyss(setup_engine):
    """Low credit forces the system into the Abyss regardless of fluid metrics."""
    engine = setup_engine
    topology = engine.determine_strategic_state(re_epsilon=25.0, current_credit=0.1)
    assert topology == StrategicTopology.ABYSS


def test_optimal_conditions_land_on_ridge(setup_engine):
    """High credit and mid-range Re land on the Ridge."""
    engine = setup_engine
    topology = engine.determine_strategic_state(re_epsilon=50.0, current_credit=0.8)
    assert topology == StrategicTopology.RIDGE


def test_bioelectric_decoupling_detection(setup_engine):
    """Severe gap-junction loss + potential deviation triggers decoupling."""
    engine = setup_engine
    decoupled_state = BioelectricState(
        resting_potential_deviation_mv=25.0, gap_junction_density=0.05
    )
    is_decoupled, severity = engine.assess_bioelectric_decoupling(decoupled_state)
    assert is_decoupled is True
    assert severity > 0.5


def test_integration_hook_with_bioelectric(setup_engine):
    """Full integration: aligned chromatin + aligned bioelectric + functional OXTR."""
    engine = setup_engine
    player_a = OrganismProfile(
        nr3c1_density=0.5,
        coherence_credit=0.8,
        bioelectric=BioelectricState(
            resting_potential_deviation_mv=2.0, gap_junction_density=0.6
        ),
    )
    player_b = OrganismProfile(
        nr3c1_density=0.52,
        coherence_credit=0.75,
        bioelectric=BioelectricState(
            resting_potential_deviation_mv=3.0, gap_junction_density=0.55
        ),
    )
    result = process_interaction_node(
        player_a=player_a,
        player_b=player_b,
        external_oxtr_stimulus=0.5,
        engine=engine,
    )
    assert "dielectric_reynolds_number" in result
    assert isinstance(result["topology_status"], StrategicTopology)
    assert result["phase_locked"] is True
    assert result["cognitive_glue_index"] > 0.0
    assert result["bioelectric_decoupled"] is False


def test_bioelectric_decoupled_players_cannot_phase_lock(setup_engine):
    """Bioelectric misalignment blocks phase-lock even with matched chromatin."""
    engine = setup_engine
    player_a = OrganismProfile(
        nr3c1_density=0.5,
        coherence_credit=0.8,
        bioelectric=BioelectricState(
            resting_potential_deviation_mv=2.0, gap_junction_density=0.6
        ),
    )
    player_b = OrganismProfile(
        nr3c1_density=0.5,
        coherence_credit=0.8,
        bioelectric=BioelectricState(
            resting_potential_deviation_mv=30.0, gap_junction_density=0.05
        ),
    )
    result = process_interaction_node(
        player_a=player_a,
        player_b=player_b,
        external_oxtr_stimulus=0.5,
        engine=engine,
    )
    assert result["bioelectric_decoupled"] is True
    assert result["phase_locked"] is False
