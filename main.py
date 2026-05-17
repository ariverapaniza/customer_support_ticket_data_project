from src.config import RAW_PATH, OUT_PATH, FIGURES_PATH
from src.io import load_csv
from src.cleaning import clean
from src.features import build_features
from src.utils import validate_raw_dataset, validate_clean_dataset
from src.viz import plot_graph


def main():
    print("Starting pipeline...")

    print(f"Loading data from: {RAW_PATH}")
    df = load_csv(RAW_PATH)

    validate_raw_dataset(df)

    print("CSV loaded successfully.")
    print(f"Rows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}")
    print("Column names:")
    print(list(df.columns))

    df = clean(df)
    df = build_features(df)
    validate_clean_dataset(df)

    FIGURES_PATH.mkdir(parents=True, exist_ok=True)
    plot_graph(df)

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT_PATH, index=False)

    print(f"Saved processed file to: {OUT_PATH}")
    print("Pipeline finished successfully.")


if __name__ == "__main__":
    main()
