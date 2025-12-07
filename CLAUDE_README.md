# Claude Code Documentation - CS439 Final Project

## Project Overview

This project analyzes the evolution of automotive markets from 2011-2024, exploring whether sports cars and mainstream EPA vehicles are converging or remaining distinct. The analysis is presented through an interactive PyQt5 dashboard with three narrative acts.

---

## Datasets

### 1. Sports Car Dataset (`data/cleaned/sports_with_mpg_clean.csv`)
- **Size**: 2,849 vehicles (100% complete)
- **Columns**:
  - `Car Make`, `Car Model`, `Year` (2011-2024)
  - `Horsepower`, `Engine Size (L)`, `0-60 MPH Time (seconds)`
  - `MPG` (combined fuel economy)
  - `Price (in USD)` (all filled via Gemini API)
- **Processing**: Enriched with MPG data to enable efficiency comparisons
- **Key Feature**: NO electric vehicles in this dataset - all combustion engines

### 2. EPA Mainstream Dataset (`data/cleaned/epa_with_hp_clean.csv`)
- **Size**: 28,000+ vehicles
- **Columns**:
  - `Make`, `Model`, `Year` (2011-2024)
  - `Horsepower (est)`, `Engine displacement`, `0-60 Time (est)`
  - `Combined Mpg For Fuel Type1`, `Co2  Tailpipe For Fuel Type1`
  - `Fuel Type` (Regular, Premium, Electricity, Hybrid varieties)
- **Processing**: Sports cars already removed during cleaning
- **Key Feature**: Contains electric and hybrid vehicles

---

## Code Architecture

### Core Files

#### `dashboard_app.py` (1,560 lines)
**Main application file with PyQt5 dashboard**

**Key Classes**:
- `ControlPanel`: Universal left sidebar with year range, fuel type, brand filters
- `Act1Tab`: Diverging Priorities visualization (sports vs EPA trendlines + slope chart)
- `Act2Tab`: Electrification visualization (fuel share + scatter plot)
- `Act3Tab`: Convergence analysis (indices + clustering + convergence score)
- `MainWindow`: Application container with 3 tabs

**Data Loading**:
- `load_sports_data()`: Loads sports dataset, validates 100% price completion
- `load_epa_data()`: Loads EPA dataset (sports cars already removed)

**Signal-Slot Architecture**:
- All charts update reactively when control panel values change
- Uses `valueChanged`, `stateChanged`, `currentIndexChanged` signals

#### `plots_act3.py` (641 lines)
**Act 3 plotting functions with advanced analytics**

**Key Functions**:
- `make_indices_chart()`: Side-by-side performance & efficiency indices
  - Normalizes to base year = 100
  - Separates Gas, Sports, EV trends

- `make_cluster_plot()`: PCA + K-means clustering
  - Combines both datasets
  - StandardScaler normalization
  - PCA reduces 3D (HP, MPG, Displacement) → 2D
  - K-means identifies market segments
  - Colors = clusters, Shapes = market type

- `make_convergence_score_chart()`: Quantitative convergence metric
  - Calculates yearly HP and MPG differences between markets
  - Normalizes to baseline (2011 = 100)
  - Overall score = (HP_score + MPG_score) / 2
  - Color zones: Green (<70), Yellow (70-100), Red (>100)

#### `plots_epa.py` (200+ lines)
**EPA-specific plotting and data aggregation**

**Key Functions**:
- `compute_epa_yearly_aggregates()`: Groups EPA data by year, calculates means
- `make_epa_trend_figure()`: MPG, CO2, displacement trendlines
- `make_epa_fuel_share_figure()`: Stacked area chart of fuel type market share
- `make_epa_performance_efficiency_scatter()`: Year vs MPG scatter with fuel categories

#### `plots_sports.py` (150+ lines)
**Sports car plotting and data aggregation**

**Key Functions**:
- `compute_sports_yearly_aggregates()`: Groups sports data by year, optional brand filter
- `make_sports_trend_figure()`: HP, Engine Size, Price trendlines

---

## Act 1: Diverging Priorities

