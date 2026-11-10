import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.metrics import (
    roc_auc_score,
    average_precision_score,
    brier_score_loss,
    roc_curve,
    precision_recall_curve,
    confusion_matrix
)

from sklearn.calibration import calibration_curve
from sklearn.model_selection import StratifiedKFold, cross_validate


def classification_metrics(y_true, y_prob):

    return {
        "roc_auc": roc_auc_score(y_true, y_prob),
        "pr_auc": average_precision_score(y_true, y_prob),
        "brier": brier_score_loss(y_true, y_prob)
    }


def plot_roc_pr(y_true, y_prob, title_prefix=""):

    fpr, tpr, _ = roc_curve(y_true, y_prob)

    prec, rec, _ = precision_recall_curve(y_true, y_prob)

    fig, ax = plt.subplots(1, 2, figsize=(10, 4))

    ax[0].plot(fpr, tpr)
    ax[0].plot([0, 1], [0, 1], "--")
    ax[0].set_title(f"{title_prefix} ROC")
    ax[0].set_xlabel("False Positive Rate")
    ax[0].set_ylabel("True Positive Rate")

    ax[1].plot(rec, prec)
    ax[1].set_title(f"{title_prefix} PR")
    ax[1].set_xlabel("Recall")
    ax[1].set_ylabel("Precision")

    plt.tight_layout()
    plt.show()

    return fig


from sklearn.model_selection import StratifiedKFold, cross_validate
from src.config import RANDOM_SEED, N_FOLDS

def run_cv(pipeline, X, y):

    cv = StratifiedKFold(
        n_splits=N_FOLDS,
        shuffle=True,
        random_state=RANDOM_SEED
    )

    scoring = {
        "roc_auc": "roc_auc",
        "pr_auc": "average_precision",
        "neg_brier": "neg_brier_score",
    }

    scores = cross_validate(
        pipeline,
        X,
        y,
        cv=cv,
        scoring=scoring,
        n_jobs=-1,
        return_train_score=False
    )

    summary = {
        "roc_auc_mean": scores["test_roc_auc"].mean(),
        "roc_auc_std": scores["test_roc_auc"].std(),
        "pr_auc_mean": scores["test_pr_auc"].mean(),
        "pr_auc_std": scores["test_pr_auc"].std(),
        "brier_mean": -scores["test_neg_brier"].mean(),
        "brier_std": scores["test_neg_brier"].std(),
    }

    return scores, summary
