# QD-TER Finite Topological Descent — Claims Taxonomy

**Status:** Draft / Conjectural
**Companion documents:**

- [`lean/FiniteDescent.lean`](lean/FiniteDescent.lean)
- [`finite_topological_descent.md`](finite_topological_descent.md) (structural memo v1.0)
- [`language_claims.md`](language_claims.md) (the Otx2/Gbx2 dual-engine claims)
- [v10.0, Part V](../suite/v10_part5_language_and_descent.md)

**Ontology note (Design Invariant):**
The macroscopic continuum is treated as an emergent presentation of a finite discrete chiral ledger. Rank contractions are residual folds, not smooth projections. The continuum is not an input type of this module.

**Relation to [`CLAIMS.md`](CLAIMS.md).** The canonical taxonomy has no "Structural Axiom" category. The two fold axioms below are the finite-first formalization of the inherited reduction D2 (12 → 6 → 3) and are classified as Axiom (modeling). Claim IDs here carry the prefix FD.

---

## Claim index

| ID | Claim | Category |
|---|---|---|
| FD1 | `LedgerCore`: unreduced Rank-12 discrete core | Definition |
| FD2 | `ChiralGating`: Rank-6 intermediary waist | Definition |
| FD3 | `BaseResidue`: Rank-3 localized base skeleton | Definition |
| FD4 | `fold₁₂₆`: Rank-12 → Rank-6 | Axiom (modeling) |
| FD5 | `fold₆₃`: Rank-6 → Rank-3 | Axiom (modeling) |
| FD6 | `fold₁₂₃ = fold₆₃ ∘ fold₁₂₆` | Definition |
| FD7 | `DualResidue`: split of a Rank-3 carrier into `otx_like` and `gbx_like` sectors | Definition |
| FD8 | The composite descent preserves seven-channel structure on `BaseResidue` | Conjecture |
| FD9 | `fold₆₃` respects residual-flux parity μ | Conjecture |
| FD10 | The continuum is not an input type | Axiom (modeling) |
| FD11 | A chain of surjective folds transmits at most $\log_2|S_{\mathrm{out}}|$ bits | Derivation |

---

## 1. Rank Carriers (Definitions — Provisional)

**FD1. Definition (LedgerCore).**
Unreduced Rank-12 discrete hypervector core of the transport phase.
Status: Provisional Definition (placeholder `Type` until bound to parent ledger geometry).

**FD2. Definition (ChiralGating).**
Rank-6 intermediary waist / chiral gating channel.
Status: Provisional Definition.

**FD3. Definition (BaseResidue).**
Rank-3 localized finite combinatorial base skeleton.
Status: Provisional Definition.

---

## 2. Residual Rank Folds

**FD4. Axiom (fold₁₂₆).**
Primary residual rank fold: Rank-12 → Rank-6. It collapses unreduced degrees of freedom into a bounded directional channel.

```lean
axiom fold₁₂₆ : LedgerCore → ChiralGating
```

Status: Axiom (modeling), finite-first ontology. Formalizes the first step of D2.

**FD5. Axiom (fold₆₃).**
Ultimate base partition: Rank-6 → Rank-3. It completes the contraction and leaves a localized topological scar or residue. It may be constrained by residual-flux parity μ once μ is defined in the parent ledger.

```lean
axiom fold₆₃ : ChiralGating → BaseResidue
```

Status: Axiom (modeling), with open dependency on μ. Formalizes the second step of D2.

**FD6. Definition (fold₁₂₃).**
Composite descent Rank-12 → Rank-3.

```lean
def fold₁₂₃ (core : LedgerCore) : BaseResidue :=
  fold₆₃ (fold₁₂₆ core)
```

Status: Definition (derived from the two axioms).

**FD11. Derivation (compression bound).**
If $S_{12}\to S_6\to S_3$ are surjections between finite sets, the output of the composite has at most $|S_3|$ values, so $I(Z;W)=H(W)\le\log_2|S_3|$. The bound uses no assumption about what a rank is. See [v10.0 §2.3](../suite/v10_part5_language_and_descent.md); the linear case is checked in [`tests/test_descent.py`](../tests/test_descent.py).
Status: Derivation (elementary).

