"""Compare against the saved development predictions from notebook 06."""
import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.calibration import CalibratedClassifierCV
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, brier_score_loss
from sklearn.model_selection import StratifiedKFold

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.config import RANDOM_SEED, TARGET_COL
from src.preprocessing import make_pipeline


def compare():
    dev = pd.read_csv(ROOT / "data/dev.csv")
    labels = dev.pop(TARGET_COL)
    saved = pd.read_csv(ROOT / "results/dev_oof_predictions.csv")
    np.testing.assert_array_equal(labels, saved.actual_default)
    logistic = np.full(len(dev), np.nan)
    boosted = saved.predicted_probability.to_numpy()
    folds = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_SEED)
    rows = []

    def record(fold, indices):
        for name, scores in [("Logistic", logistic), ("XGBoost", boosted)]:
            y, p = labels.iloc[indices], scores[indices]
            rows.append(dict(fold=fold, model=name, records=len(y),
                             average_precision=average_precision_score(y, p),
                             brier=brier_score_loss(y, p)))

    for number, (train, valid) in enumerate(folds.split(dev, labels), 1):
        base = LogisticRegression(class_weight="balanced", max_iter=2000, random_state=RANDOM_SEED)
        model = CalibratedClassifierCV(make_pipeline(base, scale=True), method="isotonic", cv=5)
        model.fit(dev.iloc[train], labels.iloc[train])
        logistic[valid] = model.predict_proba(dev.iloc[valid])[:, 1]
        record(number, valid)
    record("pooled", np.arange(len(dev)))
    paired = pd.DataFrame({"actual": labels, "logistic": logistic, "xgboost": boosted})
    paired.to_csv(ROOT / "results/calibrated_paired_predictions.csv", index=False)
    rng = np.random.default_rng(RANDOM_SEED)
    gains = []
    y = labels.to_numpy()
    for _ in range(300):
        sample = rng.integers(0, len(y), len(y))
        truth, lr, xgb = y[sample], logistic[sample], boosted[sample]
        gains.append([
            average_precision_score(truth, xgb) - average_precision_score(truth, lr),
            brier_score_loss(truth, lr) - brier_score_loss(truth, xgb),
        ])
    intervals = np.quantile(gains, [0.025, 0.975], axis=0)
    uncertainty = {
        "resamples": 300, "seed": RANDOM_SEED,
        "ap_gain_95_interval": intervals[:, 0].tolist(),
        "brier_reduction_95_interval": intervals[:, 1].tolist(),
        "scope": "Paired row bootstrap of fixed development OOF predictions. Conditional on these predictions. Excludes retraining, selection uncertainty, and population shift.",
        "development_sha256": hashlib.sha256((ROOT / "data/dev.csv").read_bytes()).hexdigest(),
        "xgboost_predictions_sha256": hashlib.sha256((ROOT / "results/dev_oof_predictions.csv").read_bytes()).hexdigest(),
    }
    (ROOT / "results/calibrated_uncertainty.json").write_text(
        json.dumps(uncertainty, indent=2) + "\n", encoding="utf-8")
    report = pd.DataFrame(rows)
    report.to_csv(ROOT / "results/calibrated_comparison.csv", index=False)
    # Stable sorting breaks score ties by the saved development row order.
    capacity = {"records": len(labels), "positives": int(labels.sum()), "budgets": {}}
    for name, scores in [("Logistic regression", logistic), ("XGBoost", boosted)]:
        ranked = np.argsort(-scores, kind="stable")
        cumulative = labels.to_numpy()[ranked].cumsum()
        for budget in [10, 25, 50, 100, 200]:
            reviewed = len(labels) * budget // 1000
            caught = int(cumulative[reviewed - 1])
            capacity["budgets"].setdefault(budget, {})[name] = {
                "reviewed": reviewed, "caught": caught,
                "missed": capacity["positives"] - caught, "false_alarms": reviewed - caught,
            }
    (ROOT / "website/data/review_capacity.json").write_text(
        json.dumps(capacity, indent=2) + "\n", encoding="utf-8")
    print(report.to_string(index=False))


if __name__ == "__main__":
    compare()
