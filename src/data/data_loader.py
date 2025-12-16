import os
import pandas as pd


def load_raw(path: str = "data/raw/jumia_product.csv") -> pd.DataFrame:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Raw data not found at {path}")
    return pd.read_csv(path)


def save_processed(df: pd.DataFrame, path: str = "data/processed/jumia_product_processed.csv") -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)


def load_processed(path: str = "data/processed/jumia_product_processed.csv") -> pd.DataFrame:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Processed data not found at {path}")
    return pd.read_csv(path)
