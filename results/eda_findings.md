# RiskLens — Exploratory Data Analysis Findings

## 1. Data Source and Row Meaning

The dataset is used to predict whether a borrower experiences serious delinquency within the next two years.

* Target variable: `SeriousDlqin2yrs`
* Each row represents one borrower/customer.
* Each column represents a customer characteristic or credit-related variable.
* The dataset contains numerical features and missing-value information.

The 10 input features are:

1. `RevolvingUtilizationOfUnsecuredLines`
2. `age`
3. `NumberOfTime30-59DaysPastDueNotWorse`
4. `DebtRatio`
5. `MonthlyIncome`
6. `NumberOfOpenCreditLinesAndLoans`
7. `NumberOfTimes90DaysLate`
8. `NumberRealEstateLoansOrLines`
9. `NumberOfTime60-89DaysPastDueNotWorse`
10. `NumberOfDependents`

## 2. Dataset Overview

The development dataset contains:

* Total rows: 120,000
* Total columns: 11
* Input features: 10
* Target variables: 1

The target variable has two possible values:

* `0`: The borrower did not experience serious delinquency within two years.
* `1`: The borrower experienced serious delinquency within two years.

### Target Distribution

| Target | Number of customers | Percentage |
| ------ | ------------------: | ---------: |
| 0      |             111,979 |    93.316% |
| 1      |               8,021 |     6.684% |
| Total  |             120,000 |       100% |

The overall default rate is approximately **6.684%**.

This indicates that the target variable is imbalanced because non-default customers greatly outnumber default customers.

The problem is a binary classification task.

## 3. Missing Data Findings

Missing values were investigated across the features.

Two important features contain missing values.

### MonthlyIncome

* Missing values: 23,675
* Missing percentage: 19.73%
* Default rate when income is missing: 5.57%
* Default rate when income is available: 6.96%

### NumberOfDependents

* Missing values: 3,128
* Missing percentage: 2.61%
* Default rate when dependents are missing: 4.41%
* Default rate when dependents are available: 6.74%

### Observations

* `MonthlyIncome` contains a considerable proportion of missing values.
* `NumberOfDependents` has fewer missing values.
* For both features, customers with missing values have lower observed default rates than customers with available values.
* Missingness may contain useful information about borrower characteristics.

### Preliminary Decision

Missing values should be handled during preprocessing rather than deleting all affected customers automatically.

Missingness indicators are considered:

* `MonthlyIncome_missing`: 1 if income is missing, otherwise 0.
* `NumberOfDependents_missing`: 1 if dependents information is missing, otherwise 0.

Their actual usefulness should be evaluated during model validation.

## 4. Sentinel Value Investigation: 96 and 98

Three late-payment features were investigated:

1. `NumberOfTime30-59DaysPastDueNotWorse`
2. `NumberOfTime60-89DaysPastDueNotWorse`
3. `NumberOfTimes90DaysLate`

All three columns contain unusual values of 96 and 98.

### Value Counts

In each of the three columns:

* Value 96: 2 customers
* Value 98: 212 customers

### Target Rates

| Value    | Number of customers | Default rate |
| -------- | ------------------: | -----------: |
| 96       |                   2 |         100% |
| 98       |                 212 |       54.25% |
| Below 96 | Remaining customers |        6.60% |

The investigation also showed:

* The same 2 customers have value 96 across all three columns.
* The same 212 customers have value 98 across all three columns.
* These values occur together in all three late-payment features.

These values are unusual and may represent special or sentinel values rather than ordinary late-payment counts. The same 214 customers have these values in all three late-payment columns.

They should not automatically be treated as genuine counts.

Further investigation is required before deciding whether to replace them, cap them, or create special indicator features.

## 5. Outliers and Unusual Values

Histograms, boxplots, minimum values, and maximum values were examined.

### Age

* Minimum age: 0.
* The boxplot shows unusually low and high age observations.
* Age 0 is suspicious because a borrower is unlikely to have an actual age of zero. The notebook identifies one such row.
* The maximum age is 109.
* These observations require investigation.

