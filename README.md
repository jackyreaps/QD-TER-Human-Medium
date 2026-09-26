

QD-TER Human-Medium

Quantum Dilation of Time Emergent Reality — Human-Medium Layer

Human-Medium Layer of the QD-TER framework: multi-scale biophysical architecture of geometric fields, dielectric waveguides, and hypergraph dynamics.

This repository contains the operational documents, production code, and falsification protocols for the QD-TER Human-Medium suite (v6.0–v9.0), built on the foundational suite (v1.0–v5.0).

Status: Parts I–IV published. The four-part additive structure is complete.

---

What This Repository Is

The public implementation layer of the QD-TER framework — the bridge between the abstract physics suite and the measurable human organism.

· Operational documents (v6.0–v9.0) mapping abstract structure to biology, game theory, and daily practice
· Production code computing measurable quantities (dielectric Reynolds number, bioelectric decoupling, strategic topology, endocrine-chromatin writing, inter-brain coherence)
· Falsification protocols with pre-registered experiments
· Test suites verifying the code against the document claims

Nothing here derives the fundamental constants (ε₀, μ₀, G_N, α_EM). The aether is treated as an immutable substrate; the 8-channel residual structure is inherited from the physics suite and[...]

---

The Four-Part Structure

Part Document Adds
Foundation v1.0–v5.0 Substrate layer: body-as-antenna model, P-V-C triad, myofascial lattice as dielectric
Part I v6.0 Control layer: authorship, inherited load, coherence hierarchy (0/7 → 7/7)
Part II v7.0 Architecture layer: P-V-C triad, ℛ-operator, α/θ signature, strategic landscape, Re_ε
Part III v8.0 Implementation layer: body optimization regimen, Sigma-1 gateway, falsification matrix
Part IV v9.0 Mechanism layer: endocrine-chromatin axis, hypergraph coordination, sustained conditions

Reading order: v1.0–v5.0 → v6.0 → v7.0 → v8.0 → v9.0

---

Repository Structure

```
QD-TER-Human-Medium/
├── README.md
├── CITATION.cff
├── QD-TER_HumanMedium_v6.0_PartI.md
├── QD-TER_HumanMedium_v7.0_PartII.md
├── QD-TER_HumanMedium_v8.0_PartIII.md
│
├── QD-TER_HumanMedium_v9.0/
│   ├── QD-TER_Human_medium_v9.0
│   ├── Theory/          # CLAIMS.md, Consolidated_specification.md, Residual_integer_8.md, ...
│   └── Docs/            # swarm_apparatus.md, liouville_parity_instance.md, ...
│
├── Frame/               # Gnosis_frame.md (interpretive layer)
├── docs/                # aether_as_residual.md, quick_reference.md
├── src/manifold/        # rheology.py, endocrine_chromatin.py, EEG_hyperscan.py
├── tests/               # test_rheology.py, Test_endocrine_chromatin.py, ...
├── examples/            # pd_tournament.py
└── POSSIBLE-NEXT-STEPS.md
```

<details>
<summary><strong>Full file descriptions</strong> (click to expand)</summary>Core documents

· QD-TER_HumanMedium_v6.0_PartI.md — Authorship, ancestry, coherence hierarchy. The control layer.
· QD-TER_HumanMedium_v7.0_PartII.md — Structural foundation. P-V-C triad, ℛ-operator, strategic landscape, Re_ε. The architecture layer.
· QD-TER_HumanMedium_v8.0_PartIII.md — Operational regimen. Nutrition, exercise, sleep, Sigma-1 gateway, falsification matrix. The implementation layer.
· QD-TER_HumanMedium_v9.0/QD-TER_Human_medium_v9.0 — Endocrine–chromatin axis. Pulsatile signaling, Takens reconstruction, hypergraph coordination, sustained conditions. The mechanism layer.

v9.0 Theory layer

· Theory/CLAIMS.md — Canonical taxonomy: Axiom (inherited/modeling), Definition, Derivation, Reduction theorem, Conjecture, Falsification test.
· Theory/Consolidated_specification.md — Meta-level document. Physics-suite dependencies, integer-8 inheritance, FEP reduction, adoption order.
· Theory/Residual_integer_8.md — Inheritance chain: N_waist = 36 → V₄ → dim_{F₂}(V₄) = 2 → N_frames = 4 → N_channels = 8.
· Theory/Reduction_fep.md — Local, conditional reduction to FEP recognition dynamics (Axioms D, S, G, C).
· Theory/Reduction_fep_derivation.md — Full derivation.
· Theory/Non_dual_adaptation.md — Riemannian metric on parameter space, parallel transport of an intentionality vector.

