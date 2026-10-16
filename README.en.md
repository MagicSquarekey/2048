# 2048 Casual Game

> A 2048 number-merging game with a "deep-space neon" dark theme, powered by Python + Pygame, built for Windows desktop.

**Current Version: [v0.0.1](https://github.com/MagicSquarekey/2048/releases/tag/v0.0.1)** · [简体中文](README.md) · [日本語](README.ja.md)

---

## 📖 Languages

| Language | Document |
|---|---|
| 简体中文 | [README.md](README.md) |
| English (current) | [README.en.md](README.en.md) |
| 日本語 | [README.ja.md](README.ja.md) |

---

## ✨ Highlights

- 🎨 **Deep-space neon theme**: indigo gradient background with drifting glows, glassmorphic cards, and tiles with gradients, rim light and neon glow
- ⚡ **Buttery-smooth controls**: input queue + hold-to-repeat sliding (~7 moves/sec) + frame-rate-independent animations — rapid combos never drop input
- 💥 **Motion & effects**: merge particle bursts, screen shake on big merges, victory confetti, animated game-over transition, page fades
- 🌍 **Bilingual UI**: switch between Chinese and English in-game

## 🎮 Game Modes

| Mode | Description |
|------|-------------|
| **Classic** | No time limit — chase your best score |
| **Timed** | Hit the target score within 60 seconds |
| **Challenge** | Reach the 128 tile within 50 moves |

**Controls**: Arrow keys / WASD / mouse swipe · `ESC` to pause

## 🧰 Power-ups

- **Undo**: revert the last move (3 per game)
- **Clear**: remove one smallest tile (1 per game)
- **Revive**: after game over, clear two smallest tiles and keep playing

## 🏆 Other Features

- Achievement system (6 achievements to unlock)
- Best score / total games tracking
- New-record badge + score roll-up animation on the result page
- Sound effects and background music toggles

---

## 🖥️ System Requirements

- Windows 10 / 11
- Python 3.10+
- Pygame 2.6.1

## 🚀 Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the game

```bash
python src/main.py
```

### 3. Package as EXE

```bash
# One-click build (recommended)
python scripts/build_auto.py

# Interactive build
python scripts/build.py
```

The executable lands at `dist/2048/2048.exe` — double-click to play, no Python or dependencies required. See [scripts/README.md](scripts/README.md) for details.

---

## 📁 Project Structure

```
2048/
├── src/                    # Source code
│   ├── main.py             # Entry point
│   ├── config.py           # Global config (theme / animation / input)
│   ├── i18n.py             # Localization (Chinese & English)
│   ├── utils.py            # Drawing helpers, caches, animation curves
│   ├── models/             # Data models (board / state / save / achievements)
│   └── views/              # View layer
│       ├── ui_components.py  # UI components (buttons / score cards / switches / alerts)
│       ├── board_view.py     # Board rendering & animation
│       ├── effects.py        # Particle system & screen shake
│       ├── sound_manager.py  # Sound management
│       └── pages/            # Pages (menu / game / result / settings / awards / pause / login)
├── tests/                  # Tests (359 unit tests + E2E user simulation)
├── scripts/                # Build & packaging scripts
├── docs/                   # Documentation
├── private/                # Private files
├── dist/                   # Build output (.gitignore)
├── build/                  # Build temp files (.gitignore)
└── requirements.txt        # Dependency list
```

## 🔧 Development Guide

### Run tests

```bash
# All unit tests
python -m pytest tests/

# End-to-end user simulation
python tests/e2e_user_simulation.py

# Capture UI screenshots
python tests/capture_ui_review.py
```

Coverage: board algorithm, game state, full lifecycles of all three modes, power-ups, pause/restart, input-queue combos, stress testing and a 60FPS performance budget.

### Code Standards

- **File / function naming**: `lower_snake_case` · **Class naming**: `PascalCase` · **Indentation**: 4 spaces · **Line width**: max 120 chars
- **Git commits**: `<type>(<scope>): <subject>` with `feat / fix / docs / style / refactor / test / chore`

---

## 📜 License

[MIT License](LICENSE) © 2026 MagicSquarekey

## 🤝 Contributing

Issues and Pull Requests are welcome!

## 📞 Contact

Questions? Reach out via [GitHub Issues](https://github.com/MagicSquarekey/2048/issues).