### Revolving Utilization

* Maximum value: 50,708.
* Several extremely large values were observed.
* Most observations are concentrated near lower values.
* The distribution is strongly right-skewed.

### Debt Ratio

* Maximum value: 329,664.
* Very large extreme values were observed.
* These values require investigation before preprocessing.

Extreme values should not automatically be removed because they may contain useful information about borrower risk.

## 6. Late-Payment Feature Distributions

The three late-payment columns were examined using value counts.

The majority of customers have zero recorded late payments.

### NumberOfTime30-59DaysPastDueNotWorse

* 0: 100,794 customers
* 1: 12,844 customers
* 2: 3,689 customers
* 3: 1,421 customers
* 4: 581 customers
* 5: 266 customers
* 96: 2 customers
* 98: 212 customers

### NumberOfTimes90DaysLate

* 0: 113,294 customers
* 1: 4,230 customers
* 2: 1,256 customers
* 3: 530 customers
* 4: 238 customers
* 96: 2 customers
* 98: 212 customers

### NumberOfTime60-89DaysPastDueNotWorse

* 0: 113,881 customers
* 1: 4,626 customers
* 2: 883 customers
* 3: 254 customers
* 4: 91 customers
* 96: 2 customers
* 98: 212 customers

The distributions are highly concentrated at zero, with a small number of customers having repeated late payments.

## 7. Default Rate by Age Groups

Age was divided into six groups to investigate how delinquency rates change with age.

| Age group | Default rate |
| --------- | -----------: |
| 0–25      |       10.99% |
| 25–35     |       10.87% |
| 35–45     |        8.81% |
| 45–55     |        7.61% |
| 55–65     |        4.67% |
| 65–120    |        2.46% |

### Observations

* Younger customers have higher default rates.
* Default rates generally decrease as age increases.
* The relationship suggests that age may be a useful predictive feature.

### Age Group Counts

| Age group | Customer count |
| --------- | -------------: |
| 0–25      |          2,456 |
| 25–35     |         14,721 |
| 35–45     |         23,875 |
| 45–55     |         29,329 |
| 55–65     |         26,769 |
| 65–120    |         22,850 |

## 8. Default Rate by Revolving Utilization

Revolving utilization was divided into five groups.

| Utilization group | Default rate |
| ----------------- | -----------: |
| 0–0.3             |        2.23% |
| 0.3–0.6           |        6.63% |
| 0.6–0.9           |       13.49% |
| 0.9–1.0           |       19.31% |
| Above 1.0         |       37.50% |

### Observations

* Default rates increase as revolving utilization increases.
* Customers with higher credit utilization have higher observed delinquency rates.
* The group above 1.0 has a particularly high default rate.
* This feature appears potentially useful for predicting borrower risk.

### Utilization Group Counts

| Utilization group | Customer count |
| ----------------- | -------------: |
| 0–0.3             |         74,347 |
| 0.3–0.6           |         17,524 |
| 0.6–0.9           |         12,163 |
| 0.9–1.0           |         13,326 |
| Above 1.0         |          2,640 |

## 9. Correlation Analysis

A Pearson correlation heatmap was generated for numerical features.

The strongest correlations with the target variable are:

### Strongest Positive Correlations

| Feature                              | Correlation |
| ------------------------------------ | ----------: |
| NumberOfTime30-59DaysPastDueNotWorse |    0.125012 |
| NumberOfTimes90DaysLate              |    0.117131 |
| NumberOfTime60-89DaysPastDueNotWorse |    0.102294 |
| NumberOfDependents                   |    0.045636 |

### Strongest Negative Correlations

| Feature                         | Correlation |
| ------------------------------- | ----------: |
| age                             |   -0.112322 |
| NumberOfOpenCreditLinesAndLoans |   -0.032654 |
| MonthlyIncome_missing           |   -0.022092 |
| MonthlyIncome                   |   -0.018634 |
| NumberOfDependents_missing      |   -0.014885 |

### Observations

