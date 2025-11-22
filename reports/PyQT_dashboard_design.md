# CS439 Final Project — PyQt Dashboard Structure & Design

This document describes the **overall structure**, **per-Act layout**, **control panels**, and **PyQt widget skeleton** for the final dashboard.

---

## 1. Top-Level Structure

### Main Window

- `QMainWindow`
- `QTabWidget` as the central widget
  - **Tab 1:** Act 1 – Diverging Priorities  
  - **Tab 2:** Act 2 – Electrification  
  - **Tab 3:** Act 3 – Convergence vs Coexistence  

Each tab uses the **same basic layout pattern** so the user doesn’t have to re-learn the UI each time.

---

## 2. Per-Act Layout (What Each Tab Looks Like)

Instead of cramming 3 plots side-by-side (which would be tiny), each tab follows this layout:

```text
+-------------------------------------------------------+
| [Tab Bar: Act 1 | Act 2 | Act 3]                      |
+-------------------------------------------------------+
| [Left Control Panel] | [Right: Charts + Narrative]    |
|                      |                                |
|                      |  [ Chart Row 1: 2 charts ]     |
|                      |  [ Chart Row 2: 1 chart + text]|
+-------------------------------------------------------+
```

### Technical Layout

- **Outer layout:** `QHBoxLayout`

- **Left:** `QFrame` or `QWidget` with a `QVBoxLayout`  
  → This is the control panel (sliders, checkboxes, dropdowns).

- **Right:** `QWidget` with a `QVBoxLayout`
  - **Row 1:** `QHBoxLayout` → 2 main charts side by side
  - **Row 2:** `QHBoxLayout` → 1 smaller supporting chart + a text/narrative panel  
    *(or 1 chart centered with a text widget beside it)*

So per Act you have:

- **2 big plots (top row)**  
- **1 supporting plot + text box (bottom row)**  

instead of 3 tiny plots squeezed into one row.

---

## 3. What Goes Where (Per Act)

---

# 🔹 Act 1 Tab – Diverging Priorities

**Goal:** Show that sports cars and EPA vehicles start with very different priorities.

---

### Left Control Panel (Act 1)

Controls:

- **Year range slider** (shared by both datasets)

- **Checkboxes:**
  - Show Sports lines (HP, Engine Size, Price)
  - Show EPA lines (MPG, CO₂, Displacement)

- **Brand dropdown for sports** (multi-select or single-select):
  - Porsche, Ferrari, Lamborghini, McLaren, Audi, BMW, etc.

- **Normalization toggle** (off / on):
  - Normalize lines to a base year.

---

### Right Side Layout (Act 1)

#### Row 1 — Two Big Charts

---

### **Chart 1A – Sports Trendlines**

- Type: Multi-line chart  
- Implementation: `FigureCanvas` for Matplotlib  
- Lines:
  - Avg Horsepower
  - Avg Engine Size (L)
  - Avg Price  
- Controlled by:
  - Year slider  
  - Sports lines checkbox  
  - Brand dropdown  
  - Normalization toggle

---

### **Chart 1B – EPA Trendlines**

- Type: Multi-line chart  
- Implementation: `FigureCanvas`  
- Lines:
  - Avg MPG  
  - Avg CO₂ emissions  
  - Avg Engine Displacement  
- Controlled by:
  - Year slider  
  - EPA lines checkbox  
  - Normalization toggle

---

#### Row 2 — Comparative + Narrative

---

### **Chart 1C – Comparison / Gap Chart**

**Purpose:** Directly compare sports vs EPA evolution.

Two options:
- Normalized indices vs year  
**or**  
- Side-by-side mini panels with aligned timelines

Implementation: `FigureCanvas`.

---

### **Narrative Panel (Act 1)**

- Type: `QTextEdit` (read-only) or `QLabel`
- Content examples:
  - “Sports prioritize performance and luxury (HP and price rising).”
  - “EPA vehicles prioritize efficiency and emissions reduction.”
  - “The two markets evolve along different priorities.”

