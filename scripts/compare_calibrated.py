"""Compare against the saved development predictions from notebook 06."""
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
    report = pd.DataFrame(rows)
    report.to_csv(ROOT / "results/calibrated_comparison.csv", index=False)
    print(report.to_string(index=False))


if __name__ == "__main__":
    compare()
