# RiskLens reproduction report

Date: 12 November 2026. Source data was downloaded from the user-provided folder; raw data and row-level predictions remain excluded from version control.

## Verified final-model evaluation

The original final-model parameters, seed, stratified split, calibration method and reporting threshold were retained. Parallel workers were limited to two for local reliability. The test was not used to select new parameters or thresholds.

| Metric | Historical result | Fixed-model rerun |
|---|---:|---:|
| roc_auc | 0.869142 | 0.869424 |
| pr_auc | 0.404330 | 0.404470 |
| brier_score | 0.048683 | 0.048665 |
| precision | 0.403259 | 0.407879 |
| recall | 0.493766 | 0.495761 |
| f1_score | 0.443946 | 0.447546 |

Small differences remain. These are reproduction differences, not evidence that maintenance improved predictive performance. The exact cause has not been isolated.

## Data audit

- Source CSV SHA-256: `1bd46da486a5708c58c7b01a034fae2a13b327f6f7b62ea7ba4fe3b5824b24ac`.
- Data dictionary SHA-256: `b49c9930b74ea7a8a7f7f2daa2ff34302339a60599647ebbe3178613a606540b`.
- 150,000 records, 10 features, 10,026 positive labels.
- 609 duplicate rows including the label; 646 duplicate feature profiles.
- 173 of 30,000 holdout rows have feature profiles present in development.
- Excluding these profiles leaves 29827 test rows: ROC-AUC 0.869018, average precision 0.403996, Brier score 0.048603.

Matching profiles do not prove borrower identity. This subset is a diagnostic of the existing test data, not a new independent holdout. Future experiments should consider grouping duplicate feature profiles before splitting and conduct model selection entirely within development data.

## Search and calibration

The 20-trial rerun search selected depth 5, learning rate 0.03, minimum child weight 7, subsample 0.9 and column subsample 0.8 (development average precision 0.4012569). The original search selected different parameters. The original frozen configuration was retained in notebooks 05–08 and in the final test above. Search CV scores reuse selection folds and are not unbiased nested-CV estimates.

Reproduced out-of-fold calibration Brier comparisons:

```text
Random Forest:
Before: 0.09592507710207476
After: 0.04956315564150904

XGBoost:
Before: 0.1394776850938797
After: 0.04905564552811319
```

The fixed model's threshold-analysis OOF ROC-AUC is 0.864500, average precision 0.399072, and Brier score 0.049035. The recomputed F1 optimum is 0.22; the illustrative cost optimum is 0.09. The final reporting threshold remains the original 0.23.

## Execution evidence

All nine notebooks completed their computational cells without recorded cell errors. Outputs were refreshed for matching source cells. The new CV export cells were separately exercised using recovered summaries; some stored CV values are rounded to six decimals. Future full runs export variables directly.

| Notebook | Seconds |
|---|---:|
| 00_lock_split.ipynb | 22.29 |
| 01_eda.ipynb | 18.20 |
| 02_preprocessing_check.ipynb | 13.74 |
| 03_baselines.ipynb | 14.95 |
| 04_models.ipynb | 397.81 |
| 05_calibration.ipynb | 574.56 |
| 06_thresholds.ipynb | 61.47 |
| 07_final_test.ipynb | 25.09 |
| 08_errors_shap.ipynb | 35.19 |

The initial Windows execution harness emitted joblib cleanup warnings and exited abnormally after completed notebooks. The shipped runner uses the Windows selector event loop and its split-notebook smoke test exited successfully (code 0). The shipped runner was not used for a second complete training run. Timings depend on local hardware and include notebook startup.

Seven lightweight regression tests and the environment dependency check passed before final packaging; final verification passed on 14 November 2026 (seven tests, strict JSON and site assets, JavaScript syntax, and Git whitespace checks). Website assets and strict JSON passed build validation. The local browser displayed final metrics and all five figures successfully. Live GitHub Actions and Pages deployment are not verified because the GitHub integration denied branch creation.

The environment snapshot is recorded separately. Model-serving, fairness certification and financial savings are not claimed.

## Phase 13 clean-source check — 15 November 2026

A clean source directory was extracted from a local Git snapshot of the prepared changes. Windows denied the local Git clone helper, so this does not verify a remote fresh clone. Only the two original data files were copied separately; no split files or fitted models were supplied.

Using the existing validated environment, the shipped runner completed notebooks 00, 02 and 07 and exited successfully (code 0). Timings were 17.59, 15.25 and 26.67 seconds respectively. Every numeric final-evaluation field matched the saved reference within `1e-8`; see `results/clean_copy_comparison.json`. A joblib resource-tracker cleanup warning appeared after notebook 02; it did not prevent notebook completion or affect the reproduced metrics. This check covers split creation, preprocessing and the frozen final evaluation, not a second complete hyperparameter search.

The fresh-environment installation is a separate check; its result is recorded in the phase checklist. Local browser checks confirmed the slider, all five figures, keyboard input and a mobile viewport. Remote deployment remains blocked by GitHub access.
