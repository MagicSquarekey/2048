# -*- coding: utf-8 -*-
# pytest 收集配置
# 1) test_full_flow.py 是独立运行脚本（模块级顺序执行 + sys.exit），
#    不适合被 pytest 导入收集，全量收集时需排除。
# 2) 将玩家数据目录重定向到临时目录，避免测试重置真实玩家数据
#    （config.py 读取 GAME_2048_DATA_DIR 环境变量；conftest 先于测试模块导入执行）。

import os
import tempfile

collect_ignore = ["test_full_flow.py"]

os.environ.setdefault(
    "GAME_2048_DATA_DIR",
    os.path.join(tempfile.gettempdir(), "2048_game_test_data"),
)
