import pandas as pd


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    features = df.copy()
    # Example placeholder transformations
    if 'name' in features.columns:
        features['normalized_name'] = features['name'].astype(str).str.lower().str.strip()
    return features
