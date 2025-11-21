# CS 439 Final Project — Sports vs. Economy Cars: Convergence or Divergence?

## Overview

This repository contains the code, data, and analysis for our CS 439 final project.  
Our central question:

> **Are sports cars and everyday “economy” vehicles converging or diverging in terms of performance, efficiency, and environmental impact over time?**

To explore this, we compare:

- A **sports car performance dataset** (horsepower, torque, 0–60 time, price, etc.)
- The **EPA all-vehicles dataset** (combined MPG, CO₂ emissions, engine displacement, fuel type, etc.)

Our analysis is organized as a three-act “story” about how different segments of the automotive market have evolved.

---

## Team

- **Aryan** – EPA dataset loading/validation, annual aggregates, backend cleaning scripts  
- **Jiin** – Sports car dataset cleaning, pricing and performance metrics  
- **Nylea** – Narrative framing, visualization storyboard, presentation flow

---

## Repository Structure

```text
cs439-final-project/
│
├── data/
│   ├── raw/
│   │   ├── all-vehicles-model.csv       # Original EPA data
│   │   ├── Sport car price.csv          # Original sports car data
│   ├── processed/
│       ├── epa_clean.csv                # Cleaned EPA subset (2000–2024)
│       ├── sports_clean.csv             # Cleaned sports car data (2014–2023)
│       ├── epa_yearly_aggregates.csv    # Yearly averages for mainstream market
│       ├── sports_yearly_aggregates.csv # Yearly averages for sports cars
│
├── notebooks/
│   ├── 01_exploration_and_cleaning.ipynb
│   ├── 02_annual_aggregates.ipynb
│   ├── 03_visualizations.ipynb
│
├── src/
│   ├── __init__.py
│   ├── cleaning.py      # Functions to clean both datasets
│   ├── aggregates.py    # Functions to compute annual summaries
│   ├── plotting.py      # Functions to generate plots for the report
│
├── reports/
│   ├── CS439_Final_Project_Proposal.pdf
│   ├── CS439_Final_Project_Update.pdf
│   ├── CS439_Final_Project_Report.pdf
│   ├── figures/         # Exported .png/.pdf plots used in the report or slides
│
├── env/
│   ├── requirements.txt  # Python dependencies
│
├── README.md
├── .gitignore
└── LICENSE               # (Optional)
