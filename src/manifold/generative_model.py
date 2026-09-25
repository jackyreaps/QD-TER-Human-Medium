"""
QD-TER Generative Model Module (Axiom G)

Implements the extra modeling assumption required by the local
conditional FEP reduction
(QD-TER_HumanMedium_v9.0/Theory/Reduction_fep.md):

  - observations o
  - hidden states s
  - likelihood p(o | s)
  - prior p(s)
  - recognition density q(s) = N(μ, Σ)
  - identification μ = Ψ_s (slow / kernel coordinate)
  - precisions Π_o, Π_s as curvatures of the quartic potential
  - Laplace-approximated variational free energy F[q]

This is an additional postulate, not a derivation from the published
suite without Axiom G.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional, Tuple

import numpy as np

# Optional tie-in to rheology quantities
try:
    from src.manifold.rheology import BioelectricState, StrategicTopology
except ImportError:  # pragma: no cover
    BioelectricState = None  # type: ignore
    StrategicTopology = None  # type: ignore


# ---------------------------------------------------------------------------
# Topology label (mirrors rheology StrategicTopology when available)
# ---------------------------------------------------------------------------

class TopologyState(str, Enum):
    ABYSS = "Abyss"
    RIDGE = "Ridge"
    VALLEY = "Valley"
    TURBULENT = "Turbulent"


# ---------------------------------------------------------------------------
# Observations and hidden states
# ---------------------------------------------------------------------------

@dataclass
class Observations:
    """
    Measurable channels accessible to the organism.

    endocrine : array-like
        Pulsatile concentrations (e.g. OXTR-linked, CRH, cortisol, ...).
    bioelectric : array-like, shape (3,)
        [resting_potential_deviation_mv, gap_junction_density, ion_channel_expression]
    chromatin : float
        Methylation density ρ_methyl (or scalar proxy).
    """
    endocrine: np.ndarray
    bioelectric: np.ndarray
    chromatin: float

    def as_vector(self) -> np.ndarray:
        return np.concatenate(
            [
                np.asarray(self.endocrine, dtype=float).ravel(),
                np.asarray(self.bioelectric, dtype=float).ravel(),
                [float(self.chromatin)],
            ]
        )

    @classmethod
    def from_bioelectric_state(
        cls,
        endocrine: np.ndarray,
        bioelectric_state: "BioelectricState",
        chromatin: float,
    ) -> "Observations":
        bio = np.array(
            [
                bioelectric_state.resting_potential_deviation_mv,
                bioelectric_state.gap_junction_density,
                bioelectric_state.ion_channel_expression,
            ],
            dtype=float,
        )
        return cls(endocrine=np.asarray(endocrine, dtype=float), bioelectric=bio, chromatin=chromatin)


@dataclass
class HiddenState:
    """
    External causes in the generative model (Axiom G).

    phase : float in [0, 2π)
        Resonance phase relative to the background coherence field.
    scale : float > 0
        Operating scale of the human belt.
    topology : TopologyState
        Strategic landscape label.
    """
    phase: float
    scale: float
    topology: TopologyState

    def as_vector(self) -> np.ndarray:
        # Topology encoded as a simple ordinal for Gaussian machinery
        topo_map = {
            TopologyState.ABYSS: 0.0,
            TopologyState.RIDGE: 1.0,
            TopologyState.VALLEY: 2.0,
            TopologyState.TURBULENT: 3.0,
        }
        return np.array(
            [float(self.phase), float(self.scale), topo_map[self.topology]],
            dtype=float,
        )


# ---------------------------------------------------------------------------
# Precisions from the quartic potential (Axiom G / Der2)
# ---------------------------------------------------------------------------

def natural_precisions(f: float, Psi_A: float, Psi_B: float) -> Tuple[float, float]:
    """
    Π_o = f Ψ_A Ψ_B          (curvature at prior well Ψ=0)
    Π_s = f Ψ_B (Ψ_B − Ψ_A)  (curvature at posterior well Ψ=Ψ_B)
    """
    Pi_o = f * Psi_A * Psi_B
    Pi_s = f * Psi_B * (Psi_B - Psi_A)
    return float(Pi_o), float(Pi_s)


def recognition_gain(Pi_s: float, glue: float) -> float:
    """Γ = Π_s * G  (local reduction gain)."""
    return float(Pi_s * glue)


# ---------------------------------------------------------------------------
# Generative model
# ---------------------------------------------------------------------------

@dataclass
class GenerativeModel:
    """
    p(o, s) = p(o | s) p(s) under Gaussian assumptions (Laplace-ready).

    Parameters
    ----------
    f, Psi_A, Psi_B :
        Reaction / well parameters used for natural precisions.
    glue :
        Cognitive glue G = √(OXTR · GJ).
    eta_prior :
        Prior mean η over the continuous latent vector
        [phase, scale, topology_code]. Default places phase near φ.
    Sigma_o, Sigma_s :
        Observation and prior covariances (diagonal by default).
    """
    f: float = 0.5
    Psi_A: float = 1.0
    Psi_B: float = 0.2
    glue: float = 0.5
    eta_prior: Optional[np.ndarray] = None
    Sigma_o: Optional[np.ndarray] = None
    Sigma_s: Optional[np.ndarray] = None
    phi: float = (1.0 + np.sqrt(5.0)) / 2.0  # golden-ratio phase prior mean

    def __post_init__(self) -> None:
        if self.eta_prior is None:
            # [phase ≈ φ mod 2π handled loosely, scale baseline, topology Ridge]
            self.eta_prior = np.array([self.phi, 1.0, 1.0], dtype=float)
        else:
            self.eta_prior = np.asarray(self.eta_prior, dtype=float)

        d_s = self.eta_prior.shape[0]
        if self.Sigma_s is None:
            self.Sigma_s = np.eye(d_s)
        else:
            self.Sigma_s = np.asarray(self.Sigma_s, dtype=float)

        # Observation dimension is set lazily on first call if needed
        if self.Sigma_o is not None:
            self.Sigma_o = np.asarray(self.Sigma_o, dtype=float)

    # --- precisions & gain -------------------------------------------------

    @property
    def Pi_o_scalar(self) -> float:
        Pi_o, _ = natural_precisions(self.f, self.Psi_A, self.Psi_B)
        return Pi_o

    @property
    def Pi_s_scalar(self) -> float:
        _, Pi_s = natural_precisions(self.f, self.Psi_A, self.Psi_B)
        return Pi_s

    @property
    def Gamma(self) -> float:
        return recognition_gain(self.Pi_s_scalar, self.glue)

    # --- observation function g(s) ----------------------------------------

    def g(self, s: np.ndarray) -> np.ndarray:
        """
        Mean observation map g(s).

        Minimal linear map: first components of s drive endocrine /
        bioelectric / chromatin channels. Override for richer models.
        """
        s = np.asarray(s, dtype=float).ravel()
        # Default: identity-style padding to observation dim 5
        # [endo_0, bio_0, bio_1, bio_2, chrom]
        g_vec = np.zeros(5)
        g_vec[0] = s[0] if s.size > 0 else 0.0          # phase → endocrine proxy
        g_vec[1] = s[1] if s.size > 1 else 0.0          # scale → potential proxy
        g_vec[2] = 0.5                                  # baseline GJ
        g_vec[3] = 1.0                                  # baseline ion channel
        g_vec[4] = s[2] / 3.0 if s.size > 2 else 0.0    # topology → chromatin proxy
        return g_vec

    def g_prime(self, s: np.ndarray) -> np.ndarray:
        """Jacobian ∂g/∂s (finite-diff or analytic for the default g)."""
        s = np.asarray(s, dtype=float).ravel()
        d_s = s.size
        d_o = 5
        J = np.zeros((d_o, d_s))
        if d_s > 0:
            J[0, 0] = 1.0
        if d_s > 1:
            J[1, 1] = 1.0
        if d_s > 2:
            J[4, 2] = 1.0 / 3.0
        return J

    # --- densities (Gaussian) ---------------------------------------------

    def log_prior(self, s: np.ndarray) -> float:
        s = np.asarray(s, dtype=float).ravel()
        eta = self.eta_prior
        diff = s - eta
        # Use precision form
        try:
            Pi_s = np.linalg.inv(self.Sigma_s)
        except np.linalg.LinAlgError:
            Pi_s = np.linalg.pinv(self.Sigma_s)
        return -0.5 * float(diff @ Pi_s @ diff)

    def log_likelihood(self, o: np.ndarray, s: np.ndarray) -> float:
        o = np.asarray(o, dtype=float).ravel()
        pred = self.g(s)
        if self.Sigma_o is None:
            Sigma_o = np.eye(o.size)
        else:
            Sigma_o = self.Sigma_o
            if Sigma_o.shape[0] != o.size:
                Sigma_o = np.eye(o.size)
        diff = o - pred
        try:
            Pi_o = np.linalg.inv(Sigma_o)
        except np.linalg.LinAlgError:
            Pi_o = np.linalg.pinv(Sigma_o)
        return -0.5 * float(diff @ Pi_o @ diff)

    def log_joint(self, o: np.ndarray, s: np.ndarray) -> float:
        return self.log_likelihood(o, s) + self.log_prior(s)


# ---------------------------------------------------------------------------
# Recognition density q(s) = N(μ, Σ)
# ---------------------------------------------------------------------------

@dataclass
class RecognitionDensity:
    """
    q(s) = N(μ, Σ) with μ identified with the QD-TER slow coordinate Ψ_s.
    """
    mu: np.ndarray
    Sigma: np.ndarray

    def __post_init__(self) -> None:
        self.mu = np.asarray(self.mu, dtype=float).ravel()
        self.Sigma = np.asarray(self.Sigma, dtype=float)

    @classmethod
    def from_slow_coordinate(
        cls,
        Psi_s: float,
        dim: int = 1,
        Sigma: Optional[np.ndarray] = None,
    ) -> "RecognitionDensity":
        """
        Axiom G identification: μ = Ψ_s (scalar slow / kernel coefficient).
        For dim > 1, places Ψ_s in the first component.
        """
        mu = np.zeros(dim)
        mu[0] = float(Psi_s)
        if Sigma is None:
            Sigma = np.eye(dim)
        return cls(mu=mu, Sigma=Sigma)

    def log_density(self, s: np.ndarray) -> float:
        s = np.asarray(s, dtype=float).ravel()
        diff = s - self.mu
        try:
            Pi = np.linalg.inv(self.Sigma)
        except np.linalg.LinAlgError:
            Pi = np.linalg.pinv(self.Sigma)
        return -0.5 * float(diff @ Pi @ diff)


# ---------------------------------------------------------------------------
# Laplace free energy
# ---------------------------------------------------------------------------

def laplace_free_energy(
    model: GenerativeModel,
    o: np.ndarray,
    mu: np.ndarray,
    Pi_o: Optional[float] = None,
    Pi_s: Optional[float] = None,
) -> float:
    """
    Scalar Laplace free energy (1-D latent for local RT1):

        F ≈ ½ Π_o (o − g(μ))² + ½ Π_s (μ − η)² + const

    For vector latents, uses the model's Sigma matrices.
    """
    o = np.asarray(o, dtype=float).ravel()
    mu = np.asarray(mu, dtype=float).ravel()

    if mu.size == 1 and (Pi_o is not None or Pi_s is not None):
        # Local RT1 scalar form
        if Pi_o is None:
            Pi_o = model.Pi_o_scalar
        if Pi_s is None:
            Pi_s = model.Pi_s_scalar
        # Use first observation channel vs g(μ)[0] for minimal scalar probe
        g_mu = model.g(mu)
        o0 = o[0] if o.size > 0 else g_mu[0]
        eta0 = float(model.eta_prior[0]) if model.eta_prior.size > 0 else 0.0
        return 0.5 * Pi_o * (o0 - g_mu[0]) ** 2 + 0.5 * Pi_s * (mu[0] - eta0) ** 2

    # Vector form
    return -model.log_joint(o, mu)  # up to entropy terms of q


def recognition_dynamics_rhs(
    mu: np.ndarray,
    o: np.ndarray,
    model: GenerativeModel,
    Pi_o: Optional[float] = None,
    Pi_s: Optional[float] = None,
    Gamma: Optional[float] = None,
) -> np.ndarray:
    """
    Linearized / Laplace recognition dynamics (scalar or vector):

        μ̇ = −Γ [ Π_o (o − g(μ)) g'(μ) + Π_s (μ − η) ]

    For the local 1-D RT1 test, reduces to
        δμ̇ = −Γ (Π_o + Π_s) δμ
    near a fixed point after linearization.
    """
    mu = np.asarray(mu, dtype=float).ravel()
    o = np.asarray(o, dtype=float).ravel()

    if Pi_o is None:
        Pi_o = model.Pi_o_scalar
    if Pi_s is None:
        Pi_s = model.Pi_s_scalar
    if Gamma is None:
        Gamma = model.Gamma

    g_mu = model.g(mu)
    J = model.g_prime(mu)  # (d_o, d_s)

    # Pad / trim observation to match g
    d_o = g_mu.size
    if o.size < d_o:
        o_pad = np.zeros(d_o)
        o_pad[: o.size] = o
        o = o_pad
    else:
        o = o[:d_o]

    pred_err = o - g_mu
    # Likelihood gradient contribution: J^T Π_o pred_err (scalar Π_o here)
    like_grad = J.T @ (Pi_o * pred_err)

    eta = model.eta_prior
    if eta.size != mu.size:
        eta_pad = np.zeros(mu.size)
        eta_pad[: min(eta.size, mu.size)] = eta[: min(eta.size, mu.size)]
        eta = eta_pad

    prior_grad = Pi_s * (mu - eta)
    return -Gamma * (like_grad + prior_grad)


# ---------------------------------------------------------------------------
# Convenience: wire rheology glue into the model
# ---------------------------------------------------------------------------

def model_from_rheology_glue(
    glue: float,
    f: float = 0.5,
   Psi_A: float = 0.2
   Psi_B: float = 1.0
) -> GenerativeModel:
    """Build a GenerativeModel with G taken from rheology.compute_cognitive_glue_index."""
    return GenerativeModel(f=f, Psi_A=Psi_A, Psi_B=Psi_B, glue=float(glue))