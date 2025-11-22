
# 📘 CS439 Final Project – Full Narrative + Visualization Engineering Blueprint

This document outlines *exactly* what visualizations we will build, what controls they require, how the user will interact with them, and how each visualization contributes to the Act-based narrative of the project.

It is both a **story outline** and a **technical specification**.

---

# 🎬 ACT 1 — Diverging Priorities  

**Goal:** Establish that Sports and EPA vehicles begin with fundamentally different priorities.

**Core contrast:**  
- Sports → Performance, luxury, horsepower, price  
- EPA → Efficiency, MPG, emissions reduction, downsizing  

---

# 📊 Visualization 1A — Sports Car Trendlines (HP, Engine Size, Price)

### **Purpose**
Show how sports cars evolve toward *more power and higher prices* over time.

### **Chart Type**
Multi-line chart or small multiples:
- Line 1: Avg Horsepower
- Line 2: Avg Engine Size (L)
- Line 3: Avg Price (separate axis or separate small plot)

---

### **LEFT PANEL CONTROLS ( REQUIRED )**
- **Brand Filter (multi-select dropdown)**  
  - Porsche  
  - Ferrari  
  - BMW  
  - Lamborghini  
  - McLaren  
  - Audi  
  - “Select All”
  
- **Year Range Slider** (e.g., 2000–2025)

- **Metric Toggles (checkboxes)**  
  - Show Horsepower  
  - Show Engine Size  
  - Show Price  

- **Smoothing Toggle**  
  - On = rolling average  
  - Off = raw data  

---

### **INTERACTION REQUIREMENTS**
- Hover tooltip → Display:  
  `Year, Avg HP, Avg Engine Size, Avg Price`
- Legend click → hide/show individual lines  
- Brand highlight → selected brand’s line becomes bolded  
- Year slider → live-updates chart  

---

### **What the User Should Learn**
- Sports cars consistently **increase horsepower**.  
- Prices rise **faster** than performance (luxury premium).  
- Sports cars prioritize performance over efficiency.

---

---

# 📊 Visualization 1B — EPA Trendlines (MPG, CO₂, Displacement)

### **Purpose**
Show everyday vehicles pursue efficiency and emissions reduction.

### **Chart Type**
Multi-line chart:
- Line 1: Avg Combined MPG
- Line 2: Avg CO₂ emissions
- Line 3: Avg Engine Displacement

---

### **LEFT PANEL CONTROLS**
- **Fuel Type Checkboxes**  
  - Gas  
  - Hybrid  
  - EV  
  - Diesel  

- **Year Range Slider**

- **Metric Toggles**  
  - Show MPG  
  - Show CO₂  
  - Show Displacement  

- **Normalization Toggle**  
  - Normalize lines to base year (2000 = 100)

---

### **INTERACTION REQUIREMENTS**
- Hover tooltip with MPG, CO₂, displacement  
- Fuel type filter re-computes yearly averages  
- Toggle visibility of specific lines  

---

### **What the User Should Learn**
- EPA cars get **more efficient** over time.  
- CO₂ emissions **drop** significantly.  
- Engine displacement **shrinks** (downsizing).  

---

---

# 📊 Visualization 1C — Side-by-Side Divergence or Gap Chart

### **Purpose**
Allow direct comparison of the two Act 1 datasets.

### **Option 1: Two stacked panels (recommended)**  
- Top: Sports HP / Engine Size / Price  
- Bottom: EPA MPG / CO₂ / Displacement  
- **Aligned on same x-axis so differences are visual**

### **Option 2: Gap/Index Chart**
- Normalize both markets  
- Show difference in trends (e.g., HP vs MPG)

---

### **LEFT PANEL CONTROLS**
- **Linked Year Slider** for both panels  
- **Normalization Toggle**  
- **Highlight a time period** (brush/drag)

---

### **What the User Should Learn**
- Sports and EPA cars evolve along **opposite priorities**.  
- This sets the foundation for Act 2’s question:  
  → *Can these markets ever converge?*

---

---

# ⚡ ACT 2 — Electrification & Market Shifts (UPDATED)

**Important:**  
Sports dataset has *no EVs*, which becomes a **central narrative point**.

**Act 2’s goal:**  
Show that electrification transforms EPA vehicles while sports cars remain unchanged.

---

# 📊 Visualization 2A — EPA Fuel Share Over Time

### **Purpose**
Show the rapid transition from gas → hybrid → EV.

### **Chart Type**
Stacked area chart:
- Gas  
- Hybrid  
- Plug-in Hybrid  
- EV  
- Diesel (optional)

---

