"""Audit the source data and fixed holdout without modifying model selection."""
import hashlib
import json
from pathlib import Path
import sys

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, average_precision_score, brier_score_loss

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.config import RANDOM_SEED, TEST_SIZE, TARGET_COL


def audit():
    source = ROOT / 'data/cs-training.csv'
    data = pd.read_csv(source, index_col=0)
    dev, test = train_test_split(data, test_size=TEST_SIZE,
                                 stratify=data[TARGET_COL], random_state=RANDOM_SEED)
    # Group on features only: matching records with different labels also overlap.
    features = data.columns.drop(TARGET_COL)
    dev_hash = pd.util.hash_pandas_object(dev[features], index=False)
    test_hash = pd.util.hash_pandas_object(test[features], index=False)
    overlap = test_hash.isin(set(dev_hash)).to_numpy()
    exact_dev = pd.util.hash_pandas_object(dev, index=False)
    exact_test = pd.util.hash_pandas_object(test, index=False)
    report = {
        'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
        'rows': len(data), 'features': len(features),
        'positive_rows': int(data[TARGET_COL].sum()),
        'duplicate_rows_including_label': int(data.duplicated().sum()),
        'duplicate_feature_rows': int(data.duplicated(subset=features).sum()),
        'development_rows': len(dev), 'test_rows': len(test),
        'test_rows_matching_development_including_label': int(exact_test.isin(set(exact_dev)).sum()),
        'test_rows_matching_development_features': int(overlap.sum()),
        'interpretation': 'Identical feature profiles are not proof of borrower identity. The original random split is retained for reproduction; the additional subset analysis is not a replacement untouched test set.'
    }
    predictions = ROOT / 'results/test_error_analysis.csv'
    if predictions.exists():
        saved_test = pd.read_csv(ROOT / 'data/test.csv')
        pd.testing.assert_frame_equal(saved_test, test.reset_index(drop=True))
        predicted = pd.read_csv(predictions)
        assert len(predicted) == len(test)
        assert (predicted.actual.to_numpy() == test[TARGET_COL].to_numpy()).all()
        late_columns = [column for column in features if 'DaysPastDue' in column or column == 'NumberOfTimes90DaysLate']
        history = saved_test[late_columns].replace([96, 98], float('nan'))
        positive_history = history.gt(0).any(axis=1)
        zero_history = history.eq(0).all(axis=1)
        groups = {
            'All three counts zero': zero_history,
            'At least one valid late count': positive_history,
            'History indeterminate': ~(positive_history | zero_history),
        }
        report['history_at_threshold_023'] = []
        for label, mask in groups.items():
            positives = mask & predicted.actual.eq(1)
            missed = int((positives & predicted.probability.lt(0.23)).sum())
            report['history_at_threshold_023'].append({
                'group': label, 'records': int(mask.sum()),
                'positives': int(positives.sum()), 'missed': missed,
            })
        subset = predicted.loc[~overlap]
        report['nonmatching_test_subset'] = {
            'rows': len(subset),
            'roc_auc': float(roc_auc_score(subset.actual, subset.probability)),
            'average_precision': float(average_precision_score(subset.actual, subset.probability)),
            'brier_score': float(brier_score_loss(subset.actual, subset.probability)),
        }
    destination = ROOT / 'results/data_audit.json'
    destination.write_text(json.dumps(report, indent=2, allow_nan=False)+'\n', encoding='utf-8')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    audit()
