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
from plots_epa import make_epa_trend_figure, compute_epa_yearly_aggregates


# ---------- Helpers to load EPA data ----------


def load_epa_data():
    """
    Try to load a preprocessed EPA dataset.
    If it fails, fall back to using cleaning.load_and_clean_epa
    on the raw file.

    Adjust paths to match your repo structure.
    """
    # First try processed file (recommended)
    try:
        df = pd.read_csv("../data/cleaned/epa_clean.csv")
        return df
    except Exception:
        print("Could not load data/processed/epa_clean.csv, falling back to raw + cleaning...")

    # Fallback: use your cleaning module on raw data
    try:
        from cleaning import load_and_clean_epa

        df = load_and_clean_epa("../data/raw/all-vehicles-model.csv")
        return df
    except Exception as e:
        print("Error loading EPA data:", e)
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

    def __init__(self, parent=None):
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
        self.year_min_spin.setValue(2011)
        self.year_max_spin.setValue(2024)

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

        self.chk_show_sports = QCheckBox("Show sports lines (HP, Engine, Price)")
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

        self.chk_show_epa = QCheckBox("Show EPA lines (MPG, CO₂, Displacement)")
        self.chk_show_epa.setChecked(True)
        epa_layout.addWidget(self.chk_show_epa)

        fuel_layout = QGridLayout()
        self.chk_gas = QCheckBox("Gas")
        self.chk_hybrid = QCheckBox("Hybrid")
        self.chk_ev = QCheckBox("EV")
        self.chk_diesel = QCheckBox("Diesel")
        self.chk_gas.setChecked(True)
        self.chk_hybrid.setChecked(True)
        self.chk_ev.setChecked(True)
        self.chk_diesel.setChecked(True)

        fuel_layout.addWidget(self.chk_gas, 0, 0)
        fuel_layout.addWidget(self.chk_hybrid, 0, 1)
        fuel_layout.addWidget(self.chk_ev, 1, 0)
        fuel_layout.addWidget(self.chk_diesel, 1, 1)
        epa_layout.addLayout(fuel_layout)

        self.chk_show_only_electrified = QCheckBox("Show only hybrids/EVs in scatter")
        epa_layout.addWidget(self.chk_show_only_electrified)

        self.chk_raw_vs_percent = QCheckBox("Use % share instead of raw counts")
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

    def __init__(self, act_name: str, parent=None):
        super().__init__(parent)
        self.act_name = act_name
        self._build_ui()

    def _build_ui(self):
        root_layout = QHBoxLayout(self)

        # Left: universal control panel
        self.control_panel = ControlPanel()
        root_layout.addWidget(self.control_panel, stretch=0)

        # Right: charts + narrative
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)

        # Row 1: two side-by-side visualizations
        row1 = QWidget()
        row1_layout = QHBoxLayout(row1)
        row1_layout.setSpacing(10)

        # Placeholders for the top two charts
        self.chart_top_left = ChartPlaceholder(f"{self.act_name} - Top Left Chart")
        self.chart_top_right = ChartPlaceholder(f"{self.act_name} - Top Right Chart")

        row1_layout.addWidget(self.chart_top_left)
        row1_layout.addWidget(self.chart_top_right)

        # Row 2: one main comparison visualization
        row2 = QWidget()
        row2_layout = QHBoxLayout(row2)
        row2_layout.setSpacing(10)

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

    def __init__(self, epa_df: pd.DataFrame, parent=None):
        super().__init__(parent)
        self.act_name = "Act 1: Diverging Priorities"
        self.epa_df = epa_df
        self._build_ui()
        self._connect_signals()
        self.update_epa_trendlines_chart()

    def _build_ui(self):
        root_layout = QHBoxLayout(self)

        # Left: universal control panel
        self.control_panel = ControlPanel()
        root_layout.addWidget(self.control_panel, stretch=0)

        # Right: charts + narrative
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)

        # Row 1: two side-by-side visualizations
        row1 = QWidget()
        row1_layout = QHBoxLayout(row1)
        row1_layout.setSpacing(10)

        # Top-left: placeholder (for sports trendlines 1A)
        self.chart_top_left = ChartPlaceholder(f"{self.act_name} - Sports Trendlines (1A)")
        row1_layout.addWidget(self.chart_top_left)

        # Top-right: real EPA trendlines chart (1B)
        self.epa_figure = Figure(figsize=(5, 4))
        self.canvas_epa = FigureCanvas(self.epa_figure)
        row1_layout.addWidget(self.canvas_epa)

        # Row 2: one main comparison visualization + narrative
        row2 = QWidget()
        row2_layout = QHBoxLayout(row2)
        row2_layout.setSpacing(10)

        # Bottom-left: placeholder for comparison chart (1C)
        self.chart_bottom_main = ChartPlaceholder(f"{self.act_name} - Comparison Chart (1C)")
        row2_layout.addWidget(self.chart_bottom_main)

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

        # Collect selected fuel types from checkboxes
        # Map UI labels to actual dataset values
        fuel_type_mapping = {
            'gas': 'Gasoline',
            'hybrid': 'Diesel/Electric',  # Hybrids often labeled this way in EPA data
            'ev': 'Electricity',
            'diesel': 'Diesel'
        }

        selected_fuel_types = []
        if cp.chk_gas.isChecked():
            selected_fuel_types.append(fuel_type_mapping['gas'])
        if cp.chk_hybrid.isChecked():
            selected_fuel_types.append(fuel_type_mapping['hybrid'])
        if cp.chk_ev.isChecked():
            selected_fuel_types.append(fuel_type_mapping['ev'])
        if cp.chk_diesel.isChecked():
            selected_fuel_types.append(fuel_type_mapping['diesel'])

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

            ax.set_xlabel("Year", fontsize=10)
            if normalize:
                ax.set_ylabel("Index (base year = 100)", fontsize=10)
            else:
                ax.set_ylabel("Value (units vary by line)", fontsize=10)
            ax.set_title("EPA Trendlines: Efficiency & Engine Size Over Time", fontsize=11)
            ax.legend(fontsize=8, loc='best', framealpha=0.9)
            ax.grid(True, alpha=0.3)

        self.epa_figure.tight_layout()
        self.canvas_epa.draw()

    def _connect_signals(self):
        """
        Connect relevant control panel signals to the EPA chart update.
        """
        cp = self.control_panel

        cp.year_min_spin.valueChanged.connect(self.update_epa_trendlines_chart)
        cp.year_max_spin.valueChanged.connect(self.update_epa_trendlines_chart)
        cp.chk_show_epa.stateChanged.connect(self.update_epa_trendlines_chart)
        cp.chk_normalize.stateChanged.connect(self.update_epa_trendlines_chart)

        # Fuel-type checkboxes are currently not used in plots_epa.py,
        # but you can later add filtering in make_epa_trend_figure and
        # then also connect these:
        cp.chk_gas.stateChanged.connect(self.update_epa_trendlines_chart)
        cp.chk_hybrid.stateChanged.connect(self.update_epa_trendlines_chart)
        cp.chk_ev.stateChanged.connect(self.update_epa_trendlines_chart)
        cp.chk_diesel.stateChanged.connect(self.update_epa_trendlines_chart)


# ---------- Main Window ----------


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("CS439 Final Project Dashboard")
        self.resize(1400, 800)

        # Load data
        self.epa_df = load_epa_data()

        tabs = QTabWidget()

        # Act 1: custom tab with real EPA trendlines visualization
        tabs.addTab(Act1Tab(self.epa_df), "Act 1: Diverging Priorities")

        # Act 2 & 3: still generic placeholders for now
        tabs.addTab(ActTab("Act 2: Electrification"), "Act 2: Electrification")
        tabs.addTab(
            ActTab("Act 3: Convergence vs Coexistence"),
            "Act 3: Convergence vs Coexistence",
        )

        self.setCentralWidget(tabs)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
