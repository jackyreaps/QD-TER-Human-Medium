# QD-TER Human-Medium

**Quantum Dilation of Time Emergent Reality — Human-Medium Layer**

Human-Medium Layer of the QD-TER framework: multi-scale biophysical
architecture of geometric fields, dielectric waveguides, and hypergraph
dynamics. This repository contains the operational documents, production
code, and falsification protocols for the QD-TER Human-Medium suite
(v6.0–v9.0), built on the foundational suite (v1.0–v5.0).

**Status:** Parts I–IV published. The four-part additive structure is
complete.

---

## Table of contents

- [Search and discovery keywords](#search-and-discovery-keywords)
- [What this repository is](#what-this-repository-is)
- [The four-part structure](#the-four-part-structure)
- [Repository structure](#repository-structure)
- [Full file descriptions](#full-file-descriptions)
- [Quick start](#quick-start)
- [Core concepts](#core-concepts)
- [Strategic landscape](#strategic-landscape)
- [Design invariants](#design-invariants)
- [Citation](#citation)
- [License](#license)

---

## Search and discovery keywords

This repository is indexed for the following concepts to improve
discoverability across search engines, repository search, and
cross-disciplinary browsing.

| Category | Keywords |
|---|---|
| **Consciousness and system reduction** | consciousness, hard problem of consciousness, free-energy principle, FEP reduction, non-dual adaptation, agency, gnosis |
| **Biophysics and somatic structures** | biophysics, quantum biology, dielectric waveguides, myofascial lattice, body-as-antenna, bioelectric decoupling, embodied cognition |
| **Neuro-dynamics and hyperscanning** | neuroscience, EEG hyperscanning, inter-brain coherence, neural oscillations, brain coherence, cognitive neuroscience |
| **Mathematical modeling and chaos theory** | hypergraph dynamics, chiral manifold, Takens embedding, rheology, dynamical systems, differential geometry, Riemannian metrics, phase-space reconstruction |
| **Cellular and endocrine pathways** | endocrine-chromatin, chromatin residue, pulsatile signaling, Sigma-1 gateway, epigenetics, endocrine system, peptidein, non-coding translation |
| **Project architecture** | qd-ter, human-medium, falsification matrix, coherence hierarchy, operational framework, framework architecture, sustained conditions |

---

## What this repository is

The public implementation layer of the QD-TER framework — the bridge
between the abstract physics suite and the measurable human organism.

- **Operational documents** (v6.0–v9.0) mapping abstract structure to
  biology, game theory, and daily practice.
- **Production code** computing measurable quantities: dielectric
  Reynolds number, bioelectric decoupling, strategic topology,
  endocrine-chromatin writing, inter-brain coherence.
- **Falsification protocols** with pre-registered experiments.
- **Test suites** verifying the code against the document claims.

Nothing here derives the fundamental constants ($\varepsilon_0$,
$\mu_0$, $G_N$, $\alpha_{EM}$). The aether is treated as an immutable
substrate; the 8-channel residual structure is inherited from the
physics suite; and the human organism is modeled as a phase-locked
dielectric interface rather than a source of the substrate itself.

---

## The four-part structure

| Part | Document | Adds |
|---|---|---|
| **Foundation** | v1.0–v5.0 | Substrate layer: body-as-antenna model, P-V-C triad, myofascial lattice as dielectric |
| **Part I** | v6.0 | Control layer: authorship, inherited load, coherence hierarchy ($0/7 \to 7/7$) |
| **Part II** | v7.0 | Architecture layer: P-V-C triad, $\mathcal{R}$-operator, $\alpha/\theta$ signature, strategic landscape, $Re_\varepsilon$ |
| **Part III** | v8.0 | Implementation layer: body optimization regimen, Sigma-1 gateway, falsification matrix |
| **Part IV** | v9.0 | Mechanism layer: endocrine-chromatin axis, hypergraph coordination, sustained conditions |

**Reading order:** v1.0–v5.0 → v6.0 → v7.0 → v8.0 → v9.0.

### Sub-document: Peptidein Load Dynamics

**Location:** `QD-TER_HumanMedium_v9.0/Theory/Peptidein_load_dynamics.md`

v9.0 established the endocrine-chromatin write pipeline. This
sub-document supplies the load-dynamics layer that v9.0 left unmodeled:
the peptidein substrate of the 8-channel sector, and the specific
biophysical constraint that causes system failure.

**The contribution.** Failure is not caused by total peptidein load.
It is caused by the conjunction of local density (Number) and spatial
distribution (Location). A saturated chromatin-adjacent channel jams
the loop; a mislocalized immune peptidein triggers a false-flag
response. Both must be measured separately.

**Delivered:**

- **Number–Location diagnostics** in `check_spatial_criticality()`.
  Local jamming (max saturation fraction), global jamming (aggregate
  load / aggregate capacity), and location error (total-variation
  distance from the expected distribution).
- **Sigma-1 clearance operator** with two modes: accelerated
  degradation for density failures, re-trafficking for location
  failures, compound correction for both. Working gamma is recomputed
  from the immutable baseline on each call, so acceleration does not
  compound across recovery cycles.
- **Empirical anchoring** to the 2026 TransCODE peptidein discovery,
  the OLMALINC pan-essential chromatin anchor, and Sigma-1R
  nuclear-envelope chromatin-remodeling recruitment.

**Files:**

| Path | Purpose |
|---|---|
| `QD-TER_HumanMedium_v9.0/Theory/Peptidein_load_dynamics.md` | Sub-document specification |
| `src/manifold/peptidein_load.py` | `PeptideinLoad`, `Sigma1Gateway` |
| `src/manifold/Endocrine_chromatin.py` | Extended with `process_with_peptideins()` |
| `tests/Test_peptidein_load.py` | Verification suite |

**Falsification protocols:** PE-PLD.A through PE-PLD.D, specified in
the sub-document. The central test is whether directivity loss
correlates with local binding-site saturation rather than total load.

---

## Repository structure
