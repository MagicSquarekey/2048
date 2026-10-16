# 2048 เกม casual

> เกมรวมตัวเลข 2048 ด้วยธีมมืด «ดิปสเปซ นีออน』 ขับเคลื่อนด้วย Python + Pygame สร้างสำหรับเดสก์ท็อป Windows

**เวอร์ชันปัจจุบัน: [v0.0.1](https://github.com/MagicSquarekey/2048/releases/tag/v0.0.1)** · [简体中文](README.md) · [English](README.en.md) · [日本語](README.ja.md) · [繁體中文](README.zh-TW.md) · [한국어](README.ko.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Español](README.es.md) · [Português](README.pt.md) · [Русский](README.ru.md) · [Italiano](README.it.md) · [Nederlands](README.nl.md) · [Türkçe](README.tr.md) · [Tiếng Việt](README.vi.md) · [Bahasa Indonesia](README.id.md) · [हिन्दी](README.hi.md) · [العربية](README.ar.md)

---

## 📖 ภาษา

| ภาษา | เอกสาร |
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
| ภาษาไทย (ปัจจุบัน) | [README.th.md](README.th.md) |
| Bahasa Indonesia | [README.id.md](README.id.md) |
| हिन्दी | [README.hi.md](README.hi.md) |
| العربية | [README.ar.md](README.ar.md) |

---

## ✨ ไฮไลต์

- 🎨 **ธีมดิปสเปซ นีออน**: พื้นหลังไล่เฉดอินดิโก้พร้อมเรืองแสงไหลช้า การ์ดกระจกฝ้า และไทล์ด้วยไล่เฉด แสงขอบ และเรืองแสงนีออน
- ⚡ **การควบคุมลื่นไหล**: คิวอินพุต + เลื่อนต่อเนื่องด้วยการกดค้าง (~7 ตา/วินาที) + อนิเมชันอิสระจากเฟมเรต — คอมโบเร็วไม่สูญเสียอินพุต
- 💥 **การเคลื่อนไหว & เอฟเฟกต์**: การระเบิดอนุภาคเมื่อรวม ภาพสั่นจอเมื่อรวมตัวใหญ่ คอนเฟตตี้ชัยชนะ ทรานซิชันจบเกมพร้อมอนิเมชัน เฟดหน้า
- 🌍 **UI สองภาษา**: สลับจีน / English ในเกมด้วยการแตะเดียว

## 🎮 โหมดเกม

| โหมด | คำอธิบาย |
|------|---------|
| **คลาสสิก** | ไม่จำกัดเวลา — ทำให้คะแนนสูงสุดของคุณ |
| **แข่งเวลา** | ทำคะแนนเป้าหมายใน 60 วินาที |
| **ท้าทาย** | สร้างไทล์ 128 ใน 50 ตา |

**การควบคุม**: ปุ่มลูกศร / WASD / ปัดเมาส์ · `ESC` หยุดชั่วคราว

## 🧰 ไอเทม

- **ย้อนกลับ**: ย้อนตาก่อนหน้า (3 ต่อเกม)
- **ล้าง**: เอาไทล์ที่เล็กที่สุดออก (1 ต่อเกม)
- **ชุบชีวิต**: หลังจบเกม เอาไทล์เล็กสุดสองอันออกแล้วเล่นต่อ

## 🏆 ฟีเจอร์อื่น

- ระบบความสำเร็จ (6 รายการให้ปลดล็อก)
- ติดตามคะแนนสูงสุด / จำนวนเกมทั้งหมด
- ตราโฉมสถิติใหม่ + อนิเมชันนับคะแนนในหน้าผลลัพธ์
- สวิตช์เสียงเอฟเฟกต์และเพลงประกอบ

---

## 🖥️ ความต้องการระบบ

- Windows 10 / 11
- Python 3.10+
- Pygame 2.6.1

## 🚀 เริ่มอย่างรวดเร็ว

### 1. ติดตั้งการอ้างอิง

```bash
pip install -r requirements.txt
```

### 2. รันเกม

```bash
python src/main.py
```

### 3. แพ็กเกจเป็น EXE

```bash
# บิลด์คลิกเดียว (แนะนำ)
python scripts/build_auto.py

# บิลด์แบบอินเทอร์แอกทีฟ
python scripts/build.py
```

ไฟล์ปฏิบัติการจะอยู่ที่ `dist/2048/2048.exe` — ดับเบิลคลิกเพื่อเล่นได้เลย ไม่ต้องติดตั้ง Python หรือการอ้างอิง ดูรายละเอียดที่ [scripts/README.md](scripts/README.md)

---

## 📁 โครงสร้างโปรเจกต์

```
2048/
├── src/                    # ซอร์สโค้ด
│   ├── main.py             # จุดเริ่มต้น
│   ├── config.py           # คอนฟิกส่วนกลาง (ธีม / อนิเมชัน / อินพุต)
│   ├── i18n.py             # การแปลภาษา (จีน & อังกฤษ)
│   ├── utils.py            # ตัวช่วยวาด แคช โค้งอนิเมชัน
│   ├── models/             # โมเดลข้อมูล (บอร์ด / สถานะ / เซฟ / ความสำเร็จ)
│   └── views/              # ชั้นมุมมอง
│       ├── ui_components.py  # คอมโพเนนต์ UI (ปุ่ม / การ์ดคะแนน / สวิตช์ / การแจ้งเตือน)
│       ├── board_view.py     # เรนเดอร์และอนิเมชันบอร์ด
│       ├── effects.py        # ระบบอนุภาคและการสั่นจอ
│       ├── sound_manager.py  # การจัดการเสียง
│       └── pages/            # หน้า (เมนู / เกม / ผลลัพธ์ / ตั้งค่า / ความสำเร็จ / หยุดชั่วคราว / ล็อกอิน)
├── tests/                  # ทดสอบ (359 ยูนิตเทสต์ + จำลองผู้ใช้ E2E)
├── scripts/                # สคริปต์บิลด์และแพ็กเกจ
├── docs/                   # เอกสาร
├── private/                # ไฟล์ส่วนตัว
├── dist/                   # เอาต์พุตบิลด์ (.gitignore)
├── build/                  # ไฟล์ชั่วคราวบิลด์ (.gitignore)
└── requirements.txt        # รายการการอ้างอิง
```

## 🔧 คู่มือพัฒนา

### รันเทสต์

```bash
# ยูนิตเทสต์ทั้งหมด
python -m pytest tests/

# จำลองผู้ใช้แบบ end-to-end (E2E)
python tests/e2e_user_simulation.py

# จับภาพหน้าจอ UI
python tests/capture_ui_review.py
```

ครอบคลุม: อัลกอริทึมบอร์ด สถานะเกม วงจรชีวิตครบของสามโหมด ไอเทม หยุดชั่วคราว / เริ่มใหม่ คอมโบคิวอินพุต เทสต์เครียด และงบประสิทธิภาพ 60FPS

### มาตรฐานโค้ด

- **ชื่อไฟล์ / ฟังก์ชัน**: `lower_snake_case` · **ชื่อคลาส**: `PascalCase` · **การเยื้อง**: 4 ช่องว่าง · **ความกว้างบรรทัด**: สูงสุด 120 ตัวอักษร
- **คอมมิต Git**: `<type>(<scope>): <subject>` ด้วย `feat / fix / docs / style / refactor / test / chore`

---

## 📜 ใบอนุญาต

[MIT License](LICENSE) © 2026 MagicSquarekey

## 🤝 มีส่วนร่วม

Issue และ Pull Request ยินดีต้อนรับ!

## 📞 ติดต่อ

มีคำถาม? ผ่าน [GitHub Issues](https://github.com/MagicSquarekey/2048/issues)
