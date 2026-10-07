"""Tests for src/manifold/peptidein_load.py.

Companion to Theory/Peptidein_load_dynamics.md.
Verifies the 8-channel peptidein load model: initialization, leaky-kernel
dynamics, Number-Location diagnostics, landscape mapping, Sigma-1
clearance, and recovery.
"""

import numpy as np
import pytest

from src.manifold.peptidein_load import (
    DEFAULT_N_CHANNELS,
    GLUE_CHANNELS,
    GLUE_DEPLETION_THRESHOLD,
    IMMUNE_CHANNELS,
    LOCATION_ERROR_THRESHOLD,
    PeptideinChannelProfile,
    PeptideinLoad,
    Sigma1Gateway,
    default_channel_profiles,
)


# ----------------------------------------------------------------------
# Fixtures
# ----------------------------------------------------------------------

@pytest.fixture
def load() -> PeptideinLoad:
    """Default PeptideinLoad at inherited_load=0.1."""
    return PeptideinLoad(inherited_load=0.1)


@pytest.fixture
def gateway() -> Sigma1Gateway:
    """Default Sigma1Gateway."""
    return Sigma1Gateway()


# ----------------------------------------------------------------------
# Channel profile construction
# ----------------------------------------------------------------------

def test_default_profiles_count_is_eight():
    assert len(default_channel_profiles()) == DEFAULT_N_CHANNELS


def test_default_profiles_expected_fractions_sum_to_one():
    total = sum(p.expected_fraction for p in default_channel_profiles())
    assert abs(total - 1.0) < 1e-9


def test_default_profiles_topology_groups():
    """Glue 0.50, immune 0.20, structural 0.30."""
    profiles = default_channel_profiles()
    glue = sum(profiles[i].expected_fraction for i in range(0, 4))
    immune = sum(profiles[i].expected_fraction for i in range(4, 7))
    structural = profiles[7].expected_fraction
    assert abs(glue - 0.50) < 1e-9
    assert abs(immune - 0.20) < 1e-9
    assert abs(structural - 0.30) < 1e-9


def test_default_profiles_all_gammas_positive():
    assert all(p.gamma > 0 for p in default_channel_profiles())


def test_default_profiles_all_capacities_positive():
    assert all(p.binding_capacity > 0 for p in default_channel_profiles())


# ----------------------------------------------------------------------
# Profile validation
# ----------------------------------------------------------------------

def test_profile_rejects_negative_channel_id():
    with pytest.raises(ValueError):
        PeptideinChannelProfile(-1, 1.0, 0.1, 0.1)


def test_profile_rejects_zero_capacity():
    with pytest.raises(ValueError):
        PeptideinChannelProfile(0, 0.0, 0.1, 0.1)


def test_profile_rejects_negative_expected_fraction():
    with pytest.raises(ValueError):
        PeptideinChannelProfile(0, 1.0, -0.1, 0.1)


def test_profile_rejects_negative_gamma():
    with pytest.raises(ValueError):
        PeptideinChannelProfile(0, 1.0, 0.1, -0.1)


# ----------------------------------------------------------------------
# PeptideinLoad initialization
# ----------------------------------------------------------------------

def test_load_initializes_with_eight_channels(load):
    assert load.n_channels == DEFAULT_N_CHANNELS
    assert len(load.states) == DEFAULT_N_CHANNELS
    assert len(load.gamma) == DEFAULT_N_CHANNELS
    assert len(load.binding_capacity) == DEFAULT_N_CHANNELS
    assert len(load.expected_distribution) == DEFAULT_N_CHANNELS


def test_load_initial_state_equals_inherited_load():
    load = PeptideinLoad(inherited_load=0.25)
    assert np.allclose(load.states, 0.25)


def test_load_rejects_negative_inherited_load():
    with pytest.raises(ValueError):
        PeptideinLoad(inherited_load=-0.01)


