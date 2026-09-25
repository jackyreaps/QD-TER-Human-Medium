# Conditional Local FEP Reduction

**Status:** Adopted specification of the FEP reduction program.
**Scope:** Local, conditional reduction. Not a claim that FEP is an
unconditional limiting case of the published QD-TER suite.
**Companion documents:** CLAIMS.md §5, theory/reduction_fep_derivation.md.

---

## 1. Scope and Status

This document specifies a **local, conditional reduction** of QD-TER dynamics
to Free Energy Principle (FEP) recognition dynamics.

> **Conditional Local Reduction Theorem.** In a neighborhood of the posterior
> well Ψ_B, under the fast-aether (large-gap) limit, under the generative-model
> assumption (Axiom G), and under the endocrinal-matrix consistency condition
> (Axiom C), the linearized projected QD-TER dynamics is identical to the
> linearized Laplace-approximated FEP recognition dynamics.

The theorem is local in state space and conditional on two additional modeling
assumptions. Global fixed-point alignment and full nonlinear identity are
explicitly not claimed.

---

## 2. Axioms

### Axiom D (QD-TER Dynamics)

    dΨ/dt = −L_H(t) Ψ + M_E(t) · F(Ψ, f)

with

    F(Ψ, f) = f · Ψ (Ψ_A − Ψ)(Ψ − Ψ_B)

The form is adopted from the theory narrative; the operators are proposed in
the human-medium layer.

### Axiom S (Spectral Structure)

The hypergraph Laplacian L_H has a spectral gap bounded below by a
Cheeger-type expression, so that the fast-aether limit is well-defined as
λ_2 ≫ λ_slow. The explicit construction is a modeling proposal.

### Axiom G (Generative Model — Extra Assumption)

The human-medium layer assumes the QD-TER system implements a generative
model p(o, s) and recognition density q(s) = N(μ, Σ) with sufficient
statistics

    μ = Ψ_s    (the slow coordinate, kernel coefficient of L_H)

and precisions

    Π_o = f Ψ_A Ψ_B,    Π_s = f Ψ_B (Ψ_B − Ψ_A).

This is an additional modeling postulate, not derived from the published suite.

### Axiom C (Endocrinal Consistency — Extra Assumption)

For the local linearized reduction to hold, the endocrinal matrix norm must
satisfy

    M_E = G · Ψ_B / (Ψ_B − Ψ_A)

where G = √(OXTR · GJ) is the cognitive glue index. This is a derived
constraint under the chosen precisions, not an independent biophysical
measurement.

---

## 3. The Local Reduction Theorem

### 3.1 Theorem Statement

**Theorem (Local FEP Reduction).** Let Axioms D, S, G, C hold. Let
Ψ_s = P_s Ψ be the slow coordinate, where P_s is the orthogonal projector
onto the kernel of L_H. Let δΨ_s = Ψ_s − Ψ_B be a small perturbation from the
posterior well. For perturbations small enough that the cubic remainder is
negligible, the linearized projected QD-TER dynamics is

    δΨ̇_s = −Γ_eff · δΨ_s + O(ε)

with

    Γ_eff = P_s · M_E · U''(Ψ_B)

where U''(Ψ_B) = f Ψ_B (Ψ_B − Ψ_A) is the curvature of the quartic potential
at the posterior well. Under Axiom C,

    Γ_eff = Γ (Π_o + Π_s)

where Γ = Π_s · G is the FEP recognition gain. Therefore

    δΨ̇_s = −Γ (Π_o + Π_s) · δΨ_s + O(ε)

which is identical to the linearized Laplace FEP recognition dynamics

    δμ̇ = −Γ (Π_o + Π_s) · δμ + O(ε)

under the identification μ = Ψ_s.

### 3.2 Proof Sketch

1. Apply P_s to the full dynamics. Since P_s L_H = 0 on the slow subspace,
   the Laplacian drops out: Ψ̇_s = P_s M_E F(Ψ_s, f) + O(ε).
2. Expand F around Ψ_B. Since F(Ψ_B, f) = 0, the linear term is
   F'(Ψ_B) δΨ_s = −U''(Ψ_B) δΨ_s.
3. The effective rate is Γ_eff = P_s M_E U''(Ψ_B).
4. Under Axiom C, Γ_eff = Π_s G · f Ψ_B².
5. The FEP rate is Γ (Π_o + Π_s) = Π_s G · f Ψ_B² under Axioms G and C.
   The two match.

Full derivation and Cheeger / Tikhonov details:
theory/reduction_fep_derivation.md.

---

## 4. Boundary of the Claim

### 4.1 What Is Established

- The linearized projected QD-TER dynamics equals the linearized FEP
  recognition dynamics in a neighborhood of Ψ_B.
- The consistency condition M_E = G Ψ_B / (Ψ_B − Ψ_A) is derived from the
  requirement that the linearized rates match.
- The quartic potential U is derived from the cubic reaction F = −∂U/∂Ψ.
- The precisions Π_o = f Ψ_A Ψ_B and Π_s = f Ψ_B (Ψ_B − Ψ_A) are derived as
  curvatures of U at the two wells.

### 4.2 What Is Not Claimed

- **Global fixed-point alignment.** Under the natural assignment, the FEP
  fixed point μ* = (Π_o · o + Π_s · η) / (Π_o + Π_s) and the QD-TER posterior
  well Ψ_B differ by a term proportional to Ψ_B − Ψ_A. Equality requires
  Ψ_A = Ψ_B, which collapses the double-well structure. Alignment holds when
  the projection P_s Ψ_B lies on the FEP manifold; this is a codimension-1
  condition on the well parameters and is not generic.
- **Full nonlinear identity.** The projected reaction is cubic; the FEP
  gradient is linear under the Laplace approximation. Away from Ψ_B they
  differ by higher-order terms.
- **Unconditional recovery from the published suite.** Axioms G and C are
  extra modeling assumptions.

### 4.3 Residual Terms

The O(ε) term is the adiabatic-elimination error, controlled by the spectral
gap: ‖error‖ ≤ C_1 / λ_2.

---

## 5. Open Items

| Item | Status |
|---|---|
| Cheeger bound for the specific hypergraph | Sketch only |
| Tikhonov constants C_1, C_2 | Symbolic |
| Linear neighborhood size | Not bounded |
| Cubic residual bound away from Ψ_B | Not bounded |
| Numerical verification inside the local regime | Planned |

---

## 6. Resolution Pathways (if global claims are desired)

| Pathway | Cost |
|---|---|
| A. Modified observation function g(μ) = μ + c | Changes the generative model |
| B. Affine map μ = α Ψ_s + β | Changes the coordinate identification |
| C. Local-only claim (default) | Restricts scope, no extra cost |

---

## 7. Physics-Suite Inheritance

The reduction program operates entirely within the human-medium layer. The
residual V_4 action, the derived 8 channels, and the waist critical-line locus
are inherited from the future physics suite and are not re-derived here. The
human-medium layer routes pulsatile signals through the eight residual
channels; it does not generate the number 8.

---

## 8. CLAIMS.md Entry

See CLAIMS.md §5 (RT1). Boundary: local, conditional, not global.
