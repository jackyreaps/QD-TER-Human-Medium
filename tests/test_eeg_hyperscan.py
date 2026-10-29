"""Tests for src/qdter/manifold/eeg_hyperscan.py.

Committed with the module per v9.0 Section 9.5.

The critical tests here are:
    test_kuramoto_coupling_actually_locks
    test_no_coupling_produces_low_icoh
    test_volume_conduction_does_not_pass_icoh
    test_zero_lag_common_source_is_rejected

The first two would have caught the signal-vs-phase bug in the original
Kuramoto implementation. The last two test the volume-conduction
rejection that motivates the iCOH choice over raw PLV. Because a
single-trial estimate is noisy, the statistical tests average over
several seeds instead of relying on one draw.
"""

import numpy as np
import pytest

SEEDS = (11, 12, 13, 14, 15)

from qdter.manifold.eeg_hyperscan import (
    DEFAULT_ICOH_THRESHOLD,
    SensorMontage,
    SourceSpace,
    compute_hyperscan_phase_lock,
    forward_project,
    generate_source_activity,
    imaginary_coherence,
    inter_brain_icoh,
    rheology_coupling,
    source_reconstruct,
)


# ----------------------------------------------------------------------
# Fixtures
# ----------------------------------------------------------------------

@pytest.fixture
def strong_coupling_result() -> dict:
    return {
        "dielectric_reynolds_number": 50.0,
        "cognitive_glue_index": 0.9,
        "chromatin_alignment_delta": 0.0,
        "bioelectric_alignment_delta": 0.0,
        "bioelectric_decoupled": False,
    }


@pytest.fixture
def weak_coupling_result() -> dict:
    return {
        "dielectric_reynolds_number": 0.0,
        "cognitive_glue_index": 0.01,
        "chromatin_alignment_delta": 1.0,
        "bioelectric_alignment_delta": 20.0,
        "bioelectric_decoupled": True,
    }


@pytest.fixture
def montage() -> SensorMontage:
    np.random.seed(0)
    return SensorMontage()


# ----------------------------------------------------------------------
# Data structures
# ----------------------------------------------------------------------

def test_source_space_default_shape():
    src = SourceSpace()
    assert src.n_sources == 6
    assert len(src.labels) == 6
    assert src.positions.shape == (6, 3)


def test_source_space_rejects_bad_shape():
    with pytest.raises(ValueError):
        SourceSpace(positions=np.zeros((5, 3)))


def test_montage_default_leadfield_shape():
    np.random.seed(0)
    m = SensorMontage()
    assert m.leadfield.shape == (16, 6)


def test_montage_rejects_bad_shape():
    with pytest.raises(ValueError):
        SensorMontage(positions=np.zeros((10, 3)))


# ----------------------------------------------------------------------
# Kuramoto coupling (the critical test)
# ----------------------------------------------------------------------

def test_kuramoto_coupling_actually_locks(strong_coupling_result):
    """High coupling should produce iCOH above threshold.

    This tests the phase-vs-signal fix directly. With the original
    (buggy) implementation, the B oscillators were driven by A's signal
    rather than A's phase, producing sin(sin(theta) - theta'), which
    does not phase-lock.
    """
    scores = []
    for seed in SEEDS:
        np.random.seed(seed)
        eeg = compute_hyperscan_phase_lock(
            strong_coupling_result, use_reconstruction=False,
        )
        scores.append(eeg["icoh_mean"])
        assert eeg["field_phase_locked"] is True
    assert np.mean(scores) > 0.4


def test_no_coupling_produces_low_icoh(weak_coupling_result):
    """Zero coupling should produce iCOH near zero."""
    scores = []
    for seed in SEEDS:
        np.random.seed(seed)
        eeg = compute_hyperscan_phase_lock(
            weak_coupling_result, use_reconstruction=False,
        )
        scores.append(eeg["icoh_mean"])
        assert eeg["field_phase_locked"] is False
    assert np.mean(scores) < 0.12