def test_load_rejects_wrong_channel_count():
    profiles = default_channel_profiles()[:7]
    with pytest.raises(ValueError):
        PeptideinLoad(channel_profiles=profiles)


def test_load_working_gamma_equals_baseline_at_init(load):
    assert np.allclose(load.gamma, load._gamma_baseline)


def test_load_allostatic_residue_equals_sum(load):
    assert abs(load.allostatic_residue - float(np.sum(load.states))) < 1e-12


# ----------------------------------------------------------------------
# compute_write_vector
# ----------------------------------------------------------------------

def test_compute_write_vector_updates_state(load):
    initial = load.states.copy()
    load.compute_write_vector(re_epsilon=50.0, bio_decoupling=0.0)
    assert not np.array_equal(load.states, initial)


def test_compute_write_vector_returns_copy(load):
    returned = load.compute_write_vector(re_epsilon=50.0, bio_decoupling=0.0)
    returned[:] = 0.0
    assert not np.all(load.states == 0.0)


def test_compute_write_vector_rejects_decoupling_above_one(load):
    with pytest.raises(ValueError):
        load.compute_write_vector(50.0, 1.5)


def test_compute_write_vector_rejects_negative_decoupling(load):
    with pytest.raises(ValueError):
        load.compute_write_vector(50.0, -0.1)


def test_states_stay_non_negative_under_many_steps(load):
    for _ in range(50):
        load.compute_write_vector(re_epsilon=1.0, bio_decoupling=0.95)
    assert np.all(load.states >= 0.0)


def test_high_coupling_activates_glue_over_immune(load):
    """Ridge-range Re with no decoupling should favor glue channels."""
    load.compute_write_vector(re_epsilon=50.0, bio_decoupling=0.0)
    glue = float(np.sum(load.states[GLUE_CHANNELS]))
    immune = float(np.sum(load.states[IMMUNE_CHANNELS]))
    assert glue > immune


def test_high_decoupling_activates_immune_over_glue(load):
    """Low Re with high decoupling should favor immune channels."""
    load.compute_write_vector(re_epsilon=1.0, bio_decoupling=0.95)
    immune = float(np.sum(load.states[IMMUNE_CHANNELS]))
    glue = float(np.sum(load.states[GLUE_CHANNELS]))
    assert immune > glue


def test_allostatic_residue_updated_after_step(load):
    before = load.allostatic_residue
    load.compute_write_vector(re_epsilon=50.0, bio_decoupling=0.0)
    assert load.allostatic_residue != before


# ----------------------------------------------------------------------
# Gamma management
# ----------------------------------------------------------------------

def test_reset_gamma_restores_baseline(load):
    load.gamma = load.gamma * 5.0
    load.reset_gamma()
    assert np.allclose(load.gamma, load._gamma_baseline)


def test_gamma_baseline_not_mutated_by_reset(load):
    baseline_before = load._gamma_baseline.copy()
    load.gamma = load.gamma * 5.0
    load.reset_gamma()
    assert np.array_equal(load._gamma_baseline, baseline_before)


# ----------------------------------------------------------------------
# check_spatial_criticality — structure
# ----------------------------------------------------------------------

def test_criticality_returns_expected_keys(load):
    result = load.check_spatial_criticality()
    for key in (
        "diagnosis",
        "local_jamming",
        "global_jamming",
        "location_error",
        "saturated_channels",
    ):
        assert key in result


def test_criticality_returns_expected_types(load):
    result = load.check_spatial_criticality()
    assert isinstance(result["diagnosis"], str)
    assert isinstance(result["local_jamming"], float)
    assert isinstance(result["global_jamming"], float)
    assert isinstance(result["location_error"], float)
    assert isinstance(result["saturated_channels"], list)


def test_location_error_bounded_in_unit_interval(load):
    result = load.check_spatial_criticality()
    assert 0.0 <= result["location_error"] <= 1.0


# ----------------------------------------------------------------------
# check_spatial_criticality — diagnoses
# ----------------------------------------------------------------------

