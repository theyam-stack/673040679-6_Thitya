import sys
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QFont
from PySide6.QtWidgets import (QApplication, QMainWindow, QLabel,
                             QVBoxLayout, QWidget, QHBoxLayout,
                             QGridLayout, QFormLayout, QLineEdit,
                             QSpinBox, QPushButton)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculator")
        self.setCentralWidget(CalculatorLayout())
        self.resize(350, 570)


class CalculatorLayout(QWidget):
    def __init__(self):
        super().__init__()

         # Create main layout
        main_layout = QVBoxLayout()
        
        # Display section
        display_layout = QVBoxLayout()
        calc_type = QLabel("Standard Calculator")
        calc_type.setFont(QFont("Arial", 14, QFont.DemiBold))

        self.current_value = "0"
        self.display = QLabel(self.current_value)
        self.display.setFont(QFont("Arial", 26, QFont.DemiBold))
        self.display.setAlignment(Qt.AlignRight)
        #self.display.setStyleSheet("padding: 10px; background-color: #f0f0f0;")

        display_layout.addWidget(calc_type)
        display_layout.addWidget(self.display)

        layout = QGridLayout()
        
         # Basic grid positioning
        bottom_percent = QPushButton("%")
        bottom_percent.clicked.connect(lambda: self.append_value("%"))
        bottom_CE = QPushButton("CE")
        bottom_CE.clicked.connect(lambda: self.append_value("CE"))
        bottom_C = QPushButton("C")
        bottom_C.clicked.connect(lambda: self.append_value("C"))
        bottom_back = QPushButton("<-")
        bottom_back.clicked.connect(lambda: self.append_value("<-"))

        layout.addWidget(bottom_percent, 0, 0)  # row 0, col 0
        layout.addWidget(bottom_CE, 0, 1)  # row 0, col 1
        layout.addWidget(bottom_C, 0, 2)  # row 0, col 2
        layout.addWidget(bottom_back, 0, 3)
        
        bottom_1overx = QPushButton("1/x")
        bottom_1overx.clicked.connect(lambda: self.append_value("1/x"))
        bottom_pow2 = QPushButton("x^2")
        bottom_pow2.clicked.connect(lambda: self.append_value("x^2"))
        bottom_sqrt = QPushButton("sqrt(x)")
        bottom_sqrt.clicked.connect(lambda: self.append_value("sqrt(x)"))
        bottom_divide = QPushButton("/")
        bottom_divide.clicked.connect(lambda: self.append_value("/"))

        layout.addWidget(bottom_1overx, 1, 0)  # row 0, col 0
        layout.addWidget(bottom_pow2, 1, 1)  # row 0, col 1
        layout.addWidget(bottom_sqrt, 1, 2)  # row 0, col 2
        layout.addWidget(bottom_divide, 1, 3)

        button7 = QPushButton("7")
        button7.clicked.connect(lambda: self.append_value("7"))
        button8 = QPushButton("8")
        button8.clicked.connect(lambda: self.append_value("8"))
        button9 = QPushButton("9")
        button9.clicked.connect(lambda: self.append_value("9"))
        buttonMultiply = QPushButton("x")
        buttonMultiply.clicked.connect(lambda: self.append_value("x"))

        layout.addWidget(button7, 2, 0)  # row 0, col 0
        layout.addWidget(button8, 2, 1)  # row 0, col 1
        layout.addWidget(button9, 2, 2)  # row 0, col 2
        layout.addWidget(buttonMultiply, 2, 3)

        button4 = QPushButton("4")
        button4.clicked.connect(lambda: self.append_value("4"))
        button5 = QPushButton("5")
        button5.clicked.connect(lambda: self.append_value("5"))
        button6 = QPushButton("6")
        button6.clicked.connect(lambda: self.append_value("6"))
        buttonMinus = QPushButton("-")  
        buttonMinus.clicked.connect(lambda: self.append_value("-"))

        layout.addWidget(button4, 3, 0)  # row 0, col 0
        layout.addWidget(button5, 3, 1)  # row 0, col 1
        layout.addWidget(button6, 3, 2)  # row 0, col 2
        layout.addWidget(buttonMinus, 3, 3)

        button1 = QPushButton("1")
        button1.clicked.connect(lambda: self.append_value("1"))
        button2 = QPushButton("2")
        button2.clicked.connect(lambda: self.append_value("2"))
        button3 = QPushButton("3")
        button3.clicked.connect(lambda: self.append_value("3"))
        buttonPlus = QPushButton("+")
        buttonPlus.clicked.connect(lambda: self.append_value("+"))

        layout.addWidget(button1, 4, 0)  # row 0, col 0
        layout.addWidget(button2, 4, 1)  # row 0, col 1
        layout.addWidget(button3, 4, 2)  # row 0, col 2
        layout.addWidget(buttonPlus, 4, 3)

        button0 = QPushButton("0")
        button0.clicked.connect(lambda: self.append_value("0"))
        buttonE = QPushButton("=")
        buttonE.clicked.connect(lambda: self.append_value("="))
        buttonPoint = QPushButton(".")
        buttonPoint.clicked.connect(lambda: self.append_value("."))
        buttonPlusMinus = QPushButton("+/-")
        buttonPlusMinus.clicked.connect(lambda: self.append_value("+/-"))

        layout.addWidget(buttonPlusMinus, 5, 0)  # row 0, col 0
        layout.addWidget(button0, 5, 1)  # row 0, col 1
        layout.addWidget(buttonPoint, 5, 2)  # row 0, col 2
        layout.addWidget(buttonE, 5, 3)

        self.setStyleSheet("""
        CalculatorLayout {
            background-color: #262626;
        }
                           
        QPushButton {
            min-width: 30px;
            min-height: 42px;
            font-size: 18px;
            background-color: #6D016A;
        }
        QLabel {
            color: #FA891A;
            font-family: Titillium;
            padding: 5px;
        }
        """)
                
        # Add display to main layout
        main_layout.addLayout(display_layout)
        main_layout.addLayout(layout)
        
        # Set the layout for MainWindow
        self.setLayout(main_layout)

    def append_value(self, new_value):
        if self.current_value == "0":
            self.current_value = str(new_value)

        elif new_value == "C": # Clear all memory
            self.current_value = "0"

        elif new_value == "CE": # Clear Last Entry
            self.current_value = "0"

        elif new_value == "<-": # Backspace
            self.current_value = self.current_value[:-1] if len(self.current_value) > 1 else "0"

        elif new_value == "/": # Divide
            self.current_value += "/"
        
        elif new_value == "+": # Add
            self.current_value += "+"
        
        elif new_value == "-": # Subtract
            self.current_value += "-"
        
        elif new_value == "x": # Multiply
            self.current_value += "*"

        elif new_value == "%": # Modulo
            self.current_value += "%"

        elif new_value == "1/x":  # Reciprocal
            try:
                value = float(self.current_value)
                self.current_value = str(1 / value)
            except ZeroDivisionError:
                self.current_value = "Error"
            except ValueError:
                self.current_value = "Error"

        elif new_value == "=":  # Evaluate expression
            try:
                expr = (
                    self.current_value
                    .replace("x^2", "**2")
                    .replace("sqrt(x)", "**0.5")
                    .replace("+/-", "*-1")
                    .replace("1/x", "1/")   # <-- handle reciprocal
                )
                result = str(eval(expr))
                self.current_value = result
            except Exception:
                self.current_value = "Error"

        else:
            self.current_value += str(new_value)
        
        #display update value
        self.display.setText(self.current_value)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()