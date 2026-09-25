"""
QD-TER Spectral Module

Constructs the normalized hypergraph Laplacian from the seven-engine
phase-lock hierarchy and provides:

  - spectrum (eigenvalues / eigenvectors)
  - exact kernel projector (global synchronization mode)
  - slow-subspace projector
  - gap control via a scalar kappa

This module supports the local conditional FEP reduction
(QD-TER_HumanMedium_v9.0/Theory/Reduction_fep.md, Axiom S).

It does not derive the aether or the residual 8-channel sector.
"""

from __future__ import annotations

import numpy as np
from typing import Any, Dict, Optional, Tuple


class HypergraphSpectral:
    """
    Normalized hypergraph Laplacian on the seven-engine hierarchy:

        VII → I → (II, III) → (IV, V) → VI

    with executive feedback VI → I so the graph is strongly connected
    and the kernel is one-dimensional (global sync mode).

    Parameters that control the gap
    --------------------------------
    kappa : float
        Scales baseline edge weights. Larger kappa → larger λ₂.
    endocrinal_norm : float
        |M_E|_F (typically identified with the cognitive glue G).
    eta : array-like, shape (n_edges,)
        Per-edge endocrine coupling strengths.
    """

    # Engine order: VII, I, II, III, IV, V, VI
    ENGINE_NAMES = ("VII", "I", "II", "III", "IV", "V", "VI")

    def __init__(self) -> None:
        # Incidence matrix H ∈ R^{7×5}
        # rows = engines, cols = directed hyperedges e1..e5
        #   e1: {VII} → {I}
        #   e2: {I}   → {II, III}
        #   e3: {II, III} → {IV, V}
        #   e4: {IV, V} → {VI}
        #   e5: {VI}  → {I}   (executive feedback)
        self.H = np.array(
            [
                [-1,  0,  0,  0,  0],  # VII
                [ 0,  1,  0,  0,  1],  # I
                [ 0, -1,  1,  0,  0],  # II
                [ 0, -1,  1,  0,  0],  # III
                [ 0,  0, -1,  1,  0],  # IV
                [ 0,  0, -1,  1,  0],  # V
                [ 0,  0,  0, -1, -1],  # VI
            ],
            dtype=float,
        )
        self.n_nodes = self.H.shape[0]
        self.n_edges = self.H.shape[1]

    # ------------------------------------------------------------------
    # Degree matrices
    # ------------------------------------------------------------------

    def _degree_matrices(self) -> Tuple[np.ndarray, np.ndarray]:
        deg_v = np.diag(np.sum(np.abs(self.H), axis=1))
        deg_e = np.diag(np.sum(np.abs(self.H), axis=0))
        return deg_v, deg_e

    # ------------------------------------------------------------------
    # Laplacian construction
    # ------------------------------------------------------------------

    def build_laplacian(
        self,
        kappa: float = 1.0,
        baseline_weights: Optional[np.ndarray] = None,
        endocrinal_norm: float = 0.0,
        eta: Optional[np.ndarray] = None,
    ) -> np.ndarray:
        """
        Build the symmetric normalized hypergraph Laplacian

            L = D_v^{-1/2} (D_v - H W D_e^{-1} H^T) D_v^{-1/2}

        with
            w_e = kappa * w_e^{(0)} * (1 + eta_e * |M_E|_F).
        """
        if baseline_weights is None:
            baseline_weights = np.ones(self.n_edges)
        else:
            baseline_weights = np.asarray(baseline_weights, dtype=float)
            if baseline_weights.shape != (self.n_edges,):
                raise ValueError(
                    f"baseline_weights must have shape ({self.n_edges},)"
                )

        if eta is None:
            eta = 0.1 * np.ones(self.n_edges)
        else:
            eta = np.asarray(eta, dtype=float)
            if eta.shape != (self.n_edges,):
                raise ValueError(f"eta must have shape ({self.n_edges},)")

        if kappa <= 0:
            raise ValueError("kappa must be positive")

        w = kappa * baseline_weights * (1.0 + eta * float(endocrinal_norm))
        W = np.diag(w)

        Dv, De = self._degree_matrices()
        # Guard against zero degrees (should not occur for this H)
        dv = np.diag(Dv).copy()
        de = np.diag(De).copy()
        if np.any(dv <= 0) or np.any(de <= 0):
            raise RuntimeError("Zero degree detected in incidence structure")

        Dv_inv_sqrt = np.diag(1.0 / np.sqrt(dv))
        De_inv = np.diag(1.0 / de)

        L_unnorm = Dv - self.H @ W @ De_inv @ self.H.T
        L = Dv_inv_sqrt @ L_unnorm @ Dv_inv_sqrt

        # Enforce exact symmetry (floating-point hygiene)
        L = 0.5 * (L + L.T)
        return L

    # ------------------------------------------------------------------
    # Spectrum
    # ------------------------------------------------------------------

    def spectrum(
        self,
        kappa: float = 1.0,
        endocrinal_norm: float = 0.0,
        baseline_weights: Optional[np.ndarray] = None,
        eta: Optional[np.ndarray] = None,
    ) -> Dict[str, Any]:
        """
        Eigen-decomposition of L_H(kappa, |M_E|_F).

        Returns
        -------
        dict with keys:
            eigenvalues, eigenvectors, lambda_1, lambda_2,
            spectral_gap, L
        """
        L = self.build_laplacian(
            kappa=kappa,
            baseline_weights=baseline_weights,
            endocrinal_norm=endocrinal_norm,
            eta=eta,
        )
        eigvals, eigvecs = np.linalg.eigh(L)

        # Numerical cleanup of the kernel eigenvalue
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

    # ------------------------------------------------------------------
    # Exact kernel projector (global sync mode)
    # ------------------------------------------------------------------

    def exact_kernel_projector(
        self,
        kappa: float = 1.0,
        endocrinal_norm: float = 0.0,
        tol: float = 1e-8,
        baseline_weights: Optional[np.ndarray] = None,
        eta: Optional[np.ndarray] = None,
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Return (Pi_kernel, V_kernel) where

            Pi_kernel = V_kernel @ V_kernel.T

        projects onto the eigenspace with eigenvalues <= tol.

        For this strongly connected hypergraph the kernel is 1-D
        (global synchronization mode). V_kernel has shape (n_nodes, 1).
        """
        spec = self.spectrum(
            kappa=kappa,
            endocrinal_norm=endocrinal_norm,
            baseline_weights=baseline_weights,
            eta=eta,
        )
        eigs = spec["eigenvalues"]
        vecs = spec["eigenvectors"]

        mask = eigs <= tol
        if not np.any(mask):
            # Fallback: take the smallest eigenvalue mode
            mask = np.zeros_like(eigs, dtype=bool)
            mask[0] = True

        V_kernel = vecs[:, mask]
        # Ensure consistent orientation (positive mean)
        if V_kernel.shape[1] == 1 and np.sum(V_kernel) < 0:
            V_kernel = -V_kernel

        Pi_kernel = V_kernel @ V_kernel.T
        return Pi_kernel, V_kernel

    # ------------------------------------------------------------------
    # Slow subspace (modes up to a gap threshold)
    # ------------------------------------------------------------------

    def slow_subspace(
        self,
        gap_threshold: float,
        kappa: float = 1.0,
        endocrinal_norm: float = 0.0,
        baseline_weights: Optional[np.ndarray] = None,
        eta: Optional[np.ndarray] = None,
    ) -> Tuple[np.ndarray, np.ndarray, int]:
        """
        Return (Pi_s, V_slow, d_slow) projecting onto the eigenspace
        with eigenvalues <= gap_threshold.

        d_slow is the dimension of that subspace.
        """
        spec = self.spectrum(
            kappa=kappa,
            endocrinal_norm=endocrinal_norm,
            baseline_weights=baseline_weights,
            eta=eta,
        )
        eigs = spec["eigenvalues"]
        vecs = spec["eigenvectors"]

        mask = eigs <= gap_threshold
        V_slow = vecs[:, mask]
        Pi_s = V_slow @ V_slow.T
        d_slow = int(np.sum(mask))
        return Pi_s, V_slow, d_slow

    def slow_projector(
        self,
        gap_threshold: Optional[float] = None,
        kappa: float = 1.0,
        endocrinal_norm: float = 0.0,
        baseline_weights: Optional[np.ndarray] = None,
        eta: Optional[np.ndarray] = None,
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Convenience wrapper. If gap_threshold is None, uses 1.5 * λ₂.
        Returns (Pi_s, V_slow).
        """
        if gap_threshold is None:
            spec = self.spectrum(
                kappa=kappa,
                endocrinal_norm=endocrinal_norm,
                baseline_weights=baseline_weights,
                eta=eta,
            )
            lam2 = spec["lambda_2"]
            gap_threshold = 1.5 * lam2 if lam2 > 0 else 1.0

        Pi_s, V_slow, _ = self.slow_subspace(
            gap_threshold=gap_threshold,
            kappa=kappa,
            endocrinal_norm=endocrinal_norm,
            baseline_weights=baseline_weights,
            eta=eta,
        )
        return Pi_s, V_slow


# ----------------------------------------------------------------------
# Module-level convenience helpers
# ----------------------------------------------------------------------

def kernel_coefficient(
    Psi: np.ndarray,
    v_sync: np.ndarray,
) -> float:
    """
    Extract the slow coordinate as the coefficient of the global
    synchronization mode: c = v_sync · Psi.
    """
    Psi = np.asarray(Psi, dtype=float).ravel()
    v_sync = np.asarray(v_sync, dtype=float).ravel()
    if Psi.shape != v_sync.shape:
        raise ValueError("Psi and v_sync must have the same shape")
    return float(v_sync @ Psi)