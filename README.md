# Sports Cars vs Mainstream Vehicles: A Story of Convergence

## Quick Start

### How to Run This Project

**1. Install Dependencies**
```bash
pip install -r env/requirements.txt
```

Or install individually:
```bash
pip install pandas numpy matplotlib pyqt5 scikit-learn
```

**2. Run the Dashboard**
```bash
cd src
python dashboard_app.py
```

A window will open with three interactive tabs: **Act 1**, **Act 2**, and **Act 3**.

### Code Structure

The main plotting and analysis code is located in:
- **`src/plots_sports.py`** - Sports car visualizations (Act 1)
- **`src/plots_epa.py`** - EPA vehicle visualizations (Acts 1-2)
- **`src/plots_act3.py`** - Advanced analytics: PCA, clustering, convergence metrics
- **`src/dashboard_app.py`** - Main application and UI
- **`src/cleaning.py`** - Data loading and preprocessing
- **`src/aggregates.py`** - Statistical computations and aggregations

## Overview

This interactive dashboard explores a fascinating question: **Are sports cars and everyday vehicles becoming more similar, or do they remain fundamentally different?**

From 2011 to 2024, we analyze nearly 28,000 vehicles across two markets:
- **Sports Cars**: 2,849 high-performance vehicles (Ferrari, Porsche, Lamborghini, etc.)
- **EPA Vehicles**: 25,078 mainstream cars tracked by the Environmental Protection Agency

The story unfolds in three acts, each revealing a different piece of the puzzle.

## The Story: Three Acts

### Act 1: Diverging Priorities (2011-2024)

**What This Act Shows**: Sports cars and mainstream vehicles have **opposite goals**.

#### Chart 1A: Sports Car Trends
**What you see**: Three lines showing how sports cars evolved over time
- **Red line (Horsepower)**: Power increased steadily
- **Orange line (Engine Size)**: Stayed relatively stable
- **Green line (Price)**: Luxury prices climbed

**Key insight**: Sports cars focused on **performance and luxury**.

#### Chart 1B: EPA Vehicle Trends
**What you see**: Three lines showing mainstream vehicle evolution
- **Blue line (MPG)**: Fuel economy improved gradually
- **Orange line (CO2 Emissions)**: Emissions decreased
- **Green line (Engine Size)**: Engines got smaller ("downsizing")

**Key insight**: Mainstream cars focused on **efficiency and environment**.

#### Chart 1C: The Divergence
**What you see**: A slope chart showing how metrics changed from start to end of your selected time range
- **Green slopes** = Sports car metrics (going up = more performance)
- **Red slopes** = EPA metrics (going up = more efficient)

**Key insight**: The slopes move in **opposite directions**. Sports cars got faster and more expensive. Mainstream cars got cleaner and more efficient. They were moving apart, not together.

### Act 2: The Electrification Revolution (2013-2024)

**What This Act Shows**: Electric vehicles **changed the game** by breaking the old rules.

In the gasoline era, you had to choose: power OR efficiency. You couldn't have both. Electric vehicles demolished this tradeoff.

#### Chart 2A: The Market Shift
**What you see**: A stacked area chart showing fuel type market share
- **Blue area (Gas)**: Traditional gasoline vehicles
- **Green area (Electric)**: Electric + hybrid vehicles

**Timeline**:
- **2013-2015**: Gas dominates 85-90% of the market
- **2016-2018**: The turning point - EVs start climbing
- **2019-2024**: EVs reach 15-20% market share

**Key insight**: The automotive market fundamentally transformed in just 10 years.

#### Chart 2B: Breaking the Efficiency Ceiling
**What you see**: A scatter plot with dots representing individual vehicles
- **Blue dots** = Gas vehicles
- **Orange dots** = Hybrids
- **Green dots** = Electric vehicles

**Hover over any dot** to see the exact vehicle (make, model, year, MPG).

**What the patterns reveal**:
- **Gas vehicles (blue)**: Stuck at 20-35 MPG across ALL years. No improvement despite decades of engineering.
- **Hybrids (orange)**: Achieve 40-60 MPG. Better, but still limited.
- **EVs (green)**: Reach 80-140+ MPG equivalent. They don't just improve efficiency - they **redefine what's possible**.