def test_initial_state_is_optimal(load):
    assert load.check_spatial_criticality()["diagnosis"] == "OPTIMAL"


def test_density_critical_on_channel_over_capacity(load):
    """Scale to expected distribution x3 so channel 8 exceeds capacity."""
    load.states = load.expected_distribution * 3.0
    result = load.check_spatial_criticality()
    assert result["diagnosis"] == "DENSITY_CRITICAL"
    assert 7 in result["saturated_channels"]


def test_topology_error_on_immune_dominant_distribution(load):
    """Immune channels dominant, no channel over capacity."""
    load.states[:] = 0.05
    load.states[4:7] = 0.5
    result = load.check_spatial_criticality()
    assert result["diagnosis"] == "TOPOLOGY_ERROR"
    assert result["location_error"] > LOCATION_ERROR_THRESHOLD
    assert result["saturated_channels"] == []


def test_compound_failure_when_both_fail(load):
    """Immune channels shifted and channel 8 saturated."""
    load.states[:] = 0.05
    load.states[4:7] = 0.5
    load.states[7] = 2.0
    result = load.check_spatial_criticality()
    assert result["diagnosis"] == "COMPOUND_FAILURE"
    assert result["local_jamming"] > 1.0
    assert result["location_error"] > LOCATION_ERROR_THRESHOLD


def test_local_jamming_is_max_not_total(load):
    """A single saturated channel drives local_jamming."""
    load.states[:] = 0.05
    load.states[7] = 2.0
    result = load.check_spatial_criticality()
    assert result["local_jamming"] == pytest.approx(
        load.states[7] / load.binding_capacity[7]
    )


def test_saturated_channels_list_is_sorted(load):
    load.states[:] = 0.05
    load.states[4:7] = 0.5
    load.states[7] = 2.0
    result = load.check_spatial_criticality()
    assert result["saturated_channels"] == sorted(
        result["saturated_channels"]
    )


# ----------------------------------------------------------------------
# evaluate_landscape_zone
# ----------------------------------------------------------------------

def test_landscape_ridge_on_optimal(load):
    assert load.evaluate_landscape_zone() == "RIDGE"


def test_landscape_valley_on_density_critical(load):
    load.states = load.expected_distribution * 3.0
    assert load.evaluate_landscape_zone() == "VALLEY"


def test_landscape_valley_on_topology_error(load):
    load.states[:] = 0.05
    load.states[4:7] = 0.5
    assert load.evaluate_landscape_zone() == "VALLEY"


def test_landscape_valley_on_compound_failure(load):
    load.states[:] = 0.05
    load.states[4:7] = 0.5
    load.states[7] = 2.0
    assert load.evaluate_landscape_zone() == "VALLEY"


def test_landscape_abyss_on_glue_depletion(load):
    load.states[:] = 0.0
    load.states[0] = 0.05
    assert load.evaluate_landscape_zone() == "ABYSS"


def test_abyss_threshold_boundary(load):
    """Glue density exactly at threshold is not Abyss."""
    load.states[:] = 0.0
    load.states[0] = GLUE_DEPLETION_THRESHOLD
    assert load.evaluate_landscape_zone() != "ABYSS"


# ----------------------------------------------------------------------
# Sigma1Gateway — constructor validation
# ----------------------------------------------------------------------

def test_gateway_rejects_low_degradation_gain():
    with pytest.raises(ValueError):
        Sigma1Gateway(degradation_gain=0.5)


def test_gateway_rejects_zero_retrafficking_rate():
    with pytest.raises(ValueError):
        Sigma1Gateway(retrafficking_rate=0.0)


def test_gateway_rejects_retrafficking_above_one():
    with pytest.raises(ValueError):
        Sigma1Gateway(retrafficking_rate=1.5)


def test_gateway_initial_state_is_closed(gateway):
    assert gateway.gate_state == "CLOSED"
    assert gateway.mode is None


