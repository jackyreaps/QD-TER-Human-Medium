# Notation

Symbols that recur across the suite, with the place where each is defined. Display equations in the documents use LaTeX; some inline symbols in prose still use plain Unicode (for example `Ψ_B`), and they denote the same objects as the entries below. When two documents use a symbol differently, the definition in the document named in the last column governs.

## Dynamics and reduction ([`theory/`](../theory/README.md))

| Symbol | Meaning | Defined in |
|---|---|---|
| $\Psi$ | State of the engine network, one component per engine | [`reduction_fep.md`](../theory/reduction_fep.md) §2 (Axiom D) |
| $\Psi_B$ | Posterior well: a zero of $F$ with positive curvature | [`reduction_fep.md`](../theory/reduction_fep.md) §1–2 |
| $\Psi_A$ | Barrier-top zero of $F$, lying between the wells at $0$ and $\Psi_B$ | [`reduction_fep_derivation.md`](../theory/reduction_fep_derivation.md) §1 |
| $f$ | Positive rate parameter of the cubic reaction | [`reduction_fep.md`](../theory/reduction_fep.md) §2 |
| $F(\Psi,f)$ | Cubic reaction $f\,\Psi(\Psi_A-\Psi)(\Psi-\Psi_B)$; $F=-U'$ | [`reduction_fep.md`](../theory/reduction_fep.md) §2; [`reduction_fep_derivation.md`](../theory/reduction_fep_derivation.md) §1 |
| $L_H$ | Hypergraph Laplacian; its kernel is the slow subspace | [`reduction_fep.md`](../theory/reduction_fep.md) §2 (Axiom S) |
| $\lambda_2$ | Spectral gap of $L_H$ | [`reduction_fep.md`](../theory/reduction_fep.md) §2, §4.3 |
| $M_E$ | Endocrinal matrix; on the slow mode, the scalar gain $m_E$ | [`reduction_fep.md`](../theory/reduction_fep.md) §2 (Axiom C); [`reduction_fep_derivation.md`](../theory/reduction_fep_derivation.md) §0 |
| $P_s$, $\Psi_s$ | Orthogonal projector onto $\ker L_H$, and the slow coordinate $P_s\Psi$ | [`reduction_fep.md`](../theory/reduction_fep.md) §3.1 |
| $\mu$ | Recognition-density mean, identified with $\Psi_s$ | [`reduction_fep.md`](../theory/reduction_fep.md) §2 (Axiom G) |
| $\Pi_o,\ \Pi_s$ | Observation and slow precisions: $f\Psi_A\Psi_B$ and $f\Psi_B(\Psi_B-\Psi_A)$ | [`reduction_fep.md`](../theory/reduction_fep.md) §2 (Axiom G) |
| $G$ | Cognitive glue index $\sqrt{\mathrm{OXTR}\cdot\mathrm{GJ}}$ | [`reduction_fep.md`](../theory/reduction_fep.md) §2 (Axiom C) |
| $\Gamma,\ \Gamma_{\mathrm{eff}}$ | FEP recognition gain; effective rate of the projected dynamics | [`reduction_fep.md`](../theory/reduction_fep.md) §3.1; see [`reduction_fep_derivation.md`](../theory/reduction_fep_derivation.md) §6 for the normalization issue |
| $N_{\mathrm{waist}},\ V_4,\ N_{\mathrm{frames}},\ N_{\mathrm{channels}}$ | Residual waist (36), Klein four-group, frame count (4), channel count (8) | [`residual_integer_8.md`](../theory/residual_integer_8.md) |

## Coupling, load, and the model gradient ([v6.0](../suite/v06_part1_authorship_and_coherence.md))

| Symbol | Meaning | Defined in |
|---|---|---|
| $\kappa_i^{(0)},\ \kappa_i^{\mathrm{eff}}$ | Baseline and effective coupling of engine $i$ | v6.0 §2.1 |
| $L_{ij}\in[0,1]$ | Load on engine $i$ in category $j$ (ancestral, developmental, chronic/acute) | v6.0 §2.1 |
| $\chi_{\mathrm{net}}$ | Net epigenetic balance: inherited plus current load minus current credit | v6.0 §2.3 |
| $G_{\mathrm{consciousness}}$ | Scalar field of the model gradient | v6.0 §3.1 |
| $H(\hat L)$ | Healing operator | v6.0 §3.2 |

## Strategic interaction and return ([v7.0](../suite/v07_part2_structural_foundation.md))

| Symbol | Meaning | Defined in |
|---|---|---|
| $\mathrm{Re}_\varepsilon$ | Dielectric Reynolds number, $\rho_{\mathrm{fluid}}\,v_{\mathrm{phase}}\,L/\mu_{EZ}$ | v7.0 §3.5.3 |
| $\rho_{\mathrm{fluid}},\ v_{\mathrm{phase}},\ L$ | Extracellular-fluid charge density, neural phase-wave velocity, interaction-node dimension | v7.0 §3.5.3 |
| $\mu_{EZ}(\mathrm{OXTR},\mathrm{GJ})$ | EZ-fluid viscosity, a strict inverse function of oxytocin-receptor activation and gap-junction density | v7.0 §3.5.3 |
| $V(x)$ | Debt gauge, built from non-spectral observables | v7.0 §4.2 |
| $r(t)$ | Return rate, $-\tfrac{d}{dt}\log V(x(t))$ | v7.0 §4.3 |
| $\langle r\rangle,\ \lambda_{\mathrm{pert}}$ | Mean return rate and perturbation rate in the stability condition $\langle r\rangle>\lambda_{\mathrm{pert}}+\varepsilon$ | v7.0 §4.4 |
| $r_{\mathrm{social}}$ | Social return rate, bounded by $r_{\mathrm{self}}$, $r_{\mathrm{partner}}$ and $\mathrm{Re}_\varepsilon$ | v7.0 §4.6 |

The code in [`src/qdter/manifold/rheology.py`](../src/qdter/manifold/rheology.py) computes $\mathrm{Re}_\varepsilon$, the glue index, and the strategic topology from these definitions.

## Descent, budget, and gating ([v10.0](../suite/v10_part5_language_and_descent.md))

| Symbol | Meaning | Defined in |
|---|---|---|
| $S_{12},\ S_6,\ S_3$ | Finite state sets of the LedgerCore, ChiralGating, and BaseResidue stages | v10.0 §2.3; [`finite_descent_claims.md`](../theory/finite_descent_claims.md) FD1–FD3 |
| $f_{12\to 6},\ f_{6\to 3}$ | Surjective rank folds (the finite-first form of D2) | v10.0 §2.2; FD4, FD5 |
| $I(Z;W)\le\log_2\lvert S_3\rvert$ | Compression bound of the composite fold | v10.0 §2.3; FD11 |
| `otx_like`, `gbx_like` | Abstract sectors of the dual residue; Otx2 and Gbx2 are candidate labels only | v10.0 §2.5; FD7 |
| $\mu$ | Residual-flux parity; **not yet defined** as a ledger quantity | v10.0 §2.6; FD9 |
| $X,\ Y$ | Macro-ceiling and micro-floor fractions, with $X+Y=1$ | v10.0 §3.2; LD3 |
| $\Sigma$ | Finite alphabet of symbols that gate the fold 6→3 | v10.0 §7.1; L5 |
| $\mathbb{P}^2(\mathbb{F}_2)$ | The Fano plane: 7 points, 7 lines | v10.0 §2.4; checked in `descent.py` |
| LI1 | Transience invariant for language-induced regimes | v10.0 §5.3; [`language_claims.md`](../theory/language_claims.md) |

