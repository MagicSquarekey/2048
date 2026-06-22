# 构建脚本说明

本目录包含2048游戏的构建和打包脚本。

## 📁 文件说明

| 文件 | 说明 |
|------|------|
| `build.py` | 交互式打包脚本（推荐） |
| `build_auto.py` | 自动化打包脚本（无需交互） |
| `build.spec` | PyInstaller配置文件 |

## 🚀 使用方法

### 方法一：一键打包（推荐）

```bash
# 在项目根目录执行
python scripts/build_auto.py
```

### 方法二：交互式打包

```bash
# 在项目根目录执行
python scripts/build.py
```

### 方法三：使用PyInstaller命令行

```bash
# 在项目根目录执行
pyinstaller --clean scripts/build.spec
```

## 📦 打包结果

打包完成后，可执行文件位于：
```
dist/2048/
├── 2048.exe          # 游戏主程序
└── _internal/        # 依赖文件
```

## 📋 分发方式

1. 将 `dist/2048/` 整个文件夹复制给用户
2. 用户双击 `2048.exe` 即可运行游戏
3. 无需安装Python或任何依赖

## ⚠️ 注意事项

- 打包前确保已安装依赖：`pip install -r requirements.txt`
- 打包后的文件夹需要完整复制，不要分离文件
- 仅支持Windows系统