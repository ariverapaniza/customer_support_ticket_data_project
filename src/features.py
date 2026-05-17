import pandas as pd
import numpy as np


def add_product_age_days(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create product_age_days.

    This feature estimates how many days passed between the product purchase date
    and the first response time.

    If first_response_time is missing, the value will remain NaN.
    Negative values, if any, are treated as invalid and converted to NaN.
    """
    df = df.copy()

    if {"date_of_purchase", "first_response_time"}.issubset(df.columns):
        df["product_age_days"] = (
            df["first_response_time"] - df["date_of_purchase"]
        ).dt.days

        df.loc[df["product_age_days"] < 0, "product_age_days"] = np.nan

    return df


def add_resolution_hours(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create resolution_hours.

    resolution_hours = time_to_resolution - first_response_time

    Some rows in the dataset have time_to_resolution earlier than first_response_time.
    Those cases are flagged as data quality issues and converted to NaN for analysis.
    """
    df = df.copy()

    if {"first_response_time", "time_to_resolution"}.issubset(df.columns):
        raw_resolution_hours = (
            df["time_to_resolution"] - df["first_response_time"]
        ).dt.total_seconds() / 3600

        df["has_negative_resolution_time"] = raw_resolution_hours < 0

        df["resolution_hours"] = raw_resolution_hours
        df.loc[df["resolution_hours"] < 0, "resolution_hours"] = np.nan

    return df


def add_has_resolution(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create has_resolution.

    A ticket is considered to have a resolution timestamp when time_to_resolution
    is not missing.
    """
    df = df.copy()

    if "time_to_resolution" in df.columns:
        df["has_resolution"] = df["time_to_resolution"].notna()

    return df


def add_satisfaction_group(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create satisfaction_group from customer_satisfaction_rating.

    Rating scale:
    - 1 to 2: Low
    - 3: Medium
    - 4 to 5: High
    - Missing: No Rating
    """
    df = df.copy()

    if "customer_satisfaction_rating" in df.columns:
        df["satisfaction_group"] = pd.cut(
            df["customer_satisfaction_rating"],
            bins=[0, 2, 3, 5],
            labels=["Low", "Medium", "High"],
            include_lowest=True,
        )

        df["satisfaction_group"] = (
            df["satisfaction_group"]
            .cat.add_categories("No Rating")
            .fillna("No Rating")
        )

    return df


def add_is_high_priority(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create is_high_priority.

    High priority tickets are those marked as High or Critical.
    """
    df = df.copy()

    if "ticket_priority" in df.columns:
        df["is_high_priority"] = df["ticket_priority"].isin(["High", "Critical"])

    return df


def add_ticket_time_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create simple time-based features from first_response_time.

    These features help analyze ticket activity by date/month/hour.
    """
    df = df.copy()

    if "first_response_time" in df.columns:
        df["first_response_date"] = df["first_response_time"].dt.date
        df["first_response_year"] = df["first_response_time"].dt.year
        df["first_response_month"] = df["first_response_time"].dt.month
        df["first_response_hour"] = df["first_response_time"].dt.hour

    return df


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply the complete feature engineering pipeline.

    New features:
    - product_age_days
    - resolution_hours
    - has_negative_resolution_time
    - has_resolution
    - satisfaction_group
    - is_high_priority
    - first_response_date
    - first_response_year
    - first_response_month
    - first_response_hour
    """
    df = df.copy()

    df = add_product_age_days(df)
    df = add_resolution_hours(df)
    df = add_has_resolution(df)
    df = add_satisfaction_group(df)
    df = add_is_high_priority(df)
    df = add_ticket_time_features(df)

    return df