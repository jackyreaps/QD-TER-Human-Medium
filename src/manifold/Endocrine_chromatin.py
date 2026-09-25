"""
QD-TER Endocrine-Chromatin Writing Pipeline (v9.0 extension).

DESIGN INVARIANT
----------------
The channel count (8) is INHERITED from the physics suite's residual V_4
action on the 36-mode waist. It is NOT derived here. This module takes
the channel count as a required parameter and does not attempt to
re-derive it from chromatin, histones, or phase-space reconstruction.
See Theory/Residual_integer_8.md.

DEPENDENCY BOUNDARY
-------------------
This module does NOT import from rheology.py. It operates on plain numpy
arrays and dataclasses so it can be reused by other layers of the suite
(biology technical notes, morphogenetic coupling work) without pulling
the rheology layer as a dependency.

Pipeline:
    endocrine pulse train x(t)
        -> Takens delay-coordinate embedding  (phase-space reconstruction)
        -> Jacobian eigenvalue classification  (dynamical regime)
        -> multi-timescale leaky-kernel integration  (chromatin state)
        -> 8-channel write vector  (addressing onto chromatin)

References:
    v9.0 Part IV, Sections 1-3 (endocrine signal, chromatin writing,
    phase-space and leaky kernel).
    Lightman & Conway-Campbell (2010); Stavreva et al. (2009);
    Takens (1981); McEwen (1998).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple

import numpy as np


# ----------------------------------------------------------------------
# Constants
# ----------------------------------------------------------------------

#: Number of residual writing channels, inherited from the physics suite.
#: See Theory/Residual_integer_8.md.
DEFAULT_N_CHANNELS: int = 8

#: Physiological ultradian step in minutes (Lightman, Veldhuis).
DEFAULT_ULTRADIAN_STEP_MIN: float = 90.0

#: Numerical tolerance for eigenvalue classification.
_EIG_TOL: float = 1e-9


# ----------------------------------------------------------------------
# Data structures
# ----------------------------------------------------------------------

@dataclass
class EndocrineSignal:
    """Discrete endocrine pulse train.

    Attributes:
        pulse_times: Time of each pulse, in minutes from an arbitrary epoch.
        pulse_amplitudes: Hormone concentration at each pulse.
        ultradian_step: Nominal inter-pulse interval, in minutes.
    """
    pulse_times: List[float]
    pulse_amplitudes: List[float]
    ultradian_step: float = DEFAULT_ULTRADIAN_STEP_MIN

    def __post_init__(self) -> None:
        if len(self.pulse_times) != len(self.pulse_amplitudes):
            raise ValueError(
                "pulse_times and pulse_amplitudes must have equal length."
            )

    def to_series(
        self,
        duration_min: Optional[float] = None,
        dt_min: float = 1.0,
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Resample the pulse train onto a uniform time grid.

        Each pulse is represented as a narrow Gaussian bump of width
        `ultradian_step / 10`, evaluated on the uniform grid. This models
        the deconvolution-style representation used by Veldhuis, where
        each secretory event contributes a brief concentration transient.

        Returns:
            (t, x) where t is the grid in minutes and x is the sampled
            concentration.
        """
        if duration_min is None:
            if not self.pulse_times:
                raise ValueError("Cannot infer duration from an empty signal.")
            duration_min = max(self.pulse_times) + self.ultradian_step

        n = int(np.ceil(duration_min / dt_min)) + 1
        t = np.arange(n) * dt_min
        x = np.zeros(n)

        width = max(self.ultradian_step / 10.0, dt_min)
        for tp, ap in zip(self.pulse_times, self.pulse_amplitudes):
            x += ap * np.exp(-0.5 * ((t - tp) / width) ** 2)

        return t, x


@dataclass
class ChromatinChannel:
    """One of the 8 residual writing channels.

    Attributes:
        channel_id: Index in [0, n_channels).
        tissue_weight: Tissue-specific multiplier for the write magnitude.
        baseline_methylation: Baseline methylation level at this channel.
        parity_class: Parity label from sigma_parity, 0 or 1.
    """
    channel_id: int
    tissue_weight: float
    baseline_methylation: float
    parity_class: int = 0

    def __post_init__(self) -> None:
        if self.parity_class not in (0, 1):
            raise ValueError("parity_class must be 0 or 1.")
        if self.channel_id < 0:
            raise ValueError("channel_id must be non-negative.")


