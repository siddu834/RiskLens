# Phases 12-14 checkpoint

## Phase 12 - website

The source lives in `website/`; `python scripts/build_site.py` creates `site/` for GitHub Actions deployment. The ES335 website was deployed on 16 November 2026. It includes browser predictions from the frozen calibrated model, fictional presets, scenario comparisons, evaluation charts, and a threshold and cost explorer.

The browser model is exported from the same frozen calibrated ensemble used for final metrics. Input values stay in memory on the visitor's device. Raw borrower rows and private test fixtures are excluded from publication.

## Phase 13 - reproducibility

Completed: clean public HTTPS clone, new Python environment with dependencies installed, dependency check, seven regression tests, final model reproduction with exact saved AP, ROC and Brier agreement, 200 synthetic plus 30,000 private browser parity comparisons, strict JSON and asset build.

After local networking became available, notebooks 00, 02 and 07 passed in the fresh environment and the runner exited successfully. The standalone exporter also reproduces the final model. A second full nine-notebook search run in this environment is not claimed. Earlier full-run evidence is in the reproduction report.

## Phase 14 - narrative

The website covers the research question, data quality, preprocessing, methods, evaluation, results, errors, limitations, conclusion, reproduction, and AI assistance. The submitted proposal was later reviewed: the question, data, models, evaluation plan, and threshold interaction align with the completed project. The prediction lab adds an input-based interaction. The confirmed contribution split for both students is in the README.

## Publication checks

GitHub Actions deployed the website from `main`; the project checks passed. The live model, scenario comparison, threshold endpoints, chart switching, and mobile layout were verified. Course portal submission is a separate student action.
