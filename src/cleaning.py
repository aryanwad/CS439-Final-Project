"""
cleaning.py

Utility functions to load and clean the EPA all-vehicles dataset
and the sports car dataset for the CS 439 final project.
"""

from __future__ import annotations
from pathlib import Path
from typing import Union
import pandas as pd

PathLike = Union[str, Path]


def load_and_clean_epa(
    path: PathLike,
    year_min: int = 2000,
    year_max: int = 2025,
) -> pd.DataFrame:
    """
    Load and clean the EPA all-vehicles dataset.

    - Reads a semicolon-separated CSV.
    - Filters to rows with valid MPG data in a given year range.
    - Keeps only columns that we actually use in the analysis.

    Parameters
    ----------
    path : str or Path
        Path to `all-vehicles-model.csv`.
    year_min : int
        Minimum year (inclusive).
    year_max : int
        Maximum year (inclusive).

    Returns
    -------
    pd.DataFrame
        Cleaned EPA dataframe.
    """
    path = Path(path)

    # EPA file uses ';' as the delimiter
    epa = pd.read_csv("../data/raw/all-vehicles-model.csv", sep=";", low_memory=False)

    # Columns we care about (you can add more if needed)
    cols_of_interest = [
        "Make",
        "Model",
        "Year",
        "Fuel Type",
        "MPG Data",
        "Combined Mpg For Fuel Type1",
        "Co2  Tailpipe For Fuel Type1",
        "Engine displacement",
    ]

    # Some files occasionally miss a column; intersect to be safe
    existing_cols = [c for c in cols_of_interest if c in epa.columns]
    epa = epa[existing_cols].copy()

    # Filter to year range and valid MPG data
    if "Year" in epa.columns:
        year_mask = (epa["Year"] >= year_min) & (epa["Year"] <= year_max)
    else:
        raise ValueError("EPA dataset is missing 'Year' column.")

    if "MPG Data" in epa.columns:
        mpg_mask = epa["MPG Data"] == "Y"
    else:
        # If the column is missing for some reason, just keep all rows
        mpg_mask = True

    epa_clean = epa.loc[year_mask & mpg_mask].copy()

    # Ensure numeric dtypes for key columns (in case of any weirdness)
    for col in [
        "Combined Mpg For Fuel Type1",
        "Co2  Tailpipe For Fuel Type1",
        "Engine displacement",
    ]:
        if col in epa_clean.columns:
            epa_clean[col] = pd.to_numeric(epa_clean[col], errors="coerce")

    return epa_clean


def load_and_clean_sports(
    path: PathLike,
    year_min: int = 2000,
    year_max: int = 2025,
) -> pd.DataFrame:
    """
    Load and clean the sports car dataset.

    - Converts performance and price columns to numeric.
    - Filters to a given year range.
    - Returns a clean dataframe ready for aggregation.

    Parameters
    ----------
    path : str or Path
        Path to `Sport car price.csv`.
    year_min : int
        Minimum year (inclusive).
    year_max : int
        Maximum year (inclusive).

    Returns
    -------
    pd.DataFrame
        Cleaned sports car dataframe.
    """
    path = Path(path)
    sports = pd.read_csv("../data/raw/Sport-car-price.csv", low_memory=False)

    numeric_cols = [
        "Engine Size (L)",
        "Horsepower",
        "Torque (lb-ft)",
        "0-60 MPH Time (seconds)",
        "Price (in USD)",
    ]

    # Clean numeric columns: remove commas, extract numeric substring, cast to float/int
    sports_clean = sports.copy()
    for col in numeric_cols:
        if col not in sports_clean.columns:
            continue

        sports_clean[col] = (
            sports_clean[col]
            .astype(str)
            .str.replace(",", "", regex=False)
            .str.extract(r"([0-9.]+)")[0]
        )
        sports_clean[col] = pd.to_numeric(sports_clean[col], errors="coerce")

    # Filter by year range (if Year column exists)
    if "Year" in sports_clean.columns:
        year_mask = (sports_clean["Year"] >= year_min) & (
            sports_clean["Year"] <= year_max
        )
        sports_clean = sports_clean.loc[year_mask].copy()
    else:
        raise ValueError("Sports dataset is missing 'Year' column.")

    return sports_clean


