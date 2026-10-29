# Contributing

This repository is a theoretical framework with reference code. The most useful contributions are corrections, verified citations, independent checks of the calculations, and improvements to the tests.

## Before you open an issue or pull request

- **Name the document and section** you are commenting on (for example "v7.0 §4.6").
- **Label claims by status** using the taxonomy in [`theory/CLAIMS.md`](theory/CLAIMS.md): axiom, definition, derivation, reduction theorem, conjecture, or falsification test. A claim without a label is treated as a conjecture.
- **Cite sources you have checked.** Give authors, year, journal, and DOI. Please read [`docs/references_audit.md`](docs/references_audit.md) first: wrong years and titles were the most common error found.
- **Make no medical claims.** The documents describe theoretical constructs, not treatment.

## Where files go

| Kind of change | Location |
|---|---|
| A new numbered document | `suite/` (and add it to `suite/README.md`) |
| A formal specification, claim, or derivation | `theory/` (Lean files in `theory/lean/`) |
| An explanatory note or roadmap item | `docs/` (companion notes in `docs/notes/`) |
| Related work the main line does not depend on | `adjacent/` |
| Code | `src/qdter/manifold/`, with a matching `tests/test_*.py` (lowercase) |

## Conventions

- Display equations use LaTeX (`$$ … $$`); symbols that recur across documents are listed in [`docs/notation.md`](docs/notation.md).
- Internal links are relative.
- Run the tests before submitting:

```bash
pip install -e ".[dev]"
pytest
```

Tests marked `xfail` record known issues listed in [`docs/known_issues.md`](docs/known_issues.md). Because they are `strict`, a test that starts passing will fail the run until its marker is removed.
