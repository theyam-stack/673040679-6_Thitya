#P1_bmiCal
import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QLineEdit,
    QPushButton, QComboBox, QVBoxLayout, QFormLayout,
    QGridLayout, QHBoxLayout
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

kg = "kilograms"
lb = "pounds"
cm = "centimeters"
m = "meters"
ft = "feet"
adult = "Adults 20+"
child = "Children and Teenagers (5-19)"

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("P1: BMI Calculator")
        self.setGeometry(100, 100, 300, 450)

        self.input_section = InputSection()
        self.output_section = OutputSection()

        result_container = QWidget()
        result_container.setStyleSheet("background-color: #F4EBDD;")
        result_layout = QVBoxLayout()
        result_layout.setContentsMargins(20, 20, 20, 20)
        result_layout.addWidget(self.output_section)
        result_container.setLayout(result_layout)

        central = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.addWidget(self.input_section)
        main_layout.addWidget(result_container)
        central.setLayout(main_layout)

        self.setCentralWidget(central)

        self.input_section.submit_btn.clicked.connect(
            lambda: self.input_section.submit(self.output_section))
        self.input_section.clear_btn.clicked.connect(
            lambda: self.input_section.clear(self.output_section))

class InputSection(QWidget):
    def __init__(self):
        super().__init__()
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignTop)

        # HEADER
        header = QLabel("Adult and Child BMI Calculator")
        header.setAlignment(Qt.AlignCenter)
        header.setFont(QFont("Arial", 12, QFont.Bold))
        header.setStyleSheet("""
            background-color: #8B3A3A;
            color: white;
            padding: 4px;
        """)
        main_layout.addWidget(header)
        main_layout.addSpacing(20)

        form = QFormLayout()
        form.setVerticalSpacing(10)

        # AGE GROUP
        self.age_group = QComboBox()
        self.age_group.addItems([adult, child])
        form.addRow("BMI age group:", self.age_group)

        # WEIGHT layout (input + unit inline) 
        self.weight_input = QLineEdit("")
        self.weight_input.setFixedWidth(110)

        self.weight_unit = QComboBox()
        self.weight_unit.addItems([kg, lb])
        #self.weight_unit.setFixedWidth(120)

        weight_layout = QHBoxLayout()
        weight_layout.addWidget(self.weight_input)
        weight_layout.addSpacing(15)
        weight_layout.addWidget(self.weight_unit)   

        form.addRow("Weight:", weight_layout)

        # HEIGHT ROW (input + unit inline)
        self.height_input = QLineEdit("")
        self.height_input.setFixedWidth(110)

        self.height_unit = QComboBox()
        self.height_unit.addItems([cm, m, ft])
        #self.height_unit.setFixedWidth(120)

        height_row = QHBoxLayout()
        height_row.addWidget(self.height_input)
        height_row.addSpacing(15)
        height_row.addWidget(self.height_unit)

        form.addRow("Height:", height_row)

        main_layout.addLayout(form)
        main_layout.addSpacing(20)

        # BUTTONS
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        self.clear_btn = QPushButton("clear")
        self.clear_btn.setFixedWidth(150)
        self.submit_btn = QPushButton("Submit Registration")
        self.submit_btn.setFixedWidth(165)

        btn_layout.addWidget(self.clear_btn)
        btn_layout.addSpacing(10)
        btn_layout.addWidget(self.submit_btn)

        btn_layout.addStretch()
        main_layout.addSpacing(10)
        main_layout.addLayout(btn_layout)

        self.setLayout(main_layout)

    def clear(self, output):
        self.weight_input.clear()
        self.height_input.clear()
        output.clear()

    def calculate(self):
        try:
            w = float(self.weight_input.text())
            h = float(self.height_input.text())

            if w <= 0 or h <= 0:
                return 0
            if self.weight_unit.currentText() == lb:
                w *= 0.453592
            if self.height_unit.currentText() == cm:
                h /= 100
            elif self.height_unit.currentText() == ft:
                h *= 0.3048
            return round(w / (h ** 2), 2)
        except:
            return 0

    def submit(self, output):
        bmi = self.calculate()
        if bmi is not None:
            output.update(bmi, self.age_group.currentText())