---

# 🔹 Act 2 Tab – Electrification (Updated, EPA-Focused)

**Goal:** Show how electrification reshapes EPA vehicles while sports cars in the dataset remain non-EV.

---

### Left Control Panel (Act 2)

Controls:

- **Fuel type checkboxes:**
  - Gas  
  - Hybrid  
  - EV  
  - Diesel  

- **Year slider**

- **Toggle: raw counts vs % share**
  - Mode 1: raw counts by fuel type  
  - Mode 2: percentage share by year  

- **Toggle: “Show only Hybrids/EVs in scatter”**
  - Highlights only electrified vehicles

---

### Right Side Layout (Act 2)

#### Row 1

---

### **Chart 2A – Fuel Share Over Time**

- Type: stacked area chart  
- Categories:
  - Gas  
  - Hybrid  
  - EV  
  - (Optional Diesel)
- Implementation: `FigureCanvas`
- Controlled by:
  - Fuel type checkboxes  
  - Year slider  
  - Raw vs % toggle  

---

### **Chart 2B – EPA Performance vs Efficiency Scatter**

- Type: scatter plot  
- Axes:
  - X: Horsepower  
  - Y: MPG or MPGe  
- Color = fuel type  
- Hover/click to inspect vehicle  
- Controlled by:
  - Fuel type checkboxes  
  - Year slider  
  - “Show only Hybrids/EVs” toggle  

---

#### Row 2

---

### **Small Supporting Chart or Table**

Examples:
- Line chart: avg HP for EVs vs Gas over time  
- Mini table:
  - “Pre-EV era” vs “EV era”
  - e.g., 2000–2008 vs 2015–2025 metrics  

---

### **Narrative Box (Act 2)**

- Type: `QTextEdit` or `QLabel`
- Text examples:
  - “Electrification transforms EPA vehicles.”
  - “Sports cars in our dataset remain non-EV.”
  - “Sports dataset includes no EVs; this contrast is intentional.”

---

# 🔹 Act 3 Tab – Convergence or Coexistence?

**Goal:** Determine whether the two markets converge or remain structurally distinct.

---

### Left Control Panel (Act 3)

Controls:

- **Year slider**  
  Pick early vs late windows (e.g., 2000–2005 vs 2018–2025)

- **Index checkboxes:**
  - Sports Performance Index  
  - EPA Performance Index  
  - EPA Efficiency Index  
  - Sports Efficiency Proxy  

- **Cluster settings:**
  - `K` dropdown (3–5 clusters)
  - Filter:
    - Show Sports  
    - Show EPA  
    - Show Both  

---

### Right Side Layout (Act 3)

#### Row 1

---

### **Chart 3A – Indices over Time**

- Type: multi-line chart
- Lines:
  - Selected indices vs year
- Controlled by:
  - Index checkboxes  
  - Year slider  

Purpose: Show how performance & efficiency indices evolve across markets.

---

### **Chart 3C – Summary Table or Bar Chart**

Types:
- `QTableView`  
**or**
- Bar chart (`FigureCanvas`)

Content:
- Compare:
  - 2000–2005 averages  
  - 2018–2025 averages  
- Metrics:
  - Avg HP  
  - Avg MPG  
  - Avg CO₂  
  - Avg displacement  
  - % EV/Hybrid  

---

#### Row 2

---

### **Chart 3B – Cluster Plot (Combined Market)**

- Type: 2D scatter (PCA-reduced)
- Axes:
  - PC1  
  - PC2  
- Color = cluster label  
- Shape = market (Sports vs EPA)
- Purpose:
  - Identify whether clusters overlap or remain separate
  - Find any “bridge” cluster in later years  

---

### **Narrative Box (Act 3)**

Examples:
- “We see partial convergence via an EV/hybrid ‘bridge’ cluster.”
- “Markets remain mostly distinct overall.”
- “EPA vehicles move toward performance; sports cars do not move toward efficiency as much.”

