# Final Model Choice — RiskLens

## 1. Selected Model

Tuned XGBoost with isotonic probability calibration.

## 2. Reason for Selection

Tuned XGBoost achieved the highest ROC-AUC (0.864819) and PR-AUC (0.400979) among the evaluated models.

After isotonic calibration, its Brier score improved from 0.139478 to 0.049029, slightly outperforming calibrated Random Forest (0.049563).

Therefore, calibrated Tuned XGBoost was selected as the final candidate based on its ranking performance and probability calibration.

## 3. Class Imbalance Handling

The selected XGBoost model uses scale_pos_weight to account for class imbalance.

## 4. Probability Calibration

The model uses isotonic probability calibration with 5-fold cross-validation.

## 5. Reporting Threshold

The threshold analysis identified:

* 0.23 as the threshold with the highest F1-score.
* 0.09 as the threshold with the lowest illustrative business cost.

A threshold of 0.09 is selected provisionally for risk screening because the illustrative cost function assigns a higher penalty to false negatives.

These costs are assumptions and should not be interpreted as actual financial losses.

## 6. Test Set Policy

The model and reporting threshold were selected using development-set results only.

The locked test set will be evaluated once. Its results will not be used for further model or threshold tuning.
