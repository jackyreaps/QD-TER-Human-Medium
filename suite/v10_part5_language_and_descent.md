# QD-TER Human-Medium v10.0

## The Human Belt — Part V: Language as a Gate Between the Global and the Local

### Finite Topological Descent, Compression, and the Dual Engine

**Status:** Working draft. Fifth part of the Human-Medium framework. Governed by [`theory/consolidated_specification.md`](../theory/consolidated_specification.md), [`theory/CLAIMS.md`](../theory/CLAIMS.md), [`theory/finite_topological_descent.md`](../theory/finite_topological_descent.md), and the two claims files [`theory/finite_descent_claims.md`](../theory/finite_descent_claims.md) and [`theory/language_claims.md`](../theory/language_claims.md). Claims that exceed established physiology are classified as Conjectures and carry the tier labels of v9.0 Section 12.

> **How to read this document.** This is the fifth part of the QD-TER Human-Medium framework. Part I (v6.0) covers conscious authorship and the coherence hierarchy. Part II (v7.0) covers the structural foundation: the P-V-C triad, the ℛ-operator, and the dielectric Reynolds number. Part III (v8.0) covers the operational regimen. Part IV (v9.0) covers the endocrine–chromatin axis, phase-space reconstruction, and hypergraph coordination. Part V asks how a finite, discrete descent from a global state to a local residue can carry compression, and proposes that language is the instrument that gates it. Section 1 sorts every statement by evidential tier; read it first.
>
> **Precondition.** As in v9.0, everything here is conditional on the future physics suite. The 12 → 6 → 3 hierarchical reduction (D2), the residual waist (D1), the parity group $V_4$ (D3), and the 8-channel sector (D8) are inherited, not derived. This part gives D2 a finite-first reading and asks what it implies for a communicating organism.
>
> **What this part does not claim.** It does not claim that any single study validates the framework. The 2026 finding on the two-origin brain is used as a source of names and a testable analogy, not as proof. No result in this part depends on the block-universe complexity conjecture (L1, Section 3.3).

---

## Abstract

The macroscopic continuum is treated as a presentation of a finite, discrete, chiral ledger. Descent from the global to the local is then a sequence of combinatorial rank folds, 12 → 6 → 3, ending in a localized residue that splits into two abstract sectors. Because each fold is a surjection between finite sets, the descent is a compression: at most $\log_2|S_3|$ bits survive the composite fold. This part develops that reading, observes a candidate structure at Rank-3 (the syndrome space of the [7,4] Hamming code, which has eight elements and carries the Fano plane), and proposes that language acts as a bounded-capacity gate on the final fold. It grounds the proposal in established findings on oscillatory speech processing and speaker–listener neural coupling, reconstructs the organism's phase space with delay embedding, and maps the abstract dual residue to the two progenitor lineages (Otx2 and Gbx2) that a 2026 Stanford-led study reports for the vertebrate brain. A transience invariant separates fast gating from slow residue writing. Speculative extensions, including a pineal tryptamine shunt and an adrenochrome failure witness, are retained as labeled Conjectures with their evidential status stated. Six falsification protocols (85–90) are specified, and the mathematical statements are checked in code.

**Keywords:** finite topological descent, rank folds, compression, symbolic gate, language, Hamming code, Fano plane, dual-engine bifurcation, Otx2, Gbx2, speech oscillations, inter-brain coupling, Takens embedding, transience invariant, falsification protocols

---

## Section 0: Inheritance and Scope

**Inherited from earlier parts and the theory layer:**

| Object | Source |
|---|---|
| Hierarchical reduction 12 → 6 → 3 (D2); residual waist $N_{\mathrm{waist}}=36$ (D1); parity group $V_4$ (D3); 8-channel sector (D8) | [`theory/CLAIMS.md`](../theory/CLAIMS.md) §1, [`theory/residual_integer_8.md`](../theory/residual_integer_8.md) |
| Control layer, P-V-C triad, $\mathrm{Re}_\varepsilon$, strategic landscape (Ridge, Valley, Abyss) | v6.0, v7.0 |
| Pulsatile endocrine signal, chromatin writing, Takens reconstruction, leaky kernel, hypergraph coordination | v9.0 Sections 1–4 |
| Epistemic tiers | v9.0 Section 12 |

**Added here:**

1. A finite-first reading of D2 as compression (Section 2).
2. A budget form of the shutter bookkeeping, $X+Y=1$ (Section 3).
3. A literature-grounded account of language as a multi-timescale modulator (Section 4).
4. Phase-space reconstruction applied to language development (Section 5).
5. The dual-engine mapping (Section 6) and a candidate symbolic-gate model (Section 7).
6. Pathological modes, speculative extensions, and collective attenuation (Sections 8–10).
7. Protocols 85–90 (Section 11).
8. An executable check of the mathematics (Section 2.7), a timescale hierarchy with a transience invariant that separates gating from residue writing (Section 5.3), and a synthesis of the pieces (Section 7.4).

---

## Section 1: Epistemic Map

Tiers follow v9.0 Section 12. A statement carries the highest tier it can support, and no more.

| Tier | Meaning | Statements in this part |
|---|---|---|
| **ESTABLISHED** | Peer-reviewed literature | Delta, theta, and gamma oscillations track the multi-timescale structure of speech (Giraud & Poeppel 2012). Speaker–listener neural coupling exists and vanishes when communication fails (Stephens et al. 2010); EEG hyperscanning shows interbrain synchronization during speech (Pérez et al. 2017). In mouse embryos, the forebrain and midbrain derive from Otx2-expressing progenitors and the hindbrain from Gbx2-expressing progenitors, with different chromatin configurations (Dundes, Jokhai, et al. 2026). DMT binds the sigma-1 receptor (Fontanilla et al. 2009). Delay embedding reconstructs attractors under stated conditions (Takens 1981; Sauer et al. 1991). |
| **INFERENCE** | Follows from the cascade plus established results | A surjective fold cannot transmit more than $\log_2|S_{\mathrm{out}}|$ bits (Section 2.3), and the combinatorial facts of Section 2.4 hold (checked, Section 2.7). Speech requires cooperation between forebrain planning and hindbrain control of breathing, face, tongue, and throat. |
| **NOVEL CLAIM** | QD-TER-specific and testable | Language gates the final fold (L5). Language couples the two engines (L3, L4). The gamma-band latch rate sets the shutter (L2). Gating is transient and writing is persistent (LI1). |
| **HYPOTHESIS (labeled)** | Conjecture in the sense of `CLAIMS.md` | L1 to L11 (Section 11.1). Includes the pineal shunt (L8) and the adrenochrome witness (L9). |
| **OWED** | Future scope | Operational definition of residual-flux parity $\mu$; Rank-3 realization; calibration of the iCOH gate on real dyads. |

