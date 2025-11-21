"""
aggregates.py

Functions to compute yearly aggregates for the EPA and sports car datasets.
"""

from __future__ import annotations

from pathlib import Path
from typing import Union

import pandas as pd

PathLike = Union[str, Path]


def compute_epa_yearly(epa_clean: pd.DataFrame) -> pd.DataFrame:
    """
    Compute yearly aggregates for the EPA dataset.

    Aggregates (by Year):
    - Combined Mpg For Fuel Type1 (mean)
    - Co2  Tailpipe For Fuel Type1 (mean)
    - Engine displacement (mean)

    Parameters
    ----------
    epa_clean : pd.DataFrame
        Cleaned EPA dataframe (output of load_and_clean_epa).

    Returns
    -------
    pd.DataFrame
        Dataframe with one row per year and mean values of key metrics.
    """
    required_cols = [
        "Year",
        "Combined Mpg For Fuel Type1",
        "Co2  Tailpipe For Fuel Type1",
        "Engine displacement",
    ]

    missing = [c for c in required_cols if c not in epa_clean.columns]
    if missing:
        raise ValueError(f"EPA dataframe is missing required columns: {missing}")

    epa_yearly = (
        epa_clean.groupby("Year")[
            [
                "Combined Mpg For Fuel Type1",
                "Co2  Tailpipe For Fuel Type1",
                "Engine displacement",
            ]
        ]
        .mean()
        .reset_index()
        .sort_values("Year")
    )

    return epa_yearly


def compute_sports_yearly(sports_clean: pd.DataFrame) -> pd.DataFrame:
    """
    Compute yearly aggregates for the sports car dataset.

    Aggregates (by Year):
    - Engine Size (L) (mean)
    - Horsepower (mean)
    - Torque (lb-ft) (mean)
    - 0-60 MPH Time (seconds) (mean)
    - Price (in USD) (mean)

    Parameters
    ----------
    sports_clean : pd.DataFrame
        Cleaned sports dataframe (output of load_and_clean_sports).

    Returns
    -------
    pd.DataFrame
        Dataframe with one row per year and mean values of key metrics.
    """
    required_cols = [
        "Year",
        "Engine Size (L)",
        "Horsepower",
        "Torque (lb-ft)",
        "0-60 MPH Time (seconds)",
        "Price (in USD)",
    ]

    missing = [c for c in required_cols if c not in sports_clean.columns]
    if missing:
        raise ValueError(f"Sports dataframe is missing required columns: {missing}")

    sports_yearly = (
        sports_clean.groupby("Year")[
            [
                "Engine Size (L)",
                "Horsepower",
                "Torque (lb-ft)",
                "0-60 MPH Time (seconds)",
                "Price (in USD)",
            ]
        ]
        .mean()
        .reset_index()
        .sort_values("Year")
    )

    return sports_yearly


def save_dataframe(df: pd.DataFrame, path: PathLike) -> None:
    """
    Save a dataframe to CSV, creating parent folders if needed.
    (Duplicated here for convenience; you can also import from cleaning.py.)

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

    python -m src.aggregates
    (Assumes you already created data/processed/epa_clean.csv and sports_clean.csv)
    """
    epa_clean_path = Path("data/processed/epa_clean.csv")
    sports_clean_path = Path("data/processed/sports_clean.csv")

    epa_clean = pd.read_csv(epa_clean_path)
    sports_clean = pd.read_csv(sports_clean_path)

    epa_yearly = compute_epa_yearly(epa_clean)
    sports_yearly = compute_sports_yearly(sports_clean)

    save_dataframe(epa_yearly, "data/processed/epa_yearly_aggregates.csv")
    save_dataframe(sports_yearly, "data/processed/sports_yearly_aggregates.csv")
