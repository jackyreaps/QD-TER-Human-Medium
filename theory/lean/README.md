# Lean Skeleton

[`FiniteDescent.lean`](FiniteDescent.lean) is the architectural skeleton of the finite topological descent: discrete rank carriers, the two folds, the composite, the dual residue, and four placeholder conjectures. Its claims layer is [`../finite_descent_claims.md`](../finite_descent_claims.md); the language-side conjecture it stubs (L3) is in [`../language_claims.md`](../language_claims.md).

## Status

- **Draft and conjectural. Not a proof artifact.**
- The file has no imports and targets a Lean 4 toolchain (for example, `lean FiniteDescent.lean`). It has **not been compiled in this repository**; the first compile may need small syntax adjustments.
- The carriers and folds are declared with `axiom`, as structural placeholders. `baseDual` and every `True := by sorry` stand for propositions that do not exist yet.

## Promotion rule

A conjecture is promoted only by replacing its `sorry` with a proof, or with a strengthened proposition tied to the parent ledger objects (ε, μ, the scar, and the 7-channel structure on `BaseResidue`). Do not replace `True` with a statement that is true only because of how it was written.

## What is checked elsewhere

The elementary facts that the narrative relies on, namely the compression bound for surjective folds and the combinatorics of the Fano plane and the [7,4] Hamming code, are checked in [`src/qdter/descent.py`](../../src/qdter/descent.py) and [`tests/test_descent.py`](../../tests/test_descent.py). They are not proved in Lean.
