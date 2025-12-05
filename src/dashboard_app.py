import sys

import pandas as pd
import matplotlib.pyplot as plt

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QFrame,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QSlider,
    QSpinBox,
    QTabWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# 🔹 IMPORTANT: match your actual function name in plots_epa.py
from plots_epa import (
    make_epa_trend_figure,
    compute_epa_yearly_aggregates,
    make_epa_fuel_share_figure,
    compute_fuel_share_by_year,
    make_epa_performance_efficiency_scatter,
)

from plots_sports import (
    compute_sports_yearly_aggregates,
    make_sports_trend_figure,
)

from plots_act3 import make_indices_chart


# ---------- Helpers to load EPA data ----------


def load_epa_data():
    """
    Load the preprocessed EPA dataset WITH horsepower data.
    Sports cars have already been removed during cleaning.

    Returns
    -------
    pd.DataFrame
        Cleaned EPA dataframe with HP and 0-60 time columns.
        Sports cars already filtered out.
    """
    try:
        df = pd.read_csv("../data/cleaned/epa_with_hp_clean.csv")
        print(f"Loaded EPA dataset: {len(df)} mainstream vehicles (sports cars already removed)")
        return df
    except Exception as e:
        print(f"Error loading EPA data: {e}")
        raise


def load_sports_data():
    """
    Load the sports car dataset WITH MPG data.

    Returns
    -------
    pd.DataFrame
        Cleaned sports car dataframe with MPG column.
    """
    try:
        df = pd.read_csv("../data/cleaned/sports_with_mpg_clean.csv")
        print(f"Loaded sports dataset: {len(df)} sports cars with MPG data")
        return df
    except Exception as e:
        print(f"Error loading sports data: {e}")
        raise


# ---------- UI Components ----------


class ChartPlaceholder(QFrame):
    """
    Simple placeholder widget for charts.
    Replace this with a FigureCanvasQTAgg later.
    """

    def __init__(self, title: str, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)

        layout = QVBoxLayout(self)
        label_title = QLabel(title)
        label_title.setAlignment(Qt.AlignCenter)
        label_title.setStyleSheet("font-weight: bold;")
        layout.addWidget(label_title)

        label_hint = QLabel("Visualization placeholder")
        label_hint.setAlignment(Qt.AlignCenter)
        label_hint.setStyleSheet("color: gray; font-size: 10pt;")
        layout.addWidget(label_hint)


class ControlPanel(QWidget):
    """
    Universal left-side control panel shared by all Acts.
    Some controls will be more relevant in certain tabs, but
    all are available for simplicity.
    """

    def __init__(self, parent=None, year_min_default=2011, year_max_default=2024):
        super().__init__(parent)

        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignTop)

        # --- Year range controls ---
        year_group = QGroupBox("Year Range")
        year_layout = QHBoxLayout()
        self.year_min_spin = QSpinBox()
        self.year_max_spin = QSpinBox()
        self.year_min_spin.setRange(2011, 2024)
        self.year_max_spin.setRange(2011, 2024)
        self.year_min_spin.setValue(year_min_default)
        self.year_max_spin.setValue(year_max_default)

        # Connect validation to ensure min <= max
        self.year_min_spin.valueChanged.connect(self._validate_year_range)
        self.year_max_spin.valueChanged.connect(self._validate_year_range)

        year_layout.addWidget(QLabel("Min:"))
        year_layout.addWidget(self.year_min_spin)
        year_layout.addWidget(QLabel("Max:"))
        year_layout.addWidget(self.year_max_spin)
        year_group.setLayout(year_layout)
        main_layout.addWidget(year_group)

        # --- Sports options ---
        sports_group = QGroupBox("Sports Car Options")
        sports_layout = QVBoxLayout()

        self.chk_show_sports = QCheckBox("Show Sports Lines")
        self.chk_show_sports.setChecked(True)
        sports_layout.addWidget(self.chk_show_sports)

        sports_brand_layout = QHBoxLayout()
        sports_brand_layout.addWidget(QLabel("Brand:"))
        self.cmb_sports_brand = QComboBox()
        self.cmb_sports_brand.addItem("All Brands")
        self.cmb_sports_brand.addItems(
            ["Porsche", "Ferrari", "Lamborghini", "McLaren", "Audi", "BMW"]
        )
        sports_brand_layout.addWidget(self.cmb_sports_brand)
        sports_layout.addLayout(sports_brand_layout)

        self.chk_normalize = QCheckBox("Normalize to base year")
        self.chk_normalize.setChecked(True)  # Enabled by default
        sports_layout.addWidget(self.chk_normalize)

        sports_group.setLayout(sports_layout)
        main_layout.addWidget(sports_group)

        # --- EPA options ---
        epa_group = QGroupBox("EPA / Fuel Type Options")
        epa_layout = QVBoxLayout()

        self.chk_show_epa = QCheckBox("Show EPA Lines")
        self.chk_show_epa.setChecked(True)
        epa_layout.addWidget(self.chk_show_epa)

        fuel_layout = QGridLayout()
        self.chk_gas = QCheckBox("Gasoline")
        self.chk_electric = QCheckBox("Electric")
        self.chk_gas.setChecked(True)
        self.chk_electric.setChecked(True)

        fuel_layout.addWidget(self.chk_gas, 0, 0)
        fuel_layout.addWidget(self.chk_electric, 0, 1)
        epa_layout.addLayout(fuel_layout)

        self.chk_show_only_electrified = QCheckBox("Show only Electric")
        epa_layout.addWidget(self.chk_show_only_electrified)

        self.chk_raw_vs_percent = QCheckBox("Use % share")
        epa_layout.addWidget(self.chk_raw_vs_percent)

        epa_group.setLayout(epa_layout)
        main_layout.addWidget(epa_group)

        # --- Index & clustering options (Act 3 style) ---
        index_group = QGroupBox("Indices & Clustering (Act 3)")
        index_layout = QVBoxLayout()

        self.chk_idx_sports_perf = QCheckBox("Sports Performance Index")
        self.chk_idx_epa_perf = QCheckBox("EPA Performance Index")
        self.chk_idx_epa_eff = QCheckBox("EPA Efficiency Index")
        self.chk_idx_sports_eff = QCheckBox("Sports Efficiency Proxy")

        for chk in [
            self.chk_idx_sports_perf,
            self.chk_idx_epa_perf,
            self.chk_idx_epa_eff,
            self.chk_idx_sports_eff,
        ]:
            chk.setChecked(True)
            index_layout.addWidget(chk)

        cluster_row = QHBoxLayout()
        cluster_row.addWidget(QLabel("Clusters (K):"))
        self.cmb_k = QComboBox()
        self.cmb_k.addItems(["3", "4", "5"])
        cluster_row.addWidget(self.cmb_k)
        index_layout.addLayout(cluster_row)

        market_row = QHBoxLayout()
        market_row.addWidget(QLabel("Market filter:"))
        self.cmb_market_filter = QComboBox()
        self.cmb_market_filter.addItems(["Both", "Sports only", "EPA only"])
        market_row.addWidget(self.cmb_market_filter)
        index_layout.addLayout(market_row)

        index_group.setLayout(index_layout)
        main_layout.addWidget(index_group)

        # --- Apply / Reset buttons (hooks for future logic) ---
        button_row = QHBoxLayout()
        self.btn_apply = QPushButton("Apply Filters")
        self.btn_reset = QPushButton("Reset")
        button_row.addWidget(self.btn_apply)
        button_row.addWidget(self.btn_reset)
        main_layout.addLayout(button_row)

        # Spacer to push everything up
        main_layout.addStretch(1)

    def _validate_year_range(self):
        """
        Ensure year_min <= year_max. If user violates this, auto-correct.
        """
        min_val = self.year_min_spin.value()
        max_val = self.year_max_spin.value()

        if min_val > max_val:
            # Block signals temporarily to avoid recursion
            self.year_min_spin.blockSignals(True)
            self.year_max_spin.blockSignals(True)

            # Auto-correct: set min to max
            self.year_min_spin.setValue(max_val)

            self.year_min_spin.blockSignals(False)
            self.year_max_spin.blockSignals(False)