* The three late-payment features have the strongest positive correlations with the target.
* Age has the strongest negative correlation with the target.
* Revolving utilization has an almost zero Pearson correlation (-0.000896) with the target. This does not contradict its clear relationship with default rates across utilization groups; Pearson correlation measures only a linear relationship and can miss nonlinear patterns.
* The missingness indicators have weak negative correlations with the target.
* Correlation does not establish causation and does not necessarily capture all predictive patterns.

### Correlations Among Late-Payment Features

The pairwise Pearson correlations among the three late-payment features are:

| Feature Pair                        | Correlation |
| ----------------------------------- | ----------: |
| 30–59 days late and 90 days late    |    0.983642 |
| 30–59 days late and 60–89 days late |    0.986941 |
| 90 days late and 60–89 days late    |    0.992823 |

These correlations are extremely high when all rows are included.

### Sensitivity Check: Excluding Sentinel Values

A temporary sensitivity check was performed by calculating the same correlations after excluding rows in which any of the three late-payment features had a value of 96 or 98. The original `dev` dataset was not modified.

| Feature Pair                        | Correlation after excluding sentinel rows |
| ----------------------------------- | ----------------------------------------: |
| 30–59 days late and 90 days late    |                                  0.220923 |
| 30–59 days late and 60–89 days late |                                  0.306186 |
| 90 days late and 60–89 days late    |                                  0.295939 |

The correlations decrease substantially after excluding these rows. This indicates that the unusual 96 and 98 observations strongly influence the correlations calculated on the full dataset. The values should therefore be investigated during preprocessing; this check alone does not determine how they should be treated.

## 10. Important Predictive Findings

Based on the univariate analysis and default-rate comparisons:

1. Age appears useful because default rates generally decrease with age.
2. Revolving utilization appears useful because default rates increase substantially with utilization groups.
3. Late-payment features may contain important information about borrower delinquency.
4. Missing `MonthlyIncome` and `NumberOfDependents` values show differences in observed default rates compared with available values.
5. Sentinel values 96 and 98 show unusually high default rates and strongly influence the pairwise correlations among the late-payment features.

These are preliminary findings. Their actual predictive importance must be evaluated using validation data and machine-learning models.

## 11. Data Quality Risks

The following issues were identified:

* The target variable is imbalanced.
* `MonthlyIncome` contains missing values.
* `NumberOfDependents` contains missing values.
* Age contains a suspicious value of zero.
* Revolving utilization contains extremely large values.
* `DebtRatio` contains extremely large values.
* The late-payment features contain unusual values of 96 and 98.
* The three late-payment features have very high pairwise correlations when sentinel rows are included; these correlations are substantially lower after excluding those rows for the sensitivity check.
* Data leakage must be avoided during preprocessing and model training.

## 12. Preliminary Preprocessing Decisions

Based on the EDA findings, the following actions should be considered:

1. Investigate and handle missing `MonthlyIncome` values.
2. Investigate and handle missing `NumberOfDependents` values.
3. Consider creating missingness indicators for both features.
4. Investigate age values of zero.
5. Investigate extreme revolving utilization and `DebtRatio` values before deciding whether to cap or transform them.
6. Investigate sentinel values 96 and 98 before treating them as ordinary numerical counts.
7. Investigate the influence of sentinel values on correlations among late-payment features before making feature-selection decisions.
8. Use stratified splitting where appropriate to preserve the target distribution.
9. Fit preprocessing transformations using training data only.
10. Evaluate model performance using suitable classification metrics, especially because the target is imbalanced.

No final outlier removal, sentinel replacement, or imputation strategy is decided at this EDA stage.

## 13. Overall Conclusion

The EDA reveals several potentially useful patterns in borrower credit data.

Age and revolving utilization show clear relationships with observed delinquency rates. Late-payment features may also provide useful information about borrower risk.

However, the dataset contains missing values, suspicious observations, extreme numerical values, and unusual sentinel values that require careful treatment.

These findings will guide the preprocessing, feature engineering, and model development stages of RiskLens.
