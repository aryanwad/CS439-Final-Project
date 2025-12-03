# plots_sports.py

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def compute_sports_yearly_aggregates(
    df: pd.DataFrame,
    year_min: int = 2000,
    year_max: int = 2025,
    brands: list = None,
) -> pd.DataFrame:
    """
    Compute yearly averages for the sports car dataset.

    Expects columns:
    - 'Year'
    - 'Horsepower'
    - 'Engine Size (L)'
    - 'Price (in USD)'
    - '0-60 MPH Time (seconds)'
    - 'Car Make' (optional, for filtering)

    Parameters
    ----------
    df : pd.DataFrame
        Sports car dataframe
    year_min, year_max : int
        Year range
    brands : list of str, optional
        List of brands to include (e.g., ['Porsche', 'Ferrari']).
        If None or empty, include all brands.
    """

    # Filter by year range
    mask = (df["Year"] >= year_min) & (df["Year"] <= year_max)

    # Filter by brand if specified
    if brands and len(brands) > 0 and "Car Make" in df.columns:
        brand_mask = df["Car Make"].isin(brands)
        mask = mask & brand_mask

    df_sub = df.loc[mask].copy()

    # Group by year and compute mean of key metrics
    grouped = (
        df_sub.groupby("Year", as_index=False)[
            [
                "Horsepower",
                "Engine Size (L)",
                "Price (in USD)",
                "0-60 MPH Time (seconds)",
            ]
        ]
        .mean()
        .sort_values("Year")
    )

    return grouped


def make_sports_trend_figure(
    df: pd.DataFrame,
    year_min: int = 2000,
    year_max: int = 2025,
    show_hp: bool = True,
    show_engine: bool = True,
    show_price: bool = True,
    normalize: bool = False,
    brands: list = None,
):
    """
    Build Visualization 1A: Sports Car Trendlines.

    - X-axis: Year
    - Y-axis: Horsepower, Engine Size, Price
    - Lines can be toggled on/off via flags.

    Parameters
    ----------
    df : pd.DataFrame
        Cleaned sports car dataframe.
    year_min, year_max : int
        Year range to include.
    show_hp, show_engine, show_price : bool
        Whether to draw each metric's line.
    normalize : bool
        If True, normalize each series so its first value in the range is 100.
    brands : list of str, optional
        List of brands to filter (e.g., ['Porsche', 'Ferrari']).

    Returns
    -------
    fig : matplotlib.figure.Figure
        Figure ready to embed in a FigureCanvasQTAgg or save/show.
    """
    yearly = compute_sports_yearly_aggregates(df, year_min, year_max, brands)

    # Copy to avoid modifying original
    plot_df = yearly.copy()

    # Optionally normalize each series to its first non-null value
    if normalize:
        for col in [
            "Horsepower",
            "Engine Size (L)",
            "Price (in USD)",
        ]:
            if col in plot_df.columns:
                non_null = plot_df[col].dropna()
                if len(non_null) > 0:
                    first_valid = non_null.iloc[0]
                    if first_valid != 0:
                        plot_df[col] = (plot_df[col] / first_valid) * 100.0

    fig, ax = plt.subplots(figsize=(8, 5))

    # Check if at least one metric is enabled
    if not (show_hp or show_engine or show_price):
        ax.text(
            0.5, 0.5,
            "No metrics selected\n\nPlease enable at least one metric\nto view the visualization",
            ha='center', va='center',
            fontsize=12, color='gray',
            transform=ax.transAxes
        )
        ax.set_xlabel("Year")
        ax.set_ylabel("Value")
        ax.set_title("Sports Car Trendlines: Performance & Price Over Time")
        ax.grid(True, alpha=0.3)
        fig.tight_layout()
        return fig

    # Plot lines based on flags
    if show_hp and "Horsepower" in plot_df.columns:
        ax.plot(
            plot_df["Year"],
            plot_df["Horsepower"],
            label="Avg Horsepower",
            linewidth=2,
            color="#d62728",  # Red
        )

    if show_engine and "Engine Size (L)" in plot_df.columns:
        ax.plot(
            plot_df["Year"],
            plot_df["Engine Size (L)"],
            label="Avg Engine Size (L)",
            linewidth=2,
            color="#ff7f0e",  # Orange
        )

    if show_price and "Price (in USD)" in plot_df.columns:
        # Price is on a different scale, so we might want to handle it differently
        # For now, plot it on the same axis (normalized view will help)
        ax.plot(
            plot_df["Year"],
            plot_df["Price (in USD)"],
            label="Avg Price (USD)",
            linewidth=2,
            color="#2ca02c",  # Green
        )

    ax.set_xlabel("Year", fontsize=10)
    if normalize:
        ax.set_ylabel("Index (base year = 100)", fontsize=10)
    else:
        ax.set_ylabel("Value (units vary by line)", fontsize=10)
    ax.set_title("Sports Car Trendlines: Performance & Price Over Time", fontsize=11)

    # Fix legend size and positioning
    ax.legend(fontsize=8, loc='best', framealpha=0.9)
    ax.grid(True, alpha=0.3)

    fig.tight_layout()
    return fig
