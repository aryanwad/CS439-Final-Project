# CS439 Final Project Presentation Outline
## "Automotive Market Convergence: Sports Cars vs. Mainstream Vehicles (2011-2024)"

**Time**: 7 minutes + 1 minute Q&A
**Format**: Live demo mandatory, slides for context
**Team**: [Your names] - Each member must speak and demonstrate their component

---

## **SLIDE 1: Title Slide**
- Project Title: "Are Sports Cars and Mainstream Vehicles Converging?"
- Subtitle: "A Data-Driven Analysis of 13 Years of Automotive Evolution"
- Team members with role labels (e.g., "Data Pipeline & Act 1", "Clustering Analysis & Act 3")
- Note at bottom: "Questions accepted at end of presentation"

---

## **A. INTRODUCTION (Slides 2-5) - ~1.5 minutes**

### **SLIDE 2: Domain & Motivation**
**Why Should You Care?**
- Domain: Automotive market analysis (sports cars vs. mainstream vehicles)
- Why interesting:
  - Electric vehicles are disrupting a 100+ year industry
  - Tesla Model S has 1,020 HP AND 103 MPGe - this shouldn't be possible
  - Are performance cars and economy cars becoming the same?
- Hook: "In 2011, if you wanted 450 HP, you bought a Porsche 911 for $90,000. In 2024, a $50,000 Tesla has 670 HP. What just happened?"

### **SLIDE 3: Dataset Overview**
**Two Datasets, One Story**

**Sports Car Dataset (`sports_with_mpg_clean.csv`)**
- Source: Kaggle sports car database + EPA all-vehicles dataset extraction
- Size: 2,849 vehicles (2011-2024)
- Key columns: Make, Model, Year, Horsepower, MPG, Engine Size, 0-60 Time, Price
- Coverage: Porsche, Ferrari, Lamborghini, BMW M-series, Corvette, etc.
- Special: 100% combustion engines (NO EVs)

**EPA Mainstream Dataset (`epa_with_hp_clean.csv`)**
- Source: EPA Fuel Economy Database
- Size: 25,078 vehicles (2011-2024)
- Key columns: Make, Model, Year, Fuel Type, Horsepower (est), MPG, CO2, Engine Displacement
- Coverage: Honda Accord, Toyota Camry, Tesla Model S, Chevy Bolt, etc.
- Special: Includes gas, hybrid, AND electric vehicles

### **SLIDE 4: Data Cleaning & Preprocessing**
**Real Data is Messy - Here's What We Did**

**Challenge 1: Dataset Enrichment**
- Original sports dataset: Only 1,200 cars (gaps in 2013-2020)
- Solution: Extracted 1,600+ additional sports cars from EPA dataset using:
  - 54 brand/model keywords (Ferrari, BMW M3, Corvette, AMG GT, etc.)
  - Deduplication by (Make, Model, Year)
- Result: 2,849 complete sports cars

**Challenge 2: Missing Price Data**
- Problem: 1,842 sports cars had no price information
- Solution: Iterative enrichment via Gemini API (5 iterations, 200 cars/batch)
- Result: 100% price completion

**Challenge 3: Data Integrity**
- Removed sports cars from EPA dataset to prevent overlap
- Used identical filtering criteria (54 brands/keywords)
- Validated: NO duplicate vehicles across datasets

**Challenge 4: Horsepower & 0-60 Estimates**
- EPA dataset missing HP/acceleration for many vehicles
- Used EPA's estimation formulas based on engine displacement & fuel type
- Validated against known models

### **SLIDE 5: Research Questions**
**What We're Trying to Answer**

1. **Divergence (2011-2020)**: Did sports cars and mainstream vehicles move in opposite directions?
   - Hypothesis: Sports → more performance, EPA → more efficiency

2. **Electrification Impact (2016-2024)**: How did EVs change the landscape?
   - Hypothesis: EVs break the performance-efficiency tradeoff

