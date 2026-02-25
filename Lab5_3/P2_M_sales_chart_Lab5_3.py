# P2 Lab 5-3
import sys, os, matplotlib
matplotlib.use("QtAgg")  # ensure QtAgg backend is used

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLineEdit, QLabel, QComboBox, QSpinBox, QFileDialog, QGroupBox, QMessageBox
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Monthly Sales Analytics")
        self.setGeometry(200, 50, 1300, 800)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout()
        # Add SalesChartApp inside MainWindow
        self.sales_chart_app = SalesChartApp()
        main_layout.addWidget(self.sales_chart_app)

        central_widget.setLayout(main_layout)

        # Apply modern fintech theme
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:2, y2:2,
                    stop:0 #0A0D15, stop:1 #65021E);  }
        """)

class SalesChartApp(QWidget):
    def __init__(self):
        super().__init__()

        main_layout = QHBoxLayout()
        main_layout.setSpacing(30)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Left Panel - Controls
        left_panel = self.create_control_panel()
        
        # Right Panel - Chart
        right_panel = self.create_chart_panel()

        main_layout.addWidget(left_panel, 1)
        main_layout.addWidget(right_panel, 2)

        self.setLayout(main_layout)

        # Data storage
        self.sales_data = []}
        
        self.update_chart()

    def create_control_panel(self):
        """Create left control panel"""
        panel = QWidget()
        panel.setObjectName("ControlPanel")
        panel_layout = QVBoxLayout()
        panel_layout.setSpacing(20)
        panel_layout.setContentsMargins(20, 20, 20, 20)

        # Title
        title = QLabel("Monthly Sales Data Input")
        title.setFont(QFont("Arial", 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)

        panel_layout.addWidget(title)

        # Filename input + file picker
        form_layout = QHBoxLayout()
        self.filename_label = QLabel("Filename:")
        self.filename_label.setFont(QFont("Arial", 12, QFont.Bold))
        self.filename_input = QLineEdit()
        self.filename_btn = QPushButton("Select File")
        self.filename_btn.clicked.connect(self.select_file)
        self.filename_btn.setStyleSheet("""
            QPushButton {
                background-color: #0074F0;
                color: white;
                border-radius: 5px;
                padding: 5px 10px;
            }
            QPushButton:hover { background-color: #005BB5; }
        """)

        form_layout.addWidget(self.filename_label)
        form_layout.addWidget(self.filename_input)
        form_layout.addWidget(self.filename_btn)

        panel_layout.addLayout(form_layout)

        # Manual Entry Section
        entry_group = QGroupBox("✏️ Manual Entry")
        entry_group.setFont(QFont("Arial", 11, QFont.Bold))
        entry_layout = QVBoxLayout()
        entry_layout.setSpacing(12)

        # Month dropdown
        month_label = QLabel("Month:")
        month_label.setFont(QFont("Arial", 12, QFont.Bold))
        self.month_dropdown = QComboBox()
        self.month_dropdown.addItems(
            ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
        )
        self.month_dropdown.setFixedHeight(40)

        # Sales amount input
        amount_label = QLabel("Sales Amount (฿):")
        amount_label.setFont(QFont("Arial", 12, QFont.Bold))
        self.sales_input = QSpinBox()
        self.sales_input.setRange(0, 100000)
        self.sales_input.setSingleStep(100)
        self.sales_input.setFixedHeight(40)
        self.sales_input.setAlignment(Qt.AlignRight)
        self.sales_input.setSuffix("฿")  # Thai Baht symbol for a fintech touch ")

        # Category dropdown
        category_label = QLabel("Product Category:")
        category_label.setFont(QFont("Arial", 12, QFont.Bold))
        self.category_dropdown = QComboBox()
        self.category_dropdown.addItems(["Electronics","Clothing","Food","Others"])
        self.category_dropdown.setFixedHeight(40)

        # Buttons which are Import Data, Add Data, Clear Chart
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(15)
#Import Data button
        self.import_btn = QPushButton("Import Data")
        self.import_btn.setStyleSheet("""
            QPushButton { background-color: #4CFFBD; color: black; border-radius: 5px; padding: 10px 20px; }
            QPushButton:hover { background-color: #3ABF8A; }
        """)
        self.import_btn.setFixedHeight(40)
        self.import_btn.clicked.connect(self.import_data)
        self.import_btn.setObjectName("importButton")
#Add Data button
        self.add_btn = QPushButton("Add Data")
        self.add_btn.setStyleSheet("""
            QPushButton { background-color: #B026FF; color: white; border-radius: 5px; padding: 10px 20px; }
            QPushButton:hover { background-color: #7A1ABF; }
        """)
        self.add_btn.setFixedHeight(40)
        self.add_btn.clicked.connect(self.add_data)
        self.add_btn.setObjectName("addButton")
#Clear Chart button
        self.clear_btn = QPushButton("Clear Chart")
        self.clear_btn.setStyleSheet("""
            QPushButton { background-color: #FF3366; color: white; border-radius: 5px; padding: 10px 20px; }
            QPushButton:hover { background-color: #CC0022; }
        """)
        self.clear_btn.setFixedHeight(40)
        self.clear_btn.clicked.connect(self.clear_chart)
        self.clear_btn.setObjectName("clearButton")

        # Add widgets to panel layout
        entry_layout.addWidget(month_label)
        entry_layout.addWidget(self.month_dropdown)
        entry_layout.addWidget(amount_label)
        entry_layout.addWidget(self.sales_input)
        entry_layout.addWidget(category_label)
        entry_layout.addWidget(self.category_dropdown)
        entry_group.setLayout(entry_layout)
        panel_layout.addWidget(entry_group)

        btn_layout.addWidget(self.import_btn)
        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.clear_btn)
        panel_layout.addLayout(btn_layout)

        panel_layout.addStretch()
        panel.setLayout(panel_layout)

        return panel
    

    def create_chart_panel(self):
        """Create right chart panel"""
        panel_layout = QVBoxLayout()
        panel = QWidget()
        panel.setObjectName("ChartPanel")

        # Chart setup
        self.figure, self.ax = plt.subplots()
        #self.figure.patch.set_facecolor('none')  # Transparent to show panel gradient
        self.ax.set_facecolor('none')  # Transparent to show panel gradient
        self.canvas = FigureCanvas(self.figure)
        
        # Panel styles
        panel.setStyleSheet("""
            QWidget#chartPanel {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #0F1629, stop:1 #1A1F3A);
                border-radius: 15px;
                border: 2px solid rgba(0, 217, 255, 0.2);
            }
        """)
        
        panel_layout.addWidget(self.canvas)
        panel.setLayout(panel_layout)

        return panel


    def select_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Select Sales Data File", "", "Text Files (*.txt)")
        if filename:
            self.filename_input.setText(filename)

    def import_data(self):
        filename = self.filename_input.text().strip()

        if not filename:
            QMessageBox.warning(self, "⚠️ Error", "Please select a file first.")
            return
        
        if not os.path.exists(filename):
            QMessageBox.warning(self, "⚠️ File Not Found", 
                f"The file '{filename}' does not exist. Please select another file.")
            return
        
        if os.path.exists(filename):
            try:
                imported_count = 0
                with open(filename, "r") as f:
                    for line in f:
                        parts = line.strip().split(",")
                        if len(parts) == 3:
                            month, amount, category = parts
                            try:
                                amount = int(amount)
                                self.sales_data.append((month, amount, category))
                            except ValueError:
                                pass
                self.update_chart()
        
                QMessageBox.information(self, "✅ Success", 
                    f"Imported {imported_count} records successfully!")
        
            except Exception as e:
                QMessageBox.critical(self, "❌ Import Error", 
                    f"Error reading file:/n{str(e)}")

    def add_data(self):
        month = self.month_dropdown.currentText()
        amount = self.sales_input.value()
        category = self.category_dropdown.currentText()
        # Validation
        if amount == 0:
            QMessageBox.warning(self, "⚠️ Input Error", "Please enter a positive sales amount.")
            return
        # Add data to list and update chart
        self.sales_data.append((month, amount, category))
        self.update_chart()

        QMessageBox.information(self, "✅ Data Added", 
            f"In {month} - {category} with sales {amount}฿ successfully!")
        
        self.sales_input.setValue(0)  # Reset input after adding

    def clear_chart(self):
        reply = QMessageBox.question(self, "⚠️ Confirm Clear", 
            "Clear all sales data?",
            QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            self.sales_data = []
            self.ax.clear()  # Clear the chart
            self.canvas.draw()  # Redraw the canvas to show the cleared chart
            self.update_chart() # Clear the chart by use self.ax.clear() and self.canvas.draw()

    def update_chart(self):
        """Update the bar chart with grouped bars per month"""
        self.ax.clear()

        if not self.sales_data:
            # Empty state
            self.ax.text(0.5, 0.5, ' No Data Available\n\nAdd sales data to visualize',
                        ha='center', va='center', transform=self.ax.transAxes,
                        fontsize=14, color="#4C2E5D", style='italic',
                        weight='bold')
            return

        # Define months and categories
        months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
        x = range(len(months))
        categories = {
            "Electronics":"#1A0DD5",
            "Clothing":"#AB0000",
            "Food":"#F78913",
            "Others":"#327B58"
        }
        # Group data by category and month
        grouped_data = {cat: [0]*len(months) for cat in categories}
        for month, amount, category in self.sales_data:
            if category in grouped_data and month in months:
                month_index = months.index(month)
                grouped_data[category][month_index] += amount

        bottom = [0]*len(months)
        for category, color in categories.items():
            amounts = grouped_data[category]
            self.ax.bar(x, amounts, bottom=bottom, color=color, label=category)
            # Update bottom for next stack
            bottom = [b + a for b, a in zip(bottom, amounts)]

        # Styling
        self.ax.set_xlabel('Months', fontsize=12, color="#32003B", fontweight='bold')
        self.ax.set_ylabel('Sales Amount (Baht)', fontsize=13, color='#380016', fontweight='bold')
        self.ax.set_xticks(list(x))
        self.ax.set_xticklabels(months, color="#7C008C", fontsize=12)

        for label in self.ax.get_yticklabels():
            label.set_color("#000000")
            label.set_fontsize(10)

        self.ax.set_title("Monthly Sales by Product Category", fontsize=14, color="#360034",
                        fontweight='bold')
        self.ax.grid(True, which='major', axis='y', linestyle='--', alpha=0.3)

        # Legend on the left side
        self.ax.legend(title="Category", title_fontsize=11, fontsize=9,
                    loc='center left', bbox_to_anchor=(1.0, 0.5), frameon=False)

        self.figure.tight_layout()
        self.canvas.draw()


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":

    main()
