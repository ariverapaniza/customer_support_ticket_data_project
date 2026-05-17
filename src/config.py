from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Change these paths to point to your data files
RAW_PATH = ROOT / "data" / "raw" / "raw_dataset.csv"
OUT_PATH = ROOT / "data" / "processed" / "clean_dataset.csv"