class ActTab(QWidget):
    """
    Generic tab for Act 2 and Act 3 with:
    - left control panel
    - right side: two charts (top row) + one main chart (bottom row)
    """

    def __init__(self, act_name: str, parent=None, year_min_default=2011, year_max_default=2024):
        super().__init__(parent)
        self.act_name = act_name
        self.year_min_default = year_min_default
        self.year_max_default = year_max_default
        self._build_ui()

    def _build_ui(self):
        root_layout = QHBoxLayout(self)
        root_layout.setSpacing(5)  # Reduce spacing between sidebar and charts
        root_layout.setContentsMargins(5, 5, 5, 5)  # Reduce margins

        # Left: universal control panel (narrow)
        self.control_panel = ControlPanel(
            year_min_default=self.year_min_default,
            year_max_default=self.year_max_default
        )
        self.control_panel.setMaximumWidth(250)  # Limit width
        root_layout.addWidget(self.control_panel, stretch=0)

        # Right: charts + narrative
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setSpacing(5)  # Reduce vertical spacing

        # Row 1: two side-by-side visualizations
        row1 = QWidget()
        row1_layout = QHBoxLayout(row1)
        row1_layout.setSpacing(5)  # Reduce spacing between charts
        row1_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins

        # Placeholders for the top two charts
        self.chart_top_left = ChartPlaceholder(f"{self.act_name} - Top Left Chart")
        self.chart_top_right = ChartPlaceholder(f"{self.act_name} - Top Right Chart")

        row1_layout.addWidget(self.chart_top_left)
        row1_layout.addWidget(self.chart_top_right)

        # Row 2: one main comparison visualization
        row2 = QWidget()
        row2_layout = QHBoxLayout(row2)
        row2_layout.setSpacing(5)  # Reduce spacing
        row2_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins

        self.chart_bottom_main = ChartPlaceholder(f"{self.act_name} - Main Comparison Chart")
        row2_layout.addWidget(self.chart_bottom_main)

        # Optional: narrative box on the right of the bottom chart
        self.narrative_box = QTextEdit()
        self.narrative_box.setReadOnly(True)
        self.narrative_box.setMinimumWidth(220)
        self.narrative_box.setPlainText(
            f"This is the narrative area for {self.act_name}.\n\n"
            "You can describe what the user should notice in these visualizations here."
        )
        row2_layout.addWidget(self.narrative_box)

        # Add rows to right layout
        right_layout.addWidget(row1, stretch=2)
        right_layout.addWidget(row2, stretch=3)

        root_layout.addWidget(right_panel, stretch=1)


