# Changelog

All notable changes to the repository. The numbered documents carry their own version numbers (v1.0–v9.0); this file tracks the repository as a whole.

## [Unreleased]

### Added
- **v10.0, Part V: Language as a Gate** (`suite/v10_part5_language_and_descent.md`): finite topological descent as compression, the Otx2/Gbx2 dual engine, symbols as gates, a transience invariant, and Protocols 85–90.
- `theory/finite_topological_descent.md` (structural memo v1.0), `theory/finite_descent_claims.md` (FD1–FD11), `theory/language_claims.md` (L0–L11, LD1–LD10, LI1), `theory/lean/FiniteDescent.lean`, and `CLAIMS.md` §10 with counts.
- `qdter.descent`, `tests/test_descent.py`, and `examples/finite_descent.py`: executable checks of the compression bound, the Fano/Hamming facts, and syndrome decoding.
- `qdter` Python package in a `src/` layout with `pyproject.toml`, installable with `pip install -e ".[dev]"`.
- GitHub Actions workflow running the tests on Python 3.10–3.12.
- `suite/README.md` reading guide; index READMEs for `theory/`, `docs/`, and `adjacent/`.
- `docs/notation.md` (symbol table), `docs/references_audit.md`, and `docs/known_issues.md`.
- `examples/pd_tournament.py`: iterated Prisoner's Dilemma on organism profiles, with tests.
- Full derivation of the FEP reduction (steps 1–5) in `theory/reduction_fep_derivation.md`.
- Abstract for v1.0; keywords for all ten documents.
- `CONTRIBUTING.md`, `.editorconfig`.

### Changed
- Documents renumbered and renamed as `suite/v01_…` to `suite/v09_…`; supporting material moved to `theory/`, `docs/`, `docs/notes/`, and `adjacent/`.
- v6, v7, v9 and the `theory/` files: display equations converted to LaTeX; v9, its companion notes, and the Guild README converted from plain text to Markdown with real headings and tables.
- Document titles normalized to "QD-TER Human-Medium vN.0"; v3.0 now expands QD-TER as "Quantum Dilation of Time Emergent Reality".
- v6–v8 now describe a four-part series; v8 no longer calls v9.0 the cascade foundation (that belongs to the separate physics suite).
- v8: early-work date corrected to 2026; duplicated bibliography merged (41 entries); two wrong citation years corrected.
- v2.0: the Kim et al. (2026) report is described as a single unreplicated report with a published erratum, not as experimental verification.

### Fixed
- v10.0 §9 and the language claims file: the evidence for L8 and L9 is now described as bearing on neighboring questions (the source of brain DMT; adrenochrome as a cause of psychosis) and not as evidence against the proposals, which are untested.
- Case-sensitive import failures on Linux (`EEG_hyperscan`, `Endocrine_chromatin`); tests renamed so pytest collects them.
- Broken integration test (missing imports and fixture).
- Non-causal convolution in `leaky_integrate()`.
- iCOH estimator: per-bin normalization by |S_xy| scored unrelated signals at about 0.65, so the field-level gate flagged almost any input. Replaced with the band-integrated imaginary coherency; simulator now couples with a nonzero phase lag; threshold recalibrated (0.18 to 0.30) on 100 simulated seeds per scenario.
- `coupling_used` in the EEG pipeline output now reports the coupling that was simulated.
- `ChiralManifoldRheology` default `characteristic_node_dimension` changed from 0.05 m to the documented 0.5 m.
- Test baseline in `test_landscape_valley_on_topology_error`.
- Broken code fence in the README citation block; literal `\uXXXX` escapes in v2.0–v4.0.

### Known issues
- See `docs/known_issues.md` (iCOH threshold calibrated on simulated data only; FEP gain normalization; unchecked citations).
