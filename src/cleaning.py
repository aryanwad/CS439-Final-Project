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
    epa = pd.read_csv(path, sep=";", low_memory=False)

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
    sports = pd.read_csv(path, low_memory=False)

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

    python -m src.cleaning
    """
    # Adjust these paths to match your repo structure
    epa_raw_path = Path("data/raw/all-vehicles-model.csv")
    sports_raw_path = Path("data/raw/Sport car price.csv")

    epa_clean = load_and_clean_epa(epa_raw_path)
    sports_clean = load_and_clean_sports(sports_raw_path)

    save_dataframe(epa_clean, "data/processed/epa_clean.csv")
    save_dataframe(sports_clean, "data/processed/sports_clean.csv")
