# AI 项目模板 / AI Project Template

🤖 一个通用的 AI 辅助开发项目起点 / A universal template for AI-assisted development

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

---

## 🚀 快速开始 / Quick Start

```bash
# 1. 复制模板 / Copy template
# 直接复制 AI-XiangMuMoBan 文件夹，重命名为你的项目名

# 2. 进入项目 / Enter project
cd 你的项目名

# 3. 安装依赖 / Install dependencies
pip install -r requirements.txt
```

---

## 📁 目录结构 / Directory Structure

```
AI-XiangMuMoBan/
├── .claude/           # Claude 配置（自动生效）
│   ├── commands/      # 快捷命令
│   └── skills/        # 技能定义
├── private/           # 私有文件（不上传 GitHub）
├── .gitignore         # Git 忽略规则
├── CLAUDE.md          # AI 指令
├── README.md          # 项目说明（本文件）
└── requirements.txt   # Python 依赖
```

---

## 🎯 快捷命令 / Quick Commands

在 Claude Code 中使用这些命令：

| 命令 | 用途 | Command |
|------|------|---------|
| `/plan` | 任务规划 | Task planning |
| `/review` | 代码审查 | Code review |
| `/fix` | 修复问题 | Bug fixing |
| `/commit` | 提交代码 | Smart commit |
| `/docs` | 文档同步 | Document sync |
| `/status` | 查看状态 | Project status |

---

## 📖 使用方法 / Usage

### 创建新项目

1. 复制 `AI-XiangMuMoBan` 文件夹
2. 重命名为你的项目名
3. 进入项目目录，开始开发

### 开始开发

```bash
cd 你的项目名
pip install -r requirements.txt

# 开始使用 Claude Code 开发
# 输入 /plan 开始任务规划
```

---

## 🔒 安全规范 / Security

### 绝对禁止 / Never Do

- ❌ 不得提交 API Key、密码、密钥
- ❌ 不得提交 .env 文件
- ❌ 不得在代码中硬编码任何凭证

### 发现安全问题时 / When发现安全问题

1. 立即停止提交
2. 告知用户
3. 清理 Git 历史（如已提交）

---

## 📚 更多信息 / More Info

- [CLAUDE.md](CLAUDE.md) - AI 指令 / AI Instructions

---

## 📄 许可证 / License

MIT License

---

*最后更新 / Last Updated: 2026-06-17*
*维护者 / Maintainer: AI 协作开发团队*