class Act1Tab(QWidget):
    """
    Specialized tab for Act 1:
    - Left: universal control panel
    - Right / Row 1:
        * Top-left: placeholder for sports trendlines (1A)
        * Top-right: EPA trendlines (1B) using plots_epa.make_epa_trend_figure
    - Right / Row 2:
        * Bottom-left: placeholder for comparison chart (1C)
        * Bottom-right: narrative text
    """

    def __init__(self, sports_df: pd.DataFrame, epa_df: pd.DataFrame, parent=None):
        super().__init__(parent)
        self.act_name = "Act 1: Diverging Priorities"
        self.sports_df = sports_df
        self.epa_df = epa_df
        self._build_ui()
        self._connect_signals()
        self.update_sports_trendlines_chart()
        self.update_epa_trendlines_chart()
        self.update_comparison_chart()

    def _build_ui(self):
        root_layout = QHBoxLayout(self)
        root_layout.setSpacing(5)  # Reduce spacing between sidebar and charts
        root_layout.setContentsMargins(5, 5, 5, 5)  # Reduce margins

        # Left: universal control panel (narrow)
        self.control_panel = ControlPanel()
        self.control_panel.setMaximumWidth(250)  # Limit width
        root_layout.addWidget(self.control_panel, stretch=0)

        # Right: charts + narrative
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setSpacing(5)  # Reduce vertical spacing

        # Row 1: two side-by-side visualizations
        row1 = QWidget()
        row1_layout = QHBoxLayout(row1)
        row1_layout.setSpacing(5)  # Reduce spacing between charts
        row1_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins

        # Top-left: Sports trendlines chart (1A)
        self.sports_figure = Figure(figsize=(6, 5.5))
        self.canvas_sports = FigureCanvas(self.sports_figure)
        row1_layout.addWidget(self.canvas_sports)

        # Top-right: EPA trendlines chart (1B)
        self.epa_figure = Figure(figsize=(6, 5.5))
        self.canvas_epa = FigureCanvas(self.epa_figure)
        row1_layout.addWidget(self.canvas_epa)

        # Row 2: one main comparison visualization + narrative
        row2 = QWidget()
        row2_layout = QHBoxLayout(row2)
        row2_layout.setSpacing(5)  # Reduce spacing
        row2_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins

        # Bottom-left: comparison chart (1C) - two stacked panels
        self.comparison_figure = Figure(figsize=(8, 5))
        self.canvas_comparison = FigureCanvas(self.comparison_figure)
        row2_layout.addWidget(self.canvas_comparison)

        # Bottom-right: narrative box
        self.narrative_box = QTextEdit()
        self.narrative_box.setReadOnly(True)
        self.narrative_box.setMinimumWidth(220)
        self.narrative_box.setPlainText(
            "Act 1 Narrative:\n\n"
            "- Sports cars prioritize performance and luxury.\n"
            "- EPA vehicles prioritize efficiency and emissions.\n"
            "- This chart (1B) shows how MPG, CO₂, and engine size evolve over time."
        )
        row2_layout.addWidget(self.narrative_box)

        # Add rows to right layout
        right_layout.addWidget(row1, stretch=2)
        right_layout.addWidget(row2, stretch=3)

        root_layout.addWidget(right_panel, stretch=1)

    # ---------- Sports trendlines wiring ----------

    def update_sports_trendlines_chart(self):
        """
        Rebuild the sports trendlines figure using the current control panel settings.
        """
        cp = self.control_panel

        year_min = cp.year_min_spin.value()
        year_max = cp.year_max_spin.value()
        normalize = cp.chk_normalize.isChecked()
        show_sports = cp.chk_show_sports.isChecked()

        # For now, we'll show all three metrics (HP, Engine, Price)
        # You can add individual toggles later if needed
        show_hp = show_sports
        show_engine = show_sports
        show_price = show_sports

        # Get selected brand from dropdown
        selected_brand = cp.cmb_sports_brand.currentText()
        if selected_brand == "All Brands":
            brands = None
        else:
            brands = [selected_brand]

        # Clear all axes from the existing figure
        self.sports_figure.clear()

        # Get yearly aggregates with brand filtering
        yearly = compute_sports_yearly_aggregates(
            self.sports_df,
            year_min,
            year_max,
            brands=brands
        )
        plot_df = yearly.copy()

        # Apply normalization if requested
        if normalize:
            for col in ["Horsepower", "Engine Size (L)", "Price (in USD)"]:
                if col in plot_df.columns:
                    non_null = plot_df[col].dropna()
                    if len(non_null) > 0:
                        first_valid = non_null.iloc[0]
                        if first_valid != 0:
                            plot_df[col] = (plot_df[col] / first_valid) * 100.0

        # Create a new axis on the existing figure
        ax = self.sports_figure.add_subplot(111)

        # Check if at least one metric is enabled
        if not (show_hp or show_engine or show_price):
            ax.text(
                0.5, 0.5,
                "No metrics selected\n\nPlease enable sports metrics\nto view the visualization",
                ha='center', va='center',
                fontsize=12, color='gray',
                transform=ax.transAxes
            )
            ax.set_xlabel("Year")
            ax.set_ylabel("Value")
            ax.set_title("Sports Car Trendlines: Performance & Price Over Time")
            ax.grid(True, alpha=0.3)
        else:
            # Plot lines based on flags
            if show_hp and "Horsepower" in plot_df.columns:
                ax.plot(
                    plot_df["Year"],
                    plot_df["Horsepower"],
                    label="Avg Horsepower",
                    linewidth=2,
                    color="#d62728",  # Red
                )

            if show_engine and "Engine Size (L)" in plot_df.columns:
                ax.plot(
                    plot_df["Year"],
                    plot_df["Engine Size (L)"],
                    label="Avg Engine Size (L)",
                    linewidth=2,
                    color="#ff7f0e",  # Orange
                )

            if show_price and "Price (in USD)" in plot_df.columns:
                ax.plot(
                    plot_df["Year"],
                    plot_df["Price (in USD)"],
                    label="Avg Price (USD)",
                    linewidth=2,
                    color="#2ca02c",  # Green
                )

            ax.set_xlabel("Year", fontsize=11)
            if normalize:
                ax.set_ylabel("Index (base year = 100)", fontsize=11)
            else:
                ax.set_ylabel("Value (units vary by line)", fontsize=11)
            ax.set_title("Sports Car Trendlines: Performance & Price Over Time", fontsize=12)
            ax.legend(fontsize=9, loc='best', framealpha=0.9)
            ax.grid(True, alpha=0.3)

        self.sports_figure.tight_layout(pad=2.5)  # Add padding to prevent cutoff
        self.canvas_sports.draw()

    # ---------- EPA trendlines wiring (uses your make_epa_trend_figure) ----------

    def update_epa_trendlines_chart(self):
        """
        Rebuild the EPA trendlines figure using the current control panel settings
        and draw it on the canvas.
        """
        cp = self.control_panel

        year_min = cp.year_min_spin.value()
        year_max = cp.year_max_spin.value()
        normalize = cp.chk_normalize.isChecked()
        show_epa = cp.chk_show_epa.isChecked()

        # Right now, we toggle all three EPA lines with one checkbox.
        show_mpg = show_epa
        show_co2 = show_epa
        show_disp = show_epa

        # Define fuel type groupings
        gas_types = ['Regular', 'Premium', 'Midgrade', 'Gasoline or E85',
                     'Premium or E85', 'Diesel', 'Gasoline or natural gas', 'CNG']
        electric_types = ['Electricity', 'Regular Gas and Electricity',
                         'Premium Gas or Electricity', 'Premium and Electricity',
                         'Regular Gas or Electricity']

        # Collect selected fuel types based on checkboxes
        selected_fuel_types = []
        if cp.chk_gas.isChecked():
            selected_fuel_types.extend(gas_types)
        if cp.chk_electric.isChecked():
            selected_fuel_types.extend(electric_types)

        # Clear all axes from the existing figure
        self.epa_figure.clear()

        # Get yearly aggregates directly with fuel type filtering
        yearly = compute_epa_yearly_aggregates(
            self.epa_df,
            year_min,
            year_max,
            fuel_types=selected_fuel_types if selected_fuel_types else None
        )
        plot_df = yearly.copy()

        # Apply normalization if requested
        if normalize:
            for col in [
                "Combined Mpg For Fuel Type1",
                "Co2  Tailpipe For Fuel Type1",
                "Engine displacement",
            ]:
                if col in plot_df.columns:
                    non_null = plot_df[col].dropna()
                    if len(non_null) > 0:
                        first_valid = non_null.iloc[0]
                        if first_valid != 0:
                            plot_df[col] = (plot_df[col] / first_valid) * 100.0

        # Create a new axis on the existing figure
        ax = self.epa_figure.add_subplot(111)

        # Check if at least one metric is enabled
        if not (show_mpg or show_co2 or show_disp):
            ax.text(
                0.5, 0.5,
                "No metrics selected\n\nPlease enable at least one metric\nto view the visualization",
                ha='center', va='center',
                fontsize=12, color='gray',
                transform=ax.transAxes
            )
            ax.set_xlabel("Year")
            ax.set_ylabel("Value")
            ax.set_title("EPA Trendlines: Efficiency & Engine Size Over Time")
            ax.grid(True, alpha=0.3)
        else:
            # Plot lines based on flags
            if show_mpg and "Combined Mpg For Fuel Type1" in plot_df.columns:
                ax.plot(
                    plot_df["Year"],
                    plot_df["Combined Mpg For Fuel Type1"],
                    label="Avg Combined MPG",
                    linewidth=2,
                )

            if show_co2 and "Co2  Tailpipe For Fuel Type1" in plot_df.columns:
                ax.plot(
                    plot_df["Year"],
                    plot_df["Co2  Tailpipe For Fuel Type1"],
                    label="Avg Tailpipe CO₂ (g/mi)",
                    linewidth=2,
                )

            if show_disp and "Engine displacement" in plot_df.columns:
                ax.plot(
                    plot_df["Year"],
                    plot_df["Engine displacement"],
                    label="Avg Engine Displacement (L)",
                    linewidth=2,
                )

            ax.set_xlabel("Year", fontsize=11)
            if normalize:
                ax.set_ylabel("Index (base year = 100)", fontsize=11)
            else:
                ax.set_ylabel("Value (units vary by line)", fontsize=11)
            ax.set_title("EPA Trendlines: Efficiency & Engine Size Over Time", fontsize=12)
            ax.legend(fontsize=9, loc='best', framealpha=0.9)
            ax.grid(True, alpha=0.3)

        self.epa_figure.tight_layout(pad=2.5)  # Add padding to prevent cutoff
        self.canvas_epa.draw()

    # ---------- Comparison chart (1C) wiring ----------

    def update_comparison_chart(self):
        """
        Rebuild the comparison chart (1C) showing diverging priorities.
        Slope chart: Start year vs End year showing how metrics change.
        """
        cp = self.control_panel

        year_min = cp.year_min_spin.value()
        year_max = cp.year_max_spin.value()

        # Clear the figure
        self.comparison_figure.clear()
        ax = self.comparison_figure.add_subplot(111)

        # Get sports data
        sports_brand = cp.cmb_sports_brand.currentText()
        sports_brands = None if sports_brand == "All Brands" else [sports_brand]
        sports_yearly = compute_sports_yearly_aggregates(
            self.sports_df, year_min, year_max, brands=sports_brands
        )

        # Get EPA data
        gas_types = ['Regular', 'Premium', 'Midgrade', 'Gasoline or E85',
                     'Premium or E85', 'Diesel', 'Gasoline or natural gas', 'CNG']
        electric_types = ['Electricity', 'Regular Gas and Electricity',
                         'Premium Gas or Electricity', 'Premium and Electricity',
                         'Regular Gas or Electricity']
        selected_fuel_types = []
        if cp.chk_gas.isChecked():
            selected_fuel_types.extend(gas_types)
        if cp.chk_electric.isChecked():
            selected_fuel_types.extend(electric_types)

        epa_yearly = compute_epa_yearly_aggregates(
            self.epa_df, year_min, year_max,
            fuel_types=selected_fuel_types if selected_fuel_types else None
        )

        # Check if we have data
        if len(sports_yearly) == 0 or len(epa_yearly) == 0:
            ax.text(0.5, 0.5, "No data available for selected filters",
                   ha='center', va='center', fontsize=12, color='gray',
                   transform=ax.transAxes)
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            self.comparison_figure.tight_layout(pad=1.5)
            self.canvas_comparison.draw()
            return

        # Get first and last year data (normalize to start = 100)
        metrics_data = []
        y_position = 0

        # Sports metrics - all GREEN to show performance/luxury priority
        sports_color = "#2ca02c"  # Green
        sports_metrics = [
            ("Engine Size (L)", "Engine Size", False),
            ("Horsepower", "Horsepower", False),
            ("0-60 MPH Time (seconds)", "Acceleration (0-60)", True)  # Inverted: lower is better
        ]

        for col, label, invert in sports_metrics:
            if col in sports_yearly.columns:
                values = sports_yearly[col].dropna()
                if len(values) >= 2:
                    start_val = values.iloc[0]
                    end_val = values.iloc[-1]
                    if start_val != 0:
                        start_norm = 100
                        if invert:
                            # For inverted metrics (lower is better), flip the ratio
                            end_norm = (start_val / end_val) * 100
                            display_label = f"{label} (inverted)"
                        else:
                            display_label = label
                            end_norm = (end_val / start_val) * 100
                        metrics_data.append({
                            'label': display_label,
                            'start': start_norm,
                            'end': end_norm,
                            'y': y_position,
                            'color': sports_color,
                            'market': 'Sports'
                        })
                        y_position += 1

        y_position += 0.5  # Add gap between markets

        # EPA metrics - all RED to show efficiency/environmental priority
        epa_color = "#d62728"  # Red
        epa_metrics = [
            ("Engine displacement", "Engine Size", False),
            ("Combined Mpg For Fuel Type1", "Efficiency (MPG)", False),
            ("Co2  Tailpipe For Fuel Type1", "Emissions (CO₂)", True)  # Inverted: lower is better
        ]

        for col, label, invert in epa_metrics:
            if col in epa_yearly.columns:
                values = epa_yearly[col].dropna()
                if len(values) >= 2:
                    start_val = values.iloc[0]
                    end_val = values.iloc[-1]
                    if start_val != 0:
                        start_norm = 100
                        if invert:
                            # For inverted metrics (lower is better), flip the ratio
                            end_norm = (start_val / end_val) * 100
                            display_label = f"{label} (inverted)"
                        else:
                            display_label = label
                            end_norm = (end_val / start_val) * 100
                        metrics_data.append({
                            'label': display_label,
                            'start': start_norm,
                            'end': end_norm,
                            'y': y_position,
                            'color': epa_color,
                            'market': 'EPA'
                        })
                        y_position += 1

        # Draw slope lines
        for metric in metrics_data:
            # Draw line from start to end
            ax.plot([0, 1], [metric['start'], metric['end']],
                   color=metric['color'], linewidth=2.5, alpha=0.8,
                   marker='o', markersize=8)

            # Label on left (start)
            ax.text(-0.05, metric['start'], f"{metric['start']:.0f}",
                   ha='right', va='center', fontsize=9, color=metric['color'])

            # Label on right (end)
            ax.text(1.05, metric['end'], f"{metric['end']:.0f}",
                   ha='left', va='center', fontsize=9, color=metric['color'])

            # Metric name on far right
            ax.text(1.15, metric['end'], metric['label'],
                   ha='left', va='center', fontsize=9,
                   color=metric['color'], weight='bold')

        # Styling
        ax.set_xlim(-0.2, 1.4)
        ax.set_ylim(min([m['start'] for m in metrics_data] + [m['end'] for m in metrics_data]) - 10,
                   max([m['start'] for m in metrics_data] + [m['end'] for m in metrics_data]) + 10)

        ax.set_xticks([0, 1])
        ax.set_xticklabels([f'{year_min}', f'{year_max}'], fontsize=11, weight='bold')
        ax.set_yticks([])  # Hide y-axis ticks

        ax.spines['left'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(True)

        ax.set_title("Diverging Priorities: Performance vs. Efficiency\n(Normalized: Start Year = 100, Higher = Better)",
                    fontsize=12, pad=20)

        # Add color-coded legend
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='#2ca02c', label='Sports Cars (Performance)'),
            Patch(facecolor='#d62728', label='EPA Vehicles (Efficiency)')
        ]
        ax.legend(handles=legend_elements, loc='upper left', fontsize=9, framealpha=0.9)

        ax.grid(True, axis='x', alpha=0.3, linestyle='--')

        self.comparison_figure.tight_layout(pad=1.5)
        self.canvas_comparison.draw()

    def _connect_signals(self):
        """
        Connect relevant control panel signals to both charts.
        """
        cp = self.control_panel

        # Sports chart signals
        cp.year_min_spin.valueChanged.connect(self.update_sports_trendlines_chart)
        cp.year_max_spin.valueChanged.connect(self.update_sports_trendlines_chart)
        cp.chk_show_sports.stateChanged.connect(self.update_sports_trendlines_chart)
        cp.chk_normalize.stateChanged.connect(self.update_sports_trendlines_chart)
        cp.cmb_sports_brand.currentIndexChanged.connect(self.update_sports_trendlines_chart)

        # EPA chart signals
        cp.year_min_spin.valueChanged.connect(self.update_epa_trendlines_chart)
        cp.year_max_spin.valueChanged.connect(self.update_epa_trendlines_chart)
        cp.chk_show_epa.stateChanged.connect(self.update_epa_trendlines_chart)
        cp.chk_normalize.stateChanged.connect(self.update_epa_trendlines_chart)

        # Fuel-type checkboxes for filtering
        cp.chk_gas.stateChanged.connect(self.update_epa_trendlines_chart)
        cp.chk_electric.stateChanged.connect(self.update_epa_trendlines_chart)

        # Comparison chart (1C) signals - updates when any control changes
        cp.year_min_spin.valueChanged.connect(self.update_comparison_chart)
        cp.year_max_spin.valueChanged.connect(self.update_comparison_chart)
        cp.chk_normalize.stateChanged.connect(self.update_comparison_chart)
        cp.cmb_sports_brand.currentIndexChanged.connect(self.update_comparison_chart)
        cp.chk_gas.stateChanged.connect(self.update_comparison_chart)
        cp.chk_electric.stateChanged.connect(self.update_comparison_chart)


