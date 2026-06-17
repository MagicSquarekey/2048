# /commit — 智能提交

生成规范的 Git commit message 并提交。

## 使用方式

```
/commit                  # 自动分析变更并生成 message
/commit --amend          # 修改上一次的 commit message
```

## Commit 规范

```
<type>(<scope>): <subject>
```

| 类型 | 说明 |
|------|------|
| feat | 新功能 |
| fix | Bug 修复 |
| docs | 文档更新 |
| style | 代码格式 |
| refactor | 重构 |
| test | 测试相关 |
| chore | 构建/工具 |