def load_and_clean_epa_with_hp(
    path: PathLike,
    year_min: int = 2000,
    year_max: int = 2025,
) -> pd.DataFrame:
    """
    Load and clean the EPA all-vehicles dataset WITH horsepower data.

    - Reads the new all-vehicles-model-with-hp-0-60.csv file (semicolon-separated).
    - Filters to rows with valid MPG data in a given year range.
    - Keeps columns including Horsepower and 0-60 time.
    - Removes sports cars to avoid overlap with sports dataset.

    Parameters
    ----------
    path : str or Path
        Path to `all-vehicles-model-with-hp-0-60.csv`.
    year_min : int
        Minimum year (inclusive).
    year_max : int
        Maximum year (inclusive).

    Returns
    -------
    pd.DataFrame
        Cleaned EPA dataframe with HP data and sports cars removed.
    """
    path = Path(path)

    # EPA file uses ';' as the delimiter
    epa = pd.read_csv(path, sep=";", low_memory=False)

    # Columns we care about
    cols_of_interest = [
        "Make",
        "Model",
        "Year",
        "Fuel Type",
        "MPG Data",
        "Combined Mpg For Fuel Type1",
        "Co2  Tailpipe For Fuel Type1",
        "Engine displacement",
        "Horsepower (est)",
        "0-60 time (est)",
    ]

    # Some files occasionally miss a column; intersect to be safe
    existing_cols = [c for c in cols_of_interest if c in epa.columns]
    epa = epa[existing_cols].copy()

    # Filter to year range
    if "Year" in epa.columns:
        year_mask = (epa["Year"] >= year_min) & (epa["Year"] <= year_max)
    else:
        raise ValueError("EPA dataset is missing 'Year' column.")

    # Filter for vehicles with valid Combined MPG data
    # NOTE: We no longer filter by "MPG Data = Y" because BOTH Y and N have valid MPG!
    # MPG Data = Y: 5-cycle EPA test (modern, more accurate)
    # MPG Data = N: 2-cycle EPA test or estimates (older, but still valid)
    # This change increases our dataset from ~9,000 to ~27,000 vehicles!
    if "Combined Mpg For Fuel Type1" in epa.columns:
        mpg_mask = pd.notna(epa["Combined Mpg For Fuel Type1"]) & (epa["Combined Mpg For Fuel Type1"] > 0)
    else:
        # If the column is missing for some reason, just keep all rows
        mpg_mask = True

    print(f"Total vehicles in year range {year_min}-{year_max}: {year_mask.sum()}")
    print(f"Vehicles with valid Combined MPG: {(year_mask & mpg_mask).sum()}")

    epa_clean = epa.loc[year_mask & mpg_mask].copy()

    # Ensure numeric dtypes for key columns
    for col in [
        "Combined Mpg For Fuel Type1",
        "Co2  Tailpipe For Fuel Type1",
        "Engine displacement",
        "Horsepower (est)",
        "0-60 time (est)",
    ]:
        if col in epa_clean.columns:
            epa_clean[col] = pd.to_numeric(epa_clean[col], errors="coerce")

    # Remove sports cars to avoid overlap with sports dataset
    print(f"Before removing sports cars: {len(epa_clean)} vehicles")
    epa_clean = filter_sports_from_epa(epa_clean)
    print(f"After removing sports cars: {len(epa_clean)} vehicles")

    return epa_clean


