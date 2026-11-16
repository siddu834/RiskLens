# RiskLens - Serious Delinquency Prediction & Evaluation

A machine learning modeling and evaluation project that predicts the probability of a customer experiencing serious financial delinquency within two years.

RiskLens compares logistic regression, random forest and XGBoost using development cross-validation, then evaluates a frozen calibrated model on a separate holdout. Its interactive website runs the frozen calibrated model on hypothetical inputs, compares scenarios, and explains the tradeoff between missed positives and false alarms. This is a reproducible historical-data study, not a validated lending system.

---

## Project Overview

Credit risk assessment is an important problem in financial institutions. Identifying customers who may experience serious delinquency can help support better lending decisions.

RiskLens uses machine learning to estimate credit default risk and provides an interactive website to explore model performance and classification thresholds.

**This project is intended as a decision-support tool, not an automated lending authority.**

## Dataset

The project uses the Kaggle **Give Me Some Credit** dataset.

- Target variable: `SeriousDlqin2yrs`
- Development samples: 120,000
- Held-out test samples: 30,000
- Split: 80/20, stratified on the target, `RANDOM_SEED=42`
- Shuffled five-fold CV, randomized search and stochastic models use seed 42. The inner calibration `cv=5` is deterministic and unshuffled; it has no random seed to set.
- Input features: 10
- Default rate: approximately 6.68%

