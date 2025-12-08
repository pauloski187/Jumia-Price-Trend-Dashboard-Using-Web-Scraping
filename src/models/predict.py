import pandas as pd
from sklearn.base import RegressorMixin


def predict(model: RegressorMixin, X: pd.DataFrame) -> pd.Series:
    return pd.Series(model.predict(X), index=X.index, name="prediction")
