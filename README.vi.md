# 2048 Trò chơi giải trí

> Trò chơi hợp số 2048 với chủ đề tối «deep-space neon», chạy bằng Python + Pygame, dành cho máy tính để bàn Windows.

**Phiên bản hiện tại: [v0.0.1](https://github.com/MagicSquarekey/2048/releases/tag/v0.0.1)** · [简体中文](README.md) · [English](README.en.md) · [日本語](README.ja.md) · [繁體中文](README.zh-TW.md) · [한국어](README.ko.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Español](README.es.md) · [Português](README.pt.md) · [Русский](README.ru.md) · [Italiano](README.it.md) · [Nederlands](README.nl.md) · [Türkçe](README.tr.md) · [ภาษาไทย](README.th.md) · [Bahasa Indonesia](README.id.md) · [हिन्दी](README.hi.md) · [العربية](README.ar.md)

---

## 📖 Ngôn ngữ

| Ngôn ngữ | Tài liệu |
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
| Tiếng Việt (hiện tại) | [README.vi.md](README.vi.md) |
| ภาษาไทย | [README.th.md](README.th.md) |
| Bahasa Indonesia | [README.id.md](README.id.md) |
| हिन्दी | [README.hi.md](README.hi.md) |
| العربية | [README.ar.md](README.ar.md) |

---

## ✨ Điểm nổi bật

- 🎨 **Chủ đề deep-space neon**: nền gradient chàm với các vệt sáng trôi dịu, thẻ kính mờ và các ô với gradient, viền sáng và hào quang neon
- ⚡ **Điều khiển mượt mà**: hàng đợi đầu vào + trượt liên tục khi giữ (~7 nước/giây) + hoạt ảnh độc lập tốc độ khung hình — combo nhanh không mất đầu vào
- 💥 **Chuyển động & hiệu ứng**: bùng hạt khi hợp nhất, rung màn hình khi hợp nhất lớn, kim tuyến chiến thắng, chuyển cảnh kết thúc có hoạt ảnh, mờ dần trang
- 🌍 **Giao diện song ngữ**: chuyển đổi tiếng Trung / tiếng Anh trong game chỉ với một chạm

## 🎮 Chế độ chơi

| Chế độ | Mô tả |
|--------|-------|
| **Cổ điển** | Không giới hạn thời gian — phá kỷ lục của bạn |
| **Tốc độ** | Đạt điểm mục tiêu trong 60 giây |
| **Thử thách** | Tạo ô 128 trong 50 nước đi |

**Điều khiển**: phím mũi tên / WASD / vuốt chuột · `ESC` để tạm dừng

## 🧰 Vật phẩm

- **Hoàn tác**: quay lại nước đi trước (3 mỗi ván)
- **Xóa**: bỏ ô nhỏ nhất (1 mỗi ván)
- **Hồi sinh**: sau khi game over, xóa hai ô nhỏ nhất và tiếp tục

## 🏆 Tính năng khác

- Hệ thống thành tích (6 thành tích cần mở)
- Theo dõi điểm cao nhất / tổng số ván
- Huy hiệu kỷ lục mới + hoạt ảnh đếm điểm ở trang kết quả
- Công tắc âm thanh và nhạc nền

---

## 🖥️ Yêu cầu hệ thống

- Windows 10 / 11
- Python 3.10+
- Pygame 2.6.1

## 🚀 Bắt đầu nhanh

### 1. Cài đặt phụ thuộc

```bash
pip install -r requirements.txt
```

### 2. Chạy game

```bash
python src/main.py
```

### 3. Đóng gói thành EXE

```bash
# Build một cú nhấp (khuyên dùng)
python scripts/build_auto.py

# Build tương tác
python scripts/build.py
```

Sau khi build, tệp thực thi nằm ở `dist/2048/2048.exe` — nhấp đúp để chơi, không cần Python hay phụ thuộc. Xem [scripts/README.md](scripts/README.md) để biết chi tiết.

---

## 📁 Cấu trúc dự án

```
2048/
├── src/                    # Mã nguồn
│   ├── main.py             # Điểm vào
│   ├── config.py           # Cấu hình toàn cục (chủ đề / hoạt ảnh / đầu vào)
│   ├── i18n.py             # Bản địa hóa (tiếng Trung & tiếng Anh)
│   ├── utils.py            # Hàm vẽ, bộ đệm, đường cong hoạt ảnh
│   ├── models/             # Mô hình dữ liệu (bàn / trạng thái / lưu / thành tích)
│   └── views/              # Lớp giao diện
│       ├── ui_components.py  # Thành phần UI (nút / thẻ điểm / công tắc / cảnh báo)
│       ├── board_view.py     # Kết xuất & hoạt ảnh bàn cờ
│       ├── effects.py        # Hệ hạt và rung màn hình
│       ├── sound_manager.py  # Quản lý âm thanh
│       └── pages/            # Các trang (menu / game / kết quả / cài đặt / thành tích / tạm dừng / đăng nhập)
├── tests/                  # Kiểm thử (359 test đơn vị + mô phỏng người dùng E2E)
├── scripts/                # Script build & đóng gói
├── docs/                   # Tài liệu
├── private/                # Tệp riêng tư
├── dist/                   # Đầu ra build (.gitignore)
├── build/                  # Tệp tạm build (.gitignore)
└── requirements.txt        # Danh sách phụ thuộc
```

## 🔧 Hướng dẫn phát triển

### Chạy kiểm thử

```bash
# Toàn bộ test đơn vị
python -m pytest tests/

# Mô phỏng người dùng đầu-cuối (E2E)
python tests/e2e_user_simulation.py

# Chụp ảnh màn hình UI
python tests/capture_ui_review.py
```

Phạm vi: thuật toán bàn cờ, trạng thái game, vòng đời đầy đủ của ba chế độ, vật phẩm, tạm dừng / chơi lại, combo hàng đợi đầu vào, kiểm thử tải và ngân sách hiệu năng 60FPS.

### Chuẩn mã

- **Đặt tên tệp / hàm**: `lower_snake_case` · **Đặt tên lớp**: `PascalCase` · **Thụt lề**: 4 dấu cách · **Độ rộng dòng**: tối đa 120 ký tự
- **Commit Git**: `<type>(<scope>): <subject>` với `feat / fix / docs / style / refactor / test / chore`

---

## 📜 Giấy phép

[MIT License](LICENSE) © 2026 MagicSquarekey

## 🤝 Đóng góp

Issue và Pull Request đều được chào đón!

## 📞 Liên hệ

Có thắc mắc? Qua [GitHub Issues](https://github.com/MagicSquarekey/2048/issues).
