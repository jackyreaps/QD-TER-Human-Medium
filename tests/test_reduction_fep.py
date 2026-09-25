"""
Step D — Local conditional FEP reduction tests (RT1).

Fixes vs earlier draft:
  - Stable well ordering: Psi_B > Psi_A (so U''(Psi_B) > 0 and M_E > 0)
  - Sync lift: all components ≈ Psi_B (constant kernel), not Psi_B * v
  - Robust solve_ivp (use sol.t / sol.y shape)
  - Combinatorial Laplacian from fixed spectral.py
"""

from __future__ import annotations

import numpy as np
import pytest
from scipy.integrate import solve_ivp

from src.manifold.rheology import AetherSubstrateConstants, ChiralManifoldRheology
from src.manifold.spectral import HypergraphSpectral, sync_mean


def natural_precisions(f, Psi_A, Psi_B):
    return f * Psi_A * Psi_B, f * Psi_B * (Psi_B - Psi_A)


def axiom_C_M_E(glue, Psi_A, Psi_B):
    denom = Psi_B - Psi_A
    if abs(denom) < 1e-12:
        raise ValueError("Psi_A ≈ Psi_B collapses the double-well")
    return glue * Psi_B / denom


def linearized_rates(f, Psi_A, Psi_B, glue, M_E_norm):
    Pi_o, Pi_s = natural_precisions(f, Psi_A, Psi_B)
    U_pp = f * Psi_B * (Psi_B - Psi_A)
    Gamma = Pi_s * glue
    return {
        "Pi_o": Pi_o,
        "Pi_s": Pi_s,
        "Gamma": Gamma,
        "Gamma_eff": Pi_s * M_E_norm * U_pp,
        "Gamma_fep": Gamma * (Pi_o + Pi_s),
        "U_pp": U_pp,
    }


class FullQDTERSystem:
    def __init__(self, L_H, M_E, f, Psi_A, Psi_B):
        self.L_H = np.asarray(L_H, float)
        self.M_E = np.asarray(M_E, float)
        self.f, self.Psi_A, self.Psi_B = float(f), float(Psi_A), float(Psi_B)

    def rhs(self, t, Psi):
        Psi = np.asarray(Psi, float)
        reaction = self.f * Psi * (self.Psi_A - Psi) * (Psi - self.Psi_B)
        return -self.L_H @ Psi + self.M_E @ reaction


class LinearizedFEP:
    def __init__(self, Gamma, Pi_o, Pi_s):
        self.rate = float(Gamma * (Pi_o + Pi_s))

    def rhs(self, t, mu):
        return -self.rate * mu[0]


@pytest.fixture
def engine():
    return ChiralManifoldRheology(
        AetherSubstrateConstants(), characteristic_node_dimension=0.5
    )


@pytest.fixture
def default_params():
    # STABLE posterior well: Psi_B > Psi_A so U''(Psi_B) > 0 and Axiom C M_E > 0
    return {"f": 0.5, "Psi_A": 0.2, "Psi_B": 1.0, "OXTR": 0.5, "GJ": 0.5}


def test_cubic_is_negative_gradient_of_quartic(default_params):
    f, A, B = default_params["f"], default_params["Psi_A"], default_params["Psi_B"]
    Psi = 0.6

    def U(x):
        return f * (x**4 / 4 - (A + B) * x**3 / 3 + A * B * x**2 / 2)

    eps = 1e-7
    dU = (U(Psi + eps) - U(Psi - eps)) / (2 * eps)
    F = f * Psi * (A - Psi) * (Psi - B)
    assert dU == pytest.approx(-F, rel=1e-5)


def test_spectral_gap_positive():
    sp = HypergraphSpectral().spectrum(kappa=1.0)
    assert sp["lambda_1"] == pytest.approx(0.0, abs=1e-10)
    assert sp["lambda_2"] > 0.0


def test_gap_increases_with_kappa():
    gaps = [
        HypergraphSpectral().spectrum(kappa=k)["lambda_2"]
        for k in (0.5, 1.0, 2.0, 5.0, 10.0)
    ]
    for i in range(len(gaps) - 1):
        assert gaps[i + 1] > gaps[i], f"gaps={gaps}"


def test_kernel_is_one_dimensional():
    _, V = HypergraphSpectral().exact_kernel_projector(kappa=1.0)
    assert V.shape[1] == 1


def test_kernel_contains_constant_mode():
    Pi, _ = HypergraphSpectral().exact_kernel_projector(kappa=1.0)
    ones = np.ones(7) / np.sqrt(7)
    assert np.allclose(Pi @ ones, ones, atol=1e-8)


def test_L_annihilates_constants():
    L = HypergraphSpectral().build_laplacian(kappa=3.0, endocrinal_norm=0.4)
    assert np.allclose(L @ np.ones(7), 0.0, atol=1e-10)


def test_axiom_C_rate_matching(default_params):
    f, A, B = default_params["f"], default_params["Psi_A"], default_params["Psi_B"]
    glue = 0.5
    r = linearized_rates(f, A, B, glue, axiom_C_M_E(glue, A, B))
    assert r["Gamma_eff"] == pytest.approx(r["Gamma_fep"], rel=1e-12)
    assert r["Pi_s"] > 0 and axiom_C_M_E(glue, A, B) > 0


