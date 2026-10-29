"""
QD-TER EEG Hyperscanning & Source-Reconstruction Layer (v9.0 extension).

DESIGN INVARIANT
----------------
Never touches aether constants. Consumes a plain dictionary of rheology
outputs only. Produces source-space inter-brain coherence that can gate
the scalar phase-lock decision.

IMPORTANT: This is a toy simulator. The lead-field is distance-based,
not a real head model. For real-data analysis, substitute the
forward/inverse operators with MNE-Python or equivalent. The module's
calling interface is designed so that substitution does not require
changes in the caller.

Dependency boundary (v9.0 Section 9.2):
    This module does NOT import from rheology.py. It consumes a plain
    dictionary of rheology outputs. This keeps it usable as a standalone
    analysis tool for any coherence-gating application.

Pipeline:
    rheology_result dict
        -> synthesize 6-source hexad activity (P-V-C for A and B)
        -> forward project to toy sensor montage
        -> source-reconstruct via ridge pseudoinverse
        -> single-trial imaginary coherence (iCOH) per P-V-C pair
        -> field-level phase-lock flag

References:
    v9.0 Part IV, Section 4.6 (the EEG hyperscanning gate).
    Dumas et al. (2010); Sänger et al. (2012) for inter-brain coherence.
    Nolte et al. (2004) for imaginary coherence.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Any, Optional, Tuple, List

import numpy as np
from scipy.signal import csd


# ----------------------------------------------------------------------
# Constants
# ----------------------------------------------------------------------

#: Default sampling rate for the toy simulator, in Hz.
DEFAULT_SFREQ: float = 250.0

#: Default analysis band for iCOH, in Hz. The lower edge is below the
#: slowest default engine frequency (P, 0.2 Hz) so that its power is
#: inside the band.
DEFAULT_BAND: Tuple[float, float] = (0.05, 40.0)

#: Default Welch segment length, in seconds. Five seconds resolves 0.2 Hz
#: and still gives many segments in a two-minute recording.
DEFAULT_SEGMENT_S: float = 5.0

#: Default simulated recording length, in seconds. Slow engines need long
#: recordings: with a 5 s segment, 120 s gives about 47 half-overlapping
#: segments, which keeps the noise floor of the estimator low.
DEFAULT_DURATION_S: float = 120.0

#: Phase lag of the inter-organism coupling, in radians. Real interaction
#: has a delay; a perfectly zero-lag coupling is indistinguishable from
#: volume conduction and is (by design) invisible to imaginary
#: coherence. An eighth of a cycle is an illustrative choice, not a
#: measured value.
DEFAULT_COUPLING_LAG: float = np.pi / 4.0

#: iCOH threshold for the field-level phase-lock flag, calibrated on the
#: simulator itself (see docs/known_issues.md for the operating
#: characteristics). Placeholder for real data: recalibrate against real
#: dyad recordings before using it as a decision boundary.
DEFAULT_ICOH_THRESHOLD: float = 0.30


# ----------------------------------------------------------------------
# Data structures
# ----------------------------------------------------------------------

@dataclass
class SourceSpace:
    """Minimal 6-source hexad: P-V-C for organism A and B.

    The source positions are toy coordinates with arbitrary units. They
    are placed to be distinct so that the distance-based lead-field
    produces a non-degenerate forward model.
    """
    n_sources: int = 6
    labels: List[str] = field(
        default_factory=lambda: [
            "P_A", "V_A", "C_A",
            "P_B", "V_B", "C_B",
        ]
    )
    positions: np.ndarray = field(
        default_factory=lambda: np.array([
            [0.00, 0.00, 0.05],   # P_A
            [0.00, 0.03, 0.00],   # V_A
            [0.00, 0.00, 0.08],   # C_A
            [0.15, 0.00, 0.05],   # P_B
            [0.15, 0.03, 0.00],   # V_B
            [0.15, 0.00, 0.08],   # C_B
        ])
    )

    def __post_init__(self) -> None:
        if self.positions.shape != (self.n_sources, 3):
            raise ValueError(
                f"positions must have shape ({self.n_sources}, 3), "
                f"got {self.positions.shape}."
            )


@dataclass
class SensorMontage:
    """Toy 16-channel montage with a distance-based lead-field.

    The default sensor positions are drawn from a fixed seed so that the
    default montage is reproducible. Not a real head model. Sufficient for simulation-level tests of the
    coherence-gating logic.
    """
    n_channels: int = 16
    positions: np.ndarray = field(
        default_factory=lambda: (
            np.random.default_rng(0).standard_normal((16, 3)) * 0.05
        )
    )
    leadfield: np.ndarray = field(init=False)

    def __post_init__(self) -> None:
        if self.positions.shape != (self.n_channels, 3):
            raise ValueError(
                f"positions must have shape ({self.n_channels}, 3), "
                f"got {self.positions.shape}."
            )
        src = SourceSpace()
        dist = np.linalg.norm(
            self.positions[:, None, :] - src.positions[None, :, :],
            axis=2,
        )
        # Inverse-distance lead-field. Avoids the singularity at zero
        # distance by adding a small constant.
        self.leadfield = 1.0 / (dist + 0.01)


# ----------------------------------------------------------------------
# Oscillator synthesis
# ----------------------------------------------------------------------

def _simulate_phases(
    t: np.ndarray,
    freqs: np.ndarray,
    phase0: np.ndarray,
    coupling: float,
    noise_std: float,
    driver_phase: Optional[np.ndarray] = None,
    lag: float = 0.0,
) -> np.ndarray:
    """Phase-coupled noisy oscillators (Kuramoto-Sakaguchi), vectorized.

    Each oscillator i obeys

        d(phase_i) = [2*pi*f_i + K*sin(driver_i - phase_i - lag)] dt + noise

    The driver must be the *phase* of the driving oscillator, not its
    signal. Passing the signal produces sin(sin(theta) - theta'), which
    is not Kuramoto coupling and does not produce phase-locking.

    Args:
        t: time axis, shape (n_times,).
        freqs: natural frequencies in Hz, shape (n_osc,).
        phase0: initial phases, shape (n_osc,).
        coupling: coupling strength K in rad/s (ignored without a driver).
        noise_std: phase-diffusion strength.
        driver_phase: phases of the driving oscillators, shape
            (n_osc, n_times), or None for autonomous oscillators.
        lag: phase lag of the coupling in radians.

    Returns:
        Phases, shape (n_osc, n_times).
    """
    freqs = np.asarray(freqs, dtype=float)
    n_osc, n = freqs.size, t.size
    dt = t[1] - t[0]
    omega = 2.0 * np.pi * freqs
    kicks = np.random.randn(n_osc, max(n - 1, 0)) * noise_std * np.sqrt(dt)
    phase = np.zeros((n_osc, n))
    phase[:, 0] = phase0
    for i in range(1, n):
        dphi = omega
        if driver_phase is not None:
            dphi = dphi + coupling * np.sin(
                driver_phase[:, i - 1] - phase[:, i - 1] - lag
            )
        phase[:, i] = phase[:, i - 1] + dphi * dt + kicks[:, i - 1]
    return phase


def _coupled_oscillator(
    t: np.ndarray,
    freq: float,
    phase0: float,
    coupling: float,
    noise_std: float,
    driver_phase: Optional[np.ndarray] = None,
    lag: float = 0.0,
) -> Tuple[np.ndarray, np.ndarray]:
    """Single phase-coupled oscillator. Returns (signal, phase)."""
    driver = None if driver_phase is None else np.asarray(driver_phase)[None, :]
    phase = _simulate_phases(
        t, np.array([freq]), np.array([phase0]), coupling, noise_std,
        driver_phase=driver, lag=lag,
    )[0]
    return np.sin(phase), phase


def rheology_coupling(rheology_result: Dict[str, Any]) -> Tuple[float, float]:
    """Map rheology scalars to (coupling strength, phase noise).

    Uses the integration-contract keys (v9.0 Section 9.4). This is the
    single place where the scalar state sets the simulated coupling, so
    that the value reported in the pipeline output is the value used.
    """
    re = float(rheology_result.get("dielectric_reynolds_number", 1.0))
    glue = float(rheology_result.get("cognitive_glue_index", 0.1))
    align = 1.0 - min(
        float(rheology_result.get("chromatin_alignment_delta", 1.0)), 1.0
    )
    bio_align = 1.0 - min(
        float(rheology_result.get("bioelectric_alignment_delta", 20.0))
        / 20.0,
        1.0,
    )
    coupling = float(np.clip(
        0.15 * np.log1p(re) * glue * align * bio_align, 0.0, 0.8,
    ))
    noise = 0.4 / (1.0 + 3.0 * glue)
    if rheology_result.get("bioelectric_decoupled", False):
        coupling *= 0.05
        noise *= 2.5
    return coupling, noise


def generate_source_activity(
    rheology_result: Dict[str, Any],
    duration_s: float = DEFAULT_DURATION_S,
    sfreq: float = DEFAULT_SFREQ,
    base_freqs: Optional[Dict[str, float]] = None,
    coupling_lag: float = DEFAULT_COUPLING_LAG,
) -> Tuple[np.ndarray, np.ndarray]:
    """Synthesize 6-source activity.

    Inter-organism coupling is modulated by the rheology scalars in
    `rheology_result` (see `rheology_coupling`). Organism A is
    autonomous; organism B's oscillators are driven by A's phases with a
    phase lag of `coupling_lag`.

    base_freqs defaults are illustrative. Override with values anchored
    to the engine-frequency table in Part II Section 2 for quantitative
    work. B's natural frequencies are detuned from A's by about 2%.

    Returns:
        (src_a, src_b), each of shape (3, n_times).
    """
    if base_freqs is None:
        base_freqs = {"P": 0.2, "V": 1.0, "C": 10.0}

    n_times = int(duration_s * sfreq)
    t = np.arange(n_times) / sfreq
    coupling, noise = rheology_coupling(rheology_result)

    freqs_a = np.array([base_freqs[k] for k in ("P", "V", "C")], dtype=float)
    phase_a = _simulate_phases(
        t, freqs_a, np.random.rand(3) * 2.0 * np.pi,
        coupling=0.0, noise_std=noise,
    )
    freqs_b = freqs_a * (1.0 + 0.02 * np.random.randn(3))
    phase_b = _simulate_phases(
        t, freqs_b, np.random.rand(3) * 2.0 * np.pi,
        coupling=coupling, noise_std=noise,
        driver_phase=phase_a, lag=coupling_lag,
    )
    return np.sin(phase_a), np.sin(phase_b)


# ----------------------------------------------------------------------
# Forward and inverse operators
# ----------------------------------------------------------------------

def forward_project(
    sources: np.ndarray,
    montage: SensorMontage,
    noise_std: float = 0.05,
) -> np.ndarray:
    """Project sources to sensor space.

    Args:
        sources: (n_sources, n_times)
        montage: SensorMontage with a lead-field.
        noise_std: Additive white noise standard deviation.

    Returns:
        (n_channels, n_times)
    """
    data = montage.leadfield @ sources
    data = data + np.random.randn(*data.shape) * noise_std
    return data


def source_reconstruct(
    sensor_data: np.ndarray,
    montage: SensorMontage,
    ridge: float = 1e-3,
) -> np.ndarray:
    """Ridge-regularized pseudoinverse reconstruction.

    Args:
        sensor_data: (n_channels, n_times)
        montage: SensorMontage with a lead-field.
        ridge: Tikhonov regularization parameter.

    Returns:
        (n_sources, n_times)
    """
    G = montage.leadfield
    GtG = G.T @ G + ridge * np.eye(G.shape[1])
    inv = np.linalg.solve(GtG, G.T)
    return inv @ sensor_data


# ----------------------------------------------------------------------
# Imaginary coherence
# ----------------------------------------------------------------------

def imaginary_coherence(
    x: np.ndarray,
    y: np.ndarray,
    fs: float = DEFAULT_SFREQ,
    band: Tuple[float, float] = DEFAULT_BAND,
    nperseg: Optional[int] = None,
) -> float:
    """Band-integrated imaginary coherence (iCOH).

    With Welch cross- and auto-spectra S_xy, S_xx, S_yy, the coherency is
    C = S_xy / sqrt(S_xx * S_yy), and its imaginary part is zero for
    zero-lag interactions (Nolte et al. 2004). This function integrates
    over the analysis band before taking the imaginary part:

        iCOH = | sum_f Im S_xy(f) | / sqrt( sum_f S_xx(f) * sum_f S_yy(f) )

    For a single dominant frequency this equals |Im C(f)|. Integrating
    first weights each frequency by its power, so empty bins do not
    dilute the estimate, and the signed sum suppresses the chance
    coherence of unrelated signals (a per-bin average of |Im C| has a
    large positive floor).

    Volume conduction produces zero-lag coherence, which is purely real
    in the cross-spectrum, so it contributes no imaginary part. A
    consequence is that genuine zero-lag locking is also invisible.

    Args:
        x, y: 1-D time series of equal length.
        fs: Sampling rate in Hz.
        band: (low, high) analysis band in Hz.
        nperseg: Welch segment length in samples. Defaults to
            DEFAULT_SEGMENT_S seconds (capped at the signal length).

    Returns:
        Scalar iCOH in [0, 1].
    """
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    if x.shape != y.shape:
        raise ValueError("x and y must have the same shape.")
    if x.ndim != 1:
        raise ValueError("x and y must be one-dimensional.")
    if len(x) < 4:
        return 0.0

    if nperseg is None:
        nperseg = int(DEFAULT_SEGMENT_S * fs)
    nperseg = min(nperseg, len(x))

    f, Sxy = csd(x, y, fs=fs, nperseg=nperseg)
    _, Sxx = csd(x, x, fs=fs, nperseg=nperseg)
    _, Syy = csd(y, y, fs=fs, nperseg=nperseg)
    mask = (f >= band[0]) & (f <= band[1])
    if not mask.any():
        return 0.0

    num = np.abs(np.sum(np.imag(Sxy[mask])))
    den = np.sqrt(np.sum(np.abs(Sxx[mask])) * np.sum(np.abs(Syy[mask])))
    return float(min(num / (den + 1e-12), 1.0))


def inter_brain_icoh(
    src_a: np.ndarray,
    src_b: np.ndarray,
    fs: float = DEFAULT_SFREQ,
    band: Tuple[float, float] = DEFAULT_BAND,
) -> Dict[str, float]:
    """iCOH for the three corresponding P-V-C pairs plus the mean.

    Args:
        src_a, src_b: (3, n_times) arrays for the P-V-C sources of each
            organism.
        fs: Sampling rate.
        band: Analysis band.

    Returns:
        Dictionary with keys "P", "V", "C", "mean".
    """
    if src_a.shape != src_b.shape or src_a.shape[0] != 3:
        raise ValueError(
            "src_a and src_b must both have shape (3, n_times)."
        )

    pairs = {"P": (0, 0), "V": (1, 1), "C": (2, 2)}
    scores: Dict[str, float] = {}
    for name, (i, j) in pairs.items():
        scores[name] = imaginary_coherence(
            src_a[i], src_b[j], fs=fs, band=band,
        )
    scores["mean"] = float(np.mean(list(scores.values())))
    return scores


# ----------------------------------------------------------------------
# Full pipeline
# ----------------------------------------------------------------------

def compute_hyperscan_phase_lock(
    rheology_result: Dict[str, Any],
    montage: Optional[SensorMontage] = None,
    icoh_threshold: float = DEFAULT_ICOH_THRESHOLD,
    use_reconstruction: bool = True,
    sfreq: float = DEFAULT_SFREQ,
    duration_s: float = DEFAULT_DURATION_S,
) -> Dict[str, Any]:
    """Full pipeline: synthesize -> forward -> reconstruct -> iCOH.

    Args:
        rheology_result: Dictionary of rheology outputs. Required keys
            per the integration contract (v9.0 Section 9.4):
            dielectric_reynolds_number, cognitive_glue_index,
            chromatin_alignment_delta, bioelectric_alignment_delta,
            bioelectric_decoupled.
        montage: SensorMontage. Constructed with defaults if not given.
        icoh_threshold: Threshold for the field-level phase-lock flag.
            Calibrated on the simulator; recalibrate on real dyad data.
        use_reconstruction: If True, run forward + inverse. If False,
            compute iCOH on source signals directly.
        sfreq: Sampling rate.
        duration_s: Simulated duration in seconds.

    Returns:
        Dictionary with keys:
            icoh (dict), icoh_mean, icoh_threshold, field_phase_locked,
            coupling_used.
    """
    if montage is None:
        montage = SensorMontage()

    src_a, src_b = generate_source_activity(
        rheology_result, duration_s=duration_s, sfreq=sfreq,
    )

    if use_reconstruction:
        sources = np.vstack([src_a, src_b])
        sensors = forward_project(sources, montage)
        recon = source_reconstruct(sensors, montage)
        src_a_hat = recon[:3]
        src_b_hat = recon[3:]
    else:
        src_a_hat, src_b_hat = src_a, src_b

    icoh = inter_brain_icoh(src_a_hat, src_b_hat, fs=sfreq)

    return {
        "icoh": icoh,
        "icoh_mean": icoh["mean"],
        "icoh_threshold": float(icoh_threshold),
        "field_phase_locked": bool(icoh["mean"] >= icoh_threshold),
        "coupling_used": rheology_coupling(rheology_result)[0],
    }
