# RiskLens — Preprocessing Decisions

## 1. Cleaning Rules

| Issue                                        | Decision                                                                             | Reason                                                                                                      |
| -------------------------------------------- | ------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------- |
| Age = 0                                      | Replace with NaN                                                                     | Age zero is an invalid borrower age.                                                                        |
| Late-payment values 96 and 98                | Replace with NaN and create separate indicator features for each late-payment column | These values are unusual and may represent sentinel values rather than genuine counts.                      |
| Extreme RevolvingUtilizationOfUnsecuredLines | Cap at the 99th percentile, calculated using training data only                      | Reduces the influence of extreme observations while avoiding data leakage.                                  |
| Extreme DebtRatio                            | Cap at the 99th percentile, calculated using training data only                      | Reduces the influence of extreme observations while preserving most observations.                           |
| MonthlyIncome missing                        | Median imputation with a missing-value indicator                                     | Median imputation is less sensitive to extreme values, and the indicator preserves missingness information. |
| NumberOfDependents missing                   | Median imputation with a missing-value indicator                                     | Preserves all customers and allows the model to use missingness information.                                |

## 2. Feature Engineering

No additional engineered features will be introduced in the initial preprocessing stage.

Additional features may be evaluated later through model validation to determine whether they improve predictive performance.

## 3. Data Leakage Prevention

* All learned preprocessing parameters will be fitted using training data only.
* Validation and test data will only be transformed using parameters learned from training data.
* The original dataset will remain unchanged.

## 4. Evaluation Strategy

The preprocessing decisions will be evaluated during model development using appropriate classification metrics, especially metrics suitable for an imbalanced target.


## 5. Preprocessing Justification

### 5.1 Handling Invalid Age Values

**Transformation:** Replace age values equal to zero with NaN.

**Reason:** Age zero is an invalid borrower age and should not be treated as a genuine numerical observation.

**Type:** Fixed rule. It does not require learning parameters from the dataset.

**Data Leakage Prevention:** This transformation uses a predefined rule and does not calculate statistics from validation or test data.

### 5.2 Handling Sentinel Values in Late-Payment Features

**Transformation:** Replace values 96 and 98 with NaN in all three late-payment columns. Create a separate binary indicator for each column to identify these unusual values.

**Reason:** EDA identified these values as unusual observations that may represent sentinel values rather than genuine late-payment counts. The indicators preserve information about which observations contained these values.

**Type:** Fixed rule. The values 96 and 98 are predefined based on EDA.

**Data Leakage Prevention:** No parameters are learned from validation or test data. The same predefined transformation is applied consistently to all datasets.

### 5.3 Capping Extreme Revolving Utilization

**Transformation:** Cap values of `RevolvingUtilizationOfUnsecuredLines` at the 99th percentile.

**Reason:** EDA identified extremely large values in this feature. Capping is intended to reduce the influence of extreme observations while retaining the customers.

**Type:** Learned transformation. The 99th-percentile threshold is calculated using training data only.

**Data Leakage Prevention:** The threshold is learned from the training data and reused to transform validation and test data.

### 5.4 Capping Extreme Debt Ratio

**Transformation:** Cap values of `DebtRatio` at the 99th percentile.

**Reason:** EDA identified extremely large values in this feature. Capping is intended to reduce the influence of extreme observations.

**Type:** Learned transformation. The 99th-percentile threshold is calculated using training data only.

**Data Leakage Prevention:** The threshold is learned from the training data and reused for validation and test data.

### 5.5 Handling Missing Monthly Income

**Transformation:** Replace missing `MonthlyIncome` values with the median and add a missing-value indicator.

**Reason:** Monthly income contains a considerable proportion of missing values. Median imputation preserves observations and is less sensitive to extreme values than mean imputation. The indicator preserves information about missingness.

**Type:** Learned transformation. The median is calculated using training data only.

**Data Leakage Prevention:** The training median is reused when transforming validation and test data.

### 5.6 Handling Missing Number of Dependents

**Transformation:** Replace missing `NumberOfDependents` values with the median and add a missing-value indicator.

**Reason:** This preserves customers with missing dependent information while allowing the model to use missingness information.

**Type:** Learned transformation. The median is calculated using training data only.

**Data Leakage Prevention:** The training median is reused when transforming validation and test data.

### 5.7 Feature Scaling

**Transformation:** Apply StandardScaler when required by the selected machine-learning model.

**Reason:** Numerical features have different scales. Standardisation can help scale-sensitive algorithms learn more effectively.

**Type:** Learned transformation. The mean and standard deviation are calculated using training data only.

**Data Leakage Prevention:** The scaler is fitted on training data and reused to transform validation and test data.

### 5.8 Pipeline-Based Preprocessing

All learned transformations will be included in a scikit-learn pipeline.

During model training and cross-validation, the pipeline will learn imputation values, percentile thresholds, and scaling parameters from the corresponding training fold only.

Validation and test data will only be transformed using parameters learned from training data.

The target variable `SeriousDlqin2yrs` will not be included among the input features.

The original dataset will remain unchanged.
