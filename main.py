import os
import time
import threading
import requests
import feedparser
import schedule
from flask import Flask
from google import genai

# ==================== إعداد سيرفر وهمي لمنصة Render ====================
app = Flask(__name__)

@app.route('/')
def home():
    return "Clash Bot is Running Successfully!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# ==================== البيانات والروابط ====================
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
ID_INSTANCE = os.environ.get("ID_INSTANCE", "710722756852")
API_TOKEN_INSTANCE = os.environ.get("API_TOKEN_INSTANCE")
CHAT_ID = os.environ.get("CHAT_ID", "120363429270874527@g.us")

RSS_URL = "https://www.reddit.com/r/ClashOfClans/hot.rss"

# إعداد مكتبة Gemini الحديثة
client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None

last_processed_title = ""

def fetch_and_send_news():
    global last_processed_title
    
    try:
        print("🔎 جاري البحث عن أخبار جديدة...")
        feed = feedparser.parse(RSS_URL)
        
        if not feed.entries:
            print("❌ لم يتم العثور على أخبار.")
            return
            
        latest_entry = feed.entries[0]
        title = latest_entry.title
        summary_raw = getattr(latest_entry, 'summary', latest_entry.title)
        
        if title == last_processed_title:
            print("ℹ️ لا توجد أخبار جديدة، تم إرسال هذا الخبر سابقاً.")
            return
            
        print(f"📰 تم العثور على خبر جديد: {title}")
        
        prompt = f"""
        أنت مساعد متخصص ومحترف في لعبة Clash of Clans. 
        قم بتلخيص الخبر المرفق باللغة العربية بأسلوب جذاب وممتع لمجتمع واتساب.
        استخدم إيموجيات مناسبة واجعل النقاط واضحة ومختصرة.

        عنوان الخبر: {title}
        تفاصيل الخبر: {summary_raw}
        """
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        arabic_summary = response.text
        
        url = f"https://api.green-api.com/waInstance{ID_INSTANCE}/sendMessage/{API_TOKEN_INSTANCE}"
        payload = {
            "chatId": CHAT_ID,
            "message": arabic_summary
        }
        headers = {'Content-Type': 'application/json'}
        
        res = requests.post(url, json=payload, headers=headers)
        
        if res.status_code == 200:
            print("✅ تم إرسال التلخيص إلى مجموعة الواتساب بنجاح!")
            last_processed_title = title
        else:
            print(f"⚠️ فشل الإرسال إلى الواتساب: {res.text}")
            
    except Exception as e:
        print(f"❌ حدث خطأ أثناء تشغيل السكربت: {e}")

# جدولة التشغيل يومياً الساعة 8:00 مساءً
schedule.every().day.at("20:00").do(fetch_and_send_news)

def run_schedule():
    # تشغيل فحص فوري عند البدء
    fetch_and_send_news()
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == '__main__':
    # تشغيل المجدول في الخلفية
    t = threading.Thread(target=run_schedule)
    t.daemon = True
    t.start()
    
    # تشغيل سيرفر الويب الاستجابي لـ Render
    run_flask()
