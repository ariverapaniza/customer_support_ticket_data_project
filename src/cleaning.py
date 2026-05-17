import re
import pandas as pd

PERSONAL_COLUMNS = [
    "customer_name",
    "customer_email",
    "ticket_description",
    "resolution",
]

DATE_COLUMNS = [
    "date_of_purchase",
    "first_response_time",
    "time_to_resolution",
]

NUMERIC_COLUMNS = [
    "ticket_id",
    "customer_age",
    "customer_satisfaction_rating",
]

CATEGORY_COLUMNS = [
    "customer_gender",
    "product_purchased",
    "ticket_type",
    "ticket_subject",
    "ticket_status",
    "ticket_priority",
    "ticket_channel",
]

def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert column names to snake_case.

    Example:
    'Ticket ID' -> 'ticket_id'
    'Date of Purchase' -> 'date_of_purchase'
    """
    df = df.copy()

    clean_columns = []
    for column in df.columns:
        column = column.strip().lower()
        column = re.sub(r"[^a-z0-9]+", "_", column)
        column = re.sub(r"_+", "_", column)
        column = column.strip("_")
        clean_columns.append(column)

    df.columns = clean_columns
    return df


def remove_personal_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove personal or high-noise text columns.

    This improves privacy and keeps the EDA focused on operational support metrics.
    """
    df = df.copy()

    columns_to_drop = [column for column in PERSONAL_COLUMNS if column in df.columns]
    df = df.drop(columns=columns_to_drop)

    return df


def convert_dates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert date columns to datetime format.

    Invalid or missing dates are converted to NaT.
    """
    df = df.copy()

    for column in DATE_COLUMNS:
        if column in df.columns:
            df[column] = pd.to_datetime(df[column], errors="coerce")

    return df


def convert_numeric_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert expected numeric columns to numeric dtype.

    Invalid values are converted to NaN.
    """
    df = df.copy()

    for column in NUMERIC_COLUMNS:
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce")

    return df


def normalize_text_value(value):
    """
    Normalize a single text value:
    - Handles missing values
    - Removes leading/trailing spaces
    - Collapses multiple spaces
    """
    if pd.isna(value):
        return value

    value = str(value).strip()
    value = re.sub(r"\s+", " ", value)

    return value


def normalize_categories(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize categorical columns.

    The goal is to reduce category inconsistencies caused by spaces,
    different casing, or inconsistent labels.
    """
    df = df.copy()

    for column in CATEGORY_COLUMNS:
        if column in df.columns:
            df[column] = df[column].apply(normalize_text_value)

    if "customer_gender" in df.columns:
        gender_map = {
            "male": "Male",
            "female": "Female",
            "other": "Other",
        }
        df["customer_gender"] = (
            df["customer_gender"]
            .str.lower()
            .map(gender_map)
            .fillna(df["customer_gender"])
        )

    if "ticket_type" in df.columns:
        ticket_type_map = {
            "technical issue": "Technical Issue",
            "billing inquiry": "Billing Inquiry",
            "product inquiry": "Product Inquiry",
            "refund request": "Refund Request",
            "cancellation request": "Cancellation Request",
        }
        df["ticket_type"] = (
            df["ticket_type"]
            .str.lower()
            .map(ticket_type_map)
            .fillna(df["ticket_type"])
        )

    if "ticket_status" in df.columns:
        status_map = {
            "open": "Open",
            "closed": "Closed",
            "pending customer response": "Pending Customer Response",
        }
        df["ticket_status"] = (
            df["ticket_status"]
            .str.lower()
            .map(status_map)
            .fillna(df["ticket_status"])
        )

    if "ticket_priority" in df.columns:
        priority_map = {
            "low": "Low",
            "medium": "Medium",
            "high": "High",
            "critical": "Critical",
        }
        df["ticket_priority"] = (
            df["ticket_priority"]
            .str.lower()
            .map(priority_map)
            .fillna(df["ticket_priority"])
        )

    if "ticket_channel" in df.columns:
        channel_map = {
            "email": "Email",
            "phone": "Phone",
            "chat": "Chat",
            "social media": "Social Media",
        }
        df["ticket_channel"] = (
            df["ticket_channel"]
            .str.lower()
            .map(channel_map)
            .fillna(df["ticket_channel"])
        )

    return df


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove duplicated records.

    First removes exact duplicated rows.
    Then, if ticket_id exists, removes duplicated ticket IDs keeping the first record.
    """
    df = df.copy()

    df = df.drop_duplicates()

    if "ticket_id" in df.columns:
        df = df.drop_duplicates(subset=["ticket_id"], keep="first")

    return df


def clean(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply the complete cleaning pipeline for the customer support tickets dataset.

    Cleaning steps:
    1. Convert column names to snake_case.
    2. Remove personal / high-noise text columns.
    3. Convert date columns.
    4. Convert numeric columns.
    5. Normalize categorical columns.
    6. Remove duplicated records.
    """
    df = df.copy()

    df = clean_column_names(df)
    df = remove_personal_columns(df)
    df = convert_dates(df)
    df = convert_numeric_columns(df)
    df = normalize_categories(df)
    df = remove_duplicates(df)

    return df