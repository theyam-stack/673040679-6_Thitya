#P1_Personal_Info_Card, Name, Age, Email, Position, Favorite Color
from PySide6.QtWidgets import (QApplication, QMainWindow, QMessageBox, QStatusBar, 
                               QWidget, QVBoxLayout, QFormLayout, QHBoxLayout, QLabel, 
                               QComboBox, QLineEdit, QPushButton, QFrame, QSpinBox, 
                               QColorDialog, QFileDialog, QToolBar, QTextEdit)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QAction, QIcon, QPixmap, QFont
import sys, pyperclip

default_color = "#ADE9F1"

class InfoCardApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("P1: Personal Info Card")
        self.setGeometry(500, 200, 400, 500)

        # Central Widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        # Input Form Section
        form_widget = self.create_form_section()
        layout.addWidget(form_widget)

        # Separator line
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet("background-color: #BDC3C9;")
        layout.addWidget(separator)

        # Display Card Section
        self.display_area = QWidget()
        self.display_layout = QVBoxLayout(self.display_area)
        self.display_layout.setContentsMargins(0, 0, 0, 0)
        self.display_layout.setAlignment(Qt.AlignTop)
        layout.addWidget(self.display_area)
        layout.addStretch()

        # Display Area
        self.display = QTextEdit()
        self.display.setReadOnly(True)
        self.display_area = QWidget()
        self.display_layout = QVBoxLayout(self.display_area)
        self.display_layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.display_area)

        # Menu Bar
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")
        edit_menu = menubar.addMenu("Edit")

        gen_action = QAction(QIcon("c:/Users/asus/OneDrive/รูปภาพ/Icons_png/generate.png"), "Generate Card", self)
        gen_action.triggered.connect(self.generate_card)
        save_action = QAction(QIcon("c:/Users/asus/OneDrive/รูปภาพ/Icons_png/save.png"), "Save Card", self)
        save_action.triggered.connect(self.save_card)
        clear_disp_action = QAction(QIcon("c:/Users/asus/OneDrive/รูปภาพ/Icons_png/clearAll.png"), "Clear Display", self)
        clear_disp_action.triggered.connect(self.clear_display)
        exit_action = QAction(QIcon("c:/Users/asus/OneDrive/รูปภาพ/Icons_png/close.png"), "Exit", self)
        exit_action.triggered.connect(self.close)

        file_menu.addActions([gen_action, save_action, clear_disp_action, exit_action])

        copy_action = QAction(QIcon("c:/Users/asus/OneDrive/รูปภาพ/Icons_png/copy.png"), "Copy Card", self)
        copy_action.triggered.connect(self.copy_card)
        clear_form_action = QAction(QIcon("c:/Users/asus/OneDrive/รูปภาพ/Icons_png/clearForm.png"), "Clear Form", self)
        clear_form_action.triggered.connect(self.clear_form)
        edit_menu.addActions([copy_action, clear_form_action])

        # Toolbar
        toolbar = QToolBar("Main Toolbar")
        toolbar.setMovable(False)
        toolbar.setIconSize(toolbar.iconSize() * 1.25)

        toolbar.addAction(gen_action)
        toolbar.addAction(save_action)
        toolbar.addAction(copy_action)
        toolbar.addAction(clear_form_action)

        self.addToolBar(toolbar)

        # Status Bar
        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self.status.showMessage("Fill in your details and click generate", 5000)
        
        # Apply styling
        self.setStyleSheet(self.get_stylesheet())

        # Initial card color
        self.fav_color = default_color

    def create_form_section(self):
        """Create the input form section"""
        form_widget = QWidget()
        form_layout = QFormLayout(form_widget)
        form_layout.setSpacing(12)
        form_layout.setLabelAlignment(Qt.AlignLeft)
        form_layout.setFormAlignment(Qt.AlignLeft | Qt.AlignTop)

        # Full name
        name_label = QLabel("Full name:")
        name_label.setFont(QFont("Arial", 10))
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("First name and Lastname")
        self.name_input.setFixedHeight(35)

        # Age
        age_label = QLabel("Age:")
        age_label.setFont(QFont("Arial", 10))
        self.age_input = QSpinBox()
        self.age_input.setRange(1, 120)
        self.age_input.setValue(25)
        self.age_input.setFixedHeight(35)
        self.age_input.setAlignment(Qt.AlignLeft)

        # Email
        email_label = QLabel("Email:")
        email_label.setFont(QFont("Arial", 10))
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("username@domain.name")
        self.email_input.setFixedHeight(35)

        # Position
        position_label = QLabel("Position:")
        position_label.setFont(QFont("Arial", 10))
        self.position_input = QComboBox()
        self.position_input.addItem("Choose your position")
        self.position_input.addItems(["Student", "Teacher", "Developer", "Other"])
        self.position_input.setFixedHeight(35)

        # Color picker row
        color_label = QLabel("Your favorite color:")
        color_label.setFont(QFont("Arial", 10))
        
        color_row = QWidget()
        color_layout = QHBoxLayout(color_row)
        color_layout.setContentsMargins(0, 0, 0, 0)
        color_layout.setSpacing(10)
        
        self.color_swatch = QLabel()
        self.color_swatch.setFixedSize(40, 35)
        self.color_swatch.setStyleSheet(f"""
            background-color: #B0E0E6; 
            border: 2px solid #999;
            border-radius: 4px;
        """)
        self.color_btn = QPushButton("Pick New Color")
        self.color_btn.setFixedHeight(35)
        self.color_btn.clicked.connect(self.pick_color)
        
        color_layout.addWidget(self.color_swatch)
        color_layout.addWidget(self.color_btn)
        color_layout.addStretch()

        # Add all rows to form
        form_layout.addRow(name_label, self.name_input)
        form_layout.addRow(age_label, self.age_input)
        form_layout.addRow(email_label, self.email_input)
        form_layout.addRow(position_label, self.position_input)
        form_layout.addRow(color_label, color_row)

        return form_widget

    # Actions
    def pick_color(self):
        """Pick a color for the card"""
        color = QColorDialog.getColor(self.fav_color, self, "Pick a Color")
        if color.isValid():
            self.fav_color = color
            self.color_swatch.setStyleSheet(f"""
                background-color: {self.fav_color.name()}; 
                border: 2px solid #888;
                border-radius: 5px;
            """)
            self.status.showMessage(f"Color changed to {self.fav_color.name()}", 2500)

    def generate_card(self):
        #text = f"{self.name_input.text()}\n({self.age_input.value()})\n{self.position_input.currentText()}\nEmail: {self.email_input.text()}"
        
        if not self.name_input.text().strip() or self.age_input.value() == 0:
            QMessageBox.warning(self, "Warning", "No information provided")
            return
        if self.position_input.currentText() == "Choose your position":
            QMessageBox.warning(self, "Warning", "Please select your position!")
            return
        # Clear previous card
        for i in reversed(range(self.display_layout.count())):
            widget = self.display_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        # Create card frame
        text_color = "#000000" if self.fav_color.lightness() > 128 else "#FFFFFF"
        card = QFrame()
        card.setObjectName("infoCard")
        card.setStyleSheet(f"""background-color:{self.fav_color.name()};
                           border-radius:10px;""")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(10,10,10,10)

        name_label = QLabel(self.name_input.text())
        name_label.setStyleSheet(f"""
            color:{text_color}; font-size:22px; font-weight:bold; text-align:left;""")
        card_layout.addWidget(name_label, alignment=Qt.AlignLeft)

        age_label = QLabel(f"({self.age_input.value()})")
        age_label.setStyleSheet(f"""
            color:{text_color}; font-size:13px; text-align:left;""")
        card_layout.addWidget(age_label, alignment=Qt.AlignLeft)

         # Add spacing
        card_layout.addSpacing(13)

        pos_label = QLabel(self.position_input.currentText())
        pos_label.setStyleSheet(f"""
            color:{text_color}; font-size:16px; font-weight:semi-bold; font-style:italic; text-align:left;""")
        card_layout.addWidget(pos_label, alignment=Qt.AlignLeft)

        email_label = QLabel(f"✉ {self.email_input.text()}")
        email_label.setStyleSheet(f"""
            color:{text_color}; font-size:13px; text-align:left;""")
        card_layout.addWidget(email_label, alignment=Qt.AlignLeft)

        #self.display.setText(text)
        self.display_layout.addWidget(card)
        self.status.showMessage("Card generated", 2000)

    def save_card(self):
        if self.display_layout.count() == 0:
            QMessageBox.warning(self, "Warning", "No card to save! Generate a card first.")
            return
        
        filename, _ = QFileDialog.getSaveFileName(self, "Save Card", "my_card.txt", "Text Files (*.txt);;All Files (*)")
        if filename:
            try:
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(self.display.toPlainText())
                self.status.showMessage(f"Card saved to {filename}", 2500)
                QMessageBox.information(self, "Success", "Card saved successfully!")

            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save card:\n{str(e)}")

    def copy_card(self):
        pyperclip.copy(self.display.toPlainText())
        self.status.showMessage("Card copied to clipboard", 2500)

    def clear_form(self):
        self.name_input.clear()
        self.age_input.setValue(0)
        self.email_input.clear()
        self.position_input.setCurrentIndex(0)
        self.status.showMessage("Form cleared", 2500)

    def clear_display(self):
        # ลบ widget ทั้งหมดใน layout
        for i in reversed(range(self.display_layout.count())):
            widget = self.display_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        # รีเซ็ต swatch
        self.color_swatch.setStyleSheet("background-color: #B0E0E6; border: 1px solid #888;")
        self.status.showMessage("Display cleared", 2500)

    def get_stylesheet(self):
        """Return application stylesheet"""
        return """
            QMainWindow {
                ###background-color: #F5F5F5;
            }
            QWidget {
                background-color: #F5F5F5;
            }
            QLabel {
                color: #2C3E50;
                background: transparent;
            }
            QLineEdit, QSpinBox, QComboBox {
                padding: 8px 10px;
                border: 1px solid #BDC3C7;
                border-radius: 4px;
                background-color: white;
                color: #2C3E50;
                font-size: 12px;
            }
            QLineEdit:focus, QSpinBox:focus, QComboBox:focus {
                border: 2px solid #3498DB;
            }
            QLineEdit::placeholder {
                color: #95A5A6;
            }
            QPushButton {
                background-color: white;
                color: #3498DB;
                border: 1px solid #BDC3C7;
                border-radius: 4px;
                padding: 8px 15px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #ECF0F1;
                border: 1px solid #3498DB;
            }
            QPushButton:pressed {
                background-color: #BDC3C7;
            }
            QComboBox::drop-down {
                border: none;
                padding-right: 10px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #7F8C8D;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                color: #2C3E50;
                selection-background-color: #3498DB;
                selection-color: white;
                border: 1px solid #BDC3C7;
            }
            QSpinBox::up-button, QSpinBox::down-button {
                background-color: #ECF0F1;
                border: none;
                width: 20px;
            }
            QSpinBox::up-button:hover, QSpinBox::down-button:hover {
                background-color: #BDC3C7;
            }
        """
def main():
    app = QApplication(sys.argv)
    win = InfoCardApp()
    win.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