---

## Section 2: Finite Topological Descent as Compression

### 2.1 Finite-first premise

The macroscopic continuum is treated as an emergent presentation of an underlying finite, discrete, chiral ledger. Continuous models may appear later as presentations or limits of discrete structure; they do not define the descent. Descent here means progressive contraction of discrete residual rank, ending in a localized structural residue (a scar or base footprint), not a smooth projection on a continuum manifold. The full statement, with the Lean 4 architectural skeleton, is in [`theory/finite_topological_descent.md`](../theory/finite_topological_descent.md).

### 2.2 The three stages

```text
  [ LedgerCore ]          Rank-12   unreduced discrete core
           │
           ▼  fold 12→6   residual rank contraction
  [ ChiralGating ]        Rank-6    intermediary waist
           │
           ▼  fold 6→3    ultimate base partition
  [ BaseResidue ]         Rank-3    finite combinatorial skeleton
           ├── otx_like   flexible / projective sector  (label only)
           └── gbx_like   rigid / dual-line sector      (label only)
```

The composite descent is

$$
\mathrm{BaseResidue}\;\leftarrow\;\mathrm{fold}_{6\to 3}\circ\mathrm{fold}_{12\to 6}\,(\mathrm{LedgerCore}).
$$

This is the finite-first reading of the inherited reduction D2. "Chiral" denotes orientation structure native to the ledger and does not introduce circle geometry as a foundation.

### 2.3 The descent is a compression (Derivation, elementary)

Let $S_{12}$, $S_6$, $S_3$ be the finite state sets of the three stages, and let $f_{12\to 6}:S_{12}\to S_6$ and $f_{6\to 3}:S_6\to S_3$ be surjective folds. For any random state $Z$ on $S_{12}$ with output $W=f_{6\to 3}(f_{12\to 6}(Z))$, the output has at most $|S_3|$ values, so

$$
I(Z;W)=H(W)\;\le\;\log_2|S_3| .
$$

At most $\log_2|S_3|$ bits survive the descent, however much structure the core carries. Each fold is therefore a lossy encoder with a fixed capacity, and "compression" in this part means exactly this bound. The bound makes no assumption about what a "rank" is.

### 2.4 Candidate: rank as $\mathbb{F}_2$-dimension, and a structure at Rank-3

> **Status: Candidate (not locked).** The memo leaves "rank" undefined. The reading below is a proposal for the open work in Section 12.

Suppose rank counts $\mathbb{F}_2$-dimension, so that $|S_k|=2^k$. Then $|S_{12}|=4096$, $|S_6|=64$, and

$$
|S_3|=2^3=8 .
$$

This equals the inherited count of 8 residual channels (D8). Two cautions apply.

1. **Tension with D1.** The same reading gives $|S_6|=64$, whereas D1 gives a 36-mode waist. If $S_6$ is identified with the waist, the reading fails at Rank-6, and it can at best describe Rank-3.
2. **Different derivations.** D8 is derived as $8=N_{\mathrm{frames}}\times\dim_{\mathbb{F}_2}V_4=4\times 2$ (see [`theory/residual_integer_8.md`](../theory/residual_integer_8.md)). That $|\mathbb{F}_2^3|=8$ is a numerical coincidence until a structural reason links the two counts. The warning in that file against writing $8=4\times(2\times 2)$ still applies.

**Observation (mathematics).** The set $\mathbb{F}_2^3$ has eight elements: zero and seven nonzero vectors. The seven nonzero vectors are the points of the Fano plane $\mathbb{P}^2(\mathbb{F}_2)$. They are also the columns of the parity-check matrix of the [7,4] Hamming code, so the syndrome of a single-bit error in a seven-bit word is one of those seven vectors, and the zero syndrome means no error. The weight-3 codewords of that code correspond to the seven lines of the Fano plane. Eight outcomes, seven channels plus "none", is the structure the memo's "7-channel" language points to.

*Correction carried from the memo.* The Fano plane is $\mathbb{P}^2(\mathbb{F}_2)$ with 7 points. $\mathbb{P}^3(\mathbb{F}_2)$ has 15 points and is a different object.

### 2.5 The dual residue

After the final fold the base is described as admitting a split into two abstract sectors:

| Label | Role (algebraic) | Biological name (candidate only) |
|---|---|---|
| `otx_like` | Flexible, projective-type invariant sector | Fore–midbrain Otx2-class lineage |
| `gbx_like` | Rigid, dual-line invariant sector | Hindbrain Gbx2-class lineage |

Algebra dictates the possibility of a disjoint partition; biology supplies names, not definitions. The sector sizes are open. Two candidates are noted:

- The three nonzero elements of $V_4$ split $1+2$ once one involution is distinguished. The parity generator $\sigma_{\mathrm{parity}}$ of v9.0 Section 8 is a natural choice, and the stabilizer of that choice swaps the other two.
- $\mathbb{F}_2^3=\{0\}\cup\{\text{seven points}\}$ splits $1+7$.

Neither is asserted. Boundary conditions for orthogonality are out of scope until Rank-3 is fixed.

### 2.6 Candidate classifications (not locked physics)

| Item | Status |
|---|---|
| Fano plane $\mathbb{P}^2(\mathbb{F}_2)$ | Combinatorially suggestive candidate for the 7-channel structure on Rank-3. Not unique; not verified as the QD-TER base. |
| Otx2 / Gbx2 | Macroscopic biological labels for `otx_like` / `gbx_like`, not the algebraic objects. |
| $\mu$ gates the fold 6→3 | Conjectural. Requires a rigorous ledger definition of residual-flux parity $\mu$. |
| Seven-channel preservation under the composite fold | Conjecture (Lean stub only). |

### 2.7 Executable check of the mathematics

