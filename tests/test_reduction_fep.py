"""
Step D — Local conditional FEP reduction tests

Verifies the local linearized reduction
(QD-TER_HumanMedium_v9.0/Theory/Reduction_fep.md, RT1):

  In a neighborhood of the posterior well Ψ_B, under Axioms G and C
  and a large spectral gap, the linearized projected QD-TER dynamics
  matches the linearized Laplace FEP recognition dynamics.

Does NOT claim:
  - global fixed-point alignment
  - full nonlinear identity of projected flow with FEP gradient
  - unconditional recovery from the published suite without G and C
"""

from __future__ import annotations

import numpy as np
import pytest
from scipy.integrate import solve_ivp

from src.manifold.rheology import (
    AetherSubstrateConstants,
    ChiralManifoldRheology,
)
from src.manifold.spectral import HypergraphSpectral, kernel_coefficient


# ---------------------------------------------------------------------------
# Algebraic helpers (Resolution C / Axiom C)
# ---------------------------------------------------------------------------

def natural_precisions(f: float, Psi_A: float, Psi_B: float):
    """Π_o, Π_s as curvatures of the quartic potential at the two wells."""
    Pi_o = f * Psi_A * Psi_B
    Pi_s = f * Psi_B * (Psi_B - Psi_A)
    return Pi_o, Pi_s


def axiom_C_M_E(glue: float, Psi_A: float, Psi_B: float) -> float:
    """
    Axiom C consistency condition:
        |M_E| = G * Ψ_B / (Ψ_B - Ψ_A)
    """
    denom = Psi_B - Psi_A
    if abs(denom) < 1e-12:
        raise ValueError("Ψ_A ≈ Ψ_B collapses the double-well; Axiom C undefined")
    return glue * Psi_B / denom


def linearized_rates(f, Psi_A, Psi_B, glue, M_E_norm, Pi_s_scale=1.0):
    """
    Γ_eff  = Π_s * M_E * U''(Ψ_B)
    Γ_fep  = Γ * (Π_o + Π_s)  with Γ = Π_s * G

    Under Axiom C these must match.
    """
    Pi_o, Pi_s = natural_precisions(f, Psi_A, Psi_B)
    Pi_s = Pi_s * Pi_s_scale
    U_pp = f * Psi_B * (Psi_B - Psi_A)  # U''(Ψ_B)
    Gamma = Pi_s * glue
    Gamma_eff = Pi_s * M_E_norm * U_pp
    Gamma_fep = Gamma * (Pi_o + Pi_s)
    return {
        "Pi_o": Pi_o,
        "Pi_s": Pi_s,
        "Gamma": Gamma,
        "Gamma_eff": Gamma_eff,
        "Gamma_fep": Gamma_fep,
        "U_pp": U_pp,
    }


# ---------------------------------------------------------------------------
# Full 7D QD-TER system (Axiom D)
# ---------------------------------------------------------------------------

class FullQDTERSystem:
    """
    dΨ/dt = -L_H Ψ + M_E · F(Ψ, f)

    with element-wise cubic reaction
        F_i = f * Ψ_i * (Ψ_A - Ψ_i) * (Ψ_i - Ψ_B)
    """

    def __init__(self, L_H, M_E, f, Psi_A, Psi_B):
        self.L_H = np.asarray(L_H, dtype=float)
        self.M_E = np.asarray(M_E, dtype=float)
        self.f = float(f)
        self.Psi_A = float(Psi_A)
        self.Psi_B = float(Psi_B)

    def rhs(self, t, Psi):
        Psi = np.asarray(Psi, dtype=float)
        reaction = self.f * Psi * (self.Psi_A - Psi) * (Psi - self.Psi_B)
        return -self.L_H @ Psi + self.M_E @ reaction


# ---------------------------------------------------------------------------
# Linearized FEP recognition (Laplace form near the well)
# ---------------------------------------------------------------------------

class LinearizedFEP:
    """
    δμ̇ = -Γ (Π_o + Π_s) δμ
    """

    def __init__(self, Gamma, Pi_o, Pi_s):
        self.rate = float(Gamma * (Pi_o + Pi_s))

    def rhs(self, t, mu):
        return -self.rate * mu[0]


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def engine():
    substrate = AetherSubstrateConstants()
    return ChiralManifoldRheology(
        substrate=substrate,
        characteristic_node_dimension=0.5,
    )


@pytest.fixture
def default_params():
    # Posterior well Ψ_B; prior well Ψ_A. Keep Ψ_B ≠ Ψ_A (non-degenerate).
    return {
        "f": 0.5,
        "Psi_A": 1.0,
        "Psi_B": 0.2,
        "OXTR": 0.5,
        "GJ": 0.5,
    }