### What Act 1 Tells Us
Act 1 establishes the fundamental tension between two automotive philosophies:
- **Sports cars** prioritize performance and luxury (horsepower, acceleration, price)
- **EPA vehicles** prioritize efficiency and environmental impact (MPG, CO2 emissions)

The narrative demonstrates that from 2011-2024, these markets pursued opposite goals, creating a "divergence" in priorities.

### Chart 1A: Sports Car Trendlines
**Location**: Top-left of Act 1 tab
**File**: `dashboard_app.py` (lines 428-529)

**Features**:
- Three metrics on same axis (units vary):
  - Horsepower (red line)
  - Engine Size in Liters (orange line)
  - Price in USD (green line)
- Brand filter (All, Porsche, Ferrari, etc.)
- Normalization toggle (base year = 100)
- Year range slider

**What It Shows**:
- Sports cars increased HP and price over time
- Engine size relatively stable
- When normalized: ~20-30% growth in performance metrics
- Performance prioritization is consistent across luxury brands

**Data Flow**:
```python
sports_df → filter by year/brand → compute_sports_yearly_aggregates()
→ optional normalization → plot 3 lines → update canvas
```

### Chart 1B: EPA Trendlines
**Location**: Top-right of Act 1 tab
**File**: `dashboard_app.py` (lines 533-642)

**Features**:
- Three metrics on same axis:
  - Combined MPG (blue)
  - Tailpipe CO2 in g/mi (orange)
  - Engine Displacement in L (green)
- Fuel type filters (Gas, Electric)
- Normalization toggle
- Year range slider

**What It Shows**:
- MPG improved ~15-20% (2011-2024)
- CO2 emissions decreased ~15-20%
- Engine displacement decreased (downsizing trend)
- Electric vehicles (post-2016) show dramatic efficiency gains

**Data Flow**:
```python
epa_df → filter by year/fuel type → compute_epa_yearly_aggregates()
→ optional normalization → plot 3 lines → update canvas
```

### Chart 1C: Diverging Priorities Slope Chart
**Location**: Bottom of Act 1 tab
**File**: `dashboard_app.py` (lines 646-815)

**Features**:
- Slope chart: Start year (left) vs End year (right)
- All metrics normalized to start = 100
- Color-coded by market:
  - Green = Sports metrics (performance)
  - Red = EPA metrics (efficiency)
- Inverted metrics (0-60 time, CO2) flipped so "higher = better"

**What It Shows**:
- Sports metrics trending UP (more performance)
- EPA efficiency metrics trending UP (more efficient)
- EPA emissions metrics trending UP (less CO2 when inverted)
- The markets are moving in OPPOSITE directions
- This is the visual proof of "diverging priorities"

**Algorithm**:
```python
1. Get first & last year of range
2. For sports: Engine Size, HP, 0-60 (inverted)
3. For EPA: Engine Size, MPG, CO2 (inverted)
4. Normalize each: first_year = 100, last_year = (last/first)*100
5. Draw slope lines from 100 to normalized endpoint
6. Label with values and metric names
```

**Key Insight**: If convergence existed in Act 1, we'd see slopes crossing or moving toward each other. Instead, they diverge.

---

## Act 2: Electrification

### What Act 2 Tells Us
Act 2 reveals the game-changer: **electrification breaks the performance-efficiency tradeoff**.

In the combustion era, you chose power OR economy. Electric vehicles deliver both. This is one-sided convergence: EPA vehicles gain performance capabilities while maintaining efficiency, but sports cars (in this dataset) remain combustion-only.

### Chart 2A: Fuel Share Stacked Area
**Location**: Top-left of Act 2 tab
**File**: `dashboard_app.py` (lines 956-1064)

**Features**:
- Stacked area chart over time
- Two fuel categories:
  - Gas (blue): All combustion types
  - Electric (green): Pure EV + Hybrids
- Toggle raw counts vs percentage share
- Fuel type filters

**What It Shows**:
- 2011-2015: 85-90% gasoline dominance
- 2016-2018: Inflection point - EVs start climbing
- 2019-2024: EV share reaches 15-20%
- The market composition fundamentally changed

