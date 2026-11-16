"""Regression tests use synthetic records; no Kaggle download is required."""
import numpy as np
import pandas as pd
import json
from pathlib import Path
from sklearn.linear_model import LogisticRegression

from src.preprocessing import clean_data, make_pipeline, PercentileCapper


def sample_rows():
    return pd.DataFrame({
        "age": [0, 25, 40, 60, 35, 50],
        "MonthlyIncome": [np.nan, 2000, 3000, 4000, 5000, 6000],
        "NumberOfDependents": [np.nan, 1, 2, 0, 1, 3],
        "RevolvingUtilizationOfUnsecuredLines": [0.1, 0.2, 0.4, 0.8, 1.2, 10],
        "DebtRatio": [0.1, 0.2, 0.3, 0.4, 0.5, 100],
        "NumberOfTime30-59DaysPastDueNotWorse": [96, 0, 1, 0, 2, 0],
        "NumberOfTime60-89DaysPastDueNotWorse": [0, 98, 0, 0, 1, 0],
        "NumberOfTimes90DaysLate": [0, 0, 98, 0, 1, 0],
        "NumberOfOpenCreditLinesAndLoans": [1, 2, 3, 4, 5, 6],
        "NumberRealEstateLoansOrLines": [0, 0, 1, 1, 2, 1],
    })


def test_sentinels_and_missing_flags_preserve_input():
    raw = sample_rows()
    original = raw.copy(deep=True)
    cleaned = clean_data(raw)
    pd.testing.assert_frame_equal(raw, original)
    assert cleaned['late_payment_sentinel'].tolist() == [1, 1, 1, 0, 0, 0]
    assert np.isnan(cleaned.loc[0, 'NumberOfTime30-59DaysPastDueNotWorse'])
    assert np.isnan(cleaned.loc[1, 'NumberOfTime60-89DaysPastDueNotWorse'])
    assert np.isnan(cleaned.loc[2, 'NumberOfTimes90DaysLate'])
    assert cleaned.loc[0, 'missingindicator_age'] == 1
    assert cleaned.loc[0, 'missingindicator_MonthlyIncome'] == 1
    assert cleaned.loc[0, 'missingindicator_NumberOfDependents'] == 1


def test_validation_outliers_do_not_change_training_caps():
    capper = PercentileCapper(columns=['DebtRatio']).fit(sample_rows())
    learned_limit = capper.upper_limits_['DebtRatio']
    validation = sample_rows()
    validation['DebtRatio'] = 1e9
    transformed = capper.transform(validation)
    assert transformed['DebtRatio'].eq(learned_limit).all()
    assert capper.upper_limits_['DebtRatio'] == learned_limit
    assert validation['DebtRatio'].eq(1e9).all()


def test_pipeline_handles_missing_data_and_unseen_extremes():
    pipeline = make_pipeline(LogisticRegression(max_iter=1000), scale=True)
    pipeline.fit(sample_rows(), [0, 0, 1, 0, 1, 1])
    new_rows = sample_rows().iloc[:2].copy()
    new_rows['DebtRatio'] = 1e8
    probabilities = pipeline.predict_proba(new_rows)
    assert probabilities.shape == (2, 2)
    assert np.isfinite(probabilities).all()
    np.testing.assert_allclose(probabilities.sum(axis=1), 1)


def test_notebook_sentinel_check_runs_against_current_pipeline():
    notebook_path = Path(__file__).resolve().parents[1] / 'notebooks/02_preprocessing_check.ipynb'
    notebook = json.loads(notebook_path.read_text(encoding='utf-8'))
    raw = sample_rows()
    namespace = {'pd': pd, 'dev': raw, 'dev_clean': clean_data(raw)}
    exec(''.join(notebook['cells'][6]['source']), namespace)
