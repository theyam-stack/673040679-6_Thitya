import json
import pandas as pd
import pyqtgraph as pg
from PySide6.QtCore import Qt

from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView

# ══════════════════════════════════════════════════════════════════════════
#  CONSTANTS - do not change
# ══════════════════════════════════════════════════════════════════════════

REQUIRED_COLS = {"date", "city", "temp_c", "humidity", "rainfall_mm", "condition"}
CONDITIONS    = ["Sunny", "Cloudy", "Rainy", "Stormy"]
CITIES        = ["Bangkok", "Chiang Mai", "Phuket"]


# ══════════════════════════════════════════════════════════════════════════
#  YOUR WORK — complete the 6 functions below
# ══════════════════════════════════════════════════════════════════════════

def read_csv(path: str) -> pd.DataFrame:
    """
    To do 1 — Read a CSV file and return a clean DataFrame.
    """
    df = pd.read_csv(path) # อ่านไฟล์ csv
    
    missing = REQUIRED_COLS - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {missing}")

    # แปลง date เป็น string format yyyy-mm-dd ให้สม่ำเสมอ
    df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")
    return df


def read_json(path: str) -> pd.DataFrame:
    """
    To do 2 — Read a JSON file and return a DataFrame.
    """
    df = pd.read_json(path) #อ่านไฟล์ json

    # ตรวจสอบคอลัมน์ให้ครบ
    missing = REQUIRED_COLS - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {missing}")

    df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")
    return df


def write_csv(df: pd.DataFrame, path: str) -> None:
    """
    To do 3 — Save a DataFrame to a CSV file.
    """
    df.to_csv(path, index=False)   # index=False = ไม่บันทึกเลข 0,1,2... ลงไฟล์


def write_json(df: pd.DataFrame, path: str) -> None:
    """
    To do 4 — Save a DataFrame to a JSON file.
    """
    df.to_json(path, orient="records", indent=2)
    # orient="records" = บันทึกเป็น list of dict เหมือน weather_extra.json
    # indent=2        = ย่อหน้า 2 space ให้อ่านง่าย

def build_stats(df: pd.DataFrame) -> QTableWidget:
    """
    To do 5 — Return a summary string shown in the Statistics panel.
    """
    stats = df.groupby("city").agg(
        avg_temp = ("temp_c", "mean"),  # ชื่อคอลัมน์ใหม่ = (คอลัมน์เดิม, วิธีคำนวณ)
        avg_hum = ("humidity", "mean"),
        total_rain = ("rainfall_mm", "sum"),
        rainy_days = ("rainfall_mm", lambda x: (x > 0).sum()),
        # นับจำนวนแถวที่ฝนมากกว่า 0 เพราะ True = 1, False = 0 พอ .sum() ก็ได้จำนวนวันที่ฝนตก
    ).reset_index()

    # สร้าง QTableWidget
    headers = ["City", "Avg Temp (°C)", "Avg Humidity (%)",
               "Total Rainfall (mm)", "Rainy Days"]

    table = QTableWidget(len(stats), len(headers))
    table.setHorizontalHeaderLabels(headers)
    table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    table.setEditTriggers(QTableWidget.NoEditTriggers)  # ห้ามแก้ไข
    table.setAlternatingRowColors(True)

    for row, r in stats.iterrows():
        table.setItem(row, 0, QTableWidgetItem(r["city"]))
        table.setItem(row, 1, QTableWidgetItem(f"{r['avg_temp']:.1f}"))
        table.setItem(row, 2, QTableWidgetItem(f"{r['avg_hum']:.1f}"))
        table.setItem(row, 3, QTableWidgetItem(f"{r['total_rain']:.1f}"))
        table.setItem(row, 4, QTableWidgetItem(str(int(r['rainy_days']))))

        # จัด text ให้อยู่กึ่งกลาง
        for col in range(len(headers)):
            item = table.item(row, col)
            if item:
                item.setTextAlignment(Qt.AlignCenter)
    return table

def show_chart(df: pd.DataFrame, chart_type: str) -> pg.PlotWidget:
    """
    To do 6 — Draw a Rainfall Histogram chart using pyqtgraph and return a PlotWidget.
    """
    rain = df.groupby("city")["rainfall_mm"].sum()

    cities  = list(rain.index)        # ["Bangkok", "Chiang Mai", "Phuket"]
    totals  = list(rain.values)       # [219.0, 145.9, 198.1]
    x_pos   = list(range(len(cities))) # [0, 1, 2]

    # สร้าง PlotWidget
    pw = pg.PlotWidget()
    pw.setBackground("w")             # พื้นหลังขาว
    pw.setTitle("Total Rainfall by City", color="k", size="13pt")
    pw.setLabel("left",   "Rainfall (mm)", color="k")
    pw.setLabel("bottom", "City",          color="k")

    # สีแต่ละเมือง
    colors = ["#378ADD", "#639922", "#D85A30"]   # blue, green, coral

    for i, (city, total, color) in enumerate(zip(cities, totals, colors)):
        bar = pg.BarGraphItem(
            x=[i],
            height=[total],
            width=0.6,
            brush=color,
            pen=pg.mkPen("w", width=1)   # ขอบขาว
        )
        pw.addItem(bar)

    # แกน x เป็นชื่อเมือง
    ticks = [[(i, city) for i, city in enumerate(cities)]]
    pw.getAxis("bottom").setTicks(ticks)
    # ── ปิด zoom แกน x ไม่ให้เลื่อนออกนอก ──
    pw.setXRange(-0.5, len(cities) - 0.5)
    pw.setYRange(0, max(totals) * 1.2)   # เผื่อ 20% ด้านบน

    return pw