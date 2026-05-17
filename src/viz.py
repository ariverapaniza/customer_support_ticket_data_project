from pathlib import Path

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from src.config import FIGURES_PATH

sns.set_theme(style="whitegrid", context="notebook", palette="Set2")


def save_figure(fig: plt.Figure, filename: str, output_dir: Path = FIGURES_PATH) -> Path:
    """
    Save a matplotlib figure to the reports/figures folder.
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    file_path = output_dir / filename
    fig.savefig(file_path, dpi=300, bbox_inches="tight")
    plt.close(fig)

    return file_path


def plot_tickets_by_type(df: pd.DataFrame, save: bool = True):
    """
    Barplot: number of tickets by ticket type.

    Question:
    What types of tickets are most frequent?
    """
    ticket_counts = (
        df["ticket_type"]
        .value_counts()
        .reset_index()
    )
    ticket_counts.columns = ["ticket_type", "ticket_count"]

    fig, ax = plt.subplots(figsize=(10, 5))

    sns.barplot(
        data=ticket_counts,
        x="ticket_count",
        y="ticket_type",
        ax=ax,
    )

    ax.set_title("Number of Tickets by Ticket Type")
    ax.set_xlabel("Number of Tickets")
    ax.set_ylabel("Ticket Type")

    plt.tight_layout()

    if save:
        return save_figure(fig, "01_tickets_by_type.png")

    return fig, ax


def plot_tickets_by_priority(df: pd.DataFrame, save: bool = True):
    """
    Barplot: number of tickets by priority.

    Question:
    How are tickets distributed by priority?
    """
    priority_order = ["Low", "Medium", "High", "Critical"]

    ticket_counts = (
        df["ticket_priority"]
        .value_counts()
        .reindex(priority_order)
        .dropna()
        .reset_index()
    )
    ticket_counts.columns = ["ticket_priority", "ticket_count"]

    fig, ax = plt.subplots(figsize=(8, 5))

    sns.barplot(
        data=ticket_counts,
        x="ticket_priority",
        y="ticket_count",
        order=priority_order,
        ax=ax,
    )

    ax.set_title("Number of Tickets by Priority")
    ax.set_xlabel("Ticket Priority")
    ax.set_ylabel("Number of Tickets")

    plt.tight_layout()

    if save:
        return save_figure(fig, "02_tickets_by_priority.png")

    return fig, ax


def plot_resolution_time_by_priority(df: pd.DataFrame, save: bool = True):
    """
    Boxplot: resolution hours by ticket priority.

    Question:
    Do critical tickets take more or less time to resolve?

    Notes:
    - Uses only valid positive resolution_hours.
    - Negative resolution times were already converted to NaN in features.py.
    """
    priority_order = ["Low", "Medium", "High", "Critical"]

    valid_df = df[
        df["resolution_hours"].notna()
        & df["ticket_priority"].notna()
    ].copy()

    fig, ax = plt.subplots(figsize=(9, 5))

    sns.boxplot(
        data=valid_df,
        x="ticket_priority",
        y="resolution_hours",
        order=priority_order,
        ax=ax,
    )

    ax.set_title("Resolution Time by Ticket Priority")
    ax.set_xlabel("Ticket Priority")
    ax.set_ylabel("Resolution Time (hours)")

    plt.tight_layout()

    if save:
        return save_figure(fig, "03_resolution_time_by_priority.png")

    return fig, ax


def plot_satisfaction_by_channel(df: pd.DataFrame, save: bool = True):
    """
    Barplot: average customer satisfaction rating by ticket channel.

    Question:
    Which support channel has the highest average satisfaction?
    """
    satisfaction_by_channel = (
        df.dropna(subset=["customer_satisfaction_rating"])
        .groupby("ticket_channel", as_index=False)
        .agg(
            avg_satisfaction=("customer_satisfaction_rating", "mean"),
            ticket_count=("ticket_id", "count"),
        )
        .sort_values("avg_satisfaction", ascending=False)
    )

    fig, ax = plt.subplots(figsize=(9, 5))

    sns.barplot(
        data=satisfaction_by_channel,
        x="ticket_channel",
        y="avg_satisfaction",
        ax=ax,
    )

    ax.set_title("Average Customer Satisfaction by Support Channel")
    ax.set_xlabel("Ticket Channel")
    ax.set_ylabel("Average Satisfaction Rating")
    ax.set_ylim(0, 5)

    for container in ax.containers:
        ax.bar_label(container, fmt="%.2f", padding=3)

    plt.tight_layout()

    if save:
        return save_figure(fig, "04_satisfaction_by_channel.png")

    return fig, ax


def plot_resolution_vs_satisfaction(df: pd.DataFrame, save: bool = True):
    """
    Scatterplot/regplot: resolution hours vs customer satisfaction rating.

    Question:
    Are longer resolution times associated with lower satisfaction?
    """
    valid_df = df[
        df["resolution_hours"].notna()
        & df["customer_satisfaction_rating"].notna()
    ].copy()

    fig, ax = plt.subplots(figsize=(9, 5))

    sns.regplot(
        data=valid_df,
        x="resolution_hours",
        y="customer_satisfaction_rating",
        scatter_kws={"alpha": 0.35},
        line_kws={"linewidth": 2},
        ax=ax,
    )

    ax.set_title("Resolution Time vs Customer Satisfaction")
    ax.set_xlabel("Resolution Time (hours)")
    ax.set_ylabel("Customer Satisfaction Rating")
    ax.set_ylim(0.5, 5.5)

    plt.tight_layout()

    if save:
        return save_figure(fig, "05_resolution_vs_satisfaction.png")

    return fig, ax


def plot_top_products_by_tickets(
    df: pd.DataFrame,
    top_n: int = 10,
    save: bool = True,
):
    """
    Horizontal barplot: top products by number of tickets.

    Question:
    Which products generate the highest support workload?
    """
    product_counts = (
        df["product_purchased"]
        .value_counts()
        .head(top_n)
        .reset_index()
    )
    product_counts.columns = ["product_purchased", "ticket_count"]

    fig, ax = plt.subplots(figsize=(10, 6))

    sns.barplot(
        data=product_counts,
        x="ticket_count",
        y="product_purchased",
        ax=ax,
    )

    ax.set_title(f"Top {top_n} Products by Number of Tickets")
    ax.set_xlabel("Number of Tickets")
    ax.set_ylabel("Product Purchased")

    plt.tight_layout()

    if save:
        return save_figure(fig, "06_top_products_by_tickets.png")

    return fig, ax


def plot_graph(df: pd.DataFrame) -> None:
    """
    Generate and save all project visualizations.

    Output:
    reports/figures/
    """
    saved_files = []

    saved_files.append(plot_tickets_by_type(df, save=True))
    saved_files.append(plot_tickets_by_priority(df, save=True))
    saved_files.append(plot_resolution_time_by_priority(df, save=True))
    saved_files.append(plot_satisfaction_by_channel(df, save=True))
    saved_files.append(plot_resolution_vs_satisfaction(df, save=True))
    saved_files.append(plot_top_products_by_tickets(df, top_n=10, save=True))

    print("Visualizations saved:")
    for file_path in saved_files:
        print(f"- {file_path}")