# ==========================================
# 1. IMPORT LIBRARIES
# ==========================================

import pandas as pd
import numpy as np

from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, FunctionTransformer


# ==========================================
# 2. PERCENTILE CAPPER
# ==========================================

class PercentileCapper(BaseEstimator, TransformerMixin):

    def __init__(self, columns=None, percentile=0.99):
        self.columns = columns
        self.percentile = percentile

    def fit(self, X, y=None):

        if self.columns is None:
            raise ValueError("Please provide columns to cap.")

        self.upper_limits_ = {}

        for col in self.columns:
            self.upper_limits_[col] = X[col].quantile(
                self.percentile
            )

        return self

    def transform(self, X):

        X = X.copy()

        for col, limit in self.upper_limits_.items():
            X[col] = X[col].clip(upper=limit)

        return X


# ==========================================
# 3. DATA CLEANING FUNCTION
# ==========================================

def clean_data(df: pd.DataFrame) -> pd.DataFrame:

    df = df.copy()

    # Handle invalid age values
    if "age" in df.columns:
        df.loc[df["age"] == 0, "age"] = np.nan

    # Preserve useful missing-value information
    for col in ["age", "MonthlyIncome", "NumberOfDependents"]:
        if col in df.columns:
            df[f"missingindicator_{col}"] = df[col].isna().astype(int)

    # Late-payment columns
    late_cols = [
        "NumberOfTime30-59DaysPastDueNotWorse",
        "NumberOfTime60-89DaysPastDueNotWorse",
        "NumberOfTimes90DaysLate"
    ]

    # Create ONE combined sentinel indicator
    available_late_cols = [
        col for col in late_cols if col in df.columns
    ]

    df["late_payment_sentinel"] = (
        df[available_late_cols].isin([96, 98]).any(axis=1).astype(int)
    )

    # Replace sentinel values with NaN
    for col in available_late_cols:
        df.loc[df[col].isin([96, 98]), col] = np.nan

    return df

# ==========================================
# 4. SKLEARN PIPELINE FUNCTION
# ==========================================

def make_pipeline(model, scale=False):

    cap_columns = [
        "RevolvingUtilizationOfUnsecuredLines",
        "DebtRatio"
    ]

    steps = [

        # Step 1: Clean data
        (
            "cleaner",
            FunctionTransformer(
                clean_data,
                validate=False
            )
        ),

        # Step 2: Cap extreme values
        (
            "capper",
            PercentileCapper(
                columns=cap_columns,
                percentile=0.99
            )
        ),

        # Step 3: Handle missing values
        (
            "imputer",
            SimpleImputer(
                strategy="median",
                add_indicator=False
            )
        )
    ]

    # Step 4: Optional feature scaling
    if scale:
        steps.append(
            ("scaler", StandardScaler())
        )

    # Step 5: Add machine learning model
    steps.append(
        ("model", model)
    )

    return Pipeline(steps)
