# QD-TER Human-Medium

**Quantum Dilation of Time Emergent Reality — Human-Medium Layer**

[![Tests](https://github.com/jackyreaps/QD-TER-Human-Medium/actions/workflows/tests.yml/badge.svg)](https://github.com/jackyreaps/QD-TER-Human-Medium/actions/workflows/tests.yml)
![License: CC BY-SA 4.0](https://img.shields.io/badge/license-CC%20BY--SA%204.0-lightgrey)

A multi-scale biophysical framework of geometric fields, dielectric waveguides, and hypergraph dynamics, with reference code and proposed falsification protocols.

> **Status:** Speculative theoretical framework. Every claim is labeled by epistemic status (see [`CLAIMS.md`](theory/CLAIMS.md)). The documents make no medical claims, and nothing here is medical advice.

---

## Contents

- [What this repository is](#what-this-repository-is)
- [The documents](#the-documents)
- [Repository layout](#repository-layout)
- [Quick start](#quick-start)
- [Core concepts](#core-concepts)
- [Strategic landscape](#strategic-landscape)
- [Design invariants](#design-invariants)
- [Scope and limitations](#scope-and-limitations)
- [Citation](#citation)
- [License](#license)

---

## What this repository is

The public implementation layer of the QD-TER framework: the bridge between the abstract physics suite and the measurable human organism.

- **Documents** (v1.0–v10.0) mapping abstract structure to biology, game theory, and daily practice.
- **Reference code** computing measurable quantities: dielectric Reynolds number, bioelectric decoupling, strategic topology, endocrine–chromatin writing, inter-brain coherence.
- **Falsification protocols** proposed for each mechanism (Protocols 51–84).
- **Tests** checking the code against the document claims.

Nothing here derives the fundamental constants (ε₀, μ₀, G_N, α_EM). The aether is treated as an immutable substrate, the 8-channel residual structure is inherited from the physics suite, and the human organism is modeled as a phase-locked dielectric interface rather than a source of the substrate itself.

## The documents

The documents form one numbered sequence. Read them in order; each part adds to the previous one without replacing it. The full reading guide is in [`suite/README.md`](suite/README.md).

| Part | Version | Layer | Document |
|---|---|---|---|
| Foundation | v1.0–v5.0 | Substrate | [`suite/`](suite/README.md) (five documents) |
| Part I | v6.0 | Control: authorship, ancestry, coherence hierarchy | [`v06`](suite/v06_part1_authorship_and_coherence.md) |
| Part II | v7.0 | Architecture: P-V-C triad, ℛ-operator, strategic landscape, Re_ε | [`v07`](suite/v07_part2_structural_foundation.md) |
| Part III | v8.0 | Implementation: operational regimen, Sigma-1 gateway, falsification matrix | [`v08`](suite/v08_part3_operational_regimen.md) |
| Part IV | v9.0 | Mechanism: endocrine–chromatin axis, hypergraph coordination, sustained conditions | [`v09`](suite/v09_part4_endocrine_chromatin.md) |
| Part V | v10.0 | Language: finite topological descent as compression, the dual engine, symbols as gates | [`v10`](suite/v10_part5_language_and_descent.md) |

Supporting material:

| Path | Description |
|---|---|
| [`theory/`](theory/README.md) | Formal specifications and derivations behind v9.0: claims taxonomy, consolidated specification, integer-8 inheritance, FEP reduction and its derivation, non-dual adaptation, peptidein load dynamics |
| [`docs/`](docs/README.md) | Narrative overview, quick reference, notation, aether-as-residual note, agency and gnosis architecture, roadmap, reference audit, known issues |
| [`docs/notes/`](docs/README.md#companion-notes-to-v90) | Companion notes to v9.0: swarm apparatus, Liouville parity instance, collective antenna, distributed belt |
| [`adjacent/`](adjacent/README.md) | Related material that nothing else depends on: the Gnosis frame and the Guild System |

## Repository layout

```text
QD-TER-Human-Medium/
├── README.md
├── CITATION.cff
├── CHANGELOG.md
├── CONTRIBUTING.md
├── pyproject.toml              # package metadata and pytest configuration
├── .github/workflows/          # CI: run the tests
│
├── suite/                      # the ten numbered documents, v1.0–v10.0
│   ├── README.md               #   reading order
│   ├── v01_consciousness_substrate.md
│   ├── v02_dna_pathway_extension.md
│   ├── v03_organismic_hypergraph.md
│   ├── v04_sensory_consciousness_interface.md
│   ├── v05_architecture_of_consciousness.md
│   ├── v06_part1_authorship_and_coherence.md
│   ├── v07_part2_structural_foundation.md
│   ├── v08_part3_operational_regimen.md
│   ├── v09_part4_endocrine_chromatin.md
│   └── v10_part5_language_and_descent.md
│
├── theory/                     # formal specifications, derivations, claims (v9.0, v10.0)
│   └── lean/                   #   Lean 4 skeleton of the finite descent (uncompiled)
├── docs/                       # overview, quick reference, notation, roadmap, audits
│   └── notes/                  #   companion notes to v9.0
├── adjacent/                   # related, not required: Gnosis frame, Guild System
│
├── src/qdter/                  # reference implementation
│   ├── descent.py              #   finite descent, Fano/Hamming checks (v10.0)
│   └── manifold/
│       ├── rheology.py
│       ├── endocrine_chromatin.py
│       ├── peptidein_load.py
│       ├── eeg_hyperscan.py
│       ├── generative_model.py
│       └── spectral.py
├── tests/
└── examples/
    ├── pd_tournament.py        # iterated Prisoner's Dilemma on organism profiles (v7.0 spec)
    └── finite_descent.py       # printed check of the v10.0 mathematics
```

**Where things go.** A new numbered document goes in `suite/`. A formal specification, claim, or derivation goes in `theory/` (Lean files in `theory/lean/`). Anything explanatory, a companion note, or a roadmap item goes in `docs/`. Related projects that the main line does not depend on go in `adjacent/`. Code goes in `src/qdter/manifold/` with a matching `tests/test_*.py` (lowercase, so pytest finds it).

| Module | Description |
|---|---|
| `src/qdter/descent.py` | Finite folds over $\mathbb{F}_2$, the Fano plane, the [7,4] Hamming code, syndrome decoding, gated folds (checks for v10.0 Sections 2 and 7) |
| `src/qdter/manifold/rheology.py` | Re_ε, bioelectric decoupling, strategic topology, cognitive glue, interaction-node processing, optional EEG gate |
| `src/qdter/manifold/endocrine_chromatin.py` | Takens embedding, regime classification, leaky-kernel integration, 8-channel write vector |
| `src/qdter/manifold/peptidein_load.py` | `PeptideinLoad`, `Sigma1Gateway`, Number–Location diagnostics |
| `src/qdter/manifold/eeg_hyperscan.py` | 6-source hexad, toy lead-field, iCOH-based field-level phase-lock gate |
| `src/qdter/manifold/generative_model.py` | Generative model for the local, conditional FEP reduction (Axiom G) |
| `src/qdter/manifold/spectral.py` | Combinatorial Laplacian on the seven-engine phase-lock hierarchy (Axiom S) |

## Quick start

```bash
git clone https://github.com/jackyreaps/QD-TER-Human-Medium.git
cd QD-TER-Human-Medium
pip install -e ".[dev]"
pytest
```

```python
from qdter.manifold.rheology import (
    ChiralManifoldRheology,
    OrganismProfile,
    BioelectricState,
    process_interaction_node,
)
from qdter.manifold.endocrine_chromatin import (
    EndocrineChromatinEngine,
    EndocrineSignal,
    ChromatinChannel,
)
from qdter.manifold.peptidein_load import PeptideinLoad, Sigma1Gateway
from qdter.manifold.eeg_hyperscan import compute_hyperscan_phase_lock
```

The code installs as the `qdter` package (Python 3.10 or later). To run the Prisoner's Dilemma tournament example from the repository root:

```bash
python -m examples.pd_tournament
python -m examples.finite_descent
```

## Core concepts

| Concept | Definition |
|---|---|
| **Human Belt** | The P-V-C triad (Proprioception–Vestibular–Cortical) as minimal geometry for biological coherence. |
| **Bioelectric Pattern Memory** | Voltage-state landscapes encoding geometric relationship to the ordered cascade. |
| **Chromatin Residue** | Hardened metabolic residue of sustained bioelectric patterns; the slow belief layer. |
| **Cognitive Glue** | Gap-junction connectivity plus oxytocin-mediated viscosity reduction. |
| **Re_ε** | Dielectric Reynolds Number; governs the fluid-to-rigid transition in social coordination. |
| **ℛ-Operator** | Scale-matching recovery kernel; returns to the synchron point, not an arbitrary equilibrium. |
| **The Grid** | Oscillation between Abyss (hyper-fluid) and Valley (hyper-rigid) via an inflammatory loop. |
| **Sigma-1 Gateway** | Non-linear state-transition safety architecture. |
| **8-Channel Sector** | Chromatin writing width, inherited from the residual V₄ action on the 36-mode waist. |
| **Sustained-Condition Mechanism** | Long-term conditions shape physiological systems; residue ∝ duration × intensity. |
| **Peptidein** | Small microprotein (< 50 aa) translated from non-coding open reading frames; substrate of the 8-channel sector. |
| **Number–Location Criticality** | Failure mode of the peptidein layer: local binding-site saturation (Number) conjoined with ectopic accumulation (Location). |

## Strategic landscape

```text
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

**The Ridge is a bounded interval, not a fixed point.** The system stays on the Ridge only while both the Number (density) and Location (distribution) constraints are satisfied. Either failure alone displaces it to the Valley; glue depletion displaces it to the Abyss.

## Design invariants

1. **The aether is an immutable substrate.** Not re-derived here.
2. **The 8-channel count is inherited** from the physics suite.
3. **The FEP reduction is local and conditional.**
4. **Intergenerational propagation** is an open empirical question.
5. **The EEG hyperscanning layer is a simulator.**
6. **Collective coordination** is a sustained-condition mechanism.
7. **The interpretive layer** ([`adjacent/gnosis_frame.md`](adjacent/gnosis_frame.md)) is adjacent, not a dependency.

## Scope and limitations

- The framework is theoretical. The falsification protocols are proposals; none has been run or pre-registered.
- The EEG hyperscanning module uses a toy forward model and is a simulator, not an analysis pipeline for real recordings. Its coupling lag, recording length, and threshold are simulation choices.
- Open problems, including the fact that the iCOH threshold is calibrated on simulated data only, are listed in [`docs/known_issues.md`](docs/known_issues.md).
- Part III (v8.0) describes an operational regimen (nutrition, exercise, sleep, protocols) as a theoretical construct. It is not medical advice.

## Citation

If you use this framework, cite it using [`CITATION.cff`](CITATION.cff) (GitHub's "Cite this repository" button) or the entry below.

```bibtex
@software{qdter_human_medium_2026,
  author = {James Dean},
  title  = {QD-TER Human-Medium: Structural Foundation v6.0--v10.0},
  year   = {2026},
  url    = {https://github.com/jackyreaps/QD-TER-Human-Medium}
}
```

## License

CC BY-SA 4.0, as declared in [`CITATION.cff`](CITATION.cff).
