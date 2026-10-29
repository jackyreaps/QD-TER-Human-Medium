# Known Issues

Open problems in the specification and code that have been identified but not resolved. Each one is a decision for the author, not a bug that can be patched without changing what the framework claims.

## 1. The iCOH threshold and simulator are calibrated on simulated data only

**Where:** [`src/qdter/manifold/eeg_hyperscan.py`](../src/qdter/manifold/eeg_hyperscan.py); `DEFAULT_ICOH_THRESHOLD = 0.30`.

The estimator, the simulator, and the threshold were repaired in this reorganization (see below). What remains open is that every number that makes the gate work is a property of the simulation:

- the coupling lag (`DEFAULT_COUPLING_LAG`, $\pi/4$), which has no empirical basis here;
- the 2% detuning between the two organisms' natural frequencies and the phase-noise model;
- the two-minute default recording length (the slowest engine, 0.2 Hz, cannot be tested for coupling in a few seconds);
- the threshold itself.

Operating characteristics of the repaired gate, over 100 simulated seeds per scenario (source space and through the toy head model agree to within 0.01):

| Scenario | Mean iCOH | 5th–95th percentile | Flagged at 0.30 |
|---|---|---|---|
| Strong coupling (Re 50, glue 0.9, aligned) | 0.57 | 0.44–0.79 | 100% |
| Moderate coupling (Re 10, glue 0.5) | 0.34 | 0.19–0.56 | 57% |
| Low coupling (Re 1, glue 0.2) | 0.17 | 0.04–0.29 | 5% |
| Bioelectrically decoupled, high scalar alignment | 0.17 | 0.05–0.31 | 6% |
| Fully decoupled | 0.07 | 0.03–0.14 | 0% |

Recalibrate on real dyad recordings before treating any of these numbers as a decision boundary. A surrogate test (phase-randomized or time-shifted signals) would give a per-recording significance level instead of a fixed threshold.

**Limitation by design.** Locking with exactly zero phase lag is indistinguishable from volume conduction and is not flagged. That is the price of rejecting volume conduction, and the reason the simulator couples with a nonzero lag.

## 2. Recognition-gain normalization in the FEP reduction

The projected QD-TER rate and the FEP rate agree only if $\Gamma=G$, while the specification sets $\Gamma=\Pi_sG$. Three consistent fixes are listed in [`theory/reduction_fep_derivation.md`](../theory/reduction_fep_derivation.md) §6.

## 3. Citation status

Most 2025–2026 references have not been checked against independent sources, and several entries are too incomplete to verify. See [`references_audit.md`](references_audit.md).

## 4. Rank-3, the 8-channel sector, and the 36-mode waist

If rank counts $\mathbb{F}_2$-dimension, a Rank-3 base has $2^3=8$ elements, matching the 8-channel sector (D8), but Rank-6 would have 64 states against the 36-mode waist (D1). D8 is also derived differently ($4\times 2$). Whether the match at Rank-3 is structural or numerical, and how Rank-6 relates to the waist, are open. See [v10.0 §2.4](../suite/v10_part5_language_and_descent.md) and Protocol 87. The combinatorial facts about the Fano plane and the Hamming code are checked in code; their identification with the ledger is not.

## 5. The Lean skeleton has not been compiled

[`theory/lean/FiniteDescent.lean`](../theory/lean/README.md) targets Lean 4 and uses `axiom` for its carriers. It has not been compiled in this repository, and every conjecture in it is a `True := by sorry` placeholder.

## 6. L1 (block universe and P/NP)

The working draft of v10.0 listed the block-universe collapse of P/NP as a grounding axiom; the first claims draft omitted it. It is restored as Conjecture L1, flagged as not following from its premise, and used nowhere. Decide whether to keep it. See [v10.0 §3.3](../suite/v10_part5_language_and_descent.md).

## 7. L8 and L9 are untested and lack operational definitions

The pineal shunt (L8) and the adrenochrome witness (L9) have no protocol, and neither has been tested: the studies cited in v10.0 §9 address neighboring questions (the source of brain DMT; adrenochrome as a cause of psychosis), not the proposed functions. Each needs an operational definition and a measurable proxy before a protocol can be written. The v10.0 text describes a test route for each.

## Fixed in this reorganization

- **The iCOH estimator could not separate unrelated signals from coupled ones.** It averaged $|\mathrm{Im}\,S_{xy}|/|S_{xy}|$ per bin, which is $|\sin\Delta\varphi|$ and scores about 0.65 for unrelated signals, above the 0.18 threshold, so `field_phase_locked` was true for almost any input. The Kuramoto-locking test passed only because of that offset. The estimator is now the imaginary part of the band-integrated coherency (Nolte et al. 2004 principle); unrelated signals score about 0.07 and a zero-lag common source about 0.004.
- **The simulator coupled B to A with zero phase lag,** which a correct iCOH cannot see. It now uses Kuramoto-Sakaguchi coupling with a lag, and is vectorized (a two-minute pipeline runs in about 0.2 s).
- **`coupling_used` in the pipeline output ignored glue, alignment, and decoupling,** so it reported a value the simulator never used. It now reports the coupling actually simulated.
- **`ChiralManifoldRheology` defaulted `characteristic_node_dimension` to 0.05 m,** while v7.0 §3.5.3, every test, and the example use the documented 0.5 m. The default is now 0.5.
- `leaky_integrate()` in `endocrine_chromatin.py` used `np.convolve(..., mode="same")` with a one-sided kernel, which shifts the output by about half the array and is not causal. It now uses the causal part of the full convolution. The existing bounded-output test passes as a result.
- `test_landscape_valley_on_topology_error` set every channel to 0.05, which put total glue (0.20) below the depletion threshold (0.25), so the code correctly returned ABYSS. The baseline is now 0.08 so the test exercises the topology error it names.
- Module and test files were renamed to lowercase so that imports resolve on case-sensitive file systems.
