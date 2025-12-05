# plots_act3.py

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def compute_performance_index(df: pd.DataFrame, hp_col: str) -> pd.DataFrame:
    """
    Compute normalized performance index based on horsepower.

    Parameters
    ----------
    df : pd.DataFrame
        Dataset with horsepower column and Year
    hp_col : str
        Name of the horsepower column

    Returns
    -------
    pd.DataFrame
        Year and Performance_Index columns
    """
    # Group by year and compute mean HP
    yearly = df.groupby("Year", as_index=False)[hp_col].mean()

    # Normalize to 0-100 scale
    hp_min, hp_max = yearly[hp_col].min(), yearly[hp_col].max()
    yearly["Performance_Index"] = 100 * (yearly[hp_col] - hp_min) / (hp_max - hp_min)

    return yearly[["Year", "Performance_Index"]]


def compute_efficiency_index(df: pd.DataFrame, mpg_col: str) -> pd.DataFrame:
    """
    Compute normalized efficiency index based on MPG.

    Parameters
    ----------
    df : pd.DataFrame
        Dataset with MPG column and Year
    mpg_col : str
        Name of the MPG column

    Returns
    -------
    pd.DataFrame
        Year and Efficiency_Index columns
    """
    # Group by year and compute mean MPG
    yearly = df.groupby("Year", as_index=False)[mpg_col].mean()

    # Normalize to 0-100 scale
    mpg_min, mpg_max = yearly[mpg_col].min(), yearly[mpg_col].max()
    yearly["Efficiency_Index"] = 100 * (yearly[mpg_col] - mpg_min) / (mpg_max - mpg_min)

    return yearly[["Year", "Efficiency_Index"]]


