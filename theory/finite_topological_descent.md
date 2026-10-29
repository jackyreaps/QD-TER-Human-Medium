# QD-TER Finite Topological Descent

**Structural Memo v1.0** (reformatted for this repository; see Revision notes)

| Field | Value |
|-------|--------|
| **Status** | Draft / conjectural design memo |
| **Domain** | QD-TER core framework · Human-Medium theory |
| **Scope** | Discrete rank folds, dual residue, candidate geometry |
| **Out of scope** | Resileos operations, Path B training, host/API surface |
| **Home** | [`finite_descent_claims.md`](finite_descent_claims.md), [`lean/FiniteDescent.lean`](lean/FiniteDescent.lean), and the narrative in [v10.0](../suite/v10_part5_language_and_descent.md) |
| **Dependencies** | Residual rank folds; $\varepsilon$–golden–primorial ladder; residual-flux parity $\mu$; scar / residual ledger |

---

## 1. Ontological premise (finite-first)

The macroscopic continuum is treated as an **emergent presentation** of an underlying **finite, discrete, chiral skeletal ledger**.

This memo **rejects** continuum-first and Lie-group-down derivations as the primary ontology of QD-TER. Continuous models may appear later as *presentations* or *limits* of discrete structure; they do not define the descent.

**Topological descent** here means progressive **contraction of discrete residual rank** in the transport phase, ending in a localized structural **residue** (scar / base footprint), not a smooth projective map on a continuum manifold.

---

## 2. Descent pipeline: Rank-12 → Rank-6 → Rank-3

Architectural steps are **combinatorial rank folds**, not continuous projections:

```text
  [ LedgerCore ]          Rank-12  unreduced discrete hypervector core
           │
           ▼  fold₁₂₆     residual rank contraction
  [ ChiralGating ]        Rank-6   intermediary waist / chiral channel
           │
           ▼  fold₆₃      ultimate base partition
  [ BaseResidue ]         Rank-3   finite combinatorial skeleton
           ├── otx_like   flexible / projective sector  (label only)
           └── gbx_like   rigid / dual-line sector      (label only)
```

### 2.1 Unreduced core (Rank-12) — `LedgerCore`

- Highest-order discrete state space of the transport phase under this memo.
- Constrained by the $\varepsilon$–golden–primorial ladder (exact binding of constants is **not** fixed in this memo).
- Carries the unreduced residual tracks before waist contraction.

### 2.2 Intermediary waist (Rank-6) — `ChiralGating`

- Intermediate phase-locking / gating channel.
- `fold₁₂₆` contracts Rank-12 → Rank-6: a residual rank fold that collapses half of the active degrees of freedom into a **bounded directional channel**.
- “Chiral” denotes orientation structure native to the ledger; it does **not** introduce continuum circle geometry as foundation.

### 2.3 Base residue (Rank-3) — `BaseResidue`

- Terminal discrete scaffolding of the descent as defined here.
- `fold₆₃` completes contraction Rank-6 → Rank-3 and leaves a **localized topological scar** (residue footprint).
- Further macroscopic continuum language is *read off* this base, not imposed onto it.

**Composite descent (statement only):**

$$
\mathrm{BaseResidue}
\;\leftarrow\;
\mathrm{fold}_{6\to 3}
\;\circ\;
\mathrm{fold}_{12\to 6}
\;(\mathrm{LedgerCore}).
$$

---

## 3. Dual residue after Rank-3

After `fold₆₃`, the base is described as admitting a **dual residual split** into two abstract sectors:

| Label | Role (algebraic) | Biological name (candidate only) |
|-------|------------------|----------------------------------|
| `otx_like` | Flexible / projective-type invariant sector | Fore–midbrain *Otx2*-class language |
| `gbx_like` | Rigid / dual-line invariant sector | Hindbrain *Gbx2*-class language |

**Rules:**

- Algebra dictates the **possibility** of an orthogonal (or otherwise disjoint) partition; biology supplies **names**, not definitions.
- Orthogonality / partition properties are **structural requirements** to be stated precisely once Rank-3 is defined operationally—not theorems of this memo.

---

## 4. Explicit candidate classifications (not locked physics)

| Item | Status in this memo |
|------|---------------------|
| **Fano plane $\mathbb{P}^2(\mathbb{F}_2)$** | Combinatorially suggestive **candidate** for organizing internal 7-channel structure on Rank-3. **Not** unique, **not** verified as the QD-TER base. |
| **Otx2 / Gbx2** | Macroscopic biological **labels** for `otx_like` / `gbx_like`. **Not** the algebraic objects. |
| **$\mu$ gates `fold₆₃`** | **Conjectural** operational rule. Requires a rigorous ledger definition of residual-flux parity $\mu$ before it may constrain the fold axiom. |
| **Seven-channel preservation** under composite fold | **Conjecture** (Lean stub only). |

Anything not listed as a candidate may still be open; silence is not endorsement.

---

## 5. Readiness matrix

