# FEP Reduction: Full Derivation

**Status:** Partial. Steps 1–5 below are complete algebraic derivations from the axioms in [`reduction_fep.md`](reduction_fep.md) (checked symbolically). The adiabatic-elimination bound (Step 6), the Cheeger bound, and the Tikhonov constants remain open and are marked as such.
**Companion to:** [`reduction_fep.md`](reduction_fep.md) §3, [`CLAIMS.md`](CLAIMS.md) §5 (RT1).

One point in the specification needs a decision from the author: the rate match in Step 5 holds only under a stated normalization convention. See [§6](#6-matching-condition-and-a-normalization-issue-in-the-specification).

---

## 0. Setting and notation

Let $\Psi\in\mathbb{R}^n$ (here $n=7$, one component per engine) evolve under Axiom D:

$$
\dot\Psi = -L_H\Psi + M_E\,F(\Psi),\qquad F(\Psi)_i = f\,\Psi_i\,(\Psi_A-\Psi_i)(\Psi_i-\Psi_B).
$$

**Standing assumptions.**

- $0<\Psi_A<\Psi_B$ and $f>0$ (the ordering in which $U''(\Psi_B)>0$).
- $L_H$ is symmetric positive semidefinite with a one-dimensional kernel spanned by $\mathbf 1$. The numerical tests confirm this for the seven-engine construction in `spectral.py`; an analytic proof for that specific hypergraph is part of the open Cheeger item below.
- The slow coordinate is $\psi := \tfrac1n\mathbf 1^{\!\top}\Psi$, so that $\Psi_s=P_s\Psi=\psi\,\mathbf 1$ with $P_s=\tfrac1n\mathbf 1\mathbf 1^{\!\top}$.
- The scalar endocrinal gain on the slow mode is
  $m_E := \tfrac1n\,\mathbf 1^{\!\top}M_E\,\mathbf 1$. This is the quantity written $M_E$ in Axiom C.

**Notation warning.** $P_s$ (the kernel projector, dimensionless) and $\Pi_s$ (the slow precision) are different objects. The proof sketch in `reduction_fep.md` §3.2 uses $P_s$ where the rate formulas need $\Pi_s$; §6 below explains why this matters.

---

## 1. Potential, wells, and precisions

**Lemma 1.** Define
$$
U(\Psi)=f\left(\frac{\Psi^4}{4}-\frac{(\Psi_A+\Psi_B)\Psi^3}{3}+\frac{\Psi_A\Psi_B\Psi^2}{2}\right).
$$
Then:

1. $F=-\,U'$, so each component of $F$ is the negative gradient of $U$.
2. The zeros of $F$ are $0,\ \Psi_A,\ \Psi_B$.
3. The curvatures at those zeros are
$$
U''(0)=f\Psi_A\Psi_B=\Pi_o,\qquad
U''(\Psi_B)=f\Psi_B(\Psi_B-\Psi_A)=\Pi_s,\qquad
U''(\Psi_A)=-f\Psi_A(\Psi_B-\Psi_A)<0 .
$$
4. $\Pi_o+\Pi_s=f\Psi_B^{2}$.

*Proof.* Differentiating, $U'(\Psi)=f\Psi(\Psi-\Psi_A)(\Psi-\Psi_B)=-F(\Psi)$, which gives (1) and (2). Then $U''(\Psi)=f\,(3\Psi^2-2(\Psi_A+\Psi_B)\Psi+\Psi_A\Psi_B)$; evaluating at the three zeros gives (3), and (4) follows by adding the first two. $\square$

So $0$ and $\Psi_B$ are the two wells, $\Psi_A$ is the barrier top, and the precisions in Axiom G are exactly the well curvatures. This closes the claim in `reduction_fep.md` §4.1 that the precisions are "derived as curvatures of $U$ at the two wells."

---

## 2. Projection onto the slow subspace (Step 1)

Apply $P_s$ to Axiom D. Because $L_H$ is symmetric with $L_H\mathbf 1=0$, we have $\mathbf 1^{\!\top}L_H=0$ and hence $P_sL_H=0$. Therefore, **exactly**,
$$
\dot\psi=\tfrac1n\,\mathbf 1^{\!\top}M_E\,F(\Psi).
$$

Write $\Psi=\psi\mathbf 1+\Psi_f$ with $\Psi_f\perp\mathbf 1$. Since $F$ acts componentwise, a Taylor expansion about $\psi\mathbf 1$ gives
$$
F(\Psi)=F(\psi)\,\mathbf 1+F'(\psi)\,\Psi_f+O(\|\Psi_f\|^2),
$$
where $F'(\psi)\,\Psi_f$ denotes the componentwise product. Substituting,
$$
\dot\psi=m_E\,F(\psi)+r,\qquad r=\tfrac1n\,\mathbf 1^{\!\top}M_E\,F'(\psi)\,\Psi_f+O(\|\Psi_f\|^2).
$$

The remainder $r$ is the "$O(\varepsilon)$" term of the theorem. It vanishes when the fast component $\Psi_f$ vanishes, and bounding it is Step 6.

---

## 3. Linearization about the posterior well (Step 2)

$F$ is a cubic polynomial, so its expansion about $\Psi_B$ is exact. With $\delta=\psi-\Psi_B$,
$$
F(\Psi_B+\delta)=-\Pi_s\,\delta\;-\;f(2\Psi_B-\Psi_A)\,\delta^{2}\;-\;f\,\delta^{3}.
$$
In particular $F(\Psi_B)=0$ and $F'(\Psi_B)=-U''(\Psi_B)=-\Pi_s=-f\Psi_B(\Psi_B-\Psi_A)$.

Hence
$$
\dot\delta=-\,m_E\,\Pi_s\,\delta+O(\delta^{2})+r,
\qquad\text{so}\qquad
\Gamma_{\mathrm{eff}}=m_E\,U''(\Psi_B)=m_E\,\Pi_s .
$$

**Size of the linear neighborhood.** The quadratic term is small compared with the linear term when
$$
|\delta|\ \ll\ \frac{\Pi_s}{f(2\Psi_B-\Psi_A)}=\frac{\Psi_B(\Psi_B-\Psi_A)}{2\Psi_B-\Psi_A}.
$$
For $\Psi_A=0.2,\ \Psi_B=1$ this scale is $0.8/1.8\approx0.44$. This is a scale estimate for the cubic nonlinearity only. It does not bound the adiabatic-elimination error, so the "linear neighborhood size" item in `reduction_fep.md` §5 stays open until Step 6 is done.

---

## 4. Effective rate under Axiom C (Step 3 and Step 4)

Axiom C sets $m_E=\dfrac{G\,\Psi_B}{\Psi_B-\Psi_A}$, with $G=\sqrt{\mathrm{OXTR}\cdot\mathrm{GJ}}$. Using $\Pi_s=f\Psi_B(\Psi_B-\Psi_A)$,
$$
\Gamma_{\mathrm{eff}}=m_E\,\Pi_s=\frac{G\Psi_B}{\Psi_B-\Psi_A}\cdot f\Psi_B(\Psi_B-\Psi_A)=G\,f\,\Psi_B^{2}.
$$

---

## 5. FEP side (Step 5)

With identity observation map $g(\mu)=\mu$, the Laplace-approximated free energy is
$$
\mathcal F(\mu)=\tfrac12\Pi_o(o-\mu)^2+\tfrac12\Pi_s(\mu-\eta)^2,
\qquad
\dot\mu=-\Gamma\,\partial_\mu\mathcal F .
$$
Its curvature is $\Pi_o+\Pi_s=f\Psi_B^2$ (Lemma 1.4), so the linearized recognition dynamics is
$$
\delta\dot\mu=-\,\Gamma\,(\Pi_o+\Pi_s)\,\delta\mu=-\,\Gamma\,f\Psi_B^{2}\,\delta\mu .
$$

---

## 6. Matching condition and a normalization issue in the specification

Comparing §4 and §5, with $\mu=\psi$:
$$
\Gamma_{\mathrm{eff}}=G f\Psi_B^2
\qquad\text{versus}\qquad
\Gamma\,(\Pi_o+\Pi_s)=\Gamma f\Psi_B^2 ,
$$
so the rates agree **if and only if $\Gamma=G$**.

The specification instead defines the recognition gain as $\Gamma=\Pi_s\,G$ (Axiom G text; `gain()` in `generative_model.py`). With that definition the FEP rate is $\Pi_s\,G\,f\Psi_B^2$, which exceeds the projected QD-TER rate by exactly the factor $\Pi_s$ (checked symbolically: the ratio is $f\Psi_B(\Psi_B-\Psi_A)$).

The existing test `test_axiom_C_rate_matching` closes this gap by writing
`Gamma_eff = Pi_s * M_E_norm * U_pp`. That extra $\Pi_s$ does not come from the projection: for the unit kernel projector $P_s$ it is $1$, as in §2. The theorem statement in `reduction_fep.md` §3.1 (with $\Gamma_{\mathrm{eff}}=P_s M_E U''(\Psi_B)$) and the match in its §3.2 step 4 therefore do not both hold as written.

Three consistent resolutions are available. Each changes the specification, so the choice belongs to the author:

| Option | Change | Effect |
|---|---|---|
| A | Define the recognition gain as $\Gamma:=G$ | Rates match exactly; update Axiom G, `gain()`, and the test |
| B | Keep $\Gamma=\Pi_sG$ and set $m_E=G f\Psi_B^2$ | Rates match; Axiom C changes form |
| C | Keep both and declare a precision-weighted slow projection $P_s^{\Pi}:=\Pi_s$ on the slow mode | Rates match; adds an explicit modeling postulate to Axiom G |

Until one is adopted, the conditional reduction theorem should be read as holding up to this normalization.

---

## 7. Error term (Step 6): open

**Needed.** A bound of the form $\|r\|\le C_1/\lambda_2$, where $\lambda_2$ is the spectral gap of $L_H$.

**Outline.** The fast component obeys
$$
\dot\Psi_f=-L_H\Psi_f+(I-P_s)M_E F(\Psi),
$$
so, by singular perturbation (Tikhonov) arguments, $\Psi_f$ relaxes on the time scale $1/\lambda_2$ to a quasi-steady value of size $O(\|(I-P_s)M_E F\|/\lambda_2)$. Inserting this in the expression for $r$ in §2 gives the claimed $1/\lambda_2$ scaling. The constant $C_1$ depends on Lipschitz bounds for $F$ and $M_E$ over the region visited, and has not been computed.

## 8. Cheeger bound for the specific hypergraph: open

To be supplied: a proof that for the seven-engine incidence structure the Cheeger constant satisfies $h(\mathcal H)\ge 4/(n\cdot\mathrm{diam}(\mathcal H))$, and the resulting spectral-gap bound
$$
\lambda_2\ \ge\ \frac{4}{n\cdot\mathrm{diam}(\mathcal H)}\bigl(1-\mathbb D\,|M_E|_F\bigr).
$$

## 9. Tikhonov constants: open

To be supplied: explicit $C_1$, $C_2$ from the actual $F$ and $M_E$, computed against the parameter ranges in `rheology.py`.

---

## 10. Numerical verification

| Result | Test in `tests/test_reduction_fep.py` |
|---|---|
| $F=-U'$ (Lemma 1.1) | `test_cubic_is_negative_gradient_of_quartic` |
| Kernel is one-dimensional and contains the constant mode (§0) | `test_kernel_is_one_dimensional`, `test_kernel_contains_constant_mode` |
| $L_H\mathbf 1=0$ (§2) | `test_L_annihilates_constants` |
| Rate match (§6) | `test_axiom_C_rate_matching` (currently encodes the $\Pi_s$-weighted convention, Option C) |

Still planned: kernel-coefficient tracking inside a small neighborhood of $\Psi_B$, gap scaling of the residual, and a separate $\mathrm{Re}_\varepsilon$ sweep at fixed gap.
