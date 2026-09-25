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

#: Default analysis band for iCOH, in Hz.
DEFAULT_BAND: Tuple[float, float] = (0.5, 40.0)

#: Placeholder iCOH threshold. Calibrate against real dyad data before
#: using as a decision boundary.
DEFAULT_ICOH_THRESHOLD: float = 0.18


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

    Not a real head model. Sufficient for simulation-level tests of the
    coherence-gating logic.
    """
    n_channels: int = 16
    positions: np.ndarray = field(
        default_factory=lambda: np.random.randn(16, 3) * 0.05
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

def _coupled_oscillator(
    t: np.ndarray,
    freq: float,
    phase0: float,
    coupling: float,
    noise_std: float,
    driver_phase: Optional[np.ndarray] = None,
) -> Tuple[np.ndarray, np.ndarray]:
    """Phase-coupled oscillator. Returns (signal, phase).

    The driver must be the *phase* of the driving oscillator, not its
    signal. Passing the signal produces sin(sin(theta) - theta'), which
    is not Kuramoto coupling and does not produce phase-locking.
    """
    dt = t[1] - t[0]
    phase = np.zeros_like(t)
    phase[0] = phase0
    for i in range(1, len(t)):
        dphi = 2.0 * np.pi * freq
        if driver_phase is not None:
            dphi += coupling * np.sin(
                driver_phase[i - 1] - phase[i - 1]
            )
        phase[i] = (
            phase[i - 1]
            + dphi * dt
            + np.random.randn() * noise_std * np.sqrt(dt)
        )
    return np.sin(phase), phase


def generate_source_activity(
    rheology_result: Dict[str, Any],
    duration_s: float = 8.0,
    sfreq: float = DEFAULT_SFREQ,
    base_freqs: Optional[Dict[str, float]] = None,
) -> Tuple[np.ndarray, np.ndarray]:
    """Synthesize 6-source activity.

    Inter-organism coupling is modulated by the rheology scalars in
    `rheology_result`. The relevant keys are those specified in the
    integration contract (v9.0 Section 9.4).

    base_freqs defaults are illustrative. Override with values anchored
    to the engine-frequency table in Part II Section 2 for quantitative
    work.

    Returns:
        (src_a, src_b), each of shape (3, n_times).
    """
    if base_freqs is None:
        base_freqs = {"P": 0.2, "V": 1.0, "C": 10.0}

    n_times = int(duration_s * sfreq)
    t = np.arange(n_times) / sfreq

    re = float(rheology_result.get("dielectric_reynolds_number", 1.0))
    glue = float(rheology_result.get("cognitive_glue_index", 0.1))
    align = 1.0 - min(
        float(rheology_result.get("chromatin_alignment_delta", 1.0)), 1.0
    )
    bio_align = 1.0 - min(
        float(rheology_result.get(
            "bioelectric_alignment_delta", 20.0
        )) / 20.0,
        1.0,
    )

    coupling = float(np.clip(
        0.15 * np.log1p(re) * glue * align * bio_align,
        0.0, 0.8,
    ))
    noise = 0.4 / (1.0 + 3.0 * glue)

    if rheology_result.get("bioelectric_decoupled", False):
        coupling *= 0.05
        noise *= 2.5

    # A side: autonomous.
    src_a_signals: List[np.ndarray] = []
    src_a_phases: List[np.ndarray] = []
    for key in ("P", "V", "C"):
        sig, ph = _coupled_oscillator(
            t,
            base_freqs[key],
            np.random.rand() * 2.0 * np.pi,
            coupling=0.0,
            noise_std=noise,
        )
        src_a_signals.append(sig)
        src_a_phases.append(ph)

    # B side: driven by A's phase.
    src_b_signals: List[np.ndarray] = []
    for i, key in enumerate(("P", "V", "C")):
        sig, _ = _coupled_oscillator(
            t,
            base_freqs[key] * (1.0 + 0.02 * np.random.randn()),
            np.random.rand() * 2.0 * np.pi,
            coupling=coupling,
            noise_std=noise,
            driver_phase=src_a_phases[i],
        )
        src_b_signals.append(sig)

    return (
        np.stack(src_a_signals, axis=0),
        np.stack(src_b_signals, axis=0),
    )


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
    """Single-trial imaginary coherence (iCOH).

        iCOH(f) = |Im(S_xy(f))| / |S_xy(f)|

    Averaged over the analysis band. Because volume conduction produces
    zero-lag coherence, which is purely real in the cross-spectrum,
    taking the imaginary part suppresses it (Nolte et al. 2004).

    Args:
        x, y: 1-D time series of equal length.
        fs: Sampling rate in Hz.
        band: (low, high) analysis band in Hz.
        nperseg: Welch segment length. Defaults to int(fs).

    Returns:
        Scalar iCOH averaged over the band.
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
        nperseg = int(fs)
    nperseg = min(nperseg, len(x))

    f, Sxy = csd(x, y, fs=fs, nperseg=nperseg)
    mask = (f >= band[0]) & (f <= band[1])
    Sxy = Sxy[mask]
    if Sxy.size == 0:
        return 0.0

    num = np.abs(np.imag(Sxy))
    den = np.abs(Sxy) + 1e-12
    return float(np.mean(num / den))


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
    duration_s: float = 8.0,
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
            Placeholder value; calibrate against real dyad data.
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
        "coupling_used": float(np.clip(
            0.15 * np.log1p(
                float(rheology_result.get(
                    "dielectric_reynolds_number", 1.0
                ))
            ),
            0.0, 0.8,
        )),
    }
