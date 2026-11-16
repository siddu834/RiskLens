"""Rebuild the frozen final model and export a browser-readable ensemble.

Uses development data only for fitting. Test data checks reproducibility and
reports errors/uncertainty; it never changes parameters or threshold.
"""
import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.calibration import CalibratedClassifierCV, calibration_curve
from sklearn.metrics import average_precision_score, roc_auc_score, brier_score_loss, confusion_matrix
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.config import RANDOM_SEED, TARGET_COL, N_JOBS
from src.preprocessing import make_pipeline


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, separators=(',', ':'), allow_nan=False) + '\n', encoding='utf-8')


def run():
    raw = ROOT / 'data/cs-training.csv'
    df = pd.read_csv(raw, index_col=0)
    dev, test = train_test_split(df, test_size=.2, stratify=df[TARGET_COL], random_state=RANDOM_SEED)
    # Preserve the CSV round trip used by the existing notebooks.
    for name, frame in [('dev', dev), ('test', test)]:
        frame.to_csv(ROOT / f'data/{name}.csv', index=False)
    dev, test = (pd.read_csv(ROOT / f'data/{name}.csv') for name in ['dev', 'test'])
    X, y = dev.drop(columns=TARGET_COL), dev[TARGET_COL]
    Xt, yt = test.drop(columns=TARGET_COL), test[TARGET_COL]
    model = CalibratedClassifierCV(make_pipeline(XGBClassifier(
        n_estimators=300, max_depth=4, learning_rate=.05, min_child_weight=5,
        subsample=.8, colsample_bytree=1., reg_lambda=1., objective='binary:logistic',
        eval_metric='logloss', scale_pos_weight=float((y == 0).sum() / (y == 1).sum()),
        random_state=RANDOM_SEED, n_jobs=N_JOBS)), method='isotonic', cv=5)
    print('Fitting the frozen five-member calibrated ensemble...', flush=True)
    model.fit(X, y)
    prob = model.predict_proba(Xt)[:, 1]
    saved = json.loads((ROOT / 'results/final_test_metrics.json').read_text())
    metrics = {'roc_auc': roc_auc_score(yt, prob), 'pr_auc': average_precision_score(yt, prob),
               'brier_score': brier_score_loss(yt, prob)}
    for key, value in metrics.items():
        if abs(value - saved[key]) > 1e-7:
            raise ValueError(f'Frozen-model reproduction mismatch: {key}: {value} vs {saved[key]}')
    counts = confusion_matrix(yt, prob >= .23).ravel()
    if any(int(count) != saved[key] for key, count in zip(['tn', 'fp', 'fn', 'tp'], counts)):
        raise ValueError('Frozen-model confusion counts do not match the saved reference')
    members = []
    for calibrated in model.calibrated_classifiers_:
        pipe = calibrated.estimator
        booster = json.loads(pipe['model'].get_booster().save_raw(raw_format='json'))['learner']
        base = float(booster['learner_model_param']['base_score'].strip('[]'))
        trees = booster['gradient_booster']['model']['trees']
        members.append({
            'caps': pipe['capper'].upper_limits_,
            'medians': pipe['imputer'].statistics_.tolist(),
            'base_margin': float(np.log(base / (1 - base))),
            'trees': [{k: t[k] for k in ['left_children', 'right_children', 'split_indices',
                       'split_conditions', 'default_left']} for t in trees],
            'isotonic_x': calibrated.calibrators[0].X_thresholds_.tolist(),
            'isotonic_y': calibrated.calibrators[0].y_thresholds_.tolist(),
        })
    # Small model parts keep individual artifacts easy to review and transfer.
    for i, member in enumerate(members):
        trees = member.pop('trees')
        member['tree_files'] = []
        for part in range(3):
            relative = f'model/member-{i}-part-{part}.json'
            save(ROOT / 'website/data' / relative, trees[part*100:(part+1)*100])
            member['tree_files'].append(relative)
    export = {'schema_version': 2, 'name': 'Frozen isotonic-calibrated XGBoost',
              'features': list(X.columns), 'members': members,
              'training_rows': len(X), 'seed': RANDOM_SEED, 'threshold': .23,
              'data_sha256': hashlib.sha256(raw.read_bytes()).hexdigest()}
    save(ROOT / 'website/data/model.json', export)
    # Synthetic fixtures can be public; no actual borrower records are exported.
    rng = np.random.default_rng(RANDOM_SEED)
    synthetic = pd.DataFrame({
        X.columns[0]: rng.uniform(0, 3, 200), X.columns[1]: rng.integers(18, 101, 200),
        X.columns[2]: rng.integers(0, 8, 200), X.columns[3]: rng.uniform(0, 4, 200),
        X.columns[4]: rng.uniform(0, 20000, 200), X.columns[5]: rng.integers(0, 30, 200),
        X.columns[6]: rng.integers(0, 5, 200), X.columns[7]: rng.integers(0, 7, 200),
        X.columns[8]: rng.integers(0, 5, 200), X.columns[9]: rng.integers(0, 7, 200),
    }).astype(float)
    synthetic.loc[0, 'age'] = 0
    synthetic.loc[1, X.columns[2]] = 96
    synthetic.loc[2, X.columns[6]] = 98
    synthetic.loc[3, ['MonthlyIncome', 'NumberOfDependents']] = np.nan
    synthetic.loc[4, ['DebtRatio', X.columns[0]]] = 100000
    synthetic.loc[5, :] = np.nan
    records = json.loads(synthetic.to_json(orient='records'))
    save(ROOT / 'tests/browser_fixtures.json', {'inputs': records,
         'expected': model.predict_proba(synthetic)[:, 1].tolist()})
    save(ROOT / '.runs/browser_test_private.json', {'inputs': json.loads(Xt.to_json(orient='records', double_precision=15)),
         'expected': prob.tolist()})
    # Aggregate all errors instead of relying on the first 20 cases.
    pred = prob >= .23
    errors = {}
    for name, mask in [('Missed positives', (yt == 1) & ~pred),
                       ('False alarms', (yt == 0) & pred),
                       ('Caught positives', (yt == 1) & pred),
                       ('Correct negatives', (yt == 0) & ~pred)]:
        group = Xt.loc[mask]
        errors[name] = {'n': int(mask.sum()), 'median_probability': float(np.median(prob[mask])),
                       'median_utilization': float(group.iloc[:, 0].median()),
                       'prior_90day_late_rate': float((group['NumberOfTimes90DaysLate'].between(1,95)).mean()),
                       'income_missing_rate': float(group['MonthlyIncome'].isna().mean())}
    # Conditional bootstrap uncertainty for the already-frozen test predictions.
    estimates = []
    truth = yt.to_numpy()
    for _ in range(300):
        idx = rng.integers(0, len(yt), len(yt))
        estimates.append(average_precision_score(truth[idx], prob[idx]))
    interval = np.quantile(estimates, [.025, .975]).tolist()
    frac, mean = calibration_curve(yt, prob, n_bins=10, strategy='quantile')
    feature_summary = []
    for col in X:
        feature_summary.append({'feature': col, 'missing': int(X[col].isna().sum()),
                                'median': float(X[col].median()),
                                'p01': float(X[col].quantile(.01)), 'p99': float(X[col].quantile(.99))})
    evidence = {'final_metrics': saved, 'errors': errors, 'features': feature_summary,
                'test_ap_interval': interval, 'bootstrap_repetitions': 300,
                'bootstrap_note': 'Percentile bootstrap of frozen test predictions; conditional on this split and fit. Not uncertainty from model selection or future population shift.',
                'calibration': {'mean_predicted': mean.tolist(), 'fraction_positive': frac.tolist()},
                'verification': {'max_metric_difference': max(abs(metrics[k]-saved[k]) for k in metrics),
                                 'fit_rows': len(X), 'test_rows': len(Xt)}}
    save(ROOT / 'website/data/evidence.json', evidence)
    save(ROOT / 'results/browser_model_verification.json', evidence['verification'])
    print(json.dumps({'metrics': metrics, 'ap_interval': interval, 'errors': errors}, indent=2), flush=True)


if __name__ == '__main__':
    run()
