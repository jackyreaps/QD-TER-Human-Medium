# Theory

Formal specifications and derivations behind the v9.0 mechanism layer. Every claim here is labeled by epistemic status in [`CLAIMS.md`](CLAIMS.md). Everything in this folder is conditional on the physics suite supplying the residual structures (the waist, V₄, the four frames, the waist-mode projector, and the 8-channel sector); see [`consolidated_specification.md`](consolidated_specification.md) §5.3.

## Suggested reading order

The order below is the adoption order given in [`consolidated_specification.md`](consolidated_specification.md) §5.4.

| # | Document | Role |
|---|---|---|
| 1 | [`CLAIMS.md`](CLAIMS.md) | Claims taxonomy: axiom, definition, derivation, reduction theorem, conjecture, falsification test |
| 2 | [`residual_integer_8.md`](residual_integer_8.md) | The 8-channel count, inherited from the residual waist |
| 3 | [`reduction_fep.md`](reduction_fep.md) | Conditional local reduction to FEP recognition dynamics (axioms and theorem) |
| 4 | [`reduction_fep_derivation.md`](reduction_fep_derivation.md) | Step-by-step derivation for #3 (partial; open items marked) |
| 5 | [`consolidated_specification.md`](consolidated_specification.md) | How the theory documents fit together |
| 6 | [`non_dual_adaptation.md`](non_dual_adaptation.md) | Conjectural adaptation layer, orthogonal to the FEP reduction |
| 7 | [`finite_topological_descent.md`](finite_topological_descent.md) | Finite-first reading of D2: rank folds 12 → 6 → 3 and the dual residue (memo v1.0) |
| 8 | [`finite_descent_claims.md`](finite_descent_claims.md) | Claims for the finite descent (FD1–FD11) |
| 9 | [`language_claims.md`](language_claims.md) | Claims for language and the dual engine (L0–L11, LD1–LD10, LI1) |
| — | [`lean/`](lean/README.md) | Lean 4 skeleton of the finite descent (uncompiled) |
| — | [`peptidein_load_dynamics.md`](peptidein_load_dynamics.md) | Number–Location criticality and Sigma-1 clearance (sub-document of the v9.0 mechanism layer) |

## Notation

Symbols are collected in [`docs/notation.md`](../docs/notation.md).

## Related code

[`src/qdter/manifold/spectral.py`](../src/qdter/manifold/spectral.py), [`generative_model.py`](../src/qdter/manifold/generative_model.py), and [`peptidein_load.py`](../src/qdter/manifold/peptidein_load.py) implement parts of these specifications, and [`tests/test_reduction_fep.py`](../tests/test_reduction_fep.py) checks them.
