#P1_login_UI
import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QLabel, QLineEdit, QPushButton, QCheckBox, QFrame)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login Page")
        self.setFixedSize(420, 600)

        # Create central widget and layout
        self.setCentralWidget(LoginUI())
        layout = QVBoxLayout(LoginUI())
        self.login_UI = LoginUI()
        layout.addWidget(self.login_UI)

class LoginUI(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        layout.setContentsMargins(50, 50, 50, 50)
        layout.setSpacing(0)
        layout.setAlignment(Qt.AlignTop)

        # Title
        title = QLabel("LOGIN")
        title.setFont(QFont("Arial", 19, QFont.Bold))
        title.setAlignment(Qt.AlignLeft)
        layout.addWidget(title)

        layout.addSpacing(20)

        # Email
        email_label = QLabel("Email")
        email_label.setFont(QFont("Arial", 14))
        layout.addWidget(email_label)

        layout.addSpacing(6)

        email_input = QLineEdit()
        #email_input.setFixedWidth(350)
        email_input.setPlaceholderText("Enter your email")
        layout.addWidget(email_input)

        layout.addSpacing(25)

        # Password
        password_label = QLabel("Password")
        password_label.setFont(QFont("Arial", 14))
        layout.addWidget(password_label)

        layout.addSpacing(6)

        password_input = QLineEdit()
        password_input.setEchoMode(QLineEdit.Password)
        #password_input.setFixedWidth(350)
        password_input.setPlaceholderText("Enter your password")
        layout.addWidget(password_input)

        layout.addSpacing(10)

        # Remember Me
        remember_check = QCheckBox("Remember me?")
        #remember_check.setStyleSheet("background-color: #FF4081; ")
        layout.addWidget(remember_check)
        layout.addSpacing(20)

        # Login Button
        login_btn = QPushButton("LOGIN")
        login_btn.setFont(QFont("Arial", 12, QFont.Bold))
        login_btn.setStyleSheet("background-color: #FF4081; color: white; height: 40px;")
        layout.addWidget(login_btn)

        layout.addSpacing(8)

        # Forgot Password
        forgot_label = QLabel("<a>Forgot Password?</a>")
        forgot_label.setFont(QFont("Arial", 10))
        forgot_label.setAlignment(Qt.AlignRight)
        forgot_label.setOpenExternalLinks(False)  # not clickable yet
        layout.addWidget(forgot_label)

        layout.addSpacing(30)

        # OR Separator
        sep_layout = QHBoxLayout()
        line_left = QFrame()
        line_left.setFrameShape(QFrame.HLine)
        line_left.setStyleSheet("color: gray;")
        sep_layout.addWidget(line_left)

        or_label = QLabel("OR")
        or_label.setFont(QFont("Arial", 12, QFont.Bold))
        or_label.setAlignment(Qt.AlignCenter)
        sep_layout.addWidget(or_label)

        line_right = QFrame()
        line_right.setFrameShape(QFrame.HLine)
        line_right.setStyleSheet("color: gray;")
        sep_layout.addWidget(line_right)

        layout.addLayout(sep_layout)
        layout.addSpacing(20)

        # Social Icons (styled buttons)
        social_layout = QHBoxLayout()
        social_layout.setSpacing(20)

        google_button = QPushButton("G")
        google_button.setFixedSize(55, 55)
        google_button.setFont(QFont("Arial", 22, QFont.Bold))
        google_button.setStyleSheet("""
            QPushButton {
                background-color: white;
                border: 3px solid #DB4437;
                border-radius: 27px;
                color: #DB4437;
            }
            QPushButton:hover {
                background-color: #FFF5F5;
            }
        """)

        facebook_button = QPushButton("f")
        facebook_button.setFixedSize(55, 55)
        facebook_button.setFont(QFont("Arial", 24, QFont.Bold))
        facebook_button.setStyleSheet("""
            QPushButton {
                background-color: white;
                border: 3px solid #4267B2;
                border-radius: 27px;
                color: #4267B2;
            }
            QPushButton:hover {
                background-color: #F0F5FF;
            }
        """)

        linkedin_button = QPushButton("in")
        linkedin_button.setFixedSize(55, 55)
        linkedin_button.setFont(QFont("Arial", 22, QFont.Bold))
        linkedin_button.setStyleSheet("""
            QPushButton {
                background-color: white;
                border: 3px solid #0077B5;
                border-radius: 27px;
                color: #0077B5;
            }
            QPushButton:hover {
                background-color: #F0F8FF;
            }
        """)

        social_layout.addStretch()
        social_layout.addWidget(google_button)
        social_layout.addWidget(facebook_button)
        social_layout.addWidget(linkedin_button)
        social_layout.addStretch()

        layout.addLayout(social_layout)
        layout.addSpacing(20)

        # Sign Up
        signup_label = QLabel("Need an account? <a href='#'>SIGN UP</a>")
        signup_label.setFont(QFont("Arial", 10))
        signup_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(signup_label)

        self.setLayout(layout)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()