**Data Grouping**:
```python
Gas = ['Regular', 'Premium', 'Midgrade', 'Diesel', 'E85', 'CNG']
Electric = ['Electricity', 'Premium and Electricity', 'Regular Gas and Electricity']
```

**Algorithm**:
```python
1. Filter EPA by year range
2. Map fuel types to Gas/Electric categories
3. Group by Year + Fuel Category, count vehicles
4. Pivot to wide format
5. Optional: Convert counts to percentages
6. Create stackplot with category colors
```

### Chart 2B: Efficiency Evolution Scatter
**Location**: Top-right of Act 2 tab
**File**: `dashboard_app.py` (lines 1066-1259)

**Features**:
- Scatter plot: Year (x-axis) vs MPG (y-axis)
- Three fuel categories with distinct colors:
  - Gas (blue dots)
  - Hybrid (orange dots)
  - Electric (green dots)
- Interactive hover tooltips showing:
  - Make, Model, Year
  - Fuel type, MPG, CO2
- "Show only Electric" filter
- Tooltip position adapts: left for years ≥2020, right for <2020

**What It Shows**:
- Gas vehicles: Stuck at 20-35 MPG across ALL years
- Hybrids: 40-60 MPG (meaningful improvement)
- EVs: 80-140+ MPGe (redefining efficiency)
- EVs appear in later years (2016+)
- No vertical improvement in gas efficiency - technology ceiling

**Tooltip Logic**:
```python
def on_scatter_hover(event):
    if year >= 2020:
        tooltip_offset = -30  # Left side (prevent overflow)
    else:
        tooltip_offset = 15   # Right side
```

**Key Insight**: The scatter plot visually proves that combustion technology plateaued. Only electrification breaks through the efficiency ceiling.

---

## Act 3: Convergence vs Coexistence

### What Act 3 Tells Us
Act 3 asks the ultimate question: **Are the markets truly converging?**

Using three complementary approaches:
1. **Temporal analysis** (3A): How metrics evolve over time
2. **Spatial clustering** (3B): Do vehicles group by market or by characteristics?
3. **Quantitative score** (3C): Is the distance between markets shrinking?

The answer depends on your definition of convergence. If EPA vehicles adopt performance features, that's one-sided movement. True convergence requires both markets to meet in the middle.

### Chart 3A: Performance & Efficiency Indices
**Location**: Top row (full width) of Act 3 tab
**File**: `plots_act3.py` (lines 25-282)

**Features**:
- **Two side-by-side panels**:
  - Left: Performance Index (HP-based)
  - Right: Efficiency Index (MPG-based)
- Three market lines per panel:
  - Gas (blue): EPA gas-only vehicles
  - Sports (red): Sports cars
  - EV (green): EPA electric vehicles
- Normalized to base year = 100
- Market filters (show/hide each line)

**What It Shows (Performance Panel)**:
- Gas: Slight growth (~5-10%)
- Sports: Volatile but generally stable
- EV: Explosive growth (120%+ by 2024)
- **EVs are gaining performance rapidly**

**What It Shows (Efficiency Panel)**:
- Gas: Slow improvement (~15%)
- Sports: Volatile, slight decline
- EV: Starts high, continues climbing
- **Sports cars are NOT improving efficiency**

**Algorithm**:
```python
1. Filter both datasets by year
2. Group EPA by Fuel Type (Gas/Electric)
3. Calculate yearly means for HP and MPG
4. Normalize to first year = 100
5. Plot two subplots side-by-side
```

**Key Insight**: One-sided convergence is visible. EVs move toward sports-level performance. Sports cars don't move toward EV efficiency.

### Chart 3B: Market Clustering (PCA + K-Means)
**Location**: Bottom-left of Act 3 tab
**File**: `plots_act3.py` (lines 285-475)

**Features**:
- **PCA (Principal Component Analysis)**:
  - Reduces 3D data (HP, MPG, Displacement) to 2D
  - PC1 and PC2 explain ~70-80% of variance
  - X-axis: PC1 (primary variance dimension)
  - Y-axis: PC2 (secondary variance dimension)

