

QD-TER Human-Medium

Quantum Dilation of Time Emergent Reality — Human-Medium Layer

Human-Medium Layer of the QD-TER framework — multi-scale biophysical architecture of geometric fields, dielectric waveguides, and hypergraph dynamics.

This repository contains the operational documents, production code, and falsification protocols for the QD-TER Human-Medium suite (v6.0–v9.0), built on the foundational suite (v1.0–v5.0).

Status: Parts I–IV published. The four-part additive structure is complete. The v9.0 Theory and Docs layers supply the formal specification and companion notes for Part IV.

---

What This Repository Is

This is the public implementation layer of the QD-TER framework — the bridge between the abstract physics suite (discrete cascade, pre-temporal symmetry operations) and the measurable human organism.

Everything here is either:

· Published operational documents (v6.0–v9.0) that map abstract structural mechanics to biology, game theory, and daily practice
· Production code that computes measurable quantities from the framework (dielectric Reynolds number, bioelectric decoupling, strategic topology, endocrine-chromatin writing, inter-brain coherence)
· Supporting documents that explain boundary conditions, provide quick reference, and enable citation
· Test suites that verify the code against the document claims

Nothing here derives the fundamental constants (ε₀, μ₀, G_N, α_EM). Those belong to the physics suite. This layer treats the aether as an immutable substrate and computes only downstream perturbations. The 8-channel residual structure is inherited from the physics suite and is not re-derived here.

---

The Four-Part Additive Structure

The Human-Medium suite is deliberately split into four additive documents, built on the foundational v1.0–v5.0 suite. None replaces the previous. Each layer adds new structure.

Part Document What It Adds
Foundation v1.0–v5.0 — Foundational Suite The substrate layer. Early QD-TER development establishing the body-as-antenna model, the P-V-C triad as three-element resonant array, the myofascial lattice as dielectric substrate, and consciousness as received signal rather than generated product.
Part I v6.0 — Conscious Authorship, Ancestry & The Coherence Hierarchy The control layer. Belief-mediated control, inherited epigenetic load as trajectory-determining physical adaptation, the coherence hierarchy (0/7 → 7/7 engine lock), the engine-load coherence tensor, the Model Gradient, and the pedological relation.
Part II v7.0 — Structural Foundation The architecture layer. The P-V-C triad as triangular scale-location, the three exchange interfaces (Proprioception-Vestibular-Cortical), the ℛ-operator as scale-matching recovery kernel, the α/θ golden ratio signature, the chiral twist map, strategic landscape topology (Abyss/Ridge/Valley), social coordination as dielectric rheology (Re_ε), and the game-theory bridge.
Part III v8.0 — Operational Regimen & Protocols The implementation layer. Complete body optimization regimen (nutrition, exercise, sleep, light, social practice), 2025–2026 advanced substrate integration (Urolithin A mitophagy, spermidine autophagy, NAD⁺ precursors, photobiomodulation), the Sigma-1 gateway safety architecture for non-linear state transitions, supra-human coherence states as deferred placeholders, tiered daily protocol, inherited-load modifications, and the operational falsification matrix.
Part IV v9.0 — The Endocrine–Chromatin Axis The mechanism layer. Pulsatile endocrine signaling as the chromatin-writing signal, Takens phase-space reconstruction of endocrine dynamics, multi-timescale leaky-kernel integration, hypergraph coordination with order-dependent composition, the common prior as measurable methylation alignment, sustained-condition mechanism, and the source modules that implement all of it.

Reading order: v1.0–v5.0 → v6.0 → v7.0 → v8.0 → v9.0. Each document assumes knowledge from the previous. Part IV's Theory layer supplies the formal specification; its Docs layer supplies the companion notes.

Document File Mapping

The repository retains versioned filenames for historical traceability. The canonical short names used in cross-references map to the following actual files:

Canonical Reference Actual File on GitHub Part
doc_6_0.md QD-TER_HumanMedium_v6.0_PartI.md Part I
doc_7_0_structural_foundation.md QD-TER_HumanMedium_v7.0_PartII.md Part II
doc_8_0.md QD-TER_HumanMedium_v8.0_PartIII.md Part III
doc_9_0.md QD-TER_HumanMedium_v9.0/QD-TER_Human_medium_v9.0 Part IV

