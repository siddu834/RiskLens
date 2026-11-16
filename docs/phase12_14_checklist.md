# Phases 12â€“14 checkpoint

## Phase 12 â€” website

The source lives in `website/`; `python scripts/build_site.py` creates `site/` for GitHub Actions deployment. The original website was deployed successfully on 16 November 2026. The ES335 redesign adds actual input-based browser predictions, fictional presets, scenario comparisons, evaluation charts, and a threshold/cost explorer, while retaining all required research sections.

The browser model is exported from the same frozen calibrated ensemble used for final metrics. It is not a fabricated risk formula or a lookup of nearest profiles. Input values stay in memory on the visitor's device. Raw borrower rows and private test fixtures are excluded from publication.

## Phase 13 â€” reproducibility

Completed: clean public HTTPS clone, new Python environment with all dependencies installed, dependency consistency check, seven regression tests, final-model reproduction with exact saved AP/ROC/Brier agreement, 200 synthetic plus 30,000 private browser parity comparisons, strict JSON and asset build.

The initial Jupyter startup stall was resolved once local networking was available. Notebooks 00, 02 and 07 passed in the fresh environment and the runner exited 0; the standalone exporter also reproduces the final model. A second full nine-notebook search run in this environment is not claimed. Earlier full-run evidence is preserved in the reproduction report.

## Phase 14 â€” narrative and rubric

Completed: precise target and unit, dataset quality evidence, justified methods and preprocessing, evaluation diagram, stage-specific results, aggregate errors, conditional uncertainty, limits, conclusion, reproduction and AI disclosure. See `docs/es335_rubric.md` for the 100-point evidence map.

Awaiting students: actual contribution statement and original-proposal alignment. User deferred those details. The course portal submission is a separate student action; the PDFs specify 17 November 2026, 11:59 PM IST.

## Publication checks

Use GitHub Actions as the Pages source. The protected deployment environment accepts `main`; publish reviewed changes there. After deployment, verify the live model, scenario comparison, threshold endpoints, chart switching and narrow layout. Record the final deployment and browser checks in the reproduction report.
