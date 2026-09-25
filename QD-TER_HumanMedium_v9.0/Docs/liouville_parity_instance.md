

The Liouville Parity Instance: A Companion Note to v9.0 Part IV

σ_parity on the Integer Lattice and the Verified Multiples-of-Four Case

Status: Public note. Companion to QD-TER_HumanMedium_v9.0. Anchored to §8 (The Arithmetic Instance).

What this note is. The residual generator σ_parity from Theory/Residual_integer_8.md acts on the integer lattice as the even/odd partition. This note identifies its arithmetic realization, states the verified Lean case, and clarifies what is and is not proved. The note is a pointer; it does not re-derive the mathematics.

---

Section 1: The Liouville Function

The arithmetic realization of σ_parity is the Liouville function:

\lambda(n) = (-1)^{\Omega(n)},

where Ω(n) counts prime factors with multiplicity.

· λ(n) = +1 when n has an even number of prime factors (with multiplicity)
· λ(n) = −1 when n has an odd number of prime factors

The condition λ(n) = −1 is the odd-parity class. Every prime p has λ(p) = −1. Many composites also have λ(n) = −1 (for example, n = 12 = 2² · 3, Ω(12) = 3, λ(12) = −1). The odd-parity class is therefore strictly larger than the primes.

Section 2: The Dirichlet Series

The Liouville function is completely multiplicative, so its Dirichlet series has an Euler product:

\sum_{n=1}^\infty \frac{\lambda(n)}{n^s} = \prod_p \left(1 + \frac{1}{p^s}\right)^{-1} = \frac{\zeta(2s)}{\zeta(s)}.

The identity ζ(2s)/ζ(s) is standard. Its analytic structure connects to the Riemann zeta function:

· The poles of ζ(2s)/ζ(s) come from the zeros of ζ(s). Given the Riemann Hypothesis, these are on the line Re(s) = 1/2 — the critical line.
· The zeros come from the zeros of ζ(2s) and the pole of ζ(s) at s = 1.

The relevant connection for the framework is that the critical line Re(s) = 1/2 appears in the analytic structure of the Liouville Dirichlet series. This is the same locus as the waist caustic from the physics suite (Theory/Consolidated_specification.md, object D6). The identification is not an analogy: the Liouville function is the arithmetic realization of σ_parity on the integer lattice, and the critical-line locus is where its analytic structure references.

Section 3: The Verified Case

Theorem (conditional). Every positive multiple of 4 is the sum of two positive integers, each with Liouville value −1.

The result is established by a Lean formalization maintained in the CaptainSude/Liouville-Goldbach-Multiples-of-Four repository (v1.0.0, 2026). The formalization checks the deduction from an external theorem — cited in the repository as Mangerel (2024), a correlation bound for the Liouville function in International Mathematics Research Notices — to the multiples-of-4 result.

The Lean development verifies the deduction (descent from larger multiples to smaller ones, scaling, and the finite base cases) but treats Mangerel's theorem as an external input. It is not a fully self-contained formal proof of the multiples-of-4 case.

Section 4: What This Proves and What It Does Not

What the repository establishes. A formalized deduction from an external arithmetic theorem (Mangerel's) to the statement that every positive multiple of 4 decomposes as a sum of two positive integers with Liouville value −1.

What the repository does not claim. The repository does not claim to prove Goldbach's conjecture. The Liouville formulation replaces "prime" with "λ = −1", which is strictly weaker: every prime has λ = −1, but many composites also do. A decomposition into two λ = −1 integers does not imply a decomposition into two primes.

What this note claims. That σ_parity — the residual generator from Theory/Residual_integer_8.md §1 — has a concrete arithmetic realization whose additive structure has been formalized for a nontrivial infinite class. This is the closest published case to a verified instance of the parity-additive structure that the physics suite places structurally.

Section 5: Structural Mapping to v9.0

v9.0 §8 identifies σ_parity as the residual generator from the physics suite. This note supplies the arithmetic realization and the verified case. The mapping:

v9.0 concept Liouville realization
σ_parity generator λ(n) = (−1)^Ω(n)
Even/odd partition of pulse index λ(n) = +1 / λ(n) = −1
Critical-line locus (waist caustic) Re(s) = 1/2 as pole line of ζ(2s)/ζ(s) (given RH)
Parity-additive structure Sum decompositions into λ = −1 components

Section 6: Epistemic Status

The identification σ_parity ↔ Liouville function is definitional. The verified case is a formalized deduction from an external theorem, not an unconditional proof. The framework does not depend on the multiples-of-4 case being true; it depends on the identification, which is a choice of realization.

Per Theory/CLAIMS.md, this note does not introduce new claims. It provides a realization and a citation for the σ_parity generator that v9.0 §8 references.

Citations

Mangerel, A. (2024). On the Liouville function and its correlations. International Mathematics Research Notices.

CaptainSude (2026). Liouville–Goldbach: Multiples of Four (v1.0.0). GitHub release. https://github.com/CaptainSude/Liouville-Goldbach-Multiples-of-Four

Relationship to v9.0

v9.0 §8 states the arithmetic instance and cites this note for the details. The instance is not load-bearing for any other claim in v9.0. It is provided as an illustration of how σ_parity realizes concretely on the integer lattice.

---
