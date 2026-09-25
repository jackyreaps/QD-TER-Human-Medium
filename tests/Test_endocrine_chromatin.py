"""Tests for src/manifold/endocrine_chromatin.py.

Committed with the module per v9.0 Section 9.5.
"""

import numpy as np
import pytest

from src.manifold.endocrine_chromatin import (
    DEFAULT_N_CHANNELS,
    ChromatinChannel,
    EndocrineChromatinEngine,
    EndocrineSignal,
)


# ----------------------------------------------------------------------
# Fixtures
# ----------------------------------------------------------------------

@pytest.fixture
def engine() -> EndocrineChromatinEngine:
    return EndocrineChromatinEngine(n_channels=8, temporal_resolution=1.0)


@pytest.fixture
def channels() -> list:
    return [
        ChromatinChannel(
            channel_id=i,
            tissue_weight=1.0 + 0.1 * i,
            baseline_methylation=0.2 * (i % 3),
            parity_class=i % 2,
        )
        for i in range(8)
    ]


# ----------------------------------------------------------------------
# Constructor / channel-count enforcement
# ----------------------------------------------------------------------

def test_default_channel_count_is_inherited_8():
    """The default must be the inherited 8, per Theory/Residual_integer_8.md."""
    eng = EndocrineChromatinEngine()
    assert eng.n_channels == 8
    assert eng.n_channels == DEFAULT_N_CHANNELS


def test_constructor_rejects_invalid_channel_count():
    with pytest.raises(ValueError):
        EndocrineChromatinEngine(n_channels=0)


def test_constructor_rejects_invalid_temporal_resolution():
    with pytest.raises(ValueError):
        EndocrineChromatinEngine(temporal_resolution=0.0)
    with pytest.raises(ValueError):
        EndocrineChromatinEngine(temporal_resolution=-1.0)


def test_write_channels_rejects_wrong_count(engine):
    """Write vector must reject mismatched channel lists."""
    bad_channels = [
        ChromatinChannel(i, 1.0, 0.0, i % 2) for i in range(7)
    ]
    with pytest.raises(ValueError):
        engine.write_channels(np.zeros(10), bad_channels)


def test_write_channels_rejects_wrong_state_dimension(engine, channels):
    with pytest.raises(ValueError):
        engine.write_channels(np.zeros((3, 3)), channels)


def test_write_channels_rejects_empty_state(engine, channels):
    with pytest.raises(ValueError):
        engine.write_channels(np.array([]), channels)


# ----------------------------------------------------------------------
# EndocrineSignal
# ----------------------------------------------------------------------

def test_signal_rejects_mismatched_lengths():
    with pytest.raises(ValueError):
        EndocrineSignal(pulse_times=[0.0, 90.0], pulse_amplitudes=[1.0])


def test_signal_resamples_onto_uniform_grid():
    sig = EndocrineSignal(
        pulse_times=[0.0, 90.0, 180.0],
        pulse_amplitudes=[1.0, 1.0, 1.0],
        ultradian_step=90.0,
    )
    t, x = sig.to_series(duration_min=270.0, dt_min=1.0)
    assert len(t) == len(x)
    assert t[0] == 0.0
    assert t[-1] >= 270.0
    # The pulses should produce non-zero concentration.
    assert np.max(x) > 0


# ----------------------------------------------------------------------
# Takens embedding
# ----------------------------------------------------------------------

def test_takens_embed_shape(engine):
    signal = np.arange(100, dtype=float)
    embedded = engine.takens_embed(signal, dim=3, tau=2)
    expected_rows = len(signal) - (3 - 1) * 2
    assert embedded.shape == (expected_rows, 3)


def test_takens_embed_first_row(engine):
    signal = np.arange(10, dtype=float)
    embedded = engine.takens_embed(signal, dim=3, tau=1)
    assert np.allclose(embedded[0], [0.0, 1.0, 2.0])


def test_takens_embed_rejects_short_signal(engine):
    with pytest.raises(ValueError):
        engine.takens_embed(np.array([1.0, 2.0]), dim=5, tau=10)


def test_takens_embed_rejects_bad_dim(engine):
    with pytest.raises(ValueError):
        engine.takens_embed(np.arange(10.0), dim=0, tau=1)


def test_takens_embed_rejects_bad_tau(engine):
    with pytest.raises(ValueError):
        engine.takens_embed(np.arange(10.0), dim=2, tau=0)


# ----------------------------------------------------------------------
# Regime classification
# ----------------------------------------------------------------------

def test_classify_stable_node(engine):
    # Both eigenvalues real, negative.
    J = np.array([[-1.0, 0.0], [0.0, -2.0]])
    assert engine.classify_regime(J) == "STABLE_NODE"


def test_classify_stable_focus(engine):
    # Complex conjugate pair with negative real part.
    J = np.array([[-1.0, 2.0], [-2.0, -1.0]])
    assert engine.classify_regime(J) == "STABLE_FOCUS"


def test_classify_unstable_node(engine):
    J = np.array([[1.0, 0.0], [0.0, 2.0]])
    assert engine.classify_regime(J) == "UNSTABLE_NODE"


