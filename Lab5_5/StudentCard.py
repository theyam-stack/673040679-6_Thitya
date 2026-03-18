from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout,
    QLabel, QPushButton, QFrame,
)
from PySide6.QtCore import Qt, Signal, QMimeData, QPoint
from PySide6.QtGui import QFont, QCursor, QDrag, QPixmap

from style import C


class StudentCard(QFrame):

    # Signal for delete request: emits self when pess del
    delete_requested = Signal(object)
     
    def __init__(self, data: dict, parent=None):
        super().__init__(parent)
        self.data = data
 
        # for drag and drop
        self._drag_start: QPoint | None = None
        self.setAcceptDrops(False)
        self.setCursor(QCursor(Qt.OpenHandCursor))
        self._build()

    def _build(self):
        # height depends on number of courses selected
        courses = self.data.get("courses", [])

        # base height: name + dept rows, plus 18px per course line
        self.setMinimumHeight(70 + len(courses) * 20)

        self.setStyleSheet(f"""
            QFrame {{
                background:{C['card']};
            }}
            QFrame:hover {{
                background:{C['surface']};
            }}
        """)

        # layout หลักของการ์ดแนวนอน
        row = QHBoxLayout(self)
        row.setContentsMargins(12, 10, 10, 10)
        row.setSpacing(10)

        # drag handle
        handle = QLabel("⠿")
        handle.setFixedWidth(16)
        handle.setAlignment(Qt.AlignTop)
        handle.setStyleSheet(
            f"background:transparent; color:{C['muted']};"
            f"font-size:18px;padding-top:2px;")
        
# ── ข้อมูลนักศึกษา ──
        info = QVBoxLayout()
        info.setSpacing(2)

        # บรรทัด 1: "FirstName LastName   StudentID"
        fname = self.data.get("fname", "")
        lname = self.data.get("lname", "")
        sid   = self.data.get("sid", "")
        name_row = QHBoxLayout()
        name_row.setSpacing(8)

        name_lbl = QLabel(f"{fname} {lname}")
        name_lbl.setFont(QFont("Segoe UI", 12, QFont.Bold))
        name_lbl.setStyleSheet(f"color:{C['text']}; background:transparent;")

        sid_lbl = QLabel(sid)
        sid_lbl.setStyleSheet(
            f"color:{C['muted']}; font-size:12px; background:transparent;"
        )

        name_row.addWidget(name_lbl)
        name_row.addWidget(sid_lbl)
        name_row.addStretch()

        # บรรทัด 2: "Faculty · Major"
        faculty = self.data.get("faculty", "")
        major   = self.data.get("major", "")
        dept_lbl = QLabel(f"{faculty}  ·  {major}")
        dept_lbl.setStyleSheet(
            f"color:{C['muted']}; font-size:12px; background:transparent;"
        )

        info.addLayout(name_row)
        info.addWidget(dept_lbl)

        # บรรทัด 3+: รายวิชา
        for course in courses:
            c_lbl = QLabel(course)
            c_lbl.setStyleSheet(
                f"color:{C['muted']}; font-size:12px; background:transparent;"
            )
            info.addWidget(c_lbl)

        # delete button
        btn_del = QPushButton("✕")
        btn_del.setFixedSize(28, 28)
        btn_del.setCursor(QCursor(Qt.PointingHandCursor))
        btn_del.setStyleSheet(f"""
            QPushButton {{
                background:transparent; color:{C['muted']};
                border:none; border-radius:14px;
                font-size:11px; font-weight:bold;
            }}
            QPushButton:hover {{
                background:{C['red']}; color:white; border:none;
            }}
        """)
        btn_del.clicked.connect(lambda: self.delete_requested.emit(self))
        
        # ── รวม layout ──
        row.addWidget(handle, alignment=Qt.AlignTop)
        row.addLayout(info, stretch=1)
        row.addWidget(btn_del, alignment=Qt.AlignTop)

    # ── Drag support ──────────────────────────────────────────
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_start = event.pos()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if (event.buttons() & Qt.LeftButton) and self._drag_start is not None:
            if (event.pos() - self._drag_start).manhattanLength() > 10:
                drag = QDrag(self)
                mime = QMimeData()
                mime.setText("student_card")
                drag.setMimeData(mime)

                pix = QPixmap(self.size())
                pix.fill(Qt.transparent)
                self.render(pix)
                drag.setPixmap(pix)
                drag.setHotSpot(event.pos())
                drag.exec(Qt.MoveAction)
        super().mouseMoveEvent(event)