# ---------------------------------------------------------------------------
# 1. Quartic potential identity (Der1)
# ---------------------------------------------------------------------------

def test_cubic_is_negative_gradient_of_quartic():
    """F = -∂U/∂Ψ exactly (Der1)."""
    f, Psi_A, Psi_B = 0.5, 1.0, 0.2
    Psi = 0.3

    def U(x):
        return f * (
            x**4 / 4.0
            - (Psi_A + Psi_B) * x**3 / 3.0
            + Psi_A * Psi_B * x**2 / 2.0
        )

    eps = 1e-7
    dU = (U(Psi + eps) - U(Psi - eps)) / (2 * eps)
    F = f * Psi * (Psi_A - Psi) * (Psi - Psi_B)
    assert dU == pytest.approx(-F, rel=1e-5)


# ---------------------------------------------------------------------------
# 2. Spectral structure (Axiom S)
# ---------------------------------------------------------------------------

def test_spectral_gap_positive():
    spectral = HypergraphSpectral()
    spec = spectral.spectrum(kappa=1.0, endocrinal_norm=0.0)
    assert spec["lambda_1"] == pytest.approx(0.0, abs=1e-10)
    assert spec["lambda_2"] > 0.0


def test_gap_increases_with_kappa():
    spectral = HypergraphSpectral()
    gaps = [
        spectral.spectrum(kappa=k, endocrinal_norm=0.0)["lambda_2"]
        for k in (0.5, 1.0, 2.0, 5.0, 10.0)
    ]
    for i in range(len(gaps) - 1):
        assert gaps[i + 1] > gaps[i], f"Gap not increasing: {gaps}"


def test_kernel_is_one_dimensional():
    spectral = HypergraphSpectral()
    _, V = spectral.exact_kernel_projector(kappa=1.0, endocrinal_norm=0.0)
    assert V.shape[1] == 1


def test_kernel_contains_constant_mode():
    """Global sync mode is (approximately) the constant vector."""
    spectral = HypergraphSpectral()
    Pi, V = spectral.exact_kernel_projector(kappa=1.0, endocrinal_norm=0.0)
    ones = np.ones(spectral.n_nodes) / np.sqrt(spectral.n_nodes)
    projected = Pi @ ones
    assert np.allclose(projected, ones, atol=1e-6)


# ---------------------------------------------------------------------------
# 3. Axiom C — linearized rate matching (core of RT1)
# ---------------------------------------------------------------------------

def test_axiom_C_rate_matching(default_params):
    """
    Under Axiom C, Γ_eff = Γ (Π_o + Π_s) to machine precision.
    """
    f = default_params["f"]
    Psi_A = default_params["Psi_A"]
    Psi_B = default_params["Psi_B"]
    glue = 0.5

    M_E = axiom_C_M_E(glue, Psi_A, Psi_B)
    rates = linearized_rates(f, Psi_A, Psi_B, glue, M_E)

    assert rates["Gamma_eff"] == pytest.approx(rates["Gamma_fep"], rel=1e-12)


def test_axiom_C_fails_without_consistency(default_params):
    """Wrong |M_E| must break rate matching (sanity check)."""
    f = default_params["f"]
    Psi_A = default_params["Psi_A"]
    Psi_B = default_params["Psi_B"]
    glue = 0.5

    M_E_wrong = glue  # not the Axiom C value
    rates = linearized_rates(f, Psi_A, Psi_B, glue, M_E_wrong)
    assert rates["Gamma_eff"] != pytest.approx(rates["Gamma_fep"], rel=1e-3)


# ---------------------------------------------------------------------------
# 4. Linearized trajectories match under Axiom C
# ---------------------------------------------------------------------------

def test_linearized_trajectories_match(default_params):
    """
    δΨ̇_s = -Γ_eff δΨ_s  and  δμ̇ = -Γ(Π_o+Π_s) δμ
    must agree when Axiom C holds.
    """
    f = default_params["f"]
    Psi_A = default_params["Psi_A"]
    Psi_B = default_params["Psi_B"]
    glue = 0.5

    M_E = axiom_C_M_E(glue, Psi_A, Psi_B)
    rates = linearized_rates(f, Psi_A, Psi_B, glue, M_E)

    t_span = (0.0, 10.0)
    t_eval = np.linspace(0, 10, 201)
    delta0 = 0.01

    sol_qd = solve_ivp(
        lambda t, x: -rates["Gamma_eff"] * x,
        t_span,
        [delta0],
        t_eval=t_eval,
        rtol=1e-10,
        atol=1e-12,
    )
    sol_fep = solve_ivp(
        lambda t, x: -rates["Gamma_fep"] * x,
        t_span,
        [delta0],
        t_eval=t_eval,
        rtol=1e-10,
        atol=1e-12,
    )

    err = np.max(np.abs(sol_qd.y[0] - sol_fep.y[0]))
    assert err < 1e-10, f"Linearized trajectories diverge: err={err:.2e}"


