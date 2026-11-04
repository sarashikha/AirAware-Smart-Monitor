import flet as ft
import firebase_admin
from firebase_admin import credentials, firestore
from plyer import notification

if not firebase_admin._apps:
    cred = credentials.Certificate("airaware-a7924-firebase-adminsdk-fbsvc-b4cf93d049.json")
    firebase_admin.initialize_app(cred)
db = firestore.client()

def main(page: ft.Page):
    page.title = "AirAware Home Monitor"
    page.bgcolor = "#0F111A"
    page.window_width = 500
    page.window_height = 900
    page.scroll = "auto"
    
    page.last_alert_temp = 27.0
    # רשימה לשמירת היסטוריית המדידות לגרף
    data_points = [] 

    # רכיבי טקסט וסטטוס
    temp_display = ft.Text("0.0°C", size=60, weight="bold", color="white")
    hum_display = ft.Text("Humidity: 0%", size=20, color="#8E94B2")
    status_text = ft.Text("SYSTEM ACTIVE", size=12, weight="bold", color="#4ECCA3")
    status_dot = ft.Container(width=10, height=10, bgcolor="#4ECCA3", border_radius=5)
    bottom_line = ft.Container(width=80, height=3, bgcolor="#4ECCA3", border_radius=2)

    # הגדרת הגרף
    chart = ft.LineChart(
        data_series=[
            ft.LineChartData(
                points=[],
                color="#4ECCA3",
                stroke_width=4,
                curved=True,
                below_line_bgcolor=ft.colors.with_opacity(0.1, "#4ECCA3"),
                below_line_style=ft.Style.SOLID,
            )
        ],
        border=ft.border.all(1, ft.colors.with_opacity(0.2, "white")),
        horizontal_grid_lines=ft.ChartGridLines(interval=1, color=ft.colors.with_opacity(0.1, "white")),
        min_y=20,
        max_y=35,
        height=200,
        expand=True,
    )

    def on_snapshot(doc_snapshot, changes, read_time):
        for doc in doc_snapshot:
            data = doc.to_dict()
            if data:
                t = float(data.get('temp', 0))
                h = float(data.get('hum', 0))
                
                temp_display.value = f"{t}°C"
                hum_display.value = f"לחות: {h}%" # עברית לאמא
                
                # עדכון נקודות הגרף
                if len(data_points) > 15: # שומר רק את 15 המדידות האחרונות
                    data_points.pop(0)
                
                data_points.append(ft.LineChartDataPoint(len(data_points), t))
                chart.data_series[0].points = data_points[:]
                
                # לוגיקת צבעים והתראות
                if t >= 27.0:
                    color = "#FF5252"
                    status_text.value = "אזהרה: חם מהרגיל"
                    if t >= page.last_alert_temp:
                        notification.notify(title="התראת חום בבית", message=f"הטמפרטורה עלתה ל-{t}°C", timeout=5)
                        page.last_alert_temp = t + 1
                else:
                    color = "#4ECCA3"
                    status_text.value = "מצב תקין"
                    page.last_alert_temp = 27.0

                temp_display.color = "white" if t < 27 else color
                status_dot.bgcolor = color
                status_text.color = color
                bottom_line.bgcolor = color
                chart.data_series[0].color = color
                
                page.update()

    db.collection("air_aware").document("latest").on_snapshot(on_snapshot)

    # בניית הממשק הסופי
    page.add(
        ft.Column([
            ft.Container(
                content=ft.Column([
                    ft.Row([status_dot, status_text], alignment="center"),
                    ft.Container(height=20),
                    temp_display,
                    hum_display,
                    ft.Container(height=30),
                    bottom_line,
                ], horizontal_alignment="center"),
                bgcolor="#1A1C2E", padding=40, border_radius=30, margin=10
            ),
            ft.Container(
                content=ft.Column([
                    ft.Text("מגמת טמפרטורה", size=16, weight="bold", color="white"),
                    ft.Container(height=10),
                    chart,
                ]),
                bgcolor="#1A1C2E", padding=20, border_radius=30, margin=10
            )
        ])
    )

ft.app(target=main)