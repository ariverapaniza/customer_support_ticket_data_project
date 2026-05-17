import pandas as pd

def assert_columns(df: pd.DataFrame, required: list[str]) -> None:
    """Validate that required columns exist in the DataFrame."""
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f'Missing columns: {missing}')

def assert_not_empty(df: pd.DataFrame) -> None:
    """Validate that the DataFrame is not empty."""
    if df.empty:
        raise ValueError("The DataFrame is empty.")