- **K-Means Clustering**:
  - Identifies 3 natural market segments (default)
  - Adjustable: 3, 4, or 5 clusters via dropdown

- **Visual Encoding**:
  - **Colors** = Cluster ID (blue, orange, green)
  - **Shapes** = Original market
    - Circles = EPA vehicles
    - Squares = Sports cars
  - **X marks** = Cluster centers (black)

- **Filters**:
  - Year range
  - Show/hide sports or EPA
  - Number of clusters (K)

**What It Shows**:
- **Convergence scenario**: Mixed clusters with circles AND squares
- **Coexistence scenario**: Separate clusters (sports in one, EPA in others)
- **Hybrid scenario**: Some overlap, some separation

**Algorithm**:
```python
# Data Preparation
1. Extract features: HP, MPG, Displacement
2. Combine sports + EPA datasets
3. StandardScaler normalization (mean=0, std=1)

# Dimensionality Reduction
4. PCA: 3D → 2D
   - Fit on normalized features
   - Transform to get PC1, PC2 coordinates

# Clustering
5. K-Means on ORIGINAL 3D normalized data
   - Fit with K clusters (default 3)
   - Predict cluster labels

# Visualization
6. Scatter plot:
   - X = PC1, Y = PC2
   - Color by cluster ID
   - Shape by market type
7. Transform cluster centers to PCA space
8. Plot centers as black X marks
```

**Interpretation Guide**:
- **Cluster 1 (Blue)**: Often economy/efficient vehicles (high MPG, low HP)
- **Cluster 2 (Orange)**: Balanced/midsize vehicles
- **Cluster 3 (Green)**: Performance vehicles (high HP, low MPG)

If sports cars and EPA vehicles appear in SAME colored clusters → convergence.
If sports are mostly green and EPA are mostly blue/orange → coexistence.

### Chart 3C: Convergence Score
**Location**: Bottom-right of Act 3 tab
**File**: `plots_act3.py` (lines 478-641)

**Features**:
- **Time series line chart**
- **Three lines** (optional):
  - Overall Convergence Score (thick purple)
  - HP Divergence (thin red)
  - MPG Divergence (thin green)
- **Color zones**:
  - Green zone (<70): Markets converging
  - Yellow zone (70-100): Moderate divergence
  - Red zone (>100): Markets diverging
- **Baseline**: First year (2011) = 100

**What It Shows**:
- Score > 100: Markets MORE different than 2011
- Score < 100: Markets MORE similar than 2011
- Score ~ 100: No change in divergence

**Algorithm**:
```python
# Yearly Distance Calculation
for each year in range:
    sports_avg_hp = mean(sports[year].HP)
    epa_avg_hp = mean(epa_gas[year].HP)  # Gas only for fair comparison
    hp_distance = abs(sports_avg_hp - epa_avg_hp)

    sports_avg_mpg = mean(sports[year].MPG)
    epa_avg_mpg = mean(epa_gas[year].MPG)
    mpg_distance = abs(sports_avg_mpg - epa_avg_mpg)

# Normalization
baseline_hp = hp_distance[2011]
baseline_mpg = mpg_distance[2011]

hp_scores = [100 * (d / baseline_hp) for d in hp_distances]
mpg_scores = [100 * (d / baseline_mpg) for d in mpg_distances]

# Overall Score
overall_scores = [(hp + mpg) / 2 for hp, mpg in zip(hp_scores, mpg_scores)]

# Interpretation Zones
ax.axhspan(0, 70, color='green', alpha=0.1)      # Converging
ax.axhspan(70, 100, color='yellow', alpha=0.1)   # Moderate
ax.axhspan(100, max_score, color='red', alpha=0.1)  # Diverging
```

**Key Insight**: This chart provides the QUANTITATIVE answer to "are they converging?". If the line trends down, yes. If flat or up, no.

---

## Control Panel Features

### Universal Sidebar (All Acts)
**File**: `dashboard_app.py` (lines 121-270)

**Year Range Controls**:
- Min/Max spinners (2011-2024)
- Auto-validation: min ≤ max

**Sports Car Options**:
- Show/hide sports lines
- Brand filter dropdown
- Normalization toggle

