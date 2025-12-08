from typing import Optional

import pandas as pd
import matplotlib.pyplot as plt


def plot_price_distribution(df: pd.DataFrame, price_col: str = "price", title: Optional[str] = None):
    if price_col not in df.columns:
        raise KeyError(f"Column '{price_col}' not in DataFrame")
    ax = df[price_col].dropna().plot(kind="hist", bins=30, alpha=0.7)
    ax.set_xlabel(price_col)
    ax.set_ylabel("count")
    ax.set_title(title or f"Distribution of {price_col}")
    plt.tight_layout()
    return ax