def test_coupling_monotonicity():
    """iCOH should increase monotonically with coupling strength."""
    np.random.seed(1)
    low = compute_hyperscan_phase_lock(
        {
            "dielectric_reynolds_number": 1.0,
            "cognitive_glue_index": 0.2,
            "chromatin_alignment_delta": 0.5,
            "bioelectric_alignment_delta": 10.0,
            "bioelectric_decoupled": False,
        },
        use_reconstruction=False,
    )
    np.random.seed(1)
    high = compute_hyperscan_phase_lock(
        {
            "dielectric_reynolds_number": 100.0,
            "cognitive_glue_index": 0.9,
            "chromatin_alignment_delta": 0.0,
            "bioelectric_alignment_delta": 0.0,
            "bioelectric_decoupled": False,
        },
        use_reconstruction=False,
    )
    assert high["icoh_mean"] > low["icoh_mean"]


# ----------------------------------------------------------------------
# Volume conduction rejection
# ----------------------------------------------------------------------

def test_volume_conduction_does_not_pass_icoh():
    """Bioelectric decoupling must block field-level phase-lock even
    with high scalar alignment.

    A single trial can cross the threshold by chance, so the test asks
    that most seeds are rejected and that the average stays well below
    the coupled case.
    """
    bad = {
        "dielectric_reynolds_number": 50.0,
        "cognitive_glue_index": 0.9,
        "chromatin_alignment_delta": 0.0,
        "bioelectric_alignment_delta": 0.0,
        "bioelectric_decoupled": True,
    }
    flags, scores = [], []
    for seed in SEEDS:
        np.random.seed(seed)
        eeg = compute_hyperscan_phase_lock(bad, use_reconstruction=False)
        flags.append(eeg["field_phase_locked"])
        scores.append(eeg["icoh_mean"])
    assert sum(flags) <= 1
    assert np.mean(scores) < 0.25


def test_zero_lag_common_source_is_rejected():
    """Two sensors that mix one common source with independent noise
    share only zero-lag coherence, which iCOH must not report."""
    scores = []
    for seed in SEEDS:
        rng = np.random.default_rng(seed)
        source = rng.standard_normal(30000)
        x = source + 0.5 * rng.standard_normal(30000)
        y = source + 0.5 * rng.standard_normal(30000)
        scores.append(imaginary_coherence(x, y))
    assert max(scores) < 0.1


def test_zero_lag_locking_is_invisible_by_design(strong_coupling_result):
    """Locking with exactly zero lag cannot be told from volume
    conduction, so iCOH does not flag it. This is the cost of the
    volume-conduction rejection, and why the simulator couples with a
    nonzero lag."""
    scores = []
    for seed in SEEDS:
        np.random.seed(seed)
        a, b = generate_source_activity(strong_coupling_result, coupling_lag=0.0)
        scores.append(inter_brain_icoh(a, b)["mean"])
    assert np.mean(scores) < DEFAULT_ICOH_THRESHOLD


def test_coupling_used_matches_the_simulated_coupling(weak_coupling_result):
    np.random.seed(0)
    eeg = compute_hyperscan_phase_lock(
        weak_coupling_result, use_reconstruction=False, duration_s=10.0,
    )
    assert eeg["coupling_used"] == rheology_coupling(weak_coupling_result)[0]
    assert eeg["coupling_used"] < 0.01


# ----------------------------------------------------------------------
# Imaginary coherence
# ----------------------------------------------------------------------

def test_imaginary_coherence_identical_signals():
    """Identical signals are perfectly real-coherent; iCOH should be low."""
    np.random.seed(3)
    t = np.linspace(0, 4, 1000)
    x = np.sin(2 * np.pi * 10 * t)
    icoh = imaginary_coherence(x, x, fs=250.0)
    assert icoh < 0.1


def test_imaginary_coherence_phase_shifted_signals():
    """A 90-degree phase shift produces maximal imaginary coherence."""
    np.random.seed(3)
    t = np.linspace(0, 4, 1000)
    x = np.sin(2 * np.pi * 10 * t)
    y = np.sin(2 * np.pi * 10 * t + np.pi / 2)
    icoh = imaginary_coherence(x, y, fs=250.0)
    assert icoh > 0.5


