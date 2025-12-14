# Final Project Report: Automotive Market Convergence Analysis
## Sports Cars vs. Mainstream Vehicles (2011-2024)

**Course**: CS439 - Data Visualization
**Project Duration**: 6 weeks
**Date**: December 2025

---

## 1. Presentation of the Data

### Data Sources and Discovery

Our project leverages two complementary datasets that together provide a comprehensive view of the automotive market over a 13-year period (2011-2024):

**Sports Car Dataset** (`sports_with_mpg_clean.csv`): We initially sourced a sports car pricing database from Kaggle containing approximately 1,200 vehicles. However, we quickly identified significant coverage gaps, particularly in the 2013-2020 period. To address this limitation, we extracted an additional 1,600+ sports cars from the EPA's comprehensive all-vehicles database using a systematic approach. We defined 54 brand/model keywords targeting pure sports brands (Ferrari, Lamborghini, Porsche, McLaren, Maserati, Aston Martin, etc.) and performance variants from mainstream manufacturers (BMW M-series, Mercedes-AMG, Audi R/RS/S, Corvette, GT-R, etc.). After deduplication by (Make, Model, Year), our final sports dataset contains 2,849 vehicles with complete metrics including horsepower, MPG, engine displacement, 0-60 time, and price.

**EPA Mainstream Dataset** (`epa_with_hp_clean.csv`): The Environmental Protection Agency's Fuel Economy Database provided our second dataset, originally containing 84,000+ vehicles spanning 1984-2024. We filtered this to our target period (2011-2024) and systematically removed all sports cars using the identical 54 brand/model keywords to prevent overlap between datasets. This cleaning process yielded 25,078 mainstream vehicles representing the broader automotive market, including gasoline, diesel, hybrid, and electric powertrains. The dataset includes manufacturers like Honda, Toyota, Ford, Chevrolet, Tesla, and hundreds of others.

### What Made This Dataset Interesting

The automotive industry is experiencing its most significant transformation since the invention of the combustion engine. Electric vehicles are disrupting fundamental assumptions about the performance-efficiency tradeoff. In 2011, achieving 450 horsepower required purchasing a $90,000 Porsche 911. By 2024, a $50,000 Tesla Model S offers 670 horsepower AND achieves 103 MPGe - a combination that traditional gasoline technology cannot match. This apparent violation of physics (high power AND high efficiency) suggested a dramatic market shift worth investigating.

We were particularly intrigued by the philosophical divide between sports cars and mainstream vehicles. Sports cars prioritize performance, acceleration, and driving experience, often at the expense of fuel economy. Mainstream vehicles prioritize efficiency, emissions reduction, and affordability. For decades, these represented distinct markets with different engineering goals. However, the emergence of EVs promised to break this. Our dataset allowed us to rigorously test whether this convergence was actually occurring.

### Research Questions Identified

Through exploratory analysis of our datasets, we formulated three central research questions corresponding to different phases of automotive evolution:

**Question 1 - Divergence Era (2011-2020)**: Did sports cars and mainstream vehicles move in opposite directions during the pre-electric era? We hypothesized that sports cars would show increasing horsepower and prices while maintaining stable (low) fuel economy, whereas EPA vehicles would demonstrate improving MPG and declining emissions while maintaining modest power outputs.

**Question 2 - Electrification Impact (2016-2024)**: How did electric vehicles fundamentally change the market landscape? We hypothesized that EVs would break the traditional performance-efficiency tradeoff, achieving both high horsepower and high MPG equivalent ratings, creating a new category that challenged historical market segmentation.

**Question 3 - Market Convergence (2023-2024)**: Are the two markets converging, and if so, is the convergence bilateral or one-sided? We hypothesized that convergence would be one-sided - EPA vehicles would gain performance through electrification, but sports cars would resist adopting efficiency-focused technologies to preserve brand identity.

## 2. Goals and Objectives

### Original Project Goals (From Proposal)

Our initial proposal outlined five primary objectives:

1. **Data Integration and Enrichment**: Merge sports car pricing data with EPA fuel economy data, fill missing values through API enrichment, and create a dataset with complete coverage of both markets.

