# CLAIMS.md

**Purpose.** Canonical taxonomy of every claim in the QD-TER Human-Medium
repository. Sections 1–9 cover the core (version 9.0); Part V (version 10.0)
claims are indexed in Section 10 and listed in two module files. Every claim is classified as exactly one of the
following.

| Category | Meaning |
|---|---|
| Axiom (inherited) | Adopted from the future physics suite. Not derived here. |
| Axiom (modeling) | Adopted as an extra assumption in the human-medium layer. |
| Definition | A named object introduced for use. |
| Derivation | Proven from axioms and definitions. |
| Reduction theorem (conditional) | Proven given explicitly stated axioms. |
| Conjecture | Proposed, not proven. |
| Falsification test | An experiment that would discriminate the framework. |

---

## 1. Axioms Inherited from the Physics Suite

| ID | Claim |
|---|---|
| D1 | Residual waist N_waist = 36 |
| D2 | Hierarchical reduction 12 → 6 → 3 |
| D3 | Residual parity group V_4 ≅ Z_2 × Z_2 |
| D4 | Four orientation frames on the waist |
| D5 | Residual V_4 action on the waist |
| D6 | Waist-mode projector Π_waist restricts V_4 to the 36-mode block |
| D7 | Waist = critical-line locus |
| D8 | 8-channel residual sector |

---

## 2. Axioms (Modeling, Human-Medium Layer)

| ID | Claim |
|---|---|
| M1 | Hypergraph incidence structure over seven engines |
| M2 | Weight law with endocrine modulation |
| M3 | Normalized hypergraph Laplacian |
| M4 | Endocrinal matrix definition |
| M5 | Cubic reaction form |
| M6 | Generative model p(o, s) |
| M7 | Recognition density q(s) = N(μ, Σ) |
| M8 | Identification μ = Ψ_s |
| M9 | Precisions Π_o, Π_s |
| M10 | Endocrinal consistency condition |
| M11 | Riemannian metric on parameter space (non-dual layer) |

---

## 3. Definitions

| ID | Definition |
|---|---|
| Def1 | Cognitive glue index G = √(OXTR · GJ) |
| Def2 | Dielectric Reynolds number Re_ε |
| Def3 | Demethylation cost ΔG_reconfig |
| Def4 | Quartic potential U(Ψ) |
| Def5 | Coherence scalar Ω |
| Def6 | Intentionality vector V |

---

## 4. Derivations

| ID | Result |
|---|---|
| Der1 | Cubic reaction is the negative gradient of the quartic potential |
| Der2 | Precisions are curvatures of U at the wells |
| Der3 | Fixed-point obstruction under natural assignments |
| Der4 | Endocrinal consistency condition from rate matching |
| Der5 | 8 = 4 × dim_{F_2} V_4 |

**Der3 in detail.** Under the natural assignment Π_o = f Ψ_A Ψ_B and
Π_s = f Ψ_B (Ψ_B − Ψ_A), the FEP fixed point
μ* = (Π_o · o + Π_s · η) / (Π_o + Π_s) and the QD-TER posterior well Ψ_B
differ by a term proportional to Ψ_B − Ψ_A. Equality requires Ψ_A = Ψ_B,
which collapses the double-well structure. Alignment holds when the
projection P_s Ψ_B lies on the FEP manifold; this is a codimension-1
condition on the well parameters and is not generic.

---

## 5. Reduction Theorems (Conditional)

| ID | Statement | Status |
|---|---|---|
| RT1 | Local linearized QD-TER dynamics = linearized FEP recognition dynamics | Proven under Axioms G, C |

**Boundary of RT1.** Local in a neighborhood of Ψ_B; not global; not
nonlinear; not unconditional on the published suite.

---

## 6. Conjectures

| ID | Conjecture |
|---|---|
| C1 | Global fixed-point alignment (requires Resolution A or B) |
| C2 | Full nonlinear projected flow = FEP gradient (false away from well) |
| C3 | Parallel transport violations are detectable via ‖∇_X V‖ ≠ 0 |
| C4 | Ω < 1 registers as a dielectric break (proposed bridge) |
| C5 | Riemannian metric on parameter space derived from QD-TER quantities |

---

## 7. Falsification Tests

| ID | Test |
|---|---|
| FT1 | Gap scaling of the reduction error |
| FT2 | Re_ε sweep at fixed gap |
| FT3 | Fibroblast voltage-sensitive dye |
| FT4 | Engine-lock perturbation hysteresis |

---

## 8. Human-Medium Layer — Integer 8

    Axiom / definition (inherited):
      The human-medium layer has exactly 8 residual writing channels,
      given by 8 = 4 × dim_{F_2} V_4 = 4 × 2,
      from the residual waist N_waist = 36.

    Derivation: residual physics suite.
    Human-medium layer: uses the integer; does not prove it.

---

## 9. Summary

| Category | Count |
|---|---|
| Axioms (inherited) | 8 |
| Axioms (modeling) | 11 |
| Definitions | 6 |
| Derivations | 5 |
| Reduction theorems (conditional) | 1 |
| Conjectures | 5 |
| Falsification tests | 4 |


---

## 10. Part V (v10.0) Module Claim Files

Part V keeps its claims in two files, each with its own IDs and claim index. The categories are those of this document.

| File | ID prefix | Axioms (modeling) | Definitions | Derivations | Conjectures | Total |
|---|---|---|---|---|---|---|
| [`finite_descent_claims.md`](finite_descent_claims.md) | FD | 3 | 5 | 1 | 2 | 11 |
| [`language_claims.md`](language_claims.md) | L, LD, LI | 2 | 10 | 0 | 11 | 23 |
| **Part V total** | | 5 | 15 | 1 | 13 | 34 |

Falsification tests FT5–FT10 correspond to Protocols 85–90 of [v10.0](../suite/v10_part5_language_and_descent.md):

| ID | Test |
|---|---|
| FT5 | Speaker–listener iCOH on real dyads (Protocol 85) |
| FT6 | Cross-engine rhythm coupling during speech (Protocol 86) |
| FT7 | Candidate Rank-3 realizations (Protocol 87, mathematical) |
| FT8 | Linguistic exposure and NR3C1 methylation (Protocol 88) |
| FT9 | Lineage-specific chromatin response (Protocol 89) |
| FT10 | Relaxation of language-induced regime shifts (Protocol 90) |