def test_imaginary_coherence_rejects_mismatched_shapes():
    with pytest.raises(ValueError):
        imaginary_coherence(np.zeros(100), np.zeros(99), fs=250.0)


def test_imaginary_coherence_rejects_2d():
    with pytest.raises(ValueError):
        imaginary_coherence(np.zeros((3, 3)), np.zeros((3, 3)))


def test_imaginary_coherence_handles_short_signal():
    assert imaginary_coherence(np.zeros(2), np.zeros(2)) == 0.0


# ----------------------------------------------------------------------
# inter_brain_icoh
# ----------------------------------------------------------------------

def test_inter_brain_icoh_returns_expected_keys():
    np.random.seed(4)
    a = np.random.randn(3, 500)
    b = np.random.randn(3, 500)
    result = inter_brain_icoh(a, b, fs=250.0)
    assert set(result.keys()) == {"P", "V", "C", "mean"}


def test_inter_brain_icoh_rejects_wrong_shape():
    with pytest.raises(ValueError):
        inter_brain_icoh(np.zeros((2, 100)), np.zeros((2, 100)))


# ----------------------------------------------------------------------
# Forward / inverse
# ----------------------------------------------------------------------

def test_forward_project_shape(montage):
    np.random.seed(5)
    sources = np.random.randn(6, 500)
    data = forward_project(sources, montage, noise_std=0.0)
    assert data.shape == (16, 500)


def test_source_reconstruct_shape(montage):
    np.random.seed(6)
    sources = np.random.randn(6, 500)
    data = forward_project(sources, montage, noise_std=0.0)
    recon = source_reconstruct(data, montage)
    assert recon.shape == (6, 500)


def test_forward_inverse_roundtrip(montage):
    """In the noiseless case with ridge, reconstruction should be close."""
    np.random.seed(7)
    sources = np.random.randn(6, 500)
    data = forward_project(sources, montage, noise_std=0.0)
    recon = source_reconstruct(data, montage, ridge=1e-6)
    # Correlation should be high for each source.
    for i in range(6):
        corr = np.corrcoef(sources[i], recon[i])[0, 1]
        assert corr > 0.5


# ----------------------------------------------------------------------
# Full pipeline
# ----------------------------------------------------------------------

def test_full_pipeline_returns_expected_keys(strong_coupling_result):
    np.random.seed(8)
    result = compute_hyperscan_phase_lock(strong_coupling_result)
    expected = {
        "icoh", "icoh_mean", "icoh_threshold",
        "field_phase_locked", "coupling_used",
    }
    assert expected.issubset(set(result.keys()))


def test_full_pipeline_phase_lock_flag(strong_coupling_result):
    np.random.seed(8)
    result = compute_hyperscan_phase_lock(
        strong_coupling_result, use_reconstruction=False,
    )
    assert result["field_phase_locked"] is True


def test_full_pipeline_default_threshold():
    np.random.seed(9)
    result = compute_hyperscan_phase_lock(
        {
            "dielectric_reynolds_number": 1.0,
            "cognitive_glue_index": 0.1,
            "chromatin_alignment_delta": 0.5,
            "bioelectric_alignment_delta": 10.0,
            "bioelectric_decoupled": False,
        },
        use_reconstruction=False,
    )
    assert result["icoh_threshold"] == DEFAULT_ICOH_THRESHOLD


def test_generate_source_activity_shapes():
    np.random.seed(10)
    result = {
        "dielectric_reynolds_number": 10.0,
        "cognitive_glue_index": 0.5,
        "chromatin_alignment_delta": 0.2,
        "bioelectric_alignment_delta": 5.0,
        "bioelectric_decoupled": False,
    }
    a, b = generate_source_activity(result, duration_s=2.0, sfreq=250.0)
    assert a.shape == (3, 500)
    assert b.shape == (3, 500)