def load_and_clean_sports_with_mpg(
    path: PathLike,
    year_min: int = 2000,
    year_max: int = 2025,
) -> pd.DataFrame:
    """
    Load and clean the sports car dataset WITH MPG data.

    - Reads the new Sport car price with mpg adjusted.csv file.
    - Converts performance, price, and MPG columns to numeric.
    - Filters to a given year range.
    - Removes duplicates (prioritizing rows with price data).
    - Returns a clean dataframe ready for aggregation.

    Parameters
    ----------
    path : str or Path
        Path to `Sport car price with mpg adjusted.csv`.
    year_min : int
        Minimum year (inclusive).
    year_max : int
        Maximum year (inclusive).

    Returns
    -------
    pd.DataFrame
        Cleaned sports car dataframe with MPG.
    """
    path = Path(path)
    sports = pd.read_csv(path, low_memory=False)

    numeric_cols = [
        "Engine Size (L)",
        "Horsepower",
        "Torque (lb-ft)",
        "0-60 MPH Time (seconds)",
        "Price (in USD)",
        "MPG",
    ]

    # Clean numeric columns: remove commas, extract numeric substring, cast to float
    sports_clean = sports.copy()
    for col in numeric_cols:
        if col not in sports_clean.columns:
            continue

        sports_clean[col] = (
            sports_clean[col]
            .astype(str)
            .str.replace(",", "", regex=False)
            .str.extract(r"([0-9.]+)")[0]
        )
        sports_clean[col] = pd.to_numeric(sports_clean[col], errors="coerce")

    # Filter by year range (if Year column exists)
    if "Year" in sports_clean.columns:
        year_mask = (sports_clean["Year"] >= year_min) & (
            sports_clean["Year"] <= year_max
        )
        sports_clean = sports_clean.loc[year_mask].copy()
    else:
        raise ValueError("Sports dataset is missing 'Year' column.")

    # Remove duplicates, prioritizing rows with price data
    # Sort by price (NaN last), then drop duplicates keeping first (with price)
    sports_clean = sports_clean.sort_values(
        by="Price (in USD)",
        ascending=False,
        na_position='last'
    )

    before_dedup = len(sports_clean)
    sports_clean = sports_clean.drop_duplicates(
        subset=["Car Make", "Car Model", "Year"],
        keep='first'
    )
    after_dedup = len(sports_clean)

    if before_dedup > after_dedup:
        print(f"Removed {before_dedup - after_dedup} duplicate cars (kept versions with price data)")

    return sports_clean


def filter_sports_from_epa(epa_df: pd.DataFrame) -> pd.DataFrame:
    """
    Filter out sports cars and luxury performance vehicles from EPA dataset.

    This creates a clean "mainstream vehicles" dataset by removing:
    1. Pure luxury/sports brands (Porsche, Ferrari, Lamborghini, etc.)
    2. Performance models from mixed brands (BMW M-series, Audi R/RS, etc.)
    3. Sports models from mainstream brands (Corvette, Mustang GT, etc.)

    Parameters
    ----------
    epa_df : pd.DataFrame
        EPA dataset with 'Make' and 'Model' columns

    Returns
    -------
    pd.DataFrame
        Filtered EPA dataset containing only mainstream vehicles
    """

    # Sports/Luxury brands to exclude entirely
    sports_brands_full = [
        'Porsche', 'Ferrari', 'Lamborghini', 'McLaren', 'Aston Martin',
        'Bentley', 'Bugatti', 'Maserati', 'Lotus', 'Alfa Romeo',
        'Rolls-Royce', 'Koenigsegg', 'Pagani', 'Alpine', 'Ariel',
        'Spyker', 'TVR', 'Morgan', 'Caterham', 'Pininfarina',
        'Rimac', 'W Motors', 'Ultima',
    ]

    # Performance model keywords (for mixed brands like BMW, Audi, Mercedes)
    performance_keywords = [
        # BMW M models
        'M2', 'M3', 'M4', 'M5', 'M6', 'M8', 'X5 M', 'X6 M', 'X3 M', 'X4 M', 'i8',
        # Audi R/RS/S models
        'R8', 'RS3', 'RS4', 'RS5', 'RS6', 'RS7', 'TT RS', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8',
        'RS e-tron GT',
        # Mercedes AMG
        'AMG GT', 'C63', 'E63', 'S63', 'G63', 'GLE63', 'GLS63', 'CLA45', 'A45', 'SL63', 'SL65',
        'C43', 'E43', 'GLE43', 'GLC43', 'SLS AMG',
        # Lexus performance
        'LC 500', 'RC F', 'GS F', 'IS F',
        # Jaguar performance
        'F-Type', 'F-PACE SVR', 'XE SV', 'XF R',
        # Cadillac V models
        'CTS-V', 'ATS-V', 'CT5-V', 'CT4-V', 'Blackwing',
        # Mainstream sports models
        'Corvette', 'Mustang GT', 'Mustang Shelby', 'Mustang Mach 1', 'GT350', 'GT500',
        'Camaro SS', 'Camaro ZL1', 'Camaro Z28',
        'Challenger Hellcat', 'Challenger SRT', 'Charger Hellcat', 'Charger SRT', 'Viper',
        'GT-R', '370Z', '350Z', '400Z',
        'Supra', 'GR Supra', '86',
        'Type R', 'NSX',
        'WRX STI', 'BRZ',
        'Veloster N',
        'Stinger GT',
    ]

    # Start with full dataset
    df_filtered = epa_df.copy()

    # Filter out pure sports/luxury brands
    if 'Make' in df_filtered.columns:
        df_filtered = df_filtered[~df_filtered['Make'].isin(sports_brands_full)]

    # Filter out performance models by keyword matching
    if 'Model' in df_filtered.columns:
        for keyword in performance_keywords:
            df_filtered = df_filtered[~df_filtered['Model'].str.contains(keyword, case=False, na=False)]

    sports_removed = len(epa_df) - len(df_filtered)
    print(f"Filtered out {sports_removed} sports cars from EPA dataset")

    return df_filtered