The elementary statements of this section are checked in [`src/qdter/descent.py`](../src/qdter/descent.py) and [`tests/test_descent.py`](../tests/test_descent.py). Run `python -m examples.finite_descent` for a printed summary.

| Statement | Checked result |
|---|---|
| A chain of surjective linear folds $\mathbb{F}_2^{12}\to\mathbb{F}_2^6\to\mathbb{F}_2^3$ transmits at most $\log_2 8=3$ bits | Surviving bits equal the rank, at most 3, for random chains |
| The composite of such a chain has exactly eight outputs | Eight distinct outputs over all $2^{12}$ inputs |
| The syndrome space of the [7,4] Hamming code has eight elements | Syndromes $\{0,\dots,7\}$ over all 128 words |
| The seven nonzero syndromes are the points of $\mathbb{P}^2(\mathbb{F}_2)$, and every two points lie on exactly one line | Seven points, seven lines, each pair on one line |
| The weight-3 codewords of the code are the seven Fano lines | The two sets are equal |
| Syndrome decoding corrects every single-bit error | All 16 codewords, all 7 positions, plus the error-free case |
| $\mathbb{P}^3(\mathbb{F}_2)$ has 15 points, not 7 | $2^4-1=15$ |

These are mathematical facts and say nothing about biology. What stays open is whether the Rank-3 base of the ledger is any of these objects (L5, Protocol 87).

---

## Section 3: Shutter Bookkeeping as a Budget Split

### 3.1 Normalization

**Axiom 0 (modeling).** The universe, taken as an undivided whole, is assigned the value 1. The identity $x=x$ is a tautology; the assignment $=1$ is a choice of unit. Everything below is measured as a fraction of that unit.

### 3.2 The budget split $X+Y=1$

**Definition.** For a localized interaction, let $X\in[0,1]$ be the macro-ceiling fraction (the causal horizon the interaction reaches) and $Y\in[0,1]$ the micro-floor fraction (the smallest resolvable semantic unit). Then

$$
X+Y=1 ,\qquad Y=\sim\!X:=1-X .
$$

A coherent linguistic token fixes the pair $(X,Y)$. The phrase "zero-drift tension" names the condition that neither fraction can move without the other. In the descent of Section 2, the macro-to-micro direction is the direction in which $X$ is exchanged for $Y$.

### 3.3 What the block universe does and does not give (Conjecture L1)

In the relativistic block universe, time does not flow and spacetime is a fixed four-dimensional geometry. An earlier draft of this part drew a further consequence: that problem and solution coexist at fixed coordinates, so that no duration separates a question from its answer and $\mathrm{P}=\mathrm{NP}$.

**Status: Conjecture L1, not used in any derivation here.** The inference does not follow from the block-universe premise. Complexity classes are defined by how the resources of an algorithm scale with input size, and a fixed spacetime geometry does not change that scaling. Aaronson (2005) surveys physical proposals for solving NP-complete problems, including relativistic time dilation and closed timelike curves, and expresses the view that none will work; he argues that the hardness of NP-complete problems may be a useful constraint on physical theories. L1 is therefore retained only as a conjecture about how the shutter picture might relate to computation, and it is not a grounding axiom.

---

## Section 4: Language as a Multi-Timescale Modulator

Within this architecture, language is not a symbolic module floating above biology. It is a high-bandwidth, multi-timescale modulator of the dielectric medium, acting through four routes: it directs sustained attentional bias (the control layer, v6.0); it shapes bioelectric pattern memory across the P-V-C triad; it writes, through repetition and social reinforcement, into the slow chromatin layer (v9.0); and it phase-locks organisms into dyads, groups, and institutions.

### 4.1 Established: speech is parsed on nested timescales (ESTABLISHED)

Giraud and Poeppel (2012) review evidence that delta, theta, and gamma oscillations are specifically engaged by the multi-timescale, quasi-rhythmic structure of speech and organize incoming information into units of matching temporal granularity. They relate phrasal, syllabic, and (sub)phonemic units to delta, theta, and gamma respectively. The account is contested in detail: Obleser, Herrmann, and Henry (2012) argue against over-weighting the speech envelope and entrainment relative to top-down processes.

The interface mapping used in this framework is an interpretation layered on that literature:

| Interface (Human Belt) | Linguistic layer | Timescale in the literature | Tier |
|---|---|---|---|
| Proprioceptive | Early vocalization coupled to bodily state and fascial feedback | Not specified by the cited work | Inference |
| Vestibular | Prosody, rhythm, intonation locked to breath, heart-rate variability, and postural tone | Delta–theta (phrasal, syllabic) | Inference |
| Cortical | Lexical and syntactic matching that retunes the lower interfaces | Theta–gamma nesting | Inference |

### 4.2 Established: speakers and listeners couple (ESTABLISHED)

Stephens, Silbert, and Hasson (2010) recorded fMRI from speakers and listeners during natural storytelling and found that the speaker's activity is spatially and temporally coupled with the listener's, that the coupling vanishes when communication fails, and that greater anticipatory coupling goes with greater comprehension. Pérez, Carreiras, and Duñabeitia (2017) used EEG hyperscanning to show interbrain synchronization of oscillations during oral narratives, partly mediated by speech-to-brain tracking and partly by the interaction itself. These findings are correlational. They establish that inter-organism coupling accompanies language; they do not establish that coupling causes comprehension or that it takes the form proposed here. The gate in [`src/qdter/manifold/eeg_hyperscan.py`](../src/qdter/manifold/eeg_hyperscan.py) is designed for exactly this setting, and Protocol 85 calibrates it on real dyads.

### 4.3 Language and the shutter rate (Conjecture L2)

The earlier draft proposed that the execution rate of the "biological camera" is driven by gamma-band synchronization at 30–80 Hz. The mainstream account above ties gamma to fine temporal granularity within nested hierarchies and assigns syllable- and phrase-scale parsing to slower rhythms. The reading of gamma as a frame rate is therefore a **Conjecture (L2)**, not an established mapping.

### 4.4 Language and the chromatin residue (Conjecture L10)

