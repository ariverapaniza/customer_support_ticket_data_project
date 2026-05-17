from pathlib import Path


def load_csv(path: str | Path):
    """Load a CSV file into a DataFrame."""
    import pandas as pd
    return pd.read_csv(path)
