# plots_act3.py

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


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


def make_cluster_plot(
    sports_df: pd.DataFrame,
    epa_df: pd.DataFrame,
    year_min: int = 2011,
    year_max: int = 2024,
    n_clusters: int = 3,
    show_sports: bool = True,
    show_epa: bool = True,
):
    """
    Build Chart 3B: Cluster Plot (PCA-reduced, K-means clustering)

    Combines sports and EPA datasets, extracts features (HP, MPG, displacement),
    runs PCA to reduce to 2D, then k-means clustering to identify market segments.

    Parameters
    ----------
    sports_df : pd.DataFrame
        Sports car dataset
    epa_df : pd.DataFrame
        EPA dataset
    year_min, year_max : int
        Year range to include
    n_clusters : int
        Number of clusters for k-means (default 3)
    show_sports : bool
        Include sports cars in clustering
    show_epa : bool
        Include EPA vehicles in clustering

    Returns
    -------
    fig : matplotlib.figure.Figure
        Figure ready to embed in dashboard
    """
    # Filter by year range
    sports_filtered = sports_df[(sports_df["Year"] >= year_min) & (sports_df["Year"] <= year_max)].copy()
    epa_filtered = epa_df[(epa_df["Year"] >= year_min) & (epa_df["Year"] <= year_max)].copy()

    # Prepare sports data
    sports_data = sports_filtered[["Horsepower", "MPG", "Engine Size (L)"]].copy()
    sports_data.columns = ["HP", "MPG", "Displacement"]
    sports_data["Market"] = "Sports"
    sports_data.dropna(inplace=True)

    # Prepare EPA data
    epa_data = epa_filtered[["Horsepower (est)", "Combined Mpg For Fuel Type1", "Engine displacement"]].copy()
    epa_data.columns = ["HP", "MPG", "Displacement"]
    epa_data["Market"] = "EPA"
    epa_data.dropna(inplace=True)

    # Combine datasets based on selections
    datasets = []
    if show_sports:
        datasets.append(sports_data)
    if show_epa:
        datasets.append(epa_data)

    if not datasets:
        # Empty plot if nothing selected
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.text(
            0.5, 0.5,
            "No market selected\n\nPlease enable Sports or EPA",
            ha='center', va='center',
            fontsize=12, color='gray',
            transform=ax.transAxes
        )
        ax.set_xlabel("PC1")
        ax.set_ylabel("PC2")
        ax.set_title("Chart 3B: Market Clustering (PCA + K-Means)")
        fig.tight_layout()
        return fig

    combined = pd.concat(datasets, ignore_index=True)

    # Check minimum sample size
    if len(combined) < n_clusters * 2:
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.text(
            0.5, 0.5,
            f"Not enough data\n\nNeed at least {n_clusters * 2} samples\nGot {len(combined)}",
            ha='center', va='center',
            fontsize=12, color='gray',
            transform=ax.transAxes
        )
        ax.set_xlabel("PC1")
        ax.set_ylabel("PC2")
        ax.set_title("Chart 3B: Market Clustering (PCA + K-Means)")
        fig.tight_layout()
        return fig

    # Extract features for clustering
    features = combined[["HP", "MPG", "Displacement"]].values

    # Standardize features (important for PCA and k-means)
    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features)

    # Run PCA to reduce to 2D
    pca = PCA(n_components=2)
    features_pca = pca.fit_transform(features_scaled)

    # Run k-means clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    clusters = kmeans.fit_predict(features_scaled)

    # Add PCA coordinates and cluster labels to dataframe
    combined["PC1"] = features_pca[:, 0]
    combined["PC2"] = features_pca[:, 1]
    combined["Cluster"] = clusters

    # Create plot
    fig, ax = plt.subplots(figsize=(8, 6))

    # Define colors for clusters
    cluster_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']

    # Plot each cluster-market combination
    for cluster_id in range(n_clusters):
        cluster_data = combined[combined["Cluster"] == cluster_id]

        # Plot sports cars in this cluster
        sports_cluster = cluster_data[cluster_data["Market"] == "Sports"]
        if len(sports_cluster) > 0:
            ax.scatter(
                sports_cluster["PC1"],
                sports_cluster["PC2"],
                c=cluster_colors[cluster_id],
                marker='s',  # Square for sports
                s=80,
                alpha=0.7,
                edgecolors='black',
                linewidth=0.5,
                label=f"Cluster {cluster_id + 1} - Sports" if show_sports and show_epa else None
            )

        # Plot EPA vehicles in this cluster
        epa_cluster = cluster_data[cluster_data["Market"] == "EPA"]
        if len(epa_cluster) > 0:
            ax.scatter(
                epa_cluster["PC1"],
                epa_cluster["PC2"],
                c=cluster_colors[cluster_id],
                marker='o',  # Circle for EPA
                s=50,
                alpha=0.6,
                edgecolors='black',
                linewidth=0.5,
                label=f"Cluster {cluster_id + 1} - EPA" if show_sports and show_epa else None
            )

    # Add cluster centers
    centers_pca = pca.transform(scaler.transform(kmeans.cluster_centers_))
    ax.scatter(
        centers_pca[:, 0],
        centers_pca[:, 1],
        c='black',
        marker='X',
        s=200,
        edgecolors='white',
        linewidth=2,
        label='Cluster Centers',
        zorder=10
    )

    ax.set_xlabel(f"PC1 ({pca.explained_variance_ratio_[0]*100:.1f}% variance)", fontsize=11)
    ax.set_ylabel(f"PC2 ({pca.explained_variance_ratio_[1]*100:.1f}% variance)", fontsize=11)
    ax.set_title(f"Chart 3B: Market Clustering (K={n_clusters})", fontsize=12, fontweight='bold')
    ax.grid(True, alpha=0.3)

    # Custom legend
    if show_sports and show_epa:
        # Create custom legend to show market types
        from matplotlib.lines import Line2D
        legend_elements = [
            Line2D([0], [0], marker='s', color='w', markerfacecolor='gray', markersize=10, label='Sports Cars', markeredgecolor='black'),
            Line2D([0], [0], marker='o', color='w', markerfacecolor='gray', markersize=8, label='EPA Vehicles', markeredgecolor='black'),
            Line2D([0], [0], marker='X', color='w', markerfacecolor='black', markersize=12, label='Cluster Centers', markeredgecolor='white', markeredgewidth=2),
        ]
        ax.legend(handles=legend_elements, fontsize=9, loc='best', framealpha=0.9)
    else:
        ax.legend(fontsize=9, loc='best', framealpha=0.9)

    fig.tight_layout()
    return fig