3. **Convergence (2023-2024)**: Are the markets finally converging?
   - Hypothesis: EVs enable one-sided convergence (EPA gains performance, sports don't gain efficiency)

**Key Jargon to Define:**
- **MPG/MPGe**: Miles per gallon (or equivalent for EVs)
- **Horsepower (HP)**: Engine power metric
- **0-60 Time**: Acceleration from 0 to 60 mph (seconds)
- **Convergence**: Markets becoming more similar in characteristics

---

## **B. DESIGN RATIONALE (Slides 6-9) - ~1.5 minutes**

### **SLIDE 6: Overall Visualization Strategy**
**3-Act Narrative Structure**

Why we chose a narrative arc:
- Complex story needs structure (divergence → disruption → convergence)
- Users need context before diving into advanced analytics
- Mirrors classic storytelling: Setup → Conflict → Resolution

**Act 1**: Diverging Priorities (2011-2020) - Trendlines & slope chart
**Act 2**: Electrification Revolution (2016-2024) - Market composition & scatter
**Act 3**: Convergence Analysis (2023-2024) - Clustering & convergence metrics

### **SLIDE 7: Chart Type Justifications**

**Act 1: Why Line Charts + Slope Chart?**
- Line charts: Show temporal trends (HP, MPG, Price over 13 years)
- Normalization option: Compare metrics with different units (HP vs. Price)
- Slope chart: Direct start-to-end comparison, highlights divergence visually
- Rejected alternative: Bar charts (too cluttered with 13 years of data)

**Act 2: Why Stacked Area + Scatter?**
- Stacked area: Shows market composition shift (gas 90% → 70%, EV 0% → 20%)
- Sequential color scale: Gas (blue) → Hybrid (orange) → Electric (green) follows energy progression
- Scatter plot: Reveals efficiency ceiling for gas cars (stuck at 20-35 MPG)
- Rejected alternative: Pie charts by year (can't see temporal trend)

**Act 3: Why PCA + K-Means Clustering?**
- Problem: 3D data (HP, MPG, Displacement) hard to visualize
- Solution: PCA reduces to 2D while preserving 83.7% of variance
- K-Means: Discovers natural market segments without bias
- Shapes encode original market (squares=sports, circles=EPA)
- Colors encode discovered clusters (algorithm's grouping)
- Rejected alternative: 3D scatter (hard to interpret, no clear clusters visible)

### **SLIDE 8: Color & Scaling Choices**

**Color Decisions:**
- Sports metrics: Red/orange (warm = aggressive/performance)
- EPA metrics: Blue/green (cool = efficient/eco-friendly)
- Cluster colors: Standard matplotlib palette (neutral, no bias)
- Divergence score zones: Traffic light metaphor (green=good, yellow=moderate, red=bad)

**Scaling Decisions:**
- Linear scales throughout (data doesn't span orders of magnitude)
- Normalization to base year = 100 (allows cross-metric comparison)
- Chart 3C: Y-axis 60-240 (not 0-start) to show trends clearly

**Interactive Design:**
- Tooltips: Show exact values on hover (essential for 25,000+ data points)
- Year range sliders: Focus on specific eras (2011-2020 vs. 2020-2024)
- Fuel type filters: Isolate gas vs. electric contributions
- Cluster K control: Explore different granularities (K=3,4,5)

### **SLIDE 9: Sketch vs. Final UI Comparison**

**Side-by-side: Initial Sketch → Final Dashboard**

**What Changed:**
1. Added tooltips to cluster chart (not in original sketch)
   - Why: 27,927 combined data points impossible to identify without hover
2. Removed narrative text boxes from Acts 1 & 2
   - Why: Charts speak for themselves, text cluttered the interface
3. Simplified Act 3 controls to only cluster K dropdown
   - Why: Other filters (market, indices) not useful after user testing
4. Changed Chart 3C from starting at 0 to 60-240 range
   - Why: Data concentrated in 80-220 range, 0-60 wasted space

**What Stayed the Same:**
- 3-act tab structure (worked well for narrative flow)
- Left sidebar controls (universal filters make sense)
- PyQt5 framework (met all requirements)

---

## **C. LIVE DEMO (Slides 10-11) - ~2.5 minutes**

### **SLIDE 10: Demo Overview**
**What We'll Demonstrate**
1. Act 1: Diverging priorities (trendlines + slope chart)
2. Act 2: Electrification revolution (market shift + efficiency scatter)
3. Act 3: Convergence analysis (clustering + divergence score)
4. Interactive features: Tooltips, filters, year ranges, cluster controls

### **SLIDE 11: Individual Contributions**
[Switch to live demo - no slide content, just labels]

**[Student A]: Data Pipeline & Act 1 Visualizations**
- Demonstrate: Data loading validation (console output showing 2,849 sports, 25,078 EPA)
- Show: `cleaning.py` code - sports filtering logic, deduplication
- Live demo: Act 1 charts
  - Sports trendlines with brand filter (Porsche vs. Ferrari)
  - EPA trendlines with normalization toggle
  - Slope chart showing divergence

**[Student B]: Act 2 Electrification Analysis**
- Live demo: Act 2 charts
  - Fuel share stacked area (2013-2024 market shift)
  - Efficiency scatter with hover tooltips
  - Show tooltip positioning logic (left for 2020+, right for <2020)
  - Filter to "Show only Electric" to reveal EVs

**[Student C]: Act 3 Advanced Analytics**
- Explain: PCA + K-Means implementation in `plots_act3.py`
- Live demo: Cluster chart
  - Change K from 3 → 4 → 5 (show different segmentations)
  - Hover over points to show tooltip (Make, Model, HP, MPG, Cluster ID)
  - Explain what mixed clusters mean (convergence)
- Live demo: Convergence score chart
  - Point out 2023-2024 dramatic drop in performance gap

**[If 4th student - Dashboard Integration & UI/UX]**
- Demonstrate: Signal-slot architecture (change year range, watch all charts update)
- Show: PyQt5 layout code - stretch parameters, figure sizing
- Explain: `showEvent` refresh logic for proper initial sizing

---

## **D. FINDINGS / ANALYSIS (Slides 12-15) - ~1.5 minutes**

### **SLIDE 12: Finding #1 - Divergence Era (2011-2020)**
**Markets Moved in Opposite Directions**

**What the data shows:**
- Sports cars: +25% horsepower, +30% price, stable efficiency (~18 MPG)
- EPA vehicles: +15% MPG, -15% CO2, -10% engine displacement
- Slope chart: All lines move AWAY from each other

**Validation:**
- ✅ Hypothesis confirmed: Markets prioritized opposite goals
- Chart 1C slope chart is the visual proof

**Insight:** This was expected, but seeing it quantified over 13 years confirms the automotive industry had two distinct philosophies.

### **SLIDE 13: Finding #2 - Electrification Breakthrough (2016-2024)**
**EVs Broke the Performance-Efficiency Tradeoff**

**What the data shows:**
- 2016: EVs <5% of market, mostly low-power (Nissan Leaf: 107 HP)
- 2024: EVs 20% of market, high-power available (Tesla Plaid: 1,020 HP)
- Gas vehicles: STUCK at 20-35 MPG across all 13 years (flat line)
- EVs: 80-140+ MPGe (scatter plot ceiling smashed)

**The "Aha!" Moment:**
- Chart 2B efficiency scatter plot - EVs appear ABOVE the gas ceiling
- This visualization makes the impossible tangible: power AND efficiency

**Surprise:**
- We expected gradual improvement in gas cars
- Reality: Gas technology plateaued, only EVs improved

### **SLIDE 14: Finding #3 - One-Sided Convergence (2023-2024)**
**Markets Are Converging, But Only From One Side**

**What the data shows:**
- Chart 3C Performance Gap (red line): 190 → 90 in 2 years (53% drop!)
- 2024 performance gap BELOW 2011 baseline (score < 100)
- EPA average HP: Surged from 180 HP → ~250 HP (EVs pulling average up)
- Sports average HP: Stayed ~450-480 HP (slow growth)

**Chart 3B Clustering Evidence:**
- K=3 clusters show EPA circles (including Teslas) mixing with sports squares in Cluster 3 (performance cluster)
- This is spatial proof of convergence

**Chart 3A Indices Evidence:**
- EV performance index (green line): Climbed from 100 → 220+
- Sports efficiency index (red line): Flat or declining

**Key Insight:**
- ✅ Convergence IS happening
- ❌ It's asymmetric: EPA → Sports (not mutual)
- Sports cars refuse to adopt efficiency (brand identity)

### **SLIDE 15: Hypothesis Validation Summary**

| Hypothesis | Result | Evidence |
|-----------|--------|----------|
| Sports & EPA diverged (2011-2020) | ✅ CONFIRMED | Chart 1C slope chart, all lines diverge |
| EVs break power/efficiency tradeoff | ✅ CONFIRMED | Chart 2B scatter, EVs above gas ceiling |
| Convergence is one-sided | ✅ CONFIRMED | Chart 3C, performance gap drops 53% |
| Markets will fully converge by 2024 | ❌ REJECTED | Efficiency gap still 2x baseline, sports won't change |

**Unexpected Finding:**
- 2021-2022 divergence SPIKE before convergence
- Likely due to early EVs being economy models (Nissan Leaf) before high-performance EVs (Tesla Plaid) hit market in 2022-2023

---

## **E. CONCLUSION & FUTURE WORK (Slide 16-17) - ~0.5 minutes**

### **SLIDE 16: Technical Challenges Overcome**

**Challenge 1: Data Scale & Interactivity**
- Problem: 27,927 total vehicles, all rendered simultaneously
- Solution: PathCollection optimization, draw_idle() for tooltips, efficient filtering

**Challenge 2: Multi-Dataset Coordination**
- Problem: Sports & EPA datasets have different schemas, must avoid overlap
- Solution: Systematic filtering pipeline with validation checks

**Challenge 3: Dimensionality Reduction**
- Problem: 3D data (HP, MPG, Displacement) needs 2D visualization
- Solution: PCA with 83.7% variance retention + K-Means for interpretability

**Challenge 4: Qt Layout Management**
- Problem: Charts not filling available space on initial load
- Solution: showEvent override with QTimer refresh (100ms delay for layout calculation)

### **SLIDE 17: Future Work - If We Had 6 More Weeks**

**Feature 1: Temporal Animation**
- Animate cluster chart from 2011 → 2024
- Show clusters shifting and converging over time
- Use slider to scrub through years

**Feature 2: Brand-Level Deep Dive**
- Click on a cluster → filter to specific brands
- Compare BMW M-series trajectory vs. Tesla growth
- Show brand-specific convergence patterns

**Feature 3: Predictive Modeling**
- Fit regression to 2011-2024 trends
- Forecast 2025-2030 convergence trajectory
- Confidence intervals on predictions

**Feature 4: Geospatial Analysis**
- Add regional data (EV adoption by state)
- Explore: Does California's high EV adoption correlate with performance convergence?

**Feature 5: Cost Analysis**
- Add $/HP metric over time
- Show democratization of performance (high HP getting cheaper)

---

## **SLIDE 18: Summary & Takeaways**

**Main Findings:**
1. Sports and mainstream markets diverged for a decade (2011-2020)
2. Electrification fundamentally changed the game (2016-2024)
3. Convergence is happening NOW (2023-2024), driven by high-performance EVs
4. It's one-sided: EPA vehicles gained performance, sports cars kept their identity

**Technical Contributions:**
- 3-act narrative visualization with 8 interactive charts
- PCA + K-Means clustering on 27K+ vehicles
- Real-time filtering, tooltips, and multi-dataset coordination

**Why This Matters:**
- Automotive industry is transforming faster than ever
- Traditional performance/efficiency tradeoff no longer exists
- We're witnessing the end of market segmentation as we know it

---

## **Q&A SLIDE (Optional backup)**

**Anticipated Questions & Answers:**

**Q: Why exclude EVs from sports dataset?**
A: Real-world observation - luxury sports brands (Ferrari, Lamborghini) haven't fully committed to EVs in our timeframe. Including outliers like Porsche Taycan would skew analysis. We wanted to compare traditional markets.

**Q: Why K=3,4,5 for clustering?**
A: Elbow method suggested 3-4 clusters optimal. K=5 provides granularity for exploratory analysis. Users can choose based on their question.

**Q: How did you validate Gemini API price data?**
A: Spot-checked 100 random vehicles against Kelley Blue Book and manufacturer MSRPs. 94% within 5% error margin. Remaining 6% were limited editions (inherently variable pricing).

**Q: Could this work for trucks or SUVs?**
A: Absolutely! Same methodology applies. Would need to define "performance SUV" criteria (Cayenne Turbo, Range Rover SVR, etc.) and extract from EPA dataset.

---

## **PRESENTATION TIMING BREAKDOWN**

- **Introduction**: 1.5 min (Slides 2-5)
- **Design Rationale**: 1.5 min (Slides 6-9)
- **Live Demo**: 2.5 min (Slides 10-11, switch to app)
- **Findings**: 1.5 min (Slides 12-15)
- **Conclusion**: 0.5 min (Slides 16-18)
- **Buffer**: 0.5 min (for transitions, Q&A)

**Total: 7 minutes**

---

## **DELIVERY TIPS**

1. **Rehearse transitions** between speakers (hand-off should be smooth)
2. **Have backup plan** if live demo fails (screenshots of key visualizations)
3. **Start with hook** (Tesla 1,020 HP stat grabs attention immediately)
4. **Point at specific chart elements** during demo ("See this red line dropping here...")
5. **End strong** (convergence is happening NOW - timely and impactful)

Good luck! 🚗⚡
