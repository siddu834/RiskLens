# RiskLens — Credit Default Risk Analysis

An end-to-end machine learning project that predicts the probability of a customer experiencing serious financial delinquency within two years.

RiskLens explores data preprocessing, exploratory data analysis, model comparison, hyperparameter tuning, probability calibration, threshold optimization, error analysis, and explainable AI.

---

## Project Overview

Credit risk assessment is an important problem in financial institutions. Identifying customers who may experience serious delinquency can help support better lending decisions.

RiskLens uses machine learning to estimate credit default risk and provides an interactive website to explore model performance and classification thresholds.

**This project is intended as a decision-support tool, not an automated lending authority.**

## Dataset

The project uses the Kaggle **Give Me Some Credit** dataset.

- Target variable: `SeriousDlqin2yrs`
- Development samples: 120,000
- Locked test samples: 30,000
- Input features: 10
- Default rate: approximately 6.68%

The dataset is not included in this repository. Place the required CSV files in the `data/` directory before running the notebooks.

## Machine Learning Workflow

1. Dataset preparation and stratified train-test splitting.
2. Exploratory data analysis (EDA).
3. Missing-value and anomalous-value handling.
4. Data preprocessing and feature transformation.
5. Baseline model development.
6. Model comparison and hyperparameter tuning.
7. Probability calibration using isotonic regression.
8. Classification threshold analysis.
9. Final evaluation on the locked test set.
10. Error analysis and SHAP-based model explanations.

## Final Model Performance

The selected model is a tuned XGBoost classifier with isotonic probability calibration.

| Metric | Test Result |
|---|---:|
| ROC-AUC | 0.8691 |
| PR-AUC | 0.4043 |
| Brier Score | 0.0487 |
| Precision | 0.4033 |
| Recall | 0.4938 |
| F1 Score | 0.4439 |

The classification metrics use a threshold of **0.23**, selected using development data.

The locked test set was reserved for final evaluation rather than model tuning.

## Explainability

SHAP (SHapley Additive exPlanations) was used to investigate feature contributions to model predictions.

The analysis includes:
- Global feature importance.
- False-negative prediction investigation.
- False-positive prediction investigation.

## Interactive Website

The project includes an interactive website for exploring credit-risk evaluation and classification threshold behaviour.

To run it locally from the project root:

```bash
python -m http.server 8000
```

Then open:

```text
http://localhost:8000/website/
```

## Project Structure

```text
RiskLens/
│
├── data/
│
├── notebooks/
│   ├── 00_lock_split.ipynb
│   ├── 01_eda.ipynb
│   ├── 02_preprocessing_check.ipynb
│   ├── 03_baselines.ipynb
│   ├── 04_models.ipynb
│   ├── 05_calibration.ipynb
│   ├── 06_thresholds.ipynb
│   ├── 07_final_test.ipynb
│   └── 08_errors_shap.ipynb
│
├── src/
│   ├── preprocessing.py
│   └── evaluation.py
│
├── figures/
│
├── results/
│
├── website/
│   ├── data/
│   ├── index.html
│   ├── styles.css
│   └── app.js
│
├── requirements.txt
├── README.md
└── .gitignore
```

## Technologies Used

- Python
- Pandas and NumPy
- Matplotlib and Seaborn
- Scikit-learn
- XGBoost
- SHAP
- Jupyter Notebook
- HTML, CSS and JavaScript
- Git and GitHub

## Limitations

- The dataset contains limited customer information.
- Historical data may not represent current financial behaviour.
- Predictions do not establish causal relationships.
- Classification thresholds require real-world cost considerations.
- Group fairness has not been fully audited.

## Future Improvements

- Build a more complete interactive prediction interface.
- Conduct a detailed fairness evaluation.
- Explore additional machine learning models.
- Improve the website's deployment and accessibility.

## Author

**Surya Siddardha Reddy Geeda**

GitHub: https://github.com/siddu834

---

*RiskLens — Exploring credit risk through machine learning and explainable AI.*

