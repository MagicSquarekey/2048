# 2048 休闲游戏 / 2048 Casual Game

一个经典的 2048 数字合成游戏，使用 Python + Pygame 开发，运行于 Windows 桌面。

A classic 2048 number merging game developed with Python + Pygame, running on Windows desktop.

---

## 🎮 游戏特性 / Game Features

### 核心玩法 / Core Gameplay
- **经典模式**: 无限时间，自由游玩
- **挑战模式**: 限定步数内合成目标方块
- **计时模式**: 在时间限制内尽可能合成大方块

- **Classic Mode**: Unlimited time, free play
- **Challenge Mode**: Merge target tiles within limited steps
- **Time Mode**: Merge as many tiles as possible within time limit

### 道具系统 / Power-ups System
- **撤销**: 撤回上一步操作
- **清除**: 移除棋盘上随机一个方块
- **复活**: 游戏结束后可使用道具继续

- **Undo**: Reverse the last move
- **Clear**: Remove a random tile from the board
- **Revive**: Continue playing after game over using power-ups

### 社交功能 / Social Features
- **排行榜**: 记录历史最佳成绩
- **成就系统**: 解锁各种游戏成就
- **分享功能**: 分享游戏成绩

- **Leaderboard**: Record historical best scores
- **Achievement System**: Unlock various game achievements
- **Share Function**: Share game scores

### 音效设置 / Audio Settings
- 可开关游戏音效
- 可开关背景音乐

- Toggle game sound effects
- Toggle background music

---

## 🖥️ 运行环境 / System Requirements

- Windows 10/11
- Python 3.10+
- Pygame 2.6+

---

## 🚀 快速开始 / Quick Start

### 1. 安装依赖 / Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. 运行游戏 / Run the Game

```bash
python src/main.py
```

### 3. 打包为 EXE（推荐）/ Package as EXE (Recommended)

```bash
# 方法一：一键打包（推荐）/ Method 1: One-click packaging (Recommended)
python scripts/build_auto.py

# 方法二：交互式打包 / Method 2: Interactive packaging
python scripts/build.py
```

打包完成后，可执行文件位于 `dist/2048/2048.exe`，用户双击即可运行游戏，无需安装 Python 或任何依赖。

After packaging, the executable file is located at `dist/2048/2048.exe`. Users can double-click to run the game without installing Python or any dependencies.

详细打包说明请查看 [scripts/README.md](scripts/README.md)

For detailed packaging instructions, see [scripts/README.md](scripts/README.md)

---

## 📁 项目结构 / Project Structure

```
2048/
├── src/                    # 源代码 / Source code
│   ├── main.py             # 入口文件 / Entry point
│   ├── config.py           # 全局配置 / Global configuration
│   ├── utils.py            # 工具函数 / Utility functions
│   ├── models/             # 数据模型 / Data models
│   ├── views/              # 视图层 / View layer
│   └── assets/             # 资源文件 / Asset files
├── tests/                  # 测试文件 / Test files
├── scripts/                # 构建脚本 / Build scripts
├── docs/                   # 文档 / Documentation
├── private/                # 私有文件 / Private files
├── dist/                   # 打包输出（.gitignore）/ Package output (.gitignore)
├── build/                  # 构建临时文件（.gitignore）/ Build temporary files (.gitignore)
├── .gitignore              # Git配置 / Git configuration
├── README.md               # 项目说明 / Project description
├── requirements.txt        # 依赖列表 / Dependency list
└── CLAUDE.md               # AI协作说明 / AI collaboration guide
```

---

## 🔧 开发指南 / Development Guide

### 运行测试 / Run Tests

```bash
# 运行所有测试 / Run all tests
python -m pytest tests/

# 运行特定测试 / Run specific tests
python -m pytest tests/test_board.py
```

### 代码规范 / Code Standards

- **文件命名**: 全小写 + 下划线 (File naming: lowercase with underscores)
- **函数命名**: 小写下划线 (Function naming: lowercase with underscores)
- **类名**: 大驼峰 (Class names: PascalCase)
- **缩进**: 4 个空格 (Indentation: 4 spaces)
- **行宽**: 最大 120 字符 (Line width: max 120 characters)

### Git 提交规范 / Git Commit Convention

```
<type>(<scope>): <subject>
```

| 类型 (Type) | 说明 (Description) | 示例 (Example) |
|-------------|-------------------|----------------|
| feat | 新功能 (New feature) | `feat(auth): 添加登录功能` |
| fix | Bug 修复 (Bug fix) | `fix(api): 修复超时问题` |
| docs | 文档更新 (Documentation) | `docs: 更新 README` |
| style | 代码格式 (Code style) | `style: 统一缩进` |
| refactor | 重构 (Refactoring) | `refactor(core): 提取基类` |
| test | 测试相关 (Testing) | `test: 添加登录测试` |
| chore | 构建/工具 (Build/tools) | `chore: 更新依赖` |

---

## 📜 许可证 / License

MIT License - 详见 [LICENSE](LICENSE) 文件

MIT License - See [LICENSE](LICENSE) file for details

---

## 🤝 贡献 / Contributing

欢迎提交 Issue 和 Pull Request！

Issues and Pull Requests are welcome!

---

## 📞 联系方式 / Contact

如有问题，请通过 GitHub Issues 联系。

For any questions, please contact via GitHub Issues.