# ---------------------------------------------------------------------------
# 5. Full-system local probe (kernel coefficient near Ψ_B)
# ---------------------------------------------------------------------------

def test_full_system_local_kernel_tracking(engine, default_params):
    """
    Integrate full 7D system with Axiom C |M_E|, extract kernel
    coefficient, and compare to linearized FEP near the well.

    This is a local consistency check, not a global reduction proof.
    """
    f = default_params["f"]
    Psi_A = default_params["Psi_A"]
    Psi_B = default_params["Psi_B"]
    OXTR = default_params["OXTR"]
    GJ = default_params["GJ"]
    kappa = 20.0  # large gap

    glue = engine.compute_cognitive_glue_index(OXTR, GJ)
    M_E_norm = axiom_C_M_E(glue, Psi_A, Psi_B)

    spectral = HypergraphSpectral()
    spec = spectral.spectrum(kappa=kappa, endocrinal_norm=M_E_norm)
    L_H = spec["L"]
    lambda_2 = spec["lambda_2"]
    assert lambda_2 > 0

    _, V_kernel = spectral.exact_kernel_projector(
        kappa=kappa, endocrinal_norm=M_E_norm
    )
    v_sync = V_kernel[:, 0]
    M_E = M_E_norm * np.eye(spectral.n_nodes)

    # Start near the posterior well along the sync mode + small noise
    rng = np.random.default_rng(0)
    # Represent the well as a scalar on the sync mode, then lift
    c_well = Psi_B
    Psi0 = c_well * v_sync + 0.005 * rng.standard_normal(spectral.n_nodes)
    c0 = kernel_coefficient(Psi0, v_sync)
    delta0 = c0 - Psi_B

    full = FullQDTERSystem(L_H, M_E, f, Psi_A, Psi_B)
    t_span = (0.0, 5.0)
    t_eval = np.linspace(0, 5, 201)

    sol = solve_ivp(
        full.rhs,
        t_span,
        Psi0,
        t_eval=t_eval,
        method="RK45",
        rtol=1e-9,
        atol=1e-11,
    )
    c_traj = np.array([kernel_coefficient(sol.y[:, i], v_sync) for i in range(len(t_eval))])
    delta_traj = c_traj - Psi_B

    rates = linearized_rates(f, Psi_A, Psi_B, glue, M_E_norm)
    fep = LinearizedFEP(rates["Gamma"], rates["Pi_o"], rates["Pi_s"])
    sol_fep = solve_ivp(
        fep.rhs,
        t_span,
        [delta0],
        t_eval=t_eval,
        method="RK45",
        rtol=1e-9,
        atol=1e-11,
    )

    # Compare deviations from the well (local regime)
    err = np.max(np.abs(delta_traj - sol_fep.y[0]))
    print(
        f"kappa={kappa:.1f}  λ2={lambda_2:.4f}  "
        f"local_err={err:.6f}  delta0={delta0:.6f}"
    )
    # Local tolerance: small initial perturbation + large gap
    assert err < 0.05, f"Local tracking error too large: {err:.6f}"


