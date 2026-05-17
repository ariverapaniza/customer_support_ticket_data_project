from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Change these paths to point to your data files
RAW_PATH = ROOT / "data" / "raw" / "customer_support_tickets.csv"
OUT_PATH = ROOT / "data" / "processed" / "clean_customer_support_tickets.csv"
FIGURES_PATH = ROOT / "reports" / "figures"