# ----------------------------------------------------------------------
# Engine
# ----------------------------------------------------------------------

class EndocrineChromatinEngine:
    """Endocrine-to-chromatin writing pipeline.

    The engine takes an endocrine pulse train and produces a write vector
    across the inherited 8-channel space. It does not derive the channel
    count; that is a required constructor parameter.

    Args:
        n_channels: Number of residual writing channels. Default 8,
            inherited from the physics suite. Override only if reusing
            the engine at a different scale with an explicit derivation.
        temporal_resolution: Sampling step in minutes for internal grids.
    """

    def __init__(
        self,
        n_channels: int = DEFAULT_N_CHANNELS,
        temporal_resolution: float = 1.0,
    ) -> None:
        if n_channels < 1:
            raise ValueError("n_channels must be at least 1.")
        if temporal_resolution <= 0:
            raise ValueError("temporal_resolution must be positive.")
        self.n_channels = n_channels
        self.dt = temporal_resolution

    # ------------------------------------------------------------------
    # Phase-space reconstruction (v9.0 Section 3.1)
    # ------------------------------------------------------------------

    def takens_embed(
        self,
        signal: np.ndarray,
        dim: int,
        tau: int,
    ) -> np.ndarray:
        """Delay-coordinate embedding (Takens 1981).

        Args:
            signal: 1-D time series.
            dim: Embedding dimension d. Must satisfy d > 2n for n active
                degrees of freedom for a true embedding. This is a caller
                responsibility; the method does not enforce it.
            tau: Delay in samples. Must be >= 1.

        Returns:
            Array of shape (n_points, dim), where each row is
            (x(t), x(t+tau), ..., x(t+(dim-1)tau)).
        """
        signal = np.asarray(signal, dtype=float)
        if signal.ndim != 1:
            raise ValueError("signal must be one-dimensional.")
        if dim < 1:
            raise ValueError("dim must be at least 1.")
        if tau < 1:
            raise ValueError("tau must be at least 1.")

        n = len(signal) - (dim - 1) * tau
        if n <= 0:
            raise ValueError(
                f"Signal of length {len(signal)} is too short for "
                f"dim={dim} and tau={tau}. Need at least "
                f"{(dim - 1) * tau + 1} samples."
            )

        return np.stack(
            [signal[i * tau: i * tau + n] for i in range(dim)],
            axis=1,
        )

    # ------------------------------------------------------------------
    # Dynamical regime classification (v9.0 Section 3.2)
    # ------------------------------------------------------------------

    def classify_regime(self, jacobian: np.ndarray) -> str:
        """Classify the local dynamical regime from Jacobian eigenvalues.

        Returns one of:
            STABLE_NODE, STABLE_FOCUS, UNSTABLE_NODE, UNSTABLE_FOCUS,
            SADDLE, BIFURCATION, UNDETERMINED.
        """
        J = np.asarray(jacobian, dtype=float)
        if J.ndim != 2 or J.shape[0] != J.shape[1]:
            raise ValueError("jacobian must be a square 2-D array.")

        eigenvalues = np.linalg.eigvals(J)
        real_parts = eigenvalues.real
        imag_parts = eigenvalues.imag

        # Marginal case: any eigenvalue on the imaginary axis.
        if np.any(np.abs(real_parts) < _EIG_TOL):
            return "BIFURCATION"

        has_imaginary = not np.allclose(imag_parts, 0.0, atol=_EIG_TOL)
        all_negative = bool(np.all(real_parts < 0))
        all_positive = bool(np.all(real_parts > 0))

        if all_negative:
            return "STABLE_FOCUS" if has_imaginary else "STABLE_NODE"
        if all_positive:
            return "UNSTABLE_FOCUS" if has_imaginary else "UNSTABLE_NODE"

        # Mixed real parts: saddle.
        if np.any(real_parts > 0) and np.any(real_parts < 0):
            return "SADDLE"

        return "UNDETERMINED"

    # ------------------------------------------------------------------
    # Leaky-kernel integration (v9.0 Section 3.3)
    # ------------------------------------------------------------------

    def leaky_integrate(
        self,
        signal: np.ndarray,
        lambda_spectrum: List[float],
        amplitudes: List[float],
    ) -> np.ndarray:
        """Integrate the endocrine signal through a multi-timescale kernel.

        The chromatin state is modeled as a sum of leaky integrators:

            X(t) = sum_k A_k * (signal * exp(-lambda_k * t)) (convolved)

        Args:
            signal: 1-D input time series.
            lambda_spectrum: Recovery rates, in inverse time units.
                Must be positive.
            amplitudes: Weight of each exponential mode.

        Returns:
            Array of the same length as `signal`.
        """
        signal = np.asarray(signal, dtype=float)
        if signal.ndim != 1:
            raise ValueError("signal must be one-dimensional.")
        if len(lambda_spectrum) != len(amplitudes):
            raise ValueError("lambda_spectrum and amplitudes must align.")
        if len(lambda_spectrum) == 0:
            raise ValueError("lambda_spectrum must be non-empty.")
        if any(lam <= 0 for lam in lambda_spectrum):
            raise ValueError("All lambda values must be strictly positive.")

        n = len(signal)
        t = np.arange(n) * self.dt
        state = np.zeros(n)

        for lam, amp in zip(lambda_spectrum, amplitudes):
            kernel = amp * np.exp(-lam * t)
            # Normalize by integral of the kernel over the grid so that
            # a constant unit input produces a bounded, calibration-stable
            # output.
            norm = float(np.sum(kernel)) * self.dt
            if norm <= 0:
                continue
            state += np.convolve(signal, kernel, mode="same") * self.dt / norm

        return state

    # ------------------------------------------------------------------
    # Allostatic load (v9.0 Section 3.4)
    # ------------------------------------------------------------------

    def allostatic_load(
        self,
        state: np.ndarray,
        baseline: float,
    ) -> float:
        """Integrated un-cleared residue (McEwen 1998).

            Lambda_allo = integral |X(t) - X_baseline| dt
        """
        state = np.asarray(state, dtype=float)
        if state.ndim != 1:
            raise ValueError("state must be one-dimensional.")
        if len(state) < 2:
            return 0.0

        deviation = np.abs(state - float(baseline))
        # Manual trapezoid integration: avoids numpy version differences
        # between np.trapz (legacy) and np.trapezoid (numpy >= 2.0).
        return float(
            0.5 * self.dt * (deviation[0] + deviation[-1])
            + self.dt * float(np.sum(deviation[1:-1]))
        )

    # ------------------------------------------------------------------
    # Channel write (v9.0 Section 2.3)
    # ------------------------------------------------------------------

    def write_channels(
        self,
        integrated_state: np.ndarray,
        channels: List[ChromatinChannel],
    ) -> np.ndarray:
        """Project the integrated chromatin state onto the 8 channels.

        The write at each channel is:

            write[i] = tissue_weight[i] * mean(integrated_state)
                       + baseline_methylation[i]

        This is the current (linear) addressing model. A nonlinear
        addressing rule would be a different model, not a refinement.
        """
        if len(channels) != self.n_channels:
            raise ValueError(
                f"Expected {self.n_channels} channels, got {len(channels)}."
            )
        integrated_state = np.asarray(integrated_state, dtype=float)
        if integrated_state.ndim != 1:
            raise ValueError("integrated_state must be one-dimensional.")
        if len(integrated_state) == 0:
            raise ValueError("integrated_state must be non-empty.")

        mean_state = float(np.mean(integrated_state))
        write_vector = np.zeros(self.n_channels)
        for i, channel in enumerate(channels):
            write_vector[i] = (
                channel.tissue_weight * mean_state
                + channel.baseline_methylation
            )
        return write_vector

    # ------------------------------------------------------------------
    # Convenience: full pipeline
    # ------------------------------------------------------------------

    def process(
        self,
        signal: EndocrineSignal,
        channels: List[ChromatinChannel],
        lambda_spectrum: List[float],
        amplitudes: List[float],
        baseline: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Run the full pipeline and return a result dictionary.

        The dictionary keys are the integration contract for downstream
        consumers. See v9.0 Section 9.4.
        """
        t, x = signal.to_series(dt_min=self.dt)
        integrated = self.leaky_integrate(x, lambda_spectrum, amplitudes)

        if baseline is None:
            baseline = float(np.mean(integrated))

        load = self.allostatic_load(integrated, baseline)
        write = self.write_channels(integrated, channels)

        return {
            "time_minutes": t,
            "raw_signal": x,
            "integrated_state": integrated,
            "baseline": float(baseline),
            "allostatic_load": float(load),
            "write_vector": write,
            "n_channels": self.n_channels,
            "mean_integrated_state": float(np.mean(integrated)),
        }