def test_axiom_C_fails_without_consistency(default_params):
    f, A, B = default_params["f"], default_params["Psi_A"], default_params["Psi_B"]
    r = linearized_rates(f, A, B, 0.5, 0.5)  # wrong M_E
    assert r["Gamma_eff"] != pytest.approx(r["Gamma_fep"], rel=1e-3)


def test_linearized_trajectories_match(default_params):
    f, A, B = default_params["f"], default_params["Psi_A"], default_params["Psi_B"]
    r = linearized_rates(f, A, B, 0.5, axiom_C_M_E(0.5, A, B))
    t = np.linspace(0, 10, 201)
    s1 = solve_ivp(lambda t, x: -r["Gamma_eff"] * x, (0, 10), [0.01], t_eval=t, rtol=1e-10, atol=1e-12)
    s2 = solve_ivp(lambda t, x: -r["Gamma_fep"] * x, (0, 10), [0.01], t_eval=t, rtol=1e-10, atol=1e-12)
    assert np.max(np.abs(s1.y[0] - s2.y[0])) < 1e-10


def test_full_system_local_kernel_tracking(engine, default_params):
    f, A, B = default_params["f"], default_params["Psi_A"], default_params["Psi_B"]
    glue = engine.compute_cognitive_glue_index(default_params["OXTR"], default_params["GJ"])
    M_E_norm = axiom_C_M_E(glue, A, B)
    kappa = 20.0

    spectral = HypergraphSpectral()
    spec = spectral.spectrum(kappa=kappa, endocrinal_norm=M_E_norm)
    assert spec["lambda_2"] > 0

    L_H = spec["L"]
    M_E = M_E_norm * np.eye(7)
    rng = np.random.default_rng(0)
    # Correct sync lift: all components near posterior well
    Psi0 = B * np.ones(7) + 0.005 * rng.standard_normal(7)
    delta0 = sync_mean(Psi0) - B

    full = FullQDTERSystem(L_H, M_E, f, A, B)
    t = np.linspace(0, 5, 201)
    sol = solve_ivp(full.rhs, (0, 5), Psi0, t_eval=t, method="RK45", rtol=1e-9, atol=1e-11)
    assert sol.success, sol.message

    delta = np.array([sync_mean(sol.y[:, i]) - B for i in range(sol.y.shape[1])])
    r = linearized_rates(f, A, B, glue, M_E_norm)
    fep = LinearizedFEP(r["Gamma"], r["Pi_o"], r["Pi_s"])
    solf = solve_ivp(fep.rhs, (0, 5), [delta0], t_eval=sol.t, method="RK45", rtol=1e-9, atol=1e-11)
    err = float(np.max(np.abs(delta - solf.y[0])))
    print(f"local_err={err:.6e} lambda2={spec['lambda_2']:.4f}")
    assert err < 0.05


def test_error_decreases_with_gap(engine, default_params):
    f, A, B = default_params["f"], default_params["Psi_A"], default_params["Psi_B"]
    glue = engine.compute_cognitive_glue_index(0.5, 0.5)
    M_E_norm = axiom_C_M_E(glue, A, B)
    r = linearized_rates(f, A, B, glue, M_E_norm)
    fep_rate = r["Gamma_fep"]

    errors = []
    for kappa in (0.5, 1.0, 2.0, 5.0, 20.0, 50.0):
        spectral = HypergraphSpectral()
        spec = spectral.spectrum(kappa=kappa, endocrinal_norm=M_E_norm)
        L_H = spec["L"]
        evecs = spec["eigenvectors"]
        rng = np.random.default_rng(2)
        # Transverse (fast-mode) perturbation so adiabatic error is visible
        fast = evecs[:, 1:] @ (0.15 * rng.standard_normal(6))
        Psi0 = B * np.ones(7) + 0.01 * rng.standard_normal() * np.ones(7) + fast
        delta0 = sync_mean(Psi0) - B
        full = FullQDTERSystem(L_H, M_E_norm * np.eye(7), f, A, B)
        t = np.linspace(0, 3, 151)
        sol = solve_ivp(full.rhs, (0, 3), Psi0, t_eval=t, method="RK45", rtol=1e-8, atol=1e-10)
        assert sol.success, sol.message
        delta = np.array([sync_mean(sol.y[:, i]) - B for i in range(sol.y.shape[1])])
        solf = solve_ivp(
            lambda t, x: -fep_rate * x[0], (0, 3), [delta0], t_eval=sol.t, rtol=1e-8, atol=1e-10
        )
        errors.append(float(np.max(np.abs(delta - solf.y[0]))))
        print(f"kappa={kappa:5.1f} lambda2={spec['lambda_2']:8.4f} err={errors[-1]:.6e}")

    assert errors[-1] < errors[0], f"errors={errors}"


def test_natural_fixed_point_obstruction(default_params):
    f, A, B = default_params["f"], default_params["Psi_A"], default_params["Psi_B"]
    Pi_o, Pi_s = natural_precisions(f, A, B)
    mu_star = (Pi_o * B + Pi_s * A) / (Pi_o + Pi_s)
    assert mu_star != pytest.approx(B, abs=1e-4)