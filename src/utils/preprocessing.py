import pandas as pd


def clean_prices(df: pd.DataFrame, price_col: str = "price") -> pd.DataFrame:
    out = df.copy()
    if price_col in out.columns:
        out[price_col] = pd.to_numeric(out[price_col], errors="coerce")
    return out
