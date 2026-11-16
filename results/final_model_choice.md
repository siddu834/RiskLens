# Final Model Choice — RiskLens

## Fixed reference model

The final evaluation reproduces the originally selected XGBoost configuration with isotonic calibration (`CalibratedClassifierCV`, five folds):

- 300 estimators; maximum depth 4; learning rate 0.05.
- Minimum child weight 5; subsample 0.8; column subsample 1.0; L2 regularization 1.0.
- Positive-class weight is the development negative/positive count ratio.
- Seed 42; two workers in this rerun.

## Reproduction finding

The new 20-trial development search selected depth 5, learning rate 0.03, minimum child weight 7, subsample 0.9 and column subsample 0.8, with average precision 0.4012569. The original search reported 0.4009789 for the fixed reference configuration. These are different runs, not a paired demonstration of improvement. The exact cause of the change has not been isolated.

`cv_results.csv` labels the new search winner explicitly. Notebooks 05–08 retain the original parameters so that the held-out test evaluation is a reproduction of a fixed candidate, not a new test-driven selection. Development selection and reporting reuse folds; their scores are not an unbiased nested-CV estimate.

## Threshold policy

The reporting threshold remains **0.23**, selected by F1 in the original development out-of-fold analysis. **0.09** is the original illustrative cost scenario using `50,000 × FN + 5,000 × FP`. These assumed costs are not measured financial losses or an operational lending policy. Recomputed threshold optima are documented in the reproduction report; they do not automatically change the frozen reporting threshold.

## Holdout policy

The original holdout split and fixed model were rerun. No test outcomes were used to change hyperparameters or thresholds. Current computed results are in `final_test_metrics.json`; historical values are in `original_final_test_metrics.json`. The duplicate-profile subset analysis is a diagnostic, not a newly untouched test set.

The metric labeled PR-AUC is scikit-learn average precision. Training-set calibration figures are diagnostic; out-of-fold comparisons are used for calibration assessment. No statistical significance or real-world lending effectiveness is claimed.
