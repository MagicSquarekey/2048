# 2048 休闲游戏

> 一款采用「深空霓虹」暗色主题打造的 2048 数字合成游戏，Python + Pygame 驱动，专为 Windows 桌面而生。

**当前版本 / Current Version: [v0.0.1](https://github.com/MagicSquarekey/2048/releases/tag/v0.0.1)** · [English](README.en.md) · [日本語](README.ja.md)

---

## 📖 语言 / Languages

| 语言 (Language) | 文档 (Document) |
|---|---|
| 简体中文 (当前) | [README.md](README.md) |
| English | [README.en.md](README.en.md) |
| 日本語 | [README.ja.md](README.ja.md) |

---

## ✨ 亮点特性

- 🎨 **深空霓虹主题**：深靛蓝渐变背景 + 动态漂移光斑 + 玻璃拟态卡片，方块自带渐变、轮辋光与霓虹辉光
- ⚡ **丝滑操作**：输入队列 + 按住连滑（约每秒 7 步）+ 帧率无关动画，快速连击不丢步
- 💥 **动效特效**：合并粒子爆发、大方块合成震屏、胜利彩带、结束过渡动画、页面淡入淡出
- 🌍 **双语界面**：游戏内一键切换中 / 英文

## 🎮 游戏玩法

| 模式 | 说明 |
|------|------|
| **经典模式** | 不限时间，挑战最高分 |
| **限时模式** | 60 秒内冲击目标分数 |
| **挑战模式** | 50 步内合成 128 方块 |

**操作方式**：方向键 / WASD / 鼠标滑动 · `ESC` 暂停

## 🧰 道具系统

- **撤销**：回退上一步（每局 3 次）
- **清理**：清除一个最小方块（每局 1 次）
- **复活**：游戏结束后移除两个最小方块继续对局

## 🏆 其他功能

- 成就系统（6 项成就待解锁）
- 历史最高分 / 总局数统计
- 结算页新纪录徽章 + 得分滚动动画
- 音效与背景音乐开关

---

## 🖥️ 运行环境

- Windows 10 / 11
- Python 3.10+
- Pygame 2.6.1

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 运行游戏

```bash
python src/main.py
```

### 3. 打包为 EXE

```bash
# 一键打包（推荐）
python scripts/build_auto.py

# 交互式打包
python scripts/build.py
```

打包完成后可执行文件位于 `dist/2048/2048.exe`，双击即玩，无需安装 Python 或任何依赖。详见 [scripts/README.md](scripts/README.md)。

---

## 📁 项目结构

```
2048/
├── src/                    # 源代码
│   ├── main.py             # 入口文件
│   ├── config.py           # 全局配置（主题色 / 动画参数 / 输入参数）
│   ├── i18n.py             # 多语言（中英）
│   ├── utils.py            # 绘图助手、缓存系统、动画曲线
│   ├── models/             # 数据模型（棋盘 / 游戏状态 / 存档 / 成就）
│   └── views/              # 视图层
│       ├── ui_components.py  # UI 组件（按钮 / 分数卡 / 开关 / 弹窗）
│       ├── board_view.py     # 棋盘渲染与动画
│       ├── effects.py        # 粒子系统与震屏
│       ├── sound_manager.py  # 音效管理
│       └── pages/            # 各页面（菜单 / 游戏 / 结算 / 设置 / 成就 / 暂停 / 登录）
├── tests/                  # 测试（359 项单元测试 + E2E 用户模拟）
├── scripts/                # 构建与打包脚本
├── docs/                   # 项目文档
├── private/                # 私有文件
├── dist/                   # 打包输出（.gitignore）
├── build/                  # 构建临时文件（.gitignore）
└── requirements.txt        # 依赖列表
```

## 🔧 开发指南

### 运行测试

```bash
# 运行全部单元测试
python -m pytest tests/

# 真实用户全流程模拟（E2E）
python tests/e2e_user_simulation.py

# 页面截图（UI 验收）
python tests/capture_ui_review.py
```

测试覆盖：棋盘算法、游戏状态、三种模式生命周期、道具、暂停 / 重开、输入队列连击、压力测试与性能预算（60FPS）。

### 代码规范

- **文件 / 函数命名**：小写下划线 · **类名**：大驼峰 · **缩进**：4 空格 · **行宽**：最大 120 字符
- **Git 提交**：`<type>(<scope>): <subject>`，type 取 `feat / fix / docs / style / refactor / test / chore`

---

## 📜 许可证

[MIT License](LICENSE) © 2026 MagicSquarekey

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📞 联系方式

如有问题，请通过 [GitHub Issues](https://github.com/MagicSquarekey/2048/issues) 联系。
