# QD-TER Human-Medium

**Quantum Discrete-Temporal Eigenfunction Resonance — Human-Medium Layer**

Public-facing structural biology and coherence framework. This repository
contains the operational documents, production code, and falsification protocols
for the QD-TER Human-Medium suite (v6.0–v8.0).

> **Status:** v7.0 published. v8.0 (Operational Regimen & Protocols) forthcoming.

---

## Repository Structure

```
QD-TER-Human-Medium/
├── README.md                           # This file
├── doc_6_0.md                          # Part I: Conscious Authorship, Ancestry & Coherence Hierarchy
├── doc_7_0_structural_foundation.md    # Part II: Structural Foundation (this release)
├── doc_8_0.md                          # Part III: Operational Regimen (forthcoming)
├── docs/
│   ├── aether_as_residual.md           # Public mathematical note on aether origin
│   └── quick_reference.md              # One-page topology + engine-lock cheat sheet
├── src/
│   └── manifold/
│       ├── __init__.py
│       └── rheology.py                 # Production rheology module
├── tests/
│   └── test_rheology.py              # Unit test suite
├── examples/
│   └── pd_tournament.py              # Prisoner's Dilemma simulation (forthcoming)
└── CITATION.cff
```

---

## Document Suite

| Document | Title | Status |
|----------|-------|--------|
| **Doc 6.0** | The Human Belt — Part I: Conscious Authorship, Ancestry & The Coherence Hierarchy | Published |
| **Doc 7.0** | The Human Belt — Part II: Structural Foundation | **Published** |
| **Doc 8.0** | The Human Belt — Part III: Operational Regimen & Protocols | Forthcoming |

### Document File Mapping

The repository retains versioned filenames for historical traceability. The canonical short names used in this README map to the following actual files in the repo:

| Canonical Reference | Actual File on GitHub | Part |
|---------------------|----------------------|------|
| `doc_6_0.md` | `QD-TER_HumanMedium_v6.0_PartI.md` | Part I |
| `doc_7_0_structural_foundation.md` | `QD-TER_HumanMedium_v7.0_PartII.md` | Part II |
| `doc_8_0.md` | *Forthcoming* | Part III |

All three documents are **additive** — Part I establishes authorship and hierarchy, Part II supplies structural foundation, and Part III (forthcoming) will provide operational regimen. None replaces the previous.

### Doc 7.0 — What's New

- **Bioelectric pattern memory** as primary belief substrate (Levin 2026)
- **Ideology / Mysticism / Truth** formalized as bioelectric-chromatin states
- **Cognitive glue** — gap-junction electrical coupling + oxytocin viscosity reduction
- **Inflammation, Hallucination, and the Grid** — chronic inflammation as bioelectric noise generator
- **Attenuation protocols** — omega-3, polyphenols, vagal stimulation, sleep as grid-dissolution preconditions
- **78 falsification experiments** with peer-reviewed anchors
- **Production Python module** with full test coverage

---

## Quick Start: Running the Code

```bash
# Clone
git clone https://github.com/JackyReaps/QD-TER-Human-Medium.git
cd QD-TER-Human-Medium

# Install dependencies
pip install numpy pytest

# Run tests
pytest tests/test_rheology.py -v

# Import in your own work
from src.manifold.rheology import (
    AetherSubstrateConstants,
    BioelectricState,
    ChiralManifoldRheology,
    OrganismProfile,
    process_interaction_node,
)
```

---

## Design Invariant

> **The aether is an immutable substrate.** The `rheology.py` module computes
> only downstream rheological responses. It does not rederive ε₀, μ₀, or any
> fundamental field properties. For the conceptual origin of the medium, see
> `docs/aether_as_residual.md`.

---

## Core Concepts (One-Minute Primer)

| Concept | One-Sentence Definition |
|---------|------------------------|
| **Human Belt** | The P-V-C triad (Proprioception-Vestibular-Cortical) as minimal geometry for biological coherence |
| **Bioelectric Pattern Memory** | Voltage-state landscapes across cell collectives that encode geometric relationship to the ordered cascade |
| **Chromatin Residue** | Hardened metabolic residue of sustained bioelectric patterns; the slow, ATP-expensive belief layer |
| **Cognitive Glue** | Gap-junction electrical connectivity + oxytocin-mediated viscosity reduction; both necessary for cross-brain phase-lock |
| **Dielectric Reynolds Number (Re_ε)** | Dimensionless number governing the fluid-to-rigid transition in social coordination |
| **ℛ-Operator** | Scale-matching recovery kernel; returns the organism to synchron point, not arbitrary equilibrium |
| **The Grid** | Self-reinforcing oscillation between Abyss (hyper-fluid hallucination) and Valley (hyper-rigid ossification) via inflammatory loop |
| **Attenuation** | Systematic reduction of inflammatory load to restore bioelectric preconditions for ℛ-operator function |

---

## Strategic Landscape Topology

```
                    The Ridge
                 (Optimal Function)
                       ▲
                       │
    Attenuation ◄──────┼──────► Bioelectric Recalibration
    (grid break)       │      (meditation, breathwork)
                       │
        ▲              │              ▲
        │              │              │
   The Abyss ◄─────────┴─────────► The Valley
(Hyper-fluid      Inflammation   (Hyper-rigid
 hallucination)      Grid        ossification)
```

---

## Falsification Commitment

Every novel claim in Doc 7.0 carries a pre-registered falsification protocol.
See §8 (Falsification Matrix) in the main document. Key test categories:

- **Bioelectric:** Voltage-sensitive dye on fascial fibroblasts; gap-junction blocker + social coordination
- **Neural:** α/θ ratio perturbation + tracking; handedness reversal + ρ shift
- **Genetic:** Recombination breakpoint density at φ-scaled chromosomal positions
- **Behavioral:** NR3C1 alignment × Prisoner's Dilemma cooperation; intranasal oxytocin × rigid defector
- **Inflammatory:** CRP/IL-6 × bioelectric variance; 8-week attenuation × grid metrics

---

## Citation

If you use this framework in published work:

```bibtex
@software{qdter_human_medium_2026,
  author = {JackyReaps},
  title = {QD-TER Human-Medium: Structural Foundation v7.0},
  year = {2026},
  url = {https://github.com/JackyReaps/QD-TER-Human-Medium}
}
```

---

## License



---

*Repository maintained by JackyReaps. For the physics suite and cascade foundation, contact via GitHub issues.*
