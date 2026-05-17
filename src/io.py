from pathlib import Path
import pandas as pd

def load_csv(path: str | Path) -> pd.DataFrame:
    """Cargar el archivo CSV en un DataFrame."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Archivo no encontrado: {path}")
    return pd.read_csv(path)
