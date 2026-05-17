from src.config import RAW_PATH, OUT_PATH, FIGURES_PATH
from src.io import load_csv
from src.cleaning import clean
from src.features import build_features
from src.utils import assert_columns, assert_not_empty
from src.viz import plot_graph


def main():
    print("Starting pipeline...")

    print(f"Loading data from: {RAW_PATH}")
    df = load_csv(RAW_PATH)

    assert_not_empty(df)

    required_columns = [
        "Ticket ID",
        "Customer Name",
        "Customer Email",
        "Customer Age",
        "Customer Gender",
        "Product Purchased",
        "Date of Purchase",
        "Ticket Type",
        "Ticket Subject",
        "Ticket Description",
        "Ticket Status",
        "Resolution",
        "Ticket Priority",
        "Ticket Channel",
        "First Response Time",
        "Time to Resolution",
        "Customer Satisfaction Rating",
    ]

    assert_columns(df, required_columns)

    print("CSV loaded successfully.")
    print(f"Rows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}")
    print("Column names:")
    print(list(df.columns))

    df = clean(df)
    df = build_features(df)

    FIGURES_PATH.mkdir(parents=True, exist_ok=True)
    plot_graph(df)

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT_PATH, index=False)

    print(f"Saved processed file to: {OUT_PATH}")
    print("Pipeline finished successfully.")


if __name__ == "__main__":
    main()
