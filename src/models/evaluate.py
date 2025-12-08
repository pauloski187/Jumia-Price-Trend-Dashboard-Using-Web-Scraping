import pandas as pd
from sklearn.metrics import mean_squared_error, r2_score


def regression_metrics(y_true: pd.Series, y_pred: pd.Series) -> dict:
    return {
        "mse": float(mean_squared_error(y_true, y_pred)),
        "r2": float(r2_score(y_true, y_pred)),
    }
