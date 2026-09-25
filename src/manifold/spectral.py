"""
QD-TER Spectral Module

Combinatorial Laplacian on the seven-engine phase-lock hierarchy.
Supports the local conditional FEP reduction
(QD-TER_HumanMedium_v9.0/Theory/Reduction_fep.md, Axiom S).

Design notes
------------
- Uses an *undirected* edge expansion of the hierarchy so that
  L = D - A is symmetric PSD with a 1-D kernel (global sync = constants).
- kappa scales all edge weights → λ₂ scales linearly with kappa.
- endocrinal_norm enters only through positive weight factors (abs).
"""

from __future__ import annotations

import numpy as np
from typing import Any, Dict, Optional, Tuple


class HypergraphSpectral:
    """
    Combinatorial Laplacian on:

        VII → I → (II, III) → (IV, V) → VI

    with executive feedback VI → I.
    """

    ENGINE_NAMES = ("VII", "I", "II", "III", "IV", "V", "VI")

    # Undirected edges expanded from the directed hierarchy (node indices)
    # VII=0, I=1, II=2, III=3, IV=4, V=5, VI=6
    EDGES = (
        (0, 1),           # VII — I
        (1, 2), (1, 3),   # I — (II, III)
        (2, 4), (2, 5),   # II — (IV, V)
        (3, 4), (3, 5),   # III — (IV, V)
        (4, 6), (5, 6),   # (IV, V) — VI
        (6, 1),           # VI — I (feedback)
    )

    def __init__(self) -> None:
        self.n_nodes = 7
        self.n_edges = len(self.EDGES)
        # Incidence retained for documentation / extensions
        self.H = np.array(
            [
                [-1,  0,  0,  0,  0],
                [ 0,  1,  0,  0,  1],
                [ 0, -1,  1,  0,  0],
                [ 0, -1,  1,  0,  0],
                [ 0,  0, -1,  1,  0],
                [ 0,  0, -1,  1,  0],
                [ 0,  0,  0, -1, -1],
            ],
            dtype=float,
        )

    def build_laplacian(
        self,
        kappa: float = 1.0,
        baseline_weights: Optional[np.ndarray] = None,
        endocrinal_norm: float = 0.0,
        eta: Optional[np.ndarray] = None,
    ) -> np.ndarray:
        """
        Combinatorial Laplacian L = D - A.

        w_e = kappa * w_e0 * (1 + eta_e * |M_E|)
        All weights stay non-negative → L is PSD, ker = span{1} when connected.
        """
        if kappa <= 0:
            raise ValueError("kappa must be positive")
        if baseline_weights is None:
            baseline_weights = np.ones(self.n_edges)
        else:
            baseline_weights = np.asarray(baseline_weights, dtype=float)
            if baseline_weights.shape != (self.n_edges,):
                raise ValueError(f"baseline_weights shape must be ({self.n_edges},)")
        if eta is None:
            eta = 0.1 * np.ones(self.n_edges)
        else:
            eta = np.asarray(eta, dtype=float)
            if eta.shape != (self.n_edges,):
                raise ValueError(f"eta shape must be ({self.n_edges},)")

        w = kappa * baseline_weights * (1.0 + eta * abs(float(endocrinal_norm)))
        if np.any(w < 0):
            raise ValueError("edge weights must be non-negative")

        A = np.zeros((self.n_nodes, self.n_nodes), dtype=float)
        for e, (i, j) in enumerate(self.EDGES):
            A[i, j] += w[e]
            A[j, i] += w[e]

        deg = A.sum(axis=1)
        L = np.diag(deg) - A
        # numerical symmetry
        return 0.5 * (L + L.T)

    def spectrum(
        self,
        kappa: float = 1.0,
        endocrinal_norm: float = 0.0,
        baseline_weights: Optional[np.ndarray] = None,
        eta: Optional[np.ndarray] = None,
    ) -> Dict[str, Any]:
        L = self.build_laplacian(
            kappa=kappa,
            baseline_weights=baseline_weights,
            endocrinal_norm=endocrinal_norm,
            eta=eta,
        )
        eigvals, eigvecs = np.linalg.eigh(L)
        if abs(eigvals[0]) < 1e-12:
            eigvals = eigvals.copy()
            eigvals[0] = 0.0
        return {
            "eigenvalues": eigvals,
            "eigenvectors": eigvecs,
            "lambda_1": float(eigvals[0]),
            "lambda_2": float(eigvals[1]) if len(eigvals) > 1 else float("nan"),
            "spectral_gap": float(eigvals[1]) if len(eigvals) > 1 else float("nan"),
            "L": L,
        }

    def exact_kernel_projector(
        self,
        kappa: float = 1.0,
        endocrinal_norm: float = 0.0,
        tol: float = 1e-8,
        baseline_weights: Optional[np.ndarray] = None,
        eta: Optional[np.ndarray] = None,
    ) -> Tuple[np.ndarray, np.ndarray]:
        """(Pi_kernel, V_kernel) for eigenvalues <= tol. Rank 1 when connected."""
        spec = self.spectrum(
            kappa=kappa,
            endocrinal_norm=endocrinal_norm,
            baseline_weights=baseline_weights,
            eta=eta,
        )
        mask = spec["eigenvalues"] <= tol
        if not np.any(mask):
            mask = np.zeros_like(spec["eigenvalues"], dtype=bool)
            mask[0] = True
        V_kernel = spec["eigenvectors"][:, mask]
        if V_kernel.shape[1] == 1 and np.sum(V_kernel) < 0:
            V_kernel = -V_kernel
        return V_kernel @ V_kernel.T, V_kernel

    def slow_subspace(
        self,
        gap_threshold: float,
        kappa: float = 1.0,
        endocrinal_norm: float = 0.0,
        baseline_weights: Optional[np.ndarray] = None,
        eta: Optional[np.ndarray] = None,
    ) -> Tuple[np.ndarray, np.ndarray, int]:
        spec = self.spectrum(
            kappa=kappa,
            endocrinal_norm=endocrinal_norm,
            baseline_weights=baseline_weights,
            eta=eta,
        )
        mask = spec["eigenvalues"] <= gap_threshold
        V_slow = spec["eigenvectors"][:, mask]
        return V_slow @ V_slow.T, V_slow, int(np.sum(mask))

    def slow_projector(
        self,
        gap_threshold: Optional[float] = None,
        kappa: float = 1.0,
        endocrinal_norm: float = 0.0,
        baseline_weights: Optional[np.ndarray] = None,
        eta: Optional[np.ndarray] = None,
    ) -> Tuple[np.ndarray, np.ndarray]:
        if gap_threshold is None:
            lam2 = self.spectrum(kappa=kappa, endocrinal_norm=endocrinal_norm)["lambda_2"]
            gap_threshold = 1.5 * lam2 if lam2 > 0 else 1.0
        Pi_s, V_slow, _ = self.slow_subspace(
            gap_threshold, kappa, endocrinal_norm, baseline_weights, eta
        )
        return Pi_s, V_slow


def kernel_coefficient(Psi: np.ndarray, v_sync: np.ndarray) -> float:
    """c = v_sync · Psi (v_sync should be unit-norm)."""
    Psi = np.asarray(Psi, dtype=float).ravel()
    v_sync = np.asarray(v_sync, dtype=float).ravel()
    if Psi.shape != v_sync.shape:
        raise ValueError("Psi and v_sync must have the same shape")
    return float(v_sync @ Psi)


def sync_mean(Psi: np.ndarray) -> float:
    """Slow coordinate for constant kernel: spatial mean of components."""
    return float(np.mean(np.asarray(Psi, dtype=float)))