**EPA Options**:
- Show/hide EPA lines
- Fuel type checkboxes (Gas, Electric)
- "Show only Electric" filter
- Raw counts vs percentage toggle

**Act 3 Specific**:
- Index line toggles (4 indices)
- Cluster count dropdown (K=3,4,5)
- Market filter (Both, Sports only, EPA only)

**Signal Architecture**:
All controls emit signals on value change:
```python
year_min_spin.valueChanged → update_all_charts()
chk_normalize.stateChanged → update_all_charts()
cmb_sports_brand.currentIndexChanged → update_all_charts()
```

---

## Data Processing Pipeline

### Stage 1: Sports Car Population from EPA Dataset
**File**: `enrich_sports_dataset.py`

**Problem**: Original sports dataset had limited coverage (especially 2013-2020)

**Solution**: Extract sports cars from EPA all-vehicles dataset

**Algorithm**:
```python
# 1. Define sports car criteria
sports_brands = ['Porsche', 'Ferrari', 'Lamborghini', 'McLaren', ...]
performance_keywords = ['M3', 'M4', 'M5', 'RS3', 'AMG GT', 'Corvette', ...]

# 2. Extract from EPA dataset
sports_from_epa = epa[epa['Make'].isin(sports_brands)]
for keyword in performance_keywords:
    matches = epa[epa['Model'].str.contains(keyword)]
    sports_from_epa = concat([sports_from_epa, matches])

# 3. Map EPA columns to sports dataset format
epa_sports_mapped = {
    'Car Make': epa['Make'],
    'Car Model': epa['Model'],
    'Horsepower': epa['Horsepower (est)'],
    'MPG': epa['Combined Mpg For Fuel Type1'],
    'Price (in USD)': NA  # Not in EPA data
}

# 4. Merge with original sports dataset
# IMPORTANT: Only add cars NOT already in sports dataset
# This preserves existing price data
enriched_sports = concat([sports_original, epa_sports_new])
```

**Sports Car Identification Criteria**:

**Pure Sports/Luxury Brands** (extracted entirely):
- European exotics: Porsche, Ferrari, Lamborghini, McLaren, Aston Martin
- Luxury brands: Bentley, Bugatti, Maserati, Rolls-Royce
- Boutique manufacturers: Lotus, Alfa Romeo, Koenigsegg, Pagani

**Performance Models** (keyword matching):
- BMW M-series: M2, M3, M4, M5, M6, M8, X5 M, X6 M, i8
- Audi performance: R8, RS3/4/5/6/7, S3/4/5/6/7/8, TT RS
- Mercedes-AMG: AMG GT, C63, E63, S63, G63, SLS AMG
- Lexus F models: LC 500, RC F, GS F, IS F
- Jaguar: F-Type, F-PACE SVR
- Cadillac V: CTS-V, ATS-V, CT5-V Blackwing
- American muscle: Corvette, Mustang GT/Shelby, Camaro SS/ZL1, Challenger/Charger Hellcat/SRT, Viper
- Japanese sports: GT-R, 370Z/350Z, Supra, NSX, WRX STI, BRZ, Type R
- Korean performance: Veloster N, Stinger GT

**Result**:
- Original sports dataset: ~1,200 cars
- Extracted from EPA: ~1,100 additional cars
- **Final enriched dataset: 2,849 sports cars**

### Stage 2: Dataset Cleaning
**File**: `cleaning.py` (457 lines)

#### Function: `load_and_clean_epa_with_hp()`
**Purpose**: Clean EPA dataset and remove sports cars to avoid overlap

