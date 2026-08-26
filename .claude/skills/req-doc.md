# 需求文档管理 / Requirement Document Management

> 自动维护项目需求文档，记录已完成和规划中的功能，确保每次开发都有据可依
> Auto-maintain project requirement document, tracking completed and planned features

## 触发条件 / Trigger Conditions

### 自动触发 / Auto Trigger
- 每次新对话开始时，检查并更新需求文档 / Check and update at conversation start
- 完成任何功能开发后，更新需求文档 / Update after feature development
- 用户讨论新功能需求时，更新需求文档 / Update when discussing new features

### 手动触发 / Manual Trigger
- 用户说"更新需求文档" / User says "update requirement document"
- 用户说"查看需求" / User says "view requirements"
- 用户说"需求状态" / User says "requirement status"
- 用户说 `/req` 或 `/requirement`

## 文档路径 / Document Path

```
docs/REQUIREMENTS.md
```

## 执行步骤 / Execution Steps

### 1. 对话开始时 / At Conversation Start

1. 读取 `docs/REQUIREMENTS.md`
2. 向用户简要汇报当前项目状态
3. 询问本次对话目标

### 2. 讨论新功能时 / When Discussing New Features

当用户提到新功能或需求时：

1. **记录需求 / Record Requirement**
   - 功能名称 / Feature name
   - 功能描述 / Description
   - 优先级评估 / Priority assessment
   - 预估工作量 / Estimated effort

2. **更新文档 / Update Document**
   - 添加到"未来规划"部分 / Add to "Future Plans" section
   - 更新变更历史 / Update change history

3. **确认理解 / Confirm Understanding**
   - 向用户复述需求 / Restate requirement to user
   - 确认是否遗漏 / Confirm no omissions

### 3. 完成开发后 / After Development Complete

1. 将功能从"进行中"移动到"已完成功能" / Move from "In Progress" to "Completed"
2. 记录完成日期、相关文件、使用方式 / Record date, files, usage
3. 更新变更历史 / Update change history
4. 检查是否有新的技术债务 / Check for new technical debt

### 4. 对话结束时 / At Conversation End

- 更新需求文档的最后更新时间 / Update last-updated time
- 总结本次对话的变更 / Summarize conversation changes
- 提醒用户下次可以继续的任务 / Remind user of next tasks

## 文档结构模板 / Document Template

```markdown
# 项目需求文档 / Project Requirements Document

> **最后更新 / Last Updated**: YYYY-MM-DD
> **文档版本 / Document Version**: v1.0.0

## 项目概述 / Project Overview
- 项目名称 / Project name
- 项目目标 / Project goal
- 技术栈 / Tech stack

## 已完成功能 / Completed Features

### [功能名称] - YYYY-MM-DD
- **描述 / Description**: xxx
- **相关文件 / Related Files**: xxx
- **使用方式 / Usage**: xxx

## 进行中 / In Progress

### [功能名称]
- **开始日期 / Start Date**: YYYY-MM-DD
- **预计完成 / Expected Completion**: YYYY-MM-DD
- **进度 / Progress**: 60%
- **当前状态 / Current Status**: xxx

## 未来规划 / Future Plans

### [功能名称]
- **优先级 / Priority**: 🔴 高 / 🟡 中 / 🟢 低
- **预估工作量 / Estimated Effort**: X 天
- **描述 / Description**: xxx
- **依赖 / Dependencies**: xxx

## 技术债务 / Technical Debt

### [问题描述]
- **严重程度 / Severity**: 高/中/低
- **影响范围 / Impact**: xxx
- **建议修复方案 / Suggested Fix**: xxx

## 变更历史 / Change History

| 日期 / Date | 变更内容 / Change | 原因 / Reason |
|-------------|-------------------|---------------|
| YYYY-MM-DD | xxx | xxx |
```

## 快捷命令 / Quick Commands

