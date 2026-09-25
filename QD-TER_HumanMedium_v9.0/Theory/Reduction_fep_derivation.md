# FEP Reduction — Full Derivation

**Status:** Stub. Full derivation to be completed.
**Companion to:** theory/reduction_fep.md §3, CLAIMS.md §5 (RT1).

---

## Contents (to be filled)

1. **Projection.** Apply the slow-subspace projector P_s to the full dynamics.
   Show P_s L_H = 0 on the slow subspace and derive the projected dynamics
   Ψ̇_s = P_s M_E F(Ψ_s, f) + O(ε).

2. **Linearization.** Expand the cubic reaction around the posterior well Ψ_B.
   Show F(Ψ_B, f) = 0 and F'(Ψ_B) = −U''(Ψ_B) = −f Ψ_B (Ψ_B − Ψ_A).

3. **Effective rate.** Derive Γ_eff = P_s M_E U''(Ψ_B).

4. **Axiom C.** Substitute M_E = G Ψ_B / (Ψ_B − Ψ_A). Show
   Γ_eff = Π_s G · f Ψ_B².

5. **FEP rate.** Under Axioms G and C, show Γ (Π_o + Π_s) = Π_s G · f Ψ_B².
   Match to Γ_eff.

6. **Error term.** Bound the O(ε) remainder using the spectral gap:
   ‖error‖ ≤ C_1 / λ_2. Estimate C_1 from Lipschitz constants of F and M_E.

---

## Cheeger Bound for the Specific Hypergraph

To be supplied: proof that for the seven-engine incidence structure, the
Cheeger constant satisfies h(H) ≥ 4 / (n · diam(H)), and derivation of the
spectral gap bound λ_2 ≥ (4 / (n · diam(H))) (1 − 𝔻 |M_E|_F).

---

## Tikhonov Constants

To be supplied: explicit C_1, C_2 from the actual F and M_E, computed against
the rheology.py parameter ranges.

---

## Numerical Verification

Companion test file: tests/test_reduction_fep.py. Scope: rate matching to
machine precision, kernel coefficient tracking inside a small neighborhood of
Ψ_B, gap scaling of the residual, and a separate Re_ε sweep at fixed gap.
