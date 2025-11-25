# plots_epa.py

import matplotlib.pyplot as plt
import pandas as pd


def compute_epa_yearly_aggregates(
    df: pd.DataFrame,
    year_min: int = 2000,
    year_max: int = 2025,
    fuel_types: list = None,
) -> pd.DataFrame:
    """
    Compute yearly averages for the EPA dataset for the metrics we care about.

    Expects columns:
    - 'Year'
    - 'Combined Mpg For Fuel Type1'
    - 'Co2  Tailpipe For Fuel Type1'
    - 'Engine displacement'
    - 'Fuel Type' (optional, for filtering)

    Parameters
    ----------
    df : pd.DataFrame
        EPA dataframe
    year_min, year_max : int
        Year range
    fuel_types : list of str, optional
        List of fuel types to include (e.g., ['Gasoline', 'Diesel/Electric']).
        If None or empty, include all fuel types.
    """

    # Filter by year range
    mask = (df["Year"] >= year_min) & (df["Year"] <= year_max)

    # Filter by fuel type if specified
    if fuel_types and len(fuel_types) > 0 and "Fuel Type" in df.columns:
        fuel_mask = df["Fuel Type"].isin(fuel_types)
        mask = mask & fuel_mask

    df_sub = df.loc[mask].copy()

    # Group by year and compute mean of key metrics
    grouped = (
        df_sub.groupby("Year", as_index=False)[
            [
                "Combined Mpg For Fuel Type1",
                "Co2  Tailpipe For Fuel Type1",
                "Engine displacement",
            ]
        ]
        .mean()
        .sort_values("Year")
    )

    return grouped


def make_epa_trend_figure(
    df: pd.DataFrame,
    year_min: int = 2000,
    year_max: int = 2025,
    show_mpg: bool = True,
    show_co2: bool = True,
    show_displacement: bool = True,
    normalize: bool = False,
):
    """
    Build Visualization 1B: EPA Trendlines.

    - X-axis: Year
    - Y-axis: MPG, CO2, and Engine displacement (on same or similar scale)
    - Lines can be toggled on/off via flags.

    Parameters
    ----------
    df : pd.DataFrame
        Cleaned EPA dataframe.
    year_min, year_max : int
        Year range to include.
    show_mpg, show_co2, show_displacement : bool
        Whether to draw each metric's line.
    normalize : bool
        If True, normalize each series so its first value in the range is 100.

    Returns
    -------
    fig : matplotlib.figure.Figure
        Figure ready to embed in a FigureCanvasQTAgg or save/show.
    """
    yearly = compute_epa_yearly_aggregates(df, year_min, year_max)

    # Copy to avoid modifying original
    plot_df = yearly.copy()

    # Optionally normalize each series to its first non-null value
    if normalize:
        for col in [
            "Combined Mpg For Fuel Type1",
            "Co2  Tailpipe For Fuel Type1",
            "Engine displacement",
        ]:
            if col in plot_df.columns:
                non_null = plot_df[col].dropna()
                if len(non_null) > 0:
                    first_valid = non_null.iloc[0]
                    if first_valid != 0:
                        plot_df[col] = (plot_df[col] / first_valid) * 100.0

    fig, ax = plt.subplots(figsize=(8, 5))

    # Check if at least one metric is enabled
    if not (show_mpg or show_co2 or show_displacement):
        ax.text(
            0.5, 0.5,
            "No metrics selected\n\nPlease enable at least one metric\nto view the visualization",
            ha='center', va='center',
            fontsize=12, color='gray',
            transform=ax.transAxes
        )
        ax.set_xlabel("Year")
        ax.set_ylabel("Value")
        ax.set_title("EPA Trendlines: Efficiency & Engine Size Over Time")
        ax.grid(True, alpha=0.3)
        fig.tight_layout()
        return fig

    # Plot lines based on flags
    if show_mpg and "Combined Mpg For Fuel Type1" in plot_df.columns:
        ax.plot(
            plot_df["Year"],
            plot_df["Combined Mpg For Fuel Type1"],
            label="Avg Combined MPG",
            linewidth=2,
        )

    if show_co2 and "Co2  Tailpipe For Fuel Type1" in plot_df.columns:
        ax.plot(
            plot_df["Year"],
            plot_df["Co2  Tailpipe For Fuel Type1"],
            label="Avg Tailpipe CO₂ (g/mi)",
            linewidth=2,
        )

    if show_displacement and "Engine displacement" in plot_df.columns:
        ax.plot(
            plot_df["Year"],
            plot_df["Engine displacement"],
            label="Avg Engine Displacement (L)",
            linewidth=2,
        )

    ax.set_xlabel("Year", fontsize=10)
    if normalize:
        ax.set_ylabel("Index (base year = 100)", fontsize=10)
    else:
        ax.set_ylabel("Value (units vary by line)", fontsize=10)
    ax.set_title("EPA Trendlines: Efficiency & Engine Size Over Time", fontsize=11)

    # Fix legend size and positioning
    ax.legend(fontsize=8, loc='best', framealpha=0.9)
    ax.grid(True, alpha=0.3)

    fig.tight_layout()
    return fig