2. **Three-Act Narrative Visualization**: Design an interactive dashboard using PyQt5 that tells a coherent story through three progressive acts: (1) Diverging Priorities, (2) Electrification Revolution, and (3) Convergence Analysis.

3. **Advanced Analytics Implementation**: Apply machine learning techniques including PCA (Principal Component Analysis) for dimensionality reduction and K-Means clustering to discover natural market segments without predefined categories.

4. **Interactive Exploration Tools**: Implement dynamic filters, year range selectors, fuel type toggles, and cluster controls to enable users to explore different time periods, manufacturers, and market segments.

5. **Quantitative Convergence Metrics**: Develop mathematical measures to objectively quantify market convergence over time, moving beyond visual interpretation to defensible numerical evidence.

## 3. Design and Implementation

### Overall Design Philosophy

We adopted a **narrative-driven visualization approach**. Rather than presenting a collection of disconnected charts, we structured the dashboard as a three-act story with setup, conflict, and resolution:

- **Act 1** establishes the baseline: markets are different and moving apart
- **Act 2** introduces the disruption: electric vehicles break traditional rules
- **Act 3** resolves the question: are markets converging, and how?

This structure guides users through increasing levels of analytical sophistication, building context before introducing advanced techniques like PCA and clustering.

### Chart Type Justifications

**Act 1 - Line Charts and Slope Charts**:
We chose line charts for  trend analysis because they excel at showing change over time, which is the fundamental question in Act 1. Users can track how horsepower, price, and MPG evolved across 13 years for both markets. The normalization toggle (base year = 100) allows direct comparison of metrics with different units - for example, comparing 20% price increase against 15% horsepower increase on the same scale.

The slope chart in Chart 1C provides a complementary perspective: instead of showing every year, it displays only the start and end points with lines connecting them. This design choice emphasizes the direction of change rather than year-by-year fluctuations. Divergent slopes moving away from each other provide immediate visual evidence of markets pursuing opposite goals.

We rejected bar charts for trends because 13 years of data creates visual clutter, and stacked bar charts would obscure individual metric trajectories.

**Act 2 - Stacked Area Chart and Scatter Plot**:
The stacked area chart for fuel type market share was chosen to show composition changes over time. This chart type excels at revealing how the total market (100%) is divided between gasoline, hybrid, and electric vehicles. The sequential color scheme (blue for gas, orange for hybrid, green for electric) follows the progression of energy technology: fossil fuels, transition technology, and clean energy.

The efficiency scatter plot allows us to plot all 25,078+ EPA vehicles simultaneously while preserving individual vehicle identity. Each dot represents a specific car, and hovering reveals its exact specifications. This chart makes visible a critical insight: gasoline vehicles form a horizontal band at 20-35 MPG across all years (a ceiling imposed by thermodynamic limits), while electric vehicles break through this ceiling to 80-140+ MPGe. This pattern would be invisible in aggregated visualizations like box plots or bar charts.

**Act 3 - PCA Scatter with Clustering and Convergence Metrics**:
The clustering visualization posed a significant design challenge: how do you visualize 3-dimensional data (horsepower, MPG, engine displacement) in 2D while revealing market segments? We applied PCA to project the data onto the two principal components that capture 83.7% of total variance. This technique preserves most of the data's structure while making it visualizable.

We used a dual-encoding strategy: **shapes** encode the original market (circles for EPA, squares for sports cars), while **colors** encode the discovered clusters from K-Means algorithm. This allows users to see both the ground truth (what market a car comes from) and the algorithmic categorization (what cluster it belongs to) simultaneously. Convergence is visible when shapes mix within color clusters - when EPA circles and sports squares occupy the same cluster, they are statistically similar despite coming from different markets.

The convergence score chart (Chart 3C) translates complex multidimensional data into a single interpretable metric. By indexing to 2011 = 100, users can immediately see whether markets are more similar (score < 100) or more different (score > 100) than the baseline. The color zones (green/yellow/red) provide intuitive interpretation without requiring statistical knowledge.

### Color Scheme Rationale

We applied **semantic color mapping** throughout the dashboard to build consistent mental models:

- **Warm colors (red, orange)** for sports car metrics: These colors culturally associate with heat, speed, aggression, and performance - matching the sports car philosophy.
- **Cool colors (blue, green)** for EPA metrics: Blue and green evoke efficiency, environmental consciousness, and calmness - matching the mainstream market's priorities.
- **Sequential energy colors** for fuel types: Blue (gasoline) → Orange (hybrid) → Green (electric) follows the historical progression from fossil fuels to clean energy.
- **Neutral palette for clusters**: We used matplotlib's default tab10 palette for cluster colors to avoid suggesting that certain clusters are "good" or "bad" - the algorithm discovers natural groups without value judgments.

### Implementation Architecture

**Technology Stack**:
- **PyQt5** for the desktop GUI framework, providing native window management and signal-slot event handling
- **Matplotlib** for all visualizations, embedded in Qt canvases for interactive rendering
- **Pandas** for data manipulation, grouping, and aggregation
- **Scikit-learn** for PCA and K-Means clustering algorithms
- **NumPy** for numerical computations and normalization

**Code Organization**:
We modularized the codebase into six primary files:
- `cleaning.py`: Data loading, filtering, deduplication, and validation (598 lines)
- `aggregates.py`: Temporal aggregation, grouping, and statistical computations (312 lines)
- `plots_sports.py`: Sports car visualizations for Act 1 (427 lines)
- `plots_epa.py`: EPA vehicle visualizations for Acts 1 and 2 (553 lines)
- `plots_act3.py`: Advanced analytics including PCA, clustering, and convergence metrics (689 lines)
- `dashboard_app.py`: PyQt5 GUI integration, signal-slot wiring, and event handling (734 lines)

### Key Implementation Details

**Tooltip Positioning Logic**: With 27,927 total data points across both datasets, identifying individual vehicles required intelligent hover tooltips. We implemented adaptive positioning: tooltips appear to the left of the cursor for recent years (2020+) to avoid extending beyond the right edge of the figure, and to the right for earlier years (< 2020) to avoid the left edge. This small detail significantly improved user experience.

**Chart Refresh Optimization**: Initial implementations refreshed all charts on every control change, causing noticeable lag (1-2 seconds). We optimized by tracking which tab is visible and only refreshing charts in the active tab. Charts in hidden tabs refresh when the user switches to them, triggered by the `showEvent` override.

**PCA Normalization**: K-Means clustering is sensitive to feature scales. A vehicle with 500 HP and 20 MPG would be dominated by the horsepower dimension if not normalized. We applied StandardScaler to ensure each feature contributes equally to the clustering algorithm, preventing horsepower from overwhelming the MPG and displacement features.


## 4. Challenges

### Challenge 1: Dataset Coverage Gaps (Week 1-2)

**Problem**: The original sports car dataset contained only 1,200 vehicles with significant gaps in 2013-2020. Many iconic models were missing (e.g., BMW M4 introduced in 2014, several Porsche 911 variants). This created an incomplete picture of the sports market evolution.

**Solution**: We extracted additional sports cars from the EPA database using keyword matching. We defined 54 brands/models (Porsche, Ferrari, BMW M3/M4/M5, Corvette, AMG GT, etc.) and systematically searched the EPA dataset. This required careful deduplication - the same vehicle might appear in both datasets under slightly different names (e.g., "Corvette Z06" vs "Chevrolet Corvette Z06"). We standardized on (Make, Model, Year) tuples and merged records when matches occurred. This expanded our sports dataset from 1,200 to 2,849 vehicles.

**Impact**: This challenge consumed the first two weeks of the project but was essential. Without comprehensive data, our trend analysis would have been unreliable and potentially misleading.

### Challenge 2: Qt Layout and Chart Sizing (Week 4)

**Problem**: Charts initially rendered at fixed sizes (e.g., 8 inches wide × 6 inches tall), leaving empty space in the window or forcing scrollbars. When users resized the window, charts didn't expand to fill available space. This created a poor user experience.

**Solution**: We discovered that Qt layouts calculate available space during the first `showEvent`, not during initialization. We implemented a solution using QTimer to trigger a delayed refresh:

```python
def showEvent(self, event):
    super().showEvent(event)
    QTimer.singleShot(100, self.refresh_charts)  # 100ms delay
```

This 100ms delay allows Qt's layout engine to complete size calculations before Matplotlib attempts to render figures. We also added `stretch` parameters to `QVBoxLayout` and `QHBoxLayout` to ensure charts expand proportionally.

**Impact**: This was a subtle bug that only appeared when testing on different screen sizes and resolutions. It consumed several hours of debugging but significantly improved the professional appearance of the dashboard.

### Challenge 3: Clustering Interpretability (Week 5)

**Problem**: K-Means clustering on 3-dimensional data (HP, MPG, displacement) was difficult to visualize. We initially tried 3D scatter plots, but these were hard to interpret - users couldn't easily see cluster boundaries or understand why vehicles were grouped together.

**Solution**: We applied PCA to reduce dimensionality from 3D to 2D while preserving as much variance as possible. PCA identified that 83.7% of variance could be captured in the first two principal components (PC1 and PC2). We then plotted vehicles on these two axes and colored them by cluster assignment. This made cluster separation visually obvious.

We also added a dual encoding: shapes indicate the original market (circle = EPA, square = sports), while colors indicate discovered clusters. This allows users to see convergence visually - when circles and squares mix within the same color cluster, those vehicles are similar despite different market origins.

**Impact**: This was a design breakthrough. The 3D plots were technically correct but cognitively overwhelming. The PCA transformation sacrificed 16.3% of variance but gained massive interpretability.


## 5. Outcome

### Results Matching Original Objectives

Our final dashboard successfully achieves all five original objectives:

**1. Data Integration and Enrichment** 
We created two clean, comprehensive datasets: 2,849 sports cars and 25,078 EPA vehicles with 100% coverage of key metrics (horsepower, MPG, price, displacement, year). Zero overlap between datasets ensures clean market separation.

**2. Three-Act Narrative Visualization** 
The dashboard implements three progressive acts:
- **Act 1** (Charts 1A, 1B, 1C): Shows diverging priorities through line charts and slope charts
- **Act 2** (Charts 2A, 2B): Reveals electrification impact through stacked area and scatter plots
- **Act 3** (Charts 3A, 3B, 3C): Analyzes convergence using PCA clustering and quantitative metrics

Each act builds on the previous, creating a coherent analytical narrative.

**3. Advanced Analytics Implementation** ✅
We successfully implemented PCA (83.7% variance retention in 2 components) and K-Means clustering (with user-selectable K = 3, 4, or 5) to discover natural market segments. The clustering reveals mixed groups containing both sports and EPA vehicles, providing algorithmic evidence of convergence.

**4. Interactive Exploration Tools** ✅
The dashboard includes:
- Year range sliders (min/max) with dynamic updating
- Brand filtering (Porsche, Ferrari, etc.)
- Fuel type toggles (gasoline, electric, hybrid)
- Normalization options (raw values vs. base year = 100)
- Cluster count controls (K = 3, 4, 5)
- Hover tooltips showing exact vehicle specifications

**5. Quantitative Convergence Metrics** ✅
Chart 3C displays a convergence score (2011 baseline = 100) that objectively quantifies market similarity over time. The score shows dramatic convergence in 2023-2024, with the performance gap dropping 53% in just two years.

### Key Findings

**Finding 1 - Confirmed Divergence (2011-2020)**:
Chart 1C slope chart provides visual proof that markets moved in opposite directions during the 2011-2020 period. Sports car slopes (green) show increasing horsepower (+25%) and prices (+30%) while maintaining stable low MPG (~18). EPA slopes (red) show increasing MPG (+15%), decreasing CO2 emissions (-15%), and shrinking engine displacement (-10%). All lines move away from each other, confirming the hypothesis of divergent market priorities.

**Finding 2 - Electrification Broke the Tradeoff (2016-2024)**:
Chart 2B scatter plot reveals a striking pattern: gasoline vehicles (blue dots) form a horizontal band at 20-35 MPG across all 13 years, representing a thermodynamic ceiling. Electric vehicles (green dots) appear far above this ceiling at 80-140+ MPGe. Chart 2A shows EVs growing from <5% market share in 2016 to 20% in 2024. The combination of high power AND high efficiency - impossible with gasoline technology - fundamentally altered market dynamics.

