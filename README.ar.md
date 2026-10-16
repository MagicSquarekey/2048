# 2048 لعبة عارضة

> لعبة دمج أرقام 2048 بمظهر داكن «الفضاء العميق النيون»، مدعومة بـ Python + Pygame، مبنية لسطح مكتب Windows.

**الإصدار الحالي: [v0.0.1](https://github.com/MagicSquarekey/2048/releases/tag/v0.0.1)** · [简体中文](README.md) · [English](README.en.md) · [日本語](README.ja.md) · [繁體中文](README.zh-TW.md) · [한국어](README.ko.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Español](README.es.md) · [Português](README.pt.md) · [Русский](README.ru.md) · [Italiano](README.it.md) · [Nederlands](README.nl.md) · [Türkçe](README.tr.md) · [Tiếng Việt](README.vi.md) · [ภาษาไทย](README.th.md) · [Bahasa Indonesia](README.id.md) · [हिन्दी](README.hi.md)

---

## 📖 اللغات

| اللغة | المستند |
|---|---|
| 简体中文 | [README.md](README.md) |
| English | [README.en.md](README.en.md) |
| 日本語 | [README.ja.md](README.ja.md) |
| 繁體中文 | [README.zh-TW.md](README.zh-TW.md) |
| 한국어 | [README.ko.md](README.ko.md) |
| Français | [README.fr.md](README.fr.md) |
| Deutsch | [README.de.md](README.de.md) |
| Español | [README.es.md](README.es.md) |
| Português | [README.pt.md](README.pt.md) |
| Русский | [README.ru.md](README.ru.md) |
| Italiano | [README.it.md](README.it.md) |
| Nederlands | [README.nl.md](README.nl.md) |
| Türkçe | [README.tr.md](README.tr.md) |
| Tiếng Việt | [README.vi.md](README.vi.md) |
| ภาษาไทย | [README.th.md](README.th.md) |
| Bahasa Indonesia | [README.id.md](README.id.md) |
| हिन्दी | [README.hi.md](README.hi.md) |
| العربية (الحالي) | [README.ar.md](README.ar.md) |

---

## ✨ أبرز الميزات

- 🎨 **مظهر الفضاء العميق النيون**: خلفية متدرجة بالنيلي مع توهجات عابرة، بطاقات زجاجية مصنفرة، وبلاطات بتدرجات وإضاءة حافة وتألق نيون
- ⚡ **تحكم سلس للغاية**: قائمة إدخال + تمرير مستمر بالضغط المطوّل (~7 نقلات/ثانية) + رسوم متحركة مستقلة عن معدل الإطارات — لا تُفقد أي إدخال في التوليفات السريعة
- 💥 **الحركة والتأثيرات**: انفجارات جسيمات عند الدمج، اهتزاز الشاشة عند الدمج الكبير، قصاصات النصر، انتقال نهاية لعبة متحرك، وتلاشي الصفحات
- 🌍 **واجهة ثنائية اللغة**: التبديل بين الصينية والإنجليزية بلمسة واحدة داخل اللعبة

## 🎮 أنماط اللعب

| النمط | الوصف |
|------|-------|
| **كلاسيكي** | بلا حدود زمنية —aspire إلى أفضل نتيجة لك |
| **سباق الوقت** | حقق النتيجة المستهدفة في 60 ثانية |
| **التحدي** | اصنع بلاطة 128 في 50 نقلة |

**التحكم**: مفاتيح الأسهم / WASD / سحب الفأرة · `ESC` للإيقاف المؤقت

## 🧰 التعزيزات

- **تراجع**: التراجع عن النقلة الأخيرة (3 لكل لعبة)
- **تنظيف**: إزالة أصغر بلاطة (1 لكل لعبة)
- **إحياء**: بعد انتهاء اللعبة، أزل أصغر بلاطتين وتابع اللعب

## 🏆 ميزات أخرى

- نظام الإنجازات (6 إنجازات لفتحها)
- تتبع أفضل نتيجة / إجمالي الألعاب
- شارة رقم قياسي جديد + رسوم متحركة لتجميع النتيجة في صفحة النتائج
- مفاتيح المؤثرات الصوتية وموسيقى الخلفية

---

## 🖥️ متطلبات النظام

- Windows 10 / 11
- Python 3.10+
- Pygame 2.6.1

## 🚀 البدء السريع

### 1. تثبيت التبعيات

```bash
pip install -r requirements.txt
```

### 2. تشغيل اللعبة

```bash
python src/main.py
```

### 3. التحزيم كملف EXE

```bash
# بناء بنقرة واحدة (موصى به)
python scripts/build_auto.py

# بناء تفاعلي
python scripts/build.py
```

بعد البناء، يكون الملف التنفيذي في `dist/2048/2048.exe` — انقر نقرة مزدوجة للعب، دون حاجة إلى Python أو أي تبعيات. انظر [scripts/README.md](scripts/README.md) للتفاصيل.

---

## 📁 بنية المشروع

```
2048/
├── src/                    # الشيفرة المصدرية
│   ├── main.py             # نقطة الدخول
│   ├── config.py           # الإعداد العام (المظهر / الحركة / الإدخال)
│   ├── i18n.py             # التوطين (الصينية والإنجليزية)
│   ├── utils.py            # مساعدات الرسم، ذاكرات التخزين، منحنيات الحركة
│   ├── models/             # نماذج البيانات (اللوحة / الحالة / الحفظ / الإنجازات)
│   └── views/              # طبقة العرض
│       ├── ui_components.py  # مكونات الواجهة (أزرار / بطاقات النقاط / مفاتيح / تنبيهات)
│       ├── board_view.py     # عرض اللوحة والحركة
│       ├── effects.py        # نظام الجسيمات واهتزاز الشاشة
│       ├── sound_manager.py  # إدارة الصوت
│       └── pages/            # الصفحات (القائمة / اللعبة / النتائج / الإعدادات / الإنجازات / الإيقاف / الدخول)
├── tests/                  # الاختبارات (359 اختبار وحدة + محاكاة مستخدم E2E)
├── scripts/                # سكربتات البناء والتغليف
├── docs/                   # التوثيق
├── private/                # ملفات خاصة
├── dist/                   # مخرجات البناء (.gitignore)
├── build/                  # ملفات البناء المؤقتة (.gitignore)
└── requirements.txt        # قائمة التبعيات
```

## 🔧 دليل التطوير

### تشغيل الاختبارات

```bash
# جميع اختبارات الوحدة
python -m pytest tests/

# محاكاة المستخدم من البداية للنهاية (E2E)
python tests/e2e_user_simulation.py

# التقاط لقطات شاشة الواجهة
python tests/capture_ui_review.py
```

التغطية: خوارزمية اللوحة، حالة اللعبة، دورات الحياة الكاملة للأنماط الثلاثة، التعزيزات، الإيقاف/إعادة التشغيل، توليفات قائمة الإدخال، اختبارات الإجهاد، وميزانية أداء 60FPS.

### معايير الشيفرة

- **تسمية الملفات / الدوال**: `lower_snake_case` · **تسمية الأصناف**: `PascalCase` · **الإزاحة**: 4 مسافات · **عرض السطر**: 120 حرفًا كحد أقصى
- **إيداعات Git**: `<type>(<scope>): <subject>` مع `feat / fix / docs / style / refactor / test / chore`

---

## 📜 الترخيص

[MIT License](LICENSE) © 2026 MagicSquarekey

## 🤝 المساهمة

الطلبات (Issues) وطلبات السحب (Pull Requests) مرحب بها!

## 📞 التواصل

لديك أسئلة؟ عبر [GitHub Issues](https://github.com/MagicSquarekey/2048/issues).
