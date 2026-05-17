import pandas as pd


def clean(df: pd.DataFrame) -> pd.DataFrame:
    """
    Temporary cleaning function for Step 1.

    In the next step, this function will:
    - clean column names
    - remove personal data
    - convert date columns
    - handle duplicates
    - normalize categories
    """
    return df.copy()