# Error analysis

The reproduced fixed calibrated model at threshold 0.23 has 1,011 false negatives and 1,443 false positives. The following means describe only the first 20 records of each error category; they are illustrative, not representative estimates.

| Feature | First 20 false negatives | First 20 false positives |
|---|---:|---:|
| RevolvingUtilizationOfUnsecuredLines | 0.467 | 0.815 |
| NumberOfTime30-59DaysPastDueNotWorse | 0.450 | 1.550 |
| NumberOfTimes90DaysLate | 0.050 | 0.600 |
| NumberOfTime60-89DaysPastDueNotWorse | 0.150 | 0.600 |

These examples suggest that some missed positive cases have relatively clean recorded repayment histories, while some flagged negative cases have concerning credit indicators. These observations are descriptive, not causal.

## SHAP scope

The plots explain a separately fitted uncalibrated XGBoost model in raw margin (log-odds) units, not the final calibrated ensemble probability. False-negative and false-positive labels come from the final classifier. The SHAP summary uses the first 1,000 development rows. It is not a population-wide importance estimate or a causal explanation.

## Limitations

The historical data, limited features, duplicate profiles, sampling of errors, and incomplete fairness assessment limit operational conclusions. Threshold costs are illustrative. See the reproduction report for the duplicate-profile sensitivity check. The project is an experimental decision-support study.
