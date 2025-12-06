"""
enrich_sports_dataset.py

Extract sports cars from EPA dataset and merge with existing sports dataset
to increase coverage in 2013-2020 years.
"""

import pandas as pd
from pathlib import Path

# Load raw datasets
print("Loading datasets...")
epa = pd.read_csv("../data/raw/all-vehicles-model-with-hp-0-60.csv", sep=";", low_memory=False)
sports = pd.read_csv("../data/raw/Sport car price with mpg adjusted.csv", low_memory=False)

print(f"EPA dataset: {len(epa)} vehicles")
print(f"Sports dataset: {len(sports)} vehicles")

# Sports/Luxury brands to extract
sports_brands_full = [
    'Porsche', 'Ferrari', 'Lamborghini', 'McLaren', 'Aston Martin',
    'Bentley', 'Bugatti', 'Maserati', 'Lotus', 'Alfa Romeo',
    'Rolls-Royce', 'Koenigsegg', 'Pagani', 'Alpine', 'Ariel',
    'Spyker', 'TVR', 'Morgan', 'Caterham', 'Pininfarina',
    'Rimac', 'W Motors', 'Ultima',
]

# Performance model keywords
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

print("\nExtracting sports cars from EPA dataset...")

# Extract sports cars by brand
sports_from_epa = epa[epa['Make'].isin(sports_brands_full)].copy()

# Extract sports cars by model keyword
for keyword in performance_keywords:
    keyword_matches = epa[epa['Model'].str.contains(keyword, case=False, na=False)].copy()
    sports_from_epa = pd.concat([sports_from_epa, keyword_matches], ignore_index=True)

# Remove duplicates
sports_from_epa = sports_from_epa.drop_duplicates(subset=['Make', 'Model', 'Year'])

print(f"Extracted {len(sports_from_epa)} sports cars from EPA dataset")

# Map EPA columns to sports dataset columns
epa_sports_mapped = pd.DataFrame({
    'Car Make': sports_from_epa['Make'],
    'Car Model': sports_from_epa['Model'],
    'Year': sports_from_epa['Year'],
    'Engine Size (L)': sports_from_epa['Engine displacement'],
    'Horsepower': sports_from_epa['Horsepower (est)'],
    'Torque (lb-ft)': pd.NA,  # Not available in EPA dataset
    '0-60 MPH Time (seconds)': sports_from_epa['0-60 time (est)'],
    'Price (in USD)': pd.NA,  # Not available in EPA dataset
    'MPG': sports_from_epa['Combined Mpg For Fuel Type1'],
})

print(f"\nMapped columns:")
print(f"  - Car Make/Model: {epa_sports_mapped['Car Make'].notna().sum()} values")
print(f"  - Year: {epa_sports_mapped['Year'].notna().sum()} values")
print(f"  - Horsepower: {epa_sports_mapped['Horsepower'].notna().sum()} values")
print(f"  - MPG: {epa_sports_mapped['MPG'].notna().sum()} values")
print(f"  - Engine Size: {epa_sports_mapped['Engine Size (L)'].notna().sum()} values")
print(f"  - 0-60 Time: {epa_sports_mapped['0-60 MPH Time (seconds)'].notna().sum()} values")

# Combine with existing sports dataset
# IMPORTANT: Only add EPA cars that DON'T already exist in sports dataset
# This preserves price data from original sports cars
print("\nCombining with existing sports dataset...")

# Create a set of (Make, Model, Year) tuples from original sports dataset
sports_keys = set(zip(sports['Car Make'], sports['Car Model'], sports['Year']))

# Filter EPA sports to only include cars NOT in original sports dataset
epa_sports_new = epa_sports_mapped[
    ~epa_sports_mapped.apply(
        lambda row: (row['Car Make'], row['Car Model'], row['Year']) in sports_keys,
        axis=1
    )
].copy()

print(f"EPA sports cars: {len(epa_sports_mapped)}")
print(f"Already in sports dataset: {len(epa_sports_mapped) - len(epa_sports_new)}")
print(f"New EPA cars to add: {len(epa_sports_new)}")

# Combine: original sports (with price) + new EPA cars (without price)
enriched_sports = pd.concat([sports, epa_sports_new], ignore_index=True)

# Convert numeric columns to proper numeric types to avoid CSV parsing issues
numeric_cols_to_convert = ['Engine Size (L)', 'Horsepower', 'Torque (lb-ft)',
                           '0-60 MPH Time (seconds)', 'Price (in USD)', 'MPG']
for col in numeric_cols_to_convert:
    if col in enriched_sports.columns:
        # Remove commas and convert to numeric
        enriched_sports[col] = (
            enriched_sports[col]
            .astype(str)
            .str.replace(',', '', regex=False)
            .str.replace('$', '', regex=False)
            .str.extract(r'([0-9.]+)')[0]
        )
        enriched_sports[col] = pd.to_numeric(enriched_sports[col], errors='coerce')

print(f"\nFinal enriched dataset: {len(enriched_sports)} sports cars")
print(f"Original: {len(sports)}, Added: {len(enriched_sports) - len(sports)}")
print(f"With price (numeric): {enriched_sports['Price (in USD)'].notna().sum()}")

# Show yearly distribution
print("\nYearly distribution:")
yearly_counts = enriched_sports['Year'].value_counts().sort_index()
print(yearly_counts)

# Save enriched dataset (without quoting to avoid CSV parsing issues)
output_path = Path("../data/raw/Sport car price with mpg adjusted ENRICHED.csv")
enriched_sports.to_csv(output_path, index=False, quoting=1)  # QUOTE_MINIMAL

print(f"\n✓ Saved enriched dataset to: {output_path}")
print(f"  Total sports cars: {len(enriched_sports)}")
print(f"  Year range: {enriched_sports['Year'].min()}-{enriched_sports['Year'].max()}")
