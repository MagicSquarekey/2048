# 2048 休閒遊戲

> 一款採用「深空霓虹」暗色主題打造的 2048 數字合成遊戲，以 Python + Pygame 驅動，專為 Windows 桌面而生。

**目前版本: [v0.0.1](https://github.com/MagicSquarekey/2048/releases/tag/v0.0.1)** · [简体中文](README.md) · [English](README.en.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Español](README.es.md) · [Português](README.pt.md) · [Русский](README.ru.md) · [Italiano](README.it.md) · [Nederlands](README.nl.md) · [Türkçe](README.tr.md) · [Tiếng Việt](README.vi.md) · [ภาษาไทย](README.th.md) · [Bahasa Indonesia](README.id.md) · [हिन्दी](README.hi.md) · [العربية](README.ar.md)

---

## 📖 語言

| 語言 | 文件 |
|---|---|
| 简体中文 | [README.md](README.md) |
| English | [README.en.md](README.en.md) |
| 日本語 | [README.ja.md](README.ja.md) |
| 繁體中文 (目前) | [README.zh-TW.md](README.zh-TW.md) |
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
| العربية | [README.ar.md](README.ar.md) |

---

## ✨ 亮點特性

- 🎨 **深空霓虹主題**：深靛藍漸層背景 + 動態漂移光斑 + 玻璃擬態卡片；方塊自帶漸層、輪輞光與頂部光澤，128 以上方塊帶霓虹輝光
- ⚡ **絲滑操作**：輸入佇列 + 按住連滑（約每秒 7 步）+ 帧率無關動畫，快速連擊不丟步
- 💥 **動態特效**：合併粒子爆發、大方塊合成震屏、勝利彩帶、結束過場動畫、頁面淡入淡出
- 🌍 **雙語介面**：遊戲內一鍵切換中 / 英文

## 🎮 遊戲玩法

| 模式 | 說明 |
|------|------|
| **經典模式** | 不限時間，挑戰最高分 |
| **限時模式** | 60 秒內衝擊目標分數 |
| **挑戰模式** | 50 步內合成 128 方塊 |

**操作方式**：方向鍵 / WASD / 滑鼠滑動 · `ESC` 暫停

## 🧰 道具系統

- **撤銷**：回退上一步（每局 3 次）
- **清理**：清除一個最小方塊（每局 1 次）
- **復活**：遊戲結束後移除兩個最小方塊繼續對局

## 🏆 其他功能

- 成就系統（6 項成就待解鎖）
- 最高分 / 總局數統計
- 結算頁新紀錄徽章 + 得分滾動動畫
- 音效與背景音樂開關

---

## 🖥️ 執行環境

- Windows 10 / 11
- Python 3.10+
- Pygame 2.6.1

## 🚀 快速開始

### 1. 安裝相依套件

```bash
pip install -r requirements.txt
```

### 2. 執行遊戲

```bash
python src/main.py
```

### 3. 打包為 EXE

```bash
# 一鍵打包（推薦）
python scripts/build_auto.py

# 互動式打包
python scripts/build.py
```

打包完成後，可執行檔位於 `dist/2048/2048.exe`，點兩下即玩，無需安裝 Python 或任何相依套件。詳見 [scripts/README.md](scripts/README.md)。

---

## 📁 專案結構

```
2048/
├── src/                    # 原始碼
│   ├── main.py             # 進入點
│   ├── config.py           # 全域設定（主題 / 動畫 / 輸入）
│   ├── i18n.py             # 多語言（中英）
│   ├── utils.py            # 繪圖助手、快取、動畫曲線
│   ├── models/             # 資料模型（棋盤 / 狀態 / 存檔 / 成就）
│   └── views/              # 檢視層
│       ├── ui_components.py  # UI 元件（按鈕 / 分數卡 / 開關 / 對話框）
│       ├── board_view.py     # 棋盤渲染與動畫
│       ├── effects.py        # 粒子系統與震屏
│       ├── sound_manager.py  # 音效管理
│       └── pages/            # 各頁面（選單 / 遊戲 / 結算 / 設定 / 成就 / 暫停 / 登入）
├── tests/                  # 測試（359 項單元測試 + E2E 使用者模擬）
├── scripts/                # 建置與打包腳本
├── docs/                   # 文件
├── private/                # 私有檔案
├── dist/                   # 打包輸出（.gitignore）
├── build/                  # 建置暫存檔（.gitignore）
└── requirements.txt        # 相依套件清單
```

## 🔧 開發指南

### 執行測試

```bash
# 執行全部單元測試
python -m pytest tests/

# 真實使用者全流程模擬（E2E）
python tests/e2e_user_simulation.py

# 頁面截圖（UI 驗收）
python tests/capture_ui_review.py
```

測試涵蓋：棋盤演算法、遊戲狀態、三種模式完整生命週期、道具、暫停 / 重開、輸入佇列連擊、壓力測試與 60FPS 效能預算。

### 程式碼規範

- **檔案 / 函式命名**：`lower_snake_case` · **類別命名**：`PascalCase` · **縮排**：4 空格 · **行寬**：最大 120 字元
- **Git 提交**：`<type>(<scope>): <subject>`，type 取 `feat / fix / docs / style / refactor / test / chore`

---

## 📜 授權條款

[MIT License](LICENSE) © 2026 MagicSquarekey

## 🤝 貢獻

歡迎提交 Issue 和 Pull Request！

## 📞 聯絡方式

如有問題，請透過 [GitHub Issues](https://github.com/MagicSquarekey/2048/issues) 聯絡。
