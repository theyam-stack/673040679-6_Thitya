#P1 CozyStay Hotel Booking
import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QStackedWidget,
    QVBoxLayout, QHBoxLayout, QGridLayout, QFormLayout,
    QLabel, QLineEdit, QDateEdit, QSpinBox,
    QPushButton, QDialog, QMessageBox, QScrollArea,
    QFrame, QSizePolicy
)
from PySide6.QtCore import Qt, Signal, QDate
from PySide6.QtGui import QFont

class RoomCard(QWidget):
    """
    Room information card — Custom Widget Class
    Practice:
      - Inheriting QWidget
      - Signal to pass data to parent
      - select() / deselect() methods to change visual state
    """

    # Signal: emits (room_name, price) when user clicks Select
    room_selected = Signal(str, int)

    def __init__(self, room_name: str, price: int, description: str, emoji: str = "🏨"):
        super().__init__()
        self._is_selected = False
        self.room_name = room_name
        self._price = price

        self._build_ui(emoji, description)
        self.deselect()  # Set default style

    def _build_ui(self, emoji: str, description: str):
        self.setFixedSize(200, 200)
        self.setCursor(Qt.PointingHandCursor)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(6)

        # 1. Create labels and button in the card
        self.emoji_label = QLabel(emoji)
        self.emoji_label.setFont(QFont("Arial", 26))
        self.emoji_label.setAlignment(Qt.AlignCenter)

        self.name_label = QLabel(self.room_name)  # ชื่อห้อง
        self.name_label.setFont(QFont("Arial", 15, QFont.Bold))
        self.name_label.setAlignment(Qt.AlignCenter)

        self.price_label = QLabel(f"Price: ${self._price}/ night")  # ราคาห้อง
        self.price_label.setFont(QFont("Arial", 13))
        self.price_label.setAlignment(Qt.AlignCenter)

        self.description_label = QLabel(description) # คำอธิบาย
        self.description_label.setFont(QFont("Arial", 10))
        self.description_label.setAlignment(Qt.AlignCenter)
        self.description_label.setWordWrap(True)

        self.select_btn = QPushButton("Select Room") # ปุ่ม

        # 2. Add Every 1. labels and button to the layout
        layout.addWidget(self.emoji_label)
        layout.addWidget(self.name_label)
        layout.addWidget(self.price_label)
        layout.addWidget(self.description_label)
        layout.addWidget(self.select_btn)

        # 3. Connect button signal to a slot
        self.select_btn.clicked.connect(self._on_select_clicked)


    def _on_select_clicked(self):
        """When button is clicked, emit signal to notify parent"""
        self._is_selected = True
        self.select()  # Change appearance to selected state # เปลี่ยนหน้าตาเป็นสีเขียว
        self.room_selected.emit(self.room_name, self._price)  # ส่งชื่อห้องและราคากลับไป BookingPage

    # Appearance and state when the button is selected
    def select(self):
        """Change to selected state (green border)"""

        self.setStyleSheet("""
            RoomCard {
                background-color: #f0fdf4;
                border: 2px solid #22c55e;
                border-radius: 12px;
            }
        """)
        self.select_btn.setStyleSheet("""
            QPushButton {
                background-color: #22c55e;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 5px;
                font-weight: bold;
            }
        """)
        self.select_btn.setText("✓ Selected")

    def deselect(self):
        """Change back to normal state"""

        self.setStyleSheet("""
            RoomCard {
                background-color: #ffffff;
                border: 2px solid #e5e7eb;
                border-radius: 12px;
            }
            RoomCard:hover {
                border: 2px solid #6366f1;
                background-color: #f5f3ff;
            }
        """)
        self.select_btn.setStyleSheet("""
            QPushButton {
                background-color: #6366f1;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 5px;
            }
            QPushButton:hover { background-color: #4f46e5; }
        """)
        self.select_btn.setText("Select Room")

    def is_selected(self):
        return self._is_selected
    