**Finding 3 - One-Sided Convergence (2023-2024)**:
Chart 3C convergence score drops from 190 in 2021 to 90 in 2024 - a 53% decrease in just three years. This dramatic shift is driven by EPA vehicles gaining performance (average HP increased from 180 to ~250 HP) through electrification, while sports cars maintained their traditional power levels (~450-480 HP). Chart 3B clustering evidence supports this: EPA circles (including Teslas) mix with sports squares in the high-performance cluster.

Critically, this is **asymmetric convergence**: EPA vehicles moved toward sports car performance levels, but sports cars did not adopt EPA-style efficiency. Chart 3A indices show EV performance climbing from 100 to 220+, while sports efficiency remains flat or declining. Sports cars preserved their brand identity by resisting efficiency-focused technologies.

### Visualization Results (Presentation Screenshots)

The following results were presented during our final presentation:

**Act 1 - Divergence Era**:
[Chart 1A] Sports car horsepower increased from ~420 HP (2011) to ~480 HP (2020), while prices climbed from $85,000 to $110,000. MPG remained stagnant at 17-19 MPG throughout.

[Chart 1B] EPA vehicles showed improving fuel economy from 23 MPG (2011) to 27 MPG (2020), while CO2 emissions dropped from 385 g/mi to 330 g/mi. Engine displacement shrank from 3.2L to 2.8L.

[Chart 1C] Slope chart displayed five pairs of diverging lines (HP, Price, MPG, CO2, Displacement), with sports and EPA slopes moving in opposite directions for every metric.

**Act 2 - Electrification Revolution**:
[Chart 2A] Stacked area chart showed gas vehicles declining from 90% (2013) to 70% (2024), while electric/hybrid grew from 10% to 30%.

[Chart 2B] Scatter plot with 25,078 points revealed the gas ceiling at 20-35 MPG (horizontal band of blue dots) and electric breakthrough above 80 MPGe (green dots in the upper region).

**Act 3 - Convergence Analysis**:
[Chart 3A] Dual line charts showed EV performance index rising from 100 (2011) to 220 (2024), while sports efficiency index remained flat at 95-105.

[Chart 3B] PCA scatter with K=4 clusters displayed mixed clusters where EPA circles and sports squares coexisted, particularly in the high-performance cluster (green color, upper right quadrant).

[Chart 3C] Convergence score line dropped from 100 (2011 baseline) to 88 (2024), crossing into the green "strong convergence" zone for the first time in 2023.

### Unexpected Discoveries

**Surprise 1 - Convergence Delay (2021-2022 Spike)**:
We expected monotonic convergence starting in 2016 when EVs emerged. Instead, Chart 3C shows a divergence SPIKE in 2021-2022 (score increased to 190) before the dramatic drop in 2023-2024. Investigation revealed this was due to early EVs being economy-focused models (Nissan Leaf, Chevy Bolt) with modest power outputs. High-performance EVs (Tesla Plaid, Lucid Air) didn't enter the market until 2022-2023, causing a lag before convergence accelerated.

**Surprise 2 - Gasoline Technology Plateau**:
We anticipated gradual MPG improvements for gasoline vehicles throughout 2011-2024 due to engineering advances (direct injection, turbocharging, cylinder deactivation). Chart 2B revealed gasoline vehicles made essentially ZERO efficiency progress - they remained locked at 20-35 MPG across all 13 years. This suggests gasoline internal combustion engines hit fundamental thermodynamic limits around 2011, and only alternative powertrains (hybrid, electric) could push efficiency further.

**Surprise 3 - Sports Car Resistance to Electrification**:
We initially hypothesized that sports car manufacturers would adopt electric powertrains to combine performance with efficiency. Our data showed this did NOT occur in the 2011-2024 timeframe (with rare exceptions like Porsche Taycan launched in 2020). Sports cars in our dataset remained 100% gasoline-powered, suggesting brand identity and customer expectations created barriers to electrification. Luxury performance brands prioritize engine sound, driving feel, and heritage over efficiency gains.