Social experience can leave epigenetic marks: in rodents, variation in maternal behavior is associated with differences in methylation of the glucocorticoid receptor gene promoter and in stress responses (Weaver et al. 2004). Whether linguistic input, specifically, writes into chromatin residue is **Conjecture L10**. It extends v9.0 Section 2 from endocrine input to language, and the language-specific effect would have to be separated from general social stress (Protocol 88).

---

## Section 5: Individual Language Development and Reconstructed Phase Space

Language acquisition is modeled as the progressive refinement of the organism's capacity to fix a coherent token at a chosen $(X,Y)$ and to hold it across the three interfaces: early sensorimotor vocalization (proprioceptive), prosody and rhythm (vestibular), and lexical and syntactic matching (cortical).

### 5.1 Delay embedding

The geometry is not imposed. It is reconstructed from a one-dimensional stream $x(t)$ of pulsatile endocrine or neural data, sampled at step $\tau$, by forming

$$
\mathbf{X}(t)=\bigl(x(t),\,x(t+\tau),\,\dots,\,x(t+(d-1)\tau)\bigr).
$$

Takens' theorem states that for a generic observation of a smooth dynamical system on an $n$-dimensional manifold, an embedding dimension $d\ge 2n+1$ gives an embedding of the manifold (Takens 1981). For an attractor of box-counting dimension $D$, $d>2D$ suffices (Sauer, Yorke, and Casdagli 1991). The reconstructed trajectory $\mathcal{M}$ has dynamical invariants, namely Lyapunov exponents and fractal dimensions, that serve as descriptors of systemic state.

**Practical caveat.** The theorem assumes noise-free data and a generic observable. Physiological series are short, noisy, and nonstationary, so reconstruction is exploratory: $\tau$ and $d$ must be chosen from the data (for example by mutual information, Fraser and Swinney 1986, and false nearest neighbors, Kennel, Brown, and Abarbanel 1992), and invariants carry wide uncertainty.

### 5.2 Regimes of the reconstructed manifold

The manifold is classified by the eigenvalues $\lambda_i$ of the local Jacobian $\mathbf{J}$. This is the same regime table as v9.0 Section 3, restated for language:

| Regime | Eigenvalue condition | Reading for language |
|---|---|---|
| Stable node | $\mathrm{Re}(\lambda_i)<0$, $\mathrm{Im}(\lambda_i)=0$ | Aperiodic rest; fast recovery from perturbation |
| Stable focus | $\mathrm{Re}(\lambda_i)<0$, some $\mathrm{Im}(\lambda_i)\neq0$ | Healthy pulsatility; linguistic forms stay phase-locked to the ordered cascade (Ridge residence) |
| Limit cycle | Isolated periodic orbit | Entrainment to the 24-hour cycle |
| Strange attractor | Positive Lyapunov exponent | Allostatic fracture state; the leaky kernel fails to clear historical noise |

### 5.3 Timescales and the transience invariant (LI1)

A language-induced state can persist in two different ways, and the descent picture separates them. The fold gate of Section 7 acts once per use and is fast. The residue that the fold leaves, the topological scar of the memo, accumulates and is slow. A claim that the two timescales are well separated is the invariant below.

| Timescale | Value | Role in this part |
|---|---|---|
| Gamma | about 30–80 Hz | Conjectured latch rate (L2) |
| Theta, delta | about 4–8 Hz, 0.5–4 Hz | Syllable- and phrase-scale parsing (Giraud and Poeppel 2012) |
| Ultradian | about 90 min | Pulsatile endocrine writing step (v9.0) |
| Circadian | 24 h | Light-entrained reference |
| Seasonal and longer | months and up | Slowest light-entrained reference |

**Invariant LI1 (modeling axiom).** Language-induced regimes and symbolic-interface states are transient relative to the light-entrained timescale. Once the input ceases, a regime induced by language relaxes toward its pre-exposure state within about one circadian cycle.

**Corollary (testable).** A shift that persists across several circadian cycles after a mild, brief exposure is not gating. It is evidence of residue writing (L10). The leaky memory kernel of v9.0 Section 3 supplies the formalism: transient regimes correspond to kernel components with decay time well under 24 h, and writing corresponds to the slow components. Protocol 90 tests the corollary.

---

## Section 6: The Dual-Engine Bifurcation

### 6.1 What the study reports

A Stanford Medicine-led study (Dundes, Jokhai, et al.; senior author Loh; *Nature Neuroscience*, 18 September 2026) reports, from mouse embryos at gastrulation, two progenitor populations: one expressing Otx2 that forms the forebrain and midbrain, and one expressing Gbx2 that forms the hindbrain. The populations are mutually exclusive from the earliest stages. The anterior and posterior neural ectoderm have different chromatin configurations that lock each progenitor into its fate. The authors used the distinction to derive human hindbrain motor neurons from pluripotent stem cells, and report the same two-origin pattern in chicken, zebrafish, and acorn worms. Loh summarizes the interpretation: "evolution took two existing neural systems and pushed them together spatially" (Stanford Medicine news release, 18 September 2026).

The release describes the forebrain as handling language, consciousness, and abstract reasoning, and the hindbrain as controlling breathing, sleeping, heartbeat, and hunger, together with the muscles of the face, tongue, and throat that affect speech and swallowing. That functional division is the release's description of general neuroanatomy. It is not a result of the study. The study does not describe either lineage as flexible or rigid.

### 6.2 Mapping to the dual residue (Candidate)

| Abstract sector | Lineage label | QD-TER functional reading (hypothesis) |
|---|---|---|
| `otx_like` | Otx2 (forebrain and midbrain) | Projective, flexible: higher-order cognition, language, frame regulation |
| `gbx_like` | Gbx2 (hindbrain) | Rigid, dual-line: autonomic and motor survival functions |

The flexible/rigid characterization is a QD-TER hypothesis. The study supplies the lineage names and the chromatin separation, and nothing more.

```text
        [ GASTRULATION: PARALLEL PROGENITOR LINEAGES ]
                          │
          ┌───────────────┴───────────────┐
          ▼                               ▼
   [ Otx2 LINEAGE ]                [ Gbx2 LINEAGE ]
   distinct chromatin              distinct chromatin
   mutually exclusive              mutually exclusive
          │                               │
          ▼                               ▼
   [ FOREBRAIN / MIDBRAIN ]        [ HINDBRAIN / BRAINSTEM ]
   language, reasoning,            breathing, heartbeat, sleep,
   frame regulation                hunger, face/tongue/throat
          │                               │
          └──────────────┬────────────────┘
                         ▼
        [ coupled in speech production and comprehension ]
```