class Act2Tab(QWidget):
    """
    Specialized tab for Act 2: Electrification
    - Left: universal control panel (defaults to 2013-2024)
    - Right / Row 1:
        * Top-left: EPA Fuel Share Over Time (2A) stacked area chart
        * Top-right: placeholder for performance/efficiency scatter (2B)
    - Right / Row 2:
        * Bottom: narrative text
    """

    def __init__(self, epa_df: pd.DataFrame, parent=None):
        super().__init__(parent)
        self.act_name = "Act 2: Electrification"
        self.epa_df = epa_df
        self.scatter_artists = []
        self.scatter_data = None
        self.scatter_annot = None
        self._build_ui()
        self._connect_signals()
        self.update_fuel_share_chart()
        self.update_scatter_chart()

    def _build_ui(self):
        root_layout = QHBoxLayout(self)
        root_layout.setSpacing(5)  # Reduce spacing between sidebar and charts
        root_layout.setContentsMargins(5, 5, 5, 5)  # Reduce margins

        # Left: control panel with Act 2 year defaults (2011-2024, narrow)
        self.control_panel = ControlPanel(year_min_default=2011, year_max_default=2024)
        self.control_panel.setMaximumWidth(250)  # Limit width
        root_layout.addWidget(self.control_panel, stretch=0)

        # Right: charts + narrative
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setSpacing(5)  # Reduce vertical spacing

        # Row 1: two side-by-side visualizations
        row1 = QWidget()
        row1_layout = QHBoxLayout(row1)
        row1_layout.setSpacing(5)  # Reduce spacing between charts
        row1_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins

        # Top-left: Fuel Share stacked area chart (2A)
        self.fuel_share_figure = Figure(figsize=(6, 5.5))
        self.canvas_fuel_share = FigureCanvas(self.fuel_share_figure)
        row1_layout.addWidget(self.canvas_fuel_share)

        # Top-right: Performance vs Efficiency scatter (2B)
        self.scatter_figure = Figure(figsize=(6, 5.5))
        self.canvas_scatter = FigureCanvas(self.scatter_figure)
        row1_layout.addWidget(self.canvas_scatter)

        # Row 2: narrative box
        row2 = QWidget()
        row2_layout = QHBoxLayout(row2)
        row2_layout.setSpacing(5)  # Reduce spacing
        row2_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins

        # Narrative box
        self.narrative_box = QTextEdit()
        self.narrative_box.setReadOnly(True)
        self.narrative_box.setMarkdown(
            "## Act 2: The Electrification Revolution\n\n"
            "### The Market Transformation (2013-2024)\n\n"
            "**What You're Seeing:**\n\n"
            "The left visualization (2A) shows a dramatic market shift:\n"
            "- **2013-2015**: Gasoline dominates ~85-90% of the market. Hybrids represent a small "
            "but growing alternative. EVs are barely visible.\n"
            "- **2016-2018**: The inflection point. EV share begins climbing while gas share "
            "steadily declines. Hybrids stabilize as a bridge technology.\n"
            "- **2019-2024**: Rapid acceleration. EVs capture 15-20% market share by 2024. "
            "The composition of mainstream vehicles fundamentally changes.\n\n"
            "### Breaking the Efficiency Ceiling\n\n"
            "The right visualization (2B) reveals something remarkable:\n"
            "- **Gas vehicles (blue dots)**: Stuck at 20-35 MPG across all years. Despite decades "
            "of engineering, efficiency improvements are incremental.\n"
            "- **Hybrids (orange dots)**: Achieve 40-60 MPG by combining gas and electric power. "
            "A meaningful improvement, but still limited.\n"
            "- **EVs (green dots)**: Appear in later years at 80-140+ MPG equivalent. They don't "
            "just improve efficiency - they redefine what's possible.\n\n"
            "**Hover over any dot** to see specific vehicle models and their exact specifications.\n\n"
            "### The Key Insight: One-Sided Convergence\n\n"
            "This is where the story gets interesting:\n"
            "- **EPA vehicles move toward performance**: By adopting electric powertrains, mainstream "
            "vehicles gain both efficiency AND performance capabilities.\n"
            "- **Sports cars stay traditional**: Our sports car dataset contains no EVs. While EPA "
            "vehicles electrify, performance vehicles in this analysis remain combustion-based.\n"
            "- **The gap narrows from one side only**: Convergence is happening, but it's asymmetric. "
            "Only one market is evolving.\n\n"
            "### Why This Matters\n\n"
            "Electrification doesn't just improve existing vehicles - it breaks the fundamental "
            "tradeoff between performance and efficiency. In the combustion era, you chose: "
            "power OR economy. EVs deliver both.\n\n"
            "This sets up our final question in Act 3: If only one market is moving, can we "
            "truly call this convergence? Or are we witnessing two markets that will remain "
            "fundamentally distinct?"
        )
        row2_layout.addWidget(self.narrative_box)

        # Add rows to right layout
        right_layout.addWidget(row1, stretch=2)
        right_layout.addWidget(row2, stretch=1)

        root_layout.addWidget(right_panel, stretch=1)

    def update_fuel_share_chart(self):
        """
        Rebuild the fuel share stacked area chart using current control panel settings.
        Groups all fuel types into just 2 categories: Gas and Electric.
        """
        cp = self.control_panel

        year_min = cp.year_min_spin.value()
        year_max = cp.year_max_spin.value()
        use_percent = cp.chk_raw_vs_percent.isChecked()

        # Define fuel type groupings
        gas_types = ['Regular', 'Premium', 'Midgrade', 'Gasoline or E85',
                     'Premium or E85', 'Diesel', 'Gasoline or natural gas', 'CNG']
        electric_types = ['Electricity', 'Regular Gas and Electricity',
                         'Premium Gas or Electricity', 'Premium and Electricity',
                         'Regular Gas or Electricity']

        # Filter by year and create grouped fuel type column
        mask = (self.epa_df["Year"] >= year_min) & (self.epa_df["Year"] <= year_max)
        df_sub = self.epa_df.loc[mask].copy()

        # Map fuel types to simplified categories
        def map_fuel_type(ft):
            if ft in gas_types:
                return "Gas"
            elif ft in electric_types:
                return "Electric"
            else:
                return "Other"

        df_sub["Fuel Category"] = df_sub["Fuel Type"].apply(map_fuel_type)

        # Filter by selected categories
        selected_categories = []
        if cp.chk_gas.isChecked():
            selected_categories.append("Gas")
        if cp.chk_electric.isChecked():
            selected_categories.append("Electric")

        if selected_categories:
            df_sub = df_sub[df_sub["Fuel Category"].isin(selected_categories)]

        # Clear the existing figure
        self.fuel_share_figure.clear()
        ax = self.fuel_share_figure.add_subplot(111)

        # If no data, show message
        if len(df_sub) == 0:
            ax.text(
                0.5, 0.5,
                "No data available for selected filters",
                ha='center', va='center',
                fontsize=12, color='gray',
                transform=ax.transAxes
            )
            ax.set_xlabel("Year")
            ax.set_ylabel("Share")
            ax.set_title("Fuel Type Market Share Over Time")
            self.fuel_share_figure.tight_layout()
            self.canvas_fuel_share.draw()
            return

        # Group by Year and Fuel Category, count occurrences
        fuel_counts = (
            df_sub.groupby(["Year", "Fuel Category"], as_index=False)
            .size()
            .rename(columns={"size": "count"})
        )

        # Pivot to wide format
        fuel_wide = fuel_counts.pivot(
            index="Year", columns="Fuel Category", values="count"
        ).fillna(0).reset_index()

        years = fuel_wide["Year"].values
        fuel_cols = [col for col in fuel_wide.columns if col != "Year"]

        # Convert to percentage if requested
        if use_percent:
            row_sums = fuel_wide[fuel_cols].sum(axis=1)
            row_sums = row_sums.replace(0, 1)
            for col in fuel_cols:
                fuel_wide[col] = (fuel_wide[col] / row_sums) * 100

        # Prepare data for stackplot
        fuel_data = [fuel_wide[col].values for col in fuel_cols]

        # Define colors: Gas=Blue, Electric=Green
        color_map = {"Gas": "#1f77b4", "Electric": "#2ca02c"}
        colors = [color_map.get(ft, "#bcbd22") for ft in fuel_cols]

        # Create stacked area chart
        ax.stackplot(years, *fuel_data, labels=fuel_cols, colors=colors, alpha=0.8)

        # Formatting
        ax.set_xlabel("Year", fontsize=11)
        if use_percent:
            ax.set_ylabel("Market Share (%)", fontsize=11)
            ax.set_ylim(0, 100)
        else:
            ax.set_ylabel("Number of Vehicle Models", fontsize=11)

        ax.set_title("Fuel Type Market Share Over Time (EPA Dataset)", fontsize=12)
        ax.legend(fontsize=9, loc='upper left', framealpha=0.9)
        ax.grid(True, alpha=0.3, axis='y')

        self.fuel_share_figure.tight_layout()
        self.canvas_fuel_share.draw()

    def update_scatter_chart(self):
        """
        Rebuild the performance vs efficiency scatter plot using current control panel settings.
        For this chart specifically, shows 3 categories: Gas, Hybrid, and Electric (pure EV).
        """
        cp = self.control_panel

        year_min = cp.year_min_spin.value()
        year_max = cp.year_max_spin.value()
        show_only_electrified = cp.chk_show_only_electrified.isChecked()

        # Define fuel type groupings - 3 categories for scatter chart
        gas_types = ['Regular', 'Premium', 'Midgrade', 'Gasoline or E85',
                     'Premium or E85', 'Diesel', 'Gasoline or natural gas', 'CNG']
        hybrid_types = ['Regular Gas and Electricity', 'Premium Gas or Electricity',
                       'Premium and Electricity', 'Regular Gas or Electricity']
        electric_types = ['Electricity']

        # Filter by year
        mask = (self.epa_df["Year"] >= year_min) & (self.epa_df["Year"] <= year_max)
        df_sub = self.epa_df.loc[mask].copy()
        df_sub = df_sub.dropna(subset=["Combined Mpg For Fuel Type1"])

        # Map fuel types to 3 categories for scatter chart
        def map_fuel_type(ft):
            if ft in gas_types:
                return "Gas"
            elif ft in hybrid_types:
                return "Hybrid"
            elif ft in electric_types:
                return "Electric"
            else:
                return "Other"

        df_sub["Fuel Category"] = df_sub["Fuel Type"].apply(map_fuel_type)

        # Filter by selected categories (Electric checkbox includes both Hybrid and Electric)
        selected_categories = []
        if cp.chk_gas.isChecked():
            selected_categories.append("Gas")
        if cp.chk_electric.isChecked():
            selected_categories.extend(["Hybrid", "Electric"])

        if selected_categories:
            df_sub = df_sub[df_sub["Fuel Category"].isin(selected_categories)]

        # Filter for electrified only if requested
        if show_only_electrified:
            df_sub = df_sub[df_sub["Fuel Category"].isin(["Hybrid", "Electric"])]

        # Store filtered data for tooltip access
        self.scatter_data = df_sub.copy()

        # Clear the existing figure
        self.scatter_figure.clear()
        ax = self.scatter_figure.add_subplot(111)

        # If no data, show message
        if len(df_sub) == 0:
            ax.text(
                0.5, 0.5,
                "No data available for selected filters",
                ha='center', va='center',
                fontsize=12, color='gray',
                transform=ax.transAxes
            )
            ax.set_xlabel("Year")
            ax.set_ylabel("Combined MPG")
            ax.set_title("Efficiency Evolution Over Time")
            self.scatter_figure.tight_layout()
            self.canvas_scatter.draw()
            return

        # Define colors: Gas=Blue, Hybrid=Orange, Electric=Green
        color_map = {"Gas": "#1f77b4", "Hybrid": "#ff7f0e", "Electric": "#2ca02c"}

        # Get unique fuel categories
        fuel_categories_present = df_sub["Fuel Category"].unique()

        # Store scatter artists for hover detection
        self.scatter_artists = []

        # Plot each fuel category separately
        for fuel_category in fuel_categories_present:
            cat_data = df_sub[df_sub["Fuel Category"] == fuel_category]
            color = color_map.get(fuel_category, "#bcbd22")

            scatter = ax.scatter(
                cat_data["Year"],
                cat_data["Combined Mpg For Fuel Type1"],
                c=color,
                label=fuel_category,
                alpha=0.5,
                s=25,
                edgecolors='none'
            )
            self.scatter_artists.append((scatter, cat_data))

        # Formatting
        ax.set_xlabel("Year", fontsize=11)
        ax.set_ylabel("Combined MPG", fontsize=11)
        ax.set_title("Efficiency Evolution Over Time", fontsize=12)
        ax.legend(fontsize=9, loc='upper left', framealpha=0.9)
        ax.grid(True, alpha=0.3)

        # Set reasonable axis limits
        ax.set_ylim(bottom=0)

        # Create annotation for tooltip (initially invisible)
        self.scatter_annot = ax.annotate(
            "",
            xy=(0, 0),
            xytext=(10, 10),
            textcoords="offset points",
            bbox=dict(boxstyle="round,pad=0.5", fc="yellow", alpha=0.9),
            arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=0", color="black"),
            fontsize=8,
            visible=False,
            ha="left"  # Default horizontal alignment
        )

        self.scatter_figure.tight_layout()
        self.canvas_scatter.draw()

        # Connect hover event
        self.canvas_scatter.mpl_connect('motion_notify_event', self.on_scatter_hover)

    def on_scatter_hover(self, event):
        """
        Handle mouse hover events on scatter plot.
        Shows tooltip on the left for years > 2020 to prevent going off-screen.
        """
        # Return early if annotation not ready or mouse not in axes
        if not self.scatter_annot or event.inaxes != self.scatter_figure.gca():
            if self.scatter_annot and self.scatter_annot.get_visible():
                self.scatter_annot.set_visible(False)
                self.canvas_scatter.draw_idle()
            return

        # Check if hovering over any data point
        point_found = False
        for scatter, fuel_data in self.scatter_artists:
            contains, ind = scatter.contains(event)
            if contains:
                # Get the data for the hovered point
                idx = ind["ind"][0]
                data_idx = fuel_data.index[idx]
                row = self.scatter_data.loc[data_idx]

                # Extract data
                make = row.get("Make", "N/A")
                model = row.get("Model", "N/A")
                year = int(row.get("Year", 0))
                fuel_category = row.get("Fuel Category", "N/A")
                mpg = row.get("Combined Mpg For Fuel Type1", 0)
                co2 = row.get("Co2  Tailpipe For Fuel Type1", 0)

                # Build tooltip text
                text = (
                    f"{make} {model}\n"
                    f"Year: {year}\n"
                    f"Type: {fuel_category}\n"
                    f"MPG: {mpg:.1f}\n"
                    f"CO₂: {co2:.1f} g/mi"
                )

                # Determine tooltip position based on year
                # For years >= 2020, show tooltip on LEFT to avoid going off screen
                # For years < 2020, show tooltip on RIGHT
                if year >= 2020:
                    x_offset = -30  # Left side
                    h_align = "right"
                else:
                    x_offset = 15  # Right side
                    h_align = "left"

                # Update annotation properties
                self.scatter_annot.set_text(text)
                self.scatter_annot.xy = (year, mpg)
                self.scatter_annot.set_position((x_offset, 10))
                self.scatter_annot.xyann = (x_offset, 10)
                self.scatter_annot.set_ha(h_align)
                self.scatter_annot.set_visible(True)

                point_found = True
                break

        # Hide tooltip if not hovering over any point
        if not point_found:
            if self.scatter_annot.get_visible():
                self.scatter_annot.set_visible(False)

        # Redraw canvas
        self.canvas_scatter.draw_idle()

    def _connect_signals(self):
        """
        Connect control panel signals to both chart updates.
        """
        cp = self.control_panel

        # Connect to fuel share chart (2A)
        cp.year_min_spin.valueChanged.connect(self.update_fuel_share_chart)
        cp.year_max_spin.valueChanged.connect(self.update_fuel_share_chart)
        cp.chk_gas.stateChanged.connect(self.update_fuel_share_chart)
        cp.chk_electric.stateChanged.connect(self.update_fuel_share_chart)
        cp.chk_raw_vs_percent.stateChanged.connect(self.update_fuel_share_chart)

        # Connect to scatter chart (2B)
        cp.year_min_spin.valueChanged.connect(self.update_scatter_chart)
        cp.year_max_spin.valueChanged.connect(self.update_scatter_chart)
        cp.chk_gas.stateChanged.connect(self.update_scatter_chart)
        cp.chk_electric.stateChanged.connect(self.update_scatter_chart)
        cp.chk_show_only_electrified.stateChanged.connect(self.update_scatter_chart)


