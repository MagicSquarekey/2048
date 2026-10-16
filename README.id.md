# 2048 Game Kasual

> Game penggabungan angka 2048 dengan tema gelap «deep-space neon», ditenagai oleh Python + Pygame, dibuat untuk desktop Windows.

**Versi saat ini: [v0.0.1](https://github.com/MagicSquarekey/2048/releases/tag/v0.0.1)** · [简体中文](README.md) · [English](README.en.md) · [日本語](README.ja.md) · [繁體中文](README.zh-TW.md) · [한국어](README.ko.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Español](README.es.md) · [Português](README.pt.md) · [Русский](README.ru.md) · [Italiano](README.it.md) · [Nederlands](README.nl.md) · [Türkçe](README.tr.md) · [Tiếng Việt](README.vi.md) · [ภาษาไทย](README.th.md) · [हिन्दी](README.hi.md) · [العربية](README.ar.md)

---

## 📖 Bahasa

| Bahasa | Dokumen |
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
| Bahasa Indonesia (saat ini) | [README.id.md](README.id.md) |
| हिन्दी | [README.hi.md](README.hi.md) |
| العربية | [README.ar.md](README.ar.md) |

---

## ✨ Sorotan

- 🎨 **Tema deep-space neon**: latar gradien indigo dengan cahaya melayang, kartu kaca buram, dan ubin dengan gradien, cahaya tepi, dan sinar neon
- ⚡ **Kendali sangat mulus**: antrian input + geser berkelanjutan dengan menahan (~7 langkah/detik) + animasi independen framerate — combo cepat tidak kehilangan input
- 💥 **Gerak & efek**: ledakan partikel saat penggabungan, getaran layar pada penggabungan besar, konfeti kemenangan, transisi akhir beranimasi, pudar halaman
- 🌍 **Antarmuka dwibahasa**: beralih antara Mandarin dan Inggris dalam game dengan satu sentuhan

## 🎮 Mode permainan

| Mode | Deskripsi |
|------|-----------|
| **Klasik** | Tanpa batas waktu — kejar skor terbaikmu |
| **Lawan waktu** | Capai skor target dalam 60 detik |
| **Tantangan** | Capai ubin 128 dalam 50 langkah |

**Kontrol**: tombol panah / WASD / geser mouse · `ESC` untuk jeda

## 🧰 Power-up

- **Batalkan**: kembalikan langkah terakhir (3 per permainan)
- **Bersihkan**: hapus ubin terkecil (1 per permainan)
- **Hidupkan kembali**: setelah game over, hapus dua ubin terkecil dan lanjutkan

## 🏆 Fitur lain

- Sistem pencapaian (6 pencapaian untuk dibuka)
- Pelacakan skor terbaik / total permainan
- Lencana rekor baru + animasi penggulungan skor di halaman hasil
- Sakelar efek suara dan musik latar

---

## 🖥️ Persyaratan sistem

- Windows 10 / 11
- Python 3.10+
- Pygame 2.6.1

## 🚀 Mulai cepat

### 1. Instal dependensi

```bash
pip install -r requirements.txt
```

### 2. Jalankan game

```bash
python src/main.py
```

### 3. Paketkan sebagai EXE

```bash
# Build satu klik (disarankan)
python scripts/build_auto.py

# Build interaktif
python scripts/build.py
```

Berkas eksekusi berada di `dist/2048/2048.exe` — klik dua kali untuk bermain, tanpa Python atau dependensi. Lihat [scripts/README.md](scripts/README.md) untuk detail.

---

## 📁 Struktur proyek

```
2048/
├── src/                    # Kode sumber
│   ├── main.py             # Titik masuk
│   ├── config.py           # Konfig global (tema / animasi / input)
│   ├── i18n.py             # Lokalisasi (Mandarin & Inggris)
│   ├── utils.py            # Pembantu gambar, cache, kurva animasi
│   ├── models/             # Model data (papan / status / simpan / pencapaian)
│   └── views/              # Lapisan tampilan
│       ├── ui_components.py  # Komponen UI (tombol / kartu skor / sakelar / peringatan)
│       ├── board_view.py     # Render & animasi papan
│       ├── effects.py        # Sistem partikel & getaran layar
│       ├── sound_manager.py  # Manajemen suara
│       └── pages/            # Halaman (menu / game / hasil / pengaturan / pencapaian / jeda / login)
├── tests/                  # Tes (359 tes unit + simulasi pengguna E2E)
├── scripts/                # Skrip build & paket
├── docs/                   # Dokumentasi
├── private/                # Berkas pribadi
├── dist/                   # Keluaran build (.gitignore)
├── build/                  # Berkas sementara build (.gitignore)
└── requirements.txt        # Daftar dependensi
```

## 🔧 Panduan pengembangan

### Jalankan tes

```bash
# Semua tes unit
python -m pytest tests/

# Simulasi pengguna end-to-end (E2E)
python tests/e2e_user_simulation.py

# Tangkap tangkapan layar UI
python tests/capture_ui_review.py
```

Cakupan: algoritma papan, status game, siklus hidup penuh ketiga mode, power-up, jeda/mulai ulang, combo antrian input, tes stres, dan anggaran performa 60FPS.

### Standar kode

- **Penamaan berkas / fungsi**: `lower_snake_case` · **Penamaan kelas**: `PascalCase` · **Indentasi**: 4 spasi · **Lebar baris**: maks. 120 karakter
- **Commit Git**: `<type>(<scope>): <subject>` dengan `feat / fix / docs / style / refactor / test / chore`

---

## 📜 Lisensi

[MIT License](LICENSE) © 2026 MagicSquarekey

## 🤝 Berkontribusi

Issue dan Pull Request diterima dengan senang hati!

## 📞 Kontak

Ada pertanyaan? Melalui [GitHub Issues](https://github.com/MagicSquarekey/2048/issues).
