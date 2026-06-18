# Bilingual Comments Skill / 中英文注释技能

> 为所有文件、代码、文档添加中英文注释
> Add bilingual (Chinese/English) comments to all files, code, and documentation

## 触发条件 / Trigger Conditions

当用户说以下关键词时触发：
- "添加注释" / "add comments"
- "中英文注释" / "bilingual comments"
- "翻译注释" / "translate comments"
- "国际化注释" / "internationalize comments"

## 功能 / Features

1. **代码注释** / Code Comments
   - 函数 docstring：中英文双语
   - 行内注释：关键逻辑添加中英文说明
   - 文件头部：保留原有格式，补充英文说明

2. **文档注释** / Documentation Comments
   - Markdown 文件：标题和段落中英文并列
   - 配置文件：添加中英文说明注释
   - README：保持中英文对照格式

3. **注释格式** / Comment Format

   **Python 文件：**
   ```python
   # -*- coding: utf-8 -*-
   # @Function: 项目配置管理 / Project configuration management

   def load_config(config_path: str) -> dict:
       """
       加载配置文件 / Load configuration file

       Args:
           config_path: 配置文件路径 / Path to configuration file

       Returns:
           配置字典 / Configuration dictionary
       """
       pass
   ```

   **Markdown 文件：**
   ```markdown
   ## 📁 目录结构 / Directory Structure

   项目的主要目录说明：
   Main directory descriptions:
   ```

   **配置文件：**
   ```yaml
   # 数据库配置 / Database configuration
   database:
     host: localhost  # 主机地址 / Host address
     port: 3306       # 端口号 / Port number
   ```

## 执行流程 / Execution Flow

1. **分析文件类型** / Analyze file type
   - 识别文件扩展名和内容格式
   - 确定适用的注释风格

2. **检查现有注释** / Check existing comments
   - 识别已有的中英文注释
   - 避免重复添加

3. **添加注释** / Add comments
   - 保持原有代码结构不变
   - 在适当位置添加中英文注释
   - 确保注释简洁明了

4. **验证结果** / Verify results
   - 检查注释格式一致性
   - 确保代码功能不受影响

## 注释规范 / Comment Standards

### 代码注释原则
- **简洁性** / Concise：注释应简短有力
- **准确性** / Accurate：翻译准确，不产生歧义
- **必要性** / Necessary：只注释关键逻辑，避免过度注释
- **一致性** / Consistent：同一项目使用统一风格

### 中英文对照规则
- 中文在前，英文在后
- 使用 `/` 或 `|` 分隔
- 保持相同的技术术语翻译

### 示例对照表

| 中文 | English |
|------|---------|
| 配置 | Configuration |
| 初始化 | Initialize |
| 加载 | Load |
| 保存 | Save |
| 删除 | Delete |
| 查询 | Query |
| 更新 | Update |
| 验证 | Validate |
| 处理 | Process |
| 返回 | Return |

## 使用示例 / Usage Examples

### 示例 1：为 Python 文件添加注释
```
用户：为 config.py 添加中英文注释
AI：分析文件 → 添加函数 docstring → 添加行内注释 → 返回结果
```

### 示例 2：为 Markdown 文件添加注释
```
用户：为 README.md 添加中英文注释
AI：检查现有格式 → 补充缺失的英文翻译 → 保持格式一致
```

### 示例 3：批量添加注释
```
用户：为所有 Python 文件添加中英文注释
AI：扫描所有 .py 文件 → 逐个处理 → 汇总报告
```

## 注意事项 / Notes

1. **保留原有注释** / Preserve existing comments
   - 不删除已有的注释
   - 只补充缺失的翻译

2. **代码优先** / Code first
   - 注释不应影响代码可读性
   - 避免在简单代码上添加过多注释

3. **技术术语** / Technical terms
   - 保持技术术语的一致性
   - 使用业界通用翻译

4. **格式规范** / Format standards
   - 遵循项目的代码规范
   - Python: PEP 8
   - Markdown: CommonMark

---

*最后更新 / Last Updated: 2026-06-17*