def test_classify_unstable_focus(engine):
    J = np.array([[1.0, 2.0], [-2.0, 1.0]])
    assert engine.classify_regime(J) == "UNSTABLE_FOCUS"


def test_classify_saddle(engine):
    J = np.array([[1.0, 0.0], [0.0, -1.0]])
    assert engine.classify_regime(J) == "SADDLE"


def test_classify_bifurcation(engine):
    # Pure imaginary eigenvalues: Hopf boundary.
    J = np.array([[0.0, 1.0], [-1.0, 0.0]])
    assert engine.classify_regime(J) == "BIFURCATION"


def test_classify_rejects_non_square(engine):
    with pytest.raises(ValueError):
        engine.classify_regime(np.zeros((2, 3)))


# ----------------------------------------------------------------------
# Leaky kernel
# ----------------------------------------------------------------------

def test_leaky_integrate_shapes(engine):
    signal = np.ones(200)
    out = engine.leaky_integrate(signal, [0.1, 0.01], [1.0, 1.0])
    assert out.shape == signal.shape


def test_leaky_integrate_rejects_mismatched_spectrum(engine):
    with pytest.raises(ValueError):
        engine.leaky_integrate(np.ones(10), [0.1, 0.2], [1.0])


def test_leaky_integrate_rejects_empty_spectrum(engine):
    with pytest.raises(ValueError):
        engine.leaky_integrate(np.ones(10), [], [])


def test_leaky_integrate_rejects_nonpositive_lambda(engine):
    with pytest.raises(ValueError):
        engine.leaky_integrate(np.ones(10), [0.0], [1.0])
    with pytest.raises(ValueError):
        engine.leaky_integrate(np.ones(10), [-0.1], [1.0])


def test_leaky_integrate_constant_input_is_bounded(engine):
    """A constant input should produce a bounded steady-state output."""
    signal = np.ones(500)
    out = engine.leaky_integrate(signal, [0.1], [1.0])
    # The kernel is normalized, so a constant unit input produces ~1.0
    # in the interior (away from edge transients).
    interior = out[100:400]
    assert np.all(interior > 0.5)
    assert np.all(interior < 2.0)


# ----------------------------------------------------------------------
# Allostatic load
# ----------------------------------------------------------------------

def test_allostatic_load_zero_for_flat_state(engine):
    state = np.ones(100) * 0.5
    assert engine.allostatic_load(state, baseline=0.5) == pytest.approx(0.0)


def test_allostatic_load_positive_for_deviation(engine):
    state = np.concatenate([np.ones(50), np.ones(50) * 2.0])
    load = engine.allostatic_load(state, baseline=1.0)
    assert load > 0


def test_allostatic_load_rejects_2d(engine):
    with pytest.raises(ValueError):
        engine.allostatic_load(np.zeros((3, 3)), baseline=0.0)


def test_allostatic_load_trivial_for_short_state(engine):
    assert engine.allostatic_load(np.array([1.0]), baseline=0.0) == 0.0


# ----------------------------------------------------------------------
# Channel write
# ----------------------------------------------------------------------

def test_write_channels_returns_8_vector(engine, channels):
    state = np.ones(50)
    write = engine.write_channels(state, channels)
    assert write.shape == (8,)


def test_write_channels_respects_baseline(engine, channels):
    state = np.zeros(50)
    write = engine.write_channels(state, channels)
    expected = np.array([c.baseline_methylation for c in channels])
    assert np.allclose(write, expected)


def test_write_channels_respects_tissue_weight(engine, channels):
    state = np.ones(50) * 2.0
    write = engine.write_channels(state, channels)
    for i, channel in enumerate(channels):
        expected = channel.tissue_weight * 2.0 + channel.baseline_methylation
        assert write[i] == pytest.approx(expected)


def test_channel_rejects_invalid_parity_class():
    with pytest.raises(ValueError):
        ChromatinChannel(0, 1.0, 0.0, parity_class=2)


def test_channel_rejects_negative_id():
    with pytest.raises(ValueError):
        ChromatinChannel(-1, 1.0, 0.0, parity_class=0)


# ----------------------------------------------------------------------
# Full pipeline
# ----------------------------------------------------------------------

def test_process_returns_expected_keys(engine, channels):
    sig = EndocrineSignal(
        pulse_times=[0.0, 90.0, 180.0],
        pulse_amplitudes=[1.0, 1.0, 1.0],
    )
    result = engine.process(
        sig, channels,
        lambda_spectrum=[0.1, 0.01],
        amplitudes=[1.0, 1.0],
    )
    expected_keys = {
        "time_minutes", "raw_signal", "integrated_state",
        "baseline", "allostatic_load", "write_vector",
        "n_channels", "mean_integrated_state",
    }
    assert expected_keys.issubset(set(result.keys()))
    assert result["n_channels"] == 8
    assert result["write_vector"].shape == (8,)


def test_process_default_baseline_is_mean(engine, channels):
    sig = EndocrineSignal(
        pulse_times=[0.0, 90.0],
        pulse_amplitudes=[1.0, 1.0],
    )
    result = engine.process(
        sig, channels, lambda_spectrum=[0.1], amplitudes=[1.0],
    )
    assert result["baseline"] == pytest.approx(
        float(np.mean(result["integrated_state"]))
    )