**Key insight**: Gasoline technology hit a wall. Only electrification broke through.

### Act 3: Convergence or Coexistence?

**What This Act Shows**: Are the markets truly merging, or just evolving separately?

This act uses three different analytical approaches to answer the question from multiple angles.

#### Chart 3A: Performance & Efficiency Over Time
**What you see**: Two side-by-side charts showing how different vehicle types evolved

**Left Panel - Performance (Horsepower)**:
- **Blue line (Gas)**: Slight increase (~5-10%)
- **Red line (Sports)**: Stays strong, some volatility
- **Green line (EVs)**: MASSIVE growth (120%+ by 2024)

**Right Panel - Efficiency (MPG)**:
- **Blue line (Gas)**: Slow improvement (~15%)
- **Red line (Sports)**: Volatile, slightly declining
- **Green line (EVs)**: Starts high, keeps climbing

**Key insight**: This is **one-sided convergence**. EVs are moving toward sports-level performance. But sports cars are NOT moving toward EV efficiency. Only one market is adapting.

#### Chart 3B: Market Clustering - Do They Group Together?
**What you see**: A scatter plot where clustering algorithms identify natural vehicle groups

**How to read this chart**:
- **Colors (blue, orange, green)** = Natural groups discovered by the algorithm
  - These groups share similar characteristics (power, efficiency, engine size)
  - The algorithm doesn't know which market a car comes from
- **Shapes** = Original market
  - **Circles** = EPA mainstream vehicles
  - **Squares** = Sports cars
- **X marks** = Centers of each group

**What does convergence look like?**
- **Convergence**: You'd see blue circles AND blue squares in the same cluster (mixed shapes, same color)
- **Coexistence**: Sports cars mostly in one cluster color, EPA vehicles in other colors

**For example**:
- If the **green cluster** has mostly squares and the **blue cluster** has mostly circles, the markets are still distinct
- If you see squares and circles evenly distributed across all colors, the markets are merging

**Technical note**: This uses PCA (Principal Component Analysis) to reduce complex 3D data (horsepower, MPG, engine size) into a 2D view you can see. PC1 and PC2 are the two most important dimensions that capture the most variation.

**Key insight**: Look for mixing. If sports and EPA vehicles appear in the same clusters, convergence is happening. If they cluster separately, coexistence remains.

#### Chart 3C: The Convergence Score - A Single Number
**What you see**: A line chart tracking a convergence score from 2011 to 2024

**How the score works**:
- **Score = 100**: Markets are as different as they were in 2011 (baseline)
- **Score < 100**: Markets are becoming MORE similar
- **Score > 100**: Markets are becoming MORE different

**How it's calculated**:
1. Each year, we measure how different the average sports car is from the average EPA car
2. We look at horsepower difference AND MPG difference
3. We normalize to 2011 = 100
4. The overall score is the average of both metrics

**Key insight**: This gives you a definitive, quantitative answer. Is the line going down? Then yes, convergence is happening. Is it flat or going up? Then no, the markets remain distinct.

## Using the Control Panel

The left sidebar controls all visualizations. Here's what each control does:

### Year Range
- **Min/Max**: Select the time period to analyze
- The charts automatically update to show only that range
- Useful for focusing on specific eras (e.g., "electrification era" 2016-2024)

### Sports Car Options
- **Show Sports Lines**: Toggle sports car data on/off
- **Brand Filter**: View specific brands (Porsche, Ferrari, etc.) or all brands
- **Normalize to base year**: Makes the first year = 100 so you can compare percentage changes

### EPA Options
- **Show EPA Lines**: Toggle EPA data on/off
- **Fuel Type Checkboxes**:
  - **Gasoline**: Include all gas-powered vehicles
  - **Electric**: Include EVs and hybrids
- **Show only Electric**: Filter to see just EVs/hybrids
- **Use % share**: For fuel charts, show percentages instead of raw counts

### Act 3 Specific Controls
- **Number of Clusters (K)**: Choose 3, 4, or 5 clusters for Chart 3B
  - More clusters = finer segmentation
  - Fewer clusters = broader categories
- **Market filter**: Show both markets, sports only, or EPA only