### 6.3 Language as coupling between the engines (Conjectures L3, L4)

Speech production plainly requires both systems: forebrain planning and comprehension, and hindbrain control of the breath and of the muscles of the face, tongue, and throat (INFERENCE from the release's functional description). The researchers describe the two systems as now almost operating as one. The QD-TER claims go further:

- **L3.** Language is the high-bandwidth channel that couples the `otx_like` and `gbx_like` engines. Cortical speech-related rhythms and brainstem-driven respiratory and orofacial rhythms stay phase-related during speech.
- **L4.** A breakdown of that coupling produces a discontinuous change (a bifurcation) in the reconstructed manifold $\mathcal{M}$.

L3 is tested by Protocol 86 and L4 by the manifold classification of Section 5.2.

---

## Section 7: Symbols as Gates (Candidate Formalization)

> **Status: Candidate (not locked).** The memo conjectures that residual-flux parity $\mu$ gates the final fold but leaves $\mu$ undefined. This section states one way a symbol system could play that role. It is a model, not a derivation.

### 7.1 A gated fold

Let $\Sigma$ be a finite alphabet of symbols. A **gated fold** is a family of surjective folds $\{f^{\sigma}_{6\to 3}\}_{\sigma\in\Sigma}$ from $S_6$ to $S_3$, where the symbol $\sigma$ selects which fold is applied. By Section 2.3 the descent still transmits at most $\log_2|S_3|$ bits, and the gate itself conveys at most $\log_2|\Sigma|$ bits per use. A symbol system is then a bounded-capacity channel that decides which local residue a global state is written into.

### 7.2 Syndrome decoding as an analogy (Conjecture L5)

Under the candidate of Section 2.4, $S_3\cong\mathbb{F}_2^3$ is the syndrome space of the [7,4] Hamming code. A syndrome selects which of seven positions to correct, or none. The analogy for gating is direct: a short symbol selects which of seven channels is written, with "none" as the eighth outcome. **Conjecture L5:** the Rank-3 base realizes this syndrome space, and symbolic gating acts as syndrome decoding. The conjecture inherits both cautions of Section 2.4 (the tension with D1 and the unproven link to D8) and is tested at the mathematical level by Protocol 87.

### 7.3 Language as compression: the mainstream framing

The idea that language is shaped by pressure for efficient, compressed communication is a mainstream position in cognitive science: Gibson et al. (2019) review evidence from the lexicon through syntax that natural language reflects a pervasive pressure for communicative efficiency, using tools from information theory. The QD-TER proposal differs in locating the compression in a finite ledger descent and in making the symbol a physical gate. The overlap is the information-theoretic framing, not the mechanism.

### 7.4 How the pieces fit

```text
  [ global identity, unit budget  X + Y = 1 ]                 Section 3
                     │
                     │  fold 12→6→3: compression, at most log2|S3| bits
                     ▼
            [ BaseResidue, Rank-3 ] ◄──── gate σ ∈ Σ selects fold 6→3   (L5, Section 7)
              │                │                    ▲
              ▼                ▼                    │ symbols, speech
        [ otx_like ]     [ gbx_like ]               │ multi-timescale oscillations (Section 4)
     (Otx2 lineage)    (Gbx2 lineage)               │
              │                │                    │
              └─── language couples the two (L3, L4) ─────┘
                     │
                     ▼
     Ridge (X+Y balanced)  ·  Valley (Y-dominant)  ·  Abyss (X-dominant)   Section 8
                     │
        gating is transient (LI1)  ·  residue writing is persistent (L10)    Section 5.3
```

Read from the top: a finite global state is compressed through two folds into a small residue that splits into two sectors. Language is the channel that carries symbols into the final fold and couples the sectors. How the coupled system sits relative to the budget $X+Y=1$ determines its regime, and whether a regime is transient or written is a question of timescale.

---

## Section 8: Pathological Modes and Temporal Slippage (Conjectures L6, L7)

Sustained linguistic input that is intense and partially resonant with the ordered cascade can degrade the shutter. Metabolic exhaustion, membrane leakage, and inflammatory cascades compromise cellular dielectric barriers, and the shutter rate drifts relative to the cascade's reference rate. The "universal tick" of the earlier draft is a metaphor for that reference rate and is not operational until a measurable definition is supplied. Two directional profiles result, matching the Valley and Abyss of the strategic landscape (v7.0):

- **The Valley (retrograde slip, $Y$-dominance; L6).** Frozen partial resonance. The system over-indexes on historical micro-coordinates $Y$, fails to clear old data, and lets past traumatic instances leak forward as noise. Strategic rigidity rises, and the `gbx_like` engine freezes into hyper-rigid postural and vocal tone.
- **The Abyss (anterograde slip, $X$-dominance; L7).** Overloaded symbolic saturation lets the predictive `otx_like` engine outrun grounding. The system stretches toward the macro-boundary $X$ without sufficient $Y$, producing compulsive projection and hallucinatory noise.

```text
                [ THE SHUTTER AXIS ]
              Stable balance: X + Y = 1
                        │
      ┌─────────────────┴─────────────────┐
      ▼                                   ▼
[ RETROGRADE SLIP ]               [ ANTEROGRADE SLIP ]
  Y-dominance (Valley)              X-dominance (Abyss)
      │                                   │
      └─────────────────┬─────────────────┘
                        ▼
              [ catastrophic threshold ]
```

Both profiles are measurable in principle through the quantities already specified: bioelectric coherence, $\mathrm{Re}_\varepsilon$, strategic topology, and the regime of the reconstructed manifold.

---

## Section 9: The Pineal Shunt and the Adrenochrome Witness (Conjectures L8, L9)

These two extensions are the least tested claims in this part. They are kept as labeled Conjectures so that the evidential status can be stated plainly: neither has been tested, and the studies cited here address neighboring questions, not the proposed functions.

**L8: the pineal temporal shunt.** The conjecture is that the pineal gland and its tryptamine matrix act as a phase-preserving temporal cushion, with binding at the sigma-1 gateway expanding processing capacity during intense linguistic states.

- *Supported:* DMT binds the sigma-1 receptor and acts as an agonist (Fontanilla et al. 2009).
- *Supported in rats:* the brain can synthesize and release DMT at extracellular concentrations comparable to canonical monoamines (Dean et al. 2019).
- *Bearing on the source, not the function:* in the same study, cortical extracellular DMT was similar in rats with and without a pineal gland, and transcripts of the biosynthetic enzyme were found in cortex, pineal gland, and choroid plexus. This constrains where brain DMT comes from. It does not test the proposed buffering function, which no cited study has examined.
- *Untested:* whether any pineal or tryptamine system acts as a phase-preserving buffer, and any function of endogenous DMT in human language processing. A test would manipulate sigma-1 signaling or pineal output during a high-load linguistic task and measure phase stability (for example iCOH or theta–gamma coupling).

**L9: the adrenochrome flashpoint witness.** The conjecture is that when symbolic saturation overwhelms the buffer, adrenochrome appears as a high-frequency, localized witness of the resulting decompression cascade, with cortisol dynamics, HRV complexity, inflammatory cytokines, and $\mathrm{Re}_\varepsilon$ shifts as low-frequency downstream echoes.

- *Background:* adrenochrome is an oxidation product of epinephrine. The Hoffer–Osmond hypothesis (1952) proposed it as a *cause* of psychosis and was not sustained: independent studies failed to replicate the reported treatment effects, and others who tried adrenochrome did not report psychedelic effects (see Dyck 2010 for the history; Encyclopaedia Britannica for a summary). That is a different claim from L9. A marker role does not require psychoactivity, so this history neither supports nor refutes the witness conjecture.
- *Untested:* nothing cited here measures adrenochrome in the proposed role, and this document cites no validated in-vivo assay for it. A test needs such an assay, or a measurable proxy (for example validated catecholamine-oxidation markers), sampled around the onset of decompensation.
- *Association note:* adrenochrome is also the subject of widely circulated unfounded claims. Nothing in this document relies on them.

Neither L8 nor L9 is used by any other section.

---

## Section 10: Frames and Collective Attenuation (Conjecture L11)

### 10.1 Frames

The Gnosis frame (see [`adjacent/gnosis_frame.md`](../adjacent/gnosis_frame.md)) and any competing interpretive frame act as higher-order linguistic regulators: they bias which moves are legible as true, safe, aligned, or anomalous, and so which trajectories are reinforced into residue. Frames are adjacent to the formal theory and can be swapped without changing the dielectric and chromatin mechanics.

### 10.2 The macro filter

At the scale of large social constructions, language operates less on meaning than on network topology. Three mechanisms are proposed, with the first two connected to established models:

- **Proximity cascade.** Nodes match states only with immediate neighbors; above a critical density the local signal overwrites the agent's independent boundary condition, and individual variance is dissipated as stress and friction.
- **Information-cascade thresholds.** Once a critical share of local nodes adopt a linguistic vector, the remaining nodes tip. Threshold models of collective behavior (Granovetter 1978) and information-cascade models (Bikhchandani, Hirshleifer, and Welch 1992) formalize this. In the present vocabulary, the individual's $Y$ is absorbed into the macro-ceiling $X$.
- **Feedback-loop saturation (Conjecture L11).** When the latency between action and reaction approaches zero, individual shutter cycles are bypassed, and the construction acts as a low-pass filter admitting only degraded consensus.

Language development is thereby the multi-scale entrainment of the Human-Medium into basins of attraction, individual and collective. Entrainment quality (Ridge, Valley, or Abyss) is measurable in principle through bioelectric coherence, endocrine–chromatin dynamics, inter-brain synchrony, strategic topology, and the reconstructed manifold.

---

## Section 11: Claims, Tests, and Protocols

### 11.1 Conjectures introduced in this part

| ID | Conjecture | Depends on | Protocol |
|---|---|---|---|
| L1 | The block-universe picture implies a collapse of the P/NP distinction at the level of the shutter. Not used elsewhere | — | none |
| L2 | The linguistic latch rate lies in the gamma band (30–80 Hz) and sets the shutter rate | §3, §4.3 | 85 |
| L3 | Language couples the `otx_like` and `gbx_like` engines; cortical speech rhythms and brainstem-driven respiratory and orofacial rhythms stay phase-related | §6 | 86, 89 |
| L4 | Breakdown of cross-engine linguistic coupling produces a bifurcation of the reconstructed manifold | §5.2, §6.3 | 86 |
| L5 | The Rank-3 base realizes the syndrome space of the [7,4] Hamming code; symbolic gating acts as syndrome decoding | §2.4, §7 | 87 |
| L6 | The Valley is $Y$-dominance with `gbx_like` freezing | §8 | 85, 89 |
| L7 | The Abyss is $X$-dominance with `otx_like` runaway | §8 | 85, 89 |
| L8 | The pineal tryptamine matrix acts as a temporal shunt via the sigma-1 gateway | §9 | none |
| L9 | Adrenochrome is a localized failure witness of the decompression cascade | §9 | none |
| L10 | Repeated linguistic input writes into chromatin residue | §4.4, §5.3 | 88, 90 |
| L11 | Zero-latency feedback bypasses individual shutter cycles and acts as a low-pass filter | §10.2 | none |

L1, L8, L9, and L11 have no protocol in this part. Protocols for them would require operational definitions that do not yet exist.

The IDs are those of [`theory/language_claims.md`](../theory/language_claims.md), which also lists the Definitions (LD1–LD10) and the invariant LI1; the finite-descent claims (FD1–FD11) are in [`theory/finite_descent_claims.md`](../theory/finite_descent_claims.md). The canonical counts are in [`theory/CLAIMS.md`](../theory/CLAIMS.md) §10. Protocol 90 tests LI1 and bears on L10.

### 11.2 Falsification protocols

Protocol numbering continues from v9.0 Section 10 (Protocols 79–84).

### Protocol 85: Speaker–Listener iCOH on Real Dyads

**Objective:** Test whether the band-integrated iCOH of [`eeg_hyperscan.py`](../src/qdter/manifold/eeg_hyperscan.py) separates comprehended from non-comprehended speech, and calibrate its threshold on real recordings (see [`docs/known_issues.md`](../docs/known_issues.md), item 1). Bears on L2, L6, L7.

**Methodology:** EEG hyperscanning of speaker–listener dyads during narrative speech, with two listener conditions: a story in the listener's language and the same story in an unfamiliar language (the contrast used by Stephens et al. 2010). Compute iCOH per band (delta, theta, gamma) with 5 s Welch segments and phase-randomized surrogates.

**Metric:** surrogate-corrected iCOH in the comprehended condition minus the unfamiliar-language condition. Set the gate threshold at a 5% false-positive rate on the unfamiliar-language dyads. **Falsifier:** no surrogate-corrected difference; or gamma-band iCOH carries no more information about comprehension than theta-band iCOH (against L2).

### Protocol 86: Cross-Engine Rhythm Coupling During Speech

**Objective:** Test L3 and L4.

**Methodology:** Simultaneous EEG, respiratory belt, surface EMG over orofacial muscles (or microphone envelope), and heart-rate recording during speech production and listening. Perturbation arm: paced breathing at a rate mismatched to spontaneous speech rhythm.

**Metric:** within-person phase coupling (iCOH) between cortical speech-envelope tracking and the respiratory and orofacial rhythms, surrogate-corrected; change in coupling, in envelope tracking, and in the reconstructed manifold regime under perturbation. **Falsifier:** no coupling beyond surrogate, or no effect of perturbation on any measure.

### Protocol 87: Candidate Rank-3 Realizations (mathematical)

**Objective:** Test L5 and the open reading of Section 2.4.

**Methodology:** For each candidate (the syndrome space $\mathbb{F}_2^3$ with the Fano structure, a $V_4$-based $\mathbb{P}^1(\mathbb{F}_2)$ candidate, and others), check: (i) the state count against D8; (ii) the existence of surjective folds from a Rank-6 candidate consistent with D1; (iii) a precise statement of "seven-channel preservation"; (iv) boundary conditions for the dual residue. Formalize in Lean 4 once the definitions are fixed. The combinatorial facts about the Fano candidate are already checked in code (Section 2.7); items (i)–(iv) are not.

**Metric:** the set of candidates satisfying (i)–(iii) together. **Falsifier:** no candidate satisfies all three, in which case the finite-first reading of D2 needs revision.

### Protocol 88: Linguistic Exposure and NR3C1 Methylation (design only)

**Objective:** Test L10.

**Methodology:** Longitudinal cohort with quantified speech input (for example wearable audio sampling), NR3C1 promoter methylation, and controls for stress, socioeconomic factors, and sleep. Pre-register the analysis. The established analog is the rodent maternal-behavior result of Weaver et al. (2004).

**Metric:** association between speech-input measures and methylation after controls. **Falsifier:** no association after controls. Ethical review is required for any work with children.

### Protocol 89: Lineage-Specific Chromatin Response

**Objective:** Test whether the `otx_like` and `gbx_like` labels correspond to a functional difference, using the cell systems of Dundes et al. (2026). Bears on L3, L6, L7.

**Methodology:** Derive forebrain-like (Otx2-lineage) and hindbrain motor-neuron (Gbx2-lineage) cultures from human pluripotent stem cells following the published protocol. Expose both to ultradian-pulsed and to constant glucocorticoid at matched total dose. Measure chromatin accessibility (ATAC-seq) at NR3C1-bound sites.

**Metric:** the lineage-by-pattern interaction in accessibility change. The QD-TER prediction, from the flexible/rigid labels, is a larger pulsed-versus-constant difference in the `otx_like` lineage than in the `gbx_like` lineage. **Falsifier:** no interaction, or the opposite ordering.

### Protocol 90: Relaxation of Language-Induced Regime Shifts (design only)

**Objective:** Test the transience invariant LI1 and separate gating from residue writing (L10).

**Methodology:** Within-subject design with a mild, brief, ethically approved exposure to sustained high-intensity linguistic load (for example a timed rapid verbal task or an emotionally evocative narrative), and a matched neutral control. Measure heart-rate-variability complexity, the cortisol awakening response, dyadic iCOH during a standard conversation, and the regime of the reconstructed manifold at baseline, immediately after, and at 24 h, 72 h, and 7 d.

**Metric:** time course of each measure relative to baseline and to the control condition. **Falsifier:** no relaxation toward baseline within about one circadian cycle after a mild exposure (against LI1), or no measurable shift at all (nothing to relax). A shift that persists across the 72 h and 7 d points is interpreted as evidence of writing, not as a failure of LI1. Ethical review is required, and exposures must be mild and reversible.

---

## Section 12: Open Work (ordered)

1. **Bind the rank objects** to parent ledger geometry ($\varepsilon$, $N_{\mathrm{saved}}$, scar, rank indices) with definitions, not metaphors.
2. **Define $\mu$ operationally** as a ledger quantity, and only then state the rule "the fold 6→3 is constrained by $\mu$."
3. **Resolve the 8-count.** Decide whether $|\mathbb{F}_2^3|=8$ and $4\times 2=8$ are the same fact, and reconcile Rank-6 with the 36-mode waist.
4. **Fix the dual-residue sector sizes** and the boundary conditions for `orthogonal` and `partition`.
5. **Calibrate the iCOH gate on real dyads** (Protocol 85).
6. **Complete the citation record** for the study of Section 6 from the publisher page, and check the remaining references against the audit.
7. **Decide the fate of L8 and L9.** Either supply operational definitions or remove them.
8. **Compile the Lean skeleton** ([`theory/lean/FiniteDescent.lean`](../theory/lean/FiniteDescent.lean)) and decide the fate of L1, which the first claims draft omitted.
9. **Define the transience criterion operationally**: which measures, over what window, count as relaxation (Protocol 90).

---

## Section 13: Caveats and Limitations

1. The two-origin finding concerns developmental lineage. It does not address language, consciousness, or any QD-TER mechanism, and it does not describe either lineage as flexible or rigid.
2. The descent bound in Section 2.3 is elementary and general. The Rank-3 structure in Section 2.4 is a candidate with a stated tension against D1.
3. The interface mapping and band assignments in Section 4 are interpretations of correlational literature.
4. Takens reconstruction is exploratory for physiological data (Section 5.1).
5. The iCOH threshold is calibrated on simulated recordings only.
6. L1, L8, L9, and L11 are retained for completeness and have no protocol.
7. The executable checks of Section 2.7 verify mathematics, not biology.
8. No medical claims are made.

---

## Section 14: References

Entries marked † were checked against independent sources in October 2026. The others are standard references that were not rechecked in that pass; see [`docs/references_audit.md`](../docs/references_audit.md).

**Brain development and chromatin**

- † Dundes, C., Jokhai, R., et al.; Loh, K. M. (senior author) (2026). Two-origin brain development; *Nature Neuroscience*, published 18 September 2026. doi:10.1038/s41593-026-02433-7. *(Full author list and title to be completed from the publisher page.)*
- † Conger, K. (2026, September 18). Human brain is two separate organs, Stanford Medicine-led research finds. Stanford Medicine News Center. https://med.stanford.edu/news/all-news/2026/09/two-separate-brains.html
- Weaver, I. C. G., et al. (2004). Epigenetic programming by maternal behavior. *Nature Neuroscience*, 7(8), 847–854.

**Speech, oscillations, and inter-brain coupling**

- † Giraud, A.-L., & Poeppel, D. (2012). Cortical oscillations and speech processing: emerging computational principles and operations. *Nature Neuroscience*, 15(4), 511–517. doi:10.1038/nn.3063
- Obleser, J., Herrmann, B., & Henry, M. J. (2012). Neural oscillations in speech: don't be enslaved by the envelope. *Frontiers in Human Neuroscience*, 6, 250.
- † Stephens, G. J., Silbert, L. J., & Hasson, U. (2010). Speaker–listener neural coupling underlies successful communication. *Proceedings of the National Academy of Sciences*, 107(32), 14425–14430. doi:10.1073/pnas.1008662107
- † Pérez, A., Carreiras, M., & Duñabeitia, J. A. (2017). Brain-to-brain entrainment: EEG interbrain synchronization while speaking and listening. *Scientific Reports*, 7, 4190. doi:10.1038/s41598-017-04464-4

**Language and information theory**

- † Gibson, E., Futrell, R., Piantadosi, S. T., Dautriche, I., Mahowald, K., Bergen, L., & Levy, R. (2019). How efficiency shapes human language. *Trends in Cognitive Sciences*, 23(5), 389–407. doi:10.1016/j.tics.2019.02.003

**Dynamics and embedding**

- Takens, F. (1981). Detecting strange attractors in turbulence. In *Dynamical Systems and Turbulence, Warwick 1980* (Lecture Notes in Mathematics 898, pp. 366–381). Springer.
- Sauer, T., Yorke, J. A., & Casdagli, M. (1991). Embedology. *Journal of Statistical Physics*, 65, 579–616.
- Fraser, A. M., & Swinney, H. L. (1986). Independent coordinates for strange attractors from mutual information. *Physical Review A*, 33, 1134–1140.
- Kennel, M. B., Brown, R., & Abarbanel, H. D. I. (1992). Determining embedding dimension for phase-space reconstruction using a geometrical construction. *Physical Review A*, 45, 3403–3411.

**Computation and physics**

- † Aaronson, S. (2005). NP-complete problems and physical reality. *ACM SIGACT News*, March 2005. arXiv:quant-ph/0502072.

**Sigma-1, DMT, and adrenochrome**

- † Fontanilla, D., Johannessen, M., Hajipour, A. R., Cozzi, N. V., Jackson, M. B., & Ruoho, A. E. (2009). The hallucinogen N,N-dimethyltryptamine (DMT) is an endogenous sigma-1 receptor regulator. *Science*, 323(5916), 934–937. doi:10.1126/science.1166127
- † Dean, J. G., Liu, T., Huff, S., Sheler, B., Barker, S. A., Strassman, R. J., Wang, M. M., & Borjigin, J. (2019). Biosynthesis and extracellular concentrations of N,N-dimethyltryptamine (DMT) in mammalian brain. *Scientific Reports*, 9, 9333. doi:10.1038/s41598-019-45812-w
- Dyck, E. (2010). Hallucinogens as hard science: the adrenochrome hypothesis for the biogenesis of schizophrenia. *History of Psychology*, 13(2), 178–195. doi:10.1037/a0019394 *(Author attribution to be confirmed.)*
- Encyclopaedia Britannica. Adrenochrome. https://www.britannica.com/science/adrenochrome

**Collective behavior**

- Granovetter, M. (1978). Threshold models of collective behavior. *American Journal of Sociology*, 83(6), 1420–1443.
- Bikhchandani, S., Hirshleifer, D., & Welch, I. (1992). A theory of fads, fashion, custom, and cultural change as informational cascades. *Journal of Political Economy*, 100(5), 992–1026.

**Within this repository**

- [`theory/finite_topological_descent.md`](../theory/finite_topological_descent.md), [`theory/finite_descent_claims.md`](../theory/finite_descent_claims.md), [`theory/language_claims.md`](../theory/language_claims.md), [`theory/lean/FiniteDescent.lean`](../theory/lean/FiniteDescent.lean), [`theory/CLAIMS.md`](../theory/CLAIMS.md), [`theory/residual_integer_8.md`](../theory/residual_integer_8.md), [`src/qdter/descent.py`](../src/qdter/descent.py), v9.0, v7.0, v6.0.

---

## Appendix: Design Invariants

1. **Finite-first.** The continuum is a presentation of the discrete ledger, never its origin.
2. **Candidates are not axioms.** Fano, Hamming, Otx2/Gbx2, and $\mu$-gating stay labeled until the ledger objects are defined; do not promote them silently.
3. **Biology supplies names, not definitions.** A study can motivate a label; it cannot fix an algebraic object.
4. **The inherited integers are inherited.** 12 → 6 → 3, 36, and 8 are not re-derived here.
5. **No result depends on L1, L8, L9, or L11.**
6. **Every conjecture with a protocol states its falsifier.**
7. **Gating is transient; writing is persistent.** The two are told apart by timescale (LI1).
8. **Mathematical facts are checked in code; biological and physical claims are not.**

---

*Document compiled: October 2026*  
*QD-TER Human-Medium v10.0 — The Human Belt: Part V — Language as a Gate Between the Global and the Local*  
*Repository: github.com/jackyreaps/QD-TER-Human-Medium*
