#P2 Lab 5-4
import sys, random
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QComboBox, QSlider, QPushButton,
    QMenuBar, QToolBar, QFileDialog, QStatusBar, QFrame)
from PySide6.QtGui import QAction, QIcon, QFont
from PySide6.QtCore import Qt, QSize

class CharacterBuilder(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RPG Character Builder")
        self.resize(900, 700)

        # Central Layout
        central = QWidget()
        main_layout = QHBoxLayout(central)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Left Panel
        left_panel = QVBoxLayout()
        left_panel.setSpacing(12)

        # Character Name
        left_panel.addWidget(QLabel("Character Name:"))
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Enter character name...")
        self.name_edit.setFixedHeight(35)
        left_panel.addWidget(self.name_edit)

        # Race
        left_panel.addWidget(QLabel("Race:"))
        self.race_combo = QComboBox()
        self.race_combo.addItem("Choose race")
        self.race_combo.addItems(["Human", "Elf", "Dwarf", "Orc", "Undead"])
        self.race_combo.setFixedHeight(35)
        left_panel.addWidget(self.race_combo)

        # Class
        left_panel.addWidget(QLabel("Class:"))
        self.class_combo = QComboBox()
        self.class_combo.addItem("Choose class")
        self.class_combo.addItems(["Warrior", "Mage", "Rogue", "Paladin", "Ranger"])
        self.class_combo.setFixedHeight(35)
        left_panel.addWidget(self.class_combo)

        # Gender
        left_panel.addWidget(QLabel("Gender:"))
        self.gender_combo = QComboBox()
        self.gender_combo.addItem("Choose gender")
        self.gender_combo.addItems(["Male", "Female", "Other"])
        self.gender_combo.setFixedHeight(35)
        left_panel.addWidget(self.gender_combo)

        # Divider
        divider = QFrame()
        divider.setFrameShape(QFrame.HLine)
        divider.setStyleSheet("background-color: #CCCCCC; margin: 10px 0;")
        left_panel.addWidget(divider)

        # Stat Allocation
        stat_title = QLabel("Stat Allocation")
        stat_title.setFont(QFont("Arial", 12, QFont.Bold))
        left_panel.addWidget(stat_title)

        self.stats = {}
        self.stat_labels = {}
        stat_icons = {
            "STR": "⚔️",
            "DEX": "🏃",
            "INT": "🧠",
            "VIT": "❤️"
        } 
        for stat, icon in stat_icons.items():
            # Stat row
            stat_row = QHBoxLayout()
            
            # Icon and label
            stat_label = QLabel(f"{icon} {stat}")
            stat_label.setFixedWidth(60)
            stat_row.addWidget(stat_label)
            
            # Slider
            slider = QSlider(Qt.Horizontal)
            slider.setRange(1, 20)
            slider.setValue(5)
            slider.setTickPosition(QSlider.TicksBelow)
            slider.setTickInterval(5)
            slider.valueChanged.connect(self.update_total)
            self.stats[stat] = slider
            stat_row.addWidget(slider)
            
            # Value label
            value_label = QLabel("5")
            value_label.setFixedWidth(30)
            value_label.setAlignment(Qt.AlignCenter)
            self.stat_labels[stat] = value_label
            slider.valueChanged.connect(lambda val, lbl=value_label: lbl.setText(str(val)))
            stat_row.addWidget(value_label)
            
            left_panel.addLayout(stat_row)

        # Points counter
        self.total_label = QLabel("Points used: 20 / 40")
        self.total_label.setFont(QFont("Arial", 10, QFont.Bold))
        self.total_label.setAlignment(Qt.AlignLeft)
        left_panel.addWidget(self.total_label)

        # Generate Button
        gen_btn = QPushButton("⚔️ Generate Character Sheet")
        gen_btn.setFont(QFont("Arial", 11, QFont.Bold))
        gen_btn.setFixedHeight(45)
        gen_btn.clicked.connect(self.generate_sheet)
        left_panel.addWidget(gen_btn)

        left_panel.addStretch()

        # Right Panel (Dark Character Sheet)
        self.sheet_widget = QFrame()
        self.sheet_widget.setObjectName("characterSheet")
        self.sheet_widget.setFixedWidth(350)
        self.sheet_panel = QVBoxLayout(self.sheet_widget)
        self.sheet_panel.setSpacing(15)
        self.sheet_panel.setContentsMargins(30, 30, 30, 30)

        main_layout.addLayout(left_panel, 1)
        main_layout.addWidget(self.sheet_widget)
        self.setCentralWidget(central)

        # Menu Bar 
        menu = self.menuBar()
        game_menu = menu.addMenu("Game")
        edit_menu = menu.addMenu("Edit")

        new_act = QAction("New Character", self)
        new_act.setShortcut("Ctrl+N")
        new_act.triggered.connect(self.reset_all)
        
        gen_act = QAction("Generate Sheet", self)
        gen_act.setShortcut("Ctrl+G")
        gen_act.triggered.connect(self.generate_sheet)
        
        save_act = QAction("Save Sheet", self)
        save_act.setShortcut("Ctrl+S")
        save_act.triggered.connect(self.save_sheet)
        
        exit_act = QAction("Exit", self)
        exit_act.setShortcut("Ctrl+Q")
        exit_act.triggered.connect(self.close)

        game_menu.addActions([new_act, gen_act, save_act, exit_act])

        reset_stats_act = QAction("Reset Stats", self)
        reset_stats_act.triggered.connect(self.reset_stats)
        
        randomize_act = QAction("Randomize", self)
        randomize_act.setShortcut("Ctrl+R")
        randomize_act.triggered.connect(self.randomize)
        
        edit_menu.addActions([reset_stats_act, randomize_act])

        # Toolbar
        toolbar = QToolBar("Main Toolbar")
        toolbar.setIconSize(QSize(32, 32))
        toolbar.setMovable(False)
        self.addToolBar(toolbar)
        toolbar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        new_icon = QIcon("C:/Users/asus/OneDrive/รูปภาพ/Icons_png/new_book.png")
        gen_icon = QIcon("C:/Users/asus/OneDrive/รูปภาพ/Icons_png/sword.png")
        rand_icon = QIcon("C:/Users/asus/OneDrive/รูปภาพ/Icons_png/dice1.png")
        save_icon = QIcon("C:/Users/asus/OneDrive/รูปภาพ/Icons_png/save3d.png")
        
        new_tool = QAction(new_icon, "New", self, triggered=self.reset_all)
        gen_tool = QAction(gen_icon, "Generate", self, triggered=self.generate_sheet)
        rand_tool = QAction(rand_icon, "Randomize", self, triggered=self.randomize)
        save_tool = QAction(save_icon, "Save", self, triggered=self.save_sheet)
        
        toolbar.addAction(new_tool)
        toolbar.addAction(gen_tool)
        toolbar.addAction(rand_tool)
        toolbar.addAction(save_tool)

        # Status Bar
        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self.status.showMessage("Ready — create your character", 0)

        self.apply_styling() # Apply styling
        self.update_total()
        self.generate_sheet()

    def apply_styling(self):
        """Apply styling matching the screenshot"""
        self.setStyleSheet("""
            QLabel {
                color: #fff;
            }
            QLineEdit, QComboBox {
                background-color: white;
                border: 2px solid #DDDDDD;
                border-radius: 5px;
                padding: 8px;
                color: #333;
            }
            QLineEdit:focus, QComboBox:focus {
                border: 2px solid #8B7DD8;
            }
            QComboBox::drop-down {
                border: none;
            }
            QSlider::groove:horizontal {
                border: 1px solid #CCCCCC;
                height: 6px;
                background: #E0E0E0;
                margin: 2px 0;
                border-radius: 3px;
            }
            QSlider::handle:horizontal {
                background: #5B7FD8;
                border: 1px solid #4A6BC0;
                width: 16px;
                height: 16px;
                margin: -6px 0;
                border-radius: 8px;
            }
            QSlider::handle:horizontal:hover {
                background: #6B8FE8;
            }
            QPushButton {
                background-color: #8B7DD8;
                color: white;
                border: 2px solid #7B6DC8;
                border-radius: 8px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #9B8DE8;
            }
            QPushButton:pressed {
                background-color: #7B6DC8;
            }
            QFrame#characterSheet {
                background-color: #2D2D3D;
                border-radius: 15px;
                border: 2px solid #3D3D4D;
            }
            QStatusBar {
                background-color: #333;
                color: #FFE400;
            }
        """)
    def update_total(self):
        total = sum(slider.value() for slider in self.stats.values())
        self.total_label.setText(f"Points used: {total} / 40")
        
        if total > 40:
            self.total_label.setStyleSheet("color: red; font-weight: bold;")
            self.status.showMessage("Warning: Total exceeds 40 points!", 3000)
        else:
            self.total_label.setStyleSheet("color: #FFE400; font-weight: bold;")

    def generate_sheet(self):
        # Clear old panel
        while self.sheet_panel.count() > 0:
            widget = self.sheet_panel.itemAt(0).widget()
            if widget:
                widget.deleteLater()

        # Character Name Title
        name_text = self.name_edit.text() or "Character Name"
        name_label = QLabel(f"— {name_text} —")
        name_label.setFont(QFont("Arial", 18, QFont.Bold))
        name_label.setAlignment(Qt.AlignCenter)
        name_label.setStyleSheet("color: #FFE400; border: none;")
        self.sheet_panel.addWidget(name_label)

        # Race • Class
        race_text = self.race_combo.currentText()
        class_text = self.class_combo.currentText()
        if race_text == "Choose race":
            race_text = "Race"
        if class_text == "Choose class":
            class_text = "Class"
        
        subtext = QLabel(f"{race_text} • {class_text}")
        subtext.setFont(QFont("Arial", 11))
        subtext.setAlignment(Qt.AlignCenter)
        subtext.setStyleSheet("color: #888899; border: none;")
        self.sheet_panel.addWidget(subtext)
        self.sheet_panel.addSpacing(20)

        # Stats with dot patterns
        for stat, slider in self.stats.items():
            stat_row = QHBoxLayout()
            
            # Stat label
            stat_label = QLabel(stat)
            stat_label.setFont(QFont("Arial", 11, QFont.Bold))
            stat_label.setStyleSheet("color: #CCCCDD; border: none;")
            stat_label.setFixedWidth(50)
            stat_row.addWidget(stat_label)
            
            # Dot pattern visualization
            value = slider.value()
            dots = "▪" * value + "▫" * (20 - value)
            dots_label = QLabel(dots)
            dots_label.setFont(QFont("Courier", 9))
            dots_label.setStyleSheet("color: #666677; border: none; letter-spacing: 2px;")
            stat_row.addWidget(dots_label, 1)
            
            # Value
            value_label = QLabel("—")
            value_label.setFont(QFont("Arial", 11))
            value_label.setStyleSheet("color: #888899; border: none;")
            value_label.setFixedWidth(30)
            value_label.setAlignment(Qt.AlignRight)
            stat_row.addWidget(value_label)
            
            stat_container = QWidget()
            stat_container.setLayout(stat_row)
            stat_container.setStyleSheet("background: transparent; border: none;")
            self.sheet_panel.addWidget(stat_container)

        self.sheet_panel.addStretch()
        self.status.showMessage("Character sheet generated", 0)

    def reset_all(self):
        self.name_edit.clear()
        self.race_combo.setCurrentIndex(0)
        self.class_combo.setCurrentIndex(0)
        self.gender_combo.setCurrentIndex(0)
        self.reset_stats()
        self.generate_sheet()
        self.status.showMessage("New character created", 5000)

    def reset_stats(self):
        for slider in self.stats.values():
            slider.setValue(5)
        self.update_total()
        self.status.showMessage("Stats reset to 5", 4000)

    def randomize(self):
        # Randomize basic info
        self.race_combo.setCurrentIndex(random.randint(1, 5))
        self.class_combo.setCurrentIndex(random.randint(1, 5))
        self.gender_combo.setCurrentIndex(random.randint(1, 3))
        
        # Randomize stats
        while True:
            values = [random.randint(1, 20) for _ in range(4)]
            if sum(values) <= 40:
                break
        for (stat, slider), val in zip(self.stats.items(), values):
            slider.setValue(val)
        
        self.update_total()
        self.generate_sheet()
        self.status.showMessage("Character randomized", 4000)

    def save_sheet(self):
        filename, _ = QFileDialog.getSaveFileName(
            self, "Save Character Sheet", "character.txt", "Text Files (*.txt);;All Files (*)")
        if filename:
            with open(filename, "w", encoding="utf-8") as f:
                f.write("RPG CHARACTER SHEET\n")
                f.write("=" * 40 + "\n\n")
                f.write(f"Name: {self.name_edit.text() or 'Character Name'}\n")
                f.write(f"Race: {self.race_combo.currentText()}\n")
                f.write(f"Class: {self.class_combo.currentText()}\n")
                f.write(f"Gender: {self.gender_combo.currentText()}\n\n")
                f.write("STATS:\n")
                f.write("-" * 40 + "\n")
                for stat, slider in self.stats.items():
                    f.write(f"{stat}: {slider.value()} / 20\n")
                f.write("\n")
                total = sum(slider.value() for slider in self.stats.values())
                f.write(f"Total Points: {total} / 40\n")
            self.status.showMessage(f"Saved to {filename}", 4000)
def main():
    app = QApplication(sys.argv)
    window = CharacterBuilder()
    window.show()
    sys.exit(app.exec())
if __name__ == "__main__":
    main()
