# 2048 कैज़ुअल गेम

> एक 2048 संख्या विलय खेल, «डीप-स्पेस नियॉन» डार्क थीम में, Python + Pygame से संचालित, Windows डेस्कटॉप के लिए निर्मित।

**वर्तमान संस्करण: [v0.0.1](https://github.com/MagicSquarekey/2048/releases/tag/v0.0.1)** · [简体中文](README.md) · [English](README.en.md) · [日本語](README.ja.md) · [繁體中文](README.zh-TW.md) · [한국어](README.ko.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Español](README.es.md) · [Português](README.pt.md) · [Русский](README.ru.md) · [Italiano](README.it.md) · [Nederlands](README.nl.md) · [Türkçe](README.tr.md) · [Tiếng Việt](README.vi.md) · [ภาษาไทย](README.th.md) · [Bahasa Indonesia](README.id.md) · [العربية](README.ar.md)

---

## 📖 भाषाएँ

| भाषा | दस्तावेज़ |
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
| हिन्दी (वर्तमान) | [README.hi.md](README.hi.md) |
| العربية | [README.ar.md](README.ar.md) |

---

## ✨ मुख्य विशेषताएँ

- 🎨 **डीप-स्पेस नियॉन थीम**: इंडिगो ग्रेडिएंट पृष्ठभूमि जिसमें तैरती चमक, कांच जैसे कार्ड, और ग्रेडिएंट, रिम लाइट व नियॉन चमक वाले टाइल
- ⚡ **बिल्कुल सहज नियंत्रण**: इनपुट कतार + दबाकर रखने पर निरंतर स्लाइड (~7 चाल/सेकंड) + फ्रेमरेट-स्वतंत्र एनिमेशन — तेज़ कॉम्बो इनपुट नहीं खोते
- 💥 **मोशन और प्रभाव**: विलय पर कण विस्फोट, बड़े विलय पर स्क्रीन कंपन, विजय कन्फेटी, एनिमेटेड गेम-ओवर संक्रमण, पेज फेड
- 🌍 **द्विभाषी UI**: खेल में एक टैप से चीनी और अंग्रेज़ी के बीच स्विच करें

## 🎮 खेल मोड

| मोड | विवरण |
|------|-------|
| **क्लासिक** | कोई समय सीमा नहीं — अपने सर्वश्रेष्ठ स्कोर का पीछा करें |
| **समय प्रतियोगिता** | 60 सेकंड में लक्ष्य स्कोर प्राप्त करें |
| **चुनौती** | 50 चालों में 128 टाइल बनाएँ |

**नियंत्रण**: तीर कुंजियाँ / WASD / माउस स्वाइप · `ESC` से विराम

## 🧰 पावर-अप

- **अनडू**: अंतिम चाल पलटें (प्रति खेल 3)
- **क्लियर**: सबसे छोटा टाइल हटाएँ (प्रति खेल 1)
- **रिवाइव**: गेम ओवर के बाद दो सबसे छोटे टाइल हटाकर जारी रखें

## 🏆 अन्य सुविधाएँ

- उपलब्धि प्रणाली (6 उपलब्धियाँ अनलॉक करने हेतु)
- सर्वश्रेष्ठ स्कोर / कुल खेल ट्रैकिंग
- परिणाम पृष्ठ पर नया रिकॉर्ड बैज + स्कोर रोल-अप एनिमेशन
- ध्वनि प्रभाव और पृष्ठभूमि संगीत टॉगल

---

## 🖥️ सिस्टम आवश्यकताएँ

- Windows 10 / 11
- Python 3.10+
- Pygame 2.6.1

## 🚀 त्वरित प्रारंभ

### 1. निर्भरताएँ स्थापित करें

```bash
pip install -r requirements.txt
```

### 2. खेल चलाएँ

```bash
python src/main.py
```

### 3. EXE के रूप में पैकेज करें

```bash
# एक-क्लिक बिल्ड (अनुशंसित)
python scripts/build_auto.py

# इंटरैक्टिव बिल्ड
python scripts/build.py
```

बिल्ड पूर्ण होने पर निष्पादनयोग्य फ़ाइल `dist/2048/2048.exe` में होती है — बिना Python या निर्भरताओं के डबल-क्लिक कर खेलें। विवरण के लिए [scripts/README.md](scripts/README.md) देखें।

---

## 📁 परियोजना संरचना

```
2048/
├── src/                    # स्रोत कोड
│   ├── main.py             # प्रवेश बिंदु
│   ├── config.py           # वैश्विक कॉन्फ़िग (थीम / एनिमेशन / इनपुट)
│   ├── i18n.py             # स्थानीयकरण (चीनी और अंग्रेज़ी)
│   ├── utils.py            # आरेखन सहायक, कैश, एनिमेशन वक्र
│   ├── models/             # डेटा मॉडल (बोर्ड / स्थिति / सेव / उपलब्धियाँ)
│   └── views/              # दृश्य परत
│       ├── ui_components.py  # UI घटक (बटन / स्कोर कार्ड / स्विच / अलर्ट)
│       ├── board_view.py     # बोर्ड रेंडरिंग और एनिमेशन
│       ├── effects.py        # कण प्रणाली और स्क्रीन कंपन
│       ├── sound_manager.py  # ध्वनि प्रबंधन
│       └── pages/            # पृष्ठ (मेनू / खेल / परिणाम / सेटिंग्स / उपलब्धियाँ / विराम / लॉगिन)
├── tests/                  # परीक्षण (359 यूनिट परीक्षण + E2E उपयोगकर्ता सिमुलेशन)
├── scripts/                # बिल्ड और पैकेजिंग स्क्रिप्ट
├── docs/                   # दस्तावेज़
├── private/                # निजी फ़ाइलें
├── dist/                   # बिल्ड आउटपुट (.gitignore)
├── build/                  # बिल्ड अस्थायी फ़ाइलें (.gitignore)
└── requirements.txt        # निर्भरता सूची
```

## 🔧 विकास गाइड

### परीक्षण चलाएँ

```bash
# सभी यूनिट परीक्षण
python -m pytest tests/

# एंड-टू-एंड उपयोगकर्ता सिमुलेशन
python tests/e2e_user_simulation.py

# UI स्क्रीनशॉट कैप्चर करें
python tests/capture_ui_review.py
```

कवरेज: बोर्ड एल्गोरिदम, खेल स्थिति, तीनों मोड के पूर्ण जीवनचक्र, पावर-अप, विराम/पुनरारंभ, इनपुट कतार कॉम्बो, तनाव परीक्षण और 60FPS प्रदर्शन बजट।

### कोड मानक

- **फ़ाइल / फ़ंक्शन नामकरण**: `lower_snake_case` · **क्लास नामकरण**: `PascalCase` · **इंडेंटेशन**: 4 स्पेस · **लाइन चौड़ाई**: अधिकतम 120 वर्ण
- **Git कमिट**: `feat / fix / docs / style / refactor / test / chore` के साथ `<type>(<scope>): <subject>`

---

## 📜 लाइसेंस

[MIT License](LICENSE) © 2026 MagicSquarekey

## 🤝 योगदान

Issue और Pull Request का स्वागत है!

## 📞 संपर्क

प्रश्न हैं? [GitHub Issues](https://github.com/MagicSquarekey/2048/issues) के माध्यम से।