# ---------- Act 3 Tab ----------


class Act3Tab(QWidget):
    """
    Act 3: Convergence vs Coexistence

    Chart 3A: Side-by-side Performance and Efficiency Indices
    - Left: Performance Index over time (Gas, Sports, EV)
    - Right: Efficiency Index over time (Gas, Sports, EV)
    """

    def __init__(self, sports_df: pd.DataFrame, epa_df: pd.DataFrame, parent=None):
        super().__init__(parent)
        self.sports_df = sports_df
        self.epa_df = epa_df
        self._build_ui()
        self._connect_signals()
        self.update_indices_chart()

    def _build_ui(self):
        root_layout = QHBoxLayout(self)
        root_layout.setSpacing(5)
        root_layout.setContentsMargins(5, 5, 5, 5)

        # Left: control panel (same as Act 1 and Act 2)
        self.control_panel = ControlPanel(year_min_default=2011, year_max_default=2024)
        self.control_panel.setMaximumWidth(250)
        root_layout.addWidget(self.control_panel, stretch=0)

        # Right: Chart 3A
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setSpacing(5)

        # Chart 3A: Performance and Efficiency Indices
        self.indices_figure = Figure(figsize=(14, 5.5))
        self.canvas_indices = FigureCanvas(self.indices_figure)
        right_layout.addWidget(self.canvas_indices, stretch=2)

        # Narrative box
        self.narrative_box = QTextEdit()
        self.narrative_box.setReadOnly(True)
        self.narrative_box.setMarkdown(
            "## Act 3: Convergence or Coexistence?\n\n"
            "### Two Markets, Two Trajectories\n\n"
            "**What You're Seeing:**\n\n"
            "The visualization above shows normalized performance (left) and efficiency (right) "
            "indices for three vehicle categories:\n"
            "- **Gas Vehicles (blue)**: Traditional mainstream vehicles\n"
            "- **Sports Cars (red)**: High-performance specialty vehicles\n"
            "- **EV Vehicles (green)**: Electric mainstream vehicles\n\n"
            "### Expected Trends:\n\n"
            "**Performance Chart (Left):**\n"
            "- EVs should show **increasing power** as electric powertrains mature\n"
            "- Sports cars maintain high performance throughout\n"
            "- Gas vehicles show modest improvements\n\n"
            "**Efficiency Chart (Right):**\n"
            "- EVs dominate efficiency with MPG-equivalent ratings\n"
            "- Gas vehicles show slow, incremental improvements\n"
            "- Sports cars: Will they show efficiency improvements or remain performance-focused?\n\n"
            "### The Convergence Question:\n\n"
            "Are the two markets converging toward similar characteristics, or do they remain "
            "fundamentally distinct? The answer lies in whether:\n"
            "1. EVs gain performance (moving toward sports car territory)\n"
            "2. Sports cars improve efficiency (moving toward mainstream eco-friendliness)\n\n"
            "If **both** trends occur, we see convergence. If only **one** occurs, the markets "
            "remain separate but one adapts while the other doesn't."
        )
        right_layout.addWidget(self.narrative_box, stretch=1)

        root_layout.addWidget(right_panel, stretch=1)

    def update_indices_chart(self):
        """
        Rebuild Chart 3A using current control panel settings.
        """
        cp = self.control_panel
        year_min = cp.year_min_spin.value()
        year_max = cp.year_max_spin.value()
        show_gas = cp.chk_gas.isChecked()
        show_sports = cp.chk_show_sports.isChecked()
        show_ev = cp.chk_electric.isChecked()

        # Clear and rebuild
        self.indices_figure.clear()
        fig = make_indices_chart(
            self.sports_df,
            self.epa_df,
            year_min=year_min,
            year_max=year_max,
            show_gas=show_gas,
            show_sports=show_sports,
            show_ev=show_ev,
        )

        # Copy axes from returned figure to our canvas figure
        for i, ax in enumerate(fig.axes):
            new_ax = self.indices_figure.add_subplot(1, 2, i + 1)
            # Copy all plot elements
            for line in ax.get_lines():
                new_ax.plot(
                    line.get_xdata(),
                    line.get_ydata(),
                    label=line.get_label(),
                    color=line.get_color(),
                    linewidth=line.get_linewidth(),
                    marker=line.get_marker(),
                    markersize=line.get_markersize(),
                )
            new_ax.set_xlabel(ax.get_xlabel(), fontsize=ax.xaxis.label.get_fontsize())
            new_ax.set_ylabel(ax.get_ylabel(), fontsize=ax.yaxis.label.get_fontsize())
            new_ax.set_title(ax.get_title(), fontsize=ax.title.get_fontsize(), fontweight=ax.title.get_fontweight())
            new_ax.set_xlim(ax.get_xlim())
            new_ax.set_ylim(ax.get_ylim())
            new_ax.grid(True, alpha=0.3)
            if ax.get_legend():
                new_ax.legend(fontsize=9, loc='best', framealpha=0.9)

        self.indices_figure.tight_layout()
        self.canvas_indices.draw()

    def _connect_signals(self):
        """
        Connect control panel signals to chart update.
        """
        cp = self.control_panel
        cp.year_min_spin.valueChanged.connect(self.update_indices_chart)
        cp.year_max_spin.valueChanged.connect(self.update_indices_chart)
        cp.chk_gas.stateChanged.connect(self.update_indices_chart)
        cp.chk_show_sports.stateChanged.connect(self.update_indices_chart)
        cp.chk_electric.stateChanged.connect(self.update_indices_chart)


# ---------- Main Window ----------


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("CS439 Final Project Dashboard")
        self.resize(1400, 800)

        # Load data
        self.sports_df = load_sports_data()
        self.epa_df = load_epa_data()

        tabs = QTabWidget()

        # Act 1: custom tab with real sports and EPA trendlines visualizations
        tabs.addTab(Act1Tab(self.sports_df, self.epa_df), "Act 1: Diverging Priorities")

        # Act 2: Focus on electrification era (2013-2024) with fuel share chart
        tabs.addTab(Act2Tab(self.epa_df), "Act 2: Electrification")

        # Act 3: Full range for convergence analysis
        tabs.addTab(Act3Tab(self.sports_df, self.epa_df), "Act 3: Convergence vs Coexistence")

        self.setCentralWidget(tabs)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