v9.0 Docs (companion notes)

· Docs/swarm_apparatus.md — Institutional closure. DiMaggio & Powell, Gieryn, Luhmann.
· Docs/liouville_parity_instance.md — Arithmetic realization of σ_parity as the Liouville function.
· Docs/collective_antenna.md — Multi-organism arrays. Array gain ∝ N, directivity ∝ N². (Conjecture)
· Docs/distributed_belt.md — Phase-locked group architecture. Constraint scaling. (Conjecture)

Source modules

· src/manifold/rheology.py — Re_ε, bioelectric decoupling, strategic topology, cognitive glue, interaction-node processing, optional EEG gate.
· src/manifold/endocrine_chromatin.py — Takens embedding, regime classification, leaky-kernel integration, 8-channel write vector.
· src/manifold/EEG_hyperscan.py — 6-source hexad, toy lead-field, iCOH-based field-level phase-lock gate.

Supporting

· docs/aether_as_residual.md — Why the code treats the aether as given.
· docs/quick_reference.md — One-page cheat sheet.
· Frame/Gnosis_frame.md — Declared interpretive layer (adjacent, not a dependency).
· tests/ — Pytest suites for each module.
· examples/pd_tournament.py — Iterated Prisoner's Dilemma example.
· POSSIBLE-NEXT-STEPS.md — Roadmap.

</details>---

Quick Start

```bash
git clone https://github.com/jackyreaps/QD-TER-Human-Medium.git
cd QD-TER-Human-Medium
pip install numpy scipy pytest
pytest tests/ -v
```

```python
from src.manifold.rheology import (
    ChiralManifoldRheology, OrganismProfile,
    BioelectricState, process_interaction_node,
)
from src.manifold.endocrine_chromatin import (
    EndocrineChromatinEngine, EndocrineSignal, ChromatinChannel,
)
from src.manifold.EEG_hyperscan import compute_hyperscan_phase_lock
```

---

Core Concepts

Concept Definition
Human Belt The P-V-C triad (Proprioception-Vestibular-Cortical) as minimal geometry for biological coherence
Bioelectric Pattern Memory Voltage-state landscapes encoding geometric relationship to the ordered cascade
Chromatin Residue Hardened metabolic residue of sustained bioelectric patterns; the slow belief layer
Cognitive Glue Gap-junction connectivity + oxytocin-mediated viscosity reduction
Re_ε Dielectric Reynolds Number — governs fluid-to-rigid transition in social coordination
ℛ-Operator Scale-matching recovery kernel; returns to synchron point, not arbitrary equilibrium
The Grid Oscillation between Abyss (hyper-fluid) and Valley (hyper-rigid) via inflammatory loop
Sigma-1 Gateway Non-linear state-transition safety architecture
8-Channel Sector Chromatin writing width, inherited from residual V₄ action on the 36-mode waist
Sustained-Condition Mechanism Long-term conditions shape physiological systems; residue ∝ duration × intensity

---

Strategic Landscape

```
                    The Ridge (Optimal)
                             ▲
                             │
    Attenuation ◄────────────┼────────────► Bioelectric
    (grid break)             │              Recalibration
                             │
    The Abyss ◄──────────────┴──────────────► The Valley
    (Hyper-fluid)                            (Hyper-rigid)
```

The Ridge is a bounded interval, not a fixed point.

---

Design Invariants

1. The aether is an immutable substrate. Not re-derived here.
2. The 8-channel count is inherited from the physics suite.
3. The FEP reduction is local and conditional.
4. Intergenerational propagation is an open empirical question.
5. The EEG hyperscanning layer is a simulator.
6. Collective coordination is a sustained-condition mechanism.
7. The interpretive layer (Frame/Gnosis_frame.md) is adjacent, not a dependency.

---

Citation

```bibtex
@software{qdter_human_medium_2026,
  author = {James Dean},
  title  = {QD-TER Human-Medium: Structural Foundation v6.0--v9.0},
  year   = {2026},
  url    = {https://github.com/jackyreaps/QD-TER-Human-Medium}
}
```

---

License

CC BY-SA 4.0. See CITATION.cff for details.

---

Maintained by James Dean. For the physics suite and cascade foundation, open a GitHub issue.
