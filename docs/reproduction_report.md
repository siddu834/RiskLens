# RiskLens reproduction report

## Complete fresh-clone verification - 17 November 2026

A new HTTPS clone at commit `2911f5fb5c32df377c8fd115f680f370c973bce5` was tested in a newly created Python 3.13 environment. Dependencies were installed from the documented requirements files and `pip check` passed. Only the original labeled CSV and dictionary were copied into the data directory. The original computational notebook sources were executed through the shipped runner.

All nine notebooks completed with zero cell error outputs, and the runner exited successfully. Total notebook execution time was 17.14 minutes. The frozen final metrics, all 101 threshold rows, calibration data and summary metrics matched the published JSON exactly after parsing. CV metrics differed by at most 0.0000005 because some old CSV entries were rounded to six decimals. The newly exported CSV retains full precision.

The calibrated comparison, paired bootstrap, data audit and browser export were rerun in the same environment. The uncertainty intervals, review-budget counts, test evidence and data-audit JSON matched the published artifacts exactly. All seven regression tests passed. Browser parity passed for 200 profiles with maximum probability error 0.00001069648 and zero classification disagreements. The static site build passed.

Detailed timings and comparisons are in [full_reproduction.json](../results/full_reproduction.json). The environment is recorded in [validated_windows_environment.txt](validated_windows_environment.txt). This full run supersedes the incomplete-run qualifications in the historical entries below.

Windows joblib workers printed resource-tracker cleanup KeyErrors on stderr. These occurred outside notebook cell execution and did not prevent successful completion. Local Jupyter kernels also printed a TCP transport warning. The recorded verification distinguishes these warnings from computational failures.


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

Seven lightweight regression tests and the environment dependency check passed before final packaging; final verification passed on 14 November 2026 (seven tests, strict JSON and site assets, JavaScript syntax, and Git whitespace checks). Website assets and strict JSON passed build validation. The local browser displayed final metrics and all five figures successfully. The original website was subsequently deployed successfully from main on 16 November (run 43859190187).

The environment snapshot is recorded separately. Model-serving, fairness certification and financial savings are not claimed.

## Phase 13 clean-source check — 15 November 2026

A clean source directory was extracted from a local Git snapshot of the prepared changes. Windows denied the local Git clone helper, so this does not verify a remote fresh clone. Only the two original data files were copied separately; no split files or fitted models were supplied.

Using the existing validated environment, the shipped runner completed notebooks 00, 02 and 07 and exited successfully (code 0). Timings were 17.59, 15.25 and 26.67 seconds respectively. Every numeric final-evaluation field matched the saved reference within `1e-8`; see `results/clean_copy_comparison.json`. A joblib resource-tracker cleanup warning appeared after notebook 02; it did not prevent notebook completion or affect the reproduced metrics. This check covers split creation, preprocessing and the frozen final evaluation, not a second complete hyperparameter search.

The fresh-environment installation is a separate check; its result is recorded in the phase checklist. Local browser checks confirmed the slider, all five figures, keyboard input and a mobile viewport. GitHub access was subsequently restored; this historical blocker is resolved.

## ES335 prediction-lab verification — 16 November 2026

- Clean HTTPS clone from public `main` at `45df8f3a0a6595a08fec5be54a357c889b74c083`.
- New Python 3.13 environment: 116 dependencies installed from the pinned requirements plus test requirements using uv. `pip check`: no broken requirements.
- `scripts/export_browser_model.py` rebuilt the original frozen five-member calibrated model from the raw CSV and recreated the original stratified split. Final ROC-AUC, AP and Brier matched the recorded values exactly (maximum difference 0).
- Browser inference comparison: 200 synthetic profiles including missing values, sentinel codes, invalid age and extreme ratios. Maximum absolute probability difference: 0.00001069648.
- Private comparison over all 30,000 test rows: maximum absolute probability difference 0.00001694502; zero classification disagreements at threshold 0.23. The acceptance tolerance is 0.00002, or 0.002 percentage points; the UI displays 0.1-point precision. Float32 sigmoid arithmetic near steep isotonic knots explains the small numerical differences.
- Seven preprocessing/reporting regression tests passed. JavaScript syntax checks, browser parity checks and site build passed.
- Error summaries now use every test record, not only the first 20 errors. Only aggregate summaries are exported publicly.
- A 300-resample percentile bootstrap of the frozen test predictions yields AP interval [0.3809448, 0.4273449]. It is conditional on this model and split, not an interval for the tuned model's gain or for future performance.
- The fresh-environment notebook runner initially stalled at kernel startup without local networking. After networking became available, notebooks 00, 02 and 07 passed in 33.07, 16.83 and 29.14 seconds; the runner exited 0. A nonfatal joblib cleanup warning appeared after notebook 02. Final metrics match the saved reference. A second complete search run in this environment is not claimed; earlier all-notebook evidence remains above.

No model parameters or reporting thresholds were selected using these new test diagnostics. The browser artifact contains tree structures and fitted preprocessing/calibration parameters, not raw borrower rows. Private parity inputs are ignored under `.runs/`.

### Redesign browser checks

The local browser loaded all ten fields, the trained model and aggregate data without console errors. Fictional steady and missed-payment presets produced 1.0% and 54.6%; changing the latter's 90-day count from 1 to 0 gave 36.4%, with a saved-scenario difference displayed. Blank income/dependents were handled; age -1 was rejected and stale predictions cleared. Thresholds 0, 0.5 and 1 matched saved counts; changing the illustrative FN:FP cost from 10:1 to 1:1 moved the grid optimum from 0.09 to 0.50. ROC and calibration switches worked. At a 390-pixel viewport, all ten inputs remained available and there was no horizontal page overflow.

The exported model is packaged as a small manifest plus 15 tree files (100 trees each). This resolves the single-file transfer review size limit without changing the ensemble. Browser and Node tests load all parts before predicting.