| 命令 / Command | 功能 / Purpose |
|----------------|----------------|
| `/req` | 显示需求文档摘要 / Show requirement summary |
| `/req add <功能>` | 快速添加新需求 / Quick add new requirement |
| `/req status` | 显示所有功能状态 / Show all feature status |
| `/req done <功能>` | 标记功能为已完成 / Mark feature as completed |

## 文档更新规则 / Update Rules

### 实时更新 / Real-time Update
- 每次代码变更后，立即更新相关功能状态 / Update status after code changes
- 新增文件时，更新相关功能的文件列表 / Update file list when adding files
- 删除文件时，从功能描述中移除 / Remove from description when deleting files

### 状态流转 / Status Flow
```
规划中 → 进行中 → 已完成
Planned → In Progress → Completed
    ↓
  已取消（如果放弃）
  Cancelled (if abandoned)
```

### 优先级标准 / Priority Standards

| 优先级 / Priority | 标准 / Criteria |
|-------------------|-----------------|
| 🔴 高 / High | 核心功能、阻塞性问题、安全相关 / Core features, blockers, security |
| 🟡 中 / Medium | 重要但非紧急、性能优化 / Important but not urgent, performance |
| 🟢 低 / Low | 锦上添花、未来扩展 / Nice-to-have, future expansion |

## 与其他 Skill 的协作 / Skill Collaboration

### 与 requirement-confirm 协作
- 确认需求时，自动检查需求文档中是否已有类似功能 / Check for existing similar features
- 避免重复开发 / Avoid duplicate development

### 与 auto-review 协作
- 代码审查时，验证是否符合需求文档描述 / Verify compliance with requirements
- 检查是否有遗漏的功能点 / Check for missing features

### 与 doc-gen 协作
- 需求文档中的"使用方式"可同步到 API 文档 / Sync usage to API docs
- 保持文档一致性 / Maintain documentation consistency

## 示例 / Examples

### 示例1：新对话开始 / Example 1: Conversation Start
```
AI:
📋 项目需求状态 / Project Status:
- 已完成 / Completed: 5 个功能 / features
- 进行中 / In Progress: 1 个功能（用户认证 70%）/ 1 feature (auth 70%)
- 规划中 / Planned: 3 个功能 / features

请问这次需要我帮你做什么？
What do you need help with?
```

### 示例2：讨论新功能 / Example 2: New Feature Discussion
```
用户：我想添加数据导出功能
User: I want to add data export feature

AI：
好的，我来记录这个需求：

📝 新增规划功能 / New Planned Feature:
- **功能名称 / Name**: 数据导出 / Data Export
- **优先级 / Priority**: 🟡 中 / Medium
- **描述 / Description**: 支持将数据导出为 CSV/Excel 格式 / Export to CSV/Excel
- **预估工作量 / Effort**: 2 天 / days

已更新到 docs/REQUIREMENTS.md
需要我现在开始设计技术方案吗？
```

### 示例3：功能完成 / Example 3: Feature Complete
```
用户：登录功能开发完成了
User: Login feature is complete

AI：
太好了！我来更新需求文档：

✅ 功能状态更新 / Status Update:
- 用户认证 / User Auth: 进行中 → 已完成 / In Progress → Completed
- 完成日期 / Completed: 2026-07-09
- 相关文件 / Related Files:
  - src/auth/login.py
  - src/auth/register.py
  - tests/test_auth.py

docs/REQUIREMENTS.md 已更新
```

## 注意事项 / Notes

1. **文档必须存在**：如果 `docs/REQUIREMENTS.md` 不存在，自动创建 / Auto-create if not exists
2. **保持同步**：代码变更必须同步更新文档 / Code changes must sync with docs
3. **不要臆测**：只记录用户明确确认的需求 / Only record explicitly confirmed requirements
4. **及时清理**：已取消的功能移至"技术债务"部分 / Move cancelled features to technical debt
5. **版本标记**：重要变更时更新文档头部的版本号 / Update version on important changes
6. **使用双语**：保持中英文双语格式 / Maintain bilingual format

---

*最后更新 / Last Updated: 2026-07-09*
*维护者 / Maintainer: AI 协作开发团队 / AI Collaboration Development Team*