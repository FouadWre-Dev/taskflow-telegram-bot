# TaskFlow Bot 🤖

بوت تيليجرام لإدارة المهام الشخصية، مبني بمعمارية غير متزامنة (async) قابلة للتوسع، مع نظام صلاحيات للمشرفين، تخزين بيانات دائم عبر SQLAlchemy، ومعالجة أخطاء موحدة.

## ✨ المميزات

- إضافة، عرض، إنهاء وحذف المهام عبر محادثة تفاعلية (FSM).
- تحديد أولوية لكل مهمة (منخفضة / متوسطة / عالية).
- لوحة أزرار Inline وReply لتجربة استخدام سلسة.
- نظام صلاحيات مشرفين: إحصائيات عامة وبث رسائل جماعي (Broadcast) مع معاينة وتأكيد قبل الإرسال.
- تخزين بيانات دائم عبر SQLAlchemy (SQLite افتراضياً، وقابل للتبديل إلى PostgreSQL/MySQL بتغيير رابط الاتصال فقط).
- Middleware مخصص لـ:
  - الحد من معدل الطلبات (Rate Limiting) لكل مستخدم.
  - حقن قاعدة البيانات تلقائياً وتسجيل المستخدمين الجدد.
- معالجة أخطاء مركزية مع تسجيل (logging) إلى ملف وConsole في آن واحد.
- إعدادات مرنة عبر متغيرات بيئة (`.env`).

## 🛠️ التقنيات المستخدمة

| التقنية | الاستخدام |
|---|---|
| Python 3.12 | لغة البرمجة الأساسية |
| aiogram 3 | إطار عمل بوت تيليجرام غير المتزامن |
| SQLAlchemy 2.0 (Async) | ORM للتعامل مع قاعدة البيانات |
| SQLite / aiosqlite | قاعدة بيانات افتراضية خفيفة |
| python-dotenv | إدارة متغيرات البيئة |

## 📁 هيكلة المشروع

```
telegram-taskflow-bot/
├── bot/
│   ├── config.py            # تحميل الإعدادات من .env
│   ├── models.py             # نماذج SQLAlchemy
│   ├── database.py           # طبقة الوصول للبيانات
│   ├── keyboards.py          # لوحات المفاتيح
│   ├── states.py             # حالات FSM
│   ├── logging_config.py     # إعداد نظام التسجيل
│   ├── handlers/
│   │   ├── start.py          # أوامر البداية والمساعدة
│   │   ├── tasks.py          # إدارة المهام
│   │   ├── admin.py          # لوحة تحكم المشرفين
│   │   └── errors.py         # معالجة الأخطاء
│   └── middlewares/
│       ├── db.py              # حقن قاعدة البيانات
│       └── throttling.py      # الحد من الطلبات
├── main.py
├── requirements.txt
├── .env.example
└── .gitignore
```

## 🚀 التثبيت والتشغيل

```bash
git clone https://github.com/FouadWre-Dev/taskflow-telegram-bot.git
cd telegram-taskflow-bot

python -m venv venv
source venv/bin/activate      # على Windows: venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env
# عدّل BOT_TOKEN و ADMIN_IDS داخل .env

python main.py
```


## 📸 لقطات شاشة


![TaskFlow Bot](docs/screenshots/task.png)


## 💼 القيمة لصاحب العمل

هذا المشروع يوضح القدرة على:
- بناء تطبيقات غير متزامنة (async/await) بشكل صحيح في بيئة إنتاجية.
- تصميم معمارية طبقات واضحة (Handlers / Database / Middlewares / Config) قابلة للتوسع والصيانة.
- التعامل مع ORM حديث (SQLAlchemy 2.0 Async) بدلاً من استعلامات SQL خام.
- تطبيق أنماط Middleware وFSM لإدارة حالة المحادثة، وهي مهارات منقولة مباشرة لأي إطار عمل خلفي آخر (FastAPI، Django...).
- التعامل مع حالات الخطأ والحدود (Rate Limiting) كما تُبنى الأنظمة الحقيقية، وليس مجرد نموذج تجريبي.

## 📄 الترخيص

MIT License
