#P3_BMI_Calculator
import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                               QComboBox, QTableWidget, QTableWidgetItem, QHeaderView)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BMI Calculator")
        self.setFixedSize(400, 700)

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        self.bmi = BMICalculatorUI()
        layout.addWidget(self.bmi)
        
        central_widget.setLayout(layout)


class BMICalculatorUI(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(15)

        # Header
        header = QLabel("Adult and Child BMI Calculator")
        header.setFont(QFont("Arial", 14, QFont.Bold))
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("""
            background-color: #8B4A4A;
            color: white;
            padding: 8px;
            border-radius: 5px;
        """)
        layout.addWidget(header)

        # Calculate BMI for
        calc_for_layout = QHBoxLayout()
        calc_for_label = QLabel("Calculate BMI for")
        calc_for_label.setFont(QFont("Arial", 12))
        
        self.age_combo = QComboBox()
        self.age_combo.addItems(["Adult Age 20+", "Child Age 2-19"])
        self.age_combo.setFixedHeight(35)
        self.age_combo.setFixedWidth(100)
        self.age_combo.setStyleSheet("""
            QComboBox {
                padding: 5px 10px;
                border: 1px solid #999;
                border-radius: 3px;
                font-size: 12px;
                background-color: white;
            }
        """)
        calc_for_layout.addWidget(calc_for_label)
        calc_for_layout.addWidget(self.age_combo)
        calc_for_layout.setAlignment(Qt.AlignCenter)
        
        layout.addLayout(calc_for_layout)
        layout.addSpacing(10)

        # Weight 
        weight_label = QLabel("Weight")
        weight_label.setFont(QFont("Arial", 12))
        weight_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        layout.addWidget(weight_label)

        weight_layout = QHBoxLayout()
        weight_input = QLineEdit()
        weight_input.setPlaceholderText("Enter weight")
        weight_unit = QComboBox()
        weight_unit.addItems(["kg", "lb"])
        weight_layout.addWidget(weight_input)
        weight_layout.addWidget(weight_unit)
        layout.addLayout(weight_layout)

        # Height
        height_label = QLabel("Height")
        height_label.setFont(QFont("Arial", 12))
        layout.addWidget(height_label)

        height_layout = QHBoxLayout()
        height_input = QLineEdit()
        height_input.setPlaceholderText("Enter height")
        height_unit = QComboBox()
        height_unit.addItems(["cm", "m", "ft/in"])
        height_layout.addWidget(height_input)
        height_layout.addWidget(height_unit)
        layout.addLayout(height_layout)

        # Buttons
        btn_layout = QHBoxLayout()
        clear_btn = QPushButton("Clear")
        clear_btn.setStyleSheet("background-color: #f44336; color: white; font-weight: bold;")
        calc_btn = QPushButton("Calculate")
        calc_btn.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")
        btn_layout.addWidget(clear_btn)
        btn_layout.addWidget(calc_btn)
        layout.addLayout(btn_layout)

        # Answer White BG Container
        answer_container = QWidget()
        answer_container.setStyleSheet("""
            #background-color: white;
            border: 1px solid #999;
            border-radius: 5px;
        """)
        
        answer_layout = QVBoxLayout()
        answer_layout.setContentsMargins(15, 15, 15, 15)
        answer_layout.setSpacing(15)
        
        answer_title = QLabel("Answer:")
        answer_title.setFont(QFont("Arial", 11))
        
        bmi_result_label = QLabel("BMI =")
        bmi_result_label.setFont(QFont("Arial", 16, QFont.Bold))
        bmi_result_label.setAlignment(Qt.AlignCenter)
        
        adult_bmi_label = QLabel("Adult BMI")
        adult_bmi_label.setFont(QFont("Arial", 14, QFont.Bold))
        adult_bmi_label.setAlignment(Qt.AlignCenter)
        
        answer_layout.addWidget(answer_title)
        answer_layout.addWidget(bmi_result_label)
        answer_layout.addWidget(adult_bmi_label)
        
        # BMI Table
        table = QTableWidget()
        table.setRowCount(4)
        table.setColumnCount(2)
        table.setHorizontalHeaderLabels(["BMI", "Status"])
        
        # Set table properties
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.verticalHeader().setVisible(False)
        table.setEditTriggers(QTableWidget.NoEditTriggers)
        table.setSelectionMode(QTableWidget.NoSelection)
        
        # Style header
        table.horizontalHeader().setStyleSheet("""
            QHeaderView::section {
                background-color: #D0D0D9;
                border: 1px solid #999;
                padding: 8px;
                font-weight: bold;
                font-size: 12px;
            }
        """)
        
        # Row 1 - Underweight (Yellow)
        item1_bmi = QTableWidgetItem("< 18.5")
        item1_bmi.setTextAlignment(Qt.AlignCenter)
        item1_bmi.setBackground(QColor(244, 208, 63))  # Yellow
        item1_status = QTableWidgetItem("Underweight")
        item1_status.setTextAlignment(Qt.AlignCenter)
        table.setItem(0, 0, item1_bmi)
        table.setItem(0, 1, item1_status)
        
        # Row 2 - Healthy Weight (Green)
        item2_bmi = QTableWidgetItem("18.5 - 24.9")
        item2_bmi.setTextAlignment(Qt.AlignCenter)
        item2_bmi.setBackground(QColor(130, 224, 170))  # Green
        item2_status = QTableWidgetItem("Healthy Weight")
        item2_status.setTextAlignment(Qt.AlignCenter)
        table.setItem(1, 0, item2_bmi)
        table.setItem(1, 1, item2_status)
        
        # Row 3 - Overweight (Orange)
        item3_bmi = QTableWidgetItem("25.0 - 29.9")
        item3_bmi.setTextAlignment(Qt.AlignCenter)
        item3_bmi.setBackground(QColor(248, 184, 120))  # Orange
        item3_status = QTableWidgetItem("Overweight")
        item3_status.setTextAlignment(Qt.AlignCenter)
        table.setItem(2, 0, item3_bmi)
        table.setItem(2, 1, item3_status)
        
        # Row 4 - Obese (Red)
        item4_bmi = QTableWidgetItem("≥ 30.0")
        item4_bmi.setTextAlignment(Qt.AlignCenter)
        item4_bmi.setBackground(QColor(229, 115, 115))  # Red
        item4_status = QTableWidgetItem("Obese")
        item4_status.setTextAlignment(Qt.AlignCenter)
        table.setItem(3, 0, item4_bmi)
        table.setItem(3, 1, item4_status)
        
        # Set row heights
        for i in range(4):
            table.setRowHeight(i, 39)
        
        table.setStyleSheet("""
            QTableWidget {
                gridline-color: #999;
            }
        """)
        
        answer_layout.addWidget(table)
        answer_container.setLayout(answer_layout)
        
        layout.addWidget(answer_container)
        
        self.setLayout(layout)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()