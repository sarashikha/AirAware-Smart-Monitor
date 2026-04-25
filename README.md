🌡️ AirAware: Smart Environment Monitoring System
AirAware היא מערכת IoT מתקדמת לניטור טמפרטורה ולחות בזמן אמת, המיועדת לשימוש חקלאי ותעשייתי. המערכת מחברת בין חומרת קצה (Raspberry Pi) לענן, ומציגה את הנתונים ב-Dashboard אינטראקטיבי הנגיש מכל מכשיר.

🚀 תכונות מרכזיות (Key Features)
Real-time Sync: סנכרון מיידי מול Google Firebase Firestore.

Cross-Platform: ממשק Responsive מבוסס Flet המתאים ל-Windows, iPhone ו-Android.

Smart Alerting: מערכת התראות מובנית הכוללת הודעות WhatsApp ונוטיפיקציות Push במצבי קיצון.

High Stability: מעקף חומרתי מובנה (Software Rendering) למניעת קפיאות ממשק במחשבים ישנים.

Remote Access: תמיכה בגישה מרשתות חיצוניות באמצעות פורט קבוע (9000).

🛠️ ארכיטקטורת המערכת (SOA)
המערכת בנויה בשיטת 4 השכבות (Service Oriented Architecture):

Presentation Layer: ממשק משתמש מודרני (Dark Mode) ב-Python Flet.

Service Layer: מאזין אסינכרוני (Firebase Snapshot Listener).

Business Logic: ניתוח ספי חום ושליחת התראות אוטומטיות.

Data Layer: בסיס נתונים NoSQL מבוזר בענן.

📦 התקנה והרצה (Setup)
התקן את הספריות הנדרשות:

Bash
pip install flet firebase-admin plyer pywhatkit
וודא שקובץ ה-JSON של Firebase נמצא בתיקיית השורש.

הרץ את המערכת:

Bash
python main.py
גש לדשבורד מכל דפדפן בכתובת: http://localhost:9000 או דרך ה-IP של המכשיר.

🧪 תהליך ה-QA והלקחים
במהלך הפיתוח זוהה באג רינדור (Rendering) בדרייברים של Windows. הבעיה נפתרה באמצעות הטמעת os.environ["FLET_RENDERER"] = "software", מה שמבטיח ריצה חלקה גם ללא האצת חומרה.
