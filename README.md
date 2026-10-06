# Clash Arabic News Bot

بوت يقرأ أحدث خبر من مدونة Clash of Clans الرسمية، يلخصه بالعربية عبر Gemini، ثم يرسله إلى مجموعة واتساب عبر Green API.

## التحديث الأخير

تم استبدال Reddit كمصدر أساسي بمدونة Supercell الرسمية لتجنب خطأ `429 Too Many Requests` الشائع على عناوين Render المجانية. يمكن ترك `RSS_URL` فارغًا، وسيستخدم التطبيق المصدر الرسمي مباشرة. كما أصبح `/health` يعكس أن خدمة الويب حية حتى لو تعطل مصدر خارجي مؤقتًا، مع إظهار تفاصيل آخر تشغيل في الحقل `state`.

## التشغيل والنشر

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python main.py
```

في Render استخدم:

```text
Build Command: pip install -r requirements.txt
Start Command: python main.py
```

وأضف متغيرات الأسرار في Environment Variables فقط. لا ترفع `.env` إلى GitHub.

```text
GEMINI_API_KEY=...
GREEN_API_ID_INSTANCE=...
GREEN_API_TOKEN_INSTANCE=...
WHATSAPP_CHAT_ID=120363429270874527@g.us
SEND_ON_START=true
RUN_AT=20:00
GEMINI_MODEL=gemini-2.5-flash
GEMINI_TIMEOUT=90
GEMINI_RETRIES=3
OFFICIAL_BLOG_URL=https://supercell.com/en/games/clashofclans/blog/
RSS_URL=
```

افتح `/health` بعد النشر. وجود `"ok": true` يعني أن خدمة الويب تعمل. راقب `state`: القيمة `success` تعني أن الرسالة أُرسلت، و`idle` تعني أنه لا يوجد خبر جديد أو أن الخبر أُرسل سابقًا، و`error` تعني وجود خطأ يحتاج مراجعة سجل Render.

## الأمان

المفاتيح القديمة التي ظهرت في النسخة الأولى أو داخل سجلات Render يجب اعتبارها مكشوفة؛ الأفضل إلغاؤها وإنشاء مفاتيح جديدة. لا تضع أي مفتاح في الكود أو GitHub أو المحادثات. النموذج `gemini-2.0-flash` تم إيقافه، لذلك يستخدم المشروع `gemini-2.5-flash`، مع احتياطي تلقائي إذا بقي إعداد قديم في Render. إذا تأخر Gemini، ينتظر التطبيق حتى 90 ثانية ويعيد المحاولة ثلاث مرات.

## التشغيل اليومي

`SEND_ON_START=true` يجعل البوت يجرب الإرسال عند كل تشغيل، وهو مناسب للاختبار الأول. بعد نجاح الاختبار يمكن جعله `false`. يرسل التطبيق مرة يوميًا عند `RUN_AT` حسب المنطقة الزمنية للخادم. خطة Render المجانية قد توقف الخدمة عند الخمول، لذلك قد يتأخر التشغيل اليومي بعد السكون.