---

## 3. Dual Residue Structure

**FD7. Definition (DualResidue).**
Abstract split of a Rank-3 carrier into two invariant sectors after the final fold.

```lean
structure DualResidue (R : Type) where
  otx_like : Type          -- Flexible / projective-type sector
  gbx_like : Type          -- Rigid / dual-line sector
  orthogonal : otx_like → gbx_like → Prop
  partition : R → otx_like ⊕ gbx_like
```

- Biological labels ("Otx2-like", "Gbx2-like") are interpretive names only; they are not algebraic definitions.
- Orthogonality and partition are structural slots; concrete boundary conditions are deferred until Rank-3 is operationally defined.
- The sector sizes are open (see [v10.0 §2.5](../suite/v10_part5_language_and_descent.md)).

Status: Definition.
Cross-reference: candidate mapping, by label only, to the dual-engine bifurcation in [`language_claims.md`](language_claims.md) (`otx_like` ↔ forebrain/midbrain Otx2-lineage engine; `gbx_like` ↔ hindbrain Gbx2-lineage engine). The mapping is a hypothesis; the biological study supplies lineage names, not algebraic objects.

---

## 4. Conjectures

**FD8. Conjecture (preserves seven-channel structure).**
The composite descent `fold₁₂₃` preserves internal 7-channel hypervector structure on the `BaseResidue`. The Fano plane $\mathbb{P}^2(\mathbb{F}_2)$ (or related Rank-3 combinatorial objects) remain candidate realizations only.

```lean
theorem preserves_seven_channel_structure :
    ∀ (_core : LedgerCore), True := by sorry
```

Status: Conjecture.
Priority: High. Replace `True` with a precise proposition once the 7-channel structure on `BaseResidue` is defined. The combinatorial facts about the Fano plane and the [7,4] Hamming code that make it a natural candidate are checked in [`src/qdter/descent.py`](../src/qdter/descent.py); whether it is the QD-TER base is not established.

**FD9. Conjecture (fold₆₃ respects residual-flux parity μ).**
The final fold `fold₆₃` is constrained by residual-flux parity μ. Not formalized until μ is introduced as a ledger quantity in the parent geometry.

```lean
theorem fold₆₃_respects_parity_μ : True := by sorry
```

Status: Conjecture (dependent).

---

## 5. Design Invariants

**FD10. Invariant (continuum not assumed).**
This module takes finite discrete rank carriers as primitive. Continuum presentations are emergent and are not used as input types.

```lean
theorem continuum_not_assumed : True := trivial
```

Status: Axiom (modeling), stated as a design invariant. The Lean theorem is a marker, not content.

---

## 6. Open Bindings (Parent Ledger Dependencies)

The following must be supplied by the parent QD-TER ledger before several conjectures can be promoted:

- the ε–golden–primorial ladder
- residual-flux parity μ
- a precise definition of "7-channel hypervector structure" on Rank-3
- an operational realization of the topological scar or residue left by `fold₆₃`
- concrete orthogonality and partition relations inside `DualResidue`

Two reconciliations are also open and are tracked in [`docs/known_issues.md`](../docs/known_issues.md): the relation between a Rank-3 state set of eight elements and the 8-channel sector (D8), and whether Rank-6 can be identified with the 36-mode waist (D1).

---

**Document Control**
This claims file is the normative taxonomic companion to [`lean/FiniteDescent.lean`](lean/FiniteDescent.lean). All statements above are classified according to the repository's standard epistemic hierarchy. Promotion of any Conjecture requires explicit replacement of the corresponding `sorry` with a proof or a strengthened proposition linked to the parent ledger.

---

## Revision notes

- Claim IDs (FD1–FD11) and the claim index were added; no claim text was removed.
- "Structural Axiom" was mapped to Axiom (modeling) to match [`CLAIMS.md`](CLAIMS.md).
- FD11 (the compression bound) was added from v10.0 §2.3.
- The dual-engine cross-reference was reworded from "directly supports" to "candidate mapping".
- Paths were updated to the repository layout, and a trailing chat sentence was removed.