---

## 4. PyQt Widget Structure (How You’d Implement It)

### High-Level Skeleton

```python
from PyQt5.QtWidgets import QMainWindow, QTabWidget, QWidget, QHBoxLayout, QVBoxLayout

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        tabs = QTabWidget()

        tabs.addTab(self.build_act1_tab(), "Act 1: Diverging Priorities")
        tabs.addTab(self.build_act2_tab(), "Act 2: Electrification")
        tabs.addTab(self.build_act3_tab(), "Act 3: Convergence?")

        self.setCentralWidget(tabs)

    def build_act1_tab(self):
        root = QWidget()
        layout = QHBoxLayout(root)

        # Left: control panel
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)

        # TODO: add sliders, checkboxes, dropdowns for Act 1
        # e.g., year slider, brand dropdown, normalization toggle

        # Right: charts + narrative
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)

        # Row 1: 2 main charts
        row1 = QWidget()
        row1_layout = QHBoxLayout(row1)
        # TODO: add FigureCanvas widgets for Chart 1A and Chart 1B

        # Row 2: 1 supporting chart + text
        row2 = QWidget()
        row2_layout = QHBoxLayout(row2)
        # TODO: add FigureCanvas for Chart 1C and a QTextEdit/QLabel for narrative

        right_layout.addWidget(row1)
        right_layout.addWidget(row2)

        layout.addWidget(left_panel)
        layout.addWidget(right_panel)

        root.setLayout(layout)
        return root

    def build_act2_tab(self):
        root = QWidget()
        layout = QHBoxLayout(root)

        # Left: control panel for Act 2
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        # TODO: add fuel type checkboxes, year slider, toggles

        # Right: charts + narrative for Act 2
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)

        # Row 1: Chart 2A + Chart 2B
        row1 = QWidget()
        row1_layout = QHBoxLayout(row1)
        # TODO: add FigureCanvas for Chart 2A and Chart 2B

        # Row 2: supporting chart/table + narrative box
        row2 = QWidget()
        row2_layout = QHBoxLayout(row2)
        # TODO: add supporting FigureCanvas or table + QTextEdit/QLabel

        right_layout.addWidget(row1)
        right_layout.addWidget(row2)

        layout.addWidget(left_panel)
        layout.addWidget(right_panel)

        root.setLayout(layout)
        return root

    def build_act3_tab(self):
        root = QWidget()
        layout = QHBoxLayout(root)

        # Left: control panel for Act 3
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        # TODO: add year slider, index checkboxes, cluster controls

        # Right: charts + narrative for Act 3
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)

        # Row 1: Chart 3A + Chart 3C
        row1 = QWidget()
        row1_layout = QHBoxLayout(row1)
        # TODO: add FigureCanvas for Chart 3A and Chart 3C (or table widget)

        # Row 2: Chart 3B + narrative box
        row2 = QWidget()
        row2_layout = QHBoxLayout(row2)
        # TODO: add FigureCanvas for Chart 3B + QTextEdit/QLabel

        right_layout.addWidget(row1)
        right_layout.addWidget(row2)

        layout.addWidget(left_panel)
        layout.addWidget(right_panel)

        root.setLayout(layout)
        return root
```

Charts will be embedded using `FigureCanvasQTAgg(fig)` from Matplotlib.

You can later wire in callbacks so that control panel widgets update the figures.

---

## 5. TL;DR Design Answer

- The final deliverable **should be** a **PyQt dashboard with 3 tabs**:
  - Act 1, Act 2, Act 3.

- For each Act, **do NOT** put 3 tiny charts side-by-side.

### Instead use:

- **Left:** control panel (sliders, checkboxes, dropdowns)  
- **Right / Row 1:** two large charts  
- **Right / Row 2:** one supporting chart + narrative text  

This layout keeps the dashboard clean, readable, and aligned with your storytelling structure.