class OutputSection(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.setLayout(self.layout)

        self.title = QLabel("Your BMI")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setFont(QFont("Arial", 10))
        self.title.setStyleSheet("color: black;")
        self.layout.addSpacing(10)
        self.layout.addWidget(self.title)

        self.value = QLabel("0.00")
        self.value.setAlignment(Qt.AlignCenter)
        self.value.setFont(QFont("Arial", 22, QFont.Bold))
        self.value.setStyleSheet("color: #5B5BFF;")
        self.layout.addWidget(self.value)
        self.layout.addSpacing(15)

        # Placeholder container for dynamic content
        self.dynamic_container = QVBoxLayout()
        self.layout.addLayout(self.dynamic_container)

    def update(self, bmi, group):
        self.value.setText(f"{bmi:.2f}")
        self.clear_dynamic()
        if group == adult:
            self.show_adult_table()
        else:
            self.show_child_links()

    def show_adult_table(self):
        table = QGridLayout()

        header1 = QLabel("BMI")
        header1.setFont(QFont("Arial", 11, QFont.Bold))
        header1.setStyleSheet("color: black;")
        header2 = QLabel("Condition")
        header2.setFont(QFont("Arial", 11, QFont.Bold))
        header2.setStyleSheet("color: black;")

        table.addWidget(header1, 0, 0)   
        table.addWidget(header2, 0, 1)

        data = [
            ("< 18.5", "Thin"),
            ("18.5 - 25.0", "Normal"),
            ("25.1 - 30.0", "Overweight"),
            ("> 30.0", "Obese"),
        ]
        for i, (b, c) in enumerate(data, start=1):
            label1 = QLabel(b)
            label1.setStyleSheet("color: black;")
            label2 = QLabel(c)
            label2.setStyleSheet("color: black;")
            table.addWidget(label1, i, 0)
            table.addWidget(label2, i, 1)
        self.dynamic_container.addLayout(table)

    # Child Links
    def show_child_links(self):
        text = QLabel(
            "For child's BMI interpretation, please click one of the following links."
        )
        text.setFont(QFont("Arial", 9))
        text.setAlignment(Qt.AlignCenter)
        text.setStyleSheet("color: black;")
        text.setWordWrap(True)
        self.dynamic_container.addSpacing(30)
        self.dynamic_container.addWidget(text)

        link_layout = QHBoxLayout()
        boy_link = QLabel('<a href="https://cdn.who.int/media/docs/default-source/child-growth/growth-reference-5-19-years/bmi-for-age-(5-19-years)/cht-bmifa-boys-z-5-19years.pdf?sfvrsn=4007e921_4">BMI graph for BOYS</a>')
        girl_link = QLabel('<a href="https://cdn.who.int/media/docs/default-source/child-growth/growth-reference-5-19-years/bmi-for-age-(5-19-years)/cht-bmifa-girls-z-5-19years.pdf?sfvrsn=c708a56b_4">BMI graph for GIRLS</a>')
        boy_link.setOpenExternalLinks(True)
        girl_link.setOpenExternalLinks(True)

        link_layout.addStretch()
        link_layout.addWidget(boy_link)
        link_layout.addSpacing(15)
        link_layout.addWidget(girl_link)
        link_layout.addStretch()

        self.dynamic_container.addLayout(link_layout)

    def clear(self):
        self.value.setText("0.00")
        self.clear_dynamic()

    def clear_dynamic(self):
        while self.dynamic_container.count():
            item = self.dynamic_container.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self.clear_layout(item.layout())

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self.clear_layout(item.layout())

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
if __name__ == "__main__":
    main()
