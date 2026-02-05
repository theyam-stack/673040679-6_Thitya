#P2_Registration_Form.py
import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QDateEdit, QComboBox,
    QRadioButton, QButtonGroup, QTextEdit, QPushButton, QCheckBox,
    QVBoxLayout, QHBoxLayout, QMainWindow
)
from PySide6.QtCore import QDate, Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("P2: Student Registration")
        self.setFixedSize(400, 600)

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        self.registration_form = RegistrationForm()
        layout.addWidget(self.registration_form)

class RegistrationForm(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        # Title label
        title = QLabel("Student Registration Form")
        title.setStyleSheet("font-size: 14pt; font-weight: bold;")
        # Create central widget and layout
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        layout.addSpacing(15)

        # Full Name
        layout.addWidget(QLabel("Full Name:"))
        self.name_edit = QLineEdit()
        layout.addWidget(self.name_edit)

        layout.addSpacing(1)

        # Email
        layout.addWidget(QLabel("Email:"))
        self.email_edit = QLineEdit()
        layout.addWidget(self.email_edit)

        layout.addSpacing(1)

        # Phone
        layout.addWidget(QLabel("Phone:"))
        self.phone_edit = QLineEdit()
        layout.addWidget(self.phone_edit)

        layout.addSpacing(1)

        # Date of Birth
        layout.addWidget(QLabel("Date of Birth (dd/MM/yyyy):"))
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDisplayFormat("dd/MM/yyyy")
        self.date_edit.setDate(QDate(2000, 1, 1))
        self.date_edit.setFixedWidth(150)
        layout.addWidget(self.date_edit)

        layout.addSpacing(1)

        # Gender
        # Button group ensures only one can be selected
        layout.addWidget(QLabel("Gender:"))
        gender_layout = QHBoxLayout()
        self.gender_group = QButtonGroup()

        self.male_radio = QRadioButton("Male")
        self.female_radio = QRadioButton("Female")
        self.nonbinary_radio = QRadioButton("Non-binary")
        self.prefer_radio = QRadioButton("Prefer not to say")

        self.gender_group.addButton(self.male_radio)
        self.gender_group.addButton(self.female_radio)
        self.gender_group.addButton(self.nonbinary_radio)
        self.gender_group.addButton(self.prefer_radio)

        gender_layout.addWidget(self.male_radio)
        gender_layout.addWidget(self.female_radio)
        gender_layout.addWidget(self.nonbinary_radio)
        gender_layout.addWidget(self.prefer_radio)

        layout.addLayout(gender_layout)

        layout.addSpacing(15)

        # Program
        layout.addWidget(QLabel("Program:"))
        self.program_combo = QComboBox()
        self.program_combo.setPlaceholderText("Select your program")
        programs = [
            "Computer Engineering",
            "Digital Media Engineering",
            "Environmental Engineering",
            "Electical Engineering",
            "Semiconductor Engineering",
            "Mechanical Engineering",
            "Industrial Engineering",
            "Logistic Engineering",
            "Power Engineering",
            "Electronic Engineering",
            "Telecommunication Engineering",
            "Agricultural Engineering",
            "Civil Engineering",
            "ARIS"
        ]

        self.program_combo.addItems(programs)
        layout.addWidget(self.program_combo)

        layout.addSpacing(5)

        # Personal description
        layout.addWidget(QLabel("Tell us a little bit about yourself:"))
        self.description_edit = QTextEdit()
        self.description_edit.setMaximumHeight(100)
        layout.addWidget(self.description_edit)

        layout.addSpacing(1)

        # Terms and conditions
        self.terms_checkbox = QCheckBox("I accept the terms and conditions.")
        layout.addWidget(self.terms_checkbox)

        layout.addSpacing(20)

        # Submit button
        self.submit_btn = QPushButton("Submit Registration")
        # Add it centered in the layout
        layout.addWidget(self.submit_btn, alignment=Qt.AlignCenter)

        #self.submit_btn.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")

        self.setLayout(layout)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()