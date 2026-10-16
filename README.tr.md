# 2048 Gündelik Oyun

> Python + Pygame ile güçlendirilen, Windows masaüstü için geliştirilmiş, «derin uzay neon» koyu temalı 2048 sayı birleştirme oyunu.

**Mevcut sürüm: [v0.0.1](https://github.com/MagicSquarekey/2048/releases/tag/v0.0.1)** · [简体中文](README.md) · [English](README.en.md) · [日本語](README.ja.md) · [繁體中文](README.zh-TW.md) · [한국어](README.ko.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Español](README.es.md) · [Português](README.pt.md) · [Русский](README.ru.md) · [Italiano](README.it.md) · [Nederlands](README.nl.md) · [Tiếng Việt](README.vi.md) · [ภาษาไทย](README.th.md) · [Bahasa Indonesia](README.id.md) · [हिन्दी](README.hi.md) · [العربية](README.ar.md)

---

## 📖 Diller

| Dil | Belge |
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
| Türkçe (mevcut) | [README.tr.md](README.tr.md) |
| Tiếng Việt | [README.vi.md](README.vi.md) |
| ภาษาไทย | [README.th.md](README.th.md) |
| Bahasa Indonesia | [README.id.md](README.id.md) |
| हिन्दी | [README.hi.md](README.hi.md) |
| العربية | [README.ar.md](README.ar.md) |

---

## ✨ Öne çıkan özellikler

- 🎨 **Derin uzay neon teması**: yavaşça süzülen parıltılarla indigo gradyan arka plan, buzlu cam kartlar ve gradyanlı, kenar ışıklı, neon parlamalı karo
- ⚡ **Yumuşak kontroller**: giriş kuyruğu + basılı tutarak sürekli kaydırma (~saniyede 7 hamle) + kare hızından bağımsız animasyonlar — hızlı kombolar giriş kaybetmez
- 💥 **Hareket & efektler**: birleştirmede parçacık patlamaları, büyük birleştirmelerde ekran sarsıntısı, zafer konfetisi, animasyonlu oyun sonu geçişi, sayfa solmaları
- 🌍 **İki dilli arayüz**: oyun içinde tek dokunuşla Çince ve İngilizce arasında geçiş

## 🎮 Oyun modları

| Mod | Açıklama |
|-----|----------|
| **Klasik** | Zaman sınırı yok — en iyi puanının peşine git |
| **Süre yarışı** | 60 saniye içinde hedef puana ulaş |
| **Meydan okuma** | 50 hamlede 128 karosunu oluştur |

**Kontroller**: yön tuşları / WASD / fare kaydırma · `ESC` ile duraklat

## 🧰 Güçlendiriciler

- **Geri al**: son hamleyi geri al (oyun başına 3)
- **Temizle**: en küçük karoyu kaldır (oyun başına 1)
- **Dirilt**: oyun bittikten sonra iki en küçük karoyu kaldırıp devam et

## 🏆 Diğer özellikler

- Başarım sistemi (kilidi açılabilir 6 başarım)
- En iyi puan / toplam oyun takibi
- Sonuç sayfasında yeni rekor rozeti + puan yuvarlama animasyonu
- Ses efektleri ve arka plan müziği anahtarları

---

## 🖥️ Sistem gereksinimleri

- Windows 10 / 11
- Python 3.10+
- Pygame 2.6.1

## 🚀 Hızlı başlangıç

### 1. Bağımlılıkları yükle

```bash
pip install -r requirements.txt
```

### 2. Oyunu çalıştır

```bash
python src/main.py
```

### 3. EXE olarak paketle

```bash
# Tek tıkla derleme (önerilen)
python scripts/build_auto.py

# Etkileşimli derleme
python scripts/build.py
```

Derleme tamamlandığında çalıştırılabilir dosya `dist/2048/2048.exe` konumunda olur — Python veya bağımlılık gerektirmeden çift tıklayıp oynayın. Ayrıntılar için [scripts/README.md](scripts/README.md) dosyasına bakın.

---

## 📁 Proje yapısı

```
2048/
├── src/                    # Kaynak kod
│   ├── main.py             # Giriş noktası
│   ├── config.py           # Genel yapılandırma (tema / animasyon / giriş)
│   ├── i18n.py             # Yerelleştirme (Çince ve İngilizce)
│   ├── utils.py            # Çizim yardımcıları, önbellekler, animasyon eğrileri
│   ├── models/             # Veri modelleri (tahta / durum / kayıt / başarımlar)
│   └── views/              # Görünüm katmanı
│       ├── ui_components.py  # UI bileşenleri (düğmeler / puan kartları / anahtarlar / uyarılar)
│       ├── board_view.py     # Tahta görselleştirme ve animasyon
│       ├── effects.py        # Parçacık sistemi ve ekran sarsıntısı
│       ├── sound_manager.py  # Ses yönetimi
│       └── pages/            # Sayfalar (menü / oyun / sonuç / ayarlar / başarımlar / duraklat / giriş)
├── tests/                  # Testler (359 birim testi + E2E kullanıcı simülasyonu)
├── scripts/                # Derleme ve paketleme betikleri
├── docs/                   # Belgeler
├── private/                # Özel dosyalar
├── dist/                   # Derleme çıktısı (.gitignore)
├── build/                  # Derleme geçici dosyaları (.gitignore)
└── requirements.txt        # Bağımlılık listesi
```

## 🔧 Geliştirme kılavuzu

### Testleri çalıştır

```bash
# Tüm birim testleri
python -m pytest tests/

# Uçtan uca kullanıcı simülasyonu (E2E)
python tests/e2e_user_simulation.py

# UI ekran görüntülerini yakala
python tests/capture_ui_review.py
```

Kapsam: tahta algoritması, oyun durumu, üç modun tam yaşam döngüleri, güçlendiriciler, duraklat/yeniden başlat, giriş kuyruğu komboları, stres testleri ve 60FPS performans bütçesi.

### Kod standartları

- **Dosya / fonksiyon adlandırma**: `lower_snake_case` · **Sınıf adlandırma**: `PascalCase` · **Girinti**: 4 boşluk · **Satır genişliği**: maks. 120 karakter
- **Git commit'leri**: `feat / fix / docs / style / refactor / test / chore` ile `<type>(<scope>): <subject>`

---

## 📜 Lisans

[MIT License](LICENSE) © 2026 MagicSquarekey

## 🤝 Katkıda bulunma

Issue ve Pull Request'ler memnuniyetle karşılanır!

## 📞 İletişim

Sorularınız mı var? [GitHub Issues](https://github.com/MagicSquarekey/2048/issues) üzerinden ulaşın.
