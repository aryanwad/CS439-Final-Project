# plots_epa.py

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


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


def compute_fuel_share_by_year(
    df: pd.DataFrame,
    year_min: int = 2011,
    year_max: int = 2024,
    fuel_types: list = None,
) -> pd.DataFrame:
    """
    Compute the count of vehicles by fuel type for each year.

    Parameters
    ----------
    df : pd.DataFrame
        EPA dataframe with 'Year' and 'Fuel Type' columns
    year_min, year_max : int
        Year range to analyze
    fuel_types : list of str, optional
        List of fuel types to include. If None, include all.

    Returns
    -------
    pd.DataFrame
        Wide-format dataframe with columns:
        - Year
        - One column per fuel type with counts
    """
    # Filter by year range
    mask = (df["Year"] >= year_min) & (df["Year"] <= year_max)

    # Filter by fuel types if specified
    if fuel_types and len(fuel_types) > 0 and "Fuel Type" in df.columns:
        fuel_mask = df["Fuel Type"].isin(fuel_types)
        mask = mask & fuel_mask

    df_sub = df.loc[mask].copy()

    # Check if we have the necessary columns
    if "Fuel Type" not in df_sub.columns:
        raise ValueError("DataFrame must have 'Fuel Type' column")

    # Group by Year and Fuel Type, count occurrences
    fuel_counts = (
        df_sub.groupby(["Year", "Fuel Type"], as_index=False)
        .size()
        .rename(columns={"size": "count"})
    )

    # Pivot to wide format: rows=years, columns=fuel types
    fuel_wide = fuel_counts.pivot(
        index="Year", columns="Fuel Type", values="count"
    ).fillna(0)

    # Reset index to make Year a column again
    fuel_wide = fuel_wide.reset_index()

    return fuel_wide


def make_epa_fuel_share_figure(
    df: pd.DataFrame,
    year_min: int = 2013,
    year_max: int = 2024,
    fuel_types: list = None,
    use_percent: bool = True,
) -> plt.Figure:
    """
    Build Visualization 2A: EPA Fuel Share Over Time (Stacked Area Chart).

    Shows the transition from gas → hybrid → EV over time.

    Parameters
    ----------
    df : pd.DataFrame
        EPA dataframe with 'Year' and 'Fuel Type' columns
    year_min, year_max : int
        Year range to display
    fuel_types : list of str, optional
        Fuel types to include in the chart. If None, include all.
    use_percent : bool
        If True, show percentage share (0-100%).
        If False, show raw counts.

    Returns
    -------
    fig : matplotlib.figure.Figure
        Figure ready to embed in FigureCanvas
    """
    # Get fuel counts by year
    fuel_wide = compute_fuel_share_by_year(df, year_min, year_max, fuel_types)

    # If no data, return empty figure with message
    if len(fuel_wide) == 0:
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.text(
            0.5, 0.5,
            "No data available for selected filters",
            ha='center', va='center',
            fontsize=12, color='gray',
            transform=ax.transAxes
        )
        ax.set_xlabel("Year")
        ax.set_ylabel("Share")
        ax.set_title("Fuel Type Market Share Over Time")
        fig.tight_layout()
        return fig

    years = fuel_wide["Year"].values

    # Get fuel type columns (all columns except 'Year')
    fuel_cols = [col for col in fuel_wide.columns if col != "Year"]

    # If no fuel types found, return empty message
    if len(fuel_cols) == 0:
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.text(
            0.5, 0.5,
            "No fuel types selected",
            ha='center', va='center',
            fontsize=12, color='gray',
            transform=ax.transAxes
        )
        ax.set_xlabel("Year")
        ax.set_ylabel("Share")
        ax.set_title("Fuel Type Market Share Over Time")
        fig.tight_layout()
        return fig

    # Convert to percentage if requested
    if use_percent:
        # Calculate row sums (total vehicles per year)
        row_sums = fuel_wide[fuel_cols].sum(axis=1)
        # Avoid division by zero
        row_sums = row_sums.replace(0, 1)
        # Normalize each row to percentage
        for col in fuel_cols:
            fuel_wide[col] = (fuel_wide[col] / row_sums) * 100

    # Prepare data for stackplot (needs lists of values for each fuel type)
    fuel_data = [fuel_wide[col].values for col in fuel_cols]

    # Define colors for fuel types - simplified to 2 categories
    # All gas types → Blue, All electric types → Green
    color_map = {
        # Gas types (Blue)
        "Regular": "#1f77b4",
        "Premium": "#1f77b4",
        "Midgrade": "#1f77b4",
        "Gasoline or E85": "#1f77b4",
        "Premium or E85": "#1f77b4",
        "Diesel": "#1f77b4",
        "Gasoline or natural gas": "#1f77b4",
        "CNG": "#1f77b4",
        # Electric types (Green)
        "Electricity": "#2ca02c",
        "Regular Gas and Electricity": "#2ca02c",
        "Premium Gas or Electricity": "#2ca02c",
        "Premium and Electricity": "#2ca02c",
        "Regular Gas or Electricity": "#2ca02c",
    }

    # Assign colors based on fuel type names
    colors = [color_map.get(ft, "#bcbd22") for ft in fuel_cols]

    # Create figure
    fig, ax = plt.subplots(figsize=(8, 5))

    # Create stacked area chart
    ax.stackplot(years, *fuel_data, labels=fuel_cols, colors=colors, alpha=0.8)

    # Formatting
    ax.set_xlabel("Year", fontsize=10)
    if use_percent:
        ax.set_ylabel("Market Share (%)", fontsize=10)
        ax.set_ylim(0, 100)
    else:
        ax.set_ylabel("Number of Vehicle Models", fontsize=10)

    ax.set_title("Fuel Type Market Share Over Time (EPA Dataset)", fontsize=11)
    ax.legend(fontsize=8, loc='upper left', framealpha=0.9)
    ax.grid(True, alpha=0.3, axis='y')

    fig.tight_layout()
    return fig