---

Repository Structure

```
QD-TER-Human-Medium/
│
├── README.md                              ← this file — canonical entry point
├── CITATION.cff                           ← software citation metadata (CC BY-SA 4.0)
│
├── QD-TER_HumanMedium_v6.0_PartI.md       ← Part I: Authorship & Hierarchy
├── QD-TER_HumanMedium_v7.0_PartII.md      ← Part II: Structural Foundation
├── QD-TER_HumanMedium_v8.0_PartIII.md     ← Part III: Operational Regimen
│
├── QD-TER_HumanMedium_v9.0/
│   ├── QD-TER_Human_medium_v9.0           ← Part IV main document
│   │
│   ├── Theory/                            ← v9.0 formal layer
│   │   ├── CLAIMS.md                      ← canonical claims taxonomy
│   │   ├── Consolidated_specification.md  ← physics-suite dependency map
│   │   ├── Residual_integer_8.md          ← channel-count inheritance
│   │   ├── Reduction_fep.md               ← conditional FEP reduction
│   │   ├── Reduction_fep_derivation.md    ← full derivation
│   │   └── Non_dual_adaptation.md         ← parallel-transport layer
│   │
│   └── Docs/                              ← v9.0 companion notes
│       ├── swarm_apparatus.md             ← institutional closure
│       ├── liouville_parity_instance.md   ← arithmetic instance of σ_parity
│       ├── collective_antenna.md          ← multi-organism array extension
│       └── distributed_belt.md            ← phase-locked group architecture
│
├── Frame/
│   └── Gnosis_frame.md                    ← interpretive layer (adjacent, not dependent)
│
├── docs/
│   ├── aether_as_residual.md              ← why the code treats the aether as given
│   └── quick_reference.md                 ← one-page topology + engine-lock cheat sheet
│
├── src/manifold/
│   ├── __init__.py                        ← package exports
│   ├── rheology.py                        ← production dielectric rheology module
│   ├── endocrine_chromatin.py             ← endocrine-to-chromatin writing pipeline
│   └── EEG_hyperscan.py                   ← source-space iCOH gate
│
├── tests/
│   ├── test_rheology.py                   ← dielectric rheology tests
│   ├── Test_endocrine_chromatin.py        ← endocrine-chromatin tests
│   ├── Test_EEG_hyperscan.py              ← hyperscanning gate tests
│   └── Test_integration_eeg.py            ← EEG gate integration tests
│
├── examples/
│   └── pd_tournament.py                   ← iterated Prisoner's Dilemma example
│
├── theory/
│   └── QD-TER-Human-Medium-Full.md        ← consolidated theory document (legacy)
│
└── POSSIBLE-NEXT-STEPS.md                 ← roadmap
```

---

Why Each File Exists

docs/aether_as_residual.md — The rheology.py module treats the aether as an immutable substrate — it does not derive ε₀, μ₀, or polaritonic density from first principles. This document explains why that assumption is structurally sound: the aether is the residual phase-space medium that remains after discrete symmetry operations (3-fold triskelion + 5-fold pentagram + dimensional projection) have been imposed on pre-structural possibility space. It is not a "thing" before the symmetries; it is the patternized void that results from them. Readers who follow the code from Part II can stop here; those who seek the structural origin of the medium itself will find it in the cascade foundation documents.

docs/quick_reference.md — A one-page cheat sheet for practitioners and researchers. Contains the strategic landscape topology (Abyss → Ridge → Valley), the seven-engine manifold with frequency bands, the P-V-C triad mapping, the coherence hierarchy levels (0/7 through 7/7), the falsification matrix summary, and key operational numbers (0.1 Hz RFB, omega-3 dosing, collagen/glycine targets). Designed to be printed or kept open during code review.

QD-TER_HumanMedium_v9.0/Theory/Consolidated_specification.md — The meta-level document governing how all other theory documents should be read. Lists the physics-suite dependencies. Consolidates the integer-8 inheritance, the FEP reduction, and the non-dual layer. References CLAIMS.md. Gives the adoption order and dependency summary.