The dataset is not included in this repository. Obtain `cs-training.csv` and `Data Dictionary.xls` from the [Give Me Some Credit competition](https://www.kaggle.com/competitions/GiveMeSomeCredit/data), subject to its access terms. Put both files in a new `data/` directory. `dev.csv` and `test.csv` are generated locally by notebook 00; the latter is this project's holdout, not Kaggle's unlabeled competition test file.

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

The reported model is the original frozen XGBoost configuration with isotonic probability calibration. The rerun search selected a different development-CV winner; it is reported separately and was not substituted into the final evaluation.

| Metric | Test Result |
|---|---:|
| ROC-AUC | 0.8694 |
| PR-AUC | 0.4045 |
| Brier Score | 0.0487 |
| Precision | 0.4079 |
| Recall | 0.4958 |
| F1 Score | 0.4475 |

The classification metrics use a threshold of **0.23**, selected for development out-of-fold F1 in the original experiment. The rerun optimum is 0.22; 0.23 is retained for the fixed-model test comparison. The alternative **0.09** threshold minimizes an illustrative cost of `50,000 * FN + 5,000 * FP`; it is not the reporting threshold or a validated lending policy.

**Metric definition:** the reported PR-AUC is scikit-learn **average precision**. The numbers above come from the 12 November 2026 rerun of the original fixed final-model configuration. The original recorded results are preserved in `results/original_final_test_metrics.json`. Small differences remain between runs; see [the reproduction report](docs/reproduction_report.md). No test-driven parameter or threshold changes were made.

The locked test set was reserved for final evaluation rather than model tuning.

## What the results support

Development average precision was 0.3828 for balanced logistic regression, 0.3863 for random forest, and 0.4013 for the rerun XGBoost search winner: an absolute gain of 0.0185 over logistic regression. These selection-influenced CV scores are not a significance test. Isotonic calibration improved the original fixed XGBoost model's OOF Brier score from 0.13948 to 0.04906. Its separate final test average precision was 0.4045. A calibrated logistic model is a worthwhile interpretable follow-up, but was not evaluated here. At threshold 0.23 the final model misses 1,011 positive cases and produces 1,443 false alarms, so strong accuracy alone would obscure important errors.

## Explainability

SHAP (SHapley Additive exPlanations) was used to investigate a separately fitted **uncalibrated XGBoost model**. Its plots explain raw margin (log-odds), not the final calibrated ensemble probability. False-positive and false-negative labels identify errors of the final classifier; the separately explained model may classify those examples differently.

The analysis includes:
- Global feature importance.
- False-negative prediction investigation.
- False-positive prediction investigation.

## Interactive Website

[Live GitHub Pages website](https://siddu834.github.io/RiskLens/) | [ES335 rubric coverage](docs/es335_rubric.md) | [Viva preparation](docs/viva_guide.md).

The static website includes a **real input-based prediction lab**: all ten features, fictional presets, missing-value handling, and a saved-scenario comparison. Five exported XGBoost members with their own preprocessing and isotonic maps run entirely in JavaScript; inputs are neither transmitted nor stored. The separate threshold explorer reads **development out-of-fold** metrics and lets visitors change illustrative error costs. ROC, precision-recall and calibration charts explain the evaluation. Final-test results are labeled separately.

Browser probabilities match Python within 0.00002 (0.002 percentage points) over 200 synthetic cases and all 30,000 held-out rows. All held-out classifications at 0.23 agree. Small differences arise from float32 arithmetic and interpolation; displayed probabilities use one decimal percentage point.

To run it locally from the project root:

```bash
python scripts/build_site.py
python -m http.server 8000 --directory site
```

Then open:

```text
http://localhost:8000/
```

## Reproduce the Analysis

Use Python 3.13. From the repository root:

```bash
python -m venv .venv
```

Activate the environment with `.venv\Scripts\Activate.ps1` on Windows PowerShell or `source .venv/bin/activate` on macOS/Linux, then:

```bash
python -m pip install -r requirements.txt
python -m jupyterlab
```

Create `data/` and add the two source files described above. Open notebooks in JupyterLab and execute them in filename order, **00 through 08**, each with its working directory set to `notebooks/`. Restart the kernel and run all cells rather than relying on variables from an earlier session. Notebook 01 uses `xlrd` to read the `.xls` dictionary.

| Notebook | Purpose / outputs |
|---|---|
| 00 | Deterministic stratified split; `data/dev.csv`, `data/test.csv` |
| 01-02 | Development-only EDA and preprocessing checks |
| 03-04 | Baselines, imbalance experiments and 20-trial XGBoost search |
| 05 | Calibration comparisons and out-of-fold calibration figure |
| 06 | Development out-of-fold predictions and website JSON exports |
| 07 | Fixed final-test evaluation, computed metric JSON, error records |
| 08 | Error inspection and separately fitted base-model SHAP figures |

Training time depends on hardware. The search performs 100 candidate-fold fits plus refitting; calibrated out-of-fold experiments add many fits. The previous all-notebook run took about 19 minutes of notebook execution on the validation machine; this is an observation, not a hardware-independent runtime guarantee. Model and CV parallelism defaults to two workers; set `RISKLENS_N_JOBS` to a positive integer before starting Jupyter to change it. Avoid running several training notebooks concurrently. On memory-constrained machines, also set `OPENBLAS_NUM_THREADS=1` and `OMP_NUM_THREADS=2` before starting Python.

The notebooks export the baseline and model comparison CSVs. Markdown interpretations still need review when experiments change. Do not choose new models or thresholds based on the held-out test results.

For unattended execution with the active Python environment:

```bash
python scripts/reproduce.py
python scripts/audit_data.py
```

Executed notebooks and timings are saved under `.runs/` (excluded from Git). To check only the fixed final evaluation after preparing the split, use `python scripts/reproduce.py --notebooks 00 02 07`. Full execution overwrites generated metrics and figures; retain previous results before comparing runs.

**Verification scope (16 November 2026):** A clean public GitHub clone and a newly installed Python 3.13 environment successfully rebuilt the frozen final ensemble using `scripts/export_browser_model.py`. ROC-AUC, average precision and Brier score matched the saved reference exactly. The dependency check and seven regression tests passed. All nine notebooks previously completed in the validated environment; the fresh-environment runner subsequently completed notebooks 00, 02 and 07 after local networking became available. The original startup stall is resolved. A second full hyperparameter-search run in the fresh environment is not claimed. The standalone exporter also independently verifies the final model. See [the reproduction report](docs/reproduction_report.md).

To reproduce the prediction lab and aggregate error audit directly, without launching a notebook kernel:

```bash
python scripts/export_browser_model.py
node tests/test_browser.cjs
node tests/test_browser.cjs .runs/browser_test_private.json
python scripts/build_site.py
```

The exporter creates the seed-42 split from the source CSV, fits only on development data, checks frozen test metrics, and writes `website/data/model.json`, its 15 small tree parts under `website/data/model/`, `evidence.json`, and synthetic test fixtures. Actual row-level parity inputs stay under ignored `.runs/`; never publish them. Node.js 22 or newer is needed only for the JavaScript parity test, not to serve the static website.

## Automated Checks

The lightweight checks do not require the private/local dataset or a model-training run:

```bash
python -m pip install -r requirements-checks.txt
python -m pytest -q
node tests/test_browser.cjs
python scripts/build_site.py
```

Checks cover sentinel handling, missing values, training-only capping, prediction shape, metric arithmetic, strict JSON, and packaged website assets. GitHub Actions runs these checks on pushes and pull requests. They are smoke/regression checks, not proof of predictive quality.

The Pages workflow publishes the generated `site/` directory, including figures. Enable GitHub Pages with **GitHub Actions** as its source in repository settings. Verify a successful deployment before adding a live demo URL to a resume.

## Project Structure

```text
RiskLens/
|
+-- data/
|
+-- notebooks/
|   +-- 00_lock_split.ipynb
|   +-- 01_eda.ipynb
|   +-- 02_preprocessing_check.ipynb
|   +-- 03_baselines.ipynb
|   +-- 04_models.ipynb
|   +-- 05_calibration.ipynb
|   +-- 06_thresholds.ipynb
|   +-- 07_final_test.ipynb
|   `-- 08_errors_shap.ipynb
|
+-- src/
|   +-- preprocessing.py
|   `-- evaluation.py
|
+-- figures/
|
+-- results/
|
+-- website/
|   +-- data/
|   +-- index.html
|   +-- styles.css
|   `-- app.js
|
+-- requirements.txt
+-- README.md
`-- .gitignore
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

## Evaluation Boundaries

- Hyperparameter selection and development score reporting reuse folds; development scores are selection-influenced. The held-out test is the primary generalization estimate.
- The random split does not establish performance on future periods or new lending populations. The source has 609 repeated full rows; 173 holdout rows have feature profiles also present in development data. The nonmatching test subset gives ROC-AUC 0.8690 and average precision 0.4040. Identical profiles do not prove shared borrower identity. See `results/data_audit.json`.
- Preliminary training-set calibration plots are diagnostic only; model comparisons should use out-of-fold results.
- The website error audit now summarizes all 30,000 test records. The older SHAP examples and first-1,000-development-row SHAP summary remain illustrative and explain a separate uncalibrated model.
- A 300-resample percentile bootstrap gives a conditional test AP interval of 0.3809-0.4273. It does not include training, model-selection or population-shift uncertainty.
- No real financial savings, production deployment, or complete fairness audit has been demonstrated.

## Future Improvements

- Evaluate calibrated logistic regression using the same development protocol.
- Conduct a detailed fairness evaluation.
- Explore additional machine learning models.
- Validate on later time periods and borrower-disjoint data when identifiers become available.

## Maintenance and Ownership

AI assistance, including OpenAI Codex for maintenance, was used for concepts, debugging, experiment execution, tests, website implementation and documentation. The browser model export, synthetic parity fixtures, full error summaries, bootstrap interval and redesigned website also used Codex assistance. The original project's complete AI-tool history has not been independently verified. The author should verify the experiments and be able to explain the implementation. See [the improvement log](docs/improvement_log.md) for changes, validation scope, and remaining work.

## Author

**Surya Siddardha Reddy Geeda**

GitHub: https://github.com/siddu834

---

*RiskLens - Exploring credit risk through machine learning and explainable AI.*


## Sources and course submission

Data: [Give Me Some Credit](https://www.kaggle.com/competitions/GiveMeSomeCredit/data). Library references: [scikit-learn](https://scikit-learn.org/stable/), [XGBoost](https://xgboost.readthedocs.io/), [imbalanced-learn](https://imbalanced-learn.org/stable/), and [SHAP](https://shap.readthedocs.io/). The browser evaluator is a project implementation of exported tree traversal, original preprocessing and isotonic interpolation.

For ES335, submit the live GitHub Pages URL and this source-repository URL through the course portal. The supplied course PDFs specify 17 November 2026, 11:59 PM IST. Submission itself has not been performed by this tooling. Individual contribution details and exact alignment with the original proposal await the students' confirmation; see the viva guide.