**Steps**:
```python
1. Load CSV (semicolon-separated)
   epa = pd.read_csv(path, sep=";")

2. Select columns of interest
   cols = ['Make', 'Model', 'Year', 'Fuel Type', 'Combined Mpg For Fuel Type1',
           'Co2  Tailpipe For Fuel Type1', 'Engine displacement',
           'Horsepower (est)', '0-60 time (est)']

3. Filter by year range (2011-2024)
   year_mask = (epa['Year'] >= 2011) & (epa['Year'] <= 2024)

4. Filter for valid MPG data
   # KEY DECISION: Keep BOTH "MPG Data=Y" and "MPG Data=N"
   # Y = 5-cycle EPA test (modern, accurate)
   # N = 2-cycle EPA test or estimates (older, still valid)
   # This increases dataset from ~9,000 to ~28,000 vehicles!
   mpg_mask = (epa['Combined Mpg For Fuel Type1'].notna()) &
              (epa['Combined Mpg For Fuel Type1'] > 0)

5. Convert to numeric types
   for col in numeric_cols:
       epa[col] = pd.to_numeric(epa[col], errors='coerce')

6. Remove sports cars using filter_sports_from_epa()
   # CRITICAL: Prevents overlap with sports dataset
   epa_clean = filter_sports_from_epa(epa_filtered)
```

**Output**: 28,000+ mainstream vehicles, no sports cars

#### Function: `filter_sports_from_epa()`
**Purpose**: Remove sports cars from EPA dataset using same criteria as extraction

**Algorithm**:
```python
1. Filter out pure sports brands
   df = df[~df['Make'].isin(sports_brands_full)]

2. Filter out performance models by keyword
   for keyword in performance_keywords:
       df = df[~df['Model'].str.contains(keyword, case=False)]

3. Report removed count
   print(f"Filtered out {count} sports cars from EPA dataset")
```

**Result**: Clean separation between markets (no overlap)

#### Function: `load_and_clean_sports_with_mpg()`
**Purpose**: Clean sports dataset with MPG data

**Steps**:
```python
1. Load enriched sports CSV
   sports = pd.read_csv(path)

2. Clean numeric columns (handle formatting issues)
   # Remove commas: "1,234" → "1234"
   # Extract numbers: "$50,000 USD" → "50000"
   # Convert to float
   for col in numeric_cols:
       sports[col] = (
           sports[col].str.replace(',', '')
                      .str.extract(r'([0-9.]+)')[0]
       )
       sports[col] = pd.to_numeric(sports[col], errors='coerce')

3. Filter by year range (2011-2024)
   year_mask = (sports['Year'] >= 2011) & (sports['Year'] <= 2024)

4. Remove duplicates, prioritizing rows WITH price data
   sports = sports.sort_values('Price (in USD)', ascending=False, na_position='last')
   sports = sports.drop_duplicates(['Car Make', 'Car Model', 'Year'], keep='first')
   # This ensures cars from original dataset (with prices) are kept
```

**Output**: 2,849 unique sports cars

