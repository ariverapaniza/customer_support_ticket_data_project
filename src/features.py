import pandas as pd


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Temporary feature engineering function for Step 1.

    In the next step, this function will create:
    - product_age_days
    - resolution_hours
    - has_resolution
    - satisfaction_group
    - is_high_priority
    """
    return df.copy()