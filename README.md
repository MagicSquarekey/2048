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

### 3. 打包为 EXE（推荐）

```bash
# 方法一：一键打包（推荐）
python scripts/build_auto.py

# 方法二：交互式打包
python scripts/build.py
```

打包完成后，可执行文件位于 `dist/2048/2048.exe`，用户双击即可运行游戏，无需安装Python或任何依赖。

详细打包说明请查看 [scripts/README.md](scripts/README.md)

## 项目结构

```
2048/
├── src/                    # 源代码
│   ├── main.py             # 入口文件
│   ├── config.py           # 全局配置
│   ├── utils.py            # 工具函数
│   ├── models/             # 数据模型
│   ├── views/              # 视图层
│   └── assets/             # 资源文件
├── tests/                  # 测试文件
├── scripts/                # 构建脚本
├── docs/                   # 文档
├── private/                # 私有文件
├── dist/                   # 打包输出（.gitignore）
├── build/                  # 构建临时文件（.gitignore）
├── .gitignore              # Git配置
├── README.md               # 项目说明
├── requirements.txt        # 依赖列表
└── CLAUDE.md               # AI协作说明
```

## 开发指南

### 运行测试
```bash
# 运行所有测试
python -m pytest tests/

# 运行特定测试
python -m pytest tests/test_board.py
```

### 代码规范
- 文件命名：全小写 + 下划线
- 类名：大驼峰（MyClass）
- 函数名：小写下划线（my_function）
- 缩进：4个空格

### Git提交
```bash
# 查看状态
git status

# 添加文件
git add src/

# 提交
git commit -m "feat: 添加新功能"
```

## 分发指南

### 打包结果
打包后生成 `dist/2048/` 文件夹，包含：
- `2048.exe` - 游戏主程序（约6MB）
- `_internal/` - 依赖文件

### 分发方式
1. **直接分发**：将 `dist/2048/` 文件夹压缩为ZIP发送
2. **U盘分发**：将文件夹复制到U盘
3. **网盘分发**：上传到网盘供下载

### 系统要求
- Windows 7/8/10/11
- 无需安装Python
- 任何现代电脑都能运行

## 常见问题

### Q: 游戏无法运行？
A: 检查以下几点：
1. 确保 `2048.exe` 和 `_internal/` 在同一文件夹
2. 不要分离文件
3. 尝试以管理员身份运行

### Q: 如何更新游戏？
A: 只需替换新的 `dist/2048/` 文件夹即可

### Q: 能否在Mac/Linux上运行？
A: 当前版本仅支持Windows，需要重新打包

## 技术支持

如遇到问题，请：
1. 查看 [scripts/README.md](scripts/README.md) 打包说明
2. 查看 `docs/` 目录下的文档
3. 联系开发者

## 许可证

MIT License

---
*最后更新：2026-06-22*