QD-TER_HumanMedium_v9.0/Theory/CLAIMS.md — The canonical taxonomy of every claim in the repository: Axiom (inherited), Axiom (modeling), Definition, Derivation, Reduction theorem (conditional), Conjecture, Falsification test. Where a claim is conditional or conjectural, it is labeled as such in the document that makes it.

QD-TER_HumanMedium_v9.0/Theory/Residual_integer_8.md — Specifies the inheritance chain for the channel count: N_waist = 36 → V₄ → dim_{F₂}(V₄) = 2 → N_frames = 4 → N_channels = 8. Includes the notation warning: do not write 8 = 4 × (2 × 2); that conflates the group order with the F₂-dimension.

QD-TER_HumanMedium_v9.0/Theory/Reduction_fep.md — Specifies a local, conditional reduction of QD-TER dynamics to FEP recognition dynamics. Conditional on Axioms D, S, G, C. The theorem is local in state space and linearized. Global fixed-point alignment and full nonlinear identity are explicitly not claimed.

QD-TER_HumanMedium_v9.0/Theory/Non_dual_adaptation.md — Proposes a Riemannian metric on the parameter space and formalizes belief updates as parallel transport of an intentionality vector. Conditional on the physics suite supplying the metric. Holonomy caveat stated. Coercion claim downgraded to detection.

QD-TER_HumanMedium_v9.0/Docs/swarm_apparatus.md — Extends the individual-scale coordination mechanism of v9.0 §4 to institutional networks. Uses established sociology (DiMaggio & Powell, Gieryn, Luhmann). Does not extend the QD-TER formal apparatus into institutional territory.

QD-TER_HumanMedium_v9.0/Docs/liouville_parity_instance.md — Provides the arithmetic realization of σ_parity as the Liouville function λ(n) = (−1)^Ω(n), and cites the conditionally Lean-verified case that every positive multiple of 4 is the sum of two positive integers with Liouville value −1.

QD-TER_HumanMedium_v9.0/Docs/collective_antenna.md — Extends the antenna framing from Part II to multi-organism arrays. Array gain ∝ N, directivity ∝ N². All claims labeled Conjecture.

QD-TER_HumanMedium_v9.0/Docs/distributed_belt.md — Formalizes the operational architecture of a phase-locked group. Specifies the constraint-scaling rule under collective coupling. All claims labeled Conjecture.

Frame/Gnosis_frame.md — The declared interpretive layer. Adjacent to the framework, not a dependency of it. Holds the metaphysical commitments as declared positions and explicitly disclaims any derivation from the mathematics.

src/manifold/rheology.py — The production implementation of the dielectric rheology layer. Computes:

· Dielectric Reynolds Number Re_ε as a function of oxytocin receptor activation and gap-junction density
· Bioelectric decoupling detection from resting-potential deviation and gap-junction density
· Strategic topology classification (Abyss / Ridge / Valley / Turbulent)
· Metabolic demethylation cost (the ATP barrier to belief revision)
· Cognitive glue index (the combined OXTR × GJ coupling strength)
· Full interaction-node processing for two-organism game-theoretic encounters
· Optional EEG gate integration via use_eeg_gate

Design invariant enforced: The aether is immutable. The module computes only downstream fluid perturbations.

src/manifold/endocrine_chromatin.py — The endocrine-to-chromatin writing pipeline. Implements:

· EndocrineSignal — pulse train with ultradian step
· ChromatinChannel — per-channel tissue weight, baseline methylation, parity class
· EndocrineChromatinEngine — Takens delay embedding, Jacobian regime classification, multi-timescale leaky-kernel integration, allostatic load computation, 8-channel write vector

Design invariant enforced: The channel count (8) is a required constructor parameter, inherited from the physics suite. The module does not re-derive it.

src/manifold/EEG_hyperscan.py — The source-space inter-brain coherence gate. Implements:

· SourceSpace — 6-source hexad (P_A, V_A, C_A, P_B, V_B, C_B)
· SensorMontage — toy 16-channel montage with a distance-based lead-field
· compute_hyperscan_phase_lock — full pipeline: synthesize → forward → reconstruct → iCOH

Design invariant enforced: Never touches aether constants. Consumes a plain dictionary of rheology outputs. Uses imaginary coherence (iCOH) rather than raw PLV so that volume conduction does not pass the gate.

tests/test_rheology.py — Pytest-validated tests covering monotonic Re_ε rise with OXTR and GJ, strategic topology classification, bioelectric decoupling detection, and full integration including phase-lock blocking.

tests/Test_endocrine_chromatin.py — Channel-count enforcement, Takens embedding dimension checks, leaky-kernel spectrum integration, allostatic load integral, and channel write validation.

tests/Test_EEG_hyperscan.py — Kuramoto coupling locks under high coupling; zero coupling produces iCOH below threshold; volume conduction does not pass iCOH.

examples/pd_tournament.py — Placeholder for the full Prisoner's Dilemma tournament simulation. The v8.0 operational regimen supplies the biological parameters; this module will eventually instantiate OrganismProfile objects, modulate Re_ε via oxytocin dosing protocols, detect cross-brain phase-lock via simulated EEG hyperscanning, and track strategic topology transitions across iterated interactions.

CITATION.cff — Standard software citation file (Citation File Format v1.2.0). Enables automated citation extraction by GitHub, Zenodo, and reference managers. License: CC BY-SA 4.0.

---

Quick Start: Running the Code

```bash
# Clone
git clone https://github.com/JackyReaps/QD-TER-Human-Medium.git
cd QD-TER-Human-Medium

# Install dependencies
pip install numpy scipy pytest

# Run all tests
pytest tests/ -v

# Import in your own work
from src.manifold.rheology import (
    AetherSubstrateConstants,
    BioelectricState,
    ChiralManifoldRheology,
    GroupAgent,
    HypergraphCoordinationEngine,
    OrganismProfile,
    process_interaction_node,
)
from src.manifold.endocrine_chromatin import (
    ChromatinChannel,
    EndocrineChromatinEngine,
    EndocrineSignal,
)
from src.manifold.EEG_hyperscan import (
    SensorMontage,
    SourceSpace,
    compute_hyperscan_phase_lock,
    imaginary_coherence,
)
```

---

Core Concepts (One-Minute Primer)

Concept One-Sentence Definition
Human Belt The P-V-C triad (Proprioception-Vestibular-Cortical) as minimal geometry for biological coherence
Bioelectric Pattern Memory Voltage-state landscapes across cell collectives that encode geometric relationship to the ordered cascade
Chromatin Residue Hardened metabolic residue of sustained bioelectric patterns; the slow, ATP-expensive belief layer
Cognitive Glue Gap-junction electrical connectivity + oxytocin-mediated viscosity reduction; both necessary for cross-brain phase-lock
Dielectric Reynolds Number (Re_ε) Dimensionless number governing the fluid-to-rigid transition in social coordination
ℛ-Operator Scale-matching recovery kernel; returns the organism to synchron point, not arbitrary equilibrium
The Grid Self-reinforcing oscillation between Abyss (hyper-fluid hallucination) and Valley (hyper-rigid ossification) via inflammatory loop
Attenuation Systematic reduction of inflammatory load to restore bioelectric preconditions for ℛ-operator function
Sigma-1 Gateway Non-linear state-transition safety architecture; transient impedance transformation via endogenous DMT–Sigma-1R binding
Antenna Maintenance The v8.0 operational regimen reframed as dielectric cleaning, impedance matching, and tuning calibration
Inherited Load Ancestral epigenetic marks (NR3C1, FKBP5 methylation) that physically constrain the organism's coherence hierarchy trajectory
Pedological Relation Pattern transmission from higher- to lower-resolution reflection; not hierarchy, but resolution differential
8-Channel Residual Sector The chromatin writing width, inherited from the physics suite's residual V₄ action on the 36-mode waist
Sustained-Condition Mechanism Long-term conditions shape the physiological systems that encode strategic posture; the residue is proportional to duration and intensity, not event content
Hypergraph Coordination N-agent coordination as a field density over hyperedges, with order-dependent composition
EEG Hyperscanning Gate Source-space iCOH measurement that gates the scalar phase-lock decision by rejecting volume conduction

---

Strategic Landscape Topology

```
                    The Ridge (Optimal Function)
                             ▲
                             │
    Attenuation ◄────────────┼────────────► Bioelectric
    (grid break)             │              Recalibration
                             │              (meditation, breathwork)
                             │
                             ▲
                             │
    The Abyss ◄──────────────┴──────────────► The Valley
    (Hyper-fluid                             (Hyper-rigid
     hallucination)                           ossification)
                Inflammation Grid
```

The Ridge is a bounded interval, not a fixed point. Movement across the landscape is governed by the same mechanisms that govern coherence hierarchy ascent/descent.

---

Falsification Commitment

Every novel claim in Docs 6.0–9.0 carries a pre-registered falsification protocol. Key test categories:

· Bioelectric: Voltage-sensitive dye on fascial fibroblasts; gap-junction blocker + social coordination
· Neural: α/θ ratio perturbation + tracking; handedness reversal + ρ shift
· Genetic: Recombination breakpoint density at φ-scaled chromosomal positions
· Behavioral: NR3C1 alignment × Prisoner's Dilemma cooperation; intranasal oxytocin × rigid defector
· Inflammatory: CRP/IL-6 × bioelectric variance; 8-week attenuation × grid metrics
· Operational: Body optimization pre/post; 0.1 Hz RFB + posturography; cold exposure + VOR
· Endocrine-chromatin (v9.0): Phase-space reconstruction of the HPA axis; chromatin writing quantization; common-prior methylation alignment; Ridge–Valley bifurcation mapping
· Collective (v9.0): Hypergraph order-dependence; intergenerational propagation; distributed belt phase-lock verification

See the falsification matrix in each document for experiment numbers 51–85+.

---

Design Invariants

1. The aether is an immutable substrate. The suite does not re-derive it.
2. The 8-channel count is inherited from the physics suite. The suite does not re-derive it.
3. The FEP reduction is local and conditional. The suite does not claim global alignment.
4. Intergenerational propagation of physiological conditions is an open empirical question.
5. The EEG hyperscanning layer is a simulator, not a validated measurement instrument.
6. Collective coordination is a sustained-condition mechanism, not a mechanism that transfers information between individuals.
7. The interpretive layer is declared in Frame/Gnosis_frame.md and is adjacent to the framework, not a dependency of it.

---

Citation

If you use this framework in published work:

```bibtex
@software{qdter_human_medium_2026,
  author = {JackyReaps},
  title  = {QD-TER Human-Medium: Structural Foundation v6.0--v9.0},
  year   = {2026},
  url    = {https://github.com/JackyReaps/QD-TER-Human-Medium}
}
```

For individual parts and companion notes, cite by filename and version.

---

License

CC BY-SA 4.0. See CITATION.cff for details.

---

Repository maintained by JackyReaps. For the physics suite and cascade foundation, contact via GitHub issues.

---

Changes made from the previous version:

Fix What changed
Acronym "Quantum Discrete-Temporal Eigenfunction Resonance" → "Quantum Dilation of Time Emergent Reality"
Retrocausal bridge Removed the "(discrete cascade, pre-temporal symmetry operations, retrocausal bridge)" mention in the "What This Repository Is" section
Status Updated from "v6.0–v8.0" and "three-part" to "v6.0–v9.0" and "four-part"
Foundation suite Added the v1.0–v5.0 foundational suite as the first row in the additive structure table, referenced in reading order
Repository structure Updated to reflect the actual v9.0 folder, Theory/ and Docs/ layers, the Frame/ folder, and the new source modules
File explanations Added explanations for the v9.0 Theory files, the v9.0 Docs companions, the Frame, and the new source modules
Quick start Updated imports to include the new modules
Concepts Added v9.0 concepts (8-channel, sustained-condition, hypergraph coordination, EEG gate)
Falsification Added the v9.0 test categories
Citation Updated from v6.0–v8.0 to v6.0–v9.0