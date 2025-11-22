import sys

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
        self.year_min_spin.setRange(1900, 2100)
        self.year_max_spin.setRange(1900, 2100)
        self.year_min_spin.setValue(2000)
        self.year_max_spin.setValue(2025)
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
        self.chk_diesel.setChecked(False)

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


class ActTab(QWidget):
    """
    Generic tab for Act 1, Act 2, Act 3 with:
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


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("CS439 Final Project Dashboard (Skeleton)")
        self.resize(1400, 800)

        tabs = QTabWidget()

        # Create three tabs with the same structure
        tabs.addTab(ActTab("Act 1: Diverging Priorities"), "Act 1")
        tabs.addTab(ActTab("Act 2: Electrification"), "Act 2")
        tabs.addTab(ActTab("Act 3: Convergence vs Coexistence"), "Act 3")

        self.setCentralWidget(tabs)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
