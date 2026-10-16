# -*- coding: utf-8 -*-
# @Function: 数据目录重定向 / Data directory redirection
# 仅供测试在运行时将存档目录指向临时目录，避免测试重置玩家真实存档。
# 生产代码请勿调用；config.DATA_DIR / DATA_FILE 保持纯常量路径，
# 使静态安全扫描能正确判定 data_manager 的写入目标。

import os

import src.config as _config


def redirect_data_dir(target_dir: str) -> None:
    """将数据目录重定向到 target_dir / Redirect save directory (test isolation only)"""
    os.makedirs(target_dir, exist_ok=True)
    _config.DATA_DIR = target_dir
    _config.DATA_FILE = os.path.join(target_dir, "game_data.json")
