import os
import time
import threading
import requests
import feedparser
import schedule
from flask import Flask
import google.generativeai as genai

# ==================== خادم وهمي لإرضاء Render ====================
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running live!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# ==================== البيانات والروابط ====================
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
ID_INSTANCE = os.environ.get("ID_INSTANCE", "710722756852")
API_TOKEN_INSTANCE = os.environ.get("API_TOKEN_INSTANCE")
CHAT_ID = os.environ.get("CHAT_ID", "120363429270874527@g.us")

RSS_URL = "https://www.reddit.com/r/ClashOfClans/hot.rss"

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

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
            print("ℹ️ لا توجد أخبار جديدة.")
            return
            
        print(f"📰 تم العثور على خبر جديد: {title}")
        
        prompt = f"""
        أنت مساعد متخصص ومحترف في لعبة Clash of Clans. 
        قم بتلخيص الخبر المرفق باللغة العربية بأسلوب جذاب وممتع لمجتمع واتساب.
        استخدم إيموجيات مناسبة واجعل النقاط واضحة ومختصرة.

        عنوان الخبر: {title}
        تفاصيل الخبر: {summary_raw}
        """
        
        response = model.generate_content(prompt)
        arabic_summary = response.text
        
        url = f"https://api.green-api.com/waInstance{ID_INSTANCE}/sendMessage/{API_TOKEN_INSTANCE}"
        payload = {"chatId": CHAT_ID, "message": arabic_summary}
        headers = {'Content-Type': 'application/json'}
        
        res = requests.post(url, json=payload, headers=headers)
        if res.status_code == 200:
            print("✅ تم إرسال التلخيص إلى الواتساب بنجاح!")
            last_processed_title = title
        else:
            print(f"⚠️ فشل الإرسال: {res.text}")
    except Exception as e:
        print(f"❌ حدث خطأ: {e}")

schedule.every().day.at("20:00").do(fetch_and_send_news)

def run_schedule():
    fetch_and_send_news()
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == '__main__':
    t = threading.Thread(target=run_schedule)
    t.daemon = True
    t.start()
    run_flask()
