# Sports Cars vs Mainstream Vehicles: A Story of Convergence

## Overview

This interactive dashboard explores a fascinating question: **Are sports cars and everyday vehicles becoming more similar, or do they remain fundamentally different?**

From 2011 to 2024, we analyze nearly 31,000 vehicles across two markets:
- **Sports Cars**: 2,849 high-performance vehicles (Ferrari, Porsche, Lamborghini, etc.)
- **EPA Vehicles**: 28,000+ mainstream cars tracked by the Environmental Protection Agency

The story unfolds in three acts, each revealing a different piece of the puzzle.

---

## How to Run the Dashboard

### Prerequisites
You need Python 3.8+ with these libraries:
```bash
pip install pandas numpy matplotlib pyqt5 scikit-learn
```

### Launch the Dashboard
```bash
cd src
python dashboard_app.py
```

A window will open with three tabs: **Act 1**, **Act 2**, and **Act 3**.

---

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

---

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

---

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

**Color zones**:
- 🟢 **Green zone (<70)**: Strong convergence - markets are getting very similar
- 🟡 **Yellow zone (70-100)**: Moderate divergence - markets are fairly different
- 🔴 **Red zone (>100)**: High divergence - markets are more different than ever

**How it's calculated**:
1. Each year, we measure how different the average sports car is from the average EPA car
2. We look at horsepower difference AND MPG difference
3. We normalize to 2011 = 100
4. The overall score is the average of both metrics

**Key insight**: This gives you a definitive, quantitative answer. Is the line going down? Then yes, convergence is happening. Is it flat or going up? Then no, the markets remain distinct.

---

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

---

## What the Data Tells Us

### The Bottom Line
After analyzing all three acts and all the data, here's what we found:

**2011-2015: Divergence**
- Sports cars and mainstream vehicles pursued completely opposite goals
- Sports = performance, luxury, power
- EPA = efficiency, emissions, cost

**2016-2020: The Shift**
- Electric vehicles entered the market
- They broke the fundamental tradeoff: you could have power AND efficiency
- Only mainstream manufacturers adopted this technology (in our dataset)

**2021-2024: One-Sided Convergence**
- EPA vehicles (through electrification) gained performance capabilities
- They became more like sports cars in horsepower
- But sports cars did NOT become more like EPA vehicles in efficiency
- The gap narrowed from ONE side only

### So... Convergence or Coexistence?

**The nuanced answer**: It depends on your definition.

**If convergence means "markets becoming similar"**: Yes, partially
- EVs in the EPA market now offer sports-level acceleration
- The performance gap has closed significantly

**If convergence means "both markets moving toward each other"**: No
- Only EPA vehicles are adapting (via electrification)
- Sports cars in this dataset remain combustion-only
- This is asymmetric convergence

**The future**: Our dataset ends in 2024, but the trend suggests:
- If sports cars adopt electrification (Porsche Taycan, etc.), TRUE convergence may occur
- If they don't, the markets will remain fundamentally distinct philosophically, even if their specifications overlap

---

## Interesting Patterns to Explore

### Things to Try in the Dashboard

1. **Set year range to 2011-2015 only**
   - Look at Chart 1C: See the original divergence
   - Check Chart 3C: Score should be near 100

2. **Set year range to 2020-2024 only**
   - Look at Chart 2B: Notice how many green dots appear
   - Check Chart 3A: See EV performance explosion

3. **Compare different cluster counts (K=3 vs K=5)**
   - Notice how market segmentation changes
   - K=3: Broad categories (economy, midsize, performance)
   - K=5: Finer segments (luxury performance, budget economy, etc.)

4. **Filter to "Porsche" brand only**
   - See how a single brand's strategy evolved
   - Compare to EPA trends in the same years

5. **Toggle "Show only Electric" in Act 2**
   - See the hybrid vs pure EV distinction
   - Notice the efficiency differences even within electrification

---

## About the Data

### How We Built the Datasets

Our analysis required two separate but complementary datasets. Here's how we created them:

#### Step 1: Populating the Sports Car Dataset

**The Challenge**: We started with a sports car dataset that had good price data but limited vehicle coverage, especially for years 2013-2020.

**The Solution**: We extracted additional sports cars from the EPA's comprehensive all-vehicles database.

