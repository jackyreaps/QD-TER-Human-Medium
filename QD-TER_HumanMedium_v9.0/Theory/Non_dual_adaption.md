# Non-Dual Adaptation Layer — Conditional Proposal

**Status:** Conjectural. Conditional on the physics suite supplying a
Riemannian metric on the human-medium parameter space.
**Scope:** Orthogonal to the FEP reduction. Not a consequence of it, and the
FEP reduction does not depend on it.
**Companion documents:** CLAIMS.md §6 (C3, C4, C5).

---

## 1. Scope

This document specifies a proposed additional layer formalizing world-model
updates as covariant derivatives on a Riemannian manifold. Without the metric
from the physics suite, the layer is a formal structure without content. The
mathematical core is stated; the metric bridge is a proposal.

---

## 2. Axioms

**Axiom M (Metric).** The world-model parameter space carries a Riemannian
metric g_ij(x) derived from QD-TER quantities (cognitive glue, Re_ε,
endocrinal matrix norm).

**Axiom V (Intentionality vector).** There exists a vector field V on this
manifold, transported along update trajectories.

**Axiom Ω (Coherence scalar).** The scalar Ω = g_ij V^i V^j is the metric
norm of V.

---

## 3. The Parallel Transport Condition

    ∇_X V = 0

expands in components to

    ∂V^k/∂x^i + Γ^k_{ij} V^j X^i = 0

with Γ^k_{ij} the Christoffel symbols of the metric g_ij.

**Note.** The Christoffel symbols are derived from the metric via

    Γ^k_{ij} = (1/2) g^{kl} (∂_i g_{jl} + ∂_j g_{il} − ∂_l g_{ij})

A flat metric (g_ij = δ_ij) gives Γ = 0, in which case the construction is
trivial. The layer is only nontrivial when g_ij(x) is derived from QD-TER
quantities.

---

## 4. Holonomy

On a curved manifold, parallel transport is path-dependent. Under a closed
loop γ,

    V(after loop) = H_γ · V(before loop)

where H_γ ∈ SO(d) is the holonomy matrix of the loop. The intentionality
vector is covariantly constant along the update trajectory. Under closed
loops it transforms by the holonomy, which is a measurable geometric phase.

---

## 5. Violation Detection

An update trajectory that does not satisfy the parallel transport condition
produces a nonzero covariant derivative:

    ‖∇_X V‖ ≠ 0

This quantity is measurable and can be monitored along the update path.
Trajectories that fail to preserve the invariant direction are identified by
a nonzero value of ‖∇_X V‖.

---

## 6. What Is Not Claimed

- That the intentionality vector is a fixed vector in R^d. It is a section of
  a vector bundle over the parameter manifold.
- That Ω < 1 registers as a dielectric grid break. The map from Ω to the
  dielectric pipeline in rheology.py is a proposed modeling bridge, not a
  derived result.
- That the metric bridge in §7 is derived from the physics suite.

---

## 7. Metric Bridge (To Be Supplied)

    g_ij(x) = δ_ij · 1/(1 + Re_ε(x)) + (G(x) / (Ψ_B − Ψ_A)) · M_E^(ij)

Requires:

1. Explicit identification of the coordinates x on the parameter space.
2. Derivation of the Re_ε and G dependence from the rheology layer.
3. Verification that the resulting metric is positive definite.

---

## 8. CLAIMS.md Entry

See CLAIMS.md §6 (C3, C4, C5). Status: conjectural, conditional on the
physics suite.
