import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QComboBox, QSpinBox, QPushButton, QTableWidget,
    QTableWidgetItem, QHeaderView, QMessageBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor

class GradeCalculator(QWidget):
    def __init__(self):
        super().__init__()
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(35, 25, 35, 20) # Left, Top, Right, Bottom
        main_layout.setSpacing(10)

        self.students = {} # Read students.txt file
        with open("c:/Users/asus/Downloads/students.txt", "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split(",")
                    if len(parts) >= 2:
                        sid, name = parts[0].strip(), parts[1].strip()
                        self.students[sid] = name

         # --- Student ID and Name Row ---
        top_row = QHBoxLayout()
        
        # Student ID
        id_label = QLabel("Student ID:")
        id_label.setFont(QFont("Segoe UI", 14, QFont.Bold))

        self.id_combo = QComboBox()
        #self.id_combo.setPlaceholderText("Select Student ID")
        self.id_combo.addItem("Select Student ID")  # Default placeholder
        self.id_combo.addItems(self.students.keys())
        self.id_combo.setFixedHeight(30)
        self.id_combo.setFixedWidth(200)
        self.id_combo.currentTextChanged.connect(self.update_name)
        
        # Student Name
        name_label = QLabel("Student Name:")
        name_label.setFont(QFont("Segoe UI", 14, QFont.Bold))
        
        self.name_display = QLabel("")
        self.name_display.setFont(QFont("Segoe UI", 13, QFont.Bold))
        self.name_display.setFixedHeight(35)
        self.name_display.setStyleSheet("""
            background-color: #FCF5EE;
            color: #660B05;
            padding: 2px 15px;
            border: 2px solid #660B05;
            border-radius: 8px;
            font-size: 14px;
        """)
        
        top_row.addWidget(id_label)
        top_row.addWidget(self.id_combo)
        top_row.addSpacing(40)
        top_row.addWidget(name_label)
        top_row.addWidget(self.name_display, 1)
        
        main_layout.addLayout(top_row)
        main_layout.addSpacing(10)

        # --- Scores Row ---
        scores_row = QHBoxLayout()
        
        # Math
        math_label = QLabel("Math:")
        math_label.setFont(QFont("Segoe UI", 10, QFont.Bold, italic=True))
        self.math_spin = QSpinBox()

        self.math_spin.setRange(0, 100)
        self.math_spin.setSingleStep(5)  # Step by 5 as requested
        self.math_spin.setValue(50)

        self.math_spin.setFixedHeight(40)
        self.math_spin.setFixedWidth(80)
        #self.math_spin.setAlignment(Qt.AlignCenter)
        
        # Science
        sci_label = QLabel("Science:")
        sci_label.setFont(QFont("Segoe UI", 10, QFont.Bold, italic=True))
        self.sci_spin = QSpinBox()

        self.sci_spin.setRange(0, 100)
        self.sci_spin.setSingleStep(5)  # Step by 5 as requested
        self.sci_spin.setValue(50)

        self.sci_spin.setFixedHeight(40)
        self.sci_spin.setFixedWidth(80)
        #self.sci_spin.setAlignment(Qt.AlignCenter)
        
        # English
        eng_label = QLabel("English:")
        eng_label.setFont(QFont("Segoe UI", 10, QFont.Bold, italic=True))
        self.eng_spin = QSpinBox()

        self.eng_spin.setRange(0, 100)
        self.eng_spin.setSingleStep(5)  # Step by 5 as requested
        self.eng_spin.setValue(50)

        self.eng_spin.setFixedHeight(40)
        self.eng_spin.setFixedWidth(80)
        #self.eng_spin.setAlignment(Qt.AlignCenter)
        
        scores_row.addWidget(math_label)
        scores_row.addWidget(self.math_spin)
        scores_row.addSpacing(20)
        scores_row.addWidget(sci_label)
        scores_row.addWidget(self.sci_spin)
        scores_row.addSpacing(20)
        scores_row.addWidget(eng_label)
        scores_row.addWidget(self.eng_spin)
        scores_row.setAlignment(Qt.AlignRight)  # Align Right
        
        main_layout.addLayout(scores_row)
        main_layout.addSpacing(10)

        # --- Table ---
        self.table = QTableWidget(0, 8)
        self.table.setHorizontalHeaderLabels([
            "Student ID", "Name", "Math", "Science", "English",
            "Total", "Average", "Grade"
        ])
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Fixed)
        self.table.setColumnWidth(1, 250)  # adjust 200 to your preferred width
        #self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        for i in range(2, 8):
            self.table.horizontalHeader().setSectionResizeMode(i, QHeaderView.Stretch)
            #self.table.horizontalHeaderItem(i).setTextAlignment(Qt.AlignCenter)
            #self.table.horizontalHeader().setSectionResizeMode(i, QHeaderView.ResizeToContents)
        
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.verticalHeader().setVisible(True)
        
        main_layout.addWidget(self.table)
        main_layout.addSpacing(10)

        self.setLayout(main_layout)

        # --- Buttons ---
        btn_layout = QHBoxLayout()
        
        add_btn = QPushButton("➕ Add Student")
        add_btn.setFont(QFont("Segoe UI", 12, QFont.DemiBold))
        add_btn.setFixedHeight(45)
        add_btn.setFixedWidth(200)
        add_btn.clicked.connect(self.add_student)
        
        reset_btn = QPushButton("🔄 Reset Input")
        reset_btn.setFont(QFont("Segoe UI", 12, QFont.DemiBold))
        reset_btn.setFixedHeight(45)
        reset_btn.setFixedWidth(200)
        reset_btn.clicked.connect(self.reset_input)
        
        clear_btn = QPushButton("🗑️ Clear All")
        clear_btn.setFont(QFont("Segoe UI", 12, QFont.DemiBold))
        clear_btn.setFixedHeight(45)
        clear_btn.setFixedWidth(200)
        clear_btn.clicked.connect(self.clear_all)
        
        btn_layout.addWidget(add_btn)
        btn_layout.addWidget(reset_btn)
        btn_layout.addWidget(clear_btn)
        btn_layout.setAlignment(Qt.AlignCenter)  # Align buttons to the center

        main_layout.addLayout(btn_layout)
        self.setLayout(main_layout)
        
        # Apply simple styles
        self.setStyleSheet("""
            QWidget {
                background-color: #black;
                font-family: Segoe UI;
                font-size: 14px;
            }
            QLabel {
                color: #f0f0f0;
            }
            QComboBox {
                padding: 5px;
                border: 1px solid #CC561E;
                border-radius: 5px;
                background-color: #A03A13;
            }
            QSpinBox {
                padding: 2px;
                border: 2px solid #CC561E;
                border-radius: 8px;
                background-color: #FF6600;
            }
            QSpinBox::up-button, QSpinBox::down-button {
                width: 20px;
                height: 20px;
            }
            QPushButton {
                background-color: #BDE8F5;
                color: black;
                border: 1px solid #6BB6D6;
                border-radius: 20px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #3A9AFF;
            }
            QPushButton:pressed {
                background-color: #4988C4;
            }
            QTableWidget {
                background-color: none;
                border: 1px solid #ccc;
                gridline-color: #F5F2F2;
            }
            QHeaderView::section {
                background-color: #660B05;
                padding: 5px;
                border: 1px solid #bbb;
                font-weight: medium;
            }
        """)
    def update_name(self, sid):
        """Update name display when student ID changes"""
        if sid == "Select Student ID":
            self.name_display.setText("")
        else:
            name = self.students.get(sid, "")
            self.name_display.setText(name)

    def add_student(self):
        """Add student record to table"""
        sid = self.id_combo.currentText() 
        if sid == "Select Student ID":
            QMessageBox.warning(self, "Error", "Please select a student ID")
            return
        
        name = self.students.get(sid, "")
        math = self.math_spin.value()
        sci = self.sci_spin.value()
        eng = self.eng_spin.value()

        total = math + sci + eng
        avg = total / 3
        grade = self.calculate_grade(avg)

        # Check if student already exists
        for row in range(self.table.rowCount()):
            if self.table.item(row, 0).text() == sid:
                reply = QMessageBox.question(self, "Duplicate", 
                    f"Student {sid} already exists. Update scores?",
                    QMessageBox.Yes | QMessageBox.No)
                if reply == QMessageBox.Yes:
                    self.update_row(row, sid, name, math, sci, eng, total, avg, grade)
                return
        # Add new row
        row = self.table.rowCount()
        self.table.insertRow(row)
        
        data = [sid, name, str(math), str(sci), str(eng),
                str(total), f"{avg:.2f}", grade]
        
        for col, val in enumerate(data):
            item = QTableWidgetItem(val)
            item.setTextAlignment(Qt.AlignCenter)
            
            # Color code individual scores that are below 50
            if col in [2, 3, 4]:  # Math, Science, English columns
                score = int(val)
                if score < 50:
                    item.setBackground(QColor(255, 200, 200))  # Light red
            
            # Apply color to grade column
            if col == 7:
                self.apply_grade_color(item, val)
            
            self.table.setItem(row, col, item)

        # Sort by Student ID
        self.table.sortItems(0, Qt.AscendingOrder)
        
        self.reset_input()

    def update_row(self, row, sid, name, math, sci, eng, total, avg, grade):
        """Update existing row"""
        data = [sid, name, str(math), str(sci), str(eng),
                str(total), f"{avg:.2f}", grade]
        
        for col, val in enumerate(data):
            item = QTableWidgetItem(val)
            item.setTextAlignment(Qt.AlignCenter)
            
            # Color code individual scores
            if col in [2, 3, 4]:
                score = int(val)
                if score < 50:
                    item.setBackground(QColor(255, 200, 200))
            if col == 7:
                self.apply_grade_color(item, val)
            
            self.table.setItem(row, col, item)

    def apply_grade_color(self, item, grade):
        """Apply color to grade based on letter grade"""
        if grade == "A":
            item.setBackground(QColor(("#33ba33")))  # Light green
        elif grade == "B":
            item.setBackground(QColor(("#2fccaf")))  # Light blue
        elif grade == "C":
            item.setBackground(QColor(("#d1d132")))  # Light yellow
        elif grade == "D":
            item.setBackground(QColor(("#cf8632")))  # Light orange
        elif grade == "F":
            item.setBackground(QColor(("#d54848")))  # Light red

    def reset_input(self):
        """Reset input fields"""
        self.id_combo.setCurrentIndex(0)
        self.math_spin.setValue(0)
        self.sci_spin.setValue(0)
        self.eng_spin.setValue(0)
        self.name_display.setText("")

    def clear_all(self):
        """Clear all records from table"""
        if self.table.rowCount() == 0:
            return
            
        reply = QMessageBox.question(self, "Confirm", 
            "Clear all records?",
            QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            self.table.setRowCount(0)

    def calculate_grade(self, avg):
        """Calculate letter grade from average"""
        if avg >= 80: return "A"
        elif avg >= 70: return "B"
        elif avg >= 60: return "C"
        elif avg >= 50: return "D"
        else: return "F"

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🎓 Student Grade Calculator")
        self.setGeometry(200, 100, 900, 700)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.grade_calculator = GradeCalculator()
        main_layout.addWidget(self.grade_calculator)
        self.setLayout(main_layout)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
if __name__ == "__main__":
    main()
