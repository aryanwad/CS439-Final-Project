# Dashboard Implementation Documentation

## Table of Contents
1. [Sidebar Control Panel](#sidebar-control-panel)
2. [Act 1: Diverging Priorities](#act-1-diverging-priorities)
3. [Act 2: Electrification](#act-2-electrification)
4. [Visualization Details](#visualization-details)

---

## Sidebar Control Panel

The left sidebar is a universal control panel that provides interactive filtering and configuration options for all visualizations across the dashboard. It is designed to be compact (250px width) and contains several grouped sections.

### Components

#### 1. Year Range Controls
- **Type**: Spin boxes (numeric input)
- **Purpose**: Sets the time period for all visualizations
- **Range**: 2011-2024
- **Default**: Min=2011, Max=2024
- **Features**:
  - Min and Max spinners
  - Automatic validation ensures Min ≤ Max
  - Changes apply to all charts immediately

#### 2. Sports Car Options
- **Show Sports Lines**: Checkbox to toggle visibility of sports car metrics on trendline charts
- **Brand Filter**: Dropdown menu to filter sports car data by manufacturer
  - Options: All Brands, Porsche, Ferrari, Lamborghini, McLaren, Audi, BMW
  - Affects sports-specific charts and comparison charts
- **Normalize to base year**: Checkbox to enable index normalization (base year = 100)
  - When enabled, all metrics are scaled relative to their first year value
  - Makes it easier to compare metrics with different units

#### 3. EPA / Fuel Type Options
- **Show EPA Lines**: Checkbox to toggle visibility of EPA vehicle metrics on trendline charts
- **Fuel Type Filters**: Two checkboxes for filtering by fuel type category
  - **Gasoline**: Includes Regular, Premium, Midgrade, Diesel, E85, CNG
  - **Electric**: Includes pure Electric, Hybrid (Gas+Electricity), Plug-in Hybrid
  - Both checked by default to show all vehicle types
- **Show only Electric**: Checkbox to filter scatter plots to show only electrified vehicles
- **Use % share**: Toggle between raw vehicle counts and percentage share for market share charts

#### 4. Indices & Clustering (Act 3)
*Note: Act 3 is planned but not yet implemented*
- **Index Toggles**: Four checkboxes for enabling/disabling composite indices
  - Sports Performance Index
  - EPA Performance Index
  - EPA Efficiency Index
  - Sports Efficiency Proxy
- **Clusters (K)**: Dropdown to select number of clusters (3, 4, or 5) for K-means clustering
- **Market Filter**: Dropdown to filter visualization by market segment
  - Options: Both, Sports only, EPA only

#### 5. Action Buttons
- **Apply Filters**: Button to manually trigger filter application (currently auto-applies)
- **Reset**: Button to reset all controls to default values

---

## Act 1: Diverging Priorities

### Overview
Act 1 establishes the central tension of the narrative: sports cars and EPA vehicles have fundamentally different priorities that have been diverging over time. Sports cars optimize for performance (horsepower, engine size, acceleration), while EPA vehicles optimize for efficiency (fuel economy, lower emissions, smaller engines).

### User Takeaway
**"Performance and efficiency have been on opposite trajectories—are they fundamentally incompatible?"**

Users should understand that:
1. Sports cars are getting more powerful with larger engines
2. EPA vehicles are becoming more efficient with smaller engines
3. These markets have historically moved in opposite directions
4. This sets up the question: Can electrification bridge this gap? (answered in Act 2)

### Layout
- **Top Row**: Two side-by-side charts (1A: Sports Trendlines, 1B: EPA Trendlines)
- **Bottom Row**: One full-width comparison chart (1C: Slope Chart)

---

## Act 2: Electrification

### Overview
Act 2 explores whether electrification (EVs and hybrids) can break the traditional tradeoff between performance and efficiency. It shows the rapid growth of electric vehicles in the market and demonstrates that EVs achieve both high efficiency (high MPG) without sacrificing environmental performance.

### User Takeaway
**"Electric vehicles are disrupting the old performance vs. efficiency tradeoff"**

Users should understand that:
1. The market is rapidly transitioning from gasoline to electric/hybrid vehicles
2. Electric vehicles achieve unprecedented efficiency levels (100+ MPG equivalent)
3. EVs break the historical constraint that high performance meant low efficiency
4. This transition is accelerating, especially after 2020

### Layout
- **Top Row**: Two side-by-side charts (2A: Fuel Type Market Share, 2B: Efficiency Evolution Scatter)
- **Bottom Row**: Narrative text placeholder (future expansion)

---

## Visualization Details

### Visualization 1A: Sports Car Trendlines

**Type**: Multi-line time series chart

**Purpose**: Show how sports car characteristics have evolved over time

**Data Source**: Sports car dataset (`sports_clean.csv`)

**Chart Components**:

1. **X-Axis**: Year (2011-2024 by default)
2. **Y-Axis**:
   - Non-normalized: "Value (units vary by line)"
   - Normalized: "Index (base year = 100)"
3. **Lines** (3 metrics, can be toggled):
   - **Horsepower** (Red #d62728): Average horsepower across all sports cars
   - **Engine Size** (Orange #ff7f0e): Average engine displacement in liters
   - **Price** (Green #2ca02c): Average price in USD
4. **Title**: "Sports Car Trendlines: Performance & Price Over Time"
5. **Legend**: Shows which color represents which metric (top-right)
6. **Grid**: Light gray grid lines (alpha=0.3) for easier reading

**Features**:
- All three lines enabled by default
- Responds to brand filter (can show trends for specific manufacturers)
- Supports normalization to base year = 100
- Updates in real-time when year range changes

**Insights to Convey**:
- Sports cars are maintaining or increasing engine sizes
- Horsepower is generally trending upward
- Prices show variability but overall upward trend
- Performance remains the primary focus

---

### Visualization 1B: EPA Trendlines

**Type**: Multi-line time series chart

**Purpose**: Show how EPA vehicle characteristics have evolved over time

**Data Source**: EPA dataset (`epa_clean.csv`)

**Chart Components**:

1. **X-Axis**: Year (2011-2024 by default)
2. **Y-Axis**:
   - Non-normalized: "Value (units vary by line)"
   - Normalized: "Index (base year = 100)"
3. **Lines** (3 metrics, can be toggled):
   - **Combined MPG** (Blue): Average fuel efficiency
   - **Tailpipe CO₂** (Orange): Average emissions in g/mi
   - **Engine Displacement** (Green): Average engine size in liters
4. **Title**: "EPA Trendlines: Efficiency & Engine Size Over Time"
5. **Legend**: Shows which color represents which metric (top-right)
6. **Grid**: Light gray grid lines (alpha=0.3)

**Features**:
- All three lines enabled by default
- Responds to fuel type filters (can show gas-only, electric-only, or both)
- Supports normalization to base year = 100
- Updates in real-time when controls change

**Insights to Convey**:
- MPG is increasing (vehicles becoming more efficient)
- CO₂ emissions are decreasing (better environmental performance)
- Engine displacement is decreasing (downsizing trend)
- Efficiency is the primary focus, opposite of sports cars

---

### Visualization 1C: Diverging Priorities Slope Chart

**Type**: Slope chart (start-to-end comparison)

**Purpose**: Directly compare how sports and EPA metrics changed from start year to end year, highlighting the divergence in priorities

**Data Sources**: Both sports car and EPA datasets

**Chart Components**:

1. **X-Axis**: Two points - Start Year (left) and End Year (right)
2. **Y-Axis**: Hidden (not meaningful for normalized comparison)
   - All metrics normalized to start year = 100
3. **Slope Lines** (6 total):

   **Sports Cars (Green #2ca02c)**:
   - **Engine Size**: Liters - shows if engines are getting larger/smaller
   - **Horsepower**: Raw HP - shows power trend
   - **Acceleration (0-60) (inverted)**: Lower is better, so inverted to show improvement as upward

   **EPA Vehicles (Red #d62728)**:
   - **Engine Size**: Displacement in liters - shows downsizing trend
   - **Efficiency (MPG)**: Combined MPG - shows fuel economy improvement
   - **Emissions (CO₂) (inverted)**: Lower is better, so inverted to show improvement as upward

4. **Value Labels**:
   - Left side: Start year value (always 100)
   - Right side: End year value (percentage change from start)
   - Far right: Metric names

5. **Title**: "Diverging Priorities: Performance vs. Efficiency"
   - Subtitle: "(Normalized: Start Year = 100, Higher = Better)"

6. **Legend**: Color-coded patches
   - Green: "Sports Cars (Performance)"
   - Red: "EPA Vehicles (Efficiency)"

7. **Grid**: Vertical dashed lines at start and end years (alpha=0.3)

**Features**:
- All metrics automatically normalized to start = 100
- Inverted metrics (acceleration, emissions) clearly labeled with "(inverted)"
- Unified color scheme makes market segments immediately recognizable
- No prefixes on metric labels since legend clarifies markets
- Responds to all sidebar filters (year range, brand, fuel type)

**Insights to Convey**:
- Sports cars: Lines trending UP show increasing performance (bigger engines, more power, faster acceleration)
- EPA vehicles: Lines trending UP show increasing efficiency (better MPG, lower emissions despite smaller engines)
- The two markets are moving in opposite directions
- Visual divergence emphasizes the fundamental tradeoff
- Sets up Act 2's question: Can this gap be bridged?

---

### Visualization 2A: Fuel Type Market Share Over Time

**Type**: Stacked area chart

**Purpose**: Show the transition from gasoline to electric/hybrid vehicles in the EPA market over time

**Data Source**: EPA dataset (`epa_clean.csv`)

**Chart Components**:

1. **X-Axis**: Year (2013-2024 by default for Act 2)
2. **Y-Axis**:
   - Percentage mode: "Market Share (%)" from 0-100%
   - Count mode: "Number of Vehicle Models"
3. **Stacked Areas**: Fuel types grouped into two color-coded categories

   **Blue (#1f77b4) - Gasoline Types**:
   - Regular, Premium, Midgrade
   - Gasoline or E85, Premium or E85
   - Diesel, CNG, Natural Gas variants

   **Green (#2ca02c) - Electric Types**:
   - Pure Electricity
   - Regular Gas and Electricity (Hybrid)
   - Premium Gas and Electricity
   - All hybrid/plug-in variants

4. **Title**: "Fuel Type Market Share Over Time (EPA Dataset)"
5. **Legend**: Lists all fuel types (upper left)
6. **Grid**: Horizontal grid lines (alpha=0.3) on y-axis only

**Features**:
- Toggle between percentage share and raw counts
- Filter by fuel type category (gas, electric, or both)
- Responds to year range changes
- Colors simplified to two categories for clarity

**Insights to Convey**:
- Clear visual of market transition from blue (gas) to green (electric)
- Acceleration in electric adoption, especially post-2020
- Gasoline vehicles still dominant but declining
- Market is at an inflection point

---

### Visualization 2B: Efficiency Evolution Over Time

**Type**: Scatter plot with color-coded fuel types

**Purpose**: Show that electric vehicles achieve much higher efficiency (MPG) than gasoline vehicles, breaking the old performance-efficiency tradeoff

**Data Source**: EPA dataset (`epa_clean.csv`)

**Chart Components**:

1. **X-Axis**: Year (2013-2024 by default)
2. **Y-Axis**: Combined MPG (fuel efficiency)
   - Starts at 0
   - Auto-scales to data range
3. **Points**: Individual vehicle models, color-coded by fuel type

   **Blue (#1f77b4) - Gasoline Types**:
   - Regular, Premium, Midgrade, Diesel, E85, CNG, Natural Gas
   - Typically 20-60 MPG range

   **Green (#2ca02c) - Electric Types**:
   - Pure Electric, Hybrid, Plug-in Hybrid
   - Often 80-140+ MPG equivalent range

4. **Title**: "Efficiency Evolution Over Time"
5. **Legend**: Lists fuel types present in filtered data (upper left)
6. **Grid**: Grid lines (alpha=0.3) for easier reading
7. **Point Properties**:
   - Size: 25 pixels
   - Alpha: 0.5 (semi-transparent for overlapping points)
   - No edge colors for cleaner look

**Features**:
- Filter by fuel type (gas, electric, or both)
- "Show only Electric" checkbox for focused analysis
- Responds to year range changes
- Hoverable points (future enhancement: could add tooltips with make/model)

**Insights to Convey**:
- Clear visual separation: blue cluster (gas) at bottom, green cluster (electric) at top
- Electric vehicles consistently achieve 2-3x the efficiency of gas vehicles
- EVs "break the ceiling" that limited traditional vehicles
- Efficiency gap is widening over time as EV technology improves
- This breaks the historical tradeoff: you can now have efficiency without sacrificing capability

---

## Technical Notes

### Color Consistency
- **Sports Cars**: Green (#2ca02c) - represents performance/luxury market
- **EPA Vehicles (Gas)**: Blue (#1f77b4) - traditional combustion
- **EPA Vehicles (Electric)**: Green (#2ca02c) - electric/hybrid technology
- **EPA Aggregate**: Red (#d62728) - used in comparison charts

### Normalization
When "Normalize to base year" is enabled:
- Each metric's first value in the selected range = 100
- All subsequent values scaled proportionally
- Formula: `normalized_value = (actual_value / first_value) * 100`
- Makes it easy to compare trends across metrics with different units

### Metric Inversion
Some metrics are inverted so "higher is better" remains consistent:
- **0-60 Time**: Lower seconds = faster = better, so we invert it
- **CO₂ Emissions**: Lower emissions = better, so we invert it
- Clearly labeled with "(inverted)" suffix

### Data Filtering
- **Brand filtering**: Only affects sports car data (1A and 1C sports metrics)
- **Fuel type filtering**: Only affects EPA data (1B, 1C EPA metrics, 2A, 2B)
- **Year range**: Affects all visualizations globally

### Responsive Updates
All visualizations update in real-time when any control changes:
- Year range spinners
- Checkboxes (normalize, fuel types, metric toggles)
- Dropdown selections (brand, clusters)

### Layout Specifications
- Sidebar width: 250px (fixed)
- Chart spacing: 5px between elements
- Figure sizes:
  - Act 1 charts: 6" × 5.5"
  - Act 2 charts: 8" × 5"
- Padding: 2.5 for Act 1 charts, 1.5 for Act 2 charts (prevents label cutoff)

---

## Future Enhancements (Act 3)

*Planned but not yet implemented*

### Visualization 3A: Performance-Efficiency Scatter with Clustering
- K-means clustering on composite indices
- Color-coded by cluster membership
- Interactive tooltips showing make/model/year

### Visualization 3B: Index Comparison Radar Chart
- Multi-axis radar showing 4 composite indices
- Compare sports vs EPA vehicles side-by-side

### Visualization 3C: Convergence Timeline
- Show how cluster centers move over time
- Animate the "convergence" of performance and efficiency

---

## User Journey Summary

1. **Act 1**: "Oh, sports cars and EPA vehicles are moving in completely opposite directions"
2. **Act 2**: "Wait, electric vehicles are achieving both high efficiency AND high performance?"
3. **Act 3** (planned): "The markets are converging—EVs are redefining what's possible"

This narrative structure guides users from understanding the historical tradeoff, to discovering the disruptive technology, to recognizing the market convergence.