| Domain | Ready | Not ready |
|--------|--------|-----------|
| Narrative | Finite-first sequence $12\to 6\to 3\to$ dual residue | Continuum / named Lie group as absolute origin |
| Model honesty | Demotion of Fano / Otx2 / $\mu$-gate to candidates | Promotion into stable QD-TER physics without $\varepsilon,\mu$ binding |
| Lean 4 | Types, fold axioms, `DualResidue` structure, `sorry` theorems | Full proofs; uniqueness of Rank-3 realization |
| Resileos | — | Any coupling to host, Titanos, Path B, or RES-xxx ops docs |

---

## 6. Formal objects (Lean 4 architectural skeleton)

Objects are **discrete types**. Axioms are **structural placeholders**, not verified theorems.

```lean
/-
  QD-TER Finite Topological Descent — architectural skeleton
  Status: draft / conjectural. Not a proof artifact.
-/

axiom LedgerCore : Type       -- Rank-12 unreduced discrete core
axiom ChiralGating : Type     -- Rank-6 intermediary waist
axiom BaseResidue : Type      -- Rank-3 localized base skeleton

/-- Residual rank fold: Rank-12 → Rank-6. -/
axiom fold₁₂₆ : LedgerCore → ChiralGating

/-- Residual rank fold: Rank-6 → Rank-3. -/
axiom fold₆₃ : ChiralGating → BaseResidue

/-- Dual residue: abstract split of a Rank-3 carrier. -/
structure DualResidue (R : Type) where
  otx_like   : Type
  gbx_like   : Type
  orthogonal : otx_like → gbx_like → Prop
  partition  : R → otx_like ⊕ gbx_like

/--
  Conjecture: composite descent preserves internal 7-channel structure
  in the base residue. Unproven; stub only.
-/
theorem preserves_seven_channel_structure :
    ∀ (_core : LedgerCore), True := by
  sorry
```

The refined skeleton, which adds the composite fold and a cross-module conjecture, is [`lean/FiniteDescent.lean`](lean/FiniteDescent.lean).

**Notes for implementers:**

- Replace `True` with a real proposition once “7-channel structure on `BaseResidue`” is defined.
- `orthogonal` should later be strengthened (e.g. mutual exclusion, no shared invariants)—boundary conditions are **out of scope** until Rank-3 is fixed.
- Do not encode $\pi$-circle phase arithmetic as the foundation of `ChiralGating`.

---

## 7. Open work (ordered)

1. **Bind Rank objects** to parent ledger geometry ($\varepsilon$, $N_{\mathrm{saved}}$, scar, rank indices)—definitions, not metaphors.  
2. **Operational $\mu$** — residual-flux parity as a ledger quantity; only then a candidate rule “`fold₆₃` constrained by $\mu$.”  
3. **Boundary conditions** for `DualResidue.orthogonal` and `partition` (mathematical, not biological).  
4. **Candidate tests** for Rank-3 realizations (including but not limited to Fano): checklist of required properties; no uniqueness claim.  
5. Optional: continuum as **presentation functor** *from* discrete base (direction finite → continuum only).

---

## 8. Placement and non-goals

- **Intended home:** Human-Medium / QD-TER theory track (Doc 36–51 line and successors).  
- **Non-goals:** Resileos RES documents, EngineGroup $\kappa$ probes, Titanos hosting, training/NLL gates.  
- **Versioning:** Bump memo version when Rank objects or $\mu$ become definitional; do not silently promote candidates.

---

## 9. Summary

This memo stabilizes a **finite-first topological descent** for QD-TER:

- Rank folds $12\to 6\to 3$ as residual contractions.  
- Dual residue as abstract sectors (`otx_like` / `gbx_like`).  
- Continuum, Fano, and biological names as **candidates or presentations**, not axioms.  
- Lean skeleton for types and folds only; proofs deferred until the ledger objects are locked.

---

## Relation to inherited claims

[`CLAIMS.md`](CLAIMS.md) already lists the hierarchical reduction 12 → 6 → 3 as inherited axiom D2, the residual waist ($N_{\mathrm{waist}}=36$) as D1, the parity group $V_4$ as D3, and the 8-channel sector as D8. This memo is the finite-first reading of D2. Three questions follow and are developed in [v10.0 §2](../suite/v10_part5_language_and_descent.md): how a Rank-3 base relates to the 8-channel sector, whether Rank-6 can be identified with the 36-mode waist, and what sizes the two dual-residue sectors have. The elementary compression bound for a chain of folds and the combinatorial facts about the Fano plane and the [7,4] Hamming code are checked in [`src/qdter/descent.py`](../src/qdter/descent.py).

---

## Revision notes

- **Formatting.** Math delimiters converted from `\( \)` and `\[ \]` to `$ $` and `$$ $$` so that they render on GitHub.
- **Fano plane.** The candidate was written "Fano / $\mathbb{P}^3(\mathbb{F}_2)$". The Fano plane is $\mathbb{P}^2(\mathbb{F}_2)$, with 7 points; $\mathbb{P}^3(\mathbb{F}_2)$ has 15. The label now reads "Fano plane $\mathbb{P}^2(\mathbb{F}_2)$". The later claims file already used the corrected form.
- **Lean.** The carriers were declared with `constant`, which is Lean 3 syntax; they now use `axiom`. The skeleton has not been compiled in this repository.
- No claim was added, removed, or promoted.

**End of structural memo v1.0.**