# ----------------------------------------------------------------------
# Sigma1Gateway — mode selection
# ----------------------------------------------------------------------

def test_gateway_no_op_on_optimal(load, gateway):
    result = gateway.detect_and_respond(load)
    assert result["diagnosis"] == "OPTIMAL"
    assert result["mode"] is None
    assert result["gate_state"] == "CLOSED"


def test_gateway_degrades_on_density_critical(load, gateway):
    load.states = load.expected_distribution * 3.0
    result = gateway.detect_and_respond(load)
    assert result["diagnosis"] == "DENSITY_CRITICAL"
    assert result["mode"] == "DEGRADATION"
    assert result["gate_state"] == "OPEN"


def test_gateway_retraffics_on_topology_error(load, gateway):
    load.states[:] = 0.05
    load.states[4:7] = 0.5
    result = gateway.detect_and_respond(load)
    assert result["diagnosis"] == "TOPOLOGY_ERROR"
    assert result["mode"] == "RETRAFFICKING"
    assert result["gate_state"] == "OPEN"


def test_gateway_compound_correction_on_compound_failure(load, gateway):
    load.states[:] = 0.05
    load.states[4:7] = 0.5
    load.states[7] = 2.0
    result = gateway.detect_and_respond(load)
    assert result["diagnosis"] == "COMPOUND_FAILURE"
    assert result["mode"] == "COMPOUND_CORRECTION"
    assert result["gate_state"] == "OPEN"


# ----------------------------------------------------------------------
# Sigma1Gateway — effects
# ----------------------------------------------------------------------

def test_degradation_raises_gamma_on_saturated_channel(load, gateway):
    load.states = load.expected_distribution * 3.0
    baseline_gamma_7 = load._gamma_baseline[7]
    gateway.detect_and_respond(load)
    assert load.gamma[7] > baseline_gamma_7


def test_gamma_recomputed_from_baseline_not_compounded(load, gateway):
    load.states = load.expected_distribution * 3.0
    gateway.detect_and_respond(load)
    first_gamma = load.gamma.copy()
    gateway.detect_and_respond(load)
    assert np.allclose(first_gamma, load.gamma)


def test_retrafficking_reduces_location_error(load, gateway):
    load.states[:] = 0.05
    load.states[4:7] = 0.5
    before = load.check_spatial_criticality()["location_error"]
    gateway.detect_and_respond(load)
    after = load.check_spatial_criticality()["location_error"]
    assert after < before


def test_retrafficking_preserves_total_load(load, gateway):
    load.states[:] = 0.05
    load.states[4:7] = 0.5
    before_total = float(np.sum(load.states))
    gateway.detect_and_respond(load)
    after_total = float(np.sum(load.states))
    assert after_total == pytest.approx(before_total, rel=1e-9)


def test_gateway_resets_gamma_on_recovery_to_optimal(load, gateway):
    load.states = load.expected_distribution * 3.0
    gateway.detect_and_respond(load)
    load.states[:] = 0.1
    gateway.detect_and_respond(load)
    assert np.allclose(load.gamma, load._gamma_baseline)


def test_gateway_close_resets_gateway_state(load, gateway):
    load.states = load.expected_distribution * 3.0
    gateway.detect_and_respond(load)
    gateway.close(load)
    assert gateway.gate_state == "CLOSED"
    assert gateway.mode is None
    assert np.allclose(load.gamma, load._gamma_baseline)


# ----------------------------------------------------------------------
# Recovery
# ----------------------------------------------------------------------

def test_saturated_channel_decays_under_repeated_correction(load, gateway):
    """A saturated channel must decay toward capacity under repeated
    Sigma-1 correction, even while the stress persists."""
    load.states[:] = 0.05
    load.states[4:7] = 0.5
    load.states[7] = 2.0
    initial = load.states[7]

    for _ in range(20):
        load.compute_write_vector(re_epsilon=50.0, bio_decoupling=0.0)
        gateway.detect_and_respond(load)

    assert load.states[7] < initial