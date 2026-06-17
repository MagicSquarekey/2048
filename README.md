# 2048 休闲游戏

一个经典的 2048 数字合成游戏，使用 Python + Pygame 开发，运行于 Windows 桌面。

## 游戏特性

### 核心玩法
- **经典模式**: 无限时间，自由游玩
- **挑战模式**: 限定步数内合成目标方块
- **计时模式**: 在时间限制内尽可能合成大方块

### 道具系统
- **撤销**: 撤回上一步操作
- **清除**: 移除棋盘上随机一个方块
- **复活**: 游戏结束后可使用道具继续

### 社交功能
- **排行榜**: 记录历史最佳成绩
- **成就系统**: 解锁各种游戏成就
- **分享功能**: 分享游戏成绩

### 音效设置
- 可开关游戏音效
- 可开关背景音乐

## 运行环境

- Windows 10/11
- Python 3.10+
- Pygame 2.6+

## 快速开始

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
pip install pyinstaller
pyinstaller --onefile --windowed --name "2048 Game" src/main.py
```

## 项目结构

```
2048/
├── src/
│   ├── main.py              # 入口文件
│   ├── config.py             # 全局配置
│   ├── utils.py              # 工具函数
│   ├── models/               # 数据模型
│   │   ├── board.py          # 棋盘逻辑
│   │   ├── tile.py           # 方块类
│   │   ├── game_state.py     # 游戏状态
│   │   ├── data_manager.py   # 数据管理
│   │   ├── ad_manager.py     # 广告管理
│   │   └── achievements.py   # 成就系统
│   ├── views/                # 视图层
│   │   ├── board_view.py     # 棋盘渲染
│   │   ├── ui_components.py  # UI 组件
│   │   ├── sound_manager.py  # 音效管理
│   │   └── pages/            # 页面
│   └── assets/               # 资源文件
├── tests/                    # 测试文件
├── requirements.txt          # 依赖列表
├── build.py                  # 打包脚本
└── README.md
```

## 游戏操作

- **方向键 / WASD**: 移动方块
- **滑动**: 在棋盘上滑动移动方块
- **P**: 暂停游戏
- **ESC**: 返回主菜单

## 数据存储

游戏数据存储在用户目录下:

```
%LOCALAPPDATA%\2048_Game\
├── game_data.json    # 主数据文件
└── game_data.json.bak  # 自动备份
```

## 开发说明

### 代码规范
- Python 文件头部: `# -*- coding: utf-8 -*-`
- 类名: 大驼峰 (PascalCase)
- 函数名: 小写下划线 (snake_case)
- 常量: 全大写 (UPPER_SNAKE)

### 测试
```bash
python -m pytest tests/ -v
```

## 许可证

MIT License

## 更新日志

### v1.0.0 (2026-06-17)
- 初始发布
- 支持经典/挑战/计时三种游戏模式
- 实现道具系统（撤销/清除/复活）
- 音效与背景音乐支持
- 成就系统
- 数据备份与恢复
- 本地广告管理（免费模式）

## 作者

AI 协作开发团队

---

**享受游戏！**