def make_indices_chart(
    sports_df: pd.DataFrame,
    epa_df: pd.DataFrame,
    year_min: int = 2000,
    year_max: int = 2025,
    show_gas: bool = True,
    show_sports: bool = True,
    show_ev: bool = True,
):
    """
    Build Chart 3A: Side-by-side Performance and Efficiency Indices

    Left chart: Performance (HP) Index over time for Gas, Sports, EV
    Right chart: Efficiency (MPG) Index over time for Gas, Sports, EV

    All categories are normalized to the same global scale for comparability.

    Parameters
    ----------
    sports_df : pd.DataFrame
        Sports car dataset with MPG and Horsepower
    epa_df : pd.DataFrame
        EPA dataset with HP and MPG data
    year_min, year_max : int
        Year range to display
    show_gas : bool
        Show Gas vehicles line
    show_sports : bool
        Show Sports vehicles line
    show_ev : bool
        Show EV vehicles line

    Returns
    -------
    fig : matplotlib.figure.Figure
        Figure ready to embed in dashboard
    """
    # Filter datasets by year range
    sports_filtered = sports_df[(sports_df["Year"] >= year_min) & (sports_df["Year"] <= year_max)].copy()
    epa_filtered = epa_df[(epa_df["Year"] >= year_min) & (epa_df["Year"] <= year_max)].copy()

    # Define fuel type categories for EPA data
    gas_types = ['Regular', 'Premium', 'Midgrade', 'Gasoline or E85',
                 'Premium or E85', 'Diesel', 'Gasoline or natural gas', 'CNG']
    electric_types = ['Electricity', 'Regular Gas and Electricity',
                     'Premium Gas or Electricity', 'Premium and Electricity',
                     'Regular Gas or Electricity']

    # Split EPA data into Gas and EV
    epa_gas = epa_filtered[epa_filtered["Fuel Type"].isin(gas_types)]
    epa_ev = epa_filtered[epa_filtered["Fuel Type"].isin(electric_types)]

    # === PERFORMANCE INDEX (BASE YEAR NORMALIZATION) ===
    # Get yearly averages for each category
    gas_hp_yearly = epa_gas.groupby("Year", as_index=False)["Horsepower (est)"].mean()
    sports_hp_yearly = sports_filtered.groupby("Year", as_index=False)["Horsepower"].mean()
    ev_hp_yearly = epa_ev.groupby("Year", as_index=False)["Horsepower (est)"].mean()

    # Normalize to base year (first year in range = 100)
    gas_perf = gas_hp_yearly.copy()
    if len(gas_perf) > 0:
        base_hp_gas = gas_perf.iloc[0]["Horsepower (est)"]
        if base_hp_gas > 0:
            gas_perf["Performance_Index"] = 100 * gas_perf["Horsepower (est)"] / base_hp_gas
        else:
            gas_perf["Performance_Index"] = 100
    gas_perf = gas_perf[["Year", "Performance_Index"]]

    sports_perf = sports_hp_yearly.copy()
    if len(sports_perf) > 0:
        base_hp_sports = sports_perf.iloc[0]["Horsepower"]
        if base_hp_sports > 0:
            sports_perf["Performance_Index"] = 100 * sports_perf["Horsepower"] / base_hp_sports
        else:
            sports_perf["Performance_Index"] = 100
    sports_perf = sports_perf[["Year", "Performance_Index"]]

    ev_perf = ev_hp_yearly.copy()
    if len(ev_perf) > 0:
        base_hp_ev = ev_perf.iloc[0]["Horsepower (est)"]
        if base_hp_ev > 0:
            ev_perf["Performance_Index"] = 100 * ev_perf["Horsepower (est)"] / base_hp_ev
        else:
            ev_perf["Performance_Index"] = 100
    ev_perf = ev_perf[["Year", "Performance_Index"]]

    # === EFFICIENCY INDEX (BASE YEAR NORMALIZATION) ===
    # Get yearly averages for each category
    gas_mpg_yearly = epa_gas.groupby("Year", as_index=False)["Combined Mpg For Fuel Type1"].mean()
    sports_mpg_yearly = sports_filtered.groupby("Year", as_index=False)["MPG"].mean()
    ev_mpg_yearly = epa_ev.groupby("Year", as_index=False)["Combined Mpg For Fuel Type1"].mean()

    # Normalize to base year (first year in range = 100)
    gas_eff = gas_mpg_yearly.copy()
    if len(gas_eff) > 0:
        base_mpg_gas = gas_eff.iloc[0]["Combined Mpg For Fuel Type1"]
        if base_mpg_gas > 0:
            gas_eff["Efficiency_Index"] = 100 * gas_eff["Combined Mpg For Fuel Type1"] / base_mpg_gas
        else:
            gas_eff["Efficiency_Index"] = 100
    gas_eff = gas_eff[["Year", "Efficiency_Index"]]

    sports_eff = sports_mpg_yearly.copy()
    if len(sports_eff) > 0:
        base_mpg_sports = sports_eff.iloc[0]["MPG"]
        if base_mpg_sports > 0:
            sports_eff["Efficiency_Index"] = 100 * sports_eff["MPG"] / base_mpg_sports
        else:
            sports_eff["Efficiency_Index"] = 100
    sports_eff = sports_eff[["Year", "Efficiency_Index"]]

    ev_eff = ev_mpg_yearly.copy()
    if len(ev_eff) > 0:
        base_mpg_ev = ev_eff.iloc[0]["Combined Mpg For Fuel Type1"]
        if base_mpg_ev > 0:
            ev_eff["Efficiency_Index"] = 100 * ev_eff["Combined Mpg For Fuel Type1"] / base_mpg_ev
        else:
            ev_eff["Efficiency_Index"] = 100
    ev_eff = ev_eff[["Year", "Efficiency_Index"]]

    # Create figure with two subplots side by side
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5))

    # === LEFT CHART: PERFORMANCE INDEX ===
    if not (show_gas or show_sports or show_ev):
        ax1.text(
            0.5, 0.5,
            "No categories selected",
            ha='center', va='center',
            fontsize=12, color='gray',
            transform=ax1.transAxes
        )
    else:
        if show_gas and len(gas_perf) > 0:
            ax1.plot(
                gas_perf["Year"],
                gas_perf["Performance_Index"],
                label="Gas Vehicles",
                linewidth=2.5,
                color="#1f77b4",  # Blue
                marker='o',
                markersize=5
            )

        if show_sports and len(sports_perf) > 0:
            ax1.plot(
                sports_perf["Year"],
                sports_perf["Performance_Index"],
                label="Sports Cars",
                linewidth=2.5,
                color="#d62728",  # Red
                marker='s',
                markersize=5
            )

        if show_ev and len(ev_perf) > 0:
            ax1.plot(
                ev_perf["Year"],
                ev_perf["Performance_Index"],
                label="EV Vehicles",
                linewidth=2.5,
                color="#2ca02c",  # Green
                marker='^',
                markersize=5
            )

    ax1.set_xlabel("Year", fontsize=11)
    ax1.set_ylabel("Performance Index (Base Year = 100)", fontsize=11)
    ax1.set_title("Performance Index Over Time", fontsize=12, fontweight='bold')
    ax1.legend(fontsize=9, loc='best', framealpha=0.9)
    ax1.grid(True, alpha=0.3)
    ax1.axhline(y=100, color='gray', linestyle='--', linewidth=1, alpha=0.5)

    # === RIGHT CHART: EFFICIENCY INDEX ===
    if not (show_gas or show_sports or show_ev):
        ax2.text(
            0.5, 0.5,
            "No categories selected",
            ha='center', va='center',
            fontsize=12, color='gray',
            transform=ax2.transAxes
        )
    else:
        if show_gas and len(gas_eff) > 0:
            ax2.plot(
                gas_eff["Year"],
                gas_eff["Efficiency_Index"],
                label="Gas Vehicles",
                linewidth=2.5,
                color="#1f77b4",  # Blue
                marker='o',
                markersize=5
            )

        if show_sports and len(sports_eff) > 0:
            ax2.plot(
                sports_eff["Year"],
                sports_eff["Efficiency_Index"],
                label="Sports Cars",
                linewidth=2.5,
                color="#d62728",  # Red
                marker='s',
                markersize=5
            )

        if show_ev and len(ev_eff) > 0:
            ax2.plot(
                ev_eff["Year"],
                ev_eff["Efficiency_Index"],
                label="EV Vehicles",
                linewidth=2.5,
                color="#2ca02c",  # Green
                marker='^',
                markersize=5
            )

    ax2.set_xlabel("Year", fontsize=11)
    ax2.set_ylabel("Efficiency Index (Base Year = 100)", fontsize=11)
    ax2.set_title("Efficiency Index Over Time", fontsize=12, fontweight='bold')
    ax2.legend(fontsize=9, loc='best', framealpha=0.9)
    ax2.grid(True, alpha=0.3)
    ax2.axhline(y=100, color='gray', linestyle='--', linewidth=1, alpha=0.5)

    fig.tight_layout()
    return fig