def save_dataframe(df: pd.DataFrame, path: PathLike) -> None:
    """
    Save a dataframe to CSV, creating parent folders if needed.

    Parameters
    ----------
    df : pd.DataFrame
        Dataframe to save.
    path : str or Path
        Path to output CSV.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)


if __name__ == "__main__":
    """
    Example usage:

    python cleaning.py

    This will clean BOTH the new datasets with HP/MPG data.
    """
    print("="*70)
    print("CLEANING NEW DATASETS WITH HP AND MPG DATA")
    print("="*70)

    # Paths to new datasets
    epa_with_hp_path = Path("../data/raw/all-vehicles-model-with-hp-0-60.csv")
    sports_with_mpg_path = Path("../data/raw/Sport car price with mpg adjusted ENRICHED.csv")

    # Clean EPA dataset with HP (and remove sports cars)
    print("\n1. Cleaning EPA dataset with HP data...")
    epa_clean_with_hp = load_and_clean_epa_with_hp(epa_with_hp_path)
    print(f"   Final mainstream dataset: {len(epa_clean_with_hp)} vehicles")
    print(f"   Columns: {list(epa_clean_with_hp.columns)}")

    # Clean sports dataset with MPG
    print("\n2. Cleaning sports car dataset with MPG data...")
    sports_clean_with_mpg = load_and_clean_sports_with_mpg(sports_with_mpg_path)
    print(f"   Final sports dataset: {len(sports_clean_with_mpg)} sports cars")
    print(f"   Columns: {list(sports_clean_with_mpg.columns)}")

    # Save cleaned datasets
    print("\n3. Saving cleaned datasets...")
    save_dataframe(epa_clean_with_hp, "../data/cleaned/epa_with_hp_clean.csv")
    save_dataframe(sports_clean_with_mpg, "../data/cleaned/sports_with_mpg_clean.csv")

    print("\n" + "="*70)
    print("CLEANING COMPLETE!")
    print("="*70)
    print(f"Saved to:")
    print(f"  - data/cleaned/epa_with_hp_clean.csv ({len(epa_clean_with_hp)} rows)")
    print(f"  - data/cleaned/sports_with_mpg_clean.csv ({len(sports_clean_with_mpg)} rows)")
    print("="*70)