### **LEFT PANEL CONTROLS**
- **Fuel Type On/Off toggles**  
- **Year Slider**  
- **Stacked vs Percentage View Toggle**  
  - Stacked (raw counts)  
  - % of market  

---

### **INTERACTION REQUIREMENTS**
- Hover tooltip: show % breakdown per year  
- Click legend item → isolate single fuel type  
- Animate timeline (optional)

---

### **What User Should Learn**
- Mainstream vehicles shift massively toward electrification.  
- EV era accelerates after ~2015.  
- Sports cars do **not** participate in this shift → one-sided convergence.

---

---

# 📊 Visualization 2B — EPA Performance vs Efficiency Scatter (Hybrid + EV)

### **Purpose**
Show EVs break the old tradeoff between performance & efficiency.

### **Chart Type**
Scatter plot:
- X-axis: Horsepower  
- Y-axis: MPG or MPGe  
- Size: Weight or Price  
- Color: Fuel Type (Gas, Hybrid, EV)

---

### **LEFT PANEL CONTROLS**
- **Fuel Type Filter**  
- **Year Slider**  
- **Show Only EV/Hybrid Toggle**  
- **Brand or Manufacturer Filter** (optional)

---

### **INTERACTION REQUIREMENTS**
- Hover tooltip → model details  
- Lasso/brush selection → highlight vehicles  
- Clicking on a point could open a side panel with stats

---

### **What User Should Learn**
- EV/hybrid vehicles cluster in a “balanced” region of high performance + high efficiency.  
- This cluster **did not exist** in Act 1.

---

### **Act 2 Narrative Message**
> “Electrification creates a new kind of car — powerful and efficient —  
> but sports cars remain traditional. Only EPA vehicles ‘move’ toward the sports market.”

---

---

# 🔮 ACT 3 — Convergence or Coexistence?

**Goal:** Evaluate whether the two markets are moving closer together.

---

# 📊 Visualization 3A — Dual Indices (Performance vs Efficiency)

### **Purpose**
Create a quantitative comparison.

### **Indices Needed**
- **Sports Performance Index**  
  - Normalized HP or 1/(0–60 time)  
- **EPA Efficiency Index**  
  - MPG or inverse CO₂  
- **EPA Performance Index**  
  - HP  
- **Sports Efficiency Proxy**  
  - 1 / Engine Size or similar

### **Chart Type**
- Two synchronized line charts or dual-axis plot.

---

### **LEFT PANEL CONTROLS**
- **Year Slider**  
- **Index Toggles** (show/hide each index)  
- **Normalization Toggle**

---

### **INTERACTION REQUIREMENTS**
- Hover → show all indices for that year  
- Line toggles  
- Period highlight

---

### **What User Should Learn**
- EPA increases performance AND efficiency.  
- Sports increases performance only.  
- The gap narrows from one side only.

---

---

# 📊 Visualization 3B — Market Segmentation / Clustering

### **Purpose**
Use clustering to reveal structural “groups” in the combined market.

### **Clustering Features**
- HP  
- Torque (if available)  
- Engine Size  
- MPG / MPGe / CO₂  
- Price  

---

### **Chart Type**
- 2D scatter after PCA reduction  
- Color = cluster  
- Shape = market (Sports vs EPA)

---

### **LEFT PANEL CONTROLS**
- **K (number of clusters)** toggle  
- **Year Slider**  
- **Feature Selection Checkbox** (HP, MPG, etc.)

---

### **INTERACTION REQUIREMENTS**
- Hover → show vehicle details  
- Click cluster → highlight all models in sidebar  
- Brush-selection → compare characteristics

---

### **What User Should Learn**
- Distinct clusters exist (performance, efficiency).  
- A “bridge” cluster appears only in later years.  
- This is partial, not full convergence.

---

---

# 📊 Visualization 3C — Summary Comparison Table (2000–2005 vs 2018–2025)

### **Purpose**
Make the story concrete with numbers.

### **Metrics**
- Avg HP  
- Avg MPG  
- Avg CO₂  
- Avg Displacement  
- % EV/Hybrid  

### **Features**
- Dropdown to pick comparison windows  
- Clicking a row highlights the corresponding years in charts above

---

### **What User Should Learn**
- EPA vehicles evolve dramatically (MPG ↑, CO₂ ↓, HP ↑).  
- Sports change primarily in HP and price.  
- Convergence is small and asymmetrical.

---

---

# 🎯 FINAL STATEMENT FOR USERS

**Act 1:** The markets begin far apart.  
**Act 2:** Electrification transforms EPA vehicles—but *not* sports cars.  
**Act 3:** Only partial convergence appears; markets remain largely distinct.

