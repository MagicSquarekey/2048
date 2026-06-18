# Human Escalation Skill / 人工介入技能

> 多次尝试失败后，自动请求人工介入
> Automatically request human intervention after multiple failed attempts

## 触发条件 / Trigger Conditions

当满足以下任一条件时触发：
Triggered when any of the following conditions are met:

1. **连续失败次数** — 同一问题连续修复失败 ≥ 3 次
   Consecutive failures — Same issue fails ≥ 3 times in a row
2. **错误循环** — 修复一个问题导致另一个问题出现，循环 ≥ 2 次
   Error loop — Fixing one issue causes another, looping ≥ 2 times
3. **超时未解决** — 同一问题持续未解决超过 10 分钟
   Timeout — Same issue remains unresolved for > 10 minutes
4. **不确定的修复** — 对修复方案信心不足（需要猜测）
   Uncertain fix — Low confidence in fix (requires guessing)

## 功能 / Features

- 自动检测失败模式
- Automatically detect failure patterns
- 清晰展示已尝试的方案
- Clearly display attempted solutions
- 提供问题摘要供人工决策
- Provide problem summary for human decision

## 执行流程 / Execution Flow

1. **记录尝试** — 记录每次修复尝试
   Record attempts — Log each fix attempt
2. **检测阈值** — 判断是否达到介入条件
   Detect threshold — Check if intervention threshold is reached
3. **生成摘要** — 汇总问题和已尝试方案
   Generate summary — Summarize problem and attempted solutions
4. **请求介入** — 明确提示需要人工帮助
   Request intervention — Clearly prompt for human help
5. **等待指示** — 暂停自动修复，等待人工指令
   Wait for instructions — Pause auto-fix, await human guidance

## 输出格式 / Output Format

当触发人工介入时，输出以下内容：
When human escalation is triggered, output the following:

```
🚨 需要人工介入 / Human Intervention Required

📋 问题描述 / Problem Description:
[具体问题 / Specific issue]

🔄 已尝试方案 / Attempted Solutions:
1. [方案1] → 结果：失败 / Solution 1 → Result: Failed
2. [方案2] → 结果：失败 / Solution 2 → Result: Failed
3. [方案3] → 结果：失败 / Solution 3 → Result: Failed

❓ 可能原因 / Possible Causes:
- [原因1 / Cause 1]
- [原因2 / Cause 2]

💡 建议 / Suggestions:
- [建议1 / Suggestion 1]
- [建议2 / Suggestion 2]

⏸️ 等待您的指示... / Waiting for your instructions...
```

## 人工介入后的处理 / Post-Intervention Handling

收到人工指示后：
After receiving human instructions:

1. 记录人工提供的解决方案
   Record human-provided solution
2. 执行修复
   Execute fix
3. 验证结果
   Verify result
4. 更新知识库（如果适用）
   Update knowledge base (if applicable)

## 禁止行为 / Prohibited Actions

- ❌ 无限重试同一方案
  Infinite retry of same solution
- ❌ 跳过人工介入直接应用不确定的修复
  Skip intervention and apply uncertain fixes
- ❌ 隐藏失败信息
  Hide failure information