**How we identified sports cars**:
1. **Pure sports/luxury brands** - We extracted every vehicle from brands like:
   - European exotics: Porsche, Ferrari, Lamborghini, McLaren, Aston Martin
   - Luxury manufacturers: Bentley, Bugatti, Maserati, Rolls-Royce
   - Boutique brands: Lotus, Alfa Romeo, Koenigsegg

2. **Performance models from mainstream brands** - We used keyword matching to find:
   - BMW M-series (M3, M4, M5, etc.)
   - Audi R/RS/S models (R8, RS6, S7, etc.)
   - Mercedes-AMG (AMG GT, C63, E63, etc.)
   - American muscle (Corvette, Mustang GT, Camaro SS, Challenger Hellcat, etc.)
   - Japanese sports cars (GT-R, Supra, NSX, WRX STI, etc.)

**The Result**:
- Started with ~1,200 sports cars (mostly with price data)
- Extracted ~1,100 additional sports cars from EPA database
- **Final dataset: 2,849 sports cars covering 2011-2024**

#### Step 2: Cleaning the EPA Dataset

**The Challenge**: The EPA database contains 84,000+ vehicles from 1984-2024, including sports cars. We needed to:
1. Filter to our time period (2011-2024)
2. Remove sports cars to avoid overlap
3. Keep only vehicles with valid fuel economy data

**The Cleaning Process**:
```
Original EPA Dataset: 84,000+ vehicles
↓ Filter to 2011-2024
↓ Keep only vehicles with valid MPG data
↓ Remove sports cars (using the SAME criteria as extraction)
↓ Result: 28,000+ mainstream vehicles
```

**Key Decision**: We kept vehicles from both modern EPA tests AND older test methods. This tripled our dataset size from ~9,000 to ~28,000 vehicles while maintaining data quality.

**The Result**: A clean EPA dataset with NO sports cars and NO overlap with our sports dataset.

#### Step 3: Enriching Missing Price Data

