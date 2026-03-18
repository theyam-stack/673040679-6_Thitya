"""
Student Registration System — PySide6
======================================
3 pages via QStackedWidget + Signal/Slot.

Page 1 : Card list (drag-drop reorder, delete)
Page 2 : Add student form
Page 3 : Review & confirm
"""

import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QStackedWidget,
    QVBoxLayout, QHBoxLayout, QGridLayout, QScrollArea,
    QLabel, QLineEdit, QPushButton, QComboBox, QFrame,
    QMessageBox,
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QCursor

from data import COURSES
from style import C, BASE, INPUT_SS, COMBO_SS, SCROLL_SS
from style import btn_ss, section_label, field_label, divider
from StudentCard import StudentCard


# ─────────────────────────────────────────────────────────────
#  Page 1 — Student List
# ─────────────────────────────────────────────────────────────
class StudentListPage(QWidget):
    go_to_add = Signal()  # Signal to switch to AddStudentPage

    def __init__(self):
        super().__init__()
        self._cards: list[StudentCard] = []  # เก็บการ์ดทั้งหมด
        self.setAcceptDrops(True)
        self._build()   # เรียก _build()

    def _build(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── top bar ──
        bar = QFrame()
        bar.setFixedHeight(64)
        bar.setStyleSheet(
            f"background:{C['bg']}; border-bottom:1px solid {C['border']};"
        )
        bl = QHBoxLayout(bar)
        bl.setContentsMargins(32, 0, 32, 0)

        title = QLabel("Students")
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title.setStyleSheet(f"color:{C['text']};")

        self.lbl_count = QLabel("0 enrolled")
        self.lbl_count.setStyleSheet(
            f"color:{C['muted']};font-size:13px;"
        )

        btn_add = QPushButton("+ Add Student")
        btn_add.setCursor(QCursor(Qt.PointingHandCursor))
        btn_add.setStyleSheet(btn_ss(C['accent'], "#1d4ed8"))
        btn_add.clicked.connect(self.go_to_add.emit)

        bl.addWidget(title)
        bl.addSpacing(12)
        bl.addWidget(self.lbl_count, alignment=Qt.AlignVCenter)
        bl.addStretch()
        bl.addWidget(btn_add)

        # ── scroll area ──
        self._scroll = QScrollArea()
        self._scroll.setWidgetResizable(True)
        self._scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self._scroll.setStyleSheet(SCROLL_SS)

        self._container = QWidget()
        self._container.setStyleSheet(f"background:{C['bg']};")
        self._card_lay = QVBoxLayout(self._container)
        self._card_lay.setContentsMargins(24, 16, 24, 16)
        self._card_lay.setSpacing(8)
        self._card_lay.addStretch()

        self._scroll.setWidget(self._container)

        # empty state label
        self._lbl_empty = QLabel("No students yet.\nClick  + Add Student to get started.")
        self._lbl_empty.setAlignment(Qt.AlignCenter)
        self._lbl_empty.setStyleSheet(f"color:{C['muted']};font-size:14px;")

        root.addWidget(bar)
        root.addWidget(self._lbl_empty, stretch=1)
        root.addWidget(self._scroll, stretch=1)

        self._refresh_empty() # ซ่อน scroll, แสดง empty label ตอนเริ่ม

    # ── public ───────────────────────────────────────────────
    def add_student(self, data: dict):

        # create card and connect the delete signal
        card = StudentCard(data)
        card.delete_requested.connect(self._remove_card)

        # Add card to the list
        self._cards.append(card)

        # insert ก่อน stretch (index = len-1 เพราะ stretch อยู่ท้าย)
        self._card_lay.insertWidget(self._card_lay.count() - 1, card)

        self._refresh_count()
        self._refresh_empty()

    # ── private ──────────────────────────────────────────────
    def _remove_card(self, card: StudentCard):
        # inline confirmation — no popup, just ask once
        reply = QMessageBox.question(
            self, "Remove student",
            f"Remove {card.data['fullname']}?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            # remove card from the list
            self._cards.remove(card)       # ลบออกจาก list
            self._card_lay.removeWidget(card)
            card.deleteLater()             # คืน memory ให้ Qt
            # remove card from layout
            self._refresh_count()
            self._refresh_empty()

    def _refresh_count(self):
        # get number of card
        n = len(self._cards)
        # update number of student label
        self.lbl_count.setText(f"{n} enrolled")

    def _refresh_empty(self):
        has = bool(self._cards)
        self._lbl_empty.setVisible(not has)
        self._scroll.setVisible(has)

    # ── drag-drop reorder ────────────────────────────────────
    def dragEnterEvent(self, event):
        if event.mimeData().hasText() and event.mimeData().text() == "student_card":
            event.acceptProposedAction()

    def dragMoveEvent(self, event):
        event.acceptProposedAction()

    def dropEvent(self, event):
        src = event.source()
        if not isinstance(src, StudentCard) or src not in self._cards:
            return

        local_y = self._container.mapFrom(self, event.position().toPoint()).y()
        target = len(self._cards) - 1
        for i, card in enumerate(self._cards):
            if local_y < card.y() + card.height() // 2:
                target = i
                break

        src_idx = self._cards.index(src)
        if src_idx == target:
            return

        self._cards.pop(src_idx)
        self._cards.insert(target, src)
        for card in self._cards:
            self._card_lay.removeWidget(card)
        for i, card in enumerate(self._cards):
            self._card_lay.insertWidget(i, card)

        event.acceptProposedAction()


# ─────────────────────────────────────────────────────────────
#  Page 2 — Add Student Form
# ─────────────────────────────────────────────────────────────
class AddStudentPage(QWidget):

    # Add signals for going back and going forward
    go_back    = Signal()         # ปุ่ม Cancel -> กลับ List
    go_review  = Signal(dict)     # ปุ่ม Review -> ส่งข้อมูลไป ReviewPage

    def __init__(self):
        super().__init__()
        self._build()

    def _inp(self, ph: str = "") -> QLineEdit:
        e = QLineEdit()
        e.setPlaceholderText(ph)
        e.setMinimumHeight(38)
        e.setStyleSheet(INPUT_SS)
        return e

    def _build(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)

        # top bar
        bar = QFrame()
        bar.setFixedHeight(64)
        bar.setStyleSheet(
            f"background:{C['bg']}; border-bottom:1px solid {C['border']};"
        )
        bl = QHBoxLayout(bar)
        bl.setContentsMargins(32, 0, 32, 0)
        t = QLabel("Add Student")
        t.setFont(QFont("Segoe UI", 16, QFont.Bold))
        t.setStyleSheet(f"color:{C['text']};")
        bl.addWidget(t)
        bl.addStretch()

        # scrollable form
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet(SCROLL_SS)

        body = QWidget()
        body.setStyleSheet(f"background:{C['bg']};")
        form = QVBoxLayout(body)
        form.setContentsMargins(40, 28, 40, 28)
        form.setSpacing(20)

        # ── personal info ─────────────────────────────────────
        form.addWidget(section_label("Personal Information"))
        # grid 2 คอลัมน์สำหรับฟอร์ม
        grid = QGridLayout()
        grid.setSpacing(10)

        self.inp_sid    = self._inp("e.g. 65010001")
        self.inp_fname  = self._inp("First name")
        self.inp_lname  = self._inp("Last name")
        self.inp_faculty = self._inp("e.g. Science & Technology")
        self.inp_major  = self._inp("e.g. Computer Science")

        self.cmb_year = QComboBox()
        self.cmb_year.addItems(["Year 1","Year 2","Year 3","Year 4"])
        self.cmb_year.setStyleSheet(COMBO_SS)
        self.cmb_year.setMinimumHeight(38)

        grid.addWidget(field_label("Student ID *"),  0, 0)
        grid.addWidget(self.inp_sid,                 0, 1, 1, 2)  # span 2 คอลัมน์
        grid.addWidget(field_label("First Name *"),  1, 0)
        grid.addWidget(self.inp_fname,               1, 1)
        grid.addWidget(field_label("Last Name *"),   1, 2)        # คอลัมน์ที่ 3
        grid.addWidget(self.inp_lname,               1, 3)
        grid.addWidget(field_label("Faculty *"),     2, 0)
        grid.addWidget(self.inp_faculty,             2, 1)
        grid.addWidget(field_label("Major *"),       2, 2)
        grid.addWidget(self.inp_major,               2, 3)

        form.addLayout(grid)
        form.addWidget(divider())

        # ── course selection ──────────────────────────────────
        form.addWidget(section_label("Course Selection  (choose 1–3)"))

        self._combos: list[QComboBox] = []
        for i in range(3):
            c_row = QHBoxLayout()
            c_row.setSpacing(10)
            lbl = field_label(f"Course {i+1}")
            cmb = QComboBox()
            cmb.addItems(COURSES)
            cmb.setStyleSheet(COMBO_SS)
            cmb.setMinimumHeight(38)
            self._combos.append(cmb)
            c_row.addWidget(lbl)
            c_row.addWidget(cmb, stretch=1)
            form.addLayout(c_row)

        # ── error label ───────────────────────────────────────
        self.lbl_err = QLabel("")
        self.lbl_err.setStyleSheet(f"color:{C['red']};font-size:13px;")
        form.addWidget(self.lbl_err)

        form.addStretch()

        # ── buttons ───────────────────────────────────────────
        btn_row = QHBoxLayout()
        bc = QPushButton("← Cancel")
        bc.setCursor(QCursor(Qt.PointingHandCursor))
        bc.setStyleSheet(
            btn_ss(C['bg'], C['surface'], C['muted'],
                   border=f"1px solid {C['border']}")
        )

        br = QPushButton("Review →")
        br.setCursor(QCursor(Qt.PointingHandCursor))
        br.setStyleSheet(btn_ss(C['accent'], "#1d4ed8"))

        bc.clicked.connect(self._on_cancel)
        br.clicked.connect(self._on_review)

        btn_row.addWidget(bc)
        btn_row.addStretch()
        btn_row.addWidget(br)
        form.addLayout(btn_row)

        scroll.setWidget(body)
        root.addWidget(bar)
        root.addWidget(scroll, stretch=1)

    def _on_cancel(self):
        self.go_back.emit()

    def _on_review(self):
        sid     = self.inp_sid.text().strip()
        fname   = self.inp_fname.text().strip()
        lname   = self.inp_lname.text().strip()
        faculty = self.inp_faculty.text().strip()
        major   = self.inp_major.text().strip()
        year    = self.cmb_year.currentText()

         # เก็บเฉพาะวิชาที่เลือกจริง (ไม่ใช่ placeholder บรรทัดแรก)
        courses = [
            c.currentText() for c in self._combos
            if c.currentIndex() != 0        # index 0 = "— Select Course —"
        ]
        # check for field errors / incomplete
        # Warn the user if needed
        # ── เก็บ errors ทั้งหมดก่อน ──
        missing = []
        if not sid:     missing.append("Student ID")
        if not fname:   missing.append("First Name")
        if not lname:   missing.append("Last Name")
        if not faculty: missing.append("Faculty")
        if not major:   missing.append("Major")
        if not courses: missing.append("at least 1 course")

        if missing:
            self.lbl_err.setText("Required: " + ",  ".join(missing))
            return
        
        self.lbl_err.setText("")   # ล้าง error

        # emit signals with data
        data = {
            "fname":    fname,
            "lname":    lname,
            "fullname": f"{fname} {lname}",   # ใช้ใน StudentCard
            "sid":      sid,
            "faculty":  faculty,
            "major":    major,
            "year":     year,
            "courses":  courses,
        }
        self.go_review.emit(data)  # ส่งข้อมูลไป ReviewPage

    # For when coming back from the review page
    def load_data(self, d: dict):
        """Pre-fill form when user clicks Edit on Page 3."""
        self.inp_sid.setText(d.get("sid", ""))
        self.inp_fname.setText(d.get("fname", ""))
        self.inp_lname.setText(d.get("lname", ""))
        self.inp_faculty.setText(d.get("faculty", ""))
        self.inp_major.setText(d.get("major", ""))

        years = ["Year 1","Year 2","Year 3","Year 4"]
        if d.get("year") in years:
            self.cmb_year.setCurrentIndex(years.index(d["year"]))

        courses = d.get("courses", [])
        for i, cmb in enumerate(self._combos):
            if i < len(courses):
                idx = cmb.findText(courses[i])
                cmb.setCurrentIndex(idx if idx >= 0 else 0)
            else:
                cmb.setCurrentIndex(0)

    # For when going back to the home page
    def clear_form(self):
        self.inp_sid.clear()
        self.inp_fname.clear()
        self.inp_lname.clear()
        self.inp_faculty.clear()
        self.inp_major.clear()
        self.cmb_year.setCurrentIndex(0)
        for cmb in self._combos:
            cmb.setCurrentIndex(0)
        self.lbl_err.setText("")

# ─────────────────────────────────────────────────────────────
#  Page 3 — Review & Confirm
# ─────────────────────────────────────────────────────────────
class ReviewPage(QWidget):
    # Emit signals for confirming and going back to edit
    confirmed = Signal(dict)   # ยืนยัน - ส่งข้อมูลกลับไป MainWindow
    go_edit   = Signal(dict)   # Edit - ส่งข้อมูลกลับไป AddStudentPage

    def __init__(self):
        super().__init__()
        self._data: dict = {}
        self._build()

    def _row(self, layout: QVBoxLayout, label: str) -> QLabel:
        row = QHBoxLayout()
        row.setSpacing(0)
        lbl = QLabel(label)
        lbl.setFixedWidth(130)
        lbl.setStyleSheet(f"color:{C['muted']};font-size:13px;")
        val = QLabel("—")
        val.setStyleSheet(f"color:{C['text']};font-size:13px;")
        val.setWordWrap(True)
        row.addWidget(lbl)
        row.addWidget(val, stretch=1)
        layout.addLayout(row)
        return val

    def _build(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)

        # top bar
        bar = QFrame()
        bar.setFixedHeight(64)
        bar.setStyleSheet(
            f"background:{C['bg']}; border-bottom:1px solid {C['border']};"
        )
        bl = QHBoxLayout(bar)
        bl.setContentsMargins(32, 0, 32, 0)
        t = QLabel("Review & Confirm")
        t.setFont(QFont("Segoe UI", 16, QFont.Bold))
        t.setStyleSheet(f"color:{C['text']};")
        bl.addWidget(t)
        bl.addStretch()

        body = QWidget()
        body.setStyleSheet(f"background:{C['bg']};")
        form = QVBoxLayout(body)
        form.setContentsMargins(40, 28, 40, 28)
        form.setSpacing(20)

        # ── summary section ───────────────────────────────────
        form.addWidget(section_label("Student Information"))

        card = QFrame()
        card.setStyleSheet(
            f"background:{C['surface']};border-radius:8px;"
        )
        card_lay = QVBoxLayout(card)
        card_lay.setContentsMargins(16, 14, 16, 14)
        card_lay.setSpacing(8)

        # สร้าง value labels ด้วย self._row() แล้วเก็บไว้ใช้ตอน load_data
        self._val_name    = self._row(card_lay, "Full Name")
        self._val_sid     = self._row(card_lay, "Student ID")
        self._val_faculty = self._row(card_lay, "Faculty")  
        self._val_major   = self._row(card_lay, "Major") 
        self._val_year    = self._row(card_lay, "Year")

        form.addWidget(card)
        form.addWidget(divider())
        form.addWidget(section_label("Courses"))

        # layout สำหรับแสดงรายวิชา (เติมตอน load_data)
        self._courses_lay = QVBoxLayout()
        self._courses_lay.setSpacing(4)
        form.addLayout(self._courses_lay)
        form.addWidget(divider())
        form.addStretch()
        
        # ── buttons ───────────────────────────────────────────
        btn_row = QHBoxLayout()
        be = QPushButton("← Edit")
        be.setCursor(QCursor(Qt.PointingHandCursor))
        be.setStyleSheet(
            btn_ss(C['bg'], C['surface'], C['muted'],
                   border=f"1px solid {C['border']}")
        )

        bc = QPushButton("Confirm Registration")
        bc.setCursor(QCursor(Qt.PointingHandCursor))
        bc.setStyleSheet(btn_ss(C['green'], "#15803d"))

        be.clicked.connect(lambda: self.go_edit.emit(self._data))
        bc.clicked.connect(lambda: self.confirmed.emit(self._data))

        btn_row.addWidget(be)
        btn_row.addStretch()
        btn_row.addWidget(bc)
        form.addLayout(btn_row)

        scroll = QScrollArea() # gพิ่ม scroll ให้ body และ add เข้า root
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet(SCROLL_SS)

        scroll.setWidget(body)
        root.addWidget(bar)
        root.addWidget(scroll, stretch=1)


    def load_data(self, d: dict):
        # fill data into the review page
        self._data = d   # เก็บไว้ใช้ตอนกด Edit / Confirm

        self._val_name.setText(d.get("fullname", "—"))
        self._val_sid.setText(d.get("sid", "—"))
        self._val_faculty.setText(d.get("faculty", "—")) 
        self._val_major.setText(d.get("major", "—"))  
        self._val_year.setText(d.get("year", "—"))

        # ล้างรายวิชาเก่าก่อน แล้ว rebuild ใหม่
        while self._courses_lay.count():
            item = self._courses_lay.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        for course in d.get("courses", []):
            lbl = QLabel(f"• {course}")
            lbl.setStyleSheet(f"color:{C['text']};font-size:13px;")
            self._courses_lay.addWidget(lbl)

# ─────────────────────────────────────────────────────────────
#  Main Window
# ─────────────────────────────────────────────────────────────
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Registration")
        self.setMinimumSize(860, 580)
        self.resize(980, 660)
        self.setStyleSheet(BASE)
        self._build()           # Called!

    def _build(self):
        central = QWidget()
        outer = QVBoxLayout(central)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)
        self.setCentralWidget(central)

        # สร้าง pages 
        self.page_list   = StudentListPage()
        self.page_add    = AddStudentPage()
        self.page_review = ReviewPage()

        # สร้าง stack และใส่ pages 
        self.stack = QStackedWidget()
        self.stack.addWidget(self.page_list)    # index 0
        self.stack.addWidget(self.page_add)     # index 1
        self.stack.addWidget(self.page_review)  # index 2
        self.stack.setCurrentIndex(0)

        outer.addWidget(self.stack)

        # เชื่อม signals
        self.page_list.go_to_add.connect(self._go_add)
        self.page_add.go_back.connect(self._go_list)
        self.page_add.go_review.connect(self._go_review)
        self.page_review.go_edit.connect(self._go_edit)
        self.page_review.confirmed.connect(self._on_confirmed)

    # Helper Method
    def _go_add(self):
        """List → Add form"""
        self.page_add.clear_form()
        self.stack.setCurrentIndex(1)

    def _go_list(self):
        """Add → กลับ List"""
        self.stack.setCurrentIndex(0)

    def _go_review(self, data: dict):
        """Add → Review (พร้อมข้อมูล)"""
        self.page_review.load_data(data)
        self.stack.setCurrentIndex(2)

    def _go_edit(self, data: dict):
        """Review → กลับ Edit (โหลดข้อมูลเดิมกลับ)"""
        self.page_add.load_data(data)
        self.stack.setCurrentIndex(1)

    def _on_confirmed(self, data: dict):
        """Review → ยืนยัน → เพิ่มการ์ดในหน้า List"""
        self.page_list.add_student(data)
        self.page_add.clear_form()
        self.stack.setCurrentIndex(0)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    w = MainWindow()
    w.show()
    sys.exit(app.exec())