class ConfirmDialog(QDialog):
    """
    Booking confirmation popup — Custom Dialog Class
    Practice:
      - Inheriting QDialog
      - Building layout and widgets inside the dialog manually
    """

    def __init__(self, guest_name: str, room_name: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Booking Confirmed")
        self.setFixedSize(360, 220)
        self.setModal(True)
        self._build_ui(guest_name, room_name)

    def _build_ui(self, guest_name: str, room_name: str):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        # 1. Create labels and button in the card
        icon = QLabel("🎉") #สร้าง icon
        icon.setFont(QFont("Arial", 28))
        icon.setAlignment(Qt.AlignCenter)

        title = QLabel("✅ Booking Confirmed!")
        title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)

        guest_name_label = QLabel(f"Thank you, <b>{guest_name}</b>!") # แสดงชื่อแขกที่จอง
        guest_name_label.setFont(QFont("Segoe UI", 10))
        guest_name_label.setTextFormat(Qt.RichText)
        guest_name_label.setAlignment(Qt.AlignCenter)

        room_name_label = QLabel(f"Your <b>{room_name}</b> has been reserved.") # แสดงชื่อห้องที่จอง
        room_name_label.setFont(QFont("Segoe UI", 10))
        room_name_label.setTextFormat(Qt.RichText)
        room_name_label.setAlignment(Qt.AlignCenter)

        ok_btn = QPushButton("OK")
        ok_btn.setFixedHeight(38)
        ok_btn.setFont(QFont("Segoe UI", 13, QFont.Bold))
        ok_btn.setCursor(Qt.PointingHandCursor)
        ok_btn.setStyleSheet("""
            QPushButton {
                background-color: #22c55e;
                color: white; border: none;
                border-radius: 8px; 
            }
            QPushButton:hover { background-color: #16a34a; }
        """)
        ok_btn.clicked.connect(self.accept) # ปิด dialog เมื่อคลิกปุ่ม
        # accept() เป็น method ของ QDialog อยู่แล้ว ไม่ต้องเขียนเอง พอเรียก dialog จะปิดตัวเองทันที

        # 2. เพิ่มทุกอย่าง labels and button ลง layout
        layout.addWidget(icon)
        layout.addWidget(title)
        layout.addWidget(guest_name_label)
        layout.addWidget(room_name_label)
        layout.addStretch()
        layout.addWidget(ok_btn)