**The Challenge**: Cars extracted from EPA had horsepower and MPG data but NO price information (EPA doesn't track vehicle prices).

**The Solution**: We used the Gemini API to look up MSRP data for the 1,842 cars missing prices.

**The Process**:
1. Export cars without prices (Make, Model, Year)
2. Query Gemini for manufacturer suggested retail prices (MSRP)
3. Parse and clean the price data
4. Update the dataset
5. Repeat until 100% complete (took 5 iterations)

**The Result**: All 2,849 sports cars now have complete data (horsepower, MPG, engine size, 0-60 time, AND price).

### Final Datasets

#### Sports Car Dataset
- **Size**: 2,849 vehicles from 2011-2024
- **Sources**:
  - Original sports car data (with prices)
  - Sports cars extracted from EPA database
  - Prices enriched using Gemini API
- **Coverage**: 100% complete for all metrics
- **Note**: Contains NO electric sports cars. All are gasoline-powered (this is intentional for the analysis).

#### EPA Dataset
- **Size**: 28,000+ vehicles from 2011-2024
- **Source**: U.S. Environmental Protection Agency (official fuel economy database)
- **Processing**: All sports cars removed using the same identification criteria
- **Includes**: Gasoline, diesel, hybrid, and pure electric vehicles
- **Coverage**: Comprehensive mainstream vehicle data

### Data Integrity

**No Overlap**: Every vehicle appears in EITHER the sports dataset OR the EPA dataset, never both. We use identical filtering criteria to ensure clean separation.

**No Duplicates**: Each (Make, Model, Year) combination appears only once per dataset.

**Complete Coverage**: All vehicles have the core metrics needed for analysis (horsepower, MPG, engine size).

### Why These Datasets?

We specifically designed the datasets this way:
- **Sports dataset WITHOUT EVs**: Represents traditional performance philosophy that hasn't adopted electrification
- **EPA dataset WITH EVs**: Captures the electrification revolution in the mainstream market

This creates a natural experiment: one market adapts (EPA adopts EVs), one doesn't (sports stays traditional), allowing us to observe **one-sided convergence**.

---

## Technical Details

### Technologies Used
- **Python 3.8+**: Programming language
- **PyQt5**: Desktop application framework
- **Matplotlib**: All visualizations
- **Pandas**: Data processing
- **Scikit-learn**: Machine learning (PCA, K-Means clustering)

### Visualization Techniques
- **Time series analysis**: Tracking metrics over time
- **Normalization**: Comparing metrics with different units
- **Slope charts**: Showing directional change from start to end
- **Stacked area charts**: Showing composition changes
- **Scatter plots**: Revealing distributions and patterns
- **PCA**: Dimensionality reduction for clustering visualization
- **K-Means clustering**: Unsupervised discovery of market segments

### Academic Context
This project was created for **CS439 - Data Visualization**.

**Learning objectives**:
- Design narrative-driven visualizations
- Implement interactive dashboards
- Apply machine learning to exploratory data analysis
- Communicate insights to non-technical audiences

---

## Frequently Asked Questions

### Q: Why aren't there electric sports cars in your dataset?
A: The sports dataset represents traditional, gasoline-powered performance vehicles through 2024. This was intentional - it allows us to see how the EPA market evolves with electrification while the sports market stays traditional, creating one-sided convergence.

### Q: What does "normalized to base year = 100" mean?
A: It sets the first year's value to 100, then scales all other years proportionally. This lets you compare percentage changes across metrics with different units (like horsepower vs price).

### Q: How do I know if clustering shows convergence?
A: Look for mixed shapes within the same color cluster. If blue circles (EPA) and blue squares (sports) appear together, those vehicles are similar despite coming from different markets.

### Q: Why does the convergence score go up sometimes?
A: A rising score means markets are becoming MORE different. This can happen when one market innovates faster than the other (e.g., EVs gaining performance rapidly while sports cars don't gain efficiency).

### Q: Can I export the data or charts?
A: Currently no, but this would be a good future enhancement. For now, you can take screenshots of the visualizations.

### Q: What's the difference between Act 2's scatter plot and Act 3's cluster plot?
A: The scatter plot (Act 2) shows efficiency over time with fuel type categories. The cluster plot (Act 3) uses machine learning to discover natural groups based on ALL features (HP, MPG, engine size) without pre-defined categories.

---

## Future Work

### Potential Enhancements
1. **Include modern electric sports cars** (Porsche Taycan, Ferrari SF90, etc.)
   - Would show true bilateral convergence
   - Compare to traditional sports cars

2. **Add more metrics**
   - Weight, torque, range (for EVs)
   - Carbon footprint over vehicle lifetime

3. **Statistical significance testing**
   - Is convergence statistically significant?
   - Confidence intervals on trends

4. **Predictive modeling**
   - Forecast where markets will be in 2030
   - Estimate when full convergence might occur

5. **Animation**
   - Show temporal evolution as an animation
   - Watch clusters form and merge over time

---

## Credits

**Data Sources**:
- EPA Fuel Economy Database
- Manufacturer specifications
- Automotive pricing databases
- Gemini API (for price enrichment)

**Developed for**: CS439 - Data Visualization

**Tools**: Python, PyQt5, Matplotlib, Scikit-learn, Pandas

---

## Additional Documentation

For detailed technical documentation, see `CLAUDE_README.md` which includes:
- Complete code architecture
- Algorithm implementations
- Data processing pipelines
- Signal-slot wiring diagrams
- Performance optimizations

---

## Quick Start Guide

1. **Install dependencies**: `pip install pandas numpy matplotlib pyqt5 scikit-learn`
2. **Run dashboard**: `python src/dashboard_app.py`
3. **Navigate tabs**: Click "Act 1", "Act 2", "Act 3" at the top
4. **Explore controls**: Use left sidebar to filter and adjust visualizations
5. **Read narratives**: Each chart tells part of the story
6. **Experiment**: Try different year ranges, brands, and cluster counts

**Pro tip**: Start with Act 1 to understand the baseline, then progress through Acts 2 and 3 to see how the story evolves.

---

## The Takeaway

In 2011, sports cars and mainstream vehicles were moving in opposite directions - one toward performance, one toward efficiency. By 2024, electric technology allowed EPA vehicles to achieve both. This created one-sided convergence: mainstream cars became more like sports cars, but not vice versa.

Whether you call this "convergence" or "coexistence" depends on your perspective. The markets are closer than they were, but the fundamental philosophies remain distinct. True convergence requires both markets to meet in the middle - and in our data, only one market is moving.

**The future is electric. The question is: will sports cars join the movement, or remain proudly distinct?**
