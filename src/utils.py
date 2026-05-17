import pandas as pd

def assert_columns(df: pd.DataFrame, required: list[str]) -> None:
    """
    Validate that required columns exist in the DataFrame.
    """
    missing = [column for column in required if column not in df.columns]

    if missing:
        raise ValueError(f"Missing columns: {missing}")


def assert_not_empty(df: pd.DataFrame) -> None:
    """
    Validate that the DataFrame is not empty.
    """
    if df.empty:
        raise ValueError("The DataFrame is empty.")


def assert_no_duplicate_ticket_ids(df: pd.DataFrame) -> None:
    """
    Validate that ticket_id does not contain duplicate values.
    """
    if "ticket_id" not in df.columns:
        return

    duplicated_count = df["ticket_id"].duplicated().sum()

    if duplicated_count > 0:
        raise ValueError(f"Found duplicated ticket_id values: {duplicated_count}")


def assert_datetime_columns(df: pd.DataFrame, columns: list[str]) -> None:
    """
    Validate that selected columns are datetime columns.
    """
    invalid_columns = []

    for column in columns:
        if column in df.columns and not pd.api.types.is_datetime64_any_dtype(df[column]):
            invalid_columns.append(column)

    if invalid_columns:
        raise TypeError(f"These columns are not datetime type: {invalid_columns}")


def assert_numeric_columns(df: pd.DataFrame, columns: list[str]) -> None:
    """
    Validate that selected columns are numeric columns.
    """
    invalid_columns = []

    for column in columns:
        if column in df.columns and not pd.api.types.is_numeric_dtype(df[column]):
            invalid_columns.append(column)

    if invalid_columns:
        raise TypeError(f"These columns are not numeric type: {invalid_columns}")


def assert_allowed_values(
    df: pd.DataFrame,
    column: str,
    allowed_values: list[str],
    allow_missing: bool = True,
) -> None:
    """
    Validate that a categorical column only contains expected values.
    """
    if column not in df.columns:
        return

    values = df[column]

    if allow_missing:
        values = values.dropna()

    unexpected_values = sorted(set(values.unique()) - set(allowed_values))

    if unexpected_values:
        raise ValueError(
            f"Unexpected values found in '{column}': {unexpected_values}. "
            f"Allowed values are: {allowed_values}"
        )


def validate_raw_dataset(df: pd.DataFrame) -> None:
    """
    Validate the raw dataset before cleaning.

    This function uses the original column names from the CSV.
    """
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

    assert_not_empty(df)
    assert_columns(df, required_columns)


def validate_clean_dataset(df: pd.DataFrame) -> None:
    """
    Validate the cleaned dataset after cleaning and feature engineering.

    This function uses snake_case column names.
    """
    required_columns = [
        "ticket_id",
        "customer_age",
        "customer_gender",
        "product_purchased",
        "date_of_purchase",
        "ticket_type",
        "ticket_subject",
        "ticket_status",
        "ticket_priority",
        "ticket_channel",
        "first_response_time",
        "time_to_resolution",
        "customer_satisfaction_rating",
        "product_age_days",
        "has_negative_resolution_time",
        "resolution_hours",
        "has_resolution",
        "satisfaction_group",
        "is_high_priority",
    ]

    assert_not_empty(df)
    assert_columns(df, required_columns)
    assert_no_duplicate_ticket_ids(df)

    assert_datetime_columns(
        df,
        [
            "date_of_purchase",
            "first_response_time",
            "time_to_resolution",
        ],
    )

    assert_numeric_columns(
        df,
        [
            "ticket_id",
            "customer_age",
            "customer_satisfaction_rating",
            "product_age_days",
            "resolution_hours",
        ],
    )

    assert_allowed_values(
        df,
        column="customer_gender",
        allowed_values=["Male", "Female", "Other"],
    )

    assert_allowed_values(
        df,
        column="ticket_type",
        allowed_values=[
            "Technical Issue",
            "Billing Inquiry",
            "Product Inquiry",
            "Refund Request",
            "Cancellation Request",
        ],
    )

    assert_allowed_values(
        df,
        column="ticket_status",
        allowed_values=[
            "Open",
            "Closed",
            "Pending Customer Response",
        ],
    )

    assert_allowed_values(
        df,
        column="ticket_priority",
        allowed_values=[
            "Low",
            "Medium",
            "High",
            "Critical",
        ],
    )

    assert_allowed_values(
        df,
        column="ticket_channel",
        allowed_values=[
            "Email",
            "Phone",
            "Chat",
            "Social Media",
        ],
    )

    assert_allowed_values(
        df,
        column="satisfaction_group",
        allowed_values=[
            "Low",
            "Medium",
            "High",
            "No Rating",
        ],
    )
    