# ---------------------------------------------------------------------------
# 6. Gap scaling (FT1) — error decreases as λ₂ grows
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("kappa", [1.0, 2.0, 5.0, 10.0, 20.0, 50.0])
def test_gap_sweep_finite_error(engine, default_params, kappa):
    """Error remains finite across gap sweep (diagnostic)."""
    f = default_params["f"]
    Psi_A = default_params["Psi_A"]
    Psi_B = default_params["Psi_B"]
    OXTR = default_params["OXTR"]
    GJ = default_params["GJ"]

    glue = engine.compute_cognitive_glue_index(OXTR, GJ)
    M_E_norm = axiom_C_M_E(glue, Psi_A, Psi_B)

    spectral = HypergraphSpectral()
    spec = spectral.spectrum(kappa=kappa, endocrinal_norm=M_E_norm)
    L_H = spec["L"]
    lambda_2 = spec["lambda_2"]

    _, V_kernel = spectral.exact_kernel_projector(
        kappa=kappa, endocrinal_norm=M_E_norm
    )
    v_sync = V_kernel[:, 0]
    M_E = M_E_norm * np.eye(spectral.n_nodes)

    rng = np.random.default_rng(1)
    Psi0 = Psi_B * v_sync + 0.005 * rng.standard_normal(spectral.n_nodes)
    c0 = kernel_coefficient(Psi0, v_sync)
    delta0 = c0 - Psi_B

    full = FullQDTERSystem(L_H, M_E, f, Psi_A, Psi_B)
    t_eval = np.linspace(0, 5, 151)
    sol = solve_ivp(
        full.rhs, (0.0, 5.0), Psi0, t_eval=t_eval,
        method="RK45", rtol=1e-8, atol=1e-10,
    )
    delta_traj = np.array(
        [kernel_coefficient(sol.y[:, i], v_sync) - Psi_B for i in range(len(t_eval))]
    )

    rates = linearized_rates(f, Psi_A, Psi_B, glue, M_E_norm)
    fep = LinearizedFEP(rates["Gamma"], rates["Pi_o"], rates["Pi_s"])
    sol_fep = solve_ivp(
        fep.rhs, (0.0, 5.0), [delta0], t_eval=t_eval,
        method="RK45", rtol=1e-8, atol=1e-10,
    )

    err = float(np.max(np.abs(delta_traj - sol_fep.y[0])))
    print(f"kappa={kappa:6.1f}  λ2={lambda_2:8.4f}  err={err:.6f}")
    assert np.isfinite(err)


def test_error_decreases_with_gap(engine, default_params):
    """
    FT1 (soft form): error at largest kappa < error at smallest kappa.
    """
    f = default_params["f"]
    Psi_A = default_params["Psi_A"]
    Psi_B = default_params["Psi_B"]
    OXTR = default_params["OXTR"]
    GJ = default_params["GJ"]
    glue = engine.compute_cognitive_glue_index(OXTR, GJ)
    M_E_norm = axiom_C_M_E(glue, Psi_A, Psi_B)

    errors = []
    gaps = []
    for kappa in (1.0, 5.0, 20.0, 50.0):
        spectral = HypergraphSpectral()
        spec = spectral.spectrum(kappa=kappa, endocrinal_norm=M_E_norm)
        L_H = spec["L"]
        gaps.append(spec["lambda_2"])

        _, V_kernel = spectral.exact_kernel_projector(
            kappa=kappa, endocrinal_norm=M_E_norm
        )
        v_sync = V_kernel[:, 0]
        M_E = M_E_norm * np.eye(spectral.n_nodes)

        rng = np.random.default_rng(2)
        Psi0 = Psi_B * v_sync + 0.005 * rng.standard_normal(spectral.n_nodes)
        c0 = kernel_coefficient(Psi0, v_sync)
        delta0 = c0 - Psi_B

        full = FullQDTERSystem(L_H, M_E, f, Psi_A, Psi_B)
        t_eval = np.linspace(0, 5, 151)
        sol = solve_ivp(
            full.rhs, (0.0, 5.0), Psi0, t_eval=t_eval,
            method="RK45", rtol=1e-8, atol=1e-10,
        )
        delta_traj = np.array(
            [kernel_coefficient(sol.y[:, i], v_sync) - Psi_B for i in range(len(t_eval))]
        )

        rates = linearized_rates(f, Psi_A, Psi_B, glue, M_E_norm)
        fep = LinearizedFEP(rates["Gamma"], rates["Pi_o"], rates["Pi_s"])
        sol_fep = solve_ivp(
            fep.rhs, (0.0, 5.0), [delta0], t_eval=t_eval,
            method="RK45", rtol=1e-8, atol=1e-10,
        )
        errors.append(float(np.max(np.abs(delta_traj - sol_fep.y[0]))))

    print("gaps=", gaps)
    print("errors=", errors)
    assert errors[-1] < errors[0], (
        f"Error did not decrease with gap: {errors[0]:.6f} -> {errors[-1]:.6f}"
    )


# ---------------------------------------------------------------------------
# 7. Natural fixed-point obstruction (Der3) — documentation test
# ---------------------------------------------------------------------------

def test_natural_fixed_point_obstruction(default_params):
    """
    Under natural assignments, μ* ≠ Ψ_B unless Ψ_A = Ψ_B.
    Documents Der3; does not attempt global alignment.
    """
    f = default_params["f"]
    Psi_A = default_params["Psi_A"]
    Psi_B = default_params["Psi_B"]
    Pi_o, Pi_s = natural_precisions(f, Psi_A, Psi_B)
    o, eta = Psi_B, Psi_A

    mu_star = (Pi_o * o + Pi_s * eta) / (Pi_o + Pi_s)
    assert mu_star != pytest.approx(Psi_B, abs=1e-4)