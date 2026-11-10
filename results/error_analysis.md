# Error Analysis

## 1. Objective

The purpose of this analysis is to understand the characteristics of customers incorrectly classified by the final calibrated XGBoost model at a threshold of 0.23.

## 2. Error Counts

* False Negatives: 1,015
* False Positives: 1,465

Twenty examples from each category were inspected.

## 3. False Negative Patterns

The inspected false negatives showed relatively low average late-payment counts:

* 30–59 days past due: 0.45
* 90 days late: 0.05
* 60–89 days late: 0.15

Some customers who eventually defaulted had relatively clean late-payment histories in the available features. This may make them difficult for the model to identify.

## 4. False Positive Patterns

The inspected false positives showed:

* Higher average revolving utilization: 0.814.
* Higher 30–59 days past due count: 1.50.
* Higher 90 days late count: 0.65.
* Higher 60–89 days late count: 0.60.

These customers displayed several risk indicators despite not experiencing the target default event during the observation period.

## 5. Conclusion

The inspected examples suggest that the model sometimes misses customers with relatively clean observed payment histories who eventually default.

It also sometimes flags customers with concerning credit indicators who do not default.

These observations illustrate the difficulty of distinguishing actual future defaults from customers who merely exhibit risky financial characteristics.




### SHAP Analysis — Global Takeaways

1. Late-payment history is among the strongest factors influencing the model's predictions.
2. Revolving credit utilization also has a significant impact on predicted default risk.
3. Higher late-payment counts generally push predictions towards default.
4. Age contributes to predictions, with its impact depending on the individual customer's value.
5. The false-negative example shows that some actual defaulters receive low predicted risk.
6. The false-positive example shows that customers with concerning repayment histories can be predicted as defaulters even when they do not actually default.

7. According to the SHAP summary plot, RevolvingUtilizationOfUnsecuredLines is the most influential feature, followed by NumberOfTime30-59DaysPastDueNotWorse and NumberOfTimes90DaysLate.


Overall, SHAP analysis improves interpretability by showing how individual features influence the model's predictions.


## 6. Limitations

Although the model provides useful predictions of customer default risk, it has several limitations:

1. **Predictions are not causal:** The model identifies patterns and relationships in historical data. It cannot establish that a particular feature directly causes a customer to default.

2. **Limited feature availability:** The dataset contains only a limited number of financial and repayment features. It does not provide complete credit bureau history or all information that may influence a lending decision.

3. **Outdated dataset:** The dataset is based on historical data from around 2011. Customer behaviour, economic conditions, and lending practices may have changed, so the model's performance may not transfer directly to current real-world applications.

4. **Data quality issues:** Income information may contain reporting errors or inaccuracies. Missing values, unusual values, and inconsistent records can also affect model predictions.

5. **Threshold selection:** The classification threshold of 0.23 was selected using development data. A real lending institution must consider the actual financial costs of false positives and false negatives before choosing an operational threshold.

6. **Fairness limitations:** This project does not include a complete fairness audit across demographic groups. Features such as age may influence predictions, so potential differences in model performance across groups require further investigation.

**Overall:** These limitations mean that the model should be treated as a decision-support tool rather than an independent system for making final lending decisions.