### Stage 3: Sports Car Price Enrichment
**Original Issue**: Sports dataset had 1,842 missing prices (out of 2,849 total)
- Original sports cars: Had prices
- EPA-extracted sports cars: No price data (EPA doesn't track MSRPs)

**Solution**: Iterative enrichment with Gemini API
1. Extract cars without prices (Make, Model, Year)
2. Query Gemini for MSRP data in batches of 200
3. Parse responses (handle formatting: "$50,000" → 50000.0)
4. Update dataset with new prices
5. Repeat until 100% complete (5 iterations)

**Files Used** (now deleted):
- `update_prices.py`: Updated raw enriched dataset
- `update_cleaned_prices.py`: Updated cleaned dataset (437 entries across iterations)
- `fix_final_prices.py`: Fixed 3 Maserati cars with spacing issue ("Ghibli  S RWD" with double space)

**Final Result**: All 2,849 sports cars have price data

**Validation** (in `dashboard_app.py`):
```python
missing_prices = df['Price (in USD)'].isna().sum()
if missing_prices > 0:
    print(f"⚠️  WARNING: {missing_prices} cars missing prices")
else:
    print(f"✓ All {len(df)} sports cars have complete data")
```

### Data Integrity Guarantees

**No Overlap**: Sports cars appear in EITHER sports dataset OR EPA dataset, never both
- `filter_sports_from_epa()` removes all sports cars from EPA
- Uses identical brand list and keyword matching

**Deduplication**: No duplicate (Make, Model, Year) combinations
- Sports dataset: Deduped with price priority
- EPA dataset: Deduped during extraction

**Complete Data**: All vehicles have core metrics
- Sports: HP, MPG, Engine Size, 0-60, Price (100% complete)
- EPA: HP, MPG, CO2, Engine Size, Fuel Type

**Year Coverage**: Both datasets span 2011-2024
- Sports: Enriched to fill gaps in 2013-2020
- EPA: Comprehensive coverage all years

### Cleaning Pipeline Summary

```
Original EPA Dataset (84,000+ vehicles, 1984-2024)
    ↓
Filter year range (2011-2024)
    ↓
Filter valid MPG data
    ↓
Remove sports cars using filter_sports_from_epa()
    ↓
Clean EPA Dataset (28,000+ vehicles)

Original Sports Dataset (~1,200 vehicles with prices)
    ↓
Extract sports from EPA using same criteria
    ↓
Merge with original (avoid duplicates)
    ↓
Enriched Sports Dataset (2,849 vehicles, missing prices)
    ↓
Enrich prices with Gemini API (5 iterations)
    ↓
Clean Sports Dataset (2,849 vehicles, 100% complete)
```

---

## Interactive Features

### Hover Tooltips (Chart 2B)
**Implementation**: `dashboard_app.py` (lines 1193-1259)

**Behavior**:
- Mouse over scatter points shows tooltip
- Tooltip contains: Make, Model, Year, Fuel Type, MPG, CO2
- Smart positioning: Left side for 2020+, right side for <2020
- Yellow background, black arrow pointer
- Updates on `motion_notify_event`

**Performance**:
- Uses `contains()` method to detect hover
- Redraws with `draw_idle()` for efficiency
- Annotation object reused (not recreated each time)

### Real-time Chart Updates
All charts rebuild on control panel changes:
```python
# Example: Year range change
def update_indices_chart(self):
    year_min = self.control_panel.year_min_spin.value()
    year_max = self.control_panel.year_max_spin.value()

    self.indices_figure.clear()  # Clear old plot
    fig = make_indices_chart(data, year_min, year_max)

    # Copy from source figure to canvas figure
    for ax in fig.axes:
        new_ax = self.indices_figure.add_subplot(...)
        # Copy lines, labels, properties

    self.canvas_indices.draw()  # Render
```

**Pattern**: Clear → Rebuild → Copy → Draw

---

## Visualization Stretch Ratios

### Act 1 Layout
```python
Row 1 (stretch=2): Sports Trendlines | EPA Trendlines
Row 2 (stretch=3): Slope Chart | Narrative Box
```

### Act 2 Layout
```python
Row 1 (stretch=2): Fuel Share | Efficiency Scatter
Row 2 (stretch=1): Narrative Box (full width)
```

### Act 3 Layout
```python
Row 1 (stretch=2): Performance & Efficiency Indices (full width)
Row 2 (stretch=2): Cluster Plot | Convergence Score
```

**Key**: Higher stretch values allocate more vertical space

---

## Dependencies

### Python Libraries
```python
# GUI Framework
PyQt5                 # Dashboard, widgets, layouts

# Data Processing
pandas                # DataFrame operations
numpy                 # Numerical computations

# Visualization
matplotlib            # All plotting
matplotlib.backends.backend_qt5agg  # Qt integration

# Machine Learning (Act 3 only)
sklearn.preprocessing.StandardScaler  # Feature normalization
sklearn.decomposition.PCA             # Dimensionality reduction
sklearn.cluster.KMeans                # Clustering algorithm
```

### File Structure
```
CS439-Final-Project/
├── data/
│   ├── cleaned/
│   │   ├── sports_with_mpg_clean.csv      (2,849 rows, 100% complete)
│   │   └── epa_with_hp_clean.csv          (28,000+ rows)
│   └── raw/
│       └── Sport car price with mpg adjusted ENRICHED.csv
├── src/
│   ├── dashboard_app.py      (Main dashboard, 1,560 lines)
│   ├── plots_act3.py          (Act 3 plotting, 641 lines)
│   ├── plots_epa.py           (EPA plotting functions)
│   └── plots_sports.py        (Sports plotting functions)
└── README.md
```

---

## Key Algorithms Summary

### 1. Normalization (All Trendlines)
```python
first_value = df[metric].iloc[0]
normalized = (df[metric] / first_value) * 100
```
**Purpose**: Compare metrics with different units on same scale

### 2. PCA Transformation (Chart 3B)
```python
scaler = StandardScaler()
features_scaled = scaler.fit_transform([HP, MPG, Displacement])
pca = PCA(n_components=2)
features_2d = pca.fit_transform(features_scaled)
```
**Purpose**: Reduce 3D → 2D while preserving maximum variance

### 3. K-Means Clustering (Chart 3B)
```python
kmeans = KMeans(n_clusters=3, random_state=42)
cluster_labels = kmeans.fit_predict(features_scaled)
centers = kmeans.cluster_centers_
```
**Purpose**: Identify natural market segments

### 4. Convergence Score (Chart 3C)
```python
distance = abs(sports_mean - epa_mean)
baseline = distance[first_year]
score = (distance / baseline) * 100
```
**Purpose**: Quantify how different markets are over time

---

## Narrative Flow

### Act 1: The Setup
**Message**: Two markets with opposite goals
**Evidence**: Charts 1A, 1B, 1C all show divergence
**Outcome**: Establishes the conflict

### Act 2: The Catalyst
**Message**: Electrification changes everything
**Evidence**: Chart 2A shows market shift, Chart 2B shows efficiency breakthrough
**Outcome**: EVs break the performance-efficiency tradeoff

### Act 3: The Resolution
**Message**: One-sided convergence, not mutual convergence
**Evidence**:
- Chart 3A: EVs gain performance, sports don't gain efficiency
- Chart 3B: Clustering reveals overlap vs separation
- Chart 3C: Quantifies the convergence trend

**Outcome**: Markets are closer than 2011, but coexistence remains

---

## Performance Optimizations

### Data Loading
- CSV files read once at startup
- DataFrames stored in tab instances
- Filtered on demand, never reloaded

### Chart Rendering
- Figure clearing avoids memory leaks
- `tight_layout()` prevents label cutoff
- `draw_idle()` for hover events (deferred rendering)

### Signal Handling
- `blockSignals()` during programmatic updates
- Prevents recursion in year range validation
- Single signal triggers single chart rebuild

---

## Future Enhancement Ideas

1. **Export Functionality**: Save filtered data as CSV
2. **Custom Date Ranges**: Allow arbitrary year selection
3. **Animation**: Show temporal evolution as animation
4. **Statistical Tests**: Add significance testing to convergence scores
5. **More Datasets**: Include Tesla, Rivian for EV sports comparison
6. **Predictive Models**: Forecast future convergence trends

---

## Common Issues & Solutions

### Issue: Charts not updating
**Cause**: Signal not connected
**Fix**: Add `cp.widget.signal.connect(self.update_chart)` in `_connect_signals()`

### Issue: Legend too large
**Cause**: Too many fuel types selected
**Fix**: Use simplified fuel groupings (Gas/Electric)

### Issue: PCA plot unclear
**Cause**: Too few clusters or too much overlap
**Fix**: Adjust K value, filter by year range to reduce data density

### Issue: Missing prices warning
**Cause**: Dataset not fully enriched
**Fix**: All prices now complete (2,849/2,849), should not occur

---

## Testing Checklist

- [ ] All 3 tabs load without errors
- [ ] Year range validation works (min ≤ max)
- [ ] All checkboxes toggle respective lines
- [ ] Brand filter updates sports charts
- [ ] Normalization toggle changes axis labels
- [ ] Cluster count dropdown updates Chart 3B
- [ ] Hover tooltips appear on Chart 2B
- [ ] All charts update on control panel changes
- [ ] No console warnings about missing data

---

## Academic Context

**Course**: CS439 - Data Visualization
**Topic**: Comparative market analysis through narrative visualization
**Techniques**:
- Time series analysis
- Clustering and dimensionality reduction
- Interactive dashboards
- Multi-view coordination

**Learning Outcomes**:
- Design narrative-driven visualizations
- Implement coordinated multiple views
- Apply unsupervised ML to exploratory analysis
- Build production-quality dashboards with PyQt5
