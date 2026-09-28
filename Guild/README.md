

The Guild System — Introduction and Framework Reference

Document ID: GS-001
Version: 1.0
Status: Draft — Entry point to the Guild System
Repository Location: /Guild/README.md
Framework Dependency: QD-TER-Human-Medium v6.0–v9.0 (James Dean, 2026)

---

1. What This Is

This is the entry point to the Guild System — a polycentric, merit-based architecture for collective intellectual work, grounded in the QD-TER Human-Medium framework published at github.com/jackyreaps/QD-TER-Human-Medium.

The Guild System is a new project. It is not part of the QD-TER framework. It does not extend, modify, or derive from the framework's mathematics. It is an application layer: a set of structural, legal, and operational documents that use the QD-TER framework's vocabulary and epistemic discipline to address a specific class of problems — preserving intellectual orientation across a distributed network, detecting institutional drift, preventing ossification, and guaranteeing exit.

Until the Guild System's own operational architecture is complete, this document does nothing more than establish what the framework claims, where those claims live, and why they are relevant to the problems the Guild System exists to solve.

The Guild points to QD-TER, and nothing more.

---

2. What the QD-TER Human-Medium Repository Contains

The repository is the public implementation layer of the QD-TER framework — the bridge between the abstract physics suite and the measurable human organism. It contains operational documents (v6.0–v9.0), production code computing measurable quantities, falsification protocols with pre-registered experiments, and test suites verifying the code against the document claims.

Nothing in the repository derives the fundamental constants. The aether is treated as an immutable substrate; the 8-channel residual structure is inherited from the physics suite; the human organism is modeled as a phase-locked dielectric interface rather than a source of the substrate itself.

2.1 The Four-Part Structure

Part Version Layer Adds
Foundation v1.0–v5.0 Substrate layer Body-as-antenna model, P-V-C triad, myofascial lattice as dielectric
Part I v6.0 Control layer Authorship, inherited load, coherence hierarchy (0/7 → 7/7)
Part II v7.0 Architecture layer P-V-C triad, ℛ-operator, α/θ signature, strategic landscape, Re_ε
Part III v8.0 Implementation layer Body optimization regimen, Sigma-1 gateway, falsification matrix
Part IV v9.0 Mechanism layer Endocrine–chromatin axis, hypergraph coordination, sustained conditions

Reading order: v1.0–v5.0 → v6.0 → v7.0 → v8.0 → v9.0.

2.2 Key Documents

Document Path Role
README.md /README.md Overview, four-part structure, design invariants
CLAIMS.md /QD-TER_HumanMedium_v9.0/Theory/CLAIMS.md Canonical taxonomy of every claim
Non_dual_adaptation.md /QD-TER_HumanMedium_v9.0/Theory/Non_dual_adaptation.md Riemannian metric, parallel transport, holonomy
Gnosis_frame.md /Frame/Gnosis_frame.md Declared interpretive layer
rheology.py /src/manifold/rheology.py Re_ε, strategic topology, cognitive glue
Endocrine_chromatin.py /src/manifold/Endocrine_chromatin.py Takens embedding, 8-channel write vector
EEG_hyperscan.py /src/manifold/EEG_hyperscan.py Field-level phase-lock gate

---

3. The Epistemic Discipline the Guild Adopts

The repository's CLAIMS.md document classifies every claim as exactly one of the following:

Category Meaning
Axiom (inherited) Adopted from the physics suite. Not derived here.
Axiom (modeling) Adopted as an extra assumption in the human-medium layer.
Definition A named object introduced for use.
Derivation Proven from axioms and definitions.
Reduction theorem (conditional) Proven given explicitly stated axioms.
Conjecture Proposed, not proven.
Falsification test An experiment that would discriminate the framework.

The Guild adopts this taxonomy as its own standard. Every Guild artifact — every proof, every training loop, every red-team report — must carry the same classification. This discipline is what separates verifiable contribution from narrative assertion.

---

4. Key Concepts the Guild Adopts

4.1 The Parallel Transport Condition

From Non_dual_adaptation.md, the framework specifies a proposed layer formalizing world-model updates as covariant derivatives on a Riemannian manifold. The key axioms:

· Axiom M (Metric): The world-model parameter space carries a Riemannian metric g_ij(x) derived from QD-TER quantities.
· Axiom V (Intentionality vector): There exists a vector field V on this manifold, transported along update trajectories.
· Axiom Ω (Coherence scalar): The scalar Ω = g_ij V^i V^j is the metric norm of V.

The parallel transport condition ∇_X V = 0 specifies that the intentionality vector is covariantly constant along the update trajectory. An update trajectory that violates this condition produces a nonzero covariant derivative: ‖∇_X V‖ ≠ 0. This quantity is measurable and can be monitored.

The Guild uses this concept as the formal analog for orientation preservation across a distributed network: an institution that maintains phase-locking preserves its founding intentionality; one that shears away has violated the parallel transport condition.

4.2 The Strategic Landscape

From rheology.py, the strategic landscape is defined via the StrategicTopology enumeration:

Position Description
RIDGE The Ridge of Optimal Function: balanced, credible strategic signaling.
ABYSS The Abyss of Decoherence: hyper-fluid strategy fragmentation.
VALLEY The Valley of Ossification: catastrophic structural engine-lock.
TURBULENT Turbulent Decoupling: high velocity, low coherence.

The README describes the Ridge as a bounded interval, not a fixed point. The Grid oscillates between Abyss and Valley via an inflammatory loop.

The Guild uses this landscape to describe institutional states: the Ridge is health; the Valley is the failure mode of ossification; the Abyss is decoherence; Turbulent is drift without direction.

4.3 The Gnosis Frame

The Frame/Gnosis_frame.md document is the declared interpretive layer — adjacent, not a dependency. It offers non-dual pantheism as a working orientation:

· Non-duality: Mind and world are not two substances. Awareness is a localized feature of the same field it appears to observe.
· Immanence: The absolute is not located in a separate realm. It is the world considered in its self-reflective totality.
· Locality: An agent is a localized node in the field — the field appearing as a perspective.
· Invariance under change: A node's orientation can persist through updates to its world-model, provided the update trajectory respects the geometry of the field it moves through.
· Gnosis: Direct knowing is participation in the field, not an external report about it.

The Guild treats the Gnosis frame as the repository itself treats it: as a ground, not the ground. Authority rests on reproducibility, not doctrinal correctness.

---

5. The Guild System: What It Is

The Guild System is a polycentric network of autonomous guilds — each with its own culture, currency, and governance — interoperating through a shared protocol for merit recognition, contribution verification, and idea protection.

It is not a single organization. It is a meta-structure: a minimal shared layer (the Compact) over many sovereign local guilds. The system's purpose is to provide a lawful, merit-based alternative to institutional narrative control — a place where formalists and builders can work together on problems that matter, with their contributions recognized by peers and protected by structure.

The Guild System's founding articles derive from the QD-TER framework's account of collective agency:

1. Public or authorized data only. No covert acquisition. Verifiability is the armor.
2. Non-convertible credits by default. Flow over hoard. The convertibility cap is a feature.
3. The Tax-Integrity Floor. Lawful obligations met. Civic provision supplements, never evades.
4. Civic substitution as a recognized purpose. Provision over exemption.

These four inversions answer the historical failure mode documented in the Templar case: exemption, hoard, patron, and secrecy were the mechanisms of destruction.

---

6. What This Document Does Not Do

This document does not:

· Derive the Guild System's operational architecture.
· Extend or modify the QD-TER framework.
· Claim to prove the framework.
· Substitute for the framework's own documents.

It is an introduction. The Guild System's operational documents — Compact, Guardrails, Fork Protocol, Merit Protocol, Currency Annex, Civic Substitution Annex, Historical Overlay, and others — are being developed separately. When they are complete, this document will be revised to point to them as well.

Until then, this is the relationship: the Guild points to QD-TER, and nothing more.

---

7. Repository Reference Index

Document Path Role
README.md /README.md Overview, four-part structure, design invariants
CLAIMS.md /QD-TER_HumanMedium_v9.0/Theory/CLAIMS.md Canonical taxonomy of every claim
Non_dual_adaptation.md /QD-TER_HumanMedium_v9.0/Theory/Non_dual_adaptation.md Riemannian metric, parallel transport, holonomy
Consolidated_specification.md /QD-TER_HumanMedium_v9.0/Theory/Consolidated_specification.md Meta-level document
Residual_integer_8.md /QD-TER_HumanMedium_v9.0/Theory/Residual_integer_8.md Inheritance chain: 36 → V₄ → 2 → 4 → 8
Reduction_fep.md /QD-TER_HumanMedium_v9.0/Theory/Reduction_fep.md Local, conditional FEP reduction
Gnosis_frame.md /Frame/Gnosis_frame.md Declared interpretive layer
rheology.py /src/manifold/rheology.py Re_ε, strategic topology, cognitive glue
Endocrine_chromatin.py /src/manifold/Endocrine_chromatin.py Takens embedding, 8-channel write vector
EEG_hyperscan.py /src/manifold/EEG_hyperscan.py Field-level phase-lock gate
swarm_apparatus.md /QD-TER_HumanMedium_v9.0/Docs/swarm_apparatus.md Institutional closure
distributed_belt.md /QD-TER_HumanMedium_v9.0/Docs/distributed_belt.md Phase-locked group architecture
collective_antenna.md /QD-TER_HumanMedium_v9.0/Docs/collective_antenna.md Multi-organism arrays
POSSIBLE-NEXT-STEPS.md /POSSIBLE-NEXT-STEPS.md Roadmap for advanced theoretical connections

---

8. Review Cycle

Annual, with framework input. If the QD-TER framework is substantially revised — particularly CLAIMS.md, Non_dual_adaptation.md, or rheology.py — this document is revised in parallel. If the Guild System's operational documents are published, this document is revised to point to them.

---

End of Document GS-001 v1.0