def make_epa_performance_efficiency_scatter(
    df: pd.DataFrame,
    year_min: int = 2013,
    year_max: int = 2024,
    fuel_types: list = None,
    show_only_electrified: bool = False,
) -> plt.Figure:
    """
    Build Visualization 2B: EPA Performance vs Efficiency Scatter Plot.

    Shows how EVs break the old tradeoff between emissions (CO2) and efficiency (MPG).

    Parameters
    ----------
    df : pd.DataFrame
        EPA dataframe with columns:
        - 'Year'
        - 'Fuel Type'
        - 'Co2  Tailpipe For Fuel Type1'
        - 'Combined Mpg For Fuel Type1'
    year_min, year_max : int
        Year range to display
    fuel_types : list of str, optional
        Fuel types to include. If None, include all.
    show_only_electrified : bool
        If True, show only Hybrid and EV vehicles.

    Returns
    -------
    fig : matplotlib.figure.Figure
        Figure ready to embed in FigureCanvas
    """
    # Filter by year range
    mask = (df["Year"] >= year_min) & (df["Year"] <= year_max)

    # Filter by fuel types if specified
    if fuel_types and len(fuel_types) > 0 and "Fuel Type" in df.columns:
        fuel_mask = df["Fuel Type"].isin(fuel_types)
        mask = mask & fuel_mask

    # Show only electrified if requested
    if show_only_electrified and "Fuel Type" in df.columns:
        electrified_mask = df["Fuel Type"].isin(["Diesel/Electric", "Electricity"])
        mask = mask & electrified_mask

    df_sub = df.loc[mask].copy()

    # Drop rows with missing MPG data
    df_sub = df_sub.dropna(subset=["Combined Mpg For Fuel Type1"])

    # Create figure
    fig, ax = plt.subplots(figsize=(8, 5))

    # If no data, show message
    if len(df_sub) == 0:
        ax.text(
            0.5, 0.5,
            "No data available for selected filters",
            ha='center', va='center',
            fontsize=12, color='gray',
            transform=ax.transAxes
        )
        ax.set_xlabel("Year")
        ax.set_ylabel("Combined MPG")
        ax.set_title("Efficiency Evolution Over Time")
        fig.tight_layout()
        return fig

    # Define colors for fuel types - simplified to 2 categories
    # All gas types → Blue, All electric types → Green
    color_map = {
        # Gas types (Blue)
        "Regular": "#1f77b4",
        "Premium": "#1f77b4",
        "Midgrade": "#1f77b4",
        "Gasoline or E85": "#1f77b4",
        "Premium or E85": "#1f77b4",
        "Diesel": "#1f77b4",
        "Gasoline or natural gas": "#1f77b4",
        "CNG": "#1f77b4",
        # Electric types (Green)
        "Electricity": "#2ca02c",
        "Regular Gas and Electricity": "#2ca02c",
        "Premium Gas or Electricity": "#2ca02c",
        "Premium and Electricity": "#2ca02c",
        "Regular Gas or Electricity": "#2ca02c",
    }

    # Get unique fuel types in the filtered data
    fuel_types_present = df_sub["Fuel Type"].unique()

    # Plot each fuel type separately for better legend control
    for fuel_type in fuel_types_present:
        fuel_data = df_sub[df_sub["Fuel Type"] == fuel_type]
        color = color_map.get(fuel_type, "#bcbd22")

        ax.scatter(
            fuel_data["Year"],
            fuel_data["Combined Mpg For Fuel Type1"],
            c=color,
            label=fuel_type,
            alpha=0.5,
            s=25,
            edgecolors='none'
        )

    # Formatting
    ax.set_xlabel("Year", fontsize=10)
    ax.set_ylabel("Combined MPG", fontsize=10)
    ax.set_title("Efficiency Evolution Over Time", fontsize=11)
    ax.legend(fontsize=8, loc='upper left', framealpha=0.9)
    ax.grid(True, alpha=0.3)

    # Set reasonable axis limits
    ax.set_ylim(bottom=0)

    fig.tight_layout()
    return fig
