import flet as ft
import firebase_admin
from firebase_admin import credentials, firestore
from plyer import notification
import threading
import time

# 1. אתחול Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate("airaware-a7924-firebase-adminsdk-fbsvc-b4cf93d049.json")
    firebase_admin.initialize_app(cred)
db = firestore.client()

def main(page: ft.Page):
   #--- הגדרות דף בסיסיות ---
    page.title = "AirAware Smart Monitor"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_always_on_top = True  # מבטיח רענון גרפי רציף ב-Windows
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    def force_rendering():
        while True:
            try:
                page.update() # זה ה"קליק" האוטומטי שמעיר את המסך
                time.sleep(0.5) # רענון כל חצי שנייה
            except:
                break

    # הפעלה מיידית של הריענון ב-Thread נפרד
    threading.Thread(target=force_rendering, daemon=True).start()
    
    # משתני דגל למניעת "הפצצת" התראות
    page.whatsapp_sent = False
    page.notification_sent = False
    page.user_phone = ""
    
    # רכיבי UI (מוגדרים ברמת ה-main לסנכרון מושלם)
    temp_txt = ft.Text("0.0°C", size=70, weight="bold", color="white")
    hum_txt = ft.Text("Humidity: 0%", size=22, color="#8E94B2")
    status_msg = ft.Text("SYSTEM ACTIVE", color="#4ECCA3", weight="bold")
    bottom_line = ft.Container(width=80, height=3, bgcolor="#4ECCA3", border_radius=2)
    monitor_card = ft.Container(bgcolor="#1A1C2E", border_radius=40, padding=40)
    
    # פונקציית ווטסאפ מהירה ב-Thread נפרד
    def send_whatsapp_fast(temp):
        # שימוש ב-Thread נפרד לחלוטין כדי שהאפליקציה לא תחכה לדפדפן
        import pywhatkit as kit
        def worker():
            try:
                phone = page.user_phone
                clean_phone = "+972" + phone[1:] if phone.startswith("0") else "+972" + phone
                # צמצום זמנים למינימום האפשרי
                kit.sendwhatmsg_instantly(clean_phone, f" חום חריג!!!: {temp}°C ", 12, True, 4)
            except: pass
        
        threading.Thread(target=worker, daemon=True).start()
        
    # מנגנון ה-Snapshot (מתעדכן מיד מה-Raspberry Pi)
    def on_snapshot(doc_snapshot, changes, read_time):
            for doc in doc_snapshot:
                data = doc.to_dict()
                if not data: continue
                
                t = float(data.get('temp', 0))
                temp_txt.value = f"{t}°C"
                hum_txt.value = f"Humidity: {data.get('hum', 0)}%"
                page.update()
                
                if t >= 27.0:
                    # שינוי ויזואלי מיידי
                    monitor_card.bgcolor = "#451414"
                    status_msg.value = "⚠️ CRITICAL: TEMP HIGH"
                    status_msg.color = "#FF5252"
                    bottom_line.bgcolor = "#FF5252"
                    page.update()
                    
                    # התראות ב-Background מבלי לעצור את האפליקציה
                    if not page.notification_sent:
                        page.notification_sent = True
                        threading.Thread(target=lambda: notification.notify(title="AirAware", message=f" חום חריג!!!: {t}°C ", timeout=2), daemon=True).start()

                    if t >= 30.0 and not page.whatsapp_sent:
                        page.whatsapp_sent = True
                        threading.Thread(target=lambda: send_whatsapp_fast(t), daemon=True).start()
                else:
                    # חזרה למצב תקין
                    monitor_card.bgcolor = "#1A1C2E"
                    status_msg.value = "SYSTEM ACTIVE"
                    status_msg.color = "#4ECCA3"
                    bottom_line.bgcolor = "#4ECCA3"
                    page.notification_sent = False
                    page.whatsapp_sent = False
                
                page.update()

    def build_dashboard(user):
        page.clean()
        monitor_card.content = ft.Column([
            ft.Row([ft.Container(width=10, height=10, bgcolor="#4ECCA3", border_radius=5), status_msg], alignment=ft.MainAxisAlignment.CENTER),
            ft.Container(height=40),
            temp_txt, hum_txt,
            ft.Container(height=40),
            bottom_line
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)

        page.add(
            ft.Column([
                ft.Text(f"שלום, {user}", size=22, weight="bold", color="white"),
                ft.Container(height=20),
                monitor_card
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )
        
        db.collection("air_aware").document("latest").on_snapshot(on_snapshot)
        
    def start_app(username, phone):
        if not username or not phone: return
        page.user_phone = phone
        build_dashboard(username)
        
    def show_login():
        page.clean()
        #input_style = {"width": 300, "color": "white", "border_color": "#303841", "focused_border_color": "#4ECCA3", "border_radius": 10}
        user_in = ft.TextField(label="שם משתמש", width=300)
        phone_in = ft.TextField(label="מספר טלפון", width=300)
        
        page.add(
            ft.Column([
                ft.Text("AirAware", size=50, weight="bold", color="white"),
                ft.Container(height=20),
                user_in, phone_in,
                ft.Container(height=10),
                ft.FilledButton(
                    "התחברות", 
                    on_click=lambda _: start_app(user_in.value, phone_in.value), 
                    width=300, 
                    style=ft.ButtonStyle(bgcolor="#4ECCA3", color="black")
                )
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )
        
    show_login()
if __name__ == "__main__":
    ft.run(
        main,
        view=ft.AppView.WEB_BROWSER, # פותח בדפדפן כפי שעבד לך
        host="127.0.0.1",               # מאפשר למכשירים אחרים (כמו הטלפון שלך) להתחבר
        port=8080                    # כאן אתה קובע את הפורט הקבוע
    )