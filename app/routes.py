from fastapi import APIRouter, HTTPException
from .schemas import Product, PredictionRequest, PredictionResponse
from typing import List, Dict, Any
import os
import pandas as pd

router = APIRouter()


@router.get("/health")
def health():
    return {"status": "ok"}


@router.post("/products", response_model=Product)
def create_product(product: Product):
    # Placeholder implementation
    return product


@router.post("/predict", response_model=PredictionResponse)
def predict_price(req: PredictionRequest):
    # Placeholder prediction
    return PredictionResponse(prediction=0.0)


@router.get("/api/price_trend")
def price_trend() -> Dict[str, Any]:
    """
    Returns chart-ready data for Plotly.
    Aggregates average current price per day per category (top categories only) from the processed CSV.
    """
    csv_path = "data/processed/jumia_product_processed.csv"
    if not os.path.exists(csv_path):
        raise HTTPException(status_code=404, detail=f"Processed data not found at {csv_path}")

    df = pd.read_csv(csv_path)

    # Ensure expected columns exist; fall back to reasonable alternatives if needed
    # Expected: date_scraped, category, current_price_ngn
    date_col = None
    for c in ["date_scraped", "Date Scraped", "date", "scrape_date"]:
        if c in df.columns:
            date_col = c
            break
    if date_col is None:
        raise HTTPException(status_code=422, detail="date_scraped column not found in processed dataset")

    cat_col = None
    for c in ["category", "Category"]:
        if c in df.columns:
            cat_col = c
            break
    if cat_col is None:
        # create a dummy category if missing
        df["category"] = "All"
        cat_col = "category"

    price_col = None
    for c in ["current_price_ngn", "Current Price", "current_price", "price"]:
        if c in df.columns:
            price_col = c
            break
    if price_col is None:
        raise HTTPException(status_code=422, detail="current_price column not found in processed dataset")

    # Coerce date and numeric types
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce").dt.date
    df = df.dropna(subset=[date_col])
    df[price_col] = pd.to_numeric(df[price_col], errors="coerce")

    # Choose top N categories by count to keep chart readable
    top_cats = (
        df[cat_col]
        .value_counts()
        .head(5)
        .index
        .tolist()
    )
    df_top = df[df[cat_col].isin(top_cats)].copy()

    grp = (
        df_top.groupby([date_col, cat_col])[price_col]
        .mean()
        .reset_index()
        .sort_values(by=[cat_col, date_col])
    )

    # Build Plotly traces
    traces: List[Dict[str, Any]] = []
    for cat in top_cats:
        sub = grp[grp[cat_col] == cat]
        traces.append({
            "type": "scatter",
            "mode": "lines+markers",
            "name": str(cat),
            "x": sub[date_col].astype(str).tolist(),
            "y": sub[price_col].round(2).tolist(),
        })

    layout = {
        "title": "Average Current Price by Category Over Time",
        "xaxis": {"title": "Date"},
        "yaxis": {"title": "Average Price (NGN)", "rangemode": "tozero"},
        "legend": {"orientation": "h"},
        "margin": {"t": 50, "r": 20, "b": 50, "l": 60},
        "hovermode": "x unified",
    }

    return {"traces": traces, "layout": layout}
