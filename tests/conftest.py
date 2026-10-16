# -*- coding: utf-8 -*-
# pytest 收集配置（仅收集期生效，不影响游戏运行）
# 1) test_full_flow.py 是独立运行脚本（模块级顺序执行 + sys.exit），
#    不适合被 pytest 导入收集，全量收集时排除。
# 2) 将存档目录重定向到临时目录，避免测试重置玩家真实存档。
#    重定向通过 src.data_paths.redirect_data_dir() 在运行时完成
#    （config.DATA_DIR 保持纯常量，静态安全扫描可正确判定写入目标）。

import os
import tempfile

collect_ignore = ["test_full_flow.py"]

# 在导入任何 src 模块之前重定向，确保 config 导入时即生效
from src.data_paths import redirect_data_dir  # noqa: E402

redirect_data_dir(os.path.join(tempfile.gettempdir(), "2048_game_test_data"))