# ─────────────────────────────────────────────
#  Page 1: Booking Page
# ─────────────────────────────────────────────
class BookingPage(QWidget):
    """
    Page 1 — Guest information form and room selection
    """

    def __init__(self):
        super().__init__()
        self.selected_room = None
        self.selected_price = 0
        self.cards = [] # a list of RoomCard object
        self._build_ui()

    def _build_ui(self):
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)

        container = QWidget()
        main_layout = QVBoxLayout(container)
        main_layout.setContentsMargins(30, 24, 30, 24)
        main_layout.setSpacing(20)

        # Title
        title = QLabel("🏨 Book Your Stay at CozyStay")
        title.setFont(QFont("Segoe UI", 19, QFont.Bold))
        title.setStyleSheet("color: #1e1b4b;")

        subtitle = QLabel("Fill in your details and choose your room")
        subtitle.setFont(QFont("Segoe UI", 12))
        subtitle.setStyleSheet("color: #6b7280;")
         # Add widgets to the main_layout
        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)

        # ── Section 1: Guest Info Form ──
        form_title = QLabel("📋 Guest Information")
        form_title.setFont(QFont("Segoe UI", 13, QFont.Bold))
        form_title.setStyleSheet("color: #374151; margin-top: 8px;")
        main_layout.addWidget(form_title)

        form_frame = QFrame()
        form_frame.setStyleSheet("""
            QFrame {
                background-color: #f9fafb;
                border-radius: 10px;
            }
        """)

        # Create widgets for inputs
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("e.g.Wednesday Addams")

        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("e.g. 081-345-6789")

        self.checkin_input = QDateEdit() # ปฏิทินเลือกวันที่เช็คอิน
        self.checkin_input.setCalendarPopup(True)
        self.checkin_input.setDate(QDate.currentDate()) # ตั้งค่าเริ่มต้นเป็นวันที่ปัจจุบัน

        self.checkout_input = QDateEdit() # ปฏิทินเลือกวันที่เช็คเอาท์
        self.checkout_input.setCalendarPopup(True)
        self.checkout_input.setDate(QDate.currentDate().addDays(1)) # ตั้งค่าเริ่มต้นเป็นวันถัดไป

        self.guests_input = QSpinBox() # เลือกจำนวนแขก
        self.guests_input.setRange(1, 10)
        self.guests_input.setValue(1)
        
        # Set style for inputs and their labels
        input_style = """
            QLineEdit, QDateEdit, QSpinBox {
                border: 1px solid #d1d5db;
                border-radius: 6px;
                padding: 6px 10px;
                font-size: 13px;
                background: white;
            }
            QLineEdit:focus, QDateEdit:focus, QSpinBox:focus {
                border: 1px solid #6366f1;
            }
        """
        for w in [self.name_input, self.phone_input,
                  self.checkin_input, self.checkout_input, self.guests_input]:
            w.setStyleSheet(input_style)
            w.setMinimumWidth(200)

        # add label and widget to your layout
        form_layout = QFormLayout(form_frame)
        form_layout.setContentsMargins(16,16,16,16)
        form_layout.setSpacing(10)

        label_style = "font-size: 13px; color: #374151; font-weight: bold;"
        for text, widget in [
            ("Full Name :",       self.name_input),
            ("Phone Number :",    self.phone_input),
            ("Check-in Date :",   self.checkin_input),
            ("Check-out Date :",  self.checkout_input),
            ("Guests :",          self.guests_input),
        ]:
            lbl = QLabel(text)
            lbl.setStyleSheet(label_style)
            form_layout.addRow(lbl, widget)


        main_layout.addWidget(form_frame)


        # ── Section 2: Room Selection ──
        room_title = QLabel("🛏 Select a Room")
        room_title.setFont(QFont("Segoe UI", 13, QFont.Bold))
        room_title.setStyleSheet("color: #374151; margin-top: 8px;")
        main_layout.addWidget(room_title)

        rooms_data = [
            ("Standard Room", 50,  "Single bed, Free Wi-Fi",             "🛌"),
            ("Deluxe Room",   120, "Double bed, Ocean view, Wi-Fi",      "🌊"),
            ("Suite Room",    250, "Living room, Jacuzzi, Premium view", "👑"),
            ("Family Room",   160, "2 Bedrooms, Perfect for families",   "👨‍👩‍👧‍👦"),
        ]

        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(14)
        cards_layout.setContentsMargins(0, 0, 0, 0)

        # Create cards according to the info above
        # Remember to put each card in self.cards
        # also catch the emitted signal from each card
        for room_name, price, description, emoji in rooms_data:
            small_card = RoomCard(room_name, price, description, emoji)
            small_card.room_selected.connect(self._on_room_selected)
            self.cards.append(small_card)
            cards_layout.addWidget(small_card)

        cards_layout.addStretch()
        main_layout.addLayout(cards_layout)


        # ── Buttons ──
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(12)

        self.clear_btn = QPushButton("🗑  Clear Info")
        self.clear_btn.setFixedHeight(42)
        self.clear_btn.setFont(QFont("Segoe UI", 11))
        self.clear_btn.setCursor(Qt.PointingHandCursor)
        self.clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #f3f4f6;
                color: #374151;
                border: 1px solid #d1d5db;
                border-radius: 8px;
                padding: 0 20px;
            }
            QPushButton:hover { background-color: #e5e7eb; }
        """)
        # Connect the button's signal to a slot
        self.clear_btn.clicked.connect(self.clear_form) # เชื่อมสัญญาณจากปุ่ม Clear Info ไปยัง slot clear_form ใน BookingPage

        self.next_btn = QPushButton("Next  →")
        self.next_btn.setFixedHeight(42)
        self.next_btn.setFont(QFont("Segoe UI", 11, QFont.Bold))
        self.next_btn.setCursor(Qt.PointingHandCursor)
        self.next_btn.setStyleSheet("""
            QPushButton {
                background-color: #6366f1;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 0 28px;
            }
            QPushButton:hover { background-color: #4f46e5; }
        """)

        btn_layout.addWidget(self.clear_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(self.next_btn)

        main_layout.addLayout(btn_layout)
        main_layout.addStretch()

        scroll.setWidget(container)

        page_layout = QVBoxLayout(self)
        page_layout.setContentsMargins(0, 0, 0, 0)
        page_layout.addWidget(scroll)

    def _on_room_selected(self, room_name: str, price: int):
        """Receive signal from RoomCard, update state, deselect other cards"""
        self.selected_room = room_name # บันทึกห้องที่เลือก
        self.selected_price = price 
        for card in self.cards:
            if card.room_name != room_name:
                card.deselect() # ยกเลิกการเลือกห้องอื่นๆ ที่ไม่ใช่ห้องที่ถูกเลือก
                card._is_selected = False # อัปเดตสถานะของการ์ดอื่นๆ ให้เป็นไม่ถูกเลือก

    def clear_form(self):
        """Clear all form fields in User From and deselect all room cards"""
        self.name_input.clear()
        self.phone_input.clear()
        self.checkin_input.setDate(QDate.currentDate())
        self.checkout_input.setDate(QDate.currentDate().addDays(1))
        self.guests_input.setValue(1)

        self.selected_room = None #str
        self.selected_price = 0 #int

        for card in self.cards:
            card.deselect()
            card._is_selected = False

    def get_booking_data(self):
        """Collect form data — returns None if validation fails"""
        name = self.name_input.text().strip()
        phone = self.phone_input.text().strip()
        checkin = self.checkin_input.date() 
        checkout = self.checkout_input.date() #เปลี่ยนจาก QDateEdit เป็น QDate เพื่อให้เปรียบเทียบวันที่ได้

        if not name:
            QMessageBox.warning(self, "Missing Information", "Please enter your full name.")
            return None
        if not phone:
            QMessageBox.warning(self, "Missing Information", "Please enter your phone number.")
            return None
        if checkin >= checkout:
            QMessageBox.warning(self, "Invalid Dates",
                                "Check-out date must be after check-in date.")
            return None
        if not self.selected_room:
            QMessageBox.warning(self, "No Room Selected",
                                "Please select a room before proceeding.")
            return None

        nights = checkin.daysTo(checkout) # คำนวณจำนวนคืนที่พัก โดยใช้เมธอด daysTo ของ QDate
        total = nights * self.selected_price # คำนวณราคารวม

        # Create a dictionary of all values to be returned
        data_dict = {
            "name": name,
            "phone": phone,
            "checkin": checkin.toString("dd-MM-yyyy"), # แปลง QDate เป็น string
            "checkout": checkout.toString("dd-MM-yyyy"),
            "guests": self.guests_input.value(),
            "room": self.selected_room,
            "price": self.selected_price,
            "nights": nights,
            "total": total
        }

        return data_dict

# ─────────────────────────────────────────────
#  PAGE 2: ReviewPage
# ─────────────────────────────────────────────
class ReviewPage(QWidget):
    """
    Page 2 — Review booking details before submitting
    """

    def __init__(self):
        super().__init__()
        self.current_data = {}
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(16)

        title = QLabel("📋 Booking Summary")
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        title.setStyleSheet("color: #1e1b4b;")

        subtitle = QLabel("Please review your details before confirming")
        subtitle.setFont(QFont("Segoe UI", 10))
        subtitle.setStyleSheet("color: #6b7280;")

        layout.addWidget(title)
        layout.addWidget(subtitle)

        self.info_frame = QFrame()
        self.info_frame.setStyleSheet("""
            QFrame {
                background-color: #f9fafb;
                border-radius: 12px;
            }
        """)

        # You can use other layout, like a form layout
        self.info_layout = QGridLayout(self.info_frame)

        display_data = [
            ("🛏  Room",            ""),
            ("💰  Price / Night",   f"$ -"),
            ("👤  Guest Name",      ""),
            ("📞  Phone",           ""),
            ("📅  Check-in",        ""),
            ("📅  Check-out",       ""),
            ("🌙  Nights",          f"- night(s)"),
            ("👥  Guests",          f"- guest(s)"),
        ]

        key_style = "font-weight: bold; color: #374151; font-size: 13px;"
        val_style = "color: #1f2937; font-size: 13px;"

        # Put labels and placeholder into the layout

        self.val_labels = {}   # เก็บ label ฝั่งขวาไว้ update ทีหลัง

        for row, (key, placeholder) in enumerate(display_data):
            key_lbl = QLabel(key)
            key_lbl.setStyleSheet(key_style)

            val_lbl = QLabel(placeholder)
            val_lbl.setStyleSheet(val_style)
            val_lbl.setObjectName(key) # Set object name to find it later when loading data

            self.info_layout.addWidget(key_lbl, row, 0,)
            self.info_layout.addWidget(val_lbl, row, 1,)

            self.val_labels[key] = val_lbl # เก็บ reference ของ label ฝั่งขวาไว้ใน dict เพื่อใช้ตอน load data

        layout.addWidget(self.info_frame)

        # hline
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("color: #e5e7eb;")
        layout.addWidget(line)

        # Create the Total label and add to the layout
        self.total_label = QLabel("💵 Total: $ -")
        self.total_label.setFont(QFont("Segoe UI", 14, QFont.Bold))
        self.total_label.setStyleSheet("color: #6366f1;")
        self.total_label.setAlignment(Qt.AlignRight)
        layout.addWidget(self.total_label)

        layout.addStretch()

        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(12)

        self.back_btn = QPushButton("←  Back")
        self.back_btn.setFixedHeight(44)
        self.back_btn.setFont(QFont("Segoe UI", 11))
        self.back_btn.setCursor(Qt.PointingHandCursor)
        self.back_btn.setStyleSheet("""
            QPushButton {
                background-color: #f3f4f6;
                color: #374151;
                border: 1px solid #d1d5db;
                border-radius: 8px;
                padding: 0 22px;
            }
            QPushButton:hover { background-color: #e5e7eb; }
        """)

        self.submit_btn = QPushButton("✅  Confirm Booking")
        self.submit_btn.setFixedHeight(44)
        self.submit_btn.setFont(QFont("Segoe UI", 11, QFont.Bold))
        self.submit_btn.setCursor(Qt.PointingHandCursor)
        self.submit_btn.setStyleSheet("""
            QPushButton {
                background-color: #22c55e;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 0 28px;
            }
            QPushButton:hover { background-color: #16a34a; }
        """)

        btn_layout.addWidget(self.back_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(self.submit_btn)
        layout.addLayout(btn_layout)

    def load_data(self, data: dict):
        """Receive data dict from BookingPage and populate the review layout"""
        self.current_data = data    

        # Set all values from data in appropriate labels
        mapping = {
            "🛏  Room": data.get("room"),
            "💰  Price / Night": f"$ {data.get('price')}",
            "👤  Guest Name": data.get("name"),
            "📞  Phone": data.get("phone"),
            "📅  Check-in": data.get("checkin"),
            "📅  Check-out": data.get("checkout"),
            "🌙  Nights": f"{data.get('nights')} night(s)",
            "👥  Guests": f"{data.get('guests')} guest(s)",
        }

        for key, value in mapping.items():
            if key in self.val_labels: 
                self.val_labels[key].setText(value) #อัปเดตข้อความใน label ฝั่งขวาตาม key ที่กำหนดไว้

        # Update the total label
        total = data.get("total", 0)
        self.total_label.setText(f"💵 Total: $ {total}")


class MainWindow(QMainWindow):
    """
    Main window — uses QStackedWidget to manage 2 pages
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("CozyStay — Hotel Booking System")
        self.setMinimumSize(620, 780)
        self.resize(900, 720)

        # QStackedWidget as central widget
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # Create pages ด้วยการเรียก class ของแต่ละหน้า
        self.booking_page = BookingPage()
        self.review_page = ReviewPage()

        # Add to stack: index 0 = booking, index 1 = review
        self.stack.addWidget(self.booking_page) # เพิ่มหน้า booking_page เข้าไปใน stack
        self.stack.addWidget(self.review_page) # เพิ่มหน้า review_page เข้าไปใน stack

        # Connect navigation
        self.booking_page.next_btn.clicked.connect(self._go_to_review)
        self.review_page.back_btn.clicked.connect(self._go_to_booking)
        self.review_page.submit_btn.clicked.connect(self._on_submit)
        
        # Start on page 0
        # Set current stack index to the first page
        self.stack.setCurrentIndex(0)
        

        self.setStyleSheet("""
            QMainWindow { background-color: #f0f0ff; }
            QScrollArea  { background-color: transparent; }
            QWidget      { font-family: 'Segoe UI', 'Tahoma', sans-serif; }
        """)

    # Slot for the next_btn on the booking page
    def _go_to_review(self):
        """Validate form, then switch to Review page"""
        
        data = self.booking_page.get_booking_data() # get booking data

        if data is None:
            return
        
        # Load Booking data into the review page
        self.review_page.load_data(data)

        # Set stack index to the review page
        self.stack.setCurrentIndex(1)

    # Slot for the back_btn on the review page
    def _go_to_booking(self):
        """Go back to Booking page, form data remains intact"""
        self.stack.setCurrentIndex(0)


    # slot for the submit_btn on the review page
    def _on_submit(self):
        """Show ConfirmDialog, then reset the entire app"""
        data = self.review_page.current_data # get current data from review page

        # Create a ConfirmDialog object
        dialog = ConfirmDialog(
                guest_name=data["name"],
                room_name=data["room"],
                parent=self) # กำหนด parent เป็น self เพื่อให้ dialog อยู่บนหน้าต่างหลัก และปิด dialog ได้ง่ายขึ้นเมื่อกดปุ่ม OK
        
        # then show the dialog
        dialog.exec() # ใช้ exec_() เพื่อแสดง dialog และรอจนกว่าผู้ใช้จะปิด dialog

        # Clear booking page data
        self.booking_page.clear_form()
        # Show the booking page
        self.stack.setCurrentIndex(0)

def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()