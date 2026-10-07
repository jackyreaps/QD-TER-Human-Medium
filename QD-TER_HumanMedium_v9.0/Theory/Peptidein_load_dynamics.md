# Peptidein Load Dynamics: Number–Location Criticality and Sigma-1 Clearance

**Status:** Active. Sub-document of the v9.0 mechanism layer.
**Governed by:** `Theory/Consolidated_specification.md`, `Theory/CLAIMS.md`.
**Dependency:** Inherits the 8-channel residual sector (D8) from `Theory/Residual_integer_8.md` and the endocrine-chromatin pipeline from `QD-TER_HumanMedium_v9.0`. Does not re-derive either.

---

## 0. How to read this sub-document

v9.0 established the endocrine-chromatin axis: pulsatile endocrine signals are written onto chromatin through an 8-channel residual sector, producing sustained conditions. That document modeled the write vector as a linear function of integrated endocrine state and left the *substrate* of the 8 channels unspecified.

This sub-document supplies two things:

1. **The substrate.** The 8 channels are populated by peptideins — small microproteins translated from non-coding open reading frames. Their fast turnover and channel-specific localization make them the physical medium of the write vector.

2. **The failure mechanism.** The system does not enter the Valley because peptidein load is high. It enters the Valley because peptidein load is **concentrated at binding sites that cannot flex** and **mislocalized away from the sites that keep chromatin open**. The failure is a *conjunction* of Number (how much) and Location (where).

The Sigma-1 Gateway is specified here as the **clearance operator** that acts on both failure modes. v8.0 introduced Sigma-1 operationally; this sub-document gives it mathematical form.

---

## 1. Substrate: The Peptidein Layer

### 1.1 Empirical grounding

The TransCODE Consortium's 2026 consensus established:

- ~25% of 7,264 analyzed non-canonical open reading frames (ncORFs) produce protein-level evidence.
- ~1,785 **peptideins** detected across 95,520 proteomics experiments; most under 50 amino acids.
- 3,116 ncORF-derived peptides preferentially presented on HLA class I.
- 51 ncORFs with pan-essential knockout phenotypes, including **OLMALINC**.

The term "peptidein" was codified by the consortium to describe microproteins whose functional potential remains indeterminate — a gray zone between demonstrated translation and defined function.

### 1.2 Channel topology

The 8-channel residual sector is inherited from the physics suite (D8). This sub-document assigns each channel a functional topology based on the empirical distribution of ncORF-encoded peptides:

| Channels | Topology | Empirical Anchor |
|---|---|---|
| π₁–π₄ | Surface-expressed "glue" peptideins | Transmembrane enrichment in ncORF microproteins |
| π₅–π₇ | Secreted immune-interface peptideins | 3,116 HLA-I-presented ncORF peptides |
| π₈ | Chromatin-associated structural anchor | OLMALINC: pan-essential, chromosomal looping, cell-cycle regulation |

---

## 2. Load Dynamics

### 2.1 The 8-channel state vector

$$\vec{W}_\pi(t) = [\pi_1(t), \pi_2(t), \ldots, \pi_8(t)]^\top \in \mathbb{R}^8_{\geq 0}$$

Each component is a peptidein concentration. The vector is the physical realization of the 8-channel write vector.

### 2.2 Leaky-kernel accumulation

$$P_i(t) = \int_0^t e^{-\gamma_i(t-\tau)} \cdot \Phi_i\big(\Delta_{be}(\tau), Re_\epsilon(\tau)\big) \, d\tau + I_{load}$$

- $\gamma_i$: channel-specific degradation rate. Peptideins are small and unstable; half-lives are on the order of hours. Glue channels turn over fastest; the chromatin-associated channel turns over slowest.
- $\Phi_i$: non-linear activation. Sinusoidal in $Re_\epsilon$ because gap-junction coupling has phase dependence. Modulated by bioelectric decoupling $\Delta_{be}$.
- $I_{load}$: inherited epigenetic constraint on the non-coding landscape. Encoded by ORBL conservation scores across clades.

### 2.3 Number–Location criticality

**This is the central contribution of this sub-document.**

#### 2.3.1 The Number Problem

Each channel has a finite binding-site capacity $B_i$. Define the saturation fraction:

$$\sigma_i = \frac{P_i}{B_i}$$

The system-level density criticality is the **local** maximum, not the total:

$$\sigma_{total} = \max_i \sigma_i$$

A single saturated channel can lock a chromatin loop. At $\sigma_i > 1$, excluded-volume effects physically restrict chromatin flexing at that locus. The nuclear interior is packed at ~300 mg/ml; additional molecular load at a saturated locus produces enhanced attractive interactions that trap chromatin-interacting proteins.

The total $\sum P_i$ is the wrong measure — it conflates channels with different capacities.

#### 2.3.2 The Location Problem

Peptideins meant for one channel can accumulate in another. Define the ectopic shift as the total-variation distance from the optimal distribution:

$$L_{error} = \frac{1}{2} \sum_i \left| \frac{P_i}{\sum_j P_j} - w_i^{expected} \right|$$

When $L_{error} > L_{crit}$, the population has redistributed away from its design topology. Two specific failure modes:

- **Immune ectopic accumulation (π₅–π₇):** immune markers bind chromatin-associated loci, triggering a false-flag response and locking the system in defense mode.
- **Structural displacement (π₈):** the OLMALINC anchor is displaced from its chromatin-looping targets, impairing cell-cycle regulation.

#### 2.3.3 The critical surface

The two failure modes are independent. Their conjunction defines the Valley.

```
                    Location Error (L_error)
                         Low            High
                    ┌─────────────┬─────────────┐
              Low   │    RIDGE    │  TOPOLOGY   │
   Density          │  (Flow)     │   ERROR     │
   (σ_total)        │             │             │
                    ├─────────────┼─────────────┤
              High  │  DENSITY    │  COMPOUND   │
                    │  CRITICAL   │  FAILURE    │
                    │             │  (Valley)   │
                    └─────────────┴─────────────┘
```

---

## 3. Landscape Mapping

### 3.1 Ridge (Flow State)

$\sigma_{total} \le 1$ and $L_{error} \le L_{crit}$. Peptideins are both within binding capacity and correctly distributed. Chromatin can flex. Adaptation is available.

### 3.2 Valley (Compound Failure)

$\sigma_{total} > 1$ and $L_{error} > L_{crit}$. Chromatin is jammed at saturated loci and mis-addressed at ectopic loci. The $\mathcal{R}$-operator cannot access the synchron point.

### 3.3 Abyss (Hyper-Fluid Break)

Glue peptidein density falls below the minimum for cognitive glue ($\sum_{i=1}^{4} P_i < 0.25$). Gap-junction resistance collapses; the array loses directivity. This is a density failure in the opposite direction: depletion, not saturation.

---

## 4. Sigma-1 Clearance Operator

Sigma-1R is an ER-resident chaperone that translocates to the nuclear envelope under cellular stress, where it recruits chromatin-remodeling factors. In the load-dynamics model, it is the **mode-specific clearance operator** $\hat{\Sigma}$.

### 4.1 Two modes

**Mode A — Degradation (Number correction).** When diagnosis is `DENSITY_CRITICAL`, Sigma-1 accelerates $\gamma_i$ on **saturated channels only**. This reduces number without disturbing the rest of the distribution.

**Mode B — Retrafficking (Location correction).** When diagnosis is `TOPOLOGY_ERROR`, Sigma-1 does not degrade. It re-traffics: a partial adjustment of the population vector toward $w^{expected}$.

### 4.2 The operator

$$\hat{\Sigma}: \vec{W}_\pi \mapsto \vec{W}_\pi'$$

$$\vec{W}_\pi' = \vec{W}_\pi - \alpha \cdot \vec{\gamma}_{sat} \odot \vec{W}_\pi + \beta \cdot (\vec{w}^{expected} - \vec{w}^{actual}) \odot \vec{W}_\pi$$

where $\alpha$ is the degradation gain, $\beta$ is the retrafficking rate, and $\odot$ is element-wise product. The first correction term acts only where $\sigma_i > 1$; the second acts globally toward the expected distribution. Compound failure engages both.

### 4.3 Biological mapping

| Load-dynamics operation | Sigma-1R biology |
|---|---|
| Detect saturated channels | ER stress sensing via unfolded protein response |
| Accelerate degradation | Chaperone-mediated ERAD |
| Re-traffick ectopic peptideins | Chaperone-assisted re-localization to chromatin targets |
| Chromatin-associated action | Translocation to nuclear envelope, recruitment of chromatin remodelers |

---

## 5. Code Architecture

Implementation: `src/manifold/peptidein_load.py`.

**Dependency invariant.** This module does **not** import from `rheology.py`. It accepts `Re_epsilon` and `bio_decoupling` as scalars, consistent with the design invariant of `Endocrine_chromatin.py`. It may be imported by that module or used independently.

**Integration point.** `PeptideinLoad.compute_write_vector()` is called **after** `leaky_integrate()` and **before** `write_channels()`. `Sigma1Gateway.detect_and_respond()` runs between the peptidein update and the chromatin write.

**Channel count invariant.** The `PeptideinLoad` constructor rejects any channel count other than the inherited 8.

---

## 6. Falsification Protocols

**PE-PLD.A — Number over Location.** In a multi-organism array under high-field bioelectric stimulation, onset of collective directivity loss (N² → 0) must correlate with **local binding-site saturation** ($\max_i \sigma_i > 1$), not with total load $\sum P_i$. If directivity loss tracks total load independent of distribution, the Number–Location distinction is falsified.

**PE-PLD.B — Sigma-1 mode specificity.** Sigma-1R knockdown must prevent recovery from `TOPOLOGY_ERROR` without preventing recovery from `DENSITY_CRITICAL`. If knockdown blocks both equally, the two-mode operator is falsified.

**PE-PLD.C — OLMALINC anchor.** Inactivation of the Channel 8 anchor (OLMALINC translation frame) must produce an immediate catastrophic drop in array gain, with collective directivity falling to baseline stochastic noise within Δt < 180 s.

**PE-PLD.D — Inherited load.** ORBL conservation scores must predict the $I_{load}$ parameter across channels. If $I_{load}$ shows no ORBL correlation, the inherited-load model is falsified.

---

*Document Class: Mechanism-layer sub-document*
*Companion to `QD-TER_HumanMedium_v9.0`*
*Verified via Pytest: `tests/Test_peptidein_load.py`*
