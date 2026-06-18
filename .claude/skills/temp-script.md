# 临时脚本管理

> 运行临时测试脚本并在完成后自动删除

## 触发条件
- 用户说"运行临时脚本"
- 用户说"测试脚本"
- 用户说"临时测试"
- 用户提到 `_` 开头的 Python 文件

## 执行步骤

### 1. 识别临时脚本
临时脚本的特征：
- 文件名以 `_` 开头（如 `_check.py`, `_fix.py`, `_patch.py`）
- 位于项目根目录
- 不是正式的测试文件（不在 `tests/` 目录）

### 2. 运行脚本
```bash
python <script_name>.py
```

### 3. 记录输出
- 保存脚本输出到 `private/logs/` 目录
- 文件名格式：`<script_name>_<timestamp>.log`

### 4. 删除脚本
```bash
rm <script_name>.py
```

### 5. 确认结果
向用户报告：
- 脚本执行状态（成功/失败）
- 输出摘要
- 脚本已删除确认

## 示例

用户：运行 `_check_i18n.py`

AI：
1. 执行 `python _check_i18n.py`
2. 保存输出到 `private/logs/check_i18n_20260617.log`
3. 删除 `_check_i18n.py`
4. 报告结果

## 注意事项

- 如果脚本执行失败，**不要删除**，保留供调试
- 所有日志保存在 `private/logs/`（已在 .gitignore 中）
- 长期使用的脚本应移动